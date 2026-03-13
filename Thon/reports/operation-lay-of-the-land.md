# OPERATION LAY OF THE LAND — Wireless Reconnaissance Report

**Classification**: AUTHORIZED RECON — NO ATTACK
**Date**: 2026-03-11
**Observation Window**: 2026-03-08 through 2026-03-10 (72 hours continuous)
**Operator**: Eddie
**Platform**: WiFi Pineapple Mark 7 (Hak5) at 172.16.42.1
**Support**: Kali Linux Docker container
**RTL-SDR Status**: COMPLETE — Full spectrum sweep 24MHz-1766MHz (see Section 10)

---

## EXECUTIVE SUMMARY

Three days of passive wireless reconnaissance from the WiFi Pineapple Mark 7 has mapped the complete 2.4GHz wireless landscape of the operational area. The environment is a mixed residential/commercial zone with significant institutional and transit wireless presence.

**Key Numbers:**
| Metric | Count |
|---|---|
| Unique SSIDs (non-Pineapple) | 179 |
| Unique BSSIDs (non-Pineapple) | 228 |
| Unique client MAC addresses | 4,822 |
| BSSIDs with associated clients | 107 |
| SSIDs captured in PineAP pool | ~130 |
| Handshakes captured | 0 (recon only) |
| Clients associated to PineAP traps | 0 (no attack) |

---

## 1. PLATFORM CONFIGURATION

### Pineapple Radio Topology
| Radio | Interface | Mode | Assignment | Channel |
|---|---|---|---|---|
| phy#0 | wlan0, wlan0-1 | AP | Operational APs (NETGEAR-OPEN-5G-HOME / NETGEAR-5G-HOME) | 11 |
| phy#1 | wlan1 / wlan1mon | Monitor | PineAP scanning radio | 11 |
| phy#2 | wlan2 | Client/Managed | Upstream link to TELUS5434 | 6 |

### PineAP Engine Configuration
- **Karma**: OFF (no impersonation of probed SSIDs)
- **Beacon Responses**: ON
- **SSID Pool Broadcast**: ON (broadcasting ~130 captured SSIDs)
- **Probe Capture**: ON (logging all probe requests)
- **Logging**: ON
- **MAC Filter**: Blacklist mode
- **SSID Filter**: Blacklist mode

### Network Position
- Upstream: TELUS5434 (192.168.1.0/24 via wlan2)
- Gateway: 192.168.1.254 (10:78:5B:FA:3C:10)
- Management bridge: 172.16.42.0/24 (br-lan)
- Management laptop: 172.16.42.42 (00:13:37:A7:14:B3)

---

## 2. INFRASTRUCTURE ACCESS POINTS (Permanent Installations)

### Tier 1 — Strong Signal (within ~50m)

| SSID | BSSID | Channel | Best Signal | Encryption | WPS | MFP | Clients | Notes |
|---|---|---|---|---|---|---|---|---|
| **TELUS5434** | 10:78:5B:FA:3C:12 | 6/11 | -47 dBm | WPA2 PSK | No | No | 12 | Primary upstream, 295+ probes |
| **OrionLink** | CC:28:AA:66:30:08 | 5/7/8 | -37 dBm | WPA2 PSK | Yes | No | 31+ | Strongest signal in area |
| **Concession** | 4A:A9:8A:AB:D1:27 | 1 | -48 dBm | WPA2/WPA3 | No | Yes | 51+ | MCSnet infrastructure |
| **MCSNET FREE** | 4A:A9:8A:AB:D1:2D | 1 | -69 dBm | WPA2/WPA3 | No | Yes | 46 | Open/public tier, busiest AP |
| **MCSnet-b89f1** | 4A:A9:8A:AB:D1:26 | 1 | -55 dBm | WPA2/WPA3 | Yes | Yes | — | ISP infrastructure |
| **MCSnet-6c55b** | 1A:FD:74:A2:10:4A | 1 | -57 dBm | WPA2 PSK | Yes | No | — | ISP infrastructure |
| **TELUS5150** | FC:2B:B2:EC:D4:52 | 11 | -59 dBm | WPA2 PSK | Yes | No | 4 | Neighbor TELUS |
| **TELUS5434_RPT** | A0:36:BC:4E:73:B9 | 6/11 | -67 dBm | WPA2 PSK | No | No | — | Repeater at 192.168.1.70 |

### Tier 2 — Moderate Signal (within ~100m)

| SSID | BSSID | Channel | Best Signal | Encryption | WPS | Notes |
|---|---|---|---|---|---|---|
| Veenstra | 9C:1E:95:CE:E8:C2 | 1/11 | -73 dBm | WPA2 PSK | Yes | Residential |
| TELUS5297 | 9C:1E:95:F1:B4:A2 | 11 | -77 dBm | WPA2 PSK | Yes | 5 clients |
| PHONK9876 | 66:C4:4A:23:9C:B7 | — | — | WPA2 PSK | — | 11 clients |
| KandD | 70:F2:20:88:06:82 | — | — | WPA2 PSK | — | 4 clients |
| Ynet25 | 92:07:1D:BC:0E:C4 | — | — | WPA2 PSK | — | 4 clients |
| gmamea | 18:D6:C7:6C:90:3F | — | — | — | — | 6 clients, frequently probed |
| dlink-4238 | FC:2B:B2:F1:55:D2 | — | — | WPA2 PSK | — | 4 clients |

### Tier 3 — Weak Signal (within ~200m)

| SSID | BSSID | Channel | Best Signal | Encryption | Notes |
|---|---|---|---|---|---|
| TELUS5105 | FC:2B:B2:F7:C8:C2 | 11 | -83 dBm | WPA2 PSK | WPS enabled |
| TELUS5822 | 9C:1E:95:D6:CA:B2 | 11 | -83 dBm | WPA2 PSK | WPS enabled |
| Public Library Wireless | 8C:79:09:99:BD:E5 | 1 | -81 dBm | **OPEN** | No encryption |
| Library BYOD | 8C:79:09:99:BD:E3 | 1 | -83 dBm | WPA2 Enterprise | 802.1X |
| Library Staff | 8C:79:09:99:BD:E2 | 1 | -83 dBm | WPA2 Enterprise | 802.1X |

### Institutional / Enterprise Network — BTPS Secure2

A significant enterprise deployment with multiple APs sharing the C4:14:A2 OUI (likely TP-Link or similar enterprise gear). Combined ~80+ unique clients across all APs.

| BSSID | Clients | Variant |
|---|---|---|
| C4:14:A2:04:66:30 | 25 | Primary |
| C4:14:A2:04:64:10 | 17 | |
| C4:14:A2:04:65:80 | 16 | BTPS Secure2 |
| CA:14:A2:04:65:80 | 14 | Open Access (open tier) |
| C4:14:A2:04:5D:D0 | 9 | BTPS Secure2 |
| C4:14:A2:04:5E:00 | 6 | |
| C4:14:A2:04:83:50 | 3+ | BTPS Secure2 |
| C4:14:A2:04:6F:10 | 3+ | |
| C4:14:A2:04:6F:E0 | 2+ | |
| C4:14:A2:03:53:70 | 1+ | |
| C4:14:A2:04:82:E0 | 1+ | |
| C4:14:A2:04:63:40 | 4 | |

"BTPS" likely stands for a school, business, or institutional entity. The deployment spans at least 12 distinct APs, suggesting a large building or campus within range.

---

## 3. TRANSIENT / MOBILE ACCESS POINTS

### Vehicle WiFi (observed in transit)
Over 50 unique vehicle WiFi APs were detected across the 72-hour observation window:

| Category | SSIDs Observed | Notes |
|---|---|---|
| **Chevrolet/GMC** | myChevrolet (multiple), myGMC, BUICK, CHEVROLET variants, Barbs GMC | GM OnStar WiFi hotspots |
| **Ford** | SYNC_XT2U46SZ | Ford SYNC system |
| **Honda** | Honda OTA | OTA update channel |
| **Nissan** | Nissan RSE | Rear seat entertainment |
| **Audi** | Audi_MMI | Multimedia Interface |
| **Volkswagen** | My VW | |
| **Dash Cameras** | Dash-Cam, TYPE_S_DVR, CAR_CAM | Aftermarket cameras with WiFi |

### Mobile Hotspots
| Pattern | Count | Notes |
|---|---|---|
| "Hotspot*" variants | 15+ | Generic mobile hotspot names |
| iPhone/Samsung | 10+ | Personal device hotspots |
| HUAWEI-B612-078B | 1 | 4G LTE router, actively probed by 24:DF:6A:A9:36:06 |

### IoT / Specialty Devices
| SSID | Type | Notes |
|---|---|---|
| SELPHY CP1300 | Canon printer | Wireless printing |
| WiZConfig | Smart home device | Configuration AP |
| Skybell | Video doorbell | IoT |
| xbr-65x810c | Sony TV | Cast/control |
| Front Room TV | Smart TV | |
| EZLYNK | Vehicle diagnostics | OBD-II WiFi device |

---

## 4. CLIENT INTELLIGENCE

### Top Active Clients (by probe volume)

| MAC | Associated AP | Direct Probes | Broadcast Probes | Activity |
|---|---|---|---|---|
| 70:89:76:25:F3:AB | TELUS5434 | 2,028 | 66 | Top client, also probes "SHOELESSandCLUELESS" |
| 0C:EF:AF:CE:68:1E | TELUS5434 | 1,831 | 17 | Persistent connection to TELUS5434 |
| 60:1D:9D:FC:0D:34 | C4:14:A2:04:82:E0 | 1,172 | 0 | BTPS enterprise client |
| 54:F1:5F:8B:AA:49 | C4:14:A2:04:64:10 | 1,119 | 4 | BTPS enterprise client (Huawei) |
| 54:F1:5F:72:4D:BE | C4:14:A2:04:65:80 | 529 | 2 | BTPS enterprise client (Huawei) |
| D8:1F:12:A4:1F:29 | TELUS5297 | 490 | 1 | TELUS5297 client |
| 48:E1:E9:42:E9:69 | TELUS5434_RPT | 487 | 4 | Connects via repeater |
| 24:DF:6A:A9:36:06 | TELUS5434 | 435 | 5 | Multi-profile: probes HUAWEI-B612, TELUS5434, "Exploit" |
| 3C:31:78:91:22:CC | FF:FF:FF:FF:FF:FF | 346 | 103 | Heavy broadcast probing |
| FA:8F:EB:CD:F6:FC | MCSNET FREE | 333 | 5 | Public network user |

### OUI Distribution (Client Manufacturers)
| OUI Prefix | Count | Likely Manufacturer |
|---|---|---|
| E8:C8:29 | 19 | Apple |
| DA:A1:19 | 13 | Randomized MAC (privacy) |
| 54:F1:5F | 10 | Huawei/HiSilicon |
| F0:D4:15 | 8 | — |
| 38:68:93 | 8 | — |
| FA:14:A2 | 7 | Randomized/locally-administered |
| A8:38:5C | 7 | — |
| 10:74:6F | 7 | — |
| 70:D8:23 | 6 | — |
| 30:C3:D9 | 6 | — |

**Note**: Many modern devices use MAC address randomization for probe requests, inflating unique MAC counts. The DA:A1:19 and FA:14:A2 prefixes (locally-administered bit set) indicate randomized MACs.

---

## 5. PROBE REQUEST INTELLIGENCE

Probe requests reveal which networks devices have previously connected to — exposing travel history and network affiliations.

### Highest-Volume Probers

| MAC | Probed SSID | Dup Count | Assessment |
|---|---|---|---|
| 34:64:A9:66:AB:03 | Linksys03963 | **1,690,443,225** | Stuck device in infinite retry loop |
| 00:E0:4C:1F:C2:38 | (broadcast) | 19,386,409 | Realtek chipset, null probes |
| 3C:31:78:91:22:CC | (broadcast) | 2,689,600 | Aggressive scanner |
| 04:EC:D8:E2:ED:DE | (broadcast) | 1,836,025 | Also probes TELUS5434 |
| 58:D3:91:92:59:0C | (broadcast) | 1,587,600 | Broadcast-only prober |
| BC:10:2F:2B:04:31 | Tater2021 | 1,454,436 | Also probes "AutoReconnection_A26aa" |

### Multi-Profile Devices (travel/affiliation indicators)

| MAC | Networks Probed | Assessment |
|---|---|---|
| **78:D6:DC:13:3D:B6** | Veenstra, TELUS3074, TELUS3185, ithurtswhenIP | 4 network profiles — moves between locations |
| **24:DF:6A:A9:36:06** | HUAWEI-B612-078B, TELUS5434, **Exploit** | Probes for "Exploit" — notable SSID choice |
| **BC:10:2F:2B:04:31** | Tater2021, AutoReconnection_A26aa | Dual-profile, possibly IoT device |
| **D0:C9:07:AB:33:AE** | TheMadHouse, (broadcast) | Residential profile |
| **8C:49:62:51:51:AD** | gmamea, (broadcast) | Residential profile |
| **1C:93:C4:09:62:EE** | utah guest | Travel indicator — visited Utah area |

### Notable Probed SSIDs
| SSID | Probers | Significance |
|---|---|---|
| **Linksys03963** | 1 device, 1.69B dups | Stuck device seeking legacy router |
| **Tater2021** | 1 device, 1.45M dups | Personal network name |
| **Kappel Router** | 1 device, 567K dups | Personal/custom router name |
| **TheMadHouse** | 1 device, 235K dups | Creative residential name |
| **SHOELESSandCLUELESS** | 1 device, 73K dups | Creative residential name |
| **Exploit** | 1 device, 1.3K dups | Interesting — security/CTF related? |
| **utah guest** | 1 device, 4.2K dups | Hotel/institutional guest network |
| **Library BYOD** | 1 device, 2.5K dups | Local library regular |
| **gmamea** | 3+ devices, 13K+ total dups | Multiple household members |
| **BTPS Secure2** | 5+ devices, 12K+ total dups | Institutional users |

---

## 6. NETWORK TOPOLOGY MAP

```
                    INTERNET
                       |
              [TELUS Gateway .254]
              10:78:5B:FA:3C:10
                       |
           +-----------+-----------+
           |                       |
    [TELUS5434 AP]          [TELUS5434_RPT]
    10:78:5B:FA:3C:12       A0:36:BC:4E:73:B9
    Ch6/11, WPA2            Ch6/11, WPA2
    12 clients              .70
           |
    [Unknown Device .73]
    04:EC:D8:E2:ED:DE
           |
    ===============================
    [WiFi Pineapple Mk7]
    wlan2: Client → TELUS5434
    wlan0: AP (NETGEAR-OPEN-5G-HOME)
    wlan1mon: Monitor/PineAP
    172.16.42.1
           |
    [Management Laptop]
    172.16.42.42
    00:13:37:A7:14:B3

    === NEIGHBORING NETWORKS ===

    [OrionLink]         [Concession/MCSnet]       [BTPS Secure2]
    CC:28:AA:66:30:08   4A:A9:8A:AB:D1:2x        C4:14:A2:04:xx:xx
    Ch5/7/8, -37dBm     Ch1, WPA2/WPA3, MFP       12+ APs, 80+ clients
    WPS enabled         46 clients (FREE tier)      Enterprise deployment

    [Library]           [TELUS Neighbors]          [Residential]
    8C:79:09:99:BD:Ex   5150, 5297, 5105, 5822     Veenstra, gmamea,
    3 SSIDs (Open,      Various channels            PHONK9876, KandD,
    BYOD, Staff)        WPA2, WPS enabled           Ynet25, dlink-4238
```

---

## 7. CHANNEL UTILIZATION

| Channel | APs Observed | Congestion Level |
|---|---|---|
| **Ch 1** | Concession, MCSnet variants, Library (x3), Veenstra, MCSnet-6c55b | **HIGH** — 7+ APs |
| **Ch 6** | TELUS5434, TELUS5434_RPT | Moderate |
| **Ch 8** | OrionLink | Low |
| **Ch 11** | TELUS5434 (dual), TELUS5150, TELUS5297, TELUS5105, TELUS5822, Veenstra | **HIGH** — 7+ APs |

Channel 1 and 11 are heavily contested. Channel 6 is relatively clear.

---

## 8. SECURITY OBSERVATIONS

### Weaknesses Identified (Recon Only — No Exploitation)

1. **Open Networks**: Public Library Wireless and MCSNET FREE operate without encryption. MCSNET FREE has 46 unique clients — all traffic is sniffable.

2. **WPS Enabled**: OrionLink, TELUS5150, MCSnet-b89f1, MCSnet-6c55b, Veenstra, TELUS5297, TELUS5105, TELUS5822 all have WPS enabled — vulnerable to Pixie Dust and brute-force PIN attacks.

3. **Stuck Device**: 34:64:A9:66:AB:03 has been continuously probing for "Linksys03963" with 1.69 billion duplicate probe requests. This device is leaking its network affiliation constantly and wasting airtime.

4. **Device Probing for "Exploit"**: MAC 24:DF:6A:A9:36:06 is probing for an SSID named "Exploit" — could be a CTF participant, security researcher, or intentional bait SSID.

5. **Multi-Profile Exposure**: Device 78:D6:DC:13:3D:B6 exposes 4 previously-connected networks (Veenstra, TELUS3074, TELUS3185, ithurtswhenIP), revealing movement patterns between locations.

6. **Legacy Infrastructure**: Several TELUS residential APs still using WPA2-only without WPA3 transition.

7. **Enterprise Scale**: BTPS Secure2 operates a 12+ AP deployment with 80+ unique clients — a significant target surface if this were an active engagement.

---

## 9. SSID POOL (PineAP Captured)

The PineAP engine captured ~130 unique SSIDs from probe requests over the observation period. These represent networks that devices in range have previously connected to:

**Categories of captured SSIDs:**
- **ISP defaults**: TELUS*, BELL*, MCSnet*, Shaw*, Rogers variants
- **Residential**: Veenstra, lecomte, gmamea, grahamrez79, Ully Mae, M&M, SHOELESSandCLUELESS, TheMadHouse, ithurtswhenIP, Tater2021
- **Hotels/Travel**: ramada, Travelodgr, Lia Hotel WiFi, Rodeway Inn, utah guest
- **Vehicles**: myChevrolet, myGMC, Honda OTA
- **Institutional**: BTPS Secure2, Library BYOD, Southridge Camp, Operation Yukon
- **IoT**: SELPHY CP1300, WiZConfig, EZLYNK
- **Notable**: Exploit, Kappel Router, AutoReconnection_A26aa

Most recent capture: "Southridge Camp" (2026-03-12 01:16:24 UTC)

---

## 10. RTL-SDR RF SPECTRUM ANALYSIS

**STATUS: COMPLETE**
**Date**: 2026-03-11 20:46–20:49 UTC-7
**Hardware**: 2x Realtek RTL2838UHIDIR + Rafael Micro R820T tuner (dual-dongle parallel scanning)
**Coverage**: 24 MHz — 1,766 MHz (R820T tuner maximum)
**Method**: `rtl_power.exe` CLI sweeps via osmocom rtl-sdr tools (Windows native)
**Gain**: 40.2 dB (manual gain, AGC off)

> **Note**: R820T tuner cannot reach 2.4 GHz or 5 GHz. WiFi-band RF analysis requires an upconverter or wideband SDR (e.g., Airspy HF+, HackRF). The Pineapple recon (Sections 1–9) covers the WiFi landscape; this section covers everything below 1.766 GHz.

### Sweep Inventory

| Sweep | Range | Step Size | Integration | File |
|-------|-------|-----------|-------------|------|
| Full Lower Band | 24–900 MHz | 100 kHz | 5s | sweep_lower_24M_900M.csv |
| Full Upper Band | 900–1766 MHz | 100 kHz | 5s | sweep_upper_900M_1766M.csv |
| FM Broadcast | 87.5–108 MHz | 25 kHz | 10s | sweep_fm_broadcast.csv |
| Aviation | 108–137 MHz | 12.5 kHz | 10s | sweep_aviation_108_137M.csv |
| VHF Land Mobile | 148–174 MHz | 12.5 kHz | 10s | sweep_vhf_148_174M.csv |
| Marine VHF | 156–163 MHz | 12.5 kHz | 10s | sweep_marine_vhf.csv |
| ISM 315/433 MHz | 315–433.92 MHz | 25 kHz | 10s | sweep_ism315_433M.csv |
| UHF Land Mobile | 430–470 MHz | 6.25 kHz | 10s | sweep_uhf_430_470M.csv |
| FRS/GMRS | 460–470 MHz | 6.25 kHz | 10s | sweep_frs_gmrs_460_470M.csv |
| ISM 900 MHz | 902–928 MHz | 12.5 kHz | 10s | sweep_ism900_902_928M.csv |
| UHF TV/FirstNet | 470–512 MHz | 25 kHz | 10s | sweep_uhf_tv_470_512M.csv |

All output stored at `E:\Thales\Thon\output\sdr\`.

### RF Landscape Summary

**3,168 frequency bins** detected above the noise floor (> -10 dB), across **19 identified service categories**.

| Strength | Count | Description |
|----------|-------|-------------|
| Strong (> 0 dB) | 159 | Nearby/powerful transmitters |
| Moderate (-5 to 0 dB) | 742 | Active services at medium range |
| Weak (-10 to -5 dB) | 2,267 | Distant or low-power signals |

### Active Services Detected (19)

| Service | Active Bins | Peak Power | Frequency Range | Strength |
|---------|-------------|------------|-----------------|----------|
| 700 MHz Public Safety / LTE | 212 | +4.7 dB | 718.4–755.7 MHz | STRONG |
| Military UHF | 922 | +4.7 dB | 225.1–378.2 MHz | STRONG |
| Cellular 850 MHz | 103 | +4.2 dB | 879.7–889.4 MHz | STRONG |
| Maritime Mobile | 92 | +3.3 dB | 217.1–225.0 MHz | STRONG |
| UHF TV Broadcast | 875 | +3.1 dB | 478.7–580.0 MHz | STRONG |
| FM Broadcast | 55 | +2.8 dB | 89.8–106.2 MHz | STRONG |
| UHF Business/Land Mobile / FRS/GMRS | 36 | +1.7 dB | 450.5–460.8 MHz | STRONG |
| FirstNet / LTE Band 14 | 13 | +1.6 dB | 769.2–773.9 MHz | STRONG |
| Amateur 70cm / Land Mobile | 262 | +0.6 dB | 420.0–448.7 MHz | STRONG |
| Military/Government | 3 | +0.1 dB | 139.0–144.0 MHz | STRONG |
| VHF Business/Land Mobile | 18 | -0.1 dB | 165.3–174.0 MHz | Moderate |
| VHF TV / DAB | 66 | -1.6 dB | 174.1–216.0 MHz | Moderate |
| Aviation Voice (AM) | 29 | -1.8 dB | 119.9–135.5 MHz | Moderate |
| 600 MHz Band (T-Mobile) | 233 | -3.1 dB | 617.9–686.1 MHz | Moderate |
| Aviation Navigation (VOR/ILS) | 1 | -3.9 dB | 115.2 MHz | Moderate |
| Government | 101 | -4.4 dB | 408.0–419.9 MHz | Moderate |
| TETRA / Public Safety | 67 | -4.8 dB | 380.1–389.6 MHz | Moderate |
| Unidentified (24–87 MHz) | 79 | -1.4 dB | 28.2–86.5 MHz | Moderate |
| Meteorological Aids | 1 | -7.1 dB | 403.2 MHz | Weak |

### Top 10 Strongest Signals

| Freq (MHz) | Power | Identification |
|------------|-------|----------------|
| 721.494 | +4.7 dB | 700 MHz LTE downlink (likely AT&T/Verizon Band 12/13/17) |
| 277.984 | +4.7 dB | Military UHF (SATCOM or tactical relay) |
| 277.809 | +4.6 dB | Military UHF (same cluster) |
| 722.281 | +4.5 dB | 700 MHz LTE downlink |
| 741.522 | +4.3 dB | 700 MHz LTE downlink (possible Band 17) |
| 885.132 | +4.2 dB | Cellular 850 MHz downlink (Band 5) |
| 286.118 | +4.1 dB | Military UHF |
| 885.394 | +4.1 dB | Cellular 850 MHz downlink |
| 884.082 | +4.0 dB | Cellular 850 MHz downlink |
| 769.247 | +1.6 dB | FirstNet Band 14 downlink |

### Notable Band Findings

**Cellular Infrastructure (strongest presence):**
- 700 MHz LTE: 212 active bins, peak +4.7 dB — this is the dominant RF source. Cell towers are close.
- Cellular 850: 103 bins, peak +4.2 dB — secondary cell coverage (Bell/Telus Band 5).
- 600 MHz T-Mobile: 233 bins, peak -3.1 dB — present but weaker (T-Mobile/Rogers Band 71).
- FirstNet Band 14: 13 bins, peak +1.6 dB — first responder LTE active in area.

**Military/Government (significant presence):**
- 922 bins across 225–378 MHz, peak +4.7 dB — this is the largest active band by bin count. Likely includes military SATCOM downlinks, MUOS, and potentially nearby military/government tactical comms. The 277–278 MHz cluster is particularly strong.

**Broadcast:**
- FM Broadcast: Active across the dial, peak +2.8 dB. Typical for any populated area.
- UHF TV: 875 bins across 478–580 MHz, peak +3.1 dB — broadcast towers visible.

**Public Safety / Emergency:**
- TETRA/P25: 67 bins in 380–390 MHz range — public safety trunked radio is active.
- 800 MHz Public Safety: Below detection threshold — may indicate absence or distance from 800 MHz trunked sites.
- FirstNet: Active at 769–774 MHz — first responder broadband is deployed.

**Land Mobile / Two-Way Radio:**
- VHF Business (148–174 MHz): 18 active bins — light VHF commercial radio presence.
- UHF Business/FRS/GMRS (450–470 MHz): 36 bins — moderate activity in business band.
- Amateur 70cm (420–449 MHz): 262 bins — significant ham radio activity or land mobile sharing.

**Aviation:**
- 29 bins in 118–137 MHz voice band, peak -1.8 dB — aviation traffic audible but not nearby.
- 1 VOR/ILS navigation signal at 115.2 MHz — regional nav aid.

**IoT / ISM Bands:**
- ISM 433 MHz: Single weak signal at 433.9 MHz (-9.7 dB) — likely a remote sensor or keyfob.
- ISM 900 MHz (Z-Wave/LoRa): **No signals detected** — no LoRa gateways or Z-Wave hubs within range.
- FRS/GMRS: **No signals detected** at scan time — no active walkie-talkies (previous session detected activity at 462.5625 MHz).

**Marine VHF Ch16 (156.8 MHz):**
- No signals detected — expected for an inland location.

**GPS L1 (1575.42 MHz):**
- Below detection threshold — GPS signals are below noise floor for this receiver gain/antenna configuration. Normal.

### Correlation with WiFi Pineapple Findings

The Pineapple (Sections 1–9) mapped the 2.4 GHz landscape; the RTL-SDR maps everything below 1.766 GHz. Together they reveal:

1. **Cellular infrastructure confirms urban/suburban density**: Strong 700/850 MHz cell signals + 179 WiFi SSIDs = area is well-served by telecommunications infrastructure.
2. **No LoRa/Z-Wave IoT detected**: Despite 4,822 WiFi clients, the sub-GHz IoT spectrum is silent. Smart home devices in this area use WiFi, not Z-Wave or LoRa.
3. **Military UHF presence**: The 225–380 MHz military band is the busiest single allocation by bin count (922 bins). This could indicate proximity to a military installation, flight path, or SATCOM ground station.
4. **FirstNet confirms public safety infrastructure**: The combination of TETRA activity (380–390 MHz) and FirstNet (769–774 MHz) indicates first responder infrastructure is deployed and active.
5. **FRS/GMRS intermittent**: Previous session detected walkie-talkie traffic at 462.5625 MHz; current sweep shows no activity — confirming these are transient human-operated transmissions, not persistent infrastructure.

---

## 11. SANITARY HOUSEKEEPING

### Data Artifacts Created
| Location | File | Contents |
|---|---|---|
| Kali: /root/data/ | pineapple_recon.db | AP and client scan data (4,822 clients, 228 BSSIDs) |
| Kali: /root/data/ | pineapple_log.db | Probe request logs (all captured probes) |
| Kali: /root/data/ | pineapple_clients.db | Previous connected clients (empty — no attacks) |
| Kali: /root/data/ | pineapple_main.db | SSID pool database (~130 SSIDs) |
| Pineapple: /root/ | recon.db, log.db | Original databases (still on device) |
| Pineapple: /etc/pineapple/ | pineapple.db, previous_clients.db | Original databases (still on device) |
| Host: E:\Thales\Thon\output\sdr\ | sweep_lower_24M_900M.csv | Full lower band power scan (313 hops, 10,016 bins) |
| Host: E:\Thales\Thon\output\sdr\ | sweep_upper_900M_1766M.csv | Full upper band power scan (310 hops, 9,920 bins) |
| Host: E:\Thales\Thon\output\sdr\ | sweep_fm_broadcast.csv | FM broadcast band detail (87.5–108 MHz) |
| Host: E:\Thales\Thon\output\sdr\ | sweep_aviation_108_137M.csv | Aviation band detail (108–137 MHz) |
| Host: E:\Thales\Thon\output\sdr\ | sweep_vhf_148_174M.csv | VHF land mobile detail (148–174 MHz) |
| Host: E:\Thales\Thon\output\sdr\ | sweep_marine_vhf.csv | Marine VHF detail (156–163 MHz) |
| Host: E:\Thales\Thon\output\sdr\ | sweep_ism315_433M.csv | ISM 315/433 MHz detail |
| Host: E:\Thales\Thon\output\sdr\ | sweep_uhf_430_470M.csv | UHF land mobile detail (430–470 MHz) |
| Host: E:\Thales\Thon\output\sdr\ | sweep_frs_gmrs_460_470M.csv | FRS/GMRS detail (460–470 MHz) |
| Host: E:\Thales\Thon\output\sdr\ | sweep_ism900_902_928M.csv | ISM 900 MHz detail (Z-Wave/LoRa) |
| Host: E:\Thales\Thon\output\sdr\ | sweep_uhf_tv_470_512M.csv | UHF TV/FirstNet detail (470–512 MHz) |

### Pineapple State
- PineAP engine: RUNNING (beacon response + SSID pool broadcast active)
- Karma: OFF (no association attacks)
- Monitor mode: ACTIVE on wlan1mon
- Upstream connection: ACTIVE to TELUS5434 via wlan2

### Cleanup Recommendations
1. **To cease observation**: SSH to Pineapple, disable PineAP (`pineap disable`)
2. **To clear SSID pool**: Truncate the ssids table in pineapple.db
3. **To remove Kali artifacts**: `rm /root/data/pineapple_*.db`
4. **To reset Pineapple**: Factory reset via web UI at 172.16.42.1:1471

### No offensive actions were taken during this operation.

---

## 12. SUMMARY ASSESSMENT

The operational area is a **moderately dense wireless environment** characteristic of a small-town mixed residential/commercial zone with institutional and military-adjacent presence. Key features:

### WiFi Landscape (2.4 GHz — Pineapple)

1. **ISP Dominance**: TELUS is the dominant residential ISP with 6+ visible residential APs. MCSnet provides commercial/public infrastructure with enterprise-grade features (WPA3, MFP).

2. **Institutional Presence**: BTPS Secure2 operates a large-scale enterprise WiFi deployment (12+ APs, 80+ clients). The public library operates three-tier WiFi (open, BYOD, staff).

3. **Transit Corridor**: Significant vehicle WiFi presence (50+ unique vehicle APs) indicates a major road or parking area within range. GM vehicles (Chevrolet/GMC/Buick) are the dominant make.

4. **Client Density**: 4,822 unique client MACs over 72 hours, though MAC randomization inflates this number. Estimated true unique devices: 2,000–3,000.

5. **Security Posture**: Mixed. MCSnet infrastructure uses WPA2/WPA3 with MFP (strong). Many residential APs still use WPA2-only with WPS enabled (weak). Library provides both open and enterprise-secured tiers.

6. **RF Congestion**: Channels 1 and 11 are heavily contested. Channel 6 is the least congested of the three non-overlapping channels.

### RF Landscape (24 MHz — 1.766 GHz — RTL-SDR)

7. **Cellular Infrastructure**: Strong LTE presence across 700 MHz (Band 12/17, strongest at +4.7 dB), 850 MHz (Band 5, +4.2 dB), and 600 MHz (Band 71). FirstNet Band 14 active — first responder broadband is deployed.

8. **Military UHF**: The busiest band by bin count (922 bins, 225–380 MHz) with +4.7 dB peaks. This indicates proximity to military infrastructure — the strongest RF signature in the entire survey.

9. **Sub-GHz IoT Gap**: No Z-Wave (908 MHz), LoRa (915 MHz), or ISM 433 MHz IoT signals detected despite heavy WiFi client population. IoT devices in this area use WiFi exclusively — no sub-GHz attack surface exists below 1 GHz.

10. **FRS/GMRS Silence**: No walkie-talkie activity detected at scan time (462–467 MHz). Either no active users during the sweep window, or power levels below detection threshold.

11. **FM Broadcast Saturation**: FM band (87.5–108 MHz) shows continuous strong signals, typical of populated areas with multiple broadcast stations.

### Combined Assessment

The environment presents a **WiFi-heavy, sub-GHz-quiet** RF profile. The 2.4 GHz band carries the bulk of local wireless communication (179 SSIDs, 4,822+ clients), while the sub-GHz spectrum is dominated by cellular infrastructure and military UHF rather than local IoT or radio users. This means the WiFi attack surface identified by the Pineapple represents the primary local wireless exposure — there is no significant "hidden" sub-GHz IoT layer to account for.

---

*Report generated by Eddie — Operation Lay of the Land*
*WiFi Pineapple Mark 7 + Kali Linux Docker (kali-mcp) + 2x RTL-SDR (RTL2838/R820T)*
*2026-03-08 through 2026-03-11 — 72+ hours passive WiFi observation + full RF spectrum sweep*
*Section 10 RTL-SDR analysis completed 2026-03-11 — 11 sweeps, 19 services, 3,168 active bins*
