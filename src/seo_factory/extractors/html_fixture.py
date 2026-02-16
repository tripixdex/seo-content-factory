"""Fixture HTML loader for offline demos."""

from __future__ import annotations

from pathlib import Path


def load_html_fixture(path: Path) -> str:
    """Load HTML from a local fixture path."""

    if not path.exists():
        msg = f"Fixture file not found: {path}"
        raise FileNotFoundError(msg)
    return path.read_text(encoding="utf-8")
