# Common PPTX Engineering Failure Modes & Remedies

This reference covers the most frequent failure modes encountered during OOXML slide engineering, their root causes, and exact mitigation strategies.

---

## 1. Unescaped XML Special Characters (#1 Cause of File Corruption)

### Problem
PowerPoint displays a repair prompt: *"PowerPoint found a problem with content in presentation.pptx"*.
### Root Cause
Injecting characters like `&`, `<`, or `>` directly into `<a:t>` nodes without entity escaping (e.g. `< 30s` or `AT&T`).
### Remedy
Always escape entities:
- `&` $ightarrow$ `&amp;`
- `<` $ightarrow$ `&lt;`
- `>` $ightarrow$ `&gt;`
Run `python scripts/validate.py <unpacked_dir>` to pinpoint exact line and column.

---

## 2. Hyperlink Text Changed But Target Left Stale

### Problem
Clicking the visible link opens the old URL or a deleted repository.
### Root Cause
Modifying `<a:t>` visible text without updating the `Target` attribute in `ppt/slides/_rels/slideN.xml.rels`.
### Remedy
Always perform a two-point update:
1. Update `<a:t>` in `slideN.xml`
2. Update `<Relationship Target="...">` in `slideN.xml.rels`

---

## 3. Hanging Indents vs Left Margin (`marL` vs `indent`)

### Problem
When replacing an inline emoji with an icon shape, the entire paragraph shifts right, or wrapped lines fail to align under the first word.
### Root Cause
Setting `marL` (left margin) shifts all lines in the paragraph. Setting `indent` without `marL` shifts only the first line.
### Remedy
For heading with external icon:
- Set `marL="0"`
- Set `indent="<icon_width + gap_in_EMU>"`
This shifts line 1 to make room for the icon while wrapping subsequent lines to the flush margin.

---

## 4. Icon Whitespace & Inconsistent Visual Spacing

### Problem
Icons positioned with identical EMU offsets look unevenly spaced relative to text.
### Root Cause
Different glyphs have differing amounts of internal transparent padding baked into their SVG/PNG canvas.
### Remedy
Crop every rendered icon to its non-transparent bounding box using Pillow before placement:
```python
from PIL import Image
im = Image.open("icon.png")
bbox = im.getbbox()
if bbox:
    cropped = im.crop(bbox)
    cropped.save("icon_cropped.png")
```

---

## 5. Unreferenced Media Causing Validation Failure

### Problem
Validation fails on leftover PNG/JPEG assets inside `ppt/media/`.
### Root Cause
Intermediate experimentation files or test images copied into `ppt/media/` were not bound to any slide `.rels`.
### Remedy
Before repacking, cross-reference all files in `ppt/media/` against all relationship targets. Remove orphaned files.

---

## 6. Slide Filename Confusion vs Slide Visual Position

### Problem
Editing `slide4.xml` changes the wrong visual slide in the presentation.
### Root Cause
Slide filenames do not determine presentation order. Presentation order is governed entirely by `<p:sldIdLst>` in `ppt/presentation.xml`.
### Remedy
Always run `python scripts/extract_text.py <target>` to determine exact visual slide numbers and their backing filenames.

---

## 7. Character Budget Overrun (Text Overflow)

### Problem
Cards, columns, or bullet boxes clip at the bottom or overlap adjacent shapes.
### Root Cause
Source text was 30-50% longer than the original template design could accommodate.
### Remedy
Apply the overflow triage ladder:
1. **Condense wording** (shorter, punchier phrasing)
2. **Remove redundancy**
3. **Adjust paragraph spacing** (`spcAft`, `spcBef`)
4. **Adjust text box dimensions** (if canvas space allows)
5. **Adjust font size slightly** (last resort, maintain readability)
