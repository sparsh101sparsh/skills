# PptxGenJS Charts & Shapes Reference

## 1. Chart Types & Data Schemas

PptxGenJS supports standard Office charting via `slide.addChart(type, data, options)`.

### Chart Types (`pptx.charts.*`):
- `pptx.charts.BAR` (horizontal bar)
- `pptx.charts.COL` (vertical column)
- `pptx.charts.LINE` (line chart)
- `pptx.charts.PIE` (pie chart)
- `pptx.charts.DOUGHNUT` (doughnut chart)
- `pptx.charts.AREA` (area chart)
- `pptx.charts.SCATTER` (scatter plot)
- `pptx.charts.RADAR` (radar / spider chart)

---

### Data Schema Format
Data is an array of series objects:
```javascript
const chartData = [
  {
    name: 'North America',
    labels: ['Q1', 'Q2', 'Q3', 'Q4'],
    values: [4.5, 5.2, 6.1, 7.8]
  },
  {
    name: 'Europe',
    labels: ['Q1', 'Q2', 'Q3', 'Q4'],
    values: [2.8, 3.4, 3.9, 4.6]
  }
];
```

---

### Chart Examples

#### Multi-Series Column Chart
```javascript
slide.addChart(pptx.charts.COL, chartData, {
  x: 0.8,
  y: 1.8,
  w: 5.0,
  h: 3.2,
  chartColors: ['1E3A8A', '0D9488'],
  showTitle: true,
  title: 'Revenue by Region ($M)',
  titleFontSize: 13,
  titleColor: '0F172A',
  showLegend: true,
  legendPos: 'b', // 't' | 'b' | 'l' | 'r' | 'tr'
  legendFontSize: 10,
  showVal: true,  // Show data labels on bars
  dataLabelColor: 'FFFFFF',
  dataLabelFontSize: 9,
  valAxisMaxVal: 10,
  valAxisMinVal: 0,
  valGridLine: { style: 'dash', color: 'E2E8F0' },
  catGridLine: { style: 'none' }
});
```

#### Doughnut / Pie Chart
```javascript
const pieData = [
  {
    name: 'Market Share',
    labels: ['Enterprise', 'Mid-Market', 'SMB'],
    values: [55, 30, 15]
  }
];

slide.addChart(pptx.charts.DOUGHNUT, pieData, {
  x: 5.8,
  y: 1.8,
  w: 3.4,
  h: 3.2,
  chartColors: ['1E3A8A', '0D9488', 'F59E0B'],
  showLegend: true,
  legendPos: 'b',
  showPercent: true,
  holeSize: 60 // percent (for doughnut)
});
```

#### Line Chart with Smooth Curves
```javascript
slide.addChart(pptx.charts.LINE, [
  {
    name: 'Active Users (Thousands)',
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    values: [120, 145, 180, 230, 310, 420]
  }
], {
  x: 0.8,
  y: 1.8,
  w: 8.4,
  h: 3.2,
  chartColors: ['2563EB'],
  lineSmooth: true,
  lineSize: 3,
  lineDataSymbol: 'circle',
  lineDataSymbolSize: 6,
  showLegend: false
});
```

---

## 2. Shape Types (`pptx.shapes.*`)

PptxGenJS includes common geometric and flow shapes:

| Shape Constant | Description | Common Usage |
|---|---|---|
| `pptx.shapes.RECTANGLE` | Sharp rectangle | Containers, background bars, headers |
| `pptx.shapes.ROUNDED_RECTANGLE` | Rounded corner rect | Cards, pills, badges, buttons (`rectRadius: 0.1`) |
| `pptx.shapes.ELLIPSE` | Circle / Oval | Avatars, icon backgrounds, status indicators |
| `pptx.shapes.LINE` | Straight line | Section dividers, timeline spines |
| `pptx.shapes.RIGHT_ARROW` | Forward arrow | Process workflows, steps, direction |
| `pptx.shapes.CHEVRON` | Chevron arrow | Sequential stage pipelines |
| `pptx.shapes.BALLOON` / `CALLOUT` | Speech bubble | Quotes, testimonials, annotations |
| `pptx.shapes.DIAMOND` | Decision diamond | Architecture flows, decision trees |
| `pptx.shapes.STAR_5_POINT` | 5-point star | Ratings, highlights, featured items |

### Common Shape Options
- `fill`: `{ color: 'HEX', transparency: 0-100 }`
- `line`: `{ color: 'HEX', width: pt, dashType: 'solid'|'dash'|'dot' }`
- `rectRadius`: Radius proportion for rounded rectangles (e.g. `0.1`)
- `shadow`: `{ type: 'outer', color: 'HEX', blur: 3, offset: 2, angle: 90, opacity: 0.1 }`
- `rotate`: Rotation degrees (e.g. `90`, `180`)
