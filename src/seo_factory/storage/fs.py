"""Filesystem output helpers for run artifacts."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

from seo_factory.domain.models import JobResult


def build_job_dir(output_dir: Path, run_id: str, job_id: str) -> Path:
    """Create and return the per-job directory."""

    job_dir = output_dir / run_id / job_id
    job_dir.mkdir(parents=True, exist_ok=True)
    return job_dir


def write_job_result(output_dir: Path, result: JobResult) -> Path:
    """Write markdown, meta, and quality report files for a job."""

    job_dir = build_job_dir(output_dir, result.run_id, result.job_id)
    (job_dir / "page.md").write_text(result.markdown, encoding="utf-8")

    meta_json = json.dumps(result.meta, indent=2, sort_keys=True)
    (job_dir / "meta.json").write_text(meta_json, encoding="utf-8")

    report_json = result.quality_report.model_dump_json(indent=2)
    (job_dir / "quality_report.json").write_text(report_json, encoding="utf-8")
    return job_dir


def write_summary_csv(output_dir: Path, run_id: str, rows: list[dict[str, str]]) -> Path:
    """Write deterministic batch summary CSV."""

    run_dir = output_dir / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    summary_path = run_dir / "summary.csv"
    columns = [
        "row_id",
        "job_id",
        "source_path",
        "slug",
        "quality_score",
        "status",
        "error_message",
    ]
    with summary_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)
    return summary_path


def file_sha256(path: Path) -> str:
    """Compute SHA256 hash for a file."""

    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, payload: dict) -> Path:
    """Write JSON payload with deterministic key ordering."""

    path.parent.mkdir(parents=True, exist_ok=True)
    payload_json = json.dumps(payload, indent=2, sort_keys=True)
    path.write_text(payload_json, encoding="utf-8")
    return path
