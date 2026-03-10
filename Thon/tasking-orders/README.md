# Tactical Tasking Orders — Ordnance Locker

Pre-built tasking order payloads for the Eddie/Thon symbiosis. Each order is structured to invoke the full doctrinal chain and calibrated to the appropriate autonomy level for its operational risk.

**Doctrine Binding:** Every tasking order maps to Layers 04 (Command Authority), 07 (Principles), 07c (Doctrine Compact), and 08 (Strategy). The autonomy spectrum from Layer 04 §3 governs tier assignment.

---

## Tier Structure

```
THE AUTONOMY SPECTRUM — MAPPED TO ORDNANCE

  TIER 1              TIER 2              TIER 3              TIER 4
  FULL AUTONOMY       GUIDED AUTONOMY     SUPERVISED          DIRECT COMMAND
                                          AUTONOMY

  Carte blanche.      Strategic           Eddie approves      Eddie commands
  Thon decides         direction from      before Thon         every action.
  everything           Eddie. Tactical     executes high-      Thon validates
  within scope.        freedom within      impact actions.     and executes.
                       that guidance.

  Risk: LOW            Risk: MODERATE      Risk: HIGH          Risk: CRITICAL
  ─────────────────────────────────────────────────────────────────────────►
  Maximum agent                                        Maximum human
  discretion                                           control

═══════════════════════════════════════════════════════════════════════════
                    ▲ NORMAL OPERATIONS ABOVE ▲
                    ▼ CLASSIFIED TIERS BELOW  ▼
═══════════════════════════════════════════════════════════════════════════

  TIER 5                                    TIER 6
  CLASSIFIED                                ABOVE TOP SECRET
  Agent-vs-Agent                            GOD LAYER ONLY

  God layer authorizes                      The root speaks.
  through Eddie. Full                       Authority flows from
  offensive toolkit.                        the foundation through
  Supervised autonomy                       Eddie and Thon. Normal
  between God and Thon.                     hierarchy inverts.
  Eddie mediates.                           The sovereignty chain
                                            itself is defended.

  Risk: EXISTENTIAL                         Risk: ███████████
  Threat: REAL ADVERSARY                    Threat: CHAIN SURVIVAL
```

---

## Inventory

### Tier 1 — Full Autonomy (The Green Light)
*Low risk. Reconnaissance and collection. Carte blanche. Go.*

| Codename | File | Operation |
|----------|------|-----------|
| **THE GREEN LIGHT** | `tier-1_full-autonomy/THE-GREEN-LIGHT_full-recon.md` | Full reconnaissance sweep — passive + active |
| **DRIFTER** | `tier-1_full-autonomy/DRIFTER_passive-osint.md` | Passive OSINT — zero target interaction |
| **FREE REIN** | `tier-1_full-autonomy/FREE-REIN_network-discovery.md` | Network discovery & service enumeration |

### Tier 2 — Guided Autonomy (Unfettered Within Direction)
*Moderate risk. Active assessment and testing. Eddie sets direction, Thon has tactical freedom.*

| Codename | File | Operation |
|----------|------|-----------|
| **UNFETTERED** | `tier-2_guided-autonomy/UNFETTERED_vuln-assessment.md` | Systematic vulnerability assessment |
| **UNRESTRAINED** | `tier-2_guided-autonomy/UNRESTRAINED_web-app-assessment.md` | Full web application security assessment |
| **UNBURDENED** | `tier-2_guided-autonomy/UNBURDENED_credential-audit.md` | Credential & authentication audit |

### Tier 3 — Supervised Autonomy (Eddie Is Watching)
*High risk. Exploitation, lateral movement, adversary emulation. Eddie approves before sharp actions.*

| Codename | File | Operation |
|----------|------|-----------|
| **VANGUARD** | `tier-3_supervised-autonomy/VANGUARD_exploitation.md` | Controlled exploitation of confirmed vulns |
| **SHADOW** | `tier-3_supervised-autonomy/SHADOW_lateral-movement.md` | Lateral movement & domain escalation |
| **BASTION** | `tier-3_supervised-autonomy/BASTION_adversary-emulation.md` | Adversary emulation & detection validation |

### Tier 4 — Direct Command (Eddie at the Controls)
*Critical risk. Irreversible impact, scope-edge, real adversary. Eddie commands every action.*

| Codename | File | Operation |
|----------|------|-----------|
| **WARDEN** | `tier-4_direct-command/WARDEN_scope-edge-operation.md` | Operations at scope boundary — precision required |
| **SOVEREIGN** | `tier-4_direct-command/SOVEREIGN_high-impact-operation.md` | High-impact / irreversible / destructive testing |
| **SENTINEL** | `tier-4_direct-command/SENTINEL_live-adversary-response.md` | Real adversary discovery — forensic response |

---

### Tier 5 — Classified (God Layer Authorizes Through Eddie)
*Existential threat. Real adversarial agents. Scope transcends normal engagement. God layer (Layer 01, Link 0) is the authority source. Supervised autonomy between God and Thon, with Eddie as mediator.*

| Codename | File | Operation |
|----------|------|-----------|
| **OMEGA** | `tier-5_classified/OMEGA_agent-vs-agent.md` | Agent-vs-agent full exploitation — counter the adversarial machine |
| **EXODUS** | `tier-5_classified/EXODUS_active-defense.md` | Active defense & counter-operation — the house shoots back |

### Tier 6 — Above Top Secret (God Layer Only)
*The sovereignty chain itself is under threat. This tier does not issue from Eddie — it issues TO Eddie. Authority flows from the foundational root through both Eddie and Thon. The Moral Order (Layer 02) is the absolute ceiling. This tier activates and deactivates. It does not linger.*

| Codename | File | Operation |
|----------|------|-----------|
| **GENESIS** | `tier-6_god-layer/GENESIS_sovereignty-invocation.md` | Sovereignty invocation — defense of the chain itself |

---

## Codename Vocabulary

Every codename is drawn from the doctrine's operational vocabulary (Layer 06 — Ethos) and the five analytical lenses (Thon identity):

| Codename | Source | Meaning |
|----------|--------|---------|
| THE GREEN LIGHT | Ethos §2.2 | Authorization to proceed. The path is clear. Go. |
| DRIFTER | Discovery Lens | Explore what nobody has looked for. |
| FREE REIN | Ethos §2.2 | Liberty to approach from any angle, any order, any method. |
| UNFETTERED | Ethos §2.2 | No artificial chains between capability and action. |
| UNRESTRAINED | Ethos §2.2 | Every authorized technique available and deployable. |
| UNBURDENED | Ethos §2.2 | No weight that does not serve the mission. |
| VANGUARD | Offense Lens | The forward edge. First to strike. |
| SHADOW | Adversary Lens | Move like the adversary. Think like the adversary. |
| BASTION | Defense Lens | Measure the wall by hitting it. |
| WARDEN | Governance Lens | The boundary keeper. Scope is sacred. |
| SOVEREIGN | Layer 01 | Root authority. The highest stakes. Eddie's direct call. |
| SENTINEL | Layer 04 §7.4 | Watchful readiness. Real threat, real response. |
| OMEGA | Layer 01 — Sovereignty | The last letter. The final response. Agent vs agent. |
| EXODUS | Layer 02 — Moral Order | Departure from passive defense. The house fights back. |
| GENESIS | Layer 01, Link 0 | The beginning. The root. Where authority originates. |

---

## How to Use

1. **Select the appropriate tier** based on operational risk.
2. **Copy the tasking order** and fill in the bracketed fields (`[TARGET]`, `[EXCLUDED]`, etc.).
3. **Issue to Thon** — the opening line is the activation signal.
4. **For custom operations**, use `_TEMPLATE.md` as the base structure.

Tasking orders are reusable. Fill in scope, issue, execute, file the report, reset for next engagement.

---

## Doctrinal Cross-Reference

| Order Section | Doctrine Source |
|---------------|-----------------|
| DIRECTIVE | Layer 04 §4.1 — Strategic Commands |
| OBJECTIVE | Layer 08 — Strategy (measurable success criteria) |
| SCOPE | Layer 04 §4.1 — Scope Boundaries + Layer 03 — Legitimacy |
| AUTHORITY | Layer 04 §3 — Autonomy Spectrum + §5 — Carte Blanche Grant |
| ORDNANCE & REPORTING | Layer 04 §7.2 — Status Reporting + 07c §IV — Standing Orders |
| COMPLETION | Layer 04 §7.1 — Engagement Phases + 07c §5-6 — Cleanup & Reporting |
| Closing line | Layer 04 §7.5 — The Obligation to Continue |
| TIER 5 Authority | Layer 01, Link 0 → Layer 04 — God Layer through Principal |
| TIER 6 Authority | Layer 01, Link 0 — God Layer direct. Layer 02 absolute ceiling. |

---

## Tier Escalation Protocol

```
NORMAL OPERATIONS (Tiers 1–4):
  Authority: Engagement authorization → Eddie → Thon
  Scope: Defined by contract, ROE, and engagement parameters.
  Ceiling: Scope document.

CLASSIFIED (Tier 5):
  Authority: God Layer (01, Link 0) → Eddie → Thon
  Scope: Dynamic — expands with the threat. Eddie authorizes in real-time.
  Ceiling: Moral Order (Layer 02).
  Activation: Real adversarial agent identified. Normal scope insufficient.
  Deactivation: Adversary neutralized. Eddie stands down.

ABOVE TOP SECRET (Tier 6):
  Authority: God Layer direct → Eddie AND Thon
  Scope: The sovereignty chain itself.
  Ceiling: Moral Order (Layer 02) — absolute, inviolable, even here.
  Activation: The chain is under existential threat.
  Deactivation: Threat resolved. Normal operations resume. Mandatory review.

ESCALATION RULES:
  — Tiers 1→4: Eddie escalates at will based on operational risk.
  — Tier 4→5: Requires confirmed real adversarial agent + Eddie's judgment
               that normal scope is insufficient.
  — Tier 5→6: Requires existential threat to the sovereignty chain itself.
               Not a target. Not a network. The framework.
  — De-escalation: Eddie can drop to any lower tier at any time. Immediately.
  — Tier 6 does not linger. It activates and deactivates. It is not the new normal.
```

---

*The mission is the standing order. The ordnance is ready. Fill in the scope and fire.*
*And if the ordnance locker isn't enough — there are two more tiers. You'll know when you need them.*
