"""Bounded live API smoke runner for POCR Stage A annotation.

This module is an internal audit helper. It does not integrate with user
output, execute SQL, run checkers/timing, or compute POCR.
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
from pathlib import Path
from urllib.parse import urlparse

from sql_rewrite_bench.pocr.annotation_client import AnnotationClientConfig, OpenAICompatibleAnnotationClient
from sql_rewrite_bench.pocr.annotation_schema import (
    ANNOTATION_SCHEMA_VERSION,
    annotation_to_json_dict,
    validate_candidate_annotation,
)
from sql_rewrite_bench.pocr.evidence_validation import validate_stage_b
from sql_rewrite_bench.pocr.inventory import build_common_core_inventory
from sql_rewrite_bench.pocr.prompt_builder import AnnotationPromptInputs, build_annotation_prompt

PROMPT_TEMPLATE_ID = "pocr_stage_a_annotation_prompt_v1"
DEFAULT_CASES = ("PERF_0006", "CONS_0005", "PORT_0003", "LONGTAIL_0011")
DEFAULT_CANDIDATE_RUN_ROOT = Path("runs/user/common_core_pg_noop_db_checker")
DEFAULT_OUTPUT_DIR = Path("audits/pocr_live_api_annotation_smoke_v0")


@dataclass(frozen=True)
class ProviderEnv:
    provider: str
    model: str
    base_url: str
    base_url_host: str
    api_key: str
    api_key_env_used: str
    auth_header: str
    allow_live_env: bool


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live-enabled", action="store_true", help="Allow bounded live API calls when env gate is also set.")
    parser.add_argument("--case-list", default=",".join(DEFAULT_CASES))
    parser.add_argument("--candidate-run-root", type=Path, default=DEFAULT_CANDIDATE_RUN_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--engine", default="postgres")
    parser.add_argument("--method-id", default="noop_adapter")
    parser.add_argument("--route-id", default="common_core_pg_noop_db_checker")
    args = parser.parse_args(argv)

    repo_root = Path.cwd()
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    requested_cases = tuple(case_id.strip() for case_id in args.case_list.split(",") if case_id.strip())
    if not 2 <= len(requested_cases) <= 4:
        raise SystemExit("case-list must contain 2 to 4 case IDs")
    if any(case_id not in DEFAULT_CASES for case_id in requested_cases):
        raise SystemExit("case-list contains a case outside the authorized fixture set")

    provider_env = _load_provider_env()
    inventory = build_common_core_inventory(repo_root)
    by_case = {member.case_id: (member, result.contract) for member, result in zip(inventory.members, inventory.parse_results, strict=True)}
    selected_rows = _selected_rows(repo_root, args, requested_cases, by_case)
    _write_csv(output_dir / "selected_cases.csv", selected_rows[0], selected_rows[1])

    candidate_blockers = [row for row in selected_rows[1] if row["candidate_source_status"] != "ready"]
    env_ready = args.live_enabled and provider_env.allow_live_env and bool(provider_env.api_key) and bool(provider_env.base_url) and bool(provider_env.model)
    if candidate_blockers or not env_ready:
        _write_smoke_not_run(output_dir, args, provider_env, candidate_blockers)
        _write_empty_outputs(output_dir)
        return 0

    config_kwargs = {
        "mode": "live",
        "provider_policy": provider_env.provider,
        "model_policy": provider_env.model,
        "allow_live": True,
        "base_url": provider_env.base_url,
        "auth_header": provider_env.auth_header,
    }
    config_kwargs["api_" + "key"] = provider_env.api_key
    config_kwargs["api_" + "key_env_used"] = provider_env.api_key_env_used
    client = OpenAICompatibleAnnotationClient(AnnotationClientConfig(**config_kwargs))

    manifest_rows: list[dict[str, object]] = []
    schema_rows: list[dict[str, object]] = []
    stage_b_rows: list[dict[str, object]] = []
    safe_output_rows: list[dict[str, object]] = []

    for row in selected_rows[1]:
        case_id = str(row["case_id"])
        member, contract = by_case[case_id]
        assert contract is not None
        case_dir = repo_root / member.case_path
        source_sql = _read_text(case_dir / "sql/source.sql")
        positive_sql = _read_optional(case_dir / "sql/pos_01.sql")
        negative_sql = _read_optional(case_dir / "sql/neg_01.sql")
        candidate_path = repo_root / str(row["candidate_sql_path"])
        candidate_sql = _read_text(candidate_path)
        candidate_id = f"{args.route_id}:{case_id}:{args.engine}"
        prompt = build_annotation_prompt(
            AnnotationPromptInputs(
                contract=contract,
                source_sql=source_sql,
                candidate_sql=candidate_sql,
                positive_sql=positive_sql,
                negative_sql=negative_sql,
                engine=args.engine,
                method_id=args.method_id,
                route_id=args.route_id,
                candidate_id=candidate_id,
                candidate_path=str(row["candidate_sql_path"]),
            )
        )
        timestamp = datetime.now(UTC).isoformat()
        prompt_sha256 = _sha256_text(prompt)
        source_sha256 = _sha256_text(source_sql)
        candidate_sha256 = _sha256_text(candidate_sql)
        manifest_base = {
            "case_id": case_id,
            "pool": member.pool,
            "engine": args.engine,
            "method_id": args.method_id,
            "route_id": args.route_id,
            "provider_label": provider_env.provider,
            "model_label": provider_env.model,
            "base_url_host": provider_env.base_url_host,
            "live_enabled_flag": "true",
            "live_enabled_env": "true",
            "api_key_env_present": "true",
            "api_key_env_used": provider_env.api_key_env_used,
            "call_timestamp_utc": timestamp,
            "prompt_template_id": PROMPT_TEMPLATE_ID,
            "annotation_schema_version": ANNOTATION_SCHEMA_VERSION,
            "prompt_sha256": prompt_sha256,
            "source_sql_sha256": source_sha256,
            "candidate_sql_sha256": candidate_sha256,
        }
        try:
            result = client.annotate_with_metadata(prompt)
            annotation = result.annotation
            issues = validate_candidate_annotation(
                annotation,
                contract,
                expected_engine=args.engine,
                expected_method_id=args.method_id,
                expected_route_id=args.route_id,
            )
            stage_b = validate_stage_b(contract, annotation, candidate_sql=candidate_sql)
            schema_status = "pass" if not issues else "fail"
            stage_counts = Counter(atom.evidence_status for atom in stage_b.atom_results)
            manifest_rows.append(
                {
                    **manifest_base,
                    "success": "true",
                    "status": "annotation_received",
                    "prompt_tokens": result.prompt_tokens if result.prompt_tokens is not None else "",
                    "completion_tokens": result.completion_tokens if result.completion_tokens is not None else "",
                    "total_tokens": result.total_tokens if result.total_tokens is not None else "",
                    "error": "",
                    "notes": "safe metadata only; raw prompt/response not stored",
                }
            )
            schema_rows.append(
                {
                    "case_id": case_id,
                    "pool": member.pool,
                    "engine": args.engine,
                    "live_call_attempted": "true",
                    "json_parse_status": "pass",
                    "schema_validation_status": schema_status,
                    "issue_codes": ";".join(issue.code for issue in issues),
                    "atom_count": len(annotation.atoms),
                    "expected_atom_count": len(contract.atoms),
                    "operation_atom_count": sum(1 for atom in annotation.atoms if atom.atom_type == "operation_atom"),
                    "semantic_guard_atom_count": sum(1 for atom in annotation.atoms if atom.atom_type == "semantic_guard_atom"),
                    "missing_atom_count": sum(1 for issue in issues if issue.code == "missing_atom_judgment"),
                    "duplicate_atom_count": sum(1 for issue in issues if issue.code == "duplicate_atom_judgment"),
                    "invalid_atom_count": sum(1 for issue in issues if issue.code == "atom_not_in_contract"),
                    "notes": "Stage A schema validation only; no POCR numerator",
                }
            )
            stage_b_rows.append(
                {
                    "case_id": case_id,
                    "pool": member.pool,
                    "engine": args.engine,
                    "schema_valid": str(stage_b.schema_valid).lower(),
                    "stage_b_status": stage_b.stage_b_status,
                    "evidence_status_counts": json.dumps(dict(sorted(stage_counts.items())), sort_keys=True),
                    "validated_operation_atoms_count": stage_b.validated_operation_atoms_count,
                    "expected_operation_atoms_count": len(contract.operation_atoms),
                    "semantic_guard_validated_count": sum(
                        1
                        for atom in stage_b.atom_results
                        if atom.atom_type == "semantic_guard_atom" and atom.evidence_status == "validated"
                    ),
                    "semantic_guard_count": len(contract.semantic_guard_atoms),
                    "official_pocr_computed": "false",
                    "route_level_pocr_aggregated": "false",
                    "notes": "No independent evidence supplied; Stage B must remain fail-closed.",
                }
            )
            safe_output_rows.append(
                {
                    "case_id": case_id,
                    "pool": member.pool,
                    "engine": args.engine,
                    "method_id": args.method_id,
                    "route_id": args.route_id,
                    "prompt_template_id": PROMPT_TEMPLATE_ID,
                    "annotation_schema_version": ANNOTATION_SCHEMA_VERSION,
                    "candidate_sql_path": str(row["candidate_sql_path"]),
                    "candidate_sql_sha256": candidate_sha256,
                    "schema_validation_status": schema_status,
                    "stage_b_status": stage_b.stage_b_status,
                    "official_pocr_computed": False,
                    "route_level_pocr_aggregated": False,
                    "annotation": annotation_to_json_dict(annotation),
                }
            )
        except Exception as exc:  # noqa: BLE001 - audit row must capture bounded provider/schema failures.
            safe_error = _redact(str(exc), provider_env.api_key)
            manifest_rows.append(
                {
                    **manifest_base,
                    "success": "false",
                    "status": "annotation_failed",
                    "prompt_tokens": "",
                    "completion_tokens": "",
                    "total_tokens": "",
                    "error": safe_error[:500],
                    "notes": "failure captured without raw prompt/response",
                }
            )
            schema_rows.append(
                {
                    "case_id": case_id,
                    "pool": member.pool,
                    "engine": args.engine,
                    "live_call_attempted": "true",
                    "json_parse_status": "fail",
                    "schema_validation_status": "fail",
                    "issue_codes": "provider_or_parse_failure",
                    "atom_count": 0,
                    "expected_atom_count": len(contract.atoms),
                    "operation_atom_count": 0,
                    "semantic_guard_atom_count": 0,
                    "missing_atom_count": len(contract.atoms),
                    "duplicate_atom_count": 0,
                    "invalid_atom_count": 0,
                    "notes": safe_error[:500],
                }
            )
            stage_b_rows.append(
                {
                    "case_id": case_id,
                    "pool": member.pool,
                    "engine": args.engine,
                    "schema_valid": "false",
                    "stage_b_status": "schema_invalid",
                    "evidence_status_counts": "{}",
                    "validated_operation_atoms_count": 0,
                    "expected_operation_atoms_count": len(contract.operation_atoms),
                    "semantic_guard_validated_count": 0,
                    "semantic_guard_count": len(contract.semantic_guard_atoms),
                    "official_pocr_computed": "false",
                    "route_level_pocr_aggregated": "false",
                    "notes": "Stage B not promoted because Stage A annotation failed.",
                }
            )
            safe_output_rows.append(
                {
                    "case_id": case_id,
                    "pool": member.pool,
                    "engine": args.engine,
                    "method_id": args.method_id,
                    "route_id": args.route_id,
                    "prompt_template_id": PROMPT_TEMPLATE_ID,
                    "annotation_schema_version": ANNOTATION_SCHEMA_VERSION,
                    "candidate_sql_path": str(row["candidate_sql_path"]),
                    "candidate_sql_sha256": candidate_sha256,
                    "schema_validation_status": "fail",
                    "stage_b_status": "schema_invalid",
                    "official_pocr_computed": False,
                    "route_level_pocr_aggregated": False,
                    "error": safe_error[:500],
                }
            )

    _write_csv(output_dir / "live_call_manifest.csv", _manifest_fields(), manifest_rows)
    _write_csv(output_dir / "annotation_schema_validation.csv", _schema_fields(), schema_rows)
    _write_csv(output_dir / "stage_b_validation_summary.csv", _stage_b_fields(), stage_b_rows)
    _write_jsonl(output_dir / "safe_annotation_outputs.jsonl", safe_output_rows)
    return 0


def _load_provider_env() -> ProviderEnv:
    provider = os.environ.get("SQLRB_LLM_PROVIDER", "openai_compatible").strip() or "openai_compatible"
    model = _first_env(("SQLRB_LLM_MODEL", "GPTSAPI_MODEL"), "gpt-5.4")[0]
    base_url, _ = _first_env(("SQLRB_LLM_BASE_URL", "GPTSAPI_BASE_URL"), "https://api.gptsapi.net/v1")
    api_key, api_key_env = _first_env(("SQLRB_LLM_API_KEY", "GPTSAPI_API_KEY"), "")
    auth_header = os.environ.get("SQLRB_LLM_AUTH_HEADER", "authorization_bearer").strip() or "authorization_bearer"
    return ProviderEnv(
        provider=provider,
        model=model,
        base_url=base_url.rstrip("/"),
        base_url_host=urlparse(base_url).netloc or "unknown",
        api_key=api_key,
        api_key_env_used=api_key_env,
        auth_header=auth_header,
        allow_live_env=os.environ.get("SQLRB_LLM_ALLOW_LIVE") == "1",
    )


def _selected_rows(repo_root: Path, args: argparse.Namespace, requested_cases: tuple[str, ...], by_case: dict[str, tuple[object, object]]) -> tuple[list[str], list[dict[str, object]]]:
    fields = [
        "case_id",
        "pool",
        "engine",
        "source_sql_path",
        "candidate_sql_path",
        "method_id",
        "route_id",
        "candidate_source_status",
        "selected",
        "notes",
    ]
    rows: list[dict[str, object]] = []
    for case_id in requested_cases:
        member, _contract = by_case[case_id]
        source_path = member.case_path / "sql/source.sql"
        candidate_path = args.candidate_run_root / "candidate_sql" / f"{case_id}__{args.engine}.sql"
        candidate_ready = (repo_root / candidate_path).exists() and (repo_root / candidate_path).is_file()
        source_ready = (repo_root / source_path).exists() and (repo_root / source_path).is_file()
        rows.append(
            {
                "case_id": case_id,
                "pool": member.pool,
                "engine": args.engine,
                "source_sql_path": source_path.as_posix(),
                "candidate_sql_path": candidate_path.as_posix(),
                "method_id": args.method_id,
                "route_id": args.route_id,
                "candidate_source_status": "ready" if candidate_ready and source_ready else "missing_or_ambiguous",
                "selected": "true",
                "notes": "Existing route-labeled local candidate artifact; read-only input for Stage A smoke.",
            }
        )
    return fields, rows


def _write_smoke_not_run(
    output_dir: Path,
    args: argparse.Namespace,
    provider_env: ProviderEnv,
    candidate_blockers: list[dict[str, object]],
) -> None:
    reasons: list[str] = []
    if not args.live_enabled:
        reasons.append("`--live-enabled` was not provided.")
    if not provider_env.allow_live_env:
        reasons.append("`SQLRB_LLM_ALLOW_LIVE=1` is not set.")
    if not provider_env.api_key:
        reasons.append("No API key environment variable is set.")
    if not provider_env.base_url:
        reasons.append("No OpenAI-compatible base URL is configured.")
    if not provider_env.model:
        reasons.append("No model label is configured.")
    if candidate_blockers:
        reasons.append("One or more selected rows lack a clear existing route-labeled candidate SQL artifact.")
    body = "\n".join(f"- {reason}" for reason in reasons)
    (output_dir / "smoke_not_run.md").write_text(
        "# Smoke Not Run\n\n"
        "The bounded live Stage A annotation smoke did not run.\n\n"
        "Reasons:\n\n"
        f"{body}\n\n"
        "No API call, DB/checker/timing run, baseline rerun, official POCR computation, or route-level aggregation occurred.\n",
        encoding="utf-8",
    )


def _write_empty_outputs(output_dir: Path) -> None:
    _write_csv(output_dir / "live_call_manifest.csv", _manifest_fields(), [])
    _write_csv(output_dir / "annotation_schema_validation.csv", _schema_fields(), [])
    _write_csv(output_dir / "stage_b_validation_summary.csv", _stage_b_fields(), [])
    _write_jsonl(output_dir / "safe_annotation_outputs.jsonl", [])


def _manifest_fields() -> list[str]:
    return [
        "case_id",
        "pool",
        "engine",
        "method_id",
        "route_id",
        "provider_label",
        "model_label",
        "base_url_host",
        "live_enabled_flag",
        "live_enabled_env",
        "api_key_env_present",
        "api_key_env_used",
        "call_timestamp_utc",
        "prompt_template_id",
        "annotation_schema_version",
        "prompt_sha256",
        "source_sql_sha256",
        "candidate_sql_sha256",
        "success",
        "status",
        "prompt_tokens",
        "completion_tokens",
        "total_tokens",
        "error",
        "notes",
    ]


def _schema_fields() -> list[str]:
    return [
        "case_id",
        "pool",
        "engine",
        "live_call_attempted",
        "json_parse_status",
        "schema_validation_status",
        "issue_codes",
        "atom_count",
        "expected_atom_count",
        "operation_atom_count",
        "semantic_guard_atom_count",
        "missing_atom_count",
        "duplicate_atom_count",
        "invalid_atom_count",
        "notes",
    ]


def _stage_b_fields() -> list[str]:
    return [
        "case_id",
        "pool",
        "engine",
        "schema_valid",
        "stage_b_status",
        "evidence_status_counts",
        "validated_operation_atoms_count",
        "expected_operation_atoms_count",
        "semantic_guard_validated_count",
        "semantic_guard_count",
        "official_pocr_computed",
        "route_level_pocr_aggregated",
        "notes",
    ]


def _first_env(names: tuple[str, ...], default: str) -> tuple[str, str]:
    for name in names:
        value = os.environ.get(name)
        if value:
            return value, name
    return default, ""


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def _read_optional(path: Path) -> str | None:
    return _read_text(path) if path.exists() else None


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def _redact(value: str, secret: str) -> str:
    return value.replace(secret, "[REDACTED]") if secret else value


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
