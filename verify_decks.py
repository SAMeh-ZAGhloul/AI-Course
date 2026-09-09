# -*- coding: utf-8 -*-
from pptx import Presentation
from pptx.util import Pt

for code in ["V06", "V07", "V08", "V09", "V10", "V11", "V12"]:
    p = Presentation(f"output/Module02_{code}_Updated.pptx")
    print(code, f"({len(p.slides.__iter__.__self__._sldIdLst)} slides)")
    for i, s in enumerate(p.slides, 1):
        texts = [sh.text_frame.text.strip() for sh in s.shapes
                 if sh.has_text_frame and sh.text_frame.text.strip()]
        # title = the 26pt textbox
        title = "(?)"
        for sh in s.shapes:
            if sh.has_text_frame:
                for par in sh.text_frame.paragraphs:
                    for r in par.runs:
                        if r.font.size == Pt(26) and r.font.bold:
                            title = sh.text_frame.text[:60]
        if i == 1:
            title = texts[1] if len(texts) > 1 else texts[0]
        print(f"  {i}. {title[:65]}")
    # verify background is white and only basic colors used
    print("  bg:", p.slides[0].background.fill.fore_color.rgb)
