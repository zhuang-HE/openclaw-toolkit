#!/usr/bin/env node
/**
 * Post-Edit: Format
 * Auto-format with Prettier after edits
 */

const { spawn } = require('child_process');
const fs = require('fs');

async function main() {
  let data = '';
  
  for await (const chunk of process.stdin) {
    data += chunk;
  }

  try {
    const input = JSON.parse(data);
    const filePath = input.tool_input?.file_path || '';

    // Check if file should be formatted
    const shouldFormat = /\.(js|jsx|ts|tsx|css|scss|json|md|yaml|yml)$/.test(filePath);

    if (shouldFormat && filePath) {
      runPrettier(filePath);
    }

    console.log(data);

  } catch (e) {
    console.error(`[Hook] Error: ${e.message}`);
    console.log(data);
  }
}

function runPrettier(filePath) {
  console.error('[Hook] Formatting with Prettier...');

  const child = spawn('npx', ['prettier', '--write', filePath], {
    stdio: ['ignore', 'pipe', 'pipe'],
    detached: true
  });

  let output = '';
  child.stderr.on('data', (data) => {
    output += data.toString();
  });

  child.on('close', (code) => {
    if (code === 0) {
      console.error('[Hook] ✓ Formatted with Prettier');
    } else {
      console.error('[Hook] ⚠️  Prettier formatting failed');
      if (output.trim()) {
        console.error(`[Hook]   ${output.trim().substring(0, 200)}`);
      }
    }
  });
}

main().catch(console.error);
