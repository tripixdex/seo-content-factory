"""Quality rules registry and scoring."""

from __future__ import annotations

from seo_factory.domain.models import QualityReport


def _extract_h1(markdown: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def evaluate_quality(markdown: str, meta: dict[str, str], keyword: str) -> QualityReport:
    """Apply deterministic checks and compute a normalized score."""

    lower_md = markdown.lower()
    lower_kw = keyword.lower()
    h1 = _extract_h1(markdown).lower()

    checks = {
        "heading_presence": bool(h1),
        "keyword_in_h1": lower_kw in h1,
        "keyword_in_body": lower_kw in lower_md,
        "meta_title_length_ok": 20 <= len(meta.get("title", "")) <= 70,
        "meta_description_length_ok": 50 <= len(meta.get("description", "")) <= 160,
    }
    passed_count = sum(1 for value in checks.values() if value)
    score = round(passed_count / len(checks), 2)
    return QualityReport(checks=checks, quality_score=score, passed=score >= 0.8)
