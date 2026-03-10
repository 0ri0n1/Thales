# Bash Bunny

## Device Summary

| Field | Value |
|-------|-------|
| Product | Bash Bunny |
| Manufacturer | Hak5 |
| Category | USB Attack Platform |
| Hardware | Quad-core ARM, 512MB RAM, 8GB storage |
| Modes | Arming, Switch Position 1, Switch Position 2 |
| USB Modes | HID, Storage, Ethernet, Serial (composites supported) |
| LED Status | Multi-color status indicators |

## Capabilities

- **HID Attacks**: Keystroke injection at USB HID speed
- **Network Attacks**: USB Ethernet adapter emulation for MITM/exfil
- **Storage Attacks**: USB mass storage emulation for payload delivery
- **Composite Attacks**: Simultaneous HID + Ethernet + Storage
- **Ducky Script**: Full Ducky Script language support for keystroke payloads
- **BashBunny Script**: Extended scripting with ATTACKMODE, LED, QUACK commands
- **Exfiltration**: Loot folder structure for captured data

## ATTACKMODE Reference

| Mode | Description |
|------|-------------|
| `ATTACKMODE HID` | Keyboard emulation |
| `ATTACKMODE STORAGE` | USB mass storage |
| `ATTACKMODE RNDIS_ETHERNET` | Windows Ethernet adapter |
| `ATTACKMODE ECM_ETHERNET` | Mac/Linux Ethernet adapter |
| `ATTACKMODE HID STORAGE` | Keyboard + mass storage |
| `ATTACKMODE HID RNDIS_ETHERNET` | Keyboard + Windows Ethernet |
| `ATTACKMODE SERIAL` | Serial console access |

## Switch Positions

- **Position 3 (closest to USB)**: Arming mode — access storage, edit payloads
- **Position 1 (middle)**: Execute `payloads/switch1/payload.txt`
- **Position 2 (far)**: Execute `payloads/switch2/payload.txt`

## Operational Notes

- Always test payloads in arming mode before deploying
- LED color patterns indicate payload stage — document per-payload
- Loot saves to `/root/udisk/loot/` on device
- Use ArgFuscator (`/argfuscator`) for AV/EDR evasion on injected commands
- LOLBAS binaries preferred for fileless execution

## Skills Reference

- `/hak5-usb-wifi` — Payload templates, Ducky Script reference
- `/argfuscator` — Command obfuscation for injection payloads
- `/lolbas-gtfobins` — Living-off-the-land binary reference

## Directory Structure

```
bash-bunny/
  config/         Device settings, switch position assignments
  payloads/       Payload scripts (switch1/, switch2/ structure)
  documentation/  Ducky Script cheat sheets, target OS notes
  engagements/    Per-engagement folders (copy from _templates/engagement/)
```
