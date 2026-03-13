"""SDR MCP Server — Configuration and path constants."""

from pathlib import Path

SDRSHARP_DIR = Path(__file__).parent.parent / "sdrsharp-x64"
RTL_CLI_DIR = Path(r"E:\Thales\Thon\tools\rtl-sdr")
OUTPUT_DIR = Path(r"E:\Thales\Thon\output\sdr")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SDRSHARP_CONFIG = SDRSHARP_DIR / "SDRSharp.config"
BANDPLAN_XML = SDRSHARP_DIR / "BandPlan.xml"
RTLSDR_DLL = SDRSHARP_DIR / "rtlsdr.dll"
ZADIG_EXE = SDRSHARP_DIR / "zadig.exe"

RTL_FREQ_MIN = 24_000_000
RTL_FREQ_MAX = 1_766_000_000

DEFAULT_SAMPLE_RATE = 2_400_000
DEFAULT_GAIN = 40
DEFAULT_SCAN_STEP = 12_500
DEFAULT_SCAN_INTEGRATION = 10
DEFAULT_TIMEOUT = 30

DEMOD_MODES = {
    "AM":  "am",
    "NFM": "fm",
    "WFM": "wbfm",
    "USB": "usb",
    "LSB": "lsb",
}

RTL_SAMPLE_RATE_MAP = {
    0: 250_000,
    1: 1_024_000,
    2: 1_536_000,
    3: 1_920_000,
    4: 2_048_000,
    5: 2_400_000,
    6: 2_560_000,
    7: 2_880_000,
    8: 3_200_000,
}
