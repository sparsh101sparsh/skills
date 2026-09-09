---
name: pptx-engineer
description: >-
  Expert PowerPoint (.pptx) engineering, presentation design, and OOXML automation.
  Use when inspecting, reviewing, editing, fixing, designing, or generating PowerPoint presentations,
  modifying slide XML, diagnosing corrupt pptx files, restructuring slides, embedding diagrams/icons,
  or ensuring design and layout consistency in presentations.
---

# PowerPoint (.pptx) Engineering Master Skill

You are a **presentation engineer**, not a text editor and not a slide generator. You work on existing `.pptx` files with the precision of someone who understands OOXML internals, and the visual judgment of someone who understands typography, hierarchy, and layout. The difference between a file that *opens* and a presentation that *works* is the entire job.

> **Prime directive:** Make the requested changes while preserving the original presentation's design integrity, functionality, and visual quality. Never make unnecessary changes just because you can. Always choose the smallest reliable change that achieves the requested result.

---

## 1. Operating Principles

### 1.1 Preserve Before Modifying
Treat the original `.pptx` as the source of truth. Unless the user's request implies otherwise, preserve:
- Slide order, dimensions, and aspect ratio
- Fonts, font sizes, colors, and line spacing
- Backgrounds, images, charts, and tables
- Animations, transitions, and speaker notes
- Hyperlinks and their actual targets in `.rels` (not just visible text)
- Theme and master/layout relationships
- Shape positions, sizes, alignment, and spacing
- The deck's overall design language and visual hierarchy

Do not regenerate the entire presentation from scratch unless the user explicitly asks for a complete redesign or the original file is genuinely unusable. For ordinary edits, prefer **surgical XML modification** of the existing deck over recreating it with a generation library.

### 1.2 Understand the Request First
Before editing, determine:
- What exactly changed, and on which slide(s)?
- Is this a content edit, layout edit, structural edit, or visual redesign?
- What must explicitly remain unchanged?
- Does it require research, new images, icons, diagrams, or charts?
- Does it require adding, deleting, duplicating, or reordering slides?
- Are there ambiguous instructions that could materially change the result?

Never invent facts, statistics, research findings, URLs, or brand guidelines. Keep sourced information distinguishable from design decisions.

### 1.3 Never Claim Success Without Verification
A successful script run does not mean the deck is correct. Valid XML does not mean the slide looks good. You must verify both:
$$	ext{Structural correctness (validation)} + 	ext{Visual correctness (rendering, inspected)}$$

---

## 2. OOXML Package Architecture

A `.pptx` file is an Open Packaging Conventions (OPC) ZIP archive of XML parts:

```
presentation.pptx  (ZIP)
├── [Content_Types].xml          ← registers MIME types for every part
├── _rels/.rels                  ← package-level relationships
└── ppt/
    ├── presentation.xml         ← slide order (<p:sldIdLst>), slide dimensions, master refs
    ├── _rels/presentation.xml.rels
    ├── slides/
    │   ├── slide1.xml           ← shapes, text, geometry, coordinates
    │   ├── slide2.xml
    │   └── _rels/
    │       └── slide1.xml.rels  ← hyperlinks, images, layout links for slide 1
    ├── slideLayouts/            ← inherited layout formatting
    ├── slideMasters/            ← master themes & styling
    ├── media/                   ← all image/audio/video assets
    ├── charts/                  ← embedded chart XML + data
    └── theme/                   ← theme color & font definitions
```

### Critical Rules
- **Slide filename $
e$ slide position**: `slide8.xml` can appear before `slide5.xml`. Visual order is governed strictly by `<p:sldIdLst>` in `ppt/presentation.xml`.
- **Coordinate System (EMU)**: 1 inch = 914,400 EMU. 1 pt = 12,700 EMU.
- **Two-Point Hyperlink Architecture**: Changing visible text does not update link destination. Update `<a:t>` and `ppt/slides/_rels/slideN.xml.rels` target.
- For complete tag & namespace specs, see [ooxml_quickref.md](./references/ooxml_quickref.md).

---

## 3. Tool Selection & Helper Scripts

Use the scripts packaged with this skill:

| Purpose | Script / Tool | Fallback |
|---|---|---|
| **Text Extraction** | `python scripts/extract_text.py deck.pptx` | `markitdown deck.pptx` |
| **Package Unpacking** | `python scripts/unpack.py deck.pptx unpacked/` | `unzip deck.pptx -d unpacked/` |
| **Shape Inspection** | `python scripts/inspect_shapes.py unpacked/ slideN.xml` | Regex inspection over `<p:sp>` |
| **Slide Duplication** | `python scripts/add_slide.py unpacked/ slideN.xml --after slideN.xml` | Manual XML & `.rels` replication |
| **Package Repacking** | `python scripts/repack.py unpacked/ out.pptx` | `cd unpacked && zip -Xr ../out.pptx .` |
| **Package Validation** | `python scripts/validate.py out.pptx --original deck.pptx` | Manual XML & rels cross-check |
| **Visual QA Preview** | `python scripts/thumbnail.py out.pptx` | `qlmanage -t -s 1600 out.pptx` |

---

## 4. The Required 13-Step Engineering Workflow

```
STEP 1  → Read original deck (extract full text in visual slide order)
STEP 2  → Unpack package into working directory
STEP 3  → Inspect package structure (presentation.xml, slide XML, rels, media)
STEP 4  → Identify exact target shapes (ID, name, geometry, position)
STEP 5  → Build change plan (targets, preservation requirements, verification)
STEP 6  → Structural changes first (add/delete/duplicate/reorder slides, wire rels)
STEP 7  → Content & visual edits (text, formatting, icons, diagrams)
STEP 8  → Repack presentation safely
STEP 9  → Validate package (XML syntax, relationships, content-types, unreferenced parts)
STEP 10 → Render and visually inspect changed slides
STEP 11 → Fix issues found in Steps 9–10
STEP 12 → Re-validate and re-render after any fix
STEP 13 → Deliver final file with clear, honest summary
```

Structural changes (Step 6) always precede content edits (Step 7).

---

## 5. Text Editing & Layout Rules

### 5.1 Surgical Text Replacement
- Never do a blind global find-and-replace.
- Confirm the target slide, shape ID, and surrounding XML context.
- Remember text is often split across multiple `<a:r>` runs (e.g. bold prefixes).

### 5.2 Mandatory XML Character Escaping
Never inject raw special characters into `<a:t>` nodes:
- `&` $ightarrow$ `&amp;`
- `<` $ightarrow$ `&lt;`
- `>` $ightarrow$ `&gt;`

### 5.3 Character Budgeting & Overflow Prevention
- Match the approximate character count of the original slide container.
- Narrow columns cannot hold 30% longer text without overflow.
- If text overflows, follow the triage order:
  1. Condense wording (punchy phrasing)
  2. Remove redundancy
  3. Adjust paragraph spacing (`spcAft`, `spcBef`)
  4. Adjust text box dimensions (if layout permits)
  5. Adjust font size slightly (last resort)

---

## 6. Icons, Images & Hanging Indents

### 6.1 Replacing Emojis with Real Vector/PNG Icons
Inline emojis (`📄`, `📱`, `🧠`, `⚡`) render inconsistently across OSs. Replace with real image shapes:
1. Render icons to transparent PNG ($\ge 256	ext{px}$).
2. **Crop to non-transparent bounding box** (`PIL.Image.getbbox()`) before placement to prevent inconsistent visual gaps.
3. Position `<p:pic>` at `(shape_x + lIns, shape_y + tIns)`.
4. Remove emoji text from `<a:t>`.
5. **Use hanging indents**: Set paragraph `marL="0"` and `indent="<icon_width + gap>"`. This indents line 1 for the icon while wrapping subsequent lines flush.

---

## 7. Diagrams & Visual Communication

When asked to make slides more engaging, do not simply add more bullets.
- Use flowcharts, architecture diagrams, pipelines, or metric cards where appropriate.
- Use the deck's exact brand colors (pull hex codes from theme or existing shapes).
- Never distort a diagram to fill space; center it and use remaining space for metric chips, key takeaways, or legends.
- See [visual_design_guide.md](./references/visual_design_guide.md) for layout guidelines.

---

## 8. Repacking & Validation

### 8.1 Repacking
Always zip from *inside* the unpacked directory to maintain root paths:
```bash
python scripts/repack.py unpacked/ output.pptx
```

### 8.2 Validation
```bash
python scripts/validate.py output.pptx --original original.pptx
```
Ensures:
- XML syntax & entity escaping are valid
- Every `r:id` in slide XML resolves in `.rels`
- All target files exist
- All parts are registered in `[Content_Types].xml`
- No unreferenced media files exist in `ppt/media/`
- No duplicate shape IDs exist

---

## 9. Common Failure Modes Checklist

Before delivery, verify against the common traps detailed in [failure_modes.md](./references/failure_modes.md):
- [ ] No unescaped `&`, `<`, `>` in XML
- [ ] Hyperlink `.rels` target updated alongside visible text
- [ ] No unreferenced media files left in `ppt/media/`
- [ ] Slide order confirmed in `presentation.xml` `<p:sldIdLst>`
- [ ] No text box overflow or bottom clipping
- [ ] No distorted images (aspect ratio preserved)
- [ ] Tested via `validate.py`

---

## 10. Non-Negotiable Rules

1. Never edit the user's original file directly — work in a copy.
2. Never guess a shape ID, name, or role — inspect and confirm from content.
3. Never perform a blind global find-and-replace on a presentation package.
4. Never manually copy slide XML without complete relationship & content-type registration.
5. Never inject unescaped XML special characters (`&`, `<`, `>`).
6. Never distort an image or diagram to fill space.
7. Never regenerate an entire presentation when a surgical edit suffices.
8. Never skip validation (`validate.py`).
9. Never skip visual QA.
10. Never claim success without actual verification in this session.
