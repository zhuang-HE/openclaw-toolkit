# AgentShield Security Integration

## Purpose

Integrate AgentShield security scanning directly into your AI agent workflow for real-time vulnerability detection and security compliance.

## What is AgentShield?

AgentShield is a security scanning framework designed for AI agent harnesses. It provides:

- **1282+ security rules** covering OWASP Top 10, CWE, and AI-specific vulnerabilities
- **Real-time scanning** of code, prompts, and agent outputs
- **Context-aware analysis** that understands agent workflows
- **Actionable findings** with fix suggestions

## Installation

### Option 1: npm (Recommended)

```bash
npm install -g ecc-agentshield
# or
pnpm add -g ecc-agentshield
```

### Option 2: From Source

```bash
git clone https://github.com/affaan-m/everything-claude-code.git
cd everything-claude-code
npm install
```

### Verify Installation

```bash
agentshield --version
agentshield rules list
```

## Usage

### /security-scan Command

Run security scan on current project:

```bash
/security-scan
/security-scan --path ./src
/security-scan --full    # Comprehensive scan
/security-scan --quick   # Quick scan (default)
```

### Direct CLI Usage

```bash
# Scan specific directory
agentshield scan ./src

# Scan with specific rules
agentshield scan --rules owasp-top-10

# Generate report
agentshield scan --format json --output report.json

# Check specific file
agentshield check file.ts
```

## Scan Categories

### Code Security
- SQL Injection
- XSS (Cross-Site Scripting)
- CSRF (Cross-Site Request Forgery)
- Path Traversal
- Command Injection
- Insecure Deserialization

### Authentication & Authorization
- Hardcoded Credentials
- Weak Password Policies
- Missing Authentication
- Broken Access Control
- Session Management Issues

### Data Protection
- Sensitive Data Exposure
- Missing Encryption
- Insecure Storage
- Privacy Violations

### AI-Specific
- Prompt Injection
- Training Data Poisoning
- Model Inversion
- Membership Inference
- Jailbreak Vulnerabilities

### Infrastructure
- Insecure Dependencies (CVEs)
- Misconfigured Services
- Exposed Secrets
- Weak TLS/SSL

## Output Format

```markdown
## Security Scan Results

### Summary
- **Total Issues:** 12
- **Critical:** 2 🔴
- **High:** 3 🟠
- **Medium:** 5 🟡
- **Low:** 2 🟢

### Critical Issues

#### [AGS-001] SQL Injection Risk
**Location:** src/api/users.ts:45
**Rule:** sql-injection-001
**Severity:** Critical

**Issue:**
User input directly concatenated into SQL query

**Code:**
```typescript
// BAD
const query = `SELECT * FROM users WHERE id = ${userId}`;
```

**Fix:**
```typescript
// GOOD
const query = 'SELECT * FROM users WHERE id = ?';
await db.execute(query, [userId]);
```

**References:**
- OWASP: https://owasp.org/www-community/attacks/SQL_Injection
- CWE-89: https://cwe.mitre.org/data/definitions/89.html

### High Issues
...
```

## Integration with Hooks

### Pre-Commit Security Scan

Add to `hooks.json`:

```json
{
  "PreToolUse": {
    "Bash": [
      {
        "id": "pre:bash:security-scan",
        "type": "command",
        "command": "agentshield scan --staged --block-on-critical",
        "description": "Security scan before commit",
        "timeout": 60,
        "async": false,
        "exitCode": 2
      }
    ]
  }
}
```

### Post-Edit Security Check

```json
{
  "PostToolUse": {
    "Edit": [
      {
        "id": "post:edit:security-check",
        "type": "command",
        "command": "agentshield check ${file_path} --async",
        "description": "Background security check after edits",
        "timeout": 30,
        "async": true
      }
    ]
  }
}
```

## Custom Rules

### Creating Custom Rules

Create `.agentshield/rules/custom.json`:

```json
{
  "rules": [
    {
      "id": "custom-001",
      "name": "No Console.log in Production",
      "severity": "medium",
      "pattern": "console\\.(log|debug|warn|error|info)\\(",
      "languages": ["typescript", "javascript"],
      "message": "Remove console statements before production",
      "fix": "Use proper logging library (winston, pino)"
    },
    {
      "id": "custom-002",
      "name": "API Key Pattern",
      "severity": "critical",
      "pattern": "API_KEY\\s*=\\s*['\"][^'\"]{8,}['\"]",
      "languages": ["typescript", "javascript", "python"],
      "message": "Hardcoded API key detected",
      "fix": "Use environment variables"
    }
  ]
}
```

### Loading Custom Rules

```bash
agentshield scan --rules custom
agentshield scan --rules owasp-top-10,custom
```

## Configuration

### .agentshield.json

```json
{
  "version": "1.0.0",
  "rules": [
    "owasp-top-10",
    "cwe-top-25",
    "ai-security"
  ],
  "ignore": [
    "node_modules/",
    "dist/",
    "build/",
    "*.test.ts",
    "*.spec.ts"
  ],
  "severity": {
    "block": ["critical", "high"],
    "warn": ["medium"],
    "info": ["low"]
  },
  "reportFormat": "markdown",
  "outputPath": "security-report.md"
}
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Security Scan

on: [push, pull_request]

jobs:
  agentshield:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install AgentShield
        run: npm install -g ecc-agentshield
      
      - name: Run Security Scan
        run: agentshield scan --format sarif --output results.sarif
      
      - name: Upload to Security Tab
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: results.sarif
```

### GitLab CI

```yaml
security-scan:
  stage: test
  image: node:18
  script:
    - npm install -g ecc-agentshield
    - agentshield scan --format json --output report.json
  artifacts:
    reports:
      security: report.json
```

## Security Rules Reference

### OWASP Top 10 Rules

| Rule ID | Name | Severity |
|---------|------|----------|
| owasp-a01 | Broken Access Control | High |
| owasp-a02 | Cryptographic Failures | High |
| owasp-a03 | Injection | Critical |
| owasp-a04 | Insecure Design | Medium |
| owasp-a05 | Security Misconfiguration | High |
| owasp-a06 | Vulnerable Components | High |
| owasp-a07 | Auth Failures | High |
| owasp-a08 | Data Integrity | Medium |
| owasp-a09 | Logging Failures | Medium |
| owasp-a10 | SSRF | High |

### AI-Specific Rules

| Rule ID | Name | Severity |
|---------|------|----------|
| ai-001 | Prompt Injection | Critical |
| ai-002 | Training Data Poisoning | High |
| ai-003 | Model Inversion | Medium |
| ai-004 | Membership Inference | Medium |
| ai-005 | Jailbreak Detection | Critical |
| ai-006 | Output Filtering | Medium |
| ai-007 | Context Leakage | High |

## Best Practices

### Before Commits
1. Run `agentshield scan --staged`
2. Fix all critical/high issues
3. Document medium issues if not fixed
4. Review low issues for patterns

### During Development
1. Enable post-edit security checks
2. Use IDE integration if available
3. Keep rules updated
4. Add custom rules for project-specific concerns

### Before Releases
1. Full security scan
2. Review all findings
3. Update security documentation
4. Verify dependency CVEs

## Troubleshooting

### Common Issues

**"agentshield command not found"**
```bash
npm install -g ecc-agentshield
# Ensure npm global bin is in PATH
```

**"No rules found"**
```bash
agentshield rules update
agentshield rules list
```

**"Scan timeout"**
```bash
# Increase timeout
agentshield scan --timeout 120

# Or scan specific directories
agentshield scan ./src --exclude node_modules
```

### Performance Tips

1. **Exclude node_modules** - Always exclude dependencies
2. **Incremental scans** - Use `--staged` for commits
3. **Parallel scanning** - Split large codebases
4. **Cache results** - Use `--cache` flag

## Integration with Other Skills

### continuous-learning
- Log security patterns as instincts
- Track common vulnerability types
- Extract secure coding patterns

### quality-gate
- Include security checks in quality gate
- Block on critical security issues

### documentation-lookup
- Reference OWASP documentation
- Link to CWE entries
- Provide fix examples

## Resources

- **AgentShield Docs:** https://github.com/affaan-m/everything-claude-code
- **OWASP Top 10:** https://owasp.org/www-project-top-ten/
- **CWE Top 25:** https://cwe.mitre.org/top25/
- **AI Security:** https://mlsec.org/

## Commands Summary

| Command | Description |
|---------|-------------|
| `/security-scan` | Run security scan on project |
| `agentshield scan` | CLI scan command |
| `agentshield check <file>` | Check specific file |
| `agentshield rules list` | List available rules |
| `agentshield rules update` | Update rules database |
| `agentshield report` | Generate security report |
