#!/usr/bin/env node
/**
 * Post-Bash: PR Created
 * Logs PR URL after gh pr create
 */

const fs = require('fs');
const path = require('path');

const PR_LOG = path.join(process.cwd(), 'logs', 'pull-requests.jsonl');

async function main() {
  let data = '';
  
  for await (const chunk of process.stdin) {
    data += chunk;
  }

  try {
    const input = JSON.parse(data);
    const command = input.tool_input?.command || '';
    const output = input.tool_output?.output || '';

    if (command.includes('gh pr create') || command.includes('gh pr edit')) {
      console.error('[Hook] PR operation detected');
      
      // Extract PR URL from output
      const urlMatch = output.match(/https:\/\/github\.com\/[^\s]+/);
      
      if (urlMatch) {
        const prUrl = urlMatch[0];
        console.error(`[Hook] ✓ PR created: ${prUrl}`);
        
        // Log PR
        const logEntry = {
          timestamp: new Date().toISOString(),
          url: prUrl,
          command
        };

        try {
          const logDir = path.dirname(PR_LOG);
          if (!fs.existsSync(logDir)) {
            fs.mkdirSync(logDir, { recursive: true });
          }
          
          fs.appendFileSync(PR_LOG, JSON.stringify(logEntry) + '\n');
        } catch (e) {
          console.error(`[Hook] Could not log PR: ${e.message}`);
        }
      }
    }

    console.log(data);

  } catch (e) {
    console.error(`[Hook] Error: ${e.message}`);
    console.log(data);
  }
}

main().catch(console.error);
