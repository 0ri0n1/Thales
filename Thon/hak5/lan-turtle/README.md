# LAN Turtle

## Device Summary

| Field | Value |
|-------|-------|
| Product | LAN Turtle |
| Manufacturer | Hak5 |
| Category | Covert Network Implant |
| Form Factor | USB Ethernet adapter |
| SoC | Atheros AR9331 (400 MHz MIPS 24Kc) |
| RAM | 64 MB DDR2 |
| Flash | 16 MB |
| Firmware | 6.2 (OpenWrt 19.07-SNAPSHOT, Linux 4.14.134) |
| Interface | USB-A (host-facing, power + data) + RJ45 (target-facing) |
| Default IP | 172.16.84.1/24 (eth0, host-facing) |
| Default Creds | root / sh3llz |
| SSH | Port 22, OpenSSH (not Dropbear) |
| Cloud C2 | Supported (cc-client installed) |
| MACs | 00:13:37:A6:FC:EF (eth0) / 00:13:37:A6:FC:ED (eth1) |

## Capabilities

- **Covert Placement**: Inline between target host and network, disguised as USB Ethernet adapter
- **Man-in-the-Middle**: Full network traffic interception on the target host
- **Reverse SSH**: Persistent reverse tunnel to C2 for remote access
- **Responder**: LLMNR/NBT-NS poisoning for credential capture
- **DNS Spoofing**: Redirect DNS queries for phishing/interception
- **Packet Capture**: Full pcap of target host traffic
- **AutoSSH**: Persistent SSH tunnels surviving network interruptions
- **Modules**: Extensible module system

## Operational Notes

- Device sits inline — transparent to the target host
- USB side provides power and connects to host's USB port
- Ethernet side connects to existing network drop
- Target host sees a USB Ethernet adapter, not an implant
- Change default credentials immediately on deployment
- Cloud C2 enrollment provides remote management without direct network access

## Current State

- **Firmware**: 6.2 — factory reset + recovery on 2026-03-08
- **Status**: FIELD READY — home network test passed 2026-03-08
- **SSH access**: Key auth only (`ssh turtle` from WSL, reverse tunnel via Pineapple port 2222)
- **VPN**: OpenVPN client → Pineapple server (10.8.0.2 ↔ 10.8.0.1)
- **Autossh**: Reverse tunnel `-R 2222:localhost:22` to Pineapple over VPN
- **Capture**: tcpdump on eth1, rotating 5MB x 4, auto-exfil every 15 min to Pineapple
- **Hardening**: MAC spoofed, key-only SSH, hostname "USB-ETH0", logs /tmp only
- **Cloud C2**: Client installed, not enrolled
- **Reboot recovery**: TESTED — all services auto-restart on both Turtle and Pineapple reboot

See `documentation/device-state.md` for full system state.
See `config/ssh-access.md` for SSH credentials and key locations.

## Skills Reference

- `/hak5-implants` — Deployment procedures, module reference, Cloud C2 integration

## Directory Structure

```
lan-turtle/
  config/         SSH access docs, firmware binaries, network settings
  payloads/       Module payloads, responder configs, DNS spoof rules
  documentation/  Device state, deployment guides, network topology
  engagements/    Per-engagement folders (copy from _templates/engagement/)
```
