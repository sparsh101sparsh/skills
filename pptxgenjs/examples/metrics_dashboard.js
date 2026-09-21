/**
 * Executive Metrics & Operations Dashboard Generator
 * Demonstrates Doughnut charts, Bar charts, multi-series tables, and KPI cards.
 *
 * Run via:
 *   node metrics_dashboard.js [output_filename.pptx]
 */

const pptxgen = require('pptxgenjs');
const path = require('path');

async function createDashboardDeck(outputPath = 'executive_dashboard.pptx') {
  const pptx = new pptxgen();

  pptx.layout = 'LAYOUT_16x9';
  pptx.title = 'Executive Operations & Financial Dashboard';
  pptx.author = 'VP Operations';

  const C = {
    bg: 'F1F5F9',
    card: 'FFFFFF',
    textMain: '0F172A',
    textMuted: '64748B',
    primary: '2563EB',
    teal: '0D9488',
    amber: 'D97706',
    rose: 'E11D48',
    green: '16A34A',
    border: 'CBD5E1'
  };

  const FONT = 'Segoe UI';

  pptx.defineSlideMaster({
    title: 'DASHBOARD_MASTER',
    background: { color: C.bg },
    objects: [
      { rect: { x: 0, y: 0, w: '100%', h: 0.08, fill: { color: C.primary } } },
      { text: {
          text: 'Executive Business Intelligence  •  Strictly Confidential',
          options: { x: 0.8, y: 5.25, w: 6.0, h: 0.3, fontFace: FONT, fontSize: 9, color: C.textMuted }
        }
      }
    ],
    slideNumber: { x: 9.0, y: 5.25, fontFace: FONT, fontSize: 9, color: C.textMuted }
  });

  // SLIDE 1: KPI Overview Dashboard
  {
    const slide = pptx.addSlide({ masterName: 'DASHBOARD_MASTER' });

    slide.addText('Q3 2026 Executive Performance Dashboard', {
      x: 0.8,
      y: 0.45,
      w: 8.4,
      h: 0.5,
      fontFace: FONT,
      fontSize: 22,
      bold: true,
      color: C.textMain
    });
    slide.addText('Consolidated operational health, pipeline velocity, and revenue distribution', {
      x: 0.8,
      y: 0.95,
      w: 8.4,
      h: 0.35,
      fontFace: FONT,
      fontSize: 12,
      color: C.textMuted
    });

    // Top 4 KPI Cards
    const kpis = [
      { label: 'GROSS REVENUE', val: '$28.4M', diff: '+24% YoY', good: true },
      { label: 'GROSS MARGIN', val: '78.2%', diff: '+3.1 pts', good: true },
      { label: 'CAC PAYBACK', val: '4.8 Mo', diff: '-1.2 Mo', good: true },
      { label: 'NET CHURN', val: '0.4%', diff: 'Target <0.5%', good: true }
    ];

    const kpiW = 1.95;
    const gap = 0.2;
    const startX = 0.8;
    const kpiY = 1.4;

    kpis.forEach((kpi, idx) => {
      const curX = startX + idx * (kpiW + gap);
      slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
        x: curX,
        y: kpiY,
        w: kpiW,
        h: 1.1,
        fill: { color: C.card },
        line: { color: C.border, width: 1 },
        rectRadius: 0.08
      });
      slide.addText(kpi.label, {
        x: curX + 0.1,
        y: kpiY + 0.1,
        w: kpiW - 0.2,
        h: 0.25,
        fontFace: FONT,
        fontSize: 9,
        bold: true,
        color: C.textMuted
      });
      slide.addText(kpi.val, {
        x: curX + 0.1,
        y: kpiY + 0.35,
        w: kpiW - 0.2,
        h: 0.45,
        fontFace: FONT,
        fontSize: 20,
        bold: true,
        color: C.textMain
      });
      slide.addText(kpi.diff, {
        x: curX + 0.1,
        y: kpiY + 0.78,
        w: kpiW - 0.2,
        h: 0.25,
        fontFace: FONT,
        fontSize: 10,
        bold: true,
        color: kpi.good ? C.green : C.rose
      });
    });

    // Left Chart: Revenue Trend (Column Chart)
    slide.addChart(pptx.charts.BAR, [
      {
        name: 'Actual Revenue',
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'],
        values: [2.6, 2.8, 3.1, 3.0, 3.3, 3.6, 3.8, 4.0, 4.2]
      }
    ], {
      x: 0.8,
      y: 2.7,
      w: 4.8,
      h: 2.3,
      barDir: 'col',
      chartColors: [C.primary],
      showTitle: true,
      title: 'Monthly Revenue Progression ($M)',
      titleFontSize: 11,
      titleColor: C.textMain,
      showLegend: false,
      valGridLine: { color: 'E2E8F0', style: 'dash' }
    });

    // Right Chart: Revenue by Segment (Doughnut Chart)
    slide.addChart(pptx.charts.DOUGHNUT, [
      {
        name: 'Revenue Share',
        labels: ['Enterprise', 'Mid-Market', 'Government', 'SMB'],
        values: [48, 28, 16, 8]
      }
    ], {
      x: 5.8,
      y: 2.7,
      w: 3.4,
      h: 2.3,
      chartColors: [C.primary, C.teal, C.amber, C.rose],
      showTitle: true,
      title: 'Revenue Share by Customer Segment',
      titleFontSize: 11,
      titleColor: C.textMain,
      showLegend: true,
      legendPos: 'b',
      holeSize: 65,
      showPercent: true
    });
  }

  const finalPath = path.resolve(process.cwd(), outputPath);
  await pptx.writeFile({ fileName: finalPath });
  console.log(`Success! Dashboard deck created at: ${finalPath}`);
}

const outputFile = process.argv[2] || 'executive_dashboard.pptx';
createDashboardDeck(outputFile).catch(err => {
  console.error('Error generating dashboard deck:', err);
  process.exit(1);
});
