"""Regression tests for path-safety and API error semantics."""

from __future__ import annotations

import csv
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from seo_factory.api.app import app

client = TestClient(app)


def test_run_id_traversal_attempt_rejected(tmp_path: Path) -> None:
    response = client.post(
        "/run-one",
        json={
            "source_path": "fixtures/pages/demo_a.html",
            "keyword": "product analytics automation",
            "job_id": "item_001",
            "run_id": "../../escape-test",
            "output_dir": "outputs/test_api_validation/api_one",
        },
    )
    assert response.status_code == 400
    assert "run_id" in response.json()["detail"]


def test_job_id_traversal_attempt_rejected(tmp_path: Path) -> None:
    response = client.post(
        "/run-one",
        json={
            "source_path": "fixtures/pages/demo_a.html",
            "keyword": "product analytics automation",
            "job_id": "../job-escape",
            "run_id": "safe-run-001",
            "output_dir": "outputs/test_api_validation/api_one",
        },
    )
    assert response.status_code == 400
    assert "job_id" in response.json()["detail"]


def test_single_run_forbidden_source_path_rejected(tmp_path: Path) -> None:
    response = client.post(
        "/run-one",
        json={
            "source_path": "README.md",
            "keyword": "product analytics automation",
            "job_id": "item_001",
            "run_id": "safe-run-001",
            "output_dir": "outputs/test_api_validation/api_one",
        },
    )
    assert response.status_code == 400
    assert "source_path must resolve inside one of" in response.json()["detail"]


def test_batch_row_forbidden_source_path_rejected(tmp_path: Path) -> None:
    csv_content = "\n".join(
        [
            "job_id,source_path,target_keyword",
            "item_001,README.md,product analytics automation",
        ]
    )
    response = client.post(
        "/run-batch",
        json={
            "csv_filename": "uploaded_batch.csv",
            "csv_content": csv_content,
            "run_id": "api-run-batch-invalid-row",
            "output_dir": "outputs/test_api_validation/api_batch",
        },
    )
    assert response.status_code == 200
    assert response.json()["status"] == "partial_success"
    assert response.json()["passed"] is False

    summary_path = Path(response.json()["output_paths"]["summary_csv"])
    with summary_path.open("r", newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert rows[0]["status"] == "failed"
    assert "source_path must resolve inside one of" in rows[0]["error_message"]


def test_missing_required_field_returns_422() -> None:
    response = client.post(
        "/run-one",
        json={
            "source_path": "fixtures/pages/demo_a.html",
            "job_id": "item_001",
            "run_id": "safe-run-001",
        },
    )
    assert response.status_code == 422


def test_business_validation_returns_400(tmp_path: Path) -> None:
    response = client.post(
        "/run-batch",
        json={
            "csv_path": "fixtures/demo_batch.csv",
            "run_id": "bad run id",
            "output_dir": "outputs/test_api_validation/api_batch",
        },
    )
    assert response.status_code == 400
    assert "run_id" in response.json()["detail"]


def test_output_dir_inside_outputs_is_allowed() -> None:
    response = client.post(
        "/run-one",
        json={
            "source_path": "fixtures/pages/demo_a.html",
            "keyword": "product analytics automation",
            "job_id": "item_900",
            "run_id": "safe-run-900",
            "output_dir": "outputs/custom/safe",
        },
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_output_dir_outside_outputs_rejected_with_400() -> None:
    response = client.post(
        "/run-one",
        json={
            "source_path": "fixtures/pages/demo_a.html",
            "keyword": "product analytics automation",
            "job_id": "item_901",
            "run_id": "safe-run-901",
            "output_dir": "../../tmp/outside",
        },
    )
    assert response.status_code == 400
    assert "output_dir must resolve inside" in response.json()["detail"]


def test_batch_partial_failure_status_and_quality_policy() -> None:
    csv_content = "\n".join(
        [
            "job_id,source_path,target_keyword",
            "item_ok,fixtures/pages/demo_a.html,product analytics automation",
            "item_bad,README.md,product analytics automation",
        ]
    )
    response = client.post(
        "/run-batch",
        json={
            "csv_filename": "mixed_batch.csv",
            "csv_content": csv_content,
            "run_id": "api-run-batch-mixed",
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "partial_success"
    assert payload["passed"] is False
    assert payload["quality_score"] == 0.5


def test_batch_systemic_failure_returns_http_500() -> None:
    with patch("seo_factory.pipeline.batch_runner.run_job", side_effect=RuntimeError("boom")):
        response = client.post(
            "/run-batch",
            json={
                "csv_path": "fixtures/demo_batch.csv",
                "run_id": "api-run-batch-system-fail",
                "output_dir": "outputs/test_api_validation/api_batch_system_fail",
            },
        )
    assert response.status_code == 500
    assert "Batch execution failed" in response.json()["detail"]


def test_html_content_over_limit_returns_413() -> None:
    response = client.post(
        "/run-one",
        json={
            "source_filename": "large.html",
            "html_content": "a" * 1_000_001,
            "keyword": "product analytics automation",
            "job_id": "item_oversize_001",
            "run_id": "api-run-oversize-html",
            "output_dir": "outputs/test_api_validation/api_oversize_html",
        },
    )
    assert response.status_code == 413
    assert "html_content exceeds max size" in response.json()["detail"]


def test_csv_content_over_limit_returns_413() -> None:
    csv_content = "job_id,source_path,target_keyword\n" + ("a" * 1_000_001)
    response = client.post(
        "/run-batch",
        json={
            "csv_filename": "large.csv",
            "csv_content": csv_content,
            "run_id": "api-run-oversize-csv",
            "output_dir": "outputs/test_api_validation/api_oversize_csv",
        },
    )
    assert response.status_code == 413
    assert "csv_content exceeds max size" in response.json()["detail"]
