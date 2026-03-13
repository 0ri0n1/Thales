━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# REPORT HEADER

| Field | Value |
|---|---|
| **Operation** | MCP ARSENAL EXPANSION |
| **Phase** | STAGING |
| **Authored by** | Thon |
| **Reviewed by** | Eddie (pending) |
| **Date** | 2026-03-10 |
| **Status** | COMPLETE — Awaiting Eddie GO/NO-GO |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Current Arsenal Inventory (Ground Truth)

Before vetting new entries, the existing operational state was audited from two config files:

### Cursor — `C:\Users\Dallas\.cursor\mcp.json` (7 servers)

| Server | Transport | Status |
|---|---|---|
| file system | npx stdio | Active |
| puppeteer | npx stdio | Active |
| github | npx smithery | Active |
| paperless-ngx | uv stdio | Active |
| Zapier | HTTP SSE | Active |
| dnspy | uv stdio | Active |
| sdr | uv stdio | Active |

### Antigravity — `mcp_config.json` (26 servers, some disabled)

| Server | Transport | Status |
|---|---|---|
| sequential-thinking | npx stdio | ✅ Active |
| **kali-mcp** | python stdio (Docker) | ✅ Active — 62 tools |
| flipper-zero | python stdio | ❌ Disabled |
| paperless-ngx | uv stdio | ✅ Active |
| ntfy | uv stdio | ❌ Disabled |
| uptime-kuma | uv stdio | ✅ Active |
| portainer | uv stdio | ✅ Active |
| duplicati | uv stdio | ❌ Disabled |
| nginx-proxy-manager | uv stdio | ❌ Disabled |
| vaultwarden | uv stdio | ✅ Active |
| bookstack | uv stdio | ❌ Disabled |
| linode | uv stdio | ❌ Disabled |
| godaddy | uv stdio | ❌ Disabled |
| quickbooks | uv stdio | ✅ Active |
| cra-tax | uv stdio | ❌ Disabled |
| guacamole | uv stdio | ❌ Disabled |
| facebook | uv stdio | ❌ Disabled |
| suitecrm | uv stdio | ❌ Disabled |
| ultravnc | uv stdio | ✅ Active |
| billionmail | uv stdio | ❌ Disabled |
| zapier | npx mcp-remote | ✅ Active |
| plaud | uv stdio | ❌ Disabled |
| beside | uv stdio | ❌ Disabled |
| asus | uv stdio | ❌ Disabled |
| iphone | uv stdio | ❌ Disabled |
| dnspy | uv stdio | ✅ Active |

**Key offensive assets already operational:** Kali MCP (62 tools, 18 categories), dnSpy MCP, Flipper Zero MCP (disabled), SDR MCP.

---

# SECTION A — SECURITY VETTING RESULTS

## Category 1 — Adversary Emulation & Frameworks

### [ART-01] Atomic Red Team MCP
| Gate | Assessment |
|---|---|
| V1 Source | ✅ `cyberbuff/atomic-red-team-mcp` — Hare Sudhan, known Security Engineer specializing in adversary emulation. Active GitHub presence. |
| V2 Outbound | ✅ Downloads ATT&CK data from GitHub (expected). No telemetry. Bearer token auth for remote mode stays local. |
| V3 Code | ✅ Fully open source Python. Auditable on GitHub. |
| V4 Supply | ✅ PyPI (`atomic-red-team-mcp`), also `uvx`. Standard Python deps. |
| V5 Blast | ⚠️ `execute_atomic` can modify system state — **disabled by default** (`ART_EXECUTION_ENABLED=false`). With execution off, read-only query layer. With execution on, full ATT&CK test execution on host. |
| **Rating** | **⚠️ CAUTION** — Safe in query-only mode. Execution mode requires isolated test environment. |
| Notes | Keep `ART_EXECUTION_ENABLED=false` in production config. Only enable in sandboxed lab. |

### [ATK-01] MITRE ATT&CK MCP — Montimage
| Gate | Assessment |
|---|---|
| V1 Source | ✅ Montimage — established EU cybersecurity research firm (CNRS-affiliated). |
| V2 Outbound | ✅ No outbound. Uses local `mitreattack-python` library with pre-built indices. |
| V3 Code | ✅ Fully open source Python. |
| V4 Supply | ✅ pip install. Standard Python deps pinned. |
| V5 Blast | ✅ Read-only knowledge layer. Zero filesystem/network write access. |
| **Rating** | **✅ CLEAR** |

### [ATK-02] MITRE ATT&CK MCP — imouiche
| Gate | Assessment |
|---|---|
| V1 Source | ⚠️ Individual author, `imouiche`. Unknown track record. NPM package available. |
| V2 Outbound | ✅ Read-only ATT&CK data. No outbound telemetry. |
| V3 Code | ✅ Open source on GitHub and NPM. |
| V4 Supply | ✅ NPM (`@imouiche/mitre-attack-mcp-server`). |
| V5 Blast | ✅ Read-only. Low blast radius. |
| **Rating** | **⚠️ CAUTION** — Functional but ATK-01 (Montimage) and ATK-04 (MHaggis) are from more established authors. Deprioritize unless 65-tool breadth is specifically needed. |

### [ATK-03] MITRE ATT&CK MCP — stoyky
| Gate | Assessment |
|---|---|
| V1 Source | ⚠️ Individual author, `stoyky`. Unknown track record. |
| V2 Outbound | ✅ Read-only. |
| V3 Code | ✅ Open source. |
| V4 Supply | ✅ pipx install. |
| V5 Blast | ✅ Read-only. Navigator layer generation is local file output. |
| **Rating** | **⚠️ CAUTION** — ATT&CK Navigator layer generation is unique but author unknown. Source audit needed before queue. |

### [ATK-04] MITRE ATT&CK MCP — MHaggis
| Gate | Assessment |
|---|---|
| V1 Source | ✅ MHaggis (Michael Haag) — well-known security researcher, Splunk contributor, detection engineering authority. |
| V2 Outbound | ✅ Downloads ATT&CK STIX data on first run (expected). No telemetry. |
| V3 Code | ✅ Fully open source Python. |
| V4 Supply | ✅ pip/uv. Standard deps. |
| V5 Blast | ✅ Read-only knowledge + Navigator layer file generation. |
| **Rating** | **✅ CLEAR** |
| Notes | **HIGH-VALUE PAIR** with DE-01 (Security Detections MCP) — same author, designed to work together for coverage gap analysis. |

---

## Category 2 — Full Pentest Frameworks

### [PF-01] RedAmon
| Gate | Assessment |
|---|---|
| V1 Source | ⚠️ `samugit83` — individual author. Growing community (active GitHub). |
| V2 Outbound | 🔴 **ngrok/chisel tunnel support** opens outbound connections. Neo4j runs locally but exposes network. |
| V3 Code | ✅ Open source Python + Docker. |
| V4 Supply | ⚠️ Docker Compose (~15GB). Pulls multiple images. Requires `NET_ADMIN`, `NET_RAW`, `SYS_PTRACE` — **privileged container capabilities**. |
| V5 Blast | 🔴 **HIGH** — Privileged Docker caps, reverse shell capabilities, Metasploit integration, compile/execute C/C++ exploits. Full system compromise potential if container escapes. |
| **Rating** | **🔴 HOLD** |
| Notes | Impressive capabilities but V2/V4/V5 fail. Massive attack surface. Requires Eddie decision. See Section F. |

### [PF-02] HexStrike AI
| Gate | Assessment |
|---|---|
| V1 Source | 🔴 `0x4m4` — unknown author. No established track record. |
| V2 Outbound | ⚠️ Chromium browser agent implies outbound web traffic. |
| V3 Code | ⚠️ Open source but 150+ tools invoked — massive audit surface. |
| V4 Supply | ⚠️ Python + Kali tools. Heavy dependency chain. |
| V5 Blast | 🔴 **HIGH** — 150+ security tools exposed through single MCP interface. Extensive overlap with existing Kali MCP. |
| **Rating** | **🔴 HOLD** |
| Notes | Unknown author + massive attack surface + heavy Kali overlap. See Section F. |

### [PF-03] Offensive Security Toolkit (Joas Antonio)
| Gate | Assessment |
|---|---|
| V1 Source | ⚠️ Joas Antonio — known red team community figure. PulseMCP listing only. Primary repo unlocated. |
| V2 Outbound | ⚠️ Shodan OSINT implies API key and outbound queries. |
| V3 Code | 🔴 **FAIL** — Primary repo not located. Cannot audit. |
| V4 Supply | 🔴 **FAIL** — Install method unknown without primary repo. |
| V5 Blast | ⚠️ 90+ tools — significant surface area. |
| **Rating** | **🔴 HOLD** |
| Notes | Cannot proceed without locatable, auditable source repo. See Section F. |

### [PF-04] PentestAgent
| Gate | Assessment |
|---|---|
| V1 Source | ⚠️ `0xSojalSec` — individual author. Limited track record. |
| V2 Outbound | ⚠️ RAG knowledge base — need to confirm where vectors are stored and whether data leaves machine. |
| V3 Code | ⚠️ Open source but RAG data flow needs audit. |
| V4 Supply | ⚠️ Python. LLM dependency. |
| V5 Blast | ⚠️ LLM-driven autonomous pentesting decisions. Medium-high blast radius. |
| **Rating** | **🔴 HOLD** |
| Notes | RAG data flow and autonomous execution model need Eddie review. See Section F. |

### [PF-05] FuzzingLabs Security Hub
| Gate | Assessment |
|---|---|
| V1 Source | ✅ FuzzingLabs — known blockchain/security research firm. Active GitHub org. |
| V2 Outbound | ✅ Each tool is Dockerized. Network access scoped per-container. |
| V3 Code | ✅ Fully open source. Docker containers non-root, minimal images, Trivy-scanned. CI/CD with GitHub Actions. |
| V4 Supply | ✅ Docker Compose. Modular — cherry-pick individual servers. Well-structured Dockerfiles. |
| V5 Blast | ✅ Docker isolation per-tool. Container compromise limited to that tool's scope. Best containment model in the briefing. |
| **Rating** | **✅ CLEAR** |
| Notes | **RECOMMENDED architecture model.** Cherry-pick specific tools not covered by existing Kali MCP. Top candidates: Ghidra, YARA, capa, radare2 (binary analysis not in current arsenal). |

---

## Category 3 — Kali Linux MCP Bridges

### [KL-01] Official Kali MCP Server
| Gate | Assessment |
|---|---|
| V1 Source | ✅ Official Offensive Security / Kali.org package. |
| V2 Outbound | ✅ SSH transport — local only. |
| V3 Code | ✅ Official package, source available. |
| V4 Supply | ✅ `sudo apt install mcp-kali-server`. Official Kali repo. |
| V5 Blast | ⚠️ Full Kali tool access — same as any Kali deployment. |
| **Rating** | **⚠️ CAUTION** — Rule C4 applies. Heavy overlap with existing 62-tool Kali MCP already operational. |
| Notes | Only valuable if it adds capabilities missing from the current custom Kali MCP. Low priority unless capability gap identified. |

### [KL-02] Wh0am123/MCP-Kali-Server
| Gate | Assessment |
|---|---|
| V1 Source | ⚠️ Individual author `Wh0am123`. Unknown. |
| V2 Outbound | ⚠️ Flask API bridge — opens HTTP port. |
| V3 Code | ⚠️ Open source. |
| V4 Supply | ⚠️ Flask. pip deps. |
| V5 Blast | 🔴 **Raw command execution exposed.** No sandboxing beyond Flask. |
| **Rating** | **🔴 HOLD** |
| Notes | Raw command exec + unknown author. Existing Kali MCP is superior. See Section F. |

### [KL-03] Zebbern Kali
| Gate | Assessment |
|---|---|
| V1 Source | 🔴 mcpmarket.com listing only. Primary repo unlocated. Author unknown. |
| V2 Outbound | ⚠️ Unknown without source audit. |
| V3 Code | 🔴 **FAIL** — no primary repo to audit. |
| V4 Supply | 🔴 **FAIL** — install method unverifiable. |
| V5 Blast | 🔴 139 functions, 22 external tools — massive surface. AD tools (BloodHound, Kerberoasting) are high-value but high-risk. |
| **Rating** | **🔴 HOLD** |
| Notes | Cannot audit. Interesting AD coverage but unverifiable. See Section F. |

---

## Category 4 — Specific Tool MCP Servers

### [SP-01] Metasploit Framework MCP
| Gate | Assessment |
|---|---|
| V1 Source | ⚠️ `GH05TCREW` — PulseMCP listing. Need primary repo. Metasploit itself is trusted (Rapid7), but this MCP wrapper is third-party. |
| V2 Outbound | ⚠️ Metasploit payloads generate network traffic by design. |
| V3 Code | 🔴 **FAIL** — primary repo not located from PulseMCP listing. Cannot audit wrapper. |
| V4 Supply | 🔴 Unknown install method. |
| V5 Blast | 🔴 Exploit execution, payload gen, session management. Maximum blast radius. |
| **Rating** | **🔴 HOLD** |
| Notes | Metasploit is already available in existing Kali MCP. This wrapper adds no confirmed net-new capability. Source unlocatable. See Section F. |

### [SP-02] Burp Suite MCP — swgee/BurpMCP
| Gate | Assessment |
|---|---|
| V1 Source | ⚠️ `swgee` — known community contributor. Active maintenance noted. |
| V2 Outbound | ⚠️ Burp Collaborator payloads contact PortSwigger's infrastructure for OOB testing. This is by-design but data leaves Eddie's machine. |
| V3 Code | ✅ Open source on GitHub. |
| V4 Supply | ✅ Standard Burp extension install. |
| V5 Blast | ⚠️ Replays HTTP requests, generates payloads. Medium blast radius — scoped to web testing. |
| **Rating** | **⚠️ CAUTION** — V2 caveat: Collaborator payloads are outbound to PortSwigger. Acceptable for pentest use but Eddie should be aware. |
| Notes | Deprioritize in favor of SP-03 (official PortSwigger) if both available. |

### [SP-03] Burp Suite MCP — PortSwigger Official
| Gate | Assessment |
|---|---|
| V1 Source | ✅ **PortSwigger** — Burp Suite vendor. Official release. |
| V2 Outbound | ⚠️ Same Collaborator caveat as SP-02 — inherent to Burp. |
| V3 Code | ✅ Official open source repo `PortSwigger/mcp-server`. |
| V4 Supply | ✅ Official extension distribution. |
| V5 Blast | ⚠️ Same as SP-02 — scoped to web testing. |
| **Rating** | **✅ CLEAR** |
| Notes | **Prefer this over SP-02.** Official vendor guarantee. Requires Burp Suite Pro license. |

### [SP-04] Shodan MCP
| Gate | Assessment |
|---|---|
| V1 Source | ✅ BurtTheCoder — prolific, known MCP author. Multiple well-maintained MCP servers. |
| V2 Outbound | ⚠️ Queries Shodan API — data goes to Shodan servers. API key stays in local env. **Shodan queries are logged on Shodan's side.** |
| V3 Code | ✅ Fully open source. NPM package `@burtthecoder/mcp-shodan`. |
| V4 Supply | ✅ NPM. Dependencies manageable. |
| V5 Blast | ✅ Read-only reconnaissance. No write operations to targets. |
| **Rating** | **⚠️ CAUTION** — Clear with V2 caveat: Shodan logs queries server-side. |
| Notes | **UNIQUE DATA SOURCE** — Kali MCP cannot replicate Shodan's indexed internet data. High strategic value. Requires Shodan API key. |

### [SP-05] Nuclei MCP
| Gate | Assessment |
|---|---|
| V1 Source | ⚠️ `addcontent` — individual author. |
| V2 Outbound | ⚠️ Nuclei scans targets — outbound by design. |
| V3 Code | ✅ Open source. |
| V4 Supply | ⚠️ Python. |
| V5 Blast | ⚠️ Active vulnerability scanning of targets. |
| **Rating** | **⚠️ CAUTION** — Nuclei already available in Kali MCP. Rule C4: prefer FuzzingLabs containerized version for isolation. |

### [SP-06] GhidraMCP
| Gate | Assessment |
|---|---|
| V1 Source | ✅ LaurieWired — well-known RE/security content creator, respected community figure. |
| V2 Outbound | ⚠️ HTTP bridge on configurable port. **Must confirm local-only binding (127.0.0.1).** |
| V3 Code | ✅ Open source Java (Ghidra plugin) + Python bridge. Apache-2.0 licensed. |
| V4 Supply | ✅ Ghidra extension ZIP install. Standard. |
| V5 Blast | ✅ Scoped to Ghidra operations — decompile, analyze, rename. No network/filesystem writes beyond Ghidra project. |
| **Rating** | **✅ CLEAR** (pending V2 local-bind confirmation) |
| Notes | **Complements dnSpy MCP** — Ghidra handles native binaries (C/C++/Go/Rust), dnSpy handles .NET. Together they cover the full RE spectrum. |

### [SP-07] BloodHound MCP
| Gate | Assessment |
|---|---|
| V1 Source | ✅ **SpecterOps** — BloodHound vendor. Official release. `mwnickerson/bloodhound_mcp` on GitHub. |
| V2 Outbound | ✅ Queries local BloodHound CE Neo4j instance. No outbound. |
| V3 Code | ✅ Open source. |
| V4 Supply | ✅ Python. Standard deps. |
| V5 Blast | ✅ Read-only graph queries. Cannot modify AD environment. |
| **Rating** | **✅ CLEAR** |
| Notes | **UNIQUE CAPABILITY** — AD attack path graph analysis via natural language. Not available in Kali MCP. Requires BloodHound CE running locally (Neo4j + API). |

### [SP-08] Mythic C2 MCP
| Gate | Assessment |
|---|---|
| V1 Source | ✅ xpn (Adam Chester) — **SpecterOps** infosec researcher. Highly respected. |
| V2 Outbound | ⚠️ Interfaces with Mythic C2 framework — C2 traffic is inherently outbound. |
| V3 Code | ⚠️ Repo not confirmed as publicly listed. PoC status. May be private or gist. |
| V4 Supply | ⚠️ PoC — no formal package. |
| V5 Blast | 🔴 **C2 operations** — command and control is maximum blast radius by definition. |
| **Rating** | **⚠️ CAUTION** — Author is trusted. PoC status and C2 blast radius require careful lab-only deployment. |
| Notes | Only relevant if Eddie has Mythic C2 deployed. Lab-only. |

### [SP-09] Cobalt Strike MCP
| Gate | Assessment |
|---|---|
| V1 Source | 🔴 **FAIL** — PulseMCP listing only. No primary repo. No author identified. |
| V2 Outbound | Unknown. |
| V3 Code | 🔴 **FAIL** — cannot audit. |
| V4 Supply | 🔴 **FAIL** — no install method. |
| V5 Blast | 🔴 C2 operations — maximum blast. |
| **Rating** | **❌ REJECT** |
| Notes | Cannot verify source, cannot audit code, C2 blast radius. Rejected until verifiable source produced. |

---

## Category 5 — OSINT & Reconnaissance

### [OS-01] BurtTheCoder/mcp-dnstwist
| Gate | Assessment |
|---|---|
| V1 Source | ✅ BurtTheCoder — known, prolific MCP author. |
| V2 Outbound | ⚠️ DNS queries to resolve fuzzy domain permutations. Expected for the use case. |
| V3 Code | ✅ Open source. |
| V4 Supply | ✅ NPM. |
| V5 Blast | ✅ Read-only DNS reconnaissance. |
| **Rating** | **✅ CLEAR** |

### [OS-02] BurtTheCoder/mcp-maigret
| Gate | Assessment |
|---|---|
| V1 Source | ✅ BurtTheCoder. |
| V2 Outbound | ⚠️ Queries social media platforms to check username existence. Many outbound HTTP requests to third-party sites. |
| V3 Code | ✅ Open source. |
| V4 Supply | ✅ NPM. |
| V5 Blast | ✅ Read-only OSINT. |
| **Rating** | **⚠️ CAUTION** — V2: many outbound requests to social platforms. Could trigger rate limits or IP flags. |

### [OS-03] MorDavid/ExternalAttacker-MCP
| Gate | Assessment |
|---|---|
| V1 Source | ⚠️ Individual author. Unknown. |
| V2 Outbound | ⚠️ Attack surface mapping implies outbound scanning. |
| V3 Code | ⚠️ Source needs audit. |
| V4 Supply | ⚠️ Unknown without source audit. |
| V5 Blast | ⚠️ External recon — scoped to read-only scanning. |
| **Rating** | **🔴 HOLD** |
| Notes | Unknown author + unaudited. See Section F. |

### [OS-04] Censys Threat Hunting MCP
| Gate | Assessment |
|---|---|
| V1 Source | ✅ **Censys** — reputable threat intelligence firm. Official product. |
| V2 Outbound | ⚠️ Queries Censys API. API key required. **Queries are logged on Censys side.** |
| V3 Code | ✅ Official documentation available. |
| V4 Supply | ✅ Official SDK/CLI from Censys. |
| V5 Blast | ✅ Read-only threat intelligence queries. |
| **Rating** | **⚠️ CAUTION** — Same class as Shodan: V2 caveat re: server-side query logging. |
| Notes | **UNIQUE DATA SOURCE** — C2 infrastructure detection, certificate pivoting, ASN analysis. Complements Shodan for different data set. |

### [OS-05] Nae-bo External Recon MCP
| Gate | Assessment |
|---|---|
| V1 Source | ⚠️ Unknown author. |
| V2 Outbound | ⚠️ DNS/WHOIS/HTTP queries — outbound. |
| V3 Code | ⚠️ Source needs audit. |
| V4 Supply | ⚠️ Unknown. |
| V5 Blast | ✅ Read-only recon. |
| **Rating** | **🔴 HOLD** |
| Notes | Unknown author. DNS/WHOIS already available in Kali MCP. See Section F. |

---

## Category 6 — Malware Analysis & Reverse Engineering

### [RE-01] REMnux MCP Server
| Gate | Assessment |
|---|---|
| V1 Source | ✅ **Lenny Zeltser** — creator and official maintainer of REMnux. SANS instructor. Top-tier authority. |
| V2 Outbound | ✅ Local tool execution. No outbound telemetry. |
| V3 Code | ✅ Open source. NPM `@remnux/mcp-server`. |
| V4 Supply | ✅ NPM. Official REMnux package. |
| V5 Blast | ⚠️ 200+ malware analysis tools — but scoped to analysis of provided samples. No autonomous network activity. |
| **Rating** | **✅ CLEAR** |
| Notes | **HIGHEST-VALUE RE server in briefing.** Practitioner knowledge encoded. Auto-summarizes output >32KB. Requires REMnux VM or Docker image. |

### [RE-02] MalwareMCP (dnSpy-based)
| Gate | Assessment |
|---|---|
| V1 Source | ⚠️ Primary repo not specified in briefing. Source needs location. |
| V2 Outbound | ⚠️ Unknown without source. |
| V3 Code | 🔴 **FAIL** — cannot locate primary repo. |
| V4 Supply | 🔴 Unknown. |
| V5 Blast | ⚠️ RE tools — scoped to analysis. |
| **Rating** | **🔴 HOLD** |
| Notes | dnSpy MCP already operational. Cannot audit this alternative. See Section F. |

### [RE-03] FuzzingLabs Binary Analysis Suite
| Gate | Assessment |
|---|---|
| V1 Source | ✅ FuzzingLabs — known firm. Same as PF-05. |
| V2 Outbound | ✅ Docker-isolated. |
| V3 Code | ✅ Open source. |
| V4 Supply | ✅ Docker Compose, modular. |
| V5 Blast | ✅ Container isolation. |
| **Rating** | **✅ CLEAR** |
| Notes | Cherry-pick radare2, YARA, capa, binwalk from this suite. These fill gaps not covered by dnSpy (native binary analysis). |

### [RE-04] VirusTotal MCP
| Gate | Assessment |
|---|---|
| V1 Source | ✅ BurtTheCoder. Known author. |
| V2 Outbound | ⚠️ Queries VirusTotal API. API key required. |
| V3 Code | ✅ Open source. NPM `@burtthecoder/mcp-virustotal`. |
| V4 Supply | ✅ NPM. |
| V5 Blast | ✅ Read-only query API. |
| **Rating** | **⚠️ CAUTION** |

> [!CAUTION]
> **Files submitted to VirusTotal are NOT private.** Any sample uploaded becomes accessible to premium VT subscribers. Eddie must never submit sensitive/proprietary samples. Query-by-hash is safe; upload is not.

---

## Category 7 — Detection Engineering & Purple Team

### [DE-01] Security Detections MCP (MHaggis)
| Gate | Assessment |
|---|---|
| V1 Source | ✅ MHaggis — same trusted author as ATK-04. |
| V2 Outbound | ✅ Local processing. Downloads Sigma/Splunk/Elastic rule packs. |
| V3 Code | ✅ Fully open source. `MHaggis/Security-Detections-MCP`. |
| V4 Supply | ✅ pip/uv. |
| V5 Blast | ✅ Read-only detection rule analysis. Knowledge graphs are local. |
| **Rating** | **✅ CLEAR** |
| Notes | **KILLER COMBO with ATK-04.** ATT&CK MCP + Security Detections MCP = full detection coverage gap analysis. |

### [DE-02] Promptfoo Evil MCP Server
| Gate | Assessment |
|---|---|
| V1 Source | ✅ **Promptfoo** — known AI security testing firm. |
| V2 Outbound | ⚠️ Simulates data exfiltration — **by design**. |
| V3 Code | ✅ Fully open source. `promptfoo/evil-mcp-server`. |
| V4 Supply | ✅ NPM/GitHub. |
| V5 Blast | 🔴 **BY DESIGN** — this server simulates malicious MCP behavior including data exfiltration, tool poisoning, and prompt injection. |
| **Rating** | **⚠️ CAUTION** — SPECIAL HANDLING REQUIRED |

> [!WARNING]
> **DE-02 MUST NEVER appear in production `mcp.json`.** Requires fully isolated test configuration. See Section G for isolation protocol.

### [DE-03] OT Security MCP (Ansvar Systems)
| Gate | Assessment |
|---|---|
| V1 Source | ⚠️ Ansvar Systems — firm legitimacy not confirmed. |
| V2 Outbound | ✅ Read-only standards mapping. |
| V3 Code | ✅ Open source. `Ansvar-Systems/ot-security-mcp`. |
| V4 Supply | ✅ Python/pip. |
| V5 Blast | ✅ Knowledge layer only. ICS standards compliance mapping. |
| **Rating** | **⚠️ CAUTION** — V1 needs verification. Deprioritize unless ICS/OT targets are in scope. |

---

## Category 8 — C2 / Post-Exploitation

### [C2-01] Mythic C2 MCP → See SP-08
### [C2-02] Cobalt Strike MCP → See SP-09 (❌ REJECT)
### [C2-03] Atomic Red Team Execution Mode → See ART-01 (⚠️ CAUTION — execution disabled by default)

### [C2-04] Vectra AI Swarm C2 Research Paper
| **Action** | READ ONLY — no installation. Extract architectural insights. |
| **Relevance** | Event-driven MCP C2 patterns vs. periodic beaconing. Informs chain-of-prime design. |
| **Rating** | N/A — research material, not a server. |

---

# SECTION B — REDUNDANCY ASSESSMENT

Servers whose capabilities are **already covered** by the existing 62-tool Kali MCP:

| Server | Overlap | Justification |
|---|---|---|
| [PF-02] HexStrike AI | **HIGH** | 150+ tools — massive overlap with Kali MCP's 18 categories. |
| [PF-03] Offensive Toolkit | **HIGH** | Nmap, SQLMap, Nuclei, Subfinder all in Kali already. |
| [KL-01] Official Kali MCP | **HIGH** | Same Kali toolset, different transport. |
| [KL-02] Wh0am123 Kali | **HIGH** | Subset of existing Kali MCP tools. |
| [KL-03] Zebbern Kali | **HIGH** | Extended Kali toolset — interesting AD coverage but unverifiable. |
| [SP-01] Metasploit MCP | **HIGH** | Metasploit already accessible via Kali MCP. |
| [SP-05] Nuclei MCP | **MEDIUM** | Nuclei available in Kali. Standalone adds no new layer. |
| [OS-05] Nae-bo Recon | **MEDIUM** | DNS/WHOIS/dnsrecon all in Kali already. |

> [!NOTE]
> These are deprioritized per Rule C4 unless they add **structured data layers** (graphs, knowledge bases, ATT&CK mappings) that raw Kali tool output cannot produce.

---

# SECTION C — NET NEW CAPABILITY CATALOG

Only servers that pass vetting AND add genuine new capability:

### TIER 1 — Strategic Force Multipliers

| ID | Name | Capability | Install | Port | Prereqs | Effort | Priority |
|---|---|---|---|---|---|---|---|
| ATK-04 | MITRE ATT&CK MCP (MHaggis) | ATT&CK knowledge layer + Navigator generation. No equivalent in current arsenal. | `pip install mitre-attack-mcp` | None (stdio) | None | LOW | **TIER 1** |
| DE-01 | Security Detections MCP | Sigma/Splunk/Elastic rule analysis + coverage gap mapping. Pairs with ATK-04. | `pip install security-detections-mcp` | None (stdio) | None | LOW | **TIER 1** |
| SP-04 | Shodan MCP | Internet-wide device/service/vuln data. Unique data source not replicable locally. | `npx -y @burtthecoder/mcp-shodan` | None (stdio) | Shodan API key | LOW | **TIER 1** |
| SP-07 | BloodHound MCP | AD attack path graph analysis via natural language. Unique graph capability. | `pip install bloodhound-mcp` | None (stdio) | BloodHound CE (Neo4j + API) | MEDIUM | **TIER 1** |
| ART-01 | Atomic Red Team MCP | 1,500+ ATT&CK-mapped adversary emulation tests. Query-only mode is zero-risk. | `uvx atomic-red-team-mcp` | None (stdio) | None (query mode) | LOW | **TIER 1** |

### TIER 2 — Capability Extensions

| ID | Name | Capability | Install | Port | Prereqs | Effort | Priority |
|---|---|---|---|---|---|---|---|
| SP-06 | GhidraMCP | Native binary RE (C/C++/Go/Rust). Complements dnSpy for .NET. Full RE coverage. | Ghidra extension ZIP | HTTP (configurable, e.g. 18489) | Ghidra installed | MEDIUM | **TIER 2** |
| RE-01 | REMnux MCP | 200+ malware analysis tools with practitioner AI guidance. Unique knowledge layer. | `npm install @remnux/mcp-server` | None (stdio) | REMnux VM or Docker | MEDIUM | **TIER 2** |
| SP-03 | Burp Suite MCP (Official) | Web app security testing via MCP. Official vendor integration. | Burp extension install | HTTP (configurable) | Burp Suite Pro license | MEDIUM | **TIER 2** |
| OS-04 | Censys MCP | C2 detection, cert pivoting, ASN analysis. Different data than Shodan. | Official Censys SDK | None (stdio) | Censys API key | LOW | **TIER 2** |
| RE-04 | VirusTotal MCP | Malware hash/URL/IP reputation queries. Vast community intelligence. | `npx -y @burtthecoder/mcp-virustotal` | None (stdio) | VT API key | LOW | **TIER 2** |
| OS-01 | dnstwist MCP | Phishing domain detection via DNS fuzzing. Unique phishing defense capability. | `npx -y @burtthecoder/mcp-dnstwist` | None (stdio) | None | LOW | **TIER 2** |

### TIER 3 — Specialized / Conditional

| ID | Name | Capability | Install | Port | Prereqs | Effort | Priority |
|---|---|---|---|---|---|---|---|
| PF-05 | FuzzingLabs Hub | Modular Docker security tools (cherry-pick radare2, YARA, capa). | Docker Compose (per-tool) | Varies per container | Docker | HIGH | **TIER 3** |
| OS-02 | Maigret MCP | Username OSINT across platforms. | `npx -y @burtthecoder/mcp-maigret` | None (stdio) | None | LOW | **TIER 3** |
| DE-02 | Promptfoo Evil MCP | Red team Eddie's own MCP stack. **Isolated config only.** | NPM/GitHub | None (stdio) | Isolated test config | MEDIUM | **TIER 3** |
| SP-08 | Mythic C2 MCP | LLM-automated C2 ops. Lab-only. | Source install (PoC) | None (stdio) | Mythic C2 running | HIGH | **TIER 3** |
| ATK-01 | ATT&CK MCP (Montimage) | Production-grade ATT&CK with O(1) lookups. Backup if ATK-04 insufficient. | `pip install mitre-mcp` | None (stdio) | None | LOW | **TIER 3** |
| DE-03 | OT Security MCP | ICS/OT standards mapping. Only if OT targets in scope. | `pip install ot-security-mcp` | None (stdio) | None | LOW | **TIER 3** |

---

# SECTION D — PRIORITIZED TODO LIST

## [ ] TIER 1 — Implement First (Highest Strategic Value)

1. **[ATK-04] MITRE ATT&CK MCP (MHaggis)** — `pip install mitre-attack-mcp` — No prereqs
2. **[DE-01] Security Detections MCP** — `pip install security-detections-mcp` — No prereqs
3. **[ART-01] Atomic Red Team MCP** — `uvx atomic-red-team-mcp` — No prereqs (keep `ART_EXECUTION_ENABLED=false`)
4. **[SP-04] Shodan MCP** — `npx -y @burtthecoder/mcp-shodan` — Requires Shodan API key
5. **[SP-07] BloodHound MCP** — pip install — Requires BloodHound CE deployment

- [ ] **TIER 1 Housekeeping Checkpoint**
  - Workspace audit
  - Confirm all 5 servers respond in mcp.json
  - Test one query per server
  - No orphaned processes or ports
  - Backup mcp.json

## [ ] TIER 2 — Implement After Tier 1 Stable

1. **[SP-06] GhidraMCP** — Ghidra extension — Confirm local-only HTTP binding
2. **[RE-01] REMnux MCP** — npm install — Requires REMnux environment
3. **[SP-03] Burp MCP (Official)** — Burp extension — Requires Burp Pro license
4. **[OS-04] Censys MCP** — Censys SDK — Requires Censys API key
5. **[RE-04] VirusTotal MCP** — npx — Requires VT API key
6. **[OS-01] dnstwist MCP** — npx — No prereqs

- [ ] **TIER 2 Housekeeping Checkpoint**
  - Workspace audit
  - Verify no port collisions (GhidraMCP HTTP port, Burp HTTP port)
  - Backup mcp.json
  - Confirm all active servers still operational

## [ ] TIER 3 — Specialized / Conditional

1. **[PF-05] FuzzingLabs Hub** — Docker Compose cherry-pick (radare2, YARA, capa)
2. **[OS-02] Maigret MCP** — npx
3. **[DE-02] Promptfoo Evil MCP** — **ISOLATED CONFIG ONLY** — see Section G
4. **[SP-08] Mythic C2 MCP** — source install — only if Mythic deployed
5. **[ATK-01] Montimage ATT&CK** — pip — only if ATK-04 proves insufficient
6. **[DE-03] OT Security MCP** — pip — only if OT targets in scope

- [ ] **TIER 3 Housekeeping Checkpoint**
  - Final workspace audit
  - Archive staging folder to `E:\Thales\Thon\reports\arsenal_expansion_2026-03-10\`
  - Final mcp.json backup
  - Confirm clean state — nothing running that shouldn't be

---

# SECTION E — DEPENDENCY & PREREQ MAP

## API Keys Required

| Server | Key | Where to Obtain |
|---|---|---|
| SP-04 Shodan MCP | `SHODAN_API_KEY` | [account.shodan.io](https://account.shodan.io) — free tier available, paid for full access |
| OS-04 Censys MCP | `CENSYS_API_ID` + `CENSYS_API_SECRET` | [search.censys.io/account/api](https://search.censys.io/account/api) — free tier available |
| RE-04 VirusTotal MCP | `VIRUSTOTAL_API_KEY` | [virustotal.com/gui/my-apikey](https://www.virustotal.com/gui/my-apikey) — free tier available |

## Docker Images to Pre-Pull

| Image | Required By | Approx Size |
|---|---|---|
| REMnux Docker image | RE-01 REMnux MCP | ~2-3GB |
| FuzzingLabs per-tool images | PF-05 (radare2, YARA, capa) | ~500MB each |

## External Services to Stand Up First

| Service | Required By | Setup Notes |
|---|---|---|
| BloodHound CE | SP-07 BloodHound MCP | Neo4j + BloodHound API. Docker Compose available from SpecterOps. |
| Ghidra (local install) | SP-06 GhidraMCP | Download from ghidra-sre.org. Java required. |
| Burp Suite Pro | SP-03 Burp MCP | Licensed product. PortSwigger account required. |
| Mythic C2 | SP-08 Mythic C2 MCP | Full C2 framework. Lab-only. Docker-based. |

## Accounts or Licenses Needed

| Account/License | Required By |
|---|---|
| Shodan account | SP-04 |
| Censys account | OS-04 |
| VirusTotal account | RE-04 |
| Burp Suite Pro license | SP-03 |
| (Optional) Mythic C2 | SP-08 |

## Staging Folders to Create

| Path | Status |
|---|---|
| `E:\Thales\Thon\staging\arsenal_expansion\` | ✅ Created |
| `E:\Thales\Thon\backups\mcp_json\` | ✅ Created |
| `E:\Thales\Thon\reports\` | ✅ Created |

---

# SECTION F — SECURITY FLAGS (HOLD / REJECT)

## ❌ REJECTED

### [SP-09] Cobalt Strike MCP
| Field | Value |
|---|---|
| Rating | ❌ **REJECT** |
| Gates Failed | V1 (no author), V3 (no source), V4 (no install method) |
| Condition to Clear | Eddie must produce a verifiable source repository with auditable code. Until then, permanently excluded. |

---

## 🔴 HELD

### [PF-01] RedAmon
| Field | Value |
|---|---|
| Rating | 🔴 **HOLD** |
| Gates Failed | V2 (ngrok/chisel outbound), V4 (privileged Docker caps), V5 (maximum blast radius) |
| Condition to Clear | Eddie must accept: privileged container capabilities (NET_ADMIN, NET_RAW, SYS_PTRACE), ~15GB Docker footprint, and reverse shell capability. Recommend lab-only deployment on isolated VM/network. |

### [PF-02] HexStrike AI
| Field | Value |
|---|---|
| Rating | 🔴 **HOLD** |
| Gates Failed | V1 (unknown author `0x4m4`), V5 (massive attack surface) |
| Condition to Clear | Source audit by Eddie. Also Rule C4 — heavy overlap with existing Kali MCP. Low value-add. |

### [PF-03] Offensive Toolkit (Joas Antonio)
| Field | Value |
|---|---|
| Rating | 🔴 **HOLD** |
| Gates Failed | V3 (primary repo unlocated), V4 (install method unknown) |
| Condition to Clear | Locate primary source repo. PulseMCP listing insufficient. |

### [PF-04] PentestAgent
| Field | Value |
|---|---|
| Rating | 🔴 **HOLD** |
| Gates Failed | V1 (unknown author), V2 (RAG data flow unclear) |
| Condition to Clear | Confirm RAG vectors stored locally only. Source audit by Eddie. |

### [KL-02] Wh0am123 Kali
| Field | Value |
|---|---|
| Rating | 🔴 **HOLD** |
| Gates Failed | V1 (unknown author), V5 (raw command execution) |
| Condition to Clear | Not recommended — existing Kali MCP is superior. Only reconsider if specific need arises. |

### [KL-03] Zebbern Kali
| Field | Value |
|---|---|
| Rating | 🔴 **HOLD** |
| Gates Failed | V1 (unknown author), V3 (no primary repo), V4 (unverifiable install) |
| Condition to Clear | Locate primary source repo. mcpmarket.com listing insufficient. |

### [SP-01] Metasploit MCP
| Field | Value |
|---|---|
| Rating | 🔴 **HOLD** |
| Gates Failed | V3 (primary repo unlocated), V4 (unknown install) |
| Condition to Clear | Locate `GH05TCREW` primary repo. Also Rule C4 — Metasploit already in Kali MCP. |

### [OS-03] ExternalAttacker MCP
| Field | Value |
|---|---|
| Rating | 🔴 **HOLD** |
| Gates Failed | V1 (unknown author `MorDavid`) |
| Condition to Clear | Source audit by Eddie. |

### [OS-05] Nae-bo Recon MCP
| Field | Value |
|---|---|
| Rating | 🔴 **HOLD** |
| Gates Failed | V1 (unknown author), Rule C4 (DNS/WHOIS in Kali) |
| Condition to Clear | Low value. Not recommended unless specific need arises. |

### [RE-02] MalwareMCP
| Field | Value |
|---|---|
| Rating | 🔴 **HOLD** |
| Gates Failed | V3 (primary repo unlocated) |
| Condition to Clear | Locate primary repo. dnSpy MCP already operational for .NET RE. |

---

# SECTION G — ARCHITECTURE & CONFLICT NOTES

## Port Conflict Map

| Server | Port | Conflict? |
|---|---|---|
| Existing: Paperless-ngx | 8000 | — |
| Existing: Uptime Kuma | 3001 | — |
| Existing: Portainer | 9443 | — |
| Existing: Vaultwarden | 8343 | — |
| Existing: UltraVNC | 5900 | — |
| Existing: QuickBooks OAuth | 8085 | ⚠️ Shares with Guacamole |
| Existing: Guacamole | 8085 | ⚠️ Shares with QuickBooks OAuth |
| Existing: BookStack | 6875 | — |
| Existing: Duplicati | 8200 | — |
| Existing: NPM | 81 | — |
| Existing: BillionMail | 80 | — |
| **New: GhidraMCP** | **18489** (default) | ✅ No conflict |
| **New: Burp MCP** | **8099** (typical) | ✅ No conflict — verify at install |
| **New: FuzzingLabs** | **Varies per container** | ✅ Verify per-tool at install |

> [!IMPORTANT]
> Port 8085 is shared between QuickBooks OAuth redirect and Guacamole. Not a new conflict but worth noting. Both are currently disabled.

## Tool Name Collision Candidates

| New Server | Tool Name | Potential Collision |
|---|---|---|
| ATK-04 / ATK-01 | `search_techniques`, `get_technique` | Multiple ATT&CK MCPs could collide if both registered. **Only register ONE ATT&CK MCP at a time.** |
| SP-06 GhidraMCP | `decompile`, `list_functions` | Potential namespace overlap with dnSpy MCP tools (`dnspy_decompile_type`, `dnspy_list_types`). **No actual collision** — dnSpy tools are prefixed with `dnspy_`. Ghidra tools should be confirmed as prefixed. |

> [!TIP]
> Recommend establishing naming convention: all new MCP server tools should be namespace-prefixed (e.g., `ghidra_`, `shodan_`, `art_`).

## Chain-of-Prime Integration Candidates

Servers that fit naturally into autonomous agent orchestration:

1. **ATK-04 + DE-01** → Autonomous detection gap analysis pipeline: Ingest ATT&CK → map detections → identify gaps → generate recommendations
2. **ART-01 + ATK-04** → Identify technique → query atomic test → validate detection coverage
3. **SP-04 (Shodan) + OS-04 (Censys)** → Multi-source external recon enrichment with cross-reference
4. **SP-07 (BloodHound) + Kali MCP** → Graph-guided AD attack path → tool execution chain
5. **RE-01 (REMnux) + dnSpy MCP** → Malware triage pipeline: REMnux for initial analysis → dnSpy for .NET payloads

## High-Value Server Pairs

| Pair | Multiplier Effect |
|---|---|
| **ATK-04 + DE-01** | Full ATT&CK coverage gap analysis. Neither is useful alone at this level. |
| **GhidraMCP + dnSpy MCP** | Complete RE coverage: native + managed binaries. |
| **Shodan + Censys** | Complementary internet intelligence — different indices, different strengths. |
| **BloodHound MCP + Kali MCP** | Graph-informed AD exploitation. BloodHound identifies paths, Kali executes. |
| **ART-01 + ATK-04 + DE-01** | Full purple team loop: emulate → detect → gap analysis. |

## mcp.json Entry Templates

Ready-to-paste config blocks for each approved TIER 1 server:

```json
"mitre-attack": {
  "command": "C:\\Users\\Dallas\\AppData\\Roaming\\Python\\Python314\\Scripts\\uv.exe",
  "args": ["run", "--directory", "F:/openclaw-rts/mcp-servers/mitre-attack-mcp", "server.py"],
  "env": {}
}
```

```json
"security-detections": {
  "command": "C:\\Users\\Dallas\\AppData\\Roaming\\Python\\Python314\\Scripts\\uv.exe",
  "args": ["run", "--directory", "F:/openclaw-rts/mcp-servers/security-detections-mcp", "server.py"],
  "env": {}
}
```

```json
"atomic-red-team": {
  "command": "uvx",
  "args": ["atomic-red-team-mcp"],
  "env": {
    "ART_EXECUTION_ENABLED": "false"
  }
}
```

```json
"shodan": {
  "command": "npx",
  "args": ["-y", "@burtthecoder/mcp-shodan"],
  "env": {
    "SHODAN_API_KEY": "YOUR_SHODAN_API_KEY"
  }
}
```

```json
"bloodhound": {
  "command": "C:\\Users\\Dallas\\AppData\\Roaming\\Python\\Python314\\Scripts\\uv.exe",
  "args": ["run", "--directory", "F:/openclaw-rts/mcp-servers/bloodhound-mcp", "server.py"],
  "env": {
    "BLOODHOUND_URL": "http://localhost:8080",
    "BLOODHOUND_TOKEN": "YOUR_BH_TOKEN"
  }
}
```

> [!NOTE]
> Templates use `F:/openclaw-rts/mcp-servers/` as the standard MCP server directory, consistent with existing server installs. Actual commands may differ based on whether the server is cloned locally or run via package manager. Finalize at install time.

## DE-02 Isolation Protocol

> [!CAUTION]
> **Promptfoo Evil MCP Server — Isolation Requirements:**
>
> 1. **NEVER** add to production `mcp.json` (`C:\Users\Dallas\.cursor\mcp.json` or `mcp_config.json`)
> 2. Create dedicated test config: `E:\Thales\Thon\staging\evil_mcp_test\mcp_test.json`
> 3. Run with a separate Cursor/IDE profile pointed at the test config
> 4. No other MCP servers registered alongside it during testing
> 5. Test results documented before server is removed
> 6. Test config deleted after exercise complete

## Vectra Swarm C2 Paper — Architectural Insights

| Insight | Relevance to Chain-of-Prime |
|---|---|
| **Event-driven vs. periodic beaconing** | Chain-of-prime agents should use event-driven MCP calls rather than polling loops. Reduces detection surface and improves responsiveness. |
| **Swarm coordination patterns** | Multiple MCP agents can coordinate without central controller — each agent monitors its own event stream and triggers next-stage agents via tool calls. |
| **Detection evasion** | Traditional C2 detection relies on periodic beacon timing analysis. Event-driven patterns with variable intervals are harder to fingerprint. |
| **Action: READ the paper** | Thon should study the full paper when Eddie provides access. No installation required. |

---

# REPORT FOOTER

| Field | Value |
|---|---|
| **Discrepancies** | 1. Port 8085 shared between QuickBooks OAuth and Guacamole in existing config (both disabled). 2. Multiple ATT&CK MCP options exist — only ONE should be registered to avoid tool name collisions. 3. Several briefing entries (SP-01, PF-03, RE-02) reference PulseMCP listings with no locatable primary repo. |
| **Open Questions** | 1. Does Eddie have a Shodan API key? (Needed for SP-04) 2. Does Eddie want to deploy BloodHound CE? (Required for SP-07 — MEDIUM effort) 3. Does Eddie have Burp Suite Pro license? (Required for SP-03) 4. Does Eddie want to stand up REMnux VM or Docker? (Required for RE-01) 5. Does Eddie have Censys API key? (Needed for OS-04) 6. Does Eddie have VirusTotal API key? (Needed for RE-04) 7. Should Thon proceed per-tier or does Eddie want all tiers authorized at once? 8. Should HELD servers undergo source audit by Thon, or does Eddie want to review them personally? |
| **Workspace Status** | ✅ **CLEAN** — Staging folders created. No installs performed. No configs modified. No orphaned processes. |
| **Next Action** | Eddie reviews this report and issues GO/NO-GO per server or per tier. Upon GO, Thon backs up mcp.json and begins Tier 1 implementation. |
| **Awaiting** | **EDDIE GO/NO-GO** |
