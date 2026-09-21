#!/usr/bin/env node
/**
 * Automated Verification Test Suite for pptxgenjs skill.
 * Tests programmatic generation, example scripts, quick_gen CLI,
 * and validates that output PPTX files are valid, non-empty, and compliant OPC archives.
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const { execSync } = require('child_process');

// Ensure local skill node_modules is resolvable from any CWD
const skillRoot = path.resolve(__dirname, '..');
const skillNodeModules = path.resolve(skillRoot, 'node_modules');
if (!module.paths.includes(skillNodeModules)) {
  module.paths.unshift(skillNodeModules);
}

// Fallback to global antigravity skill node_modules if needed
const globalNodeModules = path.resolve(os.homedir(), '.gemini/config/skills/pptxgenjs/node_modules');
if (fs.existsSync(globalNodeModules) && !module.paths.includes(globalNodeModules)) {
  module.paths.push(globalNodeModules);
}

const pptxgen = require('pptxgenjs');
const JSZip = require('jszip');

// Setup scratch directory
const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'pptxgenjs-test-'));
console.log(`\n============================================================`);
console.log(`       PPTXGENJS AUTOMATED VERIFICATION TEST SUITE          `);
console.log(`============================================================`);
console.log(`Workspace: ${tempDir}`);
console.log(`Skill Dir: ${skillRoot}\n`);

let passedCount = 0;
let failedCount = 0;

/**
 * Validate that a file is a non-empty, valid PPTX / OPC ZIP package.
 */
async function validatePptxFile(filePath, expectedMinSlides = 1) {
  if (!fs.existsSync(filePath)) {
    throw new Error(`Output file not found: ${filePath}`);
  }

  const stat = fs.statSync(filePath);
  if (stat.size === 0) {
    throw new Error(`Output file is empty (0 bytes): ${filePath}`);
  }

  const buffer = fs.readFileSync(filePath);

  // Check OPC ZIP signature (PK\x03\x04)
  if (buffer.length < 4 || buffer[0] !== 0x50 || buffer[1] !== 0x4B || buffer[2] !== 0x03 || buffer[3] !== 0x04) {
    throw new Error(`File does not start with valid ZIP magic bytes: ${filePath}`);
  }

  // Parse with JSZip to verify structural integrity
  const zip = await JSZip.loadAsync(buffer);
  const files = Object.keys(zip.files);

  const requiredParts = [
    '[Content_Types].xml',
    '_rels/.rels',
    'ppt/presentation.xml'
  ];

  for (const part of requiredParts) {
    if (!files.includes(part)) {
      throw new Error(`Missing mandatory OPC part '${part}' in ${filePath}`);
    }
  }

  // Count slides in archive
  const slideParts = files.filter(f => /^ppt\/slides\/slide\d+\.xml$/.test(f));
  if (slideParts.length < expectedMinSlides) {
    throw new Error(`Expected at least ${expectedMinSlides} slide(s), found ${slideParts.length} in ${filePath}`);
  }

  // Check [Content_Types].xml content
  const ctContent = await zip.file('[Content_Types].xml').async('text');
  if (!ctContent.includes('presentationml') && !ctContent.includes('ContentType')) {
    throw new Error(`[Content_Types].xml appears malformed in ${filePath}`);
  }

  return {
    size: stat.size,
    slides: slideParts.length,
    parts: files.length
  };
}

async function runTest(testName, testFn) {
  const start = Date.now();
  process.stdout.write(`• ${testName} ... `);
  try {
    const result = await testFn();
    const duration = Date.now() - start;
    console.log(`✅ PASS (${duration}ms)${result ? ' - ' + result : ''}`);
    passedCount++;
  } catch (err) {
    const duration = Date.now() - start;
    console.log(`❌ FAIL (${duration}ms)`);
    console.error(`  Error: ${err.message}`);
    failedCount++;
  }
}

async function main() {
  // Test 1: Direct programmatic API deck generation
  await runTest('Programmatic Deck Generation (SlideMaster, Table, Shapes, Chart)', async () => {
    const pptx = new pptxgen();
    pptx.layout = 'LAYOUT_16x9';
    pptx.title = 'Verification Suite Direct Test';

    pptx.defineSlideMaster({
      title: 'TEST_MASTER',
      background: { color: 'F8FAFC' },
      objects: [
        { rect: { x: 0, y: 0, w: '100%', h: 0.1, fill: { color: '2563EB' } } }
      ]
    });

    const slide1 = pptx.addSlide({ masterName: 'TEST_MASTER' });
    slide1.addText('Automated Verification Slide', {
      x: 0.8, y: 0.5, w: 8.4, h: 0.5,
      fontSize: 24, bold: true, color: '0F172A'
    });

    slide1.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x: 0.8, y: 1.2, w: 4.0, h: 3.5,
      fill: { color: 'FFFFFF' },
      line: { color: 'E2E8F0', width: 1 },
      rectRadius: 0.1
    });

    slide1.addTable([
      [{ text: 'Metric', options: { bold: true } }, { text: 'Status', options: { bold: true } }],
      ['Build', 'Passed'],
      ['Integrity', 'Verified']
    ], {
      x: 1.0, y: 1.5, w: 3.6,
      border: { type: 'solid', pt: 0.5, color: 'E2E8F0' }
    });

    slide1.addChart(pptx.charts.COL, [
      { name: 'Velocity', labels: ['W1', 'W2', 'W3'], values: [12, 19, 27] }
    ], {
      x: 5.2, y: 1.2, w: 4.0, h: 3.5,
      chartColors: ['2563EB']
    });

    const outPath = path.join(tempDir, 'direct_api.pptx');
    await pptx.writeFile({ fileName: outPath });

    const info = await validatePptxFile(outPath, 1);
    return `${(info.size / 1024).toFixed(1)} KB, ${info.slides} slide(s)`;
  });

  // Test 2: Generator example: pitch_deck.js
  await runTest('Example Generator: pitch_deck.js (5-slide Venture Deck)', async () => {
    const pitchDeckScript = path.join(skillRoot, 'examples', 'pitch_deck.js');
    const outPath = path.join(tempDir, 'pitch_deck_out.pptx');
    
    execSync(`node "${pitchDeckScript}" "${outPath}"`, {
      cwd: skillRoot,
      env: { ...process.env, NODE_PATH: skillNodeModules }
    });

    const info = await validatePptxFile(outPath, 5);
    return `${(info.size / 1024).toFixed(1)} KB, ${info.slides} slides`;
  });

  // Test 3: Generator example: metrics_dashboard.js
  await runTest('Example Generator: metrics_dashboard.js (KPI & Dual Charts)', async () => {
    const dashboardScript = path.join(skillRoot, 'examples', 'metrics_dashboard.js');
    const outPath = path.join(tempDir, 'dashboard_out.pptx');

    execSync(`node "${dashboardScript}" "${outPath}"`, {
      cwd: skillRoot,
      env: { ...process.env, NODE_PATH: skillNodeModules }
    });

    const info = await validatePptxFile(outPath, 1);
    return `${(info.size / 1024).toFixed(1)} KB, ${info.slides} slide`;
  });

  // Test 4: CLI Tool: quick_gen.js from JSON input
  await runTest('CLI Generator: quick_gen.js (JSON Spec -> Deck)', async () => {
    const jsonSpec = {
      title: "Automated Test Deck",
      theme: { primary: "2563EB", secondary: "10B981", dark: "0F172A", light: "F8FAFC" },
      slides: [
        {
          type: "title",
          title: "CI/CD Deployment Summary",
          subtitle: "Automated run verification",
          author: "Build Pipeline"
        },
        {
          type: "cards",
          title: "Pipeline Milestones",
          cards: [
            { title: "Linting", text: "100% clean across all modules." },
            { title: "Unit Tests", text: "All assertions passed cleanly." },
            { title: "Packaging", text: "Production bundle generated successfully." }
          ]
        },
        {
          type: "stats",
          title: "Execution Telemetry",
          stats: [
            { value: "0ms", label: "Cold Start Overhead", change: "Optimal" },
            { value: "100%", label: "Test Coverage", change: "+0% YoY" },
            { value: "0", label: "Known Regressions", change: "Stable" }
          ]
        }
      ]
    };

    const jsonPath = path.join(tempDir, 'sample_spec.json');
    fs.writeFileSync(jsonPath, JSON.stringify(jsonSpec, null, 2));

    const quickGenScript = path.join(skillRoot, 'scripts', 'quick_gen.js');
    const outPath = path.join(tempDir, 'quick_gen_out.pptx');

    execSync(`node "${quickGenScript}" "${jsonPath}" "${outPath}"`, {
      cwd: skillRoot,
      env: { ...process.env, NODE_PATH: skillNodeModules }
    });

    const info = await validatePptxFile(outPath, 3);
    return `${(info.size / 1024).toFixed(1)} KB, ${info.slides} slides`;
  });

  // Test 5: Universal Runner: scripts/run.js
  await runTest('Universal Runner: scripts/run.js execution wrapper', async () => {
    const runnerScript = path.join(skillRoot, 'scripts', 'run.js');
    const pitchDeckScript = path.join(skillRoot, 'examples', 'pitch_deck.js');
    const outPath = path.join(tempDir, 'runner_test.pptx');

    execSync(`node "${runnerScript}" "${pitchDeckScript}" "${outPath}"`, {
      cwd: tempDir
    });

    const info = await validatePptxFile(outPath, 5);
    return `${(info.size / 1024).toFixed(1)} KB, ${info.slides} slides`;
  });

  // Test 6: Cross-Validation with pptx-engineer structural validator (if python3 available)
  const pptxEngineerValidate = path.resolve(skillRoot, '..', 'pptx-engineer', 'scripts', 'validate.py');
  if (fs.existsSync(pptxEngineerValidate)) {
    await runTest('Cross-Tool Structural Validation (pptx-engineer validate.py)', async () => {
      const outPath = path.join(tempDir, 'dashboard_out.pptx');
      const pyCmd = `python3 "${pptxEngineerValidate}" "${outPath}"`;
      const output = execSync(pyCmd, { encoding: 'utf-8' });
      if (!output.includes('PASSED')) {
        throw new Error(`Structural validator failed: ${output}`);
      }
      return 'OOXML schema & rels validated';
    });
  }

  // Cleanup temporary directory
  try {
    fs.rmSync(tempDir, { recursive: true, force: true });
  } catch {
    // Ignore cleanup error
  }

  console.log(`\n------------------------------------------------------------`);
  console.log(`Results: ${passedCount} passed, ${failedCount} failed`);
  console.log(`------------------------------------------------------------\n`);

  if (failedCount > 0) {
    process.exit(1);
  }
  process.exit(0);
}

main().catch(err => {
  console.error('Fatal test suite error:', err);
  process.exit(1);
});
