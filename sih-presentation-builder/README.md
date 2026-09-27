# Smart India Hackathon Presentation Builder (`sih-presentation-builder`)

[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-agentskills.io-blue.svg)](https://agentskills.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A specialized Agent Skill engineered for AI coding assistants to build research-backed, diagram-first, competition-winning presentations for the **Smart India Hackathon (SIH)**, national engineering hackathons, and high-stakes technical defense evaluations.

---

## 🎯 Why This Skill Exists

Most AI-generated presentation slides collapse under competition jury scrutiny for predictable reasons:
1. **Wall of Text:** Slides are filled with narrative paragraphs and repetitive bullet points that no judge has time to read.
2. **"AI Slop" Clutter:** Slides are cluttered with decorative leaves, tree watermarks, floating geometric bubbles, and meaningless graphics.
3. **The Card Matrix Trap:** Every slide looks like a web dashboard with 4 to 6 identical rounded rectangles.
4. **Unverifiable Claims:** Claims of "99.9% accuracy" or "instant cloud sync" without specifying datasets, test conditions, or offline fallbacks.
5. **Domain-Blind Buzzwords:** Misplacing fintech buzzwords (e.g., "KYC") into border security, agriculture, or mining problem statements.

`sih-presentation-builder` encodes the accumulated lessons, design rules, and visual grammar reverse-engineered from **50 official SIH winning presentations** (including *Team Lumora*, *Storm Surge*, *Udaan*, *CoalWorks*, and *EcoPick*), combined with extensive live iteration on real SIH problem statements.

---

## 📐 Core Architecture & Visual Rules

* **The 80/20 Rule:** 80% diagrammatic visuals, 20% high-impact telegraphic copy.
* **Telegraphic Copy:** Maximum 6 to 8 words per bullet point. Numbers beat adjectives.
* **Dominant Diagram:** Every slide centers around one defensible visual engine (a hub-and-spoke cluster, a numbered pipeline, a paired challenge-mitigation matrix, or a horizontal stakeholder process ribbon).
* **The Non-Negotiable Offline Fallback:** Every technical architecture slide must feature an explicit, labeled fallback route for zero-internet environments.
* **Human-in-the-Loop Realism:** Replace impossible claims of 100% autonomous AI with explainable decision-support copilots featuring an Amber review tier for human judgment.

---

## 📂 Repository Structure

```
sih-presentation-builder/
├── SKILL.md                              # Core operational instructions for AI agents
├── README.md                             # User guide, installation, and overview
└── references/
    ├── lessons-from-iteration.md         # Detailed retrospective of live prompt iterations & mistakes
    ├── slide-quality-checklist.md        # Comprehensive multi-dimensional evaluation rubric
    └── visual-decision-framework.md      # Content-to-visual decision tree and geometry rules
```

---

## 🚀 Installation & Usage

### 1. Install via GitHub CLI (`gh skill`)
You can install this skill directly using GitHub CLI's preview skill manager:

```bash
gh skill install sparsh101sparsh/skills sih-presentation-builder
```

### 2. Manual Installation
Clone this repository into your agent's skill directory:

```bash
# For Google Antigravity / Gemini CLI
cp -r sih-presentation-builder ~/.gemini/config/skills/

# For Claude / Cursor / Codex
cp -r sih-presentation-builder ~/.claude/skills/
```

---

## 📋 The 6-Slide Master Architecture

| Slide | Mandatory Title | Dominant Visual Anchor | Key Defense Element |
| :--- | :--- | :--- | :--- |
| **Slide 1** | Administrative & Jury Identity | High-contrast 2x2 or 3x2 bordered card grid | Instant registration verification in under 3 seconds |
| **Slide 2** | Problem & Proposed Solution | Dual-Cluster: Problem hub (left) + Solution badges (right) | 1-to-1 mapping between systemic pain and technical capability |
| **Slide 3** | Technical Approach & Architecture | Numbered 6-Station Pipeline with trust boundaries | Explicit offline/no-internet fallback branch + labeled payloads |
| **Slide 4** | Feasibility and Viability | Top Benchmark Table + Bottom Challenge-Mitigation Matrix | Field constraints paired directly with engineered mitigations |
| **Slide 5** | Impacts and Benefits | 4-Step Stakeholder Journey Ribbon | Quantified Indian baseline math + annual savings in ₹ Crore |
| **Slide 6** | Research, References & Proof | TAM/SAM/SOM Bullseye + 3-Tier Sourced Citation Matrix | High-contrast action badges for GitHub repo & 60s demo video |

---

## 🔍 Validation & Testing

Validate this skill against the Agent Skills specification using GitHub CLI:

```bash
gh skill publish --dry-run
```

---

## 📜 Author & License

* **Author:** Sparsh ([@sparsh101sparsh](https://github.com/sparsh101sparsh))
* **License:** Licensed under the [MIT License](https://opensource.org/licenses/MIT).
