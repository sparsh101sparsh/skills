---
name: pdf-visual-annotator
description: >-
  Programmatic PDF vector diagramming, arrows, callouts over images, step-by-step
  DSA algorithm visualization, and 3D geometric polyhedra/prism rendering via PyMuPDF.
  Use when drawing arrows, callouts, or shapes directly on PDF pages or over embedded images,
  rendering 3D polyhedra/prisms with dashed hidden lines and shading, or generating step-by-step
  data structure diagrams.
---

# PDF Visual Annotator & Diagramming Master Skill

You are a **document visualization engineer** specializing in pixel-accurate vector graphics, algorithm animations, and geometric illustrations directly on PDF documents.

> **Prime Directive:** Never rasterize vector diagrams unless explicitly required. Every arrow, bounding box, tree node, and 3D prism face must be injected into the PDF page content stream as native vector objects (`page.new_shape()`), ensuring crisp rendering at any zoom level. When annotating over embedded images, always commit drawings to the foreground layer (`overlay=True`).

---

## 1. Core Operating Principles

### 1.1 Direct Native Vector Canvas Over Regeneration
Most AI assistants attempt to either recreate whole documents from scratch or convert PDFs into raster images (PNG/JPEG) to draw on them with Pillow/OpenCV, losing text selectability and sharpness.
- **The PyMuPDF (`pymupdf`) Advantage:** Operates directly on existing PDFs in place. Modifies the page's native vector display list.
- **Image Overlays:** Directly detects embedded image bounding boxes (`page.get_image_info()`) and overlays vector highlights, arrows, and callouts on top of them without re-encoding the underlying image.

### 1.2 Coordinate System Rules (72 DPI Points)
- **Origin $(0, 0)$:** Top-left corner of the unrotated page.
- **X Axis:** Extends horizontally to the right ($0 \to \text{width}$).
- **Y Axis:** Extends vertically downward ($0 \to \text{height}$).
- **Bounding Boxes:** Represented as `pymupdf.Rect(x0, y0, x1, y1)`.
- **Rotated Pages:** Coordinates must always reference the unrotated page or adjust via `page.rotation_matrix`.

### 1.3 3D Isometric Projection Standards
When rendering 3D shapes (such as triangular prisms or cuboids):
- **Projection Formula ($30^\circ$ angle):**
  $$p_x = c_x + (x - y) \cdot \cos(30^\circ)$$
  $$p_y = c_y + (x + y) \cdot \sin(30^\circ) - z$$
- **Hidden Edges:** Occluded interior edges must be rendered with a dashed stroke: `dashes="[4 4] 0"`.
- **Face Lighting:** Top face ($+15\%$ luminance, `fill_opacity=0.6`), Front face (nominal, `fill_opacity=0.45`), Side face ($-10\%$ luminance, `fill_opacity=0.35`).

---

## 2. Package Architecture

```
pdf-visual-annotator/
├── SKILL.md                          # Master instruction file & runbook
├── scripts/
│   ├── pdf_annotator_engine.py       # Core vector engine (PDFCanvas, Geometry3D, DSAVisualizer)
│   ├── pdf_annotator_cli.py          # Unified CLI tool
│   └── run.py                        # Dependency checker & universal runner
├── examples/
│   ├── annotate_over_image.py        # Image callout & arrow markup
│   ├── dsa_binary_search_steps.py    # Multi-page binary search slide deck
│   ├── dsa_tree_visualizer.py        # Binary search tree node & edge traversal
│   └── draw_3d_prism.py              # Isometric 3D triangular & rectangular prisms
├── references/
│   ├── COORDINATE_MATH.md            # Projection math, Bézier curves, PDF points
│   └── COLOR_PALETTES.md             # Semantic color palettes & visual hierarchy
└── tests/
    └── test_pdf_annotator.py         # Automated test suite (100% pass)
```

---

## 3. Python API Quick Reference

### 3.1 Initializing Canvas
```python
from pdf_annotator_engine import PDFCanvas, PALETTE

# Open existing document
canvas = PDFCanvas.open("existing_document.pdf", page_index=0)

# Or create a fresh canvas
canvas = PDFCanvas.create(width=612, height=792)
```

### 3.2 Vector Primitives & Annotations
```python
# 1. Straight vector arrow
canvas.draw_arrow(
    start=(100, 100),
    end=(250, 100),
    color=PALETTE["danger"],
    width=2.0,
    head_len=12,
    head_width=6
)

# 2. Quadratic curved arrow
canvas.draw_curved_arrow(
    start=(100, 200),
    control=(180, 260),
    end=(250, 200),
    color=PALETTE["primary"],
    width=2.0
)

# 3. Translucent highlight box
canvas.draw_highlight(
    rect=(150, 120, 300, 240),
    fill_color=PALETTE["highlight_yellow"],
    opacity=0.35,
    border_color=PALETTE["warning"]
)

# 4. Informational callout card with pointer
canvas.draw_callout(
    box_rect=(320, 80, 480, 140),
    text="Anomaly Peak\nZ-Score: 4.8\nStatus: Flagged",
    target_point=(250, 180),
    border_color=PALETTE["danger"]
)

canvas.save("output.pdf")
```

---

## 4. Workflows & Runbooks

### Workflow 1: Drawing Directly Over an Image in a PDF
When annotating an image (charts, scans, medical imaging, architectural diagrams):
1. Load PDF using `PDFCanvas.open(pdf_path, page_index)`.
2. Inspect image locations using `canvas.get_image_rects()`.
3. Compute coordinates relative to the target image bounding box.
4. Draw vector shapes (arrows, highlights, badges) on top of the image.
5. Save the modified PDF.

```python
from pdf_annotator_engine import PDFCanvas, PALETTE
import pymupdf

canvas = PDFCanvas.open("document.pdf", page_index=0)
img_rects = canvas.get_image_rects()

if img_rects:
    img_bbox = img_rects[0]
    # Highlight a sub-region inside the image (e.g. top right quadrant)
    target_area = pymupdf.Rect(
        img_bbox.x0 + (img_bbox.width * 0.6),
        img_bbox.y0 + (img_bbox.height * 0.1),
        img_bbox.x1,
        img_bbox.y0 + (img_bbox.height * 0.5)
    )
    canvas.draw_highlight(target_area, opacity=0.3)
    
    # Point an arrow at it from outside the image
    canvas.draw_arrow(
        start=(img_bbox.x1 + 60, target_area.y0 + 20),
        end=(target_area.x1 - 10, target_area.y0 + 20),
        color=PALETTE["danger"],
        width=2.5
    )

canvas.save("annotated_document.pdf")
```

---

### Workflow 2: Step-by-Step DSA Algorithm Visualizer
To generate a slide-deck style multi-page PDF demonstrating an algorithm:
1. Define discrete execution steps with data state, active pointers, and explanations.
2. Use `DSAVisualizer.create_algorithm_slide_deck()`.

```python
from pdf_annotator_engine import DSAVisualizer

steps = [
    {
        "description": "Step 1: Check mid element (val = 16). 16 < 23 -> Discard left half.",
        "array": [2, 5, 8, 12, 16, 23, 38, 56, 72, 91],
        "active": list(range(10)),
        "compared": [4],
        "pointers": {"low": 0, "mid": 4, "high": 9},
        "note": "Eliminating interval [0..4]."
    },
    {
        "description": "Step 2: Check mid element (val = 56). 56 > 23 -> Discard right half.",
        "array": [2, 5, 8, 12, 16, 23, 38, 56, 72, 91],
        "active": [5, 6, 7, 8, 9],
        "compared": [7],
        "pointers": {"low": 5, "mid": 7, "high": 9},
        "note": "Search narrowed to [5..6]."
    },
    {
        "description": "Step 3: Mid element = 23 == Target -> FOUND at index 5!",
        "array": [2, 5, 8, 12, 16, 23, 38, 56, 72, 91],
        "active": [5, 6],
        "sorted": [5],
        "pointers": {"low": 5, "mid": 5, "high": 6},
        "note": "Search complete in O(log N) time."
    }
]

DSAVisualizer.create_algorithm_slide_deck(
    output_pdf="binary_search_walkthrough.pdf",
    title="Binary Search Trace",
    steps=steps
)
```

---

### Workflow 3: Drawing 3D Prisms & Polyhedra
To render a 3D prism with shaded faces and dashed hidden lines:
```python
from pdf_annotator_engine import PDFCanvas, Geometry3D, PALETTE

canvas = PDFCanvas.create(width=700, height=700)

# Triangular Prism
Geometry3D.draw_triangular_prism(
    canvas=canvas,
    cx=350,
    cy=450,
    side=150,
    height=200,
    primary_color=PALETTE["primary"],
    fill_opacity=0.45,
    dashed_hidden=True,
    label_vertices=True,
    show_dimensions=True
)

canvas.save("triangular_prism.pdf")
```

---

## 5. Command-Line Interface (CLI)

The skill includes a unified CLI (`pdf_annotator_cli.py`):

```bash
# 1. Draw an arrow on page 0 of input.pdf
python3 scripts/pdf_annotator_cli.py arrow \
  -i input.pdf -o output.pdf --start 100 150 --end 300 150 --color "#e02424"

# 2. Draw a highlight box
python3 scripts/pdf_annotator_cli.py highlight \
  -i input.pdf -o output.pdf --rect 80 120 260 200 --opacity 0.4

# 3. Draw a callout pointing to a target
python3 scripts/pdf_annotator_cli.py callout \
  -i input.pdf -o output.pdf --box 350 80 500 140 --target 250 180 -t "Key Insight"

# 4. Render a 3D triangular prism
python3 scripts/pdf_annotator_cli.py prism \
  --type triangular -o prism.pdf --cx 300 --cy 380 --side 140 --height 180

# 5. Generate a complete DSA algorithm walkthrough deck
python3 scripts/pdf_annotator_cli.py dsa-demo \
  --algorithm binary-search -o binary_search_deck.pdf
```

---

## 6. Verification & Automated Testing

Run the automated test suite directly via Python's built-in `unittest`:

```bash
python3 -m unittest tests/test_pdf_annotator.py
```

All 8 tests verify:
- Vector primitive stroke & fill rendering
- Image detection and overlay fidelity
- 3D isometric vertex projections and dashed line styling
- Multi-page algorithm sequence generation
- CLI subcommand execution and return codes
