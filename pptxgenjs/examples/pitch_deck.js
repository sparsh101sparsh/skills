/**
 * Modern 5-Slide Pitch Deck Generator
 * Demonstrates slide masters, typography, card layouts, KPI stats, charts, and tables.
 *
 * Run via:
 *   node pitch_deck.js [output_filename.pptx]
 */

const pptxgen = require('pptxgenjs');
const path = require('path');

async function createPitchDeck(outputPath = 'modern_pitch_deck.pptx') {
  const pptx = new pptxgen();

  // 16:9 Modern Widescreen Layout (10" x 5.625")
  pptx.layout = 'LAYOUT_16x9';
  pptx.title = 'NovaScale Series A Investor Deck';
  pptx.author = 'NovaScale Inc.';

  // Color Palette
  const C = {
    brandDark: '0B132B',
    brandNavy: '1C2541',
    brandBlue: '3A86FF',
    accentCyan: '00F5D4',
    accentPurple: '7209B7',
    surfaceLight: 'F8FAFC',
    surfaceCard: 'FFFFFF',
    textMain: '0F172A',
    textMuted: '64748B',
    border: 'E2E8F0',
    white: 'FFFFFF'
  };

  const FONT = 'Segoe UI';

  // Define Reusable Clean Slide Master for Content Slides
  pptx.defineSlideMaster({
    title: 'CLEAN_SLIDE',
    background: { color: C.surfaceLight },
    objects: [
      // Top subtle accent bar
      { rect: { x: 0, y: 0, w: '100%', h: 0.08, fill: { color: C.brandBlue } } },
      // Footer text
      { text: {
          text: 'NovaScale Inc. — Series A Presentation',
          options: { x: 0.8, y: 5.25, w: 6.0, h: 0.3, fontFace: FONT, fontSize: 9, color: C.textMuted }
        }
      }
    ],
    slideNumber: { x: 9.0, y: 5.25, fontFace: FONT, fontSize: 9, color: C.textMuted }
  });

  // Helper for slide headers
  function addHeader(slide, title, category) {
    if (category) {
      slide.addText(category.toUpperCase(), {
        x: 0.8,
        y: 0.45,
        w: 8.4,
        h: 0.3,
        fontFace: FONT,
        fontSize: 10,
        bold: true,
        color: C.brandBlue
      });
    }
    slide.addText(title, {
      x: 0.8,
      y: 0.75,
      w: 8.4,
      h: 0.55,
      fontFace: FONT,
      fontSize: 24,
      bold: true,
      color: C.textMain
    });
  }

  // =========================================================================
  // SLIDE 1: Title Slide (Dark Hero)
  // =========================================================================
  {
    const slide = pptx.addSlide();
    slide.background = { color: C.brandDark };

    // Decorative gradient-like accent rectangles
    slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x: 0.8,
      y: 1.0,
      w: 1.4,
      h: 0.35,
      fill: { color: C.brandNavy },
      line: { color: C.brandBlue, width: 1 },
      rectRadius: 0.15
    });
    slide.addText('SERIES A ROUND', {
      x: 0.8,
      y: 1.0,
      w: 1.4,
      h: 0.35,
      fontFace: FONT,
      fontSize: 9,
      bold: true,
      color: C.accentCyan,
      align: 'center',
      valign: 'middle'
    });

    slide.addText('Next-Generation Autonomous\nCloud Infrastructure', {
      x: 0.8,
      y: 1.6,
      w: 8.4,
      h: 1.6,
      fontFace: FONT,
      fontSize: 36,
      bold: true,
      color: C.white,
      lineSpacingMultiple: 1.15
    });

    slide.addText('NovaScale optimizes multi-cloud compute workloads with real-time AI agents,\nslashing compute waste by 64% while maintaining 99.999% reliability.', {
      x: 0.8,
      y: 3.4,
      w: 8.4,
      h: 0.8,
      fontFace: FONT,
      fontSize: 15,
      color: '94A3B8',
      lineSpacingMultiple: 1.2
    });

    slide.addText('Confidential  •  October 2026  •  Presented by Founder & CEO', {
      x: 0.8,
      y: 4.8,
      w: 8.4,
      h: 0.4,
      fontFace: FONT,
      fontSize: 11,
      color: '64748B'
    });
  }

  // =========================================================================
  // SLIDE 2: Problem & Solution (Two-Column Comparison Cards)
  // =========================================================================
  {
    const slide = pptx.addSlide({ masterName: 'CLEAN_SLIDE' });
    addHeader(slide, 'The Multi-Cloud Efficiency Dilemma', 'Market Challenge & Solution');

    const colW = 4.0;
    const cardH = 3.6;
    const cardY = 1.45;

    // Card 1: Problem (Red-tinted accent)
    slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x: 0.8,
      y: cardY,
      w: colW,
      h: cardH,
      fill: { color: C.surfaceCard },
      line: { color: 'FCA5A5', width: 1.5 },
      rectRadius: 0.12
    });
    slide.addText('THE PROBLEM', {
      x: 1.1,
      y: cardY + 0.3,
      w: colW - 0.6,
      h: 0.35,
      fontFace: FONT,
      fontSize: 11,
      bold: true,
      color: 'DC2626'
    });
    slide.addText('Runaway Cloud Waste & Complexity', {
      x: 1.1,
      y: cardY + 0.65,
      w: colW - 0.6,
      h: 0.5,
      fontFace: FONT,
      fontSize: 16,
      bold: true,
      color: C.textMain
    });
    slide.addText([
      { text: 'Overprovisioning: ', options: { bold: true, color: C.textMain } },
      { text: 'Enterprises idle 38% of GPU and CPU nodes to handle unpredicted traffic bursts.\n', options: { color: C.textMuted } },
      { text: 'Manual Tuning: ', options: { bold: true, color: C.textMain } },
      { text: 'DevOps teams spend hundreds of hours weekly manually tweaking auto-scaler configs.\n', options: { color: C.textMuted } },
      { text: 'Siloed Observability: ', options: { bold: true, color: C.textMain } },
      { text: 'Monitoring tools show cost spikes after the fact instead of preventing them.', options: { color: C.textMuted } }
    ], {
      x: 1.1,
      y: cardY + 1.25,
      w: colW - 0.6,
      h: 2.1,
      fontFace: FONT,
      fontSize: 11,
      lineSpacingMultiple: 1.25
    });

    // Card 2: Solution (Blue/Green accent)
    slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x: 5.2,
      y: cardY,
      w: colW,
      h: cardH,
      fill: { color: C.surfaceCard },
      line: { color: C.brandBlue, width: 1.5 },
      rectRadius: 0.12
    });
    slide.addText('THE SOLUTION', {
      x: 5.5,
      y: cardY + 0.3,
      w: colW - 0.6,
      h: 0.35,
      fontFace: FONT,
      fontSize: 11,
      bold: true,
      color: C.brandBlue
    });
    slide.addText('Zero-Config Autonomous Orchestration', {
      x: 5.5,
      y: cardY + 0.65,
      w: colW - 0.6,
      h: 0.5,
      fontFace: FONT,
      fontSize: 16,
      bold: true,
      color: C.textMain
    });
    slide.addText([
      { text: 'Predictive Right-Sizing: ', options: { bold: true, color: C.textMain } },
      { text: 'Neural predictors anticipate traffic spikes 15 minutes before they hit.\n', options: { color: C.textMuted } },
      { text: 'Autonomous Action: ', options: { bold: true, color: C.textMain } },
      { text: 'Self-adjusting Kubernetes pod limits that rebalance workloads without human intervention.\n', options: { color: C.textMuted } },
      { text: 'Instant ROI: ', options: { bold: true, color: C.textMain } },
      { text: 'Drops multi-cloud bills by >50% within 48 hours of single Helm chart deployment.', options: { color: C.textMuted } }
    ], {
      x: 5.5,
      y: cardY + 1.25,
      w: colW - 0.6,
      h: 2.1,
      fontFace: FONT,
      fontSize: 11,
      lineSpacingMultiple: 1.25
    });

    slide.addNotes('Highlight customer pain points in multi-cloud Kubernetes environments and emphasize automated prevention over retroactive monitoring.');
  }

  // =========================================================================
  // SLIDE 3: Traction & Performance KPIs (3 Stat Cards)
  // =========================================================================
  {
    const slide = pptx.addSlide({ masterName: 'CLEAN_SLIDE' });
    addHeader(slide, 'Rapid Market Adoption & Efficiency', 'Traction & Unit Economics');

    const stats = [
      { val: '$14.2M', label: 'ARR Run-Rate', sub: '+310% YoY growth', color: C.brandBlue },
      { val: '142%', label: 'Net Dollar Retention', sub: 'Top decile SaaS retention', color: '16A34A' },
      { val: '64%', label: 'Average Cloud Savings', sub: 'Verified by Fortune 500 audits', color: C.accentPurple }
    ];

    const cardW = 2.6;
    const cardH = 3.6;
    const gap = 0.3;
    const startX = 0.8;
    const cardY = 1.45;

    stats.forEach((stat, idx) => {
      const curX = startX + idx * (cardW + gap);

      // Card container
      slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
        x: curX,
        y: cardY,
        w: cardW,
        h: cardH,
        fill: { color: C.surfaceCard },
        line: { color: C.border, width: 1 },
        rectRadius: 0.12
      });

      // Top colored indicator line
      slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
        x: curX,
        y: cardY,
        w: cardW,
        h: 0.08,
        fill: { color: stat.color },
        line: { color: stat.color }
      });

      // Main big number
      slide.addText(stat.val, {
        x: curX + 0.2,
        y: cardY + 0.5,
        w: cardW - 0.4,
        h: 1.0,
        fontFace: FONT,
        fontSize: 36,
        bold: true,
        color: stat.color,
        align: 'center',
        valign: 'middle'
      });

      // Label
      slide.addText(stat.label, {
        x: curX + 0.2,
        y: cardY + 1.6,
        w: cardW - 0.4,
        h: 0.5,
        fontFace: FONT,
        fontSize: 14,
        bold: true,
        color: C.textMain,
        align: 'center',
        valign: 'top'
      });

      // Subtitle
      slide.addText(stat.sub, {
        x: curX + 0.2,
        y: cardY + 2.2,
        w: cardW - 0.4,
        h: 0.6,
        fontFace: FONT,
        fontSize: 11,
        color: C.textMuted,
        align: 'center',
        valign: 'top'
      });
    });
  }

  // =========================================================================
  // SLIDE 4: Revenue Growth & Cohorts (Column Chart & Table)
  // =========================================================================
  {
    const slide = pptx.addSlide({ masterName: 'CLEAN_SLIDE' });
    addHeader(slide, 'Consistent Quarter-over-Quarter Expansion', 'Financial Trajectory');

    // Chart Data (ARR Breakdown in $M)
    const chartData = [
      {
        name: 'Enterprise ARR',
        labels: ['Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026'],
        values: [1.8, 2.7, 4.1, 6.2, 9.4, 14.2]
      }
    ];

    slide.addChart(pptx.charts.BAR, chartData, {
      x: 0.8,
      y: 1.5,
      w: 4.6,
      h: 3.5,
      barDir: 'col',
      chartColors: [C.brandBlue],
      showLegend: false,
      showTitle: true,
      title: 'ARR Growth ($M)',
      titleFontSize: 12,
      titleColor: C.textMain,
      showVal: true,
      dataLabelColor: C.white,
      dataLabelFontSize: 9,
      valGridLine: { color: C.border, style: 'dash' },
      catGridLine: { style: 'none' }
    });

    // Comparison Table
    const tableRows = [
      [
        { text: 'Segment', options: { bold: true, fill: { color: C.brandDark }, color: C.white } },
        { text: 'Customers', options: { bold: true, fill: { color: C.brandDark }, color: C.white, align: 'right' } },
        { text: 'ACV', options: { bold: true, fill: { color: C.brandDark }, color: C.white, align: 'right' } },
        { text: 'Payback', options: { bold: true, fill: { color: C.brandDark }, color: C.white, align: 'center' } }
      ],
      [
        { text: 'Global 2000', options: { bold: true } },
        { text: '48', options: { align: 'right' } },
        { text: '$185,000', options: { align: 'right' } },
        { text: '4.2 Mo', options: { align: 'center', color: '16A34A', bold: true } }
      ],
      [
        { text: 'Mid-Market Tech', options: { bold: true } },
        { text: '164', options: { align: 'right' } },
        { text: '$45,000', options: { align: 'right' } },
        { text: '3.1 Mo', options: { align: 'center', color: '16A34A', bold: true } }
      ],
      [
        { text: 'High-Growth AI', options: { bold: true } },
        { text: '92', options: { align: 'right' } },
        { text: '$88,000', options: { align: 'right' } },
        { text: '2.4 Mo', options: { align: 'center', color: '16A34A', bold: true } }
      ]
    ];

    slide.addTable(tableRows, {
      x: 5.6,
      y: 1.8,
      w: 3.6,
      colW: [1.4, 0.7, 0.9, 0.6],
      rowH: 0.45,
      fontSize: 10,
      fontFace: FONT,
      border: { type: 'solid', pt: 0.5, color: C.border }
    });
  }

  // =========================================================================
  // SLIDE 5: Strategic Growth Roadmap (Process Pipeline)
  // =========================================================================
  {
    const slide = pptx.addSlide({ masterName: 'CLEAN_SLIDE' });
    addHeader(slide, '2026–2027 Execution Milestones', 'Strategic Roadmap');

    const steps = [
      { qtr: 'Q3 2026', title: 'Global 2000 Focus', desc: 'Expand enterprise sales team across North America and EMEA.' },
      { qtr: 'Q4 2026', title: 'Kubernetes LLM Agent', desc: 'Launch autonomous zero-shot memory cache & GPU partition rebalancer.' },
      { qtr: 'Q1 2027', title: 'FedRAMP Compliance', desc: 'Secure public sector authorizations for aerospace and defense clouds.' },
      { qtr: 'Q2 2027', title: '$35M ARR Target', desc: 'Achieve GAAP cash flow positive with 250+ enterprise deployments.' }
    ];

    const stepW = 1.95;
    const gap = 0.2;
    const startX = 0.8;
    const cardY = 1.6;

    steps.forEach((step, idx) => {
      const curX = startX + idx * (stepW + gap);

      // Card
      slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
        x: curX,
        y: cardY,
        w: stepW,
        h: 3.3,
        fill: { color: C.surfaceCard },
        line: { color: C.border, width: 1 },
        rectRadius: 0.1
      });

      // Step pill
      slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
        x: curX + 0.15,
        y: cardY + 0.2,
        w: stepW - 0.3,
        h: 0.35,
        fill: { color: idx === 0 ? C.brandBlue : C.surfaceLight },
        line: { color: idx === 0 ? C.brandBlue : C.border, width: 1 },
        rectRadius: 0.08
      });
      slide.addText(step.qtr, {
        x: curX + 0.15,
        y: cardY + 0.2,
        w: stepW - 0.3,
        h: 0.35,
        fontFace: FONT,
        fontSize: 10,
        bold: true,
        color: idx === 0 ? C.white : C.textMuted,
        align: 'center',
        valign: 'middle'
      });

      // Milestone title
      slide.addText(step.title, {
        x: curX + 0.15,
        y: cardY + 0.75,
        w: stepW - 0.3,
        h: 0.6,
        fontFace: FONT,
        fontSize: 13,
        bold: true,
        color: C.textMain,
        valign: 'top'
      });

      // Milestone details
      slide.addText(step.desc, {
        x: curX + 0.15,
        y: cardY + 1.4,
        w: stepW - 0.3,
        h: 1.7,
        fontFace: FONT,
        fontSize: 11,
        color: C.textMuted,
        valign: 'top',
        lineSpacingMultiple: 1.2
      });
    });
  }

  const finalPath = path.resolve(process.cwd(), outputPath);
  await pptx.writeFile({ fileName: finalPath });
  console.log(`Success! Pitch deck created at: ${finalPath}`);
}

const outputFile = process.argv[2] || 'modern_pitch_deck.pptx';
createPitchDeck(outputFile).catch(err => {
  console.error('Error generating pitch deck:', err);
  process.exit(1);
});
