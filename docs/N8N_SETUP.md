# n8n Setup (Local)

## Start n8n
1. Copy `infra/n8n/.env.example` to `infra/n8n/.env`.
2. Run `cd infra/n8n && docker compose up -d`.
3. Open `http://localhost:5678`.

## Start API
1. In repo root, run `make setup` (or `make setup-offline` if wheelhouse exists).
2. Run `make api` (or `make up N8N=1` for API + n8n).
3. API should be reachable at `http://127.0.0.1:8000`.

## Import Workflow JSON
1. In n8n UI, open **Workflows** > **Import from File**.
2. Select `workflows/n8n/seo_factory_demo.json`.
3. Save and execute via Manual Trigger.

## Important macOS Note
- In n8n HTTP Request nodes, API URL must be:
  - `http://host.docker.internal:8000`
- This resolves host machine services from Docker Desktop containers.

## HTTP Request Node (Exact Body Examples)
- Method: `POST`
- URL: `http://host.docker.internal:8000/run-one`
- Send body as JSON.

### Variant A: `source_path`
```json
{
  "source_path": "fixtures/pages/demo_a.html",
  "keyword": "product analytics automation",
  "job_id": "item_001",
  "run_id": "n8n-demo-a-001"
}
```

### Variant B: `html_content`
```json
{
  "source_filename": "example.html",
  "html_content": "<html><head><title>Demo</title></head><body>Demo</body></html>",
  "keyword": "product analytics automation",
  "job_id": "item_001",
  "run_id": "n8n-demo-ui-001"
}
```

### Validation/Errors
- `422 Unprocessable Entity` usually means invalid JSON body shape or missing required fields (`keyword`, `job_id`, `run_id`).
- `400 Bad Request` usually means business validation error (for example invalid `source_path` or missing source data).

## Offline Demo Guarantee
- Workflow calls local API only.
- API processes local fixture files under `fixtures/`.
- No web fetching is required for scenarios A/B/C.
