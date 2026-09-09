# AI Course — Module 02 (Data Engineering for AI) + L03 Live Lab

# مقرر الذكاء الاصطناعي — الوحدة الثانية (هندسة البيانات للذكاء الاصطناعي) + مختبر L03 المباشر

Bilingual (AR/EN) teaching kit: updated slide decks, quizzes, glossary, mini-labs, environment guide, and a hands-on Mini-ETL → RAG lab (SQLite + ChromaDB + FastAPI + Streamlit, no Docker).

حقيبة تدريسية ثنائية اللغة (عربي/إنجليزي): عروض محدثة، اختبارات، المصطلحات، تمارين مصغرة، دليل تجهيز البيئة، ومختبر عملي ETL مصغر ينتهي بنقطة RAG (بدون Docker).

---

## 📦 What's inside / المحتويات

```
.
├── README.md                              # this file / هذا الملف
├── L03_Environment_Setup_Guide.md         # local setup: venv + SQLite + ChromaDB + LLM keys (AR/EN)
├── Glossary_AR_EN.md                      # Module 02 glossary, 44 terms (AR/EN)
├── Module02_Quizzes_AR_EN.md              # short quizzes V06–V12 with answers (AR/EN)
├── Module02_Mini_Labs_AR_EN.md            # ~15-min hands-on exercise per module (AR/EN)
├── Module02_Updated_Content_Proposal.md   # what changed per deck + sources (AR/EN)
├── Module02_V06..V12.pptx                 # original decks (source)
├── output/                                # generated decks (ready to present)
│   ├── Module02_V06_Updated.pptx … V12_Updated.pptx
│   ├── Module02_Glossary_Quizzes.pptx
│   └── Module02_Visualizations.pptx
├── *.py                                   # deck-generation scripts (deck_data.py, generate_decks.py, …)
├── l03_lab/                                    # live lab: mini ETL → RAG endpoint
│   ├── README.md                             # lab run guide (AR/EN) — updated
│   ├── ARCHITECTURE.md                       # ETL + backend + frontend design (AR/EN)
│   ├── ENHANCED_UI_README.md                 # 🎓 NEW: enhanced educational UI guide
│   ├── IMPLEMENTATION_SUMMARY.md             # 🎓 NEW: detailed implementation report
│   ├── QUICK_REFERENCE.md                    # 🎓 NEW: quick start guide
│   ├── requirements.txt                      # lightweight local stack — updated
│   ├── etl_pipeline.py                       # Bronze → Silver → Gold
│   ├── rag_api.py                            # FastAPI /query + evaluate
│   ├── streamlit_ui.py                       # original UI (5 tabs, minimal)
│   ├── streamlit_ui_enhanced.py              # 🎓 NEW: enhanced educational UI (6 tabs + visualizations)
│   ├── run_ui.sh                             # launcher for original UI
│   ├── run_ui_enhanced.sh                    # 🎓 NEW: launcher for enhanced UI
│   ├── golden_dataset.json                   # 12 bilingual Q&A benchmark
│   └── data/raw/                             # sample docs (rag_basics.md, etl_notes.txt, PDFs)
```

## 🗂️ Module 02 decks / عروض الوحدة الثانية

| Deck | Topic / الموضوع                                                  | Updated file / الملف المحدث |
| ---- | ----------------------------------------------------------------------- | -------------------------------------- |
| V06  | Data Fundamentals / أساسيات البيانات                     | `output/Module02_V06_Updated.pptx`   |
| V07  | Warehouses, Lakes & Lakehouse / المستودعات والبحيرات | `output/Module02_V07_Updated.pptx`   |
| V08  | Feature Engineering & Stores / هندسة الخصائص                | `output/Module02_V08_Updated.pptx`   |
| V09  | Vector DBs + Applied RAG / القواعد المتجهية + RAG        | `output/Module02_V09_Updated.pptx`   |
| V10  | Labeling at Scale / التصنيف على نطاق واسع             | `output/Module02_V10_Updated.pptx`   |
| V11  | Governance, Lineage & Catalog / الحوكمة                          | `output/Module02_V11_Updated.pptx`   |
| V12  | MLOps + Lab Introduction / أساسيات MLOps                         | `output/Module02_V12_Updated.pptx`   |

Key updates (details in `Module02_Updated_Content_Proposal.md`): Medallion vs Warehouse vs Data Mesh comparison, Data Product/Contract, 5 chunking strategies (Recursive = default), hybrid retrieval + reranking, grounded prompting, RAG evaluation triad (faithfulness / answer relevancy / context precision), semantic caching & model routing, LLM-assisted labeling + human-in-the-loop, AI Gateway/guardrails, MLflow/DVC.

## 🧪 Quizzes, glossary, mini-labs / الاختبارات والمصطلحات والتمارين

- **Quizzes:** `Module02_Quizzes_AR_EN.md` + deck `output/Module02_Glossary_Quizzes.pptx` — Q&A per module (V06–V12) with answers.
- **Glossary:** `Glossary_AR_EN.md` — 44 terms AR↔EN (ETL/ELT, Medallion, HNSW, chunking, RAG triad, guardrails, …).
- **Mini-labs:** `Module02_Mini_Labs_AR_EN.md` — one ~15-min exercise after each module (CSV cleaning, Bronze/Silver/Gold, feature consistency, ChromaDB + rerank, LLM labeling agreement, lineage map, MLflow run, retriever tuning in L03).

## 🔬 L03 live lab / المختبر المباشر

Local-only, no Docker: Python venv + built-in SQLite (Bronze/Silver) + ChromaDB Gold index (`gold_chunks`, HNSW cosine, `all-MiniLM-L6-v2` 384-d, batches of 10) + FastAPI `:8000` + Streamlit `:8501`.

**Quick start:**

```bash
cd l03_lab
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# ETL: Bronze → Silver → Gold
OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 TOKENIZERS_PARALLELISM=false python -u etl_pipeline.py

# API
uvicorn rag_api:app --reload        # http://localhost:8000/docs
curl -X POST localhost:8000/query -H "Content-Type: application/json" \
  -d '{"question": "Which chunking strategy is recommended?"}'

# Benchmark (12 bilingual Q&A)
python rag_api.py evaluate

# UI — Choose one:

# 🎓 Enhanced Educational UI (recommended for teaching/learning)
# Includes: visual ETL flow, embedding space visualization, RAG pipeline flowchart, learning resources
./run_ui_enhanced.sh                # http://localhost:8501 — 6 tabs with visualizations

# OR: Original Simple UI (lightweight)
./run_ui.sh                         # http://localhost:8501 — 5 tabs, minimal
```

**📚 UI Options:**
- **Enhanced** (`run_ui_enhanced.sh`): 🎓 Educational with 4 visualizations, learning outcomes, metrics
  - See: `l03_lab/ENHANCED_UI_README.md`, `l03_lab/QUICK_REFERENCE.md`
- **Original** (`run_ui.sh`): 💻 Simple interface, lightweight, same functionality

> Run everything **inside `.venv`** — a global Python (e.g. homebrew) segfaults at browser connect. Full guides: `L03_Environment_Setup_Guide.md`; design: `l03_lab/ARCHITECTURE.md`; lab manual: `l03_lab/README.md`; enhanced UI: `l03_lab/ENHANCED_UI_README.md`.

LLM generation defaults to OpenRouter free tier (`OPENROUTER_API_KEY`, model `nvidia/nemotron-3-super-120b-a12b:free`); `GENERATOR=openai` is supported. Key lives in `l03_lab/.env` (never committed — see `.gitignore`).

## 🛠️ Regenerate the decks / إعادة توليد العروض

```bash
pip install python-pptx pillow numpy
python generate_decks.py        # V06–V12 updated decks → output/ (agenda, tables, Q+A, footers)
python gen_glossary_quiz_deck.py  # glossary (6/slide) + Q/A split slides → output/
python integrate_visuals.py     # idempotent single-visual inserts + footer renumber
python generate_visuals.py      # standalone Module02_Visualizations.pptx (archive reference)
python check_deck_quality.py    # QA gate: duplicate titles + overflow warnings (expect PASS)
```

## 🙋 Source / المصدر

Course content proposal + reference frames: Daily Dose of Data Science (RAG chunking), McKinsey GenAI reference architecture, RAG evaluation triad. Original decks `Module02_V06..V12.pptx` are kept as sources; present from `output/`.
