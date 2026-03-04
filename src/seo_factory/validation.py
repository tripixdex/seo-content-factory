"""Shared validation helpers for IDs and local source paths."""

from __future__ import annotations

import re
from pathlib import Path

ALLOWED_SOURCE_ROOTS = (Path("fixtures"), Path("inputs"))
ALLOWED_OUTPUT_ROOT = Path("outputs")
_SAFE_ID_RE = re.compile(r"^[A-Za-z0-9._-]+$")


def validate_safe_identifier(value: str, field_name: str) -> str:
    """Validate IDs used as path segments."""

    candidate = value.strip()
    if not candidate:
        raise ValueError(f"{field_name} must be non-empty")
    if ".." in candidate:
        raise ValueError(f"{field_name} must not contain '..'")
    if "/" in candidate or "\\" in candidate:
        raise ValueError(f"{field_name} must not contain path separators")
    if not _SAFE_ID_RE.fullmatch(candidate):
        raise ValueError(f"{field_name} must match [A-Za-z0-9._-] and contain no spaces")
    return candidate


def resolve_allowed_source_path(path_value: str) -> Path:
    """Resolve a source path and require it to stay within allowed roots."""

    candidate = path_value.strip()
    if not candidate:
        raise ValueError("source_path must be non-empty")

    try:
        resolved = (Path.cwd() / Path(candidate)).resolve(strict=True)
    except FileNotFoundError as exc:
        raise ValueError(f"source_path does not exist: {candidate}") from exc

    for root in ALLOWED_SOURCE_ROOTS:
        root_resolved = root.resolve()
        if root_resolved in resolved.parents or resolved == root_resolved:
            return resolved

    allowed = ", ".join(root.as_posix() for root in ALLOWED_SOURCE_ROOTS)
    raise ValueError(f"source_path must resolve inside one of: {allowed}")


def resolve_allowed_output_dir(path_value: str | None, default_dir: Path | None = None) -> Path:
    """Resolve output dir and require it to stay within outputs/."""

    configured_default = default_dir if default_dir is not None else ALLOWED_OUTPUT_ROOT
    candidate_path = Path(path_value) if path_value else configured_default
    try:
        resolved = (Path.cwd() / candidate_path).resolve()
    except OSError as exc:
        raise ValueError(f"output_dir is invalid: {candidate_path}") from exc

    output_root = ALLOWED_OUTPUT_ROOT.resolve()
    if output_root in resolved.parents or resolved == output_root:
        return resolved
    raise ValueError("output_dir must resolve inside: outputs")
