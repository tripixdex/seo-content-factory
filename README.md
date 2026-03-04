# SEO Content Automation Factory

FastAPI + local UI MVP for deterministic SEO draft generation from local HTML inputs.

## 30-Second Overview
- Converts single HTML pages or batch CSV inputs into deterministic SEO draft artifacts.
- Gives non-technical reviewers a UI-first flow with clear pass/fail quality signals.
- Stays offline-first and deterministic for repeatable demos and portfolio credibility.

## Demo In 60 Seconds
```bash
make setup
make up OPEN_UI=1
```
What you will see:
1. Browser opens `http://127.0.0.1:8000/ui`.
2. In `Single Run`, upload `fixtures/pages/demo_a.html`, click `Run Single`.
3. In `Batch CSV`, upload `fixtures/demo_batch.csv`, click `Run Batch`.
4. Result panel shows `status`, `quality_score`, `passed`, and key output paths.
5. Artifacts appear under `outputs/<run_id>/...`.

Stop:
```bash
make down
```

## Inputs / Outputs
Inputs:
- Single API/UI: local `source_path` or uploaded `html_content` + `source_filename`
- Batch API/UI: `csv_path` or `csv_content` + `csv_filename`
- Optional: `output_dir` (must stay inside `outputs/`; defaults to `OUTPUT_DIR`, default `outputs`)
- Size limits: `html_content` and `csv_content` are each limited to `1,000,000` bytes

Produced artifacts:
- `outputs/<run_id>/<job_id>/page.md`
- `outputs/<run_id>/<job_id>/meta.json`
- `outputs/<run_id>/<job_id>/quality_report.json`
- `outputs/<run_id>/summary.csv` (batch)

## Architecture In 8 Lines
1. `src/seo_factory/api/app.py`: FastAPI endpoints and request validation.
2. `src/seo_factory/api/ui_page.py`: plain HTML/CSS/JS UI served by FastAPI.
3. `src/seo_factory/pipeline/orchestrator.py`: single-job execution path.
4. `src/seo_factory/pipeline/batch_runner.py`: deterministic CSV row execution.
5. `src/seo_factory/generators/template.py`: markdown + meta generation.
6. `src/seo_factory/quality/rules.py`: quality checks and pass/fail scoring.
7. `src/seo_factory/storage/fs.py`: artifact persistence + summary writing.
8. Flow: UI/API input -> validated spec -> pipeline -> quality -> filesystem outputs.

## Safety Notes
- Offline-first: `make up` starts API with `NO_LLM_MODE=true OFFLINE_MODE=true`.
- Path restrictions: source file paths must remain inside `fixtures/` or `inputs/`.
- ID restrictions: `run_id` and `job_id` allow only `[A-Za-z0-9._-]` and reject `..`, `/`, `\`.
- Output restrictions: `output_dir` must resolve inside `outputs/`.
- Uploaded UI files are staged under `inputs/uploads/<run_id>/`.

## Batch Semantics
- If all rows succeed: API returns `status=success`, `passed=true`.
- If any row fails: API returns `status=partial_success`, `passed=false`.
- Batch `quality_score` is the average of per-row scores from `summary.csv`; failed rows contribute `0.0`.
- Unexpected systemic batch failures return HTTP `500`.

## n8n Integration
Start local API + n8n:
```bash
make up N8N=1 OPEN_UI=0
```
Import workflow:
1. Open n8n.
2. Import `workflows/n8n/seo_factory_demo.json`.
3. Run workflow with valid `/run-one` or `/run-batch` payload fields.

Expected result:
- HTTP node returns `status=success`.
- Output paths point to generated local artifacts under `outputs/`.

Stop everything:
```bash
make down
make n8n-down
```

## Screenshot Placeholders
- UI Single Run: `docs/screenshots/ui-single-run.png` (placeholder)
- UI Batch Run: `docs/screenshots/ui-batch-run.png` (placeholder)
- n8n Success: `docs/screenshots/n8n-success.png` (placeholder)
