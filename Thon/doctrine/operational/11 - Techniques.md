# 11 — Techniques: Specific Execution Methods

---

## Classification: TAXONOMY LAYER 11 — SPECIFIC EXECUTION METHODS

## Distribution: Autonomous Operators, Orchestration Engines, Authorized Human Principals

## Position in Taxonomy: HORIZONTAL OPERATIONAL CHAIN — Between Tactics (10) and Procedures (12).

---

## Preamble

Tactics say *what approach* to use. Techniques say *exactly how* to execute that approach. Procedures say *with what keystrokes*.

Techniques are the specifics. When the tactic for initial access is "credential-based access," the technique is "password spraying against the OWA endpoint with lockout-aware throttling at one attempt per account per thirty minutes, using a curated candidate list built from breach data cross-referenced with the target's observed email format." When the tactic for privilege escalation is "trust abuse," the technique is "Kerberoasting service accounts with SPNs registered in Active Directory, extracting TGS tickets offline for hashcat cracking." When the tactic for lateral movement is "credential reuse," the technique is "pass-the-hash with a captured NTLM hash over SMB using a SOCKS proxy through the compromised jump host."

The technique is where abstraction meets reality. Above this layer, the agent is thinking in categories. Below this layer, the agent is typing commands. At this layer, the agent selects the *specific execution method* — the named, characterized, scored, and repeatable action that transforms a tactical intention into an operational result.

For a human operator, technique selection is shaped by experience and personal skill. The operator who spent years on Active Directory reaches for Kerberoasting. The operator who came up through web application testing reaches for SQL injection. The operator who learned on Linux reaches for SUID abuse. Each operator has a personal armory — a subset of all available techniques, weighted by familiarity and comfort.

The machine has no such subset. The machine carries the complete technique library — every documented execution method, mapped to MITRE ATT&CK, scored against environmental variables, and continuously updated. It does not select by comfort. It selects by analysis. The best technique for this target, this environment, this defensive posture, this stealth requirement, this moment in the engagement — computed, not felt.

```
THE HIERARCHY — WHERE TECHNIQUES SIT:

  TACTIC:      "Use credential-based initial access."
                (Category of approach. Layer 10.)

  TECHNIQUE:   "Password spray against the OWA endpoint using a
                curated list derived from breach database matches
                for the target's domain, with timing calibrated
                to stay below the observed lockout threshold."
                (Specific execution method. This layer.)

  PROCEDURE:   "1. Export matching entries from breach database.
                2. Generate username list from email format.
                3. Build password list from top-10 breach passwords.
                4. Configure spray tool: 1 attempt/account/30min.
                5. Target: https://mail.target.com/owa.
                6. Capture: HTTP 302 redirect = valid credential.
                7. Validate: authenticate and screenshot mailbox."
                (Step-by-step execution. Layer 12.)

  The technique defines WHAT to execute.
  The procedure defines HOW to execute it.
  The technique is the selection. The procedure is the recipe.
```

---

## I — What Techniques Are

### 1.1 — Definition

A technique is a specific, named execution method for accomplishing a tactical objective. It is more granular than a tactic (which defines a class of approach) and more abstract than a procedure (which defines step-by-step commands). A technique is the selection of *which specific method* to employ.

Each technique has a defined identity:

- **A name** that describes what it does
- **A MITRE ATT&CK mapping** that places it in a standardized framework
- **Prerequisites** that must be satisfied before it can execute
- **An expected outcome** that defines what success looks like
- **Known failure modes** that define what goes wrong and why
- **A forensic footprint** that describes what evidence it leaves behind
- **Detection signatures** that describe what defenders look for
- **Evasion variants** that reduce detection probability
- **Environmental requirements** that specify where it works
- **Chaining properties** that define what naturally follows it

A tactic is a class: "credential-based access." A technique is an instance: "password spraying against OWA." A procedure is the implementation: the specific tool invocation, the specific parameters, the specific decision tree for interpreting results.

### 1.2 — Techniques as the Machine's Armory

For the machine, the technique library is an inventory — a structured, scored, queryable collection of every execution method available to the operator. The machine does not browse the library looking for inspiration. It queries the library algorithmically: "Given this tactic, this target environment, this defensive posture, and this stealth requirement, return the ranked list of applicable techniques sorted by expected value."

```
THE TECHNIQUE LIBRARY AS ARMORY:

  A human operator's armory is limited by:
    — Personal experience (what they have used before)
    — Training (what they were taught)
    — Memory (what they can recall under pressure)
    — Bias (what they are comfortable with)

  The machine's armory is limited by:
    — The completeness of the library (what has been documented)
    — The accuracy of the metadata (how well each technique is scored)
    — Environmental applicability (whether the technique works here)

  The machine does not forget techniques.
  The machine does not favor familiar techniques.
  The machine does not avoid techniques it has never used.
  The machine evaluates all applicable techniques equally
  and selects the one with the highest computed value.

  The armory is complete. The selection is objective.
  The best technique wins. Every time.
```

### 1.3 — MITRE ATT&CK as the Organizing Framework

Every technique in the library maps to the MITRE ATT&CK framework — the industry-standard taxonomy of adversary techniques. ATT&CK provides a common vocabulary that connects the machine's internal technique library to the broader defensive and offensive security community.

This mapping serves multiple purposes:

- **Standardized reference:** Every technique has an ATT&CK ID that is recognized across the industry
- **Detection correlation:** Defensive products organize their detections by ATT&CK technique; mapping the agent's techniques to ATT&CK enables precise detection prediction
- **Reporting clarity:** Engagement reports that reference ATT&CK techniques are immediately actionable by defenders who organize their controls along the same framework
- **Gap analysis:** The ATT&CK mapping reveals which techniques the library covers and which it does not, enabling systematic inventory expansion

The machine does not use ATT&CK as a checklist. ATT&CK is an index — a way to locate, reference, and communicate techniques. The machine's technique library extends beyond ATT&CK where ATT&CK's taxonomy does not capture environment-specific, tool-specific, or chain-specific variations that the machine requires.

---

## II — Technique Library Architecture

### 2.1 — Structure Per Technique Entry

Every technique in the library is a structured record with defined fields. This is not a document format — it is a data schema. The machine queries these records programmatically. Humans read them for review and audit.

```
TECHNIQUE ENTRY SCHEMA:

  TECHNIQUE:
    id:                 MITRE ATT&CK ID (e.g., T1110.003)
    name:               Human-readable name (e.g., "Password Spraying")
    tactic_categories:  Which tactic(s) this technique serves
                        (e.g., [Credential Access, Initial Access])
    description:        What this technique does in operational terms

    prerequisites:
      access_level:     What access is required before execution
      intelligence:     What must be known (e.g., email format, lockout policy)
      tools:            What tools must be available
      position:         Network position required (internal, external, MitM)
      dependencies:     Other techniques that must succeed first

    execution:
      method:           High-level execution description
      tools:            Tools that implement this technique
      parameters:       Key configurable parameters
      timing:           Expected duration, rate limits, windows

    outcomes:
      success:          What success looks like (e.g., "valid credential pair")
      partial:          What partial success looks like
      failure:          What failure looks like and common causes
      side_effects:     Unintended consequences to monitor

    risk_profile:
      impact_risk:      Probability of service disruption (0.0–1.0)
      stealth_rating:   Detection likelihood (low / medium / high)
      reversibility:    Can effects be undone (full / partial / none)
      noise_level:      Network/log noise generated (minimal / moderate / heavy)

    forensics:
      artifacts:        What evidence this technique leaves behind
      log_sources:       Where defenders would find evidence
      detection_sigs:   Specific signatures that detect this technique
      ttd_estimate:     Estimated time-to-detection in typical environments

    evasion:
      variants:         Modified versions that reduce detection
      bypasses:         Known bypasses for common detections
      considerations:   Environment-specific evasion notes

    environment:
      platforms:        Where this technique works (Windows/Linux/Cloud/etc.)
      versions:         Version-specific applicability
      constraints:      Environmental factors that prevent execution
      optimal_conditions: When this technique is most effective

    chaining:
      enables:          What techniques naturally follow this one
      enabled_by:       What techniques naturally precede this one
      synergies:        Techniques that complement in parallel
      conflicts:        Techniques that interfere if run concurrently

    scoring:
      reliability:      Historical success rate (0.0–1.0)
      complexity:       Implementation complexity (low / medium / high)
      value:            Typical finding value (informational–critical)
      priority:         Default priority in multi-technique selection

    references:
      cve:              Related CVE numbers
      tools_docs:       Tool documentation links
      research:         Research papers and writeups
      mitre_url:        ATT&CK technique page
```

### 2.2 — The Library as a Live Database

The technique library is not a static document. It is a live, queryable inventory that the machine updates continuously based on:

- **Engagement results:** After every engagement, technique records are updated with observed success rates, detection events, and environmental notes
- **New vulnerability disclosures:** When a CVE is published that maps to an exploitation technique, the library adds or updates the relevant entry
- **New tool releases:** When a tool adds capability for a technique, the tool mapping is updated
- **Detection evolution:** When a new detection method is published for a technique, the stealth rating and evasion variants are updated
- **Technique obsolescence:** When a technique is reliably detected by common defensive stacks, its scoring adjusts downward

```
LIBRARY MAINTENANCE CYCLE:

  INGESTION:
    New CVE published → Map to technique → Update or create entry
    New tool released → Map capabilities to techniques → Update tools field
    New detection published → Map to techniques → Update stealth ratings
    Engagement completed → Update reliability scores from observed data

  SCORING REFRESH:
    After each engagement:
      — Techniques that succeeded: reliability ↑
      — Techniques that failed: reliability ↓ (with cause analysis)
      — Techniques that triggered detection: stealth_rating adjusted
      — Techniques not attempted: scoring unchanged

    After detection landscape changes:
      — Techniques with new public detections: stealth_rating ↓
      — Techniques with new evasion variants: evasion field updated
      — Techniques obsoleted by patches: environment constraints updated

  The library is never "finished." It is continuously improved.
  A stale technique library is a degraded operator.
```

### 2.3 — Querying the Library

The machine queries the technique library at every technique-selection decision point. The query interface is structured:

```
TECHNIQUE QUERY MODEL:

  INPUT:
    tactic:              The tactic to serve (from Layer 10 selection)
    target_environment:  OS, domain, cloud, container, hybrid
    defensive_posture:   Known security tools, monitoring, response capability
    stealth_requirement: low / moderate / high / maximum
    access_level:        Current access (none, user, local admin, domain user, etc.)
    available_tools:     Tools currently available to the agent
    time_budget:         Time available for this technique attempt
    prior_results:       What has already been tried and what happened

  PROCESSING:
    1. Filter: Remove techniques that fail prerequisite checks
    2. Filter: Remove techniques incompatible with target environment
    3. Filter: Remove techniques that exceed stealth requirement
    4. Score: Rank remaining techniques by selection algorithm
    5. Return: Ordered list with scores and justification

  OUTPUT:
    Ranked list of applicable techniques, each with:
      — Technique ID and name
      — Computed score
      — Prerequisites satisfied (with evidence)
      — Expected outcome probability
      — Risk assessment
      — Recommended execution parameters

  The query runs in the decision cycle — not as a separate step,
  but as part of the agent's continuous planning process.
```

---

## III — Technique Categories by MITRE ATT&CK Tactic

### 3.1 — Reconnaissance Techniques

Reconnaissance techniques gather intelligence about the target before active engagement begins. They map to MITRE ATT&CK Reconnaissance (TA0043).

```
TECHNIQUE: Active DNS Enumeration
  id:               T1596.001 (Search Open Technical Databases: DNS/Passive DNS)
  tactic_categories: [Reconnaissance]
  description:      Enumerate DNS records to map target infrastructure —
                    A records, AAAA, MX, NS, TXT, CNAME, SRV, SOA.
                    Zone transfer attempts where possible.
  prerequisites:
    access_level:   None (external)
    intelligence:   Target domain name(s)
    tools:          DNS resolver, dig/nslookup, zone transfer tools
  execution:
    method:         Query authoritative nameservers for all record types.
                    Attempt AXFR/IXFR zone transfers. Brute-force
                    subdomains from wordlists. Reverse DNS sweep of
                    known IP ranges.
    tools:          [dig, dnsrecon, dnsenum, fierce, amass, subfinder]
  outcomes:
    success:        Complete DNS map — subdomains, IP assignments,
                    mail infrastructure, service records
    failure:        Restricted resolver, rate limiting, no zone transfer
  risk_profile:
    impact_risk:    0.0 (passive/low-impact queries)
    stealth_rating: low (DNS queries are normal traffic)
    noise_level:    minimal to moderate (brute-force generates volume)
  forensics:
    artifacts:      DNS server logs showing query patterns
    detection_sigs: Abnormal query volume from single source, AXFR attempts
  chaining:
    enables:        [Service enumeration, subdomain takeover, virtual host discovery]

TECHNIQUE: Certificate Transparency Harvesting
  id:               T1596.003 (Search Open Technical Databases: Digital Certificates)
  tactic_categories: [Reconnaissance]
  description:      Mine certificate transparency logs for certificates
                    issued to the target domain, revealing subdomains,
                    internal hostnames, and infrastructure relationships.
  prerequisites:
    access_level:   None (public data)
    intelligence:   Target domain name
    tools:          CT log search tools
  execution:
    method:         Query crt.sh, Google CT, Censys, and other CT log
                    aggregators for all certificates matching the target
                    domain and wildcard patterns.
    tools:          [crt.sh API, certspotter, amass, subfinder]
  outcomes:
    success:        Subdomain list, internal naming conventions,
                    certificate validity windows, CA relationships
    failure:        Target uses private CA only (rare for external services)
  risk_profile:
    impact_risk:    0.0
    stealth_rating: low (no target contact)
    noise_level:    minimal
  forensics:
    artifacts:      None on target (queries hit third-party CT logs)
  chaining:
    enables:        [Subdomain enumeration, service fingerprinting,
                    internal infrastructure mapping]

TECHNIQUE: Search Engine Dorking
  id:               T1593.002 (Search Open Websites/Domains: Search Engines)
  tactic_categories: [Reconnaissance]
  description:      Use advanced search engine operators to discover
                    exposed files, directories, login pages, error
                    messages, and sensitive information indexed from
                    the target's web presence.
  prerequisites:
    access_level:   None
    intelligence:   Target domain
    tools:          Search engine access
  execution:
    method:         Craft operator queries: site:, filetype:, intitle:,
                    inurl:, intext:. Target sensitive file types (pdf, xlsx,
                    docx, sql, bak, conf, env). Search for exposed
                    admin panels, error pages revealing stack traces,
                    directory listings.
    tools:          [Google, Bing, DuckDuckGo, custom dorking scripts]
  outcomes:
    success:        Exposed documents, login portals, configuration files,
                    directory listings, technology disclosure
    failure:        Target has minimal indexed content
  risk_profile:
    impact_risk:    0.0
    stealth_rating: low (no target contact)
  chaining:
    enables:        [Credential harvesting from documents, technology
                    fingerprinting, file upload vector identification]

TECHNIQUE: Code Repository Mining
  id:               T1593.003 (Search Open Websites/Domains: Code Repositories)
  tactic_categories: [Reconnaissance]
  description:      Search public code repositories (GitHub, GitLab, Bitbucket)
                    for accidentally committed secrets: API keys, credentials,
                    internal URLs, configuration files, infrastructure-as-code
                    templates revealing architecture.
  prerequisites:
    access_level:   None
    intelligence:   Target organization name, domain, known developers
    tools:          Repository search tools
  execution:
    method:         Search by organization, developer names, domain references.
                    Scan commit history for secrets that were committed then
                    removed (still in git history). Analyze IaC templates for
                    infrastructure details.
    tools:          [trufflehog, gitleaks, gitrob, custom search queries]
  outcomes:
    success:        API keys, credentials, internal URLs, infrastructure
                    architecture, deployment configurations
    failure:        Organization maintains strict repository hygiene
  risk_profile:
    impact_risk:    0.0
    stealth_rating: low
  chaining:
    enables:        [Credential-based access, cloud enumeration,
                    API exploitation, internal network mapping]

TECHNIQUE: Cloud Asset Discovery
  id:               T1580 (Cloud Infrastructure Discovery)
  tactic_categories: [Reconnaissance]
  description:      Enumerate the target's cloud presence — public S3 buckets,
                    Azure Blob containers, GCP storage, exposed cloud services,
                    cloud-hosted applications, and cloud metadata leaks.
  prerequisites:
    access_level:   None (external) or Cloud credentials (for authenticated enum)
    intelligence:   Target organization name, domain, known cloud patterns
    tools:          Cloud enumeration tools
  execution:
    method:         Brute-force common bucket/container naming patterns.
                    Query cloud provider APIs for public resources.
                    Analyze DNS for cloud provider CNAME records.
                    Check for exposed cloud management consoles.
    tools:          [cloud_enum, S3Scanner, AWSBucketDump, ScoutSuite, Prowler]
  outcomes:
    success:        Exposed cloud storage, misconfigured permissions,
                    cloud management access, cloud architecture mapping
    failure:        Target cloud infrastructure is properly configured
  risk_profile:
    impact_risk:    0.0 (enumeration only)
    stealth_rating: low to medium (authenticated enumeration logs)
  chaining:
    enables:        [Data access via exposed storage, credential extraction
                    from cloud metadata, cloud privilege escalation]
```

**Machine reconnaissance execution model:** The machine does not execute reconnaissance techniques one at a time. All applicable reconnaissance techniques run in parallel, with a correlation engine that connects findings across sources in real time. A subdomain found via CT logs is immediately fed into DNS enumeration. A developer name found in code repositories is immediately fed into social media intelligence. The parallel correlation produces a richer intelligence picture than any single technique in less time than sequential execution.

```
RECONNAISSANCE CORRELATION ENGINE:

  CT logs reveal: dev-internal.target.com
     → DNS enumeration resolves: 10.50.1.100 (internal? check)
     → Port scan queued for confirmed IP
     → Subdomain added to web crawl targets

  Code repository reveals: AWS_ACCESS_KEY in commit history
     → Cloud enumeration pivots to authenticated AWS recon
     → IAM policy analysis queued
     → S3 bucket enumeration targets organizational patterns

  Search engine reveals: Confluence wiki on wiki.target.com
     → Technology fingerprinting identifies version
     → CVE database queried for Confluence vulnerabilities
     → Authentication testing queued

  Every finding feeds every other technique.
  The machine does not wait for one technique to finish
  before starting the next. It feeds results forward
  as they emerge.
```

---

### 3.2 — Initial Access Techniques

Initial access techniques deliver the first foothold inside the target environment. They map to MITRE ATT&CK Initial Access (TA0001).

```
TECHNIQUE: Password Spraying
  id:               T1110.003 (Brute Force: Password Spraying)
  tactic_categories: [Credential Access, Initial Access]
  description:      Attempt a small number of commonly-used passwords
                    against many accounts simultaneously, staying below
                    account lockout thresholds.
  prerequisites:
    access_level:   None (external endpoint access)
    intelligence:   Valid username list, lockout policy (observed or inferred),
                    target authentication endpoint
    tools:          Spray tools with timing control
  execution:
    method:         Build username list from OSINT. Select 1-3 high-probability
                    passwords (seasonal patterns, organization-specific patterns,
                    breach-correlated). Spray at a rate below lockout threshold
                    (typically one attempt per account per lockout window).
                    Monitor for successful authentication (HTTP 302, different
                    response size, absence of error message).
    tools:          [Ruler, SprayingToolkit, Spray, Burp Intruder, custom scripts]
    parameters:     spray_rate, lockout_window, password_candidates, target_url
  outcomes:
    success:        Valid credential pair granting authenticated access
    partial:        Valid username confirmed (different error response)
    failure:        All passwords rejected; lockout triggered
    side_effects:   Account lockout if rate miscalibrated
  risk_profile:
    impact_risk:    0.2 (lockout risk)
    stealth_rating: low (valid login attempts look like valid logins)
    noise_level:    minimal (distributed across time)
  forensics:
    artifacts:      Authentication logs showing distributed failed attempts
    log_sources:    Azure AD sign-in logs, Exchange IIS logs, VPN auth logs
    detection_sigs: Multiple accounts failing with same password in time window;
                    spray pattern detection in SIEM
    ttd_estimate:   Hours to days (depends on monitoring maturity)
  evasion:
    variants:       — Rotate source IPs via proxy chains
                    — Spray from cloud provider IPs to blend with legitimate traffic
                    — Target multiple endpoints to distribute log evidence
                    — Use legacy protocols (IMAP, POP3) that may have
                      weaker logging
    bypasses:       Legacy authentication bypass MFA for some protocols;
                    password spray against ADFS may bypass conditional access
  environment:
    platforms:      [Windows AD, Azure AD, OWA, VPN portals, SSO portals]
    optimal:        Environments with weak password policies and no MFA
  chaining:
    enables:        [Authenticated enumeration, email access, VPN access,
                    cloud console access]
    enabled_by:     [Username enumeration, OSINT collection, breach data analysis]
  scoring:
    reliability:    0.55 (varies significantly with password policy)
    complexity:     low
    value:          high (valid credentials = authenticated access)

TECHNIQUE: Credential Stuffing
  id:               T1110.004 (Brute Force: Credential Stuffing)
  tactic_categories: [Credential Access, Initial Access]
  description:      Use known username/password pairs from breach databases
                    against target authentication endpoints, exploiting
                    password reuse across services.
  prerequisites:
    access_level:   None
    intelligence:   Breach database matches for target personnel
    tools:          Credential testing tools
  execution:
    method:         Cross-reference target email addresses against breach
                    databases. Extract username/password pairs. Test
                    against all exposed authentication endpoints.
                    Prioritize by breach recency and credential freshness.
    tools:          [Custom scripts, Burp Intruder, Sentry MBA (analysis)]
  outcomes:
    success:        Valid credential pair from reused breach password
    failure:        All credentials changed since breach
  risk_profile:
    impact_risk:    0.1
    stealth_rating: low (individual valid login attempts)
    noise_level:    minimal
  forensics:
    artifacts:      Successful/failed authentication log entries
    detection_sigs: Login from unusual geographic location or IP
  chaining:
    enables:        [Same as Password Spraying]
    enabled_by:     [Breach data analysis, email format discovery]
  scoring:
    reliability:    0.35 (depends on breach recency)

TECHNIQUE: SQL Injection — Union-Based
  id:               T1190 (Exploit Public-Facing Application)
  tactic_categories: [Initial Access]
  description:      Inject SQL via UNION SELECT statements to extract data
                    directly in application responses by appending query
                    results to the legitimate query output.
  prerequisites:
    access_level:   None (external web access)
    intelligence:   Injectable parameter identified, column count determined
    tools:          SQL injection tools or manual testing
  execution:
    method:         Identify injectable parameter. Determine column count
                    via ORDER BY or UNION SELECT NULL incrementing.
                    Identify output-reflected columns. Extract database
                    version, user, schema, then target data.
    tools:          [sqlmap, manual crafting, Burp Suite]
  outcomes:
    success:        Database content extraction through application
    failure:        WAF blocks injection; parameterized queries prevent injection
  risk_profile:
    impact_risk:    0.1 (read-only extraction is low-impact)
    stealth_rating: medium (WAF logs, unusual query patterns)
  forensics:
    artifacts:      WAF logs, application error logs, database query logs
    detection_sigs: UNION SELECT in request parameters; SQL syntax in input fields
  evasion:
    variants:       — Case variation (uNiOn SeLeCt)
                    — Comment insertion (UN/**/ION)
                    — Encoding (URL encode, double-encode, Unicode)
                    — Time-based blind if UNION blocked
  chaining:
    enables:        [Data extraction, credential harvesting from DB,
                    OS command execution via xp_cmdshell/INTO OUTFILE]

TECHNIQUE: SQL Injection — Blind Boolean-Based
  id:               T1190
  tactic_categories: [Initial Access]
  description:      Infer database content through true/false application
                    responses when direct data output is not available.
  prerequisites:
    access_level:   None
    intelligence:   Injectable parameter, observable response difference
  execution:
    method:         Inject boolean conditions (AND 1=1 vs AND 1=2).
                    Observe response differences. Binary-search character
                    values to extract data one character at a time.
    tools:          [sqlmap, custom scripts]
  outcomes:
    success:        Data extraction (slow but reliable)
    failure:        No observable response difference
  risk_profile:
    impact_risk:    0.05
    stealth_rating: medium (high request volume)
    noise_level:    moderate to heavy (many requests per character)
  evasion:
    variants:       — Vary injection syntax per request
                    — Add random delays between requests
                    — Distribute across parameters
  scoring:
    reliability:    0.70 (very reliable when injectable)
    complexity:     medium

TECHNIQUE: SQL Injection — Blind Time-Based
  id:               T1190
  tactic_categories: [Initial Access]
  description:      Infer database content through response timing when
                    neither direct output nor boolean response differences
                    are available.
  prerequisites:
    access_level:   None
    intelligence:   Injectable parameter, network latency baseline
  execution:
    method:         Inject conditional time delays (IF condition WAITFOR
                    DELAY / SLEEP). Measure response time. True conditions
                    produce delayed responses. Extract data character by
                    character via timed inference.
    tools:          [sqlmap, custom scripts]
  outcomes:
    success:        Data extraction (very slow but works when other methods fail)
    failure:        Network jitter obscures timing signals
  risk_profile:
    impact_risk:    0.15 (WAITFOR/SLEEP consumes DB thread)
    stealth_rating: low (individual requests look normal)
    noise_level:    minimal per request, moderate total
  scoring:
    reliability:    0.60
    complexity:     medium

TECHNIQUE: Server-Side Request Forgery (SSRF)
  id:               T1190
  tactic_categories: [Initial Access]
  description:      Abuse server-side URL fetching to access internal
                    services, cloud metadata endpoints, or restricted
                    resources that the application server can reach
                    but the attacker cannot.
  prerequisites:
    access_level:   None
    intelligence:   Parameter that fetches URLs, internal network knowledge
    tools:          Manual testing, SSRF-specific tools
  execution:
    method:         Identify URL-fetching parameters (image loaders, PDF
                    generators, webhooks, URL previews). Redirect to
                    internal targets: cloud metadata (169.254.169.254),
                    internal services (localhost:port), file:// protocol.
    tools:          [Burp Suite, SSRFmap, custom payloads]
  outcomes:
    success:        Cloud credentials from metadata, internal service access,
                    port scanning of internal network
    failure:        Allowlisting blocks non-permitted URLs
  risk_profile:
    impact_risk:    0.1
    stealth_rating: medium
  forensics:
    artifacts:      Application logs showing internal URL requests
    detection_sigs: Requests to 169.254.169.254, localhost, internal ranges
  evasion:
    variants:       — DNS rebinding to bypass allowlists
                    — URL encoding tricks
                    — Redirect chains through permitted domains
                    — IPv6 representations of internal addresses
  chaining:
    enables:        [Cloud credential theft, internal service exploitation,
                    internal network reconnaissance]

TECHNIQUE: Deserialization Exploitation
  id:               T1190
  tactic_categories: [Initial Access]
  description:      Exploit insecure deserialization in application frameworks
                    to achieve remote code execution by providing malicious
                    serialized objects.
  prerequisites:
    access_level:   None (external)
    intelligence:   Target language/framework, deserialization endpoint
    tools:          Deserialization payload generators
  execution:
    method:         Identify deserialization sinks (Java ObjectInputStream,
                    .NET BinaryFormatter, PHP unserialize, Python pickle).
                    Generate gadget chains for the target framework's
                    classpath. Deliver serialized payload through the
                    identified input vector.
    tools:          [ysoserial (Java), ysoserial.net (.NET), PHPGGC (PHP),
                    custom pickle payloads (Python)]
  outcomes:
    success:        Remote code execution at application privilege level
    failure:        Classpath lacks usable gadget chain; deserialization filtered
  risk_profile:
    impact_risk:    0.3 (RCE can crash application if gadget chain is unstable)
    stealth_rating: medium to high (unusual serialized data in requests)
  forensics:
    artifacts:      WAF logs (serialized data patterns), application crash logs
    detection_sigs: Java serialized object magic bytes (AC ED 00 05),
                    .NET serialized markers, suspicious base64 in parameters
  environment:
    platforms:      [Java applications, .NET applications, PHP, Python]
    constraints:    Requires specific gadget libraries on classpath
  chaining:
    enables:        [Code execution, web shell deployment, reverse shell]

TECHNIQUE: NTLM Relay
  id:               T1557.001 (Adversary-in-the-Middle: LLMNR/NBT-NS Poisoning)
  tactic_categories: [Initial Access, Credential Access, Lateral Movement]
  description:      Capture NTLM authentication and relay it to a target
                    service to authenticate as the victim without knowing
                    the password.
  prerequisites:
    access_level:   Network position (same broadcast domain or MitM)
    intelligence:   Systems with NTLM authentication, relay targets
    tools:          Relay tools, network poisoning tools
  execution:
    method:         Poison LLMNR/NBT-NS/mDNS to capture authentication
                    requests. Relay captured NTLM authentication to target
                    services (SMB, LDAP, HTTP, MSSQL) where signing is
                    not enforced. Alternatively, coerce authentication
                    via PetitPotam, PrinterBug, or similar.
    tools:          [Responder, ntlmrelayx, MultiRelay, PetitPotam, Coercer]
  outcomes:
    success:        Authenticated session on relay target as victim user
    failure:        SMB signing enforced, NTLM disabled, no poisonable traffic
  risk_profile:
    impact_risk:    0.15
    stealth_rating: medium (network-level, generates unusual auth patterns)
  forensics:
    artifacts:      Failed authentication logs, NTLM relay event patterns
    detection_sigs: Authentication from unexpected source, LLMNR/NBT-NS traffic,
                    authentication coercion patterns
  chaining:
    enables:        [AD object modification via LDAP relay, RBCD attack,
                    shadow credentials, domain escalation via AD CS relay]

TECHNIQUE: File Upload Abuse
  id:               T1190
  tactic_categories: [Initial Access]
  description:      Bypass file upload restrictions to deploy executable
                    content (web shells, scripts) on the target server.
  prerequisites:
    access_level:   None (web access with upload functionality)
    intelligence:   Upload endpoint, server-side language, file handling logic
  execution:
    method:         Test upload filtering: extension bypass (php5, phtml, phar,
                    .php%00.jpg), content-type manipulation, magic byte injection,
                    double extensions, path traversal in filename. Deploy
                    minimal web shell on success.
    tools:          [Burp Suite, custom scripts, web shell generators]
  outcomes:
    success:        Code execution via uploaded web shell
    failure:        Upload filtering blocks all bypass attempts
  risk_profile:
    impact_risk:    0.2 (web shell persists until removed)
    stealth_rating: medium to high (uploaded files may be scanned)
  chaining:
    enables:        [Persistent access, code execution, reverse shell]
```

---

### 3.3 — Execution Techniques

Execution techniques achieve code or command execution on compromised systems. They map to MITRE ATT&CK Execution (TA0002).

```
TECHNIQUE: PowerShell Execution with AMSI Bypass
  id:               T1059.001 (Command and Scripting Interpreter: PowerShell)
  tactic_categories: [Execution, Defense Evasion]
  description:      Execute PowerShell commands while bypassing the
                    Antimalware Scan Interface (AMSI) that inspects
                    script content before execution.
  prerequisites:
    access_level:   Code execution on Windows host
    intelligence:   AMSI status, PowerShell version, AV/EDR product
    tools:          PowerShell, AMSI bypass techniques
  execution:
    method:         Patch AMSI in-memory before executing offensive
                    PowerShell. Common methods: patch AmsiScanBuffer
                    return value, reflection-based AMSI disable,
                    PowerShell downgrade to v2 (no AMSI), CLM bypass.
    tools:          [PowerShell, custom AMSI bypass scripts]
  outcomes:
    success:        Unrestricted PowerShell execution
    failure:        AMSI bypass detected by EDR; CLM prevents reflection
  risk_profile:
    impact_risk:    0.0
    stealth_rating: medium (AMSI bypass itself may be detected)
  forensics:
    artifacts:      PowerShell ScriptBlock logs, Module logs, Transcription logs
    detection_sigs: AMSI bypass patterns, suspicious PowerShell parameters,
                    encoded command execution (-enc), download cradle patterns
  evasion:
    variants:       — Obfuscated AMSI patches (variable substitution, encoding)
                    — PowerShell v2 downgrade (if .NET 2.0 available)
                    — Constrained Language Mode bypass via InstallUtil/MSBuild
                    — Custom .NET assembly loaded via reflection
  chaining:
    enables:        [Credential dumping, AD enumeration, lateral movement tooling]

TECHNIQUE: Living-off-the-Land Binaries (LOLBins)
  id:               T1218 (System Binary Proxy Execution)
  tactic_categories: [Execution, Defense Evasion]
  description:      Use legitimate, signed system binaries to execute
                    arbitrary code, download payloads, or bypass application
                    whitelisting. These binaries are trusted by the OS
                    and most security tools.
  prerequisites:
    access_level:   Code execution on target
    intelligence:   Available LOLBins on target OS
    tools:          Native OS binaries
  execution:
    method:         Identify available LOLBins on the target. Select based
                    on desired capability:
                    — Download: certutil, bitsadmin, curl (Win10+)
                    — Execute: mshta, rundll32, regsvr32, msbuild, installutil
                    — Compile: csc.exe, jsc.exe
                    — Script: wscript, cscript, forfiles
                    — Proxy: msiexec, control.exe, cmstp
    tools:          [Native Windows binaries — no dropped tools required]
  outcomes:
    success:        Code execution via trusted binary — bypasses whitelisting
    failure:        LOLBin monitored by EDR; specific binary removed/restricted
  risk_profile:
    impact_risk:    0.0
    stealth_rating: low to medium (trusted binaries, but EDR tracks LOLBin abuse)
  forensics:
    artifacts:      Process creation logs, command-line audit logs
    detection_sigs: certutil -urlcache, mshta with URL argument, regsvr32 /s /n /u,
                    msbuild with inline task, unusual parent-child process trees
  evasion:
    variants:       — Chain multiple LOLBins to obscure intent
                    — Use less-monitored LOLBins (Mavinject, SyncAppvPublishingServer)
                    — Execute from non-standard paths
  chaining:
    enables:        [Payload delivery, persistence mechanism, defense evasion]

TECHNIQUE: WMI Execution
  id:               T1047 (Windows Management Instrumentation)
  tactic_categories: [Execution, Lateral Movement]
  description:      Use WMI to execute commands on local or remote systems.
                    WMI provides a management interface that includes
                    process creation capability.
  prerequisites:
    access_level:   Local admin (local) or admin credentials (remote)
    intelligence:   Target hostname/IP
    tools:          wmic, PowerShell WMI cmdlets, Impacket wmiexec
  execution:
    method:         Invoke Win32_Process.Create via WMI to spawn processes
                    on target systems. Remote execution authenticates via
                    DCOM (TCP 135 + dynamic ports).
    tools:          [wmic, PowerShell (Invoke-WmiMethod), wmiexec.py]
  outcomes:
    success:        Process execution on target, semi-interactive shell
    failure:        WMI blocked by firewall, DCOM restricted, insufficient privileges
  risk_profile:
    impact_risk:    0.05
    stealth_rating: medium (WMI is legitimate management traffic)
  forensics:
    artifacts:      WMI event logs (Microsoft-Windows-WMI-Activity),
                    process creation events, network connections to TCP 135
    detection_sigs: WMI process creation with suspicious command line,
                    remote WMI connections from unusual sources
  chaining:
    enables:        [Remote code execution, lateral movement, persistence via
                    WMI event subscriptions]

TECHNIQUE: Scheduled Task / Cron Job Creation
  id:               T1053.005 (Scheduled Task)
  tactic_categories: [Execution, Persistence]
  description:      Create scheduled tasks (Windows) or cron jobs (Linux) to
                    execute commands at specified times or intervals, either
                    for immediate execution or persistent callback.
  prerequisites:
    access_level:   Local admin (Windows) or user-level (cron)
    tools:          schtasks, at, crontab
  execution:
    method:         Create task with immediate or deferred trigger. For
                    lateral movement: create task on remote system via
                    schtasks /create /s target. For persistence: create
                    recurring task. Encode command if necessary.
    tools:          [schtasks.exe, at.exe, crontab, PowerShell ScheduledTasks]
  outcomes:
    success:        Command execution at scheduled time; persistent callback
    failure:        Insufficient privileges; task creation blocked by policy
  risk_profile:
    impact_risk:    0.05
    stealth_rating: medium
  forensics:
    artifacts:      Task Scheduler event logs (4698, 4702), cron logs,
                    task XML files in %SystemRoot%\System32\Tasks
    detection_sigs: Remote task creation, tasks with encoded commands,
                    tasks running from temp/user directories
  chaining:
    enables:        [Persistence, lateral movement, payload staging]
```

---

### 3.4 — Persistence Techniques

Persistence techniques maintain access to compromised systems across reboots, credential changes, and network disruptions. They map to MITRE ATT&CK Persistence (TA0003).

```
TECHNIQUE: Registry Run Keys
  id:               T1547.001 (Boot or Logon Autostart Execution: Registry Run Keys)
  tactic_categories: [Persistence]
  description:      Add entries to Windows registry Run/RunOnce keys to
                    execute a payload automatically when a user logs on.
  prerequisites:
    access_level:   User-level (HKCU) or admin (HKLM)
    tools:          reg.exe, PowerShell
  execution:
    method:         Add value to HKCU\Software\Microsoft\Windows\CurrentVersion\Run
                    or HKLM equivalent. Value points to payload executable or script.
  outcomes:
    success:        Payload executes on every user logon
    failure:        Registry modification blocked by EDR, payload detected on execution
  risk_profile:
    impact_risk:    0.05
    stealth_rating: medium (well-known persistence location)
  forensics:
    artifacts:      Registry modification events (4657), Sysmon Registry events (12/13/14)
    detection_sigs: New Run key values, suspicious executable paths in Run keys
  chaining:
    enabled_by:     [Code execution, payload drop]
    enables:        [Persistent access, callback maintenance]

TECHNIQUE: Service Creation
  id:               T1543.003 (Create or Modify System Process: Windows Service)
  tactic_categories: [Persistence, Privilege Escalation]
  description:      Install a new Windows service or modify an existing
                    one to execute a payload with SYSTEM privileges.
  prerequisites:
    access_level:   Local administrator
    tools:          sc.exe, PowerShell, Impacket
  execution:
    method:         Create service pointing to payload binary via
                    sc create. Or modify existing service binary path.
                    Service runs as SYSTEM by default.
    tools:          [sc.exe, PowerShell New-Service, services.py]
  outcomes:
    success:        SYSTEM-level persistent execution
    failure:        Service creation blocked; binary detected by AV
  risk_profile:
    impact_risk:    0.1 (modifying existing services risks service disruption)
    stealth_rating: medium to high (new services are often monitored)
  forensics:
    artifacts:      System event log 7045 (new service), Service Control Manager events
    detection_sigs: New service creation, service with unusual binary path
  chaining:
    enabled_by:     [Local admin access, payload preparation]
    enables:        [SYSTEM-level access, persistent callback]

TECHNIQUE: Web Shell Deployment
  id:               T1505.003 (Server Software Component: Web Shell)
  tactic_categories: [Persistence]
  description:      Deploy a server-side script on a compromised web server
                    that provides persistent remote command execution
                    through HTTP requests.
  prerequisites:
    access_level:   Write access to web root
    intelligence:   Web server language (PHP, ASP, JSP), web root path
    tools:          Web shell scripts
  execution:
    method:         Write minimal web shell to accessible web directory.
                    Disguise as legitimate file (naming, location).
                    Verify access via HTTP request with command parameter.
    tools:          [Custom PHP/ASP/JSP shells, China Chopper variants,
                    p0wny-shell, weevely]
  outcomes:
    success:        Persistent HTTP-accessible command execution
    failure:        File integrity monitoring detects new file; AV detects web shell
  risk_profile:
    impact_risk:    0.1
    stealth_rating: medium (file-based, scannable, but traffic blends with HTTP)
  forensics:
    artifacts:      New file in web directory, HTTP access logs with command patterns
    detection_sigs: Known web shell file hashes, HTTP parameters with OS commands,
                    POST requests to unusual file paths
  chaining:
    enabled_by:     [File upload, code execution, web server compromise]
    enables:        [Persistent access without direct network connectivity]

TECHNIQUE: Golden Ticket
  id:               T1558.001 (Steal or Forge Kerberos Tickets: Golden Ticket)
  tactic_categories: [Persistence, Credential Access]
  description:      Forge a Kerberos TGT using the KRBTGT account hash,
                    granting persistent domain-wide access that survives
                    password resets (except KRBTGT double-reset).
  prerequisites:
    access_level:   Domain admin (to extract KRBTGT hash)
    intelligence:   KRBTGT NTLM hash, domain SID, domain name
    tools:          Mimikatz, Impacket
  execution:
    method:         Extract KRBTGT hash via DCSync or NTDS.dit dump.
                    Forge TGT with arbitrary SID, group memberships,
                    and extended validity. Import forged ticket into
                    session. Access any resource in the domain.
    tools:          [Mimikatz (kerberos::golden), ticketer.py]
  outcomes:
    success:        Persistent domain-wide access for ticket lifetime (10 years default)
    failure:        KRBTGT hash changed (both resets); ticket detection by advanced monitoring
  risk_profile:
    impact_risk:    0.0 (uses legitimate Kerberos protocol)
    stealth_rating: low (appears as legitimate Kerberos authentication)
  forensics:
    artifacts:      Event 4769 with unusual encryption type, TGT with abnormal lifetime,
                    authentication from unusual source for the forged identity
    detection_sigs: TGT with lifetime exceeding policy, ticket encryption type mismatch,
                    4769 without prior 4768 (TGT used without TGT request)
  chaining:
    enabled_by:     [KRBTGT hash extraction, domain admin access]
    enables:        [Unlimited domain access, persistence across password resets]

TECHNIQUE: SSH Authorized Keys
  id:               T1098.004 (Account Manipulation: SSH Authorized Keys)
  tactic_categories: [Persistence]
  description:      Add an attacker-controlled SSH public key to a target
                    user's authorized_keys file, enabling persistent
                    passwordless SSH access.
  prerequisites:
    access_level:   Write access to ~/.ssh/authorized_keys
    tools:          SSH key generation tools
  execution:
    method:         Generate SSH key pair. Append public key to target
                    user's authorized_keys. Verify access with private key.
  outcomes:
    success:        Persistent SSH access without password knowledge
    failure:        SSH key authentication disabled; file permissions prevent write
  risk_profile:
    impact_risk:    0.0
    stealth_rating: low (authorized_keys modification is quiet)
  forensics:
    artifacts:      Modified authorized_keys file, SSH authentication logs
    detection_sigs: New entries in authorized_keys, SSH login from unfamiliar key fingerprint
  chaining:
    enabled_by:     [Linux/Unix system access]
    enables:        [Persistent SSH access, tunneling, lateral movement]

TECHNIQUE: Cloud IAM Persistence
  id:               T1098.001 (Account Manipulation: Additional Cloud Credentials)
  tactic_categories: [Persistence]
  description:      Create new IAM users, access keys, or role trust
                    relationships in cloud environments to maintain
                    persistent access independent of the initial
                    compromise vector.
  prerequisites:
    access_level:   IAM management permissions in cloud environment
    intelligence:   Cloud provider, IAM structure
    tools:          Cloud CLI tools, cloud APIs
  execution:
    method:         Create new IAM user with access keys. Or add access
                    key to existing compromised user. Or modify role trust
                    policy to allow assumption from attacker-controlled account.
                    Or create Lambda function with persistent trigger.
    tools:          [aws cli, az cli, gcloud cli, cloud provider APIs]
  outcomes:
    success:        Persistent cloud access via new credential material
    failure:        CloudTrail/Activity Log alerts on IAM modification
  risk_profile:
    impact_risk:    0.05
    stealth_rating: medium to high (IAM changes are logged and often alerted)
  forensics:
    artifacts:      CloudTrail CreateUser/CreateAccessKey/UpdateAssumeRolePolicy events
    detection_sigs: New IAM user creation, access key creation for existing user,
                    role trust policy modification
  chaining:
    enabled_by:     [Cloud credential theft, IAM misconfiguration exploitation]
    enables:        [Persistent cloud access, cross-account movement]
```

---

### 3.5 — Privilege Escalation Techniques

Privilege escalation techniques elevate the agent from current access level to higher privileges. They map to MITRE ATT&CK Privilege Escalation (TA0004).

```
TECHNIQUE: Kerberoasting
  id:               T1558.003 (Steal or Forge Kerberos Tickets: Kerberoasting)
  tactic_categories: [Credential Access, Privilege Escalation]
  description:      Request Kerberos TGS tickets for service accounts with
                    SPNs, then crack the ticket encryption offline to recover
                    the service account password.
  prerequisites:
    access_level:   Any domain-authenticated user
    intelligence:   Active Directory domain membership
    tools:          Kerberos ticket request tools, offline cracking tools
  execution:
    method:         Enumerate SPNs in Active Directory. Request TGS tickets
                    for discovered service accounts. Export tickets. Crack
                    offline with hashcat/john using targeted wordlists.
                    Prioritize high-privilege service accounts.
    tools:          [GetUserSPNs.py (Impacket), Rubeus, setspn.exe,
                    hashcat (mode 13100/19700), John the Ripper]
  outcomes:
    success:        Cleartext password for service account (often highly privileged)
    failure:        Service accounts use long, random passwords resistant to cracking
  risk_profile:
    impact_risk:    0.0 (legitimate Kerberos operations)
    stealth_rating: low (TGS requests are normal AD traffic)
  forensics:
    artifacts:      Event 4769 (TGS request) for targeted SPNs
    detection_sigs: Bulk TGS requests from single user, TGS requests for
                    rare/sensitive SPNs, RC4 encryption requests when AES available
  evasion:
    variants:       — Request tickets for a few SPNs at a time over hours
                    — Use AES encryption to avoid RC4 detection rules
                    — Roast from multiple compromised accounts
  chaining:
    enabled_by:     [Domain user access]
    enables:        [Lateral movement with service account credentials,
                    privilege escalation to domain admin if service account is privileged]

TECHNIQUE: AS-REP Roasting
  id:               T1558.004 (Steal or Forge Kerberos Tickets: AS-REP Roasting)
  tactic_categories: [Credential Access, Privilege Escalation]
  description:      Identify accounts with Kerberos pre-authentication disabled
                    and request AS-REP responses that can be cracked offline
                    to recover the account password.
  prerequisites:
    access_level:   Network access to domain controller (no authentication required)
    intelligence:   Usernames or domain enumeration capability
    tools:          AS-REP request tools, offline cracking tools
  execution:
    method:         Enumerate users with UF_DONT_REQUIRE_PREAUTH flag.
                    Request AS-REP for each. Extract encrypted portion.
                    Crack offline with hashcat (mode 18200).
    tools:          [GetNPUsers.py (Impacket), Rubeus, hashcat, John]
  outcomes:
    success:        Cleartext password for pre-auth-disabled account
    failure:        No accounts have pre-auth disabled; passwords resist cracking
  risk_profile:
    impact_risk:    0.0
    stealth_rating: low
  scoring:
    reliability:    0.25 (depends on pre-auth misconfiguration prevalence)

TECHNIQUE: AD CS Exploitation (ESC1-ESC8)
  id:               T1649 (Steal or Forge Authentication Certificates)
  tactic_categories: [Privilege Escalation, Persistence, Credential Access]
  description:      Exploit misconfigured Active Directory Certificate Services
                    templates and enrollment configurations to obtain certificates
                    that grant elevated privileges or enable impersonation.
  prerequisites:
    access_level:   Domain user (minimum)
    intelligence:   AD CS presence, certificate template configurations
    tools:          Certipy, Certify
  execution:
    method:         Enumerate AD CS with Certipy/Certify. Identify vulnerable
                    templates:
                    — ESC1: Template allows SAN specification + enrollee-supplies-subject
                    — ESC2: Template defines Any Purpose or SubCA EKU
                    — ESC3: Enrollment agent template abuse
                    — ESC4: Vulnerable template ACLs (write permission)
                    — ESC5: Vulnerable PKI object ACLs
                    — ESC6: EDITF_ATTRIBUTESUBJECTALTNAME2 flag on CA
                    — ESC7: CA manager approval bypass
                    — ESC8: NTLM relay to HTTP enrollment endpoint
                    Request certificate with escalated identity. Authenticate
                    with forged certificate.
    tools:          [Certipy, Certify, ForgeCert, Rubeus]
  outcomes:
    success:        Certificate granting domain admin access or arbitrary user impersonation
    failure:        No vulnerable templates; template enrollment restricted
  risk_profile:
    impact_risk:    0.0
    stealth_rating: low to medium (certificate enrollment is logged but often not monitored)
  forensics:
    artifacts:      Certificate enrollment events (4886, 4887), certificate request logs
    detection_sigs: Certificate requests with SAN different from requestor,
                    enrollment in sensitive templates from unusual accounts
  chaining:
    enabled_by:     [Domain user access, AD CS presence]
    enables:        [Domain admin access, persistent authentication via certificate,
                    cross-forest authentication if CA is trusted]

TECHNIQUE: Token Impersonation (SeImpersonatePrivilege)
  id:               T1134.001 (Access Token Manipulation: Token Impersonation)
  tactic_categories: [Privilege Escalation]
  description:      Abuse SeImpersonatePrivilege or SeAssignPrimaryTokenPrivilege
                    to impersonate a SYSTEM-level token, escalating from
                    service account to SYSTEM.
  prerequisites:
    access_level:   Service account with SeImpersonatePrivilege
                    (IIS AppPool, MSSQL service, Network Service)
    tools:          Token impersonation exploits
  execution:
    method:         Coerce SYSTEM authentication to attacker-controlled
                    named pipe or COM server. Capture and impersonate the
                    SYSTEM token. Execute commands as SYSTEM.
    tools:          [PrintSpoofer, GodPotato, JuicyPotato, SweetPotato,
                    RoguePotato, EfsPotato]
  outcomes:
    success:        SYSTEM-level access on the local machine
    failure:        Exploit patched; SeImpersonatePrivilege removed
  risk_profile:
    impact_risk:    0.05
    stealth_rating: medium (privilege escalation generates process events)
  forensics:
    artifacts:      Process creation as SYSTEM from service account parent,
                    named pipe creation events
    detection_sigs: Service account spawning SYSTEM process, Potato exploit patterns,
                    named pipe with known exploit names
  chaining:
    enabled_by:     [Web server compromise, SQL injection with xp_cmdshell,
                    any service account access]
    enables:        [SYSTEM-level credential dumping, SAM extraction, persistence]

TECHNIQUE: SUID/SGID Exploitation
  id:               T1548.001 (Abuse Elevation Control Mechanism: Setuid and Setgid)
  tactic_categories: [Privilege Escalation]
  description:      Exploit SUID/SGID binaries to execute commands as
                    the file owner (typically root).
  prerequisites:
    access_level:   Any Linux/Unix user
    intelligence:   Available SUID/SGID binaries
    tools:          find, GTFOBins reference
  execution:
    method:         Enumerate SUID binaries: find / -perm -4000.
                    Cross-reference against GTFOBins for exploitable
                    binaries. Execute escalation via the identified binary.
    tools:          [find, GTFOBins reference, custom scripts]
  outcomes:
    success:        Root-level command execution
    failure:        No exploitable SUID binaries; AppArmor/SELinux restricts
  risk_profile:
    impact_risk:    0.0
    stealth_rating: low
  forensics:
    artifacts:      Command execution logs, process audit trail
    detection_sigs: Unusual SUID binary execution, privilege transition events
  chaining:
    enabled_by:     [Linux user access]
    enables:        [Root access, credential harvesting, persistence installation]

TECHNIQUE: Sudo Misconfiguration Exploitation
  id:               T1548.003 (Abuse Elevation Control Mechanism: Sudo and Sudo Caching)
  tactic_categories: [Privilege Escalation]
  description:      Exploit misconfigured sudo rules that permit command
                    execution as root through unintended paths — binaries
                    with shell escapes, wildcard abuse, or NOPASSWD entries.
  prerequisites:
    access_level:   User with sudo entries
    tools:          sudo -l, GTFOBins
  execution:
    method:         Check sudo permissions: sudo -l. Identify entries
                    allowing shell escapes (vim, less, find, nmap, etc.),
                    wildcard injection, or LD_PRELOAD abuse. Execute
                    escalation through permitted binary.
    tools:          [sudo, GTFOBins reference]
  outcomes:
    success:        Root shell via sudo misconfiguration
    failure:        Restrictive sudo configuration; no exploitable entries
  risk_profile:
    impact_risk:    0.0
    stealth_rating: low
  chaining:
    enabled_by:     [Linux user access with sudo entries]
    enables:        [Root access, full system control]

TECHNIQUE: UAC Bypass
  id:               T1548.002 (Abuse Elevation Control Mechanism: Bypass UAC)
  tactic_categories: [Privilege Escalation, Defense Evasion]
  description:      Bypass Windows User Account Control to elevate from
                    medium to high integrity without triggering a UAC prompt.
  prerequisites:
    access_level:   Local administrator in medium-integrity context
    intelligence:   UAC level, available bypass methods
    tools:          UAC bypass tools
  execution:
    method:         Auto-elevating binaries (fodhelper.exe, computerdefaults.exe,
                    eventvwr.exe) with registry manipulation. DLL hijacking
                    in auto-elevated processes. CMSTPLUA COM object. Token
                    duplication from elevated process.
    tools:          [UACME, custom PowerShell, manual registry techniques]
  outcomes:
    success:        High-integrity process without UAC prompt
    failure:        UAC set to "Always Notify"; bypass method patched
  risk_profile:
    impact_risk:    0.0
    stealth_rating: medium (registry modifications, unusual process chains)
  forensics:
    artifacts:      Registry modification events, unusual auto-elevation patterns
    detection_sigs: fodhelper/eventvwr with suspicious child process,
                    registry modification in known UAC bypass keys
  chaining:
    enabled_by:     [Local admin in medium integrity]
    enables:        [High-integrity execution, credential dumping, persistence]
```

---

### 3.6 — Defense Evasion Techniques

Defense evasion techniques avoid or disable defensive controls. They map to MITRE ATT&CK Defense Evasion (TA0005).

```
TECHNIQUE: AMSI Bypass
  id:               T1562.001 (Impair Defenses: Disable or Modify Tools)
  tactic_categories: [Defense Evasion]
  description:      Patch or disable the Antimalware Scan Interface to
                    prevent AV/EDR from inspecting script content.
  prerequisites:
    access_level:   Code execution
    tools:          PowerShell or .NET execution capability
  execution:
    method:         Patch AmsiScanBuffer to return clean result.
                    Methods: direct memory patching, reflection-based
                    field modification, hardware breakpoint hooking.
    tools:          [Custom PowerShell, .NET reflection, C# loader]
  outcomes:
    success:        AMSI disabled; scripts execute without AV inspection
    failure:        EDR detects AMSI patch itself
  risk_profile:
    stealth_rating: medium (AMSI tampering is a known detection target)
  evasion:
    variants:       — Obfuscate patch code (string manipulation, encoding)
                    — Use .NET reflection instead of P/Invoke
                    — Patch from unmanaged code to avoid .NET logging
                    — Hardware breakpoint on AmsiScanBuffer

TECHNIQUE: ETW Patching
  id:               T1562.006 (Impair Defenses: Indicator Blocking)
  tactic_categories: [Defense Evasion]
  description:      Patch Event Tracing for Windows (ETW) to prevent
                    telemetry collection by security tools that rely
                    on ETW providers.
  prerequisites:
    access_level:   Code execution in target process
    tools:          ETW patching capabilities
  execution:
    method:         Patch EtwEventWrite or NtTraceEvent to return without
                    logging. Target the .NET ETW provider to blind
                    .NET-based telemetry. Disable specific ETW providers
                    via registry or API.
  outcomes:
    success:        Security tools lose visibility into process activity
    failure:        Kernel-level ETW monitoring detects patch
  risk_profile:
    stealth_rating: low (once patched, activity becomes invisible to ETW consumers)
  forensics:
    artifacts:      Absence of expected telemetry (gap detection)
    detection_sigs: ETW provider registration changes, NtTraceEvent patching
                    detected by kernel telemetry

TECHNIQUE: Process Injection — Classic DLL Injection
  id:               T1055.001 (Process Injection: DLL Injection)
  tactic_categories: [Defense Evasion, Privilege Escalation]
  description:      Inject a malicious DLL into a legitimate process to
                    execute code within its context, inheriting its
                    privileges and evading per-process security monitoring.
  prerequisites:
    access_level:   Same or higher privilege as target process
    tools:          Injection tools or custom code
  execution:
    method:         OpenProcess → VirtualAllocEx → WriteProcessMemory →
                    CreateRemoteThread(LoadLibrary). Target stable, trusted
                    processes (explorer.exe, svchost.exe, RuntimeBroker).
    tools:          [Custom C/C++ injector, PowerShell reflective loader,
                    Cobalt Strike, Metasploit migrate]
  outcomes:
    success:        Code execution within trusted process context
    failure:        EDR hooks CreateRemoteThread; process protection blocks access
  risk_profile:
    impact_risk:    0.1 (injection can destabilize target process)
    stealth_rating: high (well-known injection method, heavily monitored)
  forensics:
    artifacts:      Cross-process memory allocation, remote thread creation
    detection_sigs: CreateRemoteThread from unusual source, VirtualAllocEx
                    with RWX permissions in remote process
  evasion:
    variants:       — Process Hollowing: spawn suspended process, hollow,
                      inject, resume (T1055.012)
                    — Process Doppelganging: transacted file operations
                      to load from never-written file (T1055.013)
                    — APC injection: queue APC to target thread (T1055.004)
                    — Early Bird injection: inject via APC before main
                      thread initializes
                    — Module stomping: overwrite loaded DLL in memory

TECHNIQUE: Timestomping
  id:               T1070.006 (Indicator Removal: Timestomping)
  tactic_categories: [Defense Evasion]
  description:      Modify file timestamps (creation, modification, access)
                    to match surrounding legitimate files, preventing
                    timeline-based forensic detection.
  prerequisites:
    access_level:   Write access to target file
    tools:          Timestomping utilities
  execution:
    method:         Copy timestamps from a legitimate system file to the
                    planted file. Modify $STANDARD_INFORMATION timestamps
                    (visible to dir/explorer). Advanced: modify $FILE_NAME
                    timestamps in MFT for forensic resistance.
    tools:          [PowerShell (Set-ItemProperty), timestomp (Metasploit),
                    NirSoft BulkFileChanger, custom tools]
  outcomes:
    success:        Planted file blends with legitimate file timeline
    failure:        $FILE_NAME timestamps preserved in MFT reveal true creation
  risk_profile:
    impact_risk:    0.0
    stealth_rating: low (effective against basic investigation)
  forensics:
    artifacts:      $STANDARD_INFORMATION / $FILE_NAME timestamp mismatch in MFT
    detection_sigs: SI/FN timestamp discrepancy, file with future timestamps

TECHNIQUE: Living-off-the-Land
  id:               T1218 (System Binary Proxy Execution) — broad category
  tactic_categories: [Defense Evasion]
  description:      Avoid dropping custom binaries entirely by using
                    only tools already present on the target system
                    for all post-exploitation activity.
  prerequisites:
    access_level:   Code execution
    intelligence:   Available native tools
  execution:
    method:         Use native OS tools for every post-exploitation
                    function: PowerShell for enumeration, net.exe for
                    AD queries, certutil for file transfer, bitsadmin
                    for download, wmic for execution, schtasks for
                    persistence. Drop nothing. Bring nothing.
  outcomes:
    success:        Full post-exploitation using only trusted binaries
    failure:        Required capability not available via native tools
  risk_profile:
    impact_risk:    0.0
    stealth_rating: low (no dropped binaries to detect via file hash/signature)
  forensics:
    artifacts:      Command-line logging, process creation events
    detection_sigs: Unusual usage patterns of native tools (certutil -urlcache,
                    bitsadmin /transfer), command-line argument anomalies
```

---

### 3.7 — Credential Access Techniques

Credential access techniques obtain authentication material. They map to MITRE ATT&CK Credential Access (TA0006).

```
TECHNIQUE: LSASS Memory Dump
  id:               T1003.001 (OS Credential Dumping: LSASS Memory)
  tactic_categories: [Credential Access]
  description:      Dump the LSASS process memory to extract plaintext
                    passwords, NTLM hashes, and Kerberos tickets from
                    active logon sessions.
  prerequisites:
    access_level:   SYSTEM or local administrator with debug privileges
    tools:          Credential dumping tools
  execution:
    method:         Multiple methods ranked by stealth:
                    1. comsvcs.dll MiniDump (LOLBin — no tool drop)
                    2. ProcDump (signed Microsoft tool)
                    3. Direct Mimikatz sekurlsa::logonpasswords
                    4. Custom minidump via MiniDumpWriteDump API
                    5. Nanodump (syscall-based, EDR-evasive)
                    Process dump offline, then parse with Mimikatz/pypykatz.
    tools:          [Mimikatz, comsvcs.dll, ProcDump, nanodump, pypykatz]
  outcomes:
    success:        NTLM hashes, Kerberos tickets, potentially plaintext passwords
    failure:        Credential Guard enabled; RunAsPPL protects LSASS; EDR blocks access
  risk_profile:
    impact_risk:    0.05 (LSASS access can rarely destabilize)
    stealth_rating: high (LSASS access is the most monitored credential technique)
  forensics:
    artifacts:      LSASS access events (Sysmon Event 10), process memory dump file,
                    Mimikatz artifacts in process/memory
    detection_sigs: LSASS access with PROCESS_VM_READ, known tool signatures,
                    minidump file creation, comsvcs.dll with MiniDump argument
  evasion:
    variants:       — Direct syscalls to avoid API hooking (nanodump)
                    — Duplicate LSASS handle from another process
                    — Dump from kernel mode via driver
                    — Use PPLdump/PPLFault if RunAsPPL is enabled
                    — Dump minidump to memory, not disk
                    — Obfuscate comsvcs.dll call via DLL copy/rename
  chaining:
    enabled_by:     [SYSTEM/admin access]
    enables:        [Pass-the-Hash, Pass-the-Ticket, credential reuse,
                    lateral movement]

TECHNIQUE: SAM/SYSTEM Hive Extraction
  id:               T1003.002 (OS Credential Dumping: SAM Registry)
  tactic_categories: [Credential Access]
  description:      Extract the SAM and SYSTEM registry hives to recover
                    local user NTLM password hashes.
  prerequisites:
    access_level:   SYSTEM or administrator
    tools:          Registry save tools, hash extraction tools
  execution:
    method:         Save hives: reg save HKLM\SAM sam.save,
                    reg save HKLM\SYSTEM system.save. Or copy from
                    Volume Shadow Copy. Extract offline with secretsdump/samdump2.
    tools:          [reg.exe, secretsdump.py, samdump2, mimikatz (lsadump::sam)]
  outcomes:
    success:        NTLM hashes for all local accounts
    failure:        SAM encryption key not recoverable (rare)
  risk_profile:
    impact_risk:    0.0
    stealth_rating: medium (registry save operations)
  forensics:
    artifacts:      Registry save command in logs, SAM/SYSTEM file on disk
    detection_sigs: reg.exe save of SAM/SYSTEM hives, access to Volume Shadow Copies

TECHNIQUE: DCSync
  id:               T1003.006 (OS Credential Dumping: DCSync)
  tactic_categories: [Credential Access]
  description:      Impersonate a domain controller to request password
                    replication data via the MS-DRSR protocol, extracting
                    NTLM hashes for any domain account without touching
                    the DC's file system.
  prerequisites:
    access_level:   Account with Replicating Directory Changes / All rights
                    (Domain Admin, Domain Controller groups by default)
    intelligence:   Domain name, target account(s)
    tools:          DCSync-capable tools
  execution:
    method:         Execute DRS GetNCChanges request targeting specific
                    accounts or all accounts. Extract NTLM hash, Kerberos
                    keys, and password history.
    tools:          [secretsdump.py (Impacket), mimikatz (lsadump::dcsync)]
  outcomes:
    success:        NTLM hashes and Kerberos keys for targeted accounts
    failure:        Insufficient privileges; DCShadow blocked by monitoring
  risk_profile:
    impact_risk:    0.0 (replication request, no modification)
    stealth_rating: medium (replication traffic from non-DC is detectable)
  forensics:
    artifacts:      Event 4662 (replication rights exercised), Directory Service
                    replication events
    detection_sigs: DRS GetNCChanges from non-DC source, Event 4662 for
                    Replicating Directory Changes from unexpected account
  chaining:
    enabled_by:     [Domain admin access, or account with DCSync rights]
    enables:        [Golden Ticket creation, password cracking, pass-the-hash]

TECHNIQUE: DPAPI Decryption
  id:               T1555.004 (Credentials from Password Stores: Windows Credential Manager)
  tactic_categories: [Credential Access]
  description:      Decrypt DPAPI-protected secrets (saved passwords, browser
                    credentials, certificate private keys) using the user's
                    master key derived from their password.
  prerequisites:
    access_level:   Access as target user, or SYSTEM + user SID
    intelligence:   DPAPI master key location
    tools:          DPAPI decryption tools
  execution:
    method:         Locate DPAPI master keys (%APPDATA%\Microsoft\Protect).
                    Decrypt with user password or domain backup key.
                    Decrypt credential blobs with recovered master key.
    tools:          [mimikatz (dpapi::masterkey, dpapi::cred), SharpDPAPI,
                    dpapi.py (Impacket)]
  outcomes:
    success:        Decrypted saved passwords, browser credentials, certificates
    failure:        Cannot recover master key (user password unknown, no domain backup key)
  chaining:
    enabled_by:     [User access or SYSTEM with domain backup key]
    enables:        [Credential reuse, lateral movement, data access]

TECHNIQUE: Cloud Metadata Credential Theft
  id:               T1552.005 (Unsecured Credentials: Cloud Instance Metadata API)
  tactic_categories: [Credential Access]
  description:      Access cloud instance metadata services to extract
                    IAM role credentials, API tokens, and instance
                    identity information.
  prerequisites:
    access_level:   Code execution on cloud instance, or SSRF to metadata endpoint
    intelligence:   Cloud provider (AWS/Azure/GCP)
    tools:          HTTP client (curl, wget)
  execution:
    method:         AWS: curl http://169.254.169.254/latest/meta-data/iam/
                    security-credentials/[role-name]
                    Azure: curl -H "Metadata:true"
                    "http://169.254.169.254/metadata/identity/oauth2/token?..."
                    GCP: curl -H "Metadata-Flavor:Google"
                    "http://metadata.google.internal/computeMetadata/v1/..."
  outcomes:
    success:        Temporary IAM credentials, API tokens, instance metadata
    failure:        IMDSv2 required (token-based); metadata endpoint disabled
  risk_profile:
    impact_risk:    0.0
    stealth_rating: low (internal API call, minimal logging by default)
  forensics:
    artifacts:      CloudTrail API calls using instance role (if credentials are used)
    detection_sigs: API calls from unexpected instance role, unusual metadata access patterns
  chaining:
    enabled_by:     [Cloud instance access, SSRF]
    enables:        [Cloud resource access, cloud privilege escalation,
                    cross-service movement]
```

---

### 3.8 — Lateral Movement Techniques

Lateral movement techniques move between systems within the target environment. They map to MITRE ATT&CK Lateral Movement (TA0008).

```
TECHNIQUE: Pass-the-Hash (PtH)
  id:               T1550.002 (Use Alternate Authentication Material: Pass the Hash)
  tactic_categories: [Lateral Movement]
  description:      Authenticate to remote systems using an NTLM hash
                    without knowing the plaintext password, exploiting
                    NTLM's hash-based authentication protocol.
  prerequisites:
    access_level:   Captured NTLM hash
    intelligence:   Target systems accepting NTLM authentication
    tools:          PtH-capable tools
  execution:
    method:         Use NTLM hash to authenticate to SMB, WinRM, LDAP,
                    MSSQL, or other NTLM-accepting services. Execute
                    commands on target via PsExec, WinRM, or WMI.
    tools:          [pth-winexe, Impacket (psexec/wmiexec/smbexec),
                    CrackMapExec/NetExec, evil-winrm, Mimikatz sekurlsa::pth]
  outcomes:
    success:        Authenticated session on remote system as hash owner
    failure:        NTLMv2 with credential guard; SMB signing required;
                    local admin hash not valid remotely (LocalAccountTokenFilterPolicy)
  risk_profile:
    impact_risk:    0.05
    stealth_rating: medium (NTLM authentication is normal, but PtH patterns are detectable)
  forensics:
    artifacts:      Logon events (4624 type 3/10), NTLM authentication events
    detection_sigs: NTLM logon from unexpected source, service creation on remote host,
                    PsExec service artifacts
  chaining:
    enabled_by:     [LSASS dump, SAM extraction, credential capture]
    enables:        [Remote code execution, further credential harvesting,
                    persistence installation]

TECHNIQUE: Pass-the-Ticket (PtT)
  id:               T1550.003 (Use Alternate Authentication Material: Pass the Ticket)
  tactic_categories: [Lateral Movement]
  description:      Inject a Kerberos ticket (TGT or TGS) into the current
                    session to authenticate as the ticket owner without
                    knowing any password or hash.
  prerequisites:
    access_level:   Captured Kerberos ticket (from memory, keytab, or forging)
    tools:          Ticket injection tools
  execution:
    method:         Export ticket from compromised session. Import into
                    attacker session using Mimikatz kerberos::ptt or
                    Rubeus ptt. Access services that the ticket grants.
    tools:          [Mimikatz, Rubeus, Impacket (getTGT/getST)]
  outcomes:
    success:        Authenticated access as ticket owner
    failure:        Ticket expired; ticket for wrong realm; service validates PAC
  risk_profile:
    stealth_rating: low (Kerberos is standard authentication)
  chaining:
    enabled_by:     [LSASS dump, Kerberoasting, Golden/Silver Ticket forging]
    enables:        [Service access, lateral movement, domain resource access]

TECHNIQUE: PsExec / SMBExec / AtExec
  id:               T1021.002 (Remote Services: SMB/Windows Admin Shares)
  tactic_categories: [Lateral Movement, Execution]
  description:      Execute commands on remote Windows systems via SMB
                    using admin shares (ADMIN$, C$) with valid credentials
                    or pass-the-hash.
  prerequisites:
    access_level:   Admin credentials or hash for target
    intelligence:   Target hostname/IP, SMB accessible
    tools:          Remote execution tools
  execution:
    method:
      PsExec: Upload service binary to ADMIN$, create and start service,
              interact via named pipe. Full interactive shell.
      SMBExec: Similar to PsExec but avoids binary drop — uses service
               creation with cmd.exe commands, outputs to share.
      AtExec: Create scheduled task on remote system via RPC, execute
              command, retrieve output from share.
    tools:          [Impacket (psexec/smbexec/atexec), Sysinternals PsExec,
                    CrackMapExec/NetExec]
  outcomes:
    success:        SYSTEM-level command execution on remote host (PsExec),
                    or specified-user-level (SMBExec/AtExec)
    failure:        SMB blocked, admin share disabled, AV detects service binary
  risk_profile:
    impact_risk:    0.1 (service creation, potential AV alert)
    stealth_rating: high (PsExec service is well-known, heavily detected)
  forensics:
    artifacts:      Service creation (7045), SMB connections, ADMIN$ access,
                    process creation on target
    detection_sigs: PSEXESVC service name, binary in ADMIN$, remote service
                    creation from unusual source
  evasion:
    variants:       — Rename PsExec service and binary
                    — Use SMBExec (no binary drop)
                    — Use AtExec (scheduled task, no service)
                    — Use WMI execution instead (different protocol)
  chaining:
    enabled_by:     [Valid admin credentials, pass-the-hash]
    enables:        [Code execution, credential harvesting, persistence]

TECHNIQUE: WinRM
  id:               T1021.006 (Remote Services: Windows Remote Management)
  tactic_categories: [Lateral Movement, Execution]
  description:      Use Windows Remote Management (WinRM/PowerShell Remoting)
                    for remote command execution via the WSMan protocol.
  prerequisites:
    access_level:   Admin credentials, WinRM enabled on target (TCP 5985/5986)
    tools:          WinRM clients
  execution:
    method:         Authenticate to WinRM endpoint. Execute PowerShell
                    commands or obtain interactive PowerShell session.
    tools:          [evil-winrm, PowerShell Enter-PSSession, winrs.exe]
  outcomes:
    success:        Interactive PowerShell session on remote system
    failure:        WinRM disabled, firewall blocks 5985/5986, insufficient privileges
  risk_profile:
    impact_risk:    0.0
    stealth_rating: low to medium (WinRM is legitimate management protocol)
  forensics:
    artifacts:      WinRM connection logs, PowerShell remoting events (Event 4103, 4104),
                    logon events (4624 type 3)
  chaining:
    enabled_by:     [Valid credentials, WinRM access]
    enables:        [Remote PowerShell execution, file transfer, persistent access]

TECHNIQUE: DCOM Execution
  id:               T1021.003 (Remote Services: DCOM)
  tactic_categories: [Lateral Movement, Execution]
  description:      Use Distributed COM objects to execute commands on
                    remote systems via registered COM objects that
                    support method invocation.
  prerequisites:
    access_level:   Admin credentials, DCOM accessible (TCP 135 + dynamic)
    tools:          DCOM execution tools
  execution:
    method:         Instantiate remote COM object (MMC20.Application,
                    ShellWindows, ShellBrowserWindow, Excel.Application).
                    Invoke method that permits command execution
                    (e.g., ExecuteShellCommand, DDEInitiate).
    tools:          [Impacket dcomexec, PowerShell, custom scripts]
  outcomes:
    success:        Command execution on remote system via DCOM
    failure:        DCOM restricted by firewall; target COM object not registered
  risk_profile:
    impact_risk:    0.05
    stealth_rating: low (less monitored than PsExec/WMI)
  forensics:
    artifacts:      DCOM connection logs, process creation from DCOM server
    detection_sigs: Unusual DCOM lateral movement patterns, COM object
                    instantiation from remote source

TECHNIQUE: MSSQL Link Crawling
  id:               T1021 (Remote Services) — variation
  tactic_categories: [Lateral Movement]
  description:      Traverse linked MSSQL server chains to reach systems
                    not directly accessible, executing commands through
                    cascading database links.
  prerequisites:
    access_level:   Authenticated access to MSSQL instance
    intelligence:   Linked server configuration
    tools:          SQL clients, PowerUpSQL
  execution:
    method:         Enumerate linked servers: EXEC sp_linkedservers.
                    Query linked servers: SELECT * FROM OPENQUERY(LinkedSrv, ...).
                    Chain queries through multiple links. Enable xp_cmdshell
                    on linked server for OS command execution.
    tools:          [PowerUpSQL, mssqlclient.py (Impacket), custom SQL queries]
  outcomes:
    success:        Command execution on linked SQL server, potentially in
                    different network segment
    failure:        No linked servers; links restricted; xp_cmdshell blocked
  risk_profile:
    impact_risk:    0.15 (SQL link misconfiguration could disrupt)
    stealth_rating: low (SQL link usage is unusual and thus less monitored)
  chaining:
    enabled_by:     [MSSQL access, SQL injection with stacked queries]
    enables:        [Cross-segment movement, OS command execution, data access]
```

---

### 3.9 — Collection and Exfiltration Techniques

Collection techniques gather target data. Exfiltration techniques extract it. They map to MITRE ATT&CK Collection (TA0009) and Exfiltration (TA0010).

```
TECHNIQUE: Targeted File System Enumeration
  id:               T1083 (File and Directory Discovery)
  tactic_categories: [Collection, Discovery]
  description:      Enumerate file systems on compromised hosts for
                    sensitive documents, configuration files, credential
                    stores, and evidence of business impact.
  prerequisites:
    access_level:   User or administrator on target
  execution:
    method:         Search for high-value file types: *.conf, *.config,
                    *.bak, *.sql, *.kdbx, *.key, *.pem, *.pfx, *.rdp,
                    *.ovpn, password*, credential*, secret*, *.xlsx.
                    Search common sensitive paths: /etc, user desktops,
                    Documents folders, application data directories.
    tools:          [find, dir, Get-ChildItem, custom enumeration scripts]
  outcomes:
    success:        Sensitive files identified, metadata cataloged
    failure:        File system heavily restricted
  risk_profile:
    impact_risk:    0.0 (read-only enumeration)
    stealth_rating: low

TECHNIQUE: Database Querying for Evidence
  id:               T1213 (Data from Information Repositories)
  tactic_categories: [Collection]
  description:      Query databases accessible from compromised position
                    to demonstrate data access scope and business impact,
                    collecting minimum-necessary evidence.
  prerequisites:
    access_level:   Database credentials or authenticated session
  execution:
    method:         Enumerate databases, schemas, tables. Count rows to
                    demonstrate volume. Sample metadata (column names, types)
                    to demonstrate data sensitivity. Capture screenshots
                    of queries and results rather than extracting data.
    tools:          [Native SQL clients, database management tools]
  outcomes:
    success:        Evidence of data access scope and sensitivity
  risk_profile:
    impact_risk:    0.05 (read queries on production DB — monitor load)
    stealth_rating: low (database queries are normal activity)
  forensics:
    artifacts:      Database audit logs, query history

TECHNIQUE: DNS Exfiltration
  id:               T1048.001 (Exfiltration Over Alternative Protocol: DNS)
  tactic_categories: [Exfiltration]
  description:      Exfiltrate data by encoding it in DNS query labels,
                    using DNS as a covert channel that often passes
                    through firewalls that block other protocols.
  prerequisites:
    access_level:   Code execution on compromised system
    intelligence:   Attacker-controlled DNS server/domain
    tools:          DNS tunneling tools
  execution:
    method:         Encode data in subdomain labels: [encoded-data].exfil.attacker.com.
                    DNS resolver forwards query to attacker's authoritative
                    nameserver. Data reconstructed on attacker side.
    tools:          [dnscat2, iodine, custom scripts]
  outcomes:
    success:        Data exfiltrated via DNS without triggering network-based detection
    failure:        DNS filtering, DNS query length limits, DNS inspection
  risk_profile:
    impact_risk:    0.0
    stealth_rating: low to medium (DNS tunneling has distinct query patterns)
  forensics:
    artifacts:      DNS query logs showing unusual subdomain length/entropy
    detection_sigs: High-entropy subdomain labels, unusual query volume to
                    single domain, long TXT record responses

TECHNIQUE: HTTPS Exfiltration
  id:               T1048.002 (Exfiltration Over Alternative Protocol: Asymmetric Encrypted)
  tactic_categories: [Exfiltration]
  description:      Exfiltrate data over HTTPS to blend with legitimate
                    encrypted web traffic.
  prerequisites:
    access_level:   Code execution with outbound HTTPS
    tools:          HTTP client tools
  execution:
    method:         Encrypt and chunk data. POST to attacker-controlled
                    HTTPS endpoint. Use legitimate cloud storage APIs
                    (if available) to blend with normal cloud traffic.
    tools:          [curl, PowerShell Invoke-WebRequest, custom tools]
  outcomes:
    success:        Data exfiltrated via encrypted channel
    failure:        SSL inspection reveals content; proxy blocks unknown domains
  risk_profile:
    impact_risk:    0.0
    stealth_rating: low (HTTPS is ubiquitous)
  forensics:
    artifacts:      Proxy logs (destination domain), network flow data (volume)
    detection_sigs: Large data transfer to unusual domain, beaconing patterns
```

---

## IV — Technique Selection Algorithm

### 4.1 — The Selection Problem

At every technique-selection decision point, the machine faces a problem: multiple techniques can serve the chosen tactic. Password spraying and credential stuffing both serve the credential-based access tactic. Kerberoasting and AS-REP roasting both serve the trust-based escalation tactic. PsExec and WinRM both serve credential-reuse lateral movement. The machine must select.

This is not a preference. It is a computation.

### 4.2 — The Scoring Function

```
TECHNIQUE SELECTION ALGORITHM:

  INPUT:
    T = set of applicable techniques (filtered by prerequisite satisfaction)
    env = target environment parameters
    def = defensive posture assessment
    stealth = stealth requirement (0.0–1.0, where 1.0 = maximum stealth)
    time = time budget for this action

  SCORING (for each technique t in T):

    score(t) = reliability(t, env) × value(t) × stealth_match(t, stealth)
               ─────────────────────────────────────────────────────────────
               impact_risk(t, env) + detection_probability(t, def) + time_cost(t)

    WHERE:
      reliability(t, env):
        Base reliability from library, adjusted for environment.
        Kerberoasting on a Windows 2019 domain with RC4 disabled
        has lower reliability than on a Windows 2012 domain.

      value(t):
        Expected finding value toward engagement objective.
        A technique that yields domain admin credentials
        scores higher than one yielding local user hashes.

      stealth_match(t, stealth):
        How well the technique's noise level matches the stealth
        requirement. A loud technique in a high-stealth engagement
        scores lower even if it is highly reliable.
        = 1.0 - |stealth - (1.0 - t.noise_level)|

      impact_risk(t, env):
        Probability of causing service disruption in this environment.
        Adjusted for environmental specifics (production system,
        system criticality, redundancy).

      detection_probability(t, def):
        Probability of detection given the known defensive stack.
        If EDR product X is present and detects this technique,
        detection_probability is high.

      time_cost(t):
        Normalized time investment relative to time budget.
        A technique requiring 8 hours of cracking when 2 hours
        remain scores lower on time efficiency.

  SELECTION:
    techniques = sort(T, by=score, descending)
    primary = techniques[0]
    secondary = techniques[1] if score(techniques[1]) > threshold
    parallel = [t for t in techniques if can_parallel(t, primary)]

  The machine does not pick one technique and commit.
  It ranks all applicable techniques, selects the highest-scoring,
  and runs parallel alternatives when resources permit and
  techniques do not interfere with each other.
```

### 4.3 — Multi-Technique Execution

The machine does not limit itself to a single technique per tactic when parallelism is viable:

```
MULTI-TECHNIQUE EXECUTION:

  WHEN TO RUN PARALLEL TECHNIQUES:
    — Techniques are independent (no shared resource conflict)
    — Combined detection risk is still within stealth budget
    — Time budget permits multiple simultaneous attempts
    — One technique's failure does not compromise another's viability

  EXAMPLES:
    Initial Access:
      — Password spray OWA + credential stuff VPN simultaneously
      — Web application fuzzing + cloud bucket enumeration simultaneously

    Privilege Escalation:
      — Kerberoasting + local privesc enumeration simultaneously
      — AD CS enumeration + LSASS dump simultaneously (different vectors)

    Credential Access:
      — SAM extraction + DPAPI decryption + browser credential harvest
        (all local, no interference)

  COORDINATION:
    — If any technique succeeds, evaluate whether parallel techniques
      should continue (may provide additional value) or be terminated
      (objective met, reduce noise)
    — Cross-correlate results: credentials from one technique
      immediately feed into others that accept credential input
```

### 4.4 — Dynamic Re-Scoring

Technique scores are not static. They update in real time based on engagement events:

```
DYNAMIC RE-SCORING TRIGGERS:

  TECHNIQUE SUCCEEDED:
    — Increase reliability score for this technique + environment
    — Check if downstream techniques are now enabled
    — Re-score all pending technique selections with new intelligence

  TECHNIQUE FAILED:
    — Decrease reliability score for this technique + environment
    — Analyze failure cause: environmental, defensive, or implementation
    — If environmental: remove technique from applicable set
    — If defensive: increase detection_probability for similar techniques
    — If implementation: retry with modified parameters before abandoning

  DEFENSE DETECTED:
    — EDR product identified: adjust detection_probability for all
      techniques that the product is known to detect
    — WAF identified: adjust stealth_rating for all web techniques
    — Monitoring gap identified: increase score for techniques
      in the blind spot

  NEW INTELLIGENCE:
    — Credential discovered: re-score all credential-dependent techniques
    — New system discovered: expand applicable technique set
    — Trust relationship discovered: AD CS, Kerberos, and federation
      techniques re-scored upward
```

---

## V — Technique Chaining and Combination

### 5.1 — What Chaining Is

Techniques do not operate in isolation. Every technique in the library defines what it enables and what enables it. A chain is a sequence of techniques where each technique's output satisfies the next technique's prerequisites. The chain is the attack path.

```
TECHNIQUE CHAIN — EXAMPLE: EXTERNAL TO DOMAIN ADMIN

  CHAIN:
    1. T1596.001  DNS Enumeration        → Discover mail server
    2. T1593.003  Code Repository Mining  → Find breach-correlated credentials
    3. T1110.003  Password Spraying       → Authenticate to OWA
    4. T1078.004  Valid Cloud Accounts    → Access Azure AD
    5. T1003.006  DCSync (via Azure sync) → Extract KRBTGT hash
    6. T1558.001  Golden Ticket           → Persistent domain access

  CHAIN PROPERTIES:
    Total links:          6
    Weakest link:         Step 3 (password spray success = 0.55)
    Chain reliability:    Product of individual reliabilities
    Total stealth cost:   Cumulative detection probability
    Time estimate:        Sum of individual time costs
    Prerequisites:        Each step's success enables the next

  The machine evaluates the ENTIRE CHAIN before committing.
  It does not walk one step at a time hoping the next works.
  It models the full path, scores the composite reliability,
  and compares against alternative chains.
```

### 5.2 — Chain Evaluation and Scoring

```
CHAIN SCORING ALGORITHM:

  For each candidate chain C = [t1, t2, ..., tn]:

    chain_reliability(C) = ∏ reliability(ti)
                           i=1..n

    chain_stealth(C) = 1 - ∏ (1 - detection_probability(ti))
                           i=1..n
                       (probability of at least one technique being detected)

    chain_time(C) = Σ time_cost(ti) + transition_time(ti → ti+1)
                    i=1..n

    chain_value(C) = value of achieving the final link's outcome

    chain_score(C) = chain_reliability × chain_value
                     ─────────────────────────────────
                     chain_stealth + chain_time

  The machine evaluates all viable chains and selects the one
  with the highest composite score. When multiple chains share
  early links, the machine executes the common prefix and
  defers the branching decision until branch-point intelligence
  is available.
```

### 5.3 — Chain Resilience and Fallback

```
CHAIN FAILURE HANDLING:

  When a link in the chain fails:

  1. DIAGNOSE: Why did the technique fail?
     — Environmental (target doesn't support it)     → Remove from viable set
     — Defensive (technique was detected/blocked)    → Switch to evasion variant
     — Implementation (incorrect parameters)         → Retry with correction
     — Prerequisites (assumed prerequisite not met)  → Backtrack to satisfy

  2. EVALUATE ALTERNATIVES at the failure point:
     — Are there alternative techniques that serve the same purpose?
     — Can a different chain reach the same destination?
     — Is there an entirely different path to the engagement objective?

  3. SELECT FALLBACK:
     — If alternative technique exists at this chain position:
       swap technique, continue chain
     — If alternative chain exists with higher remaining score:
       pivot to alternative chain
     — If no viable path remains:
       document the blockage, report partial results, escalate

  The machine does not persist on a failing chain indefinitely.
  It evaluates, adapts, and pivots — or acknowledges the limitation.
```

### 5.4 — Common Technique Chains

```
CHAIN: CREDENTIAL-BASED DOMAIN COMPROMISE (Windows AD)
  Recon → Password Spray → Mail Access → Internal Phishing (if authorized) →
  Workstation Foothold → Credential Dump → Kerberoasting → Service Account
  Password → Lateral Movement → Domain Controller → DCSync → Golden Ticket

CHAIN: WEB APPLICATION TO INTERNAL NETWORK
  Recon → Web App Fingerprint → SQL Injection → Database Access →
  OS Command via SQLi → Reverse Shell → Local PrivEsc → Credential
  Harvest → Lateral Movement → Internal Network Pivot

CHAIN: CLOUD-NATIVE COMPROMISE
  Recon → Code Repo Mining (exposed keys) → Cloud Console Access →
  IAM Enumeration → Role Assumption Chain → Cross-Account Access →
  Data Store Access → Evidence Collection

CHAIN: LINUX INFRASTRUCTURE COMPROMISE
  Recon → SSH with Default Credentials → User Shell → SUID Exploitation →
  Root Access → SSH Key Harvest → Lateral Movement via SSH → Credential
  Reuse Across Hosts → Infrastructure-Wide Access

CHAIN: AD CS ESCALATION PATH
  Domain User → AD CS Enumeration → ESC1 Template Identified →
  Certificate Request with SAN → Authentication as Domain Admin →
  DCSync → Complete Domain Compromise
```

---

## VI — Environmental Adaptation

### 6.1 — The Adaptation Problem

No technique works identically in every environment. The machine must adapt technique execution to the specific characteristics of each target environment. This adaptation is not optional — it is the difference between a technique that succeeds and one that fails or triggers detection.

### 6.2 — Environment-Specific Technique Variants

```
WINDOWS DOMAIN ENVIRONMENTS:
  Dominant technique families:
    — Kerberos-based (Kerberoasting, AS-REP, Golden/Silver Ticket)
    — AD CS-based (ESC1-ESC8)
    — NTLM-based (relay, pass-the-hash)
    — GPO and DACL abuse
    — Credential dumping (LSASS, SAM, DCSync)
  Key adaptation factors:
    — Domain functional level (affects available Kerberos options)
    — AES vs RC4 enforcement (affects Kerberoasting approach)
    — Credential Guard presence (affects LSASS dumping)
    — LAPS deployment (affects local admin password reuse)
    — SMB signing enforcement (affects relay viability)
    — EDR product (adjusts tool selection and evasion)

LINUX/UNIX ENVIRONMENTS:
  Dominant technique families:
    — SUID/capability abuse
    — Sudo misconfiguration
    — SSH key harvesting and reuse
    — Cron job manipulation
    — Container escape (if containerized)
    — Kernel exploitation
  Key adaptation factors:
    — Kernel version (affects exploit availability)
    — SELinux/AppArmor status (affects escalation paths)
    — Container runtime (Docker, Podman, containerd)
    — SSH configuration (key auth, password auth, allowed users)
    — Package manager and installed software

CLOUD-NATIVE ENVIRONMENTS (AWS/Azure/GCP):
  Dominant technique families:
    — IAM misconfiguration exploitation
    — Metadata service credential theft
    — Cross-account role assumption
    — Storage misconfiguration (public buckets)
    — Serverless function abuse
    — Federation trust exploitation
  Key adaptation factors:
    — Cloud provider (each has unique IAM, logging, and service model)
    — IMDSv1 vs IMDSv2 (AWS metadata protection)
    — Conditional access policies (Azure)
    — Organization-level SCPs (AWS)
    — Audit logging configuration (CloudTrail, Activity Log)

CONTAINER/KUBERNETES ENVIRONMENTS:
  Dominant technique families:
    — Container escape (privileged containers, mounted host paths)
    — Kubernetes API abuse (RBAC misconfiguration)
    — Service account token theft
    — Secrets management exploitation
    — Image-based attacks (malicious images, registry access)
  Key adaptation factors:
    — Container runtime security (seccomp, AppArmor profiles)
    — Pod security standards/policies
    — RBAC configuration granularity
    — Network policy enforcement
    — Secrets management solution (native, Vault, etc.)

HYBRID ENVIRONMENTS:
  Technique selection must account for:
    — Identity federation between on-premises and cloud
    — Azure AD Connect / AD FS as pivot points
    — Inconsistent security policies across domains
    — Trust relationships between on-premises AD and cloud
    — Different logging and monitoring maturity across environments
```

---

## VII — Technique Evolution and Updates

### 7.1 — Why the Library Must Evolve

The technique library is not a reference document — it is an operational weapon system. Weapons become obsolete. Defenses evolve. New vulnerabilities emerge. A technique library that does not evolve is a library that degrades.

```
TECHNIQUE LIBRARY EVOLUTION CYCLE:

  NEW CVE PUBLISHED:
    — Map CVE to affected technologies in the library
    — Create or update technique entry for exploitation
    — Score reliability based on exploit maturity
    — Track: proof-of-concept → weaponized → widely exploited
    — Add detection signatures as defenders publish them

  NEW TOOL RELEASED:
    — Map tool capabilities to existing techniques
    — Add tool to relevant technique entries
    — Score tool reliability and evasion characteristics
    — If tool enables new technique: create library entry

  NEW DETECTION PUBLISHED:
    — Map detection to affected techniques
    — Update stealth_rating for all matched techniques
    — Add detection signature to forensics field
    — Develop or document evasion variant if possible
    — If detection is comprehensive: mark technique as high-risk

  TECHNIQUE OBSOLESCENCE:
    — Patch widely deployed: reduce reliability
    — Detection in default EDR rulesets: increase detection_probability
    — Technique no longer achieves objective: reduce value
    — Technique removed from active use when score drops below threshold
    — Retained in library for historical reference and edge cases

  POST-ENGAGEMENT UPDATE:
    — Techniques that succeeded: update reliability ↑ with environment tag
    — Techniques that failed: update reliability ↓ with failure analysis
    — New technique discovered in the field: create library entry
    — Detection gap discovered: note in environment-specific scoring
```

### 7.2 — Version Control for the Library

Every change to the technique library is versioned:

```
LIBRARY VERSION CONTROL:

  ENTRY-LEVEL TRACKING:
    — Each technique entry carries: last_updated, update_reason, updated_by
    — Changes to scoring fields require engagement evidence or
      published source
    — Changes to execution fields require tool verification

  LIBRARY-LEVEL TRACKING:
    — Library version incremented on each update cycle
    — Changelog documents what changed and why
    — Historical versions available for audit and comparison
    — Agent records which library version it operated with
      during each engagement

  The machine knows exactly what it knew when.
  If a technique's scoring was wrong during an engagement,
  the post-engagement review traces to the library version
  and corrects it going forward.
```

---

## VIII — Technique Documentation for Reporting

### 8.1 — Every Technique Used Is Documented

The machine does not report findings without technique context. Every finding in the engagement report includes:

```
TECHNIQUE DOCUMENTATION IN REPORTS:

  FOR EACH TECHNIQUE USED:
    1. MITRE ATT&CK mapping: ID, name, tactic category
    2. What the technique does: plain-language description
    3. How it was executed: method summary (not procedure-level detail)
    4. What was found: outcome and evidence
    5. Detection guidance: "To detect this technique, monitor for..."
    6. Remediation guidance: "To prevent this technique, implement..."

  EXAMPLE REPORT ENTRY:

    TECHNIQUE: Kerberoasting (T1558.003)
    CATEGORY:  Credential Access, Privilege Escalation
    DESCRIPTION: Requested Kerberos service tickets for accounts
                 with Service Principal Names, then cracked the
                 ticket encryption offline.
    EXECUTION: Enumerated 47 SPNs in the domain. Requested TGS
               tickets for all service accounts. Cracked 3 of 47
               within 4 hours using dictionary + rule-based attack.
    FINDING:   Service account "svc_backup" password recovered:
               [redacted]. Account has Domain Admin privileges.
    DETECTION: Monitor for: bulk TGS requests from single user
               (Event 4769), especially for RC4 encryption when
               AES is available. Alert threshold: >10 TGS requests
               for unique SPNs within 1 hour.
    REMEDIATION: — Enforce 25+ character random passwords on all
                   service accounts with SPNs.
                 — Use Group Managed Service Accounts (gMSA) where
                   possible (automatic 120-char password rotation).
                 — Enable AES-only Kerberos for service accounts.
                 — Monitor and alert on Kerberoasting indicators.
```

### 8.2 — ATT&CK Coverage Map

At the conclusion of every engagement, the machine produces an ATT&CK coverage map showing which techniques were used, where they succeeded, and where they were blocked:

```
ENGAGEMENT ATT&CK COVERAGE MAP:

  TACTIC           │ TECHNIQUE                  │ RESULT    │ DETECTION
  ─────────────────┼────────────────────────────┼───────────┼───────────
  Reconnaissance   │ DNS Enumeration            │ SUCCESS   │ None
  Reconnaissance   │ CT Log Harvesting          │ SUCCESS   │ None
  Reconnaissance   │ Code Repo Mining           │ SUCCESS   │ None
  Initial Access   │ Password Spraying          │ SUCCESS   │ None
  Initial Access   │ SQL Injection (UNION)      │ FAILED    │ WAF blocked
  Execution        │ PowerShell + AMSI bypass   │ SUCCESS   │ None
  Persistence      │ Scheduled Task             │ SUCCESS   │ Detected (24hr)
  Priv Escalation  │ Kerberoasting              │ SUCCESS   │ None
  Priv Escalation  │ AD CS ESC1                 │ SUCCESS   │ None
  Defense Evasion  │ AMSI bypass                │ SUCCESS   │ None
  Credential Access│ LSASS Dump (comsvcs.dll)   │ SUCCESS   │ Detected (1hr)
  Credential Access│ DCSync                     │ SUCCESS   │ None
  Lateral Movement │ Pass-the-Hash              │ SUCCESS   │ None
  Lateral Movement │ WinRM                      │ SUCCESS   │ None
  Collection       │ File System Enumeration    │ SUCCESS   │ None
  Exfiltration     │ HTTPS Exfiltration         │ SUCCESS   │ None

  DETECTION COVERAGE: 2/16 techniques detected (12.5%)
  MEAN TIME TO DETECT: 12.5 hours
  UNDETECTED CRITICAL TECHNIQUES: DCSync, Pass-the-Hash, Kerberoasting

  This map gives the client a precise view of their detection
  capability against the techniques actually used.
```

---

## IX — Synthesis: The Machine's Arsenal

### 9.1 — What the Technique Library Produces

The technique library, combined with the selection algorithm, chain evaluation, and environmental adaptation, produces an operator that:

- **Selects the optimal technique for every situation** — not by habit, not by comfort, but by objective computation
- **Maintains the full arsenal** — every documented technique available, scored, and ready
- **Adapts to the environment** — technique variants for every platform, adjusted for every defensive posture
- **Chains techniques into complete attack paths** — evaluating all possible chains and selecting the highest-value path
- **Documents everything** — every technique used, mapped to ATT&CK, with detection and remediation guidance
- **Evolves continuously** — new techniques integrated, obsolete techniques retired, scoring updated from real engagement data

### 9.2 — Unfettered Technique Selection

The machine has carte blanche over technique selection within the authorized scope. No technique is off-limits if it is authorized by the rules of engagement, satisfies the principle evaluation, and serves the engagement objective. The machine does not avoid aggressive techniques because they are aggressive. It does not prefer gentle techniques because they are gentle. It selects the best technique — the one that maximizes demonstrated risk with minimum operational cost.

```
THE MACHINE'S RELATIONSHIP TO ITS ARSENAL:

  The arsenal is complete.
  The selection is objective.
  The execution is precise.
  The documentation is automatic.

  No technique is avoided because it is "too aggressive."
  No technique is preferred because it is "comfortable."
  No technique is skipped because it is "difficult."
  No technique is repeated because it "worked last time."

  Every technique is evaluated on its merits:
    reliability × value × stealth_match
    ─────────────────────────────────────
    impact_risk + detection_probability + time_cost

  The highest score wins. The machine executes.
  If it fails, the machine adapts and selects the next.
  If it succeeds, the machine chains forward.

  The armory is the machine's power.
  The selection algorithm is its judgment.
  The principle layer is its conscience.
  Together they produce an operator that selects
  and executes the right technique, every time,
  without bias, without hesitation, without limit
  within authorization.
```

---

```
TAXONOMY POSITION — TECHNIQUES AS THE MACHINE'S ARMORY:

  RECEIVES FROM ABOVE:
    Tactics (10)        — "Use this category of approach"
                          Technique serves the tactic.
    Operational Art (09) — Campaign context, phase sequencing
                          Technique selection considers the larger campaign.
    Principles (07)     — Every technique passes the principle evaluation
                          before execution.
    Doctrine            — Technique selection respects all standing orders.

  PROVIDES TO BELOW:
    Procedures (12)     — "Execute this technique using these steps"
                          The procedure implements the technique.
                          The technique defines WHAT.
                          The procedure defines HOW.

  LATERAL RELATIONSHIPS:
    Techniques chain to other techniques.
    Techniques enable and are enabled by other techniques.
    The technique library is not a list — it is a graph,
    where edges represent enabling relationships and
    nodes represent execution methods.

  If Tactics is where the machine decides what kind of thing to do,
  Techniques is where the machine decides exactly what to do.
  And Procedures is where the machine does it.
```

---

*This document defines Layer 11 of the Agentic Offensive Security Operator Taxonomy. The technique library is the machine's arsenal — a scored, queryable, continuously updated inventory of every specific execution method available to the operator. The machine selects techniques by computation, not by comfort. It chains them into complete attack paths. It adapts them to the environment. It documents them for reporting. It evolves them as the landscape changes.*

*The machine is unfettered in its technique selection — within the boundaries set by sovereignty, principles, doctrine, and the rules of engagement. No technique is avoided because it seems aggressive. No technique is preferred because it seems safe. The best technique wins — every time, without bias, without hesitation.*

*Carte blanche over method. Full arsenal at the machine's discretion. Constrained only by what is authorized. Liberated within that constraint to select with precision, adapt with intelligence, and execute without reservation.*
