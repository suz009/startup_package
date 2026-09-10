# Feature 3: Folder Structure + Naming Conventions

**Audience:** an LLM agent (or a human) installing this feature into a new repo.

**What this feature gives the new repo:** a portable scaffold of high-level
directory and file-naming conventions that have proven useful in the parent
repo. The conventions are about *structure* and *ordering*, not about
specific pipeline content — new repos have wildly different subject matter
and stage counts, but the same skeleton and rules apply.

**When to skip this feature:** repos that don't have a "data flowing through
stages" shape (e.g. a thin GUI, a documentation site, a one-off script
collection). The conventions still apply at the top level (numeric prefixes,
context dir, README at root) but the timestamp + stage-prefix rules become
overhead.

---

## What this feature defines

1. **Numeric-prefix top-level dirs.** `0_context/`, `1_data/`, `2_scripts/`,
   `3_analysis/`, `4_…` etc. Numeric prefixes force a deterministic listing
   order in any tool that sorts alphabetically. `0_` is reserved for
   non-output context (configs, protocols, background, session summaries).
2. **Stage-prefix script naming.** Pipeline scripts are named with their
   stage number first: `1a_retrieve_openalex.py`, `3_map_to_canonical_schema.py`,
   `8b_calculate_topicality_indicators.py`. Sub-stages use letter suffixes
   (`a`, `b`, `c`). This makes `ls 2_scripts/` print scripts in pipeline
   order regardless of alphabetic name.
3. **Timestamped output dirs.** Every pipeline run writes its outputs into
   `1_data/{stage}/{YYYY-MM-DD_HHMM}/`. Old runs are preserved, never
   overwritten. Manual review work attached to a run survives because it's
   tied to that timestamp.
4. **`0_context/config/`** for project configuration files (query specs,
   schema specs, parameter YAMLs).
5. **`0_context/background/`** for reference materials (PDFs, source
   tutorials, background reading). Typically gitignored to avoid bloat.
6. **`README_project.md`** at repo root: a project-overview README in a
   distinctive name so it's not confused with subdirectory READMEs (e.g.
   `0_context/protocol/README_protocol.md`).
7. **`requirements.txt`** (or equivalent) at repo root: dependency manifest.
   Use whatever is canonical for your language (Python: `requirements.txt`
   or `pyproject.toml`; R: `renv.lock`; Node: `package.json`).
8. **`.gitignore`** with patterns for ignoring large data files but tracking
   metadata + reports.
9. **Git LFS** setup via `.gitattributes` for tracking large binary/data
   files in git without bloating regular git history.

---

## Files in this subfolder

| Path | What it is | What to do with it |
|---|---|---|
| `README.md` | This file. | Read, then delete after install. |
| `naming_conventions.md` | Authoritative spec for the rules above. | Copy into target repo as `0_context/protocol/naming_conventions.md` (or similar). |
| `canonical_tree/` | Empty directory tree (`0_context/`, `1_data/`, `2_scripts/`, `3_analysis/`) with `.gitkeep` files. | Copy contents into target repo root. |
| `gitignore_TEMPLATE` | A `.gitignore` with the data-file patterns. | Copy into target repo as `.gitignore` and adapt stage paths. |
| `gitattributes_TEMPLATE` | A `.gitattributes` for Git LFS. | Copy into target repo as `.gitattributes` and run install steps. |
| `README_project_TEMPLATE.md` | A project README skeleton. | Copy into target repo as `README_project.md` and fill in. |
| `requirements_TEMPLATE.txt` | An empty Python requirements file with comment header. | Copy into target repo as `requirements.txt` (or replace with your language's manifest). |

---

## Install steps (LLM agent: execute these in order)

### Step 1 — Copy the canonical tree
```bash
cp -r canonical_tree/. <target>/
```
This creates `0_context/`, `1_data/`, `2_scripts/`, `3_analysis/` with
`.gitkeep` files so empty dirs are tracked by git.

### Step 2 — Copy and adapt `.gitignore`
- Copy `gitignore_TEMPLATE` → `<target>/.gitignore`.
- Open it and adjust the per-stage data-file patterns to match the new
  repo's actual stage names. The template includes generic placeholders;
  add or remove `1_data/<stage>/...` blocks as needed.

### Step 3 — Set up Git LFS
- Copy `gitattributes_TEMPLATE` → `<target>/.gitattributes`.
- Adjust patterns to match the new repo's actual file types and locations.
- From the target repo root:
  ```bash
  git lfs install        # one-time per machine
  git add .gitattributes
  git commit -m "Add Git LFS configuration"
  ```
- For new file types added later: `git lfs track "*.parquet"` (or whatever).

### Step 4 — Copy the project README
- Copy `README_project_TEMPLATE.md` → `<target>/README_project.md`.
- Fill in: project name, one-paragraph overview, repo structure summary,
  quick start, dependencies.

### Step 5 — Copy the requirements manifest
- Copy `requirements_TEMPLATE.txt` → `<target>/requirements.txt`.
- (Or replace with the appropriate manifest for your language.)

### Step 6 — Copy the naming conventions spec
- Copy `naming_conventions.md` → `<target>/0_context/protocol/naming_conventions.md`.
- This becomes the authoritative reference for any future contributor (or
  LLM session) about how to name new scripts and where to put output.

### Step 7 — Add to LLM operating instructions
Add to the new repo's `CLAUDE.md`:
```
Follow `0_context/protocol/naming_conventions.md` for all new files
and directories. New scripts must be stage-prefixed; new pipeline
output dirs must be timestamped (YYYY-MM-DD_HHMM).
```

### Step 8 — Delete this subfolder
Once installed, delete from target.

---

## Cross-feature notes

- **Features 1, 2, 4, 5, 6** all reference `0_context/` paths. If you skip
  Feature 3, you must still create at least `0_context/` (or change those
  features' paths).
- This feature is **structurally agnostic to project subject**. It works
  for bibliometric pipelines, ML training pipelines, data ETL projects,
  even purely qualitative analysis projects. The `1_data/`, `2_scripts/`,
  `3_analysis/` triad maps onto almost any data-driven project.
- For repos that don't have a "pipeline" shape (e.g. a GUI, a documentation
  site), only the *high-level* conventions apply: numeric-prefix top-level
  dirs, `0_context/` reservation, README at root. The stage-prefix and
  timestamp rules are pipeline-specific and can be skipped.

---

## How to know it worked

After install, the new repo should:
- Have `0_context/`, `1_data/`, `2_scripts/`, `3_analysis/` at root.
- Have `.gitignore` excluding bulky data files but tracking `*.md`, `*.txt`,
  metadata JSON.
- Have `.gitattributes` configured for Git LFS on the relevant binary/data
  patterns.
- Have `README_project.md` and `requirements.txt` at root.
- Have `0_context/protocol/naming_conventions.md` as the authoritative
  rule reference.
- The first time the LLM creates a new pipeline script or output dir,
  it follows the naming/structure rules without prompting.
