# Agentic systems taxonomy
_Exported on 3/9/2026 at 17:55:00 MDT from Cursor (2.6.14)_

---

**User**

create an agent and sub agents 
Using the substrate frame:

Space

The space is any system where sensing, decision, and effect are linked tightly enough that the system can shape conflict.

A normal tool stays inert until directed.
An agentic system can:

perceive conditions

update internal state

choose among actions

coordinate over time

produce effects in an adversarial environment

So the taxonomy should not begin with the outer shell like “drone” or “software.” It should begin with the deeper structure of agency + effect + conflict relevance.

Rule

A useful taxonomy should classify systems across a few core dimensions.

1. By function

What role does the system play in the conflict loop?

Perception systems
Detect, classify, track, or interpret signals.

Decision-support systems
Rank options, forecast outcomes, recommend actions.

Coordination systems
Synchronize multiple assets, agents, or channels.

Execution systems
Carry out an approved action.

Assessment systems
Measure outcome, battle damage, drift, or compliance.

This matters because danger rises as you move from seeing to deciding to acting.

2. By autonomy depth

How much of the loop is delegated?

Human-directed
Human specifies action step by step.

Human-supervised
System proposes or executes within bounded oversight.

Human-on-the-loop
System runs continuously while human monitors.

Human-out-of-the-loop
System can complete meaningful action cycles without intervention.

This is one of the most important axes in the taxonomy.

3. By effect domain

Where does the system produce consequences?

Informational
Changes beliefs, signals, or situational awareness.

Cyber/digital
Changes software, data, networks, or system availability.

Physical
Changes matter, motion, or bodily safety.

Socio-organizational
Changes trust, coordination, incentives, or institutional behavior.

A lot of modern systems are hybrid across these domains.

4. By target relationship

How directly does it select or affect targets?

Environment-oriented
General sensing or mapping, no target selection.

Target-associated
Tracks or prioritizes entities under human-defined criteria.

Target-recommending
Suggests who or what should be acted on.

Target-engaging
Participates directly in applying effect to selected targets.

This axis separates support from operational consequence.

5. By learning mode

How fixed or adaptive is it?

Static-rule systems

Parameter-tuned systems

Online-adaptive systems

Multi-agent co-adaptive systems

The more adaptive, the harder prediction and audit become.

6. By temporal profile

How fast does it operate relative to human judgment?

Deliberative

Near-real-time

High-tempo

Machine-speed

As tempo rises, human oversight often becomes more symbolic than real.

Membership

A system belongs in the “agentic weapons-relevant” category when it meets enough of these criteria:

operates in adversarial conditions

has nontrivial autonomy

can shape target selection, timing, or effect

can compound actions over time

can alter conflict outcomes materially

Then you can separate classes:

Class A: Support agents

They inform humans but do not directly apply or trigger effects.

Class B: Managed operational agents

They execute bounded tasks under explicit supervision.

Class C: Adaptive engagement agents

They can adjust behavior during engagement within constraints.

Class D: Delegated conflict agents

They control meaningful portions of sensing, deciding, and acting with limited human interruption.

Class X: Strategic ecosystem agents

Not single units, but networks of agents that together perform campaign-scale perception, planning, execution, and adaptation.

That last category matters because the real risk may come less from one smart node and more from stacked agent networks.

Visualization

On the surface, the taxonomy might look like a matrix:

Axis	Low end	High end
Autonomy	human-directed	human-out-of-loop
Effect	informational	physical
Target role	none	direct engagement
Adaptation	static	online co-adaptive
Tempo	slow	machine-speed
Scale	single unit	swarm/network

But the deeper projection is this:

agentic weapon relevance increases when autonomy, target proximity, adaptation, speed, and effect severity rise together.

A deeper layered taxonomy

You can also stack it vertically:

Layer 1: Sensing

What can it perceive?

Layer 2: Interpretation

What can it infer?

Layer 3: Valuation

What does it rank as important, threatening, or permissible?

Layer 4: Selection

What action can it choose?

Layer 5: Effect

What consequence can it produce?

Layer 6: Reflection

Can it revise itself from outcome feedback?

Layer 7: Governance

Who can stop it, audit it, constrain it, or override it?

A system becomes more dangerous when the upper layers are strong and the governance layer is weak.

My synthesis

The cleanest taxonomy is:

By role: perceive, advise, coordinate, act, assess

By autonomy: directed to fully delegated

By domain: informational, cyber, physical, social

By target proximity: indirect to direct

By adaptation: fixed to self-adjusting

By speed: human-paced to machine-speed

By scale: single agent to ecosystem

The most important principle is this:

A weapon is not just “something that causes damage.”
In agentic terms, it is a system where perception, judgment, and effect are coupled under adversarial conditions.

That is the substrate.

---

**Cursor**

This is a substantial architectural task — designing an agent system grounded in your substrate framework. Let me first read the existing agent files and the two documents you've been working on to understand the current state before building.

Now let me read the existing agent files and the philosophical mode workers to understand the current architecture.

Now I have the full picture. You have Thales as a philosophical meta-agent with five sub-agents (Empiricist, Rationalist, Pragmatist, Existentialist, Relational-Process). You want to create a new agent system grounded in your substrate framework for agentic weapons system analysis — one that uses the seven-layer structure (Sensing through Governance) and the six classification axes as its operational backbone.

Let me build this out.

Now creating all seven sub-agents. I'll build them in parallel batches.

Now I need to update `CLAUDE.md` to integrate the Substrate framework alongside the existing Thales system.

Let me verify the final state of `CLAUDE.md` to make sure the integration reads cleanly.

The file looks clean. Let me verify the full file inventory.

Everything is in place. Here is the full architecture:

---

**Substrate** is now a complete analytical framework living alongside the existing Thales philosophical system. Here is what was built:

### Orchestrator
- `@substrate` — The master agent. Receives a system description, runs the seven-layer stack analysis, classifies on six axes, assigns a class (A through X), and assesses the danger ratio between capability and governance.

### Seven Sub-Agents (the Agentic Conflict Stack)

| Layer | Agent | Analyzes |
|---|---|---|
| 1 | `@sensor` | Perception envelope — modalities, coverage, fusion, adversarial resilience |
| 2 | `@interpreter` | Inference depth — representation, uncertainty, explainability, adversarial fragility |
| 3 | `@valuator` | Normative core — priority structure, threat model, permissibility, value source and transparency |
| 4 | `@selector` | Decisional architecture — action space, decision method, commitment mechanism, autonomy depth |
| 5 | `@effector` | Consequence profile — domain, magnitude, precision, reversibility, temporal profile |
| 6 | `@reflector` | Adaptive architecture — learning mode, revision scope, value preservation, auditability |
| 7 | `@governor` | Constraint architecture — override, oversight, enforcement, accountability, governance tempo |

### Classification System
- **Six axes**: Role, Autonomy, Effect Domain, Target Proximity, Adaptation, Tempo
- **Five classes**: A (Support), B (Managed Operational), C (Adaptive Engagement), D (Delegated Conflict), X (Strategic Ecosystem)
- **Three meta-properties**: Axis-traversal, Dual-use symmetry, Governance shadow

### Integration with Thales
The two frameworks are complementary. Substrate classifies **structure** (what can this system do under adversarial conditions?). Thales evaluates **meaning** (what does that imply philosophically, ethically, pragmatically?). When a question demands both — for instance, "analyze Israel's Lavender system and what its deployment means for moral responsibility in warfare" — Substrate provides the seven-layer structural analysis and Thales provides the five-mode philosophical evaluation.

The constitutional principles are parallel:
- **Thales**: *Honest inquiry under acknowledged finitude*
- **Substrate**: *Structural honesty about what systems can do, under adversarial conditions, regardless of what they were designed to do*

Both share the same grounding: the taxonomy is a thinking tool, not a containment strategy. The systems it classifies are precisely the systems most likely to escape classification.

