# -*- coding: utf-8 -*-
"""Generate Module02_Quizzes_AR_EN.md from deck_data (single source of truth)."""
from deck_data import DECKS

lines = ["# Module 02 — الاختبارات القصيرة مع الإجابات / Short Quizzes with Answers", ""]
for code in sorted(DECKS):
    spec = DECKS[code]
    lines += [f"## {code} — {spec['title_ar']} / {spec['title_en']}", ""]
    for i, (q_ar, q_en, a_ar, a_en) in enumerate(spec["quiz"], 1):
        lines += [f"**س{i}:** {q_ar}", f"**Q{i}:** {q_en}",
                  f"- ✅ **الإجابة:** {a_ar}",
                  f"- ✅ **Answer:** {a_en}", ""]
with open("Module02_Quizzes_AR_EN.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("written:", len(lines), "lines")
