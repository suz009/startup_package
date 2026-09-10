# Naming Conventions

Authoritative spec for directory and file naming in this repo. Adapted from
the parent repo's startup package, Feature 3.

---

## 1. Top-level directories

Use **numeric prefixes** so directories sort in conceptual order in any
alphabetic listing tool.

| Dir | Purpose |
|---|---|
| `0_context/` | Non-output project context: protocols, configs, session summaries, background. |
| `1_data/` | Outputs of pipeline data stages (raw retrieval, cleaning, merging, dedup, etc.). |
| `2_scripts/` | All executable scripts. |
| `3_analysis/` | Reports, visualizations, derived analyses (HTML, PDF, notebooks). |
| `4_…` etc. | Add as needed for stages beyond analysis (e.g. `4_export/`, `4_publication/`). |

`0_` is reserved for context and metadata — content that **describes** the
project rather than being a project output.

---

## 2. Subdirectories of `0_context/`

| Subdir | Purpose |
|---|---|
| `0_context/protocol/` | Methodology and process protocols (decision protocol, session summary protocol, naming conventions, etc.). Plus `decision_log.json`, `CHANGELOG.md`, version archives. |
| `0_context/session_summaries/` | One markdown file per working session (`SESSION_SUMMARY_YYYY-MM-DD.md`). |
| `0_context/config/` | Project configuration: query specs, schema specs, parameter YAMLs. |
| `0_context/background/` | Reference materials (PDFs, source tutorials, background reading). Typically gitignored. |
| `0_context/archive/` | Deprecated documents kept for historical reference. |

---

## 3. Pipeline stage numbering

Pipeline stages get integer numbers starting at 1. Stages live in parallel
under `1_data/`, `2_scripts/`, `3_analysis/`:

```
1_data/1_database_api_retrieval/
2_scripts/1_database_api_retrieval/
3_analysis/1_database_api_retrieval/   (if applicable)
```

The number AND the name of the stage must match across the three top-level
dirs. Renaming a stage means updating all three.

---

## 4. Script naming

Inside `2_scripts/{stage_number}_{stage_name}/`, scripts are named:

```
{stage_number}{sub_stage_letter}_{descriptive_name}.{ext}
```

**Examples:**
- `1a_retrieve_openalex.py`
- `1b_retrieve_scopus.py`
- `3_map_to_canonical_schema.py`        (no sub-stage when the stage has only one script)
- `8b_calculate_topicality_indicators.py`
- `8d_strategy_a_or.py`

**Why:** `ls` prints them in pipeline-execution order without further effort.

**Sub-stage letters** (`a`, `b`, `c`, …) are used when a stage has multiple
related sub-steps that run in order. Skip sub-stage letters if the stage
has only one script.

**Numeric sub-stages** (`1a`, `1b`, ..., `1g`, then `1a2`, `1b2`) are
discouraged but acceptable when alphabet runs out (rare).

---

## 5. Timestamped output directories

Every pipeline run that produces non-trivial output writes into a
timestamped subdirectory:

```
1_data/{stage_number}_{stage_name}/{YYYY-MM-DD_HHMM}/
3_analysis/{stage_number}_{stage_name}/{YYYY-MM-DD_HHMM}/
```

**Format:** `YYYY-MM-DD_HHMM` (e.g. `2026-04-22_1625`). 24-hour clock,
local time, no seconds.

**Examples:**
- `1_data/8_corpus_definition/2026-04-10_1906/8a_work_records.csv`
- `3_analysis/8_corpus_definition/2026-04-10_1906/8d_strategy_a_comparison.html`

**Rationale:**
- Old runs are preserved, never overwritten.
- Manual review work attached to a run survives because it's tied to that
  timestamp.
- The timestamp format sorts correctly alphabetically.

**Files within a timestamped dir** use the script's stage prefix:
`8a_work_records.csv`, `8b_topicality_indicators.csv` — same prefix as the
script that produced them.

---

## 6. Session summary files

Format: `SESSION_SUMMARY_YYYY-MM-DD.md`

Multiple sessions in one day: append a suffix:
- `SESSION_SUMMARY_YYYY-MM-DD_afternoon.md`
- `SESSION_SUMMARY_YYYY-MM-DD_continuation.md`

Location: `0_context/session_summaries/`.

---

## 7. Decision documents

- Decision log: `0_context/protocol/decision_log.json` (JSON, machine-readable)
- Changelog: `0_context/protocol/CHANGELOG.md` (markdown, human-readable)
- Standalone decision docs (optional): `0_context/protocol/DEC-XXX_Brief_Description.md`
- Protocol versions: `0_context/protocol/protocol.md` (current),
  `0_context/protocol/versions/protocol_vX.Y.md` (archived)

Decision IDs: `DEC-` plus zero-padded 3-digit number (`DEC-001`, `DEC-042`).

---

## 8. Project-level files (repo root)

| File | Purpose |
|---|---|
| `README_project.md` | Project overview README. (Distinctively named to avoid confusion with subdirectory READMEs.) |
| `requirements.txt` | Python dependency manifest (or `pyproject.toml`, `renv.lock`, etc.). |
| `.gitignore` | Git ignore patterns (data files, venvs, secrets). |
| `.gitattributes` | Git LFS configuration for large files. |
| `.env` | Environment variables (gitignored). |

Sub-directory READMEs use distinctive names too: `0_context/protocol/README_protocol.md`,
not `README.md`. This avoids ambiguity in path references.

---

## 9. Configuration files

Live in `0_context/config/`. Use YAML (`.yaml`) for structured config when
human editing is expected; JSON when machine-only.

Naming: descriptive snake_case. Versioned configs use a version suffix:
`query_canonical.yaml` (current), historic versions stored inline as
`query_canonical_v1.0.yaml` if needed.

---

## 10. Quick reference

- **Numeric prefixes** for top-level dirs, pipeline stages, scripts.
- **Letter sub-prefixes** for sub-stages within a stage.
- **`YYYY-MM-DD_HHMM`** for timestamped output dirs.
- **`SESSION_SUMMARY_YYYY-MM-DD.md`** for session summaries.
- **`DEC-XXX`** for decision IDs.
- **Distinctive READMEs** at every level (`README_project.md`, `README_protocol.md`).
- **Match stage names** across `1_data/`, `2_scripts/`, `3_analysis/`.
