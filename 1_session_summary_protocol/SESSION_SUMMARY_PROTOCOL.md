# Session Summary Protocol

## Overview

Session summaries are detailed operational records of work performed during each working session (coding, research, analysis, planning). They are a repository management tool to help both the user and the LLM track what has been done, in what order, what remains to be completed, and what needs attention in future sessions.

**Audience:** Primarily the user and the LLM assistant (operational record).

**Relationship to Decision Protocol:** Session summaries track ALL work (decisions, implementation, testing, questions, plans). The decision protocol logs ONLY finalized methodological decisions needed for replication. Session summaries are forward-and-backward-looking; the decision protocol is backward-only.

---

## When to Create and Update Session Summaries

### 1. Creation (First Prompt of New Session)
- Create a new session summary file at the **very start** of each new working session.
- File location: `0_context/session_summaries/SESSION_SUMMARY_YYYY-MM-DD.md` (uppercase, ISO date format). Adapt the directory if your repo uses a different layout.
- If multiple sessions occur on the same day, append a suffix: `SESSION_SUMMARY_YYYY-MM-DD_afternoon.md` or `SESSION_SUMMARY_YYYY-MM-DD_continuation.md`.
- Initial status: `🔄 IN PROGRESS`.

### 2. Silent Updates During Session
Update the session summary **frequently and automatically** (no user notification required) after:
- Completing any todo item
- Making significant changes to files in the repository
- Completing a major phase of work (e.g. finishing a script, running an analysis, resolving an issue)
- Discovering important findings or encountering blockers
- The user explicitly requests an update

**How often:** Err on the side of frequent updates. Every 15–30 minutes of active work is reasonable. After every 2–3 file modifications is reasonable.

### 3. Pre-Commit Updates
**Before ANY git commit**, update the session summary and notify the user:
```
Session summary updated prior to commit.
```
This ensures the commit reflects documented work.

### 4. Session End
When the session ends (user indicates they're done or signing off):
- Perform a final comprehensive update.
- Set status to `✅ CLOSED` if all work is complete.
- Leave status as `🔄 IN PROGRESS` or `⏸️ PAUSED` if tasks remain incomplete.
- Ensure the "Next Steps" section accurately reflects what remains.

---

## File Naming Convention

**Required format:** `SESSION_SUMMARY_YYYY-MM-DD.md` (ISO 8601 date)

**Examples:**
- `SESSION_SUMMARY_2026-02-18.md`
- `SESSION_SUMMARY_2026-02-18_afternoon.md`
- `SESSION_SUMMARY_2026-02-18_continuation.md`

**Location:** `0_context/session_summaries/` (or your repo's analogous directory)

---

## Session Summary Structure

Use this exact template structure for every session summary (a copy is provided in `_TEMPLATE.md` next to this file):

```markdown
# Session Summary - YYYY-MM-DD

**Date:** YYYY-MM-DD
**Protocol Version:** X.YZ (start) [→ X.YZ (end) if changed]
**Status:** 🔄 IN PROGRESS | ✅ CLOSED | ⏸️ PAUSED
**Estimated Duration:** N hours

---

## Session Context

### Project Overview
[1–2 sentence high-level description of what this project is about.]

### Current Status at Session Start
[Snapshot of the project state when this session began.]
- Key metrics (corpus size, dataset row count, protocol version, etc.)
- Status of major workstreams/phases
- Recent completion status of strategies/analyses/pipelines

### Key Data Files
[List of primary data files relevant to this session's work.]
- File paths with brief descriptions
- Row counts, edge counts, or other key statistics

### Scripts Available
[List of key scripts that exist and are relevant to this session.]

### Known Issues
[Any data quality issues, bugs, blockers, or pending decisions that affect this session.]

---

## Session Objectives

**Main Goal:** [One-sentence description of the primary goal.]

**Priority Order:**
1. [First priority task]
2. [Second priority task]
3. [etc.]

---

## Work Completed

### [Phase/Topic 1 Name] (STATUS)
[Detailed description of work performed in this phase.]
- What was done
- Key findings or results
- Any decisions made (even if not formally logged in the decision protocol)
- Blockers encountered and how resolved (or not)

### [Phase/Topic 2 Name] (STATUS)
[Continue for each distinct phase of work…]

**Status markers:**
- (COMPLETED)
- (IN PROGRESS)
- (BLOCKED)
- (DEFERRED)

---

## Files Modified/Created

### Scripts
1. `path/to/script.py` — description of changes or purpose

### Reports/Outputs
1. `path/to/report.html` (file size if large) — description

### Data Files
1. `path/to/data.csv` (row count) — description

### Documentation/Protocol
1. `protocol/decision_log.json` — DEC-XXX logged
2. `protocol/CHANGELOG.md` — vX.Y entry added

**Important:** List ALL files touched during the session, even minor edits.

---

## Protocol Changes

[If the formal decision protocol was updated:]
- Protocol version incremented: vX.Y → vX.Z
- Decisions logged this session: DEC-XXX, DEC-YYY
- Total decisions in log: N

[If no protocol changes:]
_(None this session)_

---

## Key Decisions

[Record ALL significant decisions made during this session, whether or not they were formally logged in the decision protocol.]

### DEC-XXX: [Decision Title]
[Brief summary of decision, rationale, and implications.]

### Informal Decision: [Topic]
[Decisions made about implementation, design, or approach that don't rise to the level of formal protocol decisions but are important for continuity.]

---

## Next Steps

### Immediate (This Session if Continuing)
1. [Tasks to complete before session ends]

### Next Session
1. [Priority tasks for next working session]
2. [Blocked items waiting for external input]

### Future / Not Urgent
1. [Lower-priority tasks or ideas to revisit later]

---

## Important Notes for Next Session

[Anything the next LLM instance or user needs to know.]
- Uncommitted work and why
- Warnings about file states or data issues
- Reminders about methodology constraints
- Cross-references to decision protocol or other documentation

---

## Session Statistics

- **Protocol version at close:** X.YZ
- **Substantive decisions logged:** N (DEC-XXX, DEC-YYY)
- **Total decisions in log:** N
- **Scripts created/modified:** N
- **Reports generated:** N
- **Commits this session:** N

---

**Session Status:** [🔄 IN PROGRESS | ✅ CLOSED | ⏸️ PAUSED]
**Last Updated:** YYYY-MM-DD [HH:MM if helpful]
**Protocol Version:** X.YZ
```

---

## Content Guidelines

### 1. Level of Detail
**Session summaries should be VERY detailed.** Thoroughness is the ideal.

Include:
- Exact parameter values used in analyses
- Key statistics and results (row counts, edge counts, percentages)
- File sizes for large outputs (helps track bloat and performance)
- Error messages encountered and how resolved
- Exact commands run (especially for git, database queries, long-running processes)
- Full rationale for decisions, even informal ones
- Reasoning behind why certain approaches were tried or rejected
- Findings from exploratory analysis, even if ultimately not used
- Sample data (5–10 examples when investigating data quality issues)

**File size guidance:**
- 30 KB (~400 lines): totally normal
- 100 KB (~1300 lines): acceptable for complex sessions
- **500 KB threshold:** warn the user and ask for input.

### 2. What to Include vs. Exclude

**INCLUDE:**
- All work performed (coding, testing, analysis, investigation, Q&A)
- Implementation details (how scripts work, what they do)
- Findings and results (even negative results)
- Blockers and how they were resolved (or marked pending)
- Design decisions and rationale (even if not logged in the decision protocol)
- Questions asked and answered
- Future plans and pending tasks
- Work that was started but not completed
- Files created, modified, or deleted
- Git operations (commits, branch changes)
- Changes to directory structure or file organization
- Data quality issues discovered
- Performance metrics (runtime, file sizes, memory usage)

**EXCLUDE:**
- Conversational filler or greetings
- LLM reasoning about how to approach a task (the user doesn't need to see this unless it's relevant to understanding a decision)
- Duplicate information (reference previous sections instead)

### 3. Tone and Style
- **Factual and precise**: use exact numbers, file paths, parameter values.
- **Chronological within phases**: describe work in the order performed.
- **Objective**: record what happened without editorializing.
- **Complete**: assume the reader (future you or future LLM) knows nothing about what happened in this session.
- **Cross-referenced**: link to decision protocol entries, prior session summaries, or code locations when relevant.

### 4. Status Markers
Be **accurate** about task status:
- ✅ Complete/Done — task fully finished
- 🔄 In Progress — actively being worked on
- ❌ Not Started — planned but no work done yet
- ⏸️ Paused — started but intentionally stopped
- 🚫 Blocked — cannot proceed due to external dependency
- ⏭️ Deferred — intentionally postponed

### 5. Handling Multi-Day Work
If work on a topic spans multiple sessions:
- Create a new session summary for each calendar day.
- Reference prior session summaries: `(continuing from SESSION_SUMMARY_2026-02-17.md)`
- Provide brief context from the prior session in "Session Context".
- Don't duplicate full details from prior sessions — summarize and reference.

---

## Integration with Decision Protocol

Session summaries and the decision protocol serve **different purposes**:

| Aspect | Session Summary | Decision Protocol |
|--------|-----------------|-------------------|
| **Purpose** | Day-to-day operational record | Methodological through-line for replication |
| **Audience** | User + LLM (internal) | Peer reviewers + replicators (external) |
| **Temporal scope** | Forward + backward | Backward only |
| **Content** | All work, plans, questions | Finalized methodological decisions only |
| **Updates** | Continuous during session | Only when decisions are finalized |

### Examples of What Goes Where

**Example 1: Code implementation of a decided approach**
- **Session summary:** "Implemented equation (a) in `scripts/analysis.py:45`. Tested on synthetic data. Results: mean=2.3, SD=0.8. Committed."
- **Decision protocol:** _(Nothing logged — implementation details aren't methodological decisions.)_

**Example 2: Exploratory comparison without final decision**
- **Session summary:** "Created visualization comparing equation (a) vs (b) for modeling X. Equation (a) shows higher R²=0.89 vs 0.76. User will review and decide next session."
- **Decision protocol:** _(Nothing logged — no decision finalized yet.)_

**Example 3: Finalized methodological decision**
- **Session summary:** "After reviewing comparison plots, decided to use equation (a) for modeling X based on higher R² and interpretability. DEC-042 logged. Updated `analysis.py` to use equation (a) exclusively."
- **Decision protocol:** "DEC-042: Selected equation (a) over equation (b) for modeling X. Rationale: (a) achieves R²=0.89 vs (b) R²=0.76; (a) has clearer physical interpretation in our domain. Implemented in `analysis.py:45-67`."

**Example 4: Discussion without code changes**
- **Session summary:** "Discussed pros/cons of equation (a) vs (b). Decided equation (a) is better theoretically. Will implement next session."
- **Decision protocol:** "DEC-043: Selected equation (a) for modeling X. Rationale: superior theoretical foundation [cite]. Implementation pending."

### When Both Are Updated
Both get updated when:
1. A methodological decision is finalized AND
2. Code/analysis/data work occurred in the same session.

The session summary describes **what was done** (implementation, testing, results).
The decision protocol describes **what was decided and why** (for replication).

---

## Special Situations

### Very Short Sessions (< 30 minutes)
Still create a session summary. It may be brief, but it should exist.
- Mark status as ⏸️ PAUSED if work is incomplete.
- Be clear about what was and wasn't accomplished.

### Sessions with No Code Changes
If a session involves only:
- Discussion/planning
- Reading documentation
- Q&A about methodology
- Reviewing prior work

Still create a session summary documenting what was discussed and any decisions or plans made.

### Sessions with Failed Attempts
Document failed attempts thoroughly:
- What was tried
- Why it failed
- Error messages or unexpected results
- What was learned
- Whether it will be retried or abandoned

This prevents repeating failed approaches and documents the exploration process.

### Discovery of Prior Undocumented Work
If you discover files, commits, or work from prior sessions that wasn't documented:
- Note the discovery in the current session summary.
- Describe what you found.
- Reference the git commit hash if applicable.
- Don't try to retroactively create session summaries for past dates.

### Data Quality Issues
When data quality issues are discovered:
- Create a dedicated subsection in "Work Completed".
- Provide 5–10 specific examples.
- Quantify the scope (how many records affected).
- Describe the impact on analysis.
- Note resolution status (fixed, pending, documented-as-limitation).
- Cross-reference any decision protocol entries about how to handle.

---

## Workflow Integration

### Typical Session Flow

1. **Session Start:**
   - User begins work.
   - LLM creates `SESSION_SUMMARY_YYYY-MM-DD.md` with initial context.

2. **During Session:**
   - User requests a unit of work.
   - LLM does the work.
   - LLM silently updates the session summary: appends to "Work Completed", adds files to "Files Modified/Created".
   - Repeat.
   - Before any commit, LLM updates the session summary and notifies the user.

3. **Session End:**
   - User indicates session over.
   - LLM performs a final update, sets status accordingly, ensures "Next Steps" is accurate.

### Update Triggers (Summary)
**Automatic/Silent updates:**
- After completing todo items
- After significant file modifications
- After major phases of work
- Every 15–30 minutes of active work

**User-notified updates:**
- Before git commits: "Session summary updated prior to commit."
- When the user explicitly requests an update.

**No update needed:**
- Quick clarification questions
- Small conversational exchanges
- Reading files for context without changes

---

## Quality Checklist

Before closing a session or committing, verify the session summary:

- [ ] All sections present (no "TBD" or empty required sections)
- [ ] "Session Context" accurately reflects state at session start
- [ ] "Work Completed" describes all significant work in chronological phases
- [ ] "Files Modified/Created" lists ALL files touched (even minor edits)
- [ ] "Next Steps" clearly identifies what comes next
- [ ] Status emoji accurately reflects completion state
- [ ] All file paths are absolute or clearly relative to project root
- [ ] All statistics/metrics are exact (not "approximately" unless truly estimated)
- [ ] Any blockers or pending decisions are clearly noted
- [ ] Cross-references to decision protocol are accurate (DEC-XXX numbers)
- [ ] Session statistics are complete and accurate

---

## LLM Integration Instructions

### On Session Start
1. Check if a session summary for today exists.
2. If not, create `0_context/session_summaries/SESSION_SUMMARY_YYYY-MM-DD.md`.
3. Populate all sections with available information.
4. Set status to `🔄 IN PROGRESS`.
5. Do NOT notify the user about summary creation (this is automatic).

### During Session
1. After each significant unit of work, silently update the session summary.
2. Use the Edit tool to append to "Work Completed" and update "Files Modified/Created".
3. Update the "Last Updated" timestamp.
4. Do NOT notify the user about routine updates.

### Before Git Commits
1. Update the session summary with all work since the last update.
2. Notify the user: "Session summary updated prior to commit."
3. Proceed with the commit.

### On Session End
1. Perform a final comprehensive update.
2. Review status of all objectives.
3. Set status emoji based on completion state:
   - `✅ CLOSED` if all objectives complete
   - `🔄 IN PROGRESS` if objectives partially complete
   - `⏸️ PAUSED` if work intentionally paused
4. Ensure "Next Steps" accurately reflects what remains.
5. Ensure "Session Statistics" are accurate.

### Best Practices
- **Be thorough**: include all details (params, stats, file sizes, errors).
- **Be accurate**: use exact numbers and status markers.
- **Be chronological**: within phases, describe work in the order performed.
- **Be specific**: use absolute file paths, exact line numbers, commit hashes.
- **Cross-reference**: link to decision protocol, prior sessions, code locations.

---

## Summary

Session summaries are detailed operational logs that:
- Document ALL work performed (not just finalized decisions)
- Help user and LLM remember context across sessions
- Track open tasks, blockers, and future plans
- Provide a complete chronological record for each working day

Create them at session start, update them frequently and silently during work, update them with notification before commits, and finalize them at session end with accurate status.

Be thorough. 30–100 KB is normal. 500 KB is the warning threshold.

---

**Protocol Version:** 1.0 (startup-package snapshot, 2026-04-23)
**Maintained By:** User + LLM Assistant
