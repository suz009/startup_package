# Feature 4: Claude Code Settings

**Audience:** an LLM agent (or a human) installing this feature into a new repo.

**What this feature gives the new repo:** a clean Claude Code permissions
architecture that:
- Doesn't recurringly malform itself during cross-machine merges
- Doesn't bloat with one-off "approve and remember" entries
- Keeps durable patterns in the user's global config so they apply to every repo
- Keeps the per-project file minimal and the per-machine file untracked

This architecture was developed in the parent repo on 2026-04-23 in response
to repeated `.claude/settings.local.json` corruption. See the parent repo's
`SESSION_SUMMARY_2026-04-23.md` for the full diagnosis.

---

## Why this matters

Three failure modes were observed in the parent repo:

1. **Cause 1 — force-tracked despite `.gitignore`.** `.claude/` was in
   `.gitignore` but `settings.local.json` had been added with `git add -f`,
   so it stayed tracked. Every cross-machine pull became a merge candidate.
2. **Cause 2 — auto-bloat from "approve and remember".** Every approved
   permission appended a literal command string to `settings.local.json`
   instead of being matched against existing patterns. The file accumulated
   dozens of useless hyper-specific entries → bigger merge surface.
3. **Cause 3 — merge tools mangle JSON-encoded shell strings.** Multi-line
   bash commands got split on `;`, `awk` quotes got double-doubled, and
   eventually a paren got dropped — invalidating the JSON entirely.

The architecture below addresses all three structurally.

---

## Architecture

| File | Scope | Tracked? | Purpose |
|---|---|---|---|
| `~/.claude/settings.json` | User, all projects, this machine | No (in home) | Durable patterns: language/tool wildcards, hooks, deny rules |
| `<repo>/.claude/settings.json` | Project-shared (in principle) | No (in `.gitignore`) | Project-specific overrides only. Usually empty. |
| `<repo>/.claude/settings.local.json` | Per-project, per-machine | **No — must stay untracked** | Buffer for harness auto-appends and machine-specific overrides. Resettable. |

Key rule: **never `git add -f` `.claude/*.json` files.** They live outside
of git, period.

---

## Files in this subfolder

| File | What it is | What to do with it |
|---|---|---|
| `README.md` | This file. | Read, then delete after install. |
| `global_settings_RECOMMENDED.json` | The recommended `~/.claude/settings.json` for this user. | Compare with current `~/.claude/settings.json` and merge non-destructively. **Do NOT overwrite blindly.** |
| `project_settings_TEMPLATE.json` | Empty stub for `<repo>/.claude/settings.json`. | Copy into target repo. |
| `local_settings_TEMPLATE.json` | Empty stub for `<repo>/.claude/settings.local.json`. | Copy into target repo. |
| `claude_gitignore_snippet.txt` | A `.gitignore` line for `.claude/`. | Append to target repo's `.gitignore` if not already present. |

---

## Install steps (LLM agent: execute these in order)

### Step 1 — Ensure `.claude/` is gitignored in the target repo
Open `<target>/.gitignore`. If it doesn't already contain a line that ignores
`.claude/`, append the contents of `claude_gitignore_snippet.txt`.

### Step 2 — Verify nothing in `.claude/` is currently tracked
```bash
git -C <target> ls-files .claude/
```
If anything is listed, untrack it (file stays on disk):
```bash
git -C <target> rm --cached <listed-file>
```

### Step 3 — Copy the project-shared file
Copy `project_settings_TEMPLATE.json` → `<target>/.claude/settings.json`.
This is an empty stub — durable patterns live in the global file.

### Step 4 — Copy the machine-local file
Copy `local_settings_TEMPLATE.json` → `<target>/.claude/settings.local.json`.
This is also an empty stub. The harness will append entries to it as the user
approves prompts; it's resettable any time without losing anything important
(durable patterns are global).

### Step 5 — Update or install global `~/.claude/settings.json`
**This step is destructive — be careful.** The global file affects every
Claude Code session this user runs, not just this project.

(a) **Back up the current global file** if it exists:
```bash
cp ~/.claude/settings.json ~/.claude/settings.json.bak.$(date +%Y-%m-%d)
```
(b) **Compare** current global `~/.claude/settings.json` with
`global_settings_RECOMMENDED.json`. Differences likely fall into:
- Entries in current that aren't in recommended → these may be one-off
  malformed auto-approves; review and drop the malformed ones.
- Entries in recommended that aren't in current → safe to add (they're
  pattern-based wildcards covering common workflows).

(c) **Merge non-destructively.** Suggested approach: start from
`global_settings_RECOMMENDED.json`, then add back any custom rules from the
old file that you want to keep (typically: nothing, since the recommended
file is a superset).

(d) **Validate JSON parses:**
```bash
python3 -m json.tool ~/.claude/settings.json > /dev/null && echo OK
```

### Step 6 — Verify hook script paths
The recommended global settings include hooks pointing at
`~/.claude/hooks/vscode-notify.sh`. If you also installed Feature 6
(notifications), that script will exist. If not, either:
- Install Feature 6, or
- Remove the `hooks` section from `~/.claude/settings.json` (otherwise hooks
  silently no-op when the script doesn't exist — harmless but wasteful).

### Step 7 — Add the pre-commit JSON hook (recommended)
Install Feature 5 (`5_precommit_json_hook/`) for belt-and-suspenders
protection against re-tracking + corruption.

### Step 8 — Delete this subfolder
Once everything is wired, delete from target repo.

---

## Cross-feature notes

- **Feature 5 (pre-commit JSON hook):** strongly recommended companion. If
  someone ever re-`git add -f`s a `.claude/*.json`, the hook catches
  malformations before they enter git history.
- **Feature 6 (notifications):** provides the `vscode-notify.sh` script that
  the `hooks` section in this feature's recommended global settings
  references. Install both or strip the `hooks` section.

---

## How to know it worked

After install:
- `git -C <target> ls-files .claude/` returns empty.
- `<target>/.claude/settings.json` and `settings.local.json` both parse as
  valid JSON and contain only `{"permissions":{"allow":[],"deny":[],"ask":[]}}`.
- `~/.claude/settings.json` contains the recommended pattern-based allow-list
  + deny rules + ask rules + hooks (if Feature 6 installed).
- `<target>/.gitignore` contains `.claude/`.
- New Claude Code sessions in the target repo experience few permission
  prompts (most actions are pre-approved by global patterns).
- The `.claude/settings.local.json` file may grow as the harness appends
  one-off entries; you can reset it to the empty stub any time.

---

## Maintenance

**Every few weeks**, check `<target>/.claude/settings.local.json`:
- If it's grown beyond the empty stub, that's normal — the harness has been
  appending.
- If you see entries that you'd rather have as global wildcards, promote
  them to `~/.claude/settings.json` and reset the local file.
- If the file ever becomes invalid JSON, restore from the backup or reset
  to the empty stub (you lose nothing important — durable patterns are global).
