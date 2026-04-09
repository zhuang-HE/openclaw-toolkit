#!/usr/bin/env node
/**
 * Quality Gate Hook
 * Fast quality checks after edits
 */

const { execSync } = require('child_process');
const fs = require('fs');

async function main() {
  let data = '';
  
  for await (const chunk of process.stdin) {
    data += chunk;
  }

  try {
    const input = JSON.parse(data);
    const issues = [];

    console.error('[Hook] Running quality gate checks...');

    // Check for TypeScript errors
    try {
      execSync('npx tsc --noEmit', { stdio: 'ignore' });
      console.error('[Hook] ✓ TypeScript check passed');
    } catch (e) {
      issues.push('TypeScript errors detected');
      console.error('[Hook] ⚠️  TypeScript check failed');
    }

    // Check for lint errors
    try {
      execSync('npx eslint --quiet', { stdio: 'ignore', timeout: 30000 });
      console.error('[Hook] ✓ Lint check passed');
    } catch (e) {
      issues.push('Lint errors detected');
      console.error('[Hook] ⚠️  Lint check failed');
    }

    // Check for console.log
    const consoleLogFiles = checkForConsoleLog();
    if (consoleLogFiles.length > 0) {
      issues.push(`${consoleLogFiles.length} files with console.log`);
      console.error(`[Hook] ⚠️  console.log in ${consoleLogFiles.length} file(s)`);
    } else {
      console.error('[Hook] ✓ No console.log statements');
    }

    // Summary
    if (issues.length === 0) {
      console.error('[Hook] ✓ Quality gate PASSED');
    } else {
      console.error('[Hook] ⚠️  Quality gate warnings:');
      issues.forEach(issue => {
        console.error(`[Hook]   - ${issue}`);
      });
    }

    console.log(data);

  } catch (e) {
    console.error(`[Hook] Error: ${e.message}`);
    console.log(data);
  }
}

function checkForConsoleLog() {
  try {
    const result = execSync('grep -r "console\\.log" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" src/ 2>/dev/null || true', { 
      encoding: 'utf8',
      maxBuffer: 10 * 1024 * 1024
    });
    const lines = result.split('\n').filter(l => l.trim());
    const files = [...new Set(lines.map(l => l.split(':')[0]))];
    return files;
  } catch (e) {
    return [];
  }
}

main().catch(console.error);
