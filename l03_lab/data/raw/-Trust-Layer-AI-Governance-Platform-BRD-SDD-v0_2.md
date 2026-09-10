# AI Governance & Compliance Platform — "Trust Layer"

## Enhanced Unified Business Requirements Document (BRD) & System Design Document (SDD)

**Document Version:** 0.2 (Enhanced — adds SDD, updates BRD with build status and evaluated open questions)
**Supersedes:** Trust Layer BRD v0.1 (Draft, July 25, 2026)
**Effective Date:** August 19, 2026
**Document Status:** For Review
**Companion documents:** [[pdpl-self-assessment-platform]] (v2.3, the only Trust Layer module actually built so far), [[global-data-privacy-program-brd]] BRD/SDD v1.1 (the complementary Data Governance Platform), the Open-Source AI & Cryptography Discovery/Scanning Vendor Evaluation, and the Business Requirements Feedback memo.

> **What changed since v0.1:** the original draft flagged four open questions (commercial model, go-to-market, build-vs-partner for discovery, jurisdiction priority) and described four modules with no build status attached to any of them. Since then: the Business Requirements Feedback memo answered the commercial-model and go-to-market questions; an open-source vendor evaluation answered the build-vs-partner question with real findings rather than a guess; and the Regulatory Rules Layer module has actually been built — as the PDPL/AI-governance self-assessment tool, now at v2.3, already covering nine frameworks (wider than v0.1's "EU AI Act + GDPR overlap, others phase 2+" scoping). This revision folds all of that in and adds the SDD half that v0.1 never had.

---

# PART 1: Business Requirements Document (BRD)

## 1. Executive Summary

The EU AI Act's phased rollout — further complicated by the 2026 Digital Omnibus amendments — has created sustained, multi-year demand for tooling that helps organizations discover, classify, document, and monitor their AI systems. Enterprises face three structural problems: they don't know what AI they're running (shadow AI), they don't know which risk tier it falls under, and they can't produce audit-ready evidence on demand.

This document defines business requirements and system design for **Trust Layer**, an AI governance and compliance platform unifying AI asset discovery, automated risk classification, and continuous audit-ready documentation. **One of its four planned modules — the Regulatory Rules Layer, plus a first version of the Documentation Engine — already exists**, delivered as the PDPL/AI-governance self-assessment platform. The other three (Discovery & Inventory, Risk Classification Engine, and a continuous/automated version of the Documentation Engine) remain unbuilt, and this revision is more specific than v0.1 about why, and what to do about it.

## 2. Business Context / Problem Statement

*(Unchanged from v0.1 — still accurate.)*

- Regulatory exposure is severe and enforceable now: penalties up to €35M or 7% of global turnover for prohibited practices, with GPAI enforcement and Article 50 transparency obligations active from August 2, 2026 regardless of the Omnibus-driven delay to high-risk deadlines (now Dec 2, 2027 for Annex III; Aug 2, 2028 for Annex I).
- Most enterprises — especially outside big tech — lack a real-time inventory of the AI systems (internal, embedded, and vendor-supplied) they actually run.
- Compliance today is largely manual: spreadsheets, one-off consulting engagements, and static gap-analysis reports that go stale the moment a new model is deployed or a vendor updates theirs.
- Multi-jurisdictional overlap (EU AI Act + GDPR + sector-specific rules + non-EU regimes like Egypt's PDPL) multiplies the documentation burden rather than simplifying it.
- The compliance deadline moving does not remove the underlying work — it changes the runway, not the requirement.

## 3. Business Objectives

1. Give enterprise customers continuous, evidence-based visibility into their AI risk posture instead of point-in-time snapshots. *(Status: the point-in-time snapshot half of this exists today — the self-assessment tool. The continuous half does not.)*
2. Reduce the cost and lead time of AI Act (and adjacent) compliance relative to pure consulting engagements.
3. Establish a recurring-revenue SaaS product line for Fixed Solutions that complements existing advisory/consulting work rather than competing with it. *(Updated: the feedback memo recommends this start as an internal accelerator for existing advisory/DPO clients rather than a standalone SaaS launch — see §9.)*
4. Position "Trust Layer" as a regional entry point for MENA organizations with EU market exposure, ahead of anticipated local AI governance rules.
5. Create a defensible data asset (regulatory rule-mapping engine) that can extend to future frameworks with incremental effort. *(Status: done — this is exactly what the self-assessment tool's pack/crosswalk architecture already is, and it's proven itself across nine frameworks, not just one.)*

## 4. Target Users & Personas

*(Unchanged from v0.1.)*

| Persona | Role | Core Need |
|---|---|---|
| Chief Compliance Officer / DPO | Owns regulatory risk | Defensible, exportable evidence of compliance status at any time |
| AI/ML Platform Lead | Owns model deployment | Fast way to register new models without slowing releases |
| Risk & Audit Manager | Prepares for external audits | Continuously current documentation, not a fire drill before assessment |
| Procurement / Vendor Risk | Evaluates third-party AI tools | Standardized risk-tiering for vendor-supplied AI before contract signature |
| External Auditor / Conformity Assessment Body | Validates high-risk systems | Structured, consistent evidence package per system |

## 5. Solution Overview — with build status

Trust Layer is organized around three core modules, plus a shared rules/reporting layer. **Status as of this revision:**

1. **Discovery & Inventory** — ❌ **Not built.** Continuously scans cloud environments, code repositories, SaaS integrations, and procurement records to detect deployed AI/ML models and flag unregistered ("shadow") AI. An open-source vendor evaluation (see §9 and Part 2 §2) found this splits into a well-served layer (code-repo/AI-BOM scanning) and an unserved layer (endpoint/network/SaaS shadow-AI detection, which has no viable open-source option).
2. **Risk Classification Engine** — ❌ **Not built.** Configurable rules engine (initially EU AI Act tiers: prohibited / high-risk / limited-risk / minimal-risk), human-in-the-loop review for edge cases.
3. **Audit-Ready Documentation Engine** — 🟡 **Partially built.** The self-assessment tool's Word gap-assessment report is a first, manually-triggered version of this. What's missing: continuous/automatic regeneration as underlying systems change, data-lineage and model-drift logs, and per-system (rather than per-organization) documentation.
4. **Regulatory Rules Layer (shared)** — ✅ **Built, and already broader than v0.1 scoped it.** v0.1 scoped this to "EU AI Act rule set (post-Omnibus timeline) as the primary framework," with GDPR overlap and everything else deferred to "phase 2+." What's actually been built covers **nine frameworks**: EU AI Act, GDPR, Egypt PDPL, KSA PDPL, UAE PDPL, ISO 27701, ISO 42001, HIPAA, and NIST Privacy Framework 1.0 — via the same pack/crosswalk architecture, with per-pack changelogs and version-mismatch detection (added in the self-assessment tool's v2.2). This is a materially better starting position than v0.1 assumed, and §8 (Scope) below updates accordingly.

## 6. High-Level Functional Requirements

### 6.1 Discovery & Inventory — not built; see Part 2 §2 for the evaluated design options
- Detect AI/ML models and AI-enabled SaaS tools across connected cloud, code, and procurement sources.
- Maintain a living inventory record per system (owner, purpose, data sources, deployment status).
- Flag systems with no assigned owner or risk classification ("shadow AI").

### 6.2 Risk Classification — not built
- Score each inventoried system against configurable regulatory tiers.
- Support manual override with justification logging (for auditability).
- Re-score automatically when a system's inputs, purpose, or deployment context changes materially.

### 6.3 Documentation & Reporting — partially built (self-assessment tool's Word report)
- Maintain continuous logs of data lineage, model drift, and human-oversight decisions. *(Not built — the current report is a point-in-time snapshot, not a continuous log.)*
- Generate on-demand compliance reports mapped to specific articles/annexes of the applicable framework. *(Built — this is what the Word report already does, via the pack citations.)*
- Support export formats suitable for submission to regulators or conformity assessment bodies. *(Partially — Word export exists; other formats not evaluated.)*
- Maintain full version history/audit trail of all classification and documentation changes. *(Not built — no classification exists yet to version.)*

### 6.4 Transparency & Content Labeling (Article 50 support) — not built
- Track which systems fall under synthetic-media/labeling obligations.
- Provide status dashboard for watermarking/labeling coverage across generative AI deployments (integration with, not replacement of, dedicated watermarking infrastructure).

### 6.5 Multi-Jurisdiction Support — ✅ built, exceeds original scope
- Rule sets configurable per jurisdiction; support simultaneous mapping to more than one framework for the same inventoried system. This is precisely what the self-assessment tool's crosswalk mechanism already does across all nine of its packs, not just EU AI Act + Egypt PDPL as v0.1 anticipated.

### 6.6 Access, Roles & Workflow — not built
- Role-based access (compliance officer, platform lead, auditor/read-only, vendor-risk reviewer).
- Workflow/approval routing for new-system registration and risk-tier overrides.

## 7. Non-Functional Requirements

*(Largely unchanged from v0.1; one addition.)*

- **Data residency & sovereignty:** configurable regional data hosting to satisfy both EU and MENA data-residency expectations.
- **Security:** role-based access control, encryption at rest/in transit, audit logging of all user actions.
- **Scalability:** support enterprise customers with large, heterogeneous AI estates without performance degradation.
- **Extensibility:** new regulatory frameworks addable via configuration of the rules layer rather than core re-engineering. *(Proven, not just planned — see §5 item 4.)*
- **Auditability:** every classification decision and document must be traceable to its source data and timestamped.
- **Integration:** APIs/connectors for common cloud platforms, model registries, and procurement/vendor-management systems.
- **New — third-party/open-source dependency transparency:** if Discovery & Inventory is built partly on open-source components (Part 2 §2), the platform must be transparent to clients about which findings come from which underlying tool and what that tool's coverage limits are — clients relying on discovery output for compliance decisions need to know what wasn't scanned, not just what was.

## 8. Scope — updated

**In scope (initial release), updated:**
- ✅ Already delivered: Regulatory Rules Layer covering EU AI Act, GDPR, Egypt/KSA/UAE PDPL, ISO 27701/42001, HIPAA, NIST Privacy Framework 1.0, plus manual Word-report documentation.
- Discovery, classification, and documentation modules for internally deployed and vendor-supplied AI — still the stated goal, still not built.
- Core reporting/export functionality — partially delivered via the existing Word report.

**Out of scope (initial release, candidate for later phases), updated:**
- Native watermarking/content-authentication infrastructure (integration only, not built in-house).
- Full conformity-assessment-body workflow.
- **Endpoint/network/SaaS-level shadow-AI discovery** — added to this list based on the vendor evaluation's finding that no credible open-source option exists here; this is now explicitly a partner-or-don't-build decision, not a deferred build decision.
- Frameworks beyond the nine already covered — this line from v0.1 ("frameworks beyond EU AI Act/GDPR overlap... planned as phase 2+") is now obsolete; the actual frameworks question is whether to go *further* (US/other non-MENA jurisdictions), not whether to reach GDPR-adjacency at all.

## 9. Assumptions & Constraints — updated with answers

v0.1 listed these as open assumptions. This revision states what's actually been found:

- **Go-to-market channel:** the Business Requirements Feedback memo recommends using Fixed Solutions' existing consulting/DPO-as-a-Service relationships as the primary channel, not a cold enterprise sales motion — treat this as the working assumption rather than an open question.
- **Commercial model:** the same memo recommends a hybrid model — internal accelerator for existing advisory/DPO clients first, standalone SaaS later, informed by pilot evidence. Also now the working assumption.
- **Build-vs-partner for discovery:** no longer purely unresolved. The evaluation found: (a) code-repo/AI-BOM scanning is well-served by open source (`cdxgen`, Cisco's `aibom`) and can plausibly be built on now; (b) endpoint/network/SaaS shadow-AI discovery has no viable open-source path and is a genuine partner-or-don't-build decision; (c) cloud-provider-side AI-resource inventory (SageMaker/Vertex/Azure OpenAI endpoints already provisioned) was not evaluated and remains genuinely open.
- **Regulatory content maintenance:** still assumed to require ongoing legal/regulatory monitoring — and now has an actual mechanism (the self-assessment tool's v2.2 changelog/version-tracking discipline) rather than being purely aspirational, though it still lacks an assigned organizational owner/budget.

## 10. Success Metrics (Illustrative — still to be finalized with stakeholders)

*(Unchanged from v0.1.)*

- Time-to-inventory: time for a new customer to reach a complete AI asset inventory.
- Reduction in manual hours spent on compliance documentation vs. prior consulting-only approach.
- Number of jurisdictions/rule sets supported. *(Baseline is now nine, not zero — future metrics should track growth from that baseline.)*
- Customer retention / expansion revenue from add-on jurisdiction modules.

## 11. Key Risks — updated

| Risk | Impact |
|---|---|
| Regulatory rule sets change faster than the platform's rules layer can be updated | Classification/reporting becomes inaccurate or stale. *(Partially mitigated: the v2.2 changelog/pack-version-mismatch mechanism now exists, but still has no assigned owner — see §9.)* |
| Discovery module produces false negatives on well-hidden shadow AI | Undermines core value proposition. *(Sharper now: this risk is concentrated specifically in the endpoint/SaaS layer the evaluation found has no open-source option — the code-repo layer is comparatively low-risk.)* |
| Competing directly with established RegTech vendors already in-market | Longer sales cycles, pricing pressure. |
| Customers treat the tool as a substitute for legal advice | Liability exposure if classification is relied on without professional review. *(Partially mitigated: the self-assessment tool already carries this disclaimer; extend the same language to any new module.)* |
| **New — open-source dependency risk** | If Discovery is built on `cdxgen`/Cisco's `aibom`, both are actively maintained but neither is Fixed-Solutions-controlled; a project slowdown or breaking change becomes Fixed Solutions' operational risk, not just a vendor's. |
| **New — source-available license confusion** | `VerifyWise` and similar tools market themselves as "open source" while actually being BSL-licensed (source-available). If evaluated further, treat this as a licensing/legal question before any integration decision, not a technical one. |

## 12. Open Questions for Stakeholder Input — updated

Original four questions, with current status:

1. ~~Is this a standalone commercial SaaS product, an internal tool to support advisory engagements, or both?~~ **Answered (working assumption):** hybrid, advisory-led first, per the feedback memo — confirm with stakeholders rather than treating as settled.
2. ~~Primary go-to-market?~~ **Answered (working assumption):** consulting channel through existing clients, per the feedback memo.
3. ~~Build vs. buy/partner for discovery/scanning?~~ **Partially answered:** partner/open-source-hybrid, split by layer (see §9) — still needs a decision on *which* partner for the endpoint/SaaS layer, since none was found to be open source.
4. Priority order for additional jurisdictions after the EU AI Act? **Still open**, though less urgent than v0.1 implied — the platform already covers Egypt PDPL, KSA PDPL, and UAE PDPL, so the practical version of this question is now "which non-MENA jurisdiction, if any" rather than "which MENA jurisdiction first."

**New open questions from this revision:**

5. Should the Discovery module's code-repo/AI-BOM layer be piloted now (open source is ready), independent of resolving the harder endpoint/SaaS layer — or held until both layers have a plan, so the module isn't shipped half-finished?
6. Does the Risk Classification Engine get built before or after Discovery has real data to classify? Building classification logic against no live inventory risks over-designing for cases that don't match what Discovery actually finds.
7. Who owns the regulatory content maintenance cadence documented in the Regulatory Rules Layer (§9/§11)? This is a staffing decision, not a technical one, and nothing in either BRD resolves it.

---

# PART 2: System Design Document (SDD)

*New in this revision — v0.1 had no SDD. Design choices below default to reusing the self-assessment tool's proven architecture wherever a Trust Layer module's needs overlap with it, rather than designing a parallel system.*

## 1. Regulatory Rules Layer — architecture (already built; documented here for completeness)

This module doesn't need new design work — it already exists as the self-assessment tool's pack/crosswalk engine. Documenting its shape here so Discovery, Classification, and Documentation can be designed to plug into it rather than duplicate it:

- **Pack schema:** each regulatory framework is an object with `id`, `shortLabel`, `name`, `version`, `lawline` (or `isStandard:true` for voluntary standards), `changelog` (array of `{date, change, why, source}`), and `categories` (the framework's own control/question structure).
- **Crosswalk mechanism:** categories across packs that represent equivalent obligations (e.g., breach notification, consent, DPIA) are merged into shared crosswalk groups, so an assessment against multiple frameworks doesn't ask the same underlying question repeatedly.
- **Version governance:** each pack's `changelog` and `version` move together (per v2.2's discipline); saved assessments snapshot which pack version they were scored against, and the tool flags mismatches on reload.
- **Reuse for Trust Layer:** the Risk Classification Engine (Part 2 §3) should score inventoried *systems* against this same pack structure's EU AI Act categories, rather than defining a separate rules format — one rules layer, two consumers (self-assessment questionnaires and live system classification).

## 2. Discovery & Inventory Engine — design, by layer

Per the vendor evaluation's findings, this module has three layers with three different levels of design maturity:

### 2.1 Code-repo / AI-BOM layer — ready to design in detail
- **Scanning engine candidates:** `cdxgen` (AppThreat/CycloneDX ecosystem) for breadth, or Cisco's `cisco-ai-defense/aibom` for depth (org/group-level scanning, LLM-based classification, built-in EU AI Act/NIST AI RMF/OWASP policy mappings).
- **Output format:** CycloneDX AI-BOM — a standard, machine-readable inventory of AI services, model metadata, and MCP configs found in a scanned codebase.
- **Integration point:** either a CI/CD pipeline hook (scan on each merge/deploy) or a scheduled batch scan against connected repos — CI/CD integration surfaces shadow AI earlier but requires deeper access into client pipelines; batch scanning is lower-friction to pilot.
- **Recommendation:** pilot this layer first (per BRD §12 Q5) — it's the one layer where open source genuinely closes the gap, and a working pilot here de-risks the rest of the module.

### 2.2 Endpoint / network / SaaS shadow-AI layer — no design yet, by necessity
- No open-source tool does this credibly (BRD §9). Commercial options found in the evaluation include Bifrost Edge, Nudge Security, Harmonic Security, dope.security, Reco, Netskope, Varonis, and others — this needs a partner-selection process, not a build design.
- **Interim design, until a partner is selected:** a manual self-declared inventory intake, structurally identical to the self-assessment tool's existing `aiSystemName` client-info field (v2.3) — not real discovery, but a stopgap that at least gives the Risk Classification Engine something to score while the endpoint-discovery partner question is resolved.

### 2.3 Cloud-provider-side inventory layer — not yet evaluated
- Detecting AI resources already provisioned in a client's own cloud accounts (SageMaker, Vertex AI, Azure OpenAI endpoints) is a distinct sub-problem from both layers above and needs its own vendor evaluation before any design work here.

## 3. Risk Classification Engine — design

- **Scoring basis:** reuse the Regulatory Rules Layer's EU AI Act pack categories (Part 2 §1) as the tier-assignment logic — prohibited / high-risk / limited-risk / minimal-risk — rather than building a second classification taxonomy.
- **Human-in-the-loop:** every automated tier assignment is overridable by a compliance officer, with mandatory justification text logged against the override (for the audit trail requirement in BRD §7).
- **Re-scoring triggers:** a system's tier is recalculated when its Discovery-layer metadata changes materially (new data sources, new deployment context, new purpose) — this requires Discovery (§2) to emit change events, which is a dependency the module's build order should respect (BRD §12 Q6: build Discovery before Classification, not the reverse).

## 4. Audit-Ready Documentation Engine — design

- **Starting point:** extend the self-assessment tool's existing Word-report generation rather than building a new documentation pipeline from scratch — it already produces framework-cited, exportable reports; what's missing is making it per-system (once Discovery/Classification exist) and continuous (regenerated on a schedule or on classification change) rather than a one-time manual export.
- **Version history / audit trail:** every classification decision and document regeneration needs a timestamped, immutable log entry — this is a new data requirement (§5 below), since the self-assessment tool's current save/load JSON mechanism captures a point-in-time snapshot, not a change history.
- **Export formats:** Word is proven; PDF and structured formats suitable for regulator/conformity-assessment-body submission are unevaluated and should be scoped once there's a real Documentation Engine to export from.

## 5. Data model — sketch

A minimal AI System Inventory schema, extending the single free-text field the self-assessment tool already has (v2.3's `aiSystemName`) into an actual registry once Discovery produces real entries:

```
AI_System_Registry
- system_id (PK)
- name
- owner
- purpose
- data_sources (linked to Discovery-layer findings, e.g. AI-BOM references)
- deployment_status
- risk_tier (from Risk Classification Engine)
- classification_justification (free text, required on any manual override)
- last_scored_at (timestamp — drives re-scoring triggers)
- last_documented_at (timestamp — drives Documentation Engine regeneration)

AI_BOM_Reference
- bom_id (PK)
- system_id (FK -> AI_System_Registry)
- source_layer ('code-repo' | 'endpoint-declared' | 'cloud-provider')
- bom_format ('CycloneDX-AIBOM')
- generated_at
- generating_tool ('cdxgen' | 'cisco-aibom' | 'manual-declaration' | ...)
```

This is intentionally sketch-level, not a full DDL — it exists to make the dependency between Discovery, Classification, and Documentation concrete, matching the level of detail the companion Data Governance Platform SDD gives its own ROPA schema.

## 6. Access, Roles & Workflow

- **RBAC roles:** compliance officer, platform lead, auditor (read-only), vendor-risk reviewer — same four roles as the persona table in BRD §4, since the personas and the roles are the same people.
- **Workflow:** new-system registration and risk-tier override both require an approval step, logged the same way DPIA reviewer adjudication is logged in the companion Data Governance Platform document (Sufficient/Insufficient-style states) — reusing that pattern rather than inventing a parallel one, since both documents describe the same kind of human-review gate.

## 7. Multi-Jurisdiction Support

No new design needed — this is Part 2 §1's Regulatory Rules Layer, already proven across nine frameworks. The only Trust-Layer-specific requirement is making sure the Risk Classification Engine (Part 2 §3) can score a single system against more than one framework's categories simultaneously (e.g., EU AI Act + Egypt PDPL for the same system), which the crosswalk mechanism already supports at the assessment level and needs to be confirmed at the per-system-classification level once Classification is actually built.

## 8. Integration Points with companion platforms

- **With the Data Governance Platform** ([[global-data-privacy-program-brd]]): its Data Discovery & Classification Engine (general PII discovery) and this document's Discovery & Inventory module (AI-asset discovery) target adjacent-but-different things. `cdxgen` generating both AI-BOM and CBOM from one scan (see below) suggests a shared scanning-engine evaluation is worth doing jointly rather than separately — but only after each platform's own prerequisite decisions (partner selection, pilot results) land, per the existing enhancement roadmap's caution against building shared infrastructure ahead of confirmed direction.
- **With the Quantum-Safe CBOM Discovery Platform:** both `cdxgen` and CBOMkit were evaluated for that platform's cryptography-discovery needs and share the same CycloneDX foundation as this platform's AI-BOM approach — the same "one discovery engine, multiple BOM outputs" pattern applies here too.

---

## Summary of what changed in this revision

| Area | v0.1 | v0.2 (this document) |
|---|---|---|
| Structure | BRD only | BRD + SDD |
| Module status | Not tracked | Explicitly tracked per module (§5) |
| Regulatory Rules Layer scope | "EU AI Act + GDPR, others phase 2+" | Nine frameworks, already delivered |
| Commercial model / GTM | Open questions | Working assumptions, sourced from the feedback memo |
| Build-vs-partner for discovery | Open question | Answered by layer, with a named gap (endpoint/SaaS) |
| Technical design | None | Part 2, reusing the self-assessment tool's proven architecture throughout |
