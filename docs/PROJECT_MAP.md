# Project Map

## Repository Tree
```text
.
├── docs/
│   ├── ACCEPTANCE_CRITERIA.md
│   ├── ARCHITECTURE.md
│   ├── CONTRACTS.md
│   ├── DEMO_SCENARIOS.md
│   ├── INDEX.md
│   ├── PRD.md
│   ├── PROJECT_MAP.md
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
│       ├── cli.py
│       ├── config.py
│       ├── domain/models.py
│       ├── extractors/html_fixture.py
│       ├── generators/template.py
│       ├── pipeline/orchestrator.py
│       ├── quality/rules.py
│       └── storage/fs.py
├── tests/
│   └── test_imports.py
├── .env.example
├── .gitignore
├── Makefile
├── pyproject.toml
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
