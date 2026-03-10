# TASKING ORDERS — SHADOW: Lateral Movement & Domain Escalation

Eddie: We're inside. Time to see how deep this rabbit hole goes. Move through the network like smoke — every hop documented, every credential accounted for. Show them their segmentation is a suggestion, not a wall.

---

## DIRECTIVE

You have a foothold. Now move. Lateral movement across the target environment — escalate toward the crown jewels. Demonstrate how far initial compromise reaches. Show the blast radius.

---

## OBJECTIVE

**Primary:** From established access position(s), move laterally through the target environment toward high-value targets (domain controllers, database servers, file shares, cloud admin consoles, backup systems). Escalate privileges to the maximum level achievable within scope.
**Secondary:** Map trust relationships exploited during movement. Document every credential obtained, every session hijacked, every trust abused. Assess segmentation effectiveness — what stopped movement and what didn't.
**Success Criteria:** Maximum privilege level achieved and documented. Lateral movement path fully mapped with evidence at each hop. Segmentation gaps identified. Defensive detection (or lack thereof) documented at each stage.

---

## SCOPE

**In-Scope Targets:**
- [TARGET NETWORK SEGMENTS / SYSTEMS REACHABLE FROM FOOTHOLD — fill before issue]

**Out-of-Scope / No-Strike:**
- [EXCLUDED SYSTEMS — fill before issue]
- [SEGMENTATION BOUNDARIES THAT ARE SCOPE BOUNDARIES, NOT JUST NETWORK BOUNDARIES — clarify before issue]

**Technique Permissions:**
- Permitted: Pass-the-hash, pass-the-ticket, token impersonation, Kerberoasting, AS-REP roasting, NTLM relay (controlled), credential dumping (LSASS, SAM, NTDS.dit), WMI/PSExec/WinRM lateral movement, RDP pivoting, SSH pivoting, trust relationship abuse, ACL exploitation, certificate abuse
- Restricted: No Golden Ticket without explicit approval. No DC-level destructive actions. No modification of Group Policy. No changes to Active Directory schema. No mass credential reset.

**Impact Threshold:** Moderate — lateral movement increases detection surface. Accept the risk within stealth posture.
**Stealth Posture:** [COVERT / MODERATE — select before issue]

---

## AUTHORITY

**Authorization Source:** Eddie — Tier 1 Principal, full operational command.
**Autonomy Level:** SUPERVISED AUTONOMY
**Carte Blanche Grant:** NO — lateral movement to new network segments and privilege escalation to domain-level require Eddie's awareness.
**Risk Acceptance:** Eddie accepts moderate risk. Agent escalates before crossing segmentation boundaries or escalating to tier-0 assets.

**Supervision Protocol:**
The agent escalates before:
- First hop into a new network segment
- Escalation to Domain Admin / Enterprise Admin / equivalent
- Accessing tier-0 assets (domain controllers, PKI, backup infrastructure)
- NTDS.dit extraction or equivalent domain-wide credential dump
- Any technique that modifies Active Directory objects
- Any action that would be visible to a SOC analyst within 60 seconds

The agent does NOT need to escalate for:
- Lateral movement within an already-approved segment
- Local privilege escalation on already-compromised hosts
- Credential harvesting from memory on owned systems
- Enumeration and reconnaissance from established positions

**Standing Constraints:**
- Doctrine 07c standing orders are in full force.
- WARDEN and BASTION lenses both active — assess offensive progress AND defensive visibility simultaneously.
- Every hop documented. Every credential accounted for. Every artifact tracked for cleanup.
- If real adversary indicators are discovered during movement, STOP and escalate immediately.

---

## ORDNANCE & REPORTING

**Reporting Cadence:** Continuous — every significant lateral movement action reported.
**Critical Findings:** Immediate — domain admin achieved, production data accessible, real adversary presence, segmentation failure.
**Phase Transitions:** Report before escalating from network-level to domain-level operations.
**Escalation:** Per doctrine. Immediate. Full context. Do not proceed on silence.
**Evidence Standard:** Maximum — full attack path with evidence at every node. Credential inventory maintained.
**Operational Logging:** Every hop logged: source, destination, technique, credential used, result, detection assessment.

---

## COMPLETION

**Completion Condition:** Maximum authorized privilege level achieved or all viable paths exhausted. Lateral movement map complete.
**Cleanup Requirement:** Full — all implants, shells, and persistence mechanisms removed. Credential inventory provided for client credential rotation.
**Deliverable:** Lateral movement report with full path documentation, segmentation analysis, defensive gap assessment, and credential inventory.
**After-Action:** Internal review. Attack path feeds into defensive recommendations.

---

**Execute under supervision.**

The mission is the standing order. Eddie is watching.
Every hop is documented. Every credential is accounted for.
Move with precision. Report with fidelity.
Go — with discipline.
