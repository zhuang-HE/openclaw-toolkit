#!/usr/bin/env node
/**
 * Design Quality Check Hook
 * Warns when frontend edits drift toward generic template-looking UI
 */

const GENERIC_PATTERNS = [
  /className\s*=\s*["']container["']/,
  /className\s*=\s*["']wrapper["']/,
  /className\s*=\s*["']card["']/,
  /className\s*=\s*["']btn["']/,
  /className\s*=\s*["']button["']/,
  /style\s*=\s*{\{\s*display:\s*['"]flex['"]/,
  /className\s*=\s*["']flex["']/,
  /className\s*=\s*["']grid["']/,
  /Tailwind|tailwind|tw-/
];

async function main() {
  let data = '';
  
  for await (const chunk of process.stdin) {
    data += chunk;
  }

  try {
    const input = JSON.parse(data);
    const filePath = input.tool_input?.file_path || '';
    const newString = input.tool_input?.new_string || '';

    if (filePath && /\.(tsx|jsx|vue|svelte)$/.test(filePath)) {
      const matches = [];
      
      for (const pattern of GENERIC_PATTERNS) {
        if (pattern.test(newString)) {
          matches.push(pattern.source);
        }
      }

      if (matches.length >= 3) {
        console.error('[Hook] 🎨 Design Quality Notice');
        console.error('[Hook] Frontend code may be too generic/template-like');
        console.error('[Hook]');
        console.error('[Hook] Detected patterns:');
        matches.slice(0, 3).forEach(m => {
          console.error(`[Hook]   - ${m}`);
        });
        console.error('[Hook]');
        console.error('[Hook] Consider:');
        console.error('[Hook]   - Using more specific class names');
        console.error('[Hook]   - Adding unique styling elements');
        console.error('[Hook]   - Following brand guidelines');
        console.error('[Hook]   - Avoiding generic container/wrapper patterns');
      }
    }

    console.log(data);

  } catch (e) {
    console.error(`[Hook] Error: ${e.message}`);
    console.log(data);
  }
}

main().catch(console.error);
