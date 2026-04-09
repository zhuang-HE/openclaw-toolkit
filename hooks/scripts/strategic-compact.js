#!/usr/bin/env node
/**
 * Strategic Compact Hook
 * Suggests manual compact at logical intervals
 */

const fs = require('fs');
const path = require('path');

const TOOL_CALL_COUNT_FILE = path.join(process.cwd(), '.learnings', 'tool-call-counter.json');

async function main() {
  let data = '';
  
  for await (const chunk of process.stdin) {
    data += chunk;
  }

  try {
    const input = JSON.parse(data);
    const toolName = input.tool_name;

    // Only count Edit and Write operations
    if (toolName === 'Edit' || toolName === 'Write') {
      const count = incrementToolCallCount();
      
      // Suggest compact every ~50 tool calls
      if (count % 50 === 0) {
        console.error('[Hook] 📌 Strategic Compact Reminder');
        console.error('[Hook] You\'ve made ~50 edits in this session');
        console.error('[Hook]');
        console.error('[Hook] Consider running /compact to:');
        console.error('[Hook]   - Clear context for better performance');
        console.error('[Hook]   - Save important state to files');
        console.error('[Hook]   - Start fresh with key information');
        console.error('[Hook]');
        console.error('[Hook] Or continue if you\'re in a flow state.');
      }
    }

    console.log(data);

  } catch (e) {
    console.error(`[Hook] Error: ${e.message}`);
    console.log(data);
  }
}

function incrementToolCallCount() {
  let count = 0;
  
  try {
    if (fs.existsSync(TOOL_CALL_COUNT_FILE)) {
      const data = JSON.parse(fs.readFileSync(TOOL_CALL_COUNT_FILE, 'utf8'));
      count = data.count || 0;
    }
    
    count++;
    
    const dir = path.dirname(TOOL_CALL_COUNT_FILE);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    
    fs.writeFileSync(TOOL_CALL_COUNT_FILE, JSON.stringify({ count, timestamp: new Date().toISOString() }));
    
    return count;
  } catch (e) {
    return 1;
  }
}

main().catch(console.error);
