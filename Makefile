.PHONY: setup setup-offline vendor lint format test demo-a demo-b demo-c api api-smoke

VENV=.venv
PYTHON=$(VENV)/bin/python
WHEELHOUSE_DIR?=.vendor/wheels

setup:
	python3 -m venv $(VENV)
	$(PYTHON) -m pip install -U pip setuptools wheel
	$(PYTHON) -m pip install -e ".[dev]"

setup-offline:
	python3 -m venv $(VENV)
	@test -d "$(WHEELHOUSE_DIR)" || (echo "Missing wheelhouse: $(WHEELHOUSE_DIR)" && exit 1)
	$(PYTHON) -m pip install --no-index --find-links "$(WHEELHOUSE_DIR)" -U pip setuptools wheel
	$(PYTHON) -m pip install --no-index --find-links "$(WHEELHOUSE_DIR)" -e ".[dev]"

vendor:
	python3 -m venv $(VENV)
	$(PYTHON) -m pip install -U pip setuptools wheel
	mkdir -p "$(WHEELHOUSE_DIR)"
	$(PYTHON) -m pip download -d "$(WHEELHOUSE_DIR)" -r requirements-lock.txt

lint:
	$(PYTHON) -m ruff check .

format:
	$(PYTHON) -m ruff format .

test:
	$(PYTHON) -m pytest

demo-a:
	NO_LLM_MODE=true OFFLINE_MODE=true $(PYTHON) -m seo_factory.cli demo-a

demo-b:
	NO_LLM_MODE=true OFFLINE_MODE=true $(PYTHON) -m seo_factory.cli demo-b

demo-c:
	NO_LLM_MODE=true OFFLINE_MODE=true SEED=42 $(PYTHON) -m seo_factory.cli demo-c

api:
	NO_LLM_MODE=true OFFLINE_MODE=true $(PYTHON) -m uvicorn seo_factory.api.app:app --host 127.0.0.1 --port 8000

api-smoke:
	$(PYTHON) -m pytest -q tests/test_api_smoke.py
