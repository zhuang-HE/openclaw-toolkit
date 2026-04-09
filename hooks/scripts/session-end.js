#!/usr/bin/env node
/**
 * Session End Hook
 * Lifecycle marker and cleanup log
 */

const fs = require('fs');
const path = require('path');

const SESSION_LOG = path.join(process.cwd(), 'logs', 'sessions.log');

async function main() {
  let data = '';
  
  for await (const chunk of process.stdin) {
    data += chunk;
  }

  try {
    const input = JSON.parse(data);
    
    const timestamp = new Date().toISOString();
    
    console.error('[Hook] Session ended');
    console.error(`[Hook] Timestamp: ${timestamp}`);
    
    // Log session end
    try {
      const logDir = path.dirname(SESSION_LOG);
      if (!fs.existsSync(logDir)) {
        fs.mkdirSync(logDir, { recursive: true });
      }
      
      const logEntry = `[${timestamp}] Session ended\n`;
      fs.appendFileSync(SESSION_LOG, logEntry);
    } catch (e) {
      console.error(`[Hook] Could not write session log: ${e.message}`);
    }

    console.log(data);

  } catch (e) {
    console.error(`[Hook] Error: ${e.message}`);
    console.log(data);
  }
}

main().catch(console.error);
