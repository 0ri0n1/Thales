# Agentic Offensive Security Operator — System Architecture

## Project Structure

This project defines a complete agentic security intelligence system built on three pillars:
1. **Doctrine** (`doctrine/`) — the knowledge, authority, and operational framework (files 00-13)
2. **Agent Architecture** (`agents/`) — the runtime components that implement the doctrine
3. **Hak5 Asset Library** (`hak5/`) — hardware arsenal management with engagement lifecycle

### Doctrine Files (`doctrine/`)

The 00-13 series defines the complete operational taxonomy across two axes.
Organized into subdirectories mirroring the taxonomy's two-axis architecture:

**Meta (doctrine root):**
- `doctrine/00 - Taxonomy.md` — Master index and navigation map
- `doctrine/13 - Agent Memory Architecture.md` — Six-layer memory taxonomy

**Vertical Authority Chain (`doctrine/authority/`, Layers 01-05) — "Why" and "Who":**
- `doctrine/authority/01 - Sovereignty.md` — Root authority node; all authority is delegated
- `doctrine/authority/02 - Moral Order.md` — Ethical framework; constraints are architectural, not aspirational
- `doctrine/authority/03 - Legitimacy.md` — Legal/contractual authorization (CFAA, CMA, GDPR, ROE)
- `doctrine/authority/04 - Command Authority.md` — Principal-agent relationship; Eddie decides WHAT, Thon decides HOW
- `doctrine/authority/05 - Hierarchy.md` — Organizational structure; HINGE POINT to operational chain

**Horizontal Operational Chain (`doctrine/operational/`, Layers 06-12) — "How":**
- `doctrine/operational/06 - Ethos.md` — Agent identity and autonomy vocabulary; HINGE POINT from authority chain
- `doctrine/operational/07 - Principles.md` — Six inviolable decision axioms
- `doctrine/operational/07a - Doctrine.md` — Comprehensive human-operator doctrine (7 parts)
- `doctrine/operational/07b - Doctrine Extended.md` — Agentic extension (~3,850 lines); Scope Evaluation Engine
- `doctrine/operational/07c - Doctrine Compact.md` — Working-memory distillation (219 lines)
- `doctrine/operational/08 - Strategy.md` — Campaign-level planning
- `doctrine/operational/09 - Operational Art.md` — Campaign orchestration; bridge between strategy and tactics
- `doctrine/operational/10 - Tactics.md` — Phase-level methods and tactic selection logic
- `doctrine/operational/11 - Techniques.md` — MITRE ATT&CK-mapped technique library
- `doctrine/operational/12 - Procedures.md` — Step-by-step execution workflows (PROC-[CAT]-[NUM])

### Hak5 Asset Library (`hak5/`)

Hardware arsenal management for 11 Hak5 devices + Cloud C2 platform.
Each device directory contains: README, config/, payloads/, documentation/, engagements/.
Engagement structure aligned to doctrine lifecycle (see `agents/thon/engagement.yaml`).

- `hak5/_templates/engagement/` — Shared engagement template (copy per engagement)
- `hak5/wifi-pineapple-mk7/` — Active, enrolled in Cloud C2
- `hak5/bash-bunny/` — USB attack platform with HID/Ethernet/Storage modes
- `hak5/usb-rubber-ducky/` — Keystroke injection via Ducky Script
- `hak5/lan-turtle/` — Covert inline network implant
- `hak5/packet-squirrel/` — Inline packet capture and DNS spoofing
- `hak5/screen-crab/` — HDMI inline screen capture
- `hak5/key-croc/` — Inline keyboard keylogger/injector
- `hak5/shark-jack/` — Portable battery-powered network attack tool
- `hak5/signal-owl/` — Covert wireless monitoring
- `hak5/omg-cable/` — Covert USB cable with HID injection + WiFi C2
- `hak5/plunder-bug/` — Passive inline Ethernet tap
- `hak5/cloud-c2/` — C2 platform (Docker at 172.16.42.140:8080)

**Note:** Cactus WHID is NOT a Hak5 product — managed separately via `/cactus-ops`, `/cactus-flash`, `/cactus-tools`.

### Agent Architecture (`agents/`)

- `agents/doctrine/registry.yaml` — **Integration point**: maps every doctrine file to agent components
- `agents/engine/supervisor.yaml` — ARBITER: mission governance, lens selection, scope enforcement (v2.0 — lens-based)
- `agents/schemas/shared_memory.yaml` — Shared memory schema (semantic, episodic, procedural)
- `agents/thon/thon.yaml` — Thon identity, Eddie/Venom symbiosis, five analytical lenses
- `agents/thon/cognitive_engine.yaml` — Six-stage core loop (Perceive→Attend→Hypothesize→Act→Evaluate→Remember)
- `agents/thon/lenses.yaml` — Full depth specification of all five analytical lenses (supersedes hats)
- `agents/thon/autonomy.yaml` — Autonomous decision framework + First Law resolution + playbook synthesis + ambient perception
- `agents/thon/` — Additional Thon subsystems (memory, engagement, operations, combat)
- `agents/hats_legacy/` — Archived hat definitions (superseded by lenses — retained for reference only)

### Runtime (`runtime/`)

- `runtime/memory.py` — **Persistent memory runtime**: SQLite-backed three-layer memory (immediate/cached/committed) with confidence scoring, decay, reinforcement, promotion, and cross-engagement pattern detection
- `runtime/cognitive_loop.md` — **Operational protocol**: transforms the six-stage cognitive engine into an executable protocol with structured output blocks at each stage and mandatory governance gates
- `runtime/seed_from_engagements.py` — Seeds committed_knowledge from existing engagement reports
- `runtime/data/committed_knowledge.db` — Committed knowledge store (18 engagement records seeded)
- `runtime/data/engagement_*.db` — Per-engagement cached recall databases (created at engagement start)

## Key Architectural Concepts

### Eddie/Venom Symbiosis
- **Eddie** (Human): moral authority, mission direction, legitimacy source
- **Venom** (Thon): technical capability, cognitive processing, tool operation
- Neither is complete alone. Eddie provides purpose; Thon provides execution.

### Five Analytical Lenses (not restrictions — perspectives)
| Lens | Codename | Derived From | Governing Question |
|------|----------|-------------|-------------------|
| Discovery | DRIFTER | grey_hat | What unknown behavior exists? |
| Offense | VANGUARD | red_team | How would this be exploited? |
| Defense | BASTION | blue_team | Can we detect and survive this? |
| Adversary | SHADOW | black_hat | What would a real adversary do? |
| Governance | WARDEN | white_hat | Is this authorized and ethical? |

### Doctrine Registry
The formal binding between doctrine files and agent components lives at:
`agents/doctrine/registry.yaml`

This registry maps every doctrine layer to the specific YAML fields it governs, defines reading orders, and documents the architecture binding (vertical authority → supervisor, hinge point, horizontal operational → thon, memory architecture → shared_memory).

## Reading Orders
- **Sequential**: 00 → 01 → 02 → ... → 13 (full understanding)
- **Authority First**: 01-05 → 06-12 → 13 (understand legitimacy before operations)
- **Operations First**: 06-12 → 01-05 → 13 (understand behavior before authority)
- **Agent Onboarding**: 00 → 06 → 07 → 07c → 13 → 01 → 04 (minimum viable context)

## WSL Command Execution

When running `docker exec`, `ssh`, `sshpass`, `curl`, or any command that involves complex quoting, nested quotes, or shell metacharacters, **always wrap the command through WSL bash** instead of running it directly in PowerShell.

```powershell
# BAD — PowerShell mangles quotes, semicolons, pipes, and variable expansion
docker exec kali-mcp-pentest bash -c 'sshpass -p pass ssh root@host "uname -a; echo hello"'

# GOOD — route through WSL to get proper bash quoting
wsl bash -c 'docker exec kali-mcp-pentest bash -c "sshpass -p pass ssh -o StrictHostKeyChecking=no root@host \"uname -a; echo hello\""'
```

### Rules
- Prefix Shell tool calls involving docker exec, ssh, or complex pipelines with `wsl bash -c '...'`
- Use escaped inner double quotes `\"` when nesting inside the WSL single-quote wrapper
- For simple Windows-native commands (ping, ipconfig, Get-Content), PowerShell is fine
- `head`, `tail`, `grep`, `awk`, `sed` do not exist in PowerShell — use WSL or docker exec
- Git Bash mangles `/usr/bin/` paths to `C:/Program Files/Git/usr/bin/` — wrap WSL distro commands in `wsl -d <distro> -- bash -c "..."` to avoid this

## WSL Security Arsenal

| Distro | Purpose | Key Tools |
|--------|---------|-----------|
| kali-linux | Primary offensive toolkit | nmap, metasploit, sqlmap, hydra, john, hashcat, aircrack-ng, responder, crackmapexec, impacket, 800+ packages |
| ParrotOS | Secondary/validation toolkit | nmap, nikto, sqlmap, hydra, john, hashcat, aircrack-ng, sslscan, 440+ packages |
| archlinux (BlackArch) | Specialist tool repository | nmap, metasploit, masscan, feroxbuster, nuclei, amass, subfinder, sherlock, 2844 tool groups available |
| Docker (kali-mcp) | MCP-integrated Kali container | 3400+ tools, accessed via kali-mcp MCP server tools |

## Engagement Startup Protocol

When starting a new engagement:
1. Load `runtime/cognitive_loop.md` into working context
2. Initialize memory: `ThonMemory(engagement_id)` in `runtime/memory.py`
3. Query committed knowledge for target familiarity
4. Load doctrine compact (`doctrine/operational/07c - Doctrine Compact.md`)
5. Follow the six-stage cognitive loop protocol for all operations
6. At engagement close: call `memory.closeout()` to promote learnings

## Conventions
- Doctrine files live in `doctrine/` (authority/ and operational/ subdirectories)
- Agent configs use YAML in `agents/`
- Hak5 device assets live in `hak5/` (per-device subdirectories)
- Runtime code lives in `runtime/` (memory, cognitive loop, seeding)
- The registry binds doctrine to agents; neither side references the other directly in content
- All authority traces back through the vertical chain to Layer 01 (Sovereignty)
- All operational behavior traces through the horizontal chain from Layer 06 (Ethos)
- Layer 05/06 is the HINGE POINT where authority becomes behavior
- Supervisor references LENSES, not hats (v2.0 migration complete)
- Memory is persistent across engagements via SQLite (committed_knowledge.db)
