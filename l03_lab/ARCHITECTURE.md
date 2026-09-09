# L03 — معمارية التطبيق / Application Architecture
# L03 — ETL + Backend + Frontend

> ثنائي اللغة / Bilingual. المصدر الوحيد للحقيقة للتشغيل: `../L03_Environment_Setup_Guide.md` + `run_ui.sh`.

## 1. نظرة عامة / Overview

```
data/raw (TXT/MD/CSV/PDF)
        │  upload (UI) or drop files
        ▼
┌─────────────┐   ┌──────────────┐   ┌─────────────────────┐
│ ETL pipeline │──▶│   Backend    │──▶│      Frontend       │
│ etl_pipeline │   │  rag_api.py  │   │  streamlit_ui.py    │
│ Bronze→Silver│   │ FastAPI+eval │   │  5 tabs, bilingual  │
│ →Gold(Chroma)│   │ :8000 /query │   │  :8501              │
└──────┬───────┘   └──────┬───────┘   └─────────────────────┘
       │ SQLite           │ ChromaDB (gold_chunks, HNSW cosine)
       ▼ l03_lab.db       ▼ ./chroma_db (all-MiniLM-L6-v2, dim 384)
```

- **ETL (`etl_pipeline.py`)**: يقرأ `data/raw` ويبني `bronze_docs` ثم `silver_chunks` (SQLite) ثم `gold_chunks` (ChromaDB). دفعات 10 + سجلات `encode/inserting/done`. يُشغَّل CLI أو من تبويب الرفع.
- **Backend (`rag_api.py`)**: استرجاع كثيف `retrieve()` (top-k=5, حد 0.2) + توليد مؤرَّض `generate()` (OpenRouter `:free` افتراضيًا) + كاش دلالي (≥0.92 على آخر سؤال) + `evaluate()` على `golden_dataset.json` (12 سؤالًا). `POST /query` على `:8000`.
- **Frontend (`streamlit_ui.py`)**: رفع وفهرسة (يُعيد استخدام `rag.client` نفسه: `delete_collection` + إعادة إنشاء + ترميز بدفعات 10 مع شريط تقدم)، مستندات، استعلام، تقييم، حول. `:8501` عبر `./run_ui.sh`.

## 2. طبقات ETL بالتفصيل / ETL Layers

| Layer | Code | Store | ماذا يحدث / What happens |
|---|---|---|---|
| Bronze | `bronze(engine)` | SQLite `bronze_docs` (doc_id, name, content, ts, `if_exists="replace"`) | قراءة TXT/MD/CSV (utf-8) وPDF (pypdf) **دون تعديل**؛ يفشل برسالة واضحة إن كان `data/raw` فارغًا. |
| Silver | `silver()` + `recursive_chunk(500, 50)` | SQLite `silver_chunks` (chunk_id `{doc}::chunk-{i}`, doc_name, chunk_idx, text) | إزالة تكرار تام + تطبيع مسافات → تقسيم تكراري (فقرات ← جمل ← تقسيم صلب) → إزالة شبه-تكرار (RapidFuzz ≥95). |
| Gold | `gold(silver_df, batch_size=10)` | ChromaDB `./chroma_db`, collection **`gold_chunks`**, HNSW cosine, `all-MiniLM-L6-v2` (384) | إحماء `ef(["hello"])` يكشف فشل التنزيل مبكرًا؛ ترميز صريح `ef(batch)` ثم `add(..., embeddings=...)` بدفعات 10 مع `progress_cb`. الـ CLI يتخطى إن كانت المجموعة مملوءة (احذف `chroma_db` للبناء القسري). |

## 3. الـ Backend / Backend (`rag_api.py`)

- `retrieve(query, k)`: `col.query(n_results=min(k or 5, count))` → `score = 1 − dist` → عتبة `MIN_SCORE=0.2` → `[{text, source, score}]`. يقرأ `question_en` عند التقييم (النموذج إنجليزي الميول).
- `generate(question, hits)`: موجِّه مقيَّد بالمصادر `[1] text (source: …)` + تعليمات استشهاد `[1],[2]…` و«لا أعرف» عند غياب السياق. OpenRouter (`OPENROUTER_API_KEY`, موديل `:free`) أو OpenAI (`GENERATOR=openai`).
- `query()`: كاش دلالي على **آخر** سؤال فقط (`_similarity ≥ 0.92` → `cached:true`)؛ بلا نتائج → `لا توجد معلومات كافية / No relevant context found`.
- `evaluate()`: `python rag_api.py evaluate` → لكل سؤال: `context_precision ≈ mean(score)` + `expected_source_found` (مطابقة نهاية الاسم). أسئلة `NOT_IN_CORPUS` تفشل **عمدًا** لتوضيح السلوك المؤرَّض.
- الثوابت: `TOP_K=5, MIN_SCORE=0.2, CACHE_SIM=0.92`. ملف `.env` يُحمَّل تلقائيًا (`DB_URL/GOLDEN/GENERATOR/OPENROUTER_*`).

## 4. الـ Frontend / Frontend (`streamlit_ui.py`)

- حارس venv (`st.stop()` خارج `.venv`) + `st.cache_resource` للمجموعة.
- `ingest_file()`: Bronze→Silver ثم **عبر `rag.client` نفسه** (لا عميل ثانٍ → لا قفل SQLite): `delete_collection("gold_chunks")` + `get_or_create_collection(...)` + ترميز `rag.ef(batch of 10)` + `add(..., embeddings=...)` مع `st.progress` **وسجلات طرفية** `[Gold] encode/inserting/done`؛ ثم `rag.col = fresh` + مسح الكاش.
- التبويبات: 📤 رفع (TXT/MD/CSV/PDF → `data/raw` → فهرسة)، 📄 مستندات (عدّ + معاينة مقاطع)، 💬 استعلام (top-k 1..10 + مصادر + شارة كاش)، 📊 تقييم (جدول 12 سؤالًا + متوسط الدقة + hit-rate)، ⚙️ حول.
- التشغيل: `./run_ui.sh` (يضبط `OMP/MKL/TOKENIZERS` + يستخدم `.venv/bin/streamlit`).

## 5. المخازن والعقود / Stores & Contracts

- `l03_lab.db` (SQLite): `bronze_docs`, `silver_chunks` — يُعاد إنشاؤهما (`replace`) كل تشغيل.
- `./chroma_db` (ChromaDB 0.5.20, SQLite+HNSW): مجموعة واحدة `gold_chunks` + `metadatas {doc, idx}`.
- `golden_dataset.json`: `{id, question, question_en, reference_answer(_en), expected_source}` × 12.
- `.env` (لا يُرفَع): `OPENROUTER_API_KEY, GENERATOR, OPENROUTER_MODEL, DB_URL, CHROMA_DIR, GOLDEN`.

## 6. قرارات حرجة (دروس الجمود) / Critical Decisions (freeze lessons)

1. **عميل ChromaDB واحد فقط**: عميل ثانٍ على نفس المجلد = قفل SQLite وتجمّد بعد `[Silver]`. الواجهة تُعيد استخدام `rag.client`.
2. **حذف المجموعة وإعادة إنشائها** بدل `delete(ids)+add` على مقطع HNSW مستخدَم (يُعلَّق في 0.5.x).
3. **دفعات 10 + ترميز صريح** (`ef(batch)` خارج `add`) لتمييز تعطّل المرمّز عن تعطّل الإدخال، مع سجلات طرفية وشريط تقدم.
4. **macOS**: `OMP/MKL=1, TOKENIZERS_PARALLELISM=false` قبل استيراد onnx (وإلا جمود المرمّز).
5. **اسم مجموعة واحد** `gold_chunks` في الملفات الثلاثة (كان الخلاف يجعل الـ API يرى 0 متجهات).
6. **`python -u`** (unbuffered) لسجلات Gold الفورية + حارس venv ضد segfault.

## 7. التشغيل السريع / Quick Run

```bash
cd l03_lab
./run_ui.sh                                   # الواجهة :8501 (يبني .venv أول مرة)
# أو:
source .venv/bin/activate
OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 TOKENIZERS_PARALLELISM=false python -u etl_pipeline.py
uvicorn rag_api:app --reload                  # :8000/docs
python rag_api.py evaluate
curl -X POST localhost:8000/query -H "Content-Type: application/json" -d '{"question": "Which chunking strategy is recommended?"}'
```
