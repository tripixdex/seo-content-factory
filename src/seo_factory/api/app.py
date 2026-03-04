"""FastAPI app exposing local offline seo_factory operations."""

from __future__ import annotations

import csv
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel, Field

from seo_factory import __version__
from seo_factory.api.ui_page import build_ui_html
from seo_factory.config import Settings
from seo_factory.domain.models import JobSpec
from seo_factory.pipeline.batch_runner import run_batch_from_csv
from seo_factory.pipeline.orchestrator import run_job
from seo_factory.storage.fs import file_sha256, write_job_result
from seo_factory.validation import (
    resolve_allowed_output_dir,
    resolve_allowed_source_path,
    validate_safe_identifier,
)

app = FastAPI(title="SEO Factory API", version=__version__)
MAX_HTML_CONTENT_BYTES = 1_000_000
MAX_CSV_CONTENT_BYTES = 1_000_000


class RunOneRequest(BaseModel):
    source_path: str | None = None
    html_content: str | None = None
    source_filename: str | None = None
    keyword: str = Field(min_length=1)
    job_id: str = Field(min_length=1)
    run_id: str = Field(min_length=1)
    output_dir: str | None = None


class RunBatchRequest(BaseModel):
    csv_path: str | None = None
    csv_content: str | None = None
    csv_filename: str | None = None
    run_id: str = Field(min_length=1)
    output_dir: str | None = None


def _output_dir(path_value: str | None, settings: Settings) -> Path:
    return resolve_allowed_output_dir(path_value, settings.output_dir)


def _ensure_payload_size(content: str, field_name: str, max_bytes: int) -> None:
    size_bytes = len(content.encode("utf-8"))
    if size_bytes > max_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"{field_name} exceeds max size of {max_bytes} bytes",
        )


def _save_uploaded_text(
    content: str, run_id: str, filename: str, suffixes: tuple[str, ...]
) -> Path:
    safe_run_id = validate_safe_identifier(run_id, "run_id")
    safe_name = Path(filename).name
    if not safe_name.lower().endswith(suffixes):
        allowed = ", ".join(suffixes)
        raise ValueError(f"Uploaded file must end with one of: {allowed}")
    target_dir = Path("inputs") / "uploads" / safe_run_id
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / safe_name
    target_path.write_text(content, encoding="utf-8")
    return target_path.resolve()


def _artifact_hashes(job_dir: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for name in ("page.md", "meta.json", "quality_report.json"):
        path = job_dir / name
        if path.exists():
            hashes[name] = file_sha256(path)
    return hashes


def _run_one_internal(source_path: Path, payload: RunOneRequest) -> dict[str, object]:
    safe_job_id = validate_safe_identifier(payload.job_id, "job_id")
    safe_run_id = validate_safe_identifier(payload.run_id, "run_id")
    result = run_job(
        JobSpec(
            job_id=safe_job_id,
            source_path=source_path,
            target_keyword=payload.keyword,
            run_id=safe_run_id,
        )
    )
    output_dir = _output_dir(payload.output_dir, Settings())
    job_dir = write_job_result(output_dir, result)
    return {
        "status": "success",
        "quality_score": result.quality_report.quality_score,
        "passed": result.quality_report.passed,
        "output_paths": {
            "job_dir": str(job_dir),
            "page": str(job_dir / "page.md"),
            "meta": str(job_dir / "meta.json"),
            "quality": str(job_dir / "quality_report.json"),
        },
        "hashes": _artifact_hashes(job_dir),
    }


@app.get("/")
def root() -> RedirectResponse:
    return RedirectResponse(url="/ui", status_code=307)


@app.get("/health")
def health() -> dict[str, str | bool]:
    settings = Settings()
    return {
        "status": "ok",
        "version": __version__,
        "no_llm_mode": settings.no_llm_mode,
        "offline_mode": settings.offline_mode,
    }


@app.get("/ui", response_class=HTMLResponse)
def ui() -> str:
    output_dir = resolve_allowed_output_dir(None, Settings().output_dir)
    return build_ui_html(str(output_dir))


@app.head("/ui")
def ui_head() -> HTMLResponse:
    return HTMLResponse(content="", status_code=200)


@app.post("/run-one")
def run_one(payload: RunOneRequest) -> dict[str, object]:
    try:
        if payload.html_content:
            _ensure_payload_size(payload.html_content, "html_content", MAX_HTML_CONTENT_BYTES)
            filename = payload.source_filename or f"{payload.job_id}.html"
            source_path = _save_uploaded_text(
                payload.html_content, payload.run_id, filename, (".html", ".htm")
            )
        elif payload.source_path:
            source_path = resolve_allowed_source_path(payload.source_path)
        else:
            raise ValueError("Provide either html_content or source_path")
        return _run_one_internal(source_path, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/run-batch")
def run_batch(payload: RunBatchRequest) -> dict[str, object]:
    try:
        validate_safe_identifier(payload.run_id, "run_id")
        if payload.csv_content:
            _ensure_payload_size(payload.csv_content, "csv_content", MAX_CSV_CONTENT_BYTES)
            csv_path = _save_uploaded_text(
                payload.csv_content,
                payload.run_id,
                payload.csv_filename or f"{payload.run_id}.csv",
                (".csv",),
            )
        elif payload.csv_path:
            csv_path = resolve_allowed_source_path(payload.csv_path)
        else:
            raise ValueError("Provide either csv_content or csv_path")

        output_dir = _output_dir(payload.output_dir, Settings())
        summary_path = run_batch_from_csv(
            csv_path=csv_path, run_id=payload.run_id, output_dir=output_dir
        )
        run_dir = output_dir / payload.run_id

        scores: list[float] = []
        passed = True
        with summary_path.open("r", newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                scores.append(float(row.get("quality_score", "0")))
                if row.get("status") != "success":
                    passed = False
        avg_quality = round(sum(scores) / len(scores), 2) if scores else 0.0
        status = "success" if passed else "partial_success"
        return {
            "status": status,
            "quality_score": avg_quality,
            "passed": passed,
            "output_paths": {"run_dir": str(run_dir), "summary_csv": str(summary_path)},
            "hashes": {"summary_csv": file_sha256(summary_path)},
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Batch execution failed: {exc}") from exc
