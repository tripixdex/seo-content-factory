# Demo Scenarios

All scenarios are local, offline-first, and free-only. Use local fixture paths under `fixtures/pages/`.

## Scenario A: Single fixture -> SEO page markdown + meta + quality report

### Exact Input
- Command intent: process one local fixture file.
- Source path: `fixtures/pages/demo_a.html`
- Target keyword: `product analytics automation`
- Config:
  - `NO_LLM_MODE=true`
  - `OFFLINE_MODE=true`
  - `OUTPUT_DIR=./outputs/demo_a`
  - `RUN_ID=demo-a-001`

### Expected Outputs
- File: `outputs/demo_a/demo-a-001/item_001/page.md`
  - Deterministic sections: H1, summary, next steps.
  - Includes keyword in H1 and body.
- File: `outputs/demo_a/demo-a-001/item_001/meta.json`
  - Keys: `title`, `description`, `slug`, `canonical_url`.
  - `slug` equals `product-analytics-automation`.
- File: `outputs/demo_a/demo-a-001/item_001/quality_report.json`
  - Checks include heading presence, keyword presence, and meta length checks.
  - Includes `quality_score` and `passed`.

## Scenario B: CSV batch of fixtures -> outputs folder + summary CSV

### Exact Input
- CSV file: `fixtures/demo_batch.csv`
- CSV content (exact rows):

```csv
job_id,source_path,target_keyword
item_001,fixtures/pages/demo_b_1.html,automated seo reporting
item_002,fixtures/pages/demo_b_2.html,technical seo audits
item_003,fixtures/pages/demo_b_3.html,content workflow automation
```

- Config:
  - `NO_LLM_MODE=true`
  - `OFFLINE_MODE=true`
  - `OUTPUT_DIR=./outputs/demo_b`
  - `RUN_ID=demo-b-001`

### Expected Outputs
- Folder: `outputs/demo_b/demo-b-001/`
- Per-row artifacts:
  - `item_001/page.md`, `item_001/meta.json`, `item_001/quality_report.json`
  - `item_002/page.md`, `item_002/meta.json`, `item_002/quality_report.json`
  - `item_003/page.md`, `item_003/meta.json`, `item_003/quality_report.json`
- Summary CSV: `outputs/demo_b/demo-b-001/summary.csv`
  - Columns: `row_id`, `job_id`, `source_path`, `slug`, `quality_score`, `status`, `error_message`
  - Contains 3 rows in same order as input CSV.

## Scenario C: No LLM deterministic template generation (free/offline)

### Exact Input
- Command intent: run the same fixture twice in deterministic mode.
- Source path: `fixtures/pages/demo_a.html`
- Target keyword: `local seo automation`
- Config for both runs:
  - `NO_LLM_MODE=true`
  - `OFFLINE_MODE=true`
  - `SEED=42`
  - `OUTPUT_DIR=./outputs/demo_c/run_{1|2}`

### Expected Outputs
- Run 1 and Run 2 generate identical:
  - `page.md` content
  - `meta.json` values
  - `quality_report.json` check outcomes and score
- Determinism check:
  - Hash of `run_1/.../page.md` equals hash of `run_2/.../page.md`.
  - Hash of `run_1/.../meta.json` equals hash of `run_2/.../meta.json`.
- No network dependency required to complete scenario.
