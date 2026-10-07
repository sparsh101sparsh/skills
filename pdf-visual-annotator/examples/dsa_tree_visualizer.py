#!/usr/bin/env python3
"""
Example: Binary Search Tree (BST) Visualizer on PDF
===================================================
Demonstrates rendering a tree data structure on a PDF canvas,
with circular nodes, labels, directed branch edges, and path highlighting.
"""

import os
import sys

# Add scripts directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from pdf_annotator_engine import PDFCanvas, PALETTE
import pymupdf


def draw_tree_node(canvas: PDFCanvas, pt: pymupdf.Point, value: str, radius: float = 20.0, state: str = "normal"):
    """Render a single tree node with state coloring."""
    if state == "highlight":
        fill = PALETTE["warning"]
        stroke = PALETTE["danger"]
        text_col = PALETTE["neutral_dark"]
    elif state == "target":
        fill = PALETTE["success"]
        stroke = PALETTE["success"]
        text_col = PALETTE["white"]
    else:
        fill = PALETTE["neutral_light"]
        stroke = PALETTE["primary"]
        text_col = PALETTE["neutral_dark"]

    canvas.draw_circle(pt, radius=radius, color=stroke, fill=fill, width=2.0)
    # Centered text
    canvas.shape.insert_text(
        pymupdf.Point(pt.x - len(value)*4.2, pt.y + 4.5),
        value,
        fontsize=12,
        fontname="helv",
        color=text_col,
    )


def draw_tree_edge(canvas: PDFCanvas, p_parent: pymupdf.Point, p_child: pymupdf.Point, radius: float = 20.0, is_path: bool = False):
    """Draw directed branch between parent node and child node."""
    import math
    dx = p_child.x - p_parent.x
    dy = p_child.y - p_parent.y
    dist = math.hypot(dx, dy)
    if dist == 0:
        return
    ux, uy = dx / dist, dy / dist

    start = pymupdf.Point(p_parent.x + radius * ux, p_parent.y + radius * uy)
    end = pymupdf.Point(p_child.x - radius * ux, p_child.y - radius * uy)

    col = PALETTE["danger"] if is_path else (0.55, 0.58, 0.62)
    w = 2.5 if is_path else 1.5
    canvas.draw_arrow(start, end, color=col, width=w, head_len=8, head_width=5)


def main():
    output_pdf = "dsa_tree_output.pdf"
    print("🚀 Generating Binary Search Tree Visualizer on PDF...")

    canvas = PDFCanvas.create(width=750, height=550)

    # Header
    canvas.shape.insert_text(
        pymupdf.Point(50, 45),
        "Binary Search Tree Traversal: Search for Key = 27",
        fontsize=18,
        fontname="helv",
        color=PALETTE["neutral_dark"],
    )
    canvas.shape.insert_text(
        pymupdf.Point(50, 70),
        "Traversal Path: Root(50) -> Left(30) -> Left(20) [20 < 27] -> Right(27) [FOUND]",
        fontsize=12,
        fontname="helv",
        color=(0.35, 0.38, 0.42),
    )

    # Node positions: (id, x, y, value, state)
    nodes = {
        50: (pymupdf.Point(375, 140), "50", "highlight"),
        30: (pymupdf.Point(225, 230), "30", "highlight"),
        70: (pymupdf.Point(525, 230), "70", "normal"),
        20: (pymupdf.Point(140, 330), "20", "highlight"),
        40: (pymupdf.Point(310, 330), "40", "normal"),
        60: (pymupdf.Point(440, 330), "60", "normal"),
        85: (pymupdf.Point(610, 330), "85", "normal"),
        27: (pymupdf.Point(190, 430), "27", "target"),
    }

    # Edges: (parent, child, is_path)
    edges = [
        (50, 30, True),
        (50, 70, False),
        (30, 20, True),
        (30, 40, False),
        (70, 60, False),
        (70, 85, False),
        (20, 27, True),
    ]

    # Draw edges first
    for parent_id, child_id, is_path in edges:
        p_pt = nodes[parent_id][0]
        c_pt = nodes[child_id][0]
        draw_tree_edge(canvas, p_pt, c_pt, radius=20, is_path=is_path)

    # Draw nodes
    for node_id, (pt, val, state) in nodes.items():
        draw_tree_node(canvas, pt, val, radius=20, state=state)

    # Legend / Callout
    canvas.draw_callout(
        box_rect=pymupdf.Rect(460, 400, 700, 480),
        text="TARGET FOUND: Node 27\nTotal Comparisons: 4\nComplexity: O(h) = O(log N)",
        target_point=nodes[27][0],
        bg_color=(0.95, 1.0, 0.95),
        border_color=PALETTE["success"],
        text_color=PALETTE["neutral_dark"],
        fontsize=10,
    )

    canvas.save(output_pdf)
    print(f"✅ Generated: {output_pdf}")


if __name__ == "__main__":
    main()
