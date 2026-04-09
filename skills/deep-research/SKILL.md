# Deep Research Skill

## Purpose

Conduct thorough, multi-source research on complex topics with source attribution, cross-verification, and synthesized findings.

## When to Use

- Investigating new technologies or tools
- Competitive analysis
- Market research
- Technical feasibility studies
- Learning unfamiliar domains
- Gathering requirements for complex features

## Research Framework

### Phase 1: Define Scope

**Before starting, clarify:**
- What specific question are we answering?
- What depth is needed? (overview vs deep dive)
- What's the time budget?
- What format should the output take?

**Example scopes:**
- ❌ "Research AI" (too broad)
- ✅ "Research vector databases for semantic search in production, compare top 5 options" (specific)

### Phase 2: Multi-Source Collection

**Search layers (in order):**

1. **Official Sources**
   - Documentation, whitepapers, official blogs
   - GitHub repositories, release notes
   - Company/organization websites

2. **Expert Analysis**
   - Technical blogs from recognized experts
   - Conference talks and presentations
   - Academic papers (when applicable)

3. **Community Insights**
   - Stack Overflow discussions
   - Reddit technical communities
   - Discord/Slack community insights
   - Twitter threads from practitioners

4. **Comparative Analysis**
   - Comparison articles and benchmarks
   - Review sites (with skepticism)
   - User testimonials and case studies

### Phase 3: Cross-Verification

**For each claim:**
- Find at least 2 independent sources
- Prefer primary sources over secondary
- Note any contradictions between sources
- Flag unverified claims

**Verification levels:**
- ✅ **Verified** - Multiple independent sources confirm
- ⚠️ **Partial** - Some confirmation, needs more research
- ❓ **Unverified** - Single source or conflicting info

### Phase 4: Synthesis

**Organize findings into:**
- Key takeaways (executive summary)
- Detailed analysis (by topic)
- Comparison tables (when applicable)
- Recommendations with rationale
- Open questions and uncertainties

## Output Format

```markdown
# Research Report: [Topic]

## Executive Summary
[3-5 bullet points with key findings]

## Methodology
- **Scope:** [What we researched]
- **Sources:** [Number and types of sources]
- **Time spent:** [Research duration]
- **Confidence level:** [High/Medium/Low]

## Findings

### [Topic 1]
[Detailed findings with sources]

**Sources:**
1. [Source 1] - [URL] - [Key point]
2. [Source 2] - [URL] - [Key point]

### [Topic 2]
...

## Comparison

| Option | Pros | Cons | Best For |
|--------|------|------|----------|
| A | ... | ... | ... |
| B | ... | ... | ... |

## Recommendations

### Primary Recommendation
[What we recommend and why]

### Alternatives
[Other viable options and when to choose them]

## Risks & Considerations
- [Risk 1]
- [Risk 2]

## Open Questions
- [Question 1] - [What would resolve it]
- [Question 2] - [What would resolve it]

## Appendix: All Sources

### Primary Sources
- [List with URLs]

### Secondary Sources
- [List with URLs]

### Not Excluded (Low Quality)
- [Sources considered but not used, with reason]
```

## Search Techniques

### Advanced Search Operators

```
# Exact phrase
"exact phrase to match"

# Exclude terms
topic -unwanted

# Site-specific
topic site:github.com
topic site:medium.com

# Filetype
topic filetype:pdf

# Date range
topic after:2024-01-01

# Title search
intitle:topic

# Related sites
related:example.com
```

### Iterative Search Strategy

1. **Broad search** - Understand the landscape
2. **Identify key terms** - Learn the vocabulary
3. **Focused search** - Deep dive on specifics
4. **Gap analysis** - What's missing?
5. **Targeted search** - Fill the gaps

## Quality Assessment

### Source Credibility Checklist

**High credibility:**
- ✅ Official documentation
- ✅ Peer-reviewed papers
- ✅ Recognized experts with track record
- ✅ Well-maintained open source projects
- ✅ Major tech companies' engineering blogs

**Medium credibility:**
- ⚠️ Individual developer blogs (with good content)
- ⚠️ Community tutorials with citations
- ⚠️ Conference talks (verify claims)

**Low credibility:**
- ❌ Content farms without citations
- ❌ AI-generated content without verification
- ❌ Outdated tutorials (>2 years for fast-moving tech)
- ❌ Promotional content without technical depth

### Red Flags

- No author or date
- No citations or sources
- Contradicts official documentation
- Too good to be true claims
- Outdated information presented as current

## Integration with Other Skills

- **searxng:** Primary search tool
- **documentation-lookup:** For official documentation
- **code-review:** When researching implementation patterns

## Tips for Effective Research

1. **Start broad, then narrow** - Understand context before details
2. **Take notes as you go** - Use a research log
3. **Track your sources** - Always save URLs
4. **Note contradictions** - They reveal areas needing more research
5. **Time-box your research** - Avoid rabbit holes
6. **Know when to stop** - Diminishing returns are real

## Anti-Patterns

❌ Relying on a single source
❌ Not verifying claims
❌ Including outdated information
❌ Cherry-picking sources that confirm bias
❌ Not noting uncertainties
❌ Endless research without conclusion
❌ Copy-pasting without understanding

## Example Research Sessions

### Example 1: Technology Selection
```
Topic: "Choose a state management library for React app"

Search queries:
1. "React state management comparison 2024"
2. "Redux vs Zustand vs Jotai performance"
3. "Zustand GitHub stars trends"
4. "React state management best practices site:react.dev"

Output: Comparison table + recommendation with rationale
```

### Example 2: Technical Feasibility
```
Topic: "Can we implement real-time collaboration like Google Docs?"

Search queries:
1. "operational transformation vs CRDT"
2. "Yjs documentation"
3. "real-time collaboration architecture"
4. "Google Docs operational transformation paper"

Output: Feasibility assessment + implementation approach options
```
