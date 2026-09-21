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

  // Test 4: CLI Tool: quick_gen.js from JSON input (5 slides: title, cards, stats, table, chart)
  await runTest('CLI Generator: quick_gen.js (All 5 Slide Types -> Deck)', async () => {
    const jsonSpec = {
      title: "Automated Comprehensive Test Deck",
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
        },
        {
          type: "table",
          title: "Service Reliability Ledger",
          subtitle: "Production availability by microservice",
          headers: ["Service", "Uptime", "P99 Latency", "Error Rate"],
          rows: [
            ["Auth Gateway", "99.99%", "18ms", "0.001%"],
            ["Data Engine", "99.95%", "42ms", "0.004%"],
            ["Storage Mesh", "100.0%", "12ms", "0.000%"]
          ]
        },
        {
          type: "chart",
          title: "Throughput Progression",
          subtitle: "RPS volume over recent build cycles",
          chartType: "col",
          chartTitle: "Build Throughput (K RPS)",
          data: [
            { name: "Production", labels: ["Build 1", "Build 2", "Build 3", "Build 4"], values: [14.2, 18.5, 24.0, 31.8] }
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

    const info = await validatePptxFile(outPath, 5);
    return `${(info.size / 1024).toFixed(1)} KB, ${info.slides} slides`;
  });

  // Test 5: CLI Tool: quick_gen.js via Stdin Pipe
  await runTest('CLI Generator: quick_gen.js via Stdin Pipe (-)', async () => {
    const jsonPath = path.join(tempDir, 'sample_spec.json');
    const quickGenScript = path.join(skillRoot, 'scripts', 'quick_gen.js');
    const outPath = path.join(tempDir, 'stdin_gen_out.pptx');

    execSync(`cat "${jsonPath}" | node "${quickGenScript}" - "${outPath}"`, {
      cwd: skillRoot,
      env: { ...process.env, NODE_PATH: skillNodeModules }
    });

    const info = await validatePptxFile(outPath, 5);
    return `${(info.size / 1024).toFixed(1)} KB, ${info.slides} slides`;
  });

  // Test 6: CLI Help Flags & Error Path Validation
  await runTest('CLI Flag & Error Boundary Handling (--help, missing files)', async () => {
    const runScript = path.join(skillRoot, 'scripts', 'run.js');
    const quickGenScript = path.join(skillRoot, 'scripts', 'quick_gen.js');

    // 1. run.js --help should exit 0
    execSync(`node "${runScript}" --help`);

    // 2. quick_gen.js --help should exit 0
    execSync(`node "${quickGenScript}" --help`);

    // 3. run.js with missing file should exit 1
    let runFailed = false;
    try {
      execSync(`node "${runScript}" non_existent_script_123.js`, { stdio: 'pipe' });
    } catch {
      runFailed = true;
    }
    if (!runFailed) throw new Error('Expected run.js to exit non-zero for missing script');

    // 4. quick_gen.js with missing file should exit 1
    let quickGenFailed = false;
    try {
      execSync(`node "${quickGenScript}" non_existent_spec_123.json`, { stdio: 'pipe' });
    } catch {
      quickGenFailed = true;
    }
    if (!quickGenFailed) throw new Error('Expected quick_gen.js to exit non-zero for missing spec');

    return 'All CLI edge cases handled cleanly';
  });

  // Test 7: OPC Package Validator Negative Rejection Tests
  await runTest('OPC Package Validator Rejection Integrity (corrupt / empty files)', async () => {
    // 1. Empty file (0 bytes)
    const emptyFile = path.join(tempDir, 'empty.pptx');
    fs.writeFileSync(emptyFile, Buffer.alloc(0));
    let emptyCaught = false;
    try {
      await validatePptxFile(emptyFile);
    } catch (e) {
      emptyCaught = e.message.includes('0 bytes');
    }
    if (!emptyCaught) throw new Error('Validator failed to reject 0-byte file');

    // 2. Corrupted header bytes
    const corruptFile = path.join(tempDir, 'corrupt.pptx');
    fs.writeFileSync(corruptFile, Buffer.from('NOT A ZIP ARCHIVE AT ALL'));
    let corruptCaught = false;
    try {
      await validatePptxFile(corruptFile);
    } catch (e) {
      corruptCaught = e.message.includes('ZIP magic bytes');
    }
    if (!corruptCaught) throw new Error('Validator failed to reject corrupted magic bytes');

    return 'Rejected 0-byte and invalid archives as expected';
  });

  // Test 8: Universal Runner: scripts/run.js
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

  // Test 9: Cross-Validation with pptx-engineer structural validator (if python3 available)
  const pptxEngineerValidate = path.resolve(skillRoot, '..', 'pptx-engineer', 'scripts', 'validate.py');
  if (fs.existsSync(pptxEngineerValidate)) {
    await runTest('Cross-Tool Structural Validation (pptx-engineer validate.py)', async () => {
      // Validate both dashboard and comprehensive quick_gen deck
      const dashboardPath = path.join(tempDir, 'dashboard_out.pptx');
      const quickGenPath = path.join(tempDir, 'quick_gen_out.pptx');

      const pyCmd1 = `python3 "${pptxEngineerValidate}" "${dashboardPath}"`;
      const output1 = execSync(pyCmd1, { encoding: 'utf-8' });
      if (!output1.includes('PASSED')) {
        throw new Error(`Structural validator failed for dashboard: ${output1}`);
      }

      const pyCmd2 = `python3 "${pptxEngineerValidate}" "${quickGenPath}"`;
      const output2 = execSync(pyCmd2, { encoding: 'utf-8' });
      if (!output2.includes('PASSED')) {
        throw new Error(`Structural validator failed for quick_gen deck: ${output2}`);
      }

      return 'OOXML schema & rels validated across decks';
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
