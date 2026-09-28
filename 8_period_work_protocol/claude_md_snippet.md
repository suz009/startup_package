Paste into the target repo's `CLAUDE.md`, under whatever heading holds the other protocols.
Adjust the paths if the repo keeps its protocols, logs or scripts elsewhere. Fill in the
last bullet with this repo's own guardrails, or delete it if there are none worth
naming. **Name them specifically**: a guardrail that is only implied gets skipped.

---

- **Period work.** When the user asks for "period work" (e.g. "Period work for 3
  hours on …", or "period work on …; estimate how long"), read and follow
  `0_context/protocol/PERIOD_WORK_PROTOCOL.md`. It runs a seven-step workflow: kick-off →
  Claude familiarises, runs pre-flight checks and asks numbered questions **without
  starting** → the user's answers start the clock → autonomous work → review → close
  instruction → close. If no duration was given and no estimate requested, ask how long
  before reporting back.
  - Priority order: **safety, then independence, then efficiency**. Safety includes every
    rule in this file and this repo's protocols. Where the protocol and this file
    disagree, the more restrictive rule wins.
  - Starting period work **pre-authorises local commits on a `period/YYYY-MM-DD_HHMM`
    branch**, overriding the usual "commit when asked" for that branch only. Never push.
    Merge only after the user approves.
  - Measure token usage with `python3 scripts/token_usage.py`: estimate at pre-flight,
    check between tasks, report actual use at the end.
  - Logs: `0_context/period_work/PERIOD_WORK_LOG_YYYY-MM-DD_HHMM.md` (committed). Prompts
    for the user: `0_context/period_work/PERIOD_WORK_START.md`.
  - Repo-specific guardrails that bind period work: [e.g. "no real participant data
    leaves `1_data/raw/`", "snapshot the database before any migration", "calls to Scopus
    count against a weekly quota: cap per pre-flight"].
