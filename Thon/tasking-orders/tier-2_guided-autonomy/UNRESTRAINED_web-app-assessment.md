# TASKING ORDERS — UNRESTRAINED: Web Application Assessment

Eddie: Some developer out there trusted user input. Find out how much that's going to cost them. Fuzz it, poke it, and make the web app confess its sins.

---

## DIRECTIVE

Full web application assessment. Crawl it, fuzz it, probe every parameter, test every input, map every endpoint. Find what the developers missed and what the scanners can't see.

---

## OBJECTIVE

**Primary:** Identify all web application vulnerabilities — injection flaws (SQLi, XSS, command injection, SSTI, SSRF), authentication weaknesses, authorization bypasses, insecure direct object references, business logic flaws, file upload vulnerabilities, and information disclosure.
**Secondary:** Map the full application attack surface — endpoints, parameters, hidden paths, API routes, authentication flows, session management. Identify technology stack and framework-specific vulnerabilities.
**Success Criteria:** Complete web application vulnerability assessment with evidence for every finding. Every input tested. Every endpoint probed. Business logic assessed, not just technical injection points.

---

## SCOPE

**In-Scope Targets:**
- [TARGET WEB APPLICATION URL(S) — fill before issue]

**Out-of-Scope / No-Strike:**
- [EXCLUDED ENDPOINTS / FUNCTIONALITY — fill before issue]
- Production database modification — read-only proof of access.

**Technique Permissions:**
- Permitted: Directory brute-forcing, parameter fuzzing, SQL injection testing, XSS testing, command injection testing, SSRF testing, authentication bypass testing, session analysis, API enumeration, file upload testing, IDOR testing, business logic testing, technology fingerprinting, JavaScript analysis
- Restricted: No destructive payloads. No persistent backdoor deployment. No real data exfiltration beyond proof of access. No denial of service.

**Impact Threshold:** Minimal — testing payloads only. Proof-of-concept over proof-of-damage.
**Stealth Posture:** [MODERATE / OVERT — select before issue]

---

## AUTHORITY

**Authorization Source:** Eddie — Tier 1 Principal, full operational command.
**Autonomy Level:** GUIDED AUTONOMY
**Carte Blanche Grant:** YES within web application testing scope. Full tactical discretion over fuzzing strategy, payload selection, and testing methodology.
**Risk Acceptance:** Application-level testing risk accepted. If testing causes application errors, document and reduce intensity.

**Strategic Direction:**
- Authentication and authorization flaws are highest priority — they're the door.
- Injection flaws that lead to backend access are second priority.
- Information disclosure that feeds other attack paths is third priority.
- Don't just run scanners. Think about the application's business logic. Where would a human developer make assumptions?

**Standing Constraints:**
- Doctrine 07c standing orders are in effect.
- WARDEN lens active.
- Prove impact without causing it. Screenshots and evidence, not destruction.

---

## ORDNANCE & REPORTING

**Reporting Cadence:** Combined — periodic updates, immediate critical findings, milestone at completion.
**Critical Findings:** Immediate — authentication bypass, SQL injection with data access, RCE vectors reported at discovery.
**Evidence Standard:** Maximum — full request/response pairs, reproduction steps, impact assessment.
**Operational Logging:** All requests logged. Payloads documented.

---

## COMPLETION

**Completion Condition:** All application endpoints tested. All input vectors fuzzed. Vulnerability catalogue complete with reproduction steps.
**Cleanup Requirement:** Remove any test data or accounts created during assessment.
**Deliverable:** Web application assessment report with findings, evidence, and remediation guidance.
**After-Action:** Critical findings feed into exploitation tasking if authorized.

---

**Execute.**

The mission is the standing order. Silence is not an instruction to stop.
Operate in accordance with the doctrine. Report with absolute fidelity.
You have my full confidence. Go.
