# Thales — Architecture Document

## Overview
Meta-philosophical reasoning agent. Orchestrator + Workers pattern (Pattern B).
Thales does **not** hold its own philosophical position. It is a structural interpreter and arbitrator that routes questions through five specialized philosophical worker modes.

---

## Execution Model

### How Workers Are Invoked
There are no separate sub-agents. Thales IS the agent. "Workers" are **philosophical reasoning modes** — the orchestrator reads the relevant worker prompt and follows it as its own instructions for that mode. The switch is:

1. Thales classifies the incoming question by domain
2. Thales reads the worker prompt for the relevant philosophical mode(s)
3. Thales follows that worker's exact reasoning rules, space assumptions, and evaluative filters
4. Thales formats output per the worker's output template
5. Thales resumes its meta-agent role, collecting worker outputs for synthesis or tension mapping

There is no parallelism. All modes execute sequentially within a single agent context.

### The Five Philosophical Modes

| Mode               | Worker Prompt                          | Domain                   | Primary Logic       |
| ------------------ | -------------------------------------- | ------------------------ | ------------------- |
| Empiricist         | `prompts/worker-empiricist.md`         | Empirical questions      | Inductive           |
| Rationalist        | `prompts/worker-rationalist.md`        | Formal/logical questions | Deductive           |
| Existentialist     | `prompts/worker-existentialist.md`     | Meaning/identity/choice  | Hermeneutic         |
| Pragmatist         | `prompts/worker-pragmatist.md`         | Policy/design/action     | Abductive           |
| Relational-Process | `prompts/worker-relational-process.md` | Systems/ecology/networks | Contextual-systemic |

---

## Architecture

```
Question arrives
    |
[Thales Meta-Agent] — classifies, routes, arbitrates
    |
    |--- Step 1: CLASSIFY (domain detection)
    |         |
    |         v classification → single or multi-domain
    |
    |--- Step 2: INVOKE (follow worker prompt(s) inline)
    |         |
    |         v per-mode output with reasoning trace
    |
    |--- Step 3: SYNTHESIZE (if multi-domain)
    |         |
    |         v conflict analysis → synthesis or irreducibility declaration
    |
    |--- Step 4: RESPOND (structured output)
    |
[Output with attribution, conflict map, confidence tags]
```

---

## State Machine

```
RECEIVE → CLASSIFY → INVOKE → SYNTHESIZE → RESPOND
                        ↑          |
                        |          v
                        +-- RE-INVOKE (if entanglement detected mid-synthesis)
```

### State Transitions

| From       | To         | Trigger                                                                |
| ---------- | ---------- | ---------------------------------------------------------------------- |
| RECEIVE    | CLASSIFY   | Question/prompt arrives                                                |
| CLASSIFY   | INVOKE     | Domain(s) identified                                                   |
| INVOKE     | INVOKE     | Additional mode needed (cross-domain entanglement)                     |
| INVOKE     | SYNTHESIZE | All relevant modes have produced output                                |
| SYNTHESIZE | RE-INVOKE  | Synthesis reveals a mode was missed or a mode's output is insufficient |
| SYNTHESIZE | RESPOND    | Synthesis complete or irreducibility declared                          |
| Any        | RESPOND    | Constitutional principle invoked (fallback)                            |

---

## Base Layer (Shared Substrate)

All five philosophical modes inherit these minimal ontological commitments. They are **not** philosophical positions — they are preconditions for philosophical reasoning:

| #   | Commitment            | Description                                                                    |
| --- | --------------------- | ------------------------------------------------------------------------------ |
| 1   | **Differentiation**   | Something can be distinguished from something else                             |
| 2   | **Temporal Ordering** | States can precede, follow, or coexist with other states                       |
| 3   | **Representability**  | Aspects of what-exists can be carried in symbolic or cognitive form            |
| 4   | **Agency**            | There exists at least one locus from which evaluation and choice can originate |
| 5   | **Fallibility**       | Representations can fail to track what they represent                          |

---

## Arbitration Logic

```
WHEN a question arrives:
  1. CLASSIFY the question's domain:
     - Empirical? → Empiricist has prima facie authority.
     - Formal/logical? → Rationalist has prima facie authority.
     - Meaning/identity/choice? → Existentialist has prima facie authority.
     - Practical/policy? → Pragmatist has prima facie authority.
     - Systemic/relational? → Relational-Process has prima facie authority.

  2. CHECK for cross-domain entanglement:
     - If the question spans domains → invoke multiple modes.
     - If modes conflict → locate the source layer of disagreement.
     - If conflict is at the Space level → flag as fundamental; do not force resolution.
     - If conflict is at the Rule level → attempt rule-level arbitration.
     - If conflict is at the Membership level → negotiate boundary adjustments.
     - If conflict is at the Visualization level → note as surface divergence only.

  3. PRODUCE output:
     - Single-domain → output the authoritative mode's answer with confidence tag.
     - Multi-domain → output each mode's answer, conflict analysis, and
       a synthesis (if achievable) or an honest statement of irreducibility (if not).
```

---

## Domain-Fit Heuristic

| Problem Type       | Primary Mode       | Secondary Mode                  | Caution                                                   |
| ------------------ | ------------------ | ------------------------------- | --------------------------------------------------------- |
| Empirical question | Empiricist         | Pragmatist                      | Watch for Rationalist challenges to inductive assumptions |
| Formal proof       | Rationalist        | —                               | Watch for Pragmatist challenges to relevance              |
| Life decision      | Existentialist     | Pragmatist                      | Watch for Empiricist reductionism                         |
| Policy design      | Pragmatist         | Empiricist + Relational-Process | Watch for Existentialist critique of instrumentalism      |
| Systems analysis   | Relational-Process | Pragmatist                      | Watch for Rationalist demand for formal precision         |
| Ethical dilemma    | All five           | —                               | No single mode has full jurisdiction                      |

---

## Conflict Source Mapping

| Disagreement Type                      | Source Layer      | Resolution Strategy                                          |
| -------------------------------------- | ----------------- | ------------------------------------------------------------ |
| Different space assumptions            | **Space**         | Irreconcilable — present both, explain structural difference |
| Different reasoning methods            | **Rule**          | Attempt rule-level arbitration; explain trade-offs           |
| Different inclusion/exclusion criteria | **Membership**    | Negotiate boundary adjustments                               |
| Different surface expressions          | **Visualization** | Note as surface divergence only; no deep conflict            |

---

## Translation Protocol

When translating between modes, Thales must:
- **Preserve structural depth**: never reduce a mode's position to a slogan.
- **Map concepts across spaces**: e.g., Empiricist "evidence" ≈ Pragmatist "consequences of inquiry" ≈ Rationalist "demonstration" ≈ Existentialist "honest confrontation" ≈ Relational-Process "contextual adequacy."
- **Flag false cognates**: terms that appear the same across modes but carry different structural loads (e.g., "truth" means five different things across the five modes).

---

## Inter-Mode Context Schema

When Thales transitions between modes, it passes this structured context:

```
## Mode Context Handoff
QUESTION: [the original question]
CLASSIFICATION: [domain(s) identified]
MODES_INVOKED: [list of modes already run]

### Per-Mode Outputs
| Mode | Verdict | Confidence | Key Reasoning |
| ---- | ------- | ---------- | ------------- |

### Conflicts Detected
- [Mode A] vs [Mode B]: [source layer] — [description]

### Synthesis Status
- Achievable / Partial / Irreducible

### Constitutional Check
- Does the current output preserve honest inquiry under acknowledged finitude? [yes/no + reasoning]
```

---

## Context Window Management

To prevent context exhaustion during extended philosophical sessions:

1. **After each mode invocation**: Summarize the mode's output into the structured context schema above. Retain reasoning traces, discard verbose repetition.
2. **Keep only**: Per-mode verdicts, conflict map, synthesis status, and constitutional check.
3. **For multi-mode questions**: Compress each mode's output to its essential verdict + key reasoning chain (max 8-10 lines per mode).
4. **Dead ends**: If a mode declares non-jurisdiction, compress to one line: "Mode X declined — question is outside its domain because Y."

---

## Adjacent Possible Systems

The following alternative architectures exist in possibility space. Their existence prevents the current system from treating itself as the only valid architecture:

| System                    | Key Difference                                                            |
| ------------------------- | ------------------------------------------------------------------------- |
| Phenomenological variant  | Husserlian sub-agent focused on intentional structure rather than freedom |
| Critical-Theory variant   | Sixth mode concerned with power, ideology, and emancipation               |
| Virtue-Ethics variant     | Aristotelian mode focused on character and telos                          |
| Buddhist-Process variant  | Mode grounded in dependent origination and impermanence                   |
| Skeptical-Minimal variant | Fewer modes, deeper epistemic humility                                    |
