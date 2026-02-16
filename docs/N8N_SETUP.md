# n8n Setup (Local)

## Start n8n
1. Copy `infra/n8n/.env.example` to `infra/n8n/.env`.
2. Run `cd infra/n8n && docker compose up -d`.
3. Open `http://localhost:5678`.

## Start API
1. In repo root, run `make setup` (or `make setup-offline` if wheelhouse exists).
2. Run `make api`.
3. API should be reachable at `http://127.0.0.1:8000`.

## Import Workflow JSON
1. In n8n UI, open **Workflows** > **Import from File**.
2. Select `workflows/n8n/seo_factory_demo.json`.
3. Save and execute via Manual Trigger.

## Important macOS Note
- In n8n HTTP Request nodes, API URL must be:
  - `http://host.docker.internal:8000`
- This resolves host machine services from Docker Desktop containers.

## Offline Demo Guarantee
- Workflow calls local API only.
- API processes local fixture files under `fixtures/`.
- No web fetching is required for scenarios A/B/C.
