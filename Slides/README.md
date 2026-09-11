# Slides — Module 02: Data Engineering for AI

Bilingual (AR/EN) consolidated deck for Module 02. 89 slides: 7 lessons (V06–V12) + visual appendix + glossary.

## Files

| File | Size | Purpose |
|------|------|---------|
| `Module02_Consolidated_v1.0.pptx` | ~8.3 MB | Editable source of truth — edit this |

> Keep both in sync. Export PDF from PowerPoint/Keynote after editing the PPTX.

## Deck Map (89 slides)

Slides 1–2 — **Course intro**: title (Module 02: Data Engineering for AI), module map.

### V06 — Data Fundamentals (slides 3–12)

Unified Data/AI platform (3 slides: processing techniques), data spectrum & formats, ETL vs ELT paths, processing-pattern comparison (Medallion vs warehouse vs data mesh), Quick Quiz + Answers.

Key takeaway: ETL transforms before load, ELT loads first; Medallion = Bronze (raw immutable) → Silver (cleansed) → Gold (analytics-ready). Directly motivates the L03 lab architecture.

### V07 — Warehouses, Lakes & Lakehouse (slides 13–23)

Agenda, warehouse-vs-lake decision map (×2), Medallion layers (×2), data product & contract (schema / security / SLA), decision matrix (when to pick which model), three data patterns, Quiz + Answers.

Key takeaway: data contracts define schema, security, SLA expectations between producers and consumers.

### V08 — Feature Engineering & Stores (slides 24–31)

Agenda, raw-data-to-features flow, feature-store architecture (offline/online, training/serving consistency), agentic applications, LLM → agentic AI transition, Quiz + Answers.

Key takeaway: feature store is the source of truth behind agent decisions.

### V09 — Vector Databases + Applied RAG (slides 32–42)

Agenda, RAG pipeline, chunking strategies (recursive default), retrieval (dense + hybrid), grounded-answer pattern (cite [1],[2], say don't-know), evaluation + optimization, RAG triad (faithfulness / answer relevancy / context precision), pitfalls, Quiz + Answers.

Key takeaway: the theory behind every Lab component — chunk → embed → HNSW → retrieve → ground → evaluate.

### V10 — Labeling at Scale (slides 43–49)

Agenda, label quality loop, tooling, LLM-assisted labeling workflow, Quiz + Answers.

### V11 — Governance, Lineage & Catalog (slides 50–58)

Agenda, governance & cataloging, data lineage map, GenAI reference architecture (2-part + summary: portal / automation & compliance / shared services / governance & monitoring), Quiz + Answers.

### V12 — MLOps Fundamentals + Lab Intro (slides 59–69)

Agenda, MLOps lifecycle, concept distinctions (AI agent vs agentic AI, embedding vs generation cost), practical cost & performance, L03 lab architecture + run guide, Quiz + Answers. This lesson is the bridge into `../Lab`.

### Visual appendix (slides 70–79)

Diagram-only pages (no text) — supporting visuals referenced by earlier lessons.

### Glossary (slides 80–89)

Glossary title + map + 8 term pages (AR/EN) covering the module vocabulary.

## Conventions

- Every lesson ends with a Quick Quiz + Answers pair — use for in-class checks.
- All content slides are bilingual: Arabic headings with English parallels.
- Lessons most relevant to the Lab: V06 (Medallion), V09 (RAG), V12 (MLOps/cost/run guide).
