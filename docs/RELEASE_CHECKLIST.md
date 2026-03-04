# Release Checklist

## Commands That Must Pass
Run from repo root:
1. `make format`
2. `make lint`
3. `make test`
4. `make down || true`
5. `make up OPEN_UI=0`
6. `curl -s http://127.0.0.1:8000/health`
7. `curl -I http://127.0.0.1:8000/ui`
8. `make down`

## Manual Verification
1. Open UI and run one HTML file successfully.
2. Run one batch CSV successfully.
3. Confirm result panel shows `status`, `quality_score`, `passed`, and output paths.
4. Confirm artifacts exist under `outputs/<run_id>/...`.
5. Confirm root route redirects: `GET /` -> `/ui`.
6. Confirm offline-first flags used in `make up` flow.

## Release Tagging
1. Commit changes:
   - `git add -A`
   - `git commit -m "stage5: portfolio MVP freeze"`
2. Create annotated tag:
   - `git tag -a v0.1.0 -m "Portfolio MVP freeze"`
3. Push branch and tags:
   - `git push origin <branch>`
   - `git push origin v0.1.0`
