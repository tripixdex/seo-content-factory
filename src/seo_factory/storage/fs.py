"""Filesystem output helpers for run artifacts."""

from __future__ import annotations

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
    (job_dir / "meta.json").write_text(
        json.dumps(result.meta, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (job_dir / "quality_report.json").write_text(
        result.quality_report.model_dump_json(indent=2),
        encoding="utf-8",
    )
    return job_dir
