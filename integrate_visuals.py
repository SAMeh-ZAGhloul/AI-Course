# -*- coding: utf-8 -*-
"""Insert visualization diagram slides into the updated module decks."""
from pptx import Presentation
import generate_visuals as gv
import generate_decks as gd
from deck_data import DECKS


def insert(prs, draw_fn, after_index):
    """Draw a new slide at the end, then move it to position after_index+1."""
    draw_fn(prs)
    lst = prs.slides._sldIdLst
    ids = list(lst)
    el = ids[-1]
    lst.remove(el)
    lst.insert(after_index + 1, el)


def modules_overview(prs):
    """Course-modules description slide (V06–V12), same body style as the deck."""
    pairs = [(f"{code} — {DECKS[code]['title_ar']}",
              f"{code} — {DECKS[code]['title_en']}")
             for code in sorted(DECKS)]
    gd.content_slide(prs, "وحدات المقرر / Course Modules", pairs)


jobs = {
    "output/Module02_V06_Updated.pptx": [
        (gv.v01_roadmap, 1),    # after "خريطة المسار" (idx 1)
        (modules_overview, 2),  # course modules description after roadmap visual
    ],
    "output/Module02_V07_Updated.pptx": [
        (gv.v03_patterns, 4),   # after "متى تختار كل نموذج؟" (idx 4 → pos 5)
        (gv.v04_contract, 3),   # after "منتجات البيانات وعقودها" (idx 3 → pos 4)
        (gv.v02_medallion, 2),  # after "معمارية Lakehouse" (idx 2 → pos 3)
    ],
    "output/Module02_V08_Updated.pptx": [
        (gv.v11_feature_store, 3),  # after "اتساق Offline/Online" (idx 3)
    ],
    "output/Module02_V09_Updated.pptx": [
        (gv.v07_triad, 5),          # after "التقييم + التحسين" (idx 5)
        (gv.v06_chunking, 2),       # after "الفهرسة: استراتيجيات التقسيم" (idx 2)
        (gv.v05_rag_pipeline, 1),   # after "قواعد البيانات المتجهية" (idx 1)
    ],
    "output/Module02_V10_Updated.pptx": [
        (gv.v12_labeling_flow, 3),  # after "التصنيف بمساعدة LLM" (idx 3)
    ],
    "output/Module02_V11_Updated.pptx": [
        (gv.v08_genai_arch, 3),     # after architecture part 2/2 (idx 3)
    ],
    "output/Module02_V12_Updated.pptx": [
        (gv.v09_cost, 4),       # after "التكلفة والأداء عمليًا" (idx 4)
        (gv.v10_concepts, 2),   # after "تمييز المفاهيم" (idx 2)
    ],
}

for path, inserts in jobs.items():
    prs = Presentation(path)
    for fn, idx in inserts:
        insert(prs, fn, idx)
    prs.save(path)
    print(path, "->", len(prs.slides._sldIdLst), "slides")
