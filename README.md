# Repo Startup Package

A menu of conventions and protocols that have proven useful in practice, packaged
so they can be ported into a new repo without dragging in any project-specific
content.

**Provenance is per-feature, not per-package.** Features are contributed by
whichever repo developed them, at whatever date they were working there, and each
feature's `README.md` ends with a `Provenance` note saying where and when it came
from. There is no single snapshot date for the package as a whole.

| Features | Contributed by | As of |
|---|---|---|
| 1–6 | `2025-12-PhD-Lit-Review-Mode-1` | 2026-04-23 |
| 7 | `openquali` | 2026-09-10 |

Improvements made later in a contributing repo do not auto-propagate; re-copy the
subfolder if you want the latest.

---

## How to use

1. **Browse the feature subfolders below.** Each is independent; skip any you
   don't want.
2. **Copy the subfolders you want into your new repo** — anywhere convenient
   (suggested: `0_context/startup_package/` or `_setup/`, then delete after
   install).
3. **Open each copied subfolder's `README.md`** and either follow the
   instructions yourself or hand the README to an LLM agent and say
   *"implement this in this repo"*. Each README is written for an LLM agent
   and lists every file to create, where it goes, and what to put in it.
4. **Delete the startup-package copy from your new repo** once installed —
   the artifacts the README told you to create are now the source of truth.

---

## Features

| # | Subfolder | What it gives your new repo |
|---|---|---|
| 1 | [`1_session_summary_protocol/`](1_session_summary_protocol/) | A protocol + template for per-day operational logs that the LLM updates silently throughout each session. Provides cross-session continuity. |
| 2 | [`2_decision_protocol/`](2_decision_protocol/) | A protocol for logging substantive methodological decisions in a versioned, peer-reviewable way (PRISMA-S compatible). Includes JSON schema, CHANGELOG format, DEC-XXX numbering. |
| 3 | [`3_folder_structure/`](3_folder_structure/) | High-level dir conventions: numeric-prefix top-level dirs (`0_context/`, `1_data/`, `2_scripts/`, `3_analysis/`), stage-prefix script naming (`3_xxx.py`, `3a_xxx.py`), timestamped output dirs (`YYYY-MM-DD_HHMM`), `0_context/config/`, `0_context/background/`, `.gitignore` template, Git LFS setup, `README_project.md` template, `requirements.txt` template. Skip for repos without a pipeline shape (e.g. GUIs). |
| 4 | [`4_claude_settings/`](4_claude_settings/) | Claude Code settings architecture: durable patterns in user-global `~/.claude/settings.json`, near-empty per-project `.claude/settings.json`, untracked `.claude/settings.local.json`. Includes the rationale and recommended global-settings file. |
| 5 | [`5_precommit_json_hook/`](5_precommit_json_hook/) | A `.git/hooks/pre-commit` that blocks invalid JSON in `.claude/`. Belt-and-suspenders companion to feature 4. |
| 6 | [`6_notifications/`](6_notifications/) | Cross-platform desktop notification hook (Linux `notify-send` / macOS `osascript` / WSL→Windows BurntToast / terminal-bell fallback). Fires on Claude Code permission prompts, elicitation dialogs, idle prompts. |
| 7 | [`7_backlog_protocol/`](7_backlog_protocol/) | A cumulative, machine-readable backlog that survives the session that raised each task: `TASK-NNN` ids, priority and status vocabularies, a back-reference to the session summary that created it, and a resolution when it closes. Includes a generator producing a readable Markdown view and a sortable, filterable, self-contained HTML view, plus the pre-commit hook that stops those views going stale. |

---

## Cross-feature dependencies

- **Feature 1 references Feature 2.** The session summary protocol distinguishes
  itself from the decision protocol (session summaries log everything; decision
  log only logs finalized methodological decisions). If you install Feature 1
  but not Feature 2, edit Feature 1's protocol to drop the references — or
  install both.
- **Feature 5 belt-and-suspenders Feature 4.** Standalone-usable, but its
  raison d'être is to catch the failure mode that Feature 4's architecture
  prevents structurally.
- **Feature 6 wires into Feature 4.** The notification hook config goes into
  the global `~/.claude/settings.json` from Feature 4. Standalone-usable
  (drop the hook block into any active settings file), but Feature 4 is the
  natural home.
- **Feature 7 depends on Feature 1.** The backlog's two-place rule records every
  task twice — in the session summary where it arose, for context, and in the
  backlog, for visibility — and each task's `raised_in` field names a session
  summary file. Install both, or drop `raised_in` and accept that tasks lose
  their origin.
- **Feature 7 lands its hook in Feature 5.** The snippet that regenerates the
  backlog views on commit needs a pre-commit hook to live in; any hook will do,
  but Feature 5's is the natural home. Without it the generated views go stale,
  and the generated view is the one people actually read.
- **Feature 7 is complementary to Feature 2, not dependent on it.** Tasks cite
  decisions in their `related` array and vice versa; each works alone.
- **Feature 3 is logically independent** but assumes you adopt some directory
  for `0_context/` (or equivalent) where Features 1, 2, 4–6 and 7 reference paths.
  If you adopt an unusual top-level layout, the other features' READMEs let
  you point them at any directory.

---

## Versioning

This package is a **set of snapshots**, not a maintained library. There is no
auto-update mechanism — when you scaffold a new repo from it, you freeze each
feature's conventions at the date in that feature's `Provenance` note. To pick up
later improvements, re-copy the subfolders you want.

A feature developed in one repo and packaged here means that repo now holds the
master copy: it is a *source*, not an installation, and the "delete this
subfolder after install" step in each feature README applies to the repo it was
copied **into**, never to the one it came **from**.

If/when this package starts getting copied into >2 new repos and the desync
becomes painful, the right move is to promote it to a standalone GitHub
template repo. Until then, sibling-directory is sufficient.
