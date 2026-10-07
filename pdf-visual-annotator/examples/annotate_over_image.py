#!/usr/bin/env python3
"""
Example: Annotating Directly Over an Image in a PDF
===================================================
Demonstrates inserting an image into a PDF page, detecting its bounding box,
and overlaying precision vector arrows, translucent highlights, and callouts
directly on top of the image content.
"""

import os
import sys
import tempfile
from PIL import Image, ImageDraw

# Add scripts directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from pdf_annotator_engine import PDFCanvas, PALETTE
import pymupdf


def create_sample_chart_image(filepath: str) -> None:
    """Create a sample synthetic telemetry chart image for demonstration."""
    img = Image.new("RGB", (600, 400), color=(245, 247, 250))
    draw = ImageDraw.Draw(img)

    # Grid lines
    for y in range(50, 400, 50):
        draw.line([(50, y), (550, y)], fill=(225, 230, 235), width=1)
    for x in range(50, 600, 100):
        draw.line([(x, 50), (x, 350)], fill=(225, 230, 235), width=1)

    # Data curve
    points = [
        (50, 300), (150, 260), (250, 280), (350, 140), (450, 180), (550, 90)
    ]
    draw.line(points, fill=(40, 110, 220), width=3)
    for pt in points:
        draw.ellipse([pt[0]-4, pt[1]-4, pt[0]+4, pt[1]+4], fill=(220, 50, 50), outline=(255, 255, 255))

    img.save(filepath, "PNG")


def main():
    output_pdf = "annotated_image_output.pdf"
    print("🚀 Running Image Annotation Workflow...")

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp_img_path = tmp.name

    try:
        # 1. Generate sample image
        create_sample_chart_image(tmp_img_path)

        # 2. Create PDF canvas
        canvas = PDFCanvas.create(width=700, height=850)

        # 3. Add Page Title & Context Header
        canvas.shape.insert_text(
            pymupdf.Point(50, 50),
            "System Telemetry Report: Anomaly Inspection",
            fontsize=18,
            fontname="helv",
            color=PALETTE["neutral_dark"],
        )
        canvas.shape.insert_text(
            pymupdf.Point(50, 75),
            "Demonstration: Programmatic vector arrows and highlights overlaid directly on top of embedded PDF image.",
            fontsize=11,
            fontname="helv",
            color=(0.35, 0.38, 0.42),
        )

        # 4. Insert image onto page
        img_rect = pymupdf.Rect(50, 120, 650, 520)
        canvas.insert_image(img_rect, filename=tmp_img_path, overlay=True)

        # 5. Draw translucent highlight bounding box OVER the peak in the image
        # In PDF coordinates: peak is around X=400, Y=265
        peak_highlight = pymupdf.Rect(375, 230, 440, 310)
        canvas.draw_highlight(
            peak_highlight,
            fill_color=PALETTE["warning"],
            opacity=0.35,
            border_color=PALETTE["danger"],
            border_width=2.0,
        )

        # 6. Draw callout arrow pointing directly to the anomaly peak inside the image
        callout_box = pymupdf.Rect(470, 150, 640, 220)
        target_pt = pymupdf.Point(407, 270)
        canvas.draw_callout(
            box_rect=callout_box,
            text="CRITICAL SPIKE DETECTED\nMagnitude: +142%\nTimestamp: T+350ms\nAction: Throttling engaged",
            target_point=target_pt,
            bg_color=(1.0, 1.0, 1.0),
            border_color=PALETTE["danger"],
            text_color=PALETTE["neutral_dark"],
            fontsize=10,
        )

        # 7. Draw curved arrow highlighting baseline trend
        canvas.draw_curved_arrow(
            start=pymupdf.Point(90, 470),
            control=pymupdf.Point(200, 490),
            end=pymupdf.Point(300, 420),
            color=PALETTE["primary"],
            width=2.5,
        )
        canvas.shape.insert_text(
            pymupdf.Point(120, 505),
            "Nominal baseline drift",
            fontsize=10,
            fontname="helv",
            color=PALETTE["primary"],
        )

        # 8. Commit and save
        canvas.save(output_pdf)
        print(f"✅ Generated: {output_pdf}")

    finally:
        if os.path.exists(tmp_img_path):
            os.remove(tmp_img_path)


if __name__ == "__main__":
    main()
