"""Pipeline orchestration for fixture-based jobs."""

from __future__ import annotations

from seo_factory.domain.models import JobResult, JobSpec
from seo_factory.extractors.html_fixture import extract_fixture_content
from seo_factory.generators.template import generate_markdown_and_meta
from seo_factory.quality.rules import evaluate_quality


def run_job(spec: JobSpec) -> JobResult:
    """Run one offline job from fixture extraction to quality scoring."""

    content = extract_fixture_content(spec.source_path)
    markdown, meta = generate_markdown_and_meta(spec.source_path, spec.target_keyword, content)
    quality_report = evaluate_quality(markdown, meta, spec.target_keyword)
    return JobResult(
        job_id=spec.job_id,
        run_id=spec.run_id,
        source_path=spec.source_path,
        markdown=markdown,
        meta=meta,
        quality_report=quality_report,
    )
