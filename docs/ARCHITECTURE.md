# Architecture

## Goals
- Local-first pipeline runnable on macOS (Apple Silicon).
- Offline-friendly demo path with fixture HTML files.
- Deterministic outputs for reproducible portfolio demonstrations.

## Components
- `seo_factory.cli`:
  - Typer entrypoint (`single`, `batch`, `health`).
  - Receives user inputs and run options.
- `seo_factory.config`:
  - Typed settings via `pydantic-settings`.
  - Environment-only configuration, no committed secrets.
- `seo_factory.domain.models`:
  - Canonical contracts: `JobSpec`, `JobResult`, `QualityReport`.
- `seo_factory.pipeline.orchestrator`:
  - Coordinates extraction -> generation -> quality scoring.
- `seo_factory.extractors.html_fixture`:
  - Loads local HTML fixture files.
- `seo_factory.generators.template`:
  - Deterministic markdown/meta generation.
- `seo_factory.quality.rules`:
  - Rule registry/scoring stub for SEO checks.
- `seo_factory.storage.fs`:
  - Output folder creation and artifact writing.

## Data Flow
1. CLI resolves settings and parses input.
2. CLI builds `JobSpec`.
3. Orchestrator loads fixture HTML from local path.
4. Template generator creates markdown/meta deterministically.
5. Quality engine evaluates checks and computes score.
6. Storage writes `page.md`, `meta.json`, `quality_report.json`.

## Module Boundaries
- `pipeline` imports component modules; components do not import pipeline.
- `domain` holds shared data contracts and is dependency-light.
- `storage` handles only filesystem concerns, not business rules.
- `cli` is thin: argument handling and output messaging.

## Offline-First Design
- Inputs in demos are local files under `fixtures/pages/`.
- No network-fetch component is required for Stage 1.
- `OFFLINE_MODE=true` is supported by config contract.

## Determinism Controls
- Fixed seed (`SEED`) and stable input ordering.
- Template-based generation with deterministic slug/content layout.
- Stable JSON serialization (`sort_keys=True` where applicable).

## Stage Boundary
Stage 1 provides structure and stubs only. Full parsing logic, batch execution, richer rules, and robust error handling are Stage 2+ work.
