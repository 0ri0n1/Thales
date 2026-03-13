#!/usr/bin/env python3
"""
dnSpy MCP Server — .NET Assembly Decompiler & Analyzer
=======================================================
Wraps dnSpy.Console.exe for decompilation and uses dnfile/pefile
for in-process .NET metadata inspection.

Tools:
  Decompilation (CLI subprocess):
    dnspy_decompile_assembly  — Full project decompilation to C#
    dnspy_decompile_type      — Decompile a single type by name
    dnspy_decompile_token     — Decompile by metadata token

  Metadata Inspection (in-process):
    dnspy_list_types          — List all types in an assembly
    dnspy_list_methods        — List methods of a type
    dnspy_get_metadata        — PE headers, CLR version, entry point
    dnspy_get_references      — Assembly references and dependencies
    dnspy_search_strings      — Find string literals
    dnspy_get_resources       — List embedded managed resources
    dnspy_get_assembly_info   — Name, version, culture, public key

Environment:
  DNSPY_PATH    Path to dnSpy installation directory (required)
                e.g. E:\\Thales\\Thon\\tools\\dnSpy-net-win64
"""

import os
import sys
import json
import glob
import shutil
import struct
import logging
import asyncio
import tempfile
from pathlib import Path
from typing import Any, Optional

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DNSPY_PATH = os.getenv("DNSPY_PATH", "")
DNSPY_CONSOLE = ""

if DNSPY_PATH:
    _candidate = os.path.join(DNSPY_PATH, "dnSpy.Console.exe")
    if os.path.isfile(_candidate):
        DNSPY_CONSOLE = _candidate
    else:
        logging.basicConfig(level=logging.WARNING, stream=sys.stderr)
        logging.getLogger("dnspy-mcp").warning(
            f"dnSpy.Console.exe not found at {_candidate}"
        )
else:
    logging.basicConfig(level=logging.WARNING, stream=sys.stderr)
    logging.getLogger("dnspy-mcp").warning(
        "DNSPY_PATH not set. Decompilation tools will be unavailable."
    )

logging.basicConfig(
    level=logging.INFO, stream=sys.stderr,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("dnspy-mcp")

# ---------------------------------------------------------------------------
# Lazy imports for dnfile/pefile (heavy libraries)
# ---------------------------------------------------------------------------

_dnfile = None
_pefile = None


def _get_dnfile():
    global _dnfile
    if _dnfile is None:
        import dnfile as _mod
        _dnfile = _mod
    return _dnfile


def _get_pefile():
    global _pefile
    if _pefile is None:
        import pefile as _mod
        _pefile = _mod
    return _pefile


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _j(obj: Any) -> str:
    return json.dumps(obj, indent=2, default=str)


def _validate_assembly(path: str) -> Optional[str]:
    """Validate the assembly path exists and is a file."""
    if not path:
        return "Assembly path is required."
    p = Path(path)
    if not p.exists():
        return f"File not found: {path}"
    if not p.is_file():
        return f"Not a file: {path}"
    if p.suffix.lower() not in (".dll", ".exe", ".winmd"):
        return f"Not a .NET assembly (expected .dll/.exe/.winmd): {path}"
    return None


async def _run_dnspy_console(args: list[str], timeout: int = 120) -> tuple[int, str, str]:
    """Run dnSpy.Console.exe via PowerShell to avoid console handle crashes.

    Returns (return_code, stdout, stderr).
    """
    if not DNSPY_CONSOLE:
        return -1, "", "DNSPY_PATH not configured or dnSpy.Console.exe not found."

    # Build PowerShell command that invokes dnSpy.Console.exe
    escaped_exe = DNSPY_CONSOLE.replace("'", "''")
    escaped_args = " ".join(f"'{a.replace(chr(39), chr(39)+chr(39))}'" for a in args)
    ps_cmd = f"& '{escaped_exe}' {escaped_args}"

    proc = await asyncio.create_subprocess_exec(
        "powershell", "-NoProfile", "-NonInteractive", "-Command", ps_cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    try:
        stdout, stderr = await asyncio.wait_for(
            proc.communicate(), timeout=timeout
        )
    except asyncio.TimeoutError:
        proc.kill()
        return -1, "", f"dnSpy.Console.exe timed out after {timeout}s"

    return (
        proc.returncode or 0,
        stdout.decode("utf-8", errors="replace"),
        stderr.decode("utf-8", errors="replace"),
    )


def _open_dotnet_pe(path: str):
    """Open a .NET PE file with dnfile. Returns (dnpe, error_string)."""
    try:
        dnfile = _get_dnfile()
        pe = dnfile.dnPE(path)
        if pe.net is None:
            return None, f"'{path}' is a valid PE file but not a .NET assembly (no CLR header)."
        return pe, None
    except Exception as e:
        return None, f"Failed to parse '{path}': {type(e).__name__}: {e}"


# ---------------------------------------------------------------------------
# MCP Server
# ---------------------------------------------------------------------------

mcp = FastMCP(
    "dnspy",
    instructions=(
        ".NET assembly decompiler and analyzer powered by dnSpy. "
        "Decompile .NET assemblies to C# source code, inspect types, methods, "
        "metadata, references, strings, and resources. "
        "Use dnspy_list_types to explore an assembly. "
        "Use dnspy_decompile_type to get full C# source. "
        "Use dnspy_search_strings to find hardcoded values."
    ),
)


# ═══════════════════════════════════════════════════════════════════════════════
# DECOMPILATION TOOLS (CLI subprocess)
# ═══════════════════════════════════════════════════════════════════════════════

@mcp.tool()
async def dnspy_decompile_assembly(
    assembly_path: str,
    language: str = "C#",
    max_files: int = 50,
    max_chars_per_file: int = 8000,
) -> str:
    """Decompile an entire .NET assembly into a C# project. Returns the most
    important source files.

    Args:
        assembly_path: Absolute path to the .NET assembly (.dll or .exe)
        language: Decompilation language (C#, VB, IL)
        max_files: Maximum number of source files to return (default 50)
        max_chars_per_file: Max characters per file in output (default 8000)
    """
    if err := _validate_assembly(assembly_path):
        return err

    with tempfile.TemporaryDirectory(prefix="dnspy_") as tmpdir:
        args = [
            "-o", tmpdir,
            "--no-color",
            "--no-sln",
            "-l", language,
            assembly_path,
        ]

        rc, stdout, stderr = await _run_dnspy_console(args, timeout=180)

        if rc != 0:
            return _j({
                "error": True,
                "return_code": rc,
                "stdout": stdout[:2000],
                "stderr": stderr[:2000],
            })

        # Collect output source files
        source_exts = {".cs", ".vb", ".il", ".csproj", ".vbproj", ".resx", ".xaml"}
        found_files = []
        for root, _, files in os.walk(tmpdir):
            for f in files:
                fp = os.path.join(root, f)
                ext = os.path.splitext(f)[1].lower()
                if ext in source_exts:
                    rel = os.path.relpath(fp, tmpdir)
                    size = os.path.getsize(fp)
                    found_files.append((rel, fp, size))

        found_files.sort(key=lambda x: x[2], reverse=True)
        total = len(found_files)
        selected = found_files[:max_files]

        lines = [f"Decompiled '{os.path.basename(assembly_path)}' → {total} source files (showing {len(selected)}):"]
        for rel, fp, size in selected:
            try:
                with open(fp, "r", encoding="utf-8", errors="replace") as fh:
                    content = fh.read(max_chars_per_file)
                if len(content) >= max_chars_per_file:
                    content += "\n// ... [truncated]"
            except Exception as e:
                content = f"// Error reading file: {e}"

            lines.append(f"\n{'='*60}")
            lines.append(f"// FILE: {rel} ({size:,} bytes)")
            lines.append(f"{'='*60}")
            lines.append(content)

        return "\n".join(lines)


@mcp.tool()
async def dnspy_decompile_type(
    assembly_path: str,
    type_name: str,
    language: str = "C#",
) -> str:
    """Decompile a single type (class/struct/enum) from a .NET assembly.

    Args:
        assembly_path: Absolute path to the .NET assembly
        type_name: Full or partial type name (e.g. "System.String", "MyClass")
        language: Decompilation language (C#, VB, IL)
    """
    if err := _validate_assembly(assembly_path):
        return err

    with tempfile.TemporaryDirectory(prefix="dnspy_") as tmpdir:
        args = [
            "-o", tmpdir,
            "--no-color",
            "--no-sln",
            "-l", language,
            "-t", type_name,
            assembly_path,
        ]

        rc, stdout, stderr = await _run_dnspy_console(args, timeout=60)

        # Collect all output
        output_parts = []
        if stdout.strip():
            output_parts.append(stdout.strip())

        # Also read any generated files
        for root, _, files in os.walk(tmpdir):
            for f in files:
                fp = os.path.join(root, f)
                try:
                    with open(fp, "r", encoding="utf-8", errors="replace") as fh:
                        content = fh.read(20000)
                    rel = os.path.relpath(fp, tmpdir)
                    output_parts.append(f"// FILE: {rel}\n{content}")
                except Exception:
                    pass

        if rc != 0 and not output_parts:
            return _j({
                "error": True,
                "return_code": rc,
                "message": stderr[:2000] or "Decompilation failed.",
            })

        if not output_parts:
            return f"Type '{type_name}' not found in '{os.path.basename(assembly_path)}'."

        return "\n".join(output_parts)


@mcp.tool()
async def dnspy_decompile_token(
    assembly_path: str,
    md_token: str,
    language: str = "C#",
) -> str:
    """Decompile a specific metadata token (method, type, field) from a .NET assembly.

    Args:
        assembly_path: Absolute path to the .NET assembly
        md_token: Metadata token in hex (e.g. "0x06000123" for a MethodDef)
        language: Decompilation language (C#, VB, IL)
    """
    if err := _validate_assembly(assembly_path):
        return err

    with tempfile.TemporaryDirectory(prefix="dnspy_") as tmpdir:
        args = [
            "-o", tmpdir,
            "--no-color",
            "--no-sln",
            "-l", language,
            "--md", md_token,
            assembly_path,
        ]

        rc, stdout, stderr = await _run_dnspy_console(args, timeout=60)

        output_parts = []
        if stdout.strip():
            output_parts.append(stdout.strip())

        for root, _, files in os.walk(tmpdir):
            for f in files:
                fp = os.path.join(root, f)
                try:
                    with open(fp, "r", encoding="utf-8", errors="replace") as fh:
                        content = fh.read(20000)
                    rel = os.path.relpath(fp, tmpdir)
                    output_parts.append(f"// FILE: {rel}\n{content}")
                except Exception:
                    pass

        if rc != 0 and not output_parts:
            return _j({
                "error": True,
                "return_code": rc,
                "message": stderr[:2000] or "Decompilation failed.",
            })

        if not output_parts:
            return f"Token '{md_token}' produced no output from '{os.path.basename(assembly_path)}'."

        return "\n".join(output_parts)


# ═══════════════════════════════════════════════════════════════════════════════
# METADATA INSPECTION TOOLS (in-process via dnfile/pefile)
# ═══════════════════════════════════════════════════════════════════════════════

@mcp.tool()
async def dnspy_list_types(
    assembly_path: str,
    include_nested: bool = False,
    namespace_filter: Optional[str] = None,
) -> str:
    """List all types (classes, structs, enums, interfaces) in a .NET assembly.

    Args:
        assembly_path: Absolute path to the .NET assembly
        include_nested: Include nested/inner types (default false)
        namespace_filter: Filter to types in this namespace (partial match)
    """
    if err := _validate_assembly(assembly_path):
        return err

    pe, parse_err = _open_dotnet_pe(assembly_path)
    if parse_err:
        return parse_err

    try:
        dnfile = _get_dnfile()
        types = []
        typedef_table = pe.net.mdtables.TypeDef

        if typedef_table is None or not typedef_table.rows:
            pe.close()
            return f"No types found in '{os.path.basename(assembly_path)}'."

        for row in typedef_table:
            ns = str(row.TypeNamespace or "")
            name = str(row.TypeName or "")

            if not name or name == "<Module>":
                continue

            # Skip nested types if not requested
            if not include_nested and hasattr(row, 'Flags'):
                flags = row.Flags
                if isinstance(flags, int):
                    # Nested visibility flags: bits 1-3 set
                    if flags & 0x00000006:  # NestedPublic or NestedPrivate etc.
                        continue

            full_name = f"{ns}.{name}" if ns else name

            if namespace_filter and namespace_filter.lower() not in ns.lower():
                continue

            # Determine kind from flags
            kind = "class"
            if hasattr(row, 'Flags') and isinstance(row.Flags, int):
                flags = row.Flags
                if flags & 0x00000020:  # Interface
                    kind = "interface"
                elif flags & 0x00000100:  # Sealed + value-type heuristic
                    if flags & 0x00100000:  # Sealed
                        kind = "sealed class"
                # Check if enum (extends System.Enum)
                if hasattr(row, 'Extends') and row.Extends:
                    ext = str(row.Extends) if row.Extends else ""
                    if "Enum" in ext:
                        kind = "enum"
                    elif "ValueType" in ext:
                        kind = "struct"

            types.append((ns, name, full_name, kind))

        pe.close()

        if not types:
            return f"No matching types found in '{os.path.basename(assembly_path)}'."

        # Group by namespace
        by_ns: dict[str, list] = {}
        for ns, name, full, kind in types:
            by_ns.setdefault(ns or "(global)", []).append((name, kind))

        lines = [f"Found {len(types)} types in '{os.path.basename(assembly_path)}':"]
        for ns in sorted(by_ns.keys()):
            lines.append(f"\n  namespace {ns}:")
            for name, kind in sorted(by_ns[ns], key=lambda x: x[0]):
                lines.append(f"    [{kind}] {name}")

        return "\n".join(lines)

    except Exception as e:
        pe.close()
        return f"Error analyzing assembly: {type(e).__name__}: {e}"


@mcp.tool()
async def dnspy_list_methods(
    assembly_path: str,
    type_name: str,
) -> str:
    """List all methods of a specific type in a .NET assembly.

    Args:
        assembly_path: Absolute path to the .NET assembly
        type_name: Type name to list methods for (partial match supported)
    """
    if err := _validate_assembly(assembly_path):
        return err

    pe, parse_err = _open_dotnet_pe(assembly_path)
    if parse_err:
        return parse_err

    try:
        typedef_table = pe.net.mdtables.TypeDef
        methoddef_table = pe.net.mdtables.MethodDef

        if typedef_table is None or methoddef_table is None:
            pe.close()
            return "Assembly has no type/method definitions."

        # Find the matching type
        matched_type = None
        matched_idx = None
        type_name_lower = type_name.lower()

        for idx, row in enumerate(typedef_table):
            ns = str(row.TypeNamespace or "")
            name = str(row.TypeName or "")
            full = f"{ns}.{name}" if ns else name

            if type_name_lower in full.lower() or type_name_lower in name.lower():
                matched_type = full
                matched_idx = idx
                break

        if matched_type is None:
            pe.close()
            return f"Type '{type_name}' not found in '{os.path.basename(assembly_path)}'."

        # Get method range for this type
        # MethodList gives the first method index for each type
        current_row = typedef_table.rows[matched_idx]
        method_start = current_row.MethodList.row_index if hasattr(current_row, 'MethodList') and current_row.MethodList else 0

        # End is either the next type's MethodList or end of methods table
        if matched_idx + 1 < len(typedef_table.rows):
            next_row = typedef_table.rows[matched_idx + 1]
            method_end = next_row.MethodList.row_index if hasattr(next_row, 'MethodList') and next_row.MethodList else len(methoddef_table.rows)
        else:
            method_end = len(methoddef_table.rows)

        methods = []
        for i in range(method_start - 1, min(method_end - 1, len(methoddef_table.rows))):
            if i < 0 or i >= len(methoddef_table.rows):
                continue
            mrow = methoddef_table.rows[i]
            mname = str(mrow.Name or "")
            # Get method flags for visibility
            flags = mrow.Flags if hasattr(mrow, 'Flags') and isinstance(mrow.Flags, int) else 0
            visibility = "private"
            if flags & 0x0006 == 0x0006:
                visibility = "public"
            elif flags & 0x0005 == 0x0005:
                visibility = "family"  # protected
            elif flags & 0x0003 == 0x0003:
                visibility = "assembly"  # internal

            static = "static " if flags & 0x0010 else ""
            virtual = "virtual " if flags & 0x0040 else ""
            abstract = "abstract " if flags & 0x0400 else ""

            token = f"0x{(0x06000001 + i):08X}"
            methods.append(f"    {visibility} {static}{virtual}{abstract}{mname}  // token: {token}")

        pe.close()

        if not methods:
            return f"No methods found for type '{matched_type}'."

        lines = [f"Methods of {matched_type} ({len(methods)} methods):"]
        lines.extend(methods)
        return "\n".join(lines)

    except Exception as e:
        pe.close()
        return f"Error analyzing methods: {type(e).__name__}: {e}"


@mcp.tool()
async def dnspy_get_metadata(assembly_path: str) -> str:
    """Get PE headers, CLR metadata, and .NET runtime information from an assembly.

    Args:
        assembly_path: Absolute path to the .NET assembly
    """
    if err := _validate_assembly(assembly_path):
        return err

    info: dict[str, Any] = {"file": os.path.basename(assembly_path)}

    # PE-level analysis via pefile
    try:
        pefile = _get_pefile()
        pe = pefile.PE(assembly_path)
        info["pe"] = {
            "machine": hex(pe.FILE_HEADER.Machine),
            "subsystem": pe.OPTIONAL_HEADER.Subsystem,
            "is_64bit": pe.OPTIONAL_HEADER.Magic == 0x20b,
            "entry_point_rva": hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint),
            "timestamp": pe.FILE_HEADER.TimeDateStamp,
            "number_of_sections": pe.FILE_HEADER.NumberOfSections,
            "sections": [s.Name.decode("utf-8", errors="replace").strip("\x00") for s in pe.sections],
        }
        pe.close()
    except Exception as e:
        info["pe_error"] = str(e)

    # .NET-level analysis via dnfile
    try:
        dnpe, parse_err = _open_dotnet_pe(assembly_path)
        if parse_err:
            info["dotnet_error"] = parse_err
        else:
            clr = dnpe.net
            if clr:
                info["dotnet"] = {}
                if clr.metadata:
                    # Handle different dnfile versions
                    ver = getattr(clr.metadata, 'Version', None) or getattr(clr.metadata, 'version', None)
                    if ver:
                        info["dotnet"]["metadata_header_version"] = str(ver)

                # Count types and methods
                if clr.mdtables.TypeDef:
                    info["dotnet"]["type_count"] = len(clr.mdtables.TypeDef.rows)
                if clr.mdtables.MethodDef:
                    info["dotnet"]["method_count"] = len(clr.mdtables.MethodDef.rows)
                if clr.mdtables.Field:
                    info["dotnet"]["field_count"] = len(clr.mdtables.Field.rows)
                if clr.mdtables.MemberRef:
                    info["dotnet"]["memberref_count"] = len(clr.mdtables.MemberRef.rows)

                # Assembly info
                if clr.mdtables.Assembly and clr.mdtables.Assembly.rows:
                    asm = clr.mdtables.Assembly.rows[0]
                    info["dotnet"]["assembly"] = {
                        "name": str(asm.Name or ""),
                        "version": f"{asm.MajorVersion}.{asm.MinorVersion}.{asm.BuildNumber}.{asm.RevisionNumber}",
                        "culture": str(asm.Culture or ""),
                    }

                # Module info
                if clr.mdtables.Module and clr.mdtables.Module.rows:
                    mod = clr.mdtables.Module.rows[0]
                    info["dotnet"]["module"] = str(mod.Name or "")

            dnpe.close()

    except Exception as e:
        info["dotnet_error"] = str(e)

    return _j(info)


@mcp.tool()
async def dnspy_get_references(assembly_path: str) -> str:
    """List all assembly references (dependencies) of a .NET assembly.

    Args:
        assembly_path: Absolute path to the .NET assembly
    """
    if err := _validate_assembly(assembly_path):
        return err

    pe, parse_err = _open_dotnet_pe(assembly_path)
    if parse_err:
        return parse_err

    try:
        refs = []
        asmref_table = pe.net.mdtables.AssemblyRef

        if asmref_table and asmref_table.rows:
            for row in asmref_table:
                name = str(row.Name or "")
                version = f"{row.MajorVersion}.{row.MinorVersion}.{row.BuildNumber}.{row.RevisionNumber}"
                culture = str(row.Culture or "neutral")
                refs.append(f"  {name}, Version={version}, Culture={culture}")

        pe.close()

        if not refs:
            return f"No assembly references found in '{os.path.basename(assembly_path)}'."

        lines = [f"Assembly references for '{os.path.basename(assembly_path)}' ({len(refs)} refs):"]
        lines.extend(sorted(refs))
        return "\n".join(lines)

    except Exception as e:
        pe.close()
        return f"Error reading references: {type(e).__name__}: {e}"


@mcp.tool()
async def dnspy_search_strings(
    assembly_path: str,
    pattern: Optional[str] = None,
    max_results: int = 100,
) -> str:
    """Search for string literals in a .NET assembly's user strings heap and #Strings stream.

    Args:
        assembly_path: Absolute path to the .NET assembly
        pattern: Optional substring filter (case-insensitive). Returns all strings if empty.
        max_results: Maximum results to return (default 100)
    """
    if err := _validate_assembly(assembly_path):
        return err

    pe, parse_err = _open_dotnet_pe(assembly_path)
    if parse_err:
        return parse_err

    try:
        strings_found = []

        # Read from the #US (User Strings) heap
        if pe.net.metadata and hasattr(pe.net.metadata, 'streams_list'):
            for stream in pe.net.metadata.streams_list:
                stream_name = getattr(stream, 'name', '') or ''
                if '#US' in stream_name and hasattr(stream, '__bytes__'):
                    # Parse user strings heap manually
                    data = bytes(stream)
                    offset = 1  # Skip first null byte
                    while offset < len(data):
                        # Read compressed length
                        if offset >= len(data):
                            break
                        b0 = data[offset]
                        if b0 == 0:
                            offset += 1
                            continue
                        if b0 < 0x80:
                            length = b0
                            offset += 1
                        elif b0 < 0xC0:
                            if offset + 1 >= len(data):
                                break
                            length = ((b0 & 0x3F) << 8) | data[offset + 1]
                            offset += 2
                        else:
                            if offset + 3 >= len(data):
                                break
                            length = ((b0 & 0x1F) << 24) | (data[offset+1] << 16) | (data[offset+2] << 8) | data[offset+3]
                            offset += 4

                        if length <= 0 or offset + length > len(data):
                            offset += max(length, 1)
                            continue

                        # User strings are UTF-16LE with a trailing byte
                        str_data = data[offset:offset + length]
                        offset += length

                        if len(str_data) >= 2:
                            try:
                                # Remove trailing indicator byte
                                s = str_data[:-1].decode("utf-16-le", errors="replace").strip("\x00")
                                if s and len(s) >= 2:
                                    strings_found.append(("UserString", s))
                            except Exception:
                                pass

        # Also read #Strings heap (identifiers, not user strings)
        if pe.net.strings:
            try:
                for s in pe.net.strings:
                    if s and len(str(s)) >= 2:
                        strings_found.append(("Identifier", str(s)))
            except Exception:
                pass

        pe.close()

        # Filter
        if pattern:
            pat_lower = pattern.lower()
            strings_found = [(src, s) for src, s in strings_found if pat_lower in s.lower()]

        if not strings_found:
            msg = f"No strings found in '{os.path.basename(assembly_path)}'"
            if pattern:
                msg += f" matching '{pattern}'"
            return msg + "."

        total = len(strings_found)
        strings_found = strings_found[:max_results]

        lines = [f"Found {total} strings in '{os.path.basename(assembly_path)}' (showing {len(strings_found)}):"]
        for src, s in strings_found:
            display = s[:200] + "..." if len(s) > 200 else s
            display = display.replace("\n", "\\n").replace("\r", "\\r")
            lines.append(f"  [{src}] {display}")

        return "\n".join(lines)

    except Exception as e:
        return f"Error searching strings: {type(e).__name__}: {e}"


@mcp.tool()
async def dnspy_get_resources(assembly_path: str) -> str:
    """List embedded managed resources in a .NET assembly.

    Args:
        assembly_path: Absolute path to the .NET assembly
    """
    if err := _validate_assembly(assembly_path):
        return err

    pe, parse_err = _open_dotnet_pe(assembly_path)
    if parse_err:
        return parse_err

    try:
        resources = []
        manifest_table = pe.net.mdtables.ManifestResource

        if manifest_table and manifest_table.rows:
            for row in manifest_table:
                name = str(row.Name or "")
                flags = row.Flags if hasattr(row, 'Flags') and isinstance(row.Flags, int) else 0
                visibility = "public" if flags & 0x0001 == 0x0001 else "private"

                # Check if embedded or linked
                implementation = "embedded"
                if hasattr(row, 'Implementation') and row.Implementation:
                    implementation = f"linked → {row.Implementation}"

                resources.append(f"  [{visibility}] {name} ({implementation})")

        pe.close()

        if not resources:
            return f"No managed resources found in '{os.path.basename(assembly_path)}'."

        lines = [f"Managed resources in '{os.path.basename(assembly_path)}' ({len(resources)} resources):"]
        lines.extend(sorted(resources))
        return "\n".join(lines)

    except Exception as e:
        pe.close()
        return f"Error reading resources: {type(e).__name__}: {e}"


@mcp.tool()
async def dnspy_get_assembly_info(assembly_path: str) -> str:
    """Get detailed assembly identity — name, version, culture, public key token, module info.

    Args:
        assembly_path: Absolute path to the .NET assembly
    """
    if err := _validate_assembly(assembly_path):
        return err

    pe, parse_err = _open_dotnet_pe(assembly_path)
    if parse_err:
        return parse_err

    try:
        info = {}

        # Assembly table
        asm_table = pe.net.mdtables.Assembly
        if asm_table and asm_table.rows:
            asm = asm_table.rows[0]
            info["name"] = str(asm.Name or "")
            info["version"] = f"{asm.MajorVersion}.{asm.MinorVersion}.{asm.BuildNumber}.{asm.RevisionNumber}"
            info["culture"] = str(asm.Culture or "neutral")
            if hasattr(asm, 'PublicKey') and asm.PublicKey:
                info["has_public_key"] = True
            if hasattr(asm, 'HashAlgId'):
                info["hash_algorithm"] = hex(asm.HashAlgId) if isinstance(asm.HashAlgId, int) else str(asm.HashAlgId)

        # Module table
        mod_table = pe.net.mdtables.Module
        if mod_table and mod_table.rows:
            mod = mod_table.rows[0]
            info["module_name"] = str(mod.Name or "")
            if hasattr(mod, 'Mvid') and mod.Mvid:
                info["mvid"] = str(mod.Mvid)

        # Custom attributes count
        ca_table = pe.net.mdtables.CustomAttribute
        if ca_table:
            info["custom_attribute_count"] = len(ca_table.rows)

        # TypeRef count (external type references)
        tr_table = pe.net.mdtables.TypeRef
        if tr_table:
            info["typeref_count"] = len(tr_table.rows)

        # Metadata version
        if pe.net.metadata:
            ver = getattr(pe.net.metadata, 'Version', None) or getattr(pe.net.metadata, 'version', None)
            if ver:
                info["metadata_version"] = str(ver)

        # File size
        info["file_size_bytes"] = os.path.getsize(assembly_path)

        pe.close()

        if not info:
            return f"Could not extract assembly info from '{os.path.basename(assembly_path)}'."

        lines = [f"Assembly info for '{os.path.basename(assembly_path)}':"]
        for k, v in info.items():
            label = k.replace("_", " ").title()
            lines.append(f"  {label}: {v}")

        return "\n".join(lines)

    except Exception as e:
        pe.close()
        return f"Error reading assembly info: {type(e).__name__}: {e}"


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
