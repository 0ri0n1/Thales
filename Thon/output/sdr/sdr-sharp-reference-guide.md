# SDR# Quick Reference Guide
## RTL-SDR Blog V3 + SDR# (.NET 8 x64)

**Location**: Lloydminster area, Alberta/Saskatchewan border
**Hardware**: RTL-SDR Blog V3 (24 MHz — 1.766 GHz)
**Software**: SDR# (SDRSharp) .NET 8 x64

---

## 1. AVIATION VOICE (Airband)

### How It Works
Aviation uses **AM modulation** on **118—137 MHz**. This is one of the last major
services still using plain analog AM — completely unencrypted, anyone can listen.
Pilots and ATC talk on 25 kHz spaced channels. Your RTL-SDR can receive all of it.

### SDR# Settings for Aviation
| Setting | Value |
|---------|-------|
| Mode | **AM** |
| Center Freq | 118—137 MHz range |
| Filter BW | **10 kHz** (or 8—12 kHz) |
| Step Size | **25 kHz** |
| Gain | Start at ~38 dB, adjust if overloading |

### Key Frequencies — Your Area

| Frequency | Name | What You'll Hear |
|-----------|------|-----------------|
| **121.500 MHz** | EMERGENCY / Guard | Distress calls (usually silent — very important when active) |
| **122.800 MHz** | UNICOM / CTAF | Uncontrolled airport traffic — **busiest general freq** |
| **122.750 MHz** | Air-to-Air chat | Pilots talking to each other informally |
| **122.900 MHz** | MULTICOM | Uncontrolled field operations |
| **123.100 MHz** | Search and Rescue | SAR coordination |
| **127.000 MHz** | ATIS (common) | Automated weather/runway info broadcast (repeating loop) |
| **126.700 MHz** | Edmonton Center | ATC sector covering your area — **best for enroute traffic** |
| **132.850 MHz** | Edmonton Center | Alternate ATC sector |
| **128.200 MHz** | Cold Lake Tower | Military tower — CF-18s and exercise traffic |
| **125.550 MHz** | Cold Lake ATIS | Military automated weather broadcast |
| **243.000 MHz** | Military UHF Guard | Military emergency/common (UHF — also receivable) |

### How to Listen
1. Open SDR# — it's pre-tuned to 122.800 MHz AM (I configured this for you)
2. Click the **Play** button (triangle) with your RTL-SDR plugged in
3. You'll see the waterfall — voice transmissions appear as bright blocks
4. Click on a signal in the waterfall to tune to it, or type a frequency
5. Use the **Frequency Manager** panel (left side) to jump between bookmarked freqs
6. All your bookmarks are loaded — click any entry in the Aviation group

### Tips
- **122.800 is your bread and butter** — most small aircraft announce here
- **Edmonton Center (126.7)** gives you enroute jets and commercial traffic
- Aviation is bursty — long silences then sudden activity. Be patient.
- ATIS channels broadcast continuously — good for testing your setup
- If audio is distorted, **reduce gain**. Aviation AM is sensitive to overload.

---

## 2. POLICE / PUBLIC SAFETY SCANNER

### The Reality Check
**Important caveat**: RCMP and most Alberta police have migrated to **P25 digital
trunked radio** and/or **encrypted channels**. Your RTL-SDR can hear the RF signal
but it will sound like digital noise — you need additional decoding software
(DSD+ or OP25) to demodulate P25, and encrypted channels cannot be decoded at all.

**What you CAN still hear** on analog:
- Some rural fire departments (still analog VHF)
- Some EMS dispatch (transitional)
- Mutual aid channels (kept analog for interoperability)
- Alberta Forestry (wildfire operations)

### SDR# Settings for Public Safety
| Setting | Value |
|---------|-------|
| Mode | **NFM** (Narrowband FM) |
| Center Freq | 148—174 MHz (VHF) or 450—470 MHz (UHF) |
| Filter BW | **12.5 kHz** |
| Step Size | **12.5 kHz** |
| Gain | ~35—40 dB |

### Key Frequencies

| Frequency | Name | Notes |
|-----------|------|-------|
| **155.475 MHz** | RCMP Alberta VHF | May be digital/encrypted |
| **155.370 MHz** | RCMP Mutual Aid | More likely analog |
| **154.280 MHz** | Fire Mutual Aid AB | Best bet for analog voice |
| **155.340 MHz** | EMS Alberta | Transitional — may be analog |
| **164.050 MHz** | Alberta Forestry | Wildfire ops — active in summer |
| **460.125 MHz** | RCMP UHF | Usually digital |

### If You Want Proper P25 Decoding
1. Use **SDR#** or **rtl_fm** to capture the raw signal
2. Pipe audio to **DSD+** (Digital Speech Decoder) for P25 Phase 1
3. Or use **OP25** on Linux for full trunking follow
4. Encrypted traffic remains undecodable regardless

---

## 3. ADS-B AIRPLANE TRACKING

### How It Works
Every commercial aircraft (and most GA) broadcasts its position, altitude, speed,
heading, and callsign on **1090 MHz** using ADS-B (Automatic Dependent Surveillance
— Broadcast). Your RTL-SDR can receive and decode these to show planes on a map.

**This is the killer app for RTL-SDR** — real-time airplane radar on your screen.

### Option A: dump1090 (Recommended — Web Map)

dump1090 gives you a live map in your browser showing all aircraft in range.

**Install dump1090 on Windows:**
```
Download from: https://github.com/antirez/dump1090
Or use the Windows build: dump1090-win (search GitHub)
```

**Run:**
```cmd
dump1090.exe --interactive --net
```
Then open `http://localhost:8080` in your browser — live aircraft map.

**If using the Kali container:**
```bash
# In Kali (already has rtl-sdr tools)
apt install dump1090-mutability
dump1090-mutability --interactive --net --device-index 0
```

### Option B: rtl_adsb (Already Installed — Text Output)

You already have `rtl_adsb.exe` at:
`E:\Thales\Thon\tools\rtl-sdr\rtl_adsb.exe`

**Run from cmd/PowerShell:**
```cmd
cd E:\Thales\Thon\tools\rtl-sdr
.\rtl_adsb.exe
```

This dumps raw ADS-B messages to the console:
```
*8D4840D6202CC371C32CE0576098;
```
Each line is a Mode S message. You can pipe this to a decoder.

### Option C: Virtual Radar Server (Best Visual Experience)

1. Install Virtual Radar Server: https://www.virtualradarserver.co.uk/
2. Run dump1090 with `--net` flag
3. Point VRS to localhost:30003 (BaseStation format)
4. Get a full aviation radar display with aircraft photos, routes, etc.

### SDR# Settings for ADS-B (if listening in SDR#)
| Setting | Value |
|---------|-------|
| Center Freq | **1090 MHz** |
| Mode | AM (though you'll hear digital burps, not voice) |
| Filter BW | **2 MHz** |
| Sample Rate | **2.4 MSPS** (maximum for reliable decode) |
| Gain | **Max** (~49.6 dB) — ADS-B signals are weak |

**Note**: SDR# itself doesn't decode ADS-B. Use the dedicated tools above.
The SDR# bookmark for 1090 MHz is there so you can visually see the ADS-B
pulses on the waterfall — each burst is an aircraft broadcasting its position.

### Expected Range
With the stock RTL-SDR Blog V3 antenna: **~50—100 nautical miles**
With a proper 1090 MHz antenna (like the included dipole or a homemade collinear): **~150—250 nm**

---

## 4. OTHER INTERESTING FREQUENCIES

### Weather Radio
| Frequency | Name | SDR# Mode |
|-----------|------|-----------|
| **162.550 MHz** | Environment Canada WX1 | NFM |
| **162.400 MHz** | Environment Canada WX2 | NFM |
| **162.475 MHz** | Environment Canada WX3 | NFM |

Continuous weather broadcasts — great for testing your setup. WX1 is the primary.

### CB Radio (Truckers)
| Frequency | Name | SDR# Mode |
|-----------|------|-----------|
| **27.185 MHz** | CB Channel 19 | AM |

The trucker channel. Range is limited at 27 MHz with RTL-SDR (lower edge of range).

### FRS/GMRS (Walkie Talkies)
| Frequency | Name | SDR# Mode |
|-----------|------|-----------|
| **462.5625 MHz** | FRS Ch 1 | NFM |
| **462.550 MHz** | GMRS Ch 15 | NFM |

Local handheld radio traffic.

### Railroad
| Frequency | Name | SDR# Mode |
|-----------|------|-----------|
| **161.550 MHz** | AAR Ch 1 (End of Train) | NFM |
| **160.620 MHz** | CN Rail Dispatch | NFM |

If you're near the rail line, you'll hear train operations.

---

## 5. SDR# QUICK-START CHECKLIST

```
[ ] 1. Plug in RTL-SDR Blog V3 (the USB dongle)
[ ] 2. Open SDR# from: E:\Thales\Thon\tools\sdrsharp\sdrsharp-x64\
[ ] 3. Top-left dropdown: select "RTL-SDR (USB)" as source
[ ] 4. Click the PLAY button (triangle)
[ ] 5. You should see the waterfall — colored noise = working
[ ] 6. I've pre-set it to 122.800 MHz AM (aviation CTAF)
[ ] 7. Open "Frequency Manager" panel on the left sidebar
[ ] 8. All bookmarks are loaded — click any to jump to that frequency
[ ] 9. To tune manually: click on the frequency display and type/scroll
[ ] 10. Adjust gain with the RTL-SDR slider if audio is too quiet or distorted
```

### Mode Quick Reference
| Mode | Use For | Bandwidth |
|------|---------|-----------|
| **AM** | Aviation, CB radio, ADS-B visual | 8—10 kHz |
| **NFM** | Police, fire, EMS, FRS/GMRS, weather, railroad | 12.5 kHz |
| **WFM** | FM broadcast radio (88—108 MHz) | 200 kHz |
| **USB** | Ham radio upper sideband (HF) | 2.4 kHz |
| **LSB** | Ham radio lower sideband (HF) | 2.4 kHz |

### Gain Tips
- **Too low**: Weak signals, can't hear much
- **Too high**: Overload distortion, phantom signals everywhere
- **Sweet spot**: Start around 38 dB, lower if you hear distortion
- For ADS-B: crank to max (~49.6 dB) — the signals are very weak

---

## 6. FILE LOCATIONS

| File | Path |
|------|------|
| SDR# Application | `E:\Thales\Thon\tools\sdrsharp\sdrsharp-x64\SDRSharp.exe` |
| SDR# Config | `E:\Thales\Thon\tools\sdrsharp\sdrsharp-x64\SDRSharp.config` |
| Frequency Bookmarks | `E:\Thales\Thon\tools\sdrsharp\sdrsharp-x64\Frequencies.xml` |
| Band Plan | `E:\Thales\Thon\tools\sdrsharp\sdrsharp-x64\BandPlan.xml` |
| rtl_adsb.exe | `E:\Thales\Thon\tools\rtl-sdr\rtl_adsb.exe` |
| rtl_fm.exe | `E:\Thales\Thon\tools\rtl-sdr\rtl_fm.exe` |
| SSID Pool Archive | `E:\Thales\Thon\output\pineapple\ssid_pool_lay-of-the-land.txt` |

---

## 7. LISTENING LEGALITY (CANADA)

In Canada, listening to radio transmissions is **legal** under the Radiocommunication
Act. You can receive any signal. The restrictions are:
- You **cannot retransmit** what you hear
- You **cannot use intercepted information** for personal gain
- You **cannot divulge** the contents of private communications to third parties

Aviation, weather, and CB are explicitly public. Police scanner listening is legal
in Canada (unlike some US states). Just don't act on what you hear.
