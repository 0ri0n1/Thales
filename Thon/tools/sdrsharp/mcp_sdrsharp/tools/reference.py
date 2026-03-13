"""SDR MCP Server — Band plan lookup and RF reference tools."""

import xml.etree.ElementTree as ET
from pathlib import Path

from config import BANDPLAN_XML

FALLBACK_BANDS = [
    {"min": 150_000, "max": 280_000, "name": "Longwave Broadcast", "mode": "AM"},
    {"min": 530_000, "max": 1_700_000, "name": "Mediumwave Broadcast", "mode": "AM"},
    {"min": 1_800_000, "max": 2_000_000, "name": "160m Ham Band", "mode": "LSB"},
    {"min": 3_500_000, "max": 3_800_000, "name": "80m Ham Band", "mode": "LSB"},
    {"min": 7_000_000, "max": 7_200_000, "name": "40m Ham Band", "mode": "LSB"},
    {"min": 14_000_000, "max": 14_350_000, "name": "20m Ham Band", "mode": "USB"},
    {"min": 21_000_000, "max": 21_450_000, "name": "15m Ham Band", "mode": "USB"},
    {"min": 26_960_000, "max": 27_410_000, "name": "Citizens Band (CB)", "mode": "AM"},
    {"min": 28_000_000, "max": 29_750_000, "name": "10m Ham Band", "mode": "USB"},
    {"min": 50_000_000, "max": 54_000_000, "name": "6m Ham Band", "mode": "USB"},
    {"min": 87_500_000, "max": 108_000_000, "name": "FM Broadcast", "mode": "WFM"},
    {"min": 108_000_000, "max": 118_000_000, "name": "Aircraft VOR/ILS", "mode": "AM"},
    {"min": 118_000_000, "max": 137_000_000, "name": "Aircraft Voice", "mode": "AM"},
    {"min": 144_000_000, "max": 148_000_000, "name": "2m Ham Band", "mode": "NFM"},
    {"min": 155_750_000, "max": 162_950_000, "name": "Marine Band", "mode": "NFM"},
    {"min": 174_000_000, "max": 222_000_000, "name": "DAB Broadcast", "mode": "WFM"},
    {"min": 222_000_000, "max": 225_000_000, "name": "1.25m Ham Band", "mode": "NFM"},
    {"min": 240_000_000, "max": 270_000_000, "name": "Military Satellite", "mode": "NFM"},
    {"min": 270_000_000, "max": 380_000_000, "name": "Military Aircraft", "mode": "NFM"},
    {"min": 400_000_000, "max": 420_000_000, "name": "Government/Federal", "mode": "NFM"},
    {"min": 420_000_000, "max": 430_000_000, "name": "Federal Radiolocation", "mode": "NFM"},
    {"min": 430_000_000, "max": 440_000_000, "name": "70cm Ham Band", "mode": "NFM"},
    {"min": 440_000_000, "max": 450_000_000, "name": "UHF Land Mobile", "mode": "NFM"},
    {"min": 450_000_000, "max": 470_000_000, "name": "UHF Land Mobile / FRS/GMRS", "mode": "NFM"},
    {"min": 446_000_000, "max": 446_200_000, "name": "PMR446", "mode": "NFM"},
    {"min": 462_562_500, "max": 462_725_000, "name": "FRS/GMRS", "mode": "NFM"},
    {"min": 470_000_000, "max": 512_000_000, "name": "UHF TV / Public Safety", "mode": "NFM"},
    {"min": 806_000_000, "max": 869_000_000, "name": "Public Safety / Cellular", "mode": "NFM"},
    {"min": 869_000_000, "max": 894_000_000, "name": "Cellular (Downlink)", "mode": "NFM"},
    {"min": 902_000_000, "max": 928_000_000, "name": "ISM 900 MHz", "mode": "NFM"},
    {"min": 935_000_000, "max": 960_000_000, "name": "GSM 900 (Downlink)", "mode": "NFM"},
    {"min": 1_090_000_000, "max": 1_090_000_000, "name": "ADS-B Aircraft Tracking", "mode": "RAW"},
    {"min": 1_240_000_000, "max": 1_325_000_000, "name": "23cm Ham Band", "mode": "NFM"},
    {"min": 1_525_000_000, "max": 1_559_000_000, "name": "Inmarsat/GPS L1", "mode": "RAW"},
    {"min": 1_575_420_000, "max": 1_575_420_000, "name": "GPS L1", "mode": "RAW"},
]


def _load_bandplan(xml_path: Path | None = None) -> list[dict]:
    """Load band plan from BandPlan.xml, then merge in any fallback entries
    that cover frequency ranges not present in the XML source."""
    path = xml_path or BANDPLAN_XML
    xml_bands: list[dict] = []

    if path.exists():
        try:
            tree = ET.parse(path)
            root = tree.getroot()
            for entry in root.findall("RangeEntry"):
                xml_bands.append({
                    "min": int(entry.get("minFrequency", "0")),
                    "max": int(entry.get("maxFrequency", "0")),
                    "name": entry.text or "Unknown",
                    "mode": entry.get("mode", ""),
                    "step": int(entry.get("step", "0")),
                    "color": entry.get("color", ""),
                })
        except Exception:
            pass

    if not xml_bands:
        return FALLBACK_BANDS

    xml_ranges = {(b["min"], b["max"]) for b in xml_bands}
    for fb in FALLBACK_BANDS:
        if (fb["min"], fb["max"]) not in xml_ranges:
            covered = any(
                xb["min"] <= fb["min"] and xb["max"] >= fb["max"]
                for xb in xml_bands
            )
            if not covered:
                xml_bands.append(fb)

    xml_bands.sort(key=lambda b: b["min"])
    return xml_bands


def lookup_band(freq_hz: int) -> dict:
    """Look up which radio band/service a frequency belongs to.

    Parses BandPlan.xml from the SDR# directory, with fallback to an embedded table.
    """
    bands = _load_bandplan()
    matches = []
    for band in bands:
        if band["min"] <= freq_hz <= band["max"]:
            matches.append({
                "band_name": band["name"],
                "mode": band.get("mode", ""),
                "freq_range_hz": f"{band['min']}–{band['max']}",
                "freq_range_mhz": f"{band['min'] / 1e6:.3f}–{band['max'] / 1e6:.3f} MHz",
                "step_hz": band.get("step", 0),
            })

    if not matches:
        return {
            "band_name": "Unknown / Unallocated",
            "freq_hz": freq_hz,
            "freq_mhz": f"{freq_hz / 1e6:.3f} MHz",
            "note": "Frequency not found in band plan database",
        }

    if len(matches) == 1:
        result = matches[0]
        result["freq_hz"] = freq_hz
        result["freq_mhz"] = f"{freq_hz / 1e6:.3f} MHz"
        return result

    result = matches[0]
    result["freq_hz"] = freq_hz
    result["freq_mhz"] = f"{freq_hz / 1e6:.3f} MHz"
    result["additional_allocations"] = matches[1:]
    return result


def get_band_plan() -> dict:
    """Return the full band plan database."""
    bands = _load_bandplan()
    return {
        "bands": [
            {
                "name": b["name"],
                "mode": b.get("mode", ""),
                "min_hz": b["min"],
                "max_hz": b["max"],
                "min_mhz": f"{b['min'] / 1e6:.3f}",
                "max_mhz": f"{b['max'] / 1e6:.3f}",
            }
            for b in bands
        ],
        "band_count": len(bands),
        "source": str(BANDPLAN_XML) if BANDPLAN_XML.exists() else "embedded fallback table",
    }
