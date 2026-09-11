# AI Course

Hands-on AI course materials — slide decks + a live local RAG lab (ETL → Retrieval → Generation → Evaluation).
Fully local & lightweight: SQLite + ChromaDB + Streamlit + FastAPI. No Docker required.

> Bilingual (AR/EN) — Lab L03, Module 02 (Data Engineering for AI).

## Repository Structure

```text
AI Course/
├── README.md
├── .gitignore
├── Lab/                               ← L03 live RAG lab (Bronze → Silver → Gold)
│   ├── etl_pipeline.py                ← Bronze/Silver/Gold ETL
│   ├── rag_api.py                     ← FastAPI /query + retrieve/generate/evaluate
│   ├── streamlit_ui_enhanced.py       ← educational Streamlit UI (6 tabs)
│   ├── golden_dataset.json            ← 12 AR/EN Q&A benchmark items
│   ├── requirements.txt               ← pinned lightweight stack
│   ├── run_ui_enhanced.sh             ← venv setup + launch script
│   ├── .env                           ← secrets (git-ignored)
│   ├── l03_lab.db                     ← SQLite store (regenerated)
│   ├── chroma_db/                     ← ChromaDB HNSW index (regenerated)
│   └── data/raw/                      ← source documents indexed by ETL
└── Slides/
    ├── Module02_Consolidated_v1.0.pptx
    └── Module02_Consolidated_v1.0.pdf
```

## Lab — L03 RAG Pipeline

**Bronze → Silver → Gold → Retrieval → Generation → Evaluation**

| Stage | What happens | Code |
|-------|--------------|------|
| Bronze | Ingest txt/md/csv/pdf unmodified into SQLite `bronze_docs` | `etl_pipeline.py::bronze()` |
| Silver | Clean, dedupe (RapidFuzz), recursive chunk 500/50 | `etl_pipeline.py::silver()` |
| Gold | Embed `all-MiniLM-L6-v2` (384-dim) + HNSW in ChromaDB `gold_chunks` | `etl_pipeline.py::gold()` |
| Retrieval | Multi-variant dense cosine search (top-k=5, min-score 0.2): original + AR→EN glossary expansion + LLM translation, merged + keyword fallback (PDPL/DPIA/ROPA) | `rag_api.py::retrieve()` |
| Generation | Grounded prompt via OpenRouter (default) or OpenAI — answers in the question's language (AR→Arabic, EN→English) | `rag_api.py::generate()` |
| Cache | Demo semantic cache, cosine >= 0.92 reuses answer | `rag_api.py::_similarity()` |
| Evaluation | Golden-set check: source-found + context precision | `rag_api.py::evaluate()` |

## Key Files

- `Lab/etl_pipeline.py` (~200 lines) — env `DB_URL`, `CHROMA_DIR`, `SOURCE_DOCS`, `EMBEDDING_MODEL` (optional multilingual upgrade). Run: `python -u etl_pipeline.py`.
- `Lab/rag_api.py` (~294 lines, v1.1-bilingual) — `POST /query {"question"}` → `{"answer","cached","sources"}`. Bilingual: `detect_lang()` + `local_ar_to_en()` + `llm_translate()` + `retrieval_queries()`. Run: `uvicorn rag_api:app --reload`. Eval: `python rag_api.py evaluate`.
- `Lab/streamlit_ui_enhanced.py` (~876 lines) — 6 tabs: Educational Flow | Upload | Documents | Query | Evaluation | About. Must run inside `.venv`.
- `Lab/golden_dataset.json` — 12 bilingual items; some `expected_source=NOT_IN_CORPUS` (negative controls).
- `Lab/requirements.txt` — sqlalchemy 2.0.36, chromadb 0.5.20, fastapi 0.115.5, streamlit 1.40.1, plotly, sklearn. Python 3.10+.
- `Lab/run_ui_enhanced.sh` — creates `.venv`, installs deps, launches UI at `http://localhost:8501`.
- `Lab/data/raw/` — 8 docs: `etl_notes.txt`, `rag_basics.md`, 2 BRD/SDD markdown specs, 4 PDFs (AEGIS concept/presentation, Egypt PDPL, Quantum intro).

## Quickstart

```bash
cd Lab
./run_ui_enhanced.sh        # venv + deps + UI → http://localhost:8501

# manual:
python3 -m venv .venv && source .venv/bin/activate
pip install -q -r requirements.txt
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 TOKENIZERS_PARALLELISM=false
python -u etl_pipeline.py   # first run downloads ~80MB MiniLM model
uvicorn rag_api:app --reload
python rag_api.py evaluate
streamlit run streamlit_ui_enhanced.py
```

`.env` (git-ignored, required for generation): `OPENROUTER_API_KEY`, `GENERATOR=openrouter|openai`, `OPENROUTER_MODEL`, `DB_URL`. Rebuild index: `rm -rf chroma_db l03_lab.db`.

## Slides — Module 02: Data Engineering for AI

`Slides/Module02_Consolidated_v1.0.{pptx,pdf}` — 89 slides, bilingual AR/EN. PPTX (~8.3 MB) is the editable source; PDF (~4.1 MB) is the distributable snapshot. Keep both in sync.

### Section map (7 lessons V06–V12 + glossary)

| Slides | Lesson | Topics covered |
|--------|--------|----------------|
| 1–2 | Intro | Course title, module map |
| 3–12 | V06 Data Fundamentals | Unified Data/AI platform, data spectrum & formats, ETL vs ELT, processing patterns (Medallion vs warehouse vs mesh) + quiz |
| 13–23 | V07 Warehouses, Lakes & Lakehouse | Agenda, warehouse-vs-lake decision map, Medallion layers, data product & contract (schema/security/SLA), decision matrix, three data patterns + quiz |
| 24–31 | V08 Feature Engineering & Stores | Raw→features, feature-store architecture, agentic applications, LLM → agentic AI + quiz |
| 32–42 | V09 Vector DBs + Applied RAG | RAG pipeline, chunking strategies, retrieval, grounded-answer pattern, eval+optimization, RAG triad, pitfalls + quiz |
| 43–49 | V10 Labeling at Scale | Label quality loop, tooling, LLM-assisted labeling workflow + quiz |
| 50–58 | V11 Governance, Lineage & Catalog | Governance & cataloging, lineage map, GenAI reference architecture (2-part + summary) + quiz |
| 59–69 | V12 MLOps + Lab Intro | MLOps lifecycle, concept distinctions (agent vs agentic), cost/performance (embedding vs generation), L03 architecture + run guide + quiz |
| 70–79 | (visual appendix) | Diagram-only appendix pages |
| 80–89 | Glossary | Glossary map + 8 glossary term pages (AR/EN) |

Each lesson ends with a Quick Quiz + Answers pair. Most relevant to the Lab: V06 (Medallion = Bronze/Silver/Gold), V09 (chunking, retrieval, grounded generation, triad eval), V12 (cost, L03 run guide).


## Lab — App deep dive

### Streamlit UI (`streamlit_ui_enhanced.py`, 6 tabs)

| Tab | Purpose |
|-----|---------|
| 🎓 Educational Flow | Step-through of Bronze→Silver→Gold→Retrieval→Generation→Evaluation with visuals |
| 📤 Upload | Drop txt/md/csv/pdf → re-runs Bronze→Silver→Gold for the new file |
| 📄 Documents | Distinct docs indexed + chunk counts (from `gold_chunks` metadatas) |
| 💬 Query | Ask → dense retrieval + grounded answer with `[1],[2]` citations and scores |
| 📊 Evaluation | Golden-set run: `expected_source_found` ✅/❌ + precision + PCA/t-SNE embedding projection (plotly/sklearn) |
| ⚙️ About | Learning outcomes, stack, commands, file map |

Guard: refuses to run outside `.venv` (global env segfaults on macOS/ONNX). Launch: `./run_ui_enhanced.sh` → `http://localhost:8501`.

### API contract (`rag_api.py`)

`POST /query` body `{"question": "..."}` → `{"answer": str, "cached": bool, "sources": [{"text","source","score"}]}`. Empty hits → bilingual "not enough info" message. Cache compares against last Q only (demo-grade).

### Knowledge base (`Lab/data/raw/`, 8 files)

- `etl_notes.txt` (322 B) — Medallion layers + data contracts.
- `rag_basics.md` (575 B) — RAG definition, recursive-chunking defaults (300–800 chars, 10–20% overlap), triad/RAGAS.
- `-Global-Data-Privacy-Program-BRD-SDD-v1_3.md` (~67 KB) — enterprise privacy BRD/SDD v1.3 (consent/cookies, DPIA, ROPA vocab, metrics library; 9-framework baseline).
- `-Trust-Layer-AI-Governance-Platform-BRD-SDD-v0_2.md` (~27 KB) — Trust Layer AI-governance BRD/SDD (discovery, risk engine, doc engine, 9-framework rules layer).
- `AEGIS_AI_ConceptPaper.pdf` (45 pp) — AEGIS-AI counter-UAS concept & architecture (ITC-2026).
- `AEGIS_AI_Presentation.pdf` (29 pp) — AEGIS-AI slide deck (swarm-vs-swarm tracking).
- `Egypt-PDPL-self-assessment-v2_14.pdf` (47 pp) — PDPL/GDPR/AI-Act self-assessment readiness.
- `Introduction to Quantum mechanics.pdf` (31 pp) — off-topic distractor doc (tests retrieval precision).

## Notes

- Regenerated artefacts (`*.db`, `chroma_db/`, `.venv/`) are git-ignored — don't commit.
- Never commit `.env`. macOS: keep thread vars set, run Streamlit from `.venv`. Telemetry disabled in code for offline use.

