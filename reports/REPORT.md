# REPORT (Final Minimal Cleanup Fixes)

## What Changed
1. Output-dir contract alignment (`outputs/` only)
   - Enforced `OUTPUT_DIR` setting validation to stay under repo `outputs/`.
   - Kept request-time business validation: user-provided `output_dir` outside `outputs/` returns HTTP `400`.
   - UI text now explicitly says overrides must stay inside `outputs/`.
   - CLI defaults `--output-dir` to `outputs` and validates it with the same policy.
   - Docs updated to reflect the same single policy (no arbitrary output roots).

2. Non-destructive Makefile process management
   - `make up` no longer kills arbitrary listeners on port `8000`.
   - If `.tmp/api.pid` exists and is alive, it stops that managed process first, then restarts.
   - If port `8000` is occupied by a different process, it prints a clear error and exits non-zero.
   - `make down` only targets PID from `.tmp/api.pid`; missing pid file prints message and exits `0`.
   - Added `make status` to report managed PID status + `/health` probe status.

3. Batch exception handling refinement
   - Batch row loop now catches only expected row-level `ValueError` and records row failure.
   - Unexpected/systemic exceptions are no longer converted to row failures.
   - `/run-batch` now returns HTTP `500` with clear message for unexpected failures.
   - Preserved semantics:
     - all rows ok -> `status="success"`, `passed=true`
     - some rows fail expected validation -> `status="partial_success"`, `passed=false`
     - systemic failure -> HTTP `500`

4. Payload size limits
   - Added explicit payload byte limits:
     - `html_content <= 1_000_000`
     - `csv_content <= 1_000_000`
   - Exceeded limits now return HTTP `413` with explicit field message.

## Audit Points Closed
- Closed: `1) OUTPUT_DIR contract alignment (single truth)`
- Closed: `2) Makefile process management must be non-destructive`
- Closed: `3) Batch exception handling refinement`
- Closed: `4) Payload size limits`

## Files Updated
- `src/seo_factory/api/app.py`
- `src/seo_factory/pipeline/batch_runner.py`
- `src/seo_factory/config.py`
- `src/seo_factory/cli.py`
- `src/seo_factory/api/ui_page.py`
- `Makefile`
- `tests/test_api_validation.py`
- `README.md`
- `docs/LOCAL_SETUP.md`
- `docs/CONTRACTS.md`

## Commands Run + Outputs
- `make format`
  - `.venv/bin/python -m ruff format .`
  - `21 files left unchanged`
- `make lint`
  - `.venv/bin/python -m ruff check .`
  - `All checks passed!`
- `make test`
  - `.venv/bin/python -m pytest`
  - `24 passed in 0.21s`

## Remaining Limitations
- `OUTPUT_DIR` is still environment-configurable, but now constrained to resolve under repo `outputs/` only.
- Payload limits are currently hardcoded constants in API code (`1_000_000` bytes each), not environment-tunable.
