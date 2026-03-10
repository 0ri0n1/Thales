# Lepro Smart Lightbulb — Full Compromise Report

**Date**: 2026-03-09 to 2026-03-10  
**Operator**: Thon (autonomous, Eddie-authorized)  
**Collection Platform**: WiFi Pineapple Mark 7 (wlan2 @ 192.168.1.76)  
**Analysis Platform**: Kali Linux (kali-mcp-pentest container)  
**Capture Duration**: 5 minutes (540.68 seconds actual)  
**Capture File**: `lepro_capture.pcap`  
**Outcome**: **FULL DEVICE COMPROMISE — local key extracted, LAN control demonstrated**

---

## Target Identification

| Field | Value |
|-------|-------|
| IP Address | 192.168.1.82 |
| MAC Address | `70:89:76:25:f3:ab` |
| OUI Vendor | **Tuya Smart Inc.** (Hong Kong) |
| Network | TELUS5434 (2.4 GHz, channel 6) |
| Ping RTT | 255ms (high for LAN — typical of power-saving IoT) |

**Key Finding**: The Lepro bulb is a **Tuya-based** device. Lepro does not manufacture its own WiFi chipset or firmware — it is a white-label product running the Tuya IoT platform.

---

## Traffic Summary

| Metric | Value |
|--------|-------|
| Total Packets | 104 |
| Total Bytes | 21,024 (22.7 KB on disk with pcap headers) |
| UDP Packets | 96 (92.3% of traffic) |
| ARP Packets | 8 (7.7% of traffic) |
| DNS Packets | 0 |
| TCP Packets | 0 |
| Unique External IPs contacted | 0 |

---

## Protocol Analysis

### UDP Discovery Beacon (96 packets)

| Field | Value |
|-------|-------|
| Source | 192.168.1.82:50098 |
| Destination | 255.255.255.255:6667 |
| Packet Size | 214 bytes each |
| Interval | ~5.0 seconds (4.9-5.2s variance) |
| Payload | Encrypted, identical across all 96 packets |
| Protocol | **Tuya Protocol v3.3** (encrypted LAN discovery) |

**Protocol Identification**: 
- Magic header: `0x000055AA` (Tuya protocol start marker)
- Magic footer: `0x0000AA55` (Tuya protocol end marker)
- Command byte `0x13` = Tuya device status broadcast
- Payload length field: `0x9C` (156 bytes of encrypted data)
- Destination port 6667 = **Tuya v3.3 encrypted** discovery channel
- Encryption: AES-ECB with the device's local key (GCM on newer firmware)

**Broadcast Behavior**: The bulb sends an identical encrypted status beacon to the broadcast address every ~5 seconds. This is the Tuya LAN discovery protocol — it allows the Tuya/Lepro mobile app to find the device on the local network without cloud mediation.

### All 96 UDP Packets Are Byte-Identical

The encrypted payload is static:
```
000055aa 00000000 00000013 0000009c 00000000
d09766676f3369eb10b5e9f132fd802a53b69b94
cff2256e003e6eed67555ff96447d9b63734f329
9f30caf77083cc980be9247e29bc3fbb7cb2d42f
53db8aabc2fb8459b1155fc75d4bf6699f92cba4
c0ba520148045e7605fa0498dfea5aab32908ad1
626e2d7503771cf82556470e82b84964d4378eba
df3514b9c898d1186eda8eea40e93b1e3fc14a25
70e182795cc17d0e
0000aa55
```

This means the bulb's state (on/off, color, brightness) did NOT change during the capture window. The encrypted block would differ if settings changed.

### ARP Traffic (8 packets)

| Source MAC | Source IP | Target IP | Type |
|-----------|----------|-----------|------|
| 10:78:5b:fa:3c:10 | 192.168.1.254 (router) | 192.168.1.82 | ARP Request (x7) |
| 66:e2:1f:5e:27:f3 | 192.168.1.78 | 192.168.1.82 | ARP Request (x1) |

The router (192.168.1.254, TELUS gateway) is periodically ARP-probing the bulb to keep its ARP cache fresh. One probe came from 192.168.1.78 (randomized MAC `66:e2:1f:5e:27:f3` — likely a phone or laptop with MAC randomization).

---

## Security Assessment

### Attack Surface

1. **Tuya Protocol v3.3 Vulnerability**: The bulb broadcasts its encrypted state every 5 seconds to the entire LAN. Anyone on the network can:
   - Detect the device exists (passive reconnaissance)
   - Determine it's a Tuya device (magic bytes are unencrypted)
   - Determine the protocol version (port 6667 = v3.3)
   - Monitor state changes by comparing encrypted payloads over time (differential analysis)

2. **No Cloud Traffic Observed**: During the 5-minute window, the bulb sent **zero** packets to external IPs. This means either:
   - The bulb only phones home to Tuya cloud when state changes occur
   - The bulb's cloud heartbeat interval is longer than 5 minutes
   - Cloud communication uses a different channel not visible in broadcast capture

3. **Broadcast Storm Potential**: 96 broadcast packets in 5 minutes = ~1,152 broadcasts/hour = 27,648/day. On a busy IoT network with multiple Tuya devices, this creates measurable broadcast overhead.

4. **Decryption Path**: With the device's local key (obtainable via Tuya Cloud API or by linking the device in the tinytuya Python library), the entire encrypted payload can be decrypted to reveal:
   - Device ID
   - Device capabilities (dps - data points)
   - Current state (on/off, brightness, color, mode)
   - Firmware version

5. **Replay Potential**: Since all packets are identical, replay attacks could potentially confuse discovery clients, though the encrypted payload makes forging new commands non-trivial without the local key.

### Network Exposure

| Risk | Severity | Notes |
|------|----------|-------|
| Device fingerprinting via broadcast | Medium | Tuya magic bytes are plaintext identifiers |
| State inference via traffic analysis | Low | Encrypted payloads change with state; timing analysis reveals usage patterns |
| Local key extraction | Medium | Achievable via Tuya Cloud API with account credentials |
| Full device control (with local key) | High | tinytuya can control the device directly over LAN |
| Cloud dependency | Low | Tuya cloud appears non-essential for local broadcast function |

---

## Recommendations

1. **Network Segmentation**: Move IoT devices to a dedicated VLAN/SSID to limit broadcast domain exposure
2. **Monitor for tinytuya-style probes**: Watch for UDP traffic on ports 6666/6667/7000 from unexpected sources
3. **Firmware Audit**: Check if the Lepro bulb firmware supports Tuya v3.5 (which uses solicited discovery rather than continuous broadcast)
4. **Local Key Security**: If using local control (Home Assistant, tinytuya), protect the local key — it provides full device control

---

---

## Phase 2: Key Extraction and Device Compromise

### Attack Chain

```
1. RECON         WiFi Pineapple captures broadcast traffic
                 → Identifies Tuya v3.3 device, MAC 70:89:76:25:f3:ab
                 → OUI lookup reveals Tuya Smart Inc. (white-label)

2. APK REVERSE   Download Lampux APK (209 MB) → apktool + jadx decompile
                 → Extract client_id: h5gw8q4artygy784ww4v
                 → Extract app_secret: n3s33y3j8dsy5vm4kea75p55gn3ycsdy
                 → Extract cert hash: 37:95:F5:F7:...
                 → Discover: use_ssl_pinning = false
                 → Discover: app_scheme = lampuxledbrighter

3. OEM API       Attempted direct OEM API authentication
   (BLOCKED)     → V2 BMP signing scheme prevents key construction
                 → SING_VALIDATE_FALED across all regions

4. IoT PLATFORM  Created Tuya IoT developer account
                 → Discovered Lepro blocks third-party IoT linking
                 → China data center: "no access" (account found, OEM blocked)
                 → Other data centers: QR code expired (account not present)

5. FACTORY RESET Factory reset bulb (3x power toggle)
                 → Re-paired to Tuya Smart app (bypasses OEM lockout)
                 → Linked Tuya Smart account to IoT Platform
                 → Western America Data Center, region: US

6. KEY EXTRACT   tinytuya Cloud API → device list → local_key
                 → Confirmed MAC match: 70:89:76:25:f3:ab ✓

7. DEVICE CONTROL tinytuya BulbDevice → direct LAN commands
                 → Power on/off, brightness, RGB color — all confirmed
```

### Extracted Credentials

| Field | Value |
|-------|-------|
| Device ID | `ebbc76a9e9f9b0c0a60nof` |
| Local Key | `l}WG~Zdv8f}k;O*#` |
| MAC | `70:89:76:25:f3:ab` |
| UUID | `5248ded5b3342844` |
| Product ID | `wqecgy8f0dcaibyl` |
| Category | `dj` (light) |
| Protocol | Tuya v3.3 |

### Device Capabilities (Data Points)

| DPS | Name | Type | Current Value |
|-----|------|------|---------------|
| 20 | Power | Boolean | `true` (on) |
| 21 | Mode | Enum | `white` (white/colour/scene/music) |
| 22 | Brightness | Integer (10-1000) | `1000` (100%) |
| 24 | Colour | HSV Hex | `000003e803e8` |
| 25 | Scene Data | String | `000e0d0000000000000000c803e8` |
| 26 | Countdown | Integer (seconds) | `0` (disabled) |

### Control Demonstration

Successfully executed via LAN (no cloud):
- Power toggle (on/off)
- Brightness adjustment (50%)
- RGB color control (red, green, blue)
- White mode restoration

All commands sent from Kali container → Docker network → home network → bulb at 192.168.1.82:6668.

### Approaches Attempted and Outcomes

| Approach | Result |
|----------|--------|
| OEM API with APK credentials | FAILED — V2 BMP signing not cracked |
| Lampux APK on Nexus 6P | FAILED — split APK missing native libs |
| MITM via Pineapple | BLOCKED — managed mode can't see unicast |
| Tuya IoT Platform + Lampux account | BLOCKED — Lepro OEM blocks third-party linking |
| Tuya IoT Platform + Tuya Smart account (after factory reset) | **SUCCESS** |

### Lepro OEM Security Analysis

Lepro implements the following defensive measures:
1. **OEM walled garden**: Devices paired in Lampux cannot be seen by Smart Life or Tuya Smart
2. **Third-party IoT platform blocking**: Lampux accounts reject IoT platform QR code authorization
3. **China data center registration**: OEM accounts are registered on CN infrastructure regardless of user geography
4. **V2 signing scheme**: Updated BMP-based key derivation that resists V1 extraction tools

All of these defenses are **bypassed by factory reset**, which returns the device to generic Tuya firmware pairing mode.

---

## Recommendations

1. **Network Segmentation**: Move IoT devices to a dedicated VLAN/SSID to limit broadcast domain exposure
2. **Monitor for tinytuya-style probes**: Watch for UDP traffic on ports 6666/6667/7000 from unexpected sources
3. **Firmware Audit**: Check if the Lepro bulb firmware supports Tuya v3.5 (which uses solicited discovery rather than continuous broadcast)
4. **Local Key Security**: If using local control (Home Assistant, tinytuya), protect the local key — it provides full device control
5. **Physical Security**: Factory reset via power cycling cannot be prevented in software — physical access to the power source equals device reset capability

---

## Artifacts

| File | Description |
|------|-------------|
| `lepro_capture.pcap` | Full 5-minute packet capture (22.7 KB, 104 packets) |
| `capture.sh` | Pineapple capture deployment script |
| `deploy_capture.sh` | Container-to-Pineapple orchestration script |
| `crack_key.py` | Multi-method key extraction script |
| `pwn_bulb.py` | Full compromise script (decrypt, enumerate, control) |
| `probe_lampux_api.py` | OEM API reconnaissance script |
| `lampux.apk` | Lampux Android APK (decompiled for analysis) |
| `REPORT.md` | This report |
