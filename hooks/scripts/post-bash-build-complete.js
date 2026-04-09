#!/usr/bin/env node
/**
 * Post-Bash: Build Complete
 * Background analysis after build commands
 */

const { execSync } = require('child_process');

const BUILD_COMMANDS = [
  'npm run build',
  'yarn build',
  'pnpm build',
  'cargo build',
  'go build',
  'make',
  'gradle build',
  'mvn package'
];

async function main() {
  let data = '';
  
  for await (const chunk of process.stdin) {
    data += chunk;
  }

  try {
    const input = JSON.parse(data);
    const command = input.tool_input?.command || '';
    const output = input.tool_output?.output || '';

    const isBuildCommand = BUILD_COMMANDS.some(bc => command.includes(bc));

    if (isBuildCommand) {
      console.error('[Hook] Analyzing build output...');
      
      // Check for warnings
      const warningCount = (output.match(/warning/gi) || []).length;
      const errorCount = (output.match(/error/gi) || []).length;
      
      if (errorCount > 0) {
        console.error(`[Hook] ⚠️  Build completed with ${errorCount} error(s)`);
      } else if (warningCount > 0) {
        console.error(`[Hook] ⚠️  Build completed with ${warningCount} warning(s)`);
      } else {
        console.error('[Hook] ✓ Build completed successfully');
      }

      // Check for bundle size if applicable
      if (command.includes('build') && output.includes('kB')) {
        const sizeMatch = output.match(/(\d+\.?\d*)\s*kB/gi);
        if (sizeMatch) {
          console.error(`[Hook] 📦 Bundle size: ${sizeMatch.join(', ')}`);
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
