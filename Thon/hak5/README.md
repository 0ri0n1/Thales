# Hak5 Asset Library

Operational repository for Eddie's Hak5 hardware arsenal and Cloud C2 platform.

## Device Inventory

| Device | Category | Status | Skills |
|--------|----------|--------|--------|
| [WiFi Pineapple MK7](wifi-pineapple-mk7/) | Wireless Auditing | Active | `/hak5-usb-wifi` |
| [Bash Bunny](bash-bunny/) | USB Attack Platform | Ready | `/hak5-usb-wifi` |
| [USB Rubber Ducky](usb-rubber-ducky/) | Keystroke Injection | Ready | `/hak5-usb-wifi` |
| [LAN Turtle](lan-turtle/) | Network Implant | Ready | `/hak5-implants` |
| [Packet Squirrel](packet-squirrel/) | Network Implant | Ready | `/hak5-implants` |
| [Screen Crab](screen-crab/) | HDMI Capture | Ready | `/hak5-implants` |
| [Key Croc](key-croc/) | Keylogger/HID | Owned | — |
| [Shark Jack](shark-jack/) | Network Attack | Owned | — |
| [Signal Owl](signal-owl/) | Signals Intel | Owned | — |
| [O.MG Cable](omg-cable/) | Covert HID | Owned | — |
| [Plunder Bug](plunder-bug/) | Ethernet Tap | Owned | — |
| [Cloud C2](cloud-c2/) | C2 Platform | Active | `/hak5-implants` |

**Status Legend:**
- **Active** — Deployed and operational with full skills
- **Ready** — Skills developed, device available for deployment
- **Owned** — Hardware in inventory, skills pending

## Starting an Engagement

1. Copy `_templates/engagement/` into the device's `engagements/` directory
2. Rename to `YYYY-MM-DD_engagement-name/`
3. Fill out `engagement_brief.md` (Phase 1 — Initiation)
4. Work through phases, storing artifacts in the appropriate subdirectories
5. Complete Phase 6 reporting and Phase 7 closeout

## Directory Structure

```
hak5/
  _templates/
    engagement/           Shared engagement template (copy per engagement)
      engagement_brief.md 7-phase engagement lifecycle checklist
      scope/              Authorization, ROE, target lists
      recon/              Scan results, enumeration, OSINT
      captures/           Exploit output, credentials, pcaps
      evidence/           Screenshots, proof artifacts
      logs/               Tool logs, session logs, audit trail
      report/             Final deliverables

  <device>/
    README.md             Device reference (specs, capabilities, notes)
    config/               Device configuration and settings
    payloads/             Attack payloads and scripts
    documentation/        Guides, cheat sheets, reference material
    engagements/          Per-engagement directories (copied from template)

  cloud-c2/
    README.md             Platform reference (API, MCP tools, endpoints)
    config/               Docker compose, environment, TLS
    documentation/        API reference, enrollment, backup procedures
```

## Doctrine Alignment

This asset library's engagement structure maps to the doctrine engagement lifecycle defined in `agents/thon/engagement.yaml`:

| Doctrine Phase | Engagement Directory |
|----------------|---------------------|
| Phase 1: Initiation | `scope/` + `engagement_brief.md` |
| Phase 2: Reconnaissance | `recon/` |
| Phase 3: Analysis | `recon/` + `evidence/` |
| Phase 4: Exploitation | `captures/` + `evidence/` |
| Phase 5: Validation | `evidence/` + `report/` |
| Phase 6: Reporting | `report/` |
| Phase 7: Closeout | All directories finalized |

## Not Included

- **Cactus WHID** — ESP8266-based device (ESPloit/Exploit), not a Hak5 product. Managed separately with dedicated skills (`/esploit-cactus`, `/cactus-ops`, `/cactus-flash`, `/cactus-tools`).
