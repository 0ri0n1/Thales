# WiFi Module Capabilities — Flipper Zero WiFi Devboard v1

> **Chipset:** Espressif ESP32-S2  
> **Connection:** GPIO header passthrough via Flipper Zero  
> **Firmware:** TBD — capabilities will vary based on installed firmware  
> **Last updated:** 2026-03-10T19:45Z  

---

## Hardware Specifications

| Specification | Value |
|---------------|-------|
| **SoC** | ESP32-S2 (Xtensa® single-core 32-bit LX7, up to 240 MHz) |
| **WiFi Standard** | 802.11 b/g/n |
| **Frequency Band** | 2.4 GHz only |
| **5 GHz Support** | ❌ Not supported (hardware limitation) |
| **Antenna** | PCB trace / onboard |
| **RAM** | 320 KB SRAM + 128 KB ROM |
| **Flash** | 4 MB (typical devboard configuration) |
| **USB Interface** | USB-OTG via Flipper GPIO (or direct USB-C if standalone) |
| **Power** | Fed via Flipper GPIO 3.3V |

---

## Capability Matrix by Firmware

### Legend
- ✅ Fully supported
- ⚠️ Partial / limited
- ❌ Not supported
- ❓ Unknown / untested

| Capability | Stock AT | Marauder | Blackmagic | Notes |
|------------|----------|----------|------------|-------|
| **Passive WiFi Scan** | ✅ | ✅ | ❌ | List visible APs |
| **Active Scanning** | ✅ | ✅ | ❌ | Probe request scanning |
| **Beacon Enumeration** | ⚠️ | ✅ | ❌ | Marauder has richer parsing |
| **Station Mode** | ✅ | ⚠️ | ❌ | Connect to AP |
| **AP Mode (SoftAP)** | ✅ | ✅ | ❌ | Host an access point |
| **Monitor Mode** | ❌ | ✅ | ❌ | ESP32-S2 promiscuous mode |
| **Packet Capture (pcap)** | ❌ | ✅ | ❌ | Save to SD card |
| **Capture to SD** | ❌ | ✅ | ❌ | Via Flipper SD passthrough |
| **Live Stream** | ❌ | ⚠️ | ❌ | Serial passthrough (limited) |
| **Deauth Detection** | ❌ | ✅ | ❌ | Monitor deauth frames |
| **Deauth Attack** | ❌ | ✅ | ❌ | Send deauth frames |
| **Probe Request Logging** | ❌ | ✅ | ❌ | Log client probes |
| **Evil Portal** | ❌ | ✅ | ❌ | Captive portal with custom HTML |
| **PMKID Capture** | ❌ | ✅ | ❌ | WPA2 PMKID harvesting |
| **Beacon Spam** | ❌ | ✅ | ❌ | Fake AP broadcast |
| **Rickroll Beacon** | ❌ | ✅ | ❌ | Fun beacon variant |
| **EAPOL Capture** | ❌ | ✅ | ❌ | WPA handshake capture |
| **Channel Hopping** | ⚠️ | ✅ | ❌ | Auto channel sweep |
| **GDB Debugging** | ❌ | ❌ | ✅ | BlackMagic primary use |
| **SWD/JTAG Debug** | ❌ | ❌ | ✅ | Hardware debug interface |

---

## Operational Modes

### 1. Passive Scanning
- **Available on:** All WiFi firmwares
- **Method:** Listen for beacon frames → enumerate APs
- **Output:** SSID, BSSID, channel, RSSI, security type
- **Limitation:** 2.4 GHz only, single-channel at a time without hopping

### 2. Active Scanning
- **Available on:** Stock AT, Marauder
- **Method:** Send probe requests → collect probe responses
- **Output:** Extended AP info including capabilities

### 3. Monitor Mode (Marauder only)
- **Method:** ESP32-S2 promiscuous mode callback
- **Captures:** All 802.11 frames on selected channel
- **Note:** Not true RFMON — limited by ESP32-S2 hardware
- **Packets visible:** Beacons, probes, deauths, data frames (headers only)

### 4. Packet Capture to SD (Marauder only)
- **Format:** pcap
- **Storage:** Flipper Zero SD card via GPIO filesystem passthrough
- **Limitation:** Serial bandwidth constrains live capture throughput
- **Useful for:** Post-capture analysis in Wireshark

### 5. Evil Portal (Marauder only)
- **Method:** Captive portal served from ESP32-S2 SoftAP
- **Customizable:** HTML/CSS portal pages stored on SD
- **Capture:** Form submissions logged to serial/SD

---

## Serial Command Sets

### Marauder Commands (if installed)

| Command | Description |
|---------|-------------|
| `scanap` | Start AP scanning |
| `stopscan` | Stop current scan |
| `list -a` | List discovered APs |
| `list -c` | List discovered clients |
| `select -a [idx]` | Select AP by index |
| `attack -t deauth` | Deauth selected target |
| `ssid -a -g [n]` | Generate random SSIDs |
| `ssid -a -n [name]` | Add named SSID |
| `attack -t beacon` | Beacon spam |
| `sniff raw` | Raw packet sniffing |
| `sniff pmkid` | PMKID capture |
| `sniff eapol` | EAPOL/handshake capture |
| `channel [n]` | Set channel |
| `update` | Check firmware updates |
| `reboot` | Reboot ESP32 |

### Stock AT Commands (if installed)

| Command | Description |
|---------|-------------|
| `AT` | Test response |
| `AT+GMR` | Get version |
| `AT+CWMODE=1` | Set station mode |
| `AT+CWLAP` | List APs |
| `AT+CWJAP="ssid","pass"` | Connect to AP |
| `AT+CIFSR` | Get IP address |
| `AT+RST` | Reset module |

---

## Frequency Limitations

| Band | Support | Notes |
|------|---------|-------|
| **2.4 GHz** (ch 1-14) | ✅ | Full support, all firmwares |
| **5 GHz** | ❌ | **Not possible** — ESP32-S2 hardware limitation |
| **6 GHz (WiFi 6E)** | ❌ | Not supported |

> **Important:** The ESP32-S2 is a **2.4 GHz only** chipset. This is a fundamental hardware constraint — no firmware can enable 5 GHz operation. For 5 GHz reconnaissance, external USB WiFi adapters with monitor mode (e.g., Alfa AWUS036ACH) are required.

---

## Security & Operational Notes

1. **Deauth attacks** are illegal in most jurisdictions without explicit authorization
2. **Evil portal** credential capture requires informed consent in legitimate pentesting
3. **PMKID/EAPOL capture** is passive but derived cracking may have legal implications
4. **Monitor mode** on ESP32-S2 is limited compared to dedicated WiFi chipsets
5. All operations are **2.4 GHz only** — modern dual-band APs default to 5 GHz

---

## Comparison: What Each Firmware Unlocks

| Firmware | Best For | Limitations |
|----------|----------|-------------|
| **Stock AT** | Basic WiFi connectivity, AP listing | No offensive tools, no pcap |
| **Marauder** | Full offensive suite, scanning, capture | No debug capabilities |
| **Blackmagic** | Hardware debugging (SWD/JTAG) | No WiFi operations at all |
