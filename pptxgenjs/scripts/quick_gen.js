#!/usr/bin/env node
/**
 * Quick PPTX Generator CLI
 * Reads a JSON presentation definition and generates a polished PowerPoint file.
 *
 * Usage:
 *   node quick_gen.js input.json [output.pptx]
 *   cat input.json | node quick_gen.js - output.pptx
 */

const fs = require('fs');
const path = require('path');
const pptxgen = require('pptxgenjs');

async function main() {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.log(`
Quick PPTX Generator
Usage:
  node quick_gen.js <input.json> [output.pptx]

JSON schema sample:
{
  "title": "Quarterly Business Review",
  "theme": { "primary": "1E3A8A", "secondary": "0D9488", "dark": "0F172A", "light": "F8FAFC" },
  "slides": [
    {
      "type": "title",
      "title": "Q3 Performance Review",
      "subtitle": "Growth, Milestones & Strategic Roadmap",
      "author": "Executive Leadership Team"
    },
    {
      "type": "cards",
      "title": "Core Strategic Pillars",
      "cards": [
        { "title": "Customer First", "text": "Net Promoter Score up to 72 (+14pts YoY)." },
        { "title": "Operational Velocity", "text": "Release cycle reduced from 14 days to 48 hours." },
        { "title": "Sustainable Growth", "text": "ARR expanded 42% YoY with positive cash flow." }
      ]
    },
    {
      "type": "stats",
      "title": "Key Business Metrics",
      "stats": [
        { "value": "$18.4M", "label": "Annual Recurring Revenue", "change": "+42% YoY" },
        { "value": "118%", "label": "Net Dollar Retention", "change": "+6% vs Target" },
        { "value": "99.98%", "label": "Platform Uptime SLA", "change": "Zero Sev-1 Incidents" }
      ]
    }
  ]
}
`);
    process.exit(0);
  }

  const inputFile = args[0];
  let outputFile = args[1];

  let rawData = '';
  if (inputFile === '-') {
    rawData = fs.readFileSync(0, 'utf-8');
  } else {
    rawData = fs.readFileSync(path.resolve(process.cwd(), inputFile), 'utf-8');
    if (!outputFile) {
      outputFile = inputFile.replace(/\.json$/i, '') + '.pptx';
    }
  }

  if (!outputFile) {
    outputFile = 'presentation.pptx';
  }

  const spec = JSON.parse(rawData);
  const pptx = new pptxgen();

  pptx.layout = spec.layout || 'LAYOUT_16x9';
  pptx.author = spec.author || 'PptxGenJS Generator';
  pptx.title = spec.title || 'Presentation';

  const theme = {
    primary: (spec.theme && spec.theme.primary) || '1E3A8A',
    secondary: (spec.theme && spec.theme.secondary) || '0D9488',
    dark: (spec.theme && spec.theme.dark) || '0F172A',
    light: (spec.theme && spec.theme.light) || 'F8FAFC',
    muted: (spec.theme && spec.theme.muted) || '64748B',
    white: 'FFFFFF',
    font: (spec.theme && spec.theme.font) || 'Segoe UI'
  };

  for (const item of (spec.slides || [])) {
    const slide = pptx.addSlide();
    slide.background = { color: theme.light };

    switch (item.type) {
      case 'title': {
        // Full bleed accent bar or background
        slide.background = { color: theme.primary };
        slide.addText(item.title || spec.title, {
          x: 1.0,
          y: 2.0,
          w: 8.0,
          h: 1.5,
          fontFace: theme.font,
          fontSize: 38,
          color: theme.white,
          bold: true,
          valign: 'middle'
        });
        if (item.subtitle) {
          slide.addText(item.subtitle, {
            x: 1.0,
            y: 3.4,
            w: 8.0,
            h: 0.8,
            fontFace: theme.font,
            fontSize: 20,
            color: 'E2E8F0',
            valign: 'top'
          });
        }
        if (item.author || item.date) {
          const footer = [item.author, item.date].filter(Boolean).join(' • ');
          slide.addText(footer, {
            x: 1.0,
            y: 4.6,
            w: 8.0,
            h: 0.5,
            fontFace: theme.font,
            fontSize: 12,
            color: 'CBD5E1'
          });
        }
        break;
      }

      case 'cards': {
        addHeader(slide, item.title, item.subtitle, theme);
        const cards = item.cards || [];
        const count = cards.length;
        const totalW = 8.6;
        const startX = 0.7;
        const cardY = 1.8;
        const cardH = 3.2;
        const gap = 0.25;
        const cardW = (totalW - gap * (count - 1)) / count;

        cards.forEach((card, idx) => {
          const curX = startX + idx * (cardW + gap);
          // Card background
          slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
            x: curX,
            y: cardY,
            w: cardW,
            h: cardH,
            fill: { color: theme.white },
            line: { color: 'E2E8F0', width: 1 },
            rectRadius: 0.1
          });
          // Top accent line
          slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
            x: curX,
            y: cardY,
            w: cardW,
            h: 0.08,
            fill: { color: idx % 2 === 0 ? theme.primary : theme.secondary },
            line: { color: idx % 2 === 0 ? theme.primary : theme.secondary }
          });
          // Card Title
          slide.addText(card.title, {
            x: curX + 0.2,
            y: cardY + 0.3,
            w: cardW - 0.4,
            h: 0.6,
            fontFace: theme.font,
            fontSize: 16,
            bold: true,
            color: theme.dark,
            valign: 'top'
          });
          // Card Body
          slide.addText(card.text, {
            x: curX + 0.2,
            y: cardY + 0.9,
            w: cardW - 0.4,
            h: cardH - 1.1,
            fontFace: theme.font,
            fontSize: 12,
            color: theme.muted,
            valign: 'top',
            lineSpacingMultiple: 1.15
          });
        });
        break;
      }

      case 'stats': {
        addHeader(slide, item.title, item.subtitle, theme);
        const stats = item.stats || [];
        const count = stats.length;
        const totalW = 8.6;
        const startX = 0.7;
        const boxY = 1.8;
        const boxH = 3.0;
        const gap = 0.3;
        const boxW = (totalW - gap * (count - 1)) / count;

        stats.forEach((stat, idx) => {
          const curX = startX + idx * (boxW + gap);
          slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
            x: curX,
            y: boxY,
            w: boxW,
            h: boxH,
            fill: { color: theme.white },
            line: { color: 'E2E8F0', width: 1 },
            rectRadius: 0.12
          });

          // Stat Value
          slide.addText(stat.value, {
            x: curX + 0.2,
            y: boxY + 0.4,
            w: boxW - 0.4,
            h: 1.0,
            fontFace: theme.font,
            fontSize: 34,
            bold: true,
            color: theme.primary,
            align: 'center',
            valign: 'middle'
          });

          // Stat Label
          slide.addText(stat.label, {
            x: curX + 0.2,
            y: boxY + 1.4,
            w: boxW - 0.4,
            h: 0.6,
            fontFace: theme.font,
            fontSize: 13,
            bold: true,
            color: theme.dark,
            align: 'center',
            valign: 'top'
          });

          // Trend / Note
          if (stat.change) {
            slide.addText(stat.change, {
              x: curX + 0.2,
              y: boxY + 2.1,
              w: boxW - 0.4,
              h: 0.5,
              fontFace: theme.font,
              fontSize: 11,
              color: theme.secondary,
              align: 'center',
              bold: true
            });
          }
        });
        break;
      }

      case 'bullets':
      default: {
        addHeader(slide, item.title, item.subtitle, theme);
        const bullets = item.bullets || item.content || [];
        const formattedBullets = bullets.map(b => {
          if (typeof b === 'string') {
            return { text: b, options: { bullet: true, fontSize: 15, color: theme.dark, breakLine: true, fontFace: theme.font } };
          }
          return { text: b.text, options: { bullet: true, fontSize: b.fontSize || 15, color: b.color || theme.dark, breakLine: true, fontFace: theme.font } };
        });

        // Content box
        slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
          x: 0.7,
          y: 1.6,
          w: 8.6,
          h: 3.4,
          fill: { color: theme.white },
          line: { color: 'E2E8F0', width: 1 },
          rectRadius: 0.1
        });

        slide.addText(formattedBullets, {
          x: 1.0,
          y: 1.8,
          w: 8.0,
          h: 3.0,
          valign: 'top',
          paraSpaceAfter: 10
        });
        break;
      }
    }
  }

  function addHeader(slide, title, subtitle, theme) {
    if (title) {
      slide.addText(title, {
        x: 0.7,
        y: 0.4,
        w: 8.6,
        h: 0.6,
        fontFace: theme.font,
        fontSize: 24,
        bold: true,
        color: theme.dark,
        valign: 'bottom'
      });
    }
    if (subtitle) {
      slide.addText(subtitle, {
        x: 0.7,
        y: 1.0,
        w: 8.6,
        h: 0.4,
        fontFace: theme.font,
        fontSize: 13,
        color: theme.muted,
        valign: 'top'
      });
    }
  }

  const outPath = path.resolve(process.cwd(), outputFile);
  await pptx.writeFile({ fileName: outPath });
  console.log(`Generated PowerPoint presentation: ${outPath}`);
}

main().catch(err => {
  console.error('Generation failed:', err);
  process.exit(1);
});
