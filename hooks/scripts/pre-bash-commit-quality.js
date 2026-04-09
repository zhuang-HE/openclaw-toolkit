#!/usr/bin/env node
/**
 * Pre-Bash: Commit Quality Check
 * Runs quality checks before git commit
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

async function main() {
  let data = '';
  
  for await (const chunk of process.stdin) {
    data += chunk;
  }

  try {
    const input = JSON.parse(data);
    const command = input.tool_input?.command || '';
    let blocked = false;

    // Check if command is git commit
    if (command.includes('git commit')) {
      console.error('[Hook] Running pre-commit quality checks...');

      // Check for console.log in staged files
      const consoleLogFiles = checkStagedFilesForConsoleLog();
      if (consoleLogFiles.length > 0) {
        console.error('[Hook] ⚠️  WARNING: console.log found in staged files:');
        consoleLogFiles.forEach(file => {
          console.error(`[Hook]   - ${file}`);
        });
        console.error('[Hook] Consider removing before commit');
      }

      // Check for debugger statements
      const debuggerFiles = checkStagedFilesForDebugger();
      if (debuggerFiles.length > 0) {
        console.error('[Hook] ⚠️  WARNING: debugger statements found:');
        debuggerFiles.forEach(file => {
          console.error(`[Hook]   - ${file}`);
        });
        blocked = true;
      }

      // Check for secrets (basic pattern)
      const potentialSecrets = checkForSecrets();
      if (potentialSecrets.length > 0) {
        console.error('[Hook] ❌ BLOCKED: Potential secrets detected:');
        potentialSecrets.forEach(match => {
          console.error(`[Hook]   ${match}`);
        });
        console.error('[Hook] Remove secrets before committing!');
        blocked = true;
      }

      // Check for TODO/FIXME in commit message
      const hasCommitMessage = command.includes('-m') || command.includes('--message');
      if (hasCommitMessage) {
        const messageMatch = command.match(/-m\s+["']([^"']+)["']/);
        if (messageMatch) {
          const message = messageMatch[1];
          if (/TODO|FIXME|XXX|HACK/i.test(message)) {
            console.error('[Hook] ⚠️  WARNING: Commit message contains TODO/FIXME');
            console.error('[Hook] Consider creating an issue instead');
          }
        }
      }

      if (blocked) {
        console.error('[Hook] ❌ Pre-commit checks FAILED');
        process.exit(2);
      } else {
        console.error('[Hook] ✓ Pre-commit checks passed');
      }
    }

    console.log(data);

  } catch (e) {
    console.error(`[Hook] Error: ${e.message}`);
    console.log(data);
  }
}

function checkStagedFilesForConsoleLog() {
  try {
    const stagedFiles = execSync('git diff --cached --name-only', { encoding: 'utf8' });
    const files = stagedFiles.split('\n').filter(f => f.trim());
    const found = [];

    for (const file of files) {
      if (/\.(js|ts|jsx|tsx)$/.test(file)) {
        try {
          const content = execSync(`git show :${file}`, { encoding: 'utf8' });
          if (/console\.(log|debug|warn|error|info)/.test(content)) {
            found.push(file);
          }
        } catch (e) {
          // File might be deleted
        }
      }
    }

    return found;
  } catch (e) {
    return [];
  }
}

function checkStagedFilesForDebugger() {
  try {
    const stagedFiles = execSync('git diff --cached --name-only', { encoding: 'utf8' });
    const files = stagedFiles.split('\n').filter(f => f.trim());
    const found = [];

    for (const file of files) {
      if (/\.(js|ts|jsx|tsx)$/.test(file)) {
        try {
          const content = execSync(`git show :${file}`, { encoding: 'utf8' });
          if (/debugger\s*;/.test(content)) {
            found.push(file);
          }
        } catch (e) {
          // File might be deleted
        }
      }
    }

    return found;
  } catch (e) {
    return [];
  }
}

function checkForSecrets() {
  try {
    const stagedFiles = execSync('git diff --cached --name-only', { encoding: 'utf8' });
    const files = stagedFiles.split('\n').filter(f => f.trim());
    const found = [];

    const secretPatterns = [
      /API_KEY\s*[=:]\s*['"][^'"]{8,}['"]/i,
      /SECRET\s*[=:]\s*['"][^'"]{8,}['"]/i,
      /PASSWORD\s*[=:]\s*['"][^'"]{4,}['"]/i,
      /PRIVATE_KEY\s*[=:]\s*['"][^'"]{8,}['"]/i,
      /Bearer\s+[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+/
    ];

    for (const file of files) {
      try {
        const content = execSync(`git show :${file}`, { encoding: 'utf8' });
        for (const pattern of secretPatterns) {
          const matches = content.match(pattern);
          if (matches) {
            found.push(`${file}: ${matches[0].substring(0, 50)}...`);
          }
        }
      } catch (e) {
        // File might be deleted
      }
    }

    return found;
  } catch (e) {
    return [];
  }
}

main().catch(console.error);
