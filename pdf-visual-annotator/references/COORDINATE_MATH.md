# PDF Coordinate Math & 3D Projection Reference

This guide outlines the mathematical foundation used by `pdf-visual-annotator` for pixel-accurate PDF annotations, image overlays, and 3D isometric polyhedra rendering.

---

## 1. PDF Coordinate System Fundamentals

In standard PDF specifications (ISO 32000-1):
- **Units**: Dimensions are specified in **points** ($1 \text{ pt} = \frac{1}{72} \text{ inch} = 0.3528 \text{ mm}$).
- **Standard Letter**: $612 \times 792 \text{ pt}$.
- **Standard A4**: $595.3 \times 841.9 \text{ pt}$.
- **PyMuPDF Coordinate Convention**:
  - Origin $(0, 0)$ is at the **top-left** of the unrotated page.
  - $X$ increases **rightward** ($0 \to \text{width}$).
  - $Y$ increases **downward** ($0 \to \text{height}$).
  - Rectangles are expressed as `pymupdf.Rect(x0, y0, x1, y1)` where $(x_0, y_0)$ is the top-left and $(x_1, y_1)$ is the bottom-right coordinate.

---

## 2. Drawing Over Embedded Images (`overlay=True`)

When modifying a PDF containing images:
1. PyMuPDF identifies image locations via `page.get_image_info(xrefs=True)`, which returns `bbox: [x0, y0, x1, y1]`.
2. To draw annotations *above* the image pixels without having them obscured, the vector operations must be committed to the foreground:
   ```python
   # When inserting an image
   page.insert_image(rect, filename="sample.png", overlay=True)

   # When drawing vector shapes, commit() places them in the page foreground
   shape = page.new_shape()
   shape.draw_rect(rect)
   shape.finish(...)
   shape.commit()  # Appends to the top-level page content stream
   ```

---

## 3. Vector Arrow Mathematics

To draw a sharp, properly aligned arrowhead pointing from $P_1(x_1, y_1)$ to $P_2(x_2, y_2)$:

### Direction Vector:
$$\Delta x = x_2 - x_1, \quad \Delta y = y_2 - y_1$$
$$L = \sqrt{\Delta x^2 + \Delta y^2}$$
$$\hat{u} = \left(\frac{\Delta x}{L}, \frac{\Delta y}{L}\right), \quad \hat{u}_\perp = (-\hat{u}_y, \hat{u}_x)$$

### Arrowhead Flanges:
Given arrow head length $H_L$ and half-width $H_W$:
$$P_{\text{left}} = P_2 - H_L \hat{u} + H_W \hat{u}_\perp$$
$$P_{\text{right}} = P_2 - H_L \hat{u} - H_W \hat{u}_\perp$$

The arrowhead polygon $[P_{\text{left}}, P_2, P_{\text{right}}, P_{\text{left}}]$ is filled with the stroke color to form a solid tip.

---

## 4. Quadratic Bézier Curved Arrows

A quadratic Bézier curve with start $P_0$, control point $P_c$, and end $P_1$ is parameterized by $t \in [0, 1]$:
$$B(t) = (1 - t)^2 P_0 + 2(1 - t)t P_c + t^2 P_1$$

### Tangent at Arrow Tip ($t = 1$):
$$B'(1) = 2(P_1 - P_c)$$

The arrowhead orientation is calculated using this tangent vector $\Delta = P_1 - P_c$ rather than the chord vector $P_1 - P_0$.

---

## 5. 3D Isometric Projection

Isometric projection maps 3D Cartesian coordinates $(x, y, z)$ to 2D canvas coordinates $(p_x, p_y)$ using a standard $30^\circ$ projection angle:

$$\cos(30^\circ) = \frac{\sqrt{3}}{2} \approx 0.866025$$
$$\sin(30^\circ) = \frac{1}{2} = 0.5$$

Given 2D projection center $(c_x, c_y)$:
$$p_x = c_x + (x - y) \cdot \cos(30^\circ)$$
$$p_y = c_y + (x + y) \cdot \sin(30^\circ) - z$$

### Triangular Prism Geometry:
- **Base (at $z = 0$)**:
  - $V_0 = (0, 0, 0)$ (back-left)
  - $V_1 = (\text{side}, 0, 0)$ (front-right)
  - $V_2 = (\text{side}/2, \text{side} \cdot \frac{\sqrt{3}}{2}, 0)$ (apex)
- **Top (at $z = h$)**:
  - $V_3 = (0, 0, h)$
  - $V_4 = (\text{side}, 0, h)$
  - $V_5 = (\text{side}/2, \text{side} \cdot \frac{\sqrt{3}}{2}, h)$
- **Hidden Edges (Dashed)**:
  - $(V_0, V_1)$, $(V_0, V_2)$, and $(V_0, V_3)$ are internal/occluded and rendered with `dashes="[4 4] 0"`.
- **Visible Shaded Faces**:
  - Top: $[V_3, V_4, V_5]$ (lit face)
  - Front: $[V_1, V_2, V_5, V_4]$ (medium shaded face)
