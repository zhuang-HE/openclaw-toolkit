#!/usr/bin/env node
/**
 * Pre-Bash: Dev Server Blocker
 * Blocks dev servers outside tmux to ensure log access
 */

const DEV_SERVER_COMMANDS = [
  'npm run dev',
  'yarn dev',
  'pnpm dev',
  'npm start',
  'yarn start',
  'pnpm start',
  'next dev',
  'vite',
  'webpack serve',
  'webpack-dev-server',
  'parcel',
  'serve'
];

async function main() {
  let data = '';
  
  for await (const chunk of process.stdin) {
    data += chunk;
  }

  try {
    const input = JSON.parse(data);
    const command = input.tool_input?.command || '';

    // Check if command is a dev server
    const isDevServer = DEV_SERVER_COMMANDS.some(cmd => 
      command.includes(cmd)
    );

    // Check if already in tmux
    const inTmux = process.env.TMUX !== undefined;

    if (isDevServer && !inTmux) {
      console.error('[Hook] ❌ BLOCKED: Dev server command outside tmux!');
      console.error('[Hook] Dev servers should run in tmux for log access and persistence');
      console.error('[Hook]');
      console.error('[Hook] Solution:');
      console.error('[Hook]   1. Start tmux: tmux new -s dev');
      console.error('[Hook]   2. Run dev server inside tmux');
      console.error('[Hook]');
      console.error('[Hook] Or use background mode if available:');
      console.error('[Hook]   npm run dev &');
      process.exit(2); // Block the command
    }

    console.log(data);

  } catch (e) {
    console.error(`[Hook] Error: ${e.message}`);
    console.log(data);
  }
}

main().catch(console.error);
