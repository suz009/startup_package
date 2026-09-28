# Period Work Log — YYYY-MM-DD HH:MM

**Bottom line:** [done / partly done / blocked — N of M queued tasks complete. One sentence.]

Follows `0_context/protocol/PERIOD_WORK_PROTOCOL.md`. Update after **every** task; the
session can end without warning.

---

## Needs You

Numbered so you can answer by number. Only what Claude could not reasonably resolve
itself. Merge approval is always the last item.

1. **[TASK-NNN] [Short question]**
   - **Why it matters:**
   - **Options:** (a) … (b) …
   - **Recommendation:**
   - **Already done / can proceed without an answer:**
2. **[Proposed decision] [TASK-NNN] [Title]** *(would become DEC-XXX once approved)*
   - **Decision proposed:**
   - **Rationale / alternatives:**
3. **Merge `period/YYYY-MM-DD_HHMM` into `[BRANCH]`?**

---

## Pre-flight (Step 2)

- **Goals / scope:**
- **Time:** started [HH:MM] · window [duration or estimated range] · ends by [HH:MM]
- **Queue:** TASK-NNN (`period_work`: yes) → TASK-NNN (maybe) → …
- **Token estimate / ceiling:** [range] / [ceiling] ([% if calibrated])
- **Permissions:** [mode; commands expected to prompt and how handled]
- **Commands:** [test / lint / build] — [baseline: passing / pre-existing failures]
- **Git:** from `[BRANCH]` → `period/YYYY-MM-DD_HHMM` · tree [clean / dirty → handled how]
- **External services approved:** [service, cap] or none
- **Guardrails in play:** [repo-specific rules relevant to this work]

## Completed

- **[TASK-NNN] [title]:** what changed · how verified · commit `[sha]`

## In Progress

- **[TASK-NNN]:** current state · exact next step

## Assumptions Made

Material, non-obvious, reversible choices made without the user.

- **[TASK-NNN]:**

## Problems / Findings

Bugs, pre-existing failures, security or guardrail concerns, technical debt found but
not fixed this period. New backlog tasks raised: [TASK-NNN, …]

-

## Deferred Attempts

Lines of work deliberately stopped because further attempts had poor expected value.

- **[TASK-NNN]:** tried [A, B, C]; stopped because …

## Time and Token Usage

From `python3 scripts/token_usage.py --since <period start>`. `/usage` % is from the
user's pasted readings.

| When | Elapsed | Output | Fresh input | Cache read | `/usage` (5h / weekly) |
|---|---|---|---|---|---|
| Step 3 (start) | 0:00 | | | | |
| | | | | | |
| End of period | | | | | |
| Step 5 (review) | | | | | |

- **Against estimate / ceiling:**
- **Calibration** (from the two `/usage` readings): ≈ [N] tokens per 1% weekly
- **Notes:**

## Recommended Next Actions

1.

---

## Review Outcome (Steps 5–7)

- **Answers received:**
- **Final fixes done:**
- **Merged:** [yes → BRANCH / no]
- **Applied at close:** [DEC-XXX logged, tasks unblocked, …]
