# Continuous Learning Skill v2

## Purpose

Automatically extract patterns from successful sessions and evolve them into reusable instincts with confidence scoring.

## When to Use

- After completing a complex task successfully
- When you discover a repeatable pattern
- Before ending a session with significant learnings
- During heartbeat checks to review recent patterns
- When a pattern recurs across multiple sessions

## Core Concepts

### Instincts

Instincts are distilled, high-confidence patterns extracted from successful sessions. Unlike raw learnings, instincts are:

- **Actionable** - Clear what to do
- **Tested** - Proven in multiple sessions
- **Confidence-scored** - Ranked by reliability
- **Contextual** - Tagged with when to apply

### Confidence Scoring

Each instinct has a confidence score (0-100):

| Score | Meaning | Actions |
|-------|---------|---------|
| 90-100 | **Verified** - Multiple successful uses | Auto-apply when context matches |
| 70-89 | **Strong** - Several successes, no failures | Suggest in similar contexts |
| 50-69 | **Emerging** - Some success, needs validation | Note as possibility |
| <50 | **Experimental** - Single occurrence | Log for tracking only |

### Pattern Evolution

Instincts evolve through stages:

```
Observation → Pattern → Instinct → Refined Instinct → Archived
    ↓           ↓         ↓            ↓                 ↓
  Session   Extracted  Validated   Evolved (v2)    Deprecated
```

## Instinct Format

```markdown
## [INST-YYYYMMDD-XXX] Pattern Name

**Created**: ISO-8601 timestamp
**Confidence**: 0-100
**Status**: experimental | emerging | strong | verified | archived
**Category**: coding | debugging | workflow | communication | tooling

### Trigger Conditions
When to apply this instinct:
- [Condition 1]
- [Condition 2]

### Pattern
What to do:
[Clear, actionable description]

### Example
```language
// Concrete example from real session
```

### Evidence
Sessions where this pattern succeeded:
- Session [ID/Date]: [Brief description]
- Session [ID/Date]: [Brief description]

### Counter-Evidence
Sessions where this failed (if any):
- Session [ID/Date]: [What went wrong]

### Evolution History
- v1 (2025-01-15): Initial extraction
- v2 (2025-01-20): Refined based on [feedback]

### Metadata
- **Source Session**: [Session ID or date]
- **Domain**: [frontend/backend/infra/etc]
- **Tags**: [tag1, tag2]
- **Related Instincts**: [INST-XXX]
- **Confidence History**: 
  - 2025-01-15: 50 (initial)
  - 2025-01-20: 70 (after 2nd success)
  - 2025-01-25: 85 (after 3rd success)

---
```

## Extraction Process

### Step 1: Identify Candidates

At session end, review for patterns that:
- ✅ Solved a non-trivial problem
- ✅ Were successful on first try
- ✅ Required insight or creativity
- ✅ Could apply to future tasks
- ✅ User expressed satisfaction with

**Skip patterns that:**
- ❌ Were obvious/straightforward
- ❌ Required multiple failed attempts
- ❌ Are project-specific one-offs
- ❌ User rejected or corrected

### Step 2: Extract Pattern

For each candidate:

1. **Describe the trigger** - When does this apply?
2. **Articulate the pattern** - What should be done?
3. **Provide an example** - Concrete illustration
4. **Note confidence factors** - Why trust this?

### Step 3: Assign Confidence

Start with base score, then adjust:

**Base score: 50**

**Adjustments:**
- +20: Pattern worked on first try
- +15: User explicitly praised the approach
- +10: Similar pattern succeeded before
- +10: Pattern is general (not project-specific)
- -20: Required multiple iterations
- -10: User had to correct or refine
- -15: Pattern is highly context-specific

### Step 4: Store Instinct

Append to `.learnings/INSTINCTS.md` with full format above.

## Instinct Application

### During Session Start

1. **Load relevant instincts** - Filter by task domain
2. **Surface high-confidence** - Priority to 70+ score
3. **Apply when triggered** - Auto-apply 90+ instincts
4. **Track outcomes** - Note success/failure for evolution

### Application Modes

**Auto-Apply (90+ confidence):**
```markdown
[Instinct triggered: "TypeScript Strict Mode"]
Applying pattern: Enable strict mode for new TypeScript projects
Rationale: 95% confidence, succeeded in 12 sessions
```

**Suggest (70-89 confidence):**
```markdown
[Instinct available: "API Error Handling"]
Similar pattern succeeded before. Apply?
- Yes: Use the pattern
- No: Continue normally
- Show: Display full instinct details
```

**Note (<70 confidence):**
```markdown
[Instinct logged: "Database Migration Pattern"]
Emerging pattern noted. Mention if relevant.
```

## Confidence Evolution

### After Each Application

Update confidence based on outcome:

**Success:**
- +5 if confidence < 70
- +3 if confidence 70-89
- +1 if confidence 90+ (cap at 100)

**Failure:**
- -15 if confidence < 70
- -10 if confidence 70-89
- -5 if confidence 90+ (floor at 50)

**Partial Success:**
- No change, or +1/-1 based on specifics

### Periodic Review

During heartbeats or weekly:

1. **Review low-confidence instincts** - Promote or archive
2. **Check for contradictions** - Resolve conflicts
3. **Merge duplicates** - Combine similar instincts
4. **Archive outdated** - Move deprecated to archive

## Output Format

### Session End Summary

```markdown
## Learning Summary

### Patterns Extracted
1. **[INST-20250115-001] TypeScript Configuration**
   - Confidence: 75 (emerging)
   - Trigger: New TypeScript project setup
   - Success: First-try compilation

2. **[INST-20250115-002] API Error Structure**
   - Confidence: 65 (emerging)
   - Trigger: REST API error handling
   - Success: Consistent error responses

### Instincts Applied
1. **[INST-20250110-003] React Component Structure**
   - Confidence: 88 → 91 (strong → verified)
   - Outcome: Successful component implementation

### Confidence Changes
- INST-20250110-003: 88 → 91 (+3, success)
- INST-20250108-001: 72 → 67 (-5, partial failure)

### Net Instinct Count
- Total: 15
- Verified (90+): 4
- Strong (70-89): 6
- Emerging (50-69): 4
- Experimental (<50): 1
```

## Integration with Other Skills

### self-improvement

- **self-improvement** logs raw learnings and errors
- **continuous-learning** extracts patterns from successes
- Both feed into `.learnings/` but serve different purposes

**Workflow:**
1. Log errors to `ERRORS.md` (self-improvement)
2. Log corrections to `LEARNINGS.md` (self-improvement)
3. Extract patterns to `INSTINCTS.md` (continuous-learning)
4. Promote verified instincts to workspace files

### memory-consolidation

- Periodic review of instincts
- Merge related instincts
- Archive outdated patterns
- Promote high-value instincts to `MEMORY.md`

## Storage Structure

```
.learnings/
├── LEARNINGS.md        # Corrections and knowledge gaps
├── ERRORS.md           # Failed commands and operations
├── FEATURE_REQUESTS.md # Requested capabilities
├── INSTINCTS.md        # Extracted patterns with confidence
└── archive/
    └── instincts-YYYY-MM.md  # Archived instincts
```

## Commands

### /instinct-status

Show current instinct inventory:

```markdown
## Instinct Inventory

### By Confidence
- Verified (90+): 4 instincts
- Strong (70-89): 6 instincts
- Emerging (50-69): 4 instincts
- Experimental (<50): 1 instinct

### By Category
- Coding: 8 instincts
- Debugging: 3 instincts
- Workflow: 3 instincts
- Communication: 1 instinct

### Recent Changes (last 7 days)
- New: 2 instincts
- Updated: 5 instincts
- Archived: 1 instinct
```

### /instinct-export

Export instincts to shareable format:

```bash
/instinct-export --format json --output instincts.json
/instinct-export --format markdown --output instincts.md
```

### /instinct-import

Import instincts from another workspace:

```bash
/instinct-import --source path/to/instincts.md --merge
```

### /instinct-evolve

Manually evolve an instinct:

```bash
/instinct-evolve INST-20250115-001 --confidence 85 --reason "3rd success"
```

## Quality Gates

### Before Extracting

- [ ] Pattern succeeded on first try (or mostly)
- [ ] Pattern is generalizable (not one-off)
- [ ] Clear trigger conditions identified
- [ ] Concrete example available
- [ ] User didn't reject the approach

### Before Promoting to Verified (90+)

- [ ] Succeeded in 3+ sessions
- [ ] No failures recorded
- [ ] Clear, unambiguous trigger
- [ ] User feedback positive
- [ ] Doesn't conflict with other verified instincts

### Before Archiving

- [ ] Deprecated by newer pattern
- [ ] Consistently failing (<50% success)
- [ ] Context no longer relevant
- [ ] Merged into broader pattern

## Anti-Patterns

❌ **Over-extraction** - Extracting every small win
❌ **Confidence inflation** - High scores without evidence
❌ **Context blindness** - Applying instincts in wrong context
❌ **Stagnation** - Not updating confidence based on outcomes
❌ **Contradiction** - Maintaining conflicting instincts
❌ **Hoarding** - Never archiving outdated instincts

## Example Session

### Scenario: Building a New API Endpoint

**What happened:**
1. Created endpoint following existing patterns
2. Used instinct INST-20250110-003 (component structure)
3. Discovered new pattern for error handling
4. User praised the error response structure

**Session end actions:**
1. Apply INST-20250110-003 → success, confidence 88→91
2. Extract new pattern: "Standardized API Error Responses"
   - Trigger: Creating new API endpoints
   - Pattern: Use consistent error structure
   - Confidence: 70 (user praised, first success)
   - Store as INST-20250115-003

**Output:**
```markdown
## Learning Summary

### Instincts Applied
- INST-20250110-003: React Component Structure
  - Confidence: 88 → 91 (verified)
  - Outcome: Clean component implementation

### Patterns Extracted
- INST-20250115-003: Standardized API Error Responses
  - Confidence: 70 (strong)
  - Trigger: New API endpoint creation
  - Evidence: User praised error structure
```

## Tips for Effective Use

1. **Be selective** - Only extract truly valuable patterns
2. **Score honestly** - Don't inflate confidence
3. **Track outcomes** - Always note success/failure
4. **Review regularly** - Weekly instinct review
5. **Evolve continuously** - Update based on evidence
6. **Share wisely** - Export/instincts across workspaces
7. **Archive bravely** - Don't cling to outdated patterns

## Metrics to Track

- **Extraction rate** - Patterns per session (target: 0-2)
- **Application rate** - Instincts used per session (target: 2-5)
- **Success rate** - % of applied instincts that succeed (target: >80%)
- **Verification rate** - Instincts reaching 90+ (target: 20-30% of total)
- **Archive rate** - Instincts archived per month (target: 5-10%)
