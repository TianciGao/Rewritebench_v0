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
}

APPROVED_TOP_LEVEL_KEYS = {
    "case_id",
    "pool",
    "case_package_standard",
    "sql",
    "schema_ref",
    "evidence_ref",
    "checker",
    "validation",
    "witness",
    "metadata",
    "notes",
    "claim_boundaries",
    "benchmark_scope",
    "denominator_eligibility",
    "source_family",
    "source_id",
    "source_name",
}

COMPATIBILITY_TOP_LEVEL_KEYS = {
    "status",
    "canonical_layout",
    "compatibility",
    "source_seed",
    "source_entry",
    "source_materialization",
    "engine_support",
    "schema",
    "evidence",
    "artifact_paths",
    "performance_boundary",
}


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


def _nested_get(mapping: dict[str, Any], dotted: str) -> Any:
    current: Any = mapping
    for part in dotted.split("."):
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    return current


def _stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def _entry_path(entry: Any) -> tuple[str | None, str]:
    if isinstance(entry, str):
        return entry, "canonical string path"
    if isinstance(entry, dict):
        value = entry.get("path")
        if isinstance(value, str):
            return value, "compatibility object with path"
    return None, "unsupported entry shape"


def _is_lowercase_status(value: Any) -> bool:
    if isinstance(value, bool):
        return True
    if value is None:
        return True
    if not isinstance(value, str):
        return True
    return value == value.lower() and " " not in value


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

    references: list[ResolvedReference] = []
    checks: list[InternalFormatCheck] = []
    findings: list[FormatFinding] = []

    for key in sorted(manifest):
        if key in APPROVED_TOP_LEVEL_KEYS:
            continue
        _check(
            checks,
            findings,
            case_id=case_id,
            manifest_path=manifest_path,
            field_group="top_level",
            field=key,
            observed_value=key,
            expected_shape="approved v2 top-level key or documented compatibility key",
            ok=key in COMPATIBILITY_TOP_LEVEL_KEYS,
            warning=key in COMPATIBILITY_TOP_LEVEL_KEYS,
            finding_type="compatibility_top_level_key",
            notes="compatibility top-level key retained during branch adoption"
            if key in COMPATIBILITY_TOP_LEVEL_KEYS
            else "unapproved top-level key",
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
        notes="source SQL should use direct v2 path",
    )

    for group_name, prefix in (("positives", "pos_"), ("negatives", "neg_")):
        entries = sql.get(group_name, []) if isinstance(sql, dict) else []
        if not isinstance(entries, list):
            entries = []
        for index, entry in enumerate(entries, start=1):
            path_value, shape_note = _entry_path(entry)
            field = f"sql.{group_name}[{index}]"
            expected_prefix = f"sql/{prefix}"
            references.append(
                _resolve_path(
                    repo_root=repo_root,
                    case_dir=case_dir,
                    field_group="sql",
                    field=field,
                    observed_value=path_value,
                    path_base="case",
                    required=True,
                    notes=shape_note if shape_note != "canonical string path" else "",
                )
            )
            direct_ok = isinstance(path_value, str) and path_value.startswith(expected_prefix) and "/" not in path_value[len("sql/") :]
            _check(
                checks,
                findings,
                case_id=case_id,
                manifest_path=manifest_path,
                field_group="sql",
                field=field,
                observed_value=path_value if path_value is not None else entry,
                expected_shape=f"{expected_prefix}NN.sql as direct case-local path",
                ok=direct_ok,
                warning=path_value is not None,
                finding_type="sql_entry_shape",
                notes=shape_note,
            )
            if isinstance(entry, dict):
                _check(
                    checks,
                    findings,
                    case_id=case_id,
                    manifest_path=manifest_path,
                    field_group="sql",
                    field=f"{field}.entry_shape",
                    observed_value="mapping",
                    expected_shape="string path in canonical v2",
                    ok=False,
                    warning=True,
                    finding_type="compatibility_sql_entry_shape",
                    recommended_v2_value=path_value or "",
                    notes="mapping form retained for metadata/legacy compatibility",
                )

    checker = manifest.get("checker") if isinstance(manifest.get("checker"), dict) else {}
    checker_specs = [
        ("checker.config", checker.get("config"), checker.get("checker"), "checker/checker.yaml"),
        ("checker.normalization", checker.get("normalization"), None, "checker/normalization.yaml"),
        ("checker.compare_config", checker.get("compare_config"), None, "checker/compare_config.yaml"),
        (
            "checker.expected_rejections",
            checker.get("expected_rejections"),
            None,
            "checker/expected_rejections.yaml",
        ),
    ]
    for field, canonical, fallback, expected in checker_specs:
        value = canonical if canonical is not None else fallback
        references.append(
            _resolve_path(
                repo_root=repo_root,
                case_dir=case_dir,
                field_group="checker",
                field=field,
                observed_value=value,
                path_base="case",
                required=True,
                notes="compatibility fallback from checker.checker" if canonical is None and fallback else "",
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
            ok=canonical == expected,
            warning=value == expected,
            finding_type="checker_reference_shape",
            notes="canonical field missing; compatibility value resolves"
            if canonical is None and fallback
            else "",
        )

    schema_ref = manifest.get("schema_ref") if isinstance(manifest.get("schema_ref"), dict) else {}
    schema_id = schema_ref.get("schema_id") if isinstance(schema_ref, dict) else None
    _check(
        checks,
        findings,
        case_id=case_id,
        manifest_path=manifest_path,
        field_group="schema_ref",
        field="schema_ref.schema_id",
        observed_value=schema_id,
        expected_shape="non-empty lowercase schema id",
        ok=isinstance(schema_id, str) and bool(schema_id.strip()) and schema_id == schema_id.lower(),
        notes="schema id identifies external schema package",
    )
    engines = schema_ref.get("engines") if isinstance(schema_ref, dict) else None
    engines_present = isinstance(engines, dict)
    profile_value = schema_ref.get("profile") if isinstance(schema_ref, dict) else None
    profile_ref = _resolve_path(
        repo_root=repo_root,
        case_dir=case_dir,
        field_group="schema_ref",
        field="schema_ref.profile",
        observed_value=profile_value,
        path_base="repo",
        required=not engines_present,
    )
    references.append(profile_ref)
    expected_profile = (
        f"schemas/{schema_id}/schema_profile.yaml"
        if isinstance(schema_id, str)
        else "schemas/<SCHEMA_ID>/schema_profile.yaml"
    )
    profile_first_ok = profile_value == expected_profile and profile_ref.status != "fail"
    profile_or_legacy_engine_ok = profile_first_ok or engines_present
    _check(
        checks,
        findings,
        case_id=case_id,
        manifest_path=manifest_path,
        field_group="schema_ref",
        field="schema_ref.profile",
        observed_value=profile_value,
        expected_shape=expected_profile,
        ok=profile_or_legacy_engine_ok,
        warning=bool(profile_value) or engines_present,
        finding_type="schema_ref_profile_shape",
        notes="profile-first schema_ref should point to external schema_profile.yaml"
        if not engines_present
        else "legacy schema_ref.engines compatibility accepted",
    )

    case_schema_profile_ref = _resolve_path(
        repo_root=repo_root,
        case_dir=case_dir,
        field_group="schema",
        field="schema.schema_profile",
        observed_value="schema/schema_profile.yaml",
        path_base="case",
        required=True,
        notes="case-local profile-only schema summary",
    )
    references.append(case_schema_profile_ref)
    _check(
        checks,
        findings,
        case_id=case_id,
        manifest_path=manifest_path,
        field_group="schema",
        field="schema.schema_profile",
        observed_value="schema/schema_profile.yaml" if case_schema_profile_ref.exists else "",
        expected_shape="schema/schema_profile.yaml",
        ok=case_schema_profile_ref.status != "fail",
        finding_type="case_local_schema_profile",
        notes="clean v2 keeps only schema/schema_profile.yaml case-local",
    )

    external_schema_profile = _load_resolved_yaml_mapping(profile_ref)
    external_engines = (
        external_schema_profile.get("engines")
        if isinstance(external_schema_profile, dict)
        and isinstance(external_schema_profile.get("engines"), dict)
        else None
    )
    if profile_value and profile_ref.status != "fail":
        _check(
            checks,
            findings,
            case_id=case_id,
            manifest_path=manifest_path,
            field_group="schema_ref",
            field="schema_ref.profile.parse",
            observed_value="mapping" if external_schema_profile is not None else "unparseable",
            expected_shape="external schema_profile.yaml mapping with engines",
            ok=external_schema_profile is not None and isinstance(external_engines, dict),
            finding_type="schema_profile_parse",
            notes="external profile must be a mapping with engines.<engine>.ddl/load",
        )
        if isinstance(external_schema_profile, dict):
            profile_schema_id = external_schema_profile.get("schema_id")
            _check(
                checks,
                findings,
                case_id=case_id,
                manifest_path=manifest_path,
                field_group="schema_ref",
                field="schema_ref.profile.schema_id",
                observed_value=profile_schema_id,
                expected_shape="matches schema_ref.schema_id",
                ok=profile_schema_id == schema_id,
                finding_type="schema_profile_schema_id",
                notes="external profile schema_id must match manifest schema_ref.schema_id",
            )

    _check(
        checks,
        findings,
        case_id=case_id,
        manifest_path=manifest_path,
        field_group="schema_ref",
        field="schema_ref.engines",
        observed_value="present" if isinstance(engines, dict) else "missing",
        expected_shape="profile-first schema_ref.profile or compatibility schema_ref.engines.<engine>.ddl/load",
        ok=isinstance(engines, dict) or profile_first_ok,
        warning=True,
        finding_type="schema_ref_shape",
        notes="profile-first schema_ref resolves engines through external schema_profile.yaml"
        if not isinstance(engines, dict) and profile_first_ok
        else "compatibility schema_ref.engines shape accepted",
    )
    for engine in SUPPORTED_SCHEMA_ENGINES:
        canonical_engine = engines.get(engine) if isinstance(engines, dict) else None
        fallback_engine = schema_ref.get(engine) if isinstance(schema_ref, dict) else None
        profile_engine = external_engines.get(engine) if isinstance(external_engines, dict) else None
        engine_map = (
            canonical_engine
            if isinstance(canonical_engine, dict)
            else profile_engine
            if isinstance(profile_engine, dict)
            else fallback_engine
        )
        for leaf in ("ddl", "load"):
            value = engine_map.get(leaf) if isinstance(engine_map, dict) else None
            references.append(
                _resolve_path(
                    repo_root=repo_root,
                    case_dir=case_dir,
                    field_group="schema_ref",
                    field=f"schema_ref.engines.{engine}.{leaf}",
                    observed_value=value,
                    path_base="repo",
                    required=True,
                    notes="resolved through schema_ref.profile external schema_profile.yaml"
                    if isinstance(profile_engine, dict) and not isinstance(canonical_engine, dict)
                    else "compatibility fallback from schema_ref.<engine>"
                    if not isinstance(canonical_engine, dict) and value
                    else "",
                )
            )
            _check(
                checks,
                findings,
                case_id=case_id,
                manifest_path=manifest_path,
                field_group="schema_ref",
                field=f"schema_ref.engines.{engine}.{leaf}",
                observed_value=value,
                expected_shape=f"schemas/<SCHEMA_ID>/{engine}/{leaf}.sql",
                ok=isinstance(value, str) and value == f"schemas/{schema_id}/{engine}/{leaf}.sql",
                warning=isinstance(value, str),
                finding_type="schema_ref_engine_shape",
                notes="resolved through profile-first external schema profile"
                if isinstance(profile_engine, dict) and not isinstance(canonical_engine, dict)
                else "canonical engines nesting missing; resolved through compatibility fallback"
                if not isinstance(canonical_engine, dict) and value
                else "",
            )

    evidence_ref = manifest.get("evidence_ref")
    if evidence_ref is None:
        _check(
            checks,
            findings,
            case_id=case_id,
            manifest_path=manifest_path,
            field_group="evidence_ref",
            field="evidence_ref",
            observed_value="missing",
            expected_shape="evidence_ref.package_validation_summary and evidence_ref.runs_retention",
            ok=False,
            warning=True,
            finding_type="missing_evidence_ref",
            notes="policy recorded but not yet added to this case manifest",
        )
    elif isinstance(evidence_ref, dict):
        for key in ("package_validation_summary", "runs_retention"):
            references.append(
                _resolve_path(
                    repo_root=repo_root,
                    case_dir=case_dir,
                    field_group="evidence_ref",
                    field=f"evidence_ref.{key}",
                    observed_value=evidence_ref.get(key),
                    path_base="repo",
                    required=True,
                )
            )
        for key in ("retained_controls", "hard_negative", "plans"):
            if key in evidence_ref:
                references.append(
                    _resolve_path(
                        repo_root=repo_root,
                        case_dir=case_dir,
                        field_group="evidence_ref",
                        field=f"evidence_ref.{key}",
                        observed_value=evidence_ref.get(key),
                        path_base="repo",
                        required=False,
                    )
                )
    else:
        _check(
            checks,
            findings,
            case_id=case_id,
            manifest_path=manifest_path,
            field_group="evidence_ref",
            field="evidence_ref",
            observed_value=type(evidence_ref).__name__,
            expected_shape="mapping",
            ok=False,
            notes="evidence_ref must be a mapping when present",
        )

    witness = manifest.get("witness") if isinstance(manifest.get("witness"), dict) else {}
    for field, expected in (
        ("witness.mode", "source_as_oracle | static_reference | external_reference"),
        ("witness.data_profile_status", "optional | generated | external | materialized | unavailable"),
        ("witness.correct_result_status", "optional | generated | external | materialized | unavailable"),
    ):
        key = field.split(".", 1)[1]
        value = witness.get(key)
        _check(
            checks,
            findings,
            case_id=case_id,
            manifest_path=manifest_path,
            field_group="witness",
            field=field,
            observed_value=value,
            expected_shape=expected,
            ok=isinstance(value, str) and _is_lowercase_status(value),
            warning=True,
            finding_type="witness_policy_shape",
            notes="missing or non-canonical witness policy field",
        )
    for key in ("data_profile", "correct_result"):
        if key in witness:
            references.append(
                _resolve_path(
                    repo_root=repo_root,
                    case_dir=case_dir,
                    field_group="witness",
                    field=f"witness.{key}",
                    observed_value=witness.get(key),
                    path_base="case",
                    required=False,
                )
            )

    validation = manifest.get("validation") if isinstance(manifest.get("validation"), dict) else {}
    for key, expected in CANONICAL_VALIDATION_ENTRYPOINTS.items():
        value = validation.get(key)
        references.append(
            _resolve_path(
                repo_root=repo_root,
                case_dir=case_dir,
                field_group="validation",
                field=f"validation.{key}",
                observed_value=value,
                path_base="case",
                required=False,
                notes="validation layer conversion is pending" if value is None else "",
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
            warning=True,
            finding_type="validation_layer_pending",
            notes="v2 validation entrypoint missing; validation layer conversion is pending"
            if value is None
            else "v2 validation entrypoint",
        )
    for key in sorted(validation):
        if key not in CANONICAL_VALIDATION_ENTRYPOINTS and key.endswith(("validation", "plan_collection")):
            _check(
                checks,
                findings,
                case_id=case_id,
                manifest_path=manifest_path,
                field_group="validation",
                field=f"validation.{key}",
                observed_value=validation.get(key),
                expected_shape="canonical wrappers plus explicit compatibility assets",
                ok=False,
                warning=True,
                finding_type="validation_compatibility_entrypoint",
                notes="engine-specific validation entrypoint retained as compatibility asset",
            )

    status_key_hints = ("status",)
    for group, value in manifest.items():
        if isinstance(value, dict):
            for key, item in value.items():
                if any(hint in key for hint in status_key_hints) and not _is_lowercase_status(item):
                    _check(
                        checks,
                        findings,
                        case_id=case_id,
                        manifest_path=manifest_path,
                        field_group=group,
                        field=f"{group}.{key}",
                        observed_value=item,
                        expected_shape="lowercase boolean/status string",
                        ok=False,
                        warning=True,
                        finding_type="status_case",
                        notes="boolean/status-like string should be lowercase",
                    )

    readme_path = case_dir / "README.md"
    if readme_path.exists():
        text = readme_path.read_text(encoding="utf-8")
        headings = [line.strip("# ").strip() for line in text.splitlines() if line.startswith("## ")]
        expected_order = [
            "Purpose",
            "Release Scope",
            "Package Contents",
            "Evidence Boundary",
            "Benchmark Boundary",
            "Notes / Future Review Status",
        ]
        order_ok = [heading for heading in expected_order if heading in headings] == expected_order
        _check(
            checks,
            findings,
            case_id=case_id,
            manifest_path=readme_path,
            field_group="readme",
            field="README section order",
            observed_value=" > ".join(headings),
            expected_shape="Purpose > Release Scope > Package Contents > Evidence Boundary > Benchmark Boundary > Notes / Future Review Status",
            ok=order_ok,
            warning=True,
            finding_type="readme_section_order",
            notes="README should follow v2/public template section order",
        )

    directory_classification = classify_case_directories(case_dir)
    overall_status = "fail" if any(ref.status == "fail" for ref in references) or any(check.status == "fail" for check in checks) else "pass"
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
    """Classify known v1/v2 directories without deleting or rewriting them."""

    specs = {
        "checker": (
            "case-local checker config",
            "case-local required checker policy",
            True,
            "none; keep as v2 case-local asset",
        ),
        "data": (
            "v1 case-local data profile",
            "optional compatibility metadata",
            True,
            "after external/generated witness policy is validated",
        ),
        "evidence": (
            "v1 case-local retained evidence index/payload",
            "compatibility copy pending evidence_ref",
            True,
            "after evidence_ref mapping and retention review",
        ),
        "metadata": (
            "case-local governance metadata",
            "case-local or manifest-folded metadata",
            True,
            "after manifest/reference migration is approved",
        ),
        "notes": (
            "case-local notes",
            "optional stable case notes",
            True,
            "after public docs/hygiene review",
        ),
        "runs": (
            "legacy retained evidence",
            "legacy retained evidence only",
            True,
            "only with retention mapping and explicit approval",
        ),
        "schema": (
            "case-local schema profile plus retained v1 executable schema copies",
            "schema/schema_profile.yaml in clean v2; executable DDL/load resolve through external schema profile",
            True,
            "after external schema profile resolution and compatibility cleanup are separately approved",
        ),
        "sql": (
            "case SQL assets",
            "case-local required direct SQL assets",
            True,
            "none; keep as v2 case-local asset",
        ),
        "validation": (
            "case validation scripts",
            "thin wrapper entrypoints plus compatibility scripts",
            True,
            "after wrapper validation and shared logic approval",
        ),
        "witness": (
            "v2 pilot witness metadata/static result",
            "optional lightweight witness metadata",
            True,
            "after source-as-oracle policy and external evidence mapping are stable",
        ),
    }
    rows: list[DirectoryClassification] = []
    for directory, (current_role, v2_role, keep_now, delete_condition) in specs.items():
        path = case_dir / directory
        rows.append(
            DirectoryClassification(
                directory=directory + "/",
                current_role=current_role if path.exists() else "absent",
                v2_role=v2_role,
                keep_now=keep_now,
                delete_later_condition=delete_condition,
                notes="exists" if path.exists() else "not present in current package",
            )
        )
    return rows
