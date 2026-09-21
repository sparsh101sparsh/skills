<div align="center">

# ⚡ Antigravity Skills Collection
### Production-Grade Agentic Workflows, Skills & Tooling for Google DeepMind Antigravity

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Antigravity](https://img.shields.io/badge/Antigravity-Compatible-8A2BE2.svg?style=for-the-badge)](https://github.com/sparsh101sparsh/skills)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Node.js 18+](https://img.shields.io/badge/Node.js-18%2B-339933?style=for-the-badge&logo=node.js&logoColor=white)](https://nodejs.org/)
[![Status](https://img.shields.io/badge/Status-Active%20%26%20Tested-00C853?style=for-the-badge)](#)

*A curated repository of modular, executable skills, runbooks, and domain-specific engineering tools designed for Google Antigravity and agentic AI systems.*

[Skills Catalog](#-skills-catalog) • [pptx-engineer](#-featured-skill-pptx-engineer) • [pptxgenjs](#-featured-skill-pptxgenjs) • [Installation](#-installation--setup) • [Verification](#-verification--testing) • [Contributing](#-contributing)

</div>

---

## 📖 Overview

In modern agentic pair programming, **Skills** extend the agent's core reasoning with specialized runbooks, progressive-disclosure documentation, executable scripts, and strict failure-mode guardrails. 

This repository houses verified, production-hardened skills for:
- Complex document and binary format engineering (OOXML, PDF, PresentationML)
- High-impact programmatic document generation from JSON schemas and scripts
- Zero-drift surgical modifications with automated structural validation
- End-to-end automated verification test suites

---

## 🗂️ Skills Catalog

| Skill Name | Version | Category | Description | Status |
|---|---|---|---|---|
| [`pptx-engineer`](./pptx-engineer/) | `v1.0.0` | **Document Engineering** | Precision PowerPoint (.pptx) OOXML engineering, presentation design, and structural validation. | ✅ Production |
| [`pptxgenjs`](./pptxgenjs/) | `v1.0.0` | **Document Generation** | Programmatic PowerPoint (.pptx) deck generation, JSON-to-deck compilation, KPI dashboards, and chart creation via PptxGenJS. | ✅ Production |
| [`forensic-doc-verifier`](./forensic-doc-verifier/) | `v1.0.0` | **Security & Forensics** | ICAO Doc 9303 MRZ parsing (7-3-1 check digits), passport validation, and visual Error Level Analysis (ELA). | ✅ Production |
| [`api-security-auditor`](./api-security-auditor/) | `v1.0.0` | **Security & Penetration Testing** | Automated OWASP API Top 10 scanner for SQL injection, path traversal, and auth boundary probes. | ✅ Production |

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

## 🎨 Featured Skill: `pptxgenjs`

**Programmatic slide engineering, venture pitch deck templates, and automated PowerPoint generation via PptxGenJS & Node.js.**

While `pptx-engineer` specializes in surgical modifications of existing decks, `pptxgenjs` provides programmatic creation of brand-new, modern presentation decks from scratch or compiled directly from structured JSON definitions.

### ⚖️ When to Use Which Skill

| Requirement | Preferred Skill | Rationale |
|---|---|---|
| **Create new presentations from scratch** | `pptxgenjs` | Full programmatic control over slide layouts, themes, charts, and master definitions. |
| **Convert data / JSON into slide decks** | `pptxgenjs` | Declarative `quick_gen.js` CLI converts JSON specs into styled decks. |
| **Automate KPI dashboards & financial reports** | `pptxgenjs` | Built-in card containers, metric callouts, column/doughnut charts, and tables. |
| **Edit existing pre-authored client decks** | `pptx-engineer` | Preserves bespoke branding, subtle layout nuances, master animations, and embedded assets. |
| **Diagnose corrupt `.pptx` files or fix XML errors** | `pptx-engineer` | Direct OPC ZIP archive inspection, XML validation, and repair tooling. |

### 🏛️ Package Architecture

```
pptxgenjs/
├── SKILL.md                          # Master instruction file with YAML frontmatter
├── package.json                      # NPM package metadata and test scripts
├── scripts/
│   ├── run.js                        # Universal runner with automatic dependency resolution
│   └── quick_gen.js                  # CLI compiler: JSON slide specification -> styled .pptx
├── examples/
│   ├── pitch_deck.js                 # Complete 5-slide venture pitch deck template
│   └── metrics_dashboard.js          # Executive dashboard with KPI cards and dual charts
├── references/
│   ├── api_reference.md              # Parameter tables for text, tables, shapes, images, notes
│   └── charts_and_shapes.md          # Complete chart types schema and shape catalogue
└── tests/
    └── verify.js                     # Automated verification test suite and OPC package validator
```

### ⚙️ Core Generation Principles

1. **Master Slide Pattern (`defineSlideMaster`)**: Enforces global visual hierarchy, consistent background slate tints, top accent borders, and muted footers across all slides.
2. **Card-Based Layouts**: Groups information into rounded rectangle containers (`pptx.shapes.ROUNDED_RECTANGLE`) with subtle borders (`E2E8F0`) instead of cluttered bullet lists.
3. **Color Discipline & Typography**: Strict 3-color palette (deep navy/slate backgrounds, primary brand blue `2563EB`, accent green/amber) with clean cross-platform sans-serif typography (`Segoe UI`, `Calibri`).
4. **Data Visualizations**: Native Office chart engine integration for bar, column, line, and doughnut charts with styled value labels and muted gridlines.

---

## 🚀 Installation & Setup

### Method 1: Global Antigravity Installation (Recommended)

To make skills available across **all workspaces** in Antigravity on your machine:

```bash
# Clone directly into Antigravity global config
git clone https://github.com/sparsh101sparsh/skills.git ~/.gemini/config/skills/community-skills

# Install dependencies for pptxgenjs
cd ~/.gemini/config/skills/community-skills/pptxgenjs && npm install
```

### Method 2: Project-Specific Workspace Installation

To equip a specific repository or team workspace with these skills:

```bash
mkdir -p .agents/skills
cp -r /path/to/pptx-engineer .agents/skills/
cp -r /path/to/pptxgenjs .agents/skills/
cd .agents/skills/pptxgenjs && npm install
```

Antigravity automatically discovers skills located in `.agents/skills/<skill_name>/SKILL.md` when launching conversations.

---

## 🛠️ Tooling & Script Usage

### pptx-engineer (Surgical Editing & Inspection)

```bash
# 1. Extract slide text in true presentation reading order
python3 pptx-engineer/scripts/extract_text.py deck.pptx

# 2. Unpack safely
python3 pptx-engineer/scripts/unpack.py deck.pptx unpacked/

# 3. Inspect shapes, positions (EMU & inches), and insets
python3 pptx-engineer/scripts/inspect_shapes.py unpacked/ slide1.xml

# 4. Duplicate slide with complete relationship & [Content_Types] wiring
python3 pptx-engineer/scripts/add_slide.py unpacked/ slide1.xml --after slide1.xml

# 5. Repack presentation (preserves _rels/.rels and cleans temp files)
python3 pptx-engineer/scripts/repack.py unpacked/ modified.pptx

# 6. Run structural validation check
python3 pptx-engineer/scripts/validate.py modified.pptx --original deck.pptx
```

### pptxgenjs (Programmatic Generation & CLI)

```bash
# 1. Run any script with universal dependency runner
node pptxgenjs/scripts/run.js pptxgenjs/examples/pitch_deck.js output_pitch.pptx

# 2. Generate executive KPI dashboard
node pptxgenjs/scripts/run.js pptxgenjs/examples/metrics_dashboard.js output_dashboard.pptx

# 3. Compile JSON presentation specification directly into PowerPoint (supports title, cards, stats, table, chart, bullets)
node pptxgenjs/scripts/quick_gen.js presentation_spec.json output.pptx

# 4. Stream JSON from stdin
cat presentation_spec.json | node pptxgenjs/scripts/quick_gen.js - output.pptx
```

### forensic-doc-verifier (Document Forensics & MRZ Validation)

```bash
# 1. Parse and validate ICAO 9303 MRZ strings (TD1, TD2, TD3) with 7-3-1 check digits
python3 forensic-doc-verifier/scripts/mrz_parser.py mrz_input.txt

# 2. Run Error Level Analysis (ELA) for image tamper / splice detection
python3 forensic-doc-verifier/scripts/ela_analyzer.py passport_scan.jpg -o ela_heatmap.jpg

# 3. Unified document forensics audit report
python3 forensic-doc-verifier/scripts/verify_document.py --mrz mrz_input.txt --image passport_scan.jpg
```

---

## 📋 Verification & Testing

Every script and workflow in this repository undergoes automated end-to-end testing:

### 1. `forensic-doc-verifier` Unit & Cryptographic Test Suite
```bash
pytest forensic-doc-verifier/tests/test_forensics.py
```

### 2. `pptxgenjs` Automated Test Suite
Runs programmatic generation across all layouts, examples, and JSON compilation, verifying OPC container integrity, slide counts, and byte non-emptiness:

```bash
# Run using npm
npm test --prefix pptxgenjs

# Or run directly with Node
node pptxgenjs/tests/verify.js
```

### 2. `pptx-engineer` Structural Validation
```bash
python3 pptx-engineer/scripts/validate.py modified.pptx --original deck.pptx
```

### Verification Checklist
- ✅ Round-trip unpack $\rightarrow$ inspect $\rightarrow$ duplicate $\rightarrow$ repack $\rightarrow$ validate
- ✅ Programmatic deck generation, slide masters, tables, charts, and card layouts
- ✅ OPC ZIP container verification (`[Content_Types].xml`, `_rels/.rels`, `ppt/presentation.xml`)
- ✅ Zero unreferenced media files and dangling relationship guarantees
- ✅ Cross-platform compatibility (Node.js 18+, Python 3.10+)

---

## 🤝 Contributing

Contributions of new Antigravity skills or enhancements to existing ones are welcome!
1. Fork this repository
2. Create a feature branch (`git checkout -b skill/my-new-skill`)
3. Add your skill with `SKILL.md`, `scripts/`, `references/`, and `examples/`
4. Ensure all validation passes (`npm test --prefix pptxgenjs`)
5. Submit a Pull Request

---

## 📜 Author & License

- **Author**: Sparsh ([@sparsh101sparsh](https://github.com/sparsh101sparsh))
- **License**: Licensed under the [MIT License](LICENSE).
