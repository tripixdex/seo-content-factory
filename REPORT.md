# REPORT

## 1) Executive summary
- Stage 3 codebase is present with API, n8n compose assets, and workflow JSON in repo.
- Ruff lint is clean in the project venv.
- Test suite passes in the current venv: `8 passed`.
- `make setup` currently fails on this machine due package index resolution during editable install build deps.
- FastAPI `TestClient` dependency requirement is satisfied in the active venv (`httpx` installed).
- `requirements-lock.txt` was updated to match installed `httpx` version for reproducibility.
- Existing demo artifacts are present under `outputs/demo_a`, `outputs/demo_b`, and `outputs/demo_c`.

## 2) Environment
- OS: macOS `26.2` (`Darwin`)
- Python: `3.13.5`
- CPU arch: `arm64`
- venv: `/Users/vladgurov/Desktop/work/seo-content-factory/.venv`

## 3) Reproducibility status (checklist)
- [ ] `make setup`: **FAIL**
  - Evidence: `ERROR: No matching distribution found for setuptools>=68`.
- [x] `make lint`: **PASS**
  - Evidence: `All checks passed!`.
- [x] `make test`: **PASS**
  - Evidence: `8 passed in 0.28s`.
- [ ] `make demo-a`: **NOT RUN** (not executed in this verification session).
- [ ] `make demo-b`: **NOT RUN** (not executed in this verification session).
- [ ] `make demo-c`: **NOT RUN** (not executed in this verification session).

## 4) Dependencies note
- `fastapi.testclient.TestClient` (Starlette TestClient) requires `httpx`.
- Resolved in current venv (`pip show httpx`): `Version: 0.28.1`.
- Lock alignment fix applied: `requirements-lock.txt` updated from `httpx==0.27.2` to `httpx==0.28.1`.

## 5) Commands executed (copy-paste)
```bash
$ make setup
python3 -m venv .venv
.venv/bin/python -m pip install -U pip setuptools wheel
.venv/bin/python -m pip install -e ".[dev]"
ERROR: No matching distribution found for setuptools>=68
make: *** [setup] Error 1

$ make lint
.venv/bin/python -m ruff check .
All checks passed!

$ make test
.venv/bin/python -m pytest
........                                                                 [100%]
8 passed in 0.28s

$ uname -s && uname -m && .venv/bin/python -V && .venv/bin/python -m pip show httpx | sed -n '1,20p'
Darwin
arm64
Python 3.13.5
Name: httpx
Version: 0.28.1

$ sw_vers -productVersion
26.2
```

## 6) Artifacts produced
- `outputs/demo_a/demo-a-001/item_001/page.md`
- `outputs/demo_a/demo-a-001/item_001/meta.json`
- `outputs/demo_a/demo-a-001/item_001/quality_report.json`
- `outputs/demo_b/demo-b-001/summary.csv`
- `outputs/demo_b/demo-b-001/item_001/page.md`
- `outputs/demo_b/demo-b-001/item_002/page.md`
- `outputs/demo_b/demo-b-001/item_003/page.md`
- `outputs/demo_c/determinism_hashes.json`

## 7) Next step: Stage 3.2 runtime verification
- Run API locally:
  - `make api`
- Verify API health from another terminal:
  - `curl http://127.0.0.1:8000/health`
- Start n8n and import workflow:
  - `cd infra/n8n && docker compose up -d`
  - Open `http://localhost:5678`
  - Import `workflows/n8n/seo_factory_demo.json`
  - Ensure HTTP node URL uses `http://host.docker.internal:8000`
