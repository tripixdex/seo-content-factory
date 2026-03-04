.PHONY: setup setup-offline vendor lint format test demo-a demo-b demo-c demo-ui api api-smoke up up-api n8n-up n8n-down open-ui down clean clean-uploads

VENV=.venv
PYTHON=$(VENV)/bin/python
WHEELHOUSE_DIR?=.vendor/wheels
HOST?=127.0.0.1
PORT?=8000
OPEN_UI?=1
N8N?=0
API_PID_FILE?=.tmp/api.pid

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
	NO_LLM_MODE=true OFFLINE_MODE=true $(PYTHON) -m uvicorn seo_factory.api.app:app --host $(HOST) --port $(PORT)

up-api:
	@mkdir -p .tmp
	@stale_pids=$$(lsof -ti tcp:$(PORT) -sTCP:LISTEN 2>/dev/null || true); \
	if [ -n "$$stale_pids" ]; then \
		echo "Stopping stale listener(s) on :$(PORT): $$stale_pids"; \
		kill $$stale_pids >/dev/null 2>&1 || true; \
		sleep 1; \
		remaining=$$(lsof -ti tcp:$(PORT) -sTCP:LISTEN 2>/dev/null || true); \
		if [ -n "$$remaining" ]; then \
			kill -9 $$remaining >/dev/null 2>&1 || true; \
		fi; \
	fi
	@if [ -f "$(API_PID_FILE)" ]; then \
		old_pid=$$(cat "$(API_PID_FILE)"); \
		if ! kill -0 $$old_pid >/dev/null 2>&1; then \
			rm -f "$(API_PID_FILE)"; \
		fi; \
	fi
	@echo "Starting API on http://$(HOST):$(PORT)"
	@NO_LLM_MODE=true OFFLINE_MODE=true $(PYTHON) -m uvicorn seo_factory.api.app:app --host $(HOST) --port $(PORT) >/tmp/seo_factory_api.log 2>&1 & \
	echo $$! > "$(API_PID_FILE)"
	@healthy=0; \
	for _ in $$(seq 1 20); do \
		if curl -fsS "http://$(HOST):$(PORT)/health" 2>/dev/null | grep -q '"status":[[:space:]]*"ok"'; then \
			healthy=1; \
			break; \
		fi; \
		sleep 0.5; \
	done; \
	if [ $$healthy -ne 1 ]; then \
		echo "API did not become healthy within 10s"; \
		if [ -f "$(API_PID_FILE)" ]; then \
			pid=$$(cat "$(API_PID_FILE)"); \
			kill $$pid >/dev/null 2>&1 || true; \
			rm -f "$(API_PID_FILE)"; \
		fi; \
		exit 1; \
	fi

n8n-up:
	cd infra/n8n && docker compose up -d

n8n-down:
	cd infra/n8n && docker compose down

open-ui:
	open http://$(HOST):$(PORT)/ui

up: up-api
	@if [ "$(N8N)" = "1" ]; then \
		$(MAKE) n8n-up; \
	fi
	@if [ "$(OPEN_UI)" = "1" ]; then \
		$(MAKE) open-ui; \
	fi

down:
	@if [ -f "$(API_PID_FILE)" ]; then \
		pid=$$(cat "$(API_PID_FILE)"); \
		if kill -0 $$pid >/dev/null 2>&1; then \
			kill $$pid; \
			echo "Stopped API (pid=$$pid)"; \
		else \
			echo "PID file found but process not running (pid=$$pid)"; \
		fi; \
		rm -f "$(API_PID_FILE)"; \
	else \
		echo "API pid file not found; nothing to stop."; \
	fi

demo-ui: up-api
	@sleep 2
	@$(MAKE) open-ui
	@echo "UI opened. Choose HTML file, fill keyword/job_id/run_id, click Run."

clean-uploads:
	@mkdir -p inputs/uploads
	@find inputs/uploads -mindepth 1 ! -name '.gitkeep' -exec rm -rf {} +

clean: down clean-uploads
	@rm -rf .tmp
	@echo "Cleaned runtime state and uploads."

api-smoke:
	$(PYTHON) -m pytest -q tests/test_api_smoke.py
