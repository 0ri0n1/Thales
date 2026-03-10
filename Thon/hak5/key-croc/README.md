# Key Croc

## Device Summary

| Field | Value |
|-------|-------|
| Product | Key Croc |
| Manufacturer | Hak5 |
| Category | Keylogger / HID Implant |
| Form Factor | Inline USB keyboard implant |
| Interfaces | USB (host-side), USB (keyboard-side), WiFi |
| Language | Ducky Script |
| Cloud C2 | Supported |

## Capabilities

- **Keylogging**: Captures all keystrokes from attached keyboard
- **Keystroke Injection**: Injects keystrokes via Ducky Script when triggered
- **Pattern Matching**: Trigger payloads based on typed keyword patterns
- **WiFi Exfiltration**: Send captured keystrokes over WiFi
- **Cloud C2**: Remote management and loot retrieval
- **Save Mode**: Store captures locally for physical retrieval

## Operational Notes

- Device sits inline between target keyboard and workstation
- Transparent to the user — keyboard functions normally
- Pattern matching enables context-aware payload triggers
- WiFi range and connectivity required for real-time exfiltration
- Skills not yet developed — populate documentation/ as device is integrated

## Directory Structure

```
key-croc/
  config/         WiFi profiles, trigger patterns, C2 enrollment
  payloads/       Ducky Script payloads, trigger-based injection scripts
  documentation/  Setup guides, pattern matching reference
  engagements/    Per-engagement folders (copy from _templates/engagement/)
```
