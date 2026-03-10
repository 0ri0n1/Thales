# Engagement Brief

> Copy this entire `engagement/` directory into the target device's `engagements/` folder.
> Rename to `YYYY-MM-DD_engagement-name/`.

## Phase 1 — Initiation

| Field | Value |
|-------|-------|
| Engagement Name | |
| Date Initiated | |
| Device | |
| Mission Type | |
| Target Definition | |
| Authorization Reference | |
| Scope Boundaries | |
| Rules of Engagement | |
| Success Criteria | |
| Principal (Eddie) Directives | |

### Authorization Checklist

- [ ] Written authorization obtained
- [ ] Scope boundaries documented in `scope/`
- [ ] Target IP ranges / SSIDs / hosts confirmed
- [ ] Exclusions explicitly listed
- [ ] Emergency contact identified
- [ ] Rollback plan documented

---

## Phase 2 — Reconnaissance

**Passive Recon:**
- [ ] Target enumeration complete
- [ ] Network topology mapped
- [ ] Findings logged in `recon/`

**Active Recon:**
- [ ] Service discovery complete
- [ ] Vulnerability scan complete
- [ ] Findings logged in `recon/`

---

## Phase 3 — Analysis

- [ ] Vulnerabilities prioritized (composite scoring)
- [ ] Attack paths identified
- [ ] Risk assessment complete
- [ ] Analysis notes in `recon/` or `evidence/`

---

## Phase 4 — Exploitation

| Authorization Level | Approved |
|---------------------|----------|
| Proof of Concept | [ ] |
| Controlled Exploitation | [ ] |
| Full Compromise | [ ] |

- [ ] Exploitation artifacts saved to `captures/`
- [ ] Screenshots/logs saved to `evidence/`
- [ ] Impact documented

---

## Phase 5 — Validation

- [ ] Detection validation complete
- [ ] Remediation recommendations drafted
- [ ] Adversary simulation assessment (if applicable)

---

## Phase 6 — Reporting

- [ ] Executive summary drafted in `report/`
- [ ] Technical findings documented
- [ ] Attack narrative written
- [ ] Detection assessment included
- [ ] Appendices (raw data, tool output) compiled

---

## Phase 7 — Closeout

- [ ] All captures archived
- [ ] Logs consolidated
- [ ] Lessons learned documented
- [ ] Memory/knowledge updates filed
- [ ] Engagement directory finalized

---

## Directory Usage

| Directory | Purpose |
|-----------|---------|
| `scope/` | Authorization documents, scope definitions, ROE, target lists |
| `recon/` | Scan results, enumeration output, network maps, OSINT |
| `captures/` | Exploit output, shells, credentials, pcaps, handshakes |
| `evidence/` | Screenshots, recordings, proof-of-exploitation artifacts |
| `logs/` | Tool logs, session logs, timestamps, audit trail |
| `report/` | Final deliverables — executive summary, technical report, appendices |
