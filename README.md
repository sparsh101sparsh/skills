<div align="center">

# ⚡ Antigravity Skills Collection
### Production-Grade Agentic Workflows, Skills & Tooling for Google DeepMind Antigravity

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Antigravity](https://img.shields.io/badge/Antigravity-Compatible-8A2BE2.svg?style=for-the-badge)](https://github.com/sparsh101sparsh/skills)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Active%20%26%20Tested-00C853?style=for-the-badge)](#)

*A curated repository of modular, executable skills, runbooks, and domain-specific engineering tools designed for Google Antigravity and agentic AI systems.*

[Skills Catalog](#-skills-catalog) • [pptx-engineer](#-featured-skill-pptx-engineer) • [Installation](#-installation--setup) • [Contributing](#-contributing)

</div>

---

## 📖 Overview

In modern agentic pair programming, **Skills** extend the agent's core reasoning with specialized runbooks, progressive-disclosure documentation, executable scripts, and strict failure-mode guardrails. 

This repository houses verified, production-hardened skills for:
- Complex document and binary format engineering (OOXML, PDF, PresentationML)
- High-stakes automated refactoring and verification pipelines
- Zero-drift surgical modifications with automated structural validation

---

## 🗂️ Skills Catalog

| Skill Name | Version | Category | Description | Status |
|---|---|---|---|---|
| [`pptx-engineer`](./pptx-engineer/) | `v1.0.0` | **Document Engineering** | Precision PowerPoint (.pptx) OOXML engineering, presentation design, and structural validation. | ✅ Production |

---

## 🎯 Featured Skill: `pptx-engineer`

**Expert PowerPoint (.pptx) presentation engineering, presentation design, and OOXML automation.**

Most AI coding assistants treat PowerPoint files either as unmodifiable binaries or blindly regenerate them using libraries like `python-pptx`, inadvertently stripping bespoke typography, master animations, vector groupings, and pixel-precise EMU coordinates.

`pptx-engineer` treats `.pptx` as an Open Packaging Conventions (OPC) ZIP archive of PresentationML XML parts, applying surgical modifications while enforcing design continuity and strict schema integrity.

### 🏛️ Package Architecture

```
pptx-engineer/
├── SKILL.md                          # Master instruction file with YAML frontmatter
├── scripts/
│   ├── extract_text.py               # Extracts text following <p:sldIdLst> visual order
│   ├── unpack.py                     # Safely extracts .pptx archives to working directory
│   ├── inspect_shapes.py             # Dumps shape IDs, geometry, bounding box (EMU/in), runs, indents
│   ├── add_slide.py                  # Duplicates a slide with full rels & [Content_Types] wiring
│   ├── repack.py                     # Re-archives unpacked folder into .pptx (proper .rels handling)
│   ├── validate.py                   # Validates schema, XML syntax, relationships, unreferenced media
│   └── thumbnail.py                  # Renders visual slide previews for QA (qlmanage / soffice)
├── references/
│   ├── ooxml_quickref.md             # Package namespaces, EMU conversion, run splitting, hyperlinks
│   ├── failure_modes.md              # 20+ failure modes, root causes, hanging indent remedies
│   └── visual_design_guide.md        # Hierarchy, icon cropping, negative space, technical diagrams
└── examples/
    └── sample_modifications.md       # Tested Python patterns for surgical text and card templating
```

### ⚙️ Core Engineering Principles

1. **Preserve Before Modifying**: The original presentation is the source of truth. Layouts, themes, aspect ratios, and animations are preserved by default.
2. **Slide Filename $\ne$ Slide Position**: Visual order is governed by `<p:sldIdLst>` in `ppt/presentation.xml`, not `slide1.xml` file numbering.
3. **Mandatory XML Entity Escaping**: Automatic escaping for `&` (`&amp;`), `<` (`&lt;`), and `>` (`&gt;`) prevents PowerPoint corruption dialogues.
4. **Two-Point Hyperlink Architecture**: Synchronously updates both visible text in `slideN.xml` and target URLs in `ppt/slides/_rels/slideN.xml.rels`.
5. **Hanging Indents & Icon Bounding Boxes**: Replaces unstable emoji glyphs with cropped vector PNGs (`PIL.Image.getbbox()`) paired with `indent="<width + gap>"` and `marL="0"`.
6. **Built-in Package Validation**: `validate.py` cross-checks XML syntax, dangling relationships, unreferenced media, and duplicate shape IDs against original file baselines.

---

## 🚀 Installation & Setup

### Method 1: Global Antigravity Installation (Recommended)

To make skills available across **all workspaces** in Antigravity on your machine:

```bash
# Clone directly into Antigravity global config
git clone https://github.com/sparsh101sparsh/skills.git ~/.gemini/config/skills/community-skills

# Or symlink/copy individual skills:
cp -r pptx-engineer ~/.gemini/config/skills/
```

### Method 2: Project-Specific Workspace Installation

To equip a specific repository or team workspace with these skills:

```bash
mkdir -p .agents/skills
cp -r /path/to/pptx-engineer .agents/skills/
```

Antigravity automatically discovers skills located in `.agents/skills/<skill_name>/SKILL.md` when launching conversations.

---

## 🛠️ Tooling & Script Usage

```bash
# 1. Extract slide text in true presentation reading order
python pptx-engineer/scripts/extract_text.py deck.pptx

# 2. Unpack safely
python pptx-engineer/scripts/unpack.py deck.pptx unpacked/

# 3. Inspect shapes, positions (EMU & inches), and insets
python pptx-engineer/scripts/inspect_shapes.py unpacked/ slide1.xml

# 4. Duplicate slide with complete relationship & [Content_Types] wiring
python pptx-engineer/scripts/add_slide.py unpacked/ slide1.xml --after slide1.xml

# 5. Repack presentation (preserves _rels/.rels and cleans temp files)
python pptx-engineer/scripts/repack.py unpacked/ modified.pptx

# 6. Run structural validation check
python pptx-engineer/scripts/validate.py modified.pptx --original deck.pptx
```

---

## 📋 Verification & Testing

Every script and workflow in this repository undergoes automated end-to-end testing:
- ✅ Round-trip unpack $\rightarrow$ inspect $\rightarrow$ duplicate $\rightarrow$ repack $\rightarrow$ validate
- ✅ Python 3.10, 3.11, 3.12, 3.14 compatibility
- ✅ Zero-dependency core (standard library `xml.etree`, `zipfile`, `os`, `shutil`) with optional `Pillow` and `python-pptx` enhancements

---

## 🤝 Contributing

Contributions of new Antigravity skills or enhancements to existing ones are welcome!
1. Fork this repository
2. Create a feature branch (`git checkout -b skill/my-new-skill`)
3. Add your skill with `SKILL.md`, `scripts/`, `references/`, and `examples/`
4. Ensure all validation passes
5. Submit a Pull Request

---

## 📜 Author & License

- **Author**: Sparsh ([@sparsh101sparsh](https://github.com/sparsh101sparsh))
- **License**: Licensed under the [MIT License](LICENSE).
