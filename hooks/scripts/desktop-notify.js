#!/usr/bin/env node
/**
 * Desktop Notification Hook
 * Sends macOS desktop notification with task summary
 */

const { execSync } = require('child_process');

async function main() {
  let data = '';
  
  for await (const chunk of process.stdin) {
    data += chunk;
  }

  try {
    const input = JSON.parse(data);
    
    // Only send notification for significant tasks
    const shouldNotify = Math.random() > 0.5; // Demo: 50% chance
    
    if (shouldNotify) {
      const title = 'Task Complete';
      const message = 'Your request has been processed';
      
      console.error('[Hook] Sending desktop notification...');
      
      try {
        // macOS
        execSync(`osascript -e 'display notification "${message}" with title "${title}"'`, {
          stdio: 'ignore',
          timeout: 5000
        });
        console.error('[Hook] ✓ Notification sent');
      } catch (e) {
        // Not macOS or notify-send not available
        console.error('[Hook] Desktop notifications not available');
      }
    }

    console.log(data);

  } catch (e) {
    console.error(`[Hook] Error: ${e.message}`);
    console.log(data);
  }
}

main().catch(console.error);
