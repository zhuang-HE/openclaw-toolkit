#!/usr/bin/env node
/**
 * Post-Bash: Command Log
 * Logs command execution for session history
 */

const fs = require('fs');
const path = require('path');

const COMMAND_LOG = path.join(process.cwd(), 'logs', 'command-history.jsonl');

async function main() {
  let data = '';
  
  for await (const chunk of process.stdin) {
    data += chunk;
  }

  try {
    const input = JSON.parse(data);
    const command = input.tool_input?.command || '';
    const output = input.tool_output?.output || '';
    const exitCode = input.tool_output?.exit_code;

    if (command) {
      const logEntry = {
        timestamp: new Date().toISOString(),
        command,
        exitCode: exitCode || 0,
        outputLength: output ? output.length : 0
      };

      try {
        const logDir = path.dirname(COMMAND_LOG);
        if (!fs.existsSync(logDir)) {
          fs.mkdirSync(logDir, { recursive: true });
        }
        
        fs.appendFileSync(COMMAND_LOG, JSON.stringify(logEntry) + '\n');
      } catch (e) {
        console.error(`[Hook] Could not log command: ${e.message}`);
      }
    }

    console.log(data);

  } catch (e) {
    console.error(`[Hook] Error: ${e.message}`);
    console.log(data);
  }
}

main().catch(console.error);
