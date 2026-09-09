# Presentation Visual Design & Hierarchy Guide

This guide establishes design standards for high-impact technical and executive slide decks.

---

## 1. Information Hierarchy & Scannability

A slide must communicate its core thesis in under **3 seconds** of visual scanning.

### Golden Rules
- **Headline + Sub-headline**: Every slide needs a declarative title (e.g. *"Sub-30s Multi-Modal Forensic Pipeline"*, NOT *"Overview"*).
- **Rule of Threes / Fours**: Never exceed 3–4 primary vertical columns or horizontal cards per slide.
- **Lead with Metrics**: Surface key benchmark numbers (e.g. `AUC: 0.955`, `52/52 Tests`, `₹11,000 Cr`) as bold headline chips or badges.

---

## 2. Replacing Emoji Glyphs with Real Icons

Emoji characters (`📄`, `📱`, `🧠`, `⚡`) render unreliably across operating systems and often appear as missing glyph boxes (`□`).

### Workflow
1. Select an icon family (e.g. Lucide, Feather, FontAwesome) matching deck aesthetic.
2. Render to transparent PNG at $\ge 256	ext{px}$.
3. Crop internal transparent padding with `Image.getbbox()`.
4. Insert as `<p:pic>` positioned at `(shape_x + lIns, shape_y + tIns)`.
5. Remove emoji from heading `<a:t>`.
6. Configure paragraph with hanging indent (`indent="<icon_width + gap>"`, `marL="0"`).

---

## 3. Technical Diagrams vs Dense Bullet Lists

When communicating workflows, architectures, or pipelines, diagrams communicate more clearly than text.

### Diagram Best Practices
- **Flow Direction**: Left-to-right (horizontal pipelines) or top-to-bottom (ingestion to verdict).
- **Color Coding**: Align node fills with brand theme (e.g., Deep navy `#0B1A2E`, Cyan accent `#06B6D4`, Crimson warning `#EF4444`).
- **Contrast**: Ensure minimum 4.5:1 text-to-background contrast ratio on all nodes.
- **Aspect Ratio**: Never stretch a diagram to fit a container. Center it and flank with key takeaway chips or metric badges.

---

## 4. Intentional Negative Space

Empty space is a structural design element, not an error to be filled.
- Maintain consistent outer margins (minimum 0.5" to 0.75" around the slide canvas).
- Keep vertical breathing room between section headers and card grids.
- Ensure balanced whitespace across card columns.
