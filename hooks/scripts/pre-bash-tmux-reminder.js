#!/usr/bin/env node
/**
 * Pre-Bash: Tmux Reminder
 * Suggests tmux for long-running commands
 */

const LONG_RUNNING_COMMANDS = [
  'npm run dev',
  'npm run watch',
  'npm test',
  'yarn dev',
  'yarn watch',
  'pnpm dev',
  'pnpm watch',
  'cargo watch',
  'cargo build',
  'go run',
  'go test',
  'docker-compose up',
  'docker run',
  'python -m http.server',
  'uvicorn',
  'gunicorn',
  'rails s',
  'rake'
];

async function main() {
  let data = '';
  
  for await (const chunk of process.stdin) {
    data += chunk;
  }

  try {
    const input = JSON.parse(data);
    const command = input.tool_input?.command || '';

    // Check if command is long-running
    const isLongRunning = LONG_RUNNING_COMMANDS.some(cmd => 
      command.includes(cmd)
    );

    // Check if already in tmux
    const inTmux = process.env.TMUX !== undefined;

    if (isLongRunning && !inTmux) {
      console.error('[Hook] ⚠️  Long-running command detected!');
      console.error('[Hook] Consider running this in tmux for better log access:');
      console.error('[Hook]   tmux new -s dev');
      console.error('[Hook]   Then run your command inside tmux');
    }

    console.log(data);

  } catch (e) {
    console.error(`[Hook] Error: ${e.message}`);
    console.log(data);
  }
}

main().catch(console.error);
