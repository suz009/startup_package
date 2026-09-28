# Period Work — Prompts

Copy-paste prompts for each user step of the default workflow (Period Work Protocol §1).
Replace the bracketed parts. The protocol does the rest, so none of these need to repeat
its rules.

| Step | Who | Prompt below |
|---|---|---|
| 1. Kick-off | User | **1a** (fixed duration) or **1b** (estimate) |
| 2. Familiarise, pre-flight, ask | Claude | — |
| 3. Answers = go | User | **3** |
| 4. Period work | Claude | — |
| 5. Review | User | **5** |
| 6. Close instruction | User | **6** (can be combined with 5) |
| 7. Close | Claude | — |

---

## 1a. Kick-off: fixed duration

> **Period work for [DURATION]. Goals: [GOALS / TASK-NNN / AREA]. Then continue with
> other ready backlog work in priority order. Review the repo, run pre-flight, and come
> back with your plan and questions before starting.**

Example:

> **Period work for 3 hours. Goals: TASK-042 and its tests, then the import backlog.
> Review the repo, run pre-flight, and come back with your plan and questions before
> starting.**

## 1b. Kick-off: estimate

> **Period work on [GOALS]. Estimate how long it will take. Review the repo, run
> pre-flight, and come back with your estimate, plan and questions before starting.**

If you give neither a duration nor ask for an estimate, Claude will ask how long.

### Optional constraints (add to either)

- `Do not add new dependencies.`
- `Stay within tasks tagged [X].`
- `Up to [N] calls to [API] are fine.`
- `You may use subagents for broad searches.`
- `Token ceiling: [N]% of my weekly limit.`
- `Go straight into the period; defer all questions to the end.` (skips step 2's stop)

---

## 3. Answers = go

Paste your `/usage` output so Claude can calibrate token use (Protocol §5.1).

> **Answers: 1. [..] 2. [..] 3. [..]. [Adjustments to plan / window / ceiling / API
> limits.] /usage: [PASTE]. Go.**

The clock starts when this is sent. Run `/compact` first if Claude suggested it.

---

## 5. Review

> **Review: 1. [answer] 2. [answer] … Feedback: [..]. Merge: [yes into BRANCH / no].
> /usage: [PASTE]. Take [N] minutes to [final fixes], then report.**

## 6. Close

> **Close the session.**

Or combine with step 5:

> **[Review answers as above.] Then close the session.**

---

The protocol's safety rules and the repo's own guardrails stay in force unless you
**explicitly authorise a specific otherwise-restricted action**. A broad instruction
such as "work autonomously" or "do whatever is needed" is not permission to cross a
safety boundary.
