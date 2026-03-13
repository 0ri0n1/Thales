#!/usr/bin/env python3
"""
Flipper Zero Full-Spectrum C2 Reconnaissance
=============================================
Automated 4-phase interrogation of Flipper Zero via USB serial.
Produces MCP-ready schemas and full capability report.

Usage: python flipper_recon.py [--port COM4] [--baud 115200]
Output: E:/Thon/recon/flipper/
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone

try:
    import serial
    import serial.tools.list_ports
except ImportError:
    print("ERROR: pyserial required. Run: pip install pyserial")
    sys.exit(1)

# --- Constants ---
FLIPPER_VID = 0x0483
FLIPPER_PID = 0x5740
PROMPT = ">: "
CMD_DELIM = "\r\n"
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

KNOWN_SUBSYSTEMS = [
    "subghz", "rfid", "nfc", "infrared", "ibutton", "badusb", "gpio",
    "wifi", "bt", "storage", "power", "system", "led", "vibro", "speaker",
    "input", "notification", "loader", "crypto", "desktop", "update",
    "log", "onewire", "js", "lfrfid", "debug", "rpc", "info",
]

RISK_DEFINITIONS = {
    "none": "Read-only, no state change, no RF emission",
    "low": "Reversible config change, no RF emission",
    "medium": "RF emission, LED/vibro actuation, reversible",
    "high": "Active wireless attacks, persistent config changes",
    "critical": "Firmware mod, factory reset, bootloader ops",
}


class SessionLog:
    """Timestamped TX/RX session logger."""

    def __init__(self, path: str):
        self.f = open(path, "w", encoding="utf-8")
        self._write(f"# Flipper Zero Recon Session Log")
        self._write(f"# Started: {datetime.now(timezone.utc).isoformat()}")
        self._write("")

    def _write(self, line: str):
        self.f.write(line + "\n")
        self.f.flush()

    def tx(self, cmd: str):
        ts = datetime.now(timezone.utc).strftime("%H:%M:%S.%f")[:-3]
        self._write(f"[{ts}] TX >>> {cmd}")

    def rx(self, data: str):
        ts = datetime.now(timezone.utc).strftime("%H:%M:%S.%f")[:-3]
        for line in data.split("\n"):
            self._write(f"[{ts}] RX <<< {line}")

    def note(self, msg: str):
        ts = datetime.now(timezone.utc).strftime("%H:%M:%S.%f")[:-3]
        self._write(f"[{ts}] NOTE: {msg}")

    def close(self):
        self._write(f"\n# Ended: {datetime.now(timezone.utc).isoformat()}")
        self.f.close()


class FlipperC2:
    """USB Serial C2 channel to Flipper Zero CLI."""

    def __init__(self, port: str, baud: int, log: SessionLog):
        self.port = port
        self.baud = baud
        self.log = log
        self.ser = None
        self.connected = False

    def connect(self) -> bool:
        try:
            self.ser = serial.Serial(
                port=self.port, baudrate=self.baud, timeout=2.0,
                write_timeout=2.0, bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
            )
            time.sleep(0.5)
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
            self.log.note(f"Connected to {self.port} @ {self.baud}")
            self.connected = True
            return True
        except serial.SerialException as e:
            self.log.note(f"Connection failed: {e}")
            return False

    def disconnect(self):
        if self.ser and self.ser.is_open:
            try:
                self.ser.close()
            except Exception:
                pass
        self.connected = False
        self.log.note("Disconnected")

    def send(self, cmd: str, timeout: float = 3.0) -> str:
        """Send command, return response text. All TX/RX logged."""
        if not self.ser or not self.ser.is_open:
            return ""
        self.log.tx(cmd)
        try:
            self.ser.reset_input_buffer()
            self.ser.write(f"{cmd}{CMD_DELIM}".encode("utf-8"))
            self.ser.flush()

            lines = []
            start = time.time()
            while (time.time() - start) < timeout:
                if self.ser.in_waiting:
                    raw = self.ser.readline().decode("utf-8", errors="replace").strip()
                    if raw:
                        lines.append(raw)
                    start = time.time()  # reset on data
                else:
                    time.sleep(0.02)

            response = "\n".join(lines)
            # Strip echo of command from top
            resp_lines = response.split("\n")
            if resp_lines and resp_lines[0].strip() == cmd.strip():
                resp_lines = resp_lines[1:]
            # Strip trailing prompt
            if resp_lines and resp_lines[-1].strip().startswith(">:"):
                resp_lines = resp_lines[:-1]
            clean = "\n".join(resp_lines).strip()
            self.log.rx(clean if clean else "(empty)")
            return clean
        except serial.SerialException as e:
            self.log.note(f"Serial error: {e}")
            return ""

    def validate_session(self) -> bool:
        """Send newline and check for prompt."""
        self.log.note("Validating CLI session...")
        try:
            self.ser.reset_input_buffer()
            self.ser.write(CMD_DELIM.encode())
            self.ser.flush()
            time.sleep(0.5)
            buf = b""
            start = time.time()
            while (time.time() - start) < 3.0:
                if self.ser.in_waiting:
                    buf += self.ser.read(self.ser.in_waiting)
                    if PROMPT.encode() in buf:
                        self.log.note("CLI prompt confirmed")
                        return True
                time.sleep(0.05)
            decoded = buf.decode("utf-8", errors="replace")
            self.log.note(f"No prompt detected. Buffer: {decoded[:200]}")
            return False
        except Exception as e:
            self.log.note(f"Validation error: {e}")
            return False


def detect_port() -> str | None:
    """Find Flipper Zero COM port by VID/PID."""
    for p in serial.tools.list_ports.comports():
        if p.vid == FLIPPER_VID and p.pid == FLIPPER_PID:
            return p.device
    return None


def parse_kv(text: str) -> dict:
    """Parse 'key : value' lines from Flipper CLI output."""
    result = {}
    for line in text.split("\n"):
        if ":" in line and not line.startswith(">"):
            key, _, val = line.partition(":")
            k = key.strip().lower().replace(" ", "_")
            v = val.strip()
            if k and v:
                result[k] = v
    return result


# ============================================================
# Phase 0 — Pre-Flight & Baseline
# ============================================================

def phase0(c2: FlipperC2) -> dict:
    """Establish link, fingerprint, capture baseline."""
    print("\n" + "=" * 60)
    print("  PHASE 0 — PRE-FLIGHT & BASELINE")
    print("=" * 60)

    data = {"timestamp": datetime.now(timezone.utc).isoformat()}

    # Fingerprint
    print("  [0.1] Querying device info...")
    data["device_info"] = parse_kv(c2.send("info device", timeout=5))

    print("  [0.2] Querying power info...")
    data["power_info"] = parse_kv(c2.send("info power", timeout=5))

    # Firmware classification
    fw_origin = data["device_info"].get("firmware.origin.fork", "unknown").lower()
    if "official" in fw_origin:
        data["firmware_family"] = "official"
    elif "unleashed" in fw_origin:
        data["firmware_family"] = "unleashed"
    elif "momentum" in fw_origin or "mntm" in fw_origin:
        data["firmware_family"] = "momentum"
    elif "xtreme" in fw_origin or "xfw" in fw_origin:
        data["firmware_family"] = "xtreme"
    else:
        data["firmware_family"] = "unknown"

    print(f"  [0.3] Firmware family: {data['firmware_family']}")
    print(f"        Version: {data['device_info'].get('firmware.version', '?')}")

    # Filesystem baseline
    print("  [0.4] Capturing filesystem baseline...")
    fs_baseline = {}
    for path in ["/ext", "/int"]:
        info_raw = c2.send(f"storage info {path}", timeout=10)
        fs_baseline[f"{path}_info"] = parse_kv(info_raw)
        fs_baseline[f"{path}_info"]["_raw"] = info_raw

        listing_raw = c2.send(f"storage list {path}", timeout=15)
        entries = []
        for line in listing_raw.split("\n"):
            line = line.strip()
            if line.startswith("[D]"):
                entries.append({"type": "dir", "name": line[3:].strip()})
            elif line.startswith("[F]"):
                m = re.match(r"\[F\]\s+(.+?)\s+(\d+)b?$", line)
                if m:
                    entries.append({"type": "file", "name": m.group(1), "size": int(m.group(2))})
                else:
                    entries.append({"type": "file", "name": line[3:].strip()})
        fs_baseline[f"{path}_listing"] = entries

    data["filesystem"] = fs_baseline

    # Save baseline
    baseline_path = os.path.join(OUTPUT_DIR, "baseline-fs.json")
    with open(baseline_path, "w", encoding="utf-8") as f:
        json.dump(fs_baseline, f, indent=2)
    print(f"  [0.5] Baseline saved: {baseline_path}")

    return data


# ============================================================
# Phase 1 — Full Device Interrogation
# ============================================================

def phase1(c2: FlipperC2, phase0_data: dict) -> dict:
    """Enumerate every CLI command and subsystem."""
    print("\n" + "=" * 60)
    print("  PHASE 1 — FULL DEVICE INTERROGATION")
    print("=" * 60)

    data = {"top_level_commands": [], "subsystems": {}, "wifi_module": {}, "bluetooth": {}}

    # 1.1 Top-level commands
    print("  [1.1] Enumerating top-level commands...")
    help_raw = c2.send("?", timeout=5)
    if not help_raw or len(help_raw) < 5:
        help_raw = c2.send("help", timeout=5)

    commands = []
    for line in help_raw.split("\n"):
        line = line.strip()
        if line and not line.startswith(">") and not line.startswith("Commands"):
            # Parse "command_name    - description" format
            m = re.match(r"^(\S+)\s*(?:[-:]?\s*(.*))?$", line)
            if m:
                cmd_name = m.group(1).strip()
                cmd_desc = (m.group(2) or "").strip(" -:")
                if cmd_name and len(cmd_name) < 30:
                    commands.append({"name": cmd_name, "description": cmd_desc})

    data["top_level_commands"] = commands
    cmd_names = [c["name"] for c in commands]
    print(f"        Found {len(commands)} top-level commands")

    # 1.2 Exhaustive subsystem probe
    print("  [1.2] Probing subsystems...")
    all_subsystems = list(set(cmd_names + KNOWN_SUBSYSTEMS))
    all_subsystems.sort()

    for sub in all_subsystems:
        print(f"        Probing: {sub}...")
        sub_data = {"commands": [], "raw_help": "", "available": False}

        # Cascading probe
        for probe in [sub, f"{sub} help", f"{sub} ?"]:
            t0 = time.time()
            resp = c2.send(probe, timeout=4)
            latency_ms = int((time.time() - t0) * 1000)

            if resp and "unknown command" not in resp.lower() and "command not found" not in resp.lower():
                sub_data["available"] = True
                sub_data["raw_help"] = resp
                sub_data["probe_used"] = probe
                sub_data["latency_ms"] = latency_ms

                # Parse sub-commands from help
                for rline in resp.split("\n"):
                    rline = rline.strip()
                    if not rline or rline.startswith(">"):
                        continue
                    sm = re.match(r"^(\S+)\s*(?:[-:]?\s*(.*))?$", rline)
                    if sm:
                        scmd = sm.group(1).strip()
                        sdesc = (sm.group(2) or "").strip(" -:")
                        if scmd and len(scmd) < 40 and scmd not in ["Usage", "Commands", "Options"]:
                            sub_data["commands"].append({
                                "name": scmd,
                                "description": sdesc,
                                "full_command": f"{sub} {scmd}" if sub != scmd else scmd,
                            })
                break  # Got a response, stop cascading

        if sub_data["available"]:
            data["subsystems"][sub] = sub_data

    print(f"        Active subsystems: {len(data['subsystems'])}")

    # 1.3 Deep probe each sub-command for syntax/response
    print("  [1.3] Deep-probing sub-commands for syntax...")
    for sub_name, sub_info in data["subsystems"].items():
        for cmd_entry in sub_info["commands"]:
            full = cmd_entry["full_command"]
            # Skip dangerous commands
            if any(k in full.lower() for k in ["attack", "deauth", "beacon", "evil", "inject", "jam", "format"]):
                cmd_entry["risk_level"] = "high"
                cmd_entry["skipped"] = True
                cmd_entry["skip_reason"] = "High risk — document only"
                continue

            t0 = time.time()
            resp = c2.send(full, timeout=4)
            lat = int((time.time() - t0) * 1000)
            cmd_entry["example_response"] = resp[:500] if resp else "(empty)"
            cmd_entry["response_lines"] = len(resp.split("\n")) if resp else 0
            cmd_entry["latency_ms"] = lat

            # Detect blocking
            cmd_entry["blocking"] = lat > 3500

            # Detect error patterns
            if resp:
                low = resp.lower()
                cmd_entry["is_error"] = any(e in low for e in ["error", "usage:", "unknown", "invalid"])
            else:
                cmd_entry["is_error"] = False

    # 1.4 Bluetooth probe
    print("  [1.4] Probing Bluetooth subsystem...")
    bt_resp = c2.send("bt", timeout=4)
    data["bluetooth"]["raw_help"] = bt_resp
    bt_info = c2.send("bt hci_info", timeout=4)
    data["bluetooth"]["hci_info"] = bt_info
    data["bluetooth"]["ble_mac"] = phase0_data.get("device_info", {}).get("radio.ble.mac", "unknown")

    # 1.5 WiFi module probe
    print("  [1.5] Probing WiFi module...")
    wifi_resp = c2.send("wifi", timeout=4)
    data["wifi_module"]["raw_help"] = wifi_resp
    data["wifi_module"]["available"] = bool(wifi_resp and "unknown" not in wifi_resp.lower())

    return data


# ============================================================
# Phase 2 — Capability Classification
# ============================================================

def classify_risk(sub: str, cmd: str) -> str:
    """Classify risk level for a command."""
    c = f"{sub} {cmd}".lower()
    # Critical
    if any(k in c for k in ["update", "factory", "reset", "bootloader", "flash", "format"]):
        return "critical"
    # High
    if any(k in c for k in ["attack", "deauth", "beacon", "evil", "inject", "jam", "tx "]):
        return "high"
    # Medium
    if any(k in c for k in ["led", "vibro", "speaker", "notification", "subghz rx", "nfc emulate"]):
        return "medium"
    # Low
    if any(k in c for k in ["set", "config", "write", "remove", "delete", "mkdir"]):
        return "low"
    return "none"


def classify_action(cmd: str, resp: str) -> str:
    """Classify action type."""
    c = cmd.lower()
    if any(k in c for k in ["list", "info", "stat", "read", "get", "detect", "scan"]):
        return "read"
    if any(k in c for k in ["write", "set", "add", "mkdir", "remove"]):
        return "write"
    if any(k in c for k in ["rx", "sniff", "monitor"]):
        return "monitor"
    if any(k in c for k in ["tx", "send", "emit", "play"]):
        return "execute"
    return "read"


TEARDOWN_MAP = {
    "subghz rx": "subghz rx_stop",
    "subghz tx": "subghz tx_stop",
    "nfc detect": None,
    "rfid read": None,
    "infrared rx": "infrared rx_stop",
}


def phase2(phase1_data: dict) -> dict:
    """Classify every command for MCP tool generation."""
    print("\n" + "=" * 60)
    print("  PHASE 2 — CAPABILITY CLASSIFICATION")
    print("=" * 60)

    classified = []

    for sub_name, sub_info in phase1_data["subsystems"].items():
        for cmd_entry in sub_info["commands"]:
            full_cmd = cmd_entry["full_command"]
            risk = cmd_entry.get("risk_level", classify_risk(sub_name, cmd_entry["name"]))
            resp = cmd_entry.get("example_response", "")

            entry = {
                "subsystem": sub_name,
                "command": full_cmd,
                "action_type": classify_action(full_cmd, resp),
                "usb_controllable": "full" if not cmd_entry.get("skipped") else "partial",
                "wifi_controllable": "untested",
                "blocking": cmd_entry.get("blocking", False),
                "requires_physical": any(k in full_cmd.lower() for k in ["detect", "emulate", "read card"]),
                "has_teardown": full_cmd.lower() in TEARDOWN_MAP,
                "teardown_command": TEARDOWN_MAP.get(full_cmd.lower()),
                "risk_level": risk,
                "wifi_board_dependent": sub_name in ["wifi"],
                "firmware_gated": "none",
                "response_type": "text",
                "avg_latency_ms": cmd_entry.get("latency_ms", 0),
                "mcp_tool_candidate": risk in ["none", "low", "medium"] and not cmd_entry.get("skipped"),
                "mcp_tool_type": "compound" if cmd_entry.get("blocking") else "simple",
                "notes": cmd_entry.get("skip_reason", ""),
                "example_response": cmd_entry.get("example_response", "")[:200],
                "is_error": cmd_entry.get("is_error", False),
            }
            classified.append(entry)

    # WiFi C2 assessment
    wifi_assessment = {
        "viable": False,
        "blocker": "ESP32-S2 devboard with Marauder firmware — no native CLI relay over WiFi",
        "recommended_firmware": "ESP-AT firmware for TCP server CLI passthrough",
        "notes": "Marauder provides offensive WiFi tools but cannot relay Flipper CLI commands over WiFi"
    }

    # BT C2 assessment
    bt_assessment = {
        "viable": "unknown",
        "assessment": "BLE serial profile support depends on firmware — needs runtime probe",
        "ble_mac": phase1_data.get("bluetooth", {}).get("ble_mac", "unknown"),
    }

    print(f"  Classified {len(classified)} commands")
    stats = {}
    for c in classified:
        r = c["risk_level"]
        stats[r] = stats.get(r, 0) + 1
    for r, count in sorted(stats.items()):
        print(f"    {r}: {count}")

    return {
        "commands": classified,
        "wifi_c2": wifi_assessment,
        "bt_c2": bt_assessment,
        "stats": stats,
    }


# ============================================================
# Phase 3 — Schema Generation & Report
# ============================================================

def phase3(phase0_data: dict, phase1_data: dict, phase2_data: dict) -> None:
    """Generate all deliverable files."""
    print("\n" + "=" * 60)
    print("  PHASE 3 — SCHEMA GENERATION & REPORT")
    print("=" * 60)

    di = phase0_data.get("device_info", {})
    pi = phase0_data.get("power_info", {})

    # --- mcp-tool-schemas.json ---
    print("  [3.1] Generating mcp-tool-schemas.json...")
    tools = []
    for cmd in phase2_data["commands"]:
        if cmd.get("is_error") and not cmd.get("mcp_tool_candidate"):
            continue
        tool = {
            "name": cmd["command"].replace(" ", "_"),
            "description": cmd.get("notes") or f"{cmd['action_type']} via {cmd['subsystem']}",
            "subsystem": cmd["subsystem"],
            "cli_command_template": cmd["command"],
            "parameters": {},
            "response": {
                "type": cmd["response_type"],
                "format": "text",
            },
            "blocking": cmd["blocking"],
            "risk_level": cmd["risk_level"],
            "action_type": cmd["action_type"],
            "usb_controllable": cmd["usb_controllable"],
            "wifi_controllable": cmd["wifi_controllable"],
            "requires_physical": cmd["requires_physical"],
            "mcp_tool_type": cmd["mcp_tool_type"],
        }
        if cmd.get("has_teardown"):
            tool["teardown"] = cmd["teardown_command"]
            tool["response"]["termination"] = f"manual (requires {cmd['teardown_command']})"
        tools.append(tool)

    schema = {
        "device": {
            "model": di.get("hardware.model", "Flipper Zero"),
            "firmware": {
                "family": phase0_data.get("firmware_family", "unknown"),
                "version": di.get("firmware.version", "unknown"),
                "build_date": di.get("firmware.build.date", "unknown"),
                "api_version": f"{di.get('firmware.api.major', '?')}.{di.get('firmware.api.minor', '?')}",
                "git_hash": di.get("firmware.commit.hash", "unknown"),
                "origin": di.get("firmware.origin.fork", "unknown"),
            },
            "transports": {
                "usb": {"viable": True},
                "wifi": phase2_data["wifi_c2"],
                "bluetooth": phase2_data["bt_c2"],
            },
        },
        "tools": tools,
        "compound_sequences": [],
        "event_sources": [],
    }

    schema_path = os.path.join(OUTPUT_DIR, "mcp-tool-schemas.json")
    with open(schema_path, "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2)
    print(f"        Wrote {len(tools)} tool definitions")

    # --- transport-config.json ---
    print("  [3.2] Generating transport-config.json...")
    transport = {
        "usb": {
            "viable": True,
            "connection": {
                "vid": "0483", "pid": "5740",
                "baud_primary": 115200, "baud_fallback": 230400,
                "data_bits": 8, "parity": "none", "stop_bits": 1,
                "prompt_sentinel": ">: ", "command_delimiter": "\\r\\n",
                "read_timeout_default_ms": 2000,
                "read_timeout_slow_ms": 10000,
                "read_timeout_storage_ms": 30000,
            },
            "discovery": {
                "linux": "/dev/ttyACM* or /dev/serial/by-id/*Flipper*",
                "windows": "Get-PnPDevice -Class Ports | VID_0483&PID_5740",
            },
        },
        "wifi": phase2_data["wifi_c2"],
        "bluetooth": phase2_data["bt_c2"],
    }
    tp_path = os.path.join(OUTPUT_DIR, "transport-config.json")
    with open(tp_path, "w", encoding="utf-8") as f:
        json.dump(transport, f, indent=2)

    # --- command-tree.json ---
    print("  [3.3] Generating command-tree.json...")
    tree = {}
    for sub_name, sub_info in phase1_data["subsystems"].items():
        tree[sub_name] = {
            "available": sub_info["available"],
            "commands": [
                {
                    "name": c["name"],
                    "full_command": c["full_command"],
                    "description": c.get("description", ""),
                    "latency_ms": c.get("latency_ms", 0),
                    "blocking": c.get("blocking", False),
                }
                for c in sub_info["commands"]
            ],
        }
    ct_path = os.path.join(OUTPUT_DIR, "command-tree.json")
    with open(ct_path, "w", encoding="utf-8") as f:
        json.dump(tree, f, indent=2)

    # --- flipper-capability-report.md ---
    print("  [3.4] Generating flipper-capability-report.md...")
    report_lines = []
    r = report_lines.append

    r("# Flipper Zero — Full-Spectrum Capability Report")
    r(f"\n> Generated: {datetime.now(timezone.utc).isoformat()}")
    r(f"> Firmware: {di.get('firmware.origin.fork', '?')} {di.get('firmware.version', '?')}")
    r(f"> Device: {di.get('hardware.name', '?')} (HW rev {di.get('hardware.ver', '?')})")
    r("")

    r("## Device Identity Card\n")
    r(f"| Field | Value |")
    r(f"|-------|-------|")
    r(f"| Model | {di.get('hardware.model', '?')} |")
    r(f"| Name | {di.get('hardware.name', '?')} |")
    r(f"| UID | `{di.get('hardware.uid', '?')}` |")
    r(f"| HW Rev | {di.get('hardware.ver', '?')} |")
    r(f"| Target | {di.get('hardware.target', '?')} |")
    r(f"| Region | {di.get('hardware.region.provisioned', '?')} |")
    r(f"| FW Version | {di.get('firmware.version', '?')} |")
    r(f"| FW Origin | {di.get('firmware.origin.fork', '?')} |")
    r(f"| FW Build | {di.get('firmware.build.date', '?')} |")
    r(f"| API | {di.get('firmware.api.major', '?')}.{di.get('firmware.api.minor', '?')} |")
    r(f"| Git Hash | `{di.get('firmware.commit.hash', '?')}` |")
    r(f"| BLE MAC | `{di.get('radio.ble.mac', '?')}` |")
    r(f"| Battery | {pi.get('charge.level', '?')}% ({pi.get('charge.state', '?')}) |")
    r(f"| Battery Health | {pi.get('battery.health', '?')}% |")
    r("")

    r("## C2 Transport Assessment\n")
    r("| Transport | Status | Notes |")
    r("|-----------|--------|-------|")
    r("| USB Serial | ✅ Confirmed | COM4, 115200 baud, full CLI access |")
    r(f"| WiFi | ❌ Not viable | {phase2_data['wifi_c2']['blocker']} |")
    r(f"| Bluetooth | ❓ Unknown | {phase2_data['bt_c2']['assessment']} |")
    r("")

    r("## Command Tree\n")
    total_cmds = 0
    for sub_name in sorted(tree.keys()):
        sub = tree[sub_name]
        cmd_count = len(sub["commands"])
        total_cmds += cmd_count
        r(f"### `{sub_name}` ({cmd_count} commands)\n")
        if sub["commands"]:
            r("| Command | Description | Latency |")
            r("|---------|-------------|---------|")
            for c in sub["commands"]:
                lat = f"{c['latency_ms']}ms" if c.get("latency_ms") else "—"
                r(f"| `{c['full_command']}` | {c['description']} | {lat} |")
        r("")

    r(f"**Total commands discovered: {total_cmds}**\n")

    r("## Capability Matrix Summary\n")
    r("| Risk Level | Count | Definition |")
    r("|------------|-------|------------|")
    for risk in ["none", "low", "medium", "high", "critical"]:
        count = phase2_data["stats"].get(risk, 0)
        r(f"| {risk} | {count} | {RISK_DEFINITIONS[risk]} |")
    r("")

    mcp_candidates = sum(1 for c in phase2_data["commands"] if c["mcp_tool_candidate"])
    r(f"**MCP tool candidates: {mcp_candidates} / {len(phase2_data['commands'])}**\n")

    r("## MCP Server Architecture Recommendations\n")
    r("1. **Framework:** Python FastMCP (consistency with Thon MCP ecosystem)")
    r("2. **Transport:** USB serial primary via pyserial, WiFi fallback pending ESP firmware change")
    r("3. **Connection:** Singleton serial session with heartbeat (`power info` every 60s)")
    r("4. **Tool grouping:** By subsystem (subghz, nfc, rfid, storage, etc.)")
    r("5. **Risk gating:** Embed risk_level in tool metadata; Medium+ requires operator confirm")
    r("6. **Streaming:** Sub-GHz RX, NFC detect as async generators with teardown hooks")
    r("7. **State tracking:** Track active subsystem sessions, enforce single-active-stream")
    r("8. **Error handling:** Parse Flipper error patterns, retry on serial timeout, abort on disconnect")
    r("")

    rpt_path = os.path.join(OUTPUT_DIR, "flipper-capability-report.md")
    with open(rpt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    print(f"        Report: {len(report_lines)} lines")


# ============================================================
# Phase 4 — Filesystem Verification & Clean Disconnect
# ============================================================

def phase4(c2: FlipperC2, baseline: dict) -> None:
    """Re-capture filesystem state and diff against baseline."""
    print("\n" + "=" * 60)
    print("  PHASE 4 — FILESYSTEM VERIFICATION")
    print("=" * 60)

    diffs = []

    for path in ["/ext", "/int"]:
        info_raw = c2.send(f"storage info {path}", timeout=10)
        info = parse_kv(info_raw)
        baseline_info = baseline.get(f"{path}_info", {})

        # Compare free space
        for key in info:
            base_val = baseline_info.get(key, "")
            if base_val and base_val != info[key] and key != "_raw":
                diffs.append(f"  {path} {key}: {base_val} -> {info[key]}")

    diff_path = os.path.join(OUTPUT_DIR, "filesystem-diff.txt")
    with open(diff_path, "w", encoding="utf-8") as f:
        f.write(f"# Filesystem Diff — {datetime.now(timezone.utc).isoformat()}\n\n")
        if diffs:
            f.write("Changes detected:\n")
            for d in diffs:
                f.write(d + "\n")
        else:
            f.write("Filesystem verified clean — no action required\n")

    status = "CLEAN" if not diffs else f"{len(diffs)} changes"
    print(f"  Filesystem status: {status}")
    print(f"  Diff saved: {diff_path}")


# ============================================================
# Main
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="Flipper Zero C2 Reconnaissance")
    parser.add_argument("--port", type=str, help="COM port (auto-detect if omitted)")
    parser.add_argument("--baud", type=int, default=115200, help="Baud rate (default: 115200)")
    args = parser.parse_args()

    port = args.port or detect_port()
    if not port:
        print("❌ Flipper Zero not found. Connect via USB or use --port.")
        sys.exit(1)
    print(f"🎯 Target: {port} @ {args.baud} baud")

    # Init session log
    log = SessionLog(os.path.join(OUTPUT_DIR, "session-log.txt"))
    c2 = FlipperC2(port, args.baud, log)

    start_time = time.time()

    try:
        # Connect
        if not c2.connect():
            sys.exit(1)
        if not c2.validate_session():
            print("❌ CLI session validation failed. Device may be busy or in wrong mode.")
            sys.exit(1)

        # Phase 0
        p0 = phase0(c2)

        # Phase 1
        p1 = phase1(c2, p0)

        # Phase 2
        p2 = phase2(p1)

        # Phase 3
        phase3(p0, p1, p2)

        # Phase 4
        phase4(c2, p0.get("filesystem", {}))

    except KeyboardInterrupt:
        print("\n⚡ Interrupted — saving partial data...")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        c2.disconnect()
        log.close()

    elapsed = round(time.time() - start_time, 1)
    print(f"\n{'=' * 60}")
    print(f"  RECON COMPLETE — {elapsed}s elapsed")
    print(f"  Output: {OUTPUT_DIR}")
    print(f"{'=' * 60}")

    # List deliverables
    for fname in ["flipper-capability-report.md", "mcp-tool-schemas.json",
                   "transport-config.json", "command-tree.json",
                   "session-log.txt", "baseline-fs.json", "filesystem-diff.txt"]:
        fpath = os.path.join(OUTPUT_DIR, fname)
        exists = "✅" if os.path.exists(fpath) else "❌"
        print(f"  {exists} {fname}")


if __name__ == "__main__":
    main()
