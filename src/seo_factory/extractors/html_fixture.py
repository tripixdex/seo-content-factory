"""Fixture HTML loader/extractor for offline demos."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path

from seo_factory.domain.models import ExtractedContent


class _FixtureParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._current_tag: str | None = None
        self._title = ""
        self._h1 = ""
        self._paragraphs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._current_tag = tag

    def handle_endtag(self, tag: str) -> None:
        if self._current_tag == tag:
            self._current_tag = None

    def handle_data(self, data: str) -> None:
        text = " ".join(data.split()).strip()
        if not text or self._current_tag is None:
            return
        if self._current_tag == "title":
            self._title = f"{self._title} {text}".strip()
        elif self._current_tag == "h1" and not self._h1:
            self._h1 = text
        elif self._current_tag == "p":
            self._paragraphs.append(text)

    def to_content(self) -> ExtractedContent:
        return ExtractedContent(
            title=self._title or "Untitled Fixture",
            h1=self._h1 or "Untitled Heading",
            paragraphs=self._paragraphs,
        )


def load_html_fixture(path: Path) -> str:
    """Load raw HTML from a local fixture path."""

    if not path.exists():
        msg = f"Fixture file not found: {path}"
        raise FileNotFoundError(msg)
    return path.read_text(encoding="utf-8")


def extract_fixture_content(path: Path) -> ExtractedContent:
    """Extract title, h1, and paragraphs from a local fixture HTML file."""

    parser = _FixtureParser()
    parser.feed(load_html_fixture(path))
    return parser.to_content()
