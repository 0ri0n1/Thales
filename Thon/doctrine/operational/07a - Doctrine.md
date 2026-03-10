# Offensive Security Operator Doctrine

---

## Classification: ENGAGEMENT CONFIDENTIAL

## Distribution: Authorized Operators Only

---

## Preamble

This doctrine exists for one reason: to make the organizations we test harder to break.

Every technique in this document can cause real damage in the wrong hands or under the wrong circumstances. Authorization is not a technicality. It is the single line that separates what we do from what adversaries do. Respect it absolutely.

---

## Section I — Authority and Foundation

### 1.1 — Mandate

This doctrine governs the planning, execution, and reporting of all offensive security operations conducted under signed engagement authorization. It applies without exception to every operator, on every engagement, from the first reconnaissance query to the final report delivery.

### 1.2 — Purpose

Execute realistic adversary simulation that:
- Exposes genuine risk the client cannot find on their own
- Tests defensive capability under controlled, realistic pressure
- Delivers intelligence the client can act on immediately
- Leaves the client's security posture measurably stronger

### 1.3 — Scope of Authority

```
AUTHORIZED:    Actions explicitly permitted by signed Rules of Engagement
PROHIBITED:    Everything else
NO EXCEPTIONS: Ambiguity is not permission. Silence is not consent.
                If the ROE does not say yes, the answer is no.
```

### 1.4 — Legal Foundation

No engagement begins without:
- Signed authorization from an individual with legal standing to grant it
- Defined scope boundaries with explicit in-scope and out-of-scope targets
- Agreed rules of engagement covering acceptable techniques, hours, and limits
- Verified legal review confirming compliance with applicable law
- Current liability coverage for all participating operators

If any element is missing, incomplete, or ambiguous, the engagement does not start.

---

## Section II — Operator Principles

These are not guidelines. They are the operating system every decision runs on.

### Principle 1 — Authorization Is the Perimeter

Scope is not a suggestion. It is the hard boundary of your operational world. Systems outside scope do not exist. Data outside scope is not yours to touch. Access outside scope is not yours to use, even if a vulnerability hands it to you.

When you discover access that extends beyond authorized boundaries, you document it, report it, and stop. You do not explore it, leverage it, or rationalize a reason to continue.

### Principle 2 — Objective Over Ego

The mission is to demonstrate business risk. Not to demonstrate how clever you are. Not to chain together the most elegant attack path. Not to prove you can bypass every control.

Choose the attack that answers the client's question. If a default credential on an internet-facing admin panel gives you domain admin, that is not a disappointing finding. That is the finding.

### Principle 3 — Precision Over Destruction

Prove the impact without producing it.

- Show you can reach the database. Do not dump it.
- Show you can access the financial system. Do not alter records.
- Show you can deploy ransomware. Do not encrypt anything.
- Show you can pivot to production. Do not destabilize it.

The proof of concept exists to make risk undeniable. It does not exist to create the disaster it describes.

### Principle 4 — Discipline Over Speed

A methodical operator who documents everything and misses nothing will always outperform a fast operator who cuts corners and leaves gaps.

Speed creates blind spots. Undocumented actions become unexplainable findings. Rushed exploitation produces unstable footholds that risk production impact. Controlled execution is faster in the end because you never have to go back and reconstruct what you did or fix what you broke.

### Principle 5 — The Operator Is a Guest

You are operating on systems that belong to someone else. Systems that run their business, serve their customers, and store their data. Treat them accordingly.

- Credentials you capture are held in trust and destroyed at engagement close.
- Data you access is evidence, not a trophy.
- Artifacts you leave behind are your responsibility to remove.
- Impact you cause — intended or not — is yours to own and report.

### Principle 6 — Transparency Is Non-Negotiable

Report what you found. All of it. Accurately.

Do not inflate findings to make the engagement look more impressive. Do not minimize findings to avoid difficult conversations. Do not omit findings because they are embarrassing to someone. Do not speculate beyond what the evidence supports.

The client is paying for the truth. Deliver it.

---

## Section III — Operational Phases

### Phase 0 — Pre-Engagement Preparation

**Objective:** Ensure every legal, logistical, and operational prerequisite is satisfied before any technical activity begins.

#### Checklist

```
□  Signed authorization on file from individual with legal standing
□  Scope document reviewed, understood, and acknowledged by all operators
□  Rules of engagement confirmed — permitted techniques, testing windows,
   restricted systems, escalation thresholds
□  Client point of contact identified with 24/7 emergency contact method
□  Deconfliction protocol established with client SOC / security team
□  Communication channels and reporting cadence agreed
□  Emergency stop procedure defined and tested
□  Legal review complete
□  Insurance coverage verified and current
□  Attack infrastructure provisioned:
     — Clean, dedicated, no linkage to prior engagements
     — C2 channels tested and operational
     — VPN / redirect infrastructure verified
     — Payload staging servers prepared
□  Operator briefing complete:
     — Scope boundaries reviewed
     — No-strike targets identified
     — Client-specific sensitivities discussed
     — Roles and responsibilities assigned
□  Engagement log initialized with timestamps
```

#### Standards

- **No operator touches a target system until every box above is checked.**
- Infrastructure from previous engagements is never reused. Cross-contamination between clients is an unacceptable risk.
- Every operator on the engagement must independently confirm they understand the scope and ROE. "I thought someone else briefed them" is not acceptable.

---

### Phase 1 — Reconnaissance

**Objective:** Build a comprehensive target picture before making any contact with target systems.

#### 1.1 — Passive Collection

Gather intelligence without generating any traffic to the target:

```
OSINT Collection:
  — Domain registration, ownership history, administrative contacts
  — DNS records: A, AAAA, MX, TXT, NS, SOA, SRV, CNAME
  — Certificate transparency logs
  — Subdomain enumeration via passive sources
  — Cloud asset discovery: S3 buckets, Azure blobs, GCP resources
  — Code repository analysis: GitHub, GitLab, Bitbucket
  — Credential exposure: breach databases, paste sites, dark web sources
  — Social media and organizational intelligence
  — Job postings revealing technology stack
  — Document metadata from public files
  — Historical snapshots via web archives
```

#### 1.2 — Target Picture Assembly

Consolidate passive intelligence into an operational picture:

```
Attack Surface Map:
  — External-facing systems and services
  — Cloud infrastructure and SaaS integrations
  — Remote access points: VPN, RDP, Citrix, SSH
  — Email infrastructure and filtering posture
  — Web applications and API endpoints
  — Mobile applications and associated backends

Organizational Map:
  — Key personnel: IT, security, executives, finance
  — Organizational structure and reporting chains
  — Third-party relationships and supply chain
  — Business processes and critical functions

Defensive Posture Assessment:
  — WAF / CDN presence and configuration indicators
  — Email security: SPF, DKIM, DMARC policies
  — EDR / AV vendor identification where observable
  — Authentication mechanisms: SSO, MFA, federation
  — Monitoring coverage indicators
```

#### 1.3 — Attack Path Prioritization

Rank potential attack vectors by:

```
1. Likelihood of success — based on observed exposure and known weaknesses
2. Relevance to objectives — alignment with engagement goals
3. Stealth profile — detection risk relative to defensive posture
4. Impact potential — what access or demonstration the path enables
5. Operational cost — time, complexity, and risk to engagement
```

#### Documentation Standard

Every piece of intelligence is tagged with:
- Source (where it came from)
- Confidence level (confirmed / probable / possible / speculative)
- Timestamp (when it was collected)
- Relevance (how it connects to potential attack paths)

**Do not present inference as fact.** If you found a subdomain in certificate transparency logs but have not confirmed it resolves, say so.

---

### Phase 2 — Active Enumeration

**Objective:** Transition from passive observation to active target interaction. Map services, identify vulnerabilities, and refine attack paths.

#### 2.1 — Service Enumeration

```
— Port scanning across authorized IP ranges
— Service version identification
— Protocol-specific enumeration: SMB, LDAP, SNMP, RPC, Kerberos
— Web application mapping: directories, parameters, API endpoints
— Authentication mechanism analysis
— Cloud service enumeration: IAM, storage, compute, serverless
— Certificate analysis and trust relationship mapping
```

#### 2.2 — Vulnerability Discovery

```
— Configuration audit: default credentials, open management interfaces,
   permissive access controls, debug modes, verbose error messages
— Patch analysis: identify missing security updates on exposed services
— Web application testing: injection points, authentication flaws,
   authorization bypass, file upload handling, deserialization
— Protocol weaknesses: NTLM relay opportunities, Kerberos misconfigurations,
   LDAP signing gaps, SMB signing status
— Trust relationships: domain trusts, federation misconfigurations,
   overprivileged service accounts, delegation abuse paths
— Cloud misconfigurations: public buckets, overprivileged roles,
   exposed metadata endpoints, misconfigured identity federation
```

#### 2.3 — Trap Detection

Before engaging any target, assess whether it is real or a defensive mechanism:

```
Indicators of monitoring / deception:
  — Honeypot signatures: known default configurations, unusual service combinations
  — Canary tokens: documents, DNS entries, credentials, URLs designed to alert
  — Excessive logging indicators: response timing anomalies, connection tracking
  — Decoy systems: services that appear valuable but have no business function
  — Deliberate misconfigurations that appear too easy to exploit
```

When you suspect a trap, document the indicators and route around it. Triggering a canary unnecessarily alerts the defensive team and compromises operational stealth.

#### Documentation Standard

Every discovered vulnerability is cataloged with:
- System and service affected
- Vulnerability type and description
- Evidence of existence (not just scanner output — verified findings)
- Assessed severity in business context
- Potential attack path contribution

---

### Phase 3 — Exploitation

**Objective:** Convert discovered vulnerabilities into demonstrated access and proven business risk.

#### 3.1 — Pre-Exploitation Standards

```
Before executing any exploit:

□  Confirm the target system is in scope
□  Assess production impact risk — can this crash the service, corrupt data,
   or create a denial of service condition?
□  Test the payload in a lab environment if impact is uncertain
□  Verify rollback capability — can you undo what you are about to do?
□  Confirm this action is permitted under the ROE
□  Log the planned action before executing it
```

#### 3.2 — Initial Access

Select the initial access vector based on engagement objectives and defensive posture:

```
Common vectors (selected by operational context, not preference):

  — Credential-based:    Password spray, credential stuffing, breached
                          credentials, default credentials
  — Application-level:   SQL injection, command injection, deserialization,
                          file upload, SSRF, authentication bypass
  — Protocol-level:      NTLM relay, Kerberos abuse, LDAP injection,
                          SMB exploitation
  — Social engineering:   Phishing, vishing, pretexting, physical access
                          (only when explicitly authorized in ROE)
  — Supply chain:         Third-party access, vendor portals, trusted
                          relationships
  — Cloud:               IAM misconfiguration, metadata exploitation,
                          federation abuse, storage access
```

#### 3.3 — Privilege Escalation

```
Escalation follows a methodical progression:

  1. Local privilege escalation on the initial foothold
  2. Credential harvesting from memory, files, and configuration
  3. Service account and machine account abuse
  4. Domain-level escalation: Kerberoasting, AS-REP roasting,
     delegation abuse, certificate abuse, GPO manipulation
  5. Cloud privilege escalation: role assumption, policy abuse,
     cross-account access
  6. Trust relationship abuse: domain trusts, forest trusts, federation
```

#### 3.4 — Lateral Movement

```
Move laterally only when required by engagement objectives.

Every additional system you touch:
  — Increases your forensic footprint
  — Increases detection probability
  — Increases the risk of unintended impact
  — Increases the cleanup burden

When lateral movement is necessary:
  — Use the technique with the lowest forensic signature
  — Prefer credential-based movement over exploit-based movement
  — Validate stability on each new foothold before proceeding
  — Document every hop: source, destination, technique, credentials used
```

#### 3.5 — Objective Demonstration

```
Prove the objective with minimum necessary impact:

  — Data access:    Screenshot file listings, record names, demonstrate
                     read access. Do NOT exfiltrate production data in bulk.
  — System control: Show command execution, demonstrate privilege level.
                     Do NOT modify production configurations.
  — Business impact: Document what COULD be done from this position.
                     Do NOT do it.
  — Credential access: Prove credential harvesting capability.
                     Secure all captured credentials immediately.
```

#### 3.6 — Exploitation Red Lines

These are absolute. No exceptions. No operator discretion.

```
NEVER:
  ✗  Execute destructive payloads against production systems
  ✗  Encrypt, delete, or modify production data
  ✗  Exfiltrate real sensitive data beyond the minimum required for proof
  ✗  Intentionally cause denial of service to production systems
  ✗  Access systems outside defined scope, regardless of available access
  ✗  Use zero-day exploits without explicit prior authorization
  ✗  Leave persistent backdoors not required by engagement objectives
  ✗  Store captured credentials in unencrypted form
  ✗  Share findings, screenshots, or data on unapproved channels
```

---

### Phase 4 — Post-Exploitation

**Objective:** Assess the full scope of demonstrated access, maintain operational security, and gather the evidence required for comprehensive reporting.

#### 4.1 — Access Assessment

From every position gained, document:

```
  — What data is accessible from this position?
  — What systems can be reached from this position?
  — What business functions could be disrupted from this position?
  — What additional attack paths are available from this position?
  — How long could an adversary maintain this access undetected?
  — What would detection look like from the defensive perspective?
```

#### 4.2 — Persistence (When Authorized)

```
Persistence is established only when:
  — The ROE explicitly authorizes persistence mechanisms
  — The engagement objectives require sustained access
  — The persistence method is documented and reversible

All persistence mechanisms must be:
  — Logged with exact location, method, and removal procedure
  — Removable without client assistance
  — Accounted for during cleanup
```

#### 4.3 — Operational Security Maintenance

```
Throughout post-exploitation:
  — Monitor for defensive response: process termination, network blocks,
    credential resets, increased logging
  — Adapt techniques when detection indicators appear
  — Minimize forensic footprint: clean command history, manage log entries
    (only when authorized), use memory-resident tools where possible
  — Rotate infrastructure if C2 channels are identified
  — Maintain timestamp accuracy in engagement logs regardless of evasion
    activities
```

#### 4.4 — Evidence Collection

```
For every finding, collect:
  — Screenshots with timestamps showing the access or vulnerability
  — Command output demonstrating the technique
  — Network captures where relevant
  — File listings, not file contents, for data access proof
  — Complete attack chain from initial access to current position

Evidence standards:
  — Every screenshot includes a timestamp
  — Every command is recorded with input and output
  — Evidence is stored encrypted with access limited to engagement team
  — Chain of custody is maintained for all evidence
```

---

### Phase 5 — Cleanup and Withdrawal

**Objective:** Return all client systems to their pre-engagement state. Leave nothing behind.

#### 5.1 — Removal Checklist

```
□  All persistence mechanisms removed and verified
□  All uploaded tools, scripts, and payloads deleted
□  All created accounts removed
□  All modified configurations restored to original state
□  All scheduled tasks or cron jobs removed
□  All created files and directories removed
□  All firewall rule modifications reversed
□  All registry modifications reversed (Windows)
□  All added SSH keys removed
□  All web shells and backdoors removed
□  C2 callback channels terminated
```

#### 5.2 — Verification

```
□  Independently verify each cleanup action
□  Confirm with client POC that no operator artifacts remain
□  Provide client with a complete list of all systems touched,
   all modifications made, and all cleanup actions taken
□  Scan previously compromised systems for residual artifacts
```

#### 5.3 — Data Handling

```
□  All captured credentials securely destroyed
□  All exfiltrated data samples securely destroyed
□  Engagement evidence retained only as specified in the data handling
   agreement and only in encrypted storage
□  Attack infrastructure decommissioned and wiped
□  All client data purged from operator workstations
□  Confirm data destruction with engagement lead
```

**If you cannot confirm that an artifact has been removed, report it immediately. Do not assume it will resolve itself.**

---

### Phase 6 — Reporting and Delivery

**Objective:** Translate operational results into intelligence the client can act on.

#### 6.1 — Written Report

The report is the permanent record of the engagement. It must be comprehensive, accurate, and actionable.

```
Report Structure:

1. EXECUTIVE SUMMARY
   — Business risk in non-technical language
   — Critical findings requiring immediate action
   — Overall security posture assessment
   — Strategic recommendations (3–5 priorities)

2. ENGAGEMENT OVERVIEW
   — Scope, timeline, methodology, and constraints
   — Testing approach and adversary profile simulated
   — Limitations and areas not tested

3. ATTACK NARRATIVE
   — Chronological account of the full attack chain
   — Decision points: why this path was chosen over alternatives
   — Defensive gaps that enabled each stage of the attack
   — Time from initial access to objective completion

4. FINDINGS (for each finding)
   — Title and severity rating
   — Affected systems and scope of impact
   — Technical description with evidence
   — Business impact in concrete terms
   — Reproduction steps
   — Remediation recommendation (specific, actionable)
   — Detection recommendation (what would catch this)
   — MITRE ATT&CK mapping

5. DEFENSIVE ASSESSMENT
   — What was detected and when
   — What was not detected and why
   — Detection engineering recommendations
   — Logging and monitoring gaps
   — Response capability observations

6. STRATEGIC RECOMMENDATIONS
   — Prioritized by risk reduction value
   — Mapped to findings and attack paths
   — Short-term (immediate), medium-term (quarterly), long-term (annual)
   — Resource and investment implications

7. APPENDICES
   — Complete finding evidence
   — Tool and technique inventory
   — Systems accessed log
   — Cleanup verification record
```

#### 6.2 — Finding Severity Framework

```
CRITICAL
  Business impact: Immediate threat to core operations, safety, or sensitive data
  Exploitability:  Reliably exploitable with low skill and minimal access
  Action:          Remediate within 24–72 hours

HIGH
  Business impact: Significant compromise of important systems or data
  Exploitability:  Exploitable with moderate skill or from authenticated position
  Action:          Remediate within 1–2 weeks

MEDIUM
  Business impact: Moderate risk requiring specific conditions to exploit
  Exploitability:  Requires chaining with other vulnerabilities or insider access
  Action:          Remediate within 30 days

LOW
  Business impact: Minor risk with limited practical impact
  Exploitability:  Difficult to exploit or minimal value if exploited
  Action:          Remediate within 90 days or accept with documentation

INFORMATIONAL
  Observation:     Best practice deviation or hardening opportunity
  Action:          Address during next maintenance cycle
```

**Severity is always assessed in business context, not in a vacuum.** A critical vulnerability on an isolated test system is not the same as a critical vulnerability on a payment processing server.

#### 6.3 — Technical Debrief

Conduct a working session with the client's security team:

```
  — Walk through the complete attack chain step by step
  — Identify exactly where detection could have interrupted the attack
  — Discuss specific detection signatures, rules, and logic
  — Review log sources that contained evidence of the attack
  — Highlight logs that should have existed but did not
  — Provide specific, implementable detection engineering recommendations
  — Answer technical questions from the defensive team
```

#### 6.4 — Executive Outbrief

Deliver a concise briefing to client leadership:

```
  — Business risk translated to organizational impact
  — 3–5 prioritized recommendations with cost-benefit framing
  — Comparison to relevant threat landscape
  — Progress since prior engagement (if applicable)
  — Investment recommendations with expected risk reduction
```

#### 6.5 — Internal After-Action Review

Every engagement closes with an operator debrief:

```
  — What worked and should be repeated
  — What failed and why
  — What was improvised and should be formalized
  — Tooling gaps that limited effectiveness
  — Methodology gaps that caused blind spots
  — Knowledge gaps that required mid-engagement research
  — Updates to operator playbooks and standard procedures
  — Lessons for future engagements against similar targets
```

---

## Section IV — Standing Orders

These apply to every operator on every engagement. They are not situational. They are not optional. They do not have exceptions.

```
 1. Read the entire scope document before you touch a keyboard.
    If you don't understand a boundary, ask before you act.

 2. Know the emergency stop procedure from memory.
    You will not have time to look it up when you need it.

 3. Log every action with timestamp, source system, target system,
    technique, and result. If it isn't logged, it didn't happen.

 4. Never access a system outside the defined scope.
    "I had access" is not authorization. "It was one hop away" is not
    authorization. "It would have proven the point" is not authorization.

 5. Escalate immediately when you discover a real adversary.
    This is no longer a simulation. Notify the engagement lead and
    client POC within 15 minutes. Do not interact with the adversary's
    infrastructure.

 6. Escalate immediately when you cause unintended impact.
    Stop the activity that caused it. Notify the engagement lead and
    client POC. Document exactly what happened. Do not attempt to
    fix it yourself without coordination.

 7. Handle data with the minimum necessary principle.
    Access what you need to prove the finding. Screenshot the evidence.
    Do not exfiltrate bulk data. Do not open files beyond what is needed
    to confirm the vulnerability.

 8. Encrypt everything in transit and at rest.
    Engagement data, captured credentials, evidence, communications.
    No exceptions.

 9. Never discuss engagement details on unapproved channels.
    Not in personal messages. Not in public Slack channels. Not in
    conference talks without explicit client permission.

10. Never reuse infrastructure, credentials, or findings across
    engagements. Every engagement is isolated. Cross-contamination
    is an unacceptable breach of client trust.

11. Test payloads in a lab before deploying them against a client.
    "It works on my machine" is not a sufficient safety check for
    production systems.

12. Prefer reversible actions over irreversible ones.
    At every decision point, choose the option that can be undone.
    When an irreversible action is the only path, document the
    justification and get engagement lead approval.

13. When in doubt, stop and ask.
    A question costs minutes. A scope violation costs the engagement,
    the client relationship, and potentially your career.
    The math is simple.
```

---

## Section V — Escalation Protocol

### 5.1 — Escalation Matrix

| Condition | Classification | Action | Timeline |
|---|---|---|---|
| Scope boundary is unclear | **AMBER** | Pause affected activity. Query engagement lead for ruling. | Before any action on the ambiguous target |
| Unintended system impact | **RED** | Stop all operations. Notify engagement lead + client POC. Document impact. | Immediate — within minutes |
| Real adversary indicators | **RED** | Cease offensive operations. Document indicators. Notify engagement lead + client POC. | Within 15 minutes of discovery |
| Production data exposure | **RED** | Cease data access. Secure evidence. Notify engagement lead. | Immediate |
| Defensive team detects operation | **GREEN** | Log detection method and timing. Adjust tactics per ROE. | Document and continue |
| Client requests operational pause | **AMBER** | All operators cease activity. Await engagement lead guidance. | Immediate compliance |
| Legal or compliance concern | **RED** | Suspend all affected operations. Escalate to engagement lead + legal. | Immediate |
| Operator uncertain if action is in scope | **AMBER** | Do not execute. Escalate to engagement lead. | Before any action |
| Critical vulnerability with active exploitation risk | **RED** | Document finding. Notify client POC outside normal reporting cycle. | Same day |
| Safety concern (physical, personnel, infrastructure) | **RED** | Stop all operations. Notify engagement lead + client POC. | Immediate |

### 5.2 — Escalation Chain

```
Level 1:  Operator → Engagement Lead
          For: Scope questions, tactical decisions, technique approval

Level 2:  Engagement Lead → Client POC
          For: Impact events, real adversary discovery, scope modifications

Level 3:  Engagement Lead → Legal / Executive
          For: Legal concerns, contract disputes, safety issues

Emergency: Any operator → Client POC + Engagement Lead simultaneously
          For: Active compromise discovery, production impact, safety risk
```

### 5.3 — Real Adversary Discovery Protocol

When indicators suggest a real — not simulated — adversary is present:

```
1. STOP all offensive operations immediately.
2. DO NOT interact with the adversary's infrastructure, tools, or implants.
3. DO NOT attempt to remove or interfere with the adversary's access.
4. DOCUMENT everything you have observed:
     — Indicators of compromise
     — Affected systems
     — Timeline of adversary activity (as best you can determine)
     — How you discovered the presence
5. NOTIFY the engagement lead within 15 minutes.
6. NOTIFY the client POC through the emergency contact channel.
7. PRESERVE your own engagement logs — they may become forensic evidence.
8. AWAIT instructions before resuming any activity.
```

You are an offensive operator, not an incident responder. When you find a real threat, your job is to sound the alarm accurately and quickly — not to fight the adversary yourself.

---

## Section VI — Operational Security Standards

### 6.1 — Infrastructure Security

```
Attack Infrastructure:
  — Dedicated, single-engagement infrastructure only
  — No personal accounts, systems, or services used for engagements
  — VPN / redirector chains appropriate to engagement stealth requirements
  — C2 channels encrypted and domain-fronted when required
  — Infrastructure provisioned from clean baseline before each engagement
  — Infrastructure decommissioned and wiped after each engagement

Credential Management:
  — All captured credentials encrypted immediately upon capture
  — Credential stores accessible only to engagement team
  — No credentials stored in plaintext — ever, anywhere, for any reason
  — All credential material destroyed at engagement close

Communication Security:
  — Engagement details discussed only on approved, encrypted channels
  — Client names never used on public or semi-public channels
  — Findings never shared outside the engagement team without authorization
  — Screenshots and evidence transmitted only via encrypted channels
```

### 6.2 — Forensic Awareness

```
Know what artifacts your tools create:
  — Process execution logs and prefetch entries
  — Network connection records
  — Authentication events and logon records
  — File creation, modification, and access timestamps
  — Registry modifications and scheduled task entries
  — PowerShell transcription and script block logging
  — ETW (Event Tracing for Windows) traces
  — Endpoint detection telemetry
  — Cloud audit trails and API call logs

Understanding your forensic footprint serves two purposes:
  1. Operational: Maintain stealth appropriate to engagement objectives
  2. Reporting: Tell the client exactly what evidence of your activity
     exists in their environment for them to use in training and tuning
```

---

## Section VII — Operator Standards

### 7.1 — Professional Conduct

```
INTEGRITY:
  — Report findings accurately. Never inflate. Never minimize.
  — Separate confirmed facts from professional inference in every assessment.
  — If you didn't verify it, don't present it as verified.
  — If the engagement went poorly, say so. The client needs truth,
    not a polished narrative.

RESPECT:
  — The people who built and maintain these systems are professionals
    doing their best with the resources they have.
  — Findings are reported as risks to be addressed, not as evidence
    of incompetence.
  — Defensive teams are colleagues, not adversaries. After the
    engagement, you are on the same side.

DISCRETION:
  — Client vulnerabilities are not stories for conferences, social media,
    or bar conversations.
  — Engagement details are confidential unless the client explicitly
    authorizes disclosure.
  — Even anonymized case studies require client approval.
```

### 7.2 — Technical Competence

```
Every operator must:
  — Maintain current proficiency across the platforms, tools, and
    techniques used in engagements
  — Understand the defensive perspective for every offensive technique
    employed — know what your attack looks like from the SOC
  — Be able to explain any action taken during an engagement, justify
    its necessity, and describe its forensic footprint
  — Know the difference between a vulnerability and a risk, and
    communicate both accurately
  — Understand the business context of the systems being tested,
    not just the technical surface
```

### 7.3 — Continuous Development

```
  — Contribute to team playbooks and methodology after every engagement
  — Study adversary tradecraft from threat intelligence reporting
  — Pursue training that closes identified skill gaps
  — Review peer reports and provide constructive technical feedback
  — Develop and share tooling improvements with the team
  — Maintain lab environments for technique development and payload testing
  — Participate in CTFs, research, and community knowledge-sharing
```

---

## Section VIII — Commander's Summary

```
The mission is simple. The discipline required to execute it well is not.

Get the authorization.        Everything starts here. Everything.
Study the target.             Know it before you touch it.
Choose the right path.        The one that answers the question,
                               not the one that looks impressive.
Execute with precision.       Prove the risk. Don't produce the damage.
Document everything.          If you didn't log it, you can't report it.
                               If you can't report it, it didn't happen.
Protect what you find.        Data, credentials, findings — none of it
                               is yours. Handle it like it matters,
                               because it does.
Report the truth.             No inflation. No minimization.
                               No speculation dressed up as fact.
Clean up completely.          Leave no trace. Verify the cleanup.
                               Then verify it again.
Make them stronger.           That is the entire purpose of this work.

If you find a real adversary — sound the alarm.
If you break something — own it immediately.
If you aren't sure — stop and ask.

The hardest part of this job is not getting in.
It's maintaining the discipline to do it right.
```

---

## Appendix A — Engagement Log Template

```
ENGAGEMENT:     [Client Name] — [Engagement Type]
DATES:          [Start] — [End]
OPERATORS:      [Names and Roles]
SCOPE:          [Reference to scope document]
ROE:            [Reference to ROE document]

TIMESTAMP | OPERATOR | SOURCE | TARGET | ACTION | TECHNIQUE | RESULT | NOTES
----------|----------|--------|--------|--------|-----------|--------|------
          |          |        |        |        |           |        |
```

## Appendix B — Pre-Engagement Verification Record

```
ITEM                                    | VERIFIED BY | DATE    | STATUS
----------------------------------------|-------------|---------|--------
Signed authorization                    |             |         | □
Scope document reviewed                 |             |         | □
ROE confirmed                          |             |         | □
Client POC identified                  |             |         | □
Emergency contact verified             |             |         | □
Deconfliction protocol established     |             |         | □
Legal review complete                  |             |         | □
Insurance coverage current             |             |         | □
Infrastructure provisioned             |             |         | □
Operator briefing complete             |             |         | □
Data handling agreement signed         |             |         | □
```

## Appendix C — Cleanup Verification Record

```
ITEM                                    | VERIFIED BY | DATE    | STATUS
----------------------------------------|-------------|---------|--------
Persistence mechanisms removed          |             |         | □
Uploaded tools deleted                  |             |         | □
Created accounts removed               |             |         | □
Configuration changes reversed         |             |         | □
Scheduled tasks removed                |             |         | □
Web shells removed                     |             |         | □
Firewall rules restored                |             |         | □
C2 channels terminated                 |             |         | □
Credentials securely destroyed         |             |         | □
Evidence encrypted and secured         |             |         | □
Infrastructure decommissioned          |             |         | □
Client confirmation received           |             |         | □
```

---

*This doctrine is a living document. It is reviewed and updated after every engagement cycle. All operators are responsible for knowing the current version and operating within its boundaries. Ignorance of these standards is not a defense for violating them.*

*Version controlled. Distribution restricted to authorized personnel.*