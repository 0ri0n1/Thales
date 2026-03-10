# WiFi Pineapple Mark 7

## Device Summary

| Field | Value |
|-------|-------|
| Product | WiFi Pineapple Mark 7 |
| Manufacturer | Hak5 |
| Category | Wireless Auditing Platform |
| Chipset | MediaTek MT7628 (2.4 GHz) + MT7612E (5 GHz) |
| OS | OpenWrt-based (PineAP firmware) |
| Current Firmware | 2.1.3 |
| Management IP | 172.16.42.1 |
| SSH Access | root@172.16.42.1 (port 22) |
| Web UI | http://172.16.42.1:1471 |
| Cloud C2 | Enrolled |

## Capabilities

- **PineAP Engine**: Beacon response, probe capture, SSID impersonation, targeted/broadcast deauth
- **Recon**: Passive and active wireless site survey (2.4 GHz and 5 GHz bands)
- **Evil Twin**: Rogue AP with captive portal, credential harvesting
- **MITM**: Client interception via open/WPA rogue networks
- **Filtering**: MAC and SSID allow/deny lists for targeted operations
- **Modules**: Extensible module system for additional capabilities
- **Cloud C2**: Remote management, loot retrieval, campaign coordination

## Network Configuration

- **Management interface**: USB-C tethering to host at 172.16.42.0/24
- **Upstream WAN**: Ethernet or WiFi client mode for internet sharing
- **Open AP**: Configurable SSID for client capture
- **Management AP**: Separate SSID for operator access

## Operational Notes

- Always verify deny lists are current before rogue AP operations
- Home network MACs and SSIDs are maintained in deny lists (12 MACs, 2 SSIDs as of 2026-03-08)
- Firmware updates require USB-C tethered connection
- PineAP daemon must be running for beacon/probe/deauth features
- Recon automation available via `scripts/pineapple_recon.sh`

## Skills Reference

- `/hak5-usb-wifi` — MCP tool reference, operational procedures
- `/ariia` — Autonomous recon integration

## Directory Structure

```
wifi-pineapple-mk7/
  config/         Device configuration backups, deny lists, PineAP settings
  payloads/       Evil twin configs, captive portal templates, module configs
  documentation/  Device-specific notes, network diagrams, firmware history
  engagements/    Per-engagement folders (copy from _templates/engagement/)
```
