# Project Map

## Repository Tree
```text
.
├── docs/
│   ├── ACCEPTANCE_CRITERIA.md
│   ├── ARCHITECTURE.md
│   ├── CONTRACTS.md
│   ├── DEMO_SCENARIOS.md
│   ├── DEMO_60S.md
│   ├── INDEX.md
│   ├── LOCAL_SETUP.md
│   ├── N8N_SETUP.md
│   ├── PRD.md
│   ├── PROJECT_MAP.md
│   ├── RELEASE_CHECKLIST.md
│   └── SCOPE.md
├── fixtures/
│   ├── demo_batch.csv
│   └── pages/
│       ├── demo_a.html
│       ├── demo_b_1.html
│       ├── demo_b_2.html
│       └── demo_b_3.html
├── outputs/
│   └── .gitkeep
├── src/
│   └── seo_factory/
│       ├── __init__.py
│       ├── api/app.py
│       ├── api/ui_page.py
│       ├── cli.py
│       ├── config.py
│       ├── domain/models.py
│       ├── extractors/html_fixture.py
│       ├── generators/template.py
│       ├── pipeline/orchestrator.py
│       ├── pipeline/batch_runner.py
│       ├── quality/rules.py
│       ├── storage/fs.py
│       └── validation.py
├── tests/
│   ├── test_api_smoke.py
│   ├── test_api_validation.py
│   ├── test_batch_order.py
│   ├── test_determinism.py
│   ├── test_imports.py
│   └── test_slugify.py
├── .env.example
├── .gitignore
├── Makefile
├── pyproject.toml
├── workflows/n8n/seo_factory_demo.json
├── infra/n8n/docker-compose.yml
└── REPORT.md
```

## Where To Find What
- Product definition: `docs/PRD.md` and `docs/SCOPE.md`.
- Technical design and contracts: `docs/ARCHITECTURE.md`, `docs/CONTRACTS.md`.
- Demo instructions: `docs/DEMO_SCENARIOS.md`.
- Acceptance bar: `docs/ACCEPTANCE_CRITERIA.md`.
- Offline sample inputs: `fixtures/pages/` and `fixtures/demo_batch.csv`.
- Implementation modules: `src/seo_factory/`.
- Quick run/test commands: `Makefile`.
