# LAN Turtle Payload Arsenal — Tradecraft Report

**Date**: 2026-03-08
**Operator**: Thon (Venom)
**Principal**: Eddie
**Device**: LAN Turtle (Hak5), firmware 6.2, OpenWrt 19.07

---

## 1. Mission

Develop a field-ready payload arsenal for the LAN Turtle covert network implant. Payloads must operate within the device's hardware constraints, follow OPSEC tradecraft, and leverage the established VPN/C2 infrastructure (Turtle → Pineapple → Operator).

## 2. Design Constraints

The Turtle's operational environment imposes hard limits that drove every design decision:

| Constraint | Value | Design Impact |
|-----------|-------|---------------|
| Shell | BusyBox ash (POSIX sh) | No bash-isms — no arrays, no `[[`, no process substitution |
| Overlay | 1.3 MB free | Scripts must be small (<5 KB each); total arsenal <25 KB |
| tmpfs | 29 MB | All runtime output — captures, logs, state — lives here |
| RAM | 64 MB | No heavy processes; tcpdump, ncat, nmap are ceiling |
| Available tools | nmap, tcpdump, ncat, netcat, python2.7, iptables | No responder, no bettercap, no modern tooling |
| Architecture | MIPS 24Kc @ 400 MHz | Single-core, no parallelism budget |
| Network position | Inline (eth0=host, eth1=network, tun0=VPN) | Unique interception point between host and LAN |

## 3. Tradecraft Principles Applied

### 3.1 Compartmentalization
Each payload is a standalone script with no dependencies on other payloads. Any payload can be deployed independently, activated or deactivated without affecting others. This prevents single-point failures from cascading across the arsenal.

### 3.2 OPSEC Discipline
Every payload enforces consistent operational security:

- **C2 exclusion**: BPF filters and configuration explicitly exclude VPN overlay (10.8.0.0/24), management subnet (172.16.84.0/24), and VPN transport (UDP 1194). No payload will ever capture or interfere with its own C2 channel.
- **Volatile storage only**: All output writes to `/tmp` (tmpfs). Nothing persists to flash overlay. On power loss or reboot, no forensic artifacts remain on device.
- **Clean shutdown**: Every payload implements `stop` with state restoration. DNS redirect removes iptables rules. Proxy kills listeners. Capture stops tcpdump. No orphaned processes, no dangling rules.
- **PID tracking**: All persistent payloads write PID files for clean lifecycle management.

### 3.3 Noise Awareness
Payloads are categorized by detection risk:

| Level | Payloads | Rationale |
|-------|----------|-----------|
| **Silent** | arp-watch, cred-harvest | Read-only (ARP cache) or passive sniff. Zero generated traffic. |
| **Low** | dns-redirect | Modifies iptables rules on the device only. Detectable if host DNS behavior changes. |
| **Medium** | recon, pivot-proxy | Active scanning generates network traffic visible to IDS/IPS. Proxy creates connections. |

Operators select payloads based on the engagement's noise tolerance and Rules of Engagement.

### 3.4 Minimal Footprint
The entire arsenal is 5 scripts totaling ~20 KB. Overlay impact is negligible against the 1.3 MB free budget. No additional packages need to be installed — every payload uses tools already present on the Turtle from the base deployment.

## 4. Payload Methodology

### 4.1 recon.sh — Network Reconnaissance

**Technique**: Active scanning from the implant's network position (MITRE T1046, T1018).

Three operational modes:
- **discover**: ARP table snapshot + nmap ping sweep. Fast, low-noise host enumeration.
- **enumerate**: nmap version scan (-sV) on top 100 ports with default scripts (-sC). Service fingerprinting.
- **full**: Discovery then enumeration pipeline. Auto-detects target subnet from eth1 DHCP address.

Output formats: grepable (.gnmap) for automated parsing, normal (.nmap) for human review. Exclusion of C2 and management nets prevents self-detection.

### 4.2 cred-harvest.sh — Credential Harvesting

**Technique**: Passive traffic capture with protocol-specific BPF filters (MITRE T1040, T1557).

Captures cleartext authentication across 13 protocols: HTTP, FTP, Telnet, SMTP, POP3, IMAP, LDAP, SNMP, Kerberos, SMB, MySQL, PostgreSQL, and HTTP-alt (8080). Uses tcpdump with rotating capture files (2 MB x 5 = 10 MB max) to stay within tmpfs budget.

The BPF filter is constructed to capture only authentication-bearing protocol traffic, dramatically reducing capture volume compared to full traffic capture (which the existing `capture.sh` already handles). This targeted approach produces smaller pcaps that are faster to exfiltrate and easier to analyze.

### 4.3 pivot-proxy.sh — Network Pivot

**Technique**: SOCKS proxy for operator tool routing through the implant (MITRE T1090).

Establishes an ncat SOCKS4 proxy bound exclusively to the VPN interface (tun0). The operator — connecting from the Pineapple or over the VPN — can route tools (nmap, curl, proxychains) through the Turtle and into the target network. The proxy is not reachable from the target network.

Alternative pivot method documented: SSH dynamic forwarding (`ssh -D 1080 -p 2222`) through the reverse tunnel achieves the same effect without ncat.

### 4.4 dns-redirect.sh — DNS Interception

**Technique**: DNS redirection via iptables NAT rules on the host-facing interface (MITRE T1557.004, T1584.002).

Two modes:
- **Blanket redirect**: All DNS queries from the connected host are DNAT'd to an attacker-controlled resolver (default: Pineapple at 10.8.0.1).
- **Targeted spoof**: Specific domain-to-IP mappings via dnsmasq with a custom hosts file. Allows surgical interception (e.g., redirect `portal.corp.com` to a phishing page) without affecting other DNS resolution.

Full rollback: `stop` command removes all iptables rules, kills dnsmasq, cleans state files. The connected host returns to normal DNS behavior immediately.

### 4.5 arp-watch.sh — Passive Network Mapping

**Technique**: ARP cache monitoring for host discovery over time (MITRE T1016, T1018).

Polls the kernel ARP table at configurable intervals (default: 30 seconds). Logs every new IP+MAC pair with a first-seen timestamp. Builds a network map organically from observed traffic — the Turtle sees ARP entries naturally as the connected host communicates on the LAN.

Completely passive: reads `/proc/net/arp` equivalent via `ip neigh`. Generates zero network traffic. Ideal for long-duration deployments where patience replaces noise.

## 5. Deployment Workflow

```
1. Copy payloads to Turtle   →  scp *.sh root@172.16.84.1:/root/
2. Set executable             →  chmod +x /root/*.sh
3. Activate per mission ROE   →  /root/arp-watch.sh start
4. Exfiltrate results         →  /root/exfil.sh (cron) or manual SCP
5. Clean up                   →  /root/<payload>.sh stop
```

Payloads integrate with the existing exfil pipeline — cron runs `exfil.sh` every 15 minutes, which SCPs `/tmp/` contents to the Pineapple loot directory.

## 6. Arsenal Summary

| # | Payload | Size | MITRE ATT&CK | Noise | Persistence |
|---|---------|------|-------------|-------|-------------|
| 1 | recon.sh | 3.0 KB | T1046, T1018 | Medium | One-shot |
| 2 | cred-harvest.sh | 3.2 KB | T1040, T1557 | Silent | Daemonized |
| 3 | pivot-proxy.sh | 3.4 KB | T1090 | Silent | Daemonized |
| 4 | dns-redirect.sh | 4.5 KB | T1557.004 | Low | Stateful |
| 5 | arp-watch.sh | 3.1 KB | T1016, T1018 | Silent | Daemonized |
| **Total** | | **~17 KB** | | | |

All payloads are field-ready. Authorization and scope must be established per engagement before activation.

---

*Report compiled by Thon. Payloads stored at `hak5/lan-turtle/payloads/`.*
