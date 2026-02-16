"""FastAPI smoke tests for local offline execution."""

from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from seo_factory.api.app import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert "version" in payload


def test_run_one_endpoint(tmp_path: Path) -> None:
    response = client.post(
        "/run-one",
        json={
            "source_path": "fixtures/pages/demo_a.html",
            "keyword": "product analytics automation",
            "job_id": "item_001",
            "run_id": "api-run-one",
            "output_dir": str(tmp_path / "api_one"),
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "success"
    assert payload["passed"] is True
    assert "page.md" in payload["hashes"]


def test_run_batch_endpoint(tmp_path: Path) -> None:
    response = client.post(
        "/run-batch",
        json={
            "csv_path": "fixtures/demo_batch.csv",
            "run_id": "api-run-batch",
            "output_dir": str(tmp_path / "api_batch"),
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "success"
    assert payload["passed"] is True
    assert "summary_csv" in payload["hashes"]
