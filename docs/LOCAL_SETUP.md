# Local Setup

## One-Command MVP Run
1. `make setup`
2. `make up OPEN_UI=1`
3. Use UI at `http://127.0.0.1:8000/ui`
4. `make down`

`make up` behavior:
- If `.tmp/api.pid` points to a live process, stops that managed API first and restarts it.
- Refuses to start if port `8000` is occupied by a different process.
- Starts API in background and stores PID in `.tmp/api.pid`.
- Waits until `/health` returns `{"status":"ok"}` (max 10s).
- Opens `/ui` only when `OPEN_UI=1`.

`make down` behavior:
- Stops only the process from `.tmp/api.pid` if present.
- If pid file is missing, prints a message and exits `0`.

`make status` behavior:
- Reports whether the managed API pid is alive.
- Runs a `/health` check and prints `ok` vs unreachable/non-ok.

Use `make api` for foreground debugging.

## UI Usage Notes
- Single run tab:
  - Upload `.html/.htm`.
  - Set `keyword`, `job_id`, `run_id`.
  - Optional `output_dir` (must stay inside `outputs/`; empty means default `OUTPUT_DIR`, usually `outputs`).
- Batch run tab:
  - Upload `.csv` with columns: `job_id,source_path,target_keyword`.
  - Set `run_id`.
  - Optional `output_dir` (same `outputs/` restriction and default behavior).

## Offline-First Expectations
- Make targets start API with `NO_LLM_MODE=true` and `OFFLINE_MODE=true`.
- Inputs are local files only (`fixtures/` and `inputs/`), with uploaded files staged under `inputs/uploads/`.
