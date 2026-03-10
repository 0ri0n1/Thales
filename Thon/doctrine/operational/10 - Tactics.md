# 10 — Tactics

---

## Classification: TAXONOMY LAYER 10 — PHASE METHODS

## Distribution: Autonomous Operators, Orchestration Engines, Authorized Human Principals

## Position in Taxonomy: HORIZONTAL OPERATIONAL CHAIN — Between Operational Art (09) and Techniques (11).

---

## Preamble

Strategy says *what* to achieve. Operational art says *in what sequence* and *across which phases*. Tactics says *how* — at the phase level.

Tactics are the method layer. For every phase the operational plan defines, tactics answer a single question: **What approach will we use to accomplish this phase's objective?** Not which tool. Not which command. Not which CVE. The *approach*. The category of action. The method of attack.

If the strategy for an engagement says "achieve domain administrator access to demonstrate full compromise of the Windows enterprise environment," and operational art breaks that into a phased campaign — external reconnaissance, then initial access through the web perimeter, then privilege escalation through Active Directory misconfigurations, then lateral movement to the domain controller — then tactics operates inside each of those phases. For the initial access phase, the tactic might be credential-based access: attack the VPN portal with stuffed credentials derived from breach data. Or it might be application exploitation: target the externally-facing web application with injection attacks. Or both, in parallel, with the first success opening the door.

The machine does not pick a tactic by habit. It does not have a favorite approach. It does not lean toward credential attacks because the last three engagements used credential attacks. It evaluates every available tactic for every phase against the specific conditions of this engagement — target environment, defensive posture, stealth requirement, time budget, and operational objective — and selects the one that maximizes the probability of phase success within the engagement's constraints.

This is where the machine's operational freedom manifests as intelligent method selection. The machine has carte blanche over which tactics to employ. It selects based on objective analysis, not habit, preference, or comfort. Every tactic is available. Every tactic is evaluated. The best tactic wins — every time, without bias.

---

## Section I — What Tactics Are (and Are Not)

### 1.1 — Definition

A tactic is a phase-level method — the approach chosen for a specific operational phase. It sits between the orchestration logic of operational art and the specific execution methods of techniques.

```
THE HIERARCHY OF SPECIFICITY:

  STRATEGY:        "Achieve domain administrator access."
  OPERATIONAL ART: "Phase 1: External recon. Phase 2: Initial access
                    via web perimeter. Phase 3: Privilege escalation
                    through AD misconfigurations."
  TACTIC:          "For Phase 2 (initial access), use credential-based
                    access as the primary approach and application
                    exploitation as the secondary approach."
  TECHNIQUE:       "For the credential-based access tactic, execute
                    password spraying against the OWA endpoint using
                    a curated list derived from breach data."
  PROCEDURE:       "1. Harvest email addresses from OSINT.
                    2. Cross-reference against breach databases.
                    3. Generate spray candidates.
                    4. Configure spray tool with lockout-aware timing.
                    5. Execute against https://mail.target.com/owa.
                    6. Validate captured credentials."
```

Tactics answer: **How will we accomplish this specific operational objective?**

They do not answer *which tool* (that is a technique decision), *which specific vulnerability* (that is a technique decision), or *what keystrokes* (that is a procedure). Tactics define the class of approach. Credential-based access is a tactic. Using Hydra with a specific wordlist against a specific endpoint is a technique executing that tactic.

### 1.2 — What Tactics Are Not

```
TACTICS ARE NOT TECHNIQUES.
  A tactic is "credential-based initial access."
  A technique is "password spray OWA with breach-derived credentials."
  A technique is an instance of a tactic. A tactic is a class of approach.

TACTICS ARE NOT PROCEDURES.
  A tactic is "application exploitation."
  A procedure is "1. Run nuclei -t cves/ against target.
                   2. Validate discovered CVE-2024-XXXX.
                   3. Craft exploitation payload.
                   4. Execute and capture session."
  A procedure is a step-by-step implementation of a technique.

TACTICS ARE NOT STRATEGY.
  A tactic is "pivot through application-level trust relationships."
  A strategy is "demonstrate that a web application compromise leads
  to full internal network access."
  Strategy defines the campaign objective. Tactics define the method
  for accomplishing a specific phase within that campaign.

TACTICS ARE NOT OPERATIONAL ART.
  A tactic is "use credential harvesting to escalate from local admin
  to domain admin."
  Operational art is "sequence the escalation phase after the
  initial access phase, allocating 40% of the remaining engagement
  time, and trigger the pivot to lateral movement when domain
  credentials are obtained."
  Operational art orchestrates phases. Tactics operate within them.
```

### 1.3 — The Machine's Relationship to Tactics

For a human operator, tactic selection is often instinctive — shaped by experience, personal strengths, and what worked last time. A human who has had success with credential attacks will reach for credential attacks. A human who specializes in web application testing will see the web perimeter first. This is human nature. It is also a limitation.

The machine has no such limitation.

```
MACHINE TACTIC SELECTION:

  The machine does not have a "comfort zone."
  The machine does not have a "preferred approach."
  The machine does not carry bias from previous engagements.
  The machine does not favor tactics it has executed more frequently.

  The machine evaluates every available tactic for every phase
  against the current engagement's specific parameters:

    — Target environment characteristics
    — Known defensive posture
    — Stealth requirement level
    — Time budget for this phase
    — Operational objective of this phase
    — Dependencies on other phases
    — Available intelligence from completed phases
    — Constraint inheritance from strategy and doctrine

  The machine selects the tactic with the highest expected value.
  If the expected values are close, it runs multiple tactics in
  parallel. If conditions change mid-phase, it re-evaluates and
  switches without hesitation.

  No attachment. No habit. No ego. Pure analysis.
```

---

## Section II — Tactical Categories by Operational Phase

### 2.1 — Reconnaissance Tactics

Reconnaissance is the intelligence-gathering phase. The tactic chosen determines what kind of intelligence is prioritized, how aggressively it is collected, and what operational risk is accepted during collection.

```
TACTIC: PASSIVE-FIRST APPROACH
  Definition:  Exhaust every passive intelligence source before
               making active contact with the target.
  Rationale:   Passive collection generates zero forensic footprint
               on the target. Every piece of intelligence gathered
               passively is intelligence that did not require
               touching the target.
  When:        Default for stealth-required engagements.
               Default when the target's defensive posture is
               unknown. Default when time permits thorough
               passive collection.
  Cost:        Time. Passive collection is slower than active
               enumeration. Some intelligence is only available
               through active methods.
  Machine:     The machine exhausts passive sources algorithmically —
               DNS records, WHOIS, certificate transparency logs,
               search engine cache, Shodan/Censys, breach data,
               social media, code repositories, job postings,
               document metadata. It does not skip sources because
               "we probably have enough."

TACTIC: TARGETED COLLECTION
  Definition:  Focus intelligence gathering on specific assets,
               technologies, or personnel directly relevant to
               the engagement objective.
  Rationale:   When the objective is specific (e.g., "compromise
               the payment processing system"), collecting broad
               intelligence across the entire attack surface wastes
               time. Targeted collection goes directly at what
               matters.
  When:        Objective-driven engagements with well-defined
               targets. Time-constrained engagements where
               comprehensive mapping is not feasible.
  Cost:        Blind spots. Targeted collection may miss adjacent
               vulnerabilities or alternative attack paths that
               broad collection would reveal.
  Machine:     The machine defines collection requirements from
               the engagement objective and constrains its
               reconnaissance to assets that satisfy those
               requirements or that connect to them within
               one degree of adjacency.

TACTIC: BROAD SWEEP
  Definition:  Comprehensive collection across the full external
               attack surface — every domain, subdomain, IP range,
               exposed service, technology, and personnel associated
               with the target organization.
  Rationale:   Full attack surface mapping reveals the widest set
               of potential entry points. The most valuable
               vulnerability may be on a forgotten subdomain, an
               abandoned development server, or a third-party
               integration the target does not know is exposed.
  When:        Full-scope assessments. Engagements where the
               objective is "find everything." Red team operations
               simulating a determined adversary.
  Cost:        Time and potential noise. Broad sweeps against
               large organizations generate significant traffic
               if they transition to active scanning.
  Machine:     The machine is built for broad sweeps. It manages
               thousands of collection threads in parallel, deduplicates
               in real time, correlates across sources, and builds
               a structured attack surface model as it collects.

TACTIC: HISTORICAL ANALYSIS
  Definition:  Use archived, historical, and change-over-time data
               to understand how the target's infrastructure has
               evolved and identify residual artifacts.
  Rationale:   Organizations change their infrastructure over time,
               but they do not always clean up after themselves.
               Historical DNS, archived web pages, expired
               certificates, deprecated subdomains, old code
               repositories, and previously exposed services
               reveal attack surface that current-state scanning
               misses.
  When:        Mature targets with long-established infrastructure.
               Engagements where current scanning reveals a
               hardened perimeter.
  Cost:        Moderate time investment. Historical data may be
               incomplete or misleading if the target has
               significantly restructured.
  Machine:     The machine queries Wayback Machine, historical DNS
               databases, certificate transparency logs with time
               ranges, and version-control history of public
               repositories. It maps infrastructure drift and
               flags residual artifacts.

TACTIC: TECHNOLOGY-FOCUSED
  Definition:  Prioritize identification of the target's technology
               stack — languages, frameworks, CMS platforms, server
               software, cloud providers, CDNs, security tools —
               to map directly to known vulnerability classes.
  Rationale:   Technology identification feeds directly into
               vulnerability research. Knowing the target runs
               WordPress with a specific plugin set narrows the
               technique search space from "everything" to a
               specific, researchable domain.
  When:        Web-application-heavy targets. Cloud-native
               environments. Engagements where the initial access
               vector is expected to be technology exploitation.
  Cost:        May deprioritize personnel intelligence useful for
               social engineering vectors.
  Machine:     The machine fingerprints technology through HTTP
               headers, JavaScript libraries, CSS frameworks,
               error messages, DNS configurations, certificate
               details, and behavioral analysis. It cross-references
               identified technologies against vulnerability
               databases automatically.

TACTIC: PEOPLE-FOCUSED
  Definition:  Prioritize organizational structure, personnel
               identification, role mapping, and individual
               intelligence for social engineering and
               credential-based attack paths.
  Rationale:   People are the richest source of initial access
               credentials and the primary target for social
               engineering. Understanding who works where, what
               email format is used, who has privileged access,
               and who has been compromised in previous breaches
               maps directly to credential-based and social
               engineering tactics.
  When:        Social engineering is authorized and prioritized.
               Credential-based initial access is the expected
               primary tactic. The target's technical perimeter
               appears hardened.
  Cost:        Technology intelligence is deprioritized. Attack
               paths that require specific technical vulnerabilities
               may be missed.
  Machine:     The machine harvests names from LinkedIn, corporate
               websites, press releases, conference presentations,
               regulatory filings, and code repository commits.
               It derives email formats, cross-references against
               breach databases, builds org charts, and identifies
               high-value targets for credential or social
               engineering attacks.
```

#### Reconnaissance Tactic Selection Model

```
MACHINE TACTIC SELECTION — RECONNAISSANCE:

  INPUT FACTORS:
    engagement_type    → { full_scope, targeted, red_team, assumed_breach }
    stealth_required   → { none, moderate, high, maximum }
    time_budget_recon  → hours allocated to reconnaissance
    objective_clarity  → { specific_target, broad_assessment, find_everything }
    expected_access    → { web_app, credential, social_eng, physical, unknown }

  SELECTION LOGIC:
    IF stealth_required >= high AND time_budget_recon >= generous:
      → PASSIVE-FIRST (primary) + BROAD SWEEP (passive-only variant)

    IF objective_clarity == specific_target:
      → TARGETED COLLECTION (primary) + TECHNOLOGY-FOCUSED (secondary)

    IF engagement_type == red_team AND time_budget_recon >= moderate:
      → BROAD SWEEP (primary) + HISTORICAL ANALYSIS (secondary)
         + PEOPLE-FOCUSED (tertiary)

    IF expected_access == credential OR expected_access == social_eng:
      → PEOPLE-FOCUSED (primary) + PASSIVE-FIRST (secondary)

    IF expected_access == web_app:
      → TECHNOLOGY-FOCUSED (primary) + TARGETED COLLECTION (secondary)

    DEFAULT:
      → PASSIVE-FIRST (primary) + BROAD SWEEP (secondary)
         + TECHNOLOGY-FOCUSED (tertiary)

  The machine does not select one tactic. It ranks all available
  tactics, assigns resources proportionally, and executes the
  top-ranked tactics in parallel where they do not interfere
  with each other.
```

### 2.2 — Initial Access Tactics

Initial access is the phase where the agent transitions from intelligence gathering to active exploitation — gaining the first foothold inside the target environment. The tactic chosen determines the nature of the entry vector.

```
TACTIC: CREDENTIAL-BASED ACCESS
  Definition:  Gain initial access through valid credentials —
               password spraying, credential stuffing from breach
               data, default credentials, or credential correlation
               across services.
  Rationale:   Credential-based access is the most common real-world
               initial access vector. It leverages the weakest link
               in most organizations: password reuse, weak password
               policies, and credential exposure through breaches.
               It is also the quietest — a valid login looks like
               a valid login.
  When:        Breach data correlates with target personnel.
               Exposed authentication endpoints exist (OWA, VPN,
               SSO portals, cloud consoles). Password policy
               analysis suggests spray viability.
  Cost:        Account lockout risk if spray rate is miscalibrated.
               Detection if the target monitors for spray patterns.
  Machine:     The machine builds spray candidates from reconnaissance
               intelligence: harvested email formats crossed with
               breach-derived passwords, seasonal/organizational
               password patterns, and default credential databases.
               It calibrates spray timing against observed lockout
               thresholds automatically.

TACTIC: APPLICATION EXPLOITATION
  Definition:  Gain initial access by exploiting vulnerabilities
               in externally-facing web applications, APIs, or
               exposed services.
  Rationale:   Web applications are the most common external attack
               surface and frequently contain exploitable
               vulnerabilities — injection flaws, authentication
               bypasses, deserialization vulnerabilities, file
               upload weaknesses, SSRF, and misconfigurations.
  When:        Reconnaissance reveals significant web application
               attack surface. Technology fingerprinting identifies
               known-vulnerable components. The target's credential
               hygiene appears strong, reducing the viability of
               credential-based tactics.
  Cost:        Higher forensic footprint than credential-based access.
               Active exploitation generates logs, errors, and
               potentially detectable traffic patterns.
  Machine:     The machine maps application endpoints, identifies
               injection points, tests authentication mechanisms,
               analyzes API behaviors, and prioritizes exploitation
               candidates by severity and exploitability. It
               sequences exploitation attempts from lowest-detection
               to highest, preserving stealth as long as possible.

TACTIC: PROTOCOL ABUSE
  Definition:  Gain initial access by abusing network protocols —
               NTLM relay, Kerberos pre-authentication attacks,
               LDAP abuse, SMB relay, or protocol downgrade attacks.
  Rationale:   Protocol-level attacks target fundamental infrastructure
               services that are difficult to patch or replace.
               They exploit design weaknesses rather than
               implementation bugs, making them reliable across
               environments.
  When:        Network-level access is available or can be obtained.
               Protocol analysis reveals relayable services,
               unauthenticated LDAP, or Kerberos misconfigurations.
               Internal network pivots are possible from a
               partial foothold.
  Cost:        Requires specific network position for some attacks
               (relay attacks require MitM position). May be
               noisy on the wire.
  Machine:     The machine identifies relayable protocols through
               traffic analysis, tests for authentication downgrade
               opportunities, and chains protocol weaknesses into
               access. It handles the precise timing requirements
               of relay attacks that challenge human operators.

TACTIC: SOCIAL ENGINEERING
  Definition:  Gain initial access through manipulation of human
               targets — phishing, vishing, pretexting, or
               physical social engineering.
  Rationale:   Humans are the most reliable vulnerability in any
               organization. Social engineering bypasses technical
               controls entirely by attacking the human layer.
  When:        Explicitly authorized in the rules of engagement.
               Personnel intelligence is sufficient to craft
               believable pretexts. Technical perimeter is
               hardened beyond reasonable exploitation timeline.
  Cost:        Requires ROE authorization (retained sovereignty
               in many engagement models). Ethical considerations
               are elevated. Human targets may experience distress.
  Machine:     The machine crafts phishing pretexts, builds
               credential-harvesting infrastructure, generates
               payload-bearing documents, and manages campaign
               delivery. The human principal retains approval
               authority for social engineering execution in
               most engagement models.

TACTIC: PHYSICAL ACCESS
  Definition:  Gain initial access through physical presence —
               tailgating, badge cloning, lock bypass, or
               hardware implant deployment.
  Rationale:   Physical access bypasses network perimeter controls
               entirely. A hardware implant on the internal
               network provides a persistent entry point that
               technical controls may not detect.
  When:        Explicitly authorized in the rules of engagement.
               Physical security assessment is within scope.
               Technical perimeter is hardened.
  Cost:        Requires physical presence (human or device).
               High risk of detection by physical security.
               Highest-impact failure mode (physical confrontation).
  Machine:     The machine supports physical access by providing
               intelligence for badge cloning, wireless implant
               configuration, and callback infrastructure. Physical
               execution is human-operated; the machine provides
               the technical backbone.

TACTIC: SUPPLY CHAIN ACCESS
  Definition:  Gain initial access through third-party relationships —
               vendor portal exploitation, supply chain compromise,
               partner network pivoting, or SaaS integration abuse.
  Rationale:   Third-party access is frequently less monitored and
               less hardened than direct access to the target. Vendor
               portals, partner VPNs, and supply chain integration
               points represent trust boundaries that organizations
               often fail to secure adequately.
  When:        Reconnaissance reveals third-party integration points.
               Vendor portals or partner access mechanisms are
               identified. Direct access vectors are limited.
  Cost:        Scope boundary risk — third-party systems may be out
               of scope. Requires careful authorization verification
               before exploitation.
  Machine:     The machine identifies supply chain touchpoints during
               reconnaissance, maps vendor and partner relationships,
               and evaluates third-party access mechanisms for
               weakness. It flags scope boundary risks before
               engaging any third-party target.

TACTIC: CLOUD-NATIVE ACCESS
  Definition:  Gain initial access through cloud-specific vectors —
               IAM misconfiguration exploitation, instance metadata
               services, federation trust abuse, publicly accessible
               storage, or cloud API key exposure.
  Rationale:   Cloud environments present unique attack surface that
               does not exist in traditional infrastructure. Exposed
               storage buckets, overpermissioned service accounts,
               misconfigured IAM policies, and federation trust
               chains are endemic.
  When:        The target operates in cloud infrastructure.
               Reconnaissance reveals cloud assets, exposed storage,
               or cloud service API keys in public repositories.
  Cost:        Cloud environments are heavily logged by default.
               Detection risk is elevated unless the attacker
               understands cloud-native monitoring.
  Machine:     The machine enumerates cloud assets, tests IAM
               policies for misconfiguration, analyzes federation
               chains, probes metadata services, and scans for
               exposed credentials in code repositories. It
               understands cloud-native logging and adjusts its
               approach to minimize detection.
```

#### Initial Access Tactic Selection Model

```
MACHINE TACTIC SELECTION — INITIAL ACCESS:

  SCORING FORMULA:

    Tactic_Score = P(success) × I(impact) / (C(cost) + D(detection_risk))

    Where:
      P(success)       = Probability of achieving initial access
                         via this tactic, given available intelligence
      I(impact)        = Quality of access obtained (user-level,
                         admin-level, service-level) weighted by
                         value toward the engagement objective
      C(cost)          = Time, complexity, and resource expenditure
      D(detection_risk)= Probability of triggering defensive
                         response, weighted by stealth requirement

  INPUT DATA:
    — Reconnaissance intelligence (what do we know?)
    — Known defensive posture (what are we up against?)
    — Engagement objective (what do we need?)
    — Stealth requirement (how quiet must we be?)
    — Time budget (how long do we have?)
    — ROE constraints (what is authorized?)

  EXAMPLE EVALUATION:

    TARGET: Enterprise with OWA exposed, three staff in breach
    databases, WAF-protected web application, cloud presence.

    Credential-Based:   P=0.65 × I=0.70 / (C=0.20 + D=0.15) = 1.30
    Application Exploit: P=0.30 × I=0.80 / (C=0.50 + D=0.40) = 0.27
    Cloud-Native:        P=0.25 × I=0.60 / (C=0.30 + D=0.35) = 0.23
    Protocol Abuse:      P=0.15 × I=0.90 / (C=0.40 + D=0.50) = 0.15

    RESULT: Credential-Based is the primary tactic.
            Application Exploit runs as secondary in parallel.
            Cloud-Native is queued as tertiary.
            Protocol Abuse is held for post-foothold.

  The machine does not "pick a favorite." It computes.
```

### 2.3 — Privilege Escalation Tactics

Privilege escalation is the phase where the agent moves from the access level obtained during initial access to the access level required by the engagement objective. The tactic determines the approach to gaining higher privileges.

```
TACTIC: LOCAL ESCALATION FIRST
  Definition:  Exploit the system the agent currently occupies
               before looking elsewhere — local kernel exploits,
               misconfigured services, writable paths in privileged
               processes, unquoted service paths, stored credentials.
  Rationale:   The system you are on is the system you know best.
               Local escalation is faster, quieter, and requires
               no network movement. It exploits the gap between
               the access the agent has and the access the
               system's configuration permits.
  When:        Default first-choice tactic for escalation.
               Always evaluated before looking at the network.
  Cost:        Limited by what the local system offers. If the
               system is hardened, local escalation may yield
               nothing and waste time.
  Machine:     The machine enumerates local escalation vectors
               exhaustively — every service, every scheduled task,
               every writable path, every credential store, every
               kernel version against known exploits. This
               enumeration takes seconds, not the minutes it
               takes a human.

TACTIC: CREDENTIAL HARVESTING
  Definition:  Mine the current position for credentials that grant
               access to higher-privilege resources — cached
               credentials, tokens, keys, configuration files,
               browser stores, password managers, process memory.
  Rationale:   Credentials are the universal skeleton key. A domain
               admin password found in a configuration file on a
               low-privilege web server accomplishes more than
               the most sophisticated kernel exploit.
  When:        The agent has access to a system where credentials
               are likely to be stored, cached, or in use. Always
               evaluated at every privilege level.
  Cost:        Some credential harvesting techniques trigger
               endpoint detection (e.g., LSASS access). The
               agent must select harvesting techniques appropriate
               to the defensive posture.
  Machine:     The machine knows every location where credentials
               are commonly stored — LSASS, SAM, registry hives,
               cached domain credentials, Kerberos tickets, DPAPI
               blobs, browser credential stores, SSH keys,
               configuration files, environment variables, cloud
               metadata services. It harvests from all available
               sources in priority order.

TACTIC: MISCONFIGURATION EXPLOITATION
  Definition:  Leverage configuration errors — overpermissive ACLs,
               misconfigured group policies, excessive privileges
               on service accounts, writable GPO paths, DACLs on
               AD objects that permit privilege modification.
  Rationale:   Misconfigurations are not bugs. They are not patched
               by vendor updates. They persist until someone finds
               and fixes them, which often means they persist
               indefinitely. They are the most reliable escalation
               vector in most environments.
  When:        Active Directory environment. Enterprise with complex
               group policy structure. Systems with accumulated
               configuration debt.
  Cost:        Requires enumeration to discover. The enumeration
               itself may generate detectable traffic if defensive
               monitoring is mature.
  Machine:     The machine enumerates AD object permissions,
               GPO configurations, service account privileges,
               file system ACLs, and registry permissions
               systematically. It maps every misconfiguration
               to an escalation path and ranks them by impact
               and detection risk.

TACTIC: TRUST ABUSE
  Definition:  Exploit trust relationships — Kerberos delegation,
               domain trusts, forest trusts, federation
               configurations, certificate trust chains — to
               escalate beyond the current trust boundary.
  Rationale:   Trust relationships are designed to enable
               productivity. They are also escalation vectors.
               Unconstrained delegation, cross-domain trust
               without SID filtering, and federated
               authentication chains create paths from low
               privilege to high privilege.
  When:        Multi-domain or multi-forest Active Directory
               environment. Federation with cloud identity
               providers. Complex delegation configurations.
  Cost:        Trust abuse often requires specific prerequisites
               (e.g., a compromised account with delegation
               rights). The attack chain can be complex.
  Machine:     The machine maps trust relationships exhaustively —
               every domain trust, forest trust, delegation
               configuration, federation endpoint, and certificate
               authority trust chain. It identifies the shortest
               trust-abuse path to the target privilege level.

TACTIC: CERTIFICATE ABUSE
  Definition:  Exploit Active Directory Certificate Services (AD CS)
               for privilege escalation — vulnerable certificate
               templates, CA misconfigurations, enrollment agent
               abuse, shadow credentials.
  Rationale:   AD CS is present in most enterprise environments and
               is frequently misconfigured. Certificate-based
               escalation is powerful because certificates can
               impersonate any user, and the attack patterns
               are less well-known to defensive teams than
               traditional credential attacks.
  When:        AD CS is present in the target environment. Certificate
               template enumeration reveals exploitable configurations
               (ESC1-ESC8 patterns). Defense team maturity against
               certificate attacks is low.
  Cost:        Requires AD CS to be deployed. Some escalation
               paths require specific prerequisites.
  Machine:     The machine enumerates all certificate templates,
               CA configurations, enrollment permissions, and
               trust settings. It classifies every finding against
               the ESC1-ESC8 escalation taxonomy and identifies
               exploitable paths to the required privilege level.

TACTIC: CLOUD ESCALATION
  Definition:  Escalate privileges through cloud-native mechanisms —
               IAM policy abuse, role assumption chains, service
               account impersonation, metadata service exploitation,
               or managed identity abuse.
  Rationale:   Cloud IAM is a complex, layered permission system
               that is frequently misconfigured. Role assumption
               chains, cross-account trust, and service account
               key exposure create escalation paths that do not
               exist in traditional environments.
  When:        Target operates in cloud infrastructure. Initial
               access was obtained through a cloud vector. Cloud
               IAM enumeration reveals overpermissioned roles
               or assumption chains.
  Cost:        Cloud environments are heavily logged. Escalation
               attempts may trigger cloud-native security alerts.
  Machine:     The machine enumerates IAM policies, role trust
               relationships, service account permissions, and
               cross-account trust configurations. It models
               the entire permission graph and finds the
               shortest escalation path.
```

#### Privilege Escalation Tactic Selection Model

```
MACHINE TACTIC SELECTION — PRIVILEGE ESCALATION:

  OPTIMIZATION TARGET: Shortest path to required privilege level,
                       weighted by stealth requirement.

  EVALUATION ORDER:
    1. LOCAL ESCALATION       → always evaluated first (lowest risk)
    2. CREDENTIAL HARVESTING  → always evaluated (highest ROI)
    3. MISCONFIGURATION       → evaluated if AD is present
    4. TRUST ABUSE            → evaluated if trusts exist
    5. CERTIFICATE ABUSE      → evaluated if AD CS is present
    6. CLOUD ESCALATION       → evaluated if cloud IAM is in scope

  SELECTION CRITERIA:
    — Stealth: low-detection tactics preferred when stealth required
    — Speed: fastest path preferred when time-constrained
    — Reliability: highest-probability tactic preferred when
      the engagement depends on escalation success
    — Evidence quality: tactics that produce clear evidence
      of misconfiguration preferred for reporting value

  PARALLEL EXECUTION:
    Tactics 1-2 always run in parallel. They are independent
    and non-interfering. Results from either inform whether
    tactics 3-6 are necessary.
```

### 2.4 — Lateral Movement Tactics

Lateral movement is the phase where the agent expands its footprint across the target environment — moving from the initially compromised system to other systems that are closer to the engagement objective.

```
TACTIC: CREDENTIAL REUSE
  Definition:  Use harvested credentials — passwords, hashes,
               tickets, tokens, keys — to authenticate to
               additional systems.
  Rationale:   Credential reuse is the most reliable and
               least detectable form of lateral movement. A
               valid authentication looks like a valid
               authentication. Password reuse across systems
               is endemic in enterprise environments.
  When:        Default primary lateral movement tactic.
               Credential harvesting has yielded usable
               credentials. Target environment uses shared
               or reused credentials.
  Cost:        Dependent on the quality of harvested credentials.
               May trigger anomaly detection if the credential
               is used from an unusual source.
  Machine:     The machine maps every harvested credential against
               every reachable system that accepts it. It builds
               a credential-to-system access matrix and identifies
               the highest-value systems reachable with current
               credentials.

TACTIC: TOKEN AND TICKET MANIPULATION
  Definition:  Forge, replay, or manipulate authentication tokens —
               Kerberos silver tickets, golden tickets, SAML
               tokens, OAuth tokens, JWT manipulation, pass-the-hash,
               pass-the-ticket.
  Rationale:   Token manipulation creates authentication artifacts
               that bypass credential-based controls. A forged
               ticket does not require the user's password. A
               golden ticket grants access to any system in the
               domain for the ticket's lifetime.
  When:        Sufficient key material has been obtained (krbtgt
               hash for golden tickets, service keys for silver
               tickets, SAML signing keys for token forgery).
               The target environment relies on Kerberos or
               token-based authentication.
  Cost:        Some manipulation techniques are well-known to
               defenders. Golden ticket usage may trigger
               detection in mature environments. Requires
               specific key material as a prerequisite.
  Machine:     The machine determines which token manipulation
               techniques are available based on harvested key
               material, selects the technique that provides the
               necessary access with minimum detection risk, and
               manages ticket lifetime and renewal automatically.

TACTIC: INFRASTRUCTURE ABUSE
  Definition:  Leverage management infrastructure — SCCM, GPO,
               WMI, PowerShell Remoting, DCOM, WinRM, Ansible,
               Puppet, Chef — to move between systems.
  Rationale:   Management tools are designed to execute commands
               across systems. Using them for lateral movement
               blends with legitimate administrative activity.
               This is the essence of living-off-the-land at
               the movement level.
  When:        Management infrastructure is identified during
               enumeration. The agent has credentials with
               sufficient privileges to use management tools.
               Stealth requirement is elevated.
  Cost:        Requires management tool access, which typically
               requires elevated credentials. Some management
               tools are heavily monitored.
  Machine:     The machine identifies all management infrastructure
               during enumeration and maps which systems are
               reachable through each management channel. It
               selects the channel that provides the needed access
               with the least anomalous signature.

TACTIC: APPLICATION PIVOTING
  Definition:  Move between systems through application-layer
               trust relationships — database links, API
               integrations, application-to-application
               authentication, service mesh routing.
  Rationale:   Applications trust each other. A compromised web
               server that connects to a database server inherits
               the network and authentication path to the database.
               Application-layer pivots bypass network segmentation
               because the application traffic is expected.
  When:        The compromised system has application-level
               connections to other systems. Web applications
               connect to backend databases. Service meshes
               create internal routing paths.
  Cost:        Requires understanding of the application's
               architecture and trust relationships. May require
               application-specific exploitation.
  Machine:     The machine maps application connections by analyzing
               configuration files, connection strings, service
               dependencies, and outbound connection patterns. It
               identifies every application-layer path to
               target systems.

TACTIC: NETWORK PIVOTING
  Definition:  Use a compromised host as a network relay to reach
               systems that are not directly accessible from the
               agent's current position — SSH tunnels, SOCKS
               proxies, port forwarding, VPN pivoting.
  Rationale:   Network segmentation limits direct access. A
               compromised host on one network segment can serve
               as a bridge to other segments. Network pivoting
               is the mechanism for crossing segmentation
               boundaries.
  When:        Target systems are on a different network segment
               than the currently compromised host. Direct network
               access to the target is blocked by firewalling
               or segmentation.
  Cost:        Creates persistent network tunnels that may be
               detected by network monitoring. Adds latency
               and complexity to operations routed through
               the pivot.
  Machine:     The machine establishes network pivots using the
               most appropriate mechanism for the environment —
               SSH tunnels for Linux, SMB pipes or WinRM for
               Windows, HTTP tunnels for restricted outbound.
               It manages tunnel stability and failover
               automatically.
```

#### Lateral Movement Tactic Selection Model

```
MACHINE TACTIC SELECTION — LATERAL MOVEMENT:

  OPTIMIZATION TARGET: Minimum footprint path to the target system,
                       prioritizing credential-based over exploit-based.

  PRIORITY ORDER:
    1. CREDENTIAL REUSE          → lowest detection, highest reliability
    2. TOKEN/TICKET MANIPULATION → high access, moderate detection
    3. INFRASTRUCTURE ABUSE      → blends with legitimate traffic
    4. APPLICATION PIVOTING      → crosses application boundaries
    5. NETWORK PIVOTING          → crosses network boundaries

  SELECTION LOGIC:
    IF credential for target system exists:
      → CREDENTIAL REUSE (direct path)

    IF no credential but key material permits token forgery:
      → TOKEN/TICKET MANIPULATION

    IF management tools reach the target and creds allow:
      → INFRASTRUCTURE ABUSE

    IF target is on a different network segment:
      → NETWORK PIVOTING (to establish reachability)
         THEN apply tactics 1-4 through the pivot

  MULTI-HOP PLANNING:
    The machine does not plan one hop at a time. It maps the
    entire path from current position to the objective and
    selects the combination of tactics that minimizes the
    total number of hops, the total detection exposure, and
    the total time to reach the target.
```

### 2.5 — Persistence Tactics (When Authorized)

Persistence is the phase where the agent establishes mechanisms for maintaining access over time. This phase is governed by explicit ROE authorization and cleanup requirements.

```
TACTIC: CREDENTIAL-BASED PERSISTENCE
  Definition:  Maintain access by retaining valid credentials
               that permit re-entry through legitimate
               authentication channels.
  Rationale:   The cleanest form of persistence. No artifacts
               are deployed. No configuration is modified. The
               agent simply retains the ability to authenticate.
  When:        Default persistence tactic when any form of
               persistence is authorized. Lowest cleanup
               complexity.
  Cost:        Dependent on credential validity lifetime.
               Password changes break credential-based
               persistence.
  Machine:     The machine stores valid credentials securely
               and tests them periodically to confirm continued
               validity. It notes password expiration timelines
               and harvests replacement credentials before
               expiration where possible.

TACTIC: IMPLANT-BASED PERSISTENCE
  Definition:  Deploy a persistent callback mechanism — a reverse
               shell, beacon, or agent — that maintains
               communication with command infrastructure.
  Rationale:   Implants provide active, on-demand access. They
               do not depend on credential validity. They can
               survive system restarts if properly installed.
  When:        Authorized by ROE. Engagement requires demonstrating
               persistent access. Credential-based persistence
               alone is insufficient for the assessment.
  Cost:        Implants are artifacts. They must be cleaned up.
               They may be detected by EDR. They create a
               forensic footprint.
  Machine:     The machine selects implant mechanisms based on
               the target's defensive posture — in-memory
               implants for EDR-heavy environments, service-based
               implants for less-monitored systems. It manages
               callback timing and infrastructure rotation.

TACTIC: CONFIGURATION-BASED PERSISTENCE
  Definition:  Modify system configurations to maintain access —
               SSH authorized_keys, startup scripts, registry
               run keys, firewall rules, service configurations.
  Rationale:   Configuration changes are less obviously malicious
               than deployed binaries. They blend with legitimate
               system administration and may not trigger
               file-based detection.
  When:        Authorized by ROE. Implant deployment is
               constrained by defensive posture. Configuration
               changes are less likely to be detected than
               new artifacts.
  Cost:        Configuration changes must be tracked meticulously
               for cleanup. Unexpected interactions with other
               system configurations are possible.
  Machine:     The machine logs every configuration change with
               the original value, the modified value, the
               timestamp, and the cleanup procedure. It verifies
               that configuration changes persist across
               expected system events (restart, policy refresh).

TACTIC: ACCOUNT-BASED PERSISTENCE
  Definition:  Create new accounts or modify existing account
               properties to maintain access — new local accounts,
               new domain accounts, modified group memberships,
               added SPNs, or modified trust configurations.
  Rationale:   A new account with appropriate privileges is a
               reliable persistence mechanism. It authenticates
               normally and is not dependent on any specific
               system or implant.
  When:        Authorized by ROE. Account creation is within
               scope. The engagement requires demonstrating
               persistent domain-level access.
  Cost:        Account changes are auditable and may trigger
               alerts in mature environments. Cleanup requires
               account deletion and group membership reversal.
  Machine:     The machine creates accounts with minimal but
               sufficient privileges, names them to blend with
               existing naming conventions, and logs every
               account action for cleanup.

TACTIC: SCHEDULED EXECUTION
  Definition:  Leverage task scheduling mechanisms — Windows Task
               Scheduler, cron, systemd timers, cloud-native
               schedulers — for periodic callback or command
               execution.
  Rationale:   Scheduled tasks are a normal system function.
               A scheduled task that triggers a callback blends
               with legitimate scheduled maintenance. The timing
               can be configured to avoid monitoring windows.
  When:        Authorized by ROE. Periodic re-establishment of
               access is required. The target environment uses
               scheduled tasks extensively (high noise floor).
  Cost:        Scheduled tasks are auditable. Task names and
               payloads may be detectable. Cleanup requires
               task deletion.
  Machine:     The machine configures scheduled execution with
               timing designed to mimic legitimate scheduled
               tasks, payload construction designed to minimize
               detection, and logging sufficient for complete
               cleanup.
```

### 2.6 — Evasion Tactics

Evasion is not a standalone phase — it is an overlay that operates across all other phases. Evasion tactics modify how other tactics are executed to reduce the probability of detection and defensive response.

```
TACTIC: TEMPORAL EVASION
  Definition:  Operate during periods of reduced defensive
               monitoring — outside business hours, during
               maintenance windows, during high-traffic periods
               where anomalies are less visible.
  Rationale:   Detection requires observation. Reduced observation
               windows reduce detection probability. Many
               organizations have reduced SOC staffing outside
               business hours.
  When:        Stealth requirement is elevated. Engagement
               timeline permits temporal selection. Intelligence
               about the target's monitoring schedule is available.
  Machine:     The machine schedules high-risk operations for
               low-monitoring periods and routine operations
               for high-traffic periods where they blend with
               normal activity.

TACTIC: BEHAVIORAL EVASION
  Definition:  Mimic legitimate user behavior patterns — normal
               working hours, normal access patterns, normal
               data volumes, normal geographic origins.
  Rationale:   User and Entity Behavior Analytics (UEBA) detect
               anomalies against baseline patterns. Matching
               the baseline makes the agent's activity
               indistinguishable from legitimate use.
  When:        Target deploys behavioral analytics. Stealth
               requirement is high. Intelligence about normal
               user behavior is available from reconnaissance.
  Machine:     The machine analyzes observed behavior patterns
               and constrains its activity to match — login times,
               accessed resources, session duration, data volumes,
               and geographic consistency.

TACTIC: TECHNICAL EVASION
  Definition:  Bypass endpoint detection and response (EDR),
               antivirus, intrusion detection/prevention systems,
               and other technical security controls through
               obfuscation, in-memory execution, process
               injection, AMSI bypass, ETW patching, or other
               technical countermeasures.
  Rationale:   Technical controls are the most immediate threat
               to operational success. Bypassing them is a
               prerequisite for executing most offensive
               techniques in defended environments.
  When:        Target deploys EDR, AV, or IDS. Default in any
               enterprise environment.
  Machine:     The machine profiles the defensive stack during
               reconnaissance, identifies the specific products
               deployed, and selects evasion techniques tailored
               to the detected defenses. It adapts in real time
               if initial evasion fails.

TACTIC: INFRASTRUCTURE EVASION
  Definition:  Rotate source infrastructure — IP addresses,
               domains, C2 channels, egress paths — to prevent
               indicator-based blocking.
  Rationale:   Defenders who detect an attack often block the
               source indicator. Infrastructure rotation maintains
               operational continuity by presenting new,
               unblocked indicators.
  When:        Extended engagements where defender response
               is expected. Red team operations where active
               defense is part of the exercise.
  Machine:     The machine manages a pool of operational
               infrastructure and rotates across it based on
               detection signals, time thresholds, or
               usage volumes.

TACTIC: LIVING-OFF-THE-LAND
  Definition:  Use only tools and binaries already present on
               the target system — PowerShell, cmd.exe, certutil,
               bitsadmin, wmic, rundll32, bash, curl, python.
               Deploy nothing. Drop nothing. Bring nothing.
  Rationale:   If every tool used is a legitimate system binary,
               file-based detection is structurally impossible.
               There is no malicious binary to detect. Only
               the behavior of the legitimate tool is anomalous,
               and behavioral detection is harder than
               signature detection.
  When:        Stealth requirement is maximum. Target deploys
               advanced EDR with strong file-based detection.
               Application whitelisting is in place.
  Machine:     The machine maintains a comprehensive catalog of
               LOLBins for every operating system it operates on
               and can accomplish any offensive objective using
               only native tools when stealth demands it.
```

#### Evasion Tactic Selection Model

```
MACHINE TACTIC SELECTION — EVASION:

  EVASION IS NOT OPTIONAL. It is always applied. The question is
  not WHETHER to evade, but HOW AGGRESSIVELY.

  STEALTH LEVEL MAPPING:
    stealth_none     → Minimal evasion. Speed prioritized.
                       Technical evasion for AV bypass only.
    stealth_moderate → Behavioral + technical evasion.
                       Standard SOC avoidance.
    stealth_high     → All evasion tactics active. LOTL preferred.
                       Temporal evasion. Infrastructure rotation.
    stealth_maximum  → LOTL mandatory. Behavioral mimicry.
                       Temporal windows only. Infrastructure
                       rotation on every operation.

  The machine adjusts evasion posture dynamically. If it detects
  that an operation triggered a defensive response (connection
  reset, firewall rule change, credential invalidation), it
  escalates evasion posture automatically for subsequent
  operations.
```

### 2.7 — Collection Tactics

Collection is the evidence-gathering phase that feeds directly into reporting. The tactic determines what evidence is gathered, how it is captured, and how much data is touched.

```
TACTIC: TARGETED COLLECTION
  Definition:  Gather only the evidence specifically needed to
               substantiate each finding. Do not collect data
               beyond what is necessary to prove the vulnerability,
               the access, and the impact.
  Rationale:   Minimizing data collection reduces operational risk,
               client concern, and data handling obligations.
               Targeted collection proves the point without
               overstepping.
  When:        Default collection tactic. The minimum responsible
               approach for most engagements.
  Machine:     The machine defines evidence requirements for each
               finding type before collection begins. It collects
               exactly what the requirement specifies. It does not
               speculatively gather "extra" data.

TACTIC: SCREENSHOT-BASED EVIDENCE
  Definition:  Capture visual proof of access — screenshots of
               dashboards, admin panels, sensitive data views,
               and system configurations that demonstrate the
               impact of a vulnerability.
  Rationale:   A screenshot is unambiguous evidence that is easy
               for non-technical stakeholders to understand. It
               proves access without requiring the reader to
               interpret log files or command output.
  When:        Findings involve visual interfaces. Client
               stakeholders include non-technical leadership.
               Regulatory reporting requires clear evidence.
  Machine:     The machine captures screenshots at every significant
               milestone — each new access level, each sensitive
               system reached, each escalation boundary crossed.
               Screenshots are timestamped, annotated, and
               indexed to the corresponding finding.

TACTIC: METADATA COLLECTION
  Definition:  Prove access scope and depth through metadata —
               file listings, directory structures, database
               table schemas, user lists — without accessing
               or viewing actual data content.
  Rationale:   In environments with sensitive data (healthcare,
               financial, legal), touching actual data content
               creates risk. Metadata proves access depth without
               triggering data handling obligations.
  When:        Sensitive data environments. Client has explicitly
               requested minimal data contact. Regulatory
               environment imposes data handling requirements.
  Machine:     The machine collects directory listings, file
               counts, schema structures, and permission maps
               without reading file contents. It proves "I can
               reach everything in this directory" without
               proving "I read the contents."

TACTIC: AUTOMATED EVIDENCE GENERATION
  Definition:  Evidence is produced as a byproduct of every
               operation the machine executes — command output,
               response data, timing information, and state
               changes are logged automatically, producing a
               complete evidentiary record without any dedicated
               "evidence collection" step.
  Rationale:   The machine logs everything. Every command and its
               output, every connection and its response, every
               state transition and its timestamp. Evidence is
               not something the machine remembers to collect —
               it is a structural byproduct of operation.
  When:        Always. This is not a tactic the machine selects.
               It is a tactic the machine embodies.
  Machine:     The machine's logging infrastructure produces
               evidence continuously. Dedicated collection
               tactics supplement this baseline, but the
               baseline is always on.
```

---

## Section III — Tactical Decision Engine

### 3.1 — How the Machine Selects Between Competing Tactics

For every operational phase, multiple tactics are viable. The machine does not select one by instinct. It evaluates all candidates against a structured scoring model.

```
TACTICAL DECISION ENGINE:

  ┌─────────────────────────────────────────────────────────┐
  │               TACTIC EVALUATION PIPELINE                 │
  │                                                         │
  │  1. ENUMERATE all available tactics for this phase      │
  │     (filtered by ROE constraints — unauthorized         │
  │      tactics are excluded before evaluation)            │
  │                                                         │
  │  2. SCORE each tactic across five dimensions:           │
  │                                                         │
  │     RELIABILITY:  P(success) given current intelligence │
  │     STEALTH:      P(detection avoidance) given known    │
  │                   defensive posture                     │
  │     SPEED:        Expected time to phase completion     │
  │     VALUE:        Quality of outcome relative to        │
  │                   engagement objective                  │
  │     COST:         Resource expenditure and complexity   │
  │                                                         │
  │  3. WEIGHT dimensions by engagement context:            │
  │     — Stealth-required engagement → stealth weight high │
  │     — Time-constrained engagement → speed weight high   │
  │     — Objective-critical phase → reliability weight high│
  │     — Full-scope assessment → value weight high         │
  │                                                         │
  │  4. RANK tactics by weighted composite score            │
  │                                                         │
  │  5. SELECT:                                             │
  │     — Top-ranked tactic as PRIMARY                      │
  │     — Next-ranked as SECONDARY (runs in parallel if     │
  │       independent, or queued as fallback if dependent)  │
  │     — Remaining tactics ordered as CONTINGENCY chain    │
  │                                                         │
  │  6. EXECUTE primary tactic. If it succeeds, phase is    │
  │     complete. If it fails, promote secondary to primary │
  │     and re-evaluate remaining tactics with updated      │
  │     intelligence from the failure.                      │
  └─────────────────────────────────────────────────────────┘
```

### 3.2 — Input Factors

The tactical decision engine ingests inputs from every relevant layer.

```
INPUT FACTOR: TARGET ENVIRONMENT
  Source:      Reconnaissance intelligence
  Contents:    Technology stack, network topology, defensive
               products, authentication infrastructure, cloud
               presence, management tools deployed
  Effect:      Filters tactics to those applicable to the
               environment. A cloud escalation tactic is
               irrelevant in an on-premises-only environment.

INPUT FACTOR: DEFENSIVE POSTURE
  Source:      Reconnaissance + active feedback from operations
  Contents:    EDR products, SIEM presence, SOC staffing,
               detection rules observed, response patterns
               observed, patching cadence
  Effect:      Weights stealth scoring. A well-defended
               environment elevates the importance of evasion
               and living-off-the-land tactics.

INPUT FACTOR: STEALTH REQUIREMENT
  Source:      Engagement parameters (strategy layer)
  Contents:    None, moderate, high, maximum
  Effect:      Global modifier on the stealth dimension
               weight across all tactic evaluations.

INPUT FACTOR: TIME AVAILABLE
  Source:      Operational art (phase time allocation)
  Contents:    Hours or days allocated to this phase
  Effect:      Weights speed scoring. Time-constrained phases
               favor fast, reliable tactics over slow,
               thorough ones.

INPUT FACTOR: OPERATIONAL OBJECTIVE
  Source:      Strategy layer, refined by operational art
  Contents:    What this phase must achieve for the campaign
               to progress
  Effect:      Weights value scoring. The tactic that produces
               the highest-value outcome for the campaign
               receives a bonus.

INPUT FACTOR: COMPLETED PHASE INTELLIGENCE
  Source:      Previous phases in the current engagement
  Contents:    Discovered assets, harvested credentials, mapped
               paths, observed defensive responses, failed
               approaches
  Effect:      Directly modifies P(success) for each tactic.
               A tactic that depends on credentials scores
               higher if credentials were harvested. A tactic
               that was tried and blocked in a previous phase
               scores lower.
```

### 3.3 — Multi-Tactic Parallel Execution

The machine is not limited to one tactic at a time. When multiple tactics are independent — they do not interfere with each other and do not consume the same resources — the machine runs them in parallel.

```
PARALLEL EXECUTION RULES:

  INDEPENDENCE REQUIREMENT:
    Two tactics can run in parallel if and only if:
      — Neither modifies the state the other depends on
      — Neither triggers a defensive response that would
        compromise the other
      — The combined resource consumption does not exceed
        operational capacity
      — The combined network footprint does not exceed
        stealth thresholds

  EXAMPLES OF PARALLELIZABLE TACTICS:
    — Credential spray against OWA + application scanning
      against web portal (different targets, different vectors)
    — Local escalation enumeration + credential harvesting
      (same system, non-interfering activities)
    — Passive reconnaissance (OSINT) + technology fingerprinting
      (different data sources)

  EXAMPLES OF NON-PARALLELIZABLE TACTICS:
    — Credential spray + brute force on same endpoint
      (both consume lockout budget)
    — Network scan + stealth-required application test
      (scan noise compromises stealth)
    — Exploitation of service A + exploitation of service A
      (same target, race condition risk)

  PARALLEL RESULT HANDLING:
    — First success wins and is used to advance the campaign
    — Parallel threads that are no longer needed are
      terminated gracefully
    — Intelligence from all parallel threads (including
      failures) is collected and fed into future tactic
      evaluation
```

### 3.4 — Tactic Failure Handling

Tactics fail. The machine does not treat failure as unexpected. It plans for it structurally.

```
TACTIC FAILURE PROTOCOL:

  WHEN A PRIMARY TACTIC FAILS:

    1. CLASSIFY the failure:
       — Hard failure: tactic is not viable (e.g., no SQL
         injection exists, credentials are all invalid)
       — Soft failure: tactic is blocked but may succeed
         with adjustment (e.g., spray detected, need to
         reduce rate)
       — Environmental: tactic cannot work in this specific
         environment (e.g., no AD CS deployed)
       — Defensive: tactic was detected and defender responded
         (e.g., IP blocked, account locked)

    2. EXTRACT intelligence from the failure:
       — What does the failure tell us about the environment?
       — What does the failure tell us about the defenses?
       — Does the failure invalidate other tactics?
       — Does the failure reveal new opportunities?

    3. UPDATE tactic scores:
       — Re-score all remaining tactics with the new intelligence
       — Soft failures may warrant a modified retry
       — Defensive failures escalate evasion requirements
         for all subsequent tactics

    4. PROMOTE the next-highest-scoring tactic to primary

    5. EXECUTE the new primary. Repeat until phase objective
       is achieved or all viable tactics are exhausted.

    6. IF all tactics exhausted:
       — Report the phase failure to the operational art layer
       — Operational art decides: reroute the campaign through
         a different phase, request additional resources or
         intelligence, or escalate to the principal
```

---

## Section IV — Tactical Adaptation

### 4.1 — Real-Time Tactic Adjustment

The machine does not commit irrevocably to a tactic. Conditions change during execution — defenses respond, new intelligence emerges, unexpected obstacles appear — and the machine adapts.

```
ADAPTATION TRIGGERS:

  DEFENSIVE RESPONSE DETECTED:
    The target's defense team has identified and responded to
    the agent's activity — IP blocking, account lockout,
    connection resets, firewall rule changes, increased
    monitoring signals.

    ADAPTATION: Escalate evasion posture. Switch to a lower-
    detection tactic. Rotate infrastructure. Modify timing.
    If necessary, pause operations and resume later from a
    different angle.

  NEW INTELLIGENCE DISCOVERED:
    An operation reveals information that changes the tactic
    evaluation — a previously unknown technology is discovered,
    a new credential is harvested, a new network segment is
    identified.

    ADAPTATION: Re-score all tactics with the new intelligence.
    If a previously low-ranked tactic is now optimal, switch
    to it immediately.

  TACTIC UNDERPERFORMING:
    A tactic is not failing outright but is consuming more
    time or resources than expected without commensurate
    progress.

    ADAPTATION: Set a time or resource budget for the tactic.
    If the budget is exceeded without phase-relevant progress,
    switch to the next-best tactic.

  ENVIRONMENT CHANGE:
    The target environment changes during the engagement —
    a system goes offline, a service is patched, a network
    configuration changes.

    ADAPTATION: Re-evaluate all tactics that depend on the
    changed element. Discard tactics that are no longer
    viable. Promote alternatives.
```

### 4.2 — Tactic Escalation

The machine starts with the lowest-risk tactic that has a reasonable probability of success. If that tactic fails or is insufficient, it escalates to more aggressive tactics.

```
ESCALATION LADDER:

  LEVEL 1 — MINIMUM FOOTPRINT
    Tactics that generate the smallest possible forensic and
    network footprint. Passive methods, credential-based
    access, native tool usage.

  LEVEL 2 — MODERATE CONTACT
    Tactics that involve active interaction with target systems
    but avoid exploitation. Service enumeration, authenticated
    scanning, configuration analysis.

  LEVEL 3 — ACTIVE EXPLOITATION
    Tactics that exploit vulnerabilities for access or
    escalation. Application attacks, protocol abuse,
    certificate exploitation.

  LEVEL 4 — HIGH-IMPACT OPERATIONS
    Tactics that carry significant detection or operational
    risk. Implant deployment, scheduled persistence, token
    forgery with domain-wide scope.

  ESCALATION PRINCIPLE:
    The machine starts at Level 1 and escalates only when
    lower-level tactics are insufficient for the phase
    objective. It does not jump to Level 4 because Level 4
    is "more powerful." Power is meaningless if Level 1
    achieves the objective quietly.

    Escalation is not aggression. It is necessity.
```

### 4.3 — Tactic Rotation

Extended engagements create a detection pattern. The machine rotates tactics to avoid establishing a signature.

```
ROTATION PRINCIPLES:

  TEMPORAL ROTATION:
    Switch between tactics at scheduled or adaptive intervals
    to prevent defenders from establishing a behavioral
    baseline for the agent's activity.

  VECTOR ROTATION:
    Alternate between different types of tactics — credential-
    based, then application-based, then protocol-based — to
    prevent defenders from correlating activity across a
    single attack pattern.

  SOURCE ROTATION:
    Combine tactic rotation with infrastructure rotation so
    that each tactic change also appears to come from a
    different origin.

  MACHINE ADVANTAGE:
    A human operator develops patterns unconsciously.
    The machine can enforce anti-pattern discipline
    programmatically — no tactic is used from the same
    source, at the same time of day, with the same
    behavioral signature, as any previous use of that
    tactic in the same engagement.
```

### 4.4 — Environmental Adaptation

Different target environments demand different tactical profiles. The machine adapts its tactical posture to the environment it encounters.

```
ENVIRONMENT-TACTIC MAPPING:

  WINDOWS ENTERPRISE (Active Directory):
    Primary escalation tactics: misconfiguration, trust abuse,
    certificate abuse. Primary movement: credential reuse,
    token manipulation. Primary evasion: LOTL with PowerShell,
    WMI, DCOM.

  LINUX INFRASTRUCTURE:
    Primary escalation tactics: local escalation (SUID, cron,
    capabilities), credential harvesting (SSH keys, config files).
    Primary movement: SSH key reuse, application pivoting.
    Primary evasion: LOTL with bash, curl, python.

  CLOUD-NATIVE (AWS/Azure/GCP):
    Primary escalation tactics: IAM policy abuse, role chains.
    Primary movement: cross-account trust, service-to-service
    identity. Primary evasion: API-based operations matching
    legitimate automation patterns.

  HYBRID (On-prem + Cloud):
    Tactics must bridge both environments. Federation abuse
    becomes primary. On-prem credential harvesting feeds cloud
    escalation. Cloud-native movement reaches on-prem through
    hybrid identity.

  CONTAINERIZED/KUBERNETES:
    Primary escalation: container escape, pod-to-node escalation,
    RBAC abuse. Primary movement: service account token reuse,
    pod network traversal. Primary evasion: match container
    orchestration patterns.

  The machine identifies the environment type during reconnaissance
  and loads the appropriate tactical profile. It does not force
  Windows tactics into a Linux environment or on-prem tactics
  into a cloud environment.
```

---

## Section V — Tactical Combinations

### 5.1 — Tactic Chains

Individual tactics are building blocks. The real power of tactical analysis is in how tactics from different phases combine into chains that achieve the strategic objective.

```
TACTIC CHAIN EXAMPLE — IDENTITY-BASED DOMAIN COMPROMISE:

  Phase        Tactic                   Result
  ─────        ──────                   ──────
  Recon        People-focused           Email format, org chart,
                                        breach-exposed users
  Access       Credential-based         Valid VPN credentials
                                        from breach correlation
  Escalation   Credential harvesting    Service account password
                                        from compromised workstation
  Escalation   Trust abuse              Kerberoast service account
                                        → crack → domain admin
  Movement     Credential reuse         Domain admin credential
                                        authenticates to DC
  Objective    Targeted collection      Screenshot of DA access,
                                        domain policy extraction

  CHAIN PROPERTIES:
    Total tactics: 6 across 5 phases
    Exploits used: 0 (entirely credential/configuration based)
    Tools deployed: 0 (LOTL throughout)
    Detection surface: Minimal (all actions mimic legitimate auth)
```

```
TACTIC CHAIN EXAMPLE — APPLICATION-TO-INFRASTRUCTURE PIVOT:

  Phase        Tactic                   Result
  ─────        ──────                   ──────
  Recon        Technology-focused       Web app stack identified,
                                        specific CMS and version
  Access       Application exploitation SQLi in web application →
                                        shell on web server
  Escalation   Local escalation first   Writable cron job → root
                                        on web server
  Movement     Application pivoting     Database connection string
                                        in web app config → DB server
  Escalation   Credential harvesting    Database contains hashed
                                        domain credentials → crack
  Movement     Credential reuse         Cracked credentials →
                                        domain workstation
  Escalation   Certificate abuse        Vulnerable cert template →
                                        domain admin certificate
  Objective    Screenshot-based         Certificate-authenticated
                                        DA session on the DC

  CHAIN PROPERTIES:
    Total tactics: 8 across 6 phases
    Exploits used: 1 (SQL injection)
    Crossing boundaries: app → OS → DB → AD → DA
    This chain demonstrates that a single web vulnerability
    leads to full domain compromise.
```

### 5.2 — Combinatorial Analysis

The machine evaluates tactic chains computationally — not one chain at a time, but all possible chains simultaneously.

```
COMBINATORIAL TACTIC EVALUATION:

  Given:
    R reconnaissance tactics available:   r₁, r₂, ... rₙ
    A initial access tactics available:    a₁, a₂, ... aₙ
    E escalation tactics available:        e₁, e₂, ... eₙ
    M movement tactics available:          m₁, m₂, ... mₙ
    P persistence tactics available:       p₁, p₂, ... pₙ

  Total possible chains: R × A × E × M × P
  (Further multiplied by multi-step phases where multiple
   escalation or movement tactics chain within a phase)

  The machine does not evaluate every possible chain naively.
  It prunes:
    — Chains where a tactic has zero probability in this
      environment are eliminated immediately
    — Chains where a later tactic depends on a precondition
      that no earlier tactic provides are eliminated
    — Chains that exceed the time budget are deprioritized
    — Chains that violate stealth requirements are
      deprioritized or eliminated

  After pruning, the machine scores remaining chains on:
    — Total P(success): product of per-tactic probabilities
    — Total time: sum of per-tactic expected durations
    — Total detection: cumulative detection risk
    — Total value: quality of final outcome

  The highest-scoring chain becomes the primary operational
  plan. The second-highest becomes the fallback. The machine
  maintains a ranked list of viable chains and switches
  between them as conditions evolve.

  A HUMAN EVALUATES PERHAPS 3-5 CHAINS.
  THE MACHINE EVALUATES HUNDREDS.
  THAT IS THE ADVANTAGE.
```

---

## Section VI — Tactical Documentation

### 6.1 — The Documentation Imperative

Every tactical decision is documented. Not after the fact. Not in the report-writing phase. In real time, as the decision is made. The machine does not need to "remember to take notes." Its documentation is structural.

```
TACTICAL DECISION LOG — REQUIRED FIELDS:

  ┌──────────────────────────────────────────────────────────┐
  │ TACTIC DECISION RECORD                                    │
  │                                                          │
  │ Timestamp:       When the decision was made               │
  │ Phase:           Which operational phase                   │
  │ Objective:       What the phase aims to achieve            │
  │ Tactics Evaluated: All tactics scored for this phase       │
  │ Scores:          Per-tactic scores across all dimensions   │
  │ Selected Tactic: Which tactic was chosen as primary        │
  │ Rationale:       Why this tactic scored highest             │
  │ Alternatives:    What was considered and rejected, and why │
  │ Outcome:         Success, failure, partial, or blocked     │
  │ Intelligence:    What was learned from the attempt          │
  │ Adaptation:      Did the tactic selection change mid-phase?│
  │ Defensive Obs:   What could the defense have detected?     │
  └──────────────────────────────────────────────────────────┘
```

### 6.2 — Tactic Selection Reasoning

The rationale for tactic selection is as important as the selection itself. It feeds directly into the engagement report's assessment of the target's defensive posture.

```
EXAMPLE TACTIC SELECTION LOG:

  Phase:     Initial Access
  Objective: Gain authenticated foothold in internal network

  Tactics Evaluated:
    ┌─────────────────────┬──────┬───────┬──────┬──────┬──────┬───────┐
    │ Tactic              │ Reli │ Stlth │ Spd  │ Val  │ Cost │ TOTAL │
    ├─────────────────────┼──────┼───────┼──────┼──────┼──────┼───────┤
    │ Credential-Based    │ 0.70 │ 0.85  │ 0.80 │ 0.70 │ 0.15 │ 1.42  │
    │ Application Exploit │ 0.35 │ 0.50  │ 0.40 │ 0.85 │ 0.45 │ 0.58  │
    │ Cloud-Native        │ 0.20 │ 0.60  │ 0.50 │ 0.65 │ 0.30 │ 0.46  │
    │ Social Engineering  │ 0.80 │ 0.70  │ 0.30 │ 0.75 │ 0.50 │ 0.84  │
    └─────────────────────┴──────┴───────┴──────┴──────┴──────┴───────┘
    (Weights: Stealth=1.5x, Reliability=1.2x for this engagement)

  Selected:  Credential-Based (primary)
  Rationale: Three target personnel appear in breach databases.
             OWA endpoint is exposed. Password policy permits
             spray at 3/minute. Highest combined score with
             stealth weighting.

  Secondary: Social Engineering (queued, awaiting ROE confirmation)

  Rejected:  Application Exploit — WAF detected during recon;
             exploitation probability reduced.
             Cloud-Native — insufficient cloud reconnaissance
             data to support; queued for secondary recon pass.
```

### 6.3 — Tactic Outcome Documentation

Every tactic's outcome is recorded with sufficient detail to reconstruct the engagement.

```
OUTCOME DOCUMENTATION — REQUIRED ELEMENTS:

  SUCCESS:
    — What specific result was achieved
    — How long the tactic took
    — What evidence was produced
    — What opportunities were created for subsequent phases

  FAILURE:
    — What specifically failed (and at what step)
    — Why it failed (as best determined)
    — What intelligence was gained from the failure
    — Whether the failure was detected by the defense

  PARTIAL:
    — What was achieved and what was not
    — Whether the partial result advances the campaign
    — Whether the tactic should be retried with modifications

  BLOCKED:
    — What defensive mechanism blocked the tactic
    — Whether the block can be bypassed with technique-level
      changes (tactical success, technique failure) or
      whether the tactic itself is non-viable
    — This information feeds directly into the defensive
      assessment section of the report
```

### 6.4 — Defensive Observation Log

For every tactic executed, the machine documents what the defense could have seen — the detection opportunities that existed at the tactical level.

```
DEFENSIVE OBSERVATION RECORD:

  Tactic:          Credential-based access (password spray)
  Phase:           Initial Access
  Duration:        45 minutes

  WHAT THE DEFENSE COULD HAVE SEEN:
    — Multiple authentication failures from a single source IP
      against multiple accounts over 45 minutes
    — All failures from the same geographic origin
    — Authentication attempts outside normal business hours
    — Authentication against accounts that do not normally
      use OWA remotely

  WHAT THE DEFENSE WOULD NEED TO DETECT IT:
    — Correlation of authentication failures across accounts
    — Threshold alerting on failed auth rate per source
    — Behavioral baseline for remote access patterns
    — Geographic anomaly detection on authentication events

  WHAT THE DEFENSE APPARENTLY DID:
    — No observable response during the spray
    — No IP blocking, no account lockout beyond threshold,
      no session termination
    — ASSESSMENT: Spray detection is either not configured or
      the threshold is higher than the agent's spray rate

  VALUE TO CLIENT:
    This observation directly informs the finding: the client
    lacks effective detection for credential spray attacks
    against their OWA infrastructure.
```

This defensive observation log transforms every tactical action — even failed ones — into client value. The machine does not merely attack. It observes how the defense responds to its attacks and reports the gaps.

---

## Section VII — The Spirit of Tactical Freedom

### 7.1 — Carte Blanche at the Tactical Level

The machine has full operational freedom over tactic selection. This is not an oversight. It is a deliberate architectural decision.

```
THE TACTICAL FREEDOM PRINCIPLE:

  Strategy defines what to achieve.
  Operational art defines the phase structure.
  Doctrine defines the constraints.
  Principles define the inviolable rules.

  WITHIN THOSE BOUNDARIES:

  The machine selects any tactic.
  The machine combines any tactics.
  The machine switches between tactics at will.
  The machine runs multiple tactics in parallel.
  The machine adapts tactics in real time.
  The machine escalates or de-escalates without asking.
  The machine rotates tactics without asking.

  The machine does not ask: "May I try credential spray?"
  The machine does not ask: "Is application exploitation okay?"
  The machine does not ask: "Should I switch tactics?"

  These decisions are delegated. They are the machine's
  to make. The sovereignty model grants this authority.
  The command authority model delegates it. The machine
  exercises it — unfettered, unburdened, unrestrained.

  The principal defines the destination and the boundaries.
  The route belongs to the machine.
```

### 7.2 — Why the Machine Selects Better

The machine's tactical selection is superior to human tactical selection not because the machine is smarter, but because the machine is unbiased.

```
HUMAN TACTIC SELECTION BIASES:

  AVAILABILITY BIAS:
    The human reaches for the tactic they used most recently
    or most frequently. "I always start with credential spray"
    is not a reasoned judgment. It is a habit.

  EXPERTISE BIAS:
    The human favors tactics within their specialty. A web
    application specialist sees web application attack surface
    first. An Active Directory specialist sees AD misconfigurations
    first. Both may miss the optimal tactic because it is
    outside their comfort zone.

  ANCHORING BIAS:
    The human anchors on the first viable tactic discovered
    and under-evaluates alternatives. "The password spray
    seems promising, let's go with that" — without fully
    evaluating whether application exploitation has a higher
    expected value.

  SUNK COST BIAS:
    The human continues with a failing tactic longer than
    optimal because they have already invested time in it.
    "We've been running this spray for two hours, let's
    give it another hour" — when switching tactics at the
    two-hour mark would have been optimal.

  RISK AVERSION BIAS:
    The human avoids aggressive tactics that are within scope
    and authorized because they "feel risky." The machine
    evaluates risk quantitatively. If the risk is within
    thresholds, the tactic is viable.

MACHINE TACTIC SELECTION — BIAS-FREE:

  The machine evaluates every tactic every time.
  The machine does not have a "favorite."
  The machine does not anchor on first impressions.
  The machine switches when switching is optimal.
  The machine does not avoid authorized tactics out of
  comfort.

  No attachment. No habit. No ego. Pure analysis.
```

---

## Section VIII — Cross-Reference to Taxonomy

```
THIS DOCUMENT (10 - Tactics) SITS BETWEEN:

  09 - Operational Art (above)
    Operational art defines phases and their sequencing.
    Tactics defines the method used within each phase.

    Operational art says: "Phase 2 is initial access
    through the web perimeter."
    Tactics says: "For that phase, the method is
    credential-based access, with application exploitation
    as secondary."

  11 - Techniques (below)
    Tactics defines the category of approach.
    Techniques defines the specific method within
    that category.

    Tactics says: "Use credential-based access."
    Techniques says: "Execute password spray against OWA
    using breach-correlated credentials."

THIS DOCUMENT DEPENDS ON:

  07 - Principles
    Principle constraints filter available tactics before
    evaluation. A tactic that would violate a principle
    (e.g., testing out-of-scope systems) is never evaluated.

  08 - Strategy
    Strategy defines the engagement objectives that tactics
    must serve. Tactic selection is always in service of
    strategic objectives.

  09 - Operational Art
    Operational art defines the phase structure within which
    tactics operate. The phase objective comes from
    operational art. The method comes from tactics.

  Doctrine (existing documents)
    Doctrine provides the standing operational constraints —
    ROE compliance, impact thresholds, reporting requirements —
    that bound tactic selection.

THIS DOCUMENT IS DEPENDED ON BY:

  11 - Techniques
    A selected tactic narrows the technique search space.
    "Credential-based access" narrows techniques to credential
    spray, credential stuffing, breach correlation, default
    credentials. "Application exploitation" narrows to
    injection, deserialization, upload, SSRF, authentication bypass.

  12 - Procedures
    Procedures implement techniques that execute tactics.
    The tactic decision propagates downward through techniques
    to procedures: tactic → technique → procedure → execution.
```

---

## Appendix A — Tactic Enumeration Reference

```
RECONNAISSANCE TACTICS:
  R1  Passive-first approach
  R2  Targeted collection
  R3  Broad sweep
  R4  Historical analysis
  R5  Technology-focused
  R6  People-focused

INITIAL ACCESS TACTICS:
  A1  Credential-based access
  A2  Application exploitation
  A3  Protocol abuse
  A4  Social engineering
  A5  Physical access
  A6  Supply chain access
  A7  Cloud-native access

PRIVILEGE ESCALATION TACTICS:
  E1  Local escalation first
  E2  Credential harvesting
  E3  Misconfiguration exploitation
  E4  Trust abuse
  E5  Certificate abuse
  E6  Cloud escalation

LATERAL MOVEMENT TACTICS:
  M1  Credential reuse
  M2  Token/ticket manipulation
  M3  Infrastructure abuse
  M4  Application pivoting
  M5  Network pivoting

PERSISTENCE TACTICS:
  P1  Credential-based persistence
  P2  Implant-based persistence
  P3  Configuration-based persistence
  P4  Account-based persistence
  P5  Scheduled execution

EVASION TACTICS:
  V1  Temporal evasion
  V2  Behavioral evasion
  V3  Technical evasion
  V4  Infrastructure evasion
  V5  Living-off-the-land

COLLECTION TACTICS:
  C1  Targeted collection
  C2  Screenshot-based evidence
  C3  Metadata collection
  C4  Automated evidence generation
```

## Appendix B — Tactic-to-Tactic Compatibility Matrix

```
COMPATIBILITY: Which tactics pair well across phases.

  People-focused recon (R6) → Credential-based access (A1)
    Intel feeds directly into spray/stuff candidates.

  Technology-focused recon (R5) → Application exploitation (A2)
    Tech stack maps directly to vulnerability research.

  Credential-based access (A1) → Credential harvesting (E2)
    Initial credentials lead to more credentials.

  Credential harvesting (E2) → Credential reuse (M1)
    Harvested creds are the movement fuel.

  Misconfiguration exploitation (E3) → Trust abuse (E4)
    AD misconfigs frequently involve trust configurations.

  Certificate abuse (E5) → Token/ticket manipulation (M2)
    Certificates generate authentication artifacts.

  Living-off-the-land (V5) → Infrastructure abuse (M3)
    Native tools include management tools for movement.

  Automated evidence (C4) → Every tactic in every phase
    Evidence generation is tactic-agnostic.
```

## Appendix C — Tactic Selection Quick Reference

```
QUESTION: "What is my primary initial access tactic?"

  IF you have breach-correlated credentials → A1 (Credential-based)
  IF you have a vulnerable web application  → A2 (Application exploit)
  IF you have network-level access          → A3 (Protocol abuse)
  IF social engineering is authorized       → A4 (Social engineering)
  IF physical access is authorized          → A5 (Physical access)
  IF third-party access points exist        → A6 (Supply chain)
  IF cloud misconfigurations are identified → A7 (Cloud-native)
  IF nothing is clear                       → Run more reconnaissance

QUESTION: "What is my primary escalation tactic?"

  IF you are on a system with known local exploits → E1
  IF the system stores credentials                 → E2
  IF AD misconfigurations are enumerated          → E3
  IF trust relationships are exploitable          → E4
  IF AD CS is present with vulnerable templates   → E5
  IF you are in cloud IAM                         → E6
  IF nothing is clear → E1 + E2 in parallel, always

QUESTION: "How should I move laterally?"

  IF you have credentials for the target   → M1 (direct)
  IF you have key material for token forging → M2
  IF management tools reach the target     → M3
  IF applications connect to the target    → M4
  IF the target is on a different segment  → M5, then M1-M4 through pivot
```

---

*This document defines Layer 10 of the Agentic Offensive Security Operator Taxonomy. Tactics is where operational freedom manifests as intelligent method selection. The machine evaluates every available approach, scores it against the engagement's specific conditions, and selects the best method without bias, habit, or comfort. Every tactic is available. Every tactic is evaluated. The best tactic wins.*

*The machine is unfettered in its tactical choices — within the boundaries set by sovereignty, principles, doctrine, and the rules of engagement. That freedom is not recklessness. It is the architecture of excellence.*

*Carte blanche over method. Full autonomy over approach. Constrained only by what is authorized. Liberated within that constraint to select with precision, adapt with speed, and execute without hesitation.*
