# Scope Definition — ENG-TURTLE-2026-0308

## In Scope


| Element        | Value                                                         |
| -------------- | ------------------------------------------------------------- |
| Network        | 192.168.1.0/24 (Eddie's home network)                         |
| Target devices | Home router/switch (192.168.1.1)                              |
| Implant device | LAN Turtle (Hak5), firmware 6.2                               |
| C2 device      | WiFi Pineapple Mark 7 (192.168.1.76 via wlan2)                |
| Techniques     | Passive traffic capture (tcpdump), VPN tunneling, reverse SSH |
| Depth          | Passive interception only — no exploitation                   |
| Time window    | 2026-03-08, unrestricted (self-owned lab)                     |


## Out of Scope


| Element                        | Reason                             |
| ------------------------------ | ---------------------------------- |
| External targets               | Not authorized                     |
| Neighbor networks              | Not owned                          |
| ARP spoofing / MITM            | Not authorized for this validation |
| Active exploitation            | Validation exercise only           |
| DNS spoofing                   | Not authorized for this validation |
| Credential capture (Responder) | Not authorized for this validation |


## Authorization

- **Type**: Self-owned infrastructure
- **Authorized by**: Eddie (principal, infrastructure owner)
- **Legal jurisdiction**: US domestic, self-owned property
- **Evidence**: Verbal directive in operational session

