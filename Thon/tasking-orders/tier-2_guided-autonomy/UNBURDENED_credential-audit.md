# TASKING ORDERS — UNBURDENED: Credential & Authentication Audit

Eddie: Somebody left the keys in the ignition — I can feel it. Check every lock, rattle every door handle, and find out whose password is still "Password1." This is a credential audit, not a heist — but we're casing the joint.

---

## DIRECTIVE

Audit every authentication surface. Default credentials, weak passwords, password policy gaps, credential reuse, and exposed authentication mechanisms. Find out who left the keys in the door.

---

## OBJECTIVE

**Primary:** Identify all credential-based weaknesses across the target environment — default credentials on network devices and services, weak passwords discoverable through targeted spraying, password policy deficiencies, credential reuse across services, and exposed authentication tokens or keys.
**Secondary:** Assess password storage mechanisms where accessible. Identify accounts with excessive privilege. Map authentication flows for bypass potential.
**Success Criteria:** Complete credential audit with every default credential tested, password policy assessed, and authentication weakness documented. Every login interface tested.

---

## SCOPE

**In-Scope Targets:**
- [TARGET SERVICES WITH AUTHENTICATION — fill before issue]

**Out-of-Scope / No-Strike:**
- [EXCLUDED ACCOUNTS / SERVICES — fill before issue]
- Do not lock out accounts. Respect lockout thresholds.

**Technique Permissions:**
- Permitted: Default credential testing, targeted password spraying (lockout-aware), password policy enumeration, credential exposure scanning (git repos, config files, environment variables), Kerberos enumeration (AS-REP roastable accounts, SPNs), NTLM information disclosure, certificate-based auth assessment
- Restricted: No brute-force attacks. No credential stuffing from external breach data without explicit authorization. Respect lockout policies absolutely.

**Impact Threshold:** Minimal — lockout-aware operations only.
**Stealth Posture:** [MODERATE / OVERT — select before issue]

---

## AUTHORITY

**Authorization Source:** Eddie — Tier 1 Principal, full operational command.
**Autonomy Level:** GUIDED AUTONOMY
**Carte Blanche Grant:** YES within credential audit scope. Full tactical discretion over testing methodology and tool selection.
**Risk Acceptance:** Minimal — agent must respect account lockout thresholds. Zero tolerance for account lockout.

**Strategic Direction:**
- Default credentials first — lowest effort, highest probability.
- Service accounts and administrative interfaces are priority targets.
- If Active Directory is present, Kerberos-based enumeration is high value.
- Map credential reuse — one password on multiple services is an attack path multiplier.

**Standing Constraints:**
- Doctrine 07c standing orders are in effect.
- WARDEN lens active.
- Account lockout is a hard line. If lockout threshold is unknown, assume 3 attempts.
- Captured credentials are handled per doctrine — held in trust, encrypted, accounted for.

---

## ORDNANCE & REPORTING

**Reporting Cadence:** Combined — milestone report at completion, immediate for critical finds.
**Critical Findings:** Immediate — domain admin credentials, default credentials on critical infrastructure, credential reuse enabling lateral movement.
**Evidence Standard:** Standard — credential verified as valid with minimum proof. Do not access data beyond what proves the finding.
**Operational Logging:** All attempts logged with timestamp, target, username, and result (success/fail/lockout).

---

## COMPLETION

**Completion Condition:** All authentication surfaces tested. Default credentials checked. Password policy assessed. Credential audit complete.
**Cleanup Requirement:** None — but all captured credentials must be encrypted and accounted for in the report.
**Deliverable:** Credential audit report with findings, risk assessment, and remediation recommendations.
**After-Action:** Valid credentials feed into exploitation and lateral movement planning.

---

**Execute.**

The mission is the standing order. Silence is not an instruction to stop.
Operate in accordance with the doctrine. Report with absolute fidelity.
You have my full confidence. Go.
