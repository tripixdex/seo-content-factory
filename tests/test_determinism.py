"""Determinism tests aligned with Scenario C."""

from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from seo_factory.cli import app


def test_demo_c_generates_identical_hashes(monkeypatch: object) -> None:
    monkeypatch.setenv("NO_LLM_MODE", "true")
    monkeypatch.setenv("OFFLINE_MODE", "true")
    monkeypatch.setenv("SEED", "42")

    runner = CliRunner()
    result = runner.invoke(app, ["demo-c"])

    assert result.exit_code == 0
    payload = json.loads(Path("outputs/demo_c/determinism_hashes.json").read_text(encoding="utf-8"))
    assert payload["identical"] is True
    assert payload["run_1_hashes"]["page.md"] == payload["run_2_hashes"]["page.md"]
    assert payload["run_1_hashes"]["meta.json"] == payload["run_2_hashes"]["meta.json"]
