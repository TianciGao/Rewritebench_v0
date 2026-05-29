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
from .user_run_schema import (
    DIAGNOSTIC_MODE_CROSS_DIALECT_REFERENCE,
    DIAGNOSTIC_MODE_SAME_ENGINE,
    DIAGNOSTIC_MODE_UNSUPPORTED,
)


LOCAL_DIAGNOSTIC_LEGACY_SCHEMA_VERSION = "port_cross_dialect_diagnostic_v0"
LOCAL_DIAGNOSTIC_SCHEMA_VERSION = "port_target_engine_diagnostic_v0"
LOCAL_DIAGNOSTIC_ENGINES = {"postgres", "mysql", "spark"}
LOCAL_DIAGNOSTIC_COMPARISON = "source_reference_result_to_target_candidate_result"


@dataclass(frozen=True)
class LocalDiagnosticMetadata:
    """Explicit local diagnostic role metadata from a case manifest."""

    schema_version: str
    diagnostic_mode: str
    source_reference_engine: str
    source_reference_query_path: Path
    target_candidate_engine: str
    target_reference_query_path: Path | None
    target_reference_role: str
    checker_comparison: str
    local_diagnostic_boundary: dict[str, Any]
    unsupported_reason: str
    manual_review_required: bool
    raw: dict[str, Any]


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
    local_diagnostic: LocalDiagnosticMetadata
    diagnostic_mode: str
    source_reference_engine: str
    source_reference_query_path: Path
    target_candidate_engine: str
    target_reference_query_path: Path | None
    target_reference_role: str
    checker_comparison: str
    local_diagnostic_boundary: dict[str, Any]
    unsupported_reason: str
    manual_review_required: bool
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


def _mapping(value: object, *, field: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{field} must be a mapping")
    return value


def _required_string(value: object, *, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value.strip()


def _required_engine(value: object, *, field: str) -> str:
    engine = _required_string(value, field=field)
    if engine not in LOCAL_DIAGNOSTIC_ENGINES:
        raise ValueError(f"{field} must be one of {sorted(LOCAL_DIAGNOSTIC_ENGINES)}")
    return engine


def _as_bool(value: object, *, field: str) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "false"}:
            return lowered == "true"
    raise ValueError(f"{field} must be a boolean")


def _validate_boundary(boundary: dict[str, Any], *, field: str) -> dict[str, Any]:
    expected = {
        "local_diagnostic_only": True,
        "official_metric_input": False,
        "paper_result_input": False,
        "reports_results_update": False,
        "leaderboard_input": False,
    }
    normalized: dict[str, Any] = {}
    for key, expected_value in expected.items():
        observed = _as_bool(boundary.get(key), field=f"{field}.{key}")
        if observed is not expected_value:
            raise ValueError(f"{field}.{key} must be {expected_value}")
        normalized[key] = observed
    return normalized


def _default_local_diagnostic(
    *,
    row: SelectedCaseEngineRow,
    source_sql_path: Path,
) -> LocalDiagnosticMetadata:
    boundary = {
        "local_diagnostic_only": True,
        "official_metric_input": False,
        "paper_result_input": False,
        "reports_results_update": False,
        "leaderboard_input": False,
    }
    return LocalDiagnosticMetadata(
        schema_version="",
        diagnostic_mode=DIAGNOSTIC_MODE_SAME_ENGINE,
        source_reference_engine=row.engine,
        source_reference_query_path=source_sql_path,
        target_candidate_engine=row.engine,
        target_reference_query_path=None,
        target_reference_role="",
        checker_comparison="",
        local_diagnostic_boundary=boundary,
        unsupported_reason="",
        manual_review_required=False,
        raw={},
    )


def _resolve_role_local_diagnostic(
    *,
    case_dir: Path,
    row: SelectedCaseEngineRow,
    schema_version: str,
    metadata: dict[str, Any],
    field_prefix: str,
) -> LocalDiagnosticMetadata:
    diagnostic_mode = _required_string(
        metadata.get("diagnostic_mode"), field=f"{field_prefix}.diagnostic_mode"
    )
    if diagnostic_mode not in {
        DIAGNOSTIC_MODE_SAME_ENGINE,
        DIAGNOSTIC_MODE_CROSS_DIALECT_REFERENCE,
        DIAGNOSTIC_MODE_UNSUPPORTED,
    }:
        raise ValueError(f"{field_prefix}.diagnostic_mode is unsupported")

    boundary = _validate_boundary(
        _mapping(metadata.get("boundary"), field=f"{field_prefix}.boundary"),
        field=f"{field_prefix}.boundary",
    )

    if diagnostic_mode == DIAGNOSTIC_MODE_UNSUPPORTED:
        unsupported_reason = _required_string(
            metadata.get("unsupported_reason"), field=f"{field_prefix}.unsupported_reason"
        )
        manual_review_required = _as_bool(
            metadata.get("manual_review_required", False),
            field=f"{field_prefix}.manual_review_required",
        )
        return LocalDiagnosticMetadata(
            schema_version=schema_version,
            diagnostic_mode=diagnostic_mode,
            source_reference_engine="",
            source_reference_query_path=case_dir / "__unsupported_source_reference__",
            target_candidate_engine=row.engine,
            target_reference_query_path=None,
            target_reference_role="",
            checker_comparison="",
            local_diagnostic_boundary=boundary,
            unsupported_reason=unsupported_reason,
            manual_review_required=manual_review_required,
            raw=metadata,
        )

    source_reference = _mapping(
        metadata.get("source_reference"), field=f"{field_prefix}.source_reference"
    )
    if source_reference.get("role") != "source_reference":
        raise ValueError(f"{field_prefix}.source_reference.role must be source_reference")
    source_reference_engine = _required_engine(
        source_reference.get("engine"),
        field=f"{field_prefix}.source_reference.engine",
    )
    source_reference_query_path = _resolve_case_relative(
        case_dir,
        source_reference.get("query"),
        field=f"{field_prefix}.source_reference.query",
    )
    _require_exists(
        source_reference_query_path,
        field=f"{field_prefix}.source_reference.query",
    )

    target_candidate = _mapping(
        metadata.get("target_candidate"), field=f"{field_prefix}.target_candidate"
    )
    if target_candidate.get("role") != "adapter_output":
        raise ValueError(f"{field_prefix}.target_candidate.role must be adapter_output")
    target_candidate_engine = _required_engine(
        target_candidate.get("engine"),
        field=f"{field_prefix}.target_candidate.engine",
    )
    if target_candidate_engine != row.engine:
        raise ValueError(
            f"{field_prefix}.target_candidate.engine must match selected engine {row.engine!r}"
        )

    checker = _mapping(metadata.get("checker"), field=f"{field_prefix}.checker")
    checker_comparison = _required_string(
        checker.get("comparison"), field=f"{field_prefix}.checker.comparison"
    )
    if checker_comparison != LOCAL_DIAGNOSTIC_COMPARISON:
        raise ValueError(
            f"{field_prefix}.checker.comparison must be "
            f"{LOCAL_DIAGNOSTIC_COMPARISON}"
        )

    target_reference_query_path: Path | None = None
    target_reference_role = ""
    target_reference = metadata.get("target_reference")
    if target_reference is not None:
        target_reference_map = _mapping(
            target_reference, field=f"{field_prefix}.target_reference"
        )
        target_reference_role = _required_string(
            target_reference_map.get("role"),
            field=f"{field_prefix}.target_reference.role",
        )
        if target_reference_role != "positive_reference":
            raise ValueError(
                f"{field_prefix}.target_reference.role must be positive_reference"
            )
        target_reference_engine = _required_engine(
            target_reference_map.get("engine"),
            field=f"{field_prefix}.target_reference.engine",
        )
        if target_reference_engine != target_candidate_engine:
            raise ValueError(
                f"{field_prefix}.target_reference.engine must match target_candidate.engine"
            )
        target_reference_query_path = _resolve_case_relative(
            case_dir,
            target_reference_map.get("query"),
            field=f"{field_prefix}.target_reference.query",
        )
        _require_exists(
            target_reference_query_path,
            field=f"{field_prefix}.target_reference.query",
        )
        if _as_bool(
            target_reference_map.get("use_for_checker_oracle"),
            field=f"{field_prefix}.target_reference.use_for_checker_oracle",
        ):
            raise ValueError(
                f"{field_prefix}.target_reference.use_for_checker_oracle must be false"
            )
        _as_bool(
            target_reference_map.get("use_for_sanity_control"),
            field=f"{field_prefix}.target_reference.use_for_sanity_control",
        )

    return LocalDiagnosticMetadata(
        schema_version=schema_version,
        diagnostic_mode=diagnostic_mode,
        source_reference_engine=source_reference_engine,
        source_reference_query_path=source_reference_query_path,
        target_candidate_engine=target_candidate_engine,
        target_reference_query_path=target_reference_query_path,
        target_reference_role=target_reference_role,
        checker_comparison=checker_comparison,
        local_diagnostic_boundary=boundary,
        unsupported_reason="",
        manual_review_required=False,
        raw=metadata,
    )


def _resolve_local_diagnostic(
    *,
    case_dir: Path,
    row: SelectedCaseEngineRow,
    source_sql_path: Path,
    raw_metadata: object,
) -> LocalDiagnosticMetadata:
    if raw_metadata is None:
        return _default_local_diagnostic(row=row, source_sql_path=source_sql_path)

    metadata = _mapping(raw_metadata, field="local_diagnostic")
    schema_version = _required_string(
        metadata.get("schema_version"), field="local_diagnostic.schema_version"
    )
    if schema_version == LOCAL_DIAGNOSTIC_SCHEMA_VERSION:
        engine_roles = _mapping(
            metadata.get("engine_roles"), field="local_diagnostic.engine_roles"
        )
        role_metadata = engine_roles.get(row.engine)
        if role_metadata is None:
            boundary = {
                "local_diagnostic_only": True,
                "official_metric_input": False,
                "paper_result_input": False,
                "reports_results_update": False,
                "leaderboard_input": False,
            }
            return LocalDiagnosticMetadata(
                schema_version=schema_version,
                diagnostic_mode=DIAGNOSTIC_MODE_UNSUPPORTED,
                source_reference_engine="",
                source_reference_query_path=case_dir / "__missing_engine_role__",
                target_candidate_engine=row.engine,
                target_reference_query_path=None,
                target_reference_role="",
                checker_comparison="",
                local_diagnostic_boundary=boundary,
                unsupported_reason=(
                    f"local_diagnostic.engine_roles has no role for target engine {row.engine}"
                ),
                manual_review_required=True,
                raw={},
            )
        return _resolve_role_local_diagnostic(
            case_dir=case_dir,
            row=row,
            schema_version=schema_version,
            metadata=_mapping(
                role_metadata,
                field=f"local_diagnostic.engine_roles.{row.engine}",
            ),
            field_prefix=f"local_diagnostic.engine_roles.{row.engine}",
        )
    if schema_version == LOCAL_DIAGNOSTIC_LEGACY_SCHEMA_VERSION:
        return _resolve_role_local_diagnostic(
            case_dir=case_dir,
            row=row,
            schema_version=schema_version,
            metadata=metadata,
            field_prefix="local_diagnostic",
        )
    raise ValueError(
        "local_diagnostic.schema_version must be one of "
        f"{LOCAL_DIAGNOSTIC_SCHEMA_VERSION}, {LOCAL_DIAGNOSTIC_LEGACY_SCHEMA_VERSION}"
    )


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
    local_diagnostic = _resolve_local_diagnostic(
        case_dir=case_dir,
        row=row,
        source_sql_path=source_sql_path,
        raw_metadata=manifest.get("local_diagnostic"),
    )

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
        local_diagnostic=local_diagnostic,
        diagnostic_mode=local_diagnostic.diagnostic_mode,
        source_reference_engine=local_diagnostic.source_reference_engine,
        source_reference_query_path=local_diagnostic.source_reference_query_path,
        target_candidate_engine=local_diagnostic.target_candidate_engine,
        target_reference_query_path=local_diagnostic.target_reference_query_path,
        target_reference_role=local_diagnostic.target_reference_role,
        checker_comparison=local_diagnostic.checker_comparison,
        local_diagnostic_boundary=local_diagnostic.local_diagnostic_boundary,
        unsupported_reason=local_diagnostic.unsupported_reason,
        manual_review_required=local_diagnostic.manual_review_required,
        resolution_status="ok",
        resolution_notes="case package assets resolved",
    )
