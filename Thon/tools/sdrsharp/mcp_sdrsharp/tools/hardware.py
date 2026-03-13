"""SDR MCP Server — Hardware detection and device info tools."""

import shutil
import subprocess

from config import DEFAULT_TIMEOUT, RTL_CLI_DIR, ZADIG_EXE


def _find_rtl_tool(name: str) -> str | None:
    """Find an RTL-SDR CLI tool: check known install dir first, then PATH."""
    local = RTL_CLI_DIR / f"{name}.exe"
    if local.exists():
        return str(local)
    return shutil.which(name)


def _run_rtl(args: list[str], timeout: int = DEFAULT_TIMEOUT) -> subprocess.CompletedProcess:
    return subprocess.run(
        args,
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def detect_devices() -> dict:
    """Detect connected RTL-SDR devices.

    Returns a dict with device list or an error message with install instructions.
    """
    rtl_test = _find_rtl_tool("rtl_test")
    if not rtl_test:
        return {
            "error": "rtl_test not found",
            "install_instructions": (
                "Install rtl-sdr-blog tools:\n"
                "  1. Download from https://github.com/rtlsdrblog/rtl-sdr-blog/releases/latest\n"
                "  2. Extract and add the x64 folder to your system PATH\n"
                "  3. If the device isn't recognized, run Zadig to install WinUSB driver:\n"
                f"     {ZADIG_EXE}\n"
                "     Select 'Bulk-In, Interface (Interface 0)' > WinUSB > Replace Driver"
            ),
        }

    try:
        result = _run_rtl([rtl_test, "-t"], timeout=10)
    except subprocess.TimeoutExpired:
        return {"error": "rtl_test timed out after 10s — device may be in use by another application"}

    output = result.stdout + result.stderr
    devices = []

    for line in output.splitlines():
        if "Found" in line and "device" in line.lower():
            devices.append(line.strip())
        elif "Using device" in line:
            devices.append(line.strip())
        elif "Tuner type:" in line:
            devices.append(line.strip())

    if not devices and result.returncode != 0:
        return {
            "error": "No RTL-SDR devices found",
            "stderr": result.stderr.strip(),
            "troubleshooting": (
                "Check:\n"
                "  1. USB cable is connected\n"
                "  2. WinUSB driver is installed (run Zadig)\n"
                "  3. No other application (SDR#, rtl_tcp) is using the device\n"
                f"  Zadig location: {ZADIG_EXE}"
            ),
        }

    return {
        "devices": devices,
        "raw_output": output.strip(),
        "device_count": len([d for d in devices if "Found" in d or "Using device" in d]),
    }


def get_device_info() -> dict:
    """Get detailed info about the first RTL-SDR device (tuner type, gains, serial)."""
    rtl_test = _find_rtl_tool("rtl_test")
    if not rtl_test:
        return {"error": "rtl_test not found in PATH. See sdr_detect_devices() for install instructions."}

    try:
        result = _run_rtl([rtl_test, "-t"], timeout=10)
    except subprocess.TimeoutExpired:
        return {"error": "rtl_test timed out — device may be in use"}

    output = result.stdout + result.stderr
    info: dict = {"raw_output": output.strip()}

    for line in output.splitlines():
        stripped = line.strip()
        if "Tuner type:" in stripped:
            info["tuner_type"] = stripped.split(":", 1)[1].strip()
        elif "Supported gain values" in stripped:
            gains_str = stripped.split(":", 1)[1].strip()
            info["supported_gains"] = [
                float(g.strip()) for g in gains_str.split(",") if g.strip()
            ]
        elif "Using device" in stripped:
            info["device_name"] = stripped.split(":", 1)[1].strip() if ":" in stripped else stripped

    return info
