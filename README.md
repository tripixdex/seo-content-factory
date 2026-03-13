# SEO Content Factory

Deterministic local pipeline for turning HTML inputs into repeatable SEO draft artifacts with CLI, API, and browser demo paths.

## Why it matters

This repo is useful as a showcase of disciplined automation: same inputs, same outputs, explicit quality checks, and filesystem artifacts that are easy to inspect after a run.

## Capabilities

- Single-page and batch CSV processing from local inputs
- Deterministic markdown, metadata, and quality-report generation
- Browser UI, FastAPI endpoints, CLI demos, and optional n8n workflow
- Repo-local artifact output under `outputs/`
- Offline-first default run path with validation and path restrictions

## Quick Demo

Set up the local environment:

```bash
make setup
```

Run the browser demo:

```bash
make up OPEN_UI=1
```

Then:

1. Open `http://127.0.0.1:8000/ui` if it did not open automatically.
2. In `Single Run`, upload `fixtures/pages/demo_a.html`.
3. In `Batch CSV`, upload `fixtures/demo_batch.csv`.
4. Review `status`, `quality_score`, `passed`, and the generated artifact paths.

Stop the local API:

```bash
make down
```

## Verification

The lightweight verification path for this repo is:

```bash
make lint
make api-smoke
make demo-a
```

These commands check code style, hit the main API smoke test, and verify the single-item deterministic demo path.

## Inputs and Outputs

Accepted inputs:

- Single run: local `source_path` or uploaded `html_content` + `source_filename`
- Batch run: `csv_path` or `csv_content` + `csv_filename`
- Optional `output_dir` that must remain inside `outputs/`

Generated artifacts:

- `outputs/<run_id>/<job_id>/page.md`
- `outputs/<run_id>/<job_id>/meta.json`
- `outputs/<run_id>/<job_id>/quality_report.json`
- `outputs/<run_id>/summary.csv`

## Limitations

- This is a local deterministic draft-generation demo, not a production SEO platform
- Content generation is template-driven; it is not an editorial-quality system for every domain
- No external crawling, search-console integration, auth, or hosted workflow management
- Screenshot assets are not curated in-repo yet; the best showcase artifacts are the UI and generated files

## Why it is interesting in a portfolio

This repo shows practical automation discipline: reproducible runs, explicit validation, artifact generation, and multiple demo surfaces over the same controlled pipeline.

## Docs

- [docs/DEMO_60S.md](/Users/vladgurov/Desktop/work/seo-content-factory/docs/DEMO_60S.md)
- [docs/LOCAL_SETUP.md](/Users/vladgurov/Desktop/work/seo-content-factory/docs/LOCAL_SETUP.md)
- [docs/ARCHITECTURE.md](/Users/vladgurov/Desktop/work/seo-content-factory/docs/ARCHITECTURE.md)
- [docs/CONTRACTS.md](/Users/vladgurov/Desktop/work/seo-content-factory/docs/CONTRACTS.md)
- [docs/SCOPE.md](/Users/vladgurov/Desktop/work/seo-content-factory/docs/SCOPE.md)
