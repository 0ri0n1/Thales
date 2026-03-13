"""SDR MCP Server — Frequency management and config reading tools."""

import xml.etree.ElementTree as ET
from pathlib import Path

from config import (
    RTL_FREQ_MAX,
    RTL_FREQ_MIN,
    RTL_SAMPLE_RATE_MAP,
    SDRSHARP_CONFIG,
)


class FrequencyError(ValueError):
    pass


def validate_frequency(freq_hz: int) -> None:
    if not RTL_FREQ_MIN <= freq_hz <= RTL_FREQ_MAX:
        raise FrequencyError(
            f"Frequency {freq_hz} Hz is outside RTL-SDR range "
            f"({RTL_FREQ_MIN / 1e6:.0f}–{RTL_FREQ_MAX / 1e6:.0f} MHz)"
        )


def get_current_config(config_path: Path | None = None) -> dict:
    """Read the SDRSharp.config XML and extract current tuning state.

    This is read-only — it reflects the last state SDR# was closed with.
    """
    path = config_path or SDRSHARP_CONFIG
    if not path.exists():
        return {"error": f"SDRSharp.config not found at {path}"}

    tree = ET.parse(path)
    root = tree.getroot()

    kv: dict[str, str] = {}
    for elem in root.findall("add"):
        key = elem.get("key", "")
        val = elem.get("value", "")
        kv[key] = val

    sample_rate_raw = kv.get("sampleRate", "")
    sample_rate_value = "".join(c for c in sample_rate_raw if c.isdigit())

    rtl_sr_index = int(kv.get("rtl.sampleRate", "3"))
    rtl_actual_rate = RTL_SAMPLE_RATE_MAP.get(rtl_sr_index, 1_920_000)

    detector_map = {
        "0": "AM", "1": "SAM", "2": "NFM", "3": "WFM",
        "4": "LSB", "5": "USB", "6": "DSB", "7": "CW", "8": "RAW",
    }
    source_map = {
        "0": "WaveFile", "1": "SoundCard", "2": "AirspyHF+",
        "3": "Airspy", "4": "FunCube", "5": "RTL-SDR", "6": "SpyServer",
        "7": "IQFile", "8": "HackRF",
    }

    return {
        "center_freq_hz": int(kv.get("centerFrequency", "0")),
        "vfo_hz": int(kv.get("vfo", "0")),
        "detector_type": detector_map.get(kv.get("detectorType", "0"), "Unknown"),
        "detector_type_raw": int(kv.get("detectorType", "0")),
        "audio_sample_rate": int(sample_rate_value) if sample_rate_value else 0,
        "rtl_sample_rate_hz": rtl_actual_rate,
        "rtl_sample_rate_index": rtl_sr_index,
        "iq_source": source_map.get(kv.get("iqSource", "0"), "Unknown"),
        "iq_source_raw": int(kv.get("iqSource", "0")),
        "rtl_tuner_gain": float(kv.get("rtl.tunerGain", "0")),
        "rtl_tuner_agc": kv.get("rtl.tunerAgc", "False") == "True",
        "rtl_bias_tee": kv.get("rtl.biasTee", "False") == "True",
        "rtl_freq_correction_ppm": int(kv.get("rtl.frequencyCorrection", "0")),
        "rtl_offset_tuning": kv.get("rtl.offsetTuning", "False") == "True",
        "agc_enabled": kv.get("agcEnabled", "False") == "True",
        "theme": kv.get("theme", ""),
        "note": "Read-only snapshot of SDRSharp.config — does not control the SDR# GUI",
    }
