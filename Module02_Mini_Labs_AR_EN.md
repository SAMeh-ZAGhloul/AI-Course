# Module 02 — التمارين المصغّرة لكل وحدة / Mini-Labs per Module

تمارين تطبيقية قصيرة (~15 دقيقة) بعد كل وحدة. / Short hands-on exercises (~15 min) after each module.

## بعد V06 — تنظيف CSV / After V06 — CSV Cleaning
- **عربي:** حمّل ملف CSV فيه قيم ناقصة وتكرارات؛ نظّفه بـ pandas (إزالة التكرار، معالجة القيم الناقصة، توحيد التنسيقات)، وارفع النتيجة كملف Parquet.
- **EN:** Load a CSV with missing values and duplicates; clean it with pandas and save as Parquet.

## بعد V07 — مقارنة Bronze/Silver/Gold / Bronze/Silver/Gold Comparison
- **عربي:** خذ نفس البيانات وطبّقها على ثلاث طبقات: خام في Bronze، منقّاة في Silver، تجميعة أعمال في Gold؛ ووثّق ما تغيّر في كل طبقة.
- **EN:** Apply the same data across Bronze (raw), Silver (cleansed), and Gold (business aggregates); document what changed per layer.

## بعد V08 — اتساق الميزات / Feature Consistency
- **عربي:** أنشئ ميزة تجميعية (مثل متوسط آخر 7 أيام) في pandas، وأعِد حسابها بنفس المنطق في "مسار خدمة" وهمي؛ تحقق من تطابق القيم (إزالة الانحراف).
- **EN:** Build a rolling-7-day feature and recompute it in a mock serving path; verify value consistency (no skew).

## بعد V09 — فهرسة واسترجاع متجهي / Vector Indexing & Retrieval
- **عربي:** قسّم نصًا تقسيمًا تكراريًا، وأنشئ فهرس ChromaDB، ونفّذ بحثًا هجينًا بسيطًا؛ قارن النتائج قبل/بعد إعادة الترتيب.
- **EN:** Recursively chunk a document, build a ChromaDB index, run a hybrid search; compare results before/after reranking.

## بعد V10 — تصنيف بمساعدة LLM / LLM-assisted Labeling
- **عربي:** صنّف 20 تعليقًا بـ LLM (إيجابي/سلبي/محايد)، راجعها يدويًا، واحسب نسبة الاتفاق بين النموذج وبينك.
- **EN:** LLM-label 20 comments (pos/neg/neutral), review manually, compute human–model agreement.

## بعد V11 — خط عن بسيط / Simple Lineage Map
- **عربي:** ارسم خط عن (lineage) لخط بيانات المقرر: المصدر → Bronze → Silver → Gold → فهرس متجهي → RAG؛ مع تدقيق واحد (أمن/جودة) لكل وصلة.
- **EN:** Draw lineage: source → Bronze → Silver → Gold → vector index → RAG, with one control per hop.

## بعد V12 — تتبع تجربة / Experiment Tracking
- **عربي:** شغّل تمرين V09 مرة أخرى مع MLflow: سجّل باراميترات التقسيم والدرجات، وقارن تشغيلتين.
- **EN:** Re-run the V09 exercise with MLflow: log chunking params and scores, compare two runs.

## بعد L03 — تحسين المسترجع / Improve Your Retriever
- **عربي:** عدّل حجم التقسيم أو فعّل إعادة الترتيب في مختبر L03 وقِس أثر التغيير على مثلث RAG باستخدام المجموعة المرجعية.
- **EN:** Change chunk size or enable reranking in L03; measure the effect on the RAG triad using the golden dataset.
- **تشغيل المختبر / Lab run:** من `l03_lab/` داخل الـ venv: `python -u etl_pipeline.py` (Bronze→Silver→Gold بدفعات 10) ثم `./run_ui.sh` للواجهة (`:8501`) أو `uvicorn rag_api:app --reload` للـ API (`:8000/docs`). التفاصيل في `l03_lab/ARCHITECTURE.md` ودليل التجهيز `L03_Environment_Setup_Guide.md`.
- **Lab run:** from `l03_lab/` inside the venv: `python -u etl_pipeline.py` (Bronze→Silver→Gold in batches of 10) then `./run_ui.sh` for the UI (`:8501`) or `uvicorn rag_api:app --reload` for the API (`:8000/docs`). See `l03_lab/ARCHITECTURE.md` and `L03_Environment_Setup_Guide.md`.
