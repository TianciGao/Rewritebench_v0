"""Non-destructive case package v2 reference resolver and validator.

This module performs static path and manifest-shape checks only. It does not
run DB engines, execute checkers, parse retained evidence, compute metrics, or
write case-package outputs.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


SUPPORTED_SCHEMA_ENGINES = ("postgres", "mysql", "spark")
CANONICAL_VALIDATION_ENTRYPOINTS = {
    "run_validation": "validation/run_validation.sh",
    "run_plan_collection": "validation/run_plan_collection.sh",
    "run_engine_queries": "validation/run_engine_queries.py",
}
REQUIRED_TOP_LEVEL_KEYS = {
    "case_id",
    "pool",
    "primary_pool",
    "package_path",
    "source_family",
    "source_workload",
    "based_benchmark",
    "source_query_identity",
    "source_path",
    "draft_origin",
    "taxonomy",
    "sql",
    "schema",
    "witness",
    "checker",
    "validation",
    "evidence_policy",
    "status",
    "known_caveats",
    "artifact_warning",
}
OPTIONAL_TOP_LEVEL_KEYS = {"compatibility", "case_package_standard", "local_diagnostic"}
FORBIDDEN_TOP_LEVEL_KEYS = {"schema_ref", "evidence_ref", "metadata", "notes", "evidence", "runs"}
LOCAL_DIAGNOSTIC_SCHEMA_VERSION = "port_cross_dialect_diagnostic_v0"
LOCAL_DIAGNOSTIC_ALLOWED_MODES = {"same_engine", "cross_dialect_reference"}
LOCAL_DIAGNOSTIC_COMPARISON = "source_reference_result_to_target_candidate_result"
FORBIDDEN_REFERENCE_PATTERNS = (
    "sql/positives/",
    "sql/negatives/",
    "schema/postgres/",
    "schema/mysql/",
    "schema/spark/",
    "/evidence/",
    "evidence/cases/",
    "runs/",
    "metadata/",
    "notes/",
    "data/",
    "run_postgres_validation.sh",
    "run_mysql_validation.sh",
    "run_spark_validation.sh",
    "run_postgres_plan_collection.sh",
    "run_mysql_plan_collection.sh",
    "run_spark_plan_collection.sh",
)
RUN_ENGINE_QUERIES_REQUIRED_IMPORT = "sql_rewrite_bench.validation.engine_query_runner"
RUN_ENGINE_QUERIES_FORBIDDEN_MARKERS = (
    "psycopg2",
    "pymysql",
    "mysql.connector",
    "SparkSession",
    "sqlalchemy",
    "create_engine",
    "jdbc:",
    "subprocess.run",
    "subprocess.Popen",
    "password=",
    "POSTGRES_PASSWORD",
    "MYSQL_PASSWORD",
    "SPARK_HOME",
    "schema/postgres/",
    "schema/mysql/",
    "schema/spark/",
    "runs/",
    "reports/",
    "results/",
    "leaderboard",
)


@dataclass(frozen=True)
class ResolvedReference:
    field_group: str
    field: str
    observed_value: str
    resolved_path: str
    path_base: str
    required: bool
    exists: bool
    safety_status: str
    status: str
    notes: str


@dataclass(frozen=True)
class InternalFormatCheck:
    field_group: str
    field: str
    observed_value: str
    expected_shape: str
    status: str
    notes: str


@dataclass(frozen=True)
class FormatFinding:
    case_id: str
    file_path: str
    finding_type: str
    severity: str
    current_value: str
    recommended_v2_value: str
    fix_now: bool
    notes: str


@dataclass(frozen=True)
class DirectoryClassification:
    directory: str
    current_role: str
    v2_role: str
    keep_now: bool
    delete_later_condition: str
    notes: str


@dataclass
class V2ValidationResult:
    case_id: str
    case_path: str
    overall_status: str
    references: list[ResolvedReference]
    internal_checks: list[InternalFormatCheck]
    findings: list[FormatFinding]
    directory_classification: list[DirectoryClassification]

    @property
    def errors(self) -> list[str]:
        return [
            f"{ref.field}: {ref.notes}"
            for ref in self.references
            if ref.status == "fail"
        ] + [
            f"{check.field}: {check.notes}"
            for check in self.internal_checks
            if check.status == "fail"
        ]

    @property
    def warnings(self) -> list[str]:
        return [
            f"{ref.field}: {ref.notes}"
            for ref in self.references
            if ref.status == "warn"
        ] + [
            f"{check.field}: {check.notes}"
            for check in self.internal_checks
            if check.status == "warn"
        ]


def load_yaml_file(path: Path) -> dict[str, Any]:
    """Load YAML with PyYAML and fail closed if the parser is unavailable."""

    try:
        import yaml  # type: ignore
    except Exception as exc:  # pragma: no cover - environment dependent
        raise RuntimeError(f"PyYAML is required for v2 manifest validation: {exc}") from exc

    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be a mapping: {path}")
    return data


def _stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def _check(
    checks: list[InternalFormatCheck],
    findings: list[FormatFinding],
    *,
    case_id: str,
    manifest_path: Path,
    field_group: str,
    field: str,
    observed_value: Any,
    expected_shape: str,
    ok: bool,
    warning: bool = False,
    finding_type: str = "internal_format",
    recommended_v2_value: str = "",
    notes: str = "",
) -> None:
    status = "pass" if ok else ("warn" if warning else "fail")
    observed = _stringify(observed_value)
    checks.append(
        InternalFormatCheck(
            field_group=field_group,
            field=field,
            observed_value=observed,
            expected_shape=expected_shape,
            status=status,
            notes=notes,
        )
    )
    if status != "pass":
        findings.append(
            FormatFinding(
                case_id=case_id,
                file_path=str(manifest_path),
                finding_type=finding_type,
                severity="warning" if status == "warn" else "error",
                current_value=observed,
                recommended_v2_value=recommended_v2_value or expected_shape,
                fix_now=False,
                notes=notes,
            )
        )


def _resolve_path(
    *,
    repo_root: Path,
    case_dir: Path,
    field_group: str,
    field: str,
    observed_value: Any,
    path_base: str,
    required: bool,
    notes: str = "",
) -> ResolvedReference:
    raw = _stringify(observed_value).strip()
    if not raw:
        status = "fail" if required else "warn"
        return ResolvedReference(
            field_group=field_group,
            field=field,
            observed_value=raw,
            resolved_path="",
            path_base=path_base,
            required=required,
            exists=False,
            safety_status="missing",
            status=status,
            notes=notes or "missing path",
        )

    unsafe_reasons: list[str] = []
    candidate = Path(raw)
    if candidate.is_absolute():
        unsafe_reasons.append("absolute path")
    if raw.startswith("~"):
        unsafe_reasons.append("home-relative path")
    if ".." in candidate.parts:
        unsafe_reasons.append("parent-relative path")
    if "://" in raw or raw.startswith("file:"):
        unsafe_reasons.append("URI/local file path")
    if "\\" in raw:
        unsafe_reasons.append("backslash path")

    base_dir = case_dir if path_base == "case" else repo_root
    resolved = (base_dir / candidate).resolve()
    base_resolved = base_dir.resolve()
    if base_resolved not in resolved.parents and resolved != base_resolved:
        unsafe_reasons.append(f"path escapes {path_base} root")

    if unsafe_reasons:
        return ResolvedReference(
            field_group=field_group,
            field=field,
            observed_value=raw,
            resolved_path=str(resolved),
            path_base=path_base,
            required=required,
            exists=resolved.exists(),
            safety_status="unsafe",
            status="fail",
            notes="; ".join(unsafe_reasons),
        )

    exists = resolved.exists()
    if not exists and required:
        status = "fail"
        ref_notes = notes or "required path missing"
    elif not exists:
        status = "warn"
        ref_notes = notes or "optional path missing"
    else:
        status = "pass"
        ref_notes = notes

    return ResolvedReference(
        field_group=field_group,
        field=field,
        observed_value=raw,
        resolved_path=str(resolved),
        path_base=path_base,
        required=required,
        exists=exists,
        safety_status="safe",
        status=status,
        notes=ref_notes,
    )


def _load_resolved_yaml_mapping(ref: ResolvedReference) -> dict[str, Any] | None:
    """Load a resolved YAML reference after path safety/existence checks pass."""

    if ref.status == "fail" or not ref.resolved_path:
        return None
    try:
        return load_yaml_file(Path(ref.resolved_path))
    except Exception:
        return None


def _flatten_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        flattened: list[str] = []
        for item in value.values():
            flattened.extend(_flatten_strings(item))
        return flattened
    if isinstance(value, list):
        flattened = []
        for item in value:
            flattened.extend(_flatten_strings(item))
        return flattened
    return []


def _is_safe_metadata_string(value: str) -> tuple[bool, str]:
    candidate = Path(value)
    if candidate.is_absolute():
        return False, "absolute path"
    if value.startswith("~"):
        return False, "home-relative path"
    if "://" in value or value.startswith("file:"):
        return False, "URI/local file path"
    if "\\" in value:
        return False, "backslash path"
    if any(part in {"Users", "home", "tmp"} for part in candidate.parts[:2]):
        return False, "local machine/user path"
    return True, ""


def _sql_entries_ok(entries: Any, expected_path: str) -> bool:
    if not isinstance(entries, list) or not entries:
        return False
    for entry in entries:
        if not isinstance(entry, dict):
            return False
        if not isinstance(entry.get("id"), str) or not entry["id"].strip():
            return False
        if entry.get("path") != expected_path:
            return False
        if not isinstance(entry.get("status"), str) or not entry["status"].strip():
            return False
    return True


def _check_run_engine_queries_shim(
    *,
    checks: list[InternalFormatCheck],
    findings: list[FormatFinding],
    case_id: str,
    manifest_path: Path,
    case_dir: Path,
    observed_value: Any,
) -> None:
    """Statically require a short case-local shim, not copied runner logic."""

    if observed_value != CANONICAL_VALIDATION_ENTRYPOINTS["run_engine_queries"]:
        return

    shim_path = case_dir / CANONICAL_VALIDATION_ENTRYPOINTS["run_engine_queries"]
    if not shim_path.exists():
        return

    try:
        text = shim_path.read_text(encoding="utf-8")
    except Exception as exc:
        _check(
            checks,
            findings,
            case_id=case_id,
            manifest_path=manifest_path,
            field_group="validation",
            field="validation.run_engine_queries.thin_shim",
            observed_value=f"unreadable: {exc}",
            expected_shape="readable thin shim",
            ok=False,
            finding_type="validation_thin_shim",
            notes="run_engine_queries.py must be readable for static shim validation",
        )
        return

    lines = [line for line in text.splitlines() if line.strip() and not line.lstrip().startswith("#")]
    has_required_import = RUN_ENGINE_QUERIES_REQUIRED_IMPORT in text
    hardcoded_case_id = any(
        marker in text
        for marker in ("PERF_", "CONS_", "PORT_", "LONGTAIL_")
    )
    forbidden_markers = [marker for marker in RUN_ENGINE_QUERIES_FORBIDDEN_MARKERS if marker in text]
    ok = has_required_import and not hardcoded_case_id and not forbidden_markers and len(lines) <= 12
    notes = "run_engine_queries.py delegates to shared runner"
    if not ok:
        reasons: list[str] = []
        if not has_required_import:
            reasons.append("missing shared runner import")
        if hardcoded_case_id:
            reasons.append("hardcoded case ID marker")
        if forbidden_markers:
            reasons.append(f"forbidden implementation/output marker(s): {', '.join(forbidden_markers)}")
        if len(lines) > 12:
            reasons.append(f"too many non-comment lines for thin shim: {len(lines)}")
        notes = "; ".join(reasons)

    _check(
        checks,
        findings,
        case_id=case_id,
        manifest_path=shim_path,
        field_group="validation",
        field="validation.run_engine_queries.thin_shim",
        observed_value=f"{len(lines)} non-comment lines",
        expected_shape="short shim importing sql_rewrite_bench.validation.engine_query_runner and delegating",
        ok=ok,
        finding_type="validation_thin_shim",
        notes=notes,
    )


def _check_local_diagnostic_metadata(
    *,
    checks: list[InternalFormatCheck],
    findings: list[FormatFinding],
    references: list[ResolvedReference],
    case_id: str,
    manifest_path: Path,
    case_dir: Path,
    repo_root: Path,
    observed_value: Any,
) -> None:
    """Validate optional local diagnostic role metadata without running engines."""

    if observed_value is None:
        return
    if not isinstance(observed_value, dict):
        _check(
            checks,
            findings,
            case_id=case_id,
            manifest_path=manifest_path,
            field_group="local_diagnostic",
            field="local_diagnostic",
            observed_value=type(observed_value).__name__,
            expected_shape="mapping",
            ok=False,
            finding_type="local_diagnostic_shape",
            notes="local_diagnostic must be a mapping when present",
        )
        return

    schema_version = observed_value.get("schema_version")
    _check(
        checks,
        findings,
        case_id=case_id,
        manifest_path=manifest_path,
        field_group="local_diagnostic",
        field="local_diagnostic.schema_version",
        observed_value=schema_version,
        expected_shape=LOCAL_DIAGNOSTIC_SCHEMA_VERSION,
        ok=schema_version == LOCAL_DIAGNOSTIC_SCHEMA_VERSION,
        finding_type="local_diagnostic_schema",
        notes="local diagnostic metadata must use the approved schema version",
    )
    diagnostic_mode = observed_value.get("diagnostic_mode")
    _check(
        checks,
        findings,
        case_id=case_id,
        manifest_path=manifest_path,
        field_group="local_diagnostic",
        field="local_diagnostic.diagnostic_mode",
        observed_value=diagnostic_mode,
        expected_shape="same_engine or cross_dialect_reference",
        ok=diagnostic_mode in LOCAL_DIAGNOSTIC_ALLOWED_MODES,
        finding_type="local_diagnostic_mode",
        notes="unsupported local diagnostic mode",
    )

    source_reference = observed_value.get("source_reference")
    source_ok = isinstance(source_reference, dict)
    _check(
        checks,
        findings,
        case_id=case_id,
        manifest_path=manifest_path,
        field_group="local_diagnostic",
        field="local_diagnostic.source_reference",
        observed_value=type(source_reference).__name__,
        expected_shape="mapping",
        ok=source_ok,
        finding_type="local_diagnostic_shape",
        notes="source_reference role block is required",
    )
    if source_ok:
        _check_local_diagnostic_role_block(
            checks=checks,
            findings=findings,
            references=references,
            case_id=case_id,
            manifest_path=manifest_path,
            case_dir=case_dir,
            repo_root=repo_root,
            field_prefix="local_diagnostic.source_reference",
            block=source_reference,
            expected_role="source_reference",
            path_field="query",
            path_required=True,
        )

    target_candidate = observed_value.get("target_candidate")
    target_ok = isinstance(target_candidate, dict)
    _check(
        checks,
        findings,
        case_id=case_id,
        manifest_path=manifest_path,
        field_group="local_diagnostic",
        field="local_diagnostic.target_candidate",
        observed_value=type(target_candidate).__name__,
        expected_shape="mapping",
        ok=target_ok,
        finding_type="local_diagnostic_shape",
        notes="target_candidate role block is required",
    )
    if target_ok:
        _check_local_diagnostic_role_block(
            checks=checks,
            findings=findings,
            references=references,
            case_id=case_id,
            manifest_path=manifest_path,
            case_dir=case_dir,
            repo_root=repo_root,
            field_prefix="local_diagnostic.target_candidate",
            block=target_candidate,
            expected_role="adapter_output",
            path_field=None,
            path_required=False,
        )

    target_reference = observed_value.get("target_reference")
    if target_reference is not None:
        target_reference_ok = isinstance(target_reference, dict)
        _check(
            checks,
            findings,
            case_id=case_id,
            manifest_path=manifest_path,
            field_group="local_diagnostic",
            field="local_diagnostic.target_reference",
            observed_value=type(target_reference).__name__,
            expected_shape="mapping",
            ok=target_reference_ok,
            finding_type="local_diagnostic_shape",
            notes="target_reference must be a mapping when present",
        )
        if target_reference_ok:
            _check_local_diagnostic_role_block(
                checks=checks,
                findings=findings,
                references=references,
                case_id=case_id,
                manifest_path=manifest_path,
                case_dir=case_dir,
                repo_root=repo_root,
                field_prefix="local_diagnostic.target_reference",
                block=target_reference,
                expected_role="positive_reference",
                path_field="query",
                path_required=True,
            )
            _check(
                checks,
                findings,
                case_id=case_id,
                manifest_path=manifest_path,
                field_group="local_diagnostic",
                field="local_diagnostic.target_reference.use_for_checker_oracle",
                observed_value=target_reference.get("use_for_checker_oracle"),
                expected_shape="false",
                ok=target_reference.get("use_for_checker_oracle") is False,
                finding_type="local_diagnostic_boundary",
                notes="positive reference must not replace source-reference checker oracle",
            )
            _check(
                checks,
                findings,
                case_id=case_id,
                manifest_path=manifest_path,
                field_group="local_diagnostic",
                field="local_diagnostic.target_reference.use_for_sanity_control",
                observed_value=type(target_reference.get("use_for_sanity_control")).__name__,
                expected_shape="boolean",
                ok=isinstance(target_reference.get("use_for_sanity_control"), bool),
                finding_type="local_diagnostic_boundary",
                notes="sanity-control flag must be explicit when target_reference exists",
            )

    checker = observed_value.get("checker")
    checker_ok = isinstance(checker, dict)
    _check(
        checks,
        findings,
        case_id=case_id,
        manifest_path=manifest_path,
        field_group="local_diagnostic",
        field="local_diagnostic.checker",
        observed_value=type(checker).__name__,
        expected_shape="mapping",
        ok=checker_ok,
        finding_type="local_diagnostic_shape",
        notes="checker comparison block is required",
    )
    if checker_ok:
        comparison = checker.get("comparison")
        _check(
            checks,
            findings,
            case_id=case_id,
            manifest_path=manifest_path,
            field_group="local_diagnostic",
            field="local_diagnostic.checker.comparison",
            observed_value=comparison,
            expected_shape=LOCAL_DIAGNOSTIC_COMPARISON,
            ok=comparison == LOCAL_DIAGNOSTIC_COMPARISON,
            finding_type="local_diagnostic_checker",
            notes="checker must compare declared source-reference and target-candidate artifacts",
        )

    boundary = observed_value.get("boundary")
    boundary_ok = isinstance(boundary, dict)
    _check(
        checks,
        findings,
        case_id=case_id,
        manifest_path=manifest_path,
        field_group="local_diagnostic",
        field="local_diagnostic.boundary",
        observed_value=type(boundary).__name__,
        expected_shape="mapping",
        ok=boundary_ok,
        finding_type="local_diagnostic_boundary",
        notes="local diagnostic boundary block is required",
    )
    if boundary_ok:
        for field, expected in {
            "local_diagnostic_only": True,
            "official_metric_input": False,
            "paper_result_input": False,
            "reports_results_update": False,
            "leaderboard_input": False,
        }.items():
            _check(
                checks,
                findings,
                case_id=case_id,
                manifest_path=manifest_path,
                field_group="local_diagnostic",
                field=f"local_diagnostic.boundary.{field}",
                observed_value=boundary.get(field),
                expected_shape=_stringify(expected),
                ok=boundary.get(field) is expected,
                finding_type="local_diagnostic_boundary",
                notes="local diagnostic metadata must remain local-only",
            )


def _check_local_diagnostic_role_block(
    *,
    checks: list[InternalFormatCheck],
    findings: list[FormatFinding],
    references: list[ResolvedReference],
    case_id: str,
    manifest_path: Path,
    case_dir: Path,
    repo_root: Path,
    field_prefix: str,
    block: dict[str, Any],
    expected_role: str,
    path_field: str | None,
    path_required: bool,
) -> None:
    _check(
        checks,
        findings,
        case_id=case_id,
        manifest_path=manifest_path,
        field_group="local_diagnostic",
        field=f"{field_prefix}.role",
        observed_value=block.get("role"),
        expected_shape=expected_role,
        ok=block.get("role") == expected_role,
        finding_type="local_diagnostic_role",
        notes="local diagnostic roles must be explicit",
    )
    _check(
        checks,
        findings,
        case_id=case_id,
        manifest_path=manifest_path,
        field_group="local_diagnostic",
        field=f"{field_prefix}.engine",
        observed_value=block.get("engine"),
        expected_shape="postgres, mysql, or spark",
        ok=block.get("engine") in SUPPORTED_SCHEMA_ENGINES,
        finding_type="local_diagnostic_engine",
        notes="local diagnostic engine must be explicit and supported",
    )
    if path_field is not None:
        references.append(
            _resolve_path(
                repo_root=repo_root,
                case_dir=case_dir,
                field_group="local_diagnostic",
                field=f"{field_prefix}.{path_field}",
                observed_value=block.get(path_field),
                path_base="case",
                required=path_required,
            )
        )


def resolve_case_package_v2(
    *,
    repo_root: Path,
    case_path: Path,
) -> V2ValidationResult:
    """Resolve and statically validate v2 references for one case package."""

    repo_root = repo_root.resolve()
    case_dir = (repo_root / case_path).resolve() if not case_path.is_absolute() else case_path.resolve()
    manifest_path = case_dir / "manifest.yaml"
    manifest = load_yaml_file(manifest_path)
    case_id = _stringify(manifest.get("case_id") or case_dir.name)
    expected_pool = case_dir.parent.name
    expected_package_path = f"cases/{expected_pool}/{case_dir.name}"

    references: list[ResolvedReference] = []
    checks: list[InternalFormatCheck] = []
    findings: list[FormatFinding] = []

    for key in sorted(REQUIRED_TOP_LEVEL_KEYS):
        _check(
            checks,
            findings,
            case_id=case_id,
            manifest_path=manifest_path,
            field_group="top_level",
            field=key,
            observed_value="present" if key in manifest else "missing",
            expected_shape="required semantic v2 top-level section",
            ok=key in manifest,
            finding_type="required_top_level_key",
            notes="semantic v2 manifest requires this section",
        )
    for key in sorted(manifest):
        ok = key in REQUIRED_TOP_LEVEL_KEYS or key in OPTIONAL_TOP_LEVEL_KEYS
        _check(
            checks,
            findings,
            case_id=case_id,
            manifest_path=manifest_path,
            field_group="top_level",
            field=key,
            observed_value=key,
            expected_shape="approved semantic v2 top-level key",
            ok=ok,
            finding_type="top_level_key",
            notes="forbidden compatibility key retained" if key in FORBIDDEN_TOP_LEVEL_KEYS else "unapproved top-level key",
        )
    _check_local_diagnostic_metadata(
        checks=checks,
        findings=findings,
        references=references,
        case_id=case_id,
        manifest_path=manifest_path,
        case_dir=case_dir,
        repo_root=repo_root,
        observed_value=manifest.get("local_diagnostic"),
    )

    semantic_required = {
        "case_id": case_id == case_dir.name,
        "pool": manifest.get("pool") == expected_pool,
        "primary_pool": manifest.get("primary_pool") == expected_pool,
        "package_path": manifest.get("package_path") == expected_package_path,
        "source_family": isinstance(manifest.get("source_family"), str) and bool(manifest["source_family"].strip()),
        "based_benchmark": isinstance(manifest.get("based_benchmark"), str) and bool(manifest["based_benchmark"].strip()),
        "source_path": isinstance(manifest.get("source_path"), str) and bool(manifest["source_path"].strip()),
        "status": isinstance(manifest.get("status"), str) and bool(manifest["status"].strip()),
    }
    for field, ok in semantic_required.items():
        _check(
            checks,
            findings,
            case_id=case_id,
            manifest_path=manifest_path,
            field_group="semantic",
            field=field,
            observed_value=manifest.get(field),
            expected_shape="recovered non-empty semantic field",
            ok=ok,
            finding_type="semantic_field",
            notes="field must be recovered from branch history or registry",
        )
    for field in ("source_workload", "source_query_identity", "draft_origin", "artifact_warning"):
        _check(
            checks,
            findings,
            case_id=case_id,
            manifest_path=manifest_path,
            field_group="semantic",
            field=field,
            observed_value=type(manifest.get(field)).__name__,
            expected_shape="mapping",
            ok=isinstance(manifest.get(field), dict) and bool(manifest.get(field)),
            finding_type="semantic_field",
            notes="semantic contract requires a non-empty mapping",
        )
    _check(
        checks,
        findings,
        case_id=case_id,
        manifest_path=manifest_path,
        field_group="semantic",
        field="known_caveats",
        observed_value=type(manifest.get("known_caveats")).__name__,
        expected_shape="list",
        ok=isinstance(manifest.get("known_caveats"), list),
        finding_type="semantic_field",
        notes="known caveats must be explicit, even when empty",
    )

    taxonomy = manifest.get("taxonomy")
    taxonomy_ok = isinstance(taxonomy, dict)
    _check(
        checks,
        findings,
        case_id=case_id,
        manifest_path=manifest_path,
        field_group="taxonomy",
        field="taxonomy",
        observed_value=type(taxonomy).__name__,
        expected_shape="mapping with sql_feature, rewrite_opportunity, portability",
        ok=taxonomy_ok,
        finding_type="taxonomy",
        notes="taxonomy must be restored, not inferred from README alone",
    )
    if isinstance(taxonomy, dict):
        for group, fields in {
            "sql_feature": ("primary", "secondary"),
            "rewrite_opportunity": ("primary", "secondary"),
            "portability": ("confirmed", "suspected"),
        }.items():
            section = taxonomy.get(group)
            _check(
                checks,
                findings,
                case_id=case_id,
                manifest_path=manifest_path,
                field_group="taxonomy",
                field=f"taxonomy.{group}",
                observed_value=type(section).__name__,
                expected_shape="mapping",
                ok=isinstance(section, dict),
                finding_type="taxonomy",
                notes="required taxonomy group missing or malformed",
            )
            if isinstance(section, dict):
                for item in fields:
                    values = section.get(item)
                    _check(
                        checks,
                        findings,
                        case_id=case_id,
                        manifest_path=manifest_path,
                        field_group="taxonomy",
                        field=f"taxonomy.{group}.{item}",
                        observed_value=type(values).__name__,
                        expected_shape="list",
                        ok=isinstance(values, list),
                        finding_type="taxonomy",
                        notes="taxonomy value must be an explicit list",
                    )

    for value in _flatten_strings(manifest):
        safe, reason = _is_safe_metadata_string(value)
        if not safe:
            _check(
                checks,
                findings,
                case_id=case_id,
                manifest_path=manifest_path,
                field_group="safety",
                field="manifest.string_safety",
                observed_value=value,
                expected_shape="no absolute/local/URI paths",
                ok=False,
                finding_type="unsafe_manifest_string",
                notes=reason,
            )
        for pattern in FORBIDDEN_REFERENCE_PATTERNS:
            if pattern in value:
                _check(
                    checks,
                    findings,
                    case_id=case_id,
                    manifest_path=manifest_path,
                    field_group="compatibility_refs",
                    field="manifest.deleted_path_reference",
                    observed_value=value,
                    expected_shape=f"no references containing {pattern}",
                    ok=False,
                    finding_type="deleted_path_reference",
                    notes="semantic manifest must not reference deleted compatibility surfaces",
                )

    sql = manifest.get("sql") if isinstance(manifest.get("sql"), dict) else {}
    source = sql.get("source") if isinstance(sql, dict) else None
    references.append(
        _resolve_path(
            repo_root=repo_root,
            case_dir=case_dir,
            field_group="sql",
            field="sql.source",
            observed_value=source,
            path_base="case",
            required=True,
        )
    )
    _check(
        checks,
        findings,
        case_id=case_id,
        manifest_path=manifest_path,
        field_group="sql",
        field="sql.source",
        observed_value=source,
        expected_shape="sql/source.sql",
        ok=source == "sql/source.sql",
        finding_type="sql_shape",
        notes="source SQL must use direct clean v2 path",
    )
    positive_rewrites = sql.get("positive_rewrites") if isinstance(sql, dict) else None
    hard_negatives = sql.get("hard_negatives") if isinstance(sql, dict) else None
    _check(
        checks,
        findings,
        case_id=case_id,
        manifest_path=manifest_path,
        field_group="sql",
        field="sql.positive_rewrites",
        observed_value=type(positive_rewrites).__name__,
        expected_shape="list of mappings with id, path, status",
        ok=_sql_entries_ok(positive_rewrites, "sql/pos_01.sql"),
        finding_type="sql_shape",
        notes="positive rewrite entries must use semantic object form",
    )
    _check(
        checks,
        findings,
        case_id=case_id,
        manifest_path=manifest_path,
        field_group="sql",
        field="sql.hard_negatives",
        observed_value=type(hard_negatives).__name__,
        expected_shape="list of mappings with id, path, status",
        ok=_sql_entries_ok(hard_negatives, "sql/neg_01.sql"),
        finding_type="sql_shape",
        notes="hard negative entries must use semantic object form",
    )
    if isinstance(positive_rewrites, list):
        for index, entry in enumerate(positive_rewrites, start=1):
            path_value = entry.get("path") if isinstance(entry, dict) else None
            references.append(
                _resolve_path(
                    repo_root=repo_root,
                    case_dir=case_dir,
                    field_group="sql",
                    field=f"sql.positive_rewrites[{index}].path",
                    observed_value=path_value,
                    path_base="case",
                    required=True,
                )
            )
    if isinstance(hard_negatives, list):
        for index, entry in enumerate(hard_negatives, start=1):
            path_value = entry.get("path") if isinstance(entry, dict) else None
            references.append(
                _resolve_path(
                    repo_root=repo_root,
                    case_dir=case_dir,
                    field_group="sql",
                    field=f"sql.hard_negatives[{index}].path",
                    observed_value=path_value,
                    path_base="case",
                    required=True,
                )
            )

    checker = manifest.get("checker") if isinstance(manifest.get("checker"), dict) else {}
    checker_specs = [
        ("checker.checker", checker.get("checker"), "checker/checker.yaml"),
        ("checker.normalization", checker.get("normalization"), "checker/normalization.yaml"),
        ("checker.compare_config", checker.get("compare_config"), "checker/compare_config.yaml"),
        ("checker.expected_rejections", checker.get("expected_rejections"), "checker/expected_rejections.yaml"),
    ]
    for field, value, expected in checker_specs:
        references.append(
            _resolve_path(
                repo_root=repo_root,
                case_dir=case_dir,
                field_group="checker",
                field=field,
                observed_value=value,
                path_base="case",
                required=True,
            )
        )
        _check(
            checks,
            findings,
            case_id=case_id,
            manifest_path=manifest_path,
            field_group="checker",
            field=field,
            observed_value=value,
            expected_shape=expected,
            ok=value == expected,
            finding_type="checker_reference_shape",
            notes="checker manifest must use config-only clean v2 paths",
        )

    schema = manifest.get("schema") if isinstance(manifest.get("schema"), dict) else {}
    case_schema_profile = schema.get("profile") if isinstance(schema, dict) else None
    external_schema_profile = schema.get("external_profile") if isinstance(schema, dict) else None
    case_profile_ref = _resolve_path(
        repo_root=repo_root,
        case_dir=case_dir,
        field_group="schema",
        field="schema.profile",
        observed_value=case_schema_profile,
        path_base="case",
        required=True,
        notes="clean v2 keeps only schema/schema_profile.yaml case-local",
    )
    external_profile_ref = _resolve_path(
        repo_root=repo_root,
        case_dir=case_dir,
        field_group="schema",
        field="schema.external_profile",
        observed_value=external_schema_profile,
        path_base="repo",
        required=True,
    )
    references.extend([case_profile_ref, external_profile_ref])
    _check(
        checks,
        findings,
        case_id=case_id,
        manifest_path=manifest_path,
        field_group="schema",
        field="schema.profile",
        observed_value=case_schema_profile,
        expected_shape="schema/schema_profile.yaml",
        ok=case_schema_profile == "schema/schema_profile.yaml",
        finding_type="schema_shape",
        notes="case-local schema reference must be profile-only",
    )
    _check(
        checks,
        findings,
        case_id=case_id,
        manifest_path=manifest_path,
        field_group="schema",
        field="schema.external_profile",
        observed_value=external_schema_profile,
        expected_shape="schemas/<SCHEMA_ID>/schema_profile.yaml",
        ok=isinstance(external_schema_profile, str)
        and external_schema_profile.startswith("schemas/")
        and external_schema_profile.endswith("/schema_profile.yaml"),
        finding_type="schema_shape",
        notes="external profile must be the schema source of truth",
    )
    external_profile_data = _load_resolved_yaml_mapping(external_profile_ref)
    engines = (
        external_profile_data.get("engines")
        if isinstance(external_profile_data, dict) and isinstance(external_profile_data.get("engines"), dict)
        else None
    )
    _check(
        checks,
        findings,
        case_id=case_id,
        manifest_path=manifest_path,
        field_group="schema",
        field="schema.external_profile.parse",
        observed_value="mapping" if isinstance(external_profile_data, dict) else "unparseable",
        expected_shape="external schema_profile.yaml mapping with engines",
        ok=isinstance(engines, dict) and bool(engines),
        finding_type="schema_profile_parse",
        notes="external schema profile must resolve DDL/load assets by engine",
    )
    if isinstance(engines, dict):
        for engine, engine_map in sorted(engines.items()):
            if not isinstance(engine_map, dict):
                _check(
                    checks,
                    findings,
                    case_id=case_id,
                    manifest_path=manifest_path,
                    field_group="schema",
                    field=f"schema.external_profile.engines.{engine}",
                    observed_value=type(engine_map).__name__,
                    expected_shape="mapping with ddl/load",
                    ok=False,
                    finding_type="schema_profile_engine_shape",
                    notes="engine profile entry must be a mapping",
                )
                continue
            for kind in ("ddl", "load"):
                value = engine_map.get(kind)
                references.append(
                    _resolve_path(
                        repo_root=repo_root,
                        case_dir=case_dir,
                        field_group="schema",
                        field=f"schema.external_profile.engines.{engine}.{kind}",
                        observed_value=value,
                        path_base="repo",
                        required=True,
                    )
                )

    witness = manifest.get("witness") if isinstance(manifest.get("witness"), dict) else {}
    witness_expectations = {
        "witness.mode": (witness.get("mode"), "source_as_oracle"),
        "witness.data_profile_status": (witness.get("data_profile_status"), "external_or_generated"),
        "witness.correct_result_status": (
            witness.get("correct_result_status"),
            "not_required_for_runtime_checker",
        ),
    }
    for field, (value, expected) in witness_expectations.items():
        _check(
            checks,
            findings,
            case_id=case_id,
            manifest_path=manifest_path,
            field_group="witness",
            field=field,
            observed_value=value,
            expected_shape=expected,
            ok=value == expected,
            finding_type="witness_policy",
            notes="witness policy must use source-as-oracle runtime semantics",
        )
    for optional_field in ("witness_profile", "data_profile", "correct_result"):
        value = witness.get(optional_field)
        if value:
            references.append(
                _resolve_path(
                    repo_root=repo_root,
                    case_dir=case_dir,
                    field_group="witness",
                    field=f"witness.{optional_field}",
                    observed_value=value,
                    path_base="case",
                    required=False,
                    notes="optional static witness asset",
                )
            )

    validation = manifest.get("validation") if isinstance(manifest.get("validation"), dict) else {}
    for key, expected in CANONICAL_VALIDATION_ENTRYPOINTS.items():
        value = validation.get(key) if isinstance(validation, dict) else None
        references.append(
            _resolve_path(
                repo_root=repo_root,
                case_dir=case_dir,
                field_group="validation",
                field=f"validation.{key}",
                observed_value=value,
                path_base="case",
                required=True,
            )
        )
        _check(
            checks,
            findings,
            case_id=case_id,
            manifest_path=manifest_path,
            field_group="validation",
            field=f"validation.{key}",
            observed_value=value,
            expected_shape=expected,
            ok=value == expected,
            finding_type="validation_reference_shape",
            notes="validation must use the three-file clean v2 entrypoint contract",
        )
        if key == "run_engine_queries":
            _check_run_engine_queries_shim(
                checks=checks,
                findings=findings,
                case_id=case_id,
                manifest_path=manifest_path,
                case_dir=case_dir,
                observed_value=value,
            )

    evidence_policy = manifest.get("evidence_policy")
    evidence_ok = isinstance(evidence_policy, dict)
    _check(
        checks,
        findings,
        case_id=case_id,
        manifest_path=manifest_path,
        field_group="evidence_policy",
        field="evidence_policy",
        observed_value=type(evidence_policy).__name__,
        expected_shape="mapping",
        ok=evidence_ok,
        finding_type="evidence_policy",
        notes="clean v2 uses regeneration-first evidence_policy instead of evidence_ref",
    )
    if isinstance(evidence_policy, dict):
        static_case_evidence = evidence_policy.get("static_case_evidence")
        regeneration_policy = evidence_policy.get("regeneration_policy")
        retained_static_artifacts = evidence_policy.get("retained_static_artifacts")
        _check(
            checks,
            findings,
            case_id=case_id,
            manifest_path=manifest_path,
            field_group="evidence_policy",
            field="evidence_policy.static_case_evidence",
            observed_value=static_case_evidence,
            expected_shape="not_required or optional_retained",
            ok=static_case_evidence in {"not_required", "optional_retained"},
            finding_type="evidence_policy",
            notes="static evidence must not be mandatory in clean v2",
        )
        _check(
            checks,
            findings,
            case_id=case_id,
            manifest_path=manifest_path,
            field_group="evidence_policy",
            field="evidence_policy.regeneration_policy",
            observed_value=regeneration_policy,
            expected_shape="regenerable_by_validation_and_report_scripts",
            ok=regeneration_policy == "regenerable_by_validation_and_report_scripts",
            finding_type="evidence_policy",
            notes="evidence should be regenerated rather than required as static artifact",
        )
        retained_ok = retained_static_artifacts == "none" or isinstance(retained_static_artifacts, list)
        _check(
            checks,
            findings,
            case_id=case_id,
            manifest_path=manifest_path,
            field_group="evidence_policy",
            field="evidence_policy.retained_static_artifacts",
            observed_value=retained_static_artifacts,
            expected_shape="none or explicit retained artifact list",
            ok=retained_ok,
            finding_type="evidence_policy",
            notes="retained static artifacts must be explicit if present",
        )

    readme_path = case_dir / "README.md"
    if readme_path.exists():
        readme_text = readme_path.read_text(encoding="utf-8")
        expected_headings = [
            "## Purpose",
            "## Release Scope",
            "## Package Contents",
            "## Evidence Boundary",
            "## Benchmark Boundary",
            "## Notes / Future Review Status",
        ]
        missing = [heading for heading in expected_headings if heading not in readme_text]
        _check(
            checks,
            findings,
            case_id=case_id,
            manifest_path=readme_path,
            field_group="README",
            field="README.headings",
            observed_value=", ".join(missing) if missing else "all present",
            expected_shape="public-readable v2 README headings",
            ok=not missing,
            warning=bool(missing),
            finding_type="readme_closeout",
            notes="README missing recommended v2 closeout headings" if missing else "",
        )

    directory_classification = classify_case_directories(case_dir)
    overall_status = "fail" if any(ref.status == "fail" for ref in references) or any(
        check.status == "fail" for check in checks
    ) else "pass"
    return V2ValidationResult(
        case_id=case_id,
        case_path=str(case_dir),
        overall_status=overall_status,
        references=references,
        internal_checks=checks,
        findings=findings,
        directory_classification=directory_classification,
    )


def classify_case_directories(case_dir: Path) -> list[DirectoryClassification]:
    """Classify visible case-local directories for clean v2 review."""

    specs = {
        "sql": (
            "direct source/positive/negative SQL paths",
            "required",
            True,
            "keep direct files; delete nested positives/negatives after refs are removed",
            "clean v2 keeps sql/source.sql, sql/pos_01.sql, sql/neg_01.sql",
        ),
        "schema": (
            "case-local schema profile only",
            "required_profile_only",
            True,
            "keep schema/schema_profile.yaml only; engine DDL/load live under schemas/",
            "clean v2 case-local schema contains no engine subdirectories",
        ),
        "checker": (
            "checker configuration layer",
            "required_config_only",
            True,
            "keep YAML config; do not keep per-case Python implementations",
            "checker logic is shared outside case packages",
        ),
        "validation": (
            "validation entrypoint wrappers",
            "required_thin_wrappers",
            True,
            "keep run_validation.sh, run_plan_collection.sh, and thin run_engine_queries.py",
            "wrappers must not execute DB/checker in static validation",
        ),
        "witness": (
            "optional source-as-oracle witness metadata",
            "optional",
            True,
            "static witness assets remain optional and must not be fabricated",
            "absence is allowed under source-as-oracle runtime policy",
        ),
        "evidence": (
            "legacy static evidence surface",
            "not_required",
            False,
            "remove after references are migrated to evidence_policy",
            "clean v2 regenerates evidence through validation/report scripts",
        ),
        "metadata": (
            "legacy semantic sidecar",
            "not_required_after_manifest_repair",
            False,
            "delete after manifest semantic fields are restored",
            "semantic source of truth belongs in manifest contract",
        ),
        "notes": (
            "legacy copied notes",
            "not_required",
            False,
            "delete after README/manifest captures public wording",
            "historical audit notes stay under audits/",
        ),
        "data": (
            "legacy fixtures",
            "not_required_unless_witness_policy_requires",
            False,
            "manual review if non-placeholder fixture data appears",
            "source-as-oracle policy should not fabricate fixtures",
        ),
        "runs": (
            "case-local run outputs",
            "not_required",
            False,
            "delete empty/placeholder only after audit; map retained evidence first",
            "new run outputs belong under top-level runs/user/<run_id>/ and are not committed",
        ),
    }
    classifications: list[DirectoryClassification] = []
    for name, (current_role, v2_role, keep_now, delete_later_condition, notes) in specs.items():
        directory = case_dir / name
        if directory.exists():
            classifications.append(
                DirectoryClassification(
                    directory=name,
                    current_role=current_role,
                    v2_role=v2_role,
                    keep_now=keep_now,
                    delete_later_condition=delete_later_condition,
                    notes=notes,
                )
            )
    for child in sorted(case_dir.iterdir()):
        if not child.is_dir() or child.name in specs:
            continue
        classifications.append(
            DirectoryClassification(
                directory=child.name,
                current_role="case-local extra directory",
                v2_role="manual_review_required",
                keep_now=True,
                delete_later_condition="classify before cleanup",
                notes="unrecognized directory in case package",
            )
        )
    return classifications
