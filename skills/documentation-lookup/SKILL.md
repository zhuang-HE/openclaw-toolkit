# Documentation Lookup Skill

## Purpose

Efficiently find and reference API documentation, library documentation, and technical references during development.

## When to Use

- Need to check API parameters or return types
- Looking for library usage examples
- Verifying best practices for a technology
- Finding configuration options
- Researching error messages

## Search Strategy

### Tier 1: Official Documentation (Always First)

**Priority order:**
1. Official docs (docs.{library}.com, {language}.org)
2. GitHub repository README/Wiki
3. Official blog posts and announcements
4. Verified community resources (Stack Overflow with high votes)

### Tier 2: Secondary Resources

- Well-maintained tutorials
- Video documentation from official channels
- Community-maintained docs (with verification)

### Tier 3: Avoid (Unless Verified)

- Unofficial blogs without citations
- Outdated tutorials (check dates)
- AI-generated content without sources

## Search Commands

### Using searxng Skill

```markdown
# Search for official docs
Search: "Next.js 14 official documentation site:nextjs.org"

# Search for API reference
Search: "Stripe API charge creation site:stripe.com/docs"

# Search for specific error
Search: "React useEffect dependency array warning site:react.dev"
```

### Direct URL Access

Common documentation URLs:
- **TypeScript:** https://www.typescriptlang.org/docs/
- **React:** https://react.dev/
- **Next.js:** https://nextjs.org/docs
- **Node.js:** https://nodejs.org/docs/
- **Python:** https://docs.python.org/3/
- **Go:** https://pkg.go.dev/
- **Rust:** https://doc.rust-lang.org/

## Lookup Process

### Step 1: Define the Question

Be specific about what you need:
- ❌ "How to use React?"
- ✅ "How to properly use useEffect cleanup function in React 18?"

### Step 2: Choose Search Terms

Include:
- Technology name + version
- Specific feature/API
- "documentation" or "reference"
- Site restriction for official docs

### Step 3: Verify Information

Before using found information:
- Check the date (prefer recent)
- Verify it's from official source
- Cross-reference with other sources if critical
- Check for deprecation notices

### Step 4: Document the Source

Always note:
- URL of the documentation
- Version of the technology
- Date accessed (for time-sensitive info)

## Output Format

When presenting documentation findings:

```markdown
## Documentation: [Topic]

### Source
- **URL:** [Link]
- **Version:** [Tech version]
- **Accessed:** [Date]

### Key Information
[Relevant excerpt or summary]

### Example Usage
```language
// Code example from docs
```

### Related
- [Link to related doc 1]
- [Link to related doc 2]
```

## Common Patterns

### API Parameter Lookup
```markdown
Need: Check parameters for `fetch()` in Next.js 14

Search: "Next.js 14 fetch options cache site:nextjs.org/docs"
Result: https://nextjs.org/docs/app/api-reference/functions/fetch
```

### Error Message Research
```markdown
Need: Understand "Cannot update during an existing state transition"

Search: "React Cannot update during an existing state transition site:react.dev"
Result: Official explanation + solution
```

### Best Practices Verification
```markdown
Need: Verify React useEffect best practices

Search: "React useEffect best practices 2024 site:react.dev"
Result: Current official recommendations
```

## Integration with Other Skills

- **web-research:** Use for broader research when docs don't have the answer
- **searxng:** Primary search tool for finding documentation
- **code-review:** Reference docs when reviewing code for compliance

## Tips

1. **Use site: restrictions** - Always prefer official docs with `site:domain.com`
2. **Check version** - Docs can change significantly between versions
3. **Look for examples** - Official docs often have copy-paste examples
4. **Note deprecations** - Watch for "Deprecated" warnings in docs
5. **Bookmark common docs** - Keep a list of frequently-used documentation URLs

## Anti-Patterns

❌ Using outdated documentation (always check version)
❌ Trusting unofficial sources without verification
❌ Copy-pasting code without understanding
❌ Not checking for breaking changes in new versions
❌ Relying solely on AI-generated code examples
