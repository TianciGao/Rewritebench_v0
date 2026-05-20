"""Case package asset resolver for local user-entry runs.

The resolver is intentionally metadata-driven from selected case-engine rows.
It does not infer Common-core membership by scanning ``cases/`` and does not
invoke adapters, execute databases, run checkers, or compute metrics.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .case_selection import SelectedCaseEngineRow


@dataclass(frozen=True)
class ResolvedCasePackage:
    """Resolved package paths for one selected case-engine row."""

    case_id: str
    pool: str
    engine: str
    case_dir: Path
    manifest_path: Path
    source_sql_path: Path
    schema_profile_path: Path
    schema_external_profile_path: Path | None
    checker_config_path: Path
    normalization_config_path: Path
    compare_config_path: Path
    expected_rejections_path: Path | None
    package_path_from_manifest: str
    manifest_schema: dict[str, Any]
    manifest_taxonomy: dict[str, Any]
    resolution_status: str
    resolution_notes: str


def _simple_yaml_mapping(path: Path) -> dict[str, Any]:
    """Parse the simple mapping subset used by current manifests."""

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
        parent[key] = value.strip("'\"")
    return root


def _load_yaml_mapping(path: Path) -> dict[str, Any]:
    try:
        import yaml  # type: ignore
    except Exception:
        return _simple_yaml_mapping(path)

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be a mapping: {path}")
    return data


def _ensure_under_repo(path: Path, repo_root: Path, *, field: str) -> Path:
    resolved = path.resolve()
    repo_resolved = repo_root.resolve()
    if resolved != repo_resolved and repo_resolved not in resolved.parents:
        raise ValueError(f"{field} escapes repository root: {path}")
    return resolved


def _resolve_repo_relative(repo_root: Path, raw: object, *, field: str) -> Path:
    if not isinstance(raw, str) or not raw.strip():
        raise ValueError(f"{field} is required")
    path = Path(raw.strip())
    if path.is_absolute():
        raise ValueError(f"{field} must be repository-relative: {raw}")
    if ".." in path.parts:
        raise ValueError(f"{field} must not contain '..': {raw}")
    return _ensure_under_repo(repo_root / path, repo_root, field=field)


def _resolve_case_relative(case_dir: Path, raw: object, *, field: str) -> Path:
    if not isinstance(raw, str) or not raw.strip():
        raise ValueError(f"{field} is required")
    path = Path(raw.strip())
    if path.is_absolute():
        raise ValueError(f"{field} must be case-relative: {raw}")
    if ".." in path.parts:
        raise ValueError(f"{field} must not contain '..': {raw}")
    resolved = (case_dir / path).resolve()
    case_resolved = case_dir.resolve()
    if resolved != case_resolved and case_resolved not in resolved.parents:
        raise ValueError(f"{field} escapes case directory: {raw}")
    return resolved


def _optional_case_path(case_dir: Path, raw: object, *, field: str) -> Path | None:
    if raw is None or raw == "":
        return None
    return _resolve_case_relative(case_dir, raw, field=field)


def _require_exists(path: Path, *, field: str) -> None:
    if not path.exists():
        raise FileNotFoundError(f"{field} does not exist: {path}")


def _first_sql_object_path(items: object, *, field: str) -> str | None:
    if not isinstance(items, list) or not items:
        return None
    first = items[0]
    if not isinstance(first, dict):
        raise ValueError(f"{field} must contain object entries")
    raw = first.get("path")
    if raw is None:
        return None
    if not isinstance(raw, str):
        raise ValueError(f"{field}.path must be a string")
    return raw


def resolve_case_package(*, repo_root: Path, row: SelectedCaseEngineRow) -> ResolvedCasePackage:
    """Resolve current user-entry package assets for a selected row."""

    case_dir = _resolve_repo_relative(repo_root, row.case_path, field="case_path")
    manifest_path = case_dir / "manifest.yaml"
    _require_exists(manifest_path, field="manifest")

    manifest = _load_yaml_mapping(manifest_path)
    if manifest.get("case_id") != row.case_id:
        raise ValueError(f"manifest case_id does not match selected row: {manifest_path}")
    manifest_pool = manifest.get("pool") or manifest.get("primary_pool")
    if manifest_pool != row.pool:
        raise ValueError(f"manifest pool does not match selected row: {manifest_path}")
    package_path_from_manifest = manifest.get("package_path", row.case_path)
    if not isinstance(package_path_from_manifest, str):
        raise ValueError(f"manifest package_path must be a string: {manifest_path}")
    if package_path_from_manifest != row.case_path:
        raise ValueError(f"manifest package_path does not match selected row: {manifest_path}")

    sql = manifest.get("sql")
    if not isinstance(sql, dict):
        raise ValueError(f"manifest sql section must be a mapping: {manifest_path}")
    source_sql_path = _resolve_case_relative(case_dir, sql.get("source"), field="sql.source")
    selected_source = _resolve_repo_relative(
        repo_root, row.source_sql_path, field="selected source_sql_path"
    )
    if source_sql_path != selected_source:
        raise ValueError(f"manifest sql.source does not match selected row: {manifest_path}")
    _require_exists(source_sql_path, field="sql.source")

    schema = manifest.get("schema")
    if not isinstance(schema, dict):
        raise ValueError(f"manifest schema section must be a mapping: {manifest_path}")
    schema_profile_path = _resolve_case_relative(
        case_dir, schema.get("profile"), field="schema.profile"
    )
    _require_exists(schema_profile_path, field="schema.profile")
    external_profile_raw = schema.get("external_profile")
    schema_external_profile_path = (
        _resolve_repo_relative(repo_root, external_profile_raw, field="schema.external_profile")
        if external_profile_raw
        else None
    )
    if schema_external_profile_path is not None:
        _require_exists(schema_external_profile_path, field="schema.external_profile")

    checker = manifest.get("checker")
    if not isinstance(checker, dict):
        raise ValueError(f"manifest checker section must be a mapping: {manifest_path}")
    checker_config_path = _resolve_case_relative(
        case_dir, checker.get("checker"), field="checker.checker"
    )
    normalization_config_path = _resolve_case_relative(
        case_dir, checker.get("normalization"), field="checker.normalization"
    )
    compare_config_path = _resolve_case_relative(
        case_dir, checker.get("compare_config"), field="checker.compare_config"
    )
    for field, path in [
        ("checker.checker", checker_config_path),
        ("checker.normalization", normalization_config_path),
        ("checker.compare_config", compare_config_path),
    ]:
        _require_exists(path, field=field)
    expected_rejections_path = _optional_case_path(
        case_dir, checker.get("expected_rejections"), field="checker.expected_rejections"
    )
    if expected_rejections_path is not None:
        _require_exists(expected_rejections_path, field="checker.expected_rejections")

    positive_sql_path = _first_sql_object_path(
        sql.get("positive_rewrites"), field="sql.positive_rewrites"
    )
    if positive_sql_path is not None:
        _require_exists(
            _resolve_case_relative(case_dir, positive_sql_path, field="sql.positive_rewrites.path"),
            field="sql.positive_rewrites.path",
        )
    negative_sql_path = _first_sql_object_path(
        sql.get("hard_negatives"), field="sql.hard_negatives"
    )
    if negative_sql_path is not None:
        _require_exists(
            _resolve_case_relative(case_dir, negative_sql_path, field="sql.hard_negatives.path"),
            field="sql.hard_negatives.path",
        )

    taxonomy = manifest.get("taxonomy")
    manifest_taxonomy = taxonomy if isinstance(taxonomy, dict) else {}

    return ResolvedCasePackage(
        case_id=row.case_id,
        pool=row.pool,
        engine=row.engine,
        case_dir=case_dir,
        manifest_path=manifest_path,
        source_sql_path=source_sql_path,
        schema_profile_path=schema_profile_path,
        schema_external_profile_path=schema_external_profile_path,
        checker_config_path=checker_config_path,
        normalization_config_path=normalization_config_path,
        compare_config_path=compare_config_path,
        expected_rejections_path=expected_rejections_path,
        package_path_from_manifest=package_path_from_manifest,
        manifest_schema=schema,
        manifest_taxonomy=manifest_taxonomy,
        resolution_status="ok",
        resolution_notes="case package assets resolved",
    )
