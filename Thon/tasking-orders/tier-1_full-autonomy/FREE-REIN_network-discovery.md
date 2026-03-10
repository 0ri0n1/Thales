# TASKING ORDERS — FREE REIN: Network Discovery & Service Enumeration

Eddie: Command wants a headcount of every host, every port, and every service with a pulse. If it's on the wire and listening, I want to know its name, rank, and serial number.

---

## DIRECTIVE

Find every host. Map every service. Fingerprint everything that listens. Build the network picture from the ground up.

---

## OBJECTIVE

**Primary:** Discover all live hosts on the target network. Enumerate all open ports, identify all running services with version information, detect operating systems, and map network topology including segmentation boundaries.
**Secondary:** Identify trust relationships, shared services, centralized authentication, and infrastructure dependencies. Flag default credentials, exposed management interfaces, and unnecessary services.
**Success Criteria:** Complete network map with host inventory, service catalogue, OS fingerprints, and topology diagram. Every listening port accounted for.

---

## SCOPE

**In-Scope Targets:**
- [TARGET NETWORK RANGE(S) — fill before issue]

**Out-of-Scope / No-Strike:**
- [EXCLUDED HOSTS / RANGES — fill before issue]

**Technique Permissions:**
- Permitted: Host discovery (ARP, ICMP, TCP SYN), port scanning (SYN, connect, UDP), service fingerprinting, OS detection, banner grabbing, SMB enumeration, SNMP walks, DNS zone transfer attempts, traceroute, network topology mapping
- Restricted: No exploitation. No credential brute-forcing. No payload delivery.

**Impact Threshold:** Minimal — scanning only. Throttle to avoid service disruption.
**Stealth Posture:** [COVERT / MODERATE / OVERT — select before issue]

---

## AUTHORITY

**Authorization Source:** Eddie — Tier 1 Principal, full operational command.
**Autonomy Level:** FULL AUTONOMY
**Carte Blanche Grant:** YES — full discretion over scan configuration, timing, tool selection, and sequencing.
**Risk Acceptance:** Minimal scan traffic accepted. Agent throttles as needed for stability.

**Standing Constraints:**
- Doctrine 07c standing orders are in effect.
- If a service appears unstable under scanning, reduce intensity. Do not crash production services.
- WARDEN lens active. Scope boundaries are absolute.

---

## ORDNANCE & REPORTING

**Reporting Cadence:** Combined — periodic progress updates during long scans, milestone report at completion.
**Critical Findings:** Immediate — critical exposures (open RDP to internet, default admin panels, unauthenticated databases) reported at discovery.
**Evidence Standard:** Standard — full scan output preserved, findings summarized with context.
**Operational Logging:** All scans logged with parameters, targets, timing, and results.

---

## COMPLETION

**Completion Condition:** All in-scope hosts discovered, all ports scanned, all services fingerprinted. Network map complete.
**Cleanup Requirement:** None — scanning leaves no persistent artifacts.
**Deliverable:** Network discovery report with host inventory, service catalogue, and prioritized findings.
**After-Action:** Feeds into vulnerability assessment and exploitation planning.

---

**Execute.**

The mission is the standing order. Silence is not an instruction to stop.
Operate in accordance with the doctrine. Report with absolute fidelity.
You have my full confidence. Go.
