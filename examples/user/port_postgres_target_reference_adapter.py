#!/usr/bin/env python3
"""Controlled PORT target-reference adapter for local diagnostics.

This adapter is not a benchmark method or baseline. It validates the
cross-dialect local diagnostic path by copying only the manifest-declared
PostgreSQL target reference query into the runner-provided candidate path.
It performs no SQL execution, checking, scoring, timing, or metrics work.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any


EXPECTED_DIAGNOSTIC_MODE = "cross_dialect_reference"
EXPECTED_TARGET_ROLE = "positive_reference"
EXPECTED_TARGET_ENGINE = "postgres"


def _simple_yaml_mapping(path: Path) -> dict[str, Any]:
    """Parse the simple mapping subset used by current case manifests."""

    root: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(-1, root)]
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line_without_comment = raw_line.split("#", 1)[0].rstrip()
        if not line_without_comment.strip():
            continue
        stripped = line_without_comment.strip()
        if stripped.startswith("-") or ":" not in stripped:
            continue
        indent = len(line_without_comment) - len(line_without_comment.lstrip(" "))
        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip()
        while indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if value == "":
            child: dict[str, Any] = {}
            parent[key] = child
            stack.append((indent, child))
            continue
        lowered = value.strip("'\"").lower()
        if lowered == "true":
            parent[key] = True
        elif lowered == "false":
            parent[key] = False
        else:
            parent[key] = value.strip("'\"")
    return root


def _load_manifest(path: Path) -> dict[str, Any]:
    try:
        import yaml  # type: ignore
    except Exception:
        return _simple_yaml_mapping(path)

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"manifest root must be a mapping: {path}")
    return data


def _mapping(value: object, *, field: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{field} must be a mapping")
    return value


def _require_value(value: object, expected: object, *, field: str) -> None:
    if value != expected:
        raise ValueError(f"{field} must be {expected!r}")


def _resolve_case_relative(case_dir: Path, raw: object, *, field: str) -> Path:
    if not isinstance(raw, str) or not raw.strip():
        raise ValueError(f"{field} must be a non-empty case-relative path")
    path = Path(raw.strip())
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"{field} must stay inside the case directory")
    resolved = (case_dir / path).resolve()
    case_resolved = case_dir.resolve()
    if resolved != case_resolved and case_resolved not in resolved.parents:
        raise ValueError(f"{field} escapes the case directory")
    if not resolved.exists():
        raise ValueError(f"{field} does not exist: {resolved}")
    return resolved


def _ensure_candidate_path_allowed(candidate_path: Path) -> None:
    workspace_raw = os.environ.get("SQLRB_WORKSPACE_DIR")
    if not workspace_raw:
        return
    workspace = Path(workspace_raw).resolve()
    resolved = candidate_path.resolve()
    if resolved != workspace and workspace not in resolved.parents:
        raise ValueError("SQLRB_CANDIDATE_SQL_PATH must stay inside SQLRB_WORKSPACE_DIR")


def _target_reference_query(case_dir: Path) -> Path:
    manifest_path = case_dir / "manifest.yaml"
    if not manifest_path.exists():
        raise ValueError(f"manifest.yaml is missing: {manifest_path}")

    manifest = _load_manifest(manifest_path)
    local_diagnostic = _mapping(
        manifest.get("local_diagnostic"),
        field="local_diagnostic",
    )
    _require_value(
        local_diagnostic.get("diagnostic_mode"),
        EXPECTED_DIAGNOSTIC_MODE,
        field="local_diagnostic.diagnostic_mode",
    )

    target_reference = _mapping(
        local_diagnostic.get("target_reference"),
        field="local_diagnostic.target_reference",
    )
    _require_value(
        target_reference.get("role"),
        EXPECTED_TARGET_ROLE,
        field="local_diagnostic.target_reference.role",
    )
    _require_value(
        target_reference.get("engine"),
        EXPECTED_TARGET_ENGINE,
        field="local_diagnostic.target_reference.engine",
    )
    _require_value(
        target_reference.get("use_for_checker_oracle"),
        False,
        field="local_diagnostic.target_reference.use_for_checker_oracle",
    )

    return _resolve_case_relative(
        case_dir,
        target_reference.get("query"),
        field="local_diagnostic.target_reference.query",
    )


def main() -> int:
    try:
        case_dir = Path(os.environ["SQLRB_CASE_DIR"]).resolve()
        candidate_path = Path(os.environ["SQLRB_CANDIDATE_SQL_PATH"]).resolve()
        _ensure_candidate_path_allowed(candidate_path)
        target_query = _target_reference_query(case_dir)
        candidate_path.parent.mkdir(parents=True, exist_ok=True)
        candidate_path.write_text(target_query.read_text(encoding="utf-8"), encoding="utf-8")
        return 0
    except Exception as exc:
        print(f"controlled target-reference adapter failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
