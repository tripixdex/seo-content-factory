"""Deterministic template-based content generation."""

from __future__ import annotations

import re
from pathlib import Path

from seo_factory.domain.models import ExtractedContent


def slugify(text: str) -> str:
    """Convert text into deterministic kebab-case."""

    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "untitled"


def _build_meta_title(keyword: str, source_h1: str) -> str:
    title = f"{keyword.title()} | {source_h1}"
    return title[:70].rstrip()


def _build_meta_description(keyword: str, paragraphs: list[str]) -> str:
    fallback = "Deterministic offline SEO draft from local fixture content."
    base = paragraphs[0] if paragraphs else fallback
    description = f"{keyword}: {base}"
    return description[:160].rstrip()


def generate_markdown_and_meta(
    source_path: Path,
    keyword: str,
    content: ExtractedContent,
) -> tuple[str, dict[str, str]]:
    """Generate deterministic markdown and metadata for one fixture."""

    slug = slugify(keyword)
    h1 = f"{keyword.title()} - {content.h1}"
    summary_line = content.paragraphs[0] if content.paragraphs else "No summary paragraph found."
    details = content.paragraphs[1:3]

    body_lines = [
        f"# {h1}",
        "",
        f"This draft targets keyword: **{keyword}**.",
        "",
        "## Summary",
        summary_line,
        "",
        "## Next Steps",
    ]
    if details:
        body_lines.extend([f"- {line}" for line in details])
    else:
        body_lines.append("- Add supporting points from source content.")

    markdown = "\n".join(body_lines)
    meta = {
        "title": _build_meta_title(keyword, content.h1),
        "description": _build_meta_description(keyword, content.paragraphs),
        "slug": slug,
        "canonical_url": f"local://{source_path.as_posix()}",
    }
    return markdown, meta
