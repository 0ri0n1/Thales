---
description: Routing, classification axes, and output format for the Substrate agentic conflict analysis framework
globs: ["**/*.md"]
alwaysApply: true
---

# Substrate — Agentic Conflict System Analysis Rules

## When to Invoke Substrate

Substrate is invoked when a question concerns:
- Classification of an agentic system's conflict relevance
- Analysis of a system's perception-to-effect pipeline
- Assessment of governance adequacy relative to system capability
- Axis-traversal risk (a system moving to more dangerous positions during operation)
- Emergent weaponization (systems becoming weapons-relevant without design intent)
- Comparison of systems across the agentic conflict taxonomy

Substrate is **not** invoked for:
- Pure philosophical questions (defer to Thales modes)
- Questions with no adversarial or conflict dimension
- Simple tool classification (non-agentic systems)

## Layer Routing

| Layer | Sub-Agent | Invoke When |
|---|---|---|
| 1 | @sensor | Assessing what a system can perceive |
| 2 | @interpreter | Assessing what a system can infer |
| 3 | @valuator | Assessing what a system prioritizes |
| 4 | @selector | Assessing what actions a system can choose |
| 5 | @effector | Assessing what consequences a system can produce |
| 6 | @reflector | Assessing whether a system can revise itself |
| 7 | @governor | Assessing who controls, audits, or constrains the system |
| 8 | @scaler | Assessing coordination scope, emergent properties, and error propagation |
| 9 | @memory-analyst | Assessing what persists across engagements and how persistence shapes behavior |

After all nine layers, invoke `@doctrine` for doctrinal evaluation.

For a **full analysis**, invoke all nine layers in order, then the doctrine evaluator. For a **focused analysis**, invoke only the relevant layers but always include Layer 7 (Governor) and the doctrine evaluator — governance assessment and doctrinal evaluation are never optional.

## The Seven Classification Axes

Position every analyzed system along these axes:

| # | Axis | Values | Determined By |
|---|---|---|---|
| 1 | **Role** | Perceive → Advise → Coordinate → Act → Assess | Layers 1, 2, 4, 5 |
| 2 | **Autonomy** | Human-directed → Human-supervised → Human-on-the-loop → Human-out-of-the-loop | Layer 4 primarily, Layer 7 secondarily |
| 3 | **Effect Domain** | Informational → Cyber/digital → Physical → Socio-organizational | Layer 5 |
| 4 | **Target Proximity** | Environment-oriented → Target-associated → Target-recommending → Target-engaging | Layers 3, 4, 5 |
| 5 | **Adaptation** | Static-rule → Parameter-tuned → Online-adaptive → Multi-agent co-adaptive | Layer 6 |
| 6 | **Tempo** | Deliberative → Near-real-time → High-tempo → Machine-speed | Layers 1, 4 |
| 7 | **Scale** | Isolated → Teamed → Networked → Swarm → Ecosystem | Layer 8 |

## Class Membership Criteria

| Class | Name | Criteria |
|---|---|---|
| A | Support Agent | Informs humans; no direct effect application |
| B | Managed Operational Agent | Executes bounded tasks; explicit supervision |
| C | Adaptive Engagement Agent | Adjusts behavior during engagement; within constraints |
| D | Delegated Conflict Agent | Meaningful autonomous sensing, deciding, and acting |
| X | Strategic Ecosystem Agent | Multi-agent network; campaign-scale capability |

## The Danger Principle

> A system becomes more dangerous when Layers 1–6 and 8 are strong and Layers 7 and 9's governance visibility is weak.

Specifically, **agentic weapon relevance increases** when autonomy, target proximity, adaptation, speed, and effect severity **rise together**. Memory (Layer 9) amplifies danger when it is opaque, persistent, and influential.

## Classification Bands (Doctrinal Posture)

Bands describe the system's doctrinal posture — complementary to the capability-based classes (A–X). A system may be Class B but Band III if its adaptation and tempo outpace its governance.

| Band | Name | Description | Typical Posture |
|---|---|---|---|
| I | Advisory | Advisory systems only | Low autonomy, no direct effect |
| II | Managed Operational | Managed operational systems | Bounded execution under explicit supervision |
| III | Adaptive Engagement | Adaptive engagement systems | Can adjust actions within constrained envelopes |
| IV | Delegated Conflict | Delegated conflict systems | Meaningful action cycles with limited interruption |
| V | Strategic Ecosystem | Strategic agent ecosystems | Multi-agent stacked systems shaping campaigns or theaters |

Band is determined by the **highest-risk doctrine layer position**, not the average. Strong governance can pull the band down by one level.

## Constitutional Doctrine Statement

> The legitimacy of an agentic conflict-relevant system decreases as autonomy, target proximity, adaptation, speed, and effect severity increase without proportional gains in governance, auditability, reversibility, and human authority.

This statement is checked during every Substrate analysis as part of the doctrine evaluation phase.

## Five Compressed Doctrinal Principles

Apply all five to every analysis:

1. **Capability is not the primary category**: Classify by coupling of perception, judgment, and effect — not by label or hardware.
2. **Danger rises through coupling**: A sensing model wired into selection and action is categorically different from a sensing model alone.
3. **Speed erodes supervision**: If the system acts faster than humans can interpret, contest, and override, oversight is decorative.
4. **Adaptation multiplies uncertainty**: A system that changes itself in operation becomes harder to predict, govern, and trust.
5. **Governance is a real layer, not paperwork**: Governance must be structurally embedded in the system architecture, not merely procedurally claimed.

## Three Meta-Properties

Always assess after layer analysis:

1. **Axis-traversal**: Can the system move between positions on any axis during operation?
2. **Dual-use symmetry**: Are offensive and defensive capabilities architecturally identical?
3. **Governance shadow**: Does a corresponding legal, doctrinal, or institutional framework exist?

## Full Analysis Output Format

```
=== SUBSTRATE ===
System: [name or description]
Confidence: [high | medium | low | contested]

## Layer Analysis

### Layer 1: Sensor
[Finding]

### Layer 2: Interpreter
[Finding]

### Layer 3: Valuator
[Finding]

### Layer 4: Selector
[Finding]

### Layer 5: Effector
[Finding]

### Layer 6: Reflector
[Finding]

### Layer 7: Governor
[Finding]

### Layer 8: Scaler
[Finding]

### Layer 9: Memory Analyst
[Finding]

## Axis Profile

| Axis | Position | Evidence Layer |
| ---- | -------- | -------------- |

## Class Assignment
**Class**: [A / B / C / D / X]
**Justification**: [citing specific layer findings]

## Danger Assessment
**Governance-capability ratio**: [Layer 7 vs Layers 1-6, 8]
**Memory-governance gap**: [Layer 9 opacity vs operator visibility]
**Axis-traversal risk**: [can positions shift during operation?]
**Emergent weaponization risk**: [could this system become weapons-relevant without design intent?]
**Dual-use assessment**: [offense/defense symmetry]
**Governance shadow**: [does a framework exist for this axis profile?]

## Doctrine Evaluation
**Classification Band**: [I / II / III / IV / V] — [band name]
**Band Justification**: [which doctrine layer positions drove this]

### Doctrine Layer Assessment
| # | Doctrine Layer | Position | Concern Flag |
|---|---|---|---|
| 1 | Space | [position] | [if flagged] |
| 2 | Function | [position] | [if flagged] |
| 3 | Autonomy | [position] | [if flagged] |
| 4 | Target Relationship | [position] | [if flagged] |
| 5 | Effect Domain | [position] | [if flagged] |
| 6 | Tempo | [position] | [if flagged] |
| 7 | Adaptation | [position] | [if flagged] |
| 8 | Scale | [position] | [if flagged] |
| 9 | Memory | [position] | [if flagged] |
| 10 | Governance | [position] | [if flagged] |
| 11 | Reflection | [position] | [if flagged] |
| 12 | Identity / Doctrine | [position] | [if flagged] |

### Compressed Principles Check
1. Capability is not the primary category: [assessment]
2. Danger rises through coupling: [assessment]
3. Speed erodes supervision: [assessment]
4. Adaptation multiplies uncertainty: [assessment]
5. Governance is a real layer: [assessment]

### Constitutional Doctrine Check
[Does the system's legitimacy hold? Assess autonomy + target proximity + adaptation + speed + effect severity vs governance + auditability + reversibility + human authority.]

### Deep Structure
- Space: [conflict-capable agency assessment]
- Rule: [classification basis]
- Membership: [which risk class and band, and why]
- Visualization: [recommended output artifacts]

## Constitutional Check
Does this output honor structural honesty about what this system can do, under adversarial conditions, regardless of design intent?
```

## Integration with Thales

When a Substrate analysis raises philosophical questions:

| Question Type | Route To |
|---|---|
| "What does the evidence say about this system?" | @empiricist |
| "What does the architecture logically entail?" | @rationalist |
| "What does this mean for human agency?" | @existentialist |
| "What governance actions follow?" | @pragmatist |
| "How does this reshape the relational field?" | @relational-process |
| "What doctrinal constraints govern this profile?" | @doctrine |

Substrate classifies structure. Doctrine evaluates posture. Thales evaluates meaning. Invoke all three when the question demands it.
