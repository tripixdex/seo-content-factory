# Contracts

## API Input Contracts

### `POST /run-one`
- Required:
  - `keyword` (string, non-empty)
  - `job_id` (string, non-empty)
  - `run_id` (string, non-empty)
- Source variants:
  - `source_path` (must resolve under `fixtures/` or `inputs/`)
  - `html_content` with optional `source_filename` (`.html`/`.htm`)
- Priority:
  - If both are provided, `html_content` path is used.
- Optional:
  - `output_dir` (string path). Empty or missing falls back to `OUTPUT_DIR` (default `outputs`).

### `POST /run-batch`
- Required:
  - `run_id` (string, non-empty)
- Source variants:
  - `csv_path` (must resolve under `fixtures/` or `inputs/`)
  - `csv_content` with optional `csv_filename` (`.csv`)
- Optional:
  - `output_dir` (same fallback behavior as `/run-one`).

## API Output Contracts

### Shared Success Fields
- `status` (`"success"`)
- `quality_score` (number)
- `passed` (boolean)
- `output_paths` (object with key file/dir paths)
- `hashes` (object of deterministic hashes for key artifacts)

### `/run-one` Output Paths
- `job_dir`
- `page`
- `meta`
- `quality`

### `/run-batch` Output Paths
- `run_dir`
- `summary_csv`

## UI Contract
- `GET /` redirects (`307`) to `/ui`.
- `GET /ui` returns `text/html`.
- UI includes two modes:
  - Single HTML run (calls `/run-one`)
  - Batch CSV upload (calls `/run-batch`)
- UI shows status, quality score, pass/fail, and output paths, plus error box for failed requests.

## Filesystem Contract
- Default output root: `OUTPUT_DIR` env var, default `outputs/`.
- Single run artifacts:
  - `outputs/<run_id>/<job_id>/page.md`
  - `outputs/<run_id>/<job_id>/meta.json`
  - `outputs/<run_id>/<job_id>/quality_report.json`
- Batch summary:
  - `outputs/<run_id>/summary.csv`
- Uploaded UI files are staged locally:
  - `inputs/uploads/<run_id>/...`
