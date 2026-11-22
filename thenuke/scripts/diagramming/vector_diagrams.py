"""Native Vector Technical Diagrams for thenuke Reference Manuals.

Constructs publication-grade vector diagrams using ReportLab Drawing primitives:
- Rect, String, Line, Group, Polygon, PolyLine, Circle
- Strictly adheres to the monochrome palette:
    #000000 (black), #222222 (charcoal), #444444 (dark grey), #666666 (muted),
    #CCCCCC (hairline), #EFEFEF (code bg), #F8F8F8 (card bg), #FFFFFF (white).
- Exact 475 pt printable width to fit ISO A4 margins without overflow.
- All diagrams are pure vector math (0% rasterization, infinite DPI resolution).
"""

from __future__ import annotations

import math
from typing import List, Optional, Tuple
from reportlab.graphics.shapes import (
    Drawing,
    Group,
    Line,
    Polygon,
    Rect,
    Circle,
    String,
)
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics

# ---------------------------------------------------------------------------
# Strict Monochrome Palette Tokens
# ---------------------------------------------------------------------------
COLOR_BLACK = colors.HexColor("#000000")
COLOR_CHARCOAL = colors.HexColor("#222222")
COLOR_DARK_GREY = colors.HexColor("#444444")
COLOR_MUTED = colors.HexColor("#666666")
COLOR_HAIRLINE = colors.HexColor("#CCCCCC")
COLOR_BG_LIGHT = colors.HexColor("#F8F8F8")
COLOR_BG_BOX = colors.HexColor("#FFFFFF")
COLOR_BG_SHADED = colors.HexColor("#EFEFEF")
COLOR_WHITE = colors.HexColor("#FFFFFF")

TOTAL_WIDTH = 475.0


def _draw_arrow(
    g: Group,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    color=COLOR_CHARCOAL,
    stroke_width: float = 1.0,
    head_len: float = 6.0,
    head_width: float = 4.0,
) -> None:
    """Draw a vector line with a sharp triangular arrowhead at (x2, y2)."""
    g.add(Line(x1, y1, x2, y2, strokeColor=color, strokeWidth=stroke_width))
    angle = math.atan2(y2 - y1, x2 - x1)
    # Arrowhead vertices
    x_tip = x2
    y_tip = y2
    x_left = x2 - head_len * math.cos(angle) + head_width * math.sin(angle)
    y_left = y2 - head_len * math.sin(angle) - head_width * math.cos(angle)
    x_right = x2 - head_len * math.cos(angle) - head_width * math.sin(angle)
    y_right = y2 - head_len * math.sin(angle) + head_width * math.cos(angle)

    g.add(
        Polygon(
            [x_tip, y_tip, x_left, y_left, x_right, y_right],
            fillColor=color,
            strokeColor=color,
            strokeWidth=0.5,
        )
    )


def _draw_dashed_line(
    g: Group,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    color=COLOR_HAIRLINE,
    stroke_width: float = 0.75,
    dash_len: float = 4.0,
    gap_len: float = 3.0,
) -> None:
    """Draw a dashed line segment."""
    total_dist = math.hypot(x2 - x1, y2 - y1)
    if total_dist == 0:
        return
    dx = (x2 - x1) / total_dist
    dy = (y2 - y1) / total_dist

    curr = 0.0
    while curr < total_dist:
        seg_end = min(curr + dash_len, total_dist)
        sx = x1 + dx * curr
        sy = y1 + dy * curr
        ex = x1 + dx * seg_end
        ey = y1 + dy * seg_end
        g.add(Line(sx, sy, ex, ey, strokeColor=color, strokeWidth=stroke_width))
        curr += dash_len + gap_len


def _make_canvas_frame(height: float, title: str, subtitle: str = "") -> Tuple[Drawing, Group]:
    """Creates a framed container for a technical vector diagram."""
    d = Drawing(TOTAL_WIDTH, height)
    # Outer container box
    d.add(
        Rect(
            0,
            0,
            TOTAL_WIDTH,
            height,
            fillColor=COLOR_BG_LIGHT,
            strokeColor=COLOR_HAIRLINE,
            strokeWidth=0.75,
            rx=3,
            ry=3,
        )
    )
    # Header strip
    d.add(
        Rect(
            0,
            height - 22,
            TOTAL_WIDTH,
            22,
            fillColor=COLOR_BG_SHADED,
            strokeColor=COLOR_HAIRLINE,
            strokeWidth=0.75,
        )
    )
    # Header title
    clean_title = title.upper()
    d.add(
        String(
            10,
            height - 15,
            clean_title,
            fontName="Helvetica-Bold",
            fontSize=8.5,
            fillColor=COLOR_BLACK,
        )
    )
    if subtitle:
        title_w = pdfmetrics.stringWidth(clean_title, "Helvetica-Bold", 8.5)
        sub_w = pdfmetrics.stringWidth(subtitle, "Helvetica-Oblique", 7.5)
        # Guarantee minimum 20 pt gutter between title and subtitle
        if title_w + sub_w + 30.0 > TOTAL_WIDTH:
            avail_w = TOTAL_WIDTH - title_w - 35.0
            if avail_w < 60:
                subtitle = ""
            else:
                while subtitle and pdfmetrics.stringWidth(subtitle + "...", "Helvetica-Oblique", 7.5) > avail_w:
                    subtitle = subtitle[:-1]
                if subtitle:
                    subtitle = subtitle.rstrip() + "..."
        if subtitle:
            d.add(
                String(
                    TOTAL_WIDTH - 10,
                    height - 15,
                    subtitle,
                    fontName="Helvetica-Oblique",
                    fontSize=7.5,
                    fillColor=COLOR_MUTED,
                    textAnchor="end",
                )
            )

    g = Group()
    d.add(g)
    return d, g


# ---------------------------------------------------------------------------
# 1. Git Object Model & Storage Graph Diagram
# ---------------------------------------------------------------------------
def create_object_model_diagram() -> Drawing:
    """Renders the Git Content-Addressable Object Storage Graph.
    Shows Commit -> Tree -> Blob / Subtree hierarchy with SHA-1 pointers.
    """
    height = 165.0
    d, g = _make_canvas_frame(
        height,
        "Figure 1.1: Git Object Model & Content-Addressable Storage Graph",
        "DAG Hierarchy: Commit ➔ Tree ➔ Blob",
    )

    # 1. Commit Object Box (Left)
    g.add(Rect(15, 75, 125, 60, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.0))
    g.add(String(20, 122, "COMMIT OBJECT", fontName="Helvetica-Bold", fontSize=8.0, fillColor=COLOR_BLACK))
    g.add(Line(15, 116, 140, 116, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(String(20, 105, "hash: 8f3a9d (SHA-1)", fontName="Courier-Bold", fontSize=7.0, fillColor=COLOR_CHARCOAL))
    g.add(String(20, 94, "tree: 4b825d ➔", fontName="Courier", fontSize=7.0, fillColor=COLOR_MUTED))
    g.add(String(20, 83, "author: Linus Torvalds", fontName="Helvetica", fontSize=6.5, fillColor=COLOR_MUTED))

    # 2. Root Tree Object Box (Center)
    g.add(Rect(175, 55, 130, 80, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.0))
    g.add(String(180, 122, "ROOT TREE (DIR)", fontName="Helvetica-Bold", fontSize=8.0, fillColor=COLOR_BLACK))
    g.add(Line(175, 116, 305, 116, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(String(180, 105, "hash: 4b825d", fontName="Courier-Bold", fontSize=7.0, fillColor=COLOR_CHARCOAL))
    g.add(String(180, 93, "100644 blob a1f2 (main.c)", fontName="Courier", fontSize=6.5, fillColor=COLOR_MUTED))
    g.add(String(180, 81, "100644 blob c3e4 (README)", fontName="Courier", fontSize=6.5, fillColor=COLOR_MUTED))
    g.add(String(180, 69, "040000 tree d5a6 (src/) ➔", fontName="Courier", fontSize=6.5, fillColor=COLOR_MUTED))

    # 3. Blobs & Subtree (Right Column)
    # Blob 1
    g.add(Rect(340, 102, 120, 33, fillColor=COLOR_BG_BOX, strokeColor=COLOR_DARK_GREY, strokeWidth=0.75))
    g.add(String(345, 124, "BLOB: main.c", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK))
    g.add(String(345, 111, "hash: a1f2 (zlib data)", fontName="Courier", fontSize=6.5, fillColor=COLOR_MUTED))

    # Blob 2
    g.add(Rect(340, 62, 120, 33, fillColor=COLOR_BG_BOX, strokeColor=COLOR_DARK_GREY, strokeWidth=0.75))
    g.add(String(345, 84, "BLOB: README.md", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK))
    g.add(String(345, 71, "hash: c3e4 (zlib text)", fontName="Courier", fontSize=6.5, fillColor=COLOR_MUTED))

    # Subtree 3
    g.add(Rect(340, 20, 120, 35, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.0))
    g.add(String(345, 43, "SUBTREE: src/", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK))
    g.add(String(345, 30, "hash: d5a6 ➔ util.c", fontName="Courier", fontSize=6.5, fillColor=COLOR_MUTED))

    # Connecting Arrows
    _draw_arrow(g, 140, 95, 175, 95, color=COLOR_BLACK, stroke_width=1.2)
    _draw_arrow(g, 305, 95, 340, 118, color=COLOR_CHARCOAL, stroke_width=1.0)
    _draw_arrow(g, 305, 85, 340, 78, color=COLOR_CHARCOAL, stroke_width=1.0)
    _draw_arrow(g, 305, 70, 340, 38, color=COLOR_CHARCOAL, stroke_width=1.0)

    # Invariant Tag at Bottom
    g.add(Rect(15, 15, 300, 22, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(
        String(
            22,
            22,
            "INVARIANT: Blobs store pure data; Trees store filenames + permissions + hashes.",
            fontName="Helvetica-Bold",
            fontSize=7.0,
            fillColor=COLOR_BLACK,
        )
    )

    return d


# ---------------------------------------------------------------------------
# 2. Three Trees Architecture Diagram
# ---------------------------------------------------------------------------
def create_three_trees_diagram() -> Drawing:
    """Renders the Three Trees Architecture: Working Tree, Index, HEAD Repository."""
    height = 170.0
    d, g = _make_canvas_frame(
        height,
        "Figure 3.1: The Three Trees Architecture & Transition Lifecycle",
        "Working Tree ➔ Index / Staging ➔ HEAD Repository",
    )

    col_w = 125.0
    col_h = 95.0
    y_col = 35.0

    # Column 1: Working Tree
    g.add(Rect(15, y_col, col_w, col_h, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.0))
    g.add(String(22, y_col + col_h - 14, "WORKING TREE", fontName="Helvetica-Bold", fontSize=8.5, fillColor=COLOR_BLACK))
    g.add(String(22, y_col + col_h - 25, "Filesystem / Sandboxed", fontName="Helvetica-Oblique", fontSize=7.0, fillColor=COLOR_MUTED))
    g.add(Line(15, y_col + col_h - 30, 15 + col_w, y_col + col_h - 30, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(String(22, y_col + 50, "• Active file modifications", fontName="Helvetica", fontSize=7.0, fillColor=COLOR_CHARCOAL))
    g.add(String(22, y_col + 38, "• Untracked & dirty files", fontName="Helvetica", fontSize=7.0, fillColor=COLOR_CHARCOAL))
    g.add(String(22, y_col + 24, "• Real OS disk files", fontName="Helvetica", fontSize=7.0, fillColor=COLOR_CHARCOAL))
    g.add(String(22, y_col + 10, "state: DIRTY / MODIFIED", fontName="Courier-Bold", fontSize=6.5, fillColor=COLOR_DARK_GREY))

    # Column 2: Staging Index
    g.add(Rect(175, y_col, col_w, col_h, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.0))
    g.add(String(182, y_col + col_h - 14, "STAGING INDEX", fontName="Helvetica-Bold", fontSize=8.5, fillColor=COLOR_BLACK))
    g.add(String(182, y_col + col_h - 25, ".git/index (Binary Cache)", fontName="Helvetica-Oblique", fontSize=7.0, fillColor=COLOR_MUTED))
    g.add(Line(175, y_col + col_h - 30, 175 + col_w, y_col + col_h - 30, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(String(182, y_col + 50, "• Next commit payload", fontName="Helvetica", fontSize=7.0, fillColor=COLOR_CHARCOAL))
    g.add(String(182, y_col + 38, "• stat cache + SHA-1 hash", fontName="Helvetica", fontSize=7.0, fillColor=COLOR_CHARCOAL))
    g.add(String(182, y_col + 24, "• Stage resolution matrix", fontName="Helvetica", fontSize=7.0, fillColor=COLOR_CHARCOAL))
    g.add(String(182, y_col + 10, "state: STAGED CACHE", fontName="Courier-Bold", fontSize=6.5, fillColor=COLOR_DARK_GREY))

    # Column 3: HEAD Repository
    g.add(Rect(335, y_col, col_w, col_h, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.0))
    g.add(String(342, y_col + col_h - 14, "HEAD REPOSITORY", fontName="Helvetica-Bold", fontSize=8.5, fillColor=COLOR_BLACK))
    g.add(String(342, y_col + col_h - 25, "Immutable Commit DAG", fontName="Helvetica-Oblique", fontSize=7.0, fillColor=COLOR_MUTED))
    g.add(Line(335, y_col + col_h - 30, 335 + col_w, y_col + col_h - 30, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(String(342, y_col + 50, "• Cryptographic snapshots", fontName="Helvetica", fontSize=7.0, fillColor=COLOR_CHARCOAL))
    g.add(String(342, y_col + 38, "• Permanent commit chain", fontName="Helvetica", fontSize=7.0, fillColor=COLOR_CHARCOAL))
    g.add(String(342, y_col + 24, "• Pointer: refs/heads/...", fontName="Helvetica", fontSize=7.0, fillColor=COLOR_CHARCOAL))
    g.add(String(342, y_col + 10, "state: COMMITTED (IMMUTABLE)", fontName="Courier-Bold", fontSize=6.5, fillColor=COLOR_DARK_GREY))

    # Transition Arrows
    # 1. git add (Working Tree -> Index)
    _draw_arrow(g, 140, y_col + 65, 175, y_col + 65, color=COLOR_BLACK, stroke_width=1.2)
    g.add(String(144, y_col + 70, "git add", fontName="Courier-Bold", fontSize=7.0, fillColor=COLOR_BLACK))

    # 2. git commit (Index -> HEAD)
    _draw_arrow(g, 300, y_col + 65, 335, y_col + 65, color=COLOR_BLACK, stroke_width=1.2)
    g.add(String(302, y_col + 70, "git commit", fontName="Courier-Bold", fontSize=7.0, fillColor=COLOR_BLACK))

    # 3. git restore --staged (Index -> Working Tree or unstage)
    _draw_arrow(g, 175, y_col + 40, 140, y_col + 40, color=COLOR_MUTED, stroke_width=0.75)
    g.add(String(142, y_col + 32, "git restore", fontName="Courier", fontSize=6.5, fillColor=COLOR_MUTED))

    # 4. git reset --soft (HEAD -> Index)
    _draw_arrow(g, 335, y_col + 40, 300, y_col + 40, color=COLOR_MUTED, stroke_width=0.75)
    g.add(String(302, y_col + 32, "git reset", fontName="Courier", fontSize=6.5, fillColor=COLOR_MUTED))

    # Bottom summary legend
    g.add(
        String(
            15,
            16,
            "LIFECYCLE PIPELINE: git add copies disk bytes to object store + updates index; git commit creates immutable tree + commit object.",
            fontName="Helvetica-Bold",
            fontSize=7.0,
            fillColor=COLOR_BLACK,
        )
    )

    return d


# ---------------------------------------------------------------------------
# 3. Branching & Commit DAG Topology Diagram
# ---------------------------------------------------------------------------
def create_branching_dag_diagram() -> Drawing:
    """Renders Branching Pointers, Divergent Commit DAG, and HEAD attachment."""
    height = 155.0
    d, g = _make_canvas_frame(
        height,
        "Figure 6.1: Git Commit Directed Acyclic Graph (DAG) & Branch References",
        "Pointers, HEAD Symref & Divergence Mechanics",
    )

    y_main = 85.0
    y_feature = 40.0

    # Main commit nodes
    # C0
    g.add(Rect(25, y_main - 12, 45, 24, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.0, rx=2, ry=2))
    g.add(String(37, y_main - 4, "C0", fontName="Helvetica-Bold", fontSize=9.0, fillColor=COLOR_BLACK))

    # C1
    g.add(Rect(110, y_main - 12, 45, 24, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.0, rx=2, ry=2))
    g.add(String(122, y_main - 4, "C1", fontName="Helvetica-Bold", fontSize=9.0, fillColor=COLOR_BLACK))

    # C2 (Branch point)
    g.add(Rect(195, y_main - 12, 45, 24, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.0, rx=2, ry=2))
    g.add(String(207, y_main - 4, "C2", fontName="Helvetica-Bold", fontSize=9.0, fillColor=COLOR_BLACK))

    # C3 (main tip)
    g.add(Rect(290, y_main - 12, 45, 24, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.0, rx=2, ry=2))
    g.add(String(302, y_main - 4, "C3", fontName="Helvetica-Bold", fontSize=9.0, fillColor=COLOR_BLACK))

    # Feature branch commits (branching from C2)
    # C4
    g.add(Rect(260, y_feature - 12, 45, 24, fillColor=COLOR_BG_BOX, strokeColor=COLOR_DARK_GREY, strokeWidth=1.0, rx=2, ry=2))
    g.add(String(272, y_feature - 4, "C4", fontName="Helvetica-Bold", fontSize=9.0, fillColor=COLOR_BLACK))

    # C5 (feature tip)
    g.add(Rect(350, y_feature - 12, 45, 24, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.2, rx=2, ry=2))
    g.add(String(362, y_feature - 4, "C5", fontName="Helvetica-Bold", fontSize=9.0, fillColor=COLOR_BLACK))

    # Commit DAG Parent Arrows (Child points backwards to Parent!)
    _draw_arrow(g, 110, y_main, 70, y_main, color=COLOR_CHARCOAL, stroke_width=1.0)
    _draw_arrow(g, 195, y_main, 155, y_main, color=COLOR_CHARCOAL, stroke_width=1.0)
    _draw_arrow(g, 290, y_main, 240, y_main, color=COLOR_CHARCOAL, stroke_width=1.0)

    # Feature branch arrows
    _draw_arrow(g, 260, y_feature, 225, y_main - 12, color=COLOR_CHARCOAL, stroke_width=1.0)
    _draw_arrow(g, 350, y_feature, 305, y_feature, color=COLOR_CHARCOAL, stroke_width=1.0)

    # Branch Pointer Labels (Refs)
    # 'main' pointer -> C3
    g.add(Rect(290, y_main + 20, 52, 18, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_BLACK, strokeWidth=0.75))
    g.add(String(296, y_main + 25, "refs: main", fontName="Courier-Bold", fontSize=6.5, fillColor=COLOR_BLACK))
    _draw_arrow(g, 312, y_main + 20, 312, y_main + 12, color=COLOR_BLACK, stroke_width=0.75)

    # 'feature' pointer -> C5
    g.add(Rect(350, y_feature + 20, 60, 18, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_BLACK, strokeWidth=0.75))
    g.add(String(355, y_feature + 25, "refs: feature", fontName="Courier-Bold", fontSize=6.5, fillColor=COLOR_BLACK))
    _draw_arrow(g, 372, y_feature + 20, 372, y_feature + 12, color=COLOR_BLACK, stroke_width=0.75)

    # Active HEAD pointer -> refs: feature
    g.add(Rect(415, y_feature + 18, 50, 22, fillColor=COLOR_BLACK, strokeColor=COLOR_BLACK, strokeWidth=1.0))
    g.add(String(423, y_feature + 25, "HEAD ➔", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_WHITE))
    _draw_arrow(g, 415, y_feature + 29, 410, y_feature + 29, color=COLOR_BLACK, stroke_width=1.0)

    # Explanation text
    g.add(
        String(
            15,
            15,
            "TOPOLOGY RULE: Commits are immutable DAG nodes storing SHA-1 parent hashes. Branches are mutable 41-byte text files holding a SHA-1 pointer.",
            fontName="Helvetica-Bold",
            fontSize=6.5,
            fillColor=COLOR_BLACK,
        )
    )

    return d


# ---------------------------------------------------------------------------
# 4. 3-Way Merge & Lowest Common Ancestor (LCA) Diagram
# ---------------------------------------------------------------------------
def create_three_way_merge_diagram() -> Drawing:
    """Renders 3-Way Merge, Lowest Common Ancestor base resolution, and Merge Commit."""
    height = 160.0
    d, g = _make_canvas_frame(
        height,
        "Figure 7.1: Recursive 3-Way Merge & Lowest Common Ancestor (LCA)",
        "Base Commit B ➔ Ours O + Theirs T ➔ Merge Commit M",
    )

    y_top = 100.0
    y_mid = 70.0
    y_bot = 40.0

    # Base Ancestor B (LCA)
    g.add(Rect(30, y_mid - 14, 55, 28, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.2, rx=2, ry=2))
    g.add(String(40, y_mid - 2, "BASE (B)", fontName="Helvetica-Bold", fontSize=8.0, fillColor=COLOR_BLACK))
    g.add(String(38, y_mid - 11, "LCA Commit", fontName="Helvetica-Oblique", fontSize=6.0, fillColor=COLOR_MUTED))

    # Branch A (Ours / HEAD / main)
    g.add(Rect(160, y_top - 14, 60, 28, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.0, rx=2, ry=2))
    g.add(String(168, y_top - 2, "OURS (C2)", fontName="Helvetica-Bold", fontSize=8.0, fillColor=COLOR_BLACK))
    g.add(String(166, y_top - 11, "HEAD branch", fontName="Helvetica-Oblique", fontSize=6.0, fillColor=COLOR_MUTED))

    # Branch B (Theirs / feature)
    g.add(Rect(160, y_bot - 14, 60, 28, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.0, rx=2, ry=2))
    g.add(String(166, y_bot - 2, "THEIRS (C3)", fontName="Helvetica-Bold", fontSize=8.0, fillColor=COLOR_BLACK))
    g.add(String(165, y_bot - 11, "merged branch", fontName="Helvetica-Oblique", fontSize=6.0, fillColor=COLOR_MUTED))

    # Merge Commit M (Two Parents!)
    g.add(Rect(305, y_mid - 16, 75, 32, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.5, rx=3, ry=3))
    g.add(String(312, y_mid + 2, "MERGE (M)", fontName="Helvetica-Bold", fontSize=8.5, fillColor=COLOR_BLACK))
    g.add(String(312, y_mid - 7, "parent1: C2", fontName="Courier-Bold", fontSize=6.5, fillColor=COLOR_CHARCOAL))
    g.add(String(312, y_mid - 15, "parent2: C3", fontName="Courier-Bold", fontSize=6.5, fillColor=COLOR_CHARCOAL))

    # DAG Links
    # Ours -> Base
    _draw_arrow(g, 160, y_top, 85, y_mid + 7, color=COLOR_CHARCOAL, stroke_width=1.0)
    # Theirs -> Base
    _draw_arrow(g, 160, y_bot, 85, y_mid - 7, color=COLOR_CHARCOAL, stroke_width=1.0)
    # Merge M -> Ours (Parent 1)
    _draw_arrow(g, 305, y_mid + 5, 220, y_top, color=COLOR_BLACK, stroke_width=1.2)
    # Merge M -> Theirs (Parent 2)
    _draw_arrow(g, 305, y_mid - 5, 220, y_bot, color=COLOR_BLACK, stroke_width=1.2)

    # 3-Way Merge Delta Formula Box (Right)
    g.add(Rect(390, 30, 75, 95, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(String(395, 112, "3-WAY FORMULA:", fontName="Helvetica-Bold", fontSize=6.5, fillColor=COLOR_BLACK))
    g.add(String(395, 98, "ΔO = Ours - Base", fontName="Courier", fontSize=6.0, fillColor=COLOR_CHARCOAL))
    g.add(String(395, 85, "ΔT = Theirs - Base", fontName="Courier", fontSize=6.0, fillColor=COLOR_CHARCOAL))
    g.add(String(395, 68, "If ΔO ≠ ΔT on", fontName="Helvetica", fontSize=6.0, fillColor=COLOR_MUTED))
    g.add(String(395, 58, "same line chunk:", fontName="Helvetica", fontSize=6.0, fillColor=COLOR_MUTED))
    g.add(String(395, 42, "CONFLICT!", fontName="Helvetica-Bold", fontSize=7.0, fillColor=COLOR_BLACK))

    # Bottom summary
    g.add(
        String(
            15,
            14,
            "RESOLVER: Git computes git merge-base to find Base B, then computes Myers diff deltas Δ(B➔Ours) and Δ(B➔Theirs).",
            fontName="Helvetica-Bold",
            fontSize=6.5,
            fillColor=COLOR_BLACK,
        )
    )

    return d


# ---------------------------------------------------------------------------
# 5. Git Rebase Linear Replay Diagram
# ---------------------------------------------------------------------------
def create_rebase_replay_diagram() -> Drawing:
    """Renders Linear Commit Replay during git rebase."""
    height = 155.0
    d, g = _make_canvas_frame(
        height,
        "Figure 8.1: Git Rebase Mechanics — Detached Commit Replay",
        "Original Divergent Commits ➔ Sequential Patch Replay onto Upstream",
    )

    # 1. Before Rebase (Left Half)
    g.add(Rect(10, 25, 220, 105, fillColor=COLOR_BG_BOX, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(String(18, 118, "BEFORE REBASE (Divergent DAG)", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK))

    # Base C1
    g.add(Rect(20, 70, 32, 20, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_BLACK, strokeWidth=0.75))
    g.add(String(30, 76, "C1", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK))

    # Main C2
    g.add(Rect(75, 88, 35, 20, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_BLACK, strokeWidth=0.75))
    g.add(String(85, 94, "C2", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK))
    g.add(String(75, 110, "main", fontName="Courier-Bold", fontSize=6.5, fillColor=COLOR_MUTED))

    # Feature C3, C4
    g.add(Rect(75, 48, 32, 20, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_DARK_GREY, strokeWidth=0.75))
    g.add(String(85, 54, "C3", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK))

    g.add(Rect(130, 48, 32, 20, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_DARK_GREY, strokeWidth=0.75))
    g.add(String(140, 54, "C4", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK))
    g.add(String(130, 36, "feature", fontName="Courier-Bold", fontSize=6.5, fillColor=COLOR_MUTED))

    # Links before
    _draw_arrow(g, 75, 98, 52, 80, color=COLOR_CHARCOAL, stroke_width=0.75)
    _draw_arrow(g, 75, 58, 52, 80, color=COLOR_CHARCOAL, stroke_width=0.75)
    _draw_arrow(g, 130, 58, 107, 58, color=COLOR_CHARCOAL, stroke_width=0.75)

    # Center transition symbol
    g.add(String(235, 75, "➔", fontName="Helvetica-Bold", fontSize=14.0, fillColor=COLOR_BLACK))

    # 2. After Rebase (Right Half)
    g.add(Rect(255, 25, 210, 105, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=0.75))
    g.add(String(263, 118, "AFTER REBASE (Linear DAG)", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK))

    # Linear sequence: C1 -> C2 -> C3' -> C4'
    g.add(Rect(265, 62, 30, 22, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_BLACK, strokeWidth=0.75))
    g.add(String(273, 69, "C1", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK))

    g.add(Rect(312, 62, 30, 22, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_BLACK, strokeWidth=0.75))
    g.add(String(320, 69, "C2", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK))
    g.add(String(312, 88, "main", fontName="Courier-Bold", fontSize=6.5, fillColor=COLOR_MUTED))

    g.add(Rect(360, 62, 32, 22, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.0))
    g.add(String(368, 69, "C3'", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK))

    g.add(Rect(410, 62, 32, 22, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.2))
    g.add(String(418, 69, "C4'", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK))
    g.add(String(405, 88, "feature (HEAD)", fontName="Courier-Bold", fontSize=6.0, fillColor=COLOR_BLACK))

    # Linear Links
    _draw_arrow(g, 312, 73, 295, 73, color=COLOR_CHARCOAL, stroke_width=0.75)
    _draw_arrow(g, 360, 73, 342, 73, color=COLOR_BLACK, stroke_width=1.0)
    _draw_arrow(g, 410, 73, 392, 73, color=COLOR_BLACK, stroke_width=1.0)

    # Bottom summary
    g.add(
        String(
            15,
            12,
            "INVARIANT: git rebase creates NEW commits (C3', C4') with brand-new SHA-1 hashes; original commits (C3, C4) become unreachable orphans.",
            fontName="Helvetica-Bold",
            fontSize=6.5,
            fillColor=COLOR_BLACK,
        )
    )

    return d


# ---------------------------------------------------------------------------
# 6. Remote Tracking & Synchronization Pipeline Diagram
# ---------------------------------------------------------------------------
def create_remote_sync_diagram() -> Drawing:
    """Renders the 4-Stage Distributed Synchronization Pipeline."""
    height = 150.0
    d, g = _make_canvas_frame(
        height,
        "Figure 9.1: Distributed Remote Synchronization Pipeline",
        "Local Repositories ➔ Tracking Refs ➔ Remote Upstream",
    )

    y_pos = 42.0
    box_w = 95.0
    box_h = 75.0

    # 1. Local Working / Index
    g.add(Rect(15, y_pos, box_w, box_h, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.0))
    g.add(String(22, y_pos + box_h - 14, "WORKING / INDEX", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK))
    g.add(Line(15, y_pos + box_h - 20, 15 + box_w, y_pos + box_h - 20, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(String(22, y_pos + 38, "Local sandbox", fontName="Helvetica", fontSize=6.5, fillColor=COLOR_MUTED))
    g.add(String(22, y_pos + 26, "Dirty files / staged", fontName="Helvetica", fontSize=6.5, fillColor=COLOR_MUTED))
    g.add(String(22, y_pos + 12, "state: UNCOMMITTED", fontName="Courier-Bold", fontSize=6.0, fillColor=COLOR_CHARCOAL))

    # 2. Local HEAD branch
    g.add(Rect(130, y_pos, box_w, box_h, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.0))
    g.add(String(137, y_pos + box_h - 14, "LOCAL BRANCH", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK))
    g.add(Line(130, y_pos + box_h - 20, 130 + box_w, y_pos + box_h - 20, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(String(137, y_pos + 38, "refs/heads/main", fontName="Courier-Bold", fontSize=6.5, fillColor=COLOR_CHARCOAL))
    g.add(String(137, y_pos + 26, "Local committed tip", fontName="Helvetica", fontSize=6.5, fillColor=COLOR_MUTED))
    g.add(String(137, y_pos + 12, "state: LOCAL COMMITS", fontName="Courier-Bold", fontSize=6.0, fillColor=COLOR_CHARCOAL))

    # 3. Remote Tracking Branch
    g.add(Rect(245, y_pos, box_w, box_h, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.0))
    g.add(String(250, y_pos + box_h - 14, "REMOTE-TRACKING", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK))
    g.add(Line(245, y_pos + box_h - 20, 245 + box_w, y_pos + box_h - 20, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(String(250, y_pos + 38, "origin/main", fontName="Courier-Bold", fontSize=6.5, fillColor=COLOR_CHARCOAL))
    g.add(String(250, y_pos + 26, "Read-only pointer", fontName="Helvetica", fontSize=6.5, fillColor=COLOR_MUTED))
    g.add(String(250, y_pos + 12, "state: LAST KNOWN", fontName="Courier-Bold", fontSize=6.0, fillColor=COLOR_CHARCOAL))

    # 4. Remote Server
    g.add(Rect(360, y_pos, box_w + 5, box_h, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.2))
    g.add(String(367, y_pos + box_h - 14, "REMOTE UPSTREAM", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK))
    g.add(Line(360, y_pos + box_h - 20, 360 + box_w + 5, y_pos + box_h - 20, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(String(367, y_pos + 38, "GitHub / GitLab", fontName="Helvetica-Bold", fontSize=6.5, fillColor=COLOR_CHARCOAL))
    g.add(String(367, y_pos + 26, "Bare repository", fontName="Helvetica", fontSize=6.5, fillColor=COLOR_MUTED))
    g.add(String(367, y_pos + 12, "state: CANONICAL", fontName="Courier-Bold", fontSize=6.0, fillColor=COLOR_BLACK))

    # Connecting Commands
    # Local commit -> Tracking: git push
    _draw_arrow(g, 225, y_pos + 52, 360, y_pos + 52, color=COLOR_BLACK, stroke_width=1.2)
    g.add(String(270, y_pos + 56, "git push", fontName="Courier-Bold", fontSize=7.0, fillColor=COLOR_BLACK))

    # Remote -> Remote tracking: git fetch
    _draw_arrow(g, 360, y_pos + 30, 340, y_pos + 30, color=COLOR_CHARCOAL, stroke_width=1.0)
    g.add(String(280, y_pos + 34, "git fetch", fontName="Courier-Bold", fontSize=7.0, fillColor=COLOR_CHARCOAL))

    # Remote tracking -> Local: git merge (git pull = fetch + merge)
    _draw_arrow(g, 245, y_pos + 18, 225, y_pos + 18, color=COLOR_CHARCOAL, stroke_width=1.0)
    g.add(String(160, y_pos + 8, "git merge (pull)", fontName="Courier-Bold", fontSize=6.5, fillColor=COLOR_MUTED))

    # Bottom summary
    g.add(
        String(
            15,
            14,
            "RULE: git fetch downloads packfiles and updates origin/main safely; git pull executes fetch + merge immediately.",
            fontName="Helvetica-Bold",
            fontSize=6.5,
            fillColor=COLOR_BLACK,
        )
    )

    return d


# ---------------------------------------------------------------------------
# 7. Reset vs Restore vs Revert Comparison Matrix
# ---------------------------------------------------------------------------
def create_reset_matrix_diagram() -> Drawing:
    """Renders Comparison Matrix of git reset --soft/--mixed/--hard vs restore."""
    height = 145.0
    d, g = _make_canvas_frame(
        height,
        "Figure 8.2: Git Reset Scope Matrix & Destructive Impact Table",
        "Target Tree Mutations Across Reset Modes",
    )

    y_start = 100.0
    row_h = 18.0

    # Header Row
    g.add(Rect(15, y_start, 445, row_h, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_BLACK, strokeWidth=0.75))
    g.add(String(22, y_start + 6, "COMMAND / MODE", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK))
    g.add(String(160, y_start + 6, "HEAD", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK))
    g.add(String(250, y_start + 6, "INDEX (STAGE)", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK))
    g.add(String(350, y_start + 6, "WORKING TREE", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK))

    rows = [
        ("git reset --soft HEAD~1", "MOVES", "PRESERVED", "PRESERVED (Safe)"),
        ("git reset --mixed HEAD~1 (Default)", "MOVES", "RESET (Unstaged)", "PRESERVED (Safe)"),
        ("git reset --hard HEAD~1", "MOVES", "RESET", "OVERWRITTEN (DESTRUCTIVE)"),
        ("git restore --staged <file>", "UNCHANGED", "UNSTAGED", "PRESERVED (Safe)"),
    ]

    for idx, (cmd, head_col, idx_col, work_col) in enumerate(rows):
        y = y_start - (idx + 1) * row_h
        bg = COLOR_BG_BOX if idx % 2 == 0 else COLOR_BG_LIGHT
        g.add(Rect(15, y, 445, row_h, fillColor=bg, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
        g.add(String(22, y + 5, cmd, fontName="Courier-Bold", fontSize=6.5, fillColor=COLOR_BLACK))
        g.add(String(160, y + 5, head_col, fontName="Helvetica", fontSize=7.0, fillColor=COLOR_CHARCOAL))
        g.add(String(250, y + 5, idx_col, fontName="Helvetica", fontSize=7.0, fillColor=COLOR_CHARCOAL))
        color_w = COLOR_BLACK if "DESTRUCTIVE" in work_col else COLOR_MUTED
        g.add(String(350, y + 5, work_col, fontName="Helvetica-Bold" if "DESTRUCTIVE" in work_col else "Helvetica", fontSize=6.5, fillColor=color_w))

    g.add(
        String(
            15,
            12,
            "RECOVERY: If you run git reset --hard by accident, recover lost commit objects immediately via git reflog.",
            fontName="Helvetica-Bold",
            fontSize=6.5,
            fillColor=COLOR_BLACK,
        )
    )

    return d


# ---------------------------------------------------------------------------
# 8. Git Index Binary Structure Diagram
# ---------------------------------------------------------------------------
def create_index_binary_diagram() -> Drawing:
    """Renders the internal binary anatomy of .git/index."""
    height = 145.0
    d, g = _make_canvas_frame(
        height,
        "Figure 2.1: Binary Anatomy of the .git/index Cache File",
        "Header ➔ Entry Table ➔ Extensions ➔ SHA-1 Checksum",
    )

    y_pos = 45.0
    # 1. 12-byte Header
    g.add(Rect(15, y_pos, 85, 65, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.0))
    g.add(String(20, y_pos + 52, "12-BYTE HEADER", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK))
    g.add(Line(15, y_pos + 46, 100, y_pos + 46, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(String(20, y_pos + 34, "4B: 'DIRC' (Magic)", fontName="Courier", fontSize=6.0, fillColor=COLOR_CHARCOAL))
    g.add(String(20, y_pos + 22, "4B: Version 2/3/4", fontName="Courier", fontSize=6.0, fillColor=COLOR_CHARCOAL))
    g.add(String(20, y_pos + 10, "4B: Entry Count", fontName="Courier", fontSize=6.0, fillColor=COLOR_CHARCOAL))

    # 2. Entry Table
    g.add(Rect(110, y_pos, 185, 65, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.0))
    g.add(String(118, y_pos + 52, "SORTED INDEX ENTRIES (Variable)", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK))
    g.add(Line(110, y_pos + 46, 295, y_pos + 46, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(String(118, y_pos + 34, "ctime / mtime / dev / ino / mode / uid / gid / file size", fontName="Courier", fontSize=5.5, fillColor=COLOR_CHARCOAL))
    g.add(String(118, y_pos + 22, "20-byte SHA-1 Object ID of target Blob", fontName="Courier-Bold", fontSize=6.0, fillColor=COLOR_BLACK))
    g.add(String(118, y_pos + 10, "Flags (16-bit) + Variable-length File Path string", fontName="Courier", fontSize=5.5, fillColor=COLOR_MUTED))

    # 3. Optional Extensions
    g.add(Rect(305, y_pos, 85, 65, fillColor=COLOR_BG_BOX, strokeColor=COLOR_DARK_GREY, strokeWidth=0.75))
    g.add(String(312, y_pos + 52, "EXTENSIONS", fontName="Helvetica-Bold", fontSize=7.0, fillColor=COLOR_BLACK))
    g.add(Line(305, y_pos + 46, 390, y_pos + 46, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(String(312, y_pos + 34, "'TREE' (Cache)", fontName="Courier", fontSize=6.0, fillColor=COLOR_CHARCOAL))
    g.add(String(312, y_pos + 22, "'REUC' (Resolve)", fontName="Courier", fontSize=6.0, fillColor=COLOR_CHARCOAL))
    g.add(String(312, y_pos + 10, "'UNTR' (Untracked)", fontName="Courier", fontSize=6.0, fillColor=COLOR_CHARCOAL))

    # 4. Checksum
    g.add(Rect(400, y_pos, 60, 65, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_BLACK, strokeWidth=1.0))
    g.add(String(405, y_pos + 52, "CHECKSUM", fontName="Helvetica-Bold", fontSize=6.5, fillColor=COLOR_BLACK))
    g.add(Line(400, y_pos + 46, 460, y_pos + 46, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(String(405, y_pos + 26, "20-byte", fontName="Courier-Bold", fontSize=6.5, fillColor=COLOR_BLACK))
    g.add(String(405, y_pos + 14, "SHA-1 Hash", fontName="Courier", fontSize=6.0, fillColor=COLOR_MUTED))

    # Connectors
    _draw_arrow(g, 100, y_pos + 32, 110, y_pos + 32, color=COLOR_CHARCOAL, stroke_width=0.75)
    _draw_arrow(g, 295, y_pos + 32, 305, y_pos + 32, color=COLOR_CHARCOAL, stroke_width=0.75)
    _draw_arrow(g, 390, y_pos + 32, 400, y_pos + 32, color=COLOR_CHARCOAL, stroke_width=0.75)

    g.add(
        String(
            15,
            14,
            "STAT CACHE: Git uses lstat() filesystem metadata to avoid re-reading file contents when disk mtime equals index mtime.",
            fontName="Helvetica-Bold",
            fontSize=6.5,
            fillColor=COLOR_BLACK,
        )
    )

    return d


# ---------------------------------------------------------------------------
# 9. Merge Conflict Anatomy Diagram
# ---------------------------------------------------------------------------
def create_merge_conflict_diagram() -> Drawing:
    """Renders the anatomy of a Git 3-Way Merge Conflict block."""
    height = 150.0
    d, g = _make_canvas_frame(
        height,
        "Figure 7.2: Anatomical Structure of a 3-Way Merge Conflict Marker",
        "Diff3 Marker View: HEAD ➔ Common Base ➔ Incoming Branch",
    )

    y_base = 28.0
    box_w = 445.0
    box_h = 95.0

    g.add(Rect(15, y_base, box_w, box_h, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.0))

    # Conflict Marker Sections
    # 1. <<<<<<< HEAD
    g.add(Rect(20, y_base + 70, box_w - 10, 18, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(String(28, y_base + 75, "<<<<<<< HEAD (Current Change / Ours)", fontName="Courier-Bold", fontSize=7.0, fillColor=COLOR_BLACK))

    # Our code line
    g.add(String(28, y_base + 55, "const apiEndpoint = 'https://api.v2.internal/users';", fontName="Courier", fontSize=6.5, fillColor=COLOR_CHARCOAL))

    # 2. =======
    g.add(Line(20, y_base + 48, 20 + box_w - 10, y_base + 48, strokeColor=COLOR_BLACK, strokeWidth=1.0))
    g.add(String(28, y_base + 40, "=======", fontName="Courier-Bold", fontSize=7.0, fillColor=COLOR_BLACK))

    # Their code line
    g.add(String(28, y_base + 26, "const apiEndpoint = 'https://gateway.cloud.company.com/v1/users';", fontName="Courier", fontSize=6.5, fillColor=COLOR_CHARCOAL))

    # 3. >>>>>>> branch
    g.add(Rect(20, y_base + 5, box_w - 10, 16, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(String(28, y_base + 10, ">>>>>>> feature-cloud-migration (Incoming Change / Theirs)", fontName="Courier-Bold", fontSize=7.0, fillColor=COLOR_BLACK))

    g.add(
        String(
            15,
            12,
            "DIFF3 TIP: Enable 'git config --global merge.conflictstyle diff3' to inspect the Common Base version between markers.",
            fontName="Helvetica-Bold",
            fontSize=6.5,
            fillColor=COLOR_BLACK,
        )
    )

    return d


# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# 9b. Lecture Diagrams: Central Codebase, Status Matrix, Collaboration
# ---------------------------------------------------------------------------


def create_central_codebase_diagram() -> Drawing:
    """Renders the Central Codebase Hub-and-Spoke model vs Peer-to-Peer Zip exchange."""
    height = 165.0
    d, g = _make_canvas_frame(
        height,
        "Figure 1.1: Central Codebase Architecture vs Peer-to-Peer Exchange",
        "Single Source of Truth Hub Eliminating Manual WhatsApp Zip Overwrites",
    )

    # Center Hub (Central Codebase)
    hub_x, hub_y, hub_w, hub_h = 165.0, 48.0, 145.0, 65.0
    g.add(Rect(hub_x, hub_y, hub_w, hub_h, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_BLACK, strokeWidth=1.5))
    g.add(String(hub_x + 16, hub_y + 45, "CENTRAL CODEBASE", fontName="Helvetica-Bold", fontSize=9.0, fillColor=COLOR_BLACK))
    g.add(String(hub_x + 12, hub_y + 30, "Single Source of Truth", fontName="Helvetica-Oblique", fontSize=7.5, fillColor=COLOR_DARK_GREY))
    g.add(String(hub_x + 22, hub_y + 16, "(GitHub Cloud Remote)", fontName="Courier", fontSize=7.0, fillColor=COLOR_MUTED))

    # Dev 1: Nobita (Left)
    g.add(Rect(15, 65, 110, 42, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.0))
    g.add(String(22, 92, "NOBITA (Dev 1)", fontName="Helvetica-Bold", fontSize=8.0, fillColor=COLOR_BLACK))
    g.add(String(22, 79, "Feature: Navbar", fontName="Helvetica", fontSize=7.0, fillColor=COLOR_MUTED))
    _draw_arrow(g, 125, 86, hub_x, 86, color=COLOR_BLACK, stroke_width=1.0)
    _draw_arrow(g, hub_x, 78, 125, 78, color=COLOR_MUTED, stroke_width=1.0)

    # Dev 2: Gian (Right)
    g.add(Rect(350, 65, 110, 42, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.0))
    g.add(String(358, 92, "GIAN (Dev 2)", fontName="Helvetica-Bold", fontSize=8.0, fillColor=COLOR_BLACK))
    g.add(String(358, 79, "Feature: Footer", fontName="Helvetica", fontSize=7.0, fillColor=COLOR_MUTED))
    _draw_arrow(g, 350, 86, hub_x + hub_w, 86, color=COLOR_BLACK, stroke_width=1.0)
    _draw_arrow(g, hub_x + hub_w, 78, 350, 78, color=COLOR_MUTED, stroke_width=1.0)

    # Dev 3: Shizuka (Bottom Center)
    g.add(Rect(182, 8, 110, 32, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.0))
    g.add(String(190, 26, "SHIZUKA (Dev 3)", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK))
    g.add(String(190, 15, "Feature: Hero Section", fontName="Helvetica", fontSize=6.5, fillColor=COLOR_MUTED))
    _draw_arrow(g, 237, 40, 237, hub_y, color=COLOR_BLACK, stroke_width=1.0)

    # Warning Box: Broken Peer-to-Peer
    g.add(Rect(15, 8, 145, 45, fillColor=COLOR_BG_LIGHT, strokeColor=COLOR_HAIRLINE, strokeWidth=0.8))
    g.add(String(20, 40, "[CRISIS: Manual Exchange]", fontName="Helvetica-Bold", fontSize=6.5, fillColor=COLOR_BLACK))
    g.add(String(20, 28, "x Gian sends project_final.zip", fontName="Courier", fontSize=6.0, fillColor=COLOR_DARK_GREY))
    g.add(String(20, 17, "x Overwrites Nobita\'s work", fontName="Courier", fontSize=6.0, fillColor=COLOR_DARK_GREY))

    return d


def create_status_matrix_diagram() -> Drawing:
    """Renders the Two-Column Short Status Matrix (git status -s)."""
    height = 145.0
    d, g = _make_canvas_frame(
        height,
        "Figure 3.1: Short Status Matrix Structure (git status -s)",
        "Column 1: Staging Index State | Column 2: Working Directory State",
    )

    box_w = 445.0
    g.add(Rect(15, 12, box_w, 100, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.0))

    # Header Row
    g.add(Rect(15, 87, box_w, 25, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_BLACK, strokeWidth=0.5))
    g.add(String(25, 96, "RAW OUTPUT", fontName="Courier-Bold", fontSize=7.5, fillColor=COLOR_BLACK))
    g.add(String(125, 96, "INDEX (COL 1)", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK))
    g.add(String(235, 96, "WORKTREE (COL 2)", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK))
    g.add(String(345, 96, "EXPLANATION", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK))

    rows = [
        ("A  padhai.md", "Added (Staged)", "Pristine", "Ready for commit checkpoint", 68),
        (" M hisaab.txt", "Unchanged", "Modified (Red)", "Changes exist only on disk", 49),
        ("AM padhai.md", "Staged (Green)", "Modified (Red)", "Staged, then modified again!", 30),
        ("?? newfile.js", "Untracked", "Untracked", "Git not observing file", 11),
    ]

    for raw, c1, c2, expl, y in rows:
        g.add(String(25, y + 4, raw, fontName="Courier", fontSize=7.0, fillColor=COLOR_BLACK))
        g.add(String(125, y + 4, c1, fontName="Helvetica", fontSize=7.0, fillColor=COLOR_DARK_GREY))
        g.add(String(235, y + 4, c2, fontName="Helvetica-Bold" if "Modified" in c2 else "Helvetica", fontSize=7.0, fillColor=COLOR_BLACK if "Modified" in c2 else COLOR_DARK_GREY))
        g.add(String(345, y + 4, expl, fontName="Helvetica-Oblique", fontSize=7.0, fillColor=COLOR_MUTED))
        g.add(Line(15, y, 15 + box_w, y, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))

    return d


def create_collaboration_steps_diagram() -> Drawing:
    """Renders the 12 COMMON STEPS multi-developer collaboration workflow."""
    height = 150.0
    d, g = _make_canvas_frame(
        height,
        "Figure 4.1: The 12 COMMON STEPS Team Collaboration Lifecycle",
        "Lead Setup ➔ GitHub testingtest ➔ Feature Branch ➔ PR Review & Merge",
    )

    step_w = 98.0
    step_h = 70.0
    y_pos = 32.0

    steps = [
        (15, "1. LEAD INIT", "Repo: testingtest", "git init + README", "git push origin main"),
        (130, "2. INVITE", "Add lolpoloo", "Pending Invite", "Shivam accepts invite"),
        (245, "3. FEATURE", "git clone repo", "git switch -c feat", "index.html marquee"),
        (360, "4. PR & SYNC", "git push feat", "Open Pull Request", "Lead merges + pull"),
    ]

    for x, s_num, s_l1, s_l2, s_l3 in steps:
        g.add(Rect(x, y_pos, step_w, step_h, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.0))
        g.add(Rect(x, y_pos + step_h - 18, step_w, 18, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_BLACK, strokeWidth=0.5))
        g.add(String(x + 8, y_pos + step_h - 13, s_num, fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK))
        g.add(String(x + 6, y_pos + 36, s_l1, fontName="Courier-Bold", fontSize=6.5, fillColor=COLOR_BLACK))
        g.add(String(x + 6, y_pos + 24, s_l2, fontName="Helvetica", fontSize=6.5, fillColor=COLOR_DARK_GREY))
        g.add(String(x + 6, y_pos + 12, s_l3, fontName="Helvetica-Oblique", fontSize=6.0, fillColor=COLOR_MUTED))

    _draw_arrow(g, 113, y_pos + 35, 130, y_pos + 35, color=COLOR_BLACK, stroke_width=1.0)
    _draw_arrow(g, 228, y_pos + 35, 245, y_pos + 35, color=COLOR_BLACK, stroke_width=1.0)
    _draw_arrow(g, 343, y_pos + 35, 360, y_pos + 35, color=COLOR_BLACK, stroke_width=1.0)

    return d


# 10. Sleep Architecture & Ultradian Cycles Diagram
# ---------------------------------------------------------------------------
def create_sleep_architecture_diagram() -> Drawing:
    """Renders the 90-Minute Sleep Architecture & Ultradian Cycles."""
    height = 160.0
    d, g = _make_canvas_frame(
        height,
        "Figure 1.1: Human Sleep Architecture & 90-Min Cycles",
        "NREM Slow-Wave vs REM Distribution",
    )

    cycle_w = 100.0
    x_start = 20.0
    y_base = 35.0

    cycles = [
        ("Cycle 1 (0:00 - 1:30)", 70, 20),
        ("Cycle 2 (1:30 - 3:00)", 55, 35),
        ("Cycle 3 (3:00 - 4:30)", 40, 50),
        ("Cycle 4 (4:30 - 6:00)", 25, 65),
    ]

    for i, (title, nrem_h, rem_h) in enumerate(cycles):
        cx = x_start + i * 110.0
        g.add(Rect(cx, y_base, cycle_w, 90, fillColor=COLOR_BG_BOX, strokeColor=COLOR_HAIRLINE, strokeWidth=0.75, rx=2, ry=2))
        g.add(Rect(cx, y_base + 72, cycle_w, 18, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
        g.add(String(cx + 6, y_base + 78, title, fontName="Helvetica-Bold", fontSize=6.5, fillColor=COLOR_BLACK))

        # Deep NREM Bar (Charcoal)
        g.add(Rect(cx + 10, y_base + 20, 35, nrem_h * 0.65, fillColor=COLOR_CHARCOAL, strokeColor=COLOR_BLACK, strokeWidth=0.5))
        g.add(String(cx + 12, y_base + 8, "NREM SWS", fontName="Courier-Bold", fontSize=6.0, fillColor=COLOR_CHARCOAL))

        # REM Bar (Light shaded with border)
        g.add(Rect(cx + 55, y_base + 20, 35, rem_h * 0.65, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_BLACK, strokeWidth=0.75))
        g.add(String(cx + 62, y_base + 8, "REM DREAM", fontName="Courier-Bold", fontSize=6.0, fillColor=COLOR_BLACK))

    g.add(String(20, 14, "INVARIANT: Early night is optimized for anatomical & memory consolidation (SWS); late night for emotional & associative synthesis (REM).", fontName="Helvetica-Bold", fontSize=6.5, fillColor=COLOR_BLACK))
    return d


# ---------------------------------------------------------------------------
# 11. Hippocampal-Neocortical Memory Transfer Diagram
# ---------------------------------------------------------------------------
def create_memory_transfer_diagram() -> Drawing:
    """Renders the Hippocampal-Neocortical Memory Consolidation Protocol."""
    height = 150.0
    d, g = _make_canvas_frame(
        height,
        "Figure 2.1: Memory Consolidation Pipeline",
        "Slow-Wave Sleep & Spindle Coupling",
    )

    y_box = 35.0

    # 1. Hippocampus Box (Left - Volatile Cache / Temporary RAM)
    g.add(Rect(20, y_box, 135, 85, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.0, rx=3, ry=3))
    g.add(Rect(20, y_box + 67, 135, 18, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(String(26, y_box + 73, "HIPPOCAMPUS (Volatile RAM)", fontName="Helvetica-Bold", fontSize=7.0, fillColor=COLOR_BLACK))
    g.add(String(26, y_box + 50, "• Short-term memory buffer", fontName="Helvetica", fontSize=6.5, fillColor=COLOR_CHARCOAL))
    g.add(String(26, y_box + 38, "• Vulnerable to overwrite", fontName="Helvetica", fontSize=6.5, fillColor=COLOR_CHARCOAL))
    g.add(String(26, y_box + 26, "• High turnover rate", fontName="Helvetica", fontSize=6.5, fillColor=COLOR_CHARCOAL))
    g.add(String(26, y_box + 12, "STATUS: Cache Full at Bedtime", fontName="Courier-Bold", fontSize=6.0, fillColor=COLOR_MUTED))

    # 2. Middle Channel (The Transfer Bus)
    _draw_arrow(g, 160, y_box + 50, 310, y_box + 50, color=COLOR_BLACK, stroke_width=1.5, head_len=8, head_width=5)
    g.add(Rect(175, y_box + 56, 120, 22, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_BLACK, strokeWidth=0.75, rx=2, ry=2))
    g.add(String(182, y_box + 68, "SLOW-WAVE OSCILLATIONS (<1 Hz)", fontName="Courier-Bold", fontSize=6.0, fillColor=COLOR_BLACK))
    g.add(String(190, y_box + 59, "+ SLEEP SPINDLES (11-16 Hz)", fontName="Courier-Bold", fontSize=6.0, fillColor=COLOR_CHARCOAL))

    # Feedback / Clear Cache Arrow
    _draw_arrow(g, 310, y_box + 20, 160, y_box + 20, color=COLOR_MUTED, stroke_width=1.0, head_len=6, head_width=4)
    g.add(String(185, y_box + 10, "CACHE FLUSH (Frees Next-Day Buffer)", fontName="Courier", fontSize=5.5, fillColor=COLOR_MUTED))

    # 3. Neocortex Box (Right - Distributed Long-Term Storage / HDD)
    g.add(Rect(315, y_box, 140, 85, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.0, rx=3, ry=3))
    g.add(Rect(315, y_box + 67, 140, 18, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(String(321, y_box + 73, "NEOCORTEX (Permanent Storage)", fontName="Helvetica-Bold", fontSize=7.0, fillColor=COLOR_BLACK))
    g.add(String(321, y_box + 50, "• Infinite distributed capacity", fontName="Helvetica", fontSize=6.5, fillColor=COLOR_CHARCOAL))
    g.add(String(321, y_box + 38, "• Schema integration & synaptogenesis", fontName="Helvetica", fontSize=6.5, fillColor=COLOR_CHARCOAL))
    g.add(String(321, y_box + 26, "• Immune to simple overwrite", fontName="Helvetica", fontSize=6.5, fillColor=COLOR_CHARCOAL))
    g.add(String(321, y_box + 12, "STATUS: Consolidated Storage", fontName="Courier-Bold", fontSize=6.0, fillColor=COLOR_BLACK))

    g.add(String(20, 12, "PROVEN INVARIANT: Sleep deprivation after learning drops retention by 40% (Nature Neuroscience 10:385).", fontName="Helvetica-Bold", fontSize=6.5, fillColor=COLOR_BLACK))
    return d


# ---------------------------------------------------------------------------
# 12. Adenosine Sleep Pressure & Caffeine Blockade Diagram
# ---------------------------------------------------------------------------
def create_adenosine_caffeine_diagram() -> Drawing:
    """Renders the Adenosine Homeostatic Sleep Pressure & Caffeine Antagonism Curve."""
    height = 155.0
    d, g = _make_canvas_frame(
        height,
        "Figure 3.1: Adenosine Sleep Pressure & Caffeine Blockade",
        "Process S vs Receptor Antagonism",
    )

    y_base = 32.0

    # Axes
    g.add(Line(35, y_base, 450, y_base, strokeColor=COLOR_BLACK, strokeWidth=1.0))
    g.add(Line(35, y_base, 35, y_base + 95, strokeColor=COLOR_BLACK, strokeWidth=1.0))
    g.add(String(20, y_base + 88, "High", fontName="Helvetica", fontSize=6.0, fillColor=COLOR_MUTED))
    g.add(String(20, y_base, "Low", fontName="Helvetica", fontSize=6.0, fillColor=COLOR_MUTED))
    g.add(String(40, y_base - 10, "7:00 AM (Awake)", fontName="Courier", fontSize=6.0, fillColor=COLOR_CHARCOAL))
    g.add(String(160, y_base - 10, "1:00 PM (Coffee)", fontName="Courier", fontSize=6.0, fillColor=COLOR_CHARCOAL))
    g.add(String(290, y_base - 10, "7:00 PM (Evening)", fontName="Courier", fontSize=6.0, fillColor=COLOR_CHARCOAL))
    g.add(String(390, y_base - 10, "11:00 PM (Sleep Crash)", fontName="Courier-Bold", fontSize=6.0, fillColor=COLOR_BLACK))

    # Adenosine Accumulation Curve
    pts = [
        (35, y_base + 5), (90, y_base + 22), (160, y_base + 45),
        (230, y_base + 65), (310, y_base + 78), (390, y_base + 90)
    ]
    for idx in range(len(pts) - 1):
        g.add(Line(pts[idx][0], pts[idx][1], pts[idx+1][0], pts[idx+1][1], strokeColor=COLOR_BLACK, strokeWidth=1.5))
    g.add(String(170, y_base + 80, "Real Adenosine Pressure (Process S)", fontName="Helvetica-Bold", fontSize=6.5, fillColor=COLOR_BLACK))

    # Caffeine Blockade Shadow (Dotted line effect)
    c_pts = [
        (160, y_base + 45), (200, y_base + 25), (250, y_base + 20),
        (300, y_base + 35), (350, y_base + 60), (390, y_base + 90)
    ]
    for idx in range(len(c_pts) - 1):
        g.add(Line(c_pts[idx][0], c_pts[idx][1], c_pts[idx+1][0], c_pts[idx+1][1], strokeColor=COLOR_MUTED, strokeWidth=1.0))
    g.add(String(205, y_base + 12, "Perceived Fatigue (Caffeine Masking)", fontName="Helvetica-Oblique", fontSize=6.0, fillColor=COLOR_MUTED))

    # Crash Arrow at 11 PM
    _draw_arrow(g, 390, y_base + 88, 390, y_base + 25, color=COLOR_CHARCOAL, stroke_width=1.2, head_len=6, head_width=4)
    g.add(String(330, y_base + 45, "CAFFEINE CRASH: Liver clears drug,", fontName="Courier-Bold", fontSize=5.5, fillColor=COLOR_BLACK))
    g.add(String(330, y_base + 37, "accumulated adenosine floods brain.", fontName="Courier", fontSize=5.5, fillColor=COLOR_CHARCOAL))

    # Explanatory Callout Box
    g.add(Rect(310, y_base + 55, 140, 35, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=0.5, rx=2, ry=2))
    g.add(String(315, y_base + 78, "RECEPTOR ANTAGONISM:", fontName="Helvetica-Bold", fontSize=6.0, fillColor=COLOR_BLACK))
    g.add(String(315, y_base + 68, "Caffeine binds A1/A2A receptors without", fontName="Helvetica", fontSize=5.5, fillColor=COLOR_CHARCOAL))
    g.add(String(315, y_base + 60, "activating them. Adenosine continues to climb.", fontName="Helvetica", fontSize=5.5, fillColor=COLOR_CHARCOAL))

    g.add(String(20, 10, "PHARMACOKINETICS: Caffeine half-life is 5-7 hours; quarter-life 10-12 hours. Afternoon coffee impairs Stage 3/4 sleep.", fontName="Helvetica-Bold", fontSize=6.5, fillColor=COLOR_BLACK))
    return d


# ---------------------------------------------------------------------------
# 13. Natural Killer (NK) Cell Immunological Collapse Diagram
# ---------------------------------------------------------------------------
def create_immune_killer_cells_diagram() -> Drawing:
    """Renders the Natural Killer (NK) Cell Immunological Vulnerability Diagram."""
    height = 150.0
    d, g = _make_canvas_frame(
        height,
        "Figure 4.1: Natural Killer Cell Cytotoxic Collapse",
        "70% Deficit from 4h Sleep Loss",
    )

    y_base = 35.0

    # Left Container: Baseline 8 Hours of Sleep
    g.add(Rect(35, y_base, 180, 85, fillColor=COLOR_BG_BOX, strokeColor=COLOR_HAIRLINE, strokeWidth=0.75, rx=3, ry=3))
    g.add(Rect(35, y_base + 67, 180, 18, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(String(42, y_base + 73, "BASELINE SLEEP (8 HOURS)", fontName="Helvetica-Bold", fontSize=7.0, fillColor=COLOR_BLACK))

    # 100% Bar
    g.add(Rect(50, y_base + 15, 45, 48, fillColor=COLOR_CHARCOAL, strokeColor=COLOR_BLACK, strokeWidth=1.0))
    g.add(String(58, y_base + 35, "100%", fontName="Helvetica-Bold", fontSize=10.0, fillColor=COLOR_WHITE))
    g.add(String(105, y_base + 45, "Optimal NK Lytic Activity", fontName="Helvetica-Bold", fontSize=6.5, fillColor=COLOR_BLACK))
    g.add(String(105, y_base + 34, "• Continuous tumor surveillance", fontName="Helvetica", fontSize=6.0, fillColor=COLOR_CHARCOAL))
    g.add(String(105, y_base + 24, "• Rapid virus particle lysis", fontName="Helvetica", fontSize=6.0, fillColor=COLOR_CHARCOAL))
    g.add(String(105, y_base + 14, "• Low systemic inflammation", fontName="Helvetica", fontSize=6.0, fillColor=COLOR_CHARCOAL))

    # Right Container: Restricted Sleep (4 Hours Single Night)
    g.add(Rect(240, y_base, 205, 85, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.0, rx=3, ry=3))
    g.add(Rect(240, y_base + 67, 205, 18, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(String(247, y_base + 73, "PARTIAL SLEEP RESTRICTION (4 HOURS)", fontName="Helvetica-Bold", fontSize=7.0, fillColor=COLOR_BLACK))

    # 30% Bar (70% Deficit)
    g.add(Rect(255, y_base + 15, 45, 15, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_BLACK, strokeWidth=1.0))
    g.add(String(265, y_base + 19, "30%", fontName="Helvetica-Bold", fontSize=8.0, fillColor=COLOR_BLACK))

    # Deficit Marker
    g.add(Rect(255, y_base + 30, 45, 33, fillColor=COLOR_WHITE, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(String(258, y_base + 44, "-70% LOSS", fontName="Courier-Bold", fontSize=7.0, fillColor=COLOR_CHARCOAL))

    # Clinical Consequences
    g.add(String(310, y_base + 50, "IMMUNE DEFENSE COLLAPSE:", fontName="Helvetica-Bold", fontSize=6.5, fillColor=COLOR_BLACK))
    g.add(String(310, y_base + 38, "• 70% drop in NK cytotoxicity", fontName="Helvetica", fontSize=6.0, fillColor=COLOR_CHARCOAL))
    g.add(String(310, y_base + 27, "• WHO classifies shift-work as carcinogen", fontName="Helvetica", fontSize=6.0, fillColor=COLOR_CHARCOAL))
    g.add(String(310, y_base + 16, "• 711 genes disrupted (PNAS 110:E1132)", fontName="Helvetica", fontSize=6.0, fillColor=COLOR_CHARCOAL))

    _draw_arrow(g, 220, y_base + 40, 235, y_base + 40, color=COLOR_BLACK, stroke_width=1.0, head_len=5, head_width=3)
    g.add(String(20, 12, "ONCOLOGICAL INVARIANT: Natural killer cells act as biological 007 agents. Single-night sleep loss disables surveillance.", fontName="Helvetica-Bold", fontSize=6.5, fillColor=COLOR_BLACK))
    return d


# ---------------------------------------------------------------------------
# 14. Core Body Thermoregulation & Circadian Sleep Gate Diagram
# ---------------------------------------------------------------------------
def create_thermal_circadian_diagram() -> Drawing:
    """Renders the Core Body Thermoregulation & Circadian Sleep Gate Diagram."""
    height = 155.0
    d, g = _make_canvas_frame(
        height,
        "Figure 5.1: Thermoregulation & Circadian Sleep Gate",
        "Core Body Cooling & Melatonin Gate",
    )

    y_base = 32.0

    # Axes
    g.add(Line(35, y_base, 450, y_base, strokeColor=COLOR_BLACK, strokeWidth=1.0))
    g.add(Line(35, y_base, 35, y_base + 95, strokeColor=COLOR_BLACK, strokeWidth=1.0))
    g.add(String(40, y_base - 10, "12:00 PM (Noon)", fontName="Courier", fontSize=6.0, fillColor=COLOR_CHARCOAL))
    g.add(String(145, y_base - 10, "6:00 PM (Peak Temp)", fontName="Courier", fontSize=6.0, fillColor=COLOR_CHARCOAL))
    g.add(String(270, y_base - 10, "11:00 PM (Sleep Onset)", fontName="Courier-Bold", fontSize=6.0, fillColor=COLOR_BLACK))
    g.add(String(390, y_base - 10, "4:00 AM (Thermal Min)", fontName="Courier", fontSize=6.0, fillColor=COLOR_CHARCOAL))

    # Core Temperature Curve
    temp_pts = [
        (35, y_base + 65), (145, y_base + 85), (220, y_base + 70),
        (270, y_base + 40), (340, y_base + 20), (390, y_base + 12), (450, y_base + 35)
    ]
    for idx in range(len(temp_pts) - 1):
        g.add(Line(temp_pts[idx][0], temp_pts[idx][1], temp_pts[idx+1][0], temp_pts[idx+1][1], strokeColor=COLOR_BLACK, strokeWidth=1.5))
    g.add(String(90, y_base + 90, "Core Body Temperature (Drops 2-3°F / 1°C for sleep)", fontName="Helvetica-Bold", fontSize=6.5, fillColor=COLOR_BLACK))

    # Melatonin Secretion Surge Curve
    mel_pts = [
        (35, y_base + 8), (145, y_base + 12), (220, y_base + 30),
        (270, y_base + 70), (340, y_base + 85), (390, y_base + 75), (450, y_base + 20)
    ]
    for idx in range(len(mel_pts) - 1):
        g.add(Line(mel_pts[idx][0], mel_pts[idx][1], mel_pts[idx+1][0], mel_pts[idx+1][1], strokeColor=COLOR_MUTED, strokeWidth=1.2))
    g.add(String(275, y_base + 60, "Melatonin Surge (Pineal Gland)", fontName="Helvetica-Oblique", fontSize=6.5, fillColor=COLOR_MUTED))

    # Shaded Sleep Window Container
    g.add(Rect(270, y_base, 180, 95, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(String(275, y_base + 82, "CIRCADIAN SLEEP WINDOW", fontName="Courier-Bold", fontSize=6.5, fillColor=COLOR_BLACK))
    g.add(String(275, y_base + 30, "• Ambient Room Temp: ~65°F (18.3°C)", fontName="Helvetica", fontSize=5.5, fillColor=COLOR_CHARCOAL))
    g.add(String(275, y_base + 20, "• Distal vasodilation radiates heat from hands/feet", fontName="Helvetica", fontSize=5.5, fillColor=COLOR_CHARCOAL))
    g.add(String(275, y_base + 10, "• Warm bath paradoxical cooling effect", fontName="Helvetica", fontSize=5.5, fillColor=COLOR_CHARCOAL))

    g.add(String(20, 10, "ACTIONABLE INVARIANT: Sleeping in a room warmer than 70°F (21°C) prevents core body cooling, fracturing NREM SWS.", fontName="Helvetica-Bold", fontSize=6.5, fillColor=COLOR_BLACK))
    return d


# ---------------------------------------------------------------------------
# 15. Prefrontal-Hippocampal Neuroplastic Axis Diagram
# ---------------------------------------------------------------------------
def create_pfc_hippocampal_axis_diagram() -> Drawing:
    """Renders the Prefrontal-Hippocampal Neuroplastic Axis Diagram."""
    height = 155.0
    d, g = _make_canvas_frame(
        height,
        "Figure 1.1: Prefrontal-Hippocampal Neuroplastic Axis",
        "Dual Anatomical Targets of Exercise-Induced Transformation",
    )

    y_box = 32.0
    box_w = 205.0
    box_h = 85.0

    # Box 1: Prefrontal Cortex (Left)
    g.add(Rect(15, y_box, box_w, box_h, rx=3, ry=3, fillColor=COLOR_BG_LIGHT, strokeColor=COLOR_BLACK, strokeWidth=1.0))
    g.add(String(25, y_box + 70, "PREFRONTAL CORTEX (PFC)", fontName="Helvetica-Bold", fontSize=8.0, fillColor=COLOR_BLACK))
    g.add(String(25, y_box + 58, "Anterior Frontal Pole • Executive Center", fontName="Helvetica-Oblique", fontSize=6.5, fillColor=COLOR_MUTED))
    g.add(Line(25, y_box + 52, 210, y_box + 52, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(String(25, y_box + 40, "• Attentional focus & task switching (+2h window)", fontName="Helvetica", fontSize=6.0, fillColor=COLOR_CHARCOAL))
    g.add(String(25, y_box + 29, "• Working memory & strategic decision-making", fontName="Helvetica", fontSize=6.0, fillColor=COLOR_CHARCOAL))
    g.add(String(25, y_box + 18, "• dlPFC synaptic arborization via aerobic exercise", fontName="Helvetica", fontSize=6.0, fillColor=COLOR_CHARCOAL))
    g.add(String(25, y_box + 7, "• High vulnerability to aging & frontotemporal loss", fontName="Helvetica", fontSize=6.0, fillColor=COLOR_CHARCOAL))

    # Box 2: Hippocampus (Right)
    g.add(Rect(255, y_box, box_w, box_h, rx=3, ry=3, fillColor=COLOR_BG_LIGHT, strokeColor=COLOR_BLACK, strokeWidth=1.0))
    g.add(String(265, y_box + 70, "HIPPOCAMPUS (TEMPORAL LOBE)", fontName="Helvetica-Bold", fontSize=8.0, fillColor=COLOR_BLACK))
    g.add(String(265, y_box + 58, "Medial Temporal Lobe • Declarative Memory Hub", fontName="Helvetica-Oblique", fontSize=6.5, fillColor=COLOR_MUTED))
    g.add(Line(265, y_box + 52, 450, y_box + 52, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(String(265, y_box + 40, "• Long-term episodic & semantic memory retention", fontName="Helvetica", fontSize=6.0, fillColor=COLOR_CHARCOAL))
    g.add(String(265, y_box + 29, "• Adult Neurogenesis: Dentate Gyrus new neurons", fontName="Helvetica", fontSize=6.0, fillColor=COLOR_CHARCOAL))
    g.add(String(265, y_box + 18, "• +2% Volumetric increase (Erickson et al., PNAS)", fontName="Helvetica", fontSize=6.0, fillColor=COLOR_CHARCOAL))
    g.add(String(265, y_box + 7, "• Prime target of Alzheimer's beta-amyloid & tau", fontName="Helvetica", fontSize=6.0, fillColor=COLOR_CHARCOAL))

    # Bi-directional communication arrow between boxes
    _draw_arrow(g, 222, y_box + 48, 248, y_box + 48, color=COLOR_BLACK, stroke_width=1.2, head_len=4, head_width=3)
    _draw_arrow(g, 248, y_box + 38, 222, y_box + 38, color=COLOR_BLACK, stroke_width=1.2, head_len=4, head_width=3)
    g.add(String(224, y_box + 28, "SYNAPTO-", fontName="Courier-Bold", fontSize=5.0, fillColor=COLOR_BLACK))
    g.add(String(226, y_box + 20, "GENESIS", fontName="Courier-Bold", fontSize=5.0, fillColor=COLOR_BLACK))

    g.add(String(20, 12, "ANATOMICAL INVARIANT: The two structures most vulnerable to age-related neurodegeneration are the most neuroplastic under exercise.", fontName="Helvetica-Bold", fontSize=6.5, fillColor=COLOR_BLACK))
    return d


# ---------------------------------------------------------------------------
# 16. Acute Exercise Neurochemical Cascade Diagram
# ---------------------------------------------------------------------------
def create_neurochemical_surge_diagram() -> Drawing:
    """Renders the Acute Exercise Neurochemical Cascade Diagram."""
    height = 150.0
    d, g = _make_canvas_frame(
        height,
        "Figure 2.1: Acute Exercise Neurochemical Cascade",
        "Immediate Monoaminergic Surges & 2-Hour Focus Window",
    )

    y_base = 30.0

    # Left Track: 3 Neurotransmitter Gauges
    # Gauge 1: Dopamine
    g.add(String(15, y_base + 82, "DOPAMINE (DA)", fontName="Helvetica-Bold", fontSize=7.0, fillColor=COLOR_BLACK))
    g.add(String(15, y_base + 73, "VTA / Striatal Motor Drive", fontName="Helvetica", fontSize=5.5, fillColor=COLOR_MUTED))
    g.add(Rect(125, y_base + 75, 110, 10, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(Rect(125, y_base + 75, 88, 10, fillColor=COLOR_BLACK, strokeColor=COLOR_BLACK, strokeWidth=0.5))
    g.add(String(218, y_base + 77, "+180%", fontName="Courier-Bold", fontSize=6.5, fillColor=COLOR_BLACK))

    # Gauge 2: Serotonin
    g.add(String(15, y_base + 55, "SEROTONIN (5-HT)", fontName="Helvetica-Bold", fontSize=7.0, fillColor=COLOR_BLACK))
    g.add(String(15, y_base + 46, "Dorsal Raphe Mood Stability", fontName="Helvetica", fontSize=5.5, fillColor=COLOR_MUTED))
    g.add(Rect(125, y_base + 48, 110, 10, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(Rect(125, y_base + 48, 75, 10, fillColor=COLOR_CHARCOAL, strokeColor=COLOR_CHARCOAL, strokeWidth=0.5))
    g.add(String(205, y_base + 50, "+150%", fontName="Courier-Bold", fontSize=6.5, fillColor=COLOR_BLACK))

    # Gauge 3: Noradrenaline
    g.add(String(15, y_base + 28, "NORADRENALINE (NE)", fontName="Helvetica-Bold", fontSize=7.0, fillColor=COLOR_BLACK))
    g.add(String(15, y_base + 19, "Locus Coeruleus Alertness", fontName="Helvetica", fontSize=5.5, fillColor=COLOR_MUTED))
    g.add(Rect(125, y_base + 21, 110, 10, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(Rect(125, y_base + 21, 95, 10, fillColor=COLOR_BLACK, strokeColor=COLOR_BLACK, strokeWidth=0.5))
    g.add(String(224, y_base + 23, "+200%", fontName="Courier-Bold", fontSize=6.5, fillColor=COLOR_BLACK))

    # Right Box: 2-Hour Cognitive Window Timeline
    g.add(Rect(260, y_base + 12, 205, 85, rx=3, ry=3, fillColor=COLOR_BG_LIGHT, strokeColor=COLOR_BLACK, strokeWidth=1.0))
    g.add(String(270, y_base + 82, "POST-WORKOUT COGNITIVE WINDOW", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK))
    g.add(Line(270, y_base + 76, 455, y_base + 76, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))

    g.add(String(270, y_base + 64, "• T = 0-15m: Acute monoamine surge & euphoria", fontName="Helvetica", fontSize=6.0, fillColor=COLOR_CHARCOAL))
    g.add(String(270, y_base + 52, "• T = 15m-2h: Attentional focus window (Suzuki Lab)", fontName="Helvetica-Bold", fontSize=6.0, fillColor=COLOR_BLACK))
    g.add(String(270, y_base + 40, "• Stroop task reaction time significantly accelerated", fontName="Helvetica", fontSize=6.0, fillColor=COLOR_CHARCOAL))
    g.add(String(270, y_base + 28, "• Prefrontal executive tasks & grant-writing optimum", fontName="Helvetica", fontSize=6.0, fillColor=COLOR_CHARCOAL))
    g.add(String(270, y_base + 16, "• Transient surge bridges to chronic baseline lift", fontName="Helvetica-Oblique", fontSize=6.0, fillColor=COLOR_MUTED))

    g.add(String(20, 10, "ACUTE MECHANISM INVARIANT: A single workout primes monoamines, opening a proven minimum 2-hour high-efficiency attentional focus window.", fontName="Helvetica-Bold", fontSize=6.5, fillColor=COLOR_BLACK))
    return d


# ---------------------------------------------------------------------------
# 17. Muscle-Brain Molecular Neurogenesis Cascade Diagram
# ---------------------------------------------------------------------------
def create_bdnf_neurogenesis_diagram() -> Drawing:
    """Renders the Muscle-Brain Molecular Neurogenesis Cascade Diagram."""
    height = 150.0
    d, g = _make_canvas_frame(
        height,
        "Figure 3.1: Muscle-Brain Molecular Neurogenesis Cascade",
        "Skeletal Myokines & Hippocampal Dentate Gyrus Cell Genesis",
    )

    y_box = 32.0
    b_w = 98.0
    b_h = 80.0

    # Step 1: Muscle Contraction
    g.add(Rect(12, y_box, b_w, b_h, rx=2, ry=2, fillColor=COLOR_BG_LIGHT, strokeColor=COLOR_BLACK, strokeWidth=0.8))
    g.add(String(18, y_box + 68, "1. SKELETAL MUSCLE", fontName="Helvetica-Bold", fontSize=6.5, fillColor=COLOR_BLACK))
    g.add(Line(18, y_box + 63, 104, y_box + 63, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(String(18, y_box + 50, "Aerobic contractions", fontName="Helvetica", fontSize=5.5, fillColor=COLOR_CHARCOAL))
    g.add(String(18, y_box + 40, "synthesize myokines:", fontName="Helvetica", fontSize=5.5, fillColor=COLOR_CHARCOAL))
    g.add(String(18, y_box + 28, "• Cathepsin B (CTSB)", fontName="Courier-Bold", fontSize=5.5, fillColor=COLOR_BLACK))
    g.add(String(18, y_box + 16, "• Irisin (FNDC5)", fontName="Courier-Bold", fontSize=5.5, fillColor=COLOR_BLACK))

    _draw_arrow(g, 112, y_box + 40, 126, y_box + 40, color=COLOR_BLACK, stroke_width=1.0, head_len=4, head_width=3)

    # Step 2: Blood-Brain Barrier & Angiogenesis
    g.add(Rect(128, y_box, b_w, b_h, rx=2, ry=2, fillColor=COLOR_BG_LIGHT, strokeColor=COLOR_BLACK, strokeWidth=0.8))
    g.add(String(134, y_box + 68, "2. BBB & VASCULATURE", fontName="Helvetica-Bold", fontSize=6.5, fillColor=COLOR_BLACK))
    g.add(Line(134, y_box + 63, 220, y_box + 63, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(String(134, y_box + 50, "Circulating myokines", fontName="Helvetica", fontSize=5.5, fillColor=COLOR_CHARCOAL))
    g.add(String(134, y_box + 40, "cross BBB into brain;", fontName="Helvetica", fontSize=5.5, fillColor=COLOR_CHARCOAL))
    g.add(String(134, y_box + 28, "stimulate VEGF capillary", fontName="Helvetica", fontSize=5.5, fillColor=COLOR_CHARCOAL))
    g.add(String(134, y_box + 16, "cerebral angiogenesis", fontName="Courier", fontSize=5.5, fillColor=COLOR_BLACK))

    _draw_arrow(g, 228, y_box + 40, 242, y_box + 40, color=COLOR_BLACK, stroke_width=1.0, head_len=4, head_width=3)

    # Step 3: BDNF Synthesis & TrkB Activation
    g.add(Rect(244, y_box, b_w, b_h, rx=2, ry=2, fillColor=COLOR_BG_LIGHT, strokeColor=COLOR_BLACK, strokeWidth=0.8))
    g.add(String(250, y_box + 68, "3. BDNF CASCADE", fontName="Helvetica-Bold", fontSize=6.5, fillColor=COLOR_BLACK))
    g.add(Line(250, y_box + 63, 336, y_box + 63, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(String(250, y_box + 50, "Hippocampus up-regulates", fontName="Helvetica", fontSize=5.5, fillColor=COLOR_CHARCOAL))
    g.add(String(250, y_box + 40, "BDNF expression;", fontName="Helvetica", fontSize=5.5, fillColor=COLOR_CHARCOAL))
    g.add(String(250, y_box + 28, "binds TrkB receptors", fontName="Courier-Bold", fontSize=5.5, fillColor=COLOR_BLACK))
    g.add(String(250, y_box + 16, "-> MAPK/ERK signaling", fontName="Courier", fontSize=5.5, fillColor=COLOR_CHARCOAL))

    _draw_arrow(g, 344, y_box + 40, 358, y_box + 40, color=COLOR_BLACK, stroke_width=1.0, head_len=4, head_width=3)

    # Step 4: Adult Neurogenesis
    g.add(Rect(360, y_box, b_w, b_h, rx=2, ry=2, fillColor=COLOR_BG_LIGHT, strokeColor=COLOR_BLACK, strokeWidth=0.8))
    g.add(String(366, y_box + 68, "4. NEUROGENESIS", fontName="Helvetica-Bold", fontSize=6.5, fillColor=COLOR_BLACK))
    g.add(Line(366, y_box + 63, 452, y_box + 63, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(String(366, y_box + 50, "Dentate Gyrus (DG)", fontName="Helvetica-Bold", fontSize=5.5, fillColor=COLOR_BLACK))
    g.add(String(366, y_box + 40, "generates brand-new", fontName="Helvetica", fontSize=5.5, fillColor=COLOR_CHARCOAL))
    g.add(String(366, y_box + 28, "granule neurons;", fontName="Helvetica", fontSize=5.5, fillColor=COLOR_CHARCOAL))
    g.add(String(366, y_box + 16, "functional integration", fontName="Helvetica-Oblique", fontSize=5.5, fillColor=COLOR_CHARCOAL))

    g.add(String(20, 11, "MOLECULAR INVARIANT: Skeletal muscle is an endocrine organ; contracting muscle directly triggers de novo neurogenesis in the hippocampus.", fontName="Helvetica-Bold", fontSize=6.5, fillColor=COLOR_BLACK))
    return d


# ---------------------------------------------------------------------------
# 18. Cognitive Reserve Buffer Diagram
# ---------------------------------------------------------------------------
def create_cognitive_reserve_diagram() -> Drawing:
    """Renders the Cognitive Reserve Buffer Diagram."""
    height = 155.0
    d, g = _make_canvas_frame(
        height,
        "Figure 4.1: The Brain 401(k) Cognitive Reserve Shield",
        "Aging Trajectory: Sedentary Decline vs. Exercise-Protected Longevity",
    )

    y_base = 32.0

    # Axes
    g.add(Line(40, y_base, 450, y_base, strokeColor=COLOR_BLACK, strokeWidth=1.0))
    g.add(Line(40, y_base, 40, y_base + 95, strokeColor=COLOR_BLACK, strokeWidth=1.0))
    g.add(String(45, y_base - 10, "Age 20", fontName="Courier", fontSize=6.0, fillColor=COLOR_CHARCOAL))
    g.add(String(145, y_base - 10, "Age 40", fontName="Courier", fontSize=6.0, fillColor=COLOR_CHARCOAL))
    g.add(String(245, y_base - 10, "Age 60", fontName="Courier", fontSize=6.0, fillColor=COLOR_CHARCOAL))
    g.add(String(345, y_base - 10, "Age 75", fontName="Courier", fontSize=6.0, fillColor=COLOR_CHARCOAL))
    g.add(String(425, y_base - 10, "Age 90", fontName="Courier", fontSize=6.0, fillColor=COLOR_CHARCOAL))

    g.add(String(10, y_base + 90, "100%", fontName="Courier", fontSize=6.0, fillColor=COLOR_CHARCOAL))
    g.add(String(18, y_base + 38, "Dementia Threshold", fontName="Helvetica-Bold", fontSize=5.0, fillColor=COLOR_CHARCOAL))

    # Horizontal Threshold Line (Dementia / Clinical Impairment)
    g.add(Line(40, y_base + 35, 450, y_base + 35, strokeColor=COLOR_MUTED, strokeWidth=1.0, strokeDashArray=[3, 3]))

    # Curve A: Sedentary Decline (crosses threshold around age 68)
    sed_pts = [
        (40, y_base + 85), (145, y_base + 75), (245, y_base + 55),
        (290, y_base + 35), (345, y_base + 20), (425, y_base + 8)
    ]
    for idx in range(len(sed_pts) - 1):
        g.add(Line(sed_pts[idx][0], sed_pts[idx][1], sed_pts[idx+1][0], sed_pts[idx+1][1], strokeColor=COLOR_MUTED, strokeWidth=1.5))
    g.add(String(295, y_base + 22, "Sedentary Trajectory (Crosses threshold ~age 68)", fontName="Helvetica-Oblique", fontSize=6.0, fillColor=COLOR_MUTED))

    # Curve B: Exercise Protected Trajectory (Stays above threshold)
    ex_pts = [
        (40, y_base + 90), (145, y_base + 88), (245, y_base + 78),
        (345, y_base + 62), (425, y_base + 45)
    ]
    for idx in range(len(ex_pts) - 1):
        g.add(Line(ex_pts[idx][0], ex_pts[idx][1], ex_pts[idx+1][0], ex_pts[idx+1][1], strokeColor=COLOR_BLACK, strokeWidth=2.0))
    g.add(String(150, y_base + 92, "Exercise-Protected Trajectory (Maintains Functional Reserve)", fontName="Helvetica-Bold", fontSize=6.5, fillColor=COLOR_BLACK))

    # Shaded Cognitive Reserve Surplus Box
    g.add(Rect(260, y_base + 42, 185, 22, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(String(268, y_base + 53, "BRAIN 401(k) RESERVE BUFFER", fontName="Courier-Bold", fontSize=6.5, fillColor=COLOR_BLACK))
    g.add(String(268, y_base + 45, "Delays clinical symptom manifestation by 10-15+ years", fontName="Helvetica", fontSize=5.0, fillColor=COLOR_CHARCOAL))

    g.add(String(20, 10, "LONGEVITY INVARIANT: Exercise does not cure dementia; it builds structural reserve, keeping hippocampal volume above the clinical threshold.", fontName="Helvetica-Bold", fontSize=6.5, fillColor=COLOR_BLACK))
    return d


# ---------------------------------------------------------------------------
# 19. Exercise Dosage & Cognitive ROI Matrix Diagram
# ---------------------------------------------------------------------------
def create_exercise_dosage_diagram() -> Drawing:
    """Renders the Exercise Dosage & Cognitive ROI Matrix Diagram."""
    height = 150.0
    d, g = _make_canvas_frame(
        height,
        "Figure 5.1: Empirical Exercise Prescription & Cognitive ROI",
        "Clinical Minimum Effective Dose vs. Daily Micro-Movements",
    )

    y_box = 30.0
    card_w = 140.0
    card_h = 86.0

    # Card 1: Minimum Effective Dose (MED)
    g.add(Rect(12, y_box, card_w, card_h, rx=3, ry=3, fillColor=COLOR_BG_LIGHT, strokeColor=COLOR_BLACK, strokeWidth=1.0))
    g.add(String(20, y_box + 72, "1. MINIMUM DOSE (MED)", fontName="Helvetica-Bold", fontSize=7.0, fillColor=COLOR_BLACK))
    g.add(Line(20, y_box + 67, 144, y_box + 67, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(String(20, y_box + 54, "• Frequency: 3-4x / week", fontName="Helvetica-Bold", fontSize=6.0, fillColor=COLOR_BLACK))
    g.add(String(20, y_box + 42, "• Duration: 30 mins / session", fontName="Helvetica-Bold", fontSize=6.0, fillColor=COLOR_BLACK))
    g.add(String(20, y_box + 30, "• Modality: Aerobic cardio", fontName="Helvetica", fontSize=6.0, fillColor=COLOR_CHARCOAL))
    g.add(String(20, y_box + 18, "• Target: Heart rate elevation", fontName="Helvetica", fontSize=6.0, fillColor=COLOR_CHARCOAL))
    g.add(String(20, y_box + 7, "  (Zone 2 / Zone 3 aerobic)", fontName="Helvetica-Oblique", fontSize=5.5, fillColor=COLOR_MUTED))

    # Card 2: Daily NEAT Micro-Movement
    g.add(Rect(167, y_box, card_w, card_h, rx=3, ry=3, fillColor=COLOR_BG_LIGHT, strokeColor=COLOR_BLACK, strokeWidth=1.0))
    g.add(String(175, y_box + 72, "2. DAILY MICRO-HABITS", fontName="Helvetica-Bold", fontSize=7.0, fillColor=COLOR_BLACK))
    g.add(Line(175, y_box + 67, 299, y_box + 67, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(String(175, y_box + 54, "• Take stairs over elevator", fontName="Helvetica", fontSize=6.0, fillColor=COLOR_CHARCOAL))
    g.add(String(175, y_box + 42, "• Power-walk block breaks", fontName="Helvetica", fontSize=6.0, fillColor=COLOR_CHARCOAL))
    g.add(String(175, y_box + 30, "• Brisk domestic aerobics:", fontName="Helvetica", fontSize=6.0, fillColor=COLOR_CHARCOAL))
    g.add(String(175, y_box + 18, "  'Power-vacuuming' tempo", fontName="Helvetica-Oblique", fontSize=5.5, fillColor=COLOR_MUTED))
    g.add(String(175, y_box + 7, "• Zero gym membership needed", fontName="Helvetica-Bold", fontSize=6.0, fillColor=COLOR_BLACK))

    # Card 3: Neuroplastic ROI Timeline
    g.add(Rect(322, y_box, card_w, card_h, rx=3, ry=3, fillColor=COLOR_BG_LIGHT, strokeColor=COLOR_BLACK, strokeWidth=1.0))
    g.add(String(330, y_box + 72, "3. NEUROLOGICAL ROI", fontName="Helvetica-Bold", fontSize=7.0, fillColor=COLOR_BLACK))
    g.add(Line(330, y_box + 67, 454, y_box + 67, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(String(330, y_box + 54, "• Immediate: 2h focus boost", fontName="Courier-Bold", fontSize=5.5, fillColor=COLOR_BLACK))
    g.add(String(330, y_box + 42, "• 6-12 Wks: Elevated BDNF", fontName="Courier", fontSize=5.5, fillColor=COLOR_CHARCOAL))
    g.add(String(330, y_box + 30, "• 6 Mos: Stroop speed +35%", fontName="Courier", fontSize=5.5, fillColor=COLOR_CHARCOAL))
    g.add(String(330, y_box + 18, "• 1 Yr: +2% Hippocampus vol", fontName="Courier-Bold", fontSize=5.5, fillColor=COLOR_BLACK))
    g.add(String(330, y_box + 7, "• Lifetime: Dementia buffer", fontName="Courier", fontSize=5.5, fillColor=COLOR_CHARCOAL))

    g.add(String(20, 10, "PRACTICAL INVARIANT: No elite athleticism required; 3-4x weekly 30-minute moderate aerobic sessions trigger maximum neuroplastic adaptation.", fontName="Helvetica-Bold", fontSize=6.5, fillColor=COLOR_BLACK))
    return d


# ---------------------------------------------------------------------------
# Registry Map
# ---------------------------------------------------------------------------

def create_cvcs_vs_dvcs_diagram() -> Drawing:
    """Renders Centralized VCS (SVN) vs Distributed VCS (Git)."""
    height = 155.0
    d, g = _make_canvas_frame(
        height,
        "Figure 1.2: Centralized (CVCS) vs Distributed (DVCS) Architecture",
        "Single Point of Failure (SPOF) vs Autonomous Local Repository Nodes",
    )

    # Left: CVCS (SVN)
    g.add(Rect(15, 20, 215, 115, fillColor=COLOR_BG_BOX, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(String(25, 122, "CENTRALIZED VCS (SVN / CVS)", fontName="Helvetica-Bold", fontSize=8.0, fillColor=COLOR_BLACK))
    
    # Central Server Box
    g.add(Rect(80, 75, 85, 38, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_BLACK, strokeWidth=1.2))
    g.add(String(90, 98, "CENTRAL SERVER", fontName="Helvetica-Bold", fontSize=7.0, fillColor=COLOR_BLACK))
    g.add(String(92, 85, "(Single Point of Failure)", fontName="Helvetica-Oblique", fontSize=5.5, fillColor=COLOR_MUTED))
    
    # Client A and Client B
    g.add(Rect(25, 30, 80, 28, fillColor=COLOR_WHITE, strokeColor=COLOR_BLACK, strokeWidth=0.8))
    g.add(String(32, 45, "Client 1: Working Copy", fontName="Helvetica-Bold", fontSize=6.5, fillColor=COLOR_BLACK))
    g.add(String(32, 36, "No local history/offline", fontName="Helvetica-Oblique", fontSize=5.5, fillColor=COLOR_MUTED))
    
    g.add(Rect(140, 30, 80, 28, fillColor=COLOR_WHITE, strokeColor=COLOR_BLACK, strokeWidth=0.8))
    g.add(String(147, 45, "Client 2: Working Copy", fontName="Helvetica-Bold", fontSize=6.5, fillColor=COLOR_BLACK))
    g.add(String(147, 36, "Requires active network", fontName="Helvetica-Oblique", fontSize=5.5, fillColor=COLOR_MUTED))
    
    _draw_arrow(g, 65, 58, 100, 75, stroke_width=0.8)
    _draw_arrow(g, 180, 58, 145, 75, stroke_width=0.8)

    # Right: DVCS (Git)
    g.add(Rect(245, 20, 215, 115, fillColor=COLOR_BG_BOX, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(String(255, 122, "DISTRIBUTED VCS (GIT / DVCS)", fontName="Helvetica-Bold", fontSize=8.0, fillColor=COLOR_BLACK))
    
    # Server / Remote Hub
    g.add(Rect(310, 85, 85, 32, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_BLACK, strokeWidth=1.0))
    g.add(String(320, 104, "SERVER (GitHub)", fontName="Helvetica-Bold", fontSize=7.0, fillColor=COLOR_BLACK))
    g.add(String(322, 92, "Full Mirror Remote", fontName="Helvetica-Oblique", fontSize=5.5, fillColor=COLOR_MUTED))
    
    # Client 1 Node (Full Repo)
    g.add(Rect(255, 28, 90, 38, fillColor=COLOR_WHITE, strokeColor=COLOR_BLACK, strokeWidth=1.0))
    g.add(String(260, 54, "DEV 1: Local Repo", fontName="Helvetica-Bold", fontSize=6.5, fillColor=COLOR_BLACK))
    g.add(String(260, 44, "Full History + Commits", fontName="Helvetica-Oblique", fontSize=5.5, fillColor=COLOR_DARK_GREY))
    g.add(String(260, 34, "100% Offline Capable", fontName="Courier-Bold", fontSize=5.5, fillColor=COLOR_MUTED))

    # Client 2 Node (Full Repo)
    g.add(Rect(360, 28, 90, 38, fillColor=COLOR_WHITE, strokeColor=COLOR_BLACK, strokeWidth=1.0))
    g.add(String(365, 54, "DEV 2: Local Repo", fontName="Helvetica-Bold", fontSize=6.5, fillColor=COLOR_BLACK))
    g.add(String(365, 44, "Full History + Commits", fontName="Helvetica-Oblique", fontSize=5.5, fillColor=COLOR_DARK_GREY))
    g.add(String(365, 34, "100% Offline Capable", fontName="Courier-Bold", fontSize=5.5, fillColor=COLOR_MUTED))

    # Sync arrows
    _draw_arrow(g, 300, 66, 330, 85, stroke_width=0.8)
    _draw_arrow(g, 330, 85, 300, 66, stroke_width=0.8)
    _draw_arrow(g, 405, 66, 375, 85, stroke_width=0.8)
    _draw_arrow(g, 375, 85, 405, 66, stroke_width=0.8)
    # Peer sync between Dev 1 and Dev 2
    _draw_arrow(g, 345, 47, 360, 47, stroke_width=0.8)
    _draw_arrow(g, 360, 47, 345, 47, stroke_width=0.8)

    return d


def create_fork_upstream_diagram() -> Drawing:
    """Renders Open Source Contribution Fork & Upstream Sync Architecture."""
    height = 160.0
    d, g = _make_canvas_frame(
        height,
        "Figure 7.1: Open Source Contribution Architecture (Fork & Upstream)",
        "Canonical Upstream ➔ Personal Fork (Origin) ➔ Local Clone & Cross-Repo PR",
    )

    # 1. Canonical Upstream Box (Top Left Cloud)
    g.add(Rect(20, 85, 180, 52, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_BLACK, strokeWidth=1.2))
    g.add(String(30, 122, "CANONICAL UPSTREAM (GitHub)", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK))
    g.add(String(30, 108, "github.com/maintainer/project.git", fontName="Courier", fontSize=6.0, fillColor=COLOR_DARK_GREY))
    g.add(String(30, 94, "Branch: main (Protected Production)", fontName="Helvetica-Oblique", fontSize=6.0, fillColor=COLOR_MUTED))

    # 2. Personal Fork Box (Top Right Cloud)
    g.add(Rect(275, 85, 180, 52, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.2))
    g.add(String(285, 122, "PERSONAL FORK (Origin)", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK))
    g.add(String(285, 108, "github.com/developer/project.git", fontName="Courier", fontSize=6.0, fillColor=COLOR_DARK_GREY))
    g.add(String(285, 94, "Branch: feature/fix-issue", fontName="Helvetica-Oblique", fontSize=6.0, fillColor=COLOR_MUTED))

    # Fork Arrow (Upstream -> Fork)
    _draw_arrow(g, 200, 110, 275, 110, stroke_width=1.0)
    g.add(String(220, 115, "1. FORK", fontName="Helvetica-Bold", fontSize=6.5, fillColor=COLOR_BLACK))

    # 3. Local Clone Box (Bottom Center)
    g.add(Rect(130, 15, 215, 48, fillColor=COLOR_WHITE, strokeColor=COLOR_BLACK, strokeWidth=1.2))
    g.add(String(140, 48, "LOCAL DEVELOPER MACHINE", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK))
    g.add(String(140, 36, "origin: git@github.com:developer/project.git", fontName="Courier", fontSize=5.5, fillColor=COLOR_DARK_GREY))
    g.add(String(140, 24, "upstream: git@github.com:maintainer/project.git", fontName="Courier", fontSize=5.5, fillColor=COLOR_DARK_GREY))

    # Clone Arrow (Fork -> Local)
    _draw_arrow(g, 330, 85, 270, 63, stroke_width=0.8)
    g.add(String(305, 74, "2. git clone", fontName="Helvetica-Bold", fontSize=6.0, fillColor=COLOR_BLACK))

    # Push Arrow (Local -> Fork)
    _draw_arrow(g, 290, 63, 350, 85, stroke_width=0.8)
    g.add(String(335, 68, "3. git push", fontName="Helvetica-Bold", fontSize=6.0, fillColor=COLOR_BLACK))

    # Pull Request Arrow (Fork -> Upstream)
    _draw_arrow(g, 275, 125, 200, 125, stroke_width=1.0)
    g.add(String(208, 130, "4. PULL REQUEST", fontName="Helvetica-Bold", fontSize=6.5, fillColor=COLOR_BLACK))

    # Fetch Upstream Arrow (Upstream -> Local)
    _draw_arrow(g, 100, 85, 150, 63, stroke_width=0.8)
    g.add(String(75, 72, "git fetch upstream", fontName="Helvetica-Bold", fontSize=6.0, fillColor=COLOR_BLACK))

    return d



def create_git_vs_github_diagram() -> Drawing:
    """Renders Git vs GitHub Architectural Comparison Matrix."""
    height = 145.0
    d, g = _make_canvas_frame(
        height,
        "Figure 1.3: Git vs GitHub Architectural Comparison Matrix",
        "Local Content-Addressable Engine vs Cloud Hosting & Collaboration Platform",
    )

    # Headers
    g.add(Rect(15, 100, 215, 22, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_BLACK, strokeWidth=1.0))
    g.add(String(25, 106, "GIT  (Local Machine Engine)", fontName="Helvetica-Bold", fontSize=8.0, fillColor=COLOR_BLACK))

    g.add(Rect(245, 100, 215, 22, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_BLACK, strokeWidth=1.0))
    g.add(String(255, 106, "GITHUB  (Cloud Collaboration Hub)", fontName="Helvetica-Bold", fontSize=8.0, fillColor=COLOR_BLACK))

    rows = [
        ("Core Identity", "Command-Line Tool / Distributed VCS", "Cloud Web Service & Remote Host"),
        ("Execution", "100% Offline (Zero Network Needed)", "Requires Internet Access & Web API"),
        ("Storage Scope", "Local .git/ database on hard disk", "Remote Bare Repositories in Cloud"),
        ("Key Features", "Branching, Staging Index, DAG Commits", "Pull Requests, Code Review, CI/CD"),
    ]

    y = 80
    for idx, (label, git_val, gh_val) in enumerate(rows):
        bg = COLOR_BG_BOX if idx % 2 == 0 else COLOR_WHITE
        g.add(Rect(15, y - 4, 215, 18, fillColor=bg, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
        g.add(String(20, y + 2, f"• {git_val}", fontName="Helvetica", fontSize=6.5, fillColor=COLOR_BLACK))

        g.add(Rect(245, y - 4, 215, 18, fillColor=bg, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
        g.add(String(250, y + 2, f"• {gh_val}", fontName="Helvetica", fontSize=6.5, fillColor=COLOR_BLACK))

        y -= 20

    return d


def create_dot_git_internals_diagram() -> Drawing:
    """Renders internal directory structure of .git repository database."""
    height = 160.0
    d, g = _make_canvas_frame(
        height,
        "Figure 2.2: Internal Architecture of the .git Directory",
        "Component Breakdown: HEAD Pointer, Index Cache, Object Database & Refs",
    )

    # Root Box (Left)
    g.add(Rect(15, 30, 95, 95, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_BLACK, strokeWidth=1.5))
    g.add(String(25, 102, ".git/", fontName="Courier-Bold", fontSize=13.0, fillColor=COLOR_BLACK))
    g.add(String(25, 86, "Repository Root", fontName="Helvetica-Bold", fontSize=7.0, fillColor=COLOR_BLACK))
    g.add(String(25, 72, "The local database", fontName="Helvetica-Oblique", fontSize=6.0, fillColor=COLOR_DARK_GREY))
    g.add(String(25, 62, "and cryptographic", fontName="Helvetica-Oblique", fontSize=6.0, fillColor=COLOR_DARK_GREY))
    g.add(String(25, 52, "engine of Git.", fontName="Helvetica-Oblique", fontSize=6.0, fillColor=COLOR_DARK_GREY))
    g.add(String(25, 38, "[CRITICAL ENGINE]", fontName="Courier-Bold", fontSize=5.5, fillColor=COLOR_MUTED))

    # Connector Lines
    _draw_arrow(g, 110, 112, 135, 112, stroke_width=0.8)
    _draw_arrow(g, 110, 92, 135, 92, stroke_width=0.8)
    _draw_arrow(g, 110, 72, 135, 72, stroke_width=0.8)
    _draw_arrow(g, 110, 52, 135, 52, stroke_width=0.8)
    _draw_arrow(g, 110, 32, 135, 32, stroke_width=0.8)

    # 5 Component Cards (Right)
    components = [
        ("HEAD", "Pointer to current branch or commit", "Contains: ref: refs/heads/main (active working context)", 105),
        ("index", "Binary Staging Area cache layer", "Maps relative file paths to SHA-1 blob hashes in .git/objects", 85),
        ("objects/", "Content-Addressable Object Database", "Stores zlib-compressed blobs, trees, commits, tags & packfiles", 65),
        ("refs/", "Pointers to tip commits across timelines", "Subdirs: refs/heads/ (local branches), refs/remotes/, refs/tags/", 45),
        ("config", "Repository-specific configuration file", "Local settings overriding ~/.gitconfig (remote URLs, branches)", 25),
    ]

    for name, desc1, desc2, y in components:
        g.add(Rect(135, y - 5, 325, 18, fillColor=COLOR_BG_BOX, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
        g.add(String(142, y + 2, name, fontName="Courier-Bold", fontSize=7.0, fillColor=COLOR_BLACK))
        g.add(String(200, y + 2, f"|  {desc1}", fontName="Helvetica-Bold", fontSize=5.8, fillColor=COLOR_BLACK))
        g.add(String(200, y - 4, f"   {desc2}", fontName="Helvetica-Oblique", fontSize=5.0, fillColor=COLOR_MUTED))

    return d


def create_trunk_vs_gitflow_diagram() -> Drawing:
    """Renders Trunk-Based vs Git Flow Branching Strategy Comparison."""
    height = 155.0
    d, g = _make_canvas_frame(
        height,
        "Figure 7.2: Branching Strategy Architecture — Trunk-Based vs Git Flow",
        "Short-Lived CI Feature Arcs vs Long-Lived Multi-Tier Enterprise Pipeline",
    )

    # 1. Left Side: Trunk-Based Development
    g.add(Rect(15, 20, 215, 115, fillColor=COLOR_BG_BOX, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(String(25, 122, "TRUNK-BASED DEVELOPMENT", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK))
    g.add(String(25, 112, "SaaS / Modern High-Velocity CI/CD", fontName="Helvetica-Oblique", fontSize=5.5, fillColor=COLOR_MUTED))

    # Main Trunk Line
    g.add(Line(25, 65, 210, 65, strokeColor=COLOR_BLACK, strokeWidth=1.5))
    g.add(String(180, 56, "main trunk", fontName="Courier-Bold", fontSize=6.0, fillColor=COLOR_BLACK))

    # Trunk Commits (Circles)
    for cx in [40, 75, 110, 145, 175]:
        g.add(Circle(cx, 65, 3.5, fillColor=COLOR_WHITE, strokeColor=COLOR_BLACK, strokeWidth=1.2))

    # Feature Arc 1 (short-lived)
    g.add(Line(40, 65, 58, 85, strokeColor=COLOR_DARK_GREY, strokeWidth=1.0))
    g.add(Line(58, 85, 75, 65, strokeColor=COLOR_DARK_GREY, strokeWidth=1.0))
    g.add(Circle(58, 85, 2.8, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_BLACK, strokeWidth=1.0))
    g.add(String(45, 90, "feat 1 (1-2 days)", fontName="Helvetica", fontSize=5.0, fillColor=COLOR_DARK_GREY))

    # Feature Arc 2 (short-lived)
    g.add(Line(110, 65, 128, 85, strokeColor=COLOR_DARK_GREY, strokeWidth=1.0))
    g.add(Line(128, 85, 145, 65, strokeColor=COLOR_DARK_GREY, strokeWidth=1.0))
    g.add(Circle(128, 85, 2.8, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_BLACK, strokeWidth=1.0))
    g.add(String(115, 90, "feat 2 (<24 hrs)", fontName="Helvetica", fontSize=5.0, fillColor=COLOR_DARK_GREY))

    # Invariants for Trunk
    g.add(String(25, 38, "• Commits merge to main daily", fontName="Helvetica-Bold", fontSize=5.5, fillColor=COLOR_BLACK))
    g.add(String(25, 28, "• Automated test suite gate on PRs", fontName="Helvetica", fontSize=5.5, fillColor=COLOR_DARK_GREY))

    # 2. Right Side: Git Flow
    g.add(Rect(245, 20, 215, 115, fillColor=COLOR_BG_BOX, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(String(255, 122, "GIT FLOW (ENTERPRISE MODEL)", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK))
    g.add(String(255, 112, "Scheduled Enterprise Releases", fontName="Helvetica-Oblique", fontSize=5.5, fillColor=COLOR_MUTED))

    # Main Line (Top)
    g.add(Line(255, 95, 440, 95, strokeColor=COLOR_BLACK, strokeWidth=1.2))
    g.add(String(410, 99, "main (prod)", fontName="Courier-Bold", fontSize=5.5, fillColor=COLOR_BLACK))
    g.add(Circle(270, 95, 3.0, fillColor=COLOR_WHITE, strokeColor=COLOR_BLACK, strokeWidth=1.0))
    g.add(Circle(390, 95, 3.0, fillColor=COLOR_WHITE, strokeColor=COLOR_BLACK, strokeWidth=1.0))

    # Develop Line (Middle)
    g.add(Line(255, 65, 440, 65, strokeColor=COLOR_BLACK, strokeWidth=1.2))
    g.add(String(410, 69, "develop", fontName="Courier-Bold", fontSize=5.5, fillColor=COLOR_BLACK))
    for cx in [270, 310, 350, 390]:
        g.add(Circle(cx, 65, 3.0, fillColor=COLOR_WHITE, strokeColor=COLOR_BLACK, strokeWidth=1.0))

    # Feature Branch (Bottom)
    g.add(Line(270, 65, 290, 42, strokeColor=COLOR_DARK_GREY, strokeWidth=0.8))
    g.add(Line(290, 42, 330, 42, strokeColor=COLOR_DARK_GREY, strokeWidth=0.8))
    g.add(Line(330, 42, 350, 65, strokeColor=COLOR_DARK_GREY, strokeWidth=0.8))
    g.add(Circle(310, 42, 2.5, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_BLACK, strokeWidth=0.8))
    g.add(String(290, 33, "feature/billing", fontName="Courier", fontSize=5.0, fillColor=COLOR_MUTED))

    # Release Branch
    g.add(Line(350, 65, 370, 80, strokeColor=COLOR_DARK_GREY, strokeWidth=0.8))
    g.add(Line(370, 80, 390, 95, strokeColor=COLOR_DARK_GREY, strokeWidth=0.8))
    g.add(Line(370, 80, 390, 65, strokeColor=COLOR_DARK_GREY, strokeWidth=0.8))
    g.add(String(355, 84, "release/1.0", fontName="Courier", fontSize=4.8, fillColor=COLOR_MUTED))

    # Invariants for Git Flow
    g.add(String(255, 24, "• Strict branch roles: develop, release, hotfix", fontName="Helvetica", fontSize=5.2, fillColor=COLOR_DARK_GREY))

    return d


# ---------------------------------------------------------------------------
# Additional Git Publication Vector Diagrams
# ---------------------------------------------------------------------------

def create_github_ssot_hub_diagram() -> Drawing:
    """SSOT Hub: GitHub central repo connecting multiple developers."""
    height = 150.0
    d, g = _make_canvas_frame(
        height,
        "Figure 1.3: GitHub Remote as Single Source of Truth (SSOT)",
        "Push/Pull Bidirectional Replication & Asynchronous Coordination",
    )

    hub_w = 150.0
    hub_h = 52.0
    hub_x = (TOTAL_WIDTH - hub_w) / 2.0
    hub_y = 50.0
    g.add(Rect(hub_x, hub_y, hub_w, hub_h, fillColor=COLOR_CHARCOAL, strokeColor=COLOR_BLACK, strokeWidth=1.0, rx=3, ry=3))
    g.add(String(TOTAL_WIDTH / 2.0, hub_y + 36, "GITHUB REMOTE REPOSITORY", fontName="Helvetica-Bold", fontSize=8.0, fillColor=COLOR_WHITE, textAnchor="middle"))
    g.add(String(TOTAL_WIDTH / 2.0, hub_y + 24, "testing-test (main branch)", fontName="Courier-Bold", fontSize=7.5, fillColor=COLOR_WHITE, textAnchor="middle"))
    g.add(String(TOTAL_WIDTH / 2.0, hub_y + 11, "Single Source of Truth (SSOT)", fontName="Helvetica-Oblique", fontSize=6.5, fillColor=COLOR_HAIRLINE, textAnchor="middle"))

    dev_w = 115.0
    dev_h = 40.0
    left_x = 18.0
    g.add(Rect(left_x, 75, dev_w, dev_h, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=0.8, rx=2, ry=2))
    g.add(String(left_x + dev_w / 2.0, 101, "Gian (Australia)", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK, textAnchor="middle"))
    g.add(String(left_x + dev_w / 2.0, 90, "Local Feature Commits", fontName="Helvetica", fontSize=6.5, fillColor=COLOR_DARK_GREY, textAnchor="middle"))
    g.add(String(left_x + dev_w / 2.0, 79, "Like Button & CSS", fontName="Helvetica-Oblique", fontSize=6.0, fillColor=COLOR_MUTED, textAnchor="middle"))

    g.add(Rect(left_x, 24, dev_w, dev_h, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=0.8, rx=2, ry=2))
    g.add(String(left_x + dev_w / 2.0, 50, "Shivam (India)", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK, textAnchor="middle"))
    g.add(String(left_x + dev_w / 2.0, 39, "Local Feature Commits", fontName="Helvetica", fontSize=6.5, fillColor=COLOR_DARK_GREY, textAnchor="middle"))
    g.add(String(left_x + dev_w / 2.0, 28, "Marquee & Routing", fontName="Helvetica-Oblique", fontSize=6.0, fillColor=COLOR_MUTED, textAnchor="middle"))

    right_x = TOTAL_WIDTH - 18.0 - dev_w
    g.add(Rect(right_x, 75, dev_w, dev_h, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=0.8, rx=2, ry=2))
    g.add(String(right_x + dev_w / 2.0, 101, "Nobita (India)", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK, textAnchor="middle"))
    g.add(String(right_x + dev_w / 2.0, 90, "Local Feature Commits", fontName="Helvetica", fontSize=6.5, fillColor=COLOR_DARK_GREY, textAnchor="middle"))
    g.add(String(right_x + dev_w / 2.0, 79, "Comment Engine & Auth", fontName="Helvetica-Oblique", fontSize=6.0, fillColor=COLOR_MUTED, textAnchor="middle"))

    g.add(Rect(right_x, 24, dev_w, dev_h, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=0.8, rx=2, ry=2))
    g.add(String(right_x + dev_w / 2.0, 50, "Ruchi (London)", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK, textAnchor="middle"))
    g.add(String(right_x + dev_w / 2.0, 39, "Local Feature Commits", fontName="Helvetica", fontSize=6.5, fillColor=COLOR_DARK_GREY, textAnchor="middle"))
    g.add(String(right_x + dev_w / 2.0, 28, "Footer & Analytics", fontName="Helvetica-Oblique", fontSize=6.0, fillColor=COLOR_MUTED, textAnchor="middle"))

    _draw_arrow(g, left_x + dev_w, 95, hub_x, 85, color=COLOR_CHARCOAL, stroke_width=0.8)
    _draw_arrow(g, hub_x, 80, left_x + dev_w, 90, color=COLOR_CHARCOAL, stroke_width=0.8)
    _draw_arrow(g, left_x + dev_w, 48, hub_x, 62, color=COLOR_CHARCOAL, stroke_width=0.8)
    _draw_arrow(g, hub_x, 57, left_x + dev_w, 43, color=COLOR_CHARCOAL, stroke_width=0.8)

    _draw_arrow(g, right_x, 95, hub_x + hub_w, 85, color=COLOR_CHARCOAL, stroke_width=0.8)
    _draw_arrow(g, hub_x + hub_w, 80, right_x, 90, color=COLOR_CHARCOAL, stroke_width=0.8)
    _draw_arrow(g, right_x, 48, hub_x + hub_w, 62, color=COLOR_CHARCOAL, stroke_width=0.8)
    _draw_arrow(g, hub_x + hub_w, 57, right_x, 43, color=COLOR_CHARCOAL, stroke_width=0.8)

    g.add(String(hub_x - 5, 87, "push/fetch", fontName="Courier-Oblique", fontSize=5.5, fillColor=COLOR_MUTED, textAnchor="end"))
    g.add(String(hub_x + hub_w + 5, 87, "push/fetch", fontName="Courier-Oblique", fontSize=5.5, fillColor=COLOR_MUTED, textAnchor="start"))

    g.add(
        String(
            TOTAL_WIDTH / 2.0,
            10.0,
            "INVARIANT: Offline commits synchronize via push/pull; zero peer-to-peer runtime dependency.",
            fontName="Helvetica-Bold",
            fontSize=6.5,
            fillColor=COLOR_BLACK,
            textAnchor="middle",
        )
    )

    return d


def create_two_pillars_diagram() -> Drawing:
    """The Two Pillars of Version Control: Local Workspace vs Distributed Collaboration."""
    height = 145.0
    d, g = _make_canvas_frame(
        height,
        "Figure 2.1: The Two Pillars of Version Control",
        "Pillar 1: Local Workspace Management vs Pillar 2: Distributed Collaboration",
    )

    card_w = 215.0
    card_h = 98.0
    y_card = 20.0

    x1 = 15.0
    g.add(Rect(x1, y_card, card_w, card_h, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.0, rx=3, ry=3))
    g.add(Rect(x1, y_card + card_h - 22, card_w, 22, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(String(x1 + 10, y_card + card_h - 14, "PILLAR 1: LOCAL WORKSPACE", fontName="Helvetica-Bold", fontSize=8.0, fillColor=COLOR_BLACK))
    g.add(String(x1 + card_w - 10, y_card + card_h - 14, "Git CLI (Offline)", fontName="Courier-Bold", fontSize=6.5, fillColor=COLOR_CHARCOAL, textAnchor="end"))

    g.add(String(x1 + 10, y_card + card_h - 34, "Scope: Single-Machine Offline Architecture", fontName="Helvetica-Bold", fontSize=7.0, fillColor=COLOR_DARK_GREY))
    g.add(Line(x1 + 10, y_card + card_h - 38, x1 + card_w - 10, y_card + card_h - 38, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))

    bullets1 = [
        ("Snapshot checkpoints", "git commit -m (DAG nodes)"),
        ("Multi-state staging index", "git add (proposed cache)"),
        ("Branch context isolation", "git switch / switch -c"),
        ("Graph temporal rewinds", "git reset / git restore"),
    ]
    for idx, (label, cmd) in enumerate(bullets1):
        by = y_card + card_h - 50 - idx * 12.5
        g.add(Rect(x1 + 10, by - 1, 4, 4, fillColor=COLOR_BLACK, strokeColor=None))
        g.add(String(x1 + 20, by, label, fontName="Helvetica-Bold", fontSize=6.5, fillColor=COLOR_CHARCOAL))
        g.add(String(x1 + card_w - 10, by, cmd, fontName="Courier", fontSize=6.0, fillColor=COLOR_MUTED, textAnchor="end"))

    x2 = TOTAL_WIDTH - 15.0 - card_w
    g.add(Rect(x2, y_card, card_w, card_h, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.0, rx=3, ry=3))
    g.add(Rect(x2, y_card + card_h - 22, card_w, 22, fillColor=COLOR_CHARCOAL, strokeColor=None))
    g.add(String(x2 + 10, y_card + card_h - 14, "PILLAR 2: DISTRIBUTED COLLABORATION", fontName="Helvetica-Bold", fontSize=8.0, fillColor=COLOR_WHITE))
    g.add(String(x2 + card_w - 10, y_card + card_h - 14, "GitHub Platform (Cloud)", fontName="Courier-Bold", fontSize=6.5, fillColor=COLOR_WHITE, textAnchor="end"))

    g.add(String(x2 + 10, y_card + card_h - 34, "Scope: Multi-Node Distributed Cloud Architecture", fontName="Helvetica-Bold", fontSize=7.0, fillColor=COLOR_DARK_GREY))
    g.add(Line(x2 + 10, y_card + card_h - 38, x2 + card_w - 10, y_card + card_h - 38, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))

    bullets2 = [
        ("Upstream tracking & remotes", "git push -u origin <branch>"),
        ("Asynchronous packet sync", "git fetch / git pull"),
        ("Code review & pull requests", "PR approvals & CI gatekeepers"),
        ("Team divergence resolution", "git merge / git rebase"),
    ]
    for idx, (label, cmd) in enumerate(bullets2):
        by = y_card + card_h - 50 - idx * 12.5
        g.add(Rect(x2 + 10, by - 1, 4, 4, fillColor=COLOR_CHARCOAL, strokeColor=None))
        g.add(String(x2 + 20, by, label, fontName="Helvetica-Bold", fontSize=6.5, fillColor=COLOR_CHARCOAL))
        g.add(String(x2 + card_w - 10, by, cmd, fontName="Courier", fontSize=6.0, fillColor=COLOR_MUTED, textAnchor="end"))

    g.add(
        String(
            TOTAL_WIDTH / 2.0,
            8.0,
            "PEDAGOGICAL RULE: Master Pillar 1 (Local State Machine) completely before tackling Pillar 2 (Remote Divergence).",
            fontName="Helvetica-Bold",
            fontSize=6.5,
            fillColor=COLOR_BLACK,
            textAnchor="middle",
        )
    )

    return d


def create_config_cascade_diagram() -> Drawing:
    """Git Configuration Precedence Cascade: Local > Global > System."""
    height = 115.0
    d, g = _make_canvas_frame(
        height,
        "Figure 3.1: Git Configuration Precedence Cascade",
        "Precedence Hierarchy: Local (.git/config) > Global (~/.gitconfig) > System (/etc/gitconfig)",
    )

    tiers = [
        ("SYSTEM LEVEL", "--system", "/etc/gitconfig", "All OS Users & Repos", COLOR_BG_BOX, COLOR_MUTED),
        ("GLOBAL LEVEL", "--global", "~/.gitconfig", "Current User (All Repos)", COLOR_BG_BOX, COLOR_CHARCOAL),
        ("LOCAL LEVEL", "--local (Default)", ".git/config", "Active Single Repo", COLOR_BG_SHADED, COLOR_BLACK),
        ("WORKTREE LEVEL", "--worktree", ".git/config.worktree", "Linked Worktree", COLOR_BG_BOX, COLOR_MUTED),
    ]

    tier_w = 95.0
    tier_h = 58.0
    gap = 14.0
    start_x = 22.0
    y_box = 28.0

    for idx, (title, flag, path, scope, fill, text_col) in enumerate(tiers):
        x = start_x + idx * (tier_w + gap)
        border_w = 1.2 if idx == 2 else 0.75
        border_col = COLOR_BLACK if idx == 2 else COLOR_DARK_GREY
        g.add(Rect(x, y_box, tier_w, tier_h, fillColor=fill, strokeColor=border_col, strokeWidth=border_w, rx=3, ry=3))
        g.add(Rect(x, y_box + tier_h - 14, tier_w, 14, fillColor=COLOR_BG_SHADED if idx != 2 else COLOR_CHARCOAL, strokeColor=None))
        header_fg = COLOR_WHITE if idx == 2 else COLOR_BLACK
        g.add(String(x + tier_w / 2.0, y_box + tier_h - 10, title, fontName="Helvetica-Bold", fontSize=6.5, fillColor=header_fg, textAnchor="middle"))
        g.add(String(x + tier_w / 2.0, y_box + 30, flag, fontName="Courier-Bold", fontSize=6.5, fillColor=text_col, textAnchor="middle"))
        g.add(String(x + tier_w / 2.0, y_box + 19, path, fontName="Courier", fontSize=5.5, fillColor=COLOR_MUTED, textAnchor="middle"))
        g.add(String(x + tier_w / 2.0, y_box + 8, scope, fontName="Helvetica-Oblique", fontSize=5.5, fillColor=COLOR_DARK_GREY, textAnchor="middle"))

        if idx < len(tiers) - 1:
            arrow_x = x + tier_w
            _draw_arrow(g, arrow_x + 2, y_box + tier_h / 2.0, arrow_x + gap - 2, y_box + tier_h / 2.0, color=COLOR_BLACK, stroke_width=1.0)
            g.add(String(arrow_x + gap / 2.0, y_box + tier_h / 2.0 + 4, "wins", fontName="Helvetica-Oblique", fontSize=5.0, fillColor=COLOR_MUTED, textAnchor="middle"))

    g.add(
        String(
            TOTAL_WIDTH / 2.0,
            10.0,
            "CASCADE RULE: More specific configuration strictly overrides general configuration. Local repository always wins.",
            fontName="Helvetica-Bold",
            fontSize=6.5,
            fillColor=COLOR_BLACK,
            textAnchor="middle",
        )
    )

    return d


def create_file_lifecycle_diagram() -> Drawing:
    """Git File Lifecycle State Machine: Untracked -> Staged -> Committed -> Modified."""
    height = 150.0
    d, g = _make_canvas_frame(
        height,
        "Figure 4.2: Git File Lifecycle State Machine",
        "Untracked, Staged (Index), Committed (Clean), and Modified (Dirty) Transitions",
    )

    node_w = 95.0
    node_h = 42.0

    x_untracked = 15.0
    y_top = 70.0
    g.add(Rect(x_untracked, y_top, node_w, node_h, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.0, rx=3, ry=3))
    g.add(String(x_untracked + node_w / 2.0, y_top + 28, "UNTRACKED", fontName="Helvetica-Bold", fontSize=8.0, fillColor=COLOR_BLACK, textAnchor="middle"))
    g.add(String(x_untracked + node_w / 2.0, y_top + 16, "Badge '??' / 'U'", fontName="Courier-Bold", fontSize=6.5, fillColor=COLOR_DARK_GREY, textAnchor="middle"))
    g.add(String(x_untracked + node_w / 2.0, y_top + 6, "New file on disk only", fontName="Helvetica-Oblique", fontSize=5.5, fillColor=COLOR_MUTED, textAnchor="middle"))

    x_staged = 190.0
    g.add(Rect(x_staged, y_top, node_w, node_h, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_BLACK, strokeWidth=1.2, rx=3, ry=3))
    g.add(String(x_staged + node_w / 2.0, y_top + 28, "STAGED (INDEX)", fontName="Helvetica-Bold", fontSize=8.0, fillColor=COLOR_BLACK, textAnchor="middle"))
    g.add(String(x_staged + node_w / 2.0, y_top + 16, "Badge 'A ' / 'M '", fontName="Courier-Bold", fontSize=6.5, fillColor=COLOR_BLACK, textAnchor="middle"))
    g.add(String(x_staged + node_w / 2.0, y_top + 6, "Proposed commit snapshot", fontName="Helvetica-Oblique", fontSize=5.5, fillColor=COLOR_DARK_GREY, textAnchor="middle"))

    x_committed = 365.0
    g.add(Rect(x_committed, y_top, node_w, node_h, fillColor=COLOR_CHARCOAL, strokeColor=COLOR_BLACK, strokeWidth=1.0, rx=3, ry=3))
    g.add(String(x_committed + node_w / 2.0, y_top + 28, "COMMITTED", fontName="Helvetica-Bold", fontSize=8.0, fillColor=COLOR_WHITE, textAnchor="middle"))
    g.add(String(x_committed + node_w / 2.0, y_top + 16, "Clean / Zero Diff", fontName="Courier-Bold", fontSize=6.5, fillColor=COLOR_WHITE, textAnchor="middle"))
    g.add(String(x_committed + node_w / 2.0, y_top + 6, "Permanent in DAG", fontName="Helvetica-Oblique", fontSize=5.5, fillColor=COLOR_HAIRLINE, textAnchor="middle"))

    y_bot = 16.0
    x_mod = 190.0
    g.add(Rect(x_mod, y_bot, node_w, node_h, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.0, rx=3, ry=3))
    g.add(String(x_mod + node_w / 2.0, y_bot + 28, "MODIFIED (DIRTY)", fontName="Helvetica-Bold", fontSize=8.0, fillColor=COLOR_BLACK, textAnchor="middle"))
    g.add(String(x_mod + node_w / 2.0, y_bot + 16, "Badge ' M' (Unstaged)", fontName="Courier-Bold", fontSize=6.5, fillColor=COLOR_DARK_GREY, textAnchor="middle"))
    g.add(String(x_mod + node_w / 2.0, y_bot + 6, "Edited on disk after commit", fontName="Helvetica-Oblique", fontSize=5.5, fillColor=COLOR_MUTED, textAnchor="middle"))

    _draw_arrow(g, x_untracked + node_w, y_top + 22, x_staged, y_top + 22, color=COLOR_BLACK, stroke_width=1.0)
    g.add(String((x_untracked + node_w + x_staged) / 2.0, y_top + 26, "git add", fontName="Courier-Bold", fontSize=6.5, fillColor=COLOR_BLACK, textAnchor="middle"))

    _draw_arrow(g, x_staged + node_w, y_top + 22, x_committed, y_top + 22, color=COLOR_BLACK, stroke_width=1.0)
    g.add(String((x_staged + node_w + x_committed) / 2.0, y_top + 26, "git commit", fontName="Courier-Bold", fontSize=6.5, fillColor=COLOR_BLACK, textAnchor="middle"))

    g.add(Line(x_committed + node_w / 2.0, y_top, x_committed + node_w / 2.0, y_bot + node_h / 2.0, strokeColor=COLOR_DARK_GREY, strokeWidth=0.8))
    _draw_arrow(g, x_committed + node_w / 2.0, y_bot + node_h / 2.0, x_mod + node_w, y_bot + node_h / 2.0, color=COLOR_DARK_GREY, stroke_width=0.8)
    g.add(String(x_committed + node_w / 2.0 + 4, (y_top + y_bot) / 2.0 + 10, "edit file", fontName="Helvetica-Oblique", fontSize=6.0, fillColor=COLOR_MUTED))

    _draw_arrow(g, x_mod + 35, y_bot + node_h, x_mod + 35, y_top, color=COLOR_BLACK, stroke_width=1.0)
    g.add(String(x_mod + 38, (y_bot + node_h + y_top) / 2.0, "git add", fontName="Courier-Bold", fontSize=6.0, fillColor=COLOR_BLACK))

    _draw_arrow(g, x_mod + 75, y_top, x_mod + 75, y_bot + node_h, color=COLOR_MUTED, stroke_width=0.8)
    g.add(String(x_mod + 78, (y_bot + node_h + y_top) / 2.0, "restore --staged", fontName="Courier", fontSize=5.0, fillColor=COLOR_MUTED))

    return d


def create_git_objects_table_diagram() -> Drawing:
    """The Four Fundamental Git Objects: blob, tree, commit, tag."""
    height = 135.0
    d, g = _make_canvas_frame(
        height,
        "Figure 5.2: The Four Fundamental Git Objects",
        "Immutable Content-Addressable Storage Architecture (.git/objects/)",
    )

    y_header = 92.0
    row_h = 20.0

    g.add(Rect(15, y_header, 445, 18, fillColor=COLOR_CHARCOAL, strokeColor=COLOR_BLACK, strokeWidth=0.75))
    g.add(String(25, y_header + 5, "OBJECT TYPE", fontName="Helvetica-Bold", fontSize=7.0, fillColor=COLOR_WHITE))
    g.add(String(95, y_header + 5, "INTERNAL PAYLOAD STRUCTURE", fontName="Helvetica-Bold", fontSize=7.0, fillColor=COLOR_WHITE))
    g.add(String(285, y_header + 5, "METADATA & ATTRIBUTES STORED", fontName="Helvetica-Bold", fontSize=7.0, fillColor=COLOR_WHITE))

    rows = [
        ("blob", "Raw zlib-compressed file byte stream", "Zero! No filename, no permissions, no timestamp."),
        ("tree", "Directory entries: <mode> <type> <sha-1> <name>", "Preserves directory hierarchy, permissions, names."),
        ("commit", "Root Tree SHA, Parent SHA(s), Author, Committer, Msg", "Permanent immutable snapshot node in DAG history."),
        ("tag", "Target Commit SHA, Type, Tagger Name/Email, Timestamp", "Explicit release milestone pointer (e.g. v1.0.0)."),
    ]

    for idx, (obj_type, payload, meta) in enumerate(rows):
        y = y_header - (idx + 1) * row_h
        bg = COLOR_BG_BOX if idx % 2 == 0 else COLOR_BG_LIGHT
        g.add(Rect(15, y, 445, row_h, fillColor=bg, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))

        g.add(Rect(22, y + 3, 45, 14, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_DARK_GREY, strokeWidth=0.5, rx=2, ry=2))
        g.add(String(44.5, y + 7, obj_type, fontName="Courier-Bold", fontSize=7.0, fillColor=COLOR_BLACK, textAnchor="middle"))

        g.add(String(95, y + 7, payload, fontName="Courier", fontSize=6.0, fillColor=COLOR_CHARCOAL))
        g.add(String(285, y + 7, meta, fontName="Helvetica", fontSize=6.0, fillColor=COLOR_DARK_GREY))

    g.add(
        String(
            TOTAL_WIDTH / 2.0,
            8.0,
            "INVARIANT: All objects are cryptographically indexed by SHA-1 hash: '<type> <size>\\0<payload>'.",
            fontName="Helvetica-Bold",
            fontSize=6.5,
            fillColor=COLOR_BLACK,
            textAnchor="middle",
        )
    )

    return d


def create_status_decode_matrix_diagram() -> Drawing:
    """Two-Column Git Status Decoding Matrix (git status -s)."""
    height = 185.0
    d, g = _make_canvas_frame(
        height,
        "Figure 7.2: Two-Column Git Status Decoding Matrix",
        "Short Format (git status -s): Position 1 (Index vs HEAD) | Position 2 (Working Tree vs Index)",
    )

    y_header = 142.0
    row_h = 16.0

    g.add(Rect(15, y_header, 445, 18, fillColor=COLOR_CHARCOAL, strokeColor=COLOR_BLACK, strokeWidth=0.75))
    g.add(String(25, y_header + 5, "FLAG", fontName="Helvetica-Bold", fontSize=7.0, fillColor=COLOR_WHITE))
    g.add(String(75, y_header + 5, "POS 1: INDEX vs HEAD (STAGED)", fontName="Helvetica-Bold", fontSize=7.0, fillColor=COLOR_WHITE))
    g.add(String(260, y_header + 5, "POS 2: WORKING TREE vs INDEX (UNSTAGED)", fontName="Helvetica-Bold", fontSize=7.0, fillColor=COLOR_WHITE))

    matrix_rows = [
        ("??", "[Space] File not in Index", "Untracked new file on physical disk"),
        ("A ", "New file staged in Index", "Clean (matches Index snapshot)"),
        (" M", "Clean in Index (matches HEAD)", "Modified on disk (unstaged changes)"),
        ("AM", "New file staged in Index", "Modified AGAIN on disk after staging!"),
        ("M ", "File modification staged in Index", "Clean (matches Index snapshot)"),
        ("MM", "File modification staged in Index", "Modified AGAIN on disk after staging!"),
        ("D ", "File deletion staged in Index", "Clean in working tree (deleted on disk)"),
        ("UU", "Unmerged path (Conflict in Index!)", "Unmerged path (Conflict in Working Tree!)"),
    ]

    for idx, (flag, col1, col2) in enumerate(matrix_rows):
        y = y_header - (idx + 1) * row_h
        bg = COLOR_BG_BOX if idx % 2 == 0 else COLOR_BG_LIGHT
        g.add(Rect(15, y, 445, row_h, fillColor=bg, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))

        flag_bg = COLOR_CHARCOAL if flag == "UU" else COLOR_BG_SHADED
        flag_fg = COLOR_WHITE if flag == "UU" else COLOR_BLACK
        g.add(Rect(22, y + 2, 28, 12, fillColor=flag_bg, strokeColor=COLOR_DARK_GREY, strokeWidth=0.5, rx=2, ry=2))
        g.add(String(36, y + 5, flag, fontName="Courier-Bold", fontSize=6.5, fillColor=flag_fg, textAnchor="middle"))

        g.add(String(75, y + 5, col1, fontName="Helvetica-Bold" if "staged" in col1.lower() else "Helvetica", fontSize=6.5, fillColor=COLOR_CHARCOAL))
        
        warn_col = COLOR_BLACK if "AGAIN" in col2 or "Conflict" in col2 else COLOR_DARK_GREY
        g.add(String(260, y + 5, col2, fontName="Helvetica-Bold" if "AGAIN" in col2 or "Conflict" in col2 else "Helvetica", fontSize=6.5, fillColor=warn_col))

    g.add(
        String(
            TOTAL_WIDTH / 2.0,
            8.0,
            "CRITICAL GOTCHA: 'AM' / 'MM' indicates staged edits will be committed, but subsequent disk edits remain unstaged.",
            fontName="Helvetica-Bold",
            fontSize=6.5,
            fillColor=COLOR_BLACK,
            textAnchor="middle",
        )
    )

    return d


def create_three_tree_pipeline_diagram() -> Drawing:
    """Three-Tree Data Flow Pipeline: Working Directory -> Staging Index -> HEAD Repository."""
    height = 145.0
    d, g = _make_canvas_frame(
        height,
        "Figure 7.3: Three-Tree Transition & Command Pipeline",
        "Data Flow Across Working Directory, Staging Index, and HEAD Repository",
    )

    col_w = 125.0
    col_h = 70.0
    y_col = 32.0

    x1 = 15.0
    g.add(Rect(x1, y_col, col_w, col_h, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.0, rx=3, ry=3))
    g.add(String(x1 + col_w / 2.0, y_col + col_h - 14, "WORKING DIRECTORY", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK, textAnchor="middle"))
    g.add(String(x1 + col_w / 2.0, y_col + col_h - 26, "(Physical Disk Files)", fontName="Helvetica-Oblique", fontSize=6.5, fillColor=COLOR_MUTED, textAnchor="middle"))
    g.add(Line(x1, y_col + col_h - 30, x1 + col_w, y_col + col_h - 30, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(String(x1 + col_w / 2.0, y_col + 24, "Real OS File System", fontName="Helvetica", fontSize=6.5, fillColor=COLOR_CHARCOAL, textAnchor="middle"))
    g.add(String(x1 + col_w / 2.0, y_col + 12, "Unstaged & Dirty Edits", fontName="Courier", fontSize=6.0, fillColor=COLOR_DARK_GREY, textAnchor="middle"))

    x2 = 175.0
    g.add(Rect(x2, y_col, col_w, col_h, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_BLACK, strokeWidth=1.2, rx=3, ry=3))
    g.add(String(x2 + col_w / 2.0, y_col + col_h - 14, "STAGING INDEX", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK, textAnchor="middle"))
    g.add(String(x2 + col_w / 2.0, y_col + col_h - 26, "(.git/index Binary Cache)", fontName="Helvetica-Oblique", fontSize=6.5, fillColor=COLOR_MUTED, textAnchor="middle"))
    g.add(Line(x2, y_col + col_h - 30, x2 + col_w, y_col + col_h - 30, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
    g.add(String(x2 + col_w / 2.0, y_col + 24, "Prepared Commit Snapshot", fontName="Helvetica", fontSize=6.5, fillColor=COLOR_CHARCOAL, textAnchor="middle"))
    g.add(String(x2 + col_w / 2.0, y_col + 12, "SHA-1 / Stat Cache", fontName="Courier", fontSize=6.0, fillColor=COLOR_DARK_GREY, textAnchor="middle"))

    x3 = 335.0
    g.add(Rect(x3, y_col, col_w, col_h, fillColor=COLOR_CHARCOAL, strokeColor=COLOR_BLACK, strokeWidth=1.0, rx=3, ry=3))
    g.add(String(x3 + col_w / 2.0, y_col + col_h - 14, "HEAD REPOSITORY", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_WHITE, textAnchor="middle"))
    g.add(String(x3 + col_w / 2.0, y_col + col_h - 26, "(.git/objects/ Immutable DAG)", fontName="Helvetica-Oblique", fontSize=6.5, fillColor=COLOR_HAIRLINE, textAnchor="middle"))
    g.add(Line(x3, y_col + col_h - 30, x3 + col_w, y_col + col_h - 30, strokeColor=COLOR_DARK_GREY, strokeWidth=0.5))
    g.add(String(x3 + col_w / 2.0, y_col + 24, "Permanent Commit Objects", fontName="Helvetica", fontSize=6.5, fillColor=COLOR_WHITE, textAnchor="middle"))
    g.add(String(x3 + col_w / 2.0, y_col + 12, "Branch Pointer Targets", fontName="Courier", fontSize=6.0, fillColor=COLOR_HAIRLINE, textAnchor="middle"))

    _draw_arrow(g, x1 + col_w, y_col + 50, x2, y_col + 50, color=COLOR_BLACK, stroke_width=1.0)
    g.add(String((x1 + col_w + x2) / 2.0, y_col + 55, "git add", fontName="Courier-Bold", fontSize=6.5, fillColor=COLOR_BLACK, textAnchor="middle"))

    _draw_arrow(g, x2 + col_w, y_col + 50, x3, y_col + 50, color=COLOR_BLACK, stroke_width=1.0)
    g.add(String((x2 + col_w + x3) / 2.0, y_col + 55, "git commit", fontName="Courier-Bold", fontSize=6.5, fillColor=COLOR_BLACK, textAnchor="middle"))

    _draw_arrow(g, x3, y_col + 32, x2 + col_w, y_col + 32, color=COLOR_CHARCOAL, stroke_width=0.8)
    g.add(String((x2 + col_w + x3) / 2.0, y_col + 23, "restore --staged", fontName="Courier", fontSize=5.5, fillColor=COLOR_CHARCOAL, textAnchor="middle"))

    _draw_arrow(g, x2, y_col + 32, x1 + col_w, y_col + 32, color=COLOR_CHARCOAL, stroke_width=0.8)
    g.add(String((x1 + col_w + x2) / 2.0, y_col + 23, "restore <file>", fontName="Courier", fontSize=5.5, fillColor=COLOR_CHARCOAL, textAnchor="middle"))

    g.add(
        String(
            TOTAL_WIDTH / 2.0,
            10.0,
            "DESTRUCTIVE OVERRIDE: 'git reset --hard' overwrites both Staging Index and Working Directory to match HEAD.",
            fontName="Helvetica-Bold",
            fontSize=6.5,
            fillColor=COLOR_BLACK,
            textAnchor="middle",
        )
    )

    return d


def create_commit_dag_topology_diagram() -> Drawing:
    """Directed Acyclic Graph (DAG) commit topology with backward parent pointers."""
    height = 145.0
    d, g = _make_canvas_frame(
        height,
        "Figure 8.1: Commit Directed Acyclic Graph (DAG) Topology",
        "Child Commits Reference Immutable Parent SHAs (Time Flows Past ← Present)",
    )

    y_main = 85.0
    y_branch = 38.0

    main_commits = [("C0", 35.0, "(Root)"), ("C1", 115.0, "init"), ("C2", 195.0, "LCA"), ("C3", 285.0, "feat")]
    for name, x, tag in main_commits:
        g.add(Rect(x, y_main - 12, 42, 24, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.0, rx=2, ry=2))
        g.add(String(x + 21, y_main - 2, name, fontName="Helvetica-Bold", fontSize=8.5, fillColor=COLOR_BLACK, textAnchor="middle"))
        g.add(String(x + 21, y_main + 16, tag, fontName="Courier-Oblique", fontSize=5.5, fillColor=COLOR_MUTED, textAnchor="middle"))

    _draw_arrow(g, 115, y_main, 77, y_main, color=COLOR_BLACK, stroke_width=1.0)
    _draw_arrow(g, 195, y_main, 157, y_main, color=COLOR_BLACK, stroke_width=1.0)
    _draw_arrow(g, 285, y_main, 237, y_main, color=COLOR_BLACK, stroke_width=1.0)

    g.add(Rect(345, y_main - 11, 48, 22, fillColor=COLOR_CHARCOAL, strokeColor=COLOR_BLACK, strokeWidth=0.8, rx=2, ry=2))
    g.add(String(369, y_main - 3, "main", fontName="Courier-Bold", fontSize=7.5, fillColor=COLOR_WHITE, textAnchor="middle"))
    _draw_arrow(g, 345, y_main, 327, y_main, color=COLOR_CHARCOAL, stroke_width=0.8)

    g.add(Rect(410, y_main - 11, 48, 22, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_BLACK, strokeWidth=1.0, rx=2, ry=2))
    g.add(String(434, y_main - 3, "HEAD", fontName="Courier-Bold", fontSize=7.5, fillColor=COLOR_BLACK, textAnchor="middle"))
    _draw_arrow(g, 410, y_main, 393, y_main, color=COLOR_BLACK, stroke_width=0.8)

    branch_commits = [("C4", 255.0, "nav-ui"), ("C5", 340.0, "nav-css")]
    for name, x, tag in branch_commits:
        g.add(Rect(x, y_branch - 12, 42, 24, fillColor=COLOR_BG_BOX, strokeColor=COLOR_DARK_GREY, strokeWidth=1.0, rx=2, ry=2))
        g.add(String(x + 21, y_branch - 2, name, fontName="Helvetica-Bold", fontSize=8.5, fillColor=COLOR_BLACK, textAnchor="middle"))
        g.add(String(x + 21, y_branch + 16, tag, fontName="Courier-Oblique", fontSize=5.5, fillColor=COLOR_MUTED, textAnchor="middle"))

    _draw_arrow(g, 340, y_branch, 297, y_branch, color=COLOR_CHARCOAL, stroke_width=1.0)
    _draw_arrow(g, 255, y_branch + 4, 225, y_main - 12, color=COLOR_CHARCOAL, stroke_width=1.0)

    g.add(Rect(398, y_branch - 11, 68, 22, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_DARK_GREY, strokeWidth=0.8, rx=2, ry=2))
    g.add(String(432, y_branch - 3, "feature/navbar", fontName="Courier-Bold", fontSize=6.5, fillColor=COLOR_CHARCOAL, textAnchor="middle"))
    _draw_arrow(g, 398, y_branch, 382, y_branch, color=COLOR_CHARCOAL, stroke_width=0.8)

    g.add(
        String(
            TOTAL_WIDTH / 2.0,
            10.0,
            "INVARIANT: Edges point backward in time (Child → Parent). Branches are lightweight pointers, not containers.",
            fontName="Helvetica-Bold",
            fontSize=6.5,
            fillColor=COLOR_BLACK,
            textAnchor="middle",
        )
    )

    return d


def create_production_branching_diagram() -> Drawing:
    """Production Feature Branch Isolation Architecture (abcd.com)."""
    height = 145.0
    d, g = _make_canvas_frame(
        height,
        "Figure 8.3: Production Branch Isolation Architecture",
        "Production abcd.com Baseline vs Feature Navbar (Shivam) & Feature Footer (Ruchi)",
    )

    prod_w = 200.0
    prod_h = 42.0
    prod_x = (TOTAL_WIDTH - prod_w) / 2.0
    prod_y = 74.0
    g.add(Rect(prod_x, prod_y, prod_w, prod_h, fillColor=COLOR_CHARCOAL, strokeColor=COLOR_BLACK, strokeWidth=1.2, rx=3, ry=3))
    g.add(String(TOTAL_WIDTH / 2.0, prod_y + 28, "Production: abcd.com (32 lines)", fontName="Helvetica-Bold", fontSize=8.0, fillColor=COLOR_WHITE, textAnchor="middle"))
    g.add(String(TOTAL_WIDTH / 2.0, prod_y + 16, "Stable main branch (Zero Crash Tolerance)", fontName="Courier-Bold", fontSize=6.5, fillColor=COLOR_WHITE, textAnchor="middle"))
    g.add(String(TOTAL_WIDTH / 2.0, prod_y + 6, "Single Source of Truth for Live Deployment", fontName="Helvetica-Oblique", fontSize=5.5, fillColor=COLOR_HAIRLINE, textAnchor="middle"))

    side_w = 205.0
    side_h = 46.0
    x_left = 18.0
    y_bot = 16.0
    g.add(Rect(x_left, y_bot, side_w, side_h, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.0, rx=3, ry=3))
    g.add(String(x_left + side_w / 2.0, y_bot + 34, "Shivam: feature/navbar", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK, textAnchor="middle"))
    g.add(String(x_left + side_w / 2.0, y_bot + 22, "Diverges from Line 32 • Writes 100 new lines (132 total)", fontName="Helvetica", fontSize=6.0, fillColor=COLOR_CHARCOAL, textAnchor="middle"))
    g.add(String(x_left + side_w / 2.0, y_bot + 10, "CONTAINS EXPERIMENTAL BUGS! Isolated safely.", fontName="Courier-Bold", fontSize=5.5, fillColor=COLOR_DARK_GREY, textAnchor="middle"))

    x_right = TOTAL_WIDTH - 18.0 - side_w
    g.add(Rect(x_right, y_bot, side_w, side_h, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.0, rx=3, ry=3))
    g.add(String(x_right + side_w / 2.0, y_bot + 34, "Ruchi: feature/footer", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK, textAnchor="middle"))
    g.add(String(x_right + side_w / 2.0, y_bot + 22, "Diverges from Line 32 • Writes 200 new lines (232 total)", fontName="Helvetica", fontSize=6.0, fillColor=COLOR_CHARCOAL, textAnchor="middle"))
    g.add(String(x_right + side_w / 2.0, y_bot + 10, "CLEAN TESTED CODE • Ready for PR gatekeeper review.", fontName="Courier-Bold", fontSize=5.5, fillColor=COLOR_CHARCOAL, textAnchor="middle"))

    _draw_arrow(g, prod_x + 35, prod_y, x_left + side_w * 0.7, y_bot + side_h, color=COLOR_CHARCOAL, stroke_width=1.0)
    _draw_arrow(g, prod_x + prod_w - 35, prod_y, x_right + side_w * 0.3, y_bot + side_h, color=COLOR_CHARCOAL, stroke_width=1.0)

    g.add(String(prod_x + 20, prod_y - 10, "git switch -c feature/navbar", fontName="Courier", fontSize=5.5, fillColor=COLOR_MUTED))
    g.add(String(prod_x + prod_w - 20, prod_y - 10, "git switch -c feature/footer", fontName="Courier", fontSize=5.5, fillColor=COLOR_MUTED, textAnchor="end"))

    return d


def create_detached_head_hazard_diagram() -> Drawing:
    """Detached HEAD State and Orphan Commit Garbage Collection Hazard."""
    height = 145.0
    d, g = _make_canvas_frame(
        height,
        "Figure 8.4: Detached HEAD State & The Orphan Commit Hazard",
        "HEAD points directly to Commit SHA instead of a Branch Reference Pointer",
    )

    y_main = 85.0
    y_orphan = 35.0

    commits_main = [("C0", 35.0), ("C1", 115.0), ("C2", 195.0)]
    for name, x in commits_main:
        g.add(Rect(x, y_main - 12, 42, 24, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.0, rx=2, ry=2))
        g.add(String(x + 21, y_main - 2, name, fontName="Helvetica-Bold", fontSize=8.5, fillColor=COLOR_BLACK, textAnchor="middle"))

    _draw_arrow(g, 115, y_main, 77, y_main, color=COLOR_BLACK, stroke_width=1.0)
    _draw_arrow(g, 195, y_main, 157, y_main, color=COLOR_BLACK, stroke_width=1.0)

    g.add(Rect(245, y_main - 11, 45, 22, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_BLACK, strokeWidth=1.0, rx=2, ry=2))
    g.add(String(267.5, y_main - 3, "main", fontName="Courier-Bold", fontSize=7.5, fillColor=COLOR_BLACK, textAnchor="middle"))
    _draw_arrow(g, 245, y_main, 237, y_main, color=COLOR_BLACK, stroke_width=0.8)

    g.add(Rect(260, y_orphan - 16, 195, 38, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_DARK_GREY, strokeWidth=0.8, strokeDashArray=[2, 2], rx=3, ry=3))
    g.add(String(357.5, y_orphan + 14, "UNREFERENCED ORPHAN COMMITS", fontName="Helvetica-Bold", fontSize=6.0, fillColor=COLOR_DARK_GREY, textAnchor="middle"))

    g.add(Rect(275, y_orphan - 10, 38, 20, fillColor=COLOR_BG_BOX, strokeColor=COLOR_DARK_GREY, strokeWidth=0.8, rx=2, ry=2))
    g.add(String(294, y_orphan - 2, "C3", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK, textAnchor="middle"))

    g.add(Rect(345, y_orphan - 10, 38, 20, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.2, rx=2, ry=2))
    g.add(String(364, y_orphan - 2, "C4", fontName="Helvetica-Bold", fontSize=7.5, fillColor=COLOR_BLACK, textAnchor="middle"))

    _draw_arrow(g, 345, y_orphan, 313, y_orphan, color=COLOR_CHARCOAL, stroke_width=0.8)
    _draw_arrow(g, 275, y_orphan + 5, 225, y_main - 12, color=COLOR_CHARCOAL, stroke_width=0.8)

    g.add(Rect(405, y_orphan - 10, 42, 20, fillColor=COLOR_CHARCOAL, strokeColor=COLOR_BLACK, strokeWidth=1.0, rx=2, ry=2))
    g.add(String(426, y_orphan - 2, "HEAD", fontName="Courier-Bold", fontSize=7.0, fillColor=COLOR_WHITE, textAnchor="middle"))
    _draw_arrow(g, 405, y_orphan, 383, y_orphan, color=COLOR_CHARCOAL, stroke_width=0.8)

    g.add(
        String(
            TOTAL_WIDTH / 2.0,
            8.0,
            "HAZARD: Switching away from detached HEAD leaves C3/C4 unreferenced; git gc will purge them! Rescue: 'git switch -c rescue'.",
            fontName="Helvetica-Bold",
            fontSize=6.0,
            fillColor=COLOR_BLACK,
            textAnchor="middle",
        )
    )

    return d


def create_commands_matrix_diagram() -> Drawing:
    """Master Production Diagnostic Commands Matrix."""
    height = 215.0
    d, g = _make_canvas_frame(
        height,
        "Figure 15.2: Master Diagnostic Commands Matrix",
        "Essential Production CLI Diagnostics for Staging, Inspection, Graphing & Recovery",
    )

    y_header = 178.0
    row_h = 12.5

    g.add(Rect(15, y_header, 445, 14, fillColor=COLOR_CHARCOAL, strokeColor=COLOR_BLACK, strokeWidth=0.75))
    g.add(String(25, y_header + 4, "OBJECTIVE / DIAGNOSTIC TASK", fontName="Helvetica-Bold", fontSize=7.0, fillColor=COLOR_WHITE))
    g.add(String(245, y_header + 4, "PRODUCTION COMMAND", fontName="Helvetica-Bold", fontSize=7.0, fillColor=COLOR_WHITE))

    commands = [
        ("Inspect binary index staging cache", "git ls-files -s"),
        ("Resolve human ref to 40-char SHA", "git rev-parse HEAD"),
        ("View HEAD symbolic target branch", "git symbolic-ref HEAD"),
        ("Trace full local pointer movements", "git reflog show HEAD"),
        ("Audit unreferenced dangling objects", "git fsck --lost-found"),
        ("Find Lowest Common Ancestor (LCA)", "git merge-base branchA branchB"),
        ("Diff working tree against staging", "git diff"),
        ("Diff staging against HEAD commit", "git diff --staged"),
        ("Check for unresolved conflict markers", "git diff --check"),
        ("Safe force push verification", "git push --force-with-lease"),
        ("Rebase interactive clean up", "git rebase -i HEAD~N"),
        ("Abort failed merge operation", "git merge --abort"),
        ("Abort failed rebase operation", "git rebase --abort"),
    ]

    for idx, (objective, cmd) in enumerate(commands):
        y = y_header - (idx + 1) * row_h
        bg = COLOR_BG_BOX if idx % 2 == 0 else COLOR_BG_LIGHT
        g.add(Rect(15, y, 445, row_h, fillColor=bg, strokeColor=COLOR_HAIRLINE, strokeWidth=0.5))
        g.add(String(25, y + 3.0, objective, fontName="Helvetica", fontSize=6.0, fillColor=COLOR_CHARCOAL))
        g.add(String(245, y + 3.0, cmd, fontName="Courier-Bold", fontSize=6.0, fillColor=COLOR_BLACK))

    g.add(
        String(
            TOTAL_WIDTH / 2.0,
            5.0,
            "REFERENCE: Memorize these diagnostic commands for senior system audits and high-stakes production recovery.",
            fontName="Helvetica-Bold",
            fontSize=6.0,
            fillColor=COLOR_BLACK,
            textAnchor="middle",
        )
    )

    return d


def create_conflict_decision_tree_diagram() -> Drawing:
    """Merge Conflict Emergency Decision Tree: Source Code vs Dependency Lockfiles."""
    height = 175.0
    d, g = _make_canvas_frame(
        height,
        "Figure 15.3: Merge Conflict Emergency Decision Tree",
        "Deterministic Resolution Workflow for Source Code and Dependency Lockfiles",
    )

    top_w = 230.0
    top_h = 36.0
    top_x = (TOTAL_WIDTH - top_w) / 2.0
    top_y = 104.0
    g.add(Rect(top_x, top_y, top_w, top_h, fillColor=COLOR_CHARCOAL, strokeColor=COLOR_BLACK, strokeWidth=1.0, rx=3, ry=3))
    g.add(String(TOTAL_WIDTH / 2.0, top_y + 24, "MERGE CONFLICT TRIGGERED", fontName="Helvetica-Bold", fontSize=8.0, fillColor=COLOR_WHITE, textAnchor="middle"))
    g.add(String(TOTAL_WIDTH / 2.0, top_y + 13, "Inspect: git status -s (look for 'UU')", fontName="Courier", fontSize=6.5, fillColor=COLOR_WHITE, textAnchor="middle"))
    g.add(String(TOTAL_WIDTH / 2.0, top_y + 4, "Config: git config merge.conflictstyle diff3", fontName="Courier-Oblique", fontSize=5.5, fillColor=COLOR_HAIRLINE, textAnchor="middle"))

    card_w = 205.0
    card_h = 48.0
    x_left = 18.0
    y_card = 46.0
    g.add(Rect(x_left, y_card, card_w, card_h, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.0, rx=3, ry=3))
    g.add(String(x_left + card_w / 2.0, y_card + 36, "CODE FILE (.js, .py, .html, .ts)", fontName="Helvetica-Bold", fontSize=7.0, fillColor=COLOR_BLACK, textAnchor="middle"))
    g.add(String(x_left + 10, y_card + 25, "1. Open in VS Code 3-Way Merge Resolver", fontName="Helvetica", fontSize=6.0, fillColor=COLOR_CHARCOAL))
    g.add(String(x_left + 10, y_card + 15, "2. Compare: Ours vs Ancestor Base vs Theirs", fontName="Helvetica", fontSize=6.0, fillColor=COLOR_CHARCOAL))
    g.add(String(x_left + 10, y_card + 5, "3. Stage resolved file: git add <file>", fontName="Courier-Bold", fontSize=6.0, fillColor=COLOR_BLACK))

    x_right = TOTAL_WIDTH - 18.0 - card_w
    g.add(Rect(x_right, y_card, card_w, card_h, fillColor=COLOR_BG_BOX, strokeColor=COLOR_BLACK, strokeWidth=1.0, rx=3, ry=3))
    g.add(String(x_right + card_w / 2.0, y_card + 36, "DEPENDENCY LOCKFILE (package-lock, etc.)", fontName="Helvetica-Bold", fontSize=7.0, fillColor=COLOR_BLACK, textAnchor="middle"))
    g.add(String(x_right + 10, y_card + 25, "1. NEVER edit auto-generated lockfiles manually!", fontName="Helvetica-Bold", fontSize=6.0, fillColor=COLOR_CHARCOAL))
    g.add(String(x_right + 10, y_card + 15, "2. git checkout --theirs <lockfile>", fontName="Courier-Bold", fontSize=6.0, fillColor=COLOR_BLACK))
    g.add(String(x_right + 10, y_card + 5, "3. Regenerate & verify: npm install / cargo check", fontName="Courier", fontSize=6.0, fillColor=COLOR_CHARCOAL))

    bot_w = 240.0
    bot_h = 24.0
    bot_x = (TOTAL_WIDTH - bot_w) / 2.0
    bot_y = 12.0
    g.add(Rect(bot_x, bot_y, bot_w, bot_h, fillColor=COLOR_BG_SHADED, strokeColor=COLOR_BLACK, strokeWidth=1.0, rx=3, ry=3))
    g.add(String(TOTAL_WIDTH / 2.0, bot_y + 14, "Finalize: git commit -m \"merge: resolve integration\"", fontName="Courier-Bold", fontSize=6.5, fillColor=COLOR_BLACK, textAnchor="middle"))
    g.add(String(TOTAL_WIDTH / 2.0, bot_y + 4, "Emergency Escape / Abort: git merge --abort", fontName="Courier", fontSize=5.5, fillColor=COLOR_MUTED, textAnchor="middle"))

    _draw_arrow(g, top_x + 30, top_y, x_left + card_w / 2.0, y_card + card_h, color=COLOR_CHARCOAL, stroke_width=0.8)
    _draw_arrow(g, top_x + top_w - 30, top_y, x_right + card_w / 2.0, y_card + card_h, color=COLOR_CHARCOAL, stroke_width=0.8)
    _draw_arrow(g, x_left + card_w / 2.0, y_card, bot_x + 30, bot_y + bot_h, color=COLOR_CHARCOAL, stroke_width=0.8)
    _draw_arrow(g, x_right + card_w / 2.0, y_card, bot_x + bot_w - 30, bot_y + bot_h, color=COLOR_CHARCOAL, stroke_width=0.8)

    return d


DIAGRAM_REGISTRY = {
    "central_codebase": create_central_codebase_diagram,
    "cvcs_vs_dvcs": create_cvcs_vs_dvcs_diagram,
    "github_ssot_hub": create_github_ssot_hub_diagram,
    "two_pillars": create_two_pillars_diagram,
    "config_cascade": create_config_cascade_diagram,
    "file_lifecycle": create_file_lifecycle_diagram,
    "git_objects_table": create_git_objects_table_diagram,
    "status_decode_matrix": create_status_decode_matrix_diagram,
    "three_tree_pipeline": create_three_tree_pipeline_diagram,
    "commit_dag_topology": create_commit_dag_topology_diagram,
    "production_branching": create_production_branching_diagram,
    "detached_head_hazard": create_detached_head_hazard_diagram,
    "commands_matrix": create_commands_matrix_diagram,
    "conflict_decision_tree": create_conflict_decision_tree_diagram,
    "fork_upstream_workflow": create_fork_upstream_diagram,
    "git_vs_github": create_git_vs_github_diagram,
    "dot_git_internals": create_dot_git_internals_diagram,
    "trunk_vs_gitflow": create_trunk_vs_gitflow_diagram,
    "status_matrix": create_status_matrix_diagram,
    "collaboration_steps": create_collaboration_steps_diagram,
    "object_model": create_object_model_diagram,
    "three_trees": create_three_trees_diagram,
    "branching_dag": create_branching_dag_diagram,
    "three_way_merge": create_three_way_merge_diagram,
    "rebase_replay": create_rebase_replay_diagram,
    "remote_sync": create_remote_sync_diagram,
    "reset_matrix": create_reset_matrix_diagram,
    "index_binary": create_index_binary_diagram,
    "merge_conflict": create_merge_conflict_diagram,
    "sleep_architecture": create_sleep_architecture_diagram,
    "memory_transfer": create_memory_transfer_diagram,
    "adenosine_caffeine": create_adenosine_caffeine_diagram,
    "immune_killer_cells": create_immune_killer_cells_diagram,
    "thermal_circadian": create_thermal_circadian_diagram,
    "pfc_hippocampal_axis": create_pfc_hippocampal_axis_diagram,
    "neurochemical_surge": create_neurochemical_surge_diagram,
    "bdnf_neurogenesis": create_bdnf_neurogenesis_diagram,
    "bdnf_neurogenesis_cascade": create_bdnf_neurogenesis_diagram,
    "cognitive_reserve": create_cognitive_reserve_diagram,
    "cognitive_reserve_buffer": create_cognitive_reserve_diagram,
    "exercise_dosage": create_exercise_dosage_diagram,
    "exercise_dosage_matrix": create_exercise_dosage_diagram,
}


def get_diagram(diagram_name: str) -> Optional[Drawing]:
    """Retrieve a pre-built publication vector diagram by name."""
    builder = DIAGRAM_REGISTRY.get(diagram_name.strip().lower())
    if builder is not None:
        return builder()
    return None
