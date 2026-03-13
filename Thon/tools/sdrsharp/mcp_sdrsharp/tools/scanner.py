"""SDR MCP Server — Band scanning and signal detection tools."""

from config import DEFAULT_GAIN, DEFAULT_SCAN_INTEGRATION, DEFAULT_SCAN_STEP
from tools.capture import _scan_spectrum
from tools.frequency import validate_frequency
from tools.reference import lookup_band


def scan_band(
    start_hz: int,
    stop_hz: int,
    step_hz: int = DEFAULT_SCAN_STEP,
    gain: int = DEFAULT_GAIN,
    integration_sec: int = DEFAULT_SCAN_INTEGRATION,
) -> dict:
    """Scan a frequency band and return power spectrum data.

    Default step is 12.5 kHz (NFM channel spacing).
    """
    validate_frequency(start_hz)
    validate_frequency(stop_hz)
    if start_hz >= stop_hz:
        return {"error": f"start_hz ({start_hz}) must be less than stop_hz ({stop_hz})"}

    return _scan_spectrum(start_hz, stop_hz, step_hz, gain, integration_sec)


def find_signals(
    start_hz: int,
    stop_hz: int,
    threshold_db: float = -30.0,
    step_hz: int = DEFAULT_SCAN_STEP,
    gain: int = DEFAULT_GAIN,
    integration_sec: int = DEFAULT_SCAN_INTEGRATION,
) -> dict:
    """Scan a band and return only frequencies with power above threshold.

    Enriches results with band plan information where available.
    """
    scan = scan_band(start_hz, stop_hz, step_hz, gain, integration_sec)
    if "error" in scan:
        return scan

    bins = scan.get("bins", [])
    if not bins:
        return {"signals": [], "scan_bins": 0, "threshold_db": threshold_db}

    noise_floor = sum(b["power_db"] for b in bins) / len(bins)

    effective_threshold = max(threshold_db, noise_floor + 6)

    signals = []
    for b in bins:
        if b["power_db"] >= effective_threshold:
            band_info = lookup_band(b["freq_hz"])
            signals.append({
                "freq_hz": b["freq_hz"],
                "power_db": b["power_db"],
                "above_noise_db": round(b["power_db"] - noise_floor, 2),
                "band_name": band_info.get("band_name", "Unknown"),
                "service": band_info.get("mode", ""),
            })

    return {
        "signals": signals,
        "signal_count": len(signals),
        "scan_bins": len(bins),
        "noise_floor_db": round(noise_floor, 2),
        "threshold_used_db": round(effective_threshold, 2),
        "csv_path": scan.get("csv_path", ""),
    }
