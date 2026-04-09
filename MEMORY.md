# MEMORY.md - Long-Term Memory

## Preferences

- **联网搜索优先使用 searxng skill** —— 只要涉及联网搜索任务，优先调用 searxng 技能而非直接使用 web_search 工具。

## Notes

- Created: 2026-03-05

## Migration: everything-claude-code (2026-04-09)

Migrated key optimizations from [everything-claude-code](https://github.com/mit-network/everything-claude-code) (50K+ stars, Anthropic hackathon winner).

### New Agents
- `security-reviewer.md` - Security vulnerability analysis
- `build-error-resolver.md` - Multi-language build error diagnosis
- `planner.md` - Strategic implementation planning
- `architect.md` - System design and architecture decisions

### New Skills
- `documentation-lookup/SKILL.md` - Efficient API/doc reference lookup
- `deep-research/SKILL.md` - Multi-source research with cross-verification
- `continuous-learning/SKILL.md` - Instinct-based pattern extraction with confidence scoring

### New Commands
- `quality-gate.md` - Pre-commit quality checks (syntax, lint, secrets, TODOs)
- `harness-audit.md` - AI harness configuration audit and optimization

### Key Concepts Adopted
- **Hooks system** - Event-driven automations (PreToolUse, PostToolUse, Lifecycle)
- **Instinct-based learning** - Patterns with confidence scores that evolve
- **Selective install architecture** - Install only needed components
- **Multi-language rules** - Organized by language ecosystem

### Future Enhancements (Not Yet Implemented)
- Full hooks system with hooks.json configuration
- Automated pattern extraction at session end
- Cross-harness parity (Cursor, OpenCode, Codex)
- AgentShield integration for security scanning
