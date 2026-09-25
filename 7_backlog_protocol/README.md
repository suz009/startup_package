# Feature 7: Backlog Protocol

**Audience:** an LLM agent (or a human) installing this feature into a new repo.

**What this feature gives the new repo:** one cumulative, machine-readable list of everything
the project has decided not to do *yet*, which survives the session that raised it. Each task
gets an id (`TASK-NNN`), a priority, a status, a back-reference to the session summary that
created it, and — when it closes — a resolution saying what actually happened.

This is **distinct from** session summaries (Feature 1) and the decision log (Feature 2).
Session summaries record what happened on a day. The decision log records finalised
methodological choices. This records **outstanding work**, and it is the only one of the three
that is meant to be read as a *list* rather than as a history.

---

**Default view: `BACKLOG.html`** — a self-contained, searchable, sortable, filterable table that
opens from disk in any browser (made the default 2026-09-25 at the user's request; `BACKLOG.md`
is now opt-in via `--md`).

---

## The problem it solves

Without it, future work lives in the "Next Steps → Future / Not Urgent" section of whichever
session summary happened to be open that day. That has one fatal property: **a task written
on a given day is invisible unless somebody re-reads that day's file.** Ideas accumulate
across dozens of summaries with no single place to see them, and the ones that mattered are
indistinguishable from the ones that did not.

In the originating repo this list reached 258 tasks across five weeks. It is not a nice-to-have
at that size; it is the only thing standing between the project and a pile of forgotten
intentions.

---

## Files in this subfolder

| File | What it is | What to do with it |
|---|---|---|
| `README.md` | This file. | Read, then delete after install. |
| `BACKLOG_PROTOCOL.md` | The protocol document. | Copy into the target repo; replace `[PROJECT_NAME]`; replace the `area` table. |
| `backlog_TEMPLATE.json` | Empty scaffold for the canonical list. | Copy in, rename to `backlog.json`, fill the metadata. |
| `render_backlog_TEMPLATE.py` | Generates the searchable, sortable `BACKLOG.html` (default) and, with `--md`, an optional `BACKLOG.md`. | Copy in, rename to `render_backlog.py`, replace `[PROJECT_NAME]` and `AREA_LABEL`. |
| `precommit_snippet.sh` | Hook fragment that regenerates the views on commit. | Paste into the repo's pre-commit hook. |
| `claude_md_snippet.md` | The wiring text for the LLM's operating instructions. | Paste into the target repo's `CLAUDE.md`. |

---

## Install steps (LLM agent: execute these in order)

### Step 1 — Create the protocol directory
Recommended location: **`0_context/protocol/`** inside the target repo. If Feature 2 is
installed, it already exists.

### Step 2 — Copy files
- `BACKLOG_PROTOCOL.md` → `<target>/0_context/protocol/BACKLOG_PROTOCOL.md`
- `backlog_TEMPLATE.json` → `<target>/0_context/protocol/backlog.json`
- `render_backlog_TEMPLATE.py` → `<target>/scripts/render_backlog.py`

### Step 3 — Replace the placeholders
`[PROJECT_NAME]` appears in all three files. Replace every occurrence with the project's
name — the same string in each, since it becomes the heading of both generated views.

```bash
sed -i 's/\[PROJECT_NAME\]/Your Project Name/g' \
  0_context/protocol/BACKLOG_PROTOCOL.md \
  0_context/protocol/backlog.json \
  scripts/render_backlog.py
```

In `backlog.json`, also fill `metadata.created` and `metadata.last_updated` with today's date
in `YYYY-MM-DD` form.

### Step 4 — Replace the area vocabulary
Two places, and they must agree:
- the `area` table in `BACKLOG_PROTOCOL.md`
- the `AREA_LABEL` dictionary in `render_backlog.py`

The shipped values (`data`, `analysis`, `interface`, `schema`, `ops`, `docs`, `protocol`,
`legal`) are a **starter set, not a standard**. The point of `area` is to group the backlog
the way *this* project is actually divided; a vocabulary borrowed from another project groups
it the way that one was. Keep it short — a dozen at most.

### Step 5 — Wire it into the pre-commit hook
Paste `precommit_snippet.sh` into the repo's hook, above its final `exit`. If Feature 5 is
installed, that hook already exists at `.githooks/pre-commit`; if not, the snippet's header
comment says what two variables it expects.

Without this the views go stale, and a stale backlog is worse than none — people read the
generated file, so it is the one that has to be true.

### Step 6 — Wire it into the LLM's operating instructions
Paste `claude_md_snippet.md` into the target repo's `CLAUDE.md`. Replace
`[THE PROJECT'S USER-FACING DOCUMENTATION]` in the last bullet with whatever this project
actually shows its users. **Name the specific artefact** — a check with no address is skipped.

### Step 7 — Verify, then delete this subfolder
Run the "How to know it worked" checks below, then delete this subfolder from the target repo.

---

## The three rules that matter most

Everything else in the protocol is mechanics. These three are the ones that were learned the
hard way, and an installation that drops them keeps the format while losing the value.

**1. Integrate before you add.** Search the backlog before writing a new task. Two tasks
describing one piece of work do not look like a duplicate — they look like two pieces of work.
The list reads as longer than it is, the two drift as each is amended separately, and whichever
is picked up first silently makes the other wrong. Nobody notices, because nobody reads 200
tasks at once.

**2. Sweep at both ends of every session.** The backlog decays in a particular way: a task gets
half-done, the half that shipped is recorded in a session summary, and the task still asks for
all of it and is still marked `open`. It then reads as untouched work for ever. Correct
statuses, narrow descriptions to what actually remains, and *propose* merges and splits rather
than performing them — merging destroys an id somebody may have cited.

**3. Never take the next id from `metadata.next_id`.** Derive it from the highest id present,
plus one. In the originating repo that field drifted to "244 tasks, TASK-245 next" while the
file held 258 — and `TASK-245` already existed. The renderer now recomputes both counters and
writes the correction back, which makes them a *report* rather than a *source*.

---

## Cross-feature notes

- **Feature 1 (session summary protocol) is a real dependency.** The two-place rule says every
  task is recorded twice: in the session summary where it arose, for context, and in the
  backlog, for visibility. Each task's `raised_in` field points at a session summary filename.
  Install Feature 1 as well, or drop `raised_in` and accept that tasks lose their origin.
- **Feature 2 (decision protocol) is complementary, not required.** Tasks reference decisions
  in their `related` array (`["DEC-009"]`) and vice versa. Both work alone.
- **Feature 5 (pre-commit hook) is where Step 5 lands.** Standalone-usable — any hook will do —
  but Feature 5's is the natural home.
- **Feature 3 (folder structure)** supplies the `0_context/` directory these paths assume. If
  it is not installed, create just the two directories this feature needs.

---

## How to know it worked

After install, the new repo should:

- Have `0_context/protocol/backlog.json` with `total_tasks: 0` and an empty `tasks: []`.
- Produce `BACKLOG.html` from `python3 scripts/render_backlog.py` with no error, and its heading
  should carry the project's name rather than `[PROJECT_NAME]`.
- Open `0_context/protocol/BACKLOG.html` from disk in a browser — no server needed — and show
  an empty, sortable table with priority, status and area filters.
- Regenerate the view(s) automatically when `backlog.json` is staged for commit.

Then add one real task by hand and re-run the renderer. It should appear in the HTML table, and
the metadata counters should update themselves. Deliberately set `total_tasks` to a wrong
number first: the renderer should print `corrected metadata: total_tasks <wrong> → 1` and fix
the file. That is the check that the third rule above is actually wired in.

---

## Provenance

Developed in the **OpenQuali** repository between 2026-08-07 and 2026-09-10, across roughly
thirty sessions and 258 tasks. Unlike Features 1–6, it does **not** come from
`2025-12-PhD-Lit-Review-Mode-1` and was not part of the 2026-04-23 snapshot.
