"""FastAPI app exposing local offline seo_factory operations."""

from __future__ import annotations

import csv
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from seo_factory import __version__
from seo_factory.config import Settings
from seo_factory.domain.models import JobSpec
from seo_factory.pipeline.batch_runner import run_batch_from_csv
from seo_factory.pipeline.orchestrator import run_job
from seo_factory.storage.fs import file_sha256, write_job_result

app = FastAPI(title="SEO Factory API", version=__version__)


class RunOneRequest(BaseModel):
    source_path: str
    keyword: str = Field(min_length=1)
    job_id: str = Field(min_length=1)
    run_id: str = Field(min_length=1)
    output_dir: str | None = None


class RunBatchRequest(BaseModel):
    csv_path: str
    run_id: str = Field(min_length=1)
    output_dir: str | None = None


def _output_dir(path_value: str | None, settings: Settings) -> Path:
    return Path(path_value) if path_value else settings.output_dir


def _artifact_hashes(job_dir: Path) -> dict[str, str]:
    files = ["page.md", "meta.json", "quality_report.json"]
    hashes: dict[str, str] = {}
    for name in files:
        path = job_dir / name
        if path.exists():
            hashes[name] = file_sha256(path)
    return hashes


@app.get("/health")
def health() -> dict[str, str | bool]:
    settings = Settings()
    return {
        "status": "ok",
        "version": __version__,
        "no_llm_mode": settings.no_llm_mode,
        "offline_mode": settings.offline_mode,
    }


@app.post("/run-one")
def run_one(payload: RunOneRequest) -> dict[str, object]:
    settings = Settings()
    output_dir = _output_dir(payload.output_dir, settings)
    try:
        spec = JobSpec(
            job_id=payload.job_id,
            source_path=Path(payload.source_path),
            target_keyword=payload.keyword,
            run_id=payload.run_id,
        )
        result = run_job(spec)
        job_dir = write_job_result(output_dir, result)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "status": "success",
        "output_paths": {
            "job_dir": str(job_dir),
            "page": str(job_dir / "page.md"),
            "meta": str(job_dir / "meta.json"),
            "quality": str(job_dir / "quality_report.json"),
        },
        "quality_score": result.quality_report.quality_score,
        "passed": result.quality_report.passed,
        "hashes": _artifact_hashes(job_dir),
    }


@app.post("/run-batch")
def run_batch(payload: RunBatchRequest) -> dict[str, object]:
    settings = Settings()
    output_dir = _output_dir(payload.output_dir, settings)
    try:
        summary_path = run_batch_from_csv(
            csv_path=Path(payload.csv_path),
            run_id=payload.run_id,
            output_dir=output_dir,
        )
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    run_dir = output_dir / payload.run_id
    quality_values: list[float] = []
    all_passed = True
    with summary_path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            status = row.get("status", "")
            if status != "success":
                all_passed = False
            score_raw = row.get("quality_score", "0")
            quality_values.append(float(score_raw))

    avg_quality = round(sum(quality_values) / len(quality_values), 2) if quality_values else 0.0
    return {
        "status": "success",
        "output_paths": {
            "run_dir": str(run_dir),
            "summary_csv": str(summary_path),
        },
        "quality_score": avg_quality,
        "passed": all_passed,
        "hashes": {"summary_csv": file_sha256(summary_path)},
    }
