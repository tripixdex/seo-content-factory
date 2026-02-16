"""Domain models for pipeline contracts."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field


class JobSpec(BaseModel):
    """Input contract for a single generation job."""

    job_id: str = Field(min_length=1)
    source_path: Path
    target_keyword: str = Field(min_length=1)
    run_id: str = Field(min_length=1)


class ExtractedContent(BaseModel):
    """Deterministically extracted fixture content."""

    title: str
    h1: str
    paragraphs: list[str]


class QualityReport(BaseModel):
    """Scored quality checks produced by rules engine."""

    checks: dict[str, bool]
    quality_score: float = Field(ge=0.0, le=1.0)
    passed: bool


class JobResult(BaseModel):
    """Output contract for one processed job."""

    job_id: str
    run_id: str
    source_path: Path
    markdown: str
    meta: dict[str, str]
    quality_report: QualityReport
    status: str = "success"
    error_message: str | None = None
