# PptxGenJS Comprehensive API Reference

## 1. Presentation Initialization & Setup

```javascript
const pptxgen = require('pptxgenjs');
const pptx = new pptxgen();

// Layouts: 'LAYOUT_16x9' (10" x 5.625"), 'LAYOUT_WIDE' (13.33" x 7.5"), 'LAYOUT_4x3' (10" x 7.5"), 'LAYOUT_16x10' (10" x 6.25")
pptx.layout = 'LAYOUT_16x9';

// Custom layout (e.g. A4 landscape)
pptx.defineLayout({ name: 'A4', width: 11.69, height: 8.27 });
pptx.layout = 'A4';

// Metadata
pptx.title = 'Executive Strategy Briefing';
pptx.author = 'Design Team';
pptx.company = 'Acme Corp';
pptx.subject = 'Q3 Results';
pptx.rtlMode = false;
```

---

## 2. Master Slides (`defineSlideMaster`)

Define consistent reusable slide designs with backgrounds, recurring logos, headers, and slide numbers:

```javascript
pptx.defineSlideMaster({
  title: 'BRAND_MASTER',
  background: { color: 'F8FAFC' },
  objects: [
    // Top banner accent
    { rect: { x: 0, y: 0, w: '100%', h: 0.1, fill: { color: '1E3A8A' } } },
    // Footer label
    { text: {
        text: 'Acme Corp — Confidential',
        options: { x: 0.8, y: '92%', w: 5.0, h: 0.4, fontSize: 9, color: '94A3B8' }
      }
    }
  ],
  slideNumber: { x: '90%', y: '92%', fontSize: 9, color: '94A3B8' }
});

// Using the master slide
const slide = pptx.addSlide({ masterName: 'BRAND_MASTER' });
```

---

## 3. Adding Text (`slide.addText`)

### Basic Text Box
```javascript
slide.addText('Slide Title', {
  x: 0.8,
  y: 0.6,
  w: 8.4,
  h: 0.8,
  fontFace: 'Segoe UI', // Arial, Calibri, Trebuchet MS, Georgia, etc.
  fontSize: 28,
  color: '0F172A',      // Hex color without #
  bold: true,
  italic: false,
  underline: false,
  align: 'left',        // 'left' | 'center' | 'right' | 'justify'
  valign: 'top',        // 'top' | 'middle' | 'bottom'
  margin: [0.1, 0.1, 0.1, 0.1], // [top, right, bottom, left] in inches
  lineSpacingMultiple: 1.15
});
```

### Multi-Styled Formatted Text Runs & Bullets
```javascript
slide.addText([
  {
    text: 'Key Takeaway: ',
    options: { bold: true, color: '1E3A8A', fontSize: 16 }
  },
  {
    text: 'Revenue grew by 35% across EMEA.\n',
    options: { bold: false, color: '334155', fontSize: 16 }
  },
  {
    text: 'First bullet point with nested detail',
    options: { bullet: true, color: '475569', fontSize: 14, indentLevel: 0 }
  },
  {
    text: 'Sub-bullet with deeper context',
    options: { bullet: true, color: '64748B', fontSize: 12, indentLevel: 1 }
  }
], {
  x: 0.8,
  y: 1.8,
  w: 8.4,
  h: 3.2,
  paraSpaceAfter: 8
});
```

### Text Box Background & Border
```javascript
slide.addText('Highlight Callout', {
  x: 1.0,
  y: 2.0,
  w: 8.0,
  h: 1.2,
  fill: { color: 'EFF6FF' },
  line: { color: '3B82F6', width: 1.5, dashType: 'solid' },
  rectRadius: 0.1,
  color: '1E40AF',
  fontSize: 16,
  align: 'center',
  valign: 'middle'
});
```

---

## 4. Adding Shapes (`slide.addShape`)

Shapes are great for cards, KPI cards, dividers, badges, and process flows.

```javascript
// Card Background
slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: 0.8,
  y: 1.8,
  w: 2.6,
  h: 3.2,
  fill: { color: 'FFFFFF' },
  line: { color: 'E2E8F0', width: 1 },
  rectRadius: 0.12,
  shadow: { type: 'outer', color: '000000', opacity: 0.08, blur: 4, offset: 2, angle: 90 }
});

// Accent Line / Divider
slide.addShape(pptx.shapes.LINE, {
  x: 0.8,
  y: 1.4,
  w: 8.4,
  h: 0,
  line: { color: 'CBD5E1', width: 1 }
});

// Category Badge / Pill
slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: 1.0,
  y: 2.0,
  w: 1.2,
  h: 0.35,
  fill: { color: 'DCFCE7' },
  rectRadius: 0.15
});
slide.addText('GROWTH', {
  x: 1.0,
  y: 2.0,
  w: 1.2,
  h: 0.35,
  fontSize: 10,
  bold: true,
  color: '15803D',
  align: 'center',
  valign: 'middle'
});
```

---

## 5. Adding Tables (`slide.addTable`)

Tables accept a 2D array of cells (strings or formatted cell objects):

```javascript
const tableRows = [
  // Header row
  [
    { text: 'Quarter', options: { bold: true, fill: { color: '1E3A8A' }, color: 'FFFFFF', align: 'left' } },
    { text: 'Revenue', options: { bold: true, fill: { color: '1E3A8A' }, color: 'FFFFFF', align: 'right' } },
    { text: 'Target', options: { bold: true, fill: { color: '1E3A8A' }, color: 'FFFFFF', align: 'right' } },
    { text: 'YoY Growth', options: { bold: true, fill: { color: '1E3A8A' }, color: 'FFFFFF', align: 'center' } }
  ],
  // Data rows
  [
    { text: 'Q1 2026', options: { fill: { color: 'FFFFFF' } } },
    { text: '$4.2M', options: { fill: { color: 'FFFFFF' }, align: 'right' } },
    { text: '$4.0M', options: { fill: { color: 'FFFFFF' }, align: 'right' } },
    { text: '+22%', options: { fill: { color: 'FFFFFF' }, align: 'center', color: '16A34A', bold: true } }
  ],
  [
    { text: 'Q2 2026', options: { fill: { color: 'F8FAFC' } } },
    { text: '$5.1M', options: { fill: { color: 'F8FAFC' }, align: 'right' } },
    { text: '$4.8M', options: { fill: { color: 'F8FAFC' }, align: 'right' } },
    { text: '+28%', options: { fill: { color: 'F8FAFC' }, align: 'center', color: '16A34A', bold: true } }
  ]
];

slide.addTable(tableRows, {
  x: 0.8,
  y: 1.8,
  w: 8.4,
  colW: [2.4, 2.0, 2.0, 2.0],
  rowH: 0.45,
  fontSize: 12,
  fontFace: 'Segoe UI',
  border: { type: 'solid', pt: 0.5, color: 'E2E8F0' },
  margin: [0.08, 0.1, 0.08, 0.1]
});
```

---

## 6. Adding Images & Icons (`slide.addImage`)

Supports local files, URLs, base64 strings, and SVGs:

```javascript
// Local file path
slide.addImage({
  path: '/path/to/diagram.png',
  x: 4.8,
  y: 1.8,
  w: 4.4,
  h: 3.2,
  sizing: { type: 'contain', w: 4.4, h: 3.2 } // or 'cover' | 'crop'
});

// Base64 data
slide.addImage({
  data: 'data:image/png;base64,iVBORw0KGgoAAAANS...',
  x: 0.8,
  y: 0.8,
  w: 1.5,
  h: 0.6
});
```

---

## 7. Speaker Notes & Sections

```javascript
// Sections organize slides inside PowerPoint
pptx.addSection({ title: 'Financial Deep Dive' });

// Speaker notes for presenter view
slide.addNotes('Emphasize that Q2 exceeded expectations due to enterprise expansion. Take questions on EMEA churn.');
```

---

## 8. Exporting / Saving

```javascript
// Save directly to disk
await pptx.writeFile({ fileName: 'presentation.pptx' });

// Compressed output (saves up to 30% file size)
await pptx.writeFile({ fileName: 'presentation.pptx', compression: true });
```
