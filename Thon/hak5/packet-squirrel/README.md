# Packet Squirrel

## Device Summary

| Field | Value |
|-------|-------|
| Product | Packet Squirrel |
| Manufacturer | Hak5 |
| Category | Inline Network Implant |
| Form Factor | Small inline Ethernet device |
| Interfaces | 2x Ethernet (inline), USB (storage/power) |
| Default IP | 172.16.32.1 |
| Default Password | hak5squirrel |
| Switch Positions | 3-position selector |
| Cloud C2 | Supported |

## Capabilities

- **Inline Packet Capture**: Full pcap between two Ethernet segments
- **DNS Spoofing**: Redirect DNS for targeted interception
- **VPN Tunneling**: OpenVPN client for remote exfiltration
- **Transparent Bridge**: Pass-through mode for covert operation
- **USB Storage**: Capture to USB drive for later retrieval
- **3-Position Switch**: Quick payload selection in the field

## Switch Positions

| Position | Default Function |
|----------|-----------------|
| 1 | Payload 1 (customizable) |
| 2 | Payload 2 (customizable) |
| 3 | Arming mode (SSH access) |

## Operational Notes

- Device is fully inline — placed between target device and network switch
- Transparent bridging means target device sees no change
- Capture files save to USB storage
- LED indicates operating mode and capture status
- OpenVPN payload enables remote pcap exfiltration through VPN tunnel

## Skills Reference

- `/hak5-implants` — Deployment procedures, payload development

## Directory Structure

```
packet-squirrel/
  config/         VPN configs, network settings, switch assignments
  payloads/       Position 1/2 payload scripts, DNS spoof rules
  documentation/  Deployment notes, capture procedures
  engagements/    Per-engagement folders (copy from _templates/engagement/)
```
