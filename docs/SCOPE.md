# Scope: SEO Content Automation Factory

## MVP Scope (Must-Haves)
- CLI-first local workflow for macOS Apple Silicon.
- Input modes:
  - Single local HTML input (`source_path` or `html_content`).
  - Batch CSV input.
- Output artifacts per item:
  - SEO markdown page draft.
  - Metadata JSON (title, description, slug, canonical).
  - Quality report JSON/Markdown with pass/fail checks.
- Deterministic processing:
  - Stable row ordering.
  - Fixed templates/rules.
  - Configurable random seed (default fixed).
- `NO_LLM_MODE` for fully deterministic, offline-capable generation.
- Summary CSV for batch runs with status and quality score.
- Documentation for setup, run commands, and expected outputs.

## Nice-to-Haves
- Optional local LLM integration (open-source model runtime) behind feature flag.
- Readability scoring and keyword density diagnostics.
- Diff report between generated versions.
- Preset content styles per vertical (SaaS, e-commerce, services).
- Simple local HTML preview of markdown outputs.

## Explicitly Out of Scope
- Paid APIs or hosted inference requirements.
- Cloud deployment as required path.
- Auto-publish integrations (WordPress/Webflow/etc.) in MVP.
- Multi-user auth, roles, billing, or tenancy.
- Proprietary SEO scoring datasets.

## Phased Roadmap

### Phase 1 (2 Hours)
- Establish folder structure and config schema.
- Implement deterministic no-LLM pipeline skeleton.
- Support single URL flow with fixed template outputs.
- Produce one quality report format and one deterministic example run.

### Phase 2 (1 Day)
- Add robust CSV batch processing.
- Add summary CSV and per-item error handling.
- Expand quality checks (title length, meta length, heading presence, keyword coverage).
- Add reproducibility checks and basic tests.
- Finalize demo scripts and example fixtures.

### Phase 3 (3 Days)
- Add optional local LLM mode with explicit flag and fallback.
- Improve extraction robustness and template flexibility.
- Add local report UX (aggregated markdown/html dashboard).
- Harden docs, CI checks, and portfolio-quality walkthrough.
