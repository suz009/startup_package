# [Project Name]

[One-paragraph project overview. What is this repo for? Who is the audience?
What's the deliverable?]

---

## Repository Structure

```
0_context/                 Project context (protocols, configs, session summaries, background)
├── protocol/              Methodology + process protocols
├── session_summaries/     Per-day operational logs
├── config/                Project configuration files (queries, schemas)
└── background/            Reference materials (PDFs, tutorials)

1_data/                    Pipeline data outputs
├── 1_<stage_name>/
│   └── {YYYY-MM-DD_HHMM}/   timestamped run outputs
├── 2_<stage_name>/
└── ...

2_scripts/                 All executable scripts
├── 1_<stage_name>/
│   ├── 1a_<script_name>.py
│   └── 1b_<script_name>.py
└── ...

3_analysis/                Reports, visualizations, derived analyses
└── {stage_name}/{YYYY-MM-DD_HHMM}/

README_project.md          (this file)
requirements.txt           Dependency manifest
.gitignore                 Git ignore patterns
.gitattributes             Git LFS configuration
```

See `0_context/protocol/naming_conventions.md` for the authoritative spec.

---

## Quick Start

### 1. Clone and install dependencies
```bash
git clone <repo-url>
cd <repo-name>
git lfs install            # one-time per machine
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure
- Copy `.env.example` → `.env` and fill in API keys / credentials.
- Adjust `0_context/config/*.yaml` for your specific run.

### 3. Run the pipeline
```bash
python 2_scripts/run_pipeline.py
# Or run a single stage:
python 2_scripts/1_<stage_name>/1a_<script_name>.py
```

---

## Documentation

- **Pipeline execution:** [`PIPELINE_EXECUTION_GUIDE.md`](PIPELINE_EXECUTION_GUIDE.md)
  (create if needed)
- **Methodology decisions:** [`0_context/protocol/decision_log.json`](0_context/protocol/decision_log.json)
- **Change history:** [`0_context/protocol/CHANGELOG.md`](0_context/protocol/CHANGELOG.md)
- **Naming conventions:** [`0_context/protocol/naming_conventions.md`](0_context/protocol/naming_conventions.md)

---

## Dependencies

- Python 3.10+
- See `requirements.txt`
- API keys (if any): document them and the env vars they go in

---

## License

[Add license information]

---

## Contact

[Maintainer contact info]
