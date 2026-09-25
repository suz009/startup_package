# Backlog Protocol — [PROJECT_NAME]

**Version:** 1.0
**Created:** 2026-08-07
**Status:** Active

---

## The problem this solves

Before this protocol, future work was recorded only in the "Next Steps → Future / Not Urgent"
section of whichever session summary happened to be open that day. That has one fatal
property: **a task written on a given day is invisible unless somebody re-reads that day's
file.** Scattered future tasks accumulate across session summaries with no single place to
see them.

The fix is the same shape as the decision log: one canonical machine-readable file that
accumulates across all sessions, plus a human-readable rendering of it.

---

## The two-place rule

Every future task gets recorded **twice**, and both are required:

1. **In the session summary** where it arose — under `Next Steps`, with its task ID.
   This preserves *context*: what we were doing when the need surfaced.
2. **In `0_context/protocol/backlog.json`** — the canonical, cumulative list.
   This preserves *visibility*: it survives the session that created it.

The session summary answers "what did we decide that day". The backlog answers
"what is still outstanding, across the whole project". Neither replaces the other.

---

## Files

| File | Role |
|---|---|
| `0_context/protocol/backlog.json` | **Canonical.** Machine-readable, append-and-amend. |
| `0_context/protocol/BACKLOG.html` | **Generated — the default view.** One row per task, sortable, filterable and searchable. Self-contained: opens from disk in any browser, no server, no network. Never edit by hand. |
| `0_context/protocol/BACKLOG.md` | *Optional*, generated only with `--md` (or when it already exists). Reads in order, grouped by priority. Never edit by hand. |
| `scripts/render_backlog.py` | Regenerates the views from `backlog.json`, and corrects the metadata counters. Standard library only. |

**BACKLOG.html is how people read the backlog** (default since 2026-09-25): sort by priority,
filter to one area, search descriptions. An LLM agent reads `backlog.json` directly — the
HTML embeds the same data but is far larger. BACKLOG.md is off by default; turn it on with
`python3 scripts/render_backlog.py --md` if a document-style or diff-friendly view is wanted.

Regenerate with:

```bash
python3 scripts/render_backlog.py
```

---

## Task record format

```json
{
  "id": "TASK-001",
  "title": "One line, imperative mood",
  "description": "Why it matters and what done looks like. Two to five sentences.",
  "area": "data",
  "priority": "mvp",
  "status": "open",
  "raised": "2026-04-23",
  "raised_in": "SESSION_SUMMARY_2026-04-23.md",
  "raised_by": "user",
  "blocked_by": null,
  "related": ["DEC-009"],
  "closed": null,
  "resolution": null
}
```

### Field vocabularies

**`area`** — where the work lives.

**Replace this table with your own project's areas.** These are a starter set, not a
standard: the value of `area` is that it groups the backlog the way *this* project is
actually divided, and a vocabulary borrowed from another project groups it the way that one
was. Keep the list short — a dozen at most — and add to it only when a genuinely new part of
the project appears.

| Value | Meaning |
|---|---|
| `data` | Getting data in, out, and cleaned |
| `analysis` | Turning data into results |
| `interface` | Anything a person looks at or clicks |
| `schema` | Data structure and migrations |
| `ops` | Environment, backups, tooling, hooks |
| `docs` | Documentation and user-facing text |
| `protocol` | Process documents, logging, conventions |
| `legal` | IP, licensing, entity, domains |

**`priority`** — when, not how important.

| Value | Meaning |
|---|---|
| `now` | Blocking current work. Should be a todo, not a backlog item, unless it is waiting on someone. |
| `mvp` | Required before the project's first real use on real data. |
| `post_mvp` | Wanted, scheduled after MVP. |
| `someday` | Genuinely good idea, no committed timeline. |

**`status`** — `open` | `in_progress` | `done` | `dropped`.

A `dropped` task keeps its record and gains a `resolution` explaining why. Tasks are never
deleted, for the same reason superseded planning documents are never overwritten: the
reasoning trail is the point.

---

## When to add a task

Add one whenever any of these is true:

- The user says "someday", "eventually", "later", "future feature", or "not now".
- A design decision defers something (every `Deferred` row in a spec should have a task).
- A workaround is accepted in place of a real fix.
- A dependency, blocker, or external action is identified that we are not doing today.
- An open question in a planning document is not resolved in the session that raised it.

**Do not** add a task for work being done in the current session. That is what the todo
list is for.

---

## Integrate before you add

**Search the backlog before writing a new task.** When the user asks for something, the
question is not "what task describes this?" but "does a task already own this ground?" —
and often one does, approached from a different angle. Amend that task rather than
creating a second one beside it.

The failure this prevents is specific and it is quiet. Two tasks describing one piece of
work do not look like a duplicate: they look like two pieces of work. The backlog reads as
longer than it is, the two drift as each is amended separately, and whichever is picked up
first silently makes the other wrong. Nobody notices, because nobody reads 180 tasks at
once.

When amending, **say what changed and when** — a dated `AMENDED`, `NARROWED`, `MERGED` or
`STATUS CORRECTED` paragraph appended to the description, in the user's own words where
they gave them. The original text stays. A task's description is a record of how the
thinking arrived where it did, and overwriting it loses the reasoning while keeping the
conclusion.

Add a genuinely new task when the ask is new. The rule is *integrate before you add*, not
*never add*.

---

## Sweep the backlog at the start and end of every session

The backlog decays in a particular way: a task gets half-done, the half that shipped is
recorded in a session summary, and the task itself still asks for all of it and is still
marked `open`. It then reads as untouched work for ever.

So at session start and session end, review the backlog **as a whole**, not only the tasks
being worked on:

- **Correct statuses.** Anything finished becomes `done` with `closed` and `resolution`.
- **Correct contents.** Where some but not all of a task shipped, append a dated note
  saying which part is done and narrowing what remains. A task whose description no longer
  describes the outstanding work is worse than no task.
- **Propose merges and splits.** Tasks that turn out to be one piece of work should be
  named as such; tasks that have grown two independent halves should be split. **Propose,
  do not perform** — merging two tasks destroys an id somebody may have referred to, so it
  is the user's call.

Report what the sweep found in the session summary. If it found nothing, say that too.

---

## Keep user-facing documentation in step with the code

Whatever this project shows its users to explain itself — a help screen, a README, a
quick-start, a cheat sheet of shortcuts — **nothing keeps it in step with the code
automatically.**

It decays exactly like the backlog does, and worse. A feature is added, changed or removed;
the code is correct; the documentation still describes what used to be true. **Documentation
that lies is worse than none, because it is believed** — the reader follows it instead of
trying the thing, so a wrong line does not merely fail to help, it actively teaches the wrong
move, and the mistake survives until something breaks.

So at session start and session end, read the user-facing documentation against what the
project actually does:

- **Everything built or changed this session is described**, wherever a reader would look
  for it.
- **Every line still describes something that exists.** A feature that was removed or
  rewritten leaves its description behind; that line is the dangerous kind of wrong.
- **Changed defaults are stated.** When behaviour changes silently, the documentation is
  where the user finds out.
- **The answer to the obvious question is there.** If a change will make somebody ask "does
  X still work?", answer it in the documentation rather than waiting to be asked.

Checked at **both** ends for the same reason the backlog is. At the start it catches what a
previous session left behind; at the end it catches what this one did. The start-of-session
pass is a genuine review, not a formality — documentation is behind more often than not,
because the moment a feature is finished is the moment it feels obvious.

Record in the session summary what was added or corrected. If nothing needed changing, say
that too.

*Adapt the target to the project.* In a repo with a graphical interface this means the help
screen; in a data-pipeline repo it means the README and the runbook; in a library it means
the docstrings and the usage examples. The discipline is the same: **name the specific
artefact in your `CLAUDE.md` so the check has an address**, or it will be skipped.

---

## Assistant responsibilities

### During a session
- Add tasks to `backlog.json` as they arise, silently, alongside the session-summary update.
- **Check for an existing task that already covers the ask, and amend it instead** — see
  *Integrate before you add*.
- Assign the next sequential `TASK-NNN`. IDs are never reused.
- When a task is completed, set `status: "done"`, fill `closed` and `resolution`, and say so
  in the session summary.

### At session start
- Read `backlog.json` as part of onboarding, alongside the most recent session summaries
  (the user reads the same list in `BACKLOG.html`).
- **Sweep it** — statuses, contents, and any merges or splits worth proposing.
- Surface any `mvp`-priority open tasks that bear on the session's objectives.
- **Check the user-facing documentation** against the project as it currently stands, and
  fix what the last session left behind.

### At session end
- **Sweep it again**, and record in the session summary what the sweep changed.
- **Check the user-facing documentation again**, covering everything this session added or
  changed, and record in the session summary what was corrected.

### Before any commit
- Regenerate the views if `backlog.json` changed. The pre-commit hook does this
  automatically if it is installed.

---

## Never take the next id from `metadata.next_id`

**Derive it from the tasks themselves** — the highest id present, plus one.

`metadata.total_tasks` and `metadata.next_id` are maintained by hand and they drift. In the
originating repo they reached "244 tasks, TASK-245 next" while the file actually held 258,
so the next task created would have been given an id that already belonged to another one.
Ids are never reused, and a reused id silently reattributes work to a task somebody has
already referred to elsewhere.

`render_backlog.py` recomputes both fields from the array on every run and writes the
correction back, so the stored numbers become a *report* rather than a *source*. Treat them
that way: read them if you like, act on the array.

---

**Protocol Version:** 1.0
**Maintained By:** User + LLM Assistant
**Adapted from:** the backlog protocol developed in the OpenQuali repository, 2026-08 to 2026-09.
