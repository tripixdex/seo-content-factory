# Local Setup

## One-Command MVP Run
1. `make setup`
2. `make up OPEN_UI=1`
3. Use UI at `http://127.0.0.1:8000/ui`
4. `make down`

`make up` behavior:
- Kills stale listeners on port `8000`.
- Starts API in background and stores PID in `.tmp/api.pid`.
- Waits until `/health` returns `{"status":"ok"}` (max 10s).
- Opens `/ui` only when `OPEN_UI=1`.

`make down` behavior:
- Stops API by PID file if running.
- Cleans stale PID file safely.

Use `make api` for foreground debugging.

## UI Usage Notes
- Single run tab:
  - Upload `.html/.htm`.
  - Set `keyword`, `job_id`, `run_id`.
  - Optional `output_dir` (empty means default `OUTPUT_DIR`, usually `outputs`).
- Batch run tab:
  - Upload `.csv` with columns: `job_id,source_path,target_keyword`.
  - Set `run_id`.
  - Optional `output_dir` (same default behavior).

## Offline-First Expectations
- Make targets start API with `NO_LLM_MODE=true` and `OFFLINE_MODE=true`.
- Inputs are local files only (`fixtures/` and `inputs/`), with uploaded files staged under `inputs/uploads/`.
