# Plunder Bug

## Device Summary

| Field | Value |
|-------|-------|
| Product | Plunder Bug |
| Manufacturer | Hak5 |
| Category | Inline Ethernet Tap |
| Form Factor | Small inline Ethernet adapter |
| Interfaces | 2x Ethernet (passthrough), USB (data to host) |
| Power | USB bus-powered |
| Capture | Via host OS (Wireshark, tcpdump) |

## Capabilities

- **Passive Ethernet Tap**: Mirror all traffic on an Ethernet link to USB host
- **Full Duplex Capture**: Capture both directions of traffic simultaneously
- **Transparent**: No IP address, no MAC — completely invisible on the network
- **Host Integration**: Appears as USB network adapter on host for standard capture tools
- **Protocol Agnostic**: Captures all Ethernet-layer traffic regardless of protocol

## Operational Notes

- Passive device — does not inject, modify, or block traffic
- Connect inline between target device and network switch
- Use Wireshark, tcpdump, or tshark on connected host to capture
- No configuration needed — plug and capture
- Ideal for evidence collection during physical penetration tests
- Skills not yet developed — populate documentation/ as device is integrated

## Directory Structure

```
plunder-bug/
  config/         Capture filter presets, Wireshark profiles
  payloads/       Capture scripts, automated analysis pipelines
  documentation/  Physical deployment guides, capture methodology
  engagements/    Per-engagement folders (copy from _templates/engagement/)
```
