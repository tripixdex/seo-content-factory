.PHONY: setup lint format test demo-a demo-b demo-c

VENV=.venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip
RUFF=$(VENV)/bin/ruff
PYTEST=$(VENV)/bin/pytest

setup:
	python3 -m venv $(VENV)
	$(PYTHON) -m pip install --upgrade pip
	$(PIP) install -e ".[dev]"

lint:
	$(RUFF) check .

format:
	$(RUFF) format .

test:
	PYTHONPATH=src $(PYTEST)

demo-a:
	NO_LLM_MODE=true OFFLINE_MODE=true $(PYTHON) -m seo_factory.cli demo-a

demo-b:
	NO_LLM_MODE=true OFFLINE_MODE=true $(PYTHON) -m seo_factory.cli demo-b

demo-c:
	NO_LLM_MODE=true OFFLINE_MODE=true SEED=42 $(PYTHON) -m seo_factory.cli demo-c
