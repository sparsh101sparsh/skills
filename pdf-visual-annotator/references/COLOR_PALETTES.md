# PDF Diagram Color Palettes & Visual Hierarchy

Curated color definitions and accessibility rules for document annotations, algorithm visualizations, and 3D technical drawings.

---

## 1. Primary Semantic Palette (Normalized RGB)

PyMuPDF requires colors as normalized float tuples `(R, G, B)` in the range `0.0 .. 1.0`.

| Role | Name | Hex Code | Normalized RGB `(r, g, b)` | Application |
|---|---|---|---|---|
| **Primary** | Deep Sapphire | `#1F73D9` | `(0.12, 0.45, 0.85)` | Main arrows, active boundaries, node outlines |
| **Success** | Emerald | `#27AE60` | `(0.15, 0.68, 0.38)` | Target found, sorted array items, verified state |
| **Warning** | Amber / Gold | `#F39C12` | `(0.95, 0.60, 0.10)` | Compared elements, current partition, warnings |
| **Danger** | Crimson | `#E03838` | `(0.88, 0.22, 0.22)` | Anomaly callouts, mid/pivot pointers, errors |
| **Info** | Sky Blue | `#1AA6D9` | `(0.10, 0.65, 0.85)` | High pointer, secondary partitions, hints |
| **Neutral Dark** | Charcoal | `#262B33` | `(0.15, 0.17, 0.20)` | Text, axes, geometric dimensions, node text |
| **Neutral Light** | Cool Gray | `#EFF2F5` | `(0.94, 0.95, 0.96)` | Card backgrounds, default array cells |
| **Highlight** | Sunlight Yellow | `#FFF273` | `(1.00, 0.95, 0.45)` | Translucent bounding boxes over image regions |

---

## 2. 3D Surface Shading Ratios

For volumetric 3D shapes (e.g. prisms, cuboids):
- **Light Source**: Assumed to be top-right front.
- **Top Face**: Base color with $+15\%$ luminance, `fill_opacity = 0.55 .. 0.65`.
- **Front Face**: Base color with standard luminance, `fill_opacity = 0.45 .. 0.50`.
- **Side/Right Face**: Base color with $-10\%$ luminance, `fill_opacity = 0.35 .. 0.40`.
- **Hidden Edges**: Neutral slate `(0.55, 0.58, 0.62)` with dash pattern `"[4 4] 0"`.

---

## 3. Data Structure State Transitions

When illustrating sorting or search algorithms:
1. **Unvisited / Inactive**: Neutral Light `(0.94, 0.95, 0.96)`.
2. **Current Window / Partition**: Pale Blue `(0.85, 0.92, 1.00)`.
3. **Active Comparison**: Amber `(0.95, 0.60, 0.10)`.
4. **Sorted / Confirmed**: Emerald `(0.15, 0.68, 0.38)` with white bold text.
5. **Eliminated / Out-of-bounds**: Muted Gray `(0.85, 0.86, 0.88)`.
