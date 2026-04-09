#!/usr/bin/env node
/**
 * Config Protection Hook
 * Protects sensitive config files from accidental overwrites
 */

const SENSITIVE_PATTERNS = [
  /\.env$/,
  /\.env\..+$/,
  /config\.json$/,
  /settings\.json$/,
  /credentials\.json$/,
  /\.aws\/credentials$/,
  /\.ssh\/.+$/,
  /secrets\./,
  /\.pem$/,
  /\.key$/
];

async function main() {
  let data = '';
  
  for await (const chunk of process.stdin) {
    data += chunk;
  }

  try {
    const input = JSON.parse(data);
    const filePath = input.tool_input?.file_path || '';
    const content = input.tool_input?.content || '';

    if (filePath) {
      const isSensitive = SENSITIVE_PATTERNS.some(pattern => 
        pattern.test(filePath)
      );

      if (isSensitive && content.length > 0) {
        console.error('[Hook] ⚠️  PROTECTED: Attempting to overwrite sensitive config file:');
        console.error(`[Hook]   ${filePath}`);
        console.error('[Hook]');
        console.error('[Hook] This file may contain sensitive configuration.');
        console.error('[Hook] Please verify:');
        console.error('[Hook]   1. You intend to modify this file');
        console.error('[Hook]   2. No secrets will be committed');
        console.error('[Hook]   3. Backup exists if needed');
        console.error('[Hook]');
        console.error('[Hook] To proceed, run the command again with explicit confirmation.');
        process.exit(2); // Block the operation
      }
    }

    console.log(data);

  } catch (e) {
    console.error(`[Hook] Error: ${e.message}`);
    console.log(data);
  }
}

main().catch(console.error);
