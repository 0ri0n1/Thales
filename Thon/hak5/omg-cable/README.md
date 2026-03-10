# O.MG Cable

## Device Summary

| Field | Value |
|-------|-------|
| Product | O.MG Cable |
| Manufacturer | Hak5 (O.MG / Mischief Gadgets) |
| Category | Covert USB HID Implant |
| Form Factor | Standard-appearance USB cable |
| Interfaces | USB (appears as normal charging cable), WiFi AP |
| Capabilities | HID injection, WiFi C2, keylogging (Elite) |
| Variants | Standard, Elite (bidirectional + keylogging) |

## Capabilities

- **Covert HID Injection**: Keystroke injection from what appears to be a normal cable
- **WiFi Command & Control**: Built-in WiFi AP for remote payload triggering
- **Web Interface**: Browser-based payload management via WiFi AP
- **Keylogging (Elite)**: Inline keyboard capture on Elite variant
- **Geofencing**: Trigger payloads based on WiFi environment
- **Self-Destruct**: Payload to disable implant functionality

## Operational Notes

- Visually indistinguishable from a standard USB cable
- WiFi AP enables remote triggering without physical access
- Payload capacity limited — plan scripts accordingly
- Available in USB-A, USB-C, Lightning variants
- Skills not yet developed — populate documentation/ as device is integrated

## Directory Structure

```
omg-cable/
  config/         WiFi AP settings, geofence configs
  payloads/       HID injection scripts, trigger payloads
  documentation/  Cable variant reference, WiFi management guide
  engagements/    Per-engagement folders (copy from _templates/engagement/)
```
