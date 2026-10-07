#!/usr/bin/env python3
"""
Example: 3D Prism Geometric Rendering on PDF
============================================
Demonstrates rendering an isometric 3D triangular prism and a 3D rectangular
cuboid with translucent face shading, dashed hidden edges, and vertex badges.
"""

import os
import sys

# Add scripts directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from pdf_annotator_engine import PDFCanvas, Geometry3D, PALETTE
import pymupdf


def main():
    output_pdf = "3d_prisms_output.pdf"
    print("🚀 Rendering 3D Prisms onto PDF...")

    canvas = PDFCanvas.create(width=850, height=550)

    # Header
    canvas.shape.insert_text(
        pymupdf.Point(50, 45),
        "3D Geometric Polyhedra Rendering Engine",
        fontsize=18,
        fontname="helv",
        color=PALETTE["neutral_dark"],
    )
    canvas.shape.insert_text(
        pymupdf.Point(50, 70),
        "Isometric 3D Projection with depth sorting, translucent face lighting, and dashed hidden back edges.",
        fontsize=12,
        fontname="helv",
        color=(0.35, 0.38, 0.42),
    )

    # 1. Left side: Triangular Prism
    canvas.shape.insert_text(
        pymupdf.Point(130, 120),
        "Equilateral Triangular Prism",
        fontsize=14,
        fontname="helv",
        color=PALETTE["primary"],
    )
    Geometry3D.draw_triangular_prism(
        canvas=canvas,
        cx=240,
        cy=380,
        side=140,
        height=180,
        primary_color=PALETTE["primary"],
        fill_opacity=0.45,
        dashed_hidden=True,
        label_vertices=True,
        show_dimensions=True,
    )

    # 2. Right side: Rectangular Prism (Cuboid)
    canvas.shape.insert_text(
        pymupdf.Point(520, 120),
        "Rectangular Prism (Cuboid)",
        fontsize=14,
        fontname="helv",
        color=PALETTE["success"],
    )
    Geometry3D.draw_rectangular_prism(
        canvas=canvas,
        cx=590,
        cy=380,
        width=150,
        depth=100,
        height=140,
        primary_color=PALETTE["success"],
        fill_opacity=0.45,
        dashed_hidden=True,
        label_vertices=True,
    )

    canvas.save(output_pdf)
    print(f"✅ Generated: {output_pdf}")


if __name__ == "__main__":
    main()
