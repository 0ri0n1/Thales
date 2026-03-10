# Screen Crab

## Device Summary

| Field | Value |
|-------|-------|
| Product | Screen Crab |
| Manufacturer | Hak5 |
| Category | HDMI Inline Screen Capture |
| Form Factor | HDMI passthrough dongle |
| Interfaces | HDMI in, HDMI out, USB (power), WiFi |
| Capture Modes | Screenshot, Video, Triggered |
| Exfiltration | WiFi to Cloud C2, local storage |
| Cloud C2 | Required for remote operation |

## Capabilities

- **HDMI Interception**: Inline capture of video signal between source and display
- **Screenshot Mode**: Periodic screen captures at configurable intervals
- **Video Mode**: Continuous or triggered video recording
- **Triggered Capture**: Capture on screen content change detection
- **WiFi Exfiltration**: Captured images/video sent to Cloud C2 over WiFi
- **Covert**: Transparent HDMI passthrough — no visible change to user

## Operational Notes

- Device sits inline between HDMI source (workstation, server KVM) and display
- Requires USB power — use a USB port on the target or an external power source
- WiFi must reach a network with internet for Cloud C2 exfil
- Cloud C2 enrollment is the primary management method
- Captures are viewable as loot in Cloud C2 dashboard
- No direct SSH — management is Cloud C2 only

## Skills Reference

- `/hak5-implants` — Cloud C2 loot retrieval, deployment guidance

## Directory Structure

```
screen-crab/
  config/         WiFi profiles, capture mode settings, C2 enrollment
  payloads/       Trigger configs, capture interval settings
  documentation/  Physical deployment notes, HDMI compatibility
  engagements/    Per-engagement folders (copy from _templates/engagement/)
```
