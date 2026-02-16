"""Typer CLI for offline demo execution."""

from __future__ import annotations

import csv
from pathlib import Path

import typer

from seo_factory.config import Settings
from seo_factory.domain.models import JobSpec
from seo_factory.pipeline.orchestrator import run_job
from seo_factory.storage.fs import file_sha256, write_job_result, write_json, write_summary_csv

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
    spec = JobSpec(job_id=job_id, source_path=source, target_keyword=keyword, run_id=run_id)
    result = run_job(spec)
    job_dir = write_job_result(output_dir, result)
    return job_dir, result.meta


def _run_batch_internal(csv_path: Path, run_id: str, output_dir: Path) -> Path:
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
                _, meta = _run_one_internal(source_path, keyword, job_id, run_id, output_dir)
                slug = meta.get("slug", "")
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


def _quality_score_from_report(path: Path) -> float:
    import json

    payload = json.loads(path.read_text(encoding="utf-8"))
    return float(payload.get("quality_score", 0.0))


@app.command("health")
def health() -> None:
    """Show resolved settings for local validation."""

    settings = Settings()
    typer.echo(settings.model_dump_json(indent=2))


@app.command("run-one")
def run_one(
    source: Path = typer.Option(..., exists=True, file_okay=True, dir_okay=False),
    keyword: str = typer.Option(...),
    job_id: str = typer.Option(...),
    run_id: str = typer.Option(...),
    output_dir: Path = typer.Option(...),
) -> None:
    """Run one offline job and write artifacts."""

    job_dir, _ = _run_one_internal(source, keyword, job_id, run_id, output_dir)
    typer.echo(f"Wrote: {job_dir}")


@app.command("run-batch")
def run_batch(
    csv_path: Path = typer.Option(..., "--csv", exists=True, file_okay=True, dir_okay=False),
    run_id: str = typer.Option(..., "--run-id"),
    output_dir: Path = typer.Option(..., "--output-dir"),
) -> None:
    """Run batch jobs from CSV and write summary CSV."""

    summary = _run_batch_internal(csv_path, run_id, output_dir)
    typer.echo(f"Wrote: {summary}")


@app.command("demo-a")
def demo_a() -> None:
    """Run Scenario A exactly as defined in docs/DEMO_SCENARIOS.md."""

    settings = Settings()
    _require_deterministic_modes(settings)
    source = Path("fixtures/pages/demo_a.html")
    output_dir = Path("outputs/demo_a")
    job_dir, _ = _run_one_internal(source, "product analytics automation", "item_001", "demo-a-001", output_dir)
    typer.echo(f"Scenario A complete: {job_dir}")


@app.command("demo-b")
def demo_b() -> None:
    """Run Scenario B exactly as defined in docs/DEMO_SCENARIOS.md."""

    settings = Settings()
    _require_deterministic_modes(settings)
    summary = _run_batch_internal(Path("fixtures/demo_batch.csv"), "demo-b-001", Path("outputs/demo_b"))
    typer.echo(f"Scenario B complete: {summary}")


@app.command("demo-c")
def demo_c() -> None:
    """Run Scenario C and persist determinism hashes."""

    settings = Settings()
    _require_deterministic_modes(settings)
    source = Path("fixtures/pages/demo_a.html")
    run_id = "demo-c-001"
    job_id = "item_001"

    run_1_dir, _ = _run_one_internal(source, "local seo automation", job_id, run_id, Path("outputs/demo_c/run_1"))
    run_2_dir, _ = _run_one_internal(source, "local seo automation", job_id, run_id, Path("outputs/demo_c/run_2"))

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
