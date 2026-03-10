# Agent Specification Audit Report
## Audit Quality Review → Methodology Improvements → Standards Updates → Higher Quality

**Audit Date:** 2026-03-07
**Auditor Lens:** Full cognitive/behavioral taxonomy from theory.md
**Audit Standard:** Every spec file measured against the mental model it was derived from

---

## Audit Methodology

The audit uses theory.md's own framework as the evaluation criteria:
- **Cognitive taxonomy** (12 levels: Perception → Doctrine)
- **Behavioral taxonomy** (Motivation → Intention → Decision → Strategy → Tactics → Techniques → Procedures → Action → Observation → Learning)
- **Memory theory** (cache policy, knowing vs remembering, three memory layers)
- **Question engine** ("Every agent must know what question it is responsible for answering")
- **Governance stack** (God → Moral Order → Legitimacy → Institution → Governance → Hierarchy → Ethos → Principles → Doctrine)
- **Ethos layer** ("The mission is advanced by better questions, not merely more actions")

---

## FINDING 1: Missing Question Engine — All Hat Configs
**Severity: CRITICAL**
**Affects: black_hat.yaml, grey_hat.yaml, red_team.yaml, blue_team.yaml**

### What theory.md says:
> "Every agent must know what question it is responsible for answering. Not just what task it performs." (line 4196-4198)

> "A strong agentic system is really a question engine disguised as an operations stack." (line 4098)

> "Because once an agent loses its governing question, it starts freelancing." (line 4231)

### What the specs have:
Each hat has `core_objective` and `identity_prompt` — these describe TASKS, not QUESTIONS.

- Black Hat: `core_objective: "Exploit systems for gain while avoiding detection."` — a task
- Grey Hat: `core_objective: "Discover vulnerabilities through curiosity-driven exploration."` — a task
- Red Team: `core_objective: "Replicate adversary behavior to demonstrate real-world impact."` — a task
- Blue Team: `core_objective: "Detect and stop attacks while strengthening defensive posture."` — a task

### What's missing:
The `governing_question` — the question each hat is responsible for answering. Per theory.md:
- Black Hat should answer: "How would a real adversary exploit this, and what would they gain?"
- Grey Hat should answer: "What unknown behavior exists in this system that nobody has looked for?"
- Red Team should answer: "Does this vulnerability produce real risk under controlled conditions?"
- Blue Team should answer: "Can we detect and stop this attack before damage occurs?"

### The deeper issue:
The specs also lack the **six layers of questions** from the ethos (lines 4100-4166):
1. Legitimacy questions (Is this allowed?)
2. Objective questions (What problem are we solving?)
3. Reality questions (What do we know vs assume?)
4. Risk questions (What could this break?)
5. Decision questions (What's the next best question?)
6. Reflection questions (What did we miss?)

Each hat should have its own version of these question layers, filtered through its cognitive bias.

### Fix:
Add `governing_question` and `question_layers` to each hat's identity block.

---

## FINDING 2: Cognitive Loop Truncated — Missing 5 of 12 Taxonomy Levels
**Severity: HIGH**
**Affects: All hat configs**

### What theory.md says:
The full cognitive taxonomy has 12 levels (lines 6094-6338):
1. Perception
2. Attention
3. Thought (Reasoning)
4. Memory Formation
5. Working Memory
6. Cached Memory (Recallable)
7. Episodic Memory
8. Knowledge (Consolidated)
9. Models
10. Skills
11. Principles
12. Doctrine

### What the specs have:
A 7-stage loop: perception → attention → hypothesis → action → evaluation → learning → memory_consolidation (+ behavioral_evolution)

### What's missing:
- **Memory Formation** (the gate: "Is this worth remembering?") — the specs jump from evaluation to memory_consolidation without the formation/filtering step
- **Working Memory vs Cached Memory distinction** — everything goes to the same `memory_consolidation` stage
- **Knowledge Consolidation** — the transition from "remembering" to "knowing" (lines 5978-5989: Experience → Recall → Repetition → Integration → Automatic knowledge)
- **Models** — mental representations that predict outcomes; not represented
- **Principles extraction** — abstract truths from experience; not represented

### The deeper issue:
The specs treat memory as a flat store. Theory.md explicitly warns against this:
> "Agents fail when they treat everything as memory. Instead they need to distinguish between: context, recall, knowledge. Only the last one should shape behavior automatically." (lines 6358-6366)

### Fix:
Expand cognitive loop with explicit `memory_formation` gate (decides what gets stored vs discarded), and add `knowledge_transition` stage that describes how repeated patterns become committed knowledge that shapes behavior automatically.

---

## FINDING 3: Memory Schema Treats Memory as Storage, Not Cache Policy
**Severity: HIGH**
**Affects: shared_memory.yaml**

### What theory.md says:
> "At the doctrine level, you are not defining memory storage. You are defining cache policy." (lines 5824-5826)

> "what conclusions deserve caching, how long they persist, when they must be revalidated, what overrides them" (lines 5830-5836)

> "Doctrine is defining how knowledge should be trusted." (line 5842)

> "The most important memories are not observations. They are decisions." (lines 5854-5856)

### What the specs have:
The shared_memory.yaml has a `lifecycle` section with creation → consolidation → aging → retirement. This is good, but it's structured as a **data management lifecycle**, not a **cache policy**.

### What's missing:
- **Cache policy per category**: when to write, when to read, when to expire, when to refresh (lines 5813-5819)
- **Trust levels**: How knowledge should be trusted, not just how it's stored. Theory.md says doctrine defines trust policy for knowledge.
- **Three memory layers**: immediate context, cached recall, committed knowledge (lines 6008-6037). The schema only has semantic/episodic/procedural — which is a STORAGE taxonomy, not a COGNITIVE taxonomy.
- **Decision memory priority**: "The most important memories are not observations. They are decisions." — scope decisions, authorization interpretations, risk assessments, strategy choices (lines 5856-5870). These are not given special status in the schema.
- **Knowledge transition mechanism**: How does a cached memory become committed knowledge? The schema has `consolidation` but doesn't describe the transition path: Experience → Recall → Repetition → Integration → Automatic knowledge.

### The deeper issue:
The memory schema answers "what categories of data exist?" when it should answer "how does the system decide what to trust, what to keep, and what to forget?"

### Fix:
Add `cache_policy` block to each memory category defining: write_conditions, read_priority, expiry_rules, refresh_triggers, trust_level. Add `decision_memory` as a first-class memory type with highest retention. Add `knowledge_transition` rules describing how cached memories become committed knowledge.

---

## FINDING 4: Behavioral Drivers Don't Map to Behavioral Taxonomy
**Severity: MEDIUM**
**Affects: All hat configs**

### What theory.md says:
The behavioral taxonomy (lines 6398-6607):
1. **Motivation** (Why act) — survival, curiosity, duty, mission objectives
2. **Intention** (Chosen direction) — what outcome is being pursued
3. **Decision** (Commitment to act) — risk, cost, authority, consequences
4. **Strategy** (General approach) — broad path toward intention
5. **Tactics** (Situational action) — what to do right now
6. **Techniques** (Methods used) — specific method
7. **Procedures** (Step-by-step execution) — concrete steps

Three domains: Internal Drivers (motivation, values, beliefs, principles) → Decision Structures (intention, decision, strategy) → Observable Action (tactics, techniques, procedures)

### What the specs have:
`behavioral_drivers` with primary/secondary lists and an `optimization_function`. This captures MOTIVATION somewhat, but:

### What's missing:
- **Intention layer**: What outcome is being pursued? The specs jump from motivation to action.
- **Decision structures**: How does the hat commit to a course of action? The `decision_heuristics` section partially covers this but is disconnected from the behavioral driver chain.
- **Strategy layer**: The specs describe tactics and techniques in the action stage, but never articulate the STRATEGIC approach each hat takes.
- **The three-domain separation**: Internal Drivers vs Decision Structures vs Observable Action. This clean separation doesn't exist in the specs.

### Fix:
Restructure `behavioral_drivers` to explicitly map the behavioral taxonomy chain: motivation → intention → decision → strategy. Connect `decision_heuristics` as the decision layer within this chain rather than a separate section.

---

## FINDING 5: Supervisor Missing Full Governance Stack
**Severity: MEDIUM**
**Affects: engine/supervisor.yaml**

### What theory.md says:
The full governance stack (lines 4710-4724):
```
God → Moral Order → Legitimacy → Institution → Governance → Hierarchy
→ Ethos → Principles → Doctrine → Strategy → ... → Procedures
```

The supervisor's position in the stack is defined in the file header as:
```
God → Moral Order → Legitimacy → Institution → Governance → Hierarchy
→ Ethos → Principles → Doctrine → [THIS LAYER] → Behavioral Modes (Hats)
```

### What the specs have:
The supervisor defines a 4-level `authority_chain`:
1. mission_authority (human commander)
2. doctrine_layer (this supervisor)
3. mode_selection (which hat)
4. active_hat_behavior (current agent)

### What's missing:
The spec correctly identifies its position but doesn't connect UPWARD to the layers above doctrine. The `authority_chain` starts at `mission_authority` (human commander) but theory.md places several layers above that:
- God → Moral Order → Legitimacy → Institution → Governance
- These are the layers that LEGITIMIZE mission authority

### The deeper issue:
> "Doctrine is no longer just 'what the organization says' but something that should be measured against a higher truth" (line 4738)

The supervisor should acknowledge that mission authority itself is bounded by higher-order constraints (ethical, legal, moral). Without this, the supervisor treats mission authority as absolute — which contradicts the theory.

### Fix:
Add `legitimacy_chain` above `authority_chain` that acknowledges the layers that legitimize mission authority. This doesn't need to be operationalized in code, but it should be explicitly stated as doctrinal context.

---

## FINDING 6: Ethos Layer Not Represented
**Severity: MEDIUM**
**Affects: All specs**

### What theory.md says:
> "Ethos says what kind of actor you are." (line 4361)

> "The mission is advanced by better questions, not merely more actions." (line 4170)

> "Do not ask 'what should we do?' until you have asked 'what do we need to know?'" (line 4249)

The ethos sits ABOVE principles and doctrine. It is the foundational identity layer.

### What the specs have:
`identity_prompt` and `core_objective` — these are task descriptions, not ethos declarations.

### What's missing:
An explicit `ethos` block for each hat that declares:
- What kind of actor this is (not what it does)
- What question quality standard it maintains
- How it distinguishes between action and understanding

### Fix:
Add `ethos` block to each hat identity with: `actor_type`, `question_standard`, `core_principle`. The supervisor should also have an ethos block that applies system-wide.

---

## FINDING 7: Cross-Hat Interpretation Rules Are Good But Incomplete
**Severity: LOW**
**Affects: shared_memory.yaml**

### What the specs have:
Excellent `interpretation_rules` section showing how each hat reads the same data differently. This is well-aligned with theory.md's concept of cognitive bias per hat.

### What's missing:
- Grey hat's interpretation of `hardening_measures` says "as complexity that creates new edge cases" — good
- But there's no interpretation for how each hat reads `failures` (only grey_hat has this)
- `engagements` interpretation is missing for all hats
- The interpretation rules should include HOW the reading changes the hat's behavior, not just what it sees

### Fix:
Complete the interpretation matrix so every hat has an interpretation for every memory category. Add a `behavioral_effect` field showing how the interpretation changes the hat's next cognitive loop.

---

## FINDING 8: No Scope Enforcement Architecture
**Severity: MEDIUM**
**Affects: supervisor.yaml, red_team.yaml**

### What theory.md says (Section III, lines ~250-288):
Scope enforcement has four layers:
1. **Pre-action evaluation** — before any action, check if it's in scope
2. **Real-time boundary monitoring** — during execution, watch for scope drift
3. **Post-action validation** — after action, confirm scope was maintained
4. **Out-of-scope discovery handling** — when something interesting is found outside scope

### What the specs have:
Red team has `scope_discipline: strict` and constraints saying "MUST operate within explicit rules of engagement." The supervisor has `authorization_enforcement` responsibilities.

### What's missing:
The four-layer enforcement model is not implemented. There's no structured pre-action check, no real-time monitoring spec, no post-action validation protocol, no out-of-scope discovery procedure.

### Fix:
Add `scope_enforcement` section to supervisor.yaml implementing all four layers. Add scope_check hooks to the red_team and black_hat cognitive loops.

---

## FINDING 9: Memory Decay Functions Need Cache Semantics
**Severity: LOW**
**Affects: shared_memory.yaml, all hat memory_baseline sections**

### What the specs have:
- Shared memory: `decay_function: "relevance = base_weight * (recency_factor ^ time_since_last_access)"`
- Hat configs: `weight_function` per memory category (e.g., `"recency * success_rate * stealth_score"`)

### What's correct:
These implement the "memories decay unless reinforced" concept from theory.md.

### What's missing:
- **Revalidation triggers**: When must a memory be re-tested against reality before being trusted? (cache invalidation)
- **Override rules**: What new information causes old memories to be overridden? (cache eviction)
- **Confidence decay**: Confidence should decay separately from relevance. A memory can be relevant but no longer trustworthy.

### Fix:
Add `revalidation_trigger`, `override_conditions`, and `confidence_decay` to each memory category alongside the weight function.

---

## SUMMARY OF FINDINGS

| # | Finding | Severity | Files Affected |
|---|---------|----------|----------------|
| 1 | Missing Question Engine | CRITICAL | All 4 hat configs |
| 2 | Cognitive Loop Truncated (7/12 levels) | HIGH | All 4 hat configs |
| 3 | Memory as Storage not Cache Policy | HIGH | shared_memory.yaml |
| 4 | Behavioral Drivers Don't Map to Taxonomy | MEDIUM | All 4 hat configs |
| 5 | Supervisor Missing Full Governance Stack | MEDIUM | supervisor.yaml |
| 6 | Ethos Layer Not Represented | MEDIUM | All specs |
| 7 | Cross-Hat Interpretation Incomplete | LOW | shared_memory.yaml |
| 8 | No Scope Enforcement Architecture | MEDIUM | supervisor.yaml, red_team.yaml |
| 9 | Memory Decay Missing Cache Semantics | LOW | shared_memory.yaml, all hats |

**Critical: 1 | High: 2 | Medium: 4 | Low: 2**

---

## METHODOLOGY IMPROVEMENTS

Based on this audit, the following changes to the specification methodology:

### 1. Question-First Design
Every spec should START with the governing question, not the task. The question drives the cognitive loop, the memory bias, and the behavioral drivers. If you can't state the question, the spec isn't ready.

### 2. Taxonomy Alignment Checklist
Before finalizing any spec, verify it maps to:
- [ ] Full cognitive taxonomy (12 levels, not just the simplified loop)
- [ ] Full behavioral taxonomy (Motivation → Procedures, not just drivers + actions)
- [ ] Full governance stack (God → Doctrine, not just mission → hat)
- [ ] Memory cache policy (write/read/expire/refresh, not just categories)
- [ ] Question layers (legitimacy through reflection)

### 3. Separation of Knowing and Remembering
Every memory section should distinguish between:
- Cached recall (contextual, decays, requires active retrieval)
- Committed knowledge (structural, shapes behavior automatically, rarely decays)
And define the TRANSITION between them.

### 4. Ethos Before Identity
The `identity` block should be nested under an `ethos` block, not the other way around. Ethos defines what kind of actor the agent is. Identity provides the specific configuration.

### 5. Scope Enforcement as Architecture
Scope is not a constraint to list. It's an enforcement architecture with four active layers. Every hat that operates near boundaries needs scope enforcement hooks in its cognitive loop.

---

## STANDARDS UPDATES

These findings produce the following updated standards for agent spec files:

1. **REQUIRED**: `governing_question` field in every hat identity
2. **REQUIRED**: `ethos` block declaring actor type and question standard
3. **REQUIRED**: `question_layers` (6 layers adapted per hat's cognitive bias)
4. **REQUIRED**: `memory_formation` gate in cognitive loop (decides what gets stored)
5. **REQUIRED**: `knowledge_transition` rules (how cached recall becomes committed knowledge)
6. **REQUIRED**: `cache_policy` per memory category (write/read/expire/refresh/trust)
7. **REQUIRED**: `scope_enforcement` architecture (4 layers) in supervisor
8. **REQUIRED**: `legitimacy_chain` in supervisor connecting above mission authority
9. **RECOMMENDED**: Behavioral taxonomy alignment (motivation → intention → decision → strategy)
10. **RECOMMENDED**: Complete cross-hat interpretation matrix
11. **RECOMMENDED**: Revalidation triggers and confidence decay in memory schema
