#!/usr/bin/env node
/**
 * Post-Edit: TypeScript Check
 * Runs tsc --noEmit after editing TypeScript files
 */

const { execSync, spawn } = require('child_process');
const fs = require('fs');

async function main() {
  let data = '';
  
  for await (const chunk of process.stdin) {
    data += chunk;
  }

  try {
    const input = JSON.parse(data);
    const filePath = input.tool_input?.file_path || '';

    // Check if file is TypeScript
    if (filePath && /\.(ts|tsx)$/.test(filePath)) {
      // Run typecheck in background (async)
      runTypeCheck(filePath);
    }

    console.log(data);

  } catch (e) {
    console.error(`[Hook] Error: ${e.message}`);
    console.log(data);
  }
}

function runTypeCheck(filePath) {
  // Check if tsc is available
  try {
    execSync('which tsc', { stdio: 'ignore' });
  } catch (e) {
    // tsc not available, try npx
    console.error('[Hook] Running typecheck with npx tsc...');
  }

  console.error('[Hook] Running TypeScript check in background...');

  const child = spawn('npx', ['tsc', '--noEmit', filePath], {
    stdio: ['ignore', 'pipe', 'pipe'],
    detached: true
  });

  let output = '';
  child.stderr.on('data', (data) => {
    output += data.toString();
  });

  child.on('close', (code) => {
    if (code === 0) {
      console.error('[Hook] ✓ TypeScript check passed');
    } else {
      console.error('[Hook] ⚠️  TypeScript errors found:');
      output.split('\n').slice(0, 10).forEach(line => {
        if (line.trim()) {
          console.error(`[Hook]   ${line}`);
        }
      });
    }
  });
}

main().catch(console.error);
