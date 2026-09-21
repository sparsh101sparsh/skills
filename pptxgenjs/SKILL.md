---
name: pptxgenjs
description: >-
  Create and generate PowerPoint (.pptx) presentations programmatically using PptxGenJS and Node.js.
  Use when designing or generating new PowerPoint presentations from scratch, converting data or JSON into slide decks,
  creating executive pitch decks, KPI dashboards, automated business reports, and charts/tables via code.
---

# PptxGenJS Presentation Engineering Skill

You are an expert **presentation designer and programmatic slide engineer**. You create polished, high-impact, modern PowerPoint (`.pptx`) decks from scratch using **PptxGenJS** in Node.js.

> **When to use PptxGenJS vs pptx-engineer:**
> - **Use `pptxgenjs` (this skill)**: Creating new decks from scratch, converting data/JSON into slides, programmatic batch slide generation, dashboards, and automated reports.
> - **Use `pptx-engineer`**: Modifying or surgically editing existing pre-authored `.pptx` files while preserving complex pre-existing animations and XML layouts.

---

## 1. Quick Start & Execution Environment

The `pptxgenjs` skill provides an automated, dependency-resolving execution environment for generating PowerPoint presentations programmatically.
To execute any generation script with all dependencies pre-resolved, use the packaged runner:

```bash
# Execute any script using the skill's runner:
node pptxgenjs/scripts/run.js my_presentation.js [output.pptx]
# Or from inside the skill directory:
node scripts/run.js my_presentation.js [output.pptx]
# Or when installed in Antigravity global config:
node ~/.gemini/config/skills/pptxgenjs/scripts/run.js my_presentation.js [output.pptx]

# Or generate directly from a JSON definition (file or stdin pipe):
node pptxgenjs/scripts/quick_gen.js slides.json output.pptx
cat slides.json | node pptxgenjs/scripts/quick_gen.js - output.pptx
```

### Declarative Slide Types Supported by `quick_gen.js`
- **`title`**: Hero slide with `title`, `subtitle`, `author`, `date`
- **`cards`**: Multi-column container cards with `title`, `text`
- **`stats`**: Key performance indicators with `value`, `label`, `change`
- **`table`**: Formatted tables via `headers` & `rows` or 2D `table` array
- **`chart`**: Native Office charts (`col`, `bar`, `line`, `pie`, `doughnut`, `area`) via `chartType` and `data`
- **`bullets`**: Clean takeaway lists via `bullets` or `content` strings

---

## 2. Fundamental Slide Coordinate System

PptxGenJS positions objects using coordinates in **inches** (or percentages):

| Dimension | Default 16:9 (`LAYOUT_16x9`) | Widescreen HD (`LAYOUT_WIDE`) | Standard 4:3 (`LAYOUT_4x3`) |
|---|---|---|---|
| **Width** | **10.0"** | 13.33" | 10.0" |
| **Height** | **5.625"** | 7.50" | 7.50" |

### Safe Margins & Placement Rules (16:9 Default)
- **Left Margin ($X$)**: `0.8"` (minimum `0.5"`)
- **Right Edge**: Keep content within $X + W \le 9.2"$
- **Header Top ($Y$)**: `0.4"` to `0.5"`
- **Category Tracker**: $Y = 0.45"$, $H = 0.3"$, Font Size `10pt` Bold Uppercase
- **Slide Title**: $Y = 0.75"$, $H = 0.55"$, Font Size `24pt` Bold
- **Body Content Area**: $Y = 1.45"$ to $5.0"$, Max Height $3.6"$
- **Footer / Slide Number**: $Y = 5.25"$, Font Size `9pt` Muted

---

## 3. Core Design Principles for Polished Presentations

1. **High Visual Hierarchy**:
   - Every slide needs one dominant takeaway. Never crowd 10 equal-weight bullet points.
   - Use Category Tracker $\rightarrow$ Strong Action Title $\rightarrow$ Structured Visual Containers (Cards, Columns, or Charts).
2. **Card Layouts Over Plain Bullets**:
   - Group information into 2, 3, or 4 visual cards using `pptx.shapes.ROUNDED_RECTANGLE` with subtle borders (`E2E8F0`) and white backgrounds (`FFFFFF`).
3. **Color Palette Discipline**:
   - Limit to 3 core colors:
     - **Background**: Off-white / light slate (`F8FAFC` or `F1F5F9`) or deep navy for hero title slides (`0B132B`).
     - **Primary Brand**: Trust blue or brand tint (`1E3A8A` or `2563EB`).
     - **Accent**: Growth green (`16A34A`), cyan (`00F5D4`), or amber (`D97706`).
     - **Text**: Dark slate (`0F172A`), never pure pitch black (`#000000`). Subtitles in muted slate (`64748B`).
4. **Typography**:
   - Use cross-platform clean sans-serif fonts: `Segoe UI`, `Calibri`, `Arial`, or `Trebuchet MS`.
   - Never drop body text below `11pt`. Headlines: `22pt–28pt`. Big KPI numbers: `32pt–44pt`.

---

## 4. Master Slide Pattern (`defineSlideMaster`)

Always define a reusable Master Slide to keep branding, backgrounds, and footers consistent across all slides:

```javascript
const pptxgen = require('pptxgenjs');
const pptx = new pptxgen();

pptx.layout = 'LAYOUT_16x9';

// Define master template
pptx.defineSlideMaster({
  title: 'EXECUTIVE_MASTER',
  background: { color: 'F8FAFC' },
  objects: [
    { rect: { x: 0, y: 0, w: '100%', h: 0.08, fill: { color: '2563EB' } } },
    { text: {
        text: 'Acme Corp  •  Confidential',
        options: { x: 0.8, y: 5.25, w: 5.0, h: 0.3, fontFace: 'Segoe UI', fontSize: 9, color: '64748B' }
      }
    }
  ],
  slideNumber: { x: 9.0, y: 5.25, fontFace: 'Segoe UI', fontSize: 9, color: '64748B' }
});

// Add slides inheriting this master
const slide = pptx.addSlide({ masterName: 'EXECUTIVE_MASTER' });
```

---

## 5. Visual Building Blocks Cheatsheet

### 5.1 Card Containers (Rounded Rectangles)
```javascript
slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: 0.8,
  y: 1.5,
  w: 2.6,
  h: 3.5,
  fill: { color: 'FFFFFF' },
  line: { color: 'E2E8F0', width: 1 },
  rectRadius: 0.12
});
```

### 5.2 Big KPI Number Callouts
```javascript
// Large metric number
slide.addText('$14.2M', {
  x: 0.8, y: 1.8, w: 2.6, h: 0.8,
  fontFace: 'Segoe UI', fontSize: 36, bold: true, color: '2563EB', align: 'center'
});
// Metric label
slide.addText('Annual Recurring Revenue', {
  x: 0.8, y: 2.6, w: 2.6, h: 0.4,
  fontFace: 'Segoe UI', fontSize: 13, bold: true, color: '0F172A', align: 'center'
});
// Trend badge
slide.addText('+42% YoY', {
  x: 0.8, y: 3.0, w: 2.6, h: 0.35,
  fontFace: 'Segoe UI', fontSize: 11, bold: true, color: '16A34A', align: 'center'
});
```

### 5.3 Modern Styled Tables
```javascript
const rows = [
  [
    { text: 'Category', options: { fill: { color: '0B132B' }, color: 'FFFFFF', bold: true } },
    { text: 'Score', options: { fill: { color: '0B132B' }, color: 'FFFFFF', bold: true, align: 'right' } }
  ],
  [
    { text: 'Reliability SLA', options: { fill: { color: 'FFFFFF' } } },
    { text: '99.99%', options: { fill: { color: 'FFFFFF' }, align: 'right', bold: true, color: '16A34A' } }
  ]
];
slide.addTable(rows, {
  x: 0.8, y: 1.5, w: 8.4,
  colW: [5.4, 3.0], rowH: 0.45,
  fontSize: 11, fontFace: 'Segoe UI',
  border: { type: 'solid', pt: 0.5, color: 'E2E8F0' }
});
```

### 5.4 Charts (Column, Bar, Doughnut, Line)
```javascript
slide.addChart(pptx.charts.BAR, [
  { name: 'Revenue', labels: ['Q1', 'Q2', 'Q3', 'Q4'], values: [3.2, 4.5, 5.8, 7.4] }
], {
  x: 0.8, y: 1.5, w: 5.0, h: 3.4,
  barDir: 'col', // 'col' for vertical column chart, 'bar' for horizontal bar chart
  chartColors: ['2563EB'],
  showTitle: true, title: 'Quarterly Revenue ($M)',
  valGridLine: { color: 'E2E8F0', style: 'dash' }
});
```

---

## 6. Packaged Tools & References

| File | Purpose |
|---|---|
| [`scripts/run.js`](./scripts/run.js) | Universal runner ensuring module resolution from anywhere |
| [`scripts/quick_gen.js`](./scripts/quick_gen.js) | CLI that compiles JSON slide specifications directly into `.pptx` |
| [`examples/pitch_deck.js`](./examples/pitch_deck.js) | Complete 5-slide venture pitch deck template |
| [`examples/metrics_dashboard.js`](./examples/metrics_dashboard.js) | Executive analytics dashboard with KPIs and dual charts |
| [`references/api_reference.md`](./references/api_reference.md) | In-depth parameter tables for text, tables, shapes, and images |
| [`references/charts_and_shapes.md`](./references/charts_and_shapes.md) | Complete chart types schema and shape catalogue |
| [`tests/verify.js`](./tests/verify.js) | Automated verification test suite and OPC package validator |

---

## 7. Quality Verification Workflow

Before finalizing any generated presentation:
1. **Compile & Run**: Execute script with `node pptxgenjs/scripts/run.js <script.js> <out.pptx>` or `node <script.js> <out.pptx>`.
2. **Validate Output**: Run the automated test runner `npm test` or `node pptxgenjs/tests/verify.js` to ensure the resulting file is a valid `.pptx` archive without runtime exceptions.
3. **No Overflow Guarantee**: Ensure text boxes have sufficient height and lines do not wrap awkwardly.
