"""SDR MCP Server — Abstraction layer for selecting the active SDR backend.

Probes available backends in order: SpyServer (B) -> RTL CLI (C) -> FFI (D).
Returns a tag indicating which vector is active so callers can adapt.
"""

import shutil
import socket
from dataclasses import dataclass

from config import RTL_CLI_DIR, RTLSDR_DLL


@dataclass
class BackendStatus:
    spyserver_available: bool = False
    spyserver_host: str = ""
    spyserver_port: int = 0
    rtl_cli_available: bool = False
    rtl_cli_path: str = ""
    ffi_available: bool = False
    ffi_dll_path: str = ""
    active_vector: str = "none"


def probe_spyserver(host: str = "127.0.0.1", port: int = 5555, timeout: float = 1.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (OSError, ConnectionRefusedError, TimeoutError):
        return False


def probe_rtl_cli() -> str | None:
    local = RTL_CLI_DIR / "rtl_test.exe"
    if local.exists():
        return str(local)
    return shutil.which("rtl_test") or shutil.which("rtl_sdr")


def probe_ffi() -> bool:
    return RTLSDR_DLL.exists()


def detect_backend(spyserver_host: str = "127.0.0.1", spyserver_port: int = 5555) -> BackendStatus:
    status = BackendStatus()

    if probe_spyserver(spyserver_host, spyserver_port):
        status.spyserver_available = True
        status.spyserver_host = spyserver_host
        status.spyserver_port = spyserver_port
        status.active_vector = "B_spyserver"

    cli = probe_rtl_cli()
    if cli:
        status.rtl_cli_available = True
        status.rtl_cli_path = cli
        if status.active_vector == "none":
            status.active_vector = "C_rtl_cli"

    if probe_ffi():
        status.ffi_available = True
        status.ffi_dll_path = str(RTLSDR_DLL)
        if status.active_vector == "none":
            status.active_vector = "D_ffi"

    return status
