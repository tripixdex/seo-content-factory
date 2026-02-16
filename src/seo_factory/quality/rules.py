"""Quality rules registry and scoring stub."""

from __future__ import annotations

from seo_factory.domain.models import QualityReport


def evaluate_quality(markdown: str, meta: dict[str, str], keyword: str) -> QualityReport:
    """Apply simple deterministic checks and compute score."""

    checks = {
        "has_h1": markdown.startswith("# "),
        "keyword_in_markdown": keyword.lower() in markdown.lower(),
        "title_length_ok": 20 <= len(meta.get("title", "")) <= 70,
        "description_length_ok": 50 <= len(meta.get("description", "")) <= 160,
        "has_slug": bool(meta.get("slug")),
    }
    passed_count = sum(1 for passed in checks.values() if passed)
    score = int((passed_count / len(checks)) * 100)
    return QualityReport(checks=checks, quality_score=score, passed=score >= 80)
