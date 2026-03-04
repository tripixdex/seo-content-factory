# SEO Content Automation Factory

Local-first SEO content generation demo with FastAPI + simple browser UI.

## 30-Second Overview
- Input: one HTML file or a batch CSV of HTML sources.
- Run: `make up OPEN_UI=1` (or `OPEN_UI=0` in CI/headless).
- Result: markdown page, SEO metadata JSON, quality report JSON, plus batch summary CSV.
- Mode: offline-first (`NO_LLM_MODE=true`, `OFFLINE_MODE=true` in `make` flows).

## Quickstart
1. Setup environment:
   - `make setup`
2. Start demo stack (reliable one-command run):
   - `make up OPEN_UI=1`
3. Open UI manually (if needed):
   - `http://127.0.0.1:8000/ui`
4. Run tests:
   - `make test`
5. Stop services:
   - `make down`

## What The Project Outputs
- Single run writes:
  - `outputs/<run_id>/<job_id>/page.md`
  - `outputs/<run_id>/<job_id>/meta.json`
  - `outputs/<run_id>/<job_id>/quality_report.json`
- Batch run also writes:
  - `outputs/<run_id>/summary.csv`

## API Basics
- `POST /run-one` supports both:
  - `source_path` (must be under `fixtures/` or `inputs/`)
  - `html_content` + optional `source_filename` (saved under `inputs/uploads/<run_id>/`)
- `POST /run-batch` supports both:
  - `csv_path` (must be under `fixtures/` or `inputs/`)
  - `csv_content` + optional `csv_filename` (saved under `inputs/uploads/<run_id>/`)
- Optional for both: `output_dir`; if empty or omitted, default is `OUTPUT_DIR` (default `outputs`).

## Useful Commands
- `make format`
- `make lint`
- `make test`
- `make up OPEN_UI=0`
- `make down`
