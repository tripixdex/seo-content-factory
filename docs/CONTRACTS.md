# Contracts

## Input Schema

### Single Job (`JobSpec`)
- `job_id` (string, required): stable identifier (e.g., `item_001`).
- `source_path` (path, required): local HTML fixture path.
- `target_keyword` (string, required): target SEO phrase.
- `run_id` (string, required): run namespace (e.g., `demo-a-001`).

### Batch CSV
- File: `fixtures/demo_batch.csv`
- Columns:
  - `job_id`
  - `source_path`
  - `target_keyword`
- Determinism rule: process rows in file order.

## Output Schema

### `JobResult`
- `job_id` (string)
- `run_id` (string)
- `source_path` (path)
- `markdown` (string)
- `meta` (object)
- `quality_report` (object)
- `status` (string)
- `error_message` (string | null)

### `meta.json`
- `title` (string)
- `description` (string)
- `slug` (string)
- `canonical_url` (string)

### `quality_report.json`
- `checks` (object[string -> bool])
- `quality_score` (0-100 integer)
- `passed` (bool)

## Folder Layout Contract
- Root output path: `OUTPUT_DIR` (default `outputs/`).
- Per run: `outputs/<run_id>/`
- Per item: `outputs/<run_id>/<job_id>/`
- Required files per item:
  - `page.md`
  - `meta.json`
  - `quality_report.json`

## Determinism Rules
- Given same fixture file, keyword, run config, and seed, generated content must be identical.
- JSON keys must be written in stable order when applicable.
- Batch summary rows must preserve original CSV order.
- Dynamic timestamps are disallowed in artifact body content for deterministic mode.

## Configuration Contract
- Env vars:
  - `NO_LLM_MODE` (bool)
  - `OFFLINE_MODE` (bool)
  - `OUTPUT_DIR` (path)
  - `SEED` (int >= 0)
- Secrets policy:
  - Secrets must be provided only via environment variables.
  - No secrets committed in repository files.
