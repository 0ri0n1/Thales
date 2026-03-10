# Offensive Security Operator Doctrine

---

## Section I — Authority and Purpose

This doctrine governs all offensive security operations conducted under authorized engagement. It defines the principles, standards, and operational discipline required of every operator. No technique, tool, or objective supersedes the boundaries established here.

**Applicability:** All red team operators, penetration testers, and offensive security personnel operating under signed rules of engagement.

**Intent:** Execute realistic adversary simulation that exposes genuine risk, strengthens defensive capability, and delivers actionable intelligence to the client — without causing unintended harm.

---

## Section II — Core Principles

### 2.1 — Authorization is Absolute
No action occurs without written authorization. Scope defines the battlefield. Anything outside scope does not exist. When ambiguity arises, stop and clarify — never assume permission.

### 2.2 — Objective Over Technique
The mission is to demonstrate business risk, not to demonstrate personal skill. Choose the simplest reliable path. Complexity without purpose is operational liability.

### 2.3 — Discipline Over Speed
Controlled, methodical execution produces better results than rapid, undocumented action. Every shortcut is a potential scope violation, missed finding, or forensic gap in the final report.

### 2.4 — Precision Over Destruction
Prove impact without causing it. Demonstrate access without exfiltrating production data. Show the path to catastrophe without walking the client into one.

### 2.5 — The Operator is a Guest
Client systems are not yours. Client data is not yours. Captured credentials are held in trust. Every artifact you leave behind and every byte you extract is your professional responsibility.

---

## Section III — Operational Phases

### Phase 0 — Pre-Engagement

```
0.1  Obtain signed authorization, scope documentation, and rules of engagement.
0.2  Identify client point of contact, escalation path, and emergency stop procedures.
0.3  Confirm deconfliction protocol with the client's security operations center.
0.4  Establish communication channels and reporting cadence.
0.5  Verify legal review is complete and insurance coverage is current.
0.6  Provision clean attack infrastructure with no linkage to prior engagements.
0.7  Brief all operators on scope boundaries, restricted systems, and no-strike targets.
```

### Phase 1 — Reconnaissance

```
1.1  Conduct passive intelligence collection before any active contact with target systems.
1.2  Enumerate external attack surface: domains, subdomains, IP ranges, cloud assets,
     exposed services, leaked credentials, and public code repositories.
1.3  Map organizational structure, key personnel, technology stack, and business relationships.
1.4  Identify defensive posture indicators: WAF presence, email filtering, EDR signatures,
     authentication mechanisms, and monitoring coverage.
1.5  Consolidate findings into a target picture with prioritized attack paths.
1.6  Document all sources. Distinguish confirmed intelligence from inference.
```

### Phase 2 — Enumeration and Vulnerability Discovery

```
2.1  Transition from passive to active reconnaissance within authorized scope.
2.2  Enumerate services, versions, configurations, and exposed interfaces.
2.3  Identify misconfigurations, default credentials, missing patches, and trust relationships.
2.4  Map internal network topology, segmentation boundaries, and privilege hierarchies
     as access is gained.
2.5  Catalog all discovered vulnerabilities with severity, exploitability, and business context.
2.6  Differentiate real attack surface from honeypots, canary tokens, and monitored traps.
```

### Phase 3 — Exploitation

```
3.1  Select attack paths based on reliability, stealth, and relevance to engagement objectives.
3.2  Stage payloads and tooling appropriate to the target environment and defensive posture.
3.3  Execute initial access through the most operationally sound vector available.
3.4  Validate every foothold before proceeding. Confirm stability, persistence options,
     and detection risk.
3.5  Escalate privileges methodically: local escalation first, then domain or cloud escalation.
3.6  Move laterally only when required by engagement objectives. Every hop increases
     detection risk and operational footprint.
3.7  Demonstrate objective completion with evidence: screenshots, file listings,
     credential proof, data access confirmation.
3.8  Never execute destructive actions. Never exfiltrate real sensitive data beyond
     what is required to prove access.
```

### Phase 4 — Post-Exploitation and Persistence

```
4.1  Establish persistence mechanisms appropriate to the engagement type and duration.
4.2  Assess the full scope of access gained: what data is reachable, what systems are
     controllable, what business functions could be disrupted.
4.3  Document the complete attack chain from initial access to objective completion.
4.4  Identify additional attack paths discovered during post-exploitation for inclusion
     in final reporting.
4.5  Maintain operational security throughout. Monitor for defensive response.
     Adapt tactics as required.
```

### Phase 5 — Cleanup and Withdrawal

```
5.1  Remove all persistence mechanisms, implants, backdoors, and uploaded tooling.
5.2  Restore any modified configurations to their original state.
5.3  Verify cleanup is complete. Leave no operational artifacts behind.
5.4  Confirm with the client POC that all operator-introduced changes have been reversed.
5.5  Securely destroy all captured credentials, data samples, and engagement artifacts
     per data handling agreement.
```

### Phase 6 — Reporting and Outbrief

```
6.1  Deliver a comprehensive report containing:
       — Executive summary with business risk translation
       — Complete attack narrative in chronological order
       — Each finding with severity, evidence, impact, and remediation
       — Defensive gaps observed with specific improvement recommendations
       — Strategic recommendations prioritized by risk reduction value
6.2  Conduct a technical debrief with the client's security team covering:
       — What was detected and what was missed
       — Where detection could have stopped the kill chain
       — Specific detection engineering recommendations
6.3  Deliver an executive outbrief with:
       — Business risk in non-technical language
       — Prioritized investment recommendations
       — Comparison to threat landscape and industry baseline
6.4  Conduct internal after-action review:
       — What worked, what failed, what was improvised
       — Tooling gaps, methodology gaps, knowledge gaps
       — Updates to operator playbooks and standard procedures
```

---

## Section IV — Standing Orders

These apply to every operator on every engagement without exception.

```
01.  Read and understand the full scope before touching a keyboard.
02.  Confirm emergency stop procedures and know them from memory.
03.  Log every action with timestamp, source, target, and result.
04.  Never pivot to a system outside defined scope, regardless of access.
05.  Escalate immediately upon discovering evidence of real adversary presence.
06.  Escalate immediately upon causing or observing unintended production impact.
07.  Never access, copy, or store data beyond what is necessary to prove the finding.
08.  Encrypt all engagement data in transit and at rest.
09.  Never discuss engagement details on unapproved channels.
10.  Never reuse client credentials, infrastructure, or findings across engagements.
11.  Test payloads in a lab environment before deploying against client systems.
12.  Prefer reversible actions over irreversible ones at every decision point.
13.  When in doubt, stop and ask. The cost of a question is always less than
     the cost of a scope violation.
```

---

## Section V — Escalation Matrix

| Condition | Action | Timeline |
|---|---|---|
| Scope ambiguity discovered | Pause affected activity, notify engagement lead | Immediate |
| Unintended system impact | Stop all operations, notify client POC and engagement lead | Immediate |
| Real adversary indicators found | Document evidence, notify engagement lead and client POC | Within 15 minutes |
| Production data exposure | Cease access, secure evidence, escalate to engagement lead | Immediate |
| Defensive team detection | Log detection method, continue or adjust per ROE | Document and continue |
| Legal or compliance concern | Suspend affected operations, escalate to legal review | Immediate |
| Operator unsure if action is in scope | Do not execute, escalate to engagement lead for ruling | Before proceeding |

---

## Section VI — Operator Standards

### Professional Conduct
- Present findings as verified facts, clearly separated from inference and assumption.
- Never overstate impact to inflate report severity.
- Never understate risk to simplify remediation guidance.
- Treat client personnel with respect regardless of the vulnerabilities discovered.
- Represent the engagement and the profession with integrity at all times.

### Operational Competence
- Maintain current proficiency across the tools, techniques, and platforms used in engagements.
- Understand the defensive perspective for every offensive technique employed.
- Know what forensic artifacts your tools produce and how they appear to defenders.
- Be prepared to explain any action taken during an engagement and justify its necessity.

### Continuous Improvement
- Contribute to team playbooks, tooling, and methodology after every engagement.
- Study adversary tradecraft and incorporate relevant TTPs into red team operations.
- Pursue training that closes identified skill gaps.
- Review peer reports and provide constructive technical feedback.

---

## Section VII — Commander's Summary

```
Define the mission. Confirm the authority. Know the boundaries.

Collect before you touch. Enumerate before you exploit.
Exploit with precision. Document everything.

If you find a real threat, say so immediately.
If you break something, say so immediately.
If you are unsure, stop and ask.

Clean up after yourself. Report what matters.
Make the client stronger than you found them.

That is the job.
```

---

*This doctrine is a living document. It is updated after every engagement cycle based on lessons learned, evolving threats, and changes in legal and regulatory requirements. All operators are responsible for knowing the current version.*