"""Cross-deck regression checks for presentable Module 02 decks."""
from pathlib import Path
import re
import unittest

from pptx import Presentation


OUTPUT = Path("output")
FOOTER_TEXT = "Module 02 — Data & AI Engineering Track"
PAGE = re.compile(r"^V\d{2}\s+•\s+\d+/\d+$")


class OutputDeckTests(unittest.TestCase):
    def test_low_text_concepts_have_supporting_visuals(self):
        expected = {
            "V06": "Data Spectrum & Formats",
            "V07": "Warehouse vs Lake Decision Map",
            "V08": "Raw Data to Features",
            "V10": "Label Quality Loop",
            "V11": "Data Lineage Map",
            "V12": "MLOps Lifecycle",
        }
        for code, visual_title in expected.items():
            presentation = Presentation(OUTPUT / f"Module02_{code}_Updated.pptx")
            text = "\n".join(
                " ".join(
                    shape.text_frame.text
                    for shape in slide.shapes
                    if shape.has_text_frame and shape.text_frame.text.strip()
                )
                for slide in presentation.slides
            )
            self.assertIn(visual_title, text, code)

    def test_glossary_has_a_visual_category_map(self):
        presentation = Presentation(OUTPUT / "Module02_Glossary_Quizzes.pptx")
        text = "\n".join(
            " ".join(
                shape.text_frame.text
                for shape in slide.shapes
                if shape.has_text_frame and shape.text_frame.text.strip()
            )
            for slide in presentation.slides
        )
        self.assertIn("Glossary Map", text)

    def test_updated_module_decks_have_one_valid_footer_per_slide(self):
        for path in sorted(OUTPUT.glob("Module02_V??_Updated.pptx")):
            presentation = Presentation(path)
            for number, slide in enumerate(presentation.slides, 1):
                footer_count = sum(
                    1
                    for shape in slide.shapes
                    if shape.has_text_frame and FOOTER_TEXT in shape.text_frame.text
                )
                pages = [
                    shape.text_frame.text.strip()
                    for shape in slide.shapes
                    if shape.has_text_frame and "•" in shape.text_frame.text
                ]
                self.assertEqual(footer_count, 1, f"{path.name} slide {number}")
                self.assertEqual(sum(bool(PAGE.fullmatch(page)) for page in pages), 1,
                                 f"{path.name} slide {number}: {pages}")


if __name__ == "__main__":
    unittest.main()
