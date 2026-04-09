# /security-scan Command

## Purpose

Run AgentShield security scan on the current project or specific files.

## Usage

```bash
/security-scan                    # Quick scan of project root
/security-scan --path ./src       # Scan specific directory
/security-scan --full             # Comprehensive scan (all rules)
/security-scan --quick            # Quick scan (critical/high only)
/security-scan --file path/to.ts  # Scan specific file
/security-scan --report           # Generate full report
```

## Implementation

```bash
#!/bin/bash
# security-scan command

# Parse arguments
PATH_TO_SCAN="${1:-.}"
FULL_SCAN=false
REPORT=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --path)
      PATH_TO_SCAN="$2"
      shift 2
      ;;
    --full)
      FULL_SCAN=true
      shift
      ;;
    --quick)
      FULL_SCAN=false
      shift
      ;;
    --file)
      PATH_TO_SCAN="$2"
      shift 2
      ;;
    --report)
      REPORT=true
      shift
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Check if agentshield is installed
if ! command -v agentshield &> /dev/null; then
  echo "❌ AgentShield not installed"
  echo ""
  echo "Install with:"
  echo "  npm install -g ecc-agentshield"
  echo "  # or"
  echo "  pnpm add -g ecc-agentshield"
  exit 1
fi

# Run scan
echo "🔒 Running AgentShield security scan..."
echo "Path: $PATH_TO_SCAN"
echo ""

if [ "$FULL_SCAN" = true ]; then
  echo "Mode: Comprehensive (all rules)"
  agentshield scan "$PATH_TO_SCAN" --rules all
else
  echo "Mode: Quick (critical/high only)"
  agentshield scan "$PATH_TO_SCAN" --severity critical,high
fi

# Generate report if requested
if [ "$REPORT" = true ]; then
  echo ""
  echo "📊 Generating report..."
  agentshield scan "$PATH_TO_SCAN" --format markdown --output security-report-$(date +%Y%m%d).md
  echo "Report saved to: security-report-$(date +%Y%m%d).md"
fi
```

## Output Example

```markdown
## Security Scan Results

### Summary
- **Total Issues:** 5
- **Critical:** 1 🔴
- **High:** 2 🟠
- **Medium:** 2 🟡
- **Low:** 0 🟢

### Critical Issues

#### [AGS-003] SQL Injection Risk
**Location:** src/api/users.ts:45
**Severity:** Critical

**Issue:**
User input directly concatenated into SQL query

**Fix:**
Use parameterized queries

### High Issues
...
```

## Exit Codes

- `0` - No critical/high issues found
- `1` - Error during scan
- `2` - Critical issues found (block merge/commit)

## Integration

Use with:
- `/quality-gate` - Include security in quality checks
- `pre-bash-commit-quality` hook - Block commits with security issues
- CI/CD pipelines - Automated security scanning
