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

  // Validate DrawingML chart XML integrity for any generated charts
  const chartParts = files.filter(f => /^ppt\/charts\/chart\d+\.xml$/.test(f));
  for (const cp of chartParts) {
    const chartXml = await zip.file(cp).async('text');
    if (!/<c:[a-zA-Z0-9]+Chart>/.test(chartXml)) {
      throw new Error(`Chart part '${cp}' is missing a valid DrawingML chart element (<c:...Chart>) in ${filePath}`);
    }
  }

  // Check [Content_Types].xml content
  const ctContent = await zip.file('[Content_Types].xml').async('text');
  if (!ctContent.includes('presentationml') && !ctContent.includes('ContentType')) {
    throw new Error(`[Content_Types].xml appears malformed in ${filePath}`);
  }

  return {
    size: stat.size,
    slides: slideParts.length,
    charts: chartParts.length,
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

    slide1.addChart(pptx.charts.BAR, [
      { name: 'Velocity', labels: ['W1', 'W2', 'W3'], values: [12, 19, 27] }
    ], {
      x: 5.2, y: 1.2, w: 4.0, h: 3.5,
      barDir: 'col',
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

  // Test 6: CLI Tool: quick_gen.js from Root-Level Array JSON Specification
  await runTest('CLI Generator: quick_gen.js Root Array Format -> Deck', async () => {
    const arraySpec = [
      {
        type: "title",
        title: "Platform Engineering Architecture",
        subtitle: "Enterprise Microservices Roadmap"
      },
      {
        type: "cards",
        title: "Architectural Tenets",
        cards: [
          { title: "Stateless Execution", text: "Zero local persistence across worker nodes." },
          { title: "Idempotent Ops", text: "Safe automated replays without side effects." }
        ]
      }
    ];

    const arrayJsonPath = path.join(tempDir, 'array_spec.json');
    fs.writeFileSync(arrayJsonPath, JSON.stringify(arraySpec, null, 2));

    const quickGenScript = path.join(skillRoot, 'scripts', 'quick_gen.js');
    const outPath = path.join(tempDir, 'array_spec_out.pptx');

    execSync(`node "${quickGenScript}" "${arrayJsonPath}" "${outPath}"`, {
      cwd: skillRoot,
      env: { ...process.env, NODE_PATH: skillNodeModules }
    });

    const info = await validatePptxFile(outPath, 2);
    return `${(info.size / 1024).toFixed(1)} KB, ${info.slides} slides`;
  });

  // Test 7: CLI Flags & Error Boundary Handling
  await runTest('CLI Flag & Error Boundary Handling (--help, --version, missing/invalid specs)', async () => {
    const runScript = path.join(skillRoot, 'scripts', 'run.js');
    const quickGenScript = path.join(skillRoot, 'scripts', 'quick_gen.js');

    // 1. run.js --help & -v
    execSync(`node "${runScript}" --help`);
    execSync(`node "${runScript}" -v`);
    execSync(`node "${runScript}" --version`);

    // 2. quick_gen.js --help & -v
    execSync(`node "${quickGenScript}" --help`);
    execSync(`node "${quickGenScript}" -v`);
    execSync(`node "${quickGenScript}" --version`);

    // 3. run.js with missing file should exit 1
    let runFailed = false;
    try {
      execSync(`node "${runScript}" non_existent_script_123.js`, { stdio: 'pipe' });
    } catch {
      runFailed = true;
    }
    if (!runFailed) throw new Error('Expected run.js to exit non-zero for missing script');

    // 4. quick_gen.js with missing file should exit 1
    let quickGenMissingFailed = false;
    try {
      execSync(`node "${quickGenScript}" non_existent_spec_123.json`, { stdio: 'pipe' });
    } catch {
      quickGenMissingFailed = true;
    }
    if (!quickGenMissingFailed) throw new Error('Expected quick_gen.js to exit non-zero for missing spec');

    // 5. quick_gen.js with malformed JSON should exit 1
    const malformedJson = path.join(tempDir, 'malformed.json');
    fs.writeFileSync(malformedJson, '{ not valid json: true, ');
    let quickGenMalformedFailed = false;
    try {
      execSync(`node "${quickGenScript}" "${malformedJson}" "${path.join(tempDir, 'malformed.pptx')}"`, { stdio: 'pipe' });
    } catch {
      quickGenMalformedFailed = true;
    }
    if (!quickGenMalformedFailed) throw new Error('Expected quick_gen.js to exit non-zero for malformed JSON');

    // 6. quick_gen.js with empty slides array should exit 1
    const emptySlidesJson = path.join(tempDir, 'empty_slides.json');
    fs.writeFileSync(emptySlidesJson, JSON.stringify({ slides: [] }));
    let quickGenEmptyFailed = false;
    try {
      execSync(`node "${quickGenScript}" "${emptySlidesJson}" "${path.join(tempDir, 'empty_slides.pptx')}"`, { stdio: 'pipe' });
    } catch {
      quickGenEmptyFailed = true;
    }
    if (!quickGenEmptyFailed) throw new Error('Expected quick_gen.js to exit non-zero for empty slides');

    return 'All CLI edge cases handled cleanly';
  });

  // Test 8: OPC Package Validator Negative Rejection Tests
  await runTest('OPC Package Validator Rejection Integrity (corrupt / empty / invalid chart files)', async () => {
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

    // 3. Corrupt chart XML part (missing <c:...Chart> DrawingML tag)
    const quickGenOut = path.join(tempDir, 'quick_gen_out.pptx');
    if (fs.existsSync(quickGenOut)) {
      const validZip = await JSZip.loadAsync(fs.readFileSync(quickGenOut));
      validZip.file('ppt/charts/chart1.xml', '<?xml version="1.0"?><c:chartSpace><c:plotArea><c:catAx/></c:plotArea></c:chartSpace>');
      const corruptChartBuf = await validZip.generateAsync({ type: 'nodebuffer' });
      const corruptChartFile = path.join(tempDir, 'corrupt_chart.pptx');
      fs.writeFileSync(corruptChartFile, corruptChartBuf);

      let chartCaught = false;
      try {
        await validatePptxFile(corruptChartFile);
      } catch (e) {
        chartCaught = e.message.includes('missing a valid DrawingML chart element');
      }
      if (!chartCaught) throw new Error('Validator failed to reject chart part with missing DrawingML chart tag');
    }

    return 'Rejected 0-byte, invalid archives, and malformed DrawingML charts';
  });

  // Test 9: Universal Runner: scripts/run.js
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

  // Test 10: Cross-Validation with pptx-engineer structural validator (if python3 available)
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

  // Test 11: Table Edge Cases (rows-only, headers-only, null-cell sanitation, empty tables)
  await runTest('Table Edge Cases (rows-only, headers-only, null-cell sanitation)', async () => {
    const quickGenScript = path.join(skillRoot, 'scripts', 'quick_gen.js');

    // 1. Rows-only table (headerless)
    const rowsOnlySpec = {
      slides: [
        {
          type: "table",
          title: "Headerless Table",
          rows: [
            ["Metric A", "100ms"],
            ["Metric B", "200ms"]
          ]
        }
      ]
    };
    const rowsOnlyJson = path.join(tempDir, 'rows_only.json');
    const rowsOnlyPptx = path.join(tempDir, 'rows_only.pptx');
    fs.writeFileSync(rowsOnlyJson, JSON.stringify(rowsOnlySpec));
    execSync(`node "${quickGenScript}" "${rowsOnlyJson}" "${rowsOnlyPptx}"`, {
      env: { ...process.env, NODE_PATH: skillNodeModules }
    });
    const infoRows = await validatePptxFile(rowsOnlyPptx, 1);
    const zipRows = await JSZip.loadAsync(fs.readFileSync(rowsOnlyPptx));
    const slide1RowsXml = await zipRows.file('ppt/slides/slide1.xml').async('text');
    if (!slide1RowsXml.includes('a:tbl')) {
      throw new Error('Headerless table was not generated into slide XML');
    }

    // 2. Headers-only table
    const headersOnlySpec = {
      slides: [
        {
          type: "table",
          title: "Headers Only",
          headers: ["Col 1", "Col 2"]
        }
      ]
    };
    const headersOnlyJson = path.join(tempDir, 'headers_only.json');
    const headersOnlyPptx = path.join(tempDir, 'headers_only.pptx');
    fs.writeFileSync(headersOnlyJson, JSON.stringify(headersOnlySpec));
    execSync(`node "${quickGenScript}" "${headersOnlyJson}" "${headersOnlyPptx}"`, {
      env: { ...process.env, NODE_PATH: skillNodeModules }
    });
    await validatePptxFile(headersOnlyPptx, 1);
    const zipHeaders = await JSZip.loadAsync(fs.readFileSync(headersOnlyPptx));
    const slide1HeadersXml = await zipHeaders.file('ppt/slides/slide1.xml').async('text');
    if (!slide1HeadersXml.includes('a:tbl')) {
      throw new Error('Headers-only table was not generated into slide XML');
    }

    // 3. Null cell sanitation (must not output literal <a:t>null</a:t>)
    const nullCellSpec = {
      slides: [
        {
          type: "table",
          title: "Sanitized Table",
          headers: ["Key", "Value"],
          rows: [
            ["Latency", null],
            [null, "15ms"]
          ]
        }
      ]
    };
    const nullCellJson = path.join(tempDir, 'null_cell.json');
    const nullCellPptx = path.join(tempDir, 'null_cell.pptx');
    fs.writeFileSync(nullCellJson, JSON.stringify(nullCellSpec));
    execSync(`node "${quickGenScript}" "${nullCellJson}" "${nullCellPptx}"`, {
      env: { ...process.env, NODE_PATH: skillNodeModules }
    });
    const zipNullCell = await JSZip.loadAsync(fs.readFileSync(nullCellPptx));
    const slide1NullXml = await zipNullCell.file('ppt/slides/slide1.xml').async('text');
    if (slide1NullXml.includes('<a:t>null</a:t>')) {
      throw new Error('Found unsanitized literal <a:t>null</a:t> in generated table cell');
    }

    // 4. Empty table dimensions (headers: [], rows: []) - must not crash
    const emptyTableSpec = {
      slides: [
        {
          type: "table",
          title: "Empty Table Slide",
          headers: [],
          rows: []
        }
      ]
    };
    const emptyTableJson = path.join(tempDir, 'empty_table.json');
    const emptyTablePptx = path.join(tempDir, 'empty_table.pptx');
    fs.writeFileSync(emptyTableJson, JSON.stringify(emptyTableSpec));
    execSync(`node "${quickGenScript}" "${emptyTableJson}" "${emptyTablePptx}"`, {
      env: { ...process.env, NODE_PATH: skillNodeModules }
    });
    await validatePptxFile(emptyTablePptx, 1);

    return `Verified rows-only, headers-only, null-cell sanitation, empty tables`;
  });

  // Test 12: Resilient Element & Boundary Handling (null/primitive items, large counts)
  await runTest('Resilient Boundary Handling (null cards/stats/bullets, high counts)', async () => {
    const quickGenScript = path.join(skillRoot, 'scripts', 'quick_gen.js');

    const edgeSpec = {
      title: "Resilience Spec",
      slides: [
        null, // should be skipped safely
        {
          type: "cards",
          title: "Mixed Cards",
          cards: [
            null,
            { title: "Active Card", text: "Healthy text" },
            "Plain string card",
            undefined
          ]
        },
        {
          type: "stats",
          title: "Mixed Stats",
          stats: [
            null,
            { value: "42k", label: "QPS", change: 0 },
            { value: "99.9%", label: "SLA", change: "Optimal" },
            undefined
          ]
        },
        {
          type: "bullets",
          title: "Mixed Bullets",
          bullets: [
            null,
            "First takeaway",
            12345,
            { text: "Object takeaway", fontSize: 14 },
            undefined
          ]
        },
        {
          type: "cards",
          title: "High Card Density",
          cards: Array.from({ length: 12 }, (_, i) => ({ title: `Tier ${i + 1}`, text: `Description ${i + 1}` }))
        }
      ]
    };

    const edgeJson = path.join(tempDir, 'edge_spec.json');
    const edgePptx = path.join(tempDir, 'edge_spec.pptx');
    fs.writeFileSync(edgeJson, JSON.stringify(edgeSpec));

    execSync(`node "${quickGenScript}" "${edgeJson}" "${edgePptx}"`, {
      env: { ...process.env, NODE_PATH: skillNodeModules }
    });

    const info = await validatePptxFile(edgePptx, 4);
    return `${(info.size / 1024).toFixed(1)} KB, ${info.slides} slides verified`;
  });

  // Test 13: Large Dataset & AutoPage Stress Test (50+ slides with auto-paginating tables)
  await runTest('Large Dataset & Stress Test (50+ slides, multi-page tables, charts)', async () => {
    const quickGenScript = path.join(skillRoot, 'scripts', 'quick_gen.js');

    const stressSpec = {
      title: "Enterprise Large-Scale Stress Presentation",
      slides: []
    };

    for (let i = 1; i <= 50; i++) {
      if (i % 3 === 1) {
        stressSpec.slides.push({
          type: "cards",
          title: `Architecture Module ${i}`,
          cards: [
            { title: "Service Mesh", text: "Decentralized control plane" },
            { title: "Data Storage", text: "Immutable append-only ledger" }
          ]
        });
      } else if (i % 3 === 2) {
        stressSpec.slides.push({
          type: "stats",
          title: `Telemetry Pod ${i}`,
          stats: [
            { value: `${i * 10}ms`, label: "P99", change: "-2ms" },
            { value: `${(99.9 + (i % 5) * 0.01).toFixed(2)}%`, label: "Uptime", change: "Nominal" }
          ]
        });
      } else {
        const rows = [];
        for (let r = 1; r <= 25; r++) {
          rows.push([`Node ${r}`, `Shard ${i}-${r}`, `${(r * 1.5).toFixed(1)} GB`, "Synced"]);
        }
        stressSpec.slides.push({
          type: "table",
          title: `Data Partition Ledger ${i}`,
          headers: ["Node", "Shard ID", "Allocated RAM", "Sync State"],
          rows: rows
        });
      }
    }

    const stressJson = path.join(tempDir, 'stress_spec.json');
    const stressPptx = path.join(tempDir, 'stress_out.pptx');
    fs.writeFileSync(stressJson, JSON.stringify(stressSpec));

    execSync(`node "${quickGenScript}" "${stressJson}" "${stressPptx}"`, {
      env: { ...process.env, NODE_PATH: skillNodeModules }
    });

    const info = await validatePptxFile(stressPptx, 50);

    if (fs.existsSync(pptxEngineerValidate)) {
      const pyCmd = `python3 "${pptxEngineerValidate}" "${stressPptx}"`;
      const output = execSync(pyCmd, { encoding: 'utf-8' });
      if (!output.includes('PASSED')) {
        throw new Error(`Structural validator failed on stress deck: ${output}`);
      }
    }

    return `${(info.size / 1024).toFixed(1)} KB, ${info.slides} total generated slides verified`;
  });

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
