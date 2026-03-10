# USB Rubber Ducky

## Device Summary

| Field | Value |
|-------|-------|
| Product | USB Rubber Ducky |
| Manufacturer | Hak5 |
| Category | Keystroke Injection Tool |
| Form Factor | USB flash drive appearance |
| Injection Speed | ~1000 characters/second |
| Storage | MicroSD for payload storage |
| Language | Ducky Script |

## Capabilities

- **Keystroke Injection**: High-speed HID keyboard emulation
- **Ducky Script**: Purpose-built scripting language for keystroke payloads
- **Cross-Platform**: Payloads for Windows, macOS, Linux
- **Covert**: Appears as standard USB flash drive
- **Encoder**: Compile Ducky Script to inject.bin for deployment

## Ducky Script Quick Reference

| Command | Description |
|---------|-------------|
| `REM` | Comment |
| `DELAY` | Pause in milliseconds |
| `STRING` | Type a string |
| `ENTER` | Press Enter |
| `GUI` | Windows/Command key |
| `ALT` | Alt key |
| `CTRL` | Control key |
| `SHIFT` | Shift key |
| `TAB` | Tab key |

## Operational Notes

- Compile payloads with Ducky Encoder before deployment
- Test against target OS version — keyboard shortcuts vary
- Consider locale/keyboard layout differences
- Payload executes immediately on insertion — no abort mechanism
- MicroSD card holds inject.bin — swap cards to swap payloads

## Skills Reference

- `/hak5-usb-wifi` — Ducky Script reference, payload templates

## Directory Structure

```
usb-rubber-ducky/
  config/         Encoder settings, keyboard layout configs
  payloads/       Ducky Script source (.txt) and compiled (.bin) payloads
  documentation/  Target OS keystroke maps, encoding notes
  engagements/    Per-engagement folders (copy from _templates/engagement/)
```
