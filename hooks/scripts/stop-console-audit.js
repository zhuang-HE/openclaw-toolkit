#!/usr/bin/env node
/**
 * Stop Hook: Console Audit
 * Checks all modified files for console.log after each response
 */

const { execSync } = require('child_process');
const fs = require('fs');

async function main() {
  let data = '';
  
  for await (const chunk of process.stdin) {
    data += chunk;
  }

  try {
    const input = JSON.parse(data);
    
    // Find recently modified files (last 5 minutes)
    const recentlyModified = findRecentlyModifiedFiles();
    
    const filesWithConsoleLog = [];
    
    for (const file of recentlyModified) {
      if (/\.(js|ts|jsx|tsx)$/.test(file)) {
        try {
          const content = fs.readFileSync(file, 'utf8');
          if (/console\.(log|debug|warn|error|info)\(/.test(content)) {
            filesWithConsoleLog.push(file);
          }
        } catch (e) {
          // File might not be readable
        }
      }
    }

    if (filesWithConsoleLog.length > 0) {
      console.error('[Hook] 📋 Session Console.log Audit:');
      console.error(`[Hook] Found console statements in ${filesWithConsoleLog.length} file(s):`);
      filesWithConsoleLog.slice(0, 5).forEach(file => {
        console.error(`[Hook]   - ${file}`);
      });
      if (filesWithConsoleLog.length > 5) {
        console.error(`[Hook]   ... and ${filesWithConsoleLog.length - 5} more`);
      }
    }

    console.log(data);

  } catch (e) {
    console.error(`[Hook] Error: ${e.message}`);
    console.log(data);
  }
}

function findRecentlyModifiedFiles() {
  try {
    // Find files modified in last 5 minutes
    const result = execSync('find . -type f -mmin -5 -not -path "./node_modules/*" -not -path "./.git/*" -not -path "./dist/*" -not -path "./build/*" 2>/dev/null', { 
      encoding: 'utf8',
      maxBuffer: 10 * 1024 * 1024
    });
    return result.split('\n').filter(f => f.trim());
  } catch (e) {
    return [];
  }
}

main().catch(console.error);
