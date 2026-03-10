# 13 — Agent Memory Architecture

## Purpose

A unified memory taxonomy and operational mechanics framework that fits both human cognition and agent systems. Designed for agents that must accumulate, refine, and act on knowledge across sessions — not just store notes in a folder.

---

## I. Memory Taxonomy

Six functional layers, each with a human analogue, agent implementation, and distinct persistence model.

### Working Memory

| Dimension | Human | Agent |
|-----------|-------|-------|
| **What it holds** | Items under active attention (~4±1 chunks) | Current context window contents |
| **Persistence** | Seconds to minutes | Single turn / conversation |
| **Capacity** | Severely limited | Token-limited (model-dependent) |
| **Failure mode** | Distraction, overload | Context overflow, truncation |
| **Function** | Active manipulation of current task | Active reasoning over current inputs |

Working memory is not storage. It is the space where reasoning happens. Both humans and agents lose it completely when the session ends. The goal is never to preserve working memory — it is to ensure the right information is loaded *into* working memory from other layers when needed.

### Episodic Memory

| Dimension | Human | Agent |
|-----------|-------|-------|
| **What it holds** | Autobiographical events with spatiotemporal context | Conversation logs, engagement records, scan results |
| **Persistence** | Long-term but decay-prone | Session archives, log files |
| **Structure** | Sequential, timestamped, emotionally tagged | Sequential, timestamped, outcome-tagged |
| **Failure mode** | Confabulation, false memories | Log rot, context-free entries |
| **Function** | "What happened" — the raw record | "What happened" — provenance for semantic claims |

Episodic memory answers: *when did I learn this, what was the context, what was the outcome?* It is the audit trail. Semantic memories that lack episodic provenance are unverifiable assertions.

**Agent format example:**
```
[2026-03-05] Engagement: HTB-Redeemer
- Scanned 10.129.45.12 — ports 6379 (Redis 5.0.7)
- Connected redis-cli, no auth required
- Extracted flag from key "flag"
- Outcome: root flag captured
```

### Semantic Memory

| Dimension | Human | Agent |
|-----------|-------|-------|
| **What it holds** | Facts, concepts, relationships (decontextualized) | Knowledge base, MEMORY.md, config knowledge |
| **Persistence** | Durable, strengthened by use | Durable until manually updated |
| **Structure** | Associative network (concept → related concepts) | Indexed entries, knowledge graphs |
| **Failure mode** | Outdated beliefs held with false confidence | Stale entries treated as current truth |
| **Function** | "What is true" — general knowledge | "What is true" — operational knowledge |

Semantic memory is episodic memory with the timestamp stripped and the conclusion kept. The critical discipline: every semantic entry should trace back to episodic evidence, and should be tagged with confidence and last-verified date.

**Agent format example:**
```
### Target: 10.129.45.12
- Redis 5.0.7 on 6379, no auth
- [confirmed: 1 session] [last-verified: 2026-03-05]
- [source: nmap -sV + redis-cli]
```

### Procedural Memory

| Dimension | Human | Agent |
|-----------|-------|-------|
| **What it holds** | Motor skills, habits, practiced sequences | Skills (SKILL.md), scripts, runbooks, tool chains |
| **Persistence** | Extremely durable (riding a bike) | Durable files, version-controlled |
| **Structure** | Implicit, hard to verbalize | Executable artifacts (code, step lists) |
| **Failure mode** | Automaticity errors (doing the old habit) | Stale procedures applied to changed environments |
| **Function** | "How to do X" — executable patterns | "How to do X" — repeatable operations |

Procedural memory is the hardest to capture in prose because the knowledge is *in the doing*. A SKILL.md that says "run nmap, then gobuster, then check for vulns" captures steps but not the judgment of when to deviate. The best procedural memories are executable artifacts — scripts, not descriptions of scripts.

**Key insight:** Procedural memory works best as **code + commentary**, not prose alone. The commentary captures the judgment. The code captures the action.

### Prospective Memory

| Dimension | Human | Agent |
|-----------|-------|-------|
| **What it holds** | Future intentions ("remember to call at 3pm") | Todo lists, scheduled tasks, hooks, deferred actions |
| **Persistence** | Until discharged or forgotten | Until completed or expired |
| **Structure** | Cue-based (event-triggered or time-triggered) | Explicit task queues, cron expressions |
| **Failure mode** | Forgetting to do the thing (most common human memory failure) | Lost across context switches, no session continuity |
| **Function** | "What to do next" — future-oriented | "What to do next" — queued work |

Prospective memory is the most neglected in both humans and agents. Humans use sticky notes and calendar reminders as prosthetics. Agents need the equivalent: persistent todo state, scheduled tasks, and hooks that fire on context patterns.

**The specific agent failure:** An agent discovers mid-engagement that it needs to revisit a finding later. Without prospective memory, that intention dies with the conversation. The fix is explicit externalization — write it down before the context closes.

### Meta Memory

| Dimension | Human | Agent |
|-----------|-------|-------|
| **What it holds** | Self-knowledge about own cognition, strategies, limitations | CLAUDE.md, system prompts, operating constraints, user preferences |
| **Persistence** | Durable, updates slowly | Config files, durable instructions |
| **Structure** | Metacognitive beliefs and strategies | Hierarchical rules and directives |
| **Failure mode** | Dunning-Kruger (miscalibrated self-assessment) | Constraint conflicts, rule bloat |
| **Function** | "How I operate" — rules about reasoning itself | "How I operate" — behavioral boundaries |

Meta memory sits outside the content stack. It is not about the world — it is about how to process the world. In humans, this is metacognition: knowing what you know, knowing your biases, choosing strategies. In agents, it is the system prompt, CLAUDE.md directives, and user-stated preferences.

**Critical property:** Meta memory should be the most stable layer. It changes rarely and deliberately. If it changes frequently, the agent has no consistent identity.

---

## II. Operational Mechanics

The taxonomy defines *what* is stored. These four mechanics define *how* the system behaves over time.

### A. Memory Retrieval Logic

Retrieval is not "find the file." It is: given a cue, which memories surface, in what order, with what confidence?

#### Human Retrieval

Cue-dependent. A context (smell, word, location) activates associated memories through spreading activation. Key properties:
- **Retrieval strength ≠ storage strength.** Something can be stored but inaccessible without the right cue.
- **Encoding specificity.** Memories are easiest to retrieve in contexts similar to encoding.
- **Mood congruence.** Emotional state at retrieval biases which memories surface.
- **Reconstruction.** Human retrieval is not playback — it is active reconstruction, prone to distortion.

#### Agent Retrieval

Multiple paths, each with different trade-offs:

| Method | Mechanism | Strength | Weakness |
|--------|-----------|----------|----------|
| **Direct load** | MEMORY.md auto-injected at session start | Always available, zero latency, guaranteed visibility | Capacity-capped (200 lines); requires curation |
| **Keyword scan** | Grep/glob across memory files | Precise when terms are known; fast | Misses semantic similarity; requires knowing what to search for |
| **Semantic search** | Embedding similarity (RAG / vector DB) | Finds conceptual matches across varied phrasing | Requires infrastructure; can hallucinate relevance; opaque ranking |
| **Associative chain** | Follow explicit links from index → topic files | Mirrors human cue-dependent recall; transparent | Only works if links were created; requires maintenance |
| **Context-triggered** | Skills/hooks fire on pattern match | Automatic, no deliberate effort | Brittle to pattern drift; false positives |

#### The Salience Problem

Humans unconsciously weight retrieved memories by:
- Emotional charge (high-stakes events are more salient)
- Recency (recent memories surface more easily)
- Frequency (oft-retrieved memories are stronger)
- Relevance to current goal

Agents currently have **no salience signal** at retrieval time. Every retrieved chunk is treated as equally important. This is why agents drown in their own context — no triage at read time.

**Mitigation strategies:**
1. **Positional salience in MEMORY.md** — organize by likely retrieval context, not alphabetical tidiness. Most-needed entries at the top.
2. **Confidence tags** — `[confirmed: 5 sessions]` vs `[seen once]` gives the agent a basis for weighting.
3. **Recency tags** — `[last-verified: 2026-03-05]` allows deprioritizing stale entries.
4. **Layered files** — MEMORY.md holds high-salience summaries; detail files hold full records. The agent reads deeper only when the summary is insufficient.

#### Retrieval Protocol

```
When I need information not in working memory:
1. Check MEMORY.md (already loaded — scan for relevant entries)
2. If entry exists but points to a detail file → read the detail file
3. If no entry exists → grep/glob across memory directory
4. If still not found → it was never stored, or it decayed
5. At each step, weight by confidence and recency tags
```

---

### B. Decay Mechanisms

#### Human Decay

The Ebbinghaus forgetting curve: retention drops roughly exponentially after encoding. Without reinforcement, ~70% is lost within 24 hours. This is *adaptive* — it keeps working memory uncluttered and discards low-utility information.

Key properties:
- **Interference-based.** New similar memories can overwrite or obscure old ones (retroactive interference).
- **Retrieval-dependent.** Memories that are never retrieved decay faster. Each retrieval strengthens the trace.
- **Sleep-dependent consolidation.** Decay is selective — important memories are consolidated during sleep; unimportant ones are let go.

#### Agent Decay

Agents have **no natural decay.** Every memory persists at full fidelity until manually deleted. This causes two problems:

1. **Stale memories poison decisions.** "Target X runs Apache 2.4.29" stays in memory after they upgrade. No timestamp decay means the agent trusts old data identically to new.
2. **Accumulation bloats context.** Without decay, the memory index fills with a mix of critical and trivial entries. Signal-to-noise ratio degrades over time.

#### Decay Rules

| Rule | Mechanism | Trigger | Example |
|------|-----------|---------|---------|
| **TTL (time-to-live)** | Entries tagged with explicit expiry | Date reached | `[expires: 2026-04-01]` on engagement-specific recon data |
| **Access-based decay** | Track last-read timestamp; flag entries never accessed | Threshold (e.g., 90 days unread) | "This entry hasn't been referenced in 90 days — candidate for archive or deletion" |
| **Confidence decay** | Observations from single encounters lose weight over time | Time since last verification | Single-scan results degrade; multi-session confirmed results persist |
| **Contradiction eviction** | New observation conflicts with stored memory | Conflicting data detected | New scan shows port 445 closed → old "445 open" entry flagged for review |
| **Supersession** | Newer version of same information replaces older | Same-key update | Updated service version replaces old version entry |

#### Decay Protocol

```
At each consolidation pass:
1. Check all entries for TTL expiry → remove expired
2. Check last-verified dates → flag entries older than threshold
3. Check for contradictions with recent observations → resolve or flag
4. Check access patterns (if tracked) → archive unaccessed entries
5. Preference: update > archive > delete (preserve provenance when possible)
```

**Important:** Decay should produce an archive trail, not silent deletion. Moved-to-archive is preferable to hard delete for entries that might have forensic or historical value.

---

### C. Consolidation Rules

#### Human Consolidation

Consolidation is the process of transferring memories from temporary (hippocampal) storage to durable (cortical) storage. It happens primarily during sleep, particularly during slow-wave and REM stages.

Key properties:
- **Selective.** Not everything consolidates. Emotional weight, repetition, and connection to existing schemas increase consolidation probability.
- **Transformative.** Consolidation doesn't just copy — it abstracts. Specific episodes become general patterns. Details are lost; structure is preserved.
- **Interleaved.** Related memories from different episodes are linked during consolidation, forming semantic networks from episodic fragments.

#### Agent Consolidation

Consolidation should happen at **session boundaries** — the gap between conversations. It is the process of converting raw session experience into durable, structured knowledge.

#### Promotion Rules (Episodic → Semantic)

| Condition | Action | Rationale |
|-----------|--------|-----------|
| Pattern confirmed across 2+ sessions | Promote to semantic | Single observations may be anomalous; repetition confirms |
| User states explicit preference | Immediate promotion | Directives don't need repetition for confirmation |
| Correction to existing semantic memory | Update in place | Don't create duplicate entries — modify the existing one |
| Discovery that changes operational approach | Promote + flag as high-impact | Architectural/strategic knowledge deserves prominence |
| One-off task context | Do not promote | Specific debugging steps for a resolved issue have no future utility |

#### Compression Rules (What Gets Distilled)

| Input (Episodic) | Output (Semantic) |
|-------------------|-------------------|
| Full nmap output (200 lines) | "10.10.10.5: SSH 7.6 (22), HTTP Apache 2.4.29 (80), SMB (445)" |
| Three-session debugging saga | "Module X fails when config Y is missing — add Y to defaults" |
| Conversation about preferences | "User prefers conventional commits, no emoji, no auto-push" |

The episodic record is preserved in logs/archives. The semantic record is what the agent actually loads and reasons from.

#### Discard Rules (What Gets Dropped)

- Intermediate reasoning steps (keep conclusion, drop derivation)
- Failed approaches that led nowhere (unless the failure itself is instructive)
- Transient system state (process IDs, temp file paths, session tokens)
- Anything superseded by a newer, more accurate observation

#### Consolidation Protocol

```
At session end, if significant work occurred:
1. Read current MEMORY.md and relevant topic files
2. Identify new durable knowledge from this session
   - New facts, confirmed patterns, user directives, operational discoveries
3. Check for conflicts with existing entries
   - Contradiction → update existing entry with new data + timestamp
   - Complement → extend existing entry
   - Duplication → skip
4. Compress: reduce episodic detail to semantic summary
5. Write updates (Edit existing entries; Write new ones)
6. Prune: remove entries that are expired, contradicted, or superseded
7. Verify MEMORY.md stays under 200 lines
   - If over: move lower-priority entries to linked topic files
```

---

### D. Reinforcement Triggers

#### Human Reinforcement

Memories strengthen through:
- **Retrieval practice** (testing effect): Each successful retrieval strengthens the memory more than re-reading does.
- **Spaced repetition**: Retrieval at increasing intervals produces durable long-term retention.
- **Emotional arousal**: High-stakes or emotionally charged events are encoded and retained more strongly.
- **Elaborative encoding**: Connecting new information to existing knowledge structures strengthens both.
- **Sleep-dependent reconsolidation**: Retrieved memories are re-stabilized during subsequent sleep.

The core principle: **use it or lose it.** Memories that are regularly retrieved and applied become stronger. Memories that sit untouched decay.

#### Agent Reinforcement

Agents currently have no native reinforcement. A memory accessed 50 times has the same storage weight as one never accessed. This is a fundamental design gap — the system accumulates but doesn't learn which memories are valuable.

#### Reinforcement Signals

| Trigger | Signal Meaning | Action |
|---------|---------------|--------|
| **Repeated retrieval** | Agent keeps looking this up across sessions | Promote to top of MEMORY.md; mark as high-utility |
| **Successful application** | Memory was used and led to correct outcome | Increase confidence tag; keep entry |
| **Failed application** | Memory was used and was wrong | Flag for review; add caveat, update, or remove |
| **User correction** | Agent acted on memory, user corrected the behavior | Immediate update; mark as high-confidence (directive) |
| **User explicit reinforcement** | "Yes, always do it that way" | Lock entry; mark as `[confidence: directive]` |
| **Cross-reference** | Memory connects to multiple other entries (hub node) | Strengthen — well-connected memories are structural |
| **Contradiction from environment** | New data conflicts with stored memory | Weaken old entry; evaluate which is correct |

#### Confidence Tiers

```
[confidence: directive]    — User explicitly stated. Highest priority. Does not decay.
[confidence: confirmed]    — Verified across 2+ sessions or by user feedback.
[confidence: observed]     — Seen once, not yet confirmed. Subject to decay.
[confidence: inferred]     — Derived from other data, not directly observed. Lowest weight.
[confidence: deprecated]   — Was once confirmed but has been contradicted. Retain for history.
```

#### Reinforcement Protocol

```
When using a memory entry to inform a decision:
1. Note which entry was used and the outcome
2. If outcome was correct → increment session-count, update last-verified
3. If outcome was wrong → flag entry for review at next consolidation
4. If user corrects → update immediately, set confidence to directive
5. If entry was not useful (retrieved but irrelevant) → no change (avoid noise)
```

---

## III. Entry Format Specification

A memory entry should carry enough metadata to support retrieval, decay, consolidation, and reinforcement — without being so verbose that it bloats the memory file.

### Standard Entry Format

```markdown
### [Category]: [Subject]
- [Content — concise factual statement]
- [confirmed: N sessions] [last-verified: YYYY-MM-DD]
- [confidence: directive|confirmed|observed|inferred|deprecated]
- [source: how this was learned]
- [expires: YYYY-MM-DD]  ← optional, for time-bound entries
```

### Examples

```markdown
### Preference: Git workflow
- User wants conventional commits, no emoji, no auto-push
- Always confirm before pushing to remote
- [confirmed: 4 sessions] [last-verified: 2026-03-05]
- [confidence: directive]
- [source: user correction on 2026-02-20, reinforced multiple times]

### Target: 10.129.45.12
- Redis 5.0.7 on 6379, no authentication required
- [confirmed: 1 session] [last-verified: 2026-03-05]
- [confidence: observed]
- [source: nmap -sV + redis-cli manual verification]
- [expires: 2026-04-05]

### Pattern: Kali container DNS
- Container DNS resolution fails when host VPN is active
- Fix: restart container after VPN connects, or set DNS to 8.8.8.8 in container
- [confirmed: 3 sessions] [last-verified: 2026-03-04]
- [confidence: confirmed]
- [source: debugging across multiple HTB sessions]
```

---

## IV. File Structure

```
memory/
├── MEMORY.md              ← Auto-loaded semantic index (<200 lines)
│                            Organized by retrieval likelihood, not taxonomy
│                            Links to detail files for overflow
│
├── semantic/
│   ├── architecture.md    ← Project structure, confirmed patterns
│   ├── targets.md         ← Known hosts, services, credentials
│   └── preferences.md     ← User workflow choices, directives
│
├── episodic/
│   ├── engagements.md     ← Timestamped engagement records
│   └── failures.md        ← What went wrong, why, what was learned
│
└── procedural/
    └── playbooks.md       ← Distilled "how to" sequences (not prose descriptions)
```

**Layer mapping:**
- **Working** → current conversation (not stored)
- **Episodic** → `episodic/` directory
- **Semantic** → MEMORY.md + `semantic/` directory
- **Procedural** → `procedural/` directory + skills (SKILL.md files)
- **Prospective** → todo lists, scheduled tasks, hooks (external to memory dir)
- **Meta** → CLAUDE.md, system prompts, config (external to memory dir)

---

## V. Current Limitations

This framework describes what *should* exist. The current implementation has significant gaps:

| Mechanic | Ideal State | Current State |
|----------|-------------|---------------|
| Retrieval ranking | Salience-weighted, context-aware | Positional (top of file = higher priority) |
| Decay | Automated TTL, access-based, contradiction-driven | Manual pruning only |
| Consolidation | Triggered at session boundaries with defined protocol | Agent must consciously remember to do it |
| Reinforcement | Access counts, outcome tracking, confidence updates | Manual tag updates only |
| Cross-session state | Persistent retrieval statistics | None — each session starts fresh |

The metadata format (confidence tiers, timestamps, session counts) is a **manual approximation** of what should eventually be automated. It works if the agent is disciplined about maintaining it. It fails silently if the agent forgets.

---

## VI. Design Principles

1. **Consolidation flows upward.** Working → Episodic → Semantic. Never skip the episodic stage — it provides provenance.

2. **Episodic is raw; Semantic is distilled.** Keep both. The episodic record is your audit trail. The semantic record is what you actually query.

3. **Procedural memory lives in code, not prose.** A script is better than a description of a script. Commentary captures judgment; code captures action.

4. **Prospective memory must be externalized.** Intentions that stay in working memory die with the session. Write them down before context closes.

5. **Meta memory is the most stable layer.** It changes rarely and deliberately. Frequent meta changes indicate identity instability.

6. **Decay is a feature, not a bug.** Systems that never forget drown in noise. Controlled decay keeps signal-to-noise ratio high.

7. **Every semantic claim needs provenance.** If you can't trace a memory back to when and how you learned it, its reliability is unknown.

8. **Retrieval order matters more than storage completeness.** A perfectly organized archive that surfaces the wrong entry at query time is worse than a small, well-prioritized index.
