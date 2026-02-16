"""Typer CLI for offline demo execution."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from seo_factory.config import Settings
from seo_factory.domain.models import JobSpec
from seo_factory.pipeline.batch_runner import run_batch_from_csv
from seo_factory.pipeline.orchestrator import run_job
from seo_factory.storage.fs import file_sha256, write_job_result, write_json

app = typer.Typer(help="SEO Content Automation Factory CLI")


def _require_deterministic_modes(settings: Settings) -> None:
    if not settings.no_llm_mode or not settings.offline_mode:
        msg = "This demo requires NO_LLM_MODE=true and OFFLINE_MODE=true"
        raise typer.BadParameter(msg)


def _run_one_internal(
    source: Path,
    keyword: str,
    job_id: str,
    run_id: str,
    output_dir: Path,
) -> tuple[Path, dict[str, str]]:
    spec = JobSpec(
        job_id=job_id,
        source_path=source,
        target_keyword=keyword,
        run_id=run_id,
    )
    result = run_job(spec)
    job_dir = write_job_result(output_dir, result)
    return job_dir, result.meta


@app.command("health")
def health() -> None:
    """Show resolved settings for local validation."""

    settings = Settings()
    typer.echo(settings.model_dump_json(indent=2))


@app.command("run-one")
def run_one(
    source: Annotated[
        Path,
        typer.Option(..., exists=True, file_okay=True, dir_okay=False),
    ],
    keyword: Annotated[str, typer.Option(...)],
    job_id: Annotated[str, typer.Option(...)],
    run_id: Annotated[str, typer.Option(...)],
    output_dir: Annotated[Path, typer.Option(...)],
) -> None:
    """Run one offline job and write artifacts."""

    job_dir, _ = _run_one_internal(source, keyword, job_id, run_id, output_dir)
    typer.echo(f"Wrote: {job_dir}")


@app.command("run-batch")
def run_batch(
    csv_path: Annotated[
        Path,
        typer.Option(..., "--csv", exists=True, file_okay=True, dir_okay=False),
    ],
    run_id: Annotated[str, typer.Option(..., "--run-id")],
    output_dir: Annotated[Path, typer.Option(..., "--output-dir")],
) -> None:
    """Run batch jobs from CSV and write summary CSV."""

    summary = run_batch_from_csv(csv_path, run_id, output_dir)
    typer.echo(f"Wrote: {summary}")


@app.command("demo-a")
def demo_a() -> None:
    """Run Scenario A exactly as defined in docs/DEMO_SCENARIOS.md."""

    settings = Settings()
    _require_deterministic_modes(settings)
    job_dir, _ = _run_one_internal(
        source=Path("fixtures/pages/demo_a.html"),
        keyword="product analytics automation",
        job_id="item_001",
        run_id="demo-a-001",
        output_dir=Path("outputs/demo_a"),
    )
    typer.echo(f"Scenario A complete: {job_dir}")


@app.command("demo-b")
def demo_b() -> None:
    """Run Scenario B exactly as defined in docs/DEMO_SCENARIOS.md."""

    settings = Settings()
    _require_deterministic_modes(settings)
    summary = run_batch_from_csv(
        csv_path=Path("fixtures/demo_batch.csv"),
        run_id="demo-b-001",
        output_dir=Path("outputs/demo_b"),
    )
    typer.echo(f"Scenario B complete: {summary}")


@app.command("demo-c")
def demo_c() -> None:
    """Run Scenario C and persist determinism hashes."""

    settings = Settings()
    _require_deterministic_modes(settings)
    run_id = "demo-c-001"
    job_id = "item_001"

    run_1_dir, _ = _run_one_internal(
        source=Path("fixtures/pages/demo_a.html"),
        keyword="local seo automation",
        job_id=job_id,
        run_id=run_id,
        output_dir=Path("outputs/demo_c/run_1"),
    )
    run_2_dir, _ = _run_one_internal(
        source=Path("fixtures/pages/demo_a.html"),
        keyword="local seo automation",
        job_id=job_id,
        run_id=run_id,
        output_dir=Path("outputs/demo_c/run_2"),
    )

    files = ["page.md", "meta.json", "quality_report.json"]
    run_1_hashes = {name: file_sha256(run_1_dir / name) for name in files}
    run_2_hashes = {name: file_sha256(run_2_dir / name) for name in files}
    identical = run_1_hashes == run_2_hashes

    report = {
        "run_1_dir": str(run_1_dir),
        "run_2_dir": str(run_2_dir),
        "run_1_hashes": run_1_hashes,
        "run_2_hashes": run_2_hashes,
        "identical": identical,
    }
    report_path = write_json(Path("outputs/demo_c/determinism_hashes.json"), report)
    typer.echo(f"Scenario C complete: {report_path} (identical={identical})")


if __name__ == "__main__":
    app()
