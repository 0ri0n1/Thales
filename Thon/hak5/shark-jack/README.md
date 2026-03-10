# Shark Jack

## Device Summary

| Field | Value |
|-------|-------|
| Product | Shark Jack |
| Manufacturer | Hak5 |
| Category | Portable Network Attack Tool |
| Form Factor | Pocket-sized Ethernet device |
| Interfaces | Ethernet (RJ45), USB-C (charging) |
| Battery | Internal LiPo |
| OS | Linux-based |
| Modes | Arming, Attack |

## Capabilities

- **Network Recon**: Automated nmap scans on plug-in
- **Payload Execution**: Run bash scripts on Ethernet connection
- **Portable**: Battery-powered, no host required
- **Cloud C2**: Remote payload management and loot retrieval
- **Switch Toggle**: Arming mode for payload management, attack mode for execution

## Operational Notes

- Plug into any open Ethernet port for automated recon/attack
- Battery life limits operational window — plan payloads accordingly
- Charge via USB-C before deployments
- Payloads execute on mode switch — no user interaction needed at target
- Skills not yet developed — populate documentation/ as device is integrated

## Directory Structure

```
shark-jack/
  config/         Network settings, Cloud C2 enrollment
  payloads/       Bash payload scripts for attack mode
  documentation/  Battery management, payload development guides
  engagements/    Per-engagement folders (copy from _templates/engagement/)
```
