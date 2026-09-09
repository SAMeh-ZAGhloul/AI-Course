# -*- coding: utf-8 -*-
"""Generate updated Module 02 decks (V06-V12): light theme, basic colors,
right-to-left text direction and large fonts on all slides."""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

from deck_data import DECKS

# Basic colors only (light theme)
BG = RGBColor(0xFF, 0xFF, 0xFF)      # white
TITLE = RGBColor(0x1F, 0x3B, 0x5C)   # dark blue
BODY = RGBColor(0x33, 0x33, 0x33)    # dark gray
ACCENT = RGBColor(0x1F, 0x4E, 0x79)  # blue
MUTED = RGBColor(0x66, 0x66, 0x66)   # gray

SW, SH = Inches(13.333), Inches(7.5)

# Font sizes (increased on all slides)
SZ_TITLE, SZ_BODY, SZ_QUIZ, SZ_READ = 32, 19, 20, 20
SZ_CODE, SZ_AR, SZ_EN, SZ_SUB = 34, 48, 34, 18


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
             align=PP_ALIGN.RIGHT, rtl=True):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    set_rtl(p, rtl)
    r = p.add_run()
    r.text = text
    f = r.font
    f.size, f.bold, f.name = Pt(size), bold, "Calibri"
    f.color.rgb = color
    return box


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
            p.alignment = PP_ALIGN.RIGHT
            set_rtl(p, is_ar)
            r = p.add_run()
            r.text = ("• " if is_ar else "   ") + text
            r.font.size, r.font.name = Pt(size), "Calibri"
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
    add_text(s, code, Inches(0.9), Inches(1.4), Inches(11.5), Inches(0.8),
             SZ_CODE, ACCENT, bold=True)
    add_text(s, ar, Inches(0.9), Inches(2.4), Inches(11.5), Inches(1.2),
             SZ_AR, TITLE, bold=True)
    add_text(s, en, Inches(0.9), Inches(3.9), Inches(11.5), Inches(1.0),
             SZ_EN, BODY, rtl=False)
    add_text(s, "Module 02 — Data & AI Engineering Track  |  الوحدة الثانية",
             Inches(0.9), Inches(5.6), Inches(11.5), Inches(0.6), SZ_SUB, MUTED)
    return s


def quiz_slide(prs, quiz):
    pairs = [(f"{i}. {q_ar}", q_en) for i, (q_ar, q_en, *_ ) in
             enumerate(quiz, 1)]
    return content_slide(prs, "اختبار قصير / Quick Quiz", pairs, size=SZ_QUIZ)


def reading_slide(prs, reading):
    return content_slide(prs, "للاستزادة / Further Reading", reading,
                         size=SZ_READ)


def build(code, spec, outdir="output"):
    prs = new_deck()
    title_slide(prs, code, spec["title_ar"], spec["title_en"])
    for t, pairs in spec["slides"]:
        longest = max(len(p[0]) for p in pairs)
        content_slide(prs, t, pairs, size=SZ_BODY if longest <= 110 else 18)
    quiz_slide(prs, spec["quiz"])
    reading_slide(prs, spec["reading"])
    path = f"{outdir}/Module02_{code}_Updated.pptx"
    prs.save(path)
    return path, len(prs.slides._sldIdLst)


if __name__ == "__main__":
    import os
    os.makedirs("output", exist_ok=True)
    for code in sorted(DECKS):
        path, n = build(code, DECKS[code])
        print(f"{path}: {n} slides")
