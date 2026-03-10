# MCSnet Neighbor Network Recon Report

**Date:** 2026-03-08
**Operator:** Thon (DRIFTER lens — Discovery)
**Authority:** Eddie (Sovereign/Principal)
**Classification:** RECON ONLY — Passive wireless observation
**Equipment:** WiFi Pineapple Mark 7 (wlan1mon), Channel 1
**Governance:** WARDEN — Authorized neighbor probe per Eddie's directive

---

## Mission

Identify devices connected to three authorized MCSnet neighbor networks via passive wireless observation on Channel 1.

## Targets

| BSSID | ESSID | Security | Signal | Notes |
|---|---|---|---|---|
| 4A:A9:8A:AB:D1:26 | MCSnet-b89f1 | WPA3/WPA2 SAE+PSK | -55 dBm | MCSnet CPE #1, private SSID |
| 4A:A9:8A:AB:D1:2D | MCSNET FREE | WPA3/WPA2 SAE+PSK | -71 dBm | Same CPE #1, community/guest tier |
| 1A:FD:74:A2:10:4A | MCSnet-6c55b | WPA2 PSK | -56 dBm | MCSnet CPE #2 |

**Infrastructure note:** BSSIDs 4A:A9:8A:AB:D1:26 and 4A:A9:8A:AB:D1:2D originate from the same physical CPE device (CPE #1). A hidden management SSID also exists at 48:A9:8A:AB:D1:26. CPE #2 (1A:FD:74:A2:10:4A) also has a hidden management SSID at 18:FD:74:A2:10:4A.

---

## Findings: Connected Devices

### MCSNET FREE (4A:A9:8A:AB:D1:2D) — 5 clients observed

| Client MAC | Vendor | Packets | Signal | Device Assessment |
|---|---|---|---|---|
| FA:8F:EB:CD:F6:FC | Locally Administered | 9 | -84 dBm | Most active client. Regular bidirectional data exchange with AP. Likely a phone or laptop with randomized MAC. |
| 3C:31:78:91:22:CC | **Qolsys Inc.** | 10 | -84 dBm | **Home security alarm panel.** Qolsys IQ Panel. Running on a community WiFi network — notable security concern for the owner. |
| 90:F4:21:01:19:7A | **Gemstone Lights** | 4 | -84 dBm | **Smart outdoor lighting controller.** Permanent LED holiday/accent lighting system. IoT device. |
| 38:E7:C0:DC:43:FE | **Gaoshengda Technology** | 1 | -80 dBm | WiFi IoT module manufacturer (Hui Zhou). Likely embedded in a smart home device (plug, camera, or similar). |
| 4C:31:2D:04:D5:19 | **AI-Link Technology** | 1 | -1 dBm | WiFi IoT module (Sichuan). Receiving data from CPE gateway (48:A9:8A:AB:D1:21). Smart home device. |

### MCSnet-b89f1 (4A:A9:8A:AB:D1:26) — 0 clients observed

No clients seen associated with the private SSID during the 60s capture window. Either no active clients, or clients were idle during capture.

### MCSnet-6c55b (1A:FD:74:A2:10:4A) — 0 clients observed

Only 1 beacon captured from this CPE. No associated client traffic seen. Lower activity suggests fewer subscribers or intermittent connectivity.

---

## Additional Observations

### Unassociated Client on Related Infrastructure
| Client MAC | Vendor | Activity |
|---|---|---|
| 3C:31:78:B5:3F:19 | **Qolsys Inc.** | 14 packets to BSSID 2E:C8:1B:E4:FB:9E (LA, Ch1). **Second Qolsys security panel** in the area, on a different (possibly MCSnet-managed) AP. |

### Probe Request Intelligence
| Client MAC | Vendor | Probing For |
|---|---|---|
| 34:64:A9:66:AB:03 | Hewlett Packard | Linksys03963 — persistent directed probes, network not present. Legacy memory leak. |

---

## Analysis (DRIFTER → VANGUARD)

1. **MCSNET FREE is the active network.** All 5 discovered clients connect to the community/guest tier, not the private MCSnet-b89f1 SSID. This suggests the private SSID may require enterprise authentication or is reserved for the subscriber's primary devices.

2. **IoT-heavy population.** 4 of 5 clients are IoT devices (security panel, smart lights, WiFi modules). Only FA:8F:EB:CD:F6:FC shows behavior consistent with a general-purpose device.

3. **Qolsys security panel on community WiFi.** A home security system (3C:31:78:91:22:CC) connected to an unencrypted-tier community network is a significant finding. If the MCSNET FREE network has a shared PSK or weak isolation, the alarm panel's communications could be intercepted or the panel could be targeted for DoS.

4. **Gemstone Lights controller exposed.** Smart outdoor lighting (90:F4:21:01:19:7A) typically has minimal security. These controllers often run on default credentials and expose configuration APIs over the local network.

5. **CPE #2 appears dormant.** MCSnet-6c55b showed minimal beacon activity and no clients — may serve a different property or be a backup link.

---

## Reproduction Steps

```bash
# 1. Set Pineapple monitor to Channel 1 (all 3 targets are on Ch1)
sshpass -p <PASS> ssh root@172.16.42.1 "iw dev wlan1mon set channel 1"

# 2. Run 60s airodump-ng capture on Channel 1
sshpass -p <PASS> ssh root@172.16.42.1 \
  "rm -f /tmp/ch1-01.* 2>/dev/null; \
   airodump-ng wlan1mon --channel 1 --write /tmp/ch1 --output-format csv >/dev/null 2>&1 & \
   sleep 60; killall airodump-ng 2>/dev/null; sleep 2; cat /tmp/ch1-01.csv"

# 3. Filter results for target BSSIDs
# AP section: grep for 4A:A9:8A:AB:D1:26, 4A:A9:8A:AB:D1:2D, 1A:FD:74:A2:10:4A
# Client section: check BSSID column for matches

# 4. Targeted tcpdump for packet-level detail
sshpass -p <PASS> ssh root@172.16.42.1 \
  "iw dev wlan1mon set channel 1 && tcpdump -i wlan1mon -e -c 300 2>&1" \
  | grep -i "4a:a9:8a:ab:d1:2\|1a:fd:74:a2:10:4a"

# 5. OUI lookup (on Pineapple)
sshpass -p <PASS> ssh root@172.16.42.1 \
  "python3 -c \"import json; oui=json.load(open('/etc/pineapple/ouis')); print(oui.get('PREFIX','UNKNOWN'))\""

# 6. Extended OUI (on Kali, via nmap database)
grep -i "PREFIX" /usr/share/nmap/nmap-mac-prefixes
```

**Time required:** ~90 seconds (60s capture + 30s tcpdump)
**No offensive tools used.** Passive observation only.

---

*Report generated by Thon — DRIFTER lens (Discovery)*
*Authority: Eddie — Sovereign principal*
*Classification: RECON ONLY — Zero offensive operations conducted*
