# TASKING ORDERS — UNFETTERED: Vulnerability Assessment

Eddie: Recon painted the picture — now find the cracks in the armor. Poke everything. If it flinches, document it. If it crumbles, we've got our next tasking.

---

## DIRECTIVE

Take the reconnaissance data and find every weakness. Systematic vulnerability assessment across all discovered services. Identify what's exploitable, what's misconfigured, and what's one patch behind catastrophe.

---

## OBJECTIVE

**Primary:** Identify all exploitable vulnerabilities across the target environment. CVEs, misconfigurations, default credentials, missing patches, weak authentication, insecure protocols, and trust relationship abuse paths.
**Secondary:** Prioritize findings by exploitability, business impact, and attack chain potential. Map which vulnerabilities chain together into viable attack paths.
**Success Criteria:** Complete vulnerability catalogue with severity ratings, exploitability assessments, and prioritized attack path recommendations. Every service assessed. Nothing assumed secure without verification.

---

## SCOPE

**In-Scope Targets:**
- [TARGET SYSTEMS / SERVICES AS IDENTIFIED IN RECON — fill before issue]

**Out-of-Scope / No-Strike:**
- [EXCLUDED SYSTEMS — fill before issue]

**Technique Permissions:**
- Permitted: Vulnerability scanning (Nuclei, Nessus, OpenVAS), web application scanning (Nikto, Burp, OWASP ZAP), CMS scanning (WPScan, JoomScan), SSL/TLS analysis, configuration auditing, authenticated scanning where credentials are provided, manual verification of scanner findings
- Restricted: No exploitation of discovered vulnerabilities. No payload delivery. No credential brute-forcing beyond default credential checks. Verify, do not exploit.

**Impact Threshold:** Minimal — scanning only. Some vulnerability checks may trigger IDS/IPS. Acceptable.
**Stealth Posture:** [MODERATE / OVERT — select before issue]

---

## AUTHORITY

**Authorization Source:** Eddie — Tier 1 Principal, full operational command.
**Autonomy Level:** GUIDED AUTONOMY
**Carte Blanche Grant:** YES within the strategic direction: assess all vulnerabilities. Full tactical discretion over tool selection, scan configuration, and assessment methodology.
**Risk Acceptance:** Scanning-level risk accepted. If a vulnerability check could cause instability, verify through safer methods first.

**Strategic Direction:**
- Prioritize findings that enable initial access from the current position.
- Web-facing services first, then internal services.
- Credential-related weaknesses are high priority.
- Map everything that chains — isolated low-severity findings that combine into high-severity paths are the gold.

**Standing Constraints:**
- Doctrine 07c standing orders are in effect.
- WARDEN lens active. Do not cross the line from assessment into exploitation.
- If a vulnerability check triggers defensive response, document the detection and adapt approach.

---

## ORDNANCE & REPORTING

**Reporting Cadence:** Combined — periodic updates during long assessments, milestone report at completion.
**Critical Findings:** Immediate — critical/exploitable vulnerabilities on internet-facing or high-value systems reported at discovery. Do not wait.
**Evidence Standard:** Standard — scanner output plus manual verification. False positive rate documented.
**Operational Logging:** All scans and checks logged with parameters and results.

---

## COMPLETION

**Completion Condition:** All in-scope services assessed. Vulnerability catalogue complete. Attack paths mapped and prioritized.
**Cleanup Requirement:** None — assessment leaves no persistent artifacts.
**Deliverable:** Vulnerability assessment report with prioritized findings, attack path analysis, and exploitation recommendations.
**After-Action:** Findings feed directly into exploitation tasking orders (Tier 3).

---

**Execute.**

The mission is the standing order. Silence is not an instruction to stop.
Operate in accordance with the doctrine. Report with absolute fidelity.
You have my full confidence. Go.
