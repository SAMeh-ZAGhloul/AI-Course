# -*- coding: utf-8 -*-
"""Generate updated Module 02 decks (V06-V12): light theme, basic colors,
right-to-left text direction and large fonts on all slides."""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import re

from deck_data import DECKS

# Basic colors only (light theme)
BG = RGBColor(0xFF, 0xFF, 0xFF)      # white
TITLE = RGBColor(0x1F, 0x3B, 0x5C)   # dark blue
BODY = RGBColor(0x33, 0x33, 0x33)    # dark gray
ACCENT = RGBColor(0x1F, 0x4E, 0x79)  # blue
MUTED = RGBColor(0x66, 0x66, 0x66)   # gray

SW, SH = Inches(13.333), Inches(7.5)

# Font stacks: Arabic-capable primary, Latin fallback
FONT_AR = "Arial"
FONT_EN = "Calibri"
SZ_TITLE, SZ_BODY, SZ_QUIZ, SZ_READ = 32, 19, 20, 20
SZ_CODE, SZ_AR, SZ_EN, SZ_SUB = 28, 44, 30, 18
FOOTER_TXT = "Module 02 — Data & AI Engineering Track  |  الوحدة الثانية"
FOOTER_PAGE = re.compile(r"^V\d{2}\s+•\s+\d+/\d+$")


def set_rtl(paragraph, rtl=True):
    """Set right-to-left text direction on a paragraph (a:pPr@rtl)."""
    pPr = paragraph._p.get_or_add_pPr()
    pPr.set("rtl", "1" if rtl else "0")


def new_deck():
    prs = Presentation()
    prs.slide_width, prs.slide_height = SW, SH
    return prs


def blank(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])


def bg_white(slide):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = BG


def add_text(slide, text, left, top, width, height, size, color, bold=False,
             align=PP_ALIGN.RIGHT, rtl=True, font=None):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    set_rtl(p, rtl)
    r = p.add_run()
    r.text = text
    f = r.font
    f.size, f.bold = Pt(size), bold
    f.name = font or (FONT_AR if rtl else FONT_EN)
    f.color.rgb = color
    return box


def footer(slide, code, idx, total):
    clear_footer(slide)
    add_text(slide, FOOTER_TXT, Inches(0.7), Inches(7.0), Inches(9.5),
             Inches(0.35), 10, MUTED, rtl=True, font=FONT_AR)
    add_text(slide, f"{code}  •  {idx}/{total}", Inches(10.5), Inches(7.0),
             Inches(2.1), Inches(0.35), 10, MUTED, align=PP_ALIGN.LEFT,
             rtl=False, font=FONT_EN)


def clear_footer(slide):
    """Remove generated footer shapes before adding the current page number."""
    for shape in list(slide.shapes):
        if not shape.has_text_frame:
            continue
        text = shape.text_frame.text.strip()
        if text == FOOTER_TXT or FOOTER_PAGE.fullmatch(text):
            shape._element.getparent().remove(shape._element)


def bullets(slide, pairs, top, size=SZ_BODY):
    """pairs: list of (ar, en) tuples or plain strings.
    Arabic lines: RTL + right-aligned; English lines: LTR but right-aligned."""
    box = slide.shapes.add_textbox(Inches(0.7), top, Inches(12.0),
                                   SH - top - Inches(0.4))
    tf = box.text_frame
    tf.word_wrap = True
    first = True
    for item in pairs:
        ar, en = item if isinstance(item, tuple) else (item, None)
        for text, color, is_ar in ((ar, BODY, True), (en, MUTED, False)):
            if text is None:
                continue
            p = tf.paragraphs[0] if first else tf.add_paragraph()
            first = False
            p.space_after = Pt(10)
            p.space_before = Pt(2)
            p.alignment = PP_ALIGN.RIGHT if is_ar else PP_ALIGN.LEFT
            set_rtl(p, is_ar)
            r = p.add_run()
            r.text = ("• " if is_ar else "• ") + text
            r.font.size = Pt(size if is_ar else max(size - 3, 12))
            r.font.name = FONT_AR if is_ar else FONT_EN
            r.font.color.rgb = color
    return box


def title_bar(slide, text):
    bar = slide.shapes.add_shape(1, Inches(0), Inches(0), SW, Inches(1.1))
    bar.fill.solid()
    bar.fill.fore_color.rgb = BG
    bar.line.color.rgb = ACCENT
    bar.line.width = Pt(2)
    bar.shadow.inherit = False
    add_text(slide, text, Inches(0.7), Inches(0.2), Inches(12.0),
             Inches(0.7), SZ_TITLE, TITLE, bold=True)


def content_slide(prs, title, pairs, size=SZ_BODY):
    s = blank(prs)
    bg_white(s)
    title_bar(s, title)
    bullets(s, pairs, Inches(1.4), size)
    return s


def title_slide(prs, code, ar, en):
    s = blank(prs)
    bg_white(s)
    add_text(s, "Module 02  |  " + code, Inches(0.9), Inches(1.2), Inches(11.5), Inches(0.7),
             SZ_CODE, ACCENT, bold=True, align=PP_ALIGN.LEFT, rtl=False, font=FONT_EN)
    add_text(s, ar, Inches(0.9), Inches(2.1), Inches(11.5), Inches(1.2),
             SZ_AR, TITLE, bold=True, font=FONT_AR)
    add_text(s, en, Inches(0.9), Inches(3.5), Inches(11.5), Inches(1.0),
             SZ_EN, BODY, rtl=False, align=PP_ALIGN.LEFT, font=FONT_EN)
    add_text(s, FOOTER_TXT,
             Inches(0.9), Inches(5.4), Inches(11.5), Inches(0.6), SZ_SUB, MUTED, font=FONT_AR)
    add_text(s, "Light theme  |  Bilingual AR/EN  |  Ready to present",
             Inches(0.9), Inches(6.0), Inches(11.5), Inches(0.5), 14, MUTED,
             align=PP_ALIGN.LEFT, rtl=False, font=FONT_EN)
    return s


def quiz_slide(prs, quiz):
    pairs = [(f"{i}. {q_ar}", q_en) for i, (q_ar, q_en, *_ ) in
             enumerate(quiz, 1)]
    return content_slide(prs, "اختبار قصير / Quick Quiz", pairs, size=SZ_QUIZ)


def answer_slide(prs, quiz):
    pairs = [(f"{i}. {a_ar}", a_en) for i, (_, _, a_ar, a_en) in
             enumerate(quiz, 1)]
    return content_slide(prs, "إجابات الاختبار / Quiz Answers", pairs,
                         size=max(SZ_QUIZ - 2, 14))


def table_slide(prs, title, headers, rows):
    """Real pptx table (RTL header row first) instead of bullet paragraphs."""
    from pptx.util import Emu
    s = blank(prs)
    bg_white(s)
    title_bar(s, title)
    nrow, ncol = len(rows) + 1, len(headers)
    left, top, width = Inches(0.7), Inches(1.5), Inches(12.0)
    table_shape = s.shapes.add_table(nrow, ncol, left, top, width, Inches(0.6 * nrow))
    tbl = table_shape.table
    for j, h in enumerate(headers):
        c = tbl.cell(0, j)
        c.text = ""
        p = c.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        set_rtl(p, True)
        r = p.add_run(); r.text = h
        r.font.size, r.font.bold, r.font.name = Pt(14), True, FONT_AR
        r.font.color.rgb = BG
        c.fill.solid(); c.fill.fore_color.rgb = ACCENT
    for i, row in enumerate(rows, 1):
        for j, val in enumerate(row):
            c = tbl.cell(i, j)
            c.text = ""
            p = c.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            set_rtl(p, True)
            r = p.add_run(); r.text = val
            r.font.size, r.font.name = Pt(12), FONT_AR
            r.font.color.rgb = BODY
            c.fill.solid()
            c.fill.fore_color.rgb = RGBColor(0xF2, 0xF2, 0xF2) if i % 2 == 0 else BG
    return s


def reading_slide(prs, reading):
    return content_slide(prs, "للاستزادة / Further Reading", reading,
                         size=SZ_READ)


TABLES = {
    "V06": ("جدول المقارنة: Medallion / المستودع / Data Mesh",
            ["المعيار", "Medallion", "المستودع", "Data Mesh"],
            [["الفكرة", "طبقات Bronze→Silver→Gold", "Staging→Warehouse→Marts", "منتجات بالمجالات"],
             ["المالك", "هندسة مركزية", "فرق BI", "فرق المجالات"],
             ["الأنسب", "تحليلات و AI/RAG", "تقارير BI", "مؤسسات كبيرة"],
             ["الحوكمة", "جودة بين الطبقات", "مركزية", "موحدة + عقود"]]),
    "V07": ("متى تختار كل نموذج؟ / Decision Matrix",
            ["الحالة", "الاختيار", "السبب"],
            [["فريق مركزي + تحليلات", "Medallion / Lakehouse", "مرونة + حوكمة طبقية"],
             ["تقارير صارمة", "Warehouse", "SQL سريع + مخطط ثابت"],
             ["فرق مستقلة كبيرة", "Data Mesh", "ملكية لامركزية + عقود"]]),
}


def build(code, spec, outdir="output"):
    prs = new_deck()
    title_slide(prs, code, spec["title_ar"], spec["title_en"])
    # TOC slide for every deck (P2 polish)
    toc = [(f"{code} — {spec['title_ar']}", f"{code} — {spec['title_en']}")] + \
          [(t, None) for t, _ in spec["slides"][:6]]
    content_slide(prs, "أجندة العرض / Agenda", toc, size=16)
    for t, pairs in spec["slides"]:
        # skip redundant text slides superseded by visuals (merged P0)
        if code == "V06" and (t.startswith("خريطة المسار") or t.startswith("جدول المقارنة السريع")):
            continue  # visual roadmap + real comparison table replace them
        longest = max(len(p[0]) for p in pairs)
        content_slide(prs, t, pairs, size=SZ_BODY if longest <= 110 else 18)
    # real tables replace bullet comparison slides (P1)
    if code in TABLES:
        table_slide(prs, TABLES[code][0], TABLES[code][1], TABLES[code][2])
    quiz_slide(prs, spec["quiz"])
    answer_slide(prs, spec["quiz"])
    reading_slide(prs, spec["reading"])
    total = len(prs.slides._sldIdLst) + 3  # estimate incl. visuals
    for i, s in enumerate(prs.slides, 1):
        footer(s, code, i, total)
    path = f"{outdir}/Module02_{code}_Updated.pptx"
    prs.save(path)
    return path, len(prs.slides._sldIdLst)


if __name__ == "__main__":
    import os
    os.makedirs("output", exist_ok=True)
    for code in sorted(DECKS):
        path, n = build(code, DECKS[code])
        print(f"{path}: {n} slides")
