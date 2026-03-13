"""SDR MCP Server — IQ capture, demodulation, and spectrum tools."""

import csv
import shutil
import subprocess
import time
from pathlib import Path

from config import (
    DEFAULT_GAIN,
    DEFAULT_SAMPLE_RATE,
    DEFAULT_TIMEOUT,
    DEMOD_MODES,
    OUTPUT_DIR,
    RTL_CLI_DIR,
)
from tools.frequency import FrequencyError, validate_frequency


def _ensure_tool(name: str) -> str:
    """Find an RTL-SDR CLI tool: check known install dir first, then PATH."""
    local = RTL_CLI_DIR / f"{name}.exe"
    if local.exists():
        return str(local)
    path = shutil.which(name)
    if not path:
        raise FileNotFoundError(
            f"{name} not found at {RTL_CLI_DIR} or in PATH. Install rtl-sdr-blog tools: "
            "https://github.com/rtlsdrblog/rtl-sdr-blog/releases/latest"
        )
    return path


def capture_iq(
    freq_hz: int,
    duration_sec: float = 5.0,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
    gain: int = DEFAULT_GAIN,
    output_file: str | None = None,
) -> dict:
    """Capture raw IQ samples to a binary file.

    Returns metadata about the capture including file path and size.
    """
    validate_frequency(freq_hz)
    rtl_sdr = _ensure_tool("rtl_sdr")

    num_samples = int(sample_rate * duration_sec)
    if not output_file:
        ts = time.strftime("%Y%m%d_%H%M%S")
        output_file = str(OUTPUT_DIR / f"iq_{freq_hz}Hz_{ts}.bin")

    out_path = Path(output_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        rtl_sdr,
        "-f", str(freq_hz),
        "-s", str(sample_rate),
        "-n", str(num_samples),
        "-g", str(gain),
        str(out_path),
    ]

    timeout = max(DEFAULT_TIMEOUT, int(duration_sec) + 15)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return {"error": f"rtl_sdr timed out after {timeout}s — device may be in use"}

    if not out_path.exists():
        return {
            "error": "Capture file not created",
            "stderr": result.stderr.strip(),
            "returncode": result.returncode,
        }

    return {
        "file_path": str(out_path),
        "size_bytes": out_path.stat().st_size,
        "freq_hz": freq_hz,
        "sample_rate": sample_rate,
        "duration_sec": duration_sec,
        "num_samples": num_samples,
        "gain": gain,
        "format": "unsigned 8-bit IQ (interleaved I/Q)",
    }


def demodulate(
    freq_hz: int,
    mode: str = "NFM",
    duration_sec: float = 10.0,
    gain: int = DEFAULT_GAIN,
    squelch: int = 0,
    output_file: str | None = None,
) -> dict:
    """Demodulate an RF signal to a WAV audio file.

    Supported modes: AM, NFM, WFM, USB, LSB.
    """
    validate_frequency(freq_hz)
    mode_upper = mode.upper()
    if mode_upper not in DEMOD_MODES:
        return {"error": f"Unsupported mode '{mode}'. Valid: {list(DEMOD_MODES.keys())}"}

    rtl_fm = _ensure_tool("rtl_fm")

    if not output_file:
        ts = time.strftime("%Y%m%d_%H%M%S")
        output_file = str(OUTPUT_DIR / f"demod_{mode_upper}_{freq_hz}Hz_{ts}.wav")

    out_path = Path(output_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    bandwidth_map = {"AM": 10000, "NFM": 12500, "WFM": 200000, "USB": 3000, "LSB": 3000}
    bw = bandwidth_map.get(mode_upper, 12500)
    audio_rate = 48000 if mode_upper == "WFM" else 12500

    cmd = [
        rtl_fm,
        "-M", DEMOD_MODES[mode_upper],
        "-f", str(freq_hz),
        "-s", str(bw),
        "-g", str(gain),
    ]
    if squelch > 0:
        cmd.extend(["-l", str(squelch)])

    sox_path = shutil.which("sox")
    raw_path = out_path.with_suffix(".raw")

    timeout = max(DEFAULT_TIMEOUT, int(duration_sec) + 15)

    try:
        with open(raw_path, "wb") as raw_out:
            proc = subprocess.Popen(cmd, stdout=raw_out, stderr=subprocess.PIPE)
            try:
                proc.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                proc.terminate()
                proc.wait(timeout=5)
    except Exception as exc:
        return {"error": f"rtl_fm failed: {exc}"}

    if sox_path and raw_path.exists() and raw_path.stat().st_size > 0:
        sox_cmd = [
            sox_path,
            "-t", "raw", "-r", str(audio_rate), "-e", "signed", "-b", "16", "-c", "1",
            str(raw_path),
            str(out_path),
        ]
        try:
            subprocess.run(sox_cmd, capture_output=True, timeout=30)
            raw_path.unlink(missing_ok=True)
        except Exception:
            out_path = raw_path
    else:
        if raw_path.exists():
            out_path = raw_path

    if not out_path.exists() or out_path.stat().st_size == 0:
        stderr = proc.stderr.read().decode() if proc.stderr else ""
        return {"error": "Demodulation produced no output", "stderr": stderr}

    return {
        "file_path": str(out_path),
        "size_bytes": out_path.stat().st_size,
        "freq_hz": freq_hz,
        "mode": mode_upper,
        "duration_sec": duration_sec,
        "audio_rate": audio_rate,
        "gain": gain,
        "format": "WAV" if out_path.suffix == ".wav" else "raw signed 16-bit PCM",
        "note": "sox not found — raw PCM output" if out_path.suffix != ".wav" else None,
    }


def get_spectrum(
    freq_hz: int,
    span_hz: int = 1_000_000,
    step_hz: int = 12_500,
    gain: int = DEFAULT_GAIN,
    integration_sec: int = 10,
) -> dict:
    """Get a power spectrum snapshot around a center frequency.

    Returns an array of {freq_hz, power_db} entries.
    """
    validate_frequency(freq_hz)
    start = freq_hz - span_hz // 2
    stop = freq_hz + span_hz // 2

    if start < 24_000_000:
        start = 24_000_000
    if stop > 1_766_000_000:
        stop = 1_766_000_000

    return _scan_spectrum(start, stop, step_hz, gain, integration_sec)


def _scan_spectrum(
    start_hz: int,
    stop_hz: int,
    step_hz: int,
    gain: int,
    integration_sec: int,
) -> dict:
    rtl_power = _ensure_tool("rtl_power")

    ts = time.strftime("%Y%m%d_%H%M%S")
    csv_path = OUTPUT_DIR / f"spectrum_{start_hz}_{stop_hz}_{ts}.csv"

    freq_range = f"{start_hz}:{stop_hz}:{step_hz}"
    cmd = [
        rtl_power,
        "-f", freq_range,
        "-g", str(gain),
        "-i", str(integration_sec),
        "-1",
        str(csv_path),
    ]

    timeout = integration_sec + 60
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return {"error": f"rtl_power timed out after {timeout}s"}

    if not csv_path.exists() or csv_path.stat().st_size == 0:
        return {
            "error": "rtl_power produced no output",
            "stderr": result.stderr.strip(),
            "returncode": result.returncode,
        }

    return _parse_rtl_power_csv(csv_path)


def _parse_rtl_power_csv(csv_path: Path) -> dict:
    """Parse rtl_power CSV output into structured spectrum data.

    rtl_power CSV format:
    date, time, start_freq, stop_freq, step, samples, db1, db2, ...
    """
    bins = []
    try:
        with open(csv_path, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) < 7:
                    continue
                try:
                    start_freq = int(row[2].strip())
                    step = float(row[4].strip())
                    power_values = [float(v.strip()) for v in row[6:] if v.strip()]
                    for i, power_db in enumerate(power_values):
                        freq = start_freq + int(i * step)
                        bins.append({"freq_hz": freq, "power_db": round(power_db, 2)})
                except (ValueError, IndexError):
                    continue
    except Exception as exc:
        return {"error": f"Failed to parse CSV: {exc}", "csv_path": str(csv_path)}

    return {
        "bins": bins,
        "bin_count": len(bins),
        "csv_path": str(csv_path),
        "freq_range": f"{bins[0]['freq_hz']}–{bins[-1]['freq_hz']}" if bins else "empty",
    }
