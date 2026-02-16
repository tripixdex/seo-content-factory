"""Pipeline orchestrator stub."""

from __future__ import annotations

from seo_factory.domain.models import JobResult, JobSpec
from seo_factory.extractors.html_fixture import load_html_fixture
from seo_factory.generators.template import generate_markdown_and_meta
from seo_factory.quality.rules import evaluate_quality


def run_job(spec: JobSpec) -> JobResult:
    """Run one fixture-based job and return an in-memory result."""

    html_text = load_html_fixture(spec.source_path)
    markdown, meta = generate_markdown_and_meta(spec.job_id, spec.target_keyword, html_text)
    quality_report = evaluate_quality(markdown, meta, spec.target_keyword)
    return JobResult(
        job_id=spec.job_id,
        run_id=spec.run_id,
        source_path=spec.source_path,
        markdown=markdown,
        meta=meta,
        quality_report=quality_report,
    )
