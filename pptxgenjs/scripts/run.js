#!/usr/bin/env node
/**
 * Universal runner for PptxGenJS scripts.
 * Injects the skill's node_modules and current working directory into module resolution
 * so that scripts can require('pptxgenjs') anywhere without local installation.
 *
 * Usage:
 *   node ~/.gemini/config/skills/pptxgenjs/scripts/run.js <path-to-script.js> [args...]
 */

const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');

const args = process.argv.slice(2);
if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
  console.log(`Universal PptxGenJS Script Runner
Usage:
  node run.js <script.js> [args...]

Description:
  Executes a PowerPoint generation script with the skill's node_modules
  injected into NODE_PATH, enabling require('pptxgenjs') from any directory.

Options:
  --help, -h      Show this help message
  --version, -v   Show version number`);
  process.exit(args.length === 0 ? 1 : 0);
}

if (args[0] === '--version' || args[0] === '-v') {
  const pkg = require('../package.json');
  console.log(`agy-skill-pptxgenjs v${pkg.version}`);
  process.exit(0);
}

const targetScript = path.resolve(process.cwd(), args[0]);
if (!fs.existsSync(targetScript)) {
  console.error(`Error: Script not found: ${targetScript}`);
  process.exit(1);
}
const scriptArgs = args.slice(1);

const os = require('os');
const skillNodeModules = path.resolve(__dirname, '..', 'node_modules');
const globalNodeModules = path.resolve(os.homedir(), '.gemini/config/skills/pptxgenjs/node_modules');
const validNodePaths = [skillNodeModules];
if (fs.existsSync(globalNodeModules) && !validNodePaths.includes(globalNodeModules)) {
  validNodePaths.push(globalNodeModules);
}
const existingNodePath = process.env.NODE_PATH ? process.env.NODE_PATH.split(path.delimiter) : [];
const updatedNodePath = [...validNodePaths, ...existingNodePath].join(path.delimiter);

const child = spawn(process.execPath, [targetScript, ...scriptArgs], {
  stdio: 'inherit',
  env: {
    ...process.env,
    NODE_PATH: updatedNodePath
  }
});

child.on('exit', (code, signal) => {
  if (signal) {
    process.kill(process.pid, signal);
  } else {
    process.exit(code || 0);
  }
});

