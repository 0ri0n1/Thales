# SDR MCP Server

Model Context Protocol server for Software Defined Radio hardware control. Bypasses SDR# entirely — talks directly to RTL-SDR hardware via three vectors:

- **Vector B**: SpyServer TCP client (remote SDR access)
- **Vector C**: RTL-SDR CLI tools (rtl_power, rtl_fm, rtl_sdr, rtl_test)
- **Vector D**: Direct FFI via rtlsdr.dll (fallback)

## Prerequisites

### Hardware
- RTL-SDR USB dongle (RTL2832U-based, e.g. RTL-SDR Blog V3/V4)
- USB cable

### WinUSB Driver (Required)
The RTL-SDR needs the WinUSB driver instead of the default DVB-T driver.

1. Plug in your RTL-SDR dongle
2. Run Zadig (bundled at `../sdrsharp-x64/zadig.exe`)
3. Select **Options > List All Devices**
4. Find **Bulk-In, Interface (Interface 0)** in the dropdown
5. Set the target driver to **WinUSB**
6. Click **Replace Driver**

> If SDR# was working before, the driver is already installed.

### RTL-SDR CLI Tools (for Vector C)
These provide `rtl_test`, `rtl_sdr`, `rtl_fm`, and `rtl_power`:

1. Download from https://github.com/rtlsdrblog/rtl-sdr-blog/releases/latest
2. Extract the `Release.zip`
3. Add the `x64` folder to your system PATH
4. Verify: `rtl_test -t` should detect your device

### Sox (Optional, for WAV output)
The `sdr_demodulate` tool pipes through sox for WAV conversion:

```
winget install sox
```

Without sox, demodulated audio is saved as raw PCM.

### SpyServer (Optional, for Vector B)
For remote SDR access over the network:

1. Download SpyServer from https://airspy.com/download/
2. Edit `spyserver.config` to set your device and port (default 5555)
3. Start: `spyserver --config=spyserver.config`

## Installation

```bash
pip install mcp
```

The server has no additional Python dependencies beyond `mcp` (which provides FastMCP).

## Claude Desktop Configuration

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "sdr": {
      "command": "python",
      "args": ["E:\\Thales\\Thon\\tools\\sdrsharp\\mcp_sdrsharp\\server.py"]
    }
  }
}
```

## Tools (18 total)

### Hardware Management
| Tool | Description |
|------|-------------|
| `sdr_detect_devices` | Detect connected RTL-SDR devices |
| `sdr_get_device_info` | Get tuner type, supported gains, serial |
| `sdr_get_backend_status` | Check which SDR backends are available |

### Configuration
| Tool | Description |
|------|-------------|
| `sdr_get_current_config` | Read SDRSharp.config (read-only snapshot) |

### Capture & Demodulation (Vector C)
| Tool | Description |
|------|-------------|
| `sdr_capture_iq` | Capture raw IQ samples to binary file |
| `sdr_demodulate` | Demodulate RF to WAV audio (AM/NFM/WFM/USB/LSB) |
| `sdr_get_spectrum` | FFT power snapshot around a frequency |

### Scanning
| Tool | Description |
|------|-------------|
| `sdr_scan_spectrum` | Wideband power scan to CSV/JSON |
| `sdr_find_signals` | Detect active signals above noise floor |

### Band Plan & Reference
| Tool | Description |
|------|-------------|
| `sdr_lookup_band` | Identify band/service for a frequency |
| `sdr_get_band_plan` | Full frequency allocation database |

### SpyServer (Vector B)
| Tool | Description |
|------|-------------|
| `spy_connect` | Connect to SpyServer instance |
| `spy_set_frequency` | Tune remote SDR |
| `spy_set_gain` | Set remote RF gain |
| `spy_get_fft` | Get FFT spectrum data |
| `spy_stream_iq` | Stream IQ data to file |
| `spy_disconnect` | Disconnect from SpyServer |
| `spy_ping` | Check SpyServer latency |

## Usage Examples

```
# "What signals are active on UHF walkie-talkie frequencies?"
sdr_scan_spectrum(440000000, 450000000, 12500)

# "What band is 445.5 MHz?"
sdr_lookup_band(445500000)
# -> UHF Land Mobile, NFM

# "Record 10 seconds of audio at 445.5 MHz"
sdr_demodulate(445500000, mode="NFM", duration_sec=10)

# "Find all active signals between 430-470 MHz"
sdr_find_signals(430000000, 470000000)

# "Connect to the remote SDR on the Pi"
spy_connect("192.168.1.50", 5555)
spy_set_frequency(445500000)
spy_get_fft(1024)
```

## Output Directory

All captures, recordings, and scan results are saved to:
`E:\Thales\Thon\output\sdr\`

## Architecture

```
sdrsharp/
├── sdrsharp-x64/          <- SDR# binary directory (rtlsdr.dll, BandPlan.xml, etc.)
└── mcp_sdrsharp/          <- MCP server (this directory)
    ├── server.py          <- FastMCP entry point (stdio transport)
    ├── config.py          <- Paths (relative to ../sdrsharp-x64), defaults
    ├── sdr_client.py      <- Backend auto-detection (selects vector B/C/D)
    ├── tools/
    │   ├── hardware.py    <- Device detection with Zadig instructions
    │   ├── frequency.py   <- Config reader, frequency validation
    │   ├── capture.py     <- IQ capture, demodulation, spectrum
    │   ├── scanner.py     <- Band scanning, signal detection
    │   └── reference.py   <- BandPlan.xml + 35-entry fallback table
    ├── spyserver/
    │   └── client.py      <- SpyServer TCP protocol client
    └── README.md
```
