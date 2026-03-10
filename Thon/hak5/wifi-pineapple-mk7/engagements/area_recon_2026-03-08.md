# Area Reconnaissance Report — Pineapple Operating Environment

**Date:** 2026-03-08
**Operator:** Thon (Venom/Agent)
**Authority:** Eddie (Sovereign/Principal)
**Classification:** RECON ONLY — No exploitation, deauth, or association conducted
**Location:** TELUS5434 home network environment
**Equipment:** WiFi Pineapple Mark 7 (FW 2.1.3), MT7601U monitor radio (wlan1mon), wlan2 client radio

---

## Executive Summary

Conducted a comprehensive passive and active area reconnaissance sweep from the WiFi Pineapple MK7 to build a complete intelligence picture of the wireless and wired operating environment. Four-phase approach: wireless AP enumeration, WPS posture assessment, local network host discovery, and consolidation.

**Key Findings:**
- **42 unique access points** detected across channels 1-11 (2.4GHz band) via airodump-ng channel cycling
- **32 client stations** observed, including 4 probing for "SaskTel Select Wi-Fi 1"
- **14 WPS-enabled APs** identified, **6 with WPS UNLOCKED** (exploitable with Pixie Dust)
- **3 WPA3-capable networks** (MCSnet family) — strongest encryption in the area
- **3 open networks** (NETGEAR-OPEN-5G-HOME [Pineapple], Public Library Wireless, Open Access)
- **8 alive hosts** on 192.168.1.0/24 wired network
- **No LLDP neighbors** or **SNMP-responsive devices** detected
- Notable: Library infrastructure (3 SSIDs on same AP), MCSnet ISP presence (5+ APs), garbled probe requests suggesting malformed/fuzzing clients

---

## Phase 1: Wireless Landscape (802.11)

### Method
1. `iwinfo wlan2 scan` — Client radio survey (20 APs, snapshot)
2. `airodump-ng wlan1mon --band bg -w /tmp/area_recon` — Monitor mode, 7-minute channel-cycling capture (42 APs, 32 stations)

### Access Points (42 unique BSSIDs)

#### Named Networks (sorted by signal strength)

| BSSID | ESSID | Ch | Signal | Encryption | WPS | Notes |
|---|---|---|---|---|---|---|
| 02:13:37:A8:1A:57 | NETGEAR-5G-HOME | 11 | -19/-47 | WPA2 CCMP | — | Pineapple PineAP |
| 00:13:37:A8:1A:57 | NETGEAR-OPEN-5G-HOME | 11 | -19/-47 | OPEN | — | Pineapple Open AP |
| CC:28:AA:66:30:08 | OrionLink | 2 | -41/-47 | WPA2 CCMP | 2.0 UNLOCKED | Home network |
| 10:78:5B:FA:3C:12 | TELUS5434 | 11 | -50/-53 | WPA2 CCMP | 2.0 Locked | Home gateway |
| 4A:A9:8A:AB:D1:2D | MCSNET FREE | 1 | -56 | WPA3/WPA2 CCMP SAE | — | ISP hotspot |
| 4A:A9:8A:AB:D1:26 | MCSnet-b89f1 | 1 | -65 | WPA3/WPA2 CCMP SAE | 2.0 Locked | ISP |
| 4A:A9:8A:AB:D1:27 | Concession | 1 | -66 | WPA3/WPA2 CCMP SAE | — | ISP/venue |
| FC:2B:B2:EC:D4:52 | TELUS5150 | 11 | -63/-64 | WPA2 CCMP | 2.0 Locked | Neighbor |
| 1A:FD:74:A2:10:4A | MCSnet-6c55b | 1 | -65/-68 | WPA2 CCMP | 1.0 UNLOCKED | ISP |
| A2:CD:F3:5F:69:23 | My VW 0717 | 6 | -68/-69 | WPA2 CCMP | — | Vehicle WiFi |
| 9C:1E:95:CE:E8:C2 | Veenstra | 11 | -78/-81 | WPA2 CCMP | 2.0 Locked | Neighbor |
| C4:49:BB:A4:79:8A | DawsonTruck | 6 | -78 | CCMP TKIP PSK | — | Vehicle WiFi |
| 8C:79:09:99:BD:E5 | Public Library Wireless | 1 | -80 | OPEN | — | Library public |
| 92:07:1D:BC:0E:C4 | Ynet25 | 4 | -75/-81 | WPA2 CCMP | 2.0 UNLOCKED | Neighbor |
| 9C:1E:95:F1:B4:A2 | TELUS5297 | 11 | -81 | WPA2 CCMP | — | Neighbor |
| 9C:1E:95:D6:CA:B2 | TELUS5822 | 11 | -81/-82 | WPA2 CCMP | 2.0 Locked | Neighbor |
| A0:36:BC:4E:73:B9 | TELUS5434_RPT | 11 | -79/-82 | WPA2 CCMP | — | Home repeater |
| 18:D6:C7:6C:90:3F | gmamea | 6 | -82 | WPA2/WPA CCMP | — | Unknown |
| 66:C4:4A:23:9C:B7 | PHONK9876 | 6 | -83/-85 | WPA2 CCMP | — | Neighbor |
| 02:54:AF:F1:40:88 | Hotspot4088 | 6 | -53 | CCMP TKIP PSK | — | Mobile hotspot |
| 1E:D6:BE:70:20:83 | whiskey | 6 | -85 | WPA2 CCMP | 2.0 UNLOCKED | Neighbor |
| FC:2B:B2:F7:C8:C2 | TELUS5105 | 11 | -85 | WPA2 CCMP | 2.0 Locked | Neighbor |
| 4A:A9:8A:8B:5B:12 | MCSnet-a2505 | 1 | -85 | WPA3/WPA2 CCMP SAE | 2.0 Locked | ISP |
| 4A:A9:8A:8B:5B:17 | MCSnet-a2505-2GHz | 1 | -85 | WPA3/WPA2 CCMP SAE | 2.0 Locked | ISP |
| 8C:79:09:99:BD:E2 | Library Staff | 1 | -86 | WPA2 CCMP | — | Library staff |
| 8C:79:09:99:BD:E3 | Library BYOD | 1 | -87 | WPA2 CCMP | — | Library BYOD |
| 24:4B:FE:BF:92:B9 | M&M Guest | 2 | -88 | WPA2 CCMP | — | Business |
| — | Open Access | 11 | -85 | OPEN | — | Unknown open |

#### Hidden Networks (no ESSID broadcast)

| BSSID | Ch | Signal | Encryption | Notes |
|---|---|---|---|---|
| 46:6B:B8:6F:19:A7 | 11 | -67/-75 | WPA2 CCMP | Strong signal, WPS 2.0 UNLOCKED |
| 18:FD:74:A2:10:4A | 1 | -66 | WPA2 CCMP | Co-located with MCSnet-6c55b, WPS 1.0 UNLOCKED |
| 92:07:1D:BC:0E:C5 | 4 | -75/-79 | WPA2 CCMP | Co-located with Ynet25 |
| 48:A9:8A:AB:D1:26 | 1 | -68 | WPA3/WPA2 CCMP SAE | MCSnet infrastructure |
| FA:14:A2:04:83:50 | 11 | -83 | WPA2 CCMP CMAC | Single beacon, transient |
| 66:C4:4A:43:9C:B7 | 6 | -83 | WPA2 CCMP | Co-located with PHONK9876 |
| 66:C4:4A:63:9C:B7 | 6 | -82 | WPA2 CCMP | Co-located with PHONK9876 |

#### Channel Distribution

| Channel | AP Count | Notable Occupants |
|---|---|---|
| 1 | 10 | MCSnet family (5), Library (3), MCSnet-6c55b |
| 2 | 2 | OrionLink, M&M Guest |
| 4 | 2 | Ynet25 + hidden |
| 6 | 10 | PHONK9876, whiskey, DawsonTruck, My VW, gmamea, Hotspot4088 |
| 7 | 1 | Unknown (data-only) |
| 8 | 1 | Unknown (data-only) |
| 10 | 1 | Unknown (data-only) |
| 11 | 15 | TELUS family (5), Veenstra, Pineapple (2), hidden, Open Access |

**Assessment:** Channels 1, 6, and 11 are heavily congested (standard 2.4GHz pattern). Channel 2 is the least congested with notable targets (OrionLink).

### Client Stations (32 observed)

#### Associated Clients

| Station MAC | Associated To | Notes |
|---|---|---|
| 8C:49:62:51:51:AD | gmamea (18:D6:C7) | |
| 4C:BA:D7:A6:A4:1C | gmamea (18:D6:C7) | |
| B0:6B:11:52:E5:DB | MCSNET FREE (4A:A9:8A:AB:D1:2D) | |
| 22:39:FF:47:77:0A | MCSNET FREE (4A:A9:8A:AB:D1:2D) | |
| 38:1A:52:58:10:F6 | TELUS5150 (FC:2B:B2:EC:D4:52) | |
| 38:1A:52:53:12:B5 | TELUS5150 (FC:2B:B2:EC:D4:52) | |
| 5C:C1:D7:D7:A3:D4 | TELUS5297 (9C:1E:95:F1:B4:A2) | |

#### Probing Clients (not associated)

| Station MAC | Signal | Probed ESSID | Analysis |
|---|---|---|---|
| 52:B3:ED:57:68:8F | -76 | SaskTel Select Wi-Fi 1 | ISP hotspot seeker |
| 8E:92:7C:67:71:EA | -82 | SaskTel Select Wi-Fi 1 | ISP hotspot seeker |
| 76:2F:74:3A:AC:CE | -80 | SaskTel Select Wi-Fi 1 | ISP hotspot seeker |
| 4A:D8:33:50:7D:A8 | -72 | SaskTel Select Wi-Fi 1 | ISP hotspot seeker |
| BC:10:2F:2B:04:31 | -90 | Tater2021 | Home network absent |
| CA:F2:CB:EC:62:C7 | — | bapple | Possible typo SSID |
| BE:BF:39:32:37:B7 | -84 | hhbclàĺkugykhn | Garbled — possible fuzzing or firmware bug |
| 8E:AB:59:85:A7:E7 | -82 | nn | Truncated probe |

**Assessment:** Multiple devices actively seeking "SaskTel Select Wi-Fi 1" — this is a SaskTel ISP public hotspot SSID. These are likely mobile phones with saved SaskTel WiFi profiles. An Evil Twin for this SSID would attract multiple clients in this area (noted for future engagement planning — NOT executed in this recon).

---

## Phase 2: WPS Assessment

### Method
`wash -i wlan1mon -s` — Passive WPS beacon enumeration via monitor mode

### WPS-Enabled Access Points (14 detected)

| BSSID | ESSID | Ch | WPS Ver | WPS Locked | Risk |
|---|---|---|---|---|---|
| CC:28:AA:66:30:08 | OrionLink | 2 | 2.0 | **UNLOCKED** | HIGH — Pixie Dust candidate |
| 46:6B:B8:6F:19:A7 | *(hidden)* | 11 | 2.0 | **UNLOCKED** | HIGH — unknown owner |
| 18:FD:74:A2:10:4A | *(hidden)* | 1 | 1.0 | **UNLOCKED** | HIGH — WPS 1.0, weakest |
| 1A:FD:74:A2:10:4A | MCSnet-6c55b | 1 | 1.0 | **UNLOCKED** | HIGH — WPS 1.0 |
| 1E:D6:BE:70:20:83 | whiskey | 6 | 2.0 | **UNLOCKED** | HIGH — Pixie Dust candidate |
| 92:07:1D:BC:0E:C4 | Ynet25 | 4 | 2.0 | **UNLOCKED** | HIGH — Pixie Dust candidate |
| 10:78:5B:FA:3C:12 | TELUS5434 | 11 | 2.0 | Locked | LOW — rate-limited |
| FC:2B:B2:EC:D4:52 | TELUS5150 | 11 | 2.0 | Locked | LOW |
| 9C:1E:95:CE:E8:C2 | Veenstra | 11 | 2.0 | Locked | LOW |
| 4A:A9:8A:AB:D1:26 | MCSnet-b89f1 | 1 | 2.0 | Locked | LOW |
| FC:2B:B2:F7:C8:C2 | TELUS5105 | 11 | 2.0 | Locked | LOW |
| 9C:1E:95:D6:CA:B2 | TELUS5822 | 11 | 2.0 | Locked | LOW |
| 4A:A9:8A:8B:5B:12 | MCSnet-a2505 | 1 | 2.0 | Locked | LOW |
| 4A:A9:8A:8B:5B:17 | MCSnet-a2505-2GHz | 1 | 2.0 | Locked | LOW |

**Assessment:** 6 of 14 WPS-enabled APs have WPS UNLOCKED — vulnerable to Pixie Dust attacks (reaver -K). OrionLink is on the home network and the strongest unlocked target. Two WPS 1.0 devices (MCSnet-6c55b, hidden 18:FD:74) are the weakest — original WPS implementation with known PIN recovery flaws.

---

## Phase 3: Local Network Discovery (192.168.1.0/24)

### Method
1. `arp-scan -I wlan2 192.168.1.0/24` — Layer 2 host discovery
2. `fping -a -g 192.168.1.0/24 -I wlan2` — ICMP sweep
3. `lldpcli show neighbors` — LLDP/CDP neighbor discovery
4. `snmpwalk -v2c -c public 192.168.1.254` — Router SNMP enumeration

### Host Discovery (cross-referenced ARP + ICMP)

| IP | MAC | Vendor/OUI | ARP | ICMP | Identification |
|---|---|---|---|---|---|
| 192.168.1.254 | 10:78:5B:FA:3C:10 | Actiontec Electronics | Yes | Yes | TELUS gateway/router |
| 192.168.1.64 | CC:28:AA:66:30:08 | Unknown (locally admin) | Yes | No | OrionLink AP |
| 192.168.1.66 | BC:D7:D4:69:68:DA | Unknown | Yes | Yes | Roku streaming device |
| 192.168.1.67 | A0:36:BC:4E:73:B9 | Unknown (locally admin) | Yes | Yes | TELUS5434_RPT repeater |
| 192.168.1.68 | E8:CA:C8:83:52:AB | Unknown | Yes | Yes | **NEW** — unidentified device |
| 192.168.1.69 | CC:40:85:7A:A2:44 | Unknown (locally admin) | Yes | Yes | Home device |
| 192.168.1.71 | — | — | No | Yes | ICMP-only responder (no ARP) |
| 192.168.1.76 | 0C:EF:AF:CE:68:1E | — | — | Yes | Pineapple wlan2 (self) |

**Notable:** 192.168.1.68 (E8:CA:C8:83:52:AB) was not in the previous home device inventory from the earlier wireless_recon engagement. New device on network.

**Notable:** 192.168.1.71 responds to ICMP but not ARP — may be a device behind a bridge/NAT, or a firewall allowing ICMP but blocking ARP responses.

### Protocol Checks

| Protocol | Target | Result |
|---|---|---|
| LLDP/CDP | All interfaces | No neighbors — consumer network, no managed switches |
| SNMP v2c | 192.168.1.254 (public) | No response — SNMP disabled on router |

---

## Phase 4: Consolidation

### Environment Classification

| Category | Count | Details |
|---|---|---|
| Total APs | 42 | 28 named, 7 hidden, 7 data-only fragments |
| Home network APs | 4 | TELUS5434, TELUS5434_RPT, OrionLink, Pineapple (2 SSIDs) |
| ISP infrastructure | 7 | MCSnet (5), SaskTel probes (4 clients seeking), MCSNET FREE |
| TELUS neighbors | 5 | TELUS5150, 5105, 5297, 5822, 5243 |
| Library infrastructure | 3 | Public Library Wireless (OPEN), Library Staff, Library BYOD (same AP) |
| Vehicle hotspots | 2 | My VW 0717, DawsonTruck |
| Mobile hotspots | 1 | Hotspot4088 |
| Open networks | 3 | Pineapple Open AP, Public Library Wireless, Open Access |
| WPA3-capable | 3 | MCSnet-b89f1, MCSnet-a2505, MCSnet-a2505-2GHz, MCSNET FREE, Concession |
| WPS unlocked | 6 | OrionLink, whiskey, Ynet25, MCSnet-6c55b, 2x hidden |
| Wired hosts | 8 | 6 via ARP, 1 ICMP-only, 1 self (Pineapple) |

### Threat Surface Summary

**High-value targets (if authorized):**
1. **OrionLink** (192.168.1.64) — Home network AP, WPS 2.0 UNLOCKED, strongest signal on Ch2 (isolated channel). Pixie Dust viable.
2. **SaskTel Select Wi-Fi 1** — Not present but actively sought by 4+ client devices. Evil Twin opportunity.
3. **Public Library Wireless** — Open network, no encryption. Clients associating in clear.
4. **whiskey** — WPS 2.0 UNLOCKED, unknown owner, moderate signal.
5. **192.168.1.68** — New unidentified device on home network. Requires investigation.

**Defensive observations:**
- Home gateway TELUS5434 has WPS locked — good.
- SNMP disabled on router — good.
- No LLDP leaking switch topology — good (consumer gear, expected).
- MCSnet deploying WPA3/SAE — strongest encryption posture in the area.
- Library runs 3 SSIDs on one AP including an open network — standard public access pattern but clients are unprotected.

### Tool Performance Notes

| Tool | Status | Notes |
|---|---|---|
| horst | FAILED | ncurses terminal error in headless SSH — not viable for remote execution |
| airodump-ng (terminal) | PARTIAL | Terminal output only showed Pineapple's own APs via SSH pseudo-terminal |
| airodump-ng (CSV) | SUCCESS | Background script with --band bg produced full 42-AP, 32-station dataset |
| iwinfo scan | SUCCESS | Quick snapshot, 20 APs, reliable via SSH |
| wash | SUCCESS | 14 WPS APs with lock state, clean output |
| arp-scan | SUCCESS | 6 unique hosts, 7 responses (1 duplicate) |
| fping | SUCCESS | 7 alive hosts, cross-reference value with arp-scan |
| lldpcli | SUCCESS | Negative result (expected) |
| snmpwalk | SUCCESS | Negative result (SNMP disabled on router) |

### Cleanup Verification

- [x] All background processes killed (airodump-ng PIDs 5451, 5452, 5458)
- [x] Temp files removed (/tmp/area_recon*, /tmp/area_sweep*, /tmp/run_airodump.sh)
- [x] Pineapple daemon healthy on port 1471 (PID 3053)
- [x] Storage: 90.3MB / 1.8GB (5%) — no impact from scan operations
- [x] PineAP deny lists intact (12 MACs, 2 SSIDs)
- [x] No offensive actions taken — recon only

---

## Appendix A: Data Sources

| Source | Duration | Records | File |
|---|---|---|---|
| airodump-ng CSV | ~7 min (15:59–16:06) | 42 APs, 32 stations | /tmp/area_recon-01.csv (cleaned) |
| iwinfo wlan2 scan | Snapshot | 20 APs | Terminal output |
| wash -i wlan1mon | ~45 sec | 14 WPS APs | Terminal output |
| arp-scan wlan2 | 27.3 sec | 7 responses / 6 unique | Terminal output |
| fping wlan2 | ~5 sec | 7 alive | Terminal output |
| lldpcli | Instant | 0 neighbors | Terminal output |
| snmpwalk | Timeout | 0 responses | Terminal output |

## Appendix B: Probe Request Intelligence

Probed SSIDs reveal what networks clients have previously connected to:

| Probed SSID | Client Count | Analysis |
|---|---|---|
| SaskTel Select Wi-Fi 1 | 4 | SaskTel ISP public WiFi — clients have Saskatchewan mobile plans |
| Tater2021 | 1 | Personal home network, not present in area |
| bapple | 1 | Unknown network, possibly mistyped SSID |
| hhbclàĺkugykhn | 1 | Garbled UTF-8 — firmware bug, driver issue, or intentional fuzzing |
| nn | 1 | Truncated probe — incomplete beacon |

---

*Report generated by Thon (Venom) — WiFi Pineapple MK7 area reconnaissance*
*Engagement type: Passive/Active Reconnaissance — No exploitation conducted*
