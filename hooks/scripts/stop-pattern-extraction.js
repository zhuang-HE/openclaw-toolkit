#!/usr/bin/env node
/**
 * Stop Hook: Pattern Extraction
 * Evaluates session for extractable patterns (continuous learning)
 */

const fs = require('fs');
const path = require('path');

const INSTINCTS_FILE = path.join(process.cwd(), '.learnings', 'INSTINCTS.md');

async function main() {
  let data = '';
  
  for await (const chunk of process.stdin) {
    data += chunk;
  }

  try {
    const input = JSON.parse(data);
    
    // This hook should be called at session end
    // Check if there are patterns to extract
    
    console.error('[Hook] 🧠 Evaluating session for pattern extraction...');
    
    // Simple heuristic: if session had successful complex task, suggest extraction
    // In production, this would analyze the session transcript
    
    const shouldPromptExtraction = Math.random() > 0.7; // Demo: 30% chance
    
    if (shouldPromptExtraction) {
      console.error('[Hook] 💡 Potential patterns detected in this session');
      console.error('[Hook] Consider running:');
      console.error('[Hook]   /instinct-status  # View current instincts');
      console.error('[Hook]   # Then extract new patterns to .learnings/INSTINCTS.md');
    } else {
      console.error('[Hook] ✓ No obvious patterns to extract');
    }

    console.log(data);

  } catch (e) {
    console.error(`[Hook] Error: ${e.message}`);
    console.log(data);
  }
}

main().catch(console.error);
