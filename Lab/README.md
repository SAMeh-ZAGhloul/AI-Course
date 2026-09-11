# Lab — L03 Live RAG Lab (ETL → Retrieval → Generation → Evaluation)

Fully local RAG lab. No Docker. Stack: SQLite (Bronze/Silver) + ChromaDB HNSW (Gold) + `all-MiniLM-L6-v2` embeddings + FastAPI + Streamlit. Bilingual AR/EN (v1.1: Arabic queries auto-expanded to English for retrieval, answers generated in the question's language).

## Contents

| Path | What it is |
|------|------------|
| `etl_pipeline.py` (~200 lines) | Bronze → Silver → Gold pipeline. Honors `EMBEDDING_MODEL` (optional multilingual upgrade). Run: `python -u etl_pipeline.py` |
| `rag_api.py` (~294 lines, v1.1-bilingual) | FastAPI `POST /query`; `retrieve()` (multi-variant bilingual + keyword fallback) / `generate()` (answer in question's language) / `evaluate()`. Run: `uvicorn rag_api:app --reload`; eval: `python rag_api.py evaluate` |
| `streamlit_ui_enhanced.py` (~876 lines) | Educational UI, 6 tabs. Run: `streamlit run streamlit_ui_enhanced.py` or `./run_ui_enhanced.sh` |
| `golden_dataset.json` | 12 bilingual Q&A benchmark items (faithfulness / answer relevancy / context precision) |
| `requirements.txt` | Pinned deps (Python 3.10+): sqlalchemy 2.0.36, chromadb 0.5.20, fastapi 0.115.5, uvicorn 0.32.0, pandas 2.2.3, pypdf 5.1.0, rapidfuzz 3.10.1, streamlit 1.40.1, plotly, sklearn |
| `run_ui_enhanced.sh` | Creates `.venv`, installs deps, sets macOS thread vars, launches UI at `http://localhost:8501` |
| `data/raw/` (8 files) | Indexed corpus (see Knowledge base below) |
| `.env` | Secrets — git-ignored, never commit |
| `l03_lab.db` | SQLite Bronze/Silver store — regenerated, git-ignored |
| `chroma_db/` | ChromaDB persistent HNSW index — regenerated, git-ignored |


## Pipeline

**Bronze → Silver → Gold → Retrieval → Generation → Evaluation**

| Stage | What happens | Code |
|-------|--------------|------|
| Bronze | Ingest `txt/md/csv/pdf` unmodified into SQLite table `bronze_docs` (uuid doc_id, name, content, timestamp). PDF text via `pypdf`. Empty folder → bilingual exit message. | `etl_pipeline.py::bronze()` |
| Silver | Clean, dedupe with RapidFuzz, recursive chunk: paragraphs → sentences → hard split (default chunk 500 chars, overlap 50) into `silver_chunks` (chunk_id, doc_name, chunk_idx, text). | `etl_pipeline.py::silver()`, `recursive_chunk()` |
| Gold | Embed explicitly in batches of 10 with `all-MiniLM-L6-v2` (384-dim, ~80 MB download on first run), insert into ChromaDB collection `gold_chunks` (cosine space) persisted to `./chroma_db`. Skips insert if already populated. `progress_cb(done,total)` hook for the UI. Optional: set `EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L12-v2`, delete `./chroma_db`, re-run ETL for native Arabic semantic search. | `etl_pipeline.py::gold()` |
| Retrieval | Multi-variant dense HNSW cosine search, `top_k=5`, `min_score=0.2` (score = 1 − distance): tries original query + offline AR→EN glossary expansion + LLM translation (when API key set), merges/dedupes by score, then offline keyword fallback for abbreviations (PDPL/DPIA/ROPA/GDPR). Example: `ما هو قانون حماية البيانات الشخصية؟` → `Personal Data Protection Law PDPL …` hits `Egypt-PDPL-self-assessment-v2_14.pdf`. | `rag_api.py::retrieve()`, `retrieval_queries()`, `local_ar_to_en()`, `llm_translate()`, `detect_lang()` |
| Generation | Grounded prompt: answer ONLY from context, cite `[1],[2]…`, say don't-know if absent — **in the question's language** (Arabic questions → Modern Standard Arabic answers; English → English). OpenRouter default (`nvidia/nemotron-3-super-120b-a12b:free`, needs `OPENROUTER_API_KEY`) or OpenAI (`GENERATOR=openai`). | `rag_api.py::generate()` |
| Cache | Demo semantic cache: cosine ≥ 0.92 vs last question reuses its answer (`cached: true`). In-memory list. | `rag_api.py::_similarity()` |
| Evaluation | Golden-set spot check per item: `expected_source_found` (expected filename in top-k) + `context_precision≈avg(score)`. | `rag_api.py::evaluate()` |

Env vars: `DB_URL` (default `sqlite:///./l03_lab.db`), `CHROMA_DIR` (`./chroma_db`), `SOURCE_DOCS` (`./data/raw`), `GENERATOR`, `OPENROUTER_MODEL`, `OPENROUTER_API_KEY`, `GOLDEN`, `EMBEDDING_MODEL` (empty = `all-MiniLM-L6-v2` default; set to `paraphrase-multilingual-MiniLM-L12-v2` + rebuild index for native multilingual embeddings). `.env` is auto-loaded by `rag_api.py`.

## Streamlit App (6 tabs)

| Tab | Purpose |
|-----|---------|
| 🎓 Educational Flow | Step-through of each pipeline stage with visuals |
| 📤 Upload | Drop txt/md/csv/pdf → re-runs Bronze→Silver→Gold |
| 📄 Documents | Distinct indexed docs + chunk counts (from collection metadatas) |
| 💬 Query | Ask in EN or AR → multi-variant retrieval + grounded answer in your language with citations and scores |
| 📊 Evaluation | Golden-set run (✅/❌ per item, precision) + PCA/t-SNE embedding projection (plotly + sklearn) |
| ⚙️ About | Learning outcomes, stack, commands, file map |

Guard: refuses to run outside `.venv` (global Python segfaults on macOS/ONNX). Telemetry disabled (`posthog.capture` no-op, `anonymized_telemetry=False`); macOS deadlock fix (`OMP_NUM_THREADS=1`, `TOKENIZERS_PARALLELISM=false`) set in code and in `run_ui_enhanced.sh`; `pypdf` recovery-notice spam silenced.

## API Contract

`POST /query` with `{"question": "..."}` returns `{"answer": str, "cached": bool, "sources": [{"text","source","score"}]}`. No hits → bilingual "not enough info" message with empty sources.

## Knowledge Base (`data/raw/`, 8 files)

- `etl_notes.txt` (322 B) — Medallion layers + data contracts. Covered by golden items 2–3.
- `rag_basics.md` (575 B) — RAG definition, recursive-chunking defaults, triad/RAGAS. Covered by golden items 4, 7.
- `-Global-Data-Privacy-Program-BRD-SDD-v1_3.md` (~67 KB) — enterprise privacy BRD/SDD v1.3 (consent & cookies, DPIA Unsure path, ROPA vocab, metrics library; 9-framework baseline).
- `-Trust-Layer-AI-Governance-Platform-BRD-SDD-v0_2.md` (~27 KB) — Trust Layer AI-governance BRD/SDD v0.2 (discovery, risk engine, doc engine, 9-framework rules layer).
- `AEGIS_AI_ConceptPaper.pdf` (45 pp) — AEGIS-AI counter-UAS concept & architecture (ITC-2026).
- `AEGIS_AI_Presentation.pdf` (29 pp) — AEGIS-AI slide deck (swarm-vs-swarm tracking).
- `Egypt-PDPL-self-assessment-v2_14.pdf` (47 pp) — PDPL/GDPR/AI-Act self-assessment readiness.
- `Introduction to Quantum mechanics.pdf` (31 pp) — off-topic distractor (tests retrieval precision).

Golden set (`golden_dataset.json`, 12 items): items 2–4, 7 in-corpus (should hit ✅); items 1, 5–6, 8–12 are `NOT_IN_CORPUS` negative controls (correct = no-hit / don't-know).

## Quickstart

```bash
./run_ui_enhanced.sh        # venv + deps + UI → http://localhost:8501
python -u etl_pipeline.py   # rebuild index (first run downloads ~80 MB model)
uvicorn rag_api:app --reload
python rag_api.py evaluate
streamlit run streamlit_ui_enhanced.py
```

Rebuild from scratch: `rm -rf chroma_db l03_lab.db` then re-run ETL. Native multilingual embeddings: `EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L12-v2` on both ETL rebuild and API/UI runs. Never commit `.env`, `*.db`, `chroma_db/`, `.venv/` (all git-ignored).

## Bilingual AR/EN (v1.1)

The corpus is English (PDPL docs, BRD/SDD specs), but queries work in both languages:

- `what is PDPL?` → dense search hits `Egypt-PDPL-self-assessment-v2_14.pdf` + `Global-Data-Privacy-Program-BRD-SDD`, answer in English.
- `ما هو قانون حماية البيانات الشخصية؟` → `detect_lang()=ar` → `local_ar_to_en()` expands to `Personal Data Protection Law PDPL data privacy consent DPIA ROPA` (+ `llm_translate()` when an API key is set) → same PDPL sources retrieved → answer generated in Modern Standard Arabic with `[1],[2]` citations.

Helpers in `rag_api.py`: `detect_lang()`, `local_ar_to_en()`, `llm_translate()`, `retrieval_queries()` + abbreviation keyword fallback (PDPL/DPIA/ROPA/GDPR). No re-index required for the default path.
