# Acceptance Criteria

## Feature-Level Definition of Done

### 1) Single URL Processing
- [ ] Given one URL and keyword, system generates exactly 3 artifacts: `page.md`, `meta.json`, `quality_report.json`.
- [ ] Artifacts are written under run-scoped output directory.
- [ ] `meta.json` includes required keys: `title`, `description`, `slug`, `canonical_url`.
- [ ] `quality_report.json` contains individual checks and aggregate score.
- [ ] With same input/config and seed, outputs are byte-identical across reruns.

### 2) Batch CSV Processing
- [ ] Given valid CSV with `source_url,target_keyword`, all rows are processed in deterministic order.
- [ ] Each row produces per-item artifact set (page/meta/report).
- [ ] `summary.csv` exists and contains `row_id`, `source_url`, `slug`, `quality_score`, `status`, `error_message`.
- [ ] Failures in one row do not block processing of remaining rows.
- [ ] Total processed rows in summary equals total input rows.

### 3) No LLM Mode (Deterministic/Offline)
- [ ] `NO_LLM_MODE=true` runs without requiring model downloads or paid APIs.
- [ ] `OFFLINE_MODE=true` run completes successfully without network calls.
- [ ] Template generation is deterministic for same input and seed.
- [ ] Output quality report still generated in no-LLM mode.

### 4) Security and Configuration Hygiene
- [ ] Secrets are read only from environment variables.
- [ ] No secrets or tokens committed in tracked files.
- [ ] Example config uses placeholders (e.g., `API_KEY=`) and safe defaults.
- [ ] Project includes `.env.example` guidance (without real secrets).

### 5) Documentation and Demo Readiness
- [ ] PRD, scope, demo scenarios, and acceptance criteria docs exist and are internally consistent.
- [ ] Demo scenarios include exact input values and expected file outputs.
- [ ] New contributor can run a deterministic demo by following docs only.

## Apple-Style Quality Bar
- Reproducibility:
  - Same inputs, config, and seed produce same artifacts.
  - Output structure and naming are stable and predictable.
- Tests:
  - At minimum, one test each for single URL flow, batch flow, and determinism check.
  - Tests run locally with one command and no paid dependencies.
- Security Hygiene:
  - No hardcoded secrets.
  - Env var validation fails fast with actionable messages.
  - Sensitive files ignored via `.gitignore` where appropriate.
- Documentation:
  - Setup and run instructions are concise and complete.
  - Demo paths and expected outputs are explicit.
  - Known limitations and non-goals are documented.
