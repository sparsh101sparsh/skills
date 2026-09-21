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
const { spawn } = require('child_process');

const args = process.argv.slice(2);
if (args.length === 0) {
  console.error('Usage: node run.js <script.js> [args...]');
  process.exit(1);
}

const targetScript = path.resolve(process.cwd(), args[0]);
const scriptArgs = args.slice(1);

const skillNodeModules = path.resolve(__dirname, '..', 'node_modules');
const existingNodePath = process.env.NODE_PATH ? process.env.NODE_PATH.split(path.delimiter) : [];
const updatedNodePath = [skillNodeModules, ...existingNodePath].join(path.delimiter);

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
