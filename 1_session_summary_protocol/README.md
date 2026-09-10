# Feature 1: Session Summary Protocol

**Audience:** an LLM agent (or a human) installing this feature into a new repo.

**What this feature gives the new repo:** a per-day operational log (one
markdown file per session) that the LLM updates silently as work progresses.
The log captures *all* work — exploration, blockers, partial results, plans —
not just finalized decisions. Cross-session continuity comes for free: a fresh
LLM session can pick up where the prior one left off by reading the latest
summary file.

This is **distinct from** the decision protocol (Feature 2). Session summaries
log everything; decision logs capture only finalized methodological decisions
needed for replication.

---

## Files in this subfolder

| File | What it is | What to do with it |
|---|---|---|
| `README.md` | This file. | Read, then delete after install. |
| `SESSION_SUMMARY_PROTOCOL.md` | The protocol itself: when to create summaries, when to update, structure to use. | Copy into the target repo. |
| `session_summary_TEMPLATE.md` | A blank session summary you can copy/rename for each new session. | Copy into the target repo. |

---

## Install steps (LLM agent: execute these in order)

### Step 1 — Decide where the protocol lives
Recommended location: **`0_context/protocol/SESSION_SUMMARY_PROTOCOL.md`**
inside the target repo (matches the parent repo's convention if Feature 3 is
also installed). If the target repo uses a different top-level layout, pick
any analogous "context" or "docs" directory.

### Step 2 — Decide where session summaries live
Recommended location: **`0_context/session_summaries/`** inside the target
repo. Create the directory now.

### Step 3 — Copy files
- Copy `SESSION_SUMMARY_PROTOCOL.md` → `<target>/0_context/protocol/SESSION_SUMMARY_PROTOCOL.md`
- Copy `session_summary_TEMPLATE.md` → `<target>/0_context/session_summaries/_TEMPLATE.md`
  (Underscore prefix keeps it sorted to the top and signals it's not a real session.)

### Step 4 — Update the protocol's directory references if needed
The protocol document references `0_context/session_summaries/` as the default
location. If you chose a different location in Step 2, search-and-replace
those paths inside `SESSION_SUMMARY_PROTOCOL.md` so the protocol matches
where files actually live.

### Step 5 — Wire the protocol into LLM operating instructions
The LLM agent in the new repo needs to know to follow this protocol. Two
ways:

(a) **CLAUDE.md (preferred for Claude Code).** Add a line to the new repo's
    `CLAUDE.md` (create one at repo root if it doesn't exist):
    ```
    Follow `0_context/protocol/SESSION_SUMMARY_PROTOCOL.md` for all sessions.
    ```
(b) **Project memory.** Add a memory entry in `~/.claude/projects/<this-repo>/memory/`
    pointing at the protocol file.

### Step 6 — Create the first session summary
On the first session of the new repo, copy `_TEMPLATE.md` →
`SESSION_SUMMARY_YYYY-MM-DD.md` (today's ISO date) and start filling it in.
This validates the install.

### Step 7 — Delete this subfolder
Once the protocol and template are copied into the target repo, delete this
subfolder from the target repo. (Keep the source copy in the parent repo for
future scaffolding.)

---

## Cross-feature notes

- **Feature 2 (decision protocol):** `SESSION_SUMMARY_PROTOCOL.md` references
  the decision protocol in its "Integration with Decision Protocol" section.
  If Feature 2 is NOT installed, edit that section to remove the cross-references
  (or install Feature 2 too — they pair well).
- **Feature 3 (folder structure):** This feature assumes a `0_context/`
  top-level dir. If Feature 3 is installed first or in parallel, you'll have
  it; otherwise create just the directories this feature needs.

---

## How to know it worked

After install, every new working session should produce a file named
`SESSION_SUMMARY_YYYY-MM-DD.md` in `0_context/session_summaries/` that gets
updated silently as work progresses, and reaches a final `✅ CLOSED` status
when the session ends. New LLM sessions should be able to read the most
recent summary and resume seamlessly.
