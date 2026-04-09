#!/usr/bin/env node
/**
 * Pre-Bash: Git Push Reminder
 * Reminds to review changes before git push
 */

const { execSync } = require('child_process');

async function main() {
  let data = '';
  
  for await (const chunk of process.stdin) {
    data += chunk;
  }

  try {
    const input = JSON.parse(data);
    const command = input.tool_input?.command || '';

    // Check if command is git push
    if (command.includes('git push')) {
      try {
        // Get git status
        const status = execSync('git status --short', { encoding: 'utf8' });
        const hasChanges = status.trim().length > 0;

        if (hasChanges) {
          console.error('[Hook] ⚠️  Uncommitted changes detected!');
          console.error('[Hook] Review before pushing:');
          console.error('[Hook]');
          console.error('[Hook]   git status          # Review changes');
          console.error('[Hook]   git diff            # See detailed diff');
          console.error('[Hook]   git diff --cached   # See staged changes');
          console.error('[Hook]');
          console.error('[Hook] Current status:');
          status.split('\n').slice(0, 10).forEach(line => {
            if (line.trim()) {
              console.error(`[Hook]   ${line}`);
            }
          });
        } else {
          console.error('[Hook] ✓ No uncommitted changes. Safe to push.');
        }
      } catch (e) {
        console.error('[Hook] Could not check git status');
      }
    }

    console.log(data);

  } catch (e) {
    console.error(`[Hook] Error: ${e.message}`);
    console.log(data);
  }
}

main().catch(console.error);
