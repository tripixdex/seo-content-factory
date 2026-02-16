"""Deterministic template-based content generator stub."""

from __future__ import annotations

from hashlib import sha1


def _deterministic_slug(keyword: str) -> str:
    return "-".join(keyword.lower().strip().split())


def generate_markdown_and_meta(job_id: str, keyword: str, html_text: str) -> tuple[str, dict[str, str]]:
    """Return deterministic markdown and metadata for a job."""

    excerpt = " ".join(html_text.split())[:120]
    digest = sha1(f"{job_id}|{keyword}".encode("utf-8")).hexdigest()[:8]
    slug = _deterministic_slug(keyword)

    markdown = "\n".join(
        [
            f"# {keyword.title()}",
            "",
            f"This draft targets keyword: **{keyword}**.",
            f"Source digest: `{digest}`.",
            "",
            "## Summary",
            excerpt,
            "",
            "## Next Steps",
            "- Review claims against source content.",
            "- Edit tone for your target audience.",
        ]
    )

    meta = {
        "title": f"{keyword.title()} | SEO Content Draft",
        "description": f"Deterministic draft for {keyword}.",
        "slug": slug,
        "canonical_url": f"local://fixture/{job_id}",
    }
    return markdown, meta
