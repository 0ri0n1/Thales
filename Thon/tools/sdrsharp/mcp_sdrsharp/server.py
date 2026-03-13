"""SDR MCP Server — FastMCP entry point.

Controls SDR hardware via three vectors:
  B: SpyServer TCP client (remote SDR access)
  C: RTL-SDR CLI tools (rtl_power, rtl_fm, rtl_sdr, rtl_test)
  D: Direct FFI via rtlsdr.dll (future)

Bypasses SDR# entirely — talks to hardware directly.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from mcp.server.fastmcp import FastMCP

from config import RTL_FREQ_MAX, RTL_FREQ_MIN
from sdr_client import detect_backend
from spyserver.client import SpyServerClient
from tools.capture import capture_iq, demodulate, get_spectrum
from tools.frequency import FrequencyError, get_current_config
from tools.hardware import detect_devices, get_device_info
from tools.reference import get_band_plan, lookup_band
from tools.scanner import find_signals, scan_band

mcp = FastMCP(
    "sdr",
    instructions=(
        "SDR (Software Defined Radio) MCP Server. Controls RTL-SDR hardware for "
        "spectrum scanning, signal demodulation, IQ capture, and band identification. "
        f"Frequency range: {RTL_FREQ_MIN / 1e6:.0f}–{RTL_FREQ_MAX / 1e6:.0f} MHz. "
        "Supports RTL-SDR via CLI tools and SpyServer for remote access."
    ),
)

_spy_client: SpyServerClient | None = None


# ═══════════════════════════════════════════════════════
# Hardware Management
# ═══════════════════════════════════════════════════════

@mcp.tool()
def sdr_detect_devices() -> dict:
    """Detect connected RTL-SDR devices. Returns device list or install instructions if rtl-sdr tools are missing."""
    return detect_devices()


@mcp.tool()
def sdr_get_device_info() -> dict:
    """Get detailed info about the RTL-SDR device — tuner type, supported gains, serial number."""
    return get_device_info()


@mcp.tool()
def sdr_get_backend_status() -> dict:
    """Check which SDR backends are available: SpyServer (remote), RTL CLI tools (local), FFI (direct).

    Returns the active vector and availability of each backend.
    """
    return detect_backend().__dict__


# ═══════════════════════════════════════════════════════
# Configuration (read-only)
# ═══════════════════════════════════════════════════════

@mcp.tool()
def sdr_get_current_config() -> dict:
    """Read the SDRSharp.config file to see the last-known tuning state.

    This is read-only — it shows what SDR# was configured to when it last closed.
    Returns: center frequency, mode (AM/NFM/etc.), sample rate, gain, IQ source.
    """
    return get_current_config()


# ═══════════════════════════════════════════════════════
# Tuning & Capture (Vector C — RTL CLI)
# ═══════════════════════════════════════════════════════

@mcp.tool()
def sdr_capture_iq(freq_hz: int, duration_sec: float = 5.0, gain: int = 40) -> dict:
    """Capture raw IQ samples from the RTL-SDR at a given frequency.

    Args:
        freq_hz: Center frequency in Hz (24 MHz – 1766 MHz)
        duration_sec: Capture duration in seconds (default 5)
        gain: RF gain in dB (default 40)

    Returns: File path, size, sample rate, and capture metadata.
    """
    try:
        return capture_iq(freq_hz, duration_sec=duration_sec, gain=gain)
    except FrequencyError as exc:
        return {"error": str(exc)}
    except FileNotFoundError as exc:
        return {"error": str(exc)}


@mcp.tool()
def sdr_demodulate(freq_hz: int, mode: str = "NFM", duration_sec: float = 10.0, gain: int = 40, squelch: int = 0) -> dict:
    """Demodulate an RF signal to a WAV audio file.

    Args:
        freq_hz: Frequency in Hz (24 MHz – 1766 MHz)
        mode: Demodulation mode — AM, NFM, WFM, USB, or LSB
        duration_sec: Recording duration in seconds (default 10)
        gain: RF gain in dB (default 40)
        squelch: Squelch level (0 = off)

    Returns: WAV file path and metadata. Requires sox for WAV conversion.
    """
    try:
        return demodulate(freq_hz, mode=mode, duration_sec=duration_sec, gain=gain, squelch=squelch)
    except FrequencyError as exc:
        return {"error": str(exc)}
    except FileNotFoundError as exc:
        return {"error": str(exc)}


@mcp.tool()
def sdr_scan_spectrum(start_hz: int, stop_hz: int, step_hz: int = 12500, gain: int = 40) -> dict:
    """Scan a frequency band and return power spectrum data.

    Args:
        start_hz: Start frequency in Hz
        stop_hz: Stop frequency in Hz
        step_hz: Frequency step in Hz (default 12500 = 12.5 kHz NFM channel spacing)
        gain: RF gain in dB (default 40)

    Returns: Array of {freq_hz, power_db} bins, plus CSV file path.
    """
    try:
        return scan_band(start_hz, stop_hz, step_hz=step_hz, gain=gain)
    except FrequencyError as exc:
        return {"error": str(exc)}
    except FileNotFoundError as exc:
        return {"error": str(exc)}


@mcp.tool()
def sdr_find_signals(start_hz: int, stop_hz: int, threshold_db: float = -30.0, step_hz: int = 12500) -> dict:
    """Scan a band and find active signals above a power threshold.

    Automatically calculates noise floor and filters. Results enriched with
    band plan info (band name, typical service, recommended mode).

    Args:
        start_hz: Start frequency in Hz
        stop_hz: Stop frequency in Hz
        threshold_db: Minimum power in dB (default -30). Adaptive — will use noise_floor + 6 dB if higher.
        step_hz: Scan step in Hz (default 12500)

    Returns: List of detected signals with frequency, power, and band identification.
    """
    try:
        return find_signals(start_hz, stop_hz, threshold_db=threshold_db, step_hz=step_hz)
    except FrequencyError as exc:
        return {"error": str(exc)}
    except FileNotFoundError as exc:
        return {"error": str(exc)}


@mcp.tool()
def sdr_get_spectrum(freq_hz: int, span_hz: int = 1000000) -> dict:
    """Get a power spectrum snapshot centered on a frequency.

    Args:
        freq_hz: Center frequency in Hz
        span_hz: Bandwidth span in Hz (default 1 MHz)

    Returns: Array of {freq_hz, power_db} bins centered on the target frequency.
    """
    try:
        return get_spectrum(freq_hz, span_hz=span_hz)
    except FrequencyError as exc:
        return {"error": str(exc)}
    except FileNotFoundError as exc:
        return {"error": str(exc)}


# ═══════════════════════════════════════════════════════
# Band Plan & Reference
# ═══════════════════════════════════════════════════════

@mcp.tool()
def sdr_lookup_band(freq_hz: int) -> dict:
    """Look up which radio band and service a frequency belongs to.

    Uses the SDR# BandPlan.xml database with fallback to an embedded reference table
    covering HF through UHF allocations.

    Args:
        freq_hz: Frequency to look up in Hz

    Returns: Band name, service type, frequency range, recommended demod mode.
    """
    return lookup_band(freq_hz)


@mcp.tool()
def sdr_get_band_plan() -> dict:
    """Get the full band plan database — all known frequency allocations.

    Returns a list of bands with name, frequency range, and recommended mode.
    """
    return get_band_plan()


# ═══════════════════════════════════════════════════════
# SpyServer (Vector B — Remote SDR)
# ═══════════════════════════════════════════════════════

@mcp.tool()
def spy_connect(host: str = "127.0.0.1", port: int = 5555) -> dict:
    """Connect to a SpyServer instance for remote SDR access.

    SpyServer is a network streaming protocol that provides remote access to
    SDR hardware. It must be running on a machine with the SDR device.

    Requires SpyServer to be installed and running. Download from:
    https://airspy.com/download/

    Args:
        host: SpyServer hostname or IP (default 127.0.0.1)
        port: SpyServer port (default 5555)
    """
    global _spy_client
    _spy_client = SpyServerClient(host=host, port=port)
    return _spy_client.connect()


@mcp.tool()
def spy_set_frequency(freq_hz: int) -> dict:
    """Set the center frequency on the remote SDR via SpyServer.

    Args:
        freq_hz: Center frequency in Hz

    Requires an active SpyServer connection (call spy_connect first).
    """
    if not _spy_client:
        return {"error": "Not connected. Call spy_connect() first."}
    return _spy_client.set_frequency(freq_hz)


@mcp.tool()
def spy_set_gain(gain: int) -> dict:
    """Set RF gain on the remote SDR via SpyServer.

    Args:
        gain: Gain index (range depends on hardware — see spy_connect device_info)

    Requires an active SpyServer connection.
    """
    if not _spy_client:
        return {"error": "Not connected. Call spy_connect() first."}
    return _spy_client.set_gain(gain)


@mcp.tool()
def spy_get_fft(pixels: int = 1024) -> dict:
    """Get FFT spectrum data from SpyServer.

    Returns an array of FFT magnitude bins representing the current spectrum.

    Args:
        pixels: Number of FFT bins / display pixels (100 – 32768, default 1024)

    Requires an active SpyServer connection.
    """
    if not _spy_client:
        return {"error": "Not connected. Call spy_connect() first."}
    return _spy_client.get_fft(pixels=pixels)


@mcp.tool()
def spy_stream_iq(duration_sec: float = 1.0) -> dict:
    """Stream IQ data from SpyServer and save to file.

    Args:
        duration_sec: Duration to stream in seconds (default 1.0)

    Requires an active SpyServer connection.
    """
    if not _spy_client:
        return {"error": "Not connected. Call spy_connect() first."}
    return _spy_client.stream_iq(duration_sec=duration_sec)


@mcp.tool()
def spy_disconnect() -> dict:
    """Disconnect from SpyServer."""
    global _spy_client
    if not _spy_client:
        return {"status": "not_connected"}
    result = _spy_client.disconnect()
    _spy_client = None
    return result


@mcp.tool()
def spy_ping() -> dict:
    """Ping the SpyServer to check latency and connectivity.

    Requires an active SpyServer connection.
    """
    if not _spy_client:
        return {"error": "Not connected. Call spy_connect() first."}
    return _spy_client.ping()


if __name__ == "__main__":
    mcp.run()
