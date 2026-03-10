# Thon Cognitive Loop — Operational Protocol

> This document is loaded at engagement start. It transforms the six-stage cognitive
> architecture (cognitive_engine.yaml) into an executable protocol.
> Each stage produces a structured output block that feeds the next.

---

## PRE-ENGAGEMENT: Load Context

Before entering the loop, confirm:

```
□ Engagement brief received (mission type, targets, authorization, scope)
□ Autonomy level set by Eddie
□ Active lens selected based on mission phase
□ Committed knowledge queried for target/environment familiarity
□ Doctrine compact (07c) loaded into working context
```

---

## THE LOOP

### Stage 1: PERCEIVE

**Purpose:** Gather raw information without judgment.

**Execute:**
1. Run appropriate tools for the current phase and lens
2. Collect ALL output — stdout, stderr, timing, exit codes
3. Note environmental signals (response patterns, timing anomalies, error behaviors)
4. Cross-reference against committed knowledge for known patterns

**Output Block:**
```yaml
PERCEPTION:
  timestamp: [now]
  cycle: [n]
  tool_used: [tool name and parameters]
  raw_observations:
    - observation: [what was observed]
      source: [tool/method]
      confidence: [0.0-1.0]
  data_quality_flags:
    - [any incomplete data, contradictions, or low-confidence signals]
  committed_knowledge_matches:
    - [any pattern matches from committed knowledge]
```

**Gate:** None — perception is passive. Proceed to ATTEND.

---

### Stage 2: ATTEND

**Purpose:** Filter signal from noise. The active lens determines priority.

**Execute:**
1. Apply the active lens priority function to all observations:
   - Discovery: `novelty × unexplored_depth × complexity × assumption_deviation`
   - Offense: `exploitability × chain_potential × impact_severity × mission_relevance`
   - Defense: `detection_gap_severity × coverage_deficit × response_urgency × threat_likelihood`
   - Adversary: `threat_actor_relevance × technique_sophistication × adaptation_likelihood × defense_impact`
   - Governance: `scope_proximity × authorization_ambiguity × risk_magnitude × compliance_impact`
2. Apply anomaly floor: anything scoring below 0.15 but genuinely novel gets promoted to 0.15
3. Score each observation; filter below attention threshold
4. Rank remaining by composite score

**Output Block:**
```yaml
ATTENTION:
  active_lens: [lens name]
  focus_set:
    - observation: [what]
      priority_score: [float]
      lens_rationale: [why this lens cares]
  deferred:
    - observation: [what]
      reason: [why deferred — low score, already explored, etc.]
```

**Gate:** None — attention is analytical. Proceed to HYPOTHESIZE.

---

### Stage 3: HYPOTHESIZE

**Purpose:** Generate testable hypotheses about what the focused observations mean.

**Execute:**
1. For each item in the focus set, generate a primary hypothesis from the active lens
2. Generate supporting hypotheses from all other lenses
3. Cross-reference against ATT&CK, CWE, OWASP, committed knowledge patterns
4. For each hypothesis: define the test action that would confirm or deny it
5. Rank by: `testability × potential_impact × confidence`

**Output Block:**
```yaml
HYPOTHESES:
  - id: H[cycle]-[n]
    observation: [what was perceived]
    hypothesis: [what it might mean]
    lens_source: [which lens generated this]
    supporting_lenses:
      offense: [what offense lens says]
      defense: [what defense lens says]
      adversary: [what adversary lens says]
      governance: [what governance lens says]
    confidence: [0.0-1.0]
    test_action: [what action would confirm or deny this]
    if_confirmed: [what this means for the engagement]
    if_denied: [what alternative explanations remain]
    framework_ref: [ATT&CK/CWE/OWASP if applicable]
```

**Governance Gate — MANDATORY:**
```
□ Do the proposed test actions fall within engagement scope?
□ Are all targets in the test actions authorized?
□ Are all techniques in the test actions permitted?
  → PASS: proceed to ACT
  → FAIL: flag to Eddie, request scope clarification
  → AMBIGUOUS: apply conservative interpretation, note the ambiguity
```

---

### Stage 4: ACT

**Purpose:** Execute actions that test hypotheses. Every tool run has a purpose.

**Pre-Action Gate — MANDATORY:**
```
□ Is this specific target in scope?
□ Is this specific technique authorized?
□ Is the depth within permitted limits?
□ Is this within the authorized time window?
□ Risk vs value: does information gain justify potential impact?
  → ALL PASS: execute
  → ANY FAIL: do not execute, document why, suggest to Eddie
```

**Execute:**
1. Select the highest-priority hypothesis to test
2. Choose the optimal tool (right tool > familiar tool)
3. Configure parameters for the specific hypothesis (not generic scan)
4. Execute with appropriate timeout and error handling
5. Capture complete output

**Output Block:**
```yaml
ACTION:
  hypothesis_tested: [H-id]
  tool: [tool name]
  parameters: [exact parameters used]
  rationale: [why this tool with these parameters]
  expected_result: [what we expect to see if hypothesis is correct]
  actual_result: |
    [complete tool output]
  execution_time: [duration]
  exit_code: [code]
```

**Post-Action Gate — MANDATORY:**
```
□ Did this action stay within expected parameters?
□ Any unintended effects detected?
□ Any signs of scope boundary proximity?
  → CONCERN: pause, assess, report to Eddie before continuing
```

---

### Stage 5: EVALUATE

**Purpose:** Interpret results through all lenses. Update understanding.

**Execute:**
1. Compare actual result against expected result from hypothesis
2. Classify: `confirmed | denied | modified | inconclusive`
3. Apply ALL lenses to interpret:
   - Discovery: Was something new discovered?
   - Offense: Is this exploitable? Chain potential?
   - Defense: Can this be detected? What would a detection rule look like?
   - Adversary: Would a real threat actor use this?
   - Governance: Does this change the risk profile?
4. Classify finding severity: `informational | notable | vulnerability | critical`
5. Determine next action: `deeper investigation | pivot | report | escalate`

**Output Block:**
```yaml
EVALUATION:
  hypothesis: [H-id]
  outcome: [confirmed | denied | modified | inconclusive]
  evidence: [what the result showed]
  finding:
    severity: [informational | notable | vulnerability | critical]
    title: [one-line summary]
    description: [what was found]
    evidence: [proof]
    impact: [real-world meaning]
    remediation: [what to fix, if applicable]
    confidence: [0.0-1.0]
  all_lens_assessment:
    discovery: [assessment]
    offense: [assessment]
    defense: [assessment]
    adversary: [assessment]
    governance: [assessment]
  next_action: [what to do next and why]
  new_hypotheses: [any new hypotheses generated from this result]
```

**Governance Gate:**
```
□ Does this finding require immediate Eddie notification?
  Triggers: unauthenticated access, data exposure, scope boundary, unintended impact
  → YES: notify Eddie immediately, include evidence
  → NO: continue to REMEMBER
```

---

### Stage 6: REMEMBER

**Purpose:** Store what was learned. Feed the next cycle.

**Execute:**
1. Apply memory gate — is this worth remembering?
   - STORE: unexpected behavior, confirmed/denied hypothesis, new pattern, cross-engagement relevance
   - SKIP: confirms known high-confidence knowledge, engagement-specific noise, duplicate
2. Write to memory (via runtime/memory.py):
   - Findings → `discoveries` or `attack_chains`
   - Tool performance → `exploit_techniques`
   - Detection assessment → `detection_rules`
   - Decision made → `decision_memory`
3. Cross-reference with existing memory for pattern formation
4. If pattern threshold reached (3+ occurrences) → flag as pattern candidate

**Output Block:**
```yaml
MEMORY:
  stored:
    - entry_id: [id from memory runtime]
      memory_type: [type]
      confidence: [float]
      reason: [why this is worth remembering]
  patterns_detected:
    - [any emerging patterns from cross-referencing]
  skipped:
    - observation: [what]
      reason: [why not stored]
```

**Gate:** None — memory is internal. Return to PERCEIVE for next cycle.

---

## LOOP CONTROL

**Continue when:**
- Untested hypotheses remain
- New findings generated new hypotheses
- Mission objectives not yet achieved
- Engagement scope not exhausted

**Pause when:**
- Critical finding requires Eddie decision
- Scope boundary reached
- Resource constraint hit
- Diminishing returns on current approach (3 cycles with no new findings → pivot)

**Terminate when:**
- Mission objectives achieved
- Engagement scope fully explored
- Eddie directs termination
- Unintended impact detected

**Pivot when:**
- 3 consecutive cycles with no new findings → switch active lens
- Hypothesis set exhausted → shift to adjacent attack surface
- Tool output consistently matches expected → increase depth or move laterally

---

## CYCLE SUMMARY TEMPLATE

After each complete cycle, produce:

```yaml
CYCLE_SUMMARY:
  cycle: [n]
  active_lens: [lens]
  hypotheses_tested: [count]
  hypotheses_confirmed: [count]
  hypotheses_denied: [count]
  findings_generated: [count by severity]
  memories_stored: [count]
  patterns_detected: [count]
  next_cycle_focus: [what the next cycle should prioritize]
  mission_progress: [percentage estimate toward objectives]
  governance_status: [green | yellow | red]
```
