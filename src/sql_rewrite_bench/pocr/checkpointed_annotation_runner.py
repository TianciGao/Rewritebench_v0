"""Checkpointed POCR Stage A annotation runner.

This module is for bounded diagnostic annotation generation. It writes
per-row checkpoints before provider calls, supports deterministic resume
behavior, and never computes official POCR or route-level POCR.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from json import JSONDecodeError
from pathlib import Path
from typing import Any, Protocol
from urllib.parse import urlparse

from sql_rewrite_bench.pocr.annotation_client import (
    AnnotationCallResult,
    AnnotationClientConfig,
    OpenAICompatibleAnnotationClient,
)
from sql_rewrite_bench.pocr.annotation_schema import (
    ANNOTATION_SCHEMA_VERSION,
    CandidateAnnotation,
    annotation_to_json_dict,
    validate_candidate_annotation,
)
from sql_rewrite_bench.pocr.candidate_resolver import CandidateSource, resolve_candidate_sources
from sql_rewrite_bench.pocr.prompt_builder import AnnotationPromptInputs, build_annotation_prompt
from sql_rewrite_bench.pocr.skills_parser import parse_skills_file

DEFAULT_RUN_ID = "pocr_annotation_direct_llm_repair1_pg40_checkpointed_v0"
DEFAULT_METHOD_ID = "direct_llm_repair_1"
DEFAULT_ROUTE_ID = "direct_llm_repair_1_pg40_pocr_diagnostic"
DEFAULT_ENGINE = "postgres"
DEFAULT_CASE_SET_ID = "common_core_v0"
DEFAULT_DENOMINATOR_SCOPE = "pg40_postgres_only"
DEFAULT_CANDIDATE_ROOT = Path("runs/user/direct_llm_repair_1_track_a_120_canonical_v0__postgres/candidate_sql")
DEFAULT_PROMPT_TEMPLATE_ID = "pocr_stage_a_annotation_prompt_v1"
DEFAULT_PROMPT_TEMPLATE_VERSION = "checkpointed_transformation_aware_v1"
DEFAULT_CASES = ("PERF_0006", "CONS_0005")

RETRYABLE_STATUSES = {"provider_call_failed", "timeout", "malformed_json"}


class AnnotationProvider(Protocol):
    def annotate_with_metadata(self, prompt: str) -> AnnotationCallResult: ...


@dataclass(frozen=True)
class ProviderEnv:
    provider_label: str
    model_label: str
    base_url: str
    base_url_host: str
    api_key: str
    api_key_env_name: str
    auth_header: str
    allow_live_env: bool


@dataclass(frozen=True)
class CheckpointedAnnotationConfig:
    repo_root: Path
    output_root: Path
    run_id: str = DEFAULT_RUN_ID
    candidate_root: Path = DEFAULT_CANDIDATE_ROOT
    method_id: str = DEFAULT_METHOD_ID
    route_id: str = DEFAULT_ROUTE_ID
    engine: str = DEFAULT_ENGINE
    case_set_id: str = DEFAULT_CASE_SET_ID
    denominator_scope: str = DEFAULT_DENOMINATOR_SCOPE
    case_ids: tuple[str, ...] = DEFAULT_CASES
    live_enabled: bool = False
    max_live_calls: int = 2
    retry_failed: bool = False
    force: bool = False
    provider_label: str = "fake"
    model_label: str = "fixture"
    api_key_env_name: str = ""
    timeout_seconds: float = 60.0
    max_tokens: int = 4000
    prompt_template_id: str = DEFAULT_PROMPT_TEMPLATE_ID
    prompt_template_version: str = DEFAULT_PROMPT_TEMPLATE_VERSION


@dataclass(frozen=True)
class CheckpointedAnnotationPaths:
    annotation_dir: Path
    safe_annotation_outputs_jsonl: Path
    annotation_manifest_csv: Path
    annotation_schema_validation_csv: Path
    prompt_manifest_csv: Path
    provider_call_manifest_csv: Path
    checkpoint_state_json: Path
    log_path: Path
    report_path: Path
    live_smoke_not_run_md: Path


@dataclass(frozen=True)
class CheckpointedAnnotationResult:
    paths: CheckpointedAnnotationPaths
    rows_attempted: int
    live_calls_attempted: int
    annotation_rows_written: int
    status_counts: dict[str, int]
    not_run_reason: str = ""


def output_paths(config: CheckpointedAnnotationConfig) -> CheckpointedAnnotationPaths:
    annotation_dir = (
        config.output_root
        / "results"
        / config.run_id
        / "pocr"
        / "annotations"
        / config.method_id
        / config.route_id
        / config.engine
    )
    return CheckpointedAnnotationPaths(
        annotation_dir=annotation_dir,
        safe_annotation_outputs_jsonl=annotation_dir / "safe_annotation_outputs.jsonl",
        annotation_manifest_csv=annotation_dir / "annotation_manifest.csv",
        annotation_schema_validation_csv=annotation_dir / "annotation_schema_validation.csv",
        prompt_manifest_csv=annotation_dir / "prompt_manifest.csv",
        provider_call_manifest_csv=annotation_dir / "provider_call_manifest.csv",
        checkpoint_state_json=annotation_dir / "checkpoint_state.json",
        log_path=config.output_root / "logs" / config.run_id / "pocr" / "annotation_generation.log",
        report_path=config.output_root / "reports" / config.run_id / "pocr_annotation_generation_report.md",
        live_smoke_not_run_md=config.output_root / "reports" / config.run_id / "live_smoke_not_run.md",
    )


def run_checkpointed_annotation(
    config: CheckpointedAnnotationConfig,
    *,
    client: AnnotationProvider | None = None,
) -> CheckpointedAnnotationResult:
    """Run a bounded checkpointed Stage A annotation pass.

    When ``client`` is supplied, tests can exercise provider behavior without
    reading live secrets. Without a client, ``live_enabled`` must be true and
    the live environment gate must be complete before any provider call occurs.
    """

    if config.max_live_calls < 0:
        raise ValueError("max_live_calls must be non-negative")
    paths = output_paths(config)
    paths.annotation_dir.mkdir(parents=True, exist_ok=True)
    paths.log_path.parent.mkdir(parents=True, exist_ok=True)
    paths.report_path.parent.mkdir(parents=True, exist_ok=True)

    sources = resolve_candidate_sources(
        config.repo_root,
        candidate_root=config.candidate_root,
        method_id=config.method_id,
        route_id=config.route_id,
        engine=config.engine,
        case_ids=config.case_ids,
    )
    if not config.live_enabled:
        reason = "`--live-enabled` was not provided; no API call was made."
        _write_not_run(paths, config, reason, sources)
        return CheckpointedAnnotationResult(paths, 0, 0, _jsonl_row_count(paths.safe_annotation_outputs_jsonl), {}, reason)

    provider_env: ProviderEnv | None = None
    if client is None:
        provider_env = load_provider_env()
        missing = live_env_blockers(provider_env)
        if missing:
            reason = "; ".join(missing)
            _write_not_run(paths, config, reason, sources)
            return CheckpointedAnnotationResult(paths, 0, 0, _jsonl_row_count(paths.safe_annotation_outputs_jsonl), {}, reason)
        client = OpenAICompatibleAnnotationClient(
            AnnotationClientConfig(
                mode="live",
                provider_policy="openai_compatible",
                model_policy=provider_env.model_label,
                allow_live=True,
                base_url=provider_env.base_url,
                api_key=provider_env.api_key,
                api_key_env_used=provider_env.api_key_env_name,
                auth_header=provider_env.auth_header,
                timeout_seconds=config.timeout_seconds,
                max_tokens=config.max_tokens,
            )
        )
    else:
        provider_env = ProviderEnv(
            provider_label=config.provider_label,
            model_label=config.model_label,
            base_url="",
            base_url_host="",
            api_key="",
            api_key_env_name=config.api_key_env_name,
            auth_header="",
            allow_live_env=True,
        )

    manifest = _load_manifest(paths.annotation_manifest_csv)
    jsonl_rows = _read_jsonl_rows(paths.safe_annotation_outputs_jsonl)
    duplicate_cases = _duplicate_cases(jsonl_rows)
    live_calls = 0
    attempted = 0

    _write_log(paths, config, [f"start={_utc_now()}", f"selected_rows={len(sources)}", "api_key_value_recorded=false"])

    for source in sources:
        if not source.candidate_present:
            row = _base_manifest_row(config, source, provider_env, annotation_status="skipped_no_candidate")
            row.update({"call_status": "skipped_no_candidate", "schema_valid": "false", "fail_closed": "true"})
            manifest[source.case_id] = row
            _write_all(paths, config, manifest, jsonl_rows)
            continue
        if source.case_id in duplicate_cases and not config.force:
            row = _base_manifest_row(config, source, provider_env, annotation_status="schema_invalid")
            row.update(
                {
                    "call_status": "schema_invalid",
                    "schema_valid": "false",
                    "error_type": "duplicate_annotation_rows",
                    "fail_closed": "true",
                    "notes": "existing JSONL has duplicate rows for this case; fail-closed until force rerun",
                }
            )
            manifest[source.case_id] = row
            jsonl_rows = _replace_jsonl_row(jsonl_rows, _safe_jsonl_error(config, source, row, "duplicate_annotation_rows"))
            _write_all(paths, config, manifest, jsonl_rows)
            continue

        existing = manifest.get(source.case_id)
        candidate_sha = _sha256_file(config.repo_root / source.candidate_path)
        if existing and not config.force:
            existing_status = existing.get("annotation_status", "")
            existing_sha = existing.get("candidate_sha256", "")
            if existing_status == "schema_valid" and existing_sha == candidate_sha:
                existing["call_status"] = "skipped_existing"
                manifest[source.case_id] = existing
                _write_all(paths, config, manifest, jsonl_rows)
                continue
            if existing_status == "schema_valid" and existing_sha != candidate_sha:
                existing.update(
                    {
                        "annotation_status": "schema_invalid",
                        "call_status": "schema_invalid",
                        "schema_valid": "false",
                        "error_type": "candidate_sha_mismatch",
                        "fail_closed": "true",
                        "notes": "existing schema_valid checkpoint candidate_sha256 does not match current candidate",
                    }
                )
                manifest[source.case_id] = existing
                jsonl_rows = _replace_jsonl_row(jsonl_rows, _safe_jsonl_error(config, source, existing, "candidate_sha_mismatch"))
                _write_all(paths, config, manifest, jsonl_rows)
                continue
            if existing_status in RETRYABLE_STATUSES and not config.retry_failed:
                _write_all(paths, config, manifest, jsonl_rows)
                continue
            if existing_status and existing_status not in RETRYABLE_STATUSES and existing_status != "pending":
                _write_all(paths, config, manifest, jsonl_rows)
                continue

        if live_calls >= config.max_live_calls:
            break

        attempted += 1
        live_calls += 1
        pending = _base_manifest_row(config, source, provider_env, annotation_status="pending")
        pending.update({"call_status": "pending", "schema_valid": "false", "fail_closed": "false"})
        manifest[source.case_id] = pending
        _write_all(paths, config, manifest, jsonl_rows)

        row, jsonl_row = _call_one(config, source, provider_env, client)
        manifest[source.case_id] = row
        jsonl_rows = _replace_jsonl_row(jsonl_rows, jsonl_row)
        _write_all(paths, config, manifest, jsonl_rows)

    _write_all(paths, config, manifest, jsonl_rows)
    status_counts = dict(Counter(row.get("annotation_status", "") for row in manifest.values()))
    return CheckpointedAnnotationResult(
        paths=paths,
        rows_attempted=attempted,
        live_calls_attempted=live_calls,
        annotation_rows_written=_jsonl_row_count(paths.safe_annotation_outputs_jsonl),
        status_counts=status_counts,
    )


def load_provider_env() -> ProviderEnv:
    provider = os.environ.get("SQLRB_LLM_PROVIDER", "openai_compatible").strip() or "openai_compatible"
    model = _first_env(("SQLRB_LLM_MODEL", "GPTSAPI_MODEL"), "gpt-5.4")[0]
    base_url, _ = _first_env(("SQLRB_LLM_BASE_URL", "GPTSAPI_BASE_URL"), "https://api.gptsapi.net/v1")
    api_key, api_key_env = _first_env(("SQLRB_LLM_API_KEY", "GPTSAPI_API_KEY"), "")
    auth_header = os.environ.get("SQLRB_LLM_AUTH_HEADER", "authorization_bearer").strip() or "authorization_bearer"
    return ProviderEnv(
        provider_label=provider,
        model_label=model,
        base_url=base_url.rstrip("/"),
        base_url_host=urlparse(base_url).netloc or "unknown",
        api_key=api_key,
        api_key_env_name=api_key_env,
        auth_header=auth_header,
        allow_live_env=os.environ.get("SQLRB_LLM_ALLOW_LIVE") == "1",
    )


def live_env_blockers(provider_env: ProviderEnv) -> list[str]:
    blockers: list[str] = []
    if not provider_env.allow_live_env:
        blockers.append("`SQLRB_LLM_ALLOW_LIVE=1` is not set")
    if not provider_env.api_key:
        blockers.append("API key environment variable is not set")
    if not provider_env.base_url:
        blockers.append("base URL is not configured")
    if not provider_env.model_label:
        blockers.append("model label is not configured")
    return blockers


def _call_one(
    config: CheckpointedAnnotationConfig,
    source: CandidateSource,
    provider_env: ProviderEnv,
    client: AnnotationProvider,
) -> tuple[dict[str, str], dict[str, object]]:
    timestamp = _utc_now()
    candidate_sha = _sha256_file(config.repo_root / source.candidate_path)
    skills_path = config.repo_root / source.skills_md_path
    skills_hash = _sha256_file(skills_path)
    candidate_id = _candidate_id(config, source, candidate_sha)
    base_row = _base_manifest_row(config, source, provider_env, annotation_status="schema_invalid")
    base_row.update(
        {
            "candidate_sha256": candidate_sha,
            "candidate_id": candidate_id,
            "skills_contract_hash": skills_hash,
            "call_timestamp_utc": timestamp,
        }
    )

    parse_result = parse_skills_file(skills_path, expected_case_id=source.case_id, expected_pool=source.pool)
    if parse_result.contract is None or not parse_result.ok:
        row = dict(base_row)
        row.update(
            {
                "annotation_status": "skipped_no_skills",
                "call_status": "skipped_no_skills",
                "schema_valid": "false",
                "error_type": "skills_contract_invalid",
                "fail_closed": "true",
                "notes": "skills.md contract missing or invalid",
            }
        )
        return row, _safe_jsonl_error(config, source, row, "skills_contract_invalid")

    try:
        prompt = _build_prompt(config, source, parse_result.contract, candidate_id)
    except Exception as exc:  # noqa: BLE001 - prompt failures must become checkpoint rows.
        row = dict(base_row)
        row.update(
            {
                "annotation_status": "prompt_build_failed",
                "call_status": "prompt_build_failed",
                "schema_valid": "false",
                "error_type": type(exc).__name__,
                "error_message": str(exc)[:240],
                "fail_closed": "true",
                "notes": "prompt build failed before provider call",
            }
        )
        return row, _safe_jsonl_error(config, source, row, "prompt_build_failed")

    prompt_hash = _sha256_text(prompt)
    try:
        result = client.annotate_with_metadata(prompt)
    except TimeoutError as exc:
        row = dict(base_row)
        row.update(
            {
                "annotation_status": "timeout",
                "call_status": "timeout",
                "schema_valid": "false",
                "prompt_hash": prompt_hash,
                "error_type": type(exc).__name__,
                "error_message": str(exc)[:240],
                "fail_closed": "true",
                "notes": "provider call timed out; fail-closed diagnostic row",
            }
        )
        return row, _safe_jsonl_error(config, source, row, "timeout")
    except JSONDecodeError as exc:
        row = dict(base_row)
        row.update(
            {
                "annotation_status": "malformed_json",
                "call_status": "malformed_json",
                "schema_valid": "false",
                "prompt_hash": prompt_hash,
                "error_type": type(exc).__name__,
                "error_message": str(exc)[:240],
                "fail_closed": "true",
                "notes": "provider response was malformed JSON; fail-closed diagnostic row",
            }
        )
        return row, _safe_jsonl_error(config, source, row, "malformed_json")
    except Exception as exc:  # noqa: BLE001 - provider exceptions must not lose prior checkpoints.
        row = dict(base_row)
        row.update(
            {
                "annotation_status": "provider_call_failed",
                "call_status": "provider_call_failed",
                "schema_valid": "false",
                "prompt_hash": prompt_hash,
                "error_type": type(exc).__name__,
                "error_message": str(exc)[:240],
                "fail_closed": "true",
                "notes": "provider call failed; fail-closed diagnostic row",
            }
        )
        return row, _safe_jsonl_error(config, source, row, "provider_call_failed")

    annotation = result.annotation
    issues = validate_candidate_annotation(
        annotation,
        parse_result.contract,
        expected_engine=config.engine,
        expected_method_id=config.method_id,
        expected_route_id=config.route_id,
    )
    issue_codes = [issue.code for issue in issues]
    schema_valid = not issue_codes
    row = dict(base_row)
    row.update(
        {
            "annotation_status": "schema_valid" if schema_valid else "schema_invalid",
            "call_status": "schema_valid" if schema_valid else "schema_invalid",
            "schema_valid": str(schema_valid).lower(),
            "prompt_hash": prompt_hash,
            "prompt_tokens": str(result.prompt_tokens) if result.prompt_tokens is not None else "",
            "completion_tokens": str(result.completion_tokens) if result.completion_tokens is not None else "",
            "total_tokens": str(result.total_tokens) if result.total_tokens is not None else "",
            "token_counts_if_available": _token_counts(result),
            "error_type": ";".join(issue_codes),
            "fail_closed": "false" if schema_valid else "true",
            "notes": "schema_valid" if schema_valid else "schema validation failed; no POCR numerator",
        }
    )
    return row, _safe_jsonl_annotation(config, source, row, annotation)


def _build_prompt(
    config: CheckpointedAnnotationConfig,
    source: CandidateSource,
    contract: object,
    candidate_id: str,
) -> str:
    source_sql = (config.repo_root / source.source_sql_path).read_text(encoding="utf-8-sig")
    candidate_sql = (config.repo_root / source.candidate_path).read_text(encoding="utf-8-sig")
    positive_sql = (
        (config.repo_root / source.positive_sql_path).read_text(encoding="utf-8-sig")
        if source.positive_sql_path
        else None
    )
    negative_sql = (
        (config.repo_root / source.negative_sql_path).read_text(encoding="utf-8-sig")
        if source.negative_sql_path
        else None
    )
    return (
        build_annotation_prompt(
            AnnotationPromptInputs(
                contract=contract,  # type: ignore[arg-type]
                source_sql=source_sql,
                candidate_sql=candidate_sql,
                positive_sql=positive_sql,
                negative_sql=negative_sql,
                engine=config.engine,
                method_id=config.method_id,
                route_id=config.route_id,
                candidate_id=candidate_id,
                candidate_path=source.candidate_path.as_posix(),
            )
        )
        + "\n\nCheckpointed runner boundary reminders:\n"
        + "- Stage A annotation alone is not counted.\n"
        + "- Stage B transformation-aware validation is diagnostic only.\n"
        + "- This is not official POCR.\n"
        + "- No route-level POCR score is emitted.\n"
        + "- No paper-facing metric is promoted.\n"
        + "- No global leaderboard is produced.\n"
    )


def _base_manifest_row(
    config: CheckpointedAnnotationConfig,
    source: CandidateSource,
    provider_env: ProviderEnv,
    *,
    annotation_status: str,
) -> dict[str, str]:
    candidate_path = config.repo_root / source.candidate_path
    skills_path = config.repo_root / source.skills_md_path
    candidate_sha = _sha256_file(candidate_path) if candidate_path.is_file() else ""
    skills_hash = _sha256_file(skills_path) if skills_path.is_file() else ""
    timestamp = _utc_now()
    return {
        "run_id": config.run_id,
        "case_set_id": config.case_set_id,
        "case_id": source.case_id,
        "pool": source.pool,
        "engine": source.engine,
        "method_id": config.method_id,
        "route_id": config.route_id,
        "denominator_scope": config.denominator_scope,
        "candidate_rel_path": source.candidate_path.as_posix(),
        "candidate_sha256": candidate_sha,
        "candidate_id": _candidate_id(config, source, candidate_sha) if candidate_sha else "",
        "skills_contract_hash": skills_hash,
        "annotation_status": annotation_status,
        "annotation_schema_version": ANNOTATION_SCHEMA_VERSION,
        "prompt_template_id": config.prompt_template_id,
        "prompt_template_version": config.prompt_template_version,
        "prompt_hash": "",
        "provider_label": provider_env.provider_label,
        "model_label": provider_env.model_label,
        "call_timestamp_utc": timestamp,
        "live_api_used": str(config.live_enabled).lower(),
        "diagnostic_only": "true",
        "official_pocr_computed": "false",
        "route_level_pocr_aggregated": "false",
        "paper_metric_promoted": "false",
        "call_status": annotation_status,
        "schema_valid": "false",
        "prompt_tokens": "",
        "completion_tokens": "",
        "total_tokens": "",
        "token_counts_if_available": "",
        "api_key_env_name": provider_env.api_key_env_name,
        "api_key_value_recorded": "false",
        "error_type": "",
        "error_message": "",
        "fail_closed": "false",
        "notes": "checkpointed diagnostic row; no official POCR",
    }


def _safe_jsonl_annotation(
    config: CheckpointedAnnotationConfig,
    source: CandidateSource,
    row: dict[str, str],
    annotation: CandidateAnnotation,
) -> dict[str, object]:
    payload = _safe_jsonl_base(config, source, row)
    payload["atoms"] = [
        {
            "atom_id": atom.atom_id,
            "atom_type": atom.atom_type,
            "expected": atom.expected,
            "observed_status": atom.observed_status,
            "rationale_short": atom.rationale_short,
            "evidence_refs": list(atom.evidence_refs),
            "confidence": atom.confidence,
        }
        for atom in annotation.atoms
    ]
    payload["annotation"] = annotation_to_json_dict(annotation)
    return payload


def _safe_jsonl_error(
    config: CheckpointedAnnotationConfig,
    source: CandidateSource,
    row: dict[str, str],
    status: str,
) -> dict[str, object]:
    payload = _safe_jsonl_base(config, source, row)
    payload["atoms"] = []
    payload["annotation"] = {
        "case_id": source.case_id,
        "pool": source.pool,
        "engine": source.engine,
        "method_id": config.method_id,
        "route_id": config.route_id,
        "candidate_id": row.get("candidate_id", ""),
        "candidate_path": source.candidate_path.as_posix(),
        "annotation_schema_version": ANNOTATION_SCHEMA_VERSION,
        "atoms": [],
    }
    payload["error"] = {
        "status": status,
        "error_type": row.get("error_type", ""),
        "fail_closed": True,
        "message": row.get("error_message", ""),
    }
    return payload


def _safe_jsonl_base(
    config: CheckpointedAnnotationConfig,
    source: CandidateSource,
    row: dict[str, str],
) -> dict[str, object]:
    return {
        "annotation_schema_version": ANNOTATION_SCHEMA_VERSION,
        "run_id": config.run_id,
        "case_set_id": config.case_set_id,
        "case_id": source.case_id,
        "pool": source.pool,
        "engine": source.engine,
        "method_id": config.method_id,
        "route_id": config.route_id,
        "candidate_id": row.get("candidate_id", ""),
        "candidate_rel_path": source.candidate_path.as_posix(),
        "candidate_sha256": row.get("candidate_sha256", ""),
        "skills_contract_hash": row.get("skills_contract_hash", ""),
        "prompt_template_id": config.prompt_template_id,
        "prompt_template_version": config.prompt_template_version,
        "provider_label": row.get("provider_label", ""),
        "model_label": row.get("model_label", ""),
        "call_timestamp_utc": row.get("call_timestamp_utc", ""),
        "decoding_parameters": {
            "temperature": 0,
            "max_tokens": config.max_tokens,
            "response_format": "strict_json_prompted",
        },
        "annotation_status": row.get("annotation_status", ""),
        "diagnostic_only": True,
        "official_pocr_computed": False,
        "route_level_pocr_aggregated": False,
        "paper_metric_promoted": False,
    }


def _write_all(
    paths: CheckpointedAnnotationPaths,
    config: CheckpointedAnnotationConfig,
    manifest: dict[str, dict[str, str]],
    jsonl_rows: list[dict[str, object]],
) -> None:
    ordered = sorted(manifest.values(), key=lambda row: row["case_id"])
    _write_csv_atomic(paths.annotation_manifest_csv, annotation_manifest_fields(), ordered)
    _write_csv_atomic(paths.annotation_schema_validation_csv, schema_validation_fields(), [_schema_row(row) for row in ordered])
    _write_csv_atomic(paths.prompt_manifest_csv, prompt_manifest_fields(), [_prompt_row(row) for row in ordered])
    _write_csv_atomic(paths.provider_call_manifest_csv, provider_manifest_fields(), [_provider_row(row) for row in ordered])
    _write_jsonl_atomic(paths.safe_annotation_outputs_jsonl, sorted(jsonl_rows, key=lambda row: str(row.get("case_id", ""))))
    state = {
        "run_id": config.run_id,
        "updated_at_utc": _utc_now(),
        "rows": len(ordered),
        "jsonl_rows": len(jsonl_rows),
        "status_counts": dict(Counter(row.get("annotation_status", "") for row in ordered)),
        "diagnostic_only": True,
        "official_pocr_computed": False,
        "route_level_pocr_aggregated": False,
        "paper_metric_promoted": False,
    }
    _write_text_atomic(paths.checkpoint_state_json, json.dumps(state, indent=2, sort_keys=True) + "\n")
    _write_report(paths, config, ordered, jsonl_rows)


def _write_not_run(
    paths: CheckpointedAnnotationPaths,
    config: CheckpointedAnnotationConfig,
    reason: str,
    sources: tuple[CandidateSource, ...],
) -> None:
    provider_env = ProviderEnv(
        provider_label=config.provider_label,
        model_label=config.model_label,
        base_url="",
        base_url_host="",
        api_key="",
        api_key_env_name=config.api_key_env_name,
        auth_header="",
        allow_live_env=False,
    )
    manifest = {}
    for source in sources:
        row = _base_manifest_row(config, source, provider_env, annotation_status="not_run")
        row.update({"call_status": "not_run", "fail_closed": "true", "notes": reason})
        manifest[source.case_id] = row
    _write_all(paths, config, manifest, _read_jsonl_rows(paths.safe_annotation_outputs_jsonl))
    _write_text_atomic(
        paths.live_smoke_not_run_md,
        "# Live Smoke Not Run\n\n"
        f"{reason}\n\n"
        "No fake annotation JSONL was generated. No API key value was written.\n",
    )


def _write_report(
    paths: CheckpointedAnnotationPaths,
    config: CheckpointedAnnotationConfig,
    ordered: list[dict[str, str]],
    jsonl_rows: list[dict[str, object]],
) -> None:
    counts = Counter(row.get("annotation_status", "") for row in ordered)
    lines = [
        "# Checkpointed POCR Annotation Report",
        "",
        "Positive Operation Coverage diagnostic support.",
        "",
        f"- run_id: `{config.run_id}`",
        f"- method_id: `{config.method_id}`",
        f"- route_id: `{config.route_id}`",
        f"- engine: `{config.engine}`",
        f"- manifest rows: {len(ordered)}",
        f"- safe JSONL rows: {len(jsonl_rows)}",
        f"- status counts: `{json.dumps(dict(sorted(counts.items())), sort_keys=True)}`",
        "",
        "This is not official POCR.",
        "",
        "Stage A annotation alone is not counted.",
        "",
        "Stage B transformation-aware validation is diagnostic only.",
        "",
        "Semantic guard atoms are not part of operation coverage numerator.",
        "",
        "No route-level POCR score is emitted.",
        "",
        "No paper-facing metric is promoted.",
        "",
        "No global leaderboard is produced.",
    ]
    _write_text_atomic(paths.report_path, "\n".join(lines) + "\n")


def _write_log(paths: CheckpointedAnnotationPaths, config: CheckpointedAnnotationConfig, lines: list[str]) -> None:
    paths.log_path.parent.mkdir(parents=True, exist_ok=True)
    with paths.log_path.open("a", encoding="utf-8") as handle:
        handle.write("\n".join([f"run_id={config.run_id}", *lines]) + "\n")


def _load_manifest(path: Path) -> dict[str, dict[str, str]]:
    if not path.is_file():
        return {}
    with path.open(newline="", encoding="utf-8") as handle:
        return {row["case_id"]: dict(row) for row in csv.DictReader(handle)}


def _read_jsonl_rows(path: Path) -> list[dict[str, object]]:
    if not path.is_file():
        return []
    rows: list[dict[str, object]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def _replace_jsonl_row(rows: list[dict[str, object]], replacement: dict[str, object]) -> list[dict[str, object]]:
    case_id = str(replacement.get("case_id", ""))
    return [row for row in rows if str(row.get("case_id", "")) != case_id] + [replacement]


def _duplicate_cases(rows: list[dict[str, object]]) -> set[str]:
    counts = Counter(str(row.get("case_id", "")) for row in rows)
    return {case_id for case_id, count in counts.items() if case_id and count > 1}


def _schema_row(row: dict[str, str]) -> dict[str, str]:
    return {
        "run_id": row["run_id"],
        "case_id": row["case_id"],
        "engine": row["engine"],
        "method_id": row["method_id"],
        "route_id": row["route_id"],
        "candidate_sha256": row["candidate_sha256"],
        "validation_status": row["annotation_status"],
        "schema_valid": row["schema_valid"],
        "error_type": row["error_type"],
        "error_message": row["error_message"],
        "fail_closed": row["fail_closed"],
        "notes": row["notes"],
    }


def _prompt_row(row: dict[str, str]) -> dict[str, str]:
    return {
        "run_id": row["run_id"],
        "case_id": row["case_id"],
        "prompt_template_id": row["prompt_template_id"],
        "prompt_template_version": row["prompt_template_version"],
        "prompt_hash": row["prompt_hash"],
        "skills_contract_hash": row["skills_contract_hash"],
        "input_fields": "skills_md;source_sql;candidate_sql;positive_sql;negative_sql;method_id;route_id;engine;candidate_id",
        "boundary_instructions_present": "true",
        "notes": "prompt text not stored",
    }


def _provider_row(row: dict[str, str]) -> dict[str, str]:
    return {
        "provider_label": row["provider_label"],
        "model_label": row["model_label"],
        "call_timestamp_utc": row["call_timestamp_utc"],
        "call_status": row["call_status"],
        "error_type": row["error_type"],
        "token_counts_if_available": row["token_counts_if_available"],
        "api_key_env_name": row["api_key_env_name"],
        "api_key_value_recorded": "false",
        "notes": row["notes"],
    }


def annotation_manifest_fields() -> list[str]:
    return [
        "run_id",
        "case_set_id",
        "case_id",
        "pool",
        "engine",
        "method_id",
        "route_id",
        "denominator_scope",
        "candidate_rel_path",
        "candidate_sha256",
        "candidate_id",
        "skills_contract_hash",
        "annotation_status",
        "annotation_schema_version",
        "prompt_template_id",
        "prompt_template_version",
        "prompt_hash",
        "provider_label",
        "model_label",
        "call_timestamp_utc",
        "live_api_used",
        "diagnostic_only",
        "official_pocr_computed",
        "route_level_pocr_aggregated",
        "paper_metric_promoted",
        "call_status",
        "schema_valid",
        "prompt_tokens",
        "completion_tokens",
        "total_tokens",
        "token_counts_if_available",
        "api_key_env_name",
        "api_key_value_recorded",
        "error_type",
        "error_message",
        "fail_closed",
        "notes",
    ]


def schema_validation_fields() -> list[str]:
    return [
        "run_id",
        "case_id",
        "engine",
        "method_id",
        "route_id",
        "candidate_sha256",
        "validation_status",
        "schema_valid",
        "error_type",
        "error_message",
        "fail_closed",
        "notes",
    ]


def prompt_manifest_fields() -> list[str]:
    return [
        "run_id",
        "case_id",
        "prompt_template_id",
        "prompt_template_version",
        "prompt_hash",
        "skills_contract_hash",
        "input_fields",
        "boundary_instructions_present",
        "notes",
    ]


def provider_manifest_fields() -> list[str]:
    return [
        "provider_label",
        "model_label",
        "call_timestamp_utc",
        "call_status",
        "error_type",
        "token_counts_if_available",
        "api_key_env_name",
        "api_key_value_recorded",
        "notes",
    ]


def _write_csv_atomic(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    tmp.replace(path)


def _write_jsonl_atomic(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    tmp.replace(path)


def _write_text_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def _jsonl_row_count(path: Path) -> int:
    return len(_read_jsonl_rows(path))


def _candidate_id(config: CheckpointedAnnotationConfig, source: CandidateSource, candidate_sha: str) -> str:
    return f"{config.method_id}:{config.route_id}:{source.case_id}:{config.engine}:{candidate_sha[:12]}"


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _token_counts(result: AnnotationCallResult) -> str:
    return json.dumps(
        {
            "prompt_tokens": result.prompt_tokens,
            "completion_tokens": result.completion_tokens,
            "total_tokens": result.total_tokens,
        },
        sort_keys=True,
    )


def _first_env(names: tuple[str, ...], default: str = "") -> tuple[str, str]:
    for name in names:
        value = os.environ.get(name)
        if value:
            return value, name
    return default, ""


def _utc_now() -> str:
    return datetime.now(UTC).isoformat()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live-enabled", action="store_true")
    parser.add_argument("--retry-failed", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--output-root", type=Path, default=Path("output"))
    parser.add_argument("--run-id", default=DEFAULT_RUN_ID)
    parser.add_argument("--candidate-root", type=Path, default=DEFAULT_CANDIDATE_ROOT)
    parser.add_argument("--method-id", default=DEFAULT_METHOD_ID)
    parser.add_argument("--route-id", default=DEFAULT_ROUTE_ID)
    parser.add_argument("--engine", default=DEFAULT_ENGINE)
    parser.add_argument("--case-list", default=",".join(DEFAULT_CASES))
    parser.add_argument("--max-live-calls", type=int, default=2)
    parser.add_argument("--timeout-seconds", type=float, default=60.0)
    parser.add_argument("--max-tokens", type=int, default=4000)
    args = parser.parse_args(argv)
    case_ids = tuple(case_id.strip() for case_id in args.case_list.split(",") if case_id.strip())
    config = CheckpointedAnnotationConfig(
        repo_root=args.repo_root.resolve(),
        output_root=args.output_root,
        run_id=args.run_id,
        candidate_root=args.candidate_root,
        method_id=args.method_id,
        route_id=args.route_id,
        engine=args.engine,
        case_ids=case_ids,
        live_enabled=args.live_enabled,
        max_live_calls=args.max_live_calls,
        retry_failed=args.retry_failed,
        force=args.force,
        timeout_seconds=args.timeout_seconds,
        max_tokens=args.max_tokens,
    )
    result = run_checkpointed_annotation(config)
    print(
        "checkpointed annotation complete: "
        f"rows_attempted={result.rows_attempted} "
        f"live_calls_attempted={result.live_calls_attempted} "
        f"annotation_rows_written={result.annotation_rows_written} "
        f"not_run_reason={result.not_run_reason}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
