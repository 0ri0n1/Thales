# Tasking Order: Pineapple Area Reconnaissance

## Mission
Conduct a passive and active recon sweep of the wireless and wired environment visible from the WiFi Pineapple MK7. Recon only — no exploitation, no deauth, no association. Build a picture of what's out there.

## Constraints
- **RECON ONLY.** Do not attack, inject, deauth, or associate with any target.
- **Protect home devices.** The Pineapple's deny lists (12 MACs, 2 SSIDs) are in place. Do NOT modify them.
- **USB-first management.** SSH to `172.16.42.1` via Kali MCP container: `sshpass -p Mousepad7 ssh -o StrictHostKeyChecking=no root@172.16.42.1`
- **Storage budget.** ~1.6GB free. Keep captures lean. Kill long-running captures after reasonable sample windows.
- **No daemon conflicts.** Pineapple daemon runs on port 1471. Do not install or start anything that binds to that port.

## Execution Sequence

### Phase 1: Wireless Landscape (802.11)
1. **horst** — Run a short 802.11 scan (~60s) on the monitor interface. Capture SSIDs, BSSIDs, channels, signal strengths, client probes, encryption types. Save output.
2. **airodump-ng** — If horst alone isn't sufficient, run a brief airodump sweep (~60s) across all channels. Capture the CSV/netxml output for parsing. Do NOT run with `--wps` flag yet.
3. **Summarize** the wireless landscape: how many APs, what channels are crowded, encryption breakdown (open/WEP/WPA2/WPA3), hidden networks, and any notable client probe requests.

### Phase 2: WPS Assessment
4. **reaver** — Use `wash` (bundled with reaver) to passively scan for WPS-enabled APs. List which APs have WPS enabled and whether they're locked. Do NOT attempt any PIN attacks.

### Phase 3: Local Network Discovery (Wired Side via wlan2)
5. **arp-scan** — Sweep the home network (`192.168.1.0/24`) via wlan2. Identify all live hosts with MAC vendor lookups.
6. **fping** — Parallel ICMP sweep of `192.168.1.0/24` to cross-reference with arp-scan results and identify hosts that block ARP but respond to ICMP (or vice versa).
7. **lldpcli** — Check if any LLDP/CDP neighbors are advertising on the network. Quick check, may return nothing on a home network.
8. **snmpwalk** — Probe `192.168.1.1` (router) with community string `public` for device info. If it responds, pull system description and interface list. If no response, note SNMP is disabled and move on.

### Phase 4: Consolidation
9. **Compile results** into a structured summary:
   - Wireless environment: AP count, channel utilization, encryption posture, WPS exposure
   - Wired network: host inventory with IPs, MACs, vendor IDs
   - Network services: any LLDP/CDP/SNMP findings
   - Notable observations: anything unexpected, misconfigured, or worth investigating further
10. **Clean up** — Kill any background processes started during recon. Remove large temp files. Verify Pineapple daemon is still healthy on 1471.

## Output Format
Present the consolidated recon picture as a structured briefing. Flag anything that stands out as an attack surface worth noting for future engagement planning. Do not recommend or execute any attacks — this is intelligence gathering only.

## Tools Available on Pineapple
horst, airodump-ng (aircrack-ng suite), wash/reaver, arp-scan, fping, snmpwalk, lldpcli, kismet, netsniff-ng, nmap, tcpdump, hcxdumptool, mdk4, macchanger

## Notes
- For heavy analysis of captures, pull files back to Kali MCP or WSL Kali on the PC.
- kismet is installed but its web UI (port 2501) setup is a separate task — skip it for this sweep unless the lighter tools prove insufficient.
- If any tool fails to run post-install, note it and continue with alternatives.
