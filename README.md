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
| Retrieval | Dense cosine search, top-k=5, min-score 0.2 | `rag_api.py::retrieve()` |
| Generation | Grounded prompt via OpenRouter (default) or OpenAI | `rag_api.py::generate()` |
| Cache | Demo semantic cache, cosine >= 0.92 reuses answer | `rag_api.py::_similarity()` |
| Evaluation | Golden-set check: source-found + context precision | `rag_api.py::evaluate()` |

## Key Files

- `Lab/etl_pipeline.py` (~195 lines) — env `DB_URL`, `CHROMA_DIR`, `SOURCE_DOCS`. Run: `python -u etl_pipeline.py`.
- `Lab/rag_api.py` (~137 lines) — `POST /query {"question"}` → `{"answer","cached","sources"}`. Run: `uvicorn rag_api:app --reload`. Eval: `python rag_api.py evaluate`.
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

## Slides

`Slides/Module02_Consolidated_v1.0.{pptx,pdf}` — Module 02 deck. PPTX (~8.3 MB) editable source; PDF (~4.1 MB) snapshot.

## Notes

- Regenerated artefacts (`*.db`, `chroma_db/`, `.venv/`) are git-ignored — don't commit.
- Never commit `.env`. macOS: keep thread vars set, run Streamlit from `.venv`. Telemetry disabled in code for offline use.
