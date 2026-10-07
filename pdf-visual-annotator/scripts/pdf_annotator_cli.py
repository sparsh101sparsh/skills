#!/usr/bin/env python3
"""
PDF Visual Annotator CLI
========================
Command-line interface for PDF vector annotations, image markups, 3D prisms,
and step-by-step DSA visualizations.
"""

import argparse
import sys
import os
from typing import List

# Ensure scripts directory is on sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from pdf_annotator_engine import PDFCanvas, Geometry3D, DSAVisualizer, PALETTE, hex_to_rgb
import pymupdf


def cmd_arrow(args: argparse.Namespace) -> int:
    """Draw an arrow on a PDF page."""
    canvas = PDFCanvas.open(args.input, page_index=args.page)
    color = hex_to_rgb(args.color) if args.color else PALETTE["danger"]

    start = (args.start[0], args.start[1])
    end = (args.end[0], args.end[1])

    if args.control:
        control = (args.control[0], args.control[1])
        canvas.draw_curved_arrow(start, control, end, color=color, width=args.width)
    else:
        canvas.draw_arrow(
            start, end, color=color, width=args.width, double_ended=args.double_ended
        )

    canvas.save(args.output)
    print(f"✅ Arrow drawn successfully -> {args.output}")
    return 0


def cmd_highlight(args: argparse.Namespace) -> int:
    """Draw a highlight box on a PDF page."""
    canvas = PDFCanvas.open(args.input, page_index=args.page)
    fill_col = hex_to_rgb(args.color) if args.color else PALETTE["highlight_yellow"]
    border_col = hex_to_rgb(args.border_color) if args.border_color else PALETTE["warning"]

    rect = (args.rect[0], args.rect[1], args.rect[2], args.rect[3])
    canvas.draw_highlight(rect, fill_color=fill_col, opacity=args.opacity, border_color=border_col)

    canvas.save(args.output)
    print(f"✅ Highlight drawn successfully -> {args.output}")
    return 0


def cmd_callout(args: argparse.Namespace) -> int:
    """Draw a callout box with an arrow pointing to target."""
    canvas = PDFCanvas.open(args.input, page_index=args.page)
    border_col = hex_to_rgb(args.color) if args.color else PALETTE["primary"]

    box = (args.box[0], args.box[1], args.box[2], args.box[3])
    target = (args.target[0], args.target[1])
    canvas.draw_callout(box, args.text, target, border_color=border_col, fontsize=args.fontsize)

    canvas.save(args.output)
    print(f"✅ Callout drawn successfully -> {args.output}")
    return 0


def cmd_prism(args: argparse.Namespace) -> int:
    """Render a 3D prism on a PDF."""
    if args.input:
        canvas = PDFCanvas.open(args.input, page_index=args.page)
    else:
        canvas = PDFCanvas.create(width=600, height=600)

    color = hex_to_rgb(args.color) if args.color else PALETTE["primary"]

    if args.type == "triangular":
        Geometry3D.draw_triangular_prism(
            canvas,
            cx=args.cx,
            cy=args.cy,
            side=args.side,
            height=args.height,
            primary_color=color,
            fill_opacity=args.opacity,
            dashed_hidden=not args.no_dashed,
        )
    elif args.type == "rectangular":
        Geometry3D.draw_rectangular_prism(
            canvas,
            cx=args.cx,
            cy=args.cy,
            width=args.width,
            depth=args.depth,
            height=args.height,
            primary_color=color,
            fill_opacity=args.opacity,
            dashed_hidden=not args.no_dashed,
        )

    canvas.save(args.output)
    print(f"✅ 3D {args.type} prism rendered successfully -> {args.output}")
    return 0


def cmd_dsa_demo(args: argparse.Namespace) -> int:
    """Generate a multi-page step-by-step DSA visualization demo."""
    if args.algorithm == "binary-search":
        steps = [
            {
                "description": "Step 1: Initial state. Low=0, High=9, Mid=4 (Val=16). Target=23. 16 < 23 -> Search right half.",
                "array": [2, 5, 8, 12, 16, 23, 38, 56, 72, 91],
                "active": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                "compared": [4],
                "pointers": {"low": 0, "mid": 4, "high": 9},
                "note": "Elements at index 0..4 are now strictly less than target 23 and eliminated.",
            },
            {
                "description": "Step 2: Low=5, High=9, Mid=7 (Val=56). 56 > 23 -> Search left half.",
                "array": [2, 5, 8, 12, 16, 23, 38, 56, 72, 91],
                "active": [5, 6, 7, 8, 9],
                "compared": [7],
                "pointers": {"low": 5, "mid": 7, "high": 9},
                "note": "Search interval is reduced from [5..9] down to [5..6].",
            },
            {
                "description": "Step 3: Low=5, High=6, Mid=5 (Val=23). 23 == 23 -> TARGET FOUND!",
                "array": [2, 5, 8, 12, 16, 23, 38, 56, 72, 91],
                "active": [5, 6],
                "sorted": [5],
                "pointers": {"low": 5, "mid": 5, "high": 6},
                "note": "Target located in O(log N) comparisons. Algorithm terminates successfully.",
            },
        ]
        DSAVisualizer.create_algorithm_slide_deck(
            output_pdf=args.output,
            title="Binary Search Algorithm Visualizer",
            steps=steps,
        )
    elif args.algorithm == "two-pointers":
        steps = [
            {
                "description": "Step 1: Target sum = 18. Left=0 (Val=2), Right=6 (Val=19). Sum=21 > 18 -> Decrement Right.",
                "array": [2, 4, 7, 11, 14, 16, 19],
                "active": [0, 6],
                "compared": [0, 6],
                "pointers": {"left": 0, "right": 6},
                "note": "Current sum 2 + 19 = 21 exceeds target 18. Move right pointer leftward.",
            },
            {
                "description": "Step 2: Left=0 (Val=2), Right=5 (Val=16). Sum=18 == 18 -> PAIR FOUND!",
                "array": [2, 4, 7, 11, 14, 16, 19],
                "sorted": [0, 5],
                "pointers": {"left": 0, "right": 5},
                "note": "Indices [0, 5] with values (2, 16) sum exactly to 18.",
            },
        ]
        DSAVisualizer.create_algorithm_slide_deck(
            output_pdf=args.output,
            title="Two Pointers Algorithm Visualizer",
            steps=steps,
        )

    print(f"✅ DSA {args.algorithm} step-by-step PDF generated -> {args.output}")
    return 0


def cmd_annotate_image(args: argparse.Namespace) -> int:
    """Detect image on PDF and overlay vector annotations directly over it."""
    canvas = PDFCanvas.open(args.input, page_index=args.page)
    img_rects = canvas.get_image_rects()

    if not img_rects:
        print(f"⚠️ No embedded images detected on page {args.page} of {args.input}")
        return 1

    idx = min(args.image_idx, len(img_rects) - 1)
    target_rect = img_rects[idx]
    print(f"📷 Target image bbox: {target_rect}")

    # Center of image
    cx = (target_rect.x0 + target_rect.x1) / 2
    cy = (target_rect.y0 + target_rect.y1) / 2

    # Draw highlight over image
    canvas.draw_highlight(target_rect, fill_color=(0.2, 0.6, 1.0), opacity=0.15, border_color=(0.1, 0.4, 0.9))

    # Draw callout pointing to image center
    canvas.draw_callout(
        box_rect=(target_rect.x0 - 80, target_rect.y0 - 60, target_rect.x0 + 60, target_rect.y0 - 15),
        text=f"Detected Image #{idx}\nBBox: ({int(target_rect.x0)}, {int(target_rect.y0)})",
        target_point=(cx, cy),
        border_color=PALETTE["danger"],
    )

    canvas.save(args.output)
    print(f"✅ Image annotated successfully -> {args.output}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="PDF Visual Annotator CLI — Precision vector drawing, 3D shapes & DSA visualization"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # arrow
    p_arrow = subparsers.add_parser("arrow", help="Draw arrow on PDF")
    p_arrow.add_argument("--input", "-i", required=True, help="Input PDF path")
    p_arrow.add_argument("--output", "-o", required=True, help="Output PDF path")
    p_arrow.add_argument("--page", "-p", type=int, default=0, help="Page index (default: 0)")
    p_arrow.add_argument("--start", nargs=2, type=float, required=True, help="Start X Y")
    p_arrow.add_argument("--end", nargs=2, type=float, required=True, help="End X Y")
    p_arrow.add_argument("--control", nargs=2, type=float, help="Control X Y for curve")
    p_arrow.add_argument("--color", "-c", help="Hex color code (e.g. #e02424)")
    p_arrow.add_argument("--width", "-w", type=float, default=2.0, help="Stroke width")
    p_arrow.add_argument("--double-ended", action="store_true", help="Arrowhead on both ends")

    # highlight
    p_hl = subparsers.add_parser("highlight", help="Draw translucent highlight bounding box")
    p_hl.add_argument("--input", "-i", required=True, help="Input PDF path")
    p_hl.add_argument("--output", "-o", required=True, help="Output PDF path")
    p_hl.add_argument("--page", "-p", type=int, default=0, help="Page index (default: 0)")
    p_hl.add_argument("--rect", nargs=4, type=float, required=True, help="Rect x0 y0 x1 y1")
    p_hl.add_argument("--color", "-c", help="Fill hex color")
    p_hl.add_argument("--border-color", help="Border hex color")
    p_hl.add_argument("--opacity", type=float, default=0.35, help="Fill opacity (0..1)")

    # callout
    p_call = subparsers.add_parser("callout", help="Draw callout box with arrow")
    p_call.add_argument("--input", "-i", required=True, help="Input PDF path")
    p_call.add_argument("--output", "-o", required=True, help="Output PDF path")
    p_call.add_argument("--page", "-p", type=int, default=0, help="Page index (default: 0)")
    p_call.add_argument("--box", nargs=4, type=float, required=True, help="Box rect x0 y0 x1 y1")
    p_call.add_argument("--target", nargs=2, type=float, required=True, help="Target point X Y")
    p_call.add_argument("--text", "-t", required=True, help="Callout text")
    p_call.add_argument("--color", "-c", help="Border color")
    p_call.add_argument("--fontsize", type=float, default=10.0, help="Font size")

    # prism
    p_prism = subparsers.add_parser("prism", help="Render 3D prism")
    p_prism.add_argument("--type", choices=["triangular", "rectangular"], default="triangular")
    p_prism.add_argument("--input", "-i", help="Input PDF path (optional)")
    p_prism.add_argument("--output", "-o", required=True, help="Output PDF path")
    p_prism.add_argument("--page", "-p", type=int, default=0, help="Page index")
    p_prism.add_argument("--cx", type=float, default=300, help="Center X")
    p_prism.add_argument("--cy", type=float, default=380, help="Center Y")
    p_prism.add_argument("--side", type=float, default=130, help="Side length (triangular)")
    p_prism.add_argument("--width", type=float, default=140, help="Width (rectangular)")
    p_prism.add_argument("--depth", type=float, default=90, help="Depth (rectangular)")
    p_prism.add_argument("--height", type=float, default=160, help="Height")
    p_prism.add_argument("--color", "-c", help="Hex color")
    p_prism.add_argument("--opacity", type=float, default=0.45, help="Fill opacity")
    p_prism.add_argument("--no-dashed", action="store_true", help="Disable dashed hidden lines")

    # dsa-demo
    p_dsa = subparsers.add_parser("dsa-demo", help="Generate step-by-step DSA deck")
    p_dsa.add_argument(
        "--algorithm",
        choices=["binary-search", "two-pointers"],
        default="binary-search",
        help="Algorithm to demonstrate",
    )
    p_dsa.add_argument("--output", "-o", required=True, help="Output PDF path")

    # annotate-image
    p_ai = subparsers.add_parser("annotate-image", help="Overlay annotations on image in PDF")
    p_ai.add_argument("--input", "-i", required=True, help="Input PDF path")
    p_ai.add_argument("--output", "-o", required=True, help="Output PDF path")
    p_ai.add_argument("--page", "-p", type=int, default=0, help="Page index")
    p_ai.add_argument("--image-idx", type=int, default=0, help="Image index on page")

    args = parser.parse_args()

    dispatch = {
        "arrow": cmd_arrow,
        "highlight": cmd_highlight,
        "callout": cmd_callout,
        "prism": cmd_prism,
        "dsa-demo": cmd_dsa_demo,
        "annotate-image": cmd_annotate_image,
    }

    return dispatch[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
