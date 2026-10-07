"""
Automated Test Suite for PDF Visual Annotator
=============================================
Verifies vector drawings, image overlays, 3D prism projections,
DSA step generation, and CLI subcommands.
"""

import os
import sys
import tempfile
import unittest
import math
from PIL import Image

# Add scripts directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from pdf_annotator_engine import PDFCanvas, Geometry3D, DSAVisualizer, PALETTE, hex_to_rgb
import pdf_annotator_cli
import pymupdf


class TestPDFVisualAnnotator(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_hex_to_rgb(self):
        # White
        self.assertEqual(hex_to_rgb("#ffffff"), (1.0, 1.0, 1.0))
        # Black
        self.assertEqual(hex_to_rgb("000000"), (0.0, 0.0, 0.0))
        # Red
        self.assertEqual(hex_to_rgb("#ff0000"), (1.0, 0.0, 0.0))

    def test_canvas_creation_and_save(self):
        pdf_path = os.path.join(self.temp_dir.name, "blank.pdf")
        canvas = PDFCanvas.create(width=500, height=500)
        canvas.draw_rect((50, 50, 200, 200), color=PALETTE["primary"], fill=PALETTE["neutral_light"])
        canvas.save(pdf_path)

        self.assertTrue(os.path.exists(pdf_path))
        doc = pymupdf.open(pdf_path)
        self.assertEqual(len(doc), 1)
        self.assertEqual(int(doc[0].rect.width), 500)
        self.assertEqual(int(doc[0].rect.height), 500)
        doc.close()

    def test_vector_arrows_and_callout(self):
        pdf_path = os.path.join(self.temp_dir.name, "arrows.pdf")
        canvas = PDFCanvas.create(width=600, height=600)

        # Straight arrow
        canvas.draw_arrow((100, 100), (300, 100), color=PALETTE["danger"], width=2.0)

        # Double-ended arrow
        canvas.draw_arrow((100, 150), (300, 150), color=PALETTE["primary"], double_ended=True)

        # Curved arrow
        canvas.draw_curved_arrow((100, 200), (200, 300), (300, 200), color=PALETTE["warning"])

        # Callout box
        canvas.draw_callout(
            box_rect=(50, 350, 200, 420),
            text="Test Callout Note",
            target_point=(350, 380),
        )

        canvas.save(pdf_path)
        self.assertTrue(os.path.exists(pdf_path))
        doc = pymupdf.open(pdf_path)
        self.assertEqual(len(doc), 1)
        doc.close()

    def test_image_overlay(self):
        # 1. Create a dummy test image
        img_path = os.path.join(self.temp_dir.name, "test_img.png")
        img = Image.new("RGB", (300, 200), color=(200, 220, 240))
        img.save(img_path)

        # 2. Insert image into PDF and annotate on top of it
        pdf_path = os.path.join(self.temp_dir.name, "annotated_img.pdf")
        canvas = PDFCanvas.create(width=600, height=600)
        img_rect = pymupdf.Rect(100, 100, 400, 300)
        canvas.insert_image(img_rect, filename=img_path, overlay=True)

        # Check detected images
        detected_rects = canvas.get_image_rects()
        self.assertGreaterEqual(len(detected_rects), 1)

        # Draw highlight and arrow directly over the image bbox
        canvas.draw_highlight((150, 150, 250, 250), opacity=0.4)
        canvas.draw_arrow((120, 120), (200, 200), color=PALETTE["danger"])

        canvas.save(pdf_path)
        self.assertTrue(os.path.exists(pdf_path))
        doc = pymupdf.open(pdf_path)
        self.assertEqual(len(doc), 1)
        doc.close()

    def test_3d_triangular_prism(self):
        pdf_path = os.path.join(self.temp_dir.name, "prism_tri.pdf")
        canvas = PDFCanvas.create(width=600, height=600)
        vertices = Geometry3D.draw_triangular_prism(
            canvas=canvas,
            cx=300,
            cy=350,
            side=120,
            height=150,
            dashed_hidden=True,
            label_vertices=True,
        )
        canvas.save(pdf_path)

        # Check all 6 projected vertices exist
        for expected_v in ["V0", "V1", "V2", "V3", "V4", "V5"]:
            self.assertIn(expected_v, vertices)
            pt = vertices[expected_v]
            self.assertIsInstance(pt, pymupdf.Point)

        doc = pymupdf.open(pdf_path)
        self.assertEqual(len(doc), 1)
        doc.close()

    def test_3d_rectangular_prism(self):
        pdf_path = os.path.join(self.temp_dir.name, "prism_rect.pdf")
        canvas = PDFCanvas.create(width=600, height=600)
        vertices = Geometry3D.draw_rectangular_prism(
            canvas=canvas,
            cx=300,
            cy=350,
            width=120,
            depth=80,
            height=140,
            dashed_hidden=True,
            label_vertices=True,
        )
        canvas.save(pdf_path)

        # Check all 8 vertices exist
        for expected_v in ["A", "B", "C", "D", "E", "F", "G", "H"]:
            self.assertIn(expected_v, vertices)

        doc = pymupdf.open(pdf_path)
        self.assertEqual(len(doc), 1)
        doc.close()

    def test_dsa_multi_page_deck(self):
        pdf_path = os.path.join(self.temp_dir.name, "dsa_test.pdf")
        steps = [
            {
                "description": "Step 1: Check mid",
                "array": [10, 20, 30, 40],
                "active": [0, 1, 2, 3],
                "pointers": {"low": 0, "mid": 1, "high": 3},
            },
            {
                "description": "Step 2: Found",
                "array": [10, 20, 30, 40],
                "active": [1],
                "sorted": [1],
                "pointers": {"low": 1, "mid": 1, "high": 1},
            },
        ]
        DSAVisualizer.create_algorithm_slide_deck(
            output_pdf=pdf_path,
            title="Unit Test Algorithm",
            steps=steps,
        )

        self.assertTrue(os.path.exists(pdf_path))
        doc = pymupdf.open(pdf_path)
        self.assertEqual(len(doc), 2)  # Multi-page verification
        doc.close()

    def test_cli_subcommands(self):
        # 1. Base PDF
        base_pdf = os.path.join(self.temp_dir.name, "base.pdf")
        c = PDFCanvas.create(width=500, height=500)
        c.save(base_pdf)

        # 2. CLI arrow
        out_arrow = os.path.join(self.temp_dir.name, "out_arrow.pdf")
        res = pdf_annotator_cli.main_args = [
            "arrow", "--input", base_pdf, "--output", out_arrow,
            "--start", "50", "50", "--end", "200", "200"
        ]
        import sys
        sys.argv = ["pdf_annotator_cli.py"] + pdf_annotator_cli.main_args
        ret = pdf_annotator_cli.main()
        self.assertEqual(ret, 0)
        self.assertTrue(os.path.exists(out_arrow))

        # 3. CLI prism
        out_prism = os.path.join(self.temp_dir.name, "out_prism.pdf")
        sys.argv = [
            "pdf_annotator_cli.py", "prism", "--type", "triangular",
            "--output", out_prism, "--cx", "250", "--cy", "250"
        ]
        ret = pdf_annotator_cli.main()
        self.assertEqual(ret, 0)
        self.assertTrue(os.path.exists(out_prism))

        # 4. CLI DSA
        out_dsa = os.path.join(self.temp_dir.name, "out_dsa.pdf")
        sys.argv = [
            "pdf_annotator_cli.py", "dsa-demo", "--algorithm", "binary-search",
            "--output", out_dsa
        ]
        ret = pdf_annotator_cli.main()
        self.assertEqual(ret, 0)
        self.assertTrue(os.path.exists(out_dsa))


if __name__ == "__main__":
    unittest.main()
