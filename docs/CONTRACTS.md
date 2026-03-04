# Contracts

## API Input Contracts

### `POST /run-one`
- Required:
  - `keyword` (string, non-empty)
  - `job_id` (string, non-empty, allowed chars `[A-Za-z0-9._-]`, no `..`, `/`, `\`)
  - `run_id` (string, non-empty, allowed chars `[A-Za-z0-9._-]`, no `..`, `/`, `\`)
- Source variants:
  - `source_path` (must canonically resolve under `fixtures/` or `inputs/`)
  - `html_content` with optional `source_filename` (`.html`/`.htm`, max 1,000,000 bytes)
- Priority:
  - If both are provided, `html_content` path is used.
- Optional:
  - `output_dir` (string path). Must canonically resolve inside `outputs/`. Empty or missing falls back to `OUTPUT_DIR` (default `outputs`).

### `POST /run-batch`
- Required:
  - `run_id` (string, non-empty, allowed chars `[A-Za-z0-9._-]`, no `..`, `/`, `\`)
- Source variants:
  - `csv_path` (must canonically resolve under `fixtures/` or `inputs/`)
  - `csv_content` with optional `csv_filename` (`.csv`, max 1,000,000 bytes)
- Optional:
  - `output_dir` (same fallback behavior and `outputs/` restriction as `/run-one`).
- Batch row policy:
  - Each row must include `job_id`, `source_path`, and `target_keyword`.
  - Row `job_id` follows the same ID constraints as above.
  - Row `source_path` must canonically resolve under `fixtures/` or `inputs/`.
- Invalid rows are marked `failed` in `summary.csv`; request returns `200` with `status="partial_success"` and `passed=false` if any row fails.

## API Error Semantics
- `422 Unprocessable Entity`: JSON/schema validation errors (missing required fields, wrong types).
- `400 Bad Request`: business-rule validation errors (forbidden source paths, invalid IDs, missing source variant).
- `413 Payload Too Large`: `html_content` or `csv_content` exceeds 1,000,000 bytes.
- `500 Internal Server Error`: unexpected internal failures.

## API Output Contracts

### Shared Success Fields
- `status` (`"success"` or `"partial_success"` for batch partial failures)
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

### `/run-batch` Aggregate Score Policy
- `quality_score` is computed as the average of row `quality_score` values read from `summary.csv`.
- Failed rows contribute `0.0` to this aggregate.
- If an unexpected systemic exception occurs during batch processing, endpoint returns HTTP `500` (not `200`).

## UI Contract
- `GET /` redirects (`307`) to `/ui`.
- `GET /ui` returns `text/html`.
- UI includes two modes:
  - Single HTML run (calls `/run-one`)
  - Batch CSV upload (calls `/run-batch`)
- UI shows status, quality score, pass/fail, and output paths, plus error box for failed requests.

## Filesystem Contract
- Default output root: `OUTPUT_DIR` env var, default `outputs/`.
- Any request-level `output_dir` must resolve inside `outputs/`.
- Single run artifacts:
  - `outputs/<run_id>/<job_id>/page.md`
  - `outputs/<run_id>/<job_id>/meta.json`
  - `outputs/<run_id>/<job_id>/quality_report.json`
- Batch summary:
  - `outputs/<run_id>/summary.csv`
- Uploaded UI files are staged locally:
  - `inputs/uploads/<run_id>/...`
