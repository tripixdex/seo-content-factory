"""Tests for deterministic slug generation."""

from __future__ import annotations

from seo_factory.generators.template import slugify


def test_slugify_exact_scenario_a_keyword() -> None:
    assert slugify("product analytics automation") == "product-analytics-automation"


def test_slugify_normalizes_symbols_and_spaces() -> None:
    assert slugify("  Local SEO Automation!!  ") == "local-seo-automation"
