# Feature 2: Substantive Decision Protocol

**Audience:** an LLM agent (or a human) installing this feature into a new repo.

**What this feature gives the new repo:** a versioned, replication-ready
record of *substantive* methodological decisions. Each decision gets a unique
ID (DEC-XXX), a JSON log entry, and a CHANGELOG line. Designed to satisfy
peer-review standards (PRISMA-S, BIBLIO) and let an outside reader reconstruct
exactly *why* the project's methodology evolved.

This is **distinct from** session summaries (Feature 1). Session summaries
log everything that happens; this protocol logs only finalized methodological
decisions.

---

## What counts as a "substantive" decision?

A change that affects:
- **Data collection scope or methods** (inclusion/exclusion criteria, search
  terms, queries, extraction fields)
- **Reproducibility or validity** (validation thresholds, analysis methods,
  QA procedures)
- **Protocol deviations** (solutions to unforeseen problems, adaptations
  based on findings)

**Not substantive** (don't log):
- Typo fixes
- Formatting
- Clarifications without meaning changes
- Reorganization without content changes

---

## Files in this subfolder

| File | What it is | What to do with it |
|---|---|---|
| `README.md` | This file. | Read, then delete after install. |
| `SUBSTANTIVE_DECISION_LOGGING_PROTOCOL.md` | The protocol document. | Copy into the target repo. |
| `decision_log_TEMPLATE.json` | Empty scaffold for the machine-readable decision log. | Copy into the target repo, rename to `decision_log.json`, fill in `project` field. |
| `CHANGELOG_TEMPLATE.md` | Empty scaffold for the human-readable changelog. | Copy into the target repo, rename to `CHANGELOG.md`. |

---

## Install steps (LLM agent: execute these in order)

### Step 1 — Create the protocol directory
Recommended location: **`0_context/protocol/`** inside the target repo.

### Step 2 — Copy files
- `SUBSTANTIVE_DECISION_LOGGING_PROTOCOL.md` → `<target>/0_context/protocol/SUBSTANTIVE_DECISION_LOGGING_PROTOCOL.md`
- `decision_log_TEMPLATE.json` → `<target>/0_context/protocol/decision_log.json`
- `CHANGELOG_TEMPLATE.md` → `<target>/0_context/protocol/CHANGELOG.md`

### Step 3 — Fill in project metadata
Open `<target>/0_context/protocol/decision_log.json` and replace placeholders:
- `metadata.project`: the new project's name
- `metadata.created`: today's date in ISO 8601 with timezone
  (e.g. `2026-04-23T00:00:00Z`)
- `metadata.last_updated`: same as `created` for now

Open `<target>/0_context/protocol/CHANGELOG.md` and replace `[PROJECT_NAME]`
with the new project's name; replace the placeholder date in the `[1.0]`
entry with today's date.

### Step 4 — Create a baseline protocol document (project-specific)
Decision logging only makes sense if there's an actual *methodology protocol*
that the decisions are deviations from. Create:
- `<target>/0_context/protocol/protocol.md` — your project's living methodology
  document. Even a stub at v1.0 is fine. It will grow as the project evolves.
- `<target>/0_context/protocol/protocol_v1.0.md` — copy of the same file at
  baseline. **Never modify this.** It's the frozen reference.
- `<target>/0_context/protocol/versions/` — empty directory. Past versions
  of `protocol.md` get archived here when the version increments.

### Step 5 — Wire the protocol into LLM operating instructions
Add to the new repo's `CLAUDE.md` (create at repo root if missing):
```
Follow `0_context/protocol/SUBSTANTIVE_DECISION_LOGGING_PROTOCOL.md`
for all methodological decisions. Watch for the "SUBSTANTIVE" flag and
proactively prompt to log decisions that meet the criteria.
```

### Step 6 — Delete this subfolder
Once protocol files are copied into the target repo, delete this subfolder
from the target.

---

## Decision-logging workflow (summary)

When a substantive decision is being made (or has just been made):

1. Generate the next decision ID by reading `decision_log.json` and
   incrementing `metadata.total_decisions`. ID format: `DEC-` plus
   zero-padded 3-digit number (e.g. `DEC-007`).
2. Append a new entry to `decisions[]` matching the schema in the protocol
   document (required fields: `id`, `timestamp`, `stage`, `trigger`,
   `options_considered`, `decision`, `rationale`, `protocol_impact`).
3. Bump `metadata.protocol_current_version`, `metadata.last_updated`,
   `metadata.total_decisions`.
4. Add a corresponding entry at the top of `CHANGELOG.md` under the new
   version number, following [Keep a Changelog](https://keepachangelog.com/)
   format (`### Added` / `### Changed` / `### Removed` etc.).
5. **Archive the old protocol version** before editing it: copy
   `protocol.md` → `versions/protocol_v<OLD_VERSION>.md`.
6. Update `protocol.md`: bump version, update "Last Updated", modify the
   sections listed in `decision.protocol_impact.sections_modified`,
   reference the new DEC-XXX where appropriate.
7. (Optional but recommended for major decisions) Create a standalone
   `DEC-XXX_Brief_Description.md` document with a deeper write-up.

The session summary (Feature 1) should also note the decision was logged.

---

## Cross-feature notes

- **Feature 1 (session summary protocol):** session summaries log decisions
  too, but at a different granularity (everything that happens, not just
  finalized methodology). Both should be installed together for full
  coverage. If Feature 1 is NOT installed, the LLM still needs some way to
  remember session-to-session what the latest version is and which decisions
  are pending.
- **Feature 3 (folder structure):** assumes `0_context/` exists. If
  Feature 3 isn't installed, create just the directories this feature needs.

---

## How to know it worked

After install, the new repo should:
- Have `0_context/protocol/decision_log.json` with `metadata.total_decisions: 0`
  and an empty `decisions: []`.
- Have `0_context/protocol/CHANGELOG.md` with a single `[1.0]` entry.
- Have `0_context/protocol/protocol.md` and `protocol_v1.0.md` (identical
  copies at the start).
- The first time a substantive decision is made, the LLM proactively offers
  to log it as `DEC-001`, the version increments to `1.1`, and all four
  files (decision_log.json, CHANGELOG.md, protocol.md, versions/protocol_v1.0.md)
  reflect the change consistently.
