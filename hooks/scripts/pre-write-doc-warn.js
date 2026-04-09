#!/usr/bin/env node
/**
 * Pre-Write: Doc File Warning
 * Warns about non-standard .md/.txt files
 */

const ALLOWED_FILES = [
  'README.md',
  'CLAUDE.md',
  'CONTRIBUTING.md',
  'CHANGELOG.md',
  'LICENSE',
  'LICENSE.md',
  'SKILL.md',
  'AGENTS.md',
  'SOUL.md',
  'MEMORY.md',
  'USER.md',
  'TOOLS.md'
];

const ALLOWED_DIRS = [
  'docs/',
  'documentation/',
  'skills/',
  '.learnings/'
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

    if (filePath && /\.(md|txt)$/.test(filePath)) {
      const fileName = filePath.split('/').pop();
      const dirName = filePath.split('/').slice(0, -1).join('/') + '/';
      
      const isAllowedFile = ALLOWED_FILES.includes(fileName);
      const isInAllowedDir = ALLOWED_DIRS.some(dir => filePath.includes(dir));
      
      if (!isAllowedFile && !isInAllowedDir) {
        console.error('[Hook] ⚠️  Creating non-standard documentation file:');
        console.error(`[Hook]   ${filePath}`);
        console.error('[Hook]');
        console.error('[Hook] Allowed files:');
        ALLOWED_FILES.forEach(f => console.error(`[Hook]   - ${f}`));
        console.error('[Hook]');
        console.error('[Hook] Allowed directories:');
        ALLOWED_DIRS.forEach(d => console.error(`[Hook]   - ${d}`));
        console.error('[Hook]');
        console.error('[Hook] Consider:');
        console.error('[Hook]   - Placing in docs/ directory');
        console.error('[Hook]   - Using standard filename');
        console.error('[Hook]   - Adding to existing documentation');
      }
    }

    console.log(data);

  } catch (e) {
    console.error(`[Hook] Error: ${e.message}`);
    console.log(data);
  }
}

main().catch(console.error);
