# Practical Examples: PPTX Engineering Workflows

This document provides complete, tested code patterns for common PPTX engineering tasks.

---

## Example 1: Surgical Text & Hyperlink Replacement

```python
import os
import xml.etree.ElementTree as ET

# 1. Update text in slide XML
slide_path = "unpacked/ppt/slides/slide1.xml"
with open(slide_path, "r", encoding="utf-8") as f:
    xml_text = f.read()

old_url = "https://github.com/sparsh101sparsh/netra-v4"
new_url = "https://github.com/sparsh101sparsh/netra-deepfake-detector"

assert old_url in xml_text, "Target URL not found in slide XML"
xml_text = xml_text.replace(old_url, new_url)

with open(slide_path, "w", encoding="utf-8") as f:
    f.write(xml_text)

# 2. Update relationship target in slide1.xml.rels
rels_path = "unpacked/ppt/slides/_rels/slide1.xml.rels"
with open(rels_path, "r", encoding="utf-8") as f:
    rels_text = f.read()

if old_url in rels_text:
    rels_text = rels_text.replace(old_url, new_url)
    with open(rels_path, "w", encoding="utf-8") as f:
        f.write(rels_text)
print("Updated visible text and relationship target successfully.")
```

---

## Example 2: Templated Card / Bullet List Generation

```python
def make_bullet_para(title, description, is_first=False):
    spc = ' spcBef="0"' if is_first else ' spcBef="120000"'
    return f"""<a:p>
  <a:pPr{spc}>
    <a:buClr><a:srgbClr val="06B6D4"/></a:buClr>
    <a:buSzPts val="1200"/>
    <a:buFont typeface="Arial"/>
    <a:buChar char="•"/>
  </a:pPr>
  <a:r>
    <a:rPr b="1" sz="1200"><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill></a:rPr>
    <a:t>{title}: </a:t>
  </a:r>
  <a:r>
    <a:rPr b="0" sz="1200"><a:solidFill><a:srgbClr val="94A3B8"/></a:solidFill></a:rPr>
    <a:t>{description}</a:t>
  </a:r>
</a:p>"""
```

---

## Example 3: End-to-End Workflow with Scripts

```bash
# 1. Extract text to understand the deck
python scripts/extract_text.py presentation.pptx

# 2. Unpack safely
python scripts/unpack.py presentation.pptx unpacked/

# 3. Inspect target shapes
python scripts/inspect_shapes.py unpacked/ slide4.xml

# 4. Duplicate slide if necessary
python scripts/add_slide.py unpacked/ slide4.xml --after slide4.xml

# 5. Make surgical XML edits via Python script...

# 6. Repack presentation
python scripts/repack.py unpacked/ out.pptx

# 7. Validate package
python scripts/validate.py out.pptx --original presentation.pptx

# 8. Visual QA preview
python scripts/thumbnail.py out.pptx
```
