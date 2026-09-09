# L03 — المختبر المباشر: خط أنابيب ETL مصغّر ينتهي بنقطة نهاية RAG
# L03 — Live Lab: Mini ETL Pipeline Ending in a RAG Endpoint

تثبيت محلي خفيف — **دون Docker**: Python venv + SQLite مدمجة (Bronze/Silver) + ChromaDB (Gold) + FastAPI.
Lightweight local install — **no Docker**: Python venv + built-in SQLite (Bronze/Silver) + ChromaDB (Gold) + FastAPI.

## البناء / Structure
```
l03_lab/
├── requirements.txt                 # المكوّنات الخفيفة / lightweight deps
├── .venv/                           # بيئة التشغيل (لا تُرفع) — شغّل كل شيء من داخلها
├── data/raw/                        # ضع المستندات الخام هنا / put raw docs here
├── etl_pipeline.py                  # Bronze → Silver → Gold pipeline
├── rag_api.py                       # نقطة النهاية / endpoint + evaluation
├── streamlit_ui.py                  # الواجهة الأصلية (5 تبويبات) / original UI
├── streamlit_ui_enhanced.py         # 🎓 NEW: الواجهة التعليمية (6 تبويبات + رسوم بيانية)
├── run_ui.sh                        # تشغيل الواجهة الأصلية / run original UI
├── run_ui_enhanced.sh               # 🎓 NEW: تشغيل الواجهة التعليمية / run educational UI
├── golden_dataset.json              # المجموعة المرجعية / golden dataset (12 Q&A)
├── ARCHITECTURE.md                  # معمارية / app architecture
├── ENHANCED_UI_README.md            # 🎓 NEW: دليل الواجهة المحسّنة / enhanced UI guide
├── l03_lab.db                       # SQLite (يُنشأ تلقائيًا) / auto-created
└── chroma_db/                       # فهرس ChromaDB / local index (auto-created)
```

## خطوات التشغيل / Steps
1. **التجهيز:** اتبع `../L03_Environment_Setup_Guide.md` (venv + SQLite مدمجة + متغيرات البيئة). / Follow the setup guide.
   يوجد نموذج بيانات جاهز في `data/raw` (ملفان) — أضف مستنداتك لنفس المجلد. / Sample docs are in `data/raw` — add your own files there.
2. **التشغيل (من داخل الـ venv ومع متغيرات macOS):**
   ```bash
   cd l03_lab
   source .venv/bin/activate
   OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 TOKENIZERS_PARALLELISM=false python -u etl_pipeline.py  # Bronze → Silver → Gold
   uvicorn rag_api:app --reload      # ثم / then http://localhost:8000/docs
   ```
3. **الاستعلام:**
   ```bash
   curl -X POST localhost:8000/query -H "Content-Type: application/json" \
        -d '{"question": "ما الفرق بين ETL وELT؟"}'
   ```
4. **التقييم مقابل المجموعة المرجعية:**
   ```bash
   python rag_api.py evaluate        # دقة السياق + العثور على المصدر المتوقع / context precision + expected-source hit
   ```
5. **واجهة المستخدم (Streamlit) — Choose one:**

   **Option A: 🎓 Enhanced Educational UI (Recommended for Learning)**
   ```bash
   ./run_ui_enhanced.sh   # 6 tabs with visual explanations, embeddings, charts
   # http://localhost:8501
   ```
   ✨ Features:
   - 🎓 Educational Flow tab with visual ETL, embedding space, RAG pipeline
   - 📊 Charts: embedding projections, similarity scores, flowcharts
   - 📚 Learning outcomes, external resources
   - 🔍 Enhanced debugging & metrics
   - See: `ENHANCED_UI_README.md` for full guide
   
   **Option B: Original Simple UI**
   ```bash
   ./run_ui.sh   # 5 tabs, minimal interface
   # http://localhost:8501
   ```
   5 tabs: رفع وفهرسة، مستندات، استعلام RAG، تقييم، معلومات
   Five tabs: upload & ingest, documents, RAG query, evaluation, about
   
   > **مهم / Important:** شغّل الواجهة من الـ venv حصرًا — التشغيل من بيئة بايثون عامة (مثل homebrew) مع مكوّنات غير متوافقة يسبب انهيارًا (segfault).
   > **Important:** run the UI strictly from the venv — a global Python env (e.g. homebrew) with mismatched packages causes a segfault.

## تفاصيل مجموعة البيانات / Dataset Details
- **عربي:** نموذجان جاهزان في `data/raw/`: `rag_basics.md` (أساسيات RAG: الاسترجاع، التقسيم، مثلث التقييم) و`etl_notes.txt` (المعمارية المتدرِّجة، عقود البيانات). الصيغ المدعومة: **TXT / MD / CSV / PDF** (تُقرأ PDF عبر pypdf).
- **EN:** two sample docs ship in `data/raw/`: `rag_basics.md` (RAG basics: retrieval, chunking, evaluation triad) and `etl_notes.txt` (Medallion architecture, data contracts). Supported formats: **TXT / MD / CSV / PDF** (PDFs via pypdf).
- **عربي:** أي مستند تضيفه إلى `data/raw/` يدخل تلقائيًا في الخط عند إعادة التشغيل — لا إعدادات إضافية. المجموعة المرجعية `golden_dataset.json` فيها **12 سؤالًا ثنائي اللغة** مع الإجابة والمصدر المتوقع لكل سؤال.
- **EN:** any document dropped into `data/raw/` flows through the pipeline on the next run — no extra config. `golden_dataset.json` holds **12 bilingual questions** with expected answers and sources.

## تفاصيل ETL / ETL Details
- **Bronze — التخزين الخام:** كل مستند يُقرأ **دون تعديل** ويُخزَّن في جدول SQLite `bronze_docs` (doc_id، الاسم، المحتوى، الطابع الزمني). / **Bronze:** each doc is read **unmodified** into SQLite table `bronze_docs` (doc_id, name, content, timestamp).
- **Silver — التنظيف:** إزالة التكرار التام، تطبيع المسافات، ثم **التقسيم التكراري** (500 حرفًا، تداخل 50): فقرات ← جُمل ← تقسيم صلب، مع إزالة التكرار التقريبي (تشابه ≥ 95%) — النتيجة في جدول `silver_chunks`. / **Silver:** exact dedup, whitespace normalization, then **recursive chunking** (500 chars, 50 overlap): paragraphs → sentences → hard split, plus fuzzy near-duplicate removal (similarity ≥ 95%) — stored in `silver_chunks`.
- **Gold — الفهرسة:** تضمينات محلية (`all-MiniLM-L6-v2`, بُعد 384) وفهرس **HNSW بمسافة cosine** في ChromaDB المحلي `./chroma_db` (المجموعة `gold_chunks`) — ترميز صريح بدفعات 10 مع سجلات `encode/inserting/done` وتقدم في الواجهة. / **Gold:** local embeddings (`all-MiniLM-L6-v2`, dim 384) and an **HNSW index with cosine space** in local ChromaDB `./chroma_db` (collection `gold_chunks`) — explicit encoding in batches of 10 with `encode/inserting/done` logs + UI progress.
- **عربي:** نموذج التضمين الافتراضي إنجليزي الميول — للاستعلامات العربية استخدم `question_en` أو بدّل دالة التضمين.
- **EN:** the default embedding model is English-leaning — for Arabic queries use `question_en` or swap the embedding function.

## تفاصيل الاختبار / Testing Details
- **`python rag_api.py evaluate`** يشغّل الأسئلة الـ 12 مقابل الفهرس ويقيس: **دقة السياق** (Context Precision ≈ متوسط التشابه الكوسيني للمقاطع المسترجعة) و**expected_source_found** (هل ظهر المصدر المتوقع ضمن النتائج؟).
  / runs the 12 questions against the index and reports **context precision** (≈ mean cosine similarity of retrieved chunks) and **expected_source_found** (did the expected source appear?).
- **عربي:** مع النموذجين الافتراضيَين تنجح أسئلة رقم 2، 3، 4، 7 (موجودة في المستندات)؛ البقية `False` **عمدًا** لتوضيح سلوك «لا توجد معلومات كافية» — أضف مستنداتك وستنجح تلقائيًا. الأسئلة تُرسل للفهرس بصيغتها الإنجليزية `question_en` لتوافق نموذج التضمين.
- **EN:** with the default samples, questions 2, 3, 4, 7 pass (covered by the docs); the rest are `False` **by design**, demonstrating the "insufficient information" behavior — add your docs and they pass automatically. Questions are sent to the index in their `question_en` form to match the embedding model.
- **اختبار نقطة النهاية يدويًا:** / manual endpoint test:
  ```bash
  curl -X POST localhost:8000/query -H "Content-Type: application/json" \
       -d '{"question": "What chunking strategy is recommended as the default?"}'
  # {"answer": "...[1]", "cached": false, "sources": [{"doc": "rag_basics.md", ...}]}
  ```
- **عربي:** التخزين الدلالي المؤقت يعيد الإجابات للأسئلة المتشابهة جدًا (تشابه ≥ 0.9) مع `cached: true` — جرّب إعادة السؤال بصياغة قريبة.
- **EN:** the semantic cache returns answers for very similar questions (similarity ≥ 0.9) with `cached: true` — try re-asking with slightly different wording.

## ما يتعلمه الطلاب / Learning Outcomes
- **عربي:** تنفيذ Bronze→Silver→Gold فعليًا، التقسيم التكراري، فهرس HNSW محلي، موجِّه مقيَّد بالمصادر مع استشهاد، تخزين دلالي مؤقت، وقياس دقة السياق مقابل معيار موحد.
- **EN:** hands-on Bronze→Silver→Gold, recursive chunking, a local HNSW index, grounded prompting with citations, semantic caching, and context-precision measurement against a shared benchmark.
