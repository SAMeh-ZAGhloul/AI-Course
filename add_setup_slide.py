# -*- coding: utf-8 -*-
"""Append L03 setup slide (OpenRouter free tier) to the glossary/quizzes deck."""
from pptx import Presentation
from pptx.util import Inches
import generate_visuals as gv
from gen_glossary_quiz_deck import text_box, para

PPTX = "output/Module02_Glossary_Quizzes.pptx"

p = Presentation(PPTX)
# drop outdated setup slides if present, then (re)add the current ones
removed = True
while removed:
    removed = False
    for idx, s in enumerate(list(p.slides)):
        txt = " ".join(sh.text_frame.text for sh in s.shapes if sh.has_text_frame)
        if "L03 Lab Setup" in txt:
            p.slides._sldIdLst.remove(list(p.slides._sldIdLst)[idx])
            removed = True
            break
if any("L03 Lab Setup" in sh.text_frame.text
       for s in p.slides for sh in s.shapes if sh.has_text_frame):
    print("setup slide already present — skipping")
else:
    part1 = [
        ("المتطلب: Python 3.11+ — بيئة افتراضية: python3 -m venv .venv && source .venv/bin/activate",
         "Prerequisite: Python 3.11+ — virtualenv: python3 -m venv .venv && source .venv/bin/activate"),
        ("التثبيت: pip install -r requirements.txt (numpy<2 لضمان توافق chromadb)",
         "Install: pip install -r requirements.txt (numpy<2 keeps chromadb compatible)"),
        ("قاعدة البيانات: SQLite — مدمجة في بايثون، لا خادم ولا تثبيت ولا كلمة مرور",
         "Database: SQLite — built into Python; no server, no install, no password"),
        ("طبقتا Bronze/Silver في ملف محلي l03_lab.db (يُنشأ تلقائيًا عند أول تشغيل)",
         "Bronze/Silver layers persist to a local l03_lab.db (auto-created on first run)"),
        ("الاتصال في .env: DB_URL=sqlite:///./l03_lab.db (قابل للتغيير)",
         "Connection in .env: DB_URL=sqlite:///./l03_lab.db (changeable)"),
        ("الفهرس المتجهي: ChromaDB محليًا — يخزّن في ./chroma_db (بدون خادم أو Docker)",
         "Vector index: local ChromaDB — persists to ./chroma_db (no server, no Docker)"),
    ]
    part2 = [
        ("مولّد النص: OpenRouter الخطة المجانية — أنشئ مفتاحًا من openrouter.ai",
         "Generator: OpenRouter free tier — create an API key at openrouter.ai"),
        ("ضع المفتاح في l03_lab/.env: OPENROUTER_API_KEY=sk-or-... (يُحمَّل تلقائيًا، ولا يُرفع إلى Git)",
         "Put the key in l03_lab/.env: OPENROUTER_API_KEY=sk-or-... (auto-loaded, never committed)"),
        ("النموذج الافتراضي المجاني: nvidia/nemotron-3-super-120b-a12b:free (قابل للتغيير)",
         "Default free model: nvidia/nemotron-3-super-120b-a12b:free (changeable)"),
        ("التنفيذ: python etl_pipeline.py — Bronze ← Silver ← Gold",
         "Run: python etl_pipeline.py — Bronze → Silver → Gold"),
        ("التشغيل: uvicorn rag_api:app --reload ثم افتح http://localhost:8000/docs",
         "Serve: uvicorn rag_api:app --reload then open http://localhost:8000/docs"),
        ("الاستعلام: POST /query — والتقييم: python rag_api.py evaluate مقابل golden_dataset.json",
         "Query: POST /query — Evaluate: python rag_api.py evaluate against golden_dataset.json"),
        ("استكشاف الأخطاء: 429 ← أعد المحاولة أو اختر نموذج :free آخر؛ المنفذ مشغول ← --port 8001",
         "Troubleshooting: 429 → retry or pick another :free model; port busy → --port 8001"),
    ]
    part3 = [
        ("البيانات: نموذجان جاهزان في data/raw (rag_basics.md، etl_notes.txt) — الصيغ: TXT/MD/CSV/PDF",
         "Dataset: two samples in data/raw (rag_basics.md, etl_notes.txt) — formats: TXT/MD/CSV/PDF"),
        ("المجموعة المرجعية: golden_dataset.json — 12 سؤالًا ثنائي اللغة مع الإجابة والمصدر المتوقع",
         "Golden dataset: golden_dataset.json — 12 bilingual questions with expected answers and sources"),
        ("Bronze: تخزين خام دون تعديل في جدول SQLite bronze_docs (doc_id، الاسم، المحتوى، الوقت)",
         "Bronze: raw unmodified storage in SQLite table bronze_docs (doc_id, name, content, ts)"),
        ("Silver: تنظيف + تقسيم تكراري (500 حرف، تداخل 50) + إزالة تكرار تقريبي ≥ 95% → silver_chunks",
         "Silver: clean + recursive chunking (500 chars, 50 overlap) + fuzzy dedup ≥ 95% → silver_chunks"),
        ("Gold: تضمينات MiniLM المحلية + فهرس HNSW بمسافة cosine في ./chroma_db (يُبنى مرة واحدة)",
         "Gold: local MiniLM embeddings + HNSW cosine index in ./chroma_db (built once)"),
        ("الاختبار: python rag_api.py evaluate — دقة السياق + expected_source_found لكل سؤال",
         "Testing: python rag_api.py evaluate — context precision + expected_source_found per question"),
        ("نتيجة النموذجين: الأسئلة 2/3/4/7 تنجح، والبقية False عمدًا — أضف مستنداتك لتغطيتها",
         "Baseline: questions 2/3/4/7 pass, the rest are False by design — add your docs to cover them"),
        ("الكاش الدلالي: أسئلة متشابهة ≥ 0.9 تعيد الإجابة مع cached:true — اختبار يدوي: curl POST /query",
         "Semantic cache: similar questions ≥ 0.9 return cached:true — manual test: curl POST /query"),
    ]
    for title, items in [("ملحق: تجهيز بيئة المختبر L03 (1/2) / Appendix: L03 Lab Setup (1/2)", part1),
                         ("ملحق: تجهيز بيئة المختبر L03 (2/2) / Appendix: L03 Lab Setup (2/2)", part2),
                         ("ملحق: بيانات المختبر وETL والاختبار / Appendix: Lab Dataset, ETL & Testing", part3)]:
        sl = gv.slide_new(p, title)
        y = Inches(1.1)
        for ar, en in items:
            tf = text_box(sl, Inches(0.8), y, Inches(11.8), Inches(0.8))
            para(tf, ar, 15, gv.INK, bold=True, first=True)
            para(tf, en, 12, gv.MUTED, is_ar=False)
            y += Inches(0.82)
        tf = text_box(sl, Inches(0.8), Inches(7.0), Inches(11.8), Inches(0.5))
        para(tf, "المرجع الكامل: L03_Environment_Setup_Guide.md — لا Docker إطلاقًا.",
             12, gv.MUTED, first=True)
        para(tf, "Full reference: L03_Environment_Setup_Guide.md — no Docker at all.",
             10, gv.MUTED, is_ar=False)
    p.save(PPTX)
    print("added; slides:", len(p.slides._sldIdLst))
