#!/usr/bin/env node
/**
 * Post-Edit: Console.log Warning
 * Warns about console.log statements in edited files
 */

async function main() {
  let data = '';
  
  for await (const chunk of process.stdin) {
    data += chunk;
  }

  try {
    const input = JSON.parse(data);
    const filePath = input.tool_input?.file_path || '';
    const newString = input.tool_input?.new_string || '';
    const content = input.tool_input?.content || '';

    // Check for console.log statements
    const textToCheck = newString || content;
    
    if (textToCheck && /\.(js|ts|jsx|tsx)$/.test(filePath)) {
      const consoleLogMatches = textToCheck.match(/console\.(log|debug|warn|error|info)\(/g);
      
      if (consoleLogMatches) {
        const count = consoleLogMatches.length;
        console.error(`[Hook] ⚠️  console.${count === 1 ? 'log' : 'statements'} detected in ${filePath}`);
        console.error(`[Hook] Found ${count} console statement(s)`);
        console.error('[Hook] Consider:');
        console.error('[Hook]   - Using a proper logging library (winston, pino)');
        console.error('[Hook]   - Removing before commit');
        console.error('[Hook]   - Using debug namespace for conditional logging');
      }
    }

    console.log(data);

  } catch (e) {
    console.error(`[Hook] Error: ${e.message}`);
    console.log(data);
  }
}

main().catch(console.error);
