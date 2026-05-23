"""Exact-gated local timing diagnostics for user-entry runs.

This module writes local timing artifacts under ``runs/user/<run>/timing``.
It is opt-in, exact-gated, and local-only. It does not compute official
metrics, update reports/results, promote retained evidence, or create
leaderboard outputs.
"""

from __future__ import annotations

import hashlib
import json
import platform
import re
import statistics
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .case_package_resolver import ResolvedCasePackage
from .case_selection import SelectedCaseEngineRow
from .user_run_schema import (
    CANDIDATE_PREFLIGHT_STATUS_PASSED,
    CHECKER_STATUS_SUCCESS,
    DIAGNOSTIC_MODE_CROSS_DIALECT_REFERENCE,
    DIAGNOSTIC_MODE_SAME_ENGINE,
    EXACT_STATUS_EXACT,
    EXECUTION_STATUS_CANDIDATE_SUCCESS,
    EXECUTION_STATUS_SOURCE_SUCCESS,
    FAILURE_NONE,
)

TIMING_STATUS_NOT_ELIGIBLE = "not_eligible"
TIMING_STATUS_TIMED = "timed"
TIMING_STATUS_PARTIAL_FAILURE = "partial_failure"
TIMING_STATUS_FAILED_INTERNAL = "failed_internal"


@dataclass(frozen=True)
class TimingPolicy:
    timing_policy_id: str = "local_exact_gated_default_v0"
    warmup_count: int = 1
    measured_repetitions: int = 5
    timeout_seconds: float = 30.0
    statistic: str = "median"
    exact_gated: bool = True
    execution_order_policy: str = "source_then_candidate"
    cache_policy: str = "recorded_not_controlled"
    connection_session_policy: str = "engine_default_session_per_timing_row"
    schema_setup_policy: str = "fresh_schema_per_timing_row"
    transaction_policy: str = "engine_default"
    retry_policy: str = "no_retries"
    partial_sample_policy: str = "visible_partial_failure_no_speedup"
    sample_storage: str = "inline_json_arrays"
    claim_boundary: str = "local_diagnostic_only"


@dataclass(frozen=True)
class TimingSamples:
    source_runtime_samples_ms: list[float]
    candidate_runtime_samples_ms: list[float]
    engine_version: str = ""


@dataclass(frozen=True)
class LocalTimingResult:
    timing_eligible: bool
    timing_status: str
    timing_na_reason: str
    speedup_ratio: float | None
    timing_artifact_path: Path
    source_runtime_samples_ms: list[float]
    candidate_runtime_samples_ms: list[float]


def route_identity(adapter_command: str) -> tuple[str, str]:
    """Return route/method ids suitable for local diagnostic grouping."""

    text = adapter_command.strip()
    if (
        "calcite_hep_fail_closed_adapter" in text
        or "sql_rewrite_bench.calcite_hep_fail_closed_adapter" in text
        or re.search(r"--route(?:=|\s+)calcite_hep_fail_closed\b", text)
    ):
        return "calcite_hep_fail_closed", "calcite_hep_fail_closed"
    if "sqlglot_user_adapter.py" in text:
        route_match = re.search(r"--route(?:=|\s+)([A-Za-z0-9_.-]+)", text)
        route = route_match.group(1) if route_match else "unknown"
        return f"sqlglot_{_safe_id(route)}", "sqlglot"
    digest = hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]
    return f"adapter_{digest}", "user_adapter"


def write_timing_policy(timing_dir: Path, policy: TimingPolicy) -> Path:
    timing_dir.mkdir(parents=True, exist_ok=True)
    path = timing_dir / "timing_policy.json"
    payload = {
        "schema_version": "timing_policy_schema_v0",
        **asdict(policy),
        "allowed_timing_scopes": ["same_engine"],
        "local_diagnostic_only": True,
        "official_metric_input": False,
        "paper_result_input": False,
        "retained_evidence_promoted": False,
        "leaderboard_input": False,
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def write_environment_metadata(timing_dir: Path, *, repo_root: Path, run_id: str) -> Path:
    timing_dir.mkdir(parents=True, exist_ok=True)
    path = timing_dir / "environment_metadata.json"
    payload = {
        "schema_version": "timing_environment_metadata_v0",
        "environment_metadata_id": f"{run_id}:local",
        "created_at_utc": _utc_now_iso(),
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "repo_root_name": repo_root.name,
        "secret_redaction_policy": "no secrets or full environment dumps recorded",
        "claim_boundary": "local_diagnostic_only",
        "local_diagnostic_only": True,
        "official_metric_input": False,
        "paper_result_input": False,
        "retained_evidence_promoted": False,
        "leaderboard_input": False,
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def collect_timing_for_row(
    *,
    ledger: dict[str, object],
    row: SelectedCaseEngineRow,
    resolved_package: ResolvedCasePackage,
    repo_root: Path,
    out_dir: Path,
    run_id: str,
    adapter_command: str,
    policy: TimingPolicy,
    postgres_dsn_env: str,
    db_schema_prefix: str,
    timing_dir: Path,
    environment_metadata_path: Path,
) -> LocalTimingResult:
    """Write one timing row JSON artifact and return local timing status."""

    rows_dir = timing_dir / "rows"
    rows_dir.mkdir(parents=True, exist_ok=True)
    route_id, method_id = route_identity(adapter_command)
    candidate_id = f"{row.case_id}__{row.engine}__candidate"
    artifact_path = rows_dir / f"{row.case_id}__{row.engine}__{route_id}__{candidate_id}.json"
    source_sql_path = _source_sql_path(repo_root, row, resolved_package)
    candidate_sql_path = _candidate_sql_path(repo_root, ledger)
    timing_scope = _timing_scope(resolved_package)
    label_only = _label_only_mismatch(ledger)
    na_reason = _timing_ineligible_reason(ledger, resolved_package, label_only)

    samples = TimingSamples([], [], "")
    timing_status = TIMING_STATUS_NOT_ELIGIBLE
    speedup_ratio: float | None = None
    timing_eligible = na_reason == ""

    if timing_eligible:
        try:
            samples = _collect_samples_for_engine(
                row=row,
                resolved_package=resolved_package,
                repo_root=repo_root,
                out_dir=out_dir,
                run_id=run_id,
                candidate_sql_path=candidate_sql_path,
                policy=policy,
                postgres_dsn_env=postgres_dsn_env,
                db_schema_prefix=db_schema_prefix,
                timing_dir=timing_dir,
            )
            complete = _samples_complete(samples, policy)
            if complete:
                source_median = _median(samples.source_runtime_samples_ms)
                candidate_median = _median(samples.candidate_runtime_samples_ms)
                if source_median is not None and candidate_median is not None and source_median > 0 and candidate_median > 0:
                    speedup_ratio = source_median / candidate_median
                    timing_status = TIMING_STATUS_TIMED
                    na_reason = ""
                else:
                    timing_status = TIMING_STATUS_PARTIAL_FAILURE
                    na_reason = "non_positive_median"
            else:
                timing_status = TIMING_STATUS_PARTIAL_FAILURE
                na_reason = "timing_partial_failure"
        except Exception as exc:
            timing_status = TIMING_STATUS_PARTIAL_FAILURE
            na_reason = f"timing_partial_failure:{type(exc).__name__}"

    payload = _timing_payload(
        ledger=ledger,
        row=row,
        resolved_package=resolved_package,
        route_id=route_id,
        method_id=method_id,
        candidate_id=candidate_id,
        run_id=run_id,
        timing_scope=timing_scope,
        policy=policy,
        timing_eligible=timing_eligible,
        timing_status=timing_status,
        timing_na_reason=na_reason,
        samples=samples,
        speedup_ratio=speedup_ratio,
        source_sql_path=source_sql_path,
        candidate_sql_path=candidate_sql_path,
        repo_root=repo_root,
        environment_metadata_path=environment_metadata_path,
    )
    artifact_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return LocalTimingResult(
        timing_eligible=timing_eligible,
        timing_status=timing_status,
        timing_na_reason=na_reason,
        speedup_ratio=speedup_ratio,
        timing_artifact_path=artifact_path,
        source_runtime_samples_ms=samples.source_runtime_samples_ms,
        candidate_runtime_samples_ms=samples.candidate_runtime_samples_ms,
    )


def _timing_ineligible_reason(
    ledger: dict[str, object],
    resolved_package: ResolvedCasePackage,
    label_only: bool,
) -> str:
    if ledger.get("candidate_generated") != "true":
        return "generated_missing"
    if ledger.get("candidate_preflight_status") != CANDIDATE_PREFLIGHT_STATUS_PASSED:
        return "preflight_failed"
    if ledger.get("source_execution_status") != EXECUTION_STATUS_SOURCE_SUCCESS:
        if ledger.get("failure_bucket") == "unsupported_engine":
            return "unsupported_fail_closed"
        return "source_execution_failed"
    if ledger.get("candidate_execution_status") != EXECUTION_STATUS_CANDIDATE_SUCCESS:
        if ledger.get("failure_bucket") == "unsupported_engine":
            return "unsupported_fail_closed"
        return "candidate_execution_failed"
    if ledger.get("checker_status") != CHECKER_STATUS_SUCCESS:
        return "checker_not_success"
    if label_only:
        return "label_only_mismatch"
    if ledger.get("exact_status") != EXACT_STATUS_EXACT:
        return "checker_mismatch"
    if ledger.get("failure_bucket") != FAILURE_NONE:
        return str(ledger.get("failure_bucket") or "failure_bucket")
    if resolved_package.diagnostic_mode != DIAGNOSTIC_MODE_SAME_ENGINE:
        return "timing_scope_not_supported"
    return ""


def _collect_samples_for_engine(
    *,
    row: SelectedCaseEngineRow,
    resolved_package: ResolvedCasePackage,
    repo_root: Path,
    out_dir: Path,
    run_id: str,
    candidate_sql_path: Path,
    policy: TimingPolicy,
    postgres_dsn_env: str,
    db_schema_prefix: str,
    timing_dir: Path,
) -> TimingSamples:
    if resolved_package.diagnostic_mode != DIAGNOSTIC_MODE_SAME_ENGINE:
        raise ValueError("timing currently supports same-engine rows only")
    if row.engine == "postgres":
        return _collect_postgres_samples(
            repo_root=repo_root,
            row=row,
            run_id=run_id,
            candidate_sql_path=candidate_sql_path,
            policy=policy,
            postgres_dsn_env=postgres_dsn_env,
            db_schema_prefix=db_schema_prefix,
            timing_dir=timing_dir,
        )
    if row.engine == "mysql":
        return _collect_mysql_samples(
            repo_root=repo_root,
            row=row,
            run_id=run_id,
            candidate_sql_path=candidate_sql_path,
            policy=policy,
            db_schema_prefix=db_schema_prefix,
            timing_dir=timing_dir,
        )
    if row.engine == "spark":
        return _collect_spark_samples(
            repo_root=repo_root,
            row=row,
            run_id=run_id,
            candidate_sql_path=candidate_sql_path,
            policy=policy,
            db_schema_prefix=db_schema_prefix,
            timing_dir=timing_dir,
        )
    raise ValueError(f"unsupported timing engine: {row.engine}")


def _collect_postgres_samples(
    *,
    repo_root: Path,
    row: SelectedCaseEngineRow,
    run_id: str,
    candidate_sql_path: Path,
    policy: TimingPolicy,
    postgres_dsn_env: str,
    db_schema_prefix: str,
    timing_dir: Path,
) -> TimingSamples:
    from .postgres_execution import (
        _query_script,
        _quote_ident,
        _run_psql_file,
        _schema_name,
        _setup_script,
        resolve_postgres_schema_assets,
    )

    workspace = timing_dir / "workspaces" / row.case_id / row.engine
    workspace.mkdir(parents=True, exist_ok=True)
    schema_assets = resolve_postgres_schema_assets(repo_root=repo_root, row=row)
    schema = _schema_name(db_schema_prefix, run_id, row.case_id, "postgres_timing")
    source_sql_path = repo_root / row.source_sql_path
    setup_script = workspace / "setup.sql"
    source_script = workspace / "source_query.sql"
    candidate_script = workspace / "candidate_query.sql"
    cleanup_script = workspace / "cleanup.sql"
    setup_script.write_text(_setup_script(schema, schema_assets.ddl_path, schema_assets.load_path), encoding="utf-8")
    source_script.write_text(_query_script(schema, source_sql_path), encoding="utf-8")
    candidate_script.write_text(_query_script(schema, candidate_sql_path), encoding="utf-8")
    source_samples: list[float] = []
    candidate_samples: list[float] = []
    try:
        setup = _run_psql_file(
            script_path=setup_script,
            timeout=int(policy.timeout_seconds),
            cwd=repo_root,
            dsn_env=postgres_dsn_env,
        )
        if setup.returncode != 0:
            raise RuntimeError(setup.stderr or setup.stdout or "postgres timing setup failed")
        _run_paired_command_samples(
            run_source=lambda: _run_checked_psql(source_script, policy, repo_root, postgres_dsn_env),
            run_candidate=lambda: _run_checked_psql(candidate_script, policy, repo_root, postgres_dsn_env),
            policy=policy,
            source_samples=source_samples,
            candidate_samples=candidate_samples,
        )
    finally:
        cleanup_script.write_text(f"DROP SCHEMA IF EXISTS {_quote_ident(schema)} CASCADE;\n", encoding="utf-8")
        try:
            _run_psql_file(
                script_path=cleanup_script,
                timeout=int(policy.timeout_seconds),
                cwd=repo_root,
                dsn_env=postgres_dsn_env,
            )
        except Exception:
            pass
    return TimingSamples(source_samples, candidate_samples)


def _run_checked_psql(script_path: Path, policy: TimingPolicy, repo_root: Path, dsn_env: str) -> None:
    from .postgres_execution import _run_psql_file

    completed = _run_psql_file(
        script_path=script_path,
        timeout=int(policy.timeout_seconds),
        cwd=repo_root,
        dsn_env=dsn_env,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr or completed.stdout or f"psql failed: {script_path}")


def _collect_mysql_samples(
    *,
    repo_root: Path,
    row: SelectedCaseEngineRow,
    run_id: str,
    candidate_sql_path: Path,
    policy: TimingPolicy,
    db_schema_prefix: str,
    timing_dir: Path,
) -> TimingSamples:
    from .mysql_execution import (
        _database_name,
        _query_script,
        _quote_ident,
        _run_mysql_file,
        _setup_script,
        resolve_mysql_schema_assets,
    )

    workspace = timing_dir / "workspaces" / row.case_id / row.engine
    workspace.mkdir(parents=True, exist_ok=True)
    schema_assets = resolve_mysql_schema_assets(repo_root=repo_root, row=row)
    database = _database_name(db_schema_prefix, run_id, row.case_id, "mysql_timing")
    source_sql_path = repo_root / row.source_sql_path
    setup_script = workspace / "setup.sql"
    source_script = workspace / "source_query.sql"
    candidate_script = workspace / "candidate_query.sql"
    cleanup_script = workspace / "cleanup.sql"
    setup_script.write_text(_setup_script(database, schema_assets.ddl_path, schema_assets.load_path), encoding="utf-8")
    source_script.write_text(_query_script(database, source_sql_path), encoding="utf-8")
    candidate_script.write_text(_query_script(database, candidate_sql_path), encoding="utf-8")
    source_samples: list[float] = []
    candidate_samples: list[float] = []
    try:
        setup = _run_mysql_file(script_path=setup_script, timeout=int(policy.timeout_seconds), cwd=repo_root)
        if setup.returncode != 0:
            raise RuntimeError(setup.stderr or setup.stdout or "mysql timing setup failed")
        _run_paired_command_samples(
            run_source=lambda: _run_checked_mysql(source_script, policy, repo_root),
            run_candidate=lambda: _run_checked_mysql(candidate_script, policy, repo_root),
            policy=policy,
            source_samples=source_samples,
            candidate_samples=candidate_samples,
        )
    finally:
        cleanup_script.write_text(f"DROP DATABASE IF EXISTS {_quote_ident(database)};\n", encoding="utf-8")
        try:
            _run_mysql_file(script_path=cleanup_script, timeout=int(policy.timeout_seconds), cwd=repo_root)
        except Exception:
            pass
    return TimingSamples(source_samples, candidate_samples)


def _run_checked_mysql(script_path: Path, policy: TimingPolicy, repo_root: Path) -> None:
    from .mysql_execution import _run_mysql_file

    completed = _run_mysql_file(
        script_path=script_path,
        timeout=int(policy.timeout_seconds),
        cwd=repo_root,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr or completed.stdout or f"mysql failed: {script_path}")


def _collect_spark_samples(
    *,
    repo_root: Path,
    row: SelectedCaseEngineRow,
    run_id: str,
    candidate_sql_path: Path,
    policy: TimingPolicy,
    db_schema_prefix: str,
    timing_dir: Path,
) -> TimingSamples:
    from .spark_execution import (
        SPARK_APP_NAME_ENV,
        _create_spark_session,
        _database_name,
        _execute_statement_batch,
        _split_sql_statements,
        resolve_spark_schema_assets,
    )
    import os

    workspace = timing_dir / "workspaces" / row.case_id / row.engine
    workspace.mkdir(parents=True, exist_ok=True)
    schema_assets = resolve_spark_schema_assets(repo_root=repo_root, row=row)
    database = _database_name(db_schema_prefix, run_id, row.case_id + "_timing")
    source_sql_path = repo_root / row.source_sql_path
    setup_sql = "\n".join(
        [
            f"DROP DATABASE IF EXISTS {database} CASCADE;",
            f"CREATE DATABASE IF NOT EXISTS {database};",
            f"USE {database};",
            schema_assets.ddl_path.read_text(encoding="utf-8"),
            schema_assets.load_path.read_text(encoding="utf-8"),
            "",
        ]
    )
    source_statements = _split_sql_statements(source_sql_path.read_text(encoding="utf-8"))
    candidate_statements = _split_sql_statements(candidate_sql_path.read_text(encoding="utf-8"))
    if len(source_statements) != 1 or len(candidate_statements) != 1:
        raise ValueError("Spark timing requires exactly one source and candidate statement")
    source_samples: list[float] = []
    candidate_samples: list[float] = []
    spark = None
    try:
        spark = _create_spark_session(
            app_name=os.environ.get(SPARK_APP_NAME_ENV, f"SQLRB {run_id} {row.case_id} timing"),
            warehouse_dir=workspace / "spark_warehouse",
        )
        _execute_statement_batch(spark, _split_sql_statements(setup_sql))
        _run_paired_command_samples(
            run_source=lambda: spark.sql(source_statements[0]).collect(),
            run_candidate=lambda: spark.sql(candidate_statements[0]).collect(),
            policy=policy,
            source_samples=source_samples,
            candidate_samples=candidate_samples,
        )
        version = str(getattr(spark, "version", ""))
    finally:
        if spark is not None:
            try:
                spark.sql(f"DROP DATABASE IF EXISTS {database} CASCADE")
            except Exception:
                pass
            try:
                spark.stop()
            except Exception:
                pass
    return TimingSamples(source_samples, candidate_samples, version if "version" in locals() else "")


def _run_paired_command_samples(
    *,
    run_source: Any,
    run_candidate: Any,
    policy: TimingPolicy,
    source_samples: list[float],
    candidate_samples: list[float],
) -> None:
    for _ in range(policy.warmup_count):
        run_source()
        run_candidate()
    for _ in range(policy.measured_repetitions):
        source_samples.append(_elapsed_ms(run_source))
        candidate_samples.append(_elapsed_ms(run_candidate))


def _elapsed_ms(func: Any) -> float:
    start = time.perf_counter()
    func()
    return (time.perf_counter() - start) * 1000.0


def _timing_payload(
    *,
    ledger: dict[str, object],
    row: SelectedCaseEngineRow,
    resolved_package: ResolvedCasePackage,
    route_id: str,
    method_id: str,
    candidate_id: str,
    run_id: str,
    timing_scope: str,
    policy: TimingPolicy,
    timing_eligible: bool,
    timing_status: str,
    timing_na_reason: str,
    samples: TimingSamples,
    speedup_ratio: float | None,
    source_sql_path: Path,
    candidate_sql_path: Path,
    repo_root: Path,
    environment_metadata_path: Path,
) -> dict[str, Any]:
    source_median = _median(samples.source_runtime_samples_ms)
    candidate_median = _median(samples.candidate_runtime_samples_ms)
    return {
        "schema_version": "timing_artifact_schema_v0",
        "route_id": route_id,
        "method_id": method_id,
        "case_id": row.case_id,
        "pool": row.pool,
        "engine": row.engine,
        "denominator_id": row.denominator_id,
        "candidate_id": candidate_id,
        "local_run_id": run_id,
        "timing_scope": timing_scope,
        "timing_policy_id": policy.timing_policy_id,
        "diagnostic_mode": resolved_package.diagnostic_mode,
        "role_class": "same_engine" if resolved_package.diagnostic_mode == DIAGNOSTIC_MODE_SAME_ENGINE else resolved_package.diagnostic_mode,
        "candidate_generated": ledger.get("candidate_generated") == "true",
        "candidate_preflight_status": ledger.get("candidate_preflight_status", ""),
        "source_execution_status": ledger.get("source_execution_status", ""),
        "candidate_execution_status": ledger.get("candidate_execution_status", ""),
        "checker_status": ledger.get("checker_status", ""),
        "exact_status": ledger.get("exact_status", ""),
        "failure_bucket": ledger.get("failure_bucket", ""),
        "value_exact": _label_diagnostic_value(ledger, "value_exact"),
        "label_exact": _label_diagnostic_value(ledger, "label_exact"),
        "label_only_mismatch": _label_only_mismatch(ledger),
        "timing_eligible": timing_eligible,
        "timing_status": timing_status,
        "timing_na_reason": timing_na_reason or None,
        "source_runtime_samples_ms": samples.source_runtime_samples_ms,
        "candidate_runtime_samples_ms": samples.candidate_runtime_samples_ms,
        "source_median_ms": source_median,
        "candidate_median_ms": candidate_median,
        "speedup_ratio": speedup_ratio,
        "speedup_na_reason": None if speedup_ratio is not None else (timing_na_reason or "not_timed"),
        "warmup_count": policy.warmup_count,
        "measured_repetitions": len(samples.source_runtime_samples_ms)
        if len(samples.source_runtime_samples_ms) == len(samples.candidate_runtime_samples_ms)
        else min(len(samples.source_runtime_samples_ms), len(samples.candidate_runtime_samples_ms)),
        "requested_repetitions": policy.measured_repetitions,
        "timeout_seconds": policy.timeout_seconds,
        "timeout_status": "none" if timing_status != TIMING_STATUS_PARTIAL_FAILURE else "partial_timeout",
        "cache_policy": policy.cache_policy,
        "connection_session_policy": policy.connection_session_policy,
        "schema_setup_policy": policy.schema_setup_policy,
        "execution_order_policy": policy.execution_order_policy,
        "engine_version": samples.engine_version,
        "environment_metadata_path": _relative_to_repo(environment_metadata_path, repo_root),
        "source_sql_artifact_path": _relative_to_repo(source_sql_path, repo_root),
        "candidate_sql_artifact_path": _relative_to_repo(candidate_sql_path, repo_root),
        "source_result_artifact_path": ledger.get("source_result_path", "") or None,
        "candidate_result_artifact_path": ledger.get("candidate_result_path", "") or None,
        "checker_artifact_path": ledger.get("mismatch_artifact_path", "") or None,
        "timing_log_artifact_path": None,
        "source_sql_hash": _sha256_file(source_sql_path) if source_sql_path.exists() else None,
        "candidate_sql_hash": _sha256_file(candidate_sql_path) if candidate_sql_path.exists() else None,
        "created_at_utc": _utc_now_iso(),
        "claim_boundary": "local_diagnostic_only",
        "local_diagnostic_only": True,
        "official_metric_input": False,
        "paper_result_input": False,
        "retained_evidence_promoted": False,
        "leaderboard_input": False,
    }


def _source_sql_path(
    repo_root: Path,
    row: SelectedCaseEngineRow,
    resolved_package: ResolvedCasePackage,
) -> Path:
    if resolved_package.diagnostic_mode == DIAGNOSTIC_MODE_CROSS_DIALECT_REFERENCE:
        return resolved_package.source_reference_query_path
    return repo_root / row.source_sql_path


def _candidate_sql_path(repo_root: Path, ledger: dict[str, object]) -> Path:
    raw = str(ledger.get("candidate_sql_path") or "")
    return repo_root / raw if raw else repo_root / "__missing_candidate__.sql"


def _timing_scope(resolved_package: ResolvedCasePackage) -> str:
    if resolved_package.diagnostic_mode == DIAGNOSTIC_MODE_CROSS_DIALECT_REFERENCE:
        return "cross_engine_target"
    if resolved_package.diagnostic_mode == DIAGNOSTIC_MODE_SAME_ENGINE:
        return "same_engine"
    return "unsupported"


def _samples_complete(samples: TimingSamples, policy: TimingPolicy) -> bool:
    return (
        len(samples.source_runtime_samples_ms) == policy.measured_repetitions
        and len(samples.candidate_runtime_samples_ms) == policy.measured_repetitions
    )


def _median(values: list[float]) -> float | None:
    if not values:
        return None
    return float(statistics.median(values))


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _safe_id(value: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("_")
    return safe or "unknown"


def _relative_to_repo(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _label_only_mismatch(ledger: dict[str, object]) -> bool:
    return "label_only_mismatch=true" in str(ledger.get("notes", ""))


def _label_diagnostic_value(ledger: dict[str, object], field: str) -> bool | None:
    notes = str(ledger.get("notes", ""))
    if f"{field}=true" in notes:
        return True
    if f"{field}=false" in notes:
        return False
    return None
