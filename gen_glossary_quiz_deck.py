# -*- coding: utf-8 -*-
"""Build one PPTX from Glossary_AR_EN.md + Module02_Quizzes_AR_EN.md."""
import re
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import generate_visuals as gv

INK, ACCENT, MUTED = gv.INK, gv.ACCENT, gv.MUTED
FONT_AR, FONT_EN = gv.FONT_AR, gv.FONT_EN


def rtl(par, on=True):
    par._p.get_or_add_pPr().set("rtl", "1" if on else "0")


def text_box(slide, x, y, w, h):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tb.text_frame.word_wrap = True
    return tb.text_frame


def para(tf, txt, size, color=INK, bold=False, first=False, align=PP_ALIGN.RIGHT,
         is_ar=True):
    p = tf.paragraphs[0] if first and not tf.paragraphs[0].runs else tf.add_paragraph()
    p.alignment = align
    rtl(p, is_ar)
    r = p.add_run(); r.text = txt
    imported_font = FONT_AR if is_ar else FONT_EN
    r.font.size, r.font.bold, r.font.color.rgb, r.font.name = Pt(size), bold, color, imported_font
    return p


def parse_glossary(path):
    pairs = []
    for line in open(path, encoding="utf-8"):
        m = re.match(r"\|\s*(.+?)\s*\|\s*(.+?)\s*\|", line)
        if m and m.group(1) not in ("العربية / Arabic", "---"):
            ar, en = m.groups()
            if "----" not in ar:
                pairs.append((ar, en))
    return pairs


def parse_quizzes(path):
    sections, cur = [], None
    q = None
    for line in open(path, encoding="utf-8"):
        line = line.rstrip()
        m = re.match(r"##\s+(.+)", line)
        if m:
            cur = {"title": m.group(1), "items": []}
            sections.append(cur); q = None
            continue
        mq = re.match(r"\*\*س\d+:\*\*\s*(.+)", line)
        if mq and cur is not None:
            q = {"q_ar": mq.group(1), "a_ar": "", "a_en": ""}
            cur["items"].append(q); continue
        me = re.match(r"\*\*Q\d+:\*\*\s*(.+)", line)
        if me and q is not None:
            q["q_en"] = me.group(1); continue
        ma = re.match(r"-\s*✅\s*\*\*الإجابة:\*\*\s*(.+)", line)
        if ma and q is not None:
            q["a_ar"] = ma.group(1); continue
        men = re.match(r"-\s*✅\s*\*\*Answer:\*\*\s*(.+)", line)
        if men and q is not None:
            q["a_en"] = men.group(1)
    return sections
def title_slide(prs, ar, en):
    s = gv.slide_new(prs, "")  # blank title bar; custom big title below
    for sh in list(s.shapes):
        sh._element.getparent().remove(sh._element)
    tf = text_box(s, Inches(1.0), Inches(2.3), Inches(11.3), Inches(1.6))
    para(tf, ar, 44, gv.TITLE_C, bold=True, first=True)
    para(tf, en, 26, MUTED, is_ar=False)
    tf2 = text_box(s, Inches(1.0), Inches(4.4), Inches(11.3), Inches(0.8))
    para(tf2, "الوحدة الثانية — مادة مساندة / Module 02 — Supporting Material",
         18, MUTED, first=True)
    return s


def glossary_slides(prs, pairs, per_slide=6):
    slides = []
    for i in range(0, len(pairs), per_slide):
        chunk = pairs[i:i + per_slide]
        s = gv.slide_new(prs, f"المصطلحات ({i // per_slide + 1}) / Glossary")
        y = Inches(1.15)
        for ar, en in chunk:
            tf = text_box(s, Inches(6.7), y, Inches(6.0), Inches(0.78))
            para(tf, ar, 17, INK, bold=True, first=True)
            tf2 = text_box(s, Inches(0.7), y, Inches(5.9), Inches(0.78))
            para(tf2, en, 15, MUTED, first=True, align=PP_ALIGN.LEFT, is_ar=False)
            ln = s.shapes.add_shape(gv.MSO_SHAPE.RECTANGLE, Inches(0.7),
                                    y + Inches(0.74), Inches(12.0), Pt(0.75))
            ln.fill.solid(); ln.fill.fore_color.rgb = gv.FILL_A
            ln.line.fill.background(); ln.shadow.inherit = False
            y += Inches(0.88)
        slides.append(s)
    return slides


def quiz_slides(prs, sections):
    """Q-per-slide + A reveal: one question slide + one answer slide per section."""
    slides = []
    for sec in sections:
        # question-only slide
        s = gv.slide_new(prs, sec["title"] + " — أسئلة / Questions")
        y = Inches(1.15)
        for it in sec["items"]:
            tf = text_box(s, Inches(0.7), y, Inches(12.0), Inches(1.0))
            para(tf, "س: " + it["q_ar"], 16, INK, bold=True, first=True)
            if it.get("q_en"):
                para(tf, "Q: " + it["q_en"], 12, MUTED, is_ar=False)
            y += Inches(1.1)
        slides.append(s)
        # answer slide
        s2 = gv.slide_new(prs, sec["title"] + " — إجابات / Answers")
        y = Inches(1.15)
        for it in sec["items"]:
            tf = text_box(s2, Inches(0.7), y, Inches(12.0), Inches(1.0))
            para(tf, "✅ " + it["a_ar"], 14, ACCENT, bold=True, first=True)
            if it.get("a_en"):
                para(tf, "✅ " + it["a_en"], 11, MUTED, is_ar=False)
            y += Inches(1.1)
        slides.append(s2)
    return slides


def bullet_slide(prs, title, bullets, note_ar=None, note_en=None):
    """One architecture/setup slide: RTL title + bilingual bullet cards.

    bullets: list of (ar, en) tuples. Each gets a rounded card with
    Arabic bold on top + English muted below.
    """
    s = gv.slide_new(prs, title)
    n = max(len(bullets), 1)
    h = Inches(5.3) / n - Inches(0.1)
    h = min(max(h, Inches(0.75)), Inches(1.35))
    y = Inches(1.15)
    fills = [gv.FILL_A, gv.FILL_B, gv.FILL_C, gv.FILL_D]
    for i, (ar, en) in enumerate(bullets):
        gv.card(s, Inches(0.7), y, Inches(12.0), h,
                ar, en, fills[i % 4], size=15, sub=12)
        y += h + Inches(0.1)
    if note_ar or note_en:
        gv.note(s, note_ar or "", note_en,
                y=Inches(6.7))
    return s


def code_slide(prs, title, lines, note_ar=None, note_en=None):
    """One setup slide with literal LTR command lines (no RTL mangling)."""
    s = gv.slide_new(prs, title)
    y = Inches(1.15)
    for block in lines:
        tf = text_box(s, Inches(0.7), y, Inches(12.0), Inches(0.62))
        para(tf, block, 15, INK, bold=True, first=True,
             align=PP_ALIGN.LEFT, is_ar=False)
        y += Inches(0.62)
    if note_ar or note_en:
        gv.note(s, note_ar or "", note_en, y=Inches(6.7))
    return s


def l03_architecture_slides(prs):
    """Detailed L03 app architecture + setup (replaces the old 3-item quiz)."""
    out = []
    out.append(bullet_slide(
        prs, "معمارية مختبر L03 / L03 Lab Architecture",
        [("خط ETL ‏(etl_pipeline.py):‏ Bronze ‏(SQLite خام) ← Silver ‏(تنظيف + تقسيم 500/50) ← Gold ‏(ChromaDB HNSW cosine، دفعات 10)",
           "ETL (etl_pipeline.py): Bronze (raw SQLite) → Silver (clean + 500/50 chunk) → Gold (ChromaDB HNSW cosine, batches of 10)"),
         ("الخلفية ‏(rag_api.py:8000):‏ استرجاع كثيف top-k=5 حد 0.2 ← توليد مؤرَّض OpenRouter free ← كاش دلالي 0.92 ← تقييم golden (12 سؤالًا)",
          "Backend (rag_api.py :8000): dense top-k=5 ≥0.2 → grounded OpenRouter free → semantic cache 0.92 → golden eval (12 Q)"),
         ("الواجهة ‏(streamlit_ui.py:8501):‏ 5 تبويبات ثنائية — رفع/مستندات/استعلام/تقييم/حول — تُعيد استخدام نفس عميل Chroma مع حذف المجموعة وإعادة إنشائها",
          "Frontend (streamlit_ui.py :8501): 5 bilingual tabs — upload/docs/query/eval/about — same Chroma client, drop & recreate"),
         ("المخازن: l03_lab.db ‏(bronze_docs/silver_chunks)‏ + chroma_db ‏(gold_chunks بُعد 384)‏ + golden_dataset.json + env.‏ للمفتاح",
          "Stores: l03_lab.db (bronze_docs/silver_chunks) + chroma_db (gold_chunks dim 384) + golden_dataset.json + .env for keys")],
        note_ar="التفاصيل الكاملة في l03_lab/ARCHITECTURE.md.",
        note_en="Full detail in l03_lab/ARCHITECTURE.md."))
    out.append(code_slide(
        prs, "تشغيل مختبر L03 / Running the L03 Lab",
        ["cd l03_lab  +  source .venv/bin/activate",
         "OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 TOKENIZERS_PARALLELISM=false  python -u etl_pipeline.py",
         "./run_ui.sh   →   http://localhost:8501",
         "uvicorn rag_api:app --reload   →   http://localhost:8000/docs",
         "python rag_api.py evaluate"],
        note_ar="دائمًا من داخل الـ venv — التشغيل الخارجي يسبب segfault.",
        note_en="Always inside the venv — outside env segfaults."))
    out.append(bullet_slide(
        prs, "دروس الجمود / Freeze Lessons (مطبَّقة في الكود)",
        [("عميل ChromaDB واحد فقط — عميل ثانٍ = قفل SQLite وتجمّد بعد [Silver]",
           "Single ChromaDB client only — a 2nd client = SQLite lock, freeze after [Silver]"),
         ("حذف المجموعة وإعادة إنشائها بدل delete+add على مقطع HNSW مستخدَم",
          "Drop & recreate collection instead of delete+add on a used HNSW segment"),
         ("ترميز صريح بدفعات 10 + سجلات encode/inserting/done + شريط تقدم",
          "Explicit encoding in batches of 10 + encode/inserting/done logs + progress bar"),
         ("macOS: ‏OMP/MKL=1‏ + ‏TOKENIZERS_PARALLELISM=false‏ قبل استيراد onnx + ‏python -u‏ + اسم ‏gold_chunks‏ موحّد",
          "macOS: OMP/MKL=1 + TOKENIZERS_PARALLELISM=false before onnx import + python -u + one gold_chunks name")],
        note_ar="أول تشغيل لـ Gold يُنزّل all-MiniLM-L6-v2 ‏(~80MB)‏ لمرة واحدة.",
        note_en="First Gold run downloads all-MiniLM-L6-v2 (~80MB) once."))
    return out


if __name__ == "__main__":
    prs = gv.prs_new()
    title_slide(prs, "المصطلحات والاختبارات القصيرة", "Glossary & Short Quizzes")
    gv.v20_glossary_map(prs)
    glossary_slides(prs, parse_glossary("Glossary_AR_EN.md"))
    l03_architecture_slides(prs)  # detailed L03 architecture + setup (was: thin quiz)
    quiz_slides(prs, parse_quizzes("Module02_Quizzes_AR_EN.md"))
    out = "output/Module02_Glossary_Quizzes.pptx"
    prs.save(out)
    print(out, len(prs.slides._sldIdLst), "slides")
