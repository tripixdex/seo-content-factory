# Demo In 60 Seconds

## Exact Steps
1. `make setup`
2. `make up OPEN_UI=1`
3. Open `http://127.0.0.1:8000/ui` (auto-opens if supported).
4. In `Single Run`:
   - Upload `fixtures/pages/demo_a.html`
   - Keep defaults or set `run_id=demo-single-001`
   - Click `Run Single`
5. In `Batch CSV`:
   - Upload `fixtures/demo_batch.csv`
   - Set `run_id=demo-batch-001`
   - Click `Run Batch`
6. Confirm result panel shows `status`, `quality_score`, `passed`, and output paths.

## Where Outputs Appear
- Single artifacts:
  - `outputs/demo-single-001/ui-item-001/page.md`
  - `outputs/demo-single-001/ui-item-001/meta.json`
  - `outputs/demo-single-001/ui-item-001/quality_report.json`
- Batch artifacts:
  - `outputs/demo-batch-001/summary.csv`
  - `outputs/demo-batch-001/<job_id>/...`

## If Something Goes Wrong
- UI not opening:
  - Open `http://127.0.0.1:8000/ui` manually.
- Port conflict / stale process:
  - Run `make down` then `make up OPEN_UI=0`.
- Health check fails:
  - Verify `curl -s http://127.0.0.1:8000/health` returns `{"status":"ok",...}`.
- Bad request from UI:
  - Ensure file types are valid (`.html/.htm` for single, `.csv` for batch).

Stop demo:
- `make down`
