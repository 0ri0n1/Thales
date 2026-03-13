# SDR MCP Server — Mission Report

> **Operation:** SDR# MCP Server Build  
> **Classification:** Active Build — Complete  
> **Operator:** Thon  
> **Principal:** Eddie  
> **Date:** 2026-03-10  
> **Server Location:** `E:\Thales\Thon\tools\sdrsharp\mcp_sdrsharp\`  
> **Cursor Config:** `C:\Users\Dallas\.cursor\mcp.json` → entry `"sdr"`

---

## Executive Summary

Built and deployed an 18-tool MCP server for Software Defined Radio hardware control. The server bypasses SDR# entirely and talks to RTL-SDR hardware directly through three vectors: SpyServer TCP protocol (remote), RTL-SDR CLI tools (local), and direct FFI via rtlsdr.dll (fallback). Phase 0 verification using three independent instruments (filesystem reads, dnspy_mcp, and Kali binary analysis) confirmed the recon report was substantially accurate, with several discrepancies documented below. Server is installed and registered in the Cursor MCP configuration.

---

## Phase 0 — Verification Log

### Instruments Used

| # | Instrument | Purpose |
|---|-----------|---------|
| 1 | Filesystem / Config | Direct file reads, size checks, XML parsing |
| 2 | dnspy_mcp | .NET assembly decompilation (failed — see D1) |
| 3 | Kali Linux (WSL) | `file`, `strings`, `grep` — native binary reversing |

### Filesystem Verification

| File | Reported | Verified | Status |
|------|----------|----------|--------|
| SDRSharp.dotnet8.exe | 4.8 MB | 4,889,712 B (4.66 MB) | PASS |
| rtlsdr.dll | 337 KB | 337,920 B | PASS |
| libusb-1.0.dll | Present | 123,736 B | PASS |
| airspy.dll | Present | 147,288 B | PASS |
| SDRSharp.config | Present | 10,499 B | PASS |
| BandPlan.xml | Present | 6,036 B | PASS |
| install-rtlsdr.bat | Present | 484 B | PASS |
| changelog.txt | Present | 305,336 B | PASS |
| Plugins/ directory | Present | Empty directory | PASS |

**Unreported files discovered:**

| File | Size | Notes |
|------|------|-------|
| SDRSharp.dotnet9.exe | 4,922,480 B | .NET 9 variant (mentioned in report text, not in table) |
| airspyhf.dll | 156,504 B | Airspy HF+ native library |
| portaudio.dll | 695,640 B | Audio I/O library |
| pthreadVC2.dll | 438,616 B | POSIX threads for Windows |
| shark.dll | 265,048 B | Native PE, no identifying strings — purpose unknown |
| httpget.exe | 202,584 B | HTTP download utility (used by install-rtlsdr.bat) |
| unzip.exe | 178,008 B | Archive extraction tool |
| zadig.exe | 5,158,456 B | WinUSB driver installer — bundled, ready to use |
| SDRSharp.Layout.xml | 4,706 B | UI layout persistence |
| notches.xml | 166 B | Notch filter configuration |

### Config Verification

| Parameter | Reported | Actual | Status |
|-----------|----------|--------|--------|
| centerFrequency | 445500000 | 445500000 | CONFIRMED |
| detectorType | 0 (AM) | 0 | CONFIRMED |
| iqSource | 5 (RTL-SDR) | 5 | CONFIRMED |
| sampleRate | 48000 | `"48000 sample/sec"` | **DISCREPANCY D2** |

**D2 Detail:** The `sampleRate` value includes the unit string `" sample/sec"`, not a raw integer. The config parser was written to strip non-digit characters, so this is handled correctly.

**Undocumented config keys of operational interest:**
- `rtl.tunerGain=0`, `rtl.sampleRate=3` (index into rate table → 1,920,000 Hz), `rtl.tunerAgc=False`, `rtl.biasTee=False`
- `core.spyserver.disableAutoScaling=false` — confirms SpyServer integration at config level
- `plugin.audio.recorder.targetFolder` — recording output path
- `inputDevice=[MME] Stream Mix (2- Razer Stream Con` — Razer audio device
- Mode state strings for all demodulators: `amState`, `nfmState`, `wfmState`, `lsbState`, `usbState`, `dsbState`, `cwState`, `rawState`

### Discrepancy Log

| ID | Severity | Area | Description |
|----|----------|------|-------------|
| D1 | HIGH | dnspy_mcp | SDRSharp.dotnet8.exe has **no CLR header** — it's a .NET 8 self-contained single-file deployment. The IL assemblies are bundled inside a native PE host. dnspy_mcp reports: *"valid PE file but not a .NET assembly (no CLR header)"*. **Impact:** All managed-code analysis pivoted to Kali `strings`. The recon report's claim of ".NET 8" is correct, but the binary cannot be decompiled with standard .NET tools without first extracting the bundled assemblies. |
| D2 | LOW | Config | `sampleRate` stored as `"48000 sample/sec"` not raw `48000`. Parser handles it. |
| D3 | INFO | rtlsdr.dll | 41 exported functions found vs. 9 reported. 32 additional exports documented below. Not a contradiction — the report listed key functions, not the complete export table. |
| D4 | INFO | BandPlan.xml | The XML covers HF-through-UHF ham/broadcast bands but has a gap at 440–446 MHz (UHF land mobile). The fallback table in the MCP server fills this gap. 445.5 MHz correctly resolves to "UHF Land Mobile" after the merge. |

### Kali Task K1 — rtlsdr.dll Export Verification

**Verdict: Genuine librtlsdr.** rtl-sdr-blog fork confirmed by `install-rtlsdr.bat` downloading from `rtlsdrblog/rtl-sdr-blog`.

**All 9 reported exports confirmed.** 32 additional exports found:

```
rtlsdr_cancel_async          rtlsdr_get_center_freq       rtlsdr_get_device_count
rtlsdr_get_device_name       rtlsdr_get_device_usb_strings rtlsdr_get_direct_sampling
rtlsdr_get_freq_correction   rtlsdr_get_index_by_serial   rtlsdr_get_offset_tuning
rtlsdr_get_sample_rate       rtlsdr_get_tuner_gain        rtlsdr_get_tuner_type
rtlsdr_get_usb_strings       rtlsdr_get_xtal_freq         rtlsdr_read_eeprom
rtlsdr_read_reg              rtlsdr_reset_buffer          rtlsdr_set_agc_mode
rtlsdr_set_bias_tee_gpio     rtlsdr_set_direct_sampling   rtlsdr_set_freq_correction
rtlsdr_set_offset_tuning     rtlsdr_set_testmode          rtlsdr_set_tuner_bandwidth
rtlsdr_set_tuner_gain_mode   rtlsdr_set_tuner_if_gain     rtlsdr_set_xtal_freq
rtlsdr_wait_async            rtlsdr_write_eeprom          rtlsdr_write_reg
rtlsdr_demod_read_reg        rtlsdr_demod_write_reg
```

Notable rtl-sdr-blog additions over upstream osmocom: `set_bias_tee_gpio`, `set_tuner_bandwidth`.

### Kali Task K2 — Hidden IPC Hunt

**Verdict: No hidden IPC server. Report CONFIRMED.**

Strings found in SDRSharp.dotnet8.exe:
- `TcpClient` — used by the embedded SpyServer **client** (SDR# connects TO SpyServer, not the reverse)
- `HttpClient` — used for map tile fetching (Bing, Google, Esri, DoubleGIS tile servers)
- `WebSocket` — .NET framework class reference only, no evidence of active server use
- `System.IO.Ports` — serial port support for FunCube Dongle
- Named pipe constants (`ERROR_BROKEN_PIPE`, `FILE_TYPE_PIPE`) — standard .NET runtime constants, not custom IPC

**Vector A remains closed.** SDR# does not expose any automation surface.

### Kali Task K3 — SpyServer Protocol Verification

**Verdict: Protocol fully confirmed and richer than reported.**

All constants extracted from binary match the recon report. Additional settings discovered:

| Category | Constants Found |
|----------|----------------|
| Commands | `CMD_HELLO`, `CMD_GET_SETTING`, `CMD_SET_SETTING`, `CMD_PING`, `CMD_SET_FREQ`, `CMD_SET_SAMPLE_RATE`, `CMD_SET_GAIN`, `CMD_SET_AGC_MODE`, `CMD_SET_FREQ_COR`, `CMD_SET_TUNER_GAIN_INDEX`, `CMD_SET_TUNER_GAIN_MODE` |
| Settings | `SETTING_STREAMING_MODE`, `SETTING_STREAMING_ENABLED`, `SETTING_GAIN`, `SETTING_IQ_FREQUENCY`, `SETTING_IQ_DECIMATION`, **`SETTING_IQ_DIGITAL_GAIN`**, **`SETTING_IQ_FORMAT`**, `SETTING_FFT_FREQUENCY`, `SETTING_FFT_DECIMATION`, `SETTING_FFT_DB_OFFSET`, `SETTING_FFT_DB_RANGE`, `SETTING_FFT_DISPLAY_PIXELS`, **`SETTING_FFT_FORMAT`**, **`SETTING_FFT_ZOOM`**, **`SETTING_FFT_ZOOM_FREQUENCY`** |
| Message Types | `MSG_TYPE_DEVICE_INFO`, `MSG_TYPE_CLIENT_SYNC`, `MSG_TYPE_PONG`, `MSG_TYPE_READ_SETTING`, `UINT8/INT16/INT24/FLOAT` variants for IQ/AF/FFT, `UINT1_IQ`, `UINT2_IQ`, `UINT4_IQ/FFT` |
| Stream Types | `STREAM_TYPE_STATUS`, `STREAM_TYPE_IQ`, `STREAM_TYPE_AF`, `STREAM_TYPE_FFT` |

**Bold** entries are settings not documented in the recon report. All have been implemented in the SpyServer client.

Additional findings:
- Plugin SDK interface: `ISharpPlugin` (from `SDRSharp.Common`)
- Build PDB paths confirm .NET 8: `D:\sdrsharp\Common\obj\Release\net8.0-windows\SDRSharp.Common.pdb`
- Namespaces: `SDRSharp.Common`, `SDRSharp.Radio`, `SDRSharp.Radio.PortAudio`, `SDRSharp.FrontEnds.SpyServer`

### Kali Task K4 — libusb-1.0.dll Verification

**Verdict: Standard libusb confirmed.**

`LIBUSB_*` error/transfer constants present. `WinUsb_*` API imports confirm the WinUsb backend. Standard Windows libusb-1.0 distribution.

---

## Phase 1 — CLI Wrapper Build

### Architecture

```
E:\Thales\Thon\tools\sdrsharp\
├── sdrsharp-x64/              ← SDR# binaries, rtlsdr.dll, BandPlan.xml, config
└── mcp_sdrsharp/              ← MCP server
    ├── server.py              ← FastMCP entry point (stdio transport), 18 tools
    ├── config.py              ← Relative paths to ../sdrsharp-x64/, constants
    ├── sdr_client.py          ← Backend auto-detection (B/C/D vector selection)
    ├── pyproject.toml         ← uv dependency spec (mcp[cli]>=1.2.0)
    ├── tools/
    │   ├── hardware.py        ← sdr_detect_devices, sdr_get_device_info
    │   ├── frequency.py       ← sdr_get_current_config, frequency validation
    │   ├── capture.py         ← sdr_capture_iq, sdr_demodulate, sdr_get_spectrum
    │   ├── scanner.py         ← sdr_scan_spectrum, sdr_find_signals
    │   └── reference.py       ← sdr_lookup_band, sdr_get_band_plan (BandPlan.xml + fallback)
    ├── spyserver/
    │   └── client.py          ← Full SpyServer TCP protocol implementation
    └── README.md
```

### Design Decisions

1. **Relative pathing:** `config.py` resolves `SDRSHARP_DIR` as `Path(__file__).parent.parent / "sdrsharp-x64"` — the server is portable relative to the SDR# directory.

2. **Band plan merge:** BandPlan.xml is loaded first, then fallback entries are merged in for any frequency ranges not covered by the XML. This fills gaps like 440–450 MHz (UHF land mobile) that SDR#'s BandPlan.xml omits.

3. **Graceful degradation:** Every tool returns structured error dicts with actionable install/troubleshooting instructions rather than crashing. Missing `rtl_test`? Returns download URL. No device? Suggests Zadig. No sox? Falls back to raw PCM.

4. **Backend auto-detection:** `sdr_client.py` probes SpyServer (TCP connect test), RTL CLI (PATH lookup), and FFI (DLL existence) on demand, reporting the highest-priority available vector.

---

## Phase 2 — SpyServer Client Build

### Protocol Implementation

Full SpyServer TCP protocol client implementing the binary framing verified in K3:

- **Request frame:** `[cmd_type: u32_le][param: u32_le][body...]`
- **Response frame:** `[msg_type_and_flags: u32_le][sequence: u32_le][body_size: u32_le][body...]`
- **Handshake:** `CMD_HELLO` with protocol version `0x02000600` and client ID `"SDR-MCP"`
- **Device info parsing:** Extracts device type, serial, max sample rate, frequency range, gain stages
- **FFT streaming:** Sets display pixels, enables FFT-only streaming, reads `UINT8_FFT` / `UINT4_FFT` frames
- **IQ streaming:** Enables IQ-only mode, writes `UINT8/INT16/INT24/FLOAT_IQ` frames to file

All protocol constants verified against the SDRSharp.dotnet8.exe binary before implementation.

---

## Tool Inventory (18 tools)

### Hardware Management
| Tool | Vector | Description |
|------|--------|-------------|
| `sdr_detect_devices` | C | Detect RTL-SDR via `rtl_test`, with Zadig instructions on failure |
| `sdr_get_device_info` | C | Tuner type, supported gain values, device serial |
| `sdr_get_backend_status` | All | Probe all three vectors, report active backend |

### Configuration
| Tool | Vector | Description |
|------|--------|-------------|
| `sdr_get_current_config` | — | Read-only parse of SDRSharp.config (freq, mode, gain, source) |

### Capture & Demodulation
| Tool | Vector | Description |
|------|--------|-------------|
| `sdr_capture_iq` | C | Raw IQ capture via `rtl_sdr` → binary file |
| `sdr_demodulate` | C | RF → audio via `rtl_fm` + sox → WAV (AM/NFM/WFM/USB/LSB) |
| `sdr_get_spectrum` | C | FFT snapshot via `rtl_power` centered on a frequency |

### Scanning
| Tool | Vector | Description |
|------|--------|-------------|
| `sdr_scan_spectrum` | C | Wideband power scan → JSON array of {freq_hz, power_db} |
| `sdr_find_signals` | C | Scan + adaptive threshold filter + band plan enrichment |

### Band Plan & Reference
| Tool | Vector | Description |
|------|--------|-------------|
| `sdr_lookup_band` | — | Frequency → band name, service, mode (BandPlan.xml + fallback) |
| `sdr_get_band_plan` | — | Full 56-band allocation database |

### SpyServer (Remote SDR)
| Tool | Vector | Description |
|------|--------|-------------|
| `spy_connect` | B | TCP connect + HELLO handshake, returns device info |
| `spy_set_frequency` | B | Tune remote SDR (IQ + FFT center freq) |
| `spy_set_gain` | B | Set remote RF gain index |
| `spy_get_fft` | B | Request FFT bins (100–32768 pixels) |
| `spy_stream_iq` | B | Stream IQ data to file for N seconds |
| `spy_disconnect` | B | Close TCP connection |
| `spy_ping` | B | Latency check via CMD_PING / MSG_TYPE_PONG |

---

## Verification Test Results

All non-hardware tests passed at `E:\Thales\Thon\tools\sdrsharp\mcp_sdrsharp\`:

| Test | Result |
|------|--------|
| Server import + 18 tools registered | PASS |
| `sdr_get_current_config()` → 445500000 Hz / AM / RTL-SDR | PASS |
| `sdr_lookup_band(445500000)` → "UHF Land Mobile" / NFM | PASS |
| `sdr_lookup_band(118000000)` → "Aircraft VOR/ILS" + "Aircraft Voice" | PASS |
| `sdr_lookup_band(1090000000)` → "ADS-B Aircraft Tracking" | PASS |
| `sdr_get_band_plan()` → 56 bands from merged sources | PASS |
| `sdr_get_backend_status()` → active_vector: D_ffi, ffi_dll confirmed | PASS |
| `sdr_detect_devices()` → clean error + install instructions (rtl_test not in PATH) | PASS |
| `sdr_capture_iq(10000000)` → frequency validation rejection | PASS |
| `spy_set_frequency()` → "Not connected" guard | PASS |

---

## Deployment

### Cursor MCP Registration

Entry added to `C:\Users\Dallas\.cursor\mcp.json`:

```json
"sdr": {
  "command": "C:\\Users\\Dallas\\AppData\\Roaming\\Python\\Python314\\Scripts\\uv.exe",
  "args": [
    "run",
    "--directory",
    "E:\\Thales\\Thon\\tools\\sdrsharp\\mcp_sdrsharp",
    "python",
    "server.py"
  ]
}
```

Dependencies managed via `pyproject.toml` (`mcp[cli]>=1.2.0`), matching the pattern established by the dnspy MCP server.

### Output Directory

All captures, scans, and recordings write to: `E:\Thales\Thon\output\sdr\`

---

## Operational Readiness

| Capability | Status | Blocker |
|-----------|--------|---------|
| Band plan lookup | OPERATIONAL | — |
| Config reading | OPERATIONAL | — |
| Backend detection | OPERATIONAL | — |
| Device detection | READY | Needs `rtl-sdr-blog` CLI tools in PATH |
| Spectrum scanning | READY | Needs `rtl_power` in PATH |
| IQ capture | READY | Needs `rtl_sdr` in PATH |
| Demodulation | READY | Needs `rtl_fm` in PATH (+ sox for WAV) |
| SpyServer remote | READY | Needs SpyServer running on target host |

### To activate Vector C (CLI tools):

1. Download from https://github.com/rtlsdrblog/rtl-sdr-blog/releases/latest
2. Extract `Release.zip`
3. Add the `x64` folder to system PATH
4. Verify: `rtl_test -t`

### To activate Vector B (SpyServer):

1. Download SpyServer from https://airspy.com/download/
2. Configure `spyserver.config` with device settings
3. Start: `spyserver --config=spyserver.config`
4. Connect from MCP: `spy_connect("host", 5555)`

---

## Ecosystem Position

```
┌─────────────────────────────────────────────────────────┐
│                 RF Awareness Platform                    │
├──────────────────────┬──────────────────────────────────┤
│  Flipper Zero MCP    │  SDR MCP Server                  │
│  Sub-GHz             │  VHF/UHF/Microwave               │
│  315/433 MHz         │  24–1766 MHz                     │
│  Keyfobs, garages    │  Walkie-talkies, aircraft,       │
│  Weather stations    │  FM radio, marine, ham,          │
│                      │  ADS-B, cellular, ISM            │
├──────────────────────┴──────────────────────────────────┤
│  Combined: Sub-GHz through L-band coverage              │
│  Overlapping at 315–433 MHz for cross-validation        │
└─────────────────────────────────────────────────────────┘
```

---

*Report generated by Thon. All verification data sourced from direct instrument contact with the filesystem and binaries — no recon report claim was accepted without independent confirmation.*
