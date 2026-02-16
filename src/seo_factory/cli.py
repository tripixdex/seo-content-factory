"""Typer CLI skeleton for offline demo flows."""

from __future__ import annotations

from pathlib import Path

import typer

from seo_factory.config import Settings
from seo_factory.domain.models import JobSpec
from seo_factory.pipeline.orchestrator import run_job
from seo_factory.storage.fs import write_job_result

app = typer.Typer(help="SEO Content Automation Factory CLI")


@app.command("single")
def single(
    source_path: Path = typer.Option(..., exists=True, file_okay=True, dir_okay=False),
    keyword: str = typer.Option(...),
    run_id: str = typer.Option("demo-a-001"),
) -> None:
    """Stub for single fixture processing."""

    settings = Settings()
    spec = JobSpec(job_id="item_001", source_path=source_path, target_keyword=keyword, run_id=run_id)
    result = run_job(spec)
    job_dir = write_job_result(settings.output_dir, result)
    typer.echo(f"Stub complete. Wrote artifacts to {job_dir}")


@app.command("batch")
def batch(csv_path: Path = typer.Option(..., exists=True, file_okay=True, dir_okay=False)) -> None:
    """Stub for batch fixture processing."""

    typer.echo(f"Batch stub received CSV: {csv_path}")


@app.command("health")
def health() -> None:
    """Show resolved settings for local validation."""

    settings = Settings()
    typer.echo(settings.model_dump_json(indent=2))


if __name__ == "__main__":
    app()
