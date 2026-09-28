# Feature 8: Period Work Protocol

**Audience:** an LLM agent (or a human) installing this feature into a repo, either a
**new** repo (see "Install steps") or an **existing** repo set up from an earlier version
of this package (see "Retrofit into an existing repo", which is the faster path for a
Claude instance arriving from another repo).

**What this feature gives the repo:** a protocol for leaving Claude Code working
unsupervised for a bounded period (about 30 minutes to 12 hours). Claude makes safe,
verified progress, measures its token use, and packages every question, decision and
approval into one review packet. The user deals with them all at once instead of being
interrupted.

The user's time is spent in predictable places: a short kick-off, answering pre-flight
questions, then one review at the end.

---

## The default workflow

| Step | Who | What happens |
|---|---|---|
| 1. Kick-off | User | Goals, plus a duration **or** a request for an estimate. |
| 2. Familiarise, pre-flight, ask | Claude | Reviews repo and backlog, checks time, permissions, git, external APIs and token budget, then asks numbered questions. **Does not start.** Asks for a duration if none was given. |
| 3. Answers = go | User | Answers by number, pastes `/usage`. The clock starts. |
| 4. Period work | Claude | Works alone; logs after every task; reports back at the end. |
| 5. Review | User | Answers the collected questions, gives feedback, approves the merge, allows a few minutes of fixes. |
| 6. Close instruction | User | "Close the session." |
| 7. Close | Claude | Final work, then session-closing tasks. |

The full rules are in `PERIOD_WORK_PROTOCOL.md` §1; the copy-paste prompts are in
`PERIOD_WORK_START.md`.

---

## Files in this subfolder

| File | What it is | Where it goes in the target repo |
|---|---|---|
| `README.md` | This file. | Read, then delete after install. |
| `PERIOD_WORK_PROTOCOL.md` | The protocol. | `0_context/protocol/PERIOD_WORK_PROTOCOL.md` |
| `PERIOD_WORK_START.md` | Copy-paste prompts for the user's steps. | `0_context/period_work/PERIOD_WORK_START.md` |
| `PERIOD_WORK_LOG_TEMPLATE.md` | The per-period log and review packet. | `0_context/period_work/_TEMPLATE.md` |
| `token_usage.py` | Measures token use from Claude Code's local transcripts. | `scripts/token_usage.py` |
| `claude_md_snippet.md` | Wiring text for `CLAUDE.md`. | Pasted into `CLAUDE.md`. |

---

## Install steps (new repo; LLM agent: execute in order)

### Step 1 — Copy files
Create `0_context/protocol/`, `0_context/period_work/` and `scripts/` if missing, and copy
the files to the locations in the table above. `chmod +x scripts/token_usage.py`.

### Step 2 — Adjust paths if the repo's layout differs
The protocol and snippet assume `0_context/protocol/backlog.json`,
`0_context/protocol/decision_log.json`, `0_context/session_summaries/` and
`scripts/token_usage.py`. If the repo keeps any of these elsewhere, edit the paths in
`PERIOD_WORK_PROTOCOL.md` (§§5, 6, 8) and in the snippet. If Feature 1, 2 or 7 is not
installed, delete the matching subsection of protocol §6.

### Step 3 — Wire it into `CLAUDE.md`
Paste `claude_md_snippet.md` (below its `---`) into the repo's `CLAUDE.md`, and fill in
its last bullet with this repo's specific guardrails. Without this line, a fresh session
does not know that "period work" means anything.

### Step 4 — Add the backlog field (if Feature 7 is installed)
Feature 7's current version already includes the `period_work` field (`yes` / `maybe`
/ `no`) in its protocol and renderer. For a new install nothing more is needed.

### Step 5 — Verify, then delete this subfolder
Run the checks in "How to know it worked", then delete this subfolder from the target.

---

## Retrofit into an existing repo

**For a Claude instance working in another repo, whose user has asked it to add period
work.** Read this README only. Open the other files when a step says to. The package
lives at `~/code/personal/startup_package/` (on this user's machine).

### R1 — Survey the target repo (read-only, a few commands)
```bash
cat CLAUDE.md
ls 0_context/protocol/ 0_context/session_summaries/ 2>/dev/null | head -40
find . -name render_backlog.py -not -path './.git/*'
ls .githooks/ 2>/dev/null; git config core.hooksPath
git status --short | head
```
From this, establish:
- **Which of Features 1, 2 and 7 are installed and where.** Paths vary between repos:
  the renderer can be at `scripts/`, `2_scripts/` or `0_context/protocol/`, and session
  summaries can have lower-case file names.
- **Instructions in `CLAUDE.md` that conflict with period work.** Typical ones:
  - "commit/push when the user asks": the snippet's commit carve-out resolves it; keep
    the original rule for normal sessions.
  - a standing "work autonomously until a pause point" default: keep it, and note
    that period work is the separate, time-bounded, fully-protocolled mode.
- **Guardrails that bind period work.** These include ethics commitments, real-data
  rules, snapshot-before-migration rules, paid or quota-limited APIs, and git hooks
  that run on commit (they will run on every checkpoint commit).

### R2 — Copy the four files
As in Install Step 1. If a file already exists at a destination, compare before
overwriting; do not overwrite silently.

### R3 — Adapt paths
Edit the copied `PERIOD_WORK_PROTOCOL.md` (§§5.1, 6, 8) and the snippet so every path
matches what R1 found. Delete §6 subsections for features the repo lacks.

### R4 — Wire into `CLAUDE.md`
Paste the snippet next to the repo's other protocol bullets. Fill its guardrails bullet
with what R1 found, **by name**. If R1 found conflicting instructions, add a
one-line cross-reference beside each (e.g. after "commit when asked": "except the
period branch; see Period work").

### R5 — Add `period_work` to the backlog (if the repo has Feature 7)
The repo's copy of Feature 7 predates the field. Port it from
`~/code/personal/startup_package/7_backlog_protocol/`:
- **`BACKLOG_PROTOCOL.md`:** add `"period_work": null` to the record example and copy
  the `period_work` vocabulary table, plus the sweep bullet that rates tasks.
- **The renderer:** port the changes by searching the package template for
  `period_work` (constants, HTML column, filter, Markdown marker). If the repo's renderer
  has diverged from the template, port by hand. Do not replace the file.
- **`backlog.json`:** do **not** bulk-edit ratings. Leave them unset. The first
  period's pre-flight and the regular sweeps rate tasks as they are touched.
- Re-run the renderer and confirm the column and filter appear.

### R6 — Other small alignments
- Session summary protocol (Feature 1): add the "Period work sessions" paragraph from
  the package's `1_session_summary_protocol/SESSION_SUMMARY_PROTOCOL.md` (Special
  Situations).
- Create `0_context/period_work/` and make sure it is **not** gitignored.

### R7 — Verify and report
Run the checks below. Then report to the user: what was installed, what paths were
adapted, which conflicts and guardrails were found and how each was handled, and
anything that needs their decision. Do **not** commit unless the repo's rules or the
user say so. Do not modify the startup package itself.

---

## Cross-feature notes

- **Feature 7 (backlog):** the period's work queue, and the `period_work` rating that
  decides which tasks are suitable for it. Strongly recommended. Without it, the
  queue comes from the user's kick-off prompt alone.
- **Feature 1 (session summaries):** the session summary keeps one phase entry per
  period that points to the log. The detail lives in the log (protocol §6.3).
- **Feature 2 (decision log):** methodological decisions are never finalised during a
  period. They are proposed in the log and logged at close once approved.
- **Feature 4 (settings):** permission prompts freeze unattended sessions. Pre-flight
  checks the permission mode. The deny rules in Feature 4's recommended global settings
  (force-push, `reset --hard`, `rm -rf`) back up the protocol's git rules.
- **Feature 6 (notifications):** the user is away during a period, so desktop
  notifications are mostly unseen. Harmless; no change needed.

---

## How to know it worked

- In a fresh session, "Period work for 1 hour on [small task]" makes Claude read the
  protocol, run pre-flight, create a log in `0_context/period_work/`, and come back with
  a plan and numbered questions **without starting work**.
- "Period work on [task]" with no duration: Claude offers an estimate range, or asks
  how long.
- `python3 scripts/token_usage.py` prints session and all-projects rows without error.
- If Feature 7 is installed: `BACKLOG.html` shows a "Period" column and filter.

---

## Design notes

- **This is a behavioural layer, not a sandbox.** It does not grant permission to
  bypass Claude Code's permission controls. Configure those separately and
  conservatively.
- **Token percentages need the user.** Claude can measure tokens but cannot see plan
  limits, so the user pastes `/usage` at steps 3 and 5. The ratio is recorded in each log
  and reused by the next pre-flight.

---

## Provenance

Drafted by the user and added to this package on 2026-09-28, then revised the same day
to fit Features 1, 2 and 7 and the user's default seven-step workflow. Not yet
field-tested in a contributing repo. Expect revisions after the first few periods.
