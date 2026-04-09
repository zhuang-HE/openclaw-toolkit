#!/usr/bin/env node
/**
 * Session Start Hook
 * Loads previous context and detects package manager
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE_ROOT = process.env.OPENCLAW_WORKSPACE || process.cwd();
const STATE_FILE = path.join(WORKSPACE_ROOT, '.learnings', 'session-state.json');

async function main() {
  let data = '';
  
  // Read stdin for hook input
  for await (const chunk of process.stdin) {
    data += chunk;
  }

  try {
    const input = JSON.parse(data);
    
    // Load previous session state if exists
    let previousContext = null;
    if (fs.existsSync(STATE_FILE)) {
      try {
        previousContext = JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
        console.error(`[Hook] Loaded previous session state from ${STATE_FILE}`);
      } catch (e) {
        console.error(`[Hook] Failed to load previous state: ${e.message}`);
      }
    }

    // Detect package manager
    const packageManager = detectPackageManager(WORKSPACE_ROOT);
    console.error(`[Hook] Detected package manager: ${packageManager}`);

    // Output original data (required for hooks)
    console.log(data);

  } catch (e) {
    console.error(`[Hook] Error: ${e.message}`);
    console.log(data);
  }
}

function detectPackageManager(root) {
  // Check environment variable
  if (process.env.CLAUDE_PACKAGE_MANAGER) {
    return process.env.CLAUDE_PACKAGE_MANAGER;
  }

  // Check for lock files
  const lockFiles = {
    'pnpm-lock.yaml': 'pnpm',
    'yarn.lock': 'yarn',
    'package-lock.json': 'npm',
    'bun.lockb': 'bun'
  };

  for (const [lockFile, manager] of Object.entries(lockFiles)) {
    if (fs.existsSync(path.join(root, lockFile))) {
      return manager;
    }
  }

  // Default to npm
  return 'npm';
}

main().catch(console.error);
