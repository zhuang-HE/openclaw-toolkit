# /harness-audit Command

## Purpose

Audit and optimize your AI agent harness configuration for performance, cost, and effectiveness.

## Usage

```bash
/harness-audit [options]
/harness-audit --full      # Comprehensive audit
/harness-audit --quick     # Quick check (default)
/harness-audit --report    # Generate detailed report
```

## What It Audits

### Configuration Analysis

**1. Model Selection**
- Is the model appropriate for the task?
- Are we over-using expensive models?
- Could simpler models handle some tasks?

**2. System Prompt Analysis**
- Is the system prompt too long?
- Are there redundant instructions?
- Is the persona clearly defined?

**3. Context Usage**
- Current context utilization
- Token budget remaining
- Compaction opportunities

**4. Skills & Agents**
- Are the right agents being used?
- Are skills properly configured?
- Missing agents for common tasks?

### Performance Metrics

**5. Session Analysis**
- Average session length
- Token consumption per session
- Common task patterns

**6. Cost Analysis**
- Estimated cost per session
- Cost breakdown by model
- Optimization opportunities

**7. Quality Indicators**
- Re-run frequency (indicates unsatisfactory outputs)
- Manual correction rate
- Task completion rate

## Audit Checks

### Quick Audit (--quick)

```markdown
## Harness Audit Summary

### Configuration
- **Model:** [Current model]
- **System prompt length:** [X tokens]
- **Context utilization:** [X%]

### Recommendations
1. [High priority recommendation]
2. [Medium priority recommendation]

### Score: [X/100]
```

### Full Audit (--full)

```markdown
## Comprehensive Harness Audit

### 1. Model Configuration
| Task Type | Current Model | Recommended | Reason |
|-----------|---------------|-------------|--------|
| Code review | qwen3.5-plus | qwen3.5-plus | ✅ Appropriate |
| Simple Q&A | qwen3.5-plus | qwen3-max | ⚠️ Overkill |

### 2. System Prompt Analysis
- **Current length:** 2,400 tokens
- **Recommended:** <2,000 tokens
- **Redundant sections:** [List]
- **Missing sections:** [List]

### 3. Context Efficiency
- **Average utilization:** 65%
- **Compaction frequency:** Every 40 messages
- **Recommendation:** Increase to every 50 messages

### 4. Agent Utilization
- **Most used:** code-reviewer (45% of sessions)
- **Underused:** security-reviewer (2% of sessions)
- **Missing:** build-error-resolver (requested 12 times)

### 5. Cost Analysis
- **Daily average:** $X.XX
- **Monthly projection:** $XX.XX
- **Optimization potential:** -XX%

### 6. Quality Metrics
- **Re-run rate:** 15% (target: <10%)
- **Manual correction rate:** 8% (target: <5%)
- **Task completion rate:** 92% (target: >90%)

## Priority Actions

### High Priority
1. [Action 1] - Expected impact: [X%]
2. [Action 2] - Expected impact: [X%]

### Medium Priority
1. [Action 1]
2. [Action 2]

### Low Priority
1. [Action 1]
2. [Action 2]

## Overall Score: [X/100]
```

## Scoring System

| Category | Weight | Metrics |
|----------|--------|---------|
| Configuration | 25% | Model selection, prompt efficiency |
| Performance | 25% | Context usage, response time |
| Cost | 20% | Token efficiency, model optimization |
| Quality | 30% | Completion rate, re-run rate |

## Output Actions

After audit, the agent should:

1. **Present findings** - Clear summary of issues
2. **Prioritize actions** - What to fix first
3. **Offer to implement** - "Should I apply these changes?"
4. **Track improvements** - Compare with previous audits

## Integration

Use with:
- `/quality-gate` - For code quality
- `/sessions` - For session analysis
- `/model-route` - For model optimization

## Report Generation

```bash
/harness-audit --report > audit-report-$(date +%Y-%m-%d).md
```

Report includes:
- Historical comparison
- Trend analysis
- Detailed metrics
- Action items checklist

## Best Practices

### Model Selection
- Use powerful models for complex reasoning
- Use lighter models for simple tasks
- Consider latency requirements

### Prompt Optimization
- Keep system prompts concise
- Remove redundant instructions
- Test changes incrementally

### Context Management
- Compact before hitting limits
- Save important context to files
- Use strategic summarization

### Cost Optimization
- Match model to task complexity
- Use caching when possible
- Batch similar requests
