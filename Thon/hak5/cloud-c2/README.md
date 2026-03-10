# Hak5 Cloud C2

## Platform Summary

| Field | Value |
|-------|-------|
| Product | Cloud C2 |
| Manufacturer | Hak5 |
| Category | Command & Control Platform |
| Type | Software (Docker container) |
| Container | joshuapfritz/hak5c2:3.5.0 |
| Container Name | hak5-cloudc2 |
| URL | http://172.16.42.140:8080 |
| API | REST (Bearer token auth) |
| MCP Integration | kali-mcp server tools (kali_c2_*) |

## Capabilities

- **Device Management**: Enroll, monitor, reboot, and update Hak5 devices remotely
- **Loot Retrieval**: Centralized loot collection from all enrolled devices
- **Site Organization**: Group devices by physical site/engagement
- **Notifications**: Real-time alerts for device events and loot captures
- **API Access**: Full REST API for automation and integration
- **Audit Logging**: Complete API and device action audit trail

## Supported Devices

All Hak5 devices with Cloud C2 support:
- WiFi Pineapple Mark 7
- LAN Turtle
- Packet Squirrel
- Screen Crab
- Key Croc
- Shark Jack
- Signal Owl
- O.MG Cable

## MCP Tools Reference

| Tool | Function |
|------|----------|
| `kali_c2_login` | Authenticate, obtain Bearer token |
| `kali_c2_status` | Server version, uptime, hostname |
| `kali_c2_sites` | List configured sites |
| `kali_c2_devices` | List enrolled devices with online status |
| `kali_c2_device_status` | Detailed device info (IP, firmware, uptime) |
| `kali_c2_loot` | Retrieve captured loot from a device |
| `kali_c2_loot_export` | Export all loot for download |
| `kali_c2_notifications` | Device events and alerts |
| `kali_c2_reboot_device` | Remote device reboot |
| `kali_c2_logs` | Server and API audit logs |

## Pineapple-Specific C2 Tools

| Tool | Function |
|------|----------|
| `kali_pineapple_pineap` | Get PineAP engine config |
| `kali_pineapple_pineap_set` | Configure PineAP engine |
| `kali_pineapple_ssid_pool` | Manage SSID impersonation pool |
| `kali_pineapple_clients` | List connected clients |
| `kali_pineapple_probes` | View captured probe requests |
| `kali_pineapple_recon` | Start/stop/get wireless recon scans |
| `kali_pineapple_filters` | Manage MAC/SSID filters |
| `kali_pineapple_deauth` | Send deauth to specific client |

## Operational Notes

- Container runs on Docker host at 172.16.42.140
- Authentication required for all API operations — token expires, re-auth as needed
- Device enrollment requires physical access to each device for initial setup
- Loot is stored server-side until exported or cleaned
- Backup container data volume for engagement continuity

## Skills Reference

- `/hak5-implants` — Cloud C2 API reference, device management procedures

## Directory Structure

```
cloud-c2/
  config/         Docker compose files, environment configs, TLS certs
  documentation/  API reference, enrollment procedures, backup guides
```
