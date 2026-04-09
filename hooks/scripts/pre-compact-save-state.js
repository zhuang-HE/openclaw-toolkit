#!/usr/bin/env node
/**
 * Pre-Compact Hook: Save State
 * Saves state before context compaction
 */

const fs = require('fs');
const path = require('path');

const STATE_FILE = path.join(process.cwd(), '.learnings', 'pre-compact-state.json');

async function main() {
  let data = '';
  
  for await (const chunk of process.stdin) {
    data += chunk;
  }

  try {
    const input = JSON.parse(data);
    
    console.error('[Hook] Saving state before compaction...');
    
    // Save current context state
    const state = {
      timestamp: new Date().toISOString(),
      compactTriggered: true,
      contextLength: JSON.stringify(data).length
    };

    try {
      const stateDir = path.dirname(STATE_FILE);
      if (!fs.existsSync(stateDir)) {
        fs.mkdirSync(stateDir, { recursive: true });
      }
      
      fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
      console.error(`[Hook] ✓ State saved to ${STATE_FILE}`);
    } catch (e) {
      console.error(`[Hook] Could not save state: ${e.message}`);
    }

    console.log(data);

  } catch (e) {
    console.error(`[Hook] Error: ${e.message}`);
    console.log(data);
  }
}

main().catch(console.error);
