# P25 Decoding Setup Guide
## RTL-SDR Blog V3 (Dual Dongle) + DSDcc

**Location**: Lloydminster area, Alberta/Saskatchewan border
**Hardware**: 2x RTL-SDR Blog V3 dongles
**Decoder**: DSDcc (dsdccx) installed in WSL Kali + Docker Kali

---

## 1. THE PROBLEM (AND WHAT TO EXPECT)

RCMP Alberta uses **P25 digital trunked radio**. This means:
- **Layer 1 — Modulation**: The signal is transmitted as narrowband FM, but the audio
  content is digitally encoded using IMBE/AMBE voice codecs. A standard FM radio
  hears digital noise (buzzing/burping). You need a P25 decoder.
- **Layer 2 — Trunking**: Conversations hop between frequencies coordinated by a
  control channel. Without trunking follow, you only hear fragments. DSDcc can
  decode single-channel P25 but does NOT follow trunking.
- **Layer 3 — Encryption**: Many RCMP talkgroups use AES-256 encryption. Encrypted
  traffic outputs silence from the decoder. **This cannot be bypassed.**

**Realistic expectations**:
- You WILL be able to decode **unencrypted P25 channels** (dispatch, interoperability,
  mutual aid channels kept clear for multi-agency coordination)
- You WILL hear **analog channels** that haven't migrated to P25 yet (some rural fire,
  EMS, Alberta Forestry)
- You will NOT hear encrypted RCMP tactical channels
- You will NOT follow trunked conversations automatically (would need OP25 + gnuradio)

---

## 2. FIX THE DRIVER (ONE-TIME SETUP)

Your second RTL-SDR dongle needs the WinUSB driver installed via Zadig.
Currently dongle 1 returns `usb_open error -3` because it's still on the
default Windows driver.

### Steps:
1. Download Zadig if you don't have it: https://zadig.akeo.ie/
2. Open Zadig
3. Go to **Options** > **List All Devices**
4. In the dropdown, find the **second** "Bulk-In, Interface (Interface 0)"
   - There will be two entries with similar names
   - Check which USB port each is on (look at USB ID)
   - You already did one — pick the OTHER one
5. Make sure the target driver says **WinUSB** (on the right side of the arrow)
6. Click **Replace Driver** (or **Install Driver**)
7. Wait for it to complete
8. Both dongles should now be accessible from rtl_fm/rtl_tcp/SDR#

### How to verify:
```cmd
cd E:\Thales\Thon\tools\rtl-sdr
rtl_test.exe -d 0 -t
rtl_test.exe -d 1 -t
```
Both should say "Found Rafael Micro R820T tuner" without errors.

### Optional: Set unique serial numbers
Both dongles currently show serial `00000001`. To distinguish them:
```cmd
cd E:\Thales\Thon\tools\rtl-sdr
rtl_eeprom.exe -d 0 -s 00000001
rtl_eeprom.exe -d 1 -s 00000002
```
Then unplug and replug both dongles. After this:
- Dongle 1 (serial 00000001) = Aviation / SDR#
- Dongle 2 (serial 00000002) = P25 decode

---

## 3. ARCHITECTURE

```
Dongle 0 (Aviation)          Dongle 1 (P25)
     |                            |
   SDR#                     rtl_fm.exe (Windows)
   AM mode                  NFM demod, 48 kHz
   122.800 MHz                    |
                            dsdccx (WSL Kali)
                            P25 Phase 1 decode
                                  |
                            Voice audio output
```

The pipeline:
1. `rtl_fm.exe` on Windows FM-demodulates the signal from dongle 1
2. Output is piped (via WSL) to `dsdccx` which decodes the P25 digital voice
3. Decoded audio comes out as raw PCM (or can be saved to file)

---

## 4. HOW TO USE

### Method A: Live Listen (Recommended)
Double-click or run from cmd:
```
E:\Thales\Thon\tools\p25\p25_listen_wsl.bat 155.475
```

Change the frequency by passing a different number:
```
p25_listen_wsl.bat 155.370    # RCMP Mutual Aid
p25_listen_wsl.bat 154.280    # Fire Mutual Aid
p25_listen_wsl.bat 164.050    # Alberta Forestry
```

### Method B: Scanner (Scans all freqs with squelch)
```
E:\Thales\Thon\tools\p25\p25_scan_rcmp.bat
```
This scans across all known public safety frequencies and decodes
whatever signal breaks squelch.

### Method C: Capture + Offline Decode
```
E:\Thales\Thon\tools\p25\p25_capture_windows.bat 155.475 60
```
Records 60 seconds of audio, then decodes in Docker Kali.

### Method D: Docker Pipeline (via rtl_tcp bridge)
Terminal 1 (Windows):
```
E:\Thales\Thon\tools\p25\start_rtl_tcp_server.bat
```
Terminal 2 (Docker Kali):
```
bash /root/data/p25_listen_rcmp.sh 155.475
```

---

## 5. RCMP / PUBLIC SAFETY FREQUENCIES

| Frequency | Name | Type | Likely Status |
|-----------|------|------|---------------|
| **155.475 MHz** | RCMP Alberta VHF | P25 Digital | May be encrypted |
| **155.370 MHz** | RCMP Mutual Aid | P25/Analog | More likely clear |
| **154.280 MHz** | Fire Mutual Aid AB | Analog FM | **Best bet for voice** |
| **155.340 MHz** | EMS Alberta | Transitional | May be analog |
| **164.050 MHz** | Alberta Forestry | Analog FM | **Active in fire season** |
| **460.125 MHz** | RCMP UHF | P25 Digital | Usually encrypted |

### Tips for finding active channels:
1. Start with **154.280 MHz** (Fire Mutual Aid) — most likely analog
2. Try **155.370 MHz** (RCMP Mutual Aid) — interop channels kept clear
3. **164.050 MHz** is golden during wildfire season (June-September)
4. If you hear clear digital buzzing that dsdccx can't decode, it's encrypted
5. If dsdccx shows "P25" frame sync but outputs silence, that's encrypted traffic

---

## 6. INTERPRETING DSDCC OUTPUT

When dsdccx is receiving P25:
```
Sync: +P25p1    # Good! P25 Phase 1 detected
slot0: 04 40    # Talkgroup/channel info
inlvl: 65       # Input level (signal strength)
```

When it's encrypted:
```
Sync: +P25p1
[encrypted]      # DSDcc flags encrypted frames
```

When it's just noise (no signal):
```
no sync          # No digital signal found
```

---

## 7. FILE LOCATIONS

| File | Path |
|------|------|
| P25 Tools Directory | `E:\Thales\Thon\tools\p25\` |
| Live Listener (WSL) | `E:\Thales\Thon\tools\p25\p25_listen_wsl.bat` |
| Scanner | `E:\Thales\Thon\tools\p25\p25_scan_rcmp.bat` |
| Capture + Decode | `E:\Thales\Thon\tools\p25\p25_capture_windows.bat` |
| RTL-TCP Server | `E:\Thales\Thon\tools\p25\start_rtl_tcp_server.bat` |
| Docker Script | Docker: `/root/data/p25_listen_rcmp.sh` |
| Captures Output | `E:\Thales\Thon\output\sdr\p25_captures\` |
| dsdccx (WSL) | WSL Kali: `/usr/bin/dsdccx` |
| dsdccx (Docker) | Docker Kali: `/usr/bin/dsdccx` |
| rtl_fm.exe | `E:\Thales\Thon\tools\rtl-sdr\rtl_fm.exe` |
| rtl_tcp.exe | `E:\Thales\Thon\tools\rtl-sdr\rtl_tcp.exe` |

---

## 8. TROUBLESHOOTING

**"usb_open error -3"**: Dongle doesn't have WinUSB driver. Run Zadig (Section 2).

**"PLL not locked"**: Frequency out of range or dongle warming up. Wait 30 seconds.

**dsdccx shows no sync**: Either no signal, wrong frequency, or wrong modulation.
Make sure rtl_fm is using `-M fm` (narrowband FM).

**Audio is garbled/robotic**: Sample rate mismatch. DSDcc expects 48 kHz input.
Make sure rtl_fm uses `-s 48000`.

**Silent output but "Sync: +P25p1"**: Channel is encrypted. Try a different frequency.

**SDR# won't start after Zadig**: You may have replaced the wrong device's driver.
SDR# needs WinUSB too. Re-run Zadig for the other dongle.

---

## 9. UPGRADE PATH

### Full Trunking Follow (OP25)
For proper RCMP monitoring with automatic trunking follow:
1. Install Linux (bare metal or WSL2 with USB passthrough)
2. Install gnuradio + OP25 from source
3. Configure with RCMP P25 system parameters (NAC, WACN, talkgroup list)
4. OP25 follows conversations across frequencies automatically
5. This is a significant project but gives you a proper scanner

### DSD+ (Windows Alternative)
DSD+ is a Windows P25 decoder (freeware):
1. Download from: https://www.dsdplus.com/
2. Runs natively on Windows without WSL
3. Has a GUI for monitoring multiple talkgroups
4. Can be fed from SDR# via Virtual Audio Cable
5. More user-friendly than the command-line pipeline above
