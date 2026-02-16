"""Import-level smoke tests for Stage 1 skeleton."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def test_key_modules_import() -> None:
    modules = [
        "seo_factory",
        "seo_factory.cli",
        "seo_factory.config",
        "seo_factory.domain.models",
        "seo_factory.pipeline.orchestrator",
        "seo_factory.pipeline.batch_runner",
        "seo_factory.extractors.html_fixture",
        "seo_factory.generators.template",
        "seo_factory.quality.rules",
        "seo_factory.storage.fs",
    ]
    for module_name in modules:
        assert importlib.import_module(module_name) is not None
