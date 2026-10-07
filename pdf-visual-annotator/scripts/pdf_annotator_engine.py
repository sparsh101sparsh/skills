"""
PDF Visual Annotator Engine
===========================
High-performance programmatic PDF vector diagramming, image annotations,
step-by-step DSA algorithm visualization, and 3D geometric shape rendering.

Powered by PyMuPDF (pymupdf).
"""

import math
from typing import List, Tuple, Dict, Any, Optional, Union
import pymupdf


# ==============================================================================
# 1. Color Utilities & Palettes
# ==============================================================================

RGBColor = Tuple[float, float, float]

PALETTE = {
    "primary": (0.12, 0.45, 0.85),       # Deep blue
    "secondary": (0.42, 0.25, 0.75),     # Purple
    "success": (0.15, 0.68, 0.38),       # Green
    "warning": (0.95, 0.60, 0.10),       # Orange
    "danger": (0.88, 0.22, 0.22),        # Red
    "info": (0.10, 0.65, 0.85),          # Cyan / Teal
    "neutral_dark": (0.15, 0.17, 0.20),  # Charcoal
    "neutral_light": (0.94, 0.95, 0.96), # Light gray
    "white": (1.0, 1.0, 1.0),
    "black": (0.0, 0.0, 0.0),
    "discarded": (0.85, 0.86, 0.88),     # Inactive array item
    "highlight_yellow": (1.0, 0.92, 0.3),
}


def hex_to_rgb(hex_code: str) -> RGBColor:
    """Convert hex string (e.g. '#1e70d6' or '1e70d6') to normalized RGB tuple (0.0 - 1.0)."""
    hex_clean = hex_code.lstrip("#")
    if len(hex_clean) != 6:
        raise ValueError(f"Invalid hex color code: {hex_code}")
    r = int(hex_clean[0:2], 16) / 255.0
    g = int(hex_clean[2:4], 16) / 255.0
    b = int(hex_clean[4:6], 16) / 255.0
    return (round(r, 4), round(g, 4), round(b, 4))


# ==============================================================================
# 2. PDFCanvas — Core Vector Drawing & Annotation Canvas
# ==============================================================================

class PDFCanvas:
    """
    High-level canvas wrapper over PyMuPDF documents and pages.
    Provides vector primitives, arrows, callouts, and image overlays.
    """

    def __init__(self, doc: Optional[pymupdf.Document] = None, page_index: int = 0):
        if doc is None:
            self.doc = pymupdf.open()
            self.page = self.doc.new_page(width=612, height=792)  # Standard Letter
        else:
            self.doc = doc
            if page_index < len(self.doc):
                self.page = self.doc[page_index]
            else:
                self.page = self.doc.new_page()
        self._shape: Optional[pymupdf.Shape] = None

    @classmethod
    def open(cls, pdf_path: str, page_index: int = 0) -> "PDFCanvas":
        """Open an existing PDF document."""
        doc = pymupdf.open(pdf_path)
        return cls(doc=doc, page_index=page_index)

    @classmethod
    def create(cls, width: float = 612, height: float = 792) -> "PDFCanvas":
        """Create a new blank PDF canvas."""
        doc = pymupdf.open()
        doc.new_page(width=width, height=height)
        return cls(doc=doc, page_index=0)

    @property
    def shape(self) -> pymupdf.Shape:
        """Lazy-initialize active shape canvas."""
        if self._shape is None:
            self._shape = self.page.new_shape()
        return self._shape

    def commit(self) -> None:
        """Commit active shape drawing buffer to the page."""
        if self._shape is not None:
            self._shape.commit()
            self._shape = None

    def save(self, output_path: str) -> None:
        """Commit pending drawings and save document to disk."""
        self.commit()
        self.doc.save(output_path)

    def close(self) -> None:
        """Close document."""
        self.doc.close()

    def select_page(self, page_index: int) -> None:
        """Switch active page."""
        self.commit()
        if 0 <= page_index < len(self.doc):
            self.page = self.doc[page_index]
        else:
            raise IndexError(f"Page index {page_index} out of range (0..{len(self.doc)-1})")

    def new_page(self, width: float = 612, height: float = 792) -> pymupdf.Page:
        """Append a new page and select it."""
        self.commit()
        self.page = self.doc.new_page(width=width, height=height)
        return self.page

    # --- Vector Drawing Primitives ---

    def draw_line(
        self,
        start: Union[pymupdf.Point, Tuple[float, float]],
        end: Union[pymupdf.Point, Tuple[float, float]],
        color: RGBColor = PALETTE["neutral_dark"],
        width: float = 1.5,
        dashes: Optional[str] = None,
        stroke_opacity: float = 1.0,
    ) -> None:
        """Draw a straight vector line."""
        p1 = pymupdf.Point(start)
        p2 = pymupdf.Point(end)
        self.shape.draw_line(p1, p2)
        self.shape.finish(
            color=color,
            width=width,
            dashes=dashes,
            stroke_opacity=stroke_opacity,
            closePath=False,
        )

    def draw_arrow(
        self,
        start: Union[pymupdf.Point, Tuple[float, float]],
        end: Union[pymupdf.Point, Tuple[float, float]],
        color: RGBColor = PALETTE["danger"],
        width: float = 2.0,
        head_len: float = 12.0,
        head_width: float = 6.0,
        dashes: Optional[str] = None,
        double_ended: bool = False,
    ) -> None:
        """Draw a precision vector arrow with a sharp triangular arrowhead."""
        p1 = pymupdf.Point(start)
        p2 = pymupdf.Point(end)

        dx = p2.x - p1.x
        dy = p2.y - p1.y
        length = math.hypot(dx, dy)
        if length == 0:
            return

        ux, uy = dx / length, dy / length
        perp_x, perp_y = -uy, ux

        # Arrow shaft
        self.shape.draw_line(p1, p2)
        self.shape.finish(color=color, width=width, dashes=dashes, closePath=False)

        # Arrowhead at 'end'
        left = pymupdf.Point(
            p2.x - head_len * ux + head_width * perp_x,
            p2.y - head_len * uy + head_width * perp_y,
        )
        right = pymupdf.Point(
            p2.x - head_len * ux - head_width * perp_x,
            p2.y - head_len * uy - head_width * perp_y,
        )
        self.shape.draw_polyline([left, p2, right, left])
        self.shape.finish(fill=color, color=color, closePath=True)

        # Optional head at 'start' (double-ended)
        if double_ended:
            s_left = pymupdf.Point(
                p1.x + head_len * ux + head_width * perp_x,
                p1.y + head_len * uy + head_width * perp_y,
            )
            s_right = pymupdf.Point(
                p1.x + head_len * ux - head_width * perp_x,
                p1.y + head_len * uy - head_width * perp_y,
            )
            self.shape.draw_polyline([s_left, p1, s_right, s_left])
            self.shape.finish(fill=color, color=color, closePath=True)

    def draw_curved_arrow(
        self,
        start: Union[pymupdf.Point, Tuple[float, float]],
        control: Union[pymupdf.Point, Tuple[float, float]],
        end: Union[pymupdf.Point, Tuple[float, float]],
        color: RGBColor = PALETTE["danger"],
        width: float = 2.0,
        head_len: float = 12.0,
        head_width: float = 6.0,
    ) -> None:
        """Draw a quadratic/Bézier curved arrow."""
        p1 = pymupdf.Point(start)
        pc = pymupdf.Point(control)
        p2 = pymupdf.Point(end)

        self.shape.draw_curve(p1, pc, p2)
        self.shape.finish(color=color, width=width, closePath=False)

        # Tangent vector at the end of quadratic Bézier curve: B'(1) = 2*(p2 - pc)
        dx = p2.x - pc.x
        dy = p2.y - pc.y
        length = math.hypot(dx, dy)
        if length == 0:
            return
        ux, uy = dx / length, dy / length
        perp_x, perp_y = -uy, ux

        left = pymupdf.Point(
            p2.x - head_len * ux + head_width * perp_x,
            p2.y - head_len * uy + head_width * perp_y,
        )
        right = pymupdf.Point(
            p2.x - head_len * ux - head_width * perp_x,
            p2.y - head_len * uy - head_width * perp_y,
        )
        self.shape.draw_polyline([left, p2, right, left])
        self.shape.finish(fill=color, color=color, closePath=True)

    def draw_rect(
        self,
        rect: Union[pymupdf.Rect, Tuple[float, float, float, float]],
        color: RGBColor = PALETTE["neutral_dark"],
        fill: Optional[RGBColor] = None,
        width: float = 1.5,
        fill_opacity: float = 1.0,
        stroke_opacity: float = 1.0,
        dashes: Optional[str] = None,
    ) -> None:
        """Draw a vector rectangle."""
        r = pymupdf.Rect(rect)
        self.shape.draw_rect(r)
        self.shape.finish(
            color=color,
            fill=fill,
            width=width,
            fill_opacity=fill_opacity,
            stroke_opacity=stroke_opacity,
            dashes=dashes,
            closePath=True,
        )

    def draw_circle(
        self,
        center: Union[pymupdf.Point, Tuple[float, float]],
        radius: float,
        color: RGBColor = PALETTE["neutral_dark"],
        fill: Optional[RGBColor] = None,
        width: float = 1.5,
        fill_opacity: float = 1.0,
    ) -> None:
        """Draw a vector circle."""
        pt = pymupdf.Point(center)
        self.shape.draw_circle(pt, radius)
        self.shape.finish(
            color=color,
            fill=fill,
            width=width,
            fill_opacity=fill_opacity,
            closePath=True,
        )

    def draw_highlight(
        self,
        rect: Union[pymupdf.Rect, Tuple[float, float, float, float]],
        fill_color: RGBColor = PALETTE["highlight_yellow"],
        opacity: float = 0.35,
        border: bool = True,
        border_color: RGBColor = PALETTE["warning"],
        border_width: float = 1.5,
    ) -> None:
        """Draw a translucent highlight bounding box (ideal for PDF images or code)."""
        r = pymupdf.Rect(rect)
        self.shape.draw_rect(r)
        self.shape.finish(
            color=border_color if border else None,
            fill=fill_color,
            width=border_width if border else 0,
            fill_opacity=opacity,
            stroke_opacity=0.9 if border else 0.0,
            closePath=True,
        )

    def draw_badge(
        self,
        center: Union[pymupdf.Point, Tuple[float, float]],
        text: str,
        radius: float = 11.0,
        bg_color: RGBColor = PALETTE["primary"],
        text_color: RGBColor = PALETTE["white"],
        fontsize: float = 10.0,
    ) -> None:
        """Draw a circular step/callout badge with centered number or text."""
        pt = pymupdf.Point(center)
        self.shape.draw_circle(pt, radius)
        self.shape.finish(fill=bg_color, color=bg_color, closePath=True)
        # Approximate centered text placement
        x_offset = -3.2 * len(text)
        y_offset = fontsize * 0.35
        self.shape.insert_text(
            pymupdf.Point(pt.x + x_offset, pt.y + y_offset),
            text,
            fontsize=fontsize,
            fontname="helv",
            color=text_color,
        )

    def draw_callout(
        self,
        box_rect: Union[pymupdf.Rect, Tuple[float, float, float, float]],
        text: str,
        target_point: Union[pymupdf.Point, Tuple[float, float]],
        bg_color: RGBColor = PALETTE["white"],
        border_color: RGBColor = PALETTE["primary"],
        text_color: RGBColor = PALETTE["neutral_dark"],
        fontsize: float = 10.0,
    ) -> None:
        """Draw an informational callout box with an arrow pointing directly to target_point."""
        rect = pymupdf.Rect(box_rect)
        target = pymupdf.Point(target_point)

        # 1. Draw callout card
        self.shape.draw_rect(rect)
        self.shape.finish(
            fill=bg_color,
            color=border_color,
            width=1.5,
            fill_opacity=0.95,
            closePath=True,
        )

        # 2. Compute closest edge center of box to target for clean arrow origin
        box_center = pymupdf.Point((rect.x0 + rect.x1) / 2, (rect.y0 + rect.y1) / 2)
        candidates = [
            pymupdf.Point((rect.x0 + rect.x1) / 2, rect.y1),  # Bottom
            pymupdf.Point((rect.x0 + rect.x1) / 2, rect.y0),  # Top
            pymupdf.Point(rect.x0, (rect.y0 + rect.y1) / 2),  # Left
            pymupdf.Point(rect.x1, (rect.y0 + rect.y1) / 2),  # Right
        ]
        start_pt = min(candidates, key=lambda c: math.hypot(c.x - target.x, c.y - target.y))

        # 3. Draw arrow pointing to target
        self.draw_arrow(start_pt, target, color=border_color, width=1.8, head_len=9, head_width=5)

        # 4. Insert text inside box
        pad = 6.0
        text_rect = pymupdf.Rect(rect.x0 + pad, rect.y0 + pad, rect.x1 - pad, rect.y1 - pad)
        self.shape.insert_textbox(
            text_rect,
            text,
            fontsize=fontsize,
            fontname="helv",
            color=text_color,
            align=pymupdf.TEXT_ALIGN_LEFT,
        )

    # --- Image Annotation Helpers ---

    def get_image_rects(self) -> List[pymupdf.Rect]:
        """Detect and return bounding boxes of images embedded on the current page."""
        image_info_list = self.page.get_image_info(xrefs=True)
        return [pymupdf.Rect(info["bbox"]) for info in image_info_list if "bbox" in info]

    def insert_image(
        self,
        rect: Union[pymupdf.Rect, Tuple[float, float, float, float]],
        filename: Optional[str] = None,
        stream: Optional[bytes] = None,
        overlay: bool = True,
    ) -> None:
        """Insert an image into the current page."""
        self.commit()
        r = pymupdf.Rect(rect)
        self.page.insert_image(r, filename=filename, stream=stream, overlay=overlay)


# ==============================================================================
# 3. Geometry3D — 3D Polyhedra & Prism Renderer
# ==============================================================================

class Geometry3D:
    """
    Renders 3D geometric shapes (triangular prisms, rectangular prisms,
    cubes, pyramids) directly onto PDF canvas with isometric projection,
    depth-sorted shaded faces, and dashed hidden edges.
    """

    @staticmethod
    def project_isometric(
        x: float, y: float, z: float,
        cx: float, cy: float,
        angle_deg: float = 30.0
    ) -> pymupdf.Point:
        """
        Projects 3D Cartesian coordinates (x, y, z) into 2D isometric canvas coordinates.
        px = cx + (x - y) * cos(angle)
        py = cy + (x + y) * sin(angle) - z
        """
        rad = math.radians(angle_deg)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        px = cx + (x - y) * cos_a
        py = cy + (x + y) * sin_a - z
        return pymupdf.Point(px, py)

    @classmethod
    def draw_triangular_prism(
        cls,
        canvas: PDFCanvas,
        cx: float = 300,
        cy: float = 400,
        side: float = 130,
        height: float = 160,
        primary_color: RGBColor = PALETTE["primary"],
        fill_opacity: float = 0.45,
        dashed_hidden: bool = True,
        label_vertices: bool = True,
        show_dimensions: bool = True,
    ) -> Dict[str, pymupdf.Point]:
        """
        Renders an isometric 3D triangular prism:
        - Base equilateral triangle at z=0 (V0, V1, V2)
        - Top equilateral triangle at z=height (V3, V4, V5)
        - Hidden edges dashed: (V0-V1), (V0-V2), (V0-V3)
        - Shaded visible front & top faces
        """
        tri_h = side * (math.sqrt(3) / 2)

        # 3D Coordinates
        p3d = {
            "V0": (0.0, 0.0, 0.0),             # Back-left base
            "V1": (side, 0.0, 0.0),            # Front-right base
            "V2": (side / 2.0, tri_h, 0.0),    # Apex base
            "V3": (0.0, 0.0, height),          # Back-left top
            "V4": (side, 0.0, height),         # Front-right top
            "V5": (side / 2.0, tri_h, height), # Apex top
        }

        # Project to 2D
        v = {k: cls.project_isometric(coords[0], coords[1], coords[2], cx, cy) for k, coords in p3d.items()}

        # 1. Draw hidden interior edges (dashed)
        hidden_edges = [("V0", "V1"), ("V0", "V2"), ("V0", "V3")]
        if dashed_hidden:
            for p_from, p_to in hidden_edges:
                canvas.draw_line(v[p_from], v[p_to], color=(0.55, 0.58, 0.62), width=1.5, dashes="[4 4] 0")

        # 2. Draw front/right shaded face (V1, V2, V5, V4)
        canvas.shape.draw_polyline([v["V1"], v["V2"], v["V5"], v["V4"], v["V1"]])
        canvas.shape.finish(
            fill=primary_color,
            color=primary_color,
            width=2.0,
            fill_opacity=fill_opacity * 0.8,
            closePath=True,
        )

        # 3. Draw top triangular face (V3, V4, V5)
        canvas.shape.draw_polyline([v["V3"], v["V4"], v["V5"], v["V3"]])
        canvas.shape.finish(
            fill=(min(1.0, primary_color[0] + 0.15), min(1.0, primary_color[1] + 0.15), min(1.0, primary_color[2] + 0.15)),
            color=primary_color,
            width=2.0,
            fill_opacity=fill_opacity * 1.2,
            closePath=True,
        )

        # 4. Draw front visible vertical edges
        canvas.draw_line(v["V1"], v["V4"], color=primary_color, width=2.0)
        canvas.draw_line(v["V2"], v["V5"], color=primary_color, width=2.0)

        # 5. Dimension markers
        if show_dimensions:
            # Height arrow alongside V4-V1
            h_start = pymupdf.Point(v["V4"].x + 25, v["V4"].y)
            h_end = pymupdf.Point(v["V1"].x + 25, v["V1"].y)
            canvas.draw_arrow(h_start, h_end, color=PALETTE["neutral_dark"], width=1.2, head_len=8, head_width=4, double_ended=True)
            canvas.shape.insert_text(
                pymupdf.Point(h_start.x + 8, (h_start.y + h_end.y) / 2 + 4),
                f"h = {int(height)}",
                fontsize=9,
                fontname="helv",
                color=PALETTE["neutral_dark"],
            )

        # 6. Vertex labels
        if label_vertices:
            for name, pt in v.items():
                canvas.draw_badge(pt, name, radius=9, bg_color=PALETTE["neutral_dark"], text_color=PALETTE["white"], fontsize=8)

        return v

    @classmethod
    def draw_rectangular_prism(
        cls,
        canvas: PDFCanvas,
        cx: float = 300,
        cy: float = 400,
        width: float = 140,
        depth: float = 90,
        height: float = 130,
        primary_color: RGBColor = PALETTE["success"],
        fill_opacity: float = 0.45,
        dashed_hidden: bool = True,
        label_vertices: bool = True,
    ) -> Dict[str, pymupdf.Point]:
        """
        Renders an isometric 3D rectangular prism (cuboid):
        - Base: A(0,0,0), B(w,0,0), C(w,d,0), D(0,d,0)
        - Top:  E(0,0,h), F(w,0,h), G(w,d,h), H(0,d,h)
        - Hidden back edges from A are dashed.
        """
        p3d = {
            "A": (0.0, 0.0, 0.0),
            "B": (width, 0.0, 0.0),
            "C": (width, depth, 0.0),
            "D": (0.0, depth, 0.0),
            "E": (0.0, 0.0, height),
            "F": (width, 0.0, height),
            "G": (width, depth, height),
            "H": (0.0, depth, height),
        }
        v = {k: cls.project_isometric(c[0], c[1], c[2], cx, cy) for k, c in p3d.items()}

        # Hidden interior edges from back-vertex A
        if dashed_hidden:
            for neighbor in ["B", "D", "E"]:
                canvas.draw_line(v["A"], v[neighbor], color=(0.55, 0.58, 0.62), width=1.5, dashes="[4 4] 0")

        # Shaded Right Face (B, C, G, F)
        canvas.shape.draw_polyline([v["B"], v["C"], v["G"], v["F"], v["B"]])
        canvas.shape.finish(
            fill=primary_color,
            color=primary_color,
            width=2.0,
            fill_opacity=fill_opacity * 0.7,
            closePath=True,
        )

        # Shaded Front Face (D, C, G, H)
        canvas.shape.draw_polyline([v["D"], v["C"], v["G"], v["H"], v["D"]])
        canvas.shape.finish(
            fill=primary_color,
            color=primary_color,
            width=2.0,
            fill_opacity=fill_opacity * 0.9,
            closePath=True,
        )

        # Shaded Top Face (E, F, G, H)
        canvas.shape.draw_polyline([v["E"], v["F"], v["G"], v["H"], v["E"]])
        canvas.shape.finish(
            fill=(min(1.0, primary_color[0] + 0.15), min(1.0, primary_color[1] + 0.15), min(1.0, primary_color[2] + 0.15)),
            color=primary_color,
            width=2.0,
            fill_opacity=fill_opacity * 1.2,
            closePath=True,
        )

        # Front visible vertical edge (C-G)
        canvas.draw_line(v["C"], v["G"], color=primary_color, width=2.0)

        # Vertex labels
        if label_vertices:
            for name, pt in v.items():
                canvas.draw_badge(pt, name, radius=9, bg_color=PALETTE["neutral_dark"], text_color=PALETTE["white"], fontsize=8)

        return v


# ==============================================================================
# 4. DSAVisualizer — Step-by-Step Data Structures & Algorithms Visualizer
# ==============================================================================

class DSAVisualizer:
    """
    Renders clean, beautiful step-by-step visualizations of algorithms:
    - Arrays (values, indices, search bounds, two-pointers)
    - Linked Lists (nodes, links, NULL terminators)
    - Trees (BST nodes, hierarchical edges, visited/active status)
    """

    @staticmethod
    def draw_array_step(
        canvas: PDFCanvas,
        array: List[Any],
        active_indices: Optional[List[int]] = None,
        compared_indices: Optional[List[int]] = None,
        sorted_indices: Optional[List[int]] = None,
        pointers: Optional[Dict[str, int]] = None,
        start_x: float = 70,
        start_y: float = 160,
        cell_w: float = 60,
        cell_h: float = 50,
    ) -> None:
        """
        Draw an annotated array bar with index labels and named pointer arrows.
        """
        active_indices = active_indices or []
        compared_indices = compared_indices or []
        sorted_indices = sorted_indices or []
        pointers = pointers or {}

        for i, val in enumerate(array):
            bx = start_x + i * cell_w
            by = start_y
            rect = pymupdf.Rect(bx, by, bx + cell_w, by + cell_h)

            # Determine cell color based on state
            if i in sorted_indices:
                fill = PALETTE["success"]
                text_col = PALETTE["white"]
            elif i in compared_indices:
                fill = PALETTE["warning"]
                text_col = PALETTE["neutral_dark"]
            elif i in active_indices:
                fill = (0.85, 0.92, 1.0)
                text_col = PALETTE["primary"]
            else:
                fill = PALETTE["neutral_light"]
                text_col = PALETTE["neutral_dark"]

            # Draw cell box
            canvas.draw_rect(rect, color=PALETTE["neutral_dark"], fill=fill, width=1.5)

            # Value
            val_str = str(val)
            v_offset = bx + (cell_w / 2.0) - (len(val_str) * 4.5)
            canvas.shape.insert_text(
                pymupdf.Point(v_offset, by + (cell_h * 0.65)),
                val_str,
                fontsize=16,
                fontname="helv",
                color=text_col,
            )

            # Index label below cell
            idx_str = f"[{i}]"
            i_offset = bx + (cell_w / 2.0) - (len(idx_str) * 3.2)
            canvas.shape.insert_text(
                pymupdf.Point(i_offset, by + cell_h + 20),
                idx_str,
                fontsize=11,
                fontname="helv",
                color=(0.45, 0.48, 0.52),
            )

        # Draw pointer arrows above array
        # e.g. {"low": 0, "mid": 4, "high": 9}
        arrow_level = 0
        pointer_colors = {
            "low": PALETTE["primary"],
            "left": PALETTE["primary"],
            "mid": PALETTE["danger"],
            "pivot": PALETTE["danger"],
            "high": PALETTE["info"],
            "right": PALETTE["info"],
            "i": PALETTE["primary"],
            "j": PALETTE["secondary"],
        }

        # Track which indices have pointers to offset stacking
        index_ptr_count: Dict[int, int] = {}
        for name, idx in pointers.items():
            if not (0 <= idx < len(array)):
                continue
            count = index_ptr_count.get(idx, 0)
            index_ptr_count[idx] = count + 1

            col = pointer_colors.get(name.lower(), PALETTE["neutral_dark"])
            bx = start_x + idx * cell_w + (cell_w / 2.0)
            by = start_y

            arrow_bottom_y = by - 5
            arrow_top_y = by - 22 - (count * 24)
            text_y = arrow_top_y - 6

            # Text label
            lbl = name.upper()
            canvas.shape.insert_text(
                pymupdf.Point(bx - (len(lbl) * 3.5), text_y),
                lbl,
                fontsize=10,
                fontname="helv",
                color=col,
            )
            # Arrow pointing down to cell
            canvas.draw_arrow(
                pymupdf.Point(bx, arrow_top_y),
                pymupdf.Point(bx, arrow_bottom_y),
                color=col,
                width=2.0,
                head_len=8,
                head_width=4.5,
            )

    @classmethod
    def create_algorithm_slide_deck(
        cls,
        output_pdf: str,
        title: str,
        steps: List[Dict[str, Any]],
        slide_w: float = 850,
        slide_h: float = 460,
    ) -> None:
        """
        Creates a sequential multi-page PDF where each page presents a discrete step
        of the algorithm with an explanatory header, visual state, and commentary.
        """
        doc = pymupdf.open()

        for step_idx, step in enumerate(steps, 1):
            doc.new_page(width=slide_w, height=slide_h)
            canvas = PDFCanvas(doc=doc, page_index=len(doc) - 1)

            # Header Card
            canvas.draw_rect(
                pymupdf.Rect(40, 30, slide_w - 40, 105),
                color=PALETTE["neutral_light"],
                fill=PALETTE["neutral_light"],
                width=1.0,
            )
            # Title
            step_header = f"{title} — Step {step_idx} of {len(steps)}"
            canvas.shape.insert_text(
                pymupdf.Point(55, 60),
                step_header,
                fontsize=17,
                fontname="helv",
                color=PALETTE["neutral_dark"],
            )
            # Commentary / description
            desc = step.get("description", "")
            canvas.shape.insert_text(
                pymupdf.Point(55, 88),
                desc,
                fontsize=12,
                fontname="helv",
                color=(0.25, 0.28, 0.32),
            )

            # Render Array visualization if present in step
            if "array" in step:
                cls.draw_array_step(
                    canvas=canvas,
                    array=step["array"],
                    active_indices=step.get("active", []),
                    compared_indices=step.get("compared", []),
                    sorted_indices=step.get("sorted", []),
                    pointers=step.get("pointers", {}),
                    start_x=step.get("start_x", 70),
                    start_y=step.get("start_y", 220),
                    cell_w=step.get("cell_w", 60),
                    cell_h=step.get("cell_h", 50),
                )

            # Extra notes card at bottom if present
            note = step.get("note")
            if note:
                canvas.draw_callout(
                    box_rect=pymupdf.Rect(70, 340, slide_w - 70, 410),
                    text=f"Insight: {note}",
                    target_point=pymupdf.Point(slide_w / 2.0, 275),
                    bg_color=(1.0, 0.98, 0.92),
                    border_color=PALETTE["warning"],
                    text_color=PALETTE["neutral_dark"],
                    fontsize=11,
                )

            canvas.commit()

        doc.save(output_pdf)
        doc.close()
