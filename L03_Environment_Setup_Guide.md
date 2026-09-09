# L03 — دليل تجهيز البيئة (تثبيت محلي، دون Docker)
# L03 — Environment Setup Guide (Local Installation, No Docker)

**الهدف:** تجهيز بيئة محلية خفيفة قبل أسبوع المختبر: Python في بيئة افتراضية (venv)، وSQLite المدمجة في بايثون لطبقتَي Bronze/Silver، وChromaDB لفهرس Gold، ونقطة نهاية FastAPI وواجهة Streamlit.
**Goal:** a lightweight local environment ready before lab week: Python venv, SQLite (built into Python) for Bronze/Silver, ChromaDB for the Gold index, plus a FastAPI endpoint and a Streamlit UI.

## 1. Python 3.11+ وبيئة افتراضية / venv
```bash
cd l03_lab
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

> ⚠️ **مهم / Important:** كل أوامر التشغيل (`etl_pipeline.py` / `uvicorn` / `streamlit`) يجب أن تُنفَّذ **من داخل الـ venv** — التشغيل من بيئة عامة (مثل homebrew python) مع خلط الحزم يسبب انهيارًا (segfault) عند فتح المتصفح.
> Run everything **inside the venv** — a global Python with mismatched packages segfaults at browser connect.

## 2. SQLite (مدمجة في بايثون — لا تثبيت) / SQLite (built into Python — no install)
- **عربي:** طبقتا Bronze/Silver تخزنان في ملف محلي `l03_lab.db` عبر SQLite — **تأتي ضمن مكتبة Python القياسية**، فلا خادم ولا خدمة ولا كلمة مرور. تُنشأ قاعدة البيانات تلقائيًا عند أول تشغيل لـ `etl_pipeline.py`.
- **EN:** the Bronze/Silver layers persist to a local `l03_lab.db` file via SQLite — **part of the Python standard library**, so no server, service, or password. The database file is created automatically on the first run of `etl_pipeline.py`.
- **عربي:** رابط الاتصال مضبوط في `.env`: `DB_URL=sqlite:///./l03_lab.db` (يمكن تغييره).
- **EN:** the connection URL is set in `.env`: `DB_URL=sqlite:///./l03_lab.db` (changeable).

## 3. ChromaDB (فهرس متجهي محلي) / Local Vector Index
- **عربي:** يُثبَّت عبر pip ويخزّن الفهرس في مجلد محلي `./chroma_db` — لا يحتاج خادمًا ولا حاويات. اسم المجموعة الموحّد: **`gold_chunks`** (يجب أن يتطابق في `etl_pipeline.py` و`rag_api.py` و`streamlit_ui.py`).
- **EN:** installed via pip, persists to a local `./chroma_db` folder — no server, no containers. Canonical collection name: **`gold_chunks`** (must match in `etl_pipeline.py`, `rag_api.py`, `streamlit_ui.py`).
- **عربي:** أول تشغيل لطبقة Gold يُنزّل نموذج التضمين `all-MiniLM-L6-v2` (~80MB من HuggingFace) — يلزم اتصال إنترنت لمرة واحدة.
- **EN:** the first Gold run downloads the `all-MiniLM-L6-v2` embedding model (~80MB from HuggingFace) — one-time internet access required.
- **عربي (macOS M1/M2):** لتفادي تجمّد ONNX/tokenizers شغّل دائمًا مع `OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 TOKENIZERS_PARALLELISM=false` (مثال: `... python -u etl_pipeline.py`). سكربت `run_ui.sh` يضبطها تلقائيًا — فضّله: `./run_ui.sh`.
- **EN (macOS M1/M2):** to avoid the ONNX/tokenizers deadlock always run with `OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 TOKENIZERS_PARALLELISM=false`. `run_ui.sh` sets them automatically — prefer `./run_ui.sh`.

## 4. مفاتيح LLM / LLM Keys
- **عربي:** للمولّد النصي نستخدم **OpenRouter (الخطة المجانية)**: أنشئ حسابًا في openrouter.ai، وأنشئ مفتاح API، ثم اختر نموذجًا مجانيًا (الافتراضي `nvidia/nemotron-3-super-120b-a12b:free`). بديل مدفوع: OpenAI API مباشرة.
- **EN:** generation uses **OpenRouter (free tier)**: create an account at openrouter.ai, generate an API key, and pick a free model (default `nvidia/nemotron-3-super-120b-a12b:free`). Paid alternative: OpenAI API directly.
```bash
export OPENROUTER_API_KEY="sk-or-..."  # مطلوب للمسار الافتراضي / required for the default path
export GENERATOR="openrouter"          # أو "openai" / or "openai"
export OPENROUTER_MODEL="nvidia/nemotron-3-super-120b-a12b:free"  # اختياري / optional
```
- **عربي:** النموذج الافتراضي مضبوط في ملف `.env` داخل `l03_lab/` — يُحمَّل تلقائيًا عند التشغيل (المفتاح سرّي: لا ترفعه إلى Git، وقد حُمي عبر `.gitignore`).
- **EN:** the default model is set in `l03_lab/.env` — loaded automatically at startup (the key is a secret: never commit it; protected via `.gitignore`).
- **عربي:** ملاحظة — النماذج المجانية (`:free`) لها حد استخدام يومي؛ يكفي لأغراض المختبر.
- **EN:** note — `:free` models have daily rate limits; sufficient for lab purposes.

## 5. التحقق / Smoke Test
```bash
cd l03_lab
source .venv/bin/activate
python -u etl_pipeline.py      # Bronze → Silver → Gold (ينتهي بـ "ChromaDB HNSW index ready: N vectors")
uvicorn rag_api:app --reload   # ثم افتح http://localhost:8000/docs
./run_ui.sh                    # أو الواجهة: http://localhost:8501
```

## استكشاف الأخطاء / Troubleshooting
- **عربي:** بطء أول تشغيل لـ Gold → تحميل نموذج التضمين (~80MB) لمرة واحدة؛ تجمّد Gold عند `... 32/222` أو بعده → أعد التشغيل مع متغيرات `OMP/MKL/TOKENIZERS` أعلاه ثم `rm -rf chroma_db l03_lab.db` وأعد البناء.
- **EN:** slow first Gold run → one-time embedding-model download (~80MB); Gold freeze at `... 32/222` or later → re-run with the `OMP/MKL/TOKENIZERS` vars above, then `rm -rf chroma_db l03_lab.db` and rebuild.
- **عربي:** تجمّد الرفع في Streamlit بعد `[Silver]` → سببه عميل ChromaDB ثانٍ (قفل SQLite)؛ أُصلح بإعادة استخدام نفس العميل + حذف المجموعة وإعادة إنشائها (`delete_collection` ثم `get_or_create_collection`) بدفعات 10 مع شريط تقدم. إن تكرر: أوقف Streamlit (مفتاح `Ctrl+C`) وأعد التشغيل عبر `./run_ui.sh`.
- **EN:** Streamlit upload freeze after `[Silver]` → caused by a second ChromaDB client (SQLite lock); fixed by reusing the same client + drop & recreate (`delete_collection` then `get_or_create_collection`) in batches of 10 with a progress bar. If it recurs: stop Streamlit (the `Ctrl+C` key) and relaunch via `./run_ui.sh`.
- **عربي:** `zsh: no matches found: (Ctrl+C)` → لصقتَ سطر تعليمات فيه أقواس؛ نفّذ الأوامر فقط دون سطور `# ...`.
- **EN:** `zsh: no matches found: (Ctrl+C)` → you pasted an instruction line containing parens; run only the commands, not `# ...` lines.
- **عربي:** منفذ 8000 مشغول → `uvicorn rag_api:app --port 8001`؛ خطأ قاعدة البيانات → احذف `l03_lab.db` وأعد تشغيل `etl_pipeline.py` (سيُعاد إنشاؤه)؛ حد 429 من OpenRouter → النموذج المجاني مشغول مؤقتًا، أعد المحاولة أو اختر `:free` آخر.
- **EN:** port 8000 busy → use `--port 8001`; database error → delete `l03_lab.db` and re-run `etl_pipeline.py` (it is recreated); OpenRouter 429 → the free model is temporarily rate-limited, retry or pick another `:free` model.
- **عربي:** التشغيل خارج الـ venv يسبب segfault عند فتح المتصفح → تحقق أن `which python` داخل `l03_lab/.venv`، أو شغّل عبر `./run_ui.sh`.
- **EN:** running outside the venv segfaults at browser connect → verify `which python` points inside `l03_lab/.venv`, or launch via `./run_ui.sh`.
