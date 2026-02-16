"""Batch execution helpers for CSV-based runs."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from seo_factory.domain.models import JobSpec
from seo_factory.pipeline.orchestrator import run_job
from seo_factory.storage.fs import write_job_result, write_summary_csv


def _quality_score_from_report(path: Path) -> float:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return float(payload.get("quality_score", 0.0))


def run_batch_from_csv(csv_path: Path, run_id: str, output_dir: Path) -> Path:
    """Run jobs in CSV order and write deterministic summary."""

    rows: list[dict[str, str]] = []
    with csv_path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for index, row in enumerate(reader, start=1):
            job_id = (row.get("job_id") or "").strip()
            source_path = Path((row.get("source_path") or "").strip())
            keyword = (row.get("target_keyword") or "").strip()

            status = "success"
            error_message = ""
            slug = ""
            quality_score = "0.0"

            try:
                if not job_id or not keyword or not str(source_path):
                    raise ValueError("CSV row missing required fields")
                spec = JobSpec(
                    job_id=job_id,
                    source_path=source_path,
                    target_keyword=keyword,
                    run_id=run_id,
                )
                result = run_job(spec)
                write_job_result(output_dir, result)
                slug = result.meta.get("slug", "")

                quality_path = output_dir / run_id / job_id / "quality_report.json"
                quality_score = str(_quality_score_from_report(quality_path))
            except Exception as exc:  # noqa: BLE001
                status = "failed"
                error_message = str(exc)

            rows.append(
                {
                    "row_id": str(index),
                    "job_id": job_id,
                    "source_path": str(source_path),
                    "slug": slug,
                    "quality_score": quality_score,
                    "status": status,
                    "error_message": error_message,
                }
            )

    return write_summary_csv(output_dir, run_id, rows)
