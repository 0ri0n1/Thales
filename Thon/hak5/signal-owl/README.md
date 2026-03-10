# Signal Owl

## Device Summary

| Field | Value |
|-------|-------|
| Product | Signal Owl |
| Manufacturer | Hak5 |
| Category | Covert Signals Intelligence Platform |
| Form Factor | USB dongle |
| Interfaces | USB (power + host), WiFi |
| OS | Linux-based |
| Cloud C2 | Supported |

## Capabilities

- **WiFi Monitoring**: Passive wireless reconnaissance
- **Signal Analysis**: Wireless environment assessment
- **Payload Execution**: Automated bash payloads on boot
- **Cloud C2**: Remote management and data exfiltration
- **Covert**: Small form factor, powered by USB port

## Operational Notes

- Plug into any USB port for power — executes payload on boot
- WiFi adapter used for monitoring, not injection
- Ideal for persistent wireless monitoring in physical engagements
- Skills not yet developed — populate documentation/ as device is integrated

## Directory Structure

```
signal-owl/
  config/         WiFi settings, Cloud C2 enrollment, boot scripts
  payloads/       Automated monitoring and recon payloads
  documentation/  Wireless monitoring guides, deployment notes
  engagements/    Per-engagement folders (copy from _templates/engagement/)
```
