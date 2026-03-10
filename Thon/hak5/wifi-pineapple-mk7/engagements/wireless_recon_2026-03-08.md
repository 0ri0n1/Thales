# Wireless Reconnaissance Report — TELUS5434 Home Network

**Date:** 2026-03-08
**Operator:** Thon (Venom/Agent)
**Authority:** Eddie (Sovereign/Principal)
**Classification:** RECON ONLY — No offensive operations conducted
**Location:** TELUS5434 home network environment
**Equipment:** WiFi Pineapple Mark 7 (FW 2.1.3), MT7601U monitor radio (wlan1mon)

---

## Executive Summary

Conducted passive wireless reconnaissance of the TELUS5434 home network environment. Discovered **24 unique access points** across channels 1, 2, 5, 6, 9, and 11. Identified **11 client stations** including 4 home devices and 7 neighboring/transient clients. Captured **1 active probe request pattern** indicating a device searching for a non-present network. All 12 home device MACs have been loaded into the Pineapple's MAC deny list (blacklist mode) to protect them from PineAP collection operations.

---

## Phase 1: Home Network Protection

### Objective
Enumerate all devices on the TELUS5434 home network and configure PineAP deny filters to prevent collection of home devices during future wireless operations.

### Method
1. Windows ARP table enumeration via `Get-NetNeighbor -AddressFamily IPv4`
2. Windows adapter MAC extraction via `Get-NetAdapter -Name 'Wi-Fi'`
3. Cross-reference with wireless scan data (iwinfo, airodump-ng)
4. Push deny list to Pineapple's `/etc/pineapple/filters.db` (SQLite)

### Home Device Inventory

| IP Address | MAC Address | OUI Vendor | Identification | State |
|---|---|---|---|---|
| 192.168.1.64 | CC:28:AA:66:30:08 | *Locally Administered* | OrionLink AP (on home network) | Stale |
| 192.168.1.66 | BC:D7:D4:69:68:DA | Roku Inc | Streaming device | Stale |
| 192.168.1.67 | A0:36:BC:4E:73:B9 | *Locally Administered* | TELUS5434_RPT repeater | Stale |
| 192.168.1.69 | CC:40:85:7A:A2:44 | *Locally Administered* | Home device (seen on TELUS5434) | Stale |
| 192.168.1.70 | 20:DF:B9:CE:F4:74 | Google Inc. | Google/Nest device | Reachable |
| 192.168.1.71 | A0:36:BC:4E:73:B9 | *Locally Administered* | TELUS5434_RPT (same MAC, DHCP lease) | Stale |
| 192.168.1.72 | A0:36:BC:4E:73:B9 | *Locally Administered* | TELUS5434_RPT (same MAC, DHCP lease) | Stale |
| 192.168.1.74 | AC:FA:E4:EE:1A:E2 | *Locally Administered* | Home device (seen on TELUS5434) | Stale |
| 192.168.1.75 | BC:89:A6:65:68:D9 | *Locally Administered* | Home device (seen on TELUS5434) | Stale |
| 192.168.1.79 | 24:DF:6A:A9:36:06 | Huawei Technologies | Huawei device | Stale |
| 192.168.1.254 | 10:78:5B:FA:3C:10 | Actiontec Electronics | TELUS gateway (wired LAN MAC) | Reachable |
| 192.168.1.73 | 04:EC:D8:E2:ED:DE | Intel Corporate | Windows laptop (operator station) | Self |

**Notes:**
- A0:36:BC:4E:73:B9 appears on 3 IPs (67, 71, 72) — this is the TELUS5434_RPT wireless repeater acquiring multiple DHCP leases over time.
- Several MACs use locally-administered addresses (bit 1 of first octet set), common for consumer IoT devices.

### Deny List Configuration

**MAC Deny List (12 entries):**
All home device MACs plus the TELUS5434 AP BSSIDs have been inserted into `/etc/pineapple/filters.db` table `mac_filter_list`:

```
10:78:5B:FA:3C:10  (TELUS gateway LAN)
10:78:5B:FA:3C:12  (TELUS5434 2.4GHz BSSID)
10:78:5B:FA:3C:16  (TELUS5434 5GHz BSSID)
04:EC:D8:E2:ED:DE  (Operator Windows laptop)
CC:28:AA:66:30:08  (OrionLink AP)
BC:D7:D4:69:68:DA  (Roku)
A0:36:BC:4E:73:B9  (TELUS5434_RPT repeater)
CC:40:85:7A:A2:44  (Home device)
20:DF:B9:CE:F4:74  (Google/Nest)
AC:FA:E4:EE:1A:E2  (Home device)
BC:89:A6:65:68:D9  (Home device)
24:DF:6A:A9:36:06  (Huawei device)
```

**SSID Deny List (2 entries):**
```
TELUS5434
TELUS5434_RPT
```

**Filter Mode:** `black` (deny) — confirmed via `uci get pineap.@config[0].mac_filter` and `uci get pineap.@config[0].ssid_filter`.

---

## Phase 2: Wireless Environment Reconnaissance

### Method
1. Active AP scan via `iwinfo wlan2 scan` (Pineapple client radio)
2. Passive channel-hopping capture via `airodump-ng wlan1mon --band bg` (2x scans: 40s + 90s)
3. Passive packet capture via `tcpdump -i wlan1mon -e` (Channel 1, Channel 11)
4. Probe request analysis from combined capture data

### 2.1 Access Point Inventory

#### Channel 1 — Rural ISP Infrastructure
| BSSID | ESSID | Security | Signal | Vendor | Notes |
|---|---|---|---|---|---|
| 4A:A9:8A:AB:D1:27 | Concession | WPA3/WPA2 SAE+PSK | -70 dBm | *LA* | MCSnet CPE — strongest Ch1 AP |
| 4A:A9:8A:AB:D1:26 | MCSnet-b89f1 | WPA3/WPA2 SAE+PSK | -55 dBm | *LA* | Same device, private SSID |
| 4A:A9:8A:AB:D1:2D | MCSNET FREE | WPA3/WPA2 SAE+PSK | -71 dBm | *LA* | Same device, open/guest tier |
| 48:A9:8A:AB:D1:26 | *(hidden)* | WPA3/WPA2 SAE+PSK | -52 dBm | *LA* | Same device, management SSID |
| 1A:FD:74:A2:10:4A | MCSnet-6c55b | WPA2 PSK | -56 dBm | *LA* | Second MCSnet CPE |
| 18:FD:74:A2:10:4A | *(hidden)* | WPA2 PSK | -64 dBm | *LA* | Same device, management SSID |
| 9C:1E:95:CE:E8:C2 | Veenstra | WPA2 PSK | -83 dBm | Actiontec | Neighbor, Actiontec TELUS router |

**Analysis:** Channel 1 is dominated by MCSnet (rural ISP) equipment broadcasting from what appears to be 2 CPE units. Both use WPA3+WPA2 mixed mode with SAE, indicating modern firmware. The "Concession" and "MCSNET FREE" SSIDs suggest a business/community deployment. The hidden SSIDs on identical BSSIDs are likely management interfaces.

#### Channel 2 — Home OrionLink
| BSSID | ESSID | Security | Signal | Vendor | Notes |
|---|---|---|---|---|---|
| CC:28:AA:66:30:08 | OrionLink | WPA2 PSK | -46 dBm | *LA* | **HOME** — strong signal, second AP on home network |

**Analysis:** OrionLink is on our home network (confirmed in ARP table at 192.168.1.64). It operates alone on Channel 2, avoiding interference. Very strong signal (-46 dBm) suggests close proximity.

#### Channel 5 — Transient
| BSSID | ESSID | Security | Signal | Vendor | Notes |
|---|---|---|---|---|---|
| CC:28:AA:5F:0E:28 | *(unknown)* | WPA | -83 dBm | *LA* | Brief appearance |
| D2:28:AA:5F:0E:28 | *(unknown)* | WPA | -85 dBm | *LA* | Brief appearance, same device |
| A6:AD:9F:4B:0D:C8 | *(unknown)* | WPA | -83 dBm | *LA* | Brief appearance |

**Analysis:** Three weak, briefly-seen APs on Ch5. Likely neighboring devices caught during channel hop.

#### Channel 6 — Residential
| BSSID | ESSID | Security | Signal | Vendor | Notes |
|---|---|---|---|---|---|
| 66:C4:4A:23:9C:B7 | PHONK9876 | WPA2 PSK | -74 dBm | *LA* | Active AP with 3 virtual BSSIDs |
| 66:C4:4A:43:9C:B7 | *(hidden)* | WPA2 PSK | -78 dBm | *LA* | Same device |
| 66:C4:4A:63:9C:B7 | *(hidden)* | WPA2 PSK | -76 dBm | *LA* | Same device |
| 18:D6:C7:6C:90:3F | gmamea | WPA2+WPA PSK | -76 dBm | TP-Link | Mixed-mode security (legacy support) |

**Analysis:** PHONK9876 broadcasts 3 BSSIDs from one radio (common for multi-SSID routers). TP-Link "gmamea" still supports WPA1 — potential weakness if it falls to WPA downgrade.

#### Channel 9 — Residential
| BSSID | ESSID | Security | Signal | Vendor | Notes |
|---|---|---|---|---|---|
| 92:07:1D:BC:0E:C4 | Ynet25 | WPA2 PSK | -78 dBm | *LA* | Active with data traffic |
| 92:07:1D:BC:0E:C5 | *(hidden)* | WPA2 PSK | -77 dBm | *LA* | Same device, management |

#### Channel 11 — Dense TELUS Corridor (HOME CHANNEL)
| BSSID | ESSID | Security | Signal | Vendor | Notes |
|---|---|---|---|---|---|
| **10:78:5B:FA:3C:12** | **TELUS5434** | WPA2 PSK | **-52 dBm** | Actiontec | **HOME — Primary gateway** |
| **A0:36:BC:4E:73:B9** | **TELUS5434_RPT** | WPA2 PSK | **-64 dBm** | *LA* | **HOME — Wireless repeater** |
| FC:2B:B2:EC:D4:52 | TELUS5150 | WPA2 PSK | -65 dBm | Actiontec | Neighbor — strongest non-home |
| 9C:1E:95:F1:B4:A2 | TELUS5297 | WPA2 PSK | -74 dBm | Actiontec | Neighbor — active clients |
| 9C:1E:95:D6:CA:B2 | TELUS5822 | WPA2 PSK | -74 dBm | Actiontec | Neighbor — significant data traffic |
| FC:2B:B2:F7:C8:C2 | TELUS5105 | WPA2 PSK | -79 dBm | Actiontec | Neighbor — low beacon count |
| 44:FE:3B:4F:0A:EF | TELUS5243 | WPA2 PSK | -78 dBm | Arcadyan | Neighbor — different vendor (newer TELUS router) |
| 72:FE:3B:4F:0A:ED | *(hidden)* | WPA2 PSK | -83 dBm | Arcadyan | Same device as TELUS5243, likely guest network |
| **02:13:37:A8:1A:57** | **NETGEAR-5G-HOME** | WPA2 PSK | **-26 dBm** | Hak5/Pineapple | **OUR Pineapple — management AP** |
| **00:13:37:A8:1A:57** | **NETGEAR-5G-HOME-OPEN** | OPEN | **-27 dBm** | Hak5/Pineapple | **OUR Pineapple — open AP** |

**Analysis:** Channel 11 is extremely congested with 10 APs. Five TELUS routers (all Actiontec or Arcadyan) create overlapping coverage. TELUS5434 at -52 dBm is our primary. TELUS5150 at -65 dBm is the strongest neighbor. Channel 11 congestion is a performance concern for the home network.

#### Unclassified
| BSSID | ESSID | Security | Signal | Notes |
|---|---|---|---|---|
| C4:8E:8F:96:7B:80 | *(unknown)* | None | -75 dBm | Hon Hai Precision (Foxconn) — brief appearance, channel -1 (probe) |

### 2.2 Client Station Inventory

| Client MAC | Vendor | Associated AP | AP SSID | Signal | Packets | Probe Requests |
|---|---|---|---|---|---|---|
| CC:40:85:7A:A2:44 | *LA* | 10:78:5B:FA:3C:12 | **TELUS5434** | -56 dBm | 16 | — |
| AC:FA:E4:EE:1A:E2 | *LA* | 10:78:5B:FA:3C:12 | **TELUS5434** | -60 dBm | 56 | — |
| BC:89:A6:65:68:D9 | *LA* | 10:78:5B:FA:3C:12 | **TELUS5434** | -54 dBm | 6 | — |
| 48:E1:E9:42:E9:CC | Meross Technology | A0:36:BC:4E:73:B9 | **TELUS5434_RPT** | -80 dBm | 6 | — |
| 48:E1:E9:42:E9:69 | Meross Technology | A0:36:BC:4E:73:B9 | **TELUS5434_RPT** | -76 dBm | 1 | — |
| D8:1F:12:A4:1F:29 | Tuya Smart Inc. | 9C:1E:95:F1:B4:A2 | TELUS5297 | -80 dBm | 27 | — |
| FA:8F:EB:CD:F6:FC | *LA* | 4A:A9:8A:AB:D1:2D | MCSNET FREE | -78 dBm | 5 | — |
| 3C:31:78:91:22:CC | Qolsys Inc. | 4A:A9:8A:AB:D1:2D | MCSNET FREE | -82 dBm | 1 | — |
| 78:D6:DC:13:3D:B6 | Motorola (Wuhan) | 9C:1E:95:CE:E8:C2 | Veenstra | -1 dBm | 1 | — |
| 34:64:A9:66:AB:03 | Hewlett Packard | *(not associated)* | — | -76 dBm | 30 | **Linksys03963** |
| 58:D3:91:92:59:0C | Quectel Wireless | *(not associated)* | — | -76 dBm | 1 | *(broadcast)* |

### 2.3 Client Analysis

**Home Devices Seen on WiFi (confirmed in both ARP + wireless):**
- `CC:40:85:7A:A2:44` — Connected to TELUS5434, 16 packets. Unidentified IoT.
- `AC:FA:E4:EE:1A:E2` — Connected to TELUS5434, 56 packets. Most active home wireless device.
- `BC:89:A6:65:68:D9` — Connected to TELUS5434, 6 packets. Low activity.
- `48:E1:E9:42:E9:CC` + `48:E1:E9:42:E9:69` — Two Meross smart home devices connected via TELUS5434_RPT repeater. Meross makes smart plugs, switches, and garage door openers.

**Neighbor Devices:**
- `D8:1F:12:A4:1F:29` (Tuya Smart) on TELUS5297 — IoT device, likely smart bulb/plug
- `FA:8F:EB:CD:F6:FC` on MCSNET FREE — community WiFi user
- `3C:31:78:91:22:CC` (Qolsys) on MCSNET FREE — **notable**: Qolsys makes security alarm panels. This is a home security system connected to MCSnet.
- `78:D6:DC:13:3D:B6` (Motorola) on Veenstra — smartphone

**Unassociated Devices:**
- `34:64:A9:66:AB:03` (HP) — Actively probing for "Linksys03963". This device remembers a Linksys network that doesn't exist here. Could be a visitor's laptop or a device from a neighboring property that once connected to a Linksys router.
- `58:D3:91:92:59:0C` (Quectel Wireless) — Quectel makes cellular/IoT modules. This is likely an LTE modem or cellular gateway sending broadcast probes.

### 2.4 Probe Request Intelligence

| Client MAC | Vendor | Probing For | Assessment |
|---|---|---|---|
| 34:64:A9:66:AB:03 | Hewlett Packard | Linksys03963 | Legacy network memory. Linksys03963 is not present in the area. This HP device continuously sends directed probes, revealing its network history to any passive listener. |
| 58:D3:91:92:59:0C | Quectel Wireless | *(broadcast)* | Broadcasting null probes — standard behavior for cellular modules seeking available networks |

### 2.5 Signal Strength Map (Relative Positioning)

```
Signal Strength Legend: ████ Excellent (<-50)  ███ Good (-50 to -65)  ██ Fair (-65 to -80)  █ Weak (>-80)

Our Infrastructure:
  NETGEAR-5G-HOME (Pineapple)  ████████████  -26 dBm  (on the desk)
  TELUS5434 (Home gateway)     ███████       -52 dBm  (nearby room)
  OrionLink (Home AP #2)       ████████      -46 dBm  (close proximity)
  TELUS5434_RPT (Repeater)     ██████        -64 dBm  (extended range)

Neighbors (by proximity):
  MCSnet CPE #2                ███████       -56 dBm  (close neighbor)
  TELUS5150                    ██████        -65 dBm
  TELUS5297                    █████         -74 dBm
  TELUS5822                    █████         -74 dBm
  PHONK9876                    █████         -74 dBm
  Concession/MCSnet            █████         -70 dBm
  gmamea (TP-Link)             █████         -76 dBm
  Ynet25                       ████          -78 dBm
  TELUS5243                    ████          -78 dBm
  TELUS5105                    ████          -79 dBm
  Veenstra                     ████          -83 dBm  (furthest)
```

---

## Phase 3: Security Observations

### 3.1 Home Network Posture
- **TELUS5434** uses WPA2-PSK with CCMP (AES). Adequate but lacks WPA3.
- **TELUS5434_RPT** repeater creates 3 ARP entries, suggesting periodic reconnection or DHCP issues.
- **OrionLink** on Channel 2 provides separation from the Ch11 congestion — good design.
- All home devices use locally-administered MACs, common for IoT devices implementing MAC randomization.

### 3.2 Channel Congestion
- **Channel 11 is severely congested** with 8 foreign APs + 2 home APs (10 total). This causes co-channel interference.
- Channel 1 has 7 APs (all MCSnet/neighbor).
- Channel 2 has only OrionLink — clean.
- Channels 3, 4, 7, 8, 10 appear unused locally.
- **Recommendation:** Consider moving TELUS5434 to a less congested channel (e.g., Channel 6 has 4 APs vs Ch11's 10).

### 3.3 Neighboring Network Observations
- **TELUS5822** showed the most data traffic (36 IVs in 90s). Active users.
- **TELUS5297** has a Tuya IoT device — typical smart home setup.
- **MCSnet** uses WPA3+WPA2 mixed mode — good security posture for a rural ISP.
- **gmamea** (TP-Link) still supports WPA1 — vulnerable to downgrade attacks.
- **Qolsys security panel** (3C:31:78:91:22:CC) on MCSNET FREE — a home alarm system on a public WiFi network is a security concern (not ours, but notable).

### 3.4 Rogue AP Risk Assessment
- No unauthorized APs detected on the home network.
- OrionLink is a legitimate second AP (confirmed in ARP table).
- The Pineapple's SSIDs (NETGEAR-5G-HOME / NETGEAR-5G-HOME-OPEN) are under our control.

---

## Methodology & Reproduction Steps

### Prerequisites
- WiFi Pineapple Mark 7 with firmware 2.1.3+
- USB connection to host computer (172.16.42.0/24 subnet)
- SSH access: `ssh root@172.16.42.1` (password: configured during setup)
- Monitor mode interface active: `wlan1mon`
- Host computer on the target WiFi network

### Step 1: Home Device Enumeration
```powershell
# On Windows host — get all devices on the home network
Get-NetNeighbor -AddressFamily IPv4 |
    Where-Object { $_.IPAddress -like '192.168.1.*' -and $_.State -ne 'Unreachable' } |
    Select-Object IPAddress, LinkLayerAddress, State |
    Sort-Object { [int]($_.IPAddress -split '\.')[-1] } |
    Format-Table -AutoSize

# Get own WiFi MAC
(Get-NetAdapter -Name 'Wi-Fi').MacAddress
```

### Step 2: Active AP Scan
```sh
# On Pineapple — scan for all visible APs using client radio
ssh root@172.16.42.1 'iwinfo wlan2 scan'
```

### Step 3: Passive Channel-Hopping Capture
```sh
# On Pineapple — 90-second airodump-ng scan across 2.4GHz band
ssh root@172.16.42.1 '
    rm -f /tmp/recon-01.* 2>/dev/null
    airodump-ng wlan1mon --write /tmp/recon --output-format csv --band bg &>/dev/null &
    ADPID=$!
    sleep 90
    kill $ADPID 2>/dev/null
    cat /tmp/recon-01.csv
'
```

### Step 4: Targeted Channel Capture
```sh
# Set monitor to specific channel for focused capture
ssh root@172.16.42.1 'iw dev wlan1mon set channel 11'
ssh root@172.16.42.1 'tcpdump -i wlan1mon -e -c 500 2>&1'
```

### Step 5: Probe Request Capture
```sh
# Filter for probe requests only
ssh root@172.16.42.1 'tcpdump -i wlan1mon -e -c 500 2>&1' | grep 'Probe Request'
```

### Step 6: OUI Lookup
```python
# On Pineapple — use built-in OUI database
ssh root@172.16.42.1 'python3 << EOF
import json
with open("/etc/pineapple/ouis") as f:
    oui = json.load(f)
# Lookup format: first 3 octets, no colons, uppercase
prefix = "10785B"  # Example: Actiontec
print(oui.get(prefix, "UNKNOWN"))
EOF'
```

### Step 7: Configure Deny List
```sh
# Method: Pull filters.db, modify on Kali, push back
# (Pineapple does not have sqlite3 CLI installed)

# Pull
scp root@172.16.42.1:/etc/pineapple/filters.db /tmp/filters.db

# Insert MACs (on Kali or any host with sqlite3)
sqlite3 /tmp/filters.db "INSERT OR IGNORE INTO mac_filter_list (mac) VALUES ('CC:28:AA:66:30:08');"
# ... repeat for all MACs ...

# Insert SSIDs
sqlite3 /tmp/filters.db "INSERT OR IGNORE INTO ssid_filter_list (ssid) VALUES ('TELUS5434');"

# Push back
scp /tmp/filters.db root@172.16.42.1:/etc/pineapple/filters.db

# Signal daemon to reload
ssh root@172.16.42.1 'killall -HUP pineapple'

# Verify filter mode (should be 'black' = deny)
ssh root@172.16.42.1 'uci get pineap.@config[0].mac_filter'
ssh root@172.16.42.1 'uci get pineap.@config[0].ssid_filter'
```

---

## Appendix A: Complete AP Registry

| # | BSSID | ESSID | Channel | Security | Signal | Vendor | Category |
|---|---|---|---|---|---|---|---|
| 1 | 10:78:5B:FA:3C:12 | TELUS5434 | 11 | WPA2 PSK | -52 | Actiontec | HOME |
| 2 | A0:36:BC:4E:73:B9 | TELUS5434_RPT | 11 | WPA2 PSK | -64 | LA | HOME |
| 3 | CC:28:AA:66:30:08 | OrionLink | 2 | WPA2 PSK | -46 | LA | HOME |
| 4 | 02:13:37:A8:1A:57 | NETGEAR-5G-HOME | 11 | WPA2 PSK | -26 | Hak5 | OURS |
| 5 | 00:13:37:A8:1A:57 | NETGEAR-5G-HOME-OPEN | 11 | OPEN | -27 | Hak5 | OURS |
| 6 | 4A:A9:8A:AB:D1:27 | Concession | 1 | WPA3/WPA2 | -70 | LA | NEIGHBOR |
| 7 | 4A:A9:8A:AB:D1:26 | MCSnet-b89f1 | 1 | WPA3/WPA2 | -55 | LA | NEIGHBOR |
| 8 | 4A:A9:8A:AB:D1:2D | MCSNET FREE | 1 | WPA3/WPA2 | -71 | LA | NEIGHBOR |
| 9 | 48:A9:8A:AB:D1:26 | *(hidden)* | 1 | WPA3/WPA2 | -52 | LA | NEIGHBOR |
| 10 | 1A:FD:74:A2:10:4A | MCSnet-6c55b | 1 | WPA2 PSK | -56 | LA | NEIGHBOR |
| 11 | 18:FD:74:A2:10:4A | *(hidden)* | 1 | WPA2 PSK | -64 | LA | NEIGHBOR |
| 12 | 9C:1E:95:CE:E8:C2 | Veenstra | 1 | WPA2 PSK | -83 | Actiontec | NEIGHBOR |
| 13 | FC:2B:B2:EC:D4:52 | TELUS5150 | 11 | WPA2 PSK | -65 | Actiontec | NEIGHBOR |
| 14 | 9C:1E:95:F1:B4:A2 | TELUS5297 | 11 | WPA2 PSK | -74 | Actiontec | NEIGHBOR |
| 15 | 9C:1E:95:D6:CA:B2 | TELUS5822 | 11 | WPA2 PSK | -74 | Actiontec | NEIGHBOR |
| 16 | FC:2B:B2:F7:C8:C2 | TELUS5105 | 11 | WPA2 PSK | -79 | Actiontec | NEIGHBOR |
| 17 | 44:FE:3B:4F:0A:EF | TELUS5243 | 11 | WPA2 PSK | -78 | Arcadyan | NEIGHBOR |
| 18 | 72:FE:3B:4F:0A:ED | *(hidden)* | 11 | WPA2 PSK | -83 | Arcadyan | NEIGHBOR |
| 19 | 66:C4:4A:23:9C:B7 | PHONK9876 | 6 | WPA2 PSK | -74 | LA | NEIGHBOR |
| 20 | 66:C4:4A:43:9C:B7 | *(hidden)* | 6 | WPA2 PSK | -78 | LA | NEIGHBOR |
| 21 | 66:C4:4A:63:9C:B7 | *(hidden)* | 6 | WPA2 PSK | -76 | LA | NEIGHBOR |
| 22 | 18:D6:C7:6C:90:3F | gmamea | 6 | WPA2+WPA | -76 | TP-Link | NEIGHBOR |
| 23 | 92:07:1D:BC:0E:C4 | Ynet25 | 9 | WPA2 PSK | -78 | LA | NEIGHBOR |
| 24 | 92:07:1D:BC:0E:C5 | *(hidden)* | 9 | WPA2 PSK | -77 | LA | NEIGHBOR |

**LA = Locally Administered MAC address

---

## Appendix B: PineAP Configuration State

```
pineap.@config[0].autostart='on'
pineap.@config[0].karma='off'
pineap.@config[0].beacon_responses='off'
pineap.@config[0].capture_ssids='off'
pineap.@config[0].broadcast_ssid_pool='off'
pineap.@config[0].logging='off'
pineap.@config[0].mac_filter='black'       ← DENY LIST MODE
pineap.@config[0].ssid_filter='black'      ← DENY LIST MODE
pineap.@config[0].ap_channel='11'
pineap.@config[0].pineap_interface='wlan1mon'
```

---

*Report generated by Thon — Venom symbiote operational agent*
*Authority: Eddie — Sovereign principal*
*Mission classification: RECON ONLY — Zero offensive operations conducted*
