# /quality-gate Command

## Purpose

Run a quick quality check on recent changes before committing or merging.

## Usage

```bash
/quality-gate [options]
/quality-gate --full    # Run comprehensive checks
/quality-gate --quick   # Run only essential checks (default)
```

## What It Checks

### Quick Mode (--quick)

**1. Syntax Check**
- TypeScript: `tsc --noEmit`
- Python: `python -m py_compile`
- Go: `go build`
- Rust: `cargo check`

**2. Linting**
- Run configured linter for the project
- Check for obvious code style issues

**3. Console.log Detection**
```bash
grep -r "console.log\|console.debug\|debugger" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" src/
```

**4. TODO/FIXME Check**
```bash
grep -r "TODO\|FIXME\|XXX\|HACK" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.py" src/
```

**5. Secret Detection**
```bash
grep -rE "(API_KEY|SECRET|PASSWORD|TOKEN|PRIVATE_KEY)\s*[=:]\s*['\"][^'\"]+['\"]" --include="*.ts" --include="*.js" --include="*.py" --include="*.env" .
```

### Full Mode (--full)

Includes quick mode checks plus:

**6. Test Suite**
```bash
npm test
# or
pytest
# or
go test ./...
```

**7. Type Coverage** (TypeScript)
```bash
npx tsc --noEmit --strict
```

**8. Dependency Audit**
```bash
npm audit
# or
pip-audit
# or
cargo audit
```

**9. Code Coverage** (if tests run)
- Report coverage percentage
- Flag significant drops

**10. Build Verification**
```bash
npm run build
# or
go build
# or
cargo build
```

## Output Format

```markdown
## Quality Gate Results

### ✅ Passed
- [x] Syntax check
- [x] Linting
- [x] No console.log statements

### ⚠️ Warnings
- [ ] 3 TODO comments found
  - src/utils.ts:45
  - src/api/handler.ts:123
  - src/components/Button.tsx:67

### ❌ Failed
- [ ] Secret detection: Potential API key in src/config.ts:12

## Summary
- **Status:** FAILED (1 critical issue)
- **Warnings:** 3
- **Recommendation:** Fix critical issues before committing
```

## Exit Codes

- `0` - All checks passed
- `1` - Warnings only (can proceed with caution)
- `2` - Critical issues found (should not proceed)

## Integration

This command can be used:
- Manually before committing
- In pre-commit hooks
- In CI/CD pipelines
- As part of `/code-review` workflow

## Customization

Project-specific checks can be added in:
- `.quality-gate.json` (project config)
- `~/.openclaw/quality-gate.json` (global config)

Example config:
```json
{
  "languages": ["typescript", "python"],
  "skipChecks": ["dependency-audit"],
  "customChecks": [
    {
      "name": "Database migrations",
      "command": "ls migrations/*.sql | wc -l",
      "expect": "non-zero"
    }
  ]
}
```
