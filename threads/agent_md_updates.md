# AGENT.md updates
_Exported on 3/9/2026 at 18:23:22 MDT from Cursor (2.6.14)_

---

**User**

Update AGENT.md

---

**Cursor**

Let me start by reading the current `AGENT.md` and the related configuration files to understand what needs updating.

Now let me examine the actual file structure to see what exists — the current `AGENT.md` references `prompts/worker-*.md` paths but `CLAUDE.md` references `@substrate`, `@doctrine`, and the cursor agents. Let me check the actual directory layout.

Now I have a clear picture. The `AGENT.md` currently only documents Framework 1 (the five philosophical modes). It's missing the entire Substrate framework (Framework 2) and the Doctrine evaluator, which are fully specified in `CLAUDE.md` and implemented in `.cursor/agents/`. Let me also read the substrate and doctrine agent files for precise details.

Now I have a complete picture of the current state. Let me also check the state schema to include it accurately.

Now I have everything. The current `AGENT.md` only covers Framework 1 (the five philosophical modes) — it's missing the entire Substrate framework, the Doctrine evaluator, the dual-framework integration model, the state schema for Substrate variables, and the correct file paths (it references `prompts/worker-*.md` but should also reference `.cursor/agents/*.md`). Let me write the updated version.

Let me verify the file paths referenced in the new `AGENT.md` actually exist, and cross-check alignment with `CLAUDE.md`.

All 17 agent files, all 5 worker prompts, and the state schema exist exactly as referenced in the file map. Let me also verify the rules directory.

All file paths verified — every file referenced in the updated `AGENT.md` exists on disk. Here's what changed:

**The old `AGENT.md`** documented only Framework 1 (the five philosophical modes) in 205 lines. It referenced `prompts/worker-*.md` paths but had no awareness of the Substrate framework, the Doctrine evaluator, or the `.cursor/agents/` structure.

**The updated `AGENT.md`** now documents the full architecture:

- **File Map** — complete directory tree showing where every component lives (`.cursor/agents/`, `.cursor/rules/`, `prompts/`, `state/`)
- **Question Routing** — how Thales decides between Framework 1, Framework 2, or both
- **Framework 1** — preserved in full: five modes, state machine, arbitration logic, domain-fit heuristic, conflict source mapping, translation protocol
- **Framework 2** — new: nine-layer stack, seven classification axes, capability classes (A–X), doctrinal bands (I–V), the 12-layer doctrine chart, five compressed principles, danger principle, meta-properties
- **Framework Integration** — when to use each, how they hand off (Substrate classifies structure, Doctrine evaluates posture, Thales evaluates meaning)
- **State Variables** — expanded to cover both frameworks
- **Inter-Layer Context Schema** — new handoff format for Substrate sub-agent transitions
- **Output Formats** — added Substrate analysis response template
- **Constitutional Principles** — all three gathered in one place (Thales, Substrate, Doctrine)
- **Constraints** — separated by framework with shared constraints

