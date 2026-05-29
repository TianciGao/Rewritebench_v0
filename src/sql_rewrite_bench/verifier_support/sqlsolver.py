"""Bounded SQLSolver smoke support for local diagnostic verifier outputs.

The wrapper is intentionally narrow. It detects an available SQLSolver command,
can run explicitly supplied bounded smoke pairs, and writes D035-shaped local
verifier artifacts. It does not implement broad user-facing verifier execution,
VeriEQL execution, official metrics, retained-evidence promotion, or
leaderboard output.
"""

from __future__ import annotations

import csv
import json
import os
import shlex
import shutil
import subprocess
import tempfile
import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .pairs import PAIR_FIELDS, validate_pair_record
from .summary import generate_semantic_equivalence_summary
from .verdicts import build_verdict_record

SQLSOLVER_TOOL = "sqlsolver"
DEFAULT_SQLSOLVER_COMMANDS = ("sqlsolver", "SQLSolver", "sql-solver", "sqlsolver-cli")
SQLSOLVER_ENV_VARS = ("SQLRB_SQLSOLVER_CMD", "SQLSOLVER_COMMAND", "SQLSOLVER_BIN")
SQLSOLVER_JAR_ENV_VAR = "SQLRB_SQLSOLVER_JAR"
SQLSOLVER_ROOT_ENV_VAR = "SQLRB_SQLSOLVER_ROOT"
SQLSOLVER_LD_LIBRARY_PATH_ENV_VAR = "SQLRB_SQLSOLVER_LD_LIBRARY_PATH"
SQLSOLVER_JAVA_ENV_VAR = "SQLRB_SQLSOLVER_JAVA"
SQLSOLVER_LEGACY_COMMAND_MODE = "command_cli"
SQLSOLVER_JAR_MODE = "jar_cli"
SQLSOLVER_COMMAND_SHAPE = (
    "java -jar <sqlsolver.jar> -sql1=<sql1_file> -sql2=<sql2_file> "
    "-schema=<schema_file> -output=<output_file>"
)
SQLSOLVER_GUARD_CATEGORIES = {
    "unsupported_sql_feature",
    "unsupported_postgres_dialect",
    "schema_canonicalization_gap",
    "wrapper_input_format_gap",
    "type_or_function_modeling_gap",
    "query_normalization_gap",
    "unknown_tool_behavior",
}


@dataclass(frozen=True)
class SQLSolverCanonicalizationResult:
    canonical_text: str
    safe_for_sqlsolver: bool
    guard_categories: tuple[str, ...]
    fail_closed_reason: str | None = None
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class SQLSolverSupportScopeDecision:
    sqlsolver_invocation_allowed: bool
    family: str | None
    normalized_guard_category: str | None
    normalized_verdict: str | None
    support_scope_verdict: str | None
    reason: str | None
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class SQLSolverAvailability:
    tool_available: bool
    command: tuple[str, ...] | None
    command_path: str | None
    tool_version: str | None
    detection_reason: str
    invocation_mode: str = SQLSOLVER_LEGACY_COMMAND_MODE
    jar_path: str | None = None
    sqlsolver_root: str | None = None
    ld_library_path: str | None = None
    java_command: tuple[str, ...] | None = None
    command_shape: str = "sqlsolver <sql1_file> <sql2_file> [--schema <schema_file>]"


@dataclass(frozen=True)
class SQLSolverSmokeOutput:
    run_id: str
    tool_available: bool
    tool_version: str | None
    result_verifier_dir: Path
    log_dir: Path
    report_dir: Path
    pairs_path: Path
    verdicts_path: Path
    summary_path: Path
    log_path: Path
    report_path: Path
    summary: dict[str, Any]


def canonicalize_sqlsolver_query(sql_text: str) -> SQLSolverCanonicalizationResult:
    """Prepare one SQL query for SQLSolver's line-oriented input contract.

    This is a syntax-shaping layer only. It removes comments, checks statement
    boundaries, normalizes whitespace outside literals, and leaves SQL
    semantics intact. Unsafe cases fail closed so callers do not fabricate
    verifier evidence from malformed SQLSolver input.
    """

    stripped = _strip_sql_comments(sql_text)
    if not stripped.safe_for_sqlsolver:
        return stripped
    statement = _single_statement_without_terminal_semicolon(stripped.canonical_text)
    if not statement.safe_for_sqlsolver:
        return statement
    line = _collapse_sql_whitespace(statement.canonical_text)
    categories = list(dict.fromkeys([*stripped.guard_categories, *statement.guard_categories, *_classify_query_guards(line)]))
    notes = [*stripped.notes, *statement.notes]
    if line != sql_text.strip():
        notes.append("query_line_shaped_for_sqlsolver")
    if any(category in {"unsupported_sql_feature", "unsupported_postgres_dialect"} for category in categories):
        notes.append("guard_category_reported_not_silent")
    if not line:
        return SQLSolverCanonicalizationResult(
            canonical_text="",
            safe_for_sqlsolver=False,
            guard_categories=tuple(categories or ["wrapper_input_format_gap"]),
            fail_closed_reason="empty_sql_after_canonicalization",
            notes=tuple(notes),
        )
    return SQLSolverCanonicalizationResult(
        canonical_text=line,
        safe_for_sqlsolver=True,
        guard_categories=tuple(categories),
        notes=tuple(notes),
    )


def canonicalize_sqlsolver_schema(schema_text: str) -> SQLSolverCanonicalizationResult:
    """Prepare schema DDL for SQLSolver without modifying source artifacts."""

    stripped = _strip_sql_comments(schema_text)
    if not stripped.safe_for_sqlsolver:
        return stripped
    statements = _schema_statements(stripped.canonical_text)
    if statements is None:
        return SQLSolverCanonicalizationResult(
            canonical_text="",
            safe_for_sqlsolver=False,
            guard_categories=("schema_canonicalization_gap",),
            fail_closed_reason="schema_statement_boundary_ambiguous",
            notes=("unsafe_schema_statement_boundary",),
        )
    canonical: list[str] = []
    notes = list(stripped.notes)
    categories = list(stripped.guard_categories)
    for statement in statements:
        upper = statement.strip().upper()
        if not upper:
            continue
        if upper.startswith("DROP TABLE"):
            notes.append("drop_table_preamble_removed")
            categories.append("schema_canonicalization_gap")
            continue
        if not upper.startswith("CREATE TABLE"):
            return SQLSolverCanonicalizationResult(
                canonical_text="",
                safe_for_sqlsolver=False,
                guard_categories=tuple(dict.fromkeys([*categories, "schema_canonicalization_gap"])),
                fail_closed_reason="unsupported_schema_statement",
                notes=tuple([*notes, f"unsupported_schema_statement:{upper.split()[0]}"]),
            )
        normalized = _normalize_schema_types(_collapse_sql_whitespace(statement))
        if normalized != _collapse_sql_whitespace(statement):
            notes.append("schema_type_normalized")
            categories.append("schema_canonicalization_gap")
        canonical.append(normalized)
    if not canonical:
        return SQLSolverCanonicalizationResult(
            canonical_text="",
            safe_for_sqlsolver=False,
            guard_categories=tuple(dict.fromkeys([*categories, "schema_canonicalization_gap"])),
            fail_closed_reason="no_create_table_schema_statement",
            notes=tuple(notes),
        )
    return SQLSolverCanonicalizationResult(
        canonical_text="\n".join(canonical) + "\n",
        safe_for_sqlsolver=True,
        guard_categories=tuple(dict.fromkeys(categories)),
        notes=tuple(dict.fromkeys(notes)),
    )


def classify_sqlsolver_guard(sql_text: str, schema_text: str | None = None) -> tuple[str, ...]:
    """Classify SQLSolver support risks without claiming verifier evidence."""

    categories = list(_classify_query_guards(sql_text))
    if schema_text is not None:
        schema = canonicalize_sqlsolver_schema(schema_text)
        categories.extend(schema.guard_categories)
        if not schema.safe_for_sqlsolver:
            categories.append("schema_canonicalization_gap")
    return tuple(dict.fromkeys(category for category in categories if category in SQLSOLVER_GUARD_CATEGORIES))


def sqlsolver_support_scope_decision(sql_text: str) -> SQLSolverSupportScopeDecision:
    """Return whether a canonical SQL query is in current SQLSolver support scope."""

    family = _known_no_support_family(sql_text)
    if family is None:
        return SQLSolverSupportScopeDecision(
            sqlsolver_invocation_allowed=True,
            family=None,
            normalized_guard_category=None,
            normalized_verdict=None,
            support_scope_verdict=None,
            reason=None,
            notes=(),
        )
    category = "unsupported_sql_feature" if family == "dense_rank_cte_ranking" else "unsupported_postgres_dialect"
    return SQLSolverSupportScopeDecision(
        sqlsolver_invocation_allowed=False,
        family=family,
        normalized_guard_category=category,
        normalized_verdict="unsupported",
        support_scope_verdict="no_verifier_support",
        reason=f"{family}_outside_current_sqlsolver_support_scope",
        notes=("blocked_before_sqlsolver_invocation", "verifier_support_boundary_not_method_failure"),
    )


def detect_sqlsolver(
    command: str | Sequence[str] | None = None,
    *,
    env: Mapping[str, str] | None = None,
    search_path: str | None = None,
    version_timeout_seconds: float = 5.0,
) -> SQLSolverAvailability:
    """Detect a local SQLSolver command or external SQLSolver JAR.

    The preferred SQL-RewriteBench integration path is the official SQLSolver
    JAR outside this repository, discovered through ``SQLRB_SQLSOLVER_JAR`` or
    ``SQLRB_SQLSOLVER_ROOT``. The older command-style path is retained for
    fail-closed tests and local developer shims.
    """

    effective_env = dict(os.environ if env is None else env)
    if command:
        explicit = _split_command(command)
        jar_availability = _detect_explicit_jar_command(
            explicit,
            effective_env,
            search_path=search_path,
            version_timeout_seconds=version_timeout_seconds,
        )
        if jar_availability is not None:
            return jar_availability
        return _detect_legacy_command(
            explicit,
            search_path=search_path,
            version_timeout_seconds=version_timeout_seconds,
        )

    jar_availability = _detect_env_jar(
        effective_env,
        search_path=search_path,
        version_timeout_seconds=version_timeout_seconds,
    )
    if jar_availability is not None:
        return jar_availability

    for candidate in _candidate_commands(command, effective_env, search_path=search_path):
        availability = _detect_legacy_command(
            candidate,
            search_path=search_path,
            version_timeout_seconds=version_timeout_seconds,
        )
        if availability.tool_available:
            return availability
    return SQLSolverAvailability(
        tool_available=False,
        command=None,
        command_path=None,
        tool_version=None,
        detection_reason="sqlsolver_command_not_found",
    )


def build_sqlsolver_jar_command(
    *,
    java_command: Sequence[str],
    jar_path: str | Path,
    sql1_path: str | Path,
    sql2_path: str | Path,
    schema_path: str | Path,
    output_path: str | Path,
    print_output: bool = False,
) -> list[str]:
    """Build the official SQLSolver JAR CLI invocation."""

    command = [
        *[str(part) for part in java_command],
        "-jar",
        str(jar_path),
        f"-sql1={sql1_path}",
        f"-sql2={sql2_path}",
        f"-schema={schema_path}",
    ]
    if print_output:
        command.append("-print")
    command.append(f"-output={output_path}")
    return command


def normalize_sqlsolver_output(
    *,
    stdout: str,
    stderr: str = "",
    output_text: str = "",
    returncode: int = 0,
    timed_out: bool = False,
) -> str:
    """Map bounded SQLSolver-like process output to the shared verdict vocabulary."""

    if timed_out:
        return "timeout"
    text = f"{output_text}\n{stdout}\n{stderr}".strip()
    compact = text.lower().replace("-", "_").replace(" ", "_")
    if any(token in compact for token in ["timeout", "timed_out", "time_limit_exceeded"]):
        return "timeout"
    if any(token in compact for token in ["unsupported", "not_supported", "unsupported_sql", "unsupported_syntax"]):
        return "unsupported"
    if returncode != 0:
        return "tool_error"
    official = _normalize_official_result_lines(text)
    if official is not None:
        return official
    if any(
        token in compact
        for token in [
            "non_equivalent",
            "not_equivalent",
            "not_equiv",
            "inequivalent",
            "counterexample",
            "counter_example",
            "refute",
            "refuted",
            "refutation",
            "not_valid",
            "invalid",
            "not_proved",
            "disproved",
        ]
    ):
        return "non_equivalent"
    if any(
        token in compact
        for token in [
            "equivalent",
            "semantically_equivalent",
            "verified",
            "proved",
            "valid",
            "same_result",
        ]
    ):
        return "equivalent"
    if any(token in compact for token in ["unknown", "inconclusive", "undecidable"]):
        return "unknown"
    if returncode != 0:
        return "tool_error"
    if text:
        return "tool_error"
    return "unknown"


def write_sqlsolver_smoke(
    *,
    output_root: str | Path,
    run_id: str,
    pair_records: list[Mapping[str, Any]],
    command: str | Sequence[str] | None = None,
    timeout_seconds: float = 30.0,
    env: Mapping[str, str] | None = None,
    search_path: str | None = None,
    result_consistent_pairs: int | None = None,
) -> SQLSolverSmokeOutput:
    """Run a bounded SQLSolver smoke or write fail-closed unavailable outputs."""

    availability = detect_sqlsolver(command=command, env=env, search_path=search_path)
    root = Path(output_root)
    verifier_dir = root / "results" / run_id / "verifier"
    log_dir = root / "logs" / run_id
    report_dir = root / "reports" / run_id
    verifier_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)

    pairs = [_validate_sqlsolver_pair(record) for record in pair_records]
    pairs_path = verifier_dir / "verifier_pairs.csv"
    with pairs_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=PAIR_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(pairs)

    verdict_records = []
    for pair in pairs:
        if availability.tool_available and availability.command:
            record = _run_available_pair(
                pair=pair,
                availability=availability,
                verifier_dir=verifier_dir,
                timeout_seconds=timeout_seconds,
                env=env,
            )
        else:
            record = _not_attempted_pair(
                pair=pair,
                verifier_dir=verifier_dir,
                timeout_seconds=timeout_seconds,
                reason=availability.detection_reason,
            )
        verdict_records.append(record)

    verdicts_path = verifier_dir / "verifier_verdicts.jsonl"
    with verdicts_path.open("w", encoding="utf-8") as handle:
        for record in verdict_records:
            handle.write(json.dumps(record, sort_keys=True) + "\n")

    summary = generate_semantic_equivalence_summary(
        run_id=run_id,
        verdict_rows=verdict_records,
        verifier_tools_requested=[SQLSOLVER_TOOL],
        pairs_planned=len(pairs),
        result_consistent_pairs=result_consistent_pairs,
    )
    summary["tool_available"] = availability.tool_available
    summary["tool_version"] = availability.tool_version
    if not availability.tool_available:
        summary["na_reason"] = "sqlsolver_unavailable"
    summary_path = verifier_dir / "semantic_equivalence_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    log_path = log_dir / "verifier.log"
    log_path.write_text(_log_text(availability, len(pairs)), encoding="utf-8")
    report_path = report_dir / "verifier_summary.md"
    report_path.write_text(_report_text(summary, availability), encoding="utf-8")

    return SQLSolverSmokeOutput(
        run_id=run_id,
        tool_available=availability.tool_available,
        tool_version=availability.tool_version,
        result_verifier_dir=verifier_dir,
        log_dir=log_dir,
        report_dir=report_dir,
        pairs_path=pairs_path,
        verdicts_path=verdicts_path,
        summary_path=summary_path,
        log_path=log_path,
        report_path=report_path,
        summary=summary,
    )


def _run_available_pair(
    *,
    pair: dict[str, str],
    availability: SQLSolverAvailability,
    verifier_dir: Path,
    timeout_seconds: float,
    env: Mapping[str, str] | None,
) -> dict[str, Any]:
    if availability.invocation_mode == SQLSOLVER_JAR_MODE:
        return _run_available_jar_pair(
            pair=pair,
            availability=availability,
            verifier_dir=verifier_dir,
            timeout_seconds=timeout_seconds,
            env=env,
        )
    return _run_available_command_pair(
        pair=pair,
        availability=availability,
        verifier_dir=verifier_dir,
        timeout_seconds=timeout_seconds,
        env=env,
    )


def _run_available_command_pair(
    *,
    pair: dict[str, str],
    availability: SQLSolverAvailability,
    verifier_dir: Path,
    timeout_seconds: float,
    env: Mapping[str, str] | None,
) -> dict[str, Any]:
    pair_id = pair["pair_id"]
    tool_dir = verifier_dir / "tools" / SQLSOLVER_TOOL / pair_id
    tool_dir.mkdir(parents=True, exist_ok=True)
    stdout_path = tool_dir / "raw_stdout.txt"
    stderr_path = tool_dir / "raw_stderr.txt"
    comparison_path = _comparison_sql_path(pair)
    try:
        source_prepared = canonicalize_sqlsolver_query(Path(pair["source_sql_path"]).read_text(encoding="utf-8"))
        comparison_prepared = canonicalize_sqlsolver_query(Path(comparison_path).read_text(encoding="utf-8"))
        schema_prepared = (
            canonicalize_sqlsolver_schema(Path(pair["schema_context_path"]).read_text(encoding="utf-8"))
            if pair.get("schema_context_path")
            else SQLSolverCanonicalizationResult("", True, ())
        )
    except OSError:
        source_prepared = SQLSolverCanonicalizationResult("", True, ())
        comparison_prepared = SQLSolverCanonicalizationResult("", True, ())
        schema_prepared = SQLSolverCanonicalizationResult("", True, ())
    support_decision = _pair_support_scope_decision(source_prepared, comparison_prepared)
    if not support_decision.sqlsolver_invocation_allowed:
        raw_output_path = tool_dir / "sqlsolver_output.txt"
        return _support_scope_guarded_pair(
            pair=pair,
            tool_dir=tool_dir,
            stdout_path=stdout_path,
            stderr_path=stderr_path,
            raw_output_path=raw_output_path,
            timeout_seconds=timeout_seconds,
            availability=availability,
            support_decision=support_decision,
            source_prepared=source_prepared,
            comparison_prepared=comparison_prepared,
            schema_prepared=schema_prepared,
        )
    command = [*(availability.command or ()), pair["source_sql_path"], comparison_path]
    if pair.get("schema_context_path"):
        command.extend(["--schema", pair["schema_context_path"]])
    started = time.monotonic()
    timed_out = False
    try:
        completed = subprocess.run(
            command,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout_seconds,
            env=dict(os.environ if env is None else env),
        )
        stdout = completed.stdout
        stderr = completed.stderr
        returncode = completed.returncode
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        stdout = exc.stdout if isinstance(exc.stdout, str) else ""
        stderr = exc.stderr if isinstance(exc.stderr, str) else ""
        returncode = 124
    runtime_ms = (time.monotonic() - started) * 1000
    stdout_path.write_text(stdout, encoding="utf-8")
    stderr_path.write_text(stderr, encoding="utf-8")
    normalized = normalize_sqlsolver_output(stdout=stdout, stderr=stderr, returncode=returncode, timed_out=timed_out)
    invocation_status = "completed"
    if normalized in {"timeout", "unsupported", "tool_error"}:
        invocation_status = normalized
    return build_verdict_record(
        pair_id=pair_id,
        tool=SQLSOLVER_TOOL,
        raw_verdict=normalized,
        invocation_status=invocation_status,
        tool_version=availability.tool_version or "unknown",
        raw_stdout_path=stdout_path.as_posix(),
        raw_stderr_path=stderr_path.as_posix(),
        runtime_ms=runtime_ms,
        timeout_seconds=timeout_seconds,
        artifact_paths={
            "tool_dir": tool_dir.as_posix(),
            "command": _redacted_command(command),
            "command_shape": availability.command_shape,
            "verifier_mode": availability.invocation_mode,
            "tool_available": True,
            "result_checker_exactness_used": False,
            "local_only": True,
            "official_metric_input": False,
        },
    )


def _run_available_jar_pair(
    *,
    pair: dict[str, str],
    availability: SQLSolverAvailability,
    verifier_dir: Path,
    timeout_seconds: float,
    env: Mapping[str, str] | None,
) -> dict[str, Any]:
    pair_id = pair["pair_id"]
    tool_dir = verifier_dir / "tools" / SQLSOLVER_TOOL / pair_id
    tool_dir.mkdir(parents=True, exist_ok=True)
    stdout_path = tool_dir / "raw_stdout.txt"
    stderr_path = tool_dir / "raw_stderr.txt"
    raw_output_path = tool_dir / "sqlsolver_output.txt"
    if not availability.jar_path or not availability.java_command:
        return _tool_error_pair(
            pair=pair,
            tool_dir=tool_dir,
            stdout_path=stdout_path,
            stderr_path=stderr_path,
            raw_output_path=raw_output_path,
            timeout_seconds=timeout_seconds,
            reason="sqlsolver_jar_invocation_incomplete",
            availability=availability,
        )
    schema_context = pair.get("schema_context_path")
    if not schema_context:
        return _tool_error_pair(
            pair=pair,
            tool_dir=tool_dir,
            stdout_path=stdout_path,
            stderr_path=stderr_path,
            raw_output_path=raw_output_path,
            timeout_seconds=timeout_seconds,
            reason="sqlsolver_schema_context_missing",
            availability=availability,
        )

    comparison_path = _comparison_sql_path(pair)
    try:
        source_raw = Path(pair["source_sql_path"]).read_text(encoding="utf-8")
        comparison_raw = Path(comparison_path).read_text(encoding="utf-8")
        schema_raw = Path(schema_context).read_text(encoding="utf-8")
    except OSError as exc:
        return _tool_error_pair(
            pair=pair,
            tool_dir=tool_dir,
            stdout_path=stdout_path,
            stderr_path=stderr_path,
            raw_output_path=raw_output_path,
            timeout_seconds=timeout_seconds,
            reason=f"sqlsolver_input_read_failed:{type(exc).__name__}",
            availability=availability,
        )
    source_prepared = canonicalize_sqlsolver_query(source_raw)
    comparison_prepared = canonicalize_sqlsolver_query(comparison_raw)
    schema_prepared = canonicalize_sqlsolver_schema(schema_raw)
    unsafe = [
        ("source", source_prepared),
        ("comparison", comparison_prepared),
        ("schema", schema_prepared),
    ]
    unsafe = [(name, result) for name, result in unsafe if not result.safe_for_sqlsolver]
    if unsafe:
        reason = ";".join(f"{name}:{result.fail_closed_reason}" for name, result in unsafe)
        return _canonicalization_failed_pair(
            pair=pair,
            tool_dir=tool_dir,
            stdout_path=stdout_path,
            stderr_path=stderr_path,
            raw_output_path=raw_output_path,
            timeout_seconds=timeout_seconds,
            reason=reason,
            availability=availability,
            source_prepared=source_prepared,
            comparison_prepared=comparison_prepared,
            schema_prepared=schema_prepared,
        )
    support_decision = _pair_support_scope_decision(source_prepared, comparison_prepared)
    if not support_decision.sqlsolver_invocation_allowed:
        return _support_scope_guarded_pair(
            pair=pair,
            tool_dir=tool_dir,
            stdout_path=stdout_path,
            stderr_path=stderr_path,
            raw_output_path=raw_output_path,
            timeout_seconds=timeout_seconds,
            availability=availability,
            support_decision=support_decision,
            source_prepared=source_prepared,
            comparison_prepared=comparison_prepared,
            schema_prepared=schema_prepared,
        )

    started = time.monotonic()
    timed_out = False
    stdout = ""
    stderr = ""
    returncode = 0
    output_text = ""
    with tempfile.TemporaryDirectory(prefix=f"sqlrb_sqlsolver_{_safe_name(pair_id)}_") as tmp:
        tmp_path = Path(tmp)
        sql1_path = tmp_path / "sql1.sql"
        sql2_path = tmp_path / "sql2.sql"
        schema_path = tmp_path / "schema.sql"
        output_path = tmp_path / "sqlsolver_result.txt"
        sql1_path.write_text(source_prepared.canonical_text + "\n", encoding="utf-8")
        sql2_path.write_text(comparison_prepared.canonical_text + "\n", encoding="utf-8")
        schema_path.write_text(schema_prepared.canonical_text, encoding="utf-8")
        command = build_sqlsolver_jar_command(
            java_command=availability.java_command,
            jar_path=availability.jar_path,
            sql1_path=sql1_path,
            sql2_path=sql2_path,
            schema_path=schema_path,
            output_path=output_path,
        )
        try:
            completed = subprocess.run(
                command,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout_seconds,
                env=_sqlsolver_process_env(env, availability),
            )
            stdout = completed.stdout
            stderr = completed.stderr
            returncode = completed.returncode
        except subprocess.TimeoutExpired as exc:
            timed_out = True
            stdout = exc.stdout if isinstance(exc.stdout, str) else ""
            stderr = exc.stderr if isinstance(exc.stderr, str) else ""
            returncode = 124
        if output_path.exists():
            output_text = output_path.read_text(encoding="utf-8", errors="replace")

    runtime_ms = (time.monotonic() - started) * 1000
    stdout_path.write_text(stdout, encoding="utf-8")
    stderr_path.write_text(stderr, encoding="utf-8")
    raw_output_path.write_text(output_text, encoding="utf-8")
    normalized = normalize_sqlsolver_output(
        stdout=stdout,
        stderr=stderr,
        output_text=output_text,
        returncode=returncode,
        timed_out=timed_out,
    )
    invocation_status = "completed"
    if normalized in {"timeout", "unsupported", "tool_error"}:
        invocation_status = normalized
    return build_verdict_record(
        pair_id=pair_id,
        tool=SQLSOLVER_TOOL,
        raw_verdict=normalized,
        invocation_status=invocation_status,
        tool_version=availability.tool_version or "unknown",
        raw_stdout_path=stdout_path.as_posix(),
        raw_stderr_path=stderr_path.as_posix(),
        runtime_ms=runtime_ms,
        timeout_seconds=timeout_seconds,
        artifact_paths={
            "tool_dir": tool_dir.as_posix(),
            "raw_output_path": raw_output_path.as_posix(),
            "command_shape": availability.command_shape,
            "verifier_mode": SQLSOLVER_JAR_MODE,
            "jar_path": availability.jar_path,
            "ld_library_path": availability.ld_library_path,
            "canonicalization_applied": True,
            "canonicalization_mode": "temp_verifier_input_only",
            "source_guard_categories": list(source_prepared.guard_categories),
            "comparison_guard_categories": list(comparison_prepared.guard_categories),
            "schema_guard_categories": list(schema_prepared.guard_categories),
            "source_canonicalization_notes": list(source_prepared.notes),
            "comparison_canonicalization_notes": list(comparison_prepared.notes),
            "schema_canonicalization_notes": list(schema_prepared.notes),
            "tool_available": True,
            "result_checker_exactness_used": False,
            "local_only": True,
            "official_metric_input": False,
        },
    )


def _tool_error_pair(
    *,
    pair: dict[str, str],
    tool_dir: Path,
    stdout_path: Path,
    stderr_path: Path,
    raw_output_path: Path,
    timeout_seconds: float,
    reason: str,
    availability: SQLSolverAvailability,
) -> dict[str, Any]:
    stdout_path.write_text("", encoding="utf-8")
    stderr_path.write_text(reason + "\n", encoding="utf-8")
    raw_output_path.write_text("", encoding="utf-8")
    return build_verdict_record(
        pair_id=pair["pair_id"],
        tool=SQLSOLVER_TOOL,
        raw_verdict="tool_error",
        invocation_status="tool_error",
        tool_version=availability.tool_version or "unknown",
        raw_stdout_path=stdout_path.as_posix(),
        raw_stderr_path=stderr_path.as_posix(),
        runtime_ms=None,
        timeout_seconds=timeout_seconds,
        artifact_paths={
            "tool_dir": tool_dir.as_posix(),
            "raw_output_path": raw_output_path.as_posix(),
            "detection_reason": reason,
            "command_shape": availability.command_shape,
            "verifier_mode": availability.invocation_mode,
            "tool_available": availability.tool_available,
            "result_checker_exactness_used": False,
            "local_only": True,
            "official_metric_input": False,
        },
    )


def _canonicalization_failed_pair(
    *,
    pair: dict[str, str],
    tool_dir: Path,
    stdout_path: Path,
    stderr_path: Path,
    raw_output_path: Path,
    timeout_seconds: float,
    reason: str,
    availability: SQLSolverAvailability,
    source_prepared: SQLSolverCanonicalizationResult,
    comparison_prepared: SQLSolverCanonicalizationResult,
    schema_prepared: SQLSolverCanonicalizationResult,
) -> dict[str, Any]:
    stdout_path.write_text("", encoding="utf-8")
    stderr_path.write_text(f"SQLSolver canonicalization failed closed: {reason}\n", encoding="utf-8")
    raw_output_path.write_text("", encoding="utf-8")
    return build_verdict_record(
        pair_id=pair["pair_id"],
        tool=SQLSOLVER_TOOL,
        raw_verdict="unsupported",
        invocation_status="unsupported",
        tool_version=availability.tool_version or "unknown",
        raw_stdout_path=stdout_path.as_posix(),
        raw_stderr_path=stderr_path.as_posix(),
        runtime_ms=None,
        timeout_seconds=timeout_seconds,
        artifact_paths={
            "tool_dir": tool_dir.as_posix(),
            "raw_output_path": raw_output_path.as_posix(),
            "detection_reason": reason,
            "command_shape": availability.command_shape,
            "verifier_mode": availability.invocation_mode,
            "tool_available": availability.tool_available,
            "canonicalization_applied": True,
            "canonicalization_failed_closed": True,
            "canonicalization_mode": "temp_verifier_input_only",
            "source_guard_categories": list(source_prepared.guard_categories),
            "comparison_guard_categories": list(comparison_prepared.guard_categories),
            "schema_guard_categories": list(schema_prepared.guard_categories),
            "source_canonicalization_notes": list(source_prepared.notes),
            "comparison_canonicalization_notes": list(comparison_prepared.notes),
            "schema_canonicalization_notes": list(schema_prepared.notes),
            "result_checker_exactness_used": False,
            "local_only": True,
            "official_metric_input": False,
        },
    )


def _support_scope_guarded_pair(
    *,
    pair: dict[str, str],
    tool_dir: Path,
    stdout_path: Path,
    stderr_path: Path,
    raw_output_path: Path,
    timeout_seconds: float,
    availability: SQLSolverAvailability,
    support_decision: SQLSolverSupportScopeDecision,
    source_prepared: SQLSolverCanonicalizationResult,
    comparison_prepared: SQLSolverCanonicalizationResult,
    schema_prepared: SQLSolverCanonicalizationResult,
) -> dict[str, Any]:
    reason = support_decision.reason or "outside_current_sqlsolver_support_scope"
    stdout_path.write_text("", encoding="utf-8")
    stderr_path.write_text(f"SQLSolver support-scope guard blocked invocation: {reason}\n", encoding="utf-8")
    raw_output_path.write_text("", encoding="utf-8")
    return build_verdict_record(
        pair_id=pair["pair_id"],
        tool=SQLSOLVER_TOOL,
        raw_verdict=support_decision.normalized_verdict or "unsupported",
        invocation_status=support_decision.normalized_verdict or "unsupported",
        tool_version=availability.tool_version or "unknown",
        raw_stdout_path=stdout_path.as_posix(),
        raw_stderr_path=stderr_path.as_posix(),
        runtime_ms=None,
        timeout_seconds=timeout_seconds,
        artifact_paths={
            "tool_dir": tool_dir.as_posix(),
            "raw_output_path": raw_output_path.as_posix(),
            "detection_reason": reason,
            "command_shape": availability.command_shape,
            "verifier_mode": availability.invocation_mode,
            "tool_available": availability.tool_available,
            "canonicalization_applied": True,
            "canonicalization_mode": "temp_verifier_input_only",
            "support_scope_guarded": True,
            "support_scope_family": support_decision.family,
            "support_scope_guard_category": support_decision.normalized_guard_category,
            "support_scope_verdict": support_decision.support_scope_verdict,
            "sqlsolver_invocation_allowed": False,
            "source_guard_categories": list(source_prepared.guard_categories),
            "comparison_guard_categories": list(comparison_prepared.guard_categories),
            "schema_guard_categories": list(schema_prepared.guard_categories),
            "source_canonicalization_notes": list(source_prepared.notes),
            "comparison_canonicalization_notes": list(comparison_prepared.notes),
            "schema_canonicalization_notes": list(schema_prepared.notes),
            "support_scope_notes": list(support_decision.notes),
            "result_checker_exactness_used": False,
            "local_only": True,
            "official_metric_input": False,
        },
    )


def _not_attempted_pair(
    *,
    pair: dict[str, str],
    verifier_dir: Path,
    timeout_seconds: float,
    reason: str,
) -> dict[str, Any]:
    pair_id = pair["pair_id"]
    tool_dir = verifier_dir / "tools" / SQLSOLVER_TOOL / pair_id
    tool_dir.mkdir(parents=True, exist_ok=True)
    stdout_path = tool_dir / "raw_stdout.txt"
    stderr_path = tool_dir / "raw_stderr.txt"
    stdout_path.write_text("", encoding="utf-8")
    stderr_path.write_text(f"SQLSolver not attempted: {reason}\n", encoding="utf-8")
    return build_verdict_record(
        pair_id=pair_id,
        tool=SQLSOLVER_TOOL,
        raw_verdict="not_attempted",
        invocation_status="not_attempted",
        tool_version="unavailable",
        raw_stdout_path=stdout_path.as_posix(),
        raw_stderr_path=stderr_path.as_posix(),
        runtime_ms=None,
        timeout_seconds=timeout_seconds,
        artifact_paths={
            "tool_dir": tool_dir.as_posix(),
            "detection_reason": reason,
            "command_shape": SQLSOLVER_COMMAND_SHAPE,
            "verifier_mode": SQLSOLVER_JAR_MODE,
            "tool_available": False,
            "result_checker_exactness_used": False,
            "local_only": True,
            "official_metric_input": False,
        },
    )


def _validate_sqlsolver_pair(record: Mapping[str, Any]) -> dict[str, str]:
    pair = validate_pair_record(record)
    if pair["tool"] != SQLSOLVER_TOOL:
        raise ValueError("SQLSolver smoke accepts only sqlsolver pair records")
    return pair


def _comparison_sql_path(pair: Mapping[str, str]) -> str:
    pair_type = pair["pair_type"]
    if pair_type in {"source_vs_candidate", "source_vs_candidate_port_target", "support_pair_smoke"}:
        return pair["candidate_sql_path"]
    if pair_type == "source_vs_positive":
        return pair["positive_sql_path"]
    if pair_type == "source_vs_hard_negative":
        return pair["negative_sql_path"]
    raise ValueError(f"unsupported SQLSolver smoke pair type: {pair_type}")


def _detect_env_jar(
    env: Mapping[str, str],
    *,
    search_path: str | None,
    version_timeout_seconds: float,
) -> SQLSolverAvailability | None:
    jar_value = env.get(SQLSOLVER_JAR_ENV_VAR)
    root_value = env.get(SQLSOLVER_ROOT_ENV_VAR)
    if not jar_value and not root_value:
        return None
    root = Path(root_value).expanduser() if root_value else None
    jar_path = Path(jar_value).expanduser() if jar_value else _find_sqlsolver_jar(root)
    return _detect_jar(
        jar_path=jar_path,
        root=root,
        java_value=env.get(SQLSOLVER_JAVA_ENV_VAR),
        ld_library_path_value=env.get(SQLSOLVER_LD_LIBRARY_PATH_ENV_VAR),
        search_path=search_path,
        version_timeout_seconds=version_timeout_seconds,
    )


def _detect_explicit_jar_command(
    command: tuple[str, ...],
    env: Mapping[str, str],
    *,
    search_path: str | None,
    version_timeout_seconds: float,
) -> SQLSolverAvailability | None:
    if len(command) == 1 and command[0].endswith(".jar"):
        jar_path = Path(command[0]).expanduser()
        root = _infer_sqlsolver_root_from_jar(jar_path)
        return _detect_jar(
            jar_path=jar_path,
            root=root,
            java_value=env.get(SQLSOLVER_JAVA_ENV_VAR),
            ld_library_path_value=env.get(SQLSOLVER_LD_LIBRARY_PATH_ENV_VAR),
            search_path=search_path,
            version_timeout_seconds=version_timeout_seconds,
        )
    if "-jar" in command:
        jar_index = command.index("-jar") + 1
        if jar_index >= len(command):
            return SQLSolverAvailability(
                tool_available=False,
                command=None,
                command_path=None,
                tool_version=None,
                detection_reason="sqlsolver_jar_not_found",
                invocation_mode=SQLSOLVER_JAR_MODE,
                command_shape=SQLSOLVER_COMMAND_SHAPE,
            )
        java_command = command[: jar_index - 1]
        jar_path = Path(command[jar_index]).expanduser()
        root = _infer_sqlsolver_root_from_jar(jar_path)
        return _detect_jar(
            jar_path=jar_path,
            root=root,
            java_value=" ".join(java_command),
            ld_library_path_value=env.get(SQLSOLVER_LD_LIBRARY_PATH_ENV_VAR),
            search_path=search_path,
            version_timeout_seconds=version_timeout_seconds,
        )
    return None


def _detect_jar(
    *,
    jar_path: Path | None,
    root: Path | None,
    java_value: str | None,
    ld_library_path_value: str | None,
    search_path: str | None,
    version_timeout_seconds: float,
) -> SQLSolverAvailability:
    if jar_path is None or not jar_path.exists():
        return SQLSolverAvailability(
            tool_available=False,
            command=None,
            command_path=None,
            tool_version=None,
            detection_reason="sqlsolver_jar_not_found",
            invocation_mode=SQLSOLVER_JAR_MODE,
            jar_path=jar_path.as_posix() if jar_path else None,
            sqlsolver_root=root.as_posix() if root else None,
            command_shape=SQLSOLVER_COMMAND_SHAPE,
        )
    java_command = _split_command(java_value or "java")
    java_path = _resolve_executable(java_command[0], search_path=search_path)
    if java_path is None:
        return SQLSolverAvailability(
            tool_available=False,
            command=None,
            command_path=None,
            tool_version=None,
            detection_reason="java_not_found",
            invocation_mode=SQLSOLVER_JAR_MODE,
            jar_path=jar_path.as_posix(),
            sqlsolver_root=root.as_posix() if root else None,
            command_shape=SQLSOLVER_COMMAND_SHAPE,
        )
    resolved_java_command = (java_path, *java_command[1:])
    ld_library_path = _resolve_ld_library_path(ld_library_path_value, root, jar_path)
    if not ld_library_path:
        return SQLSolverAvailability(
            tool_available=False,
            command=None,
            command_path=None,
            tool_version=None,
            detection_reason="sqlsolver_ld_library_path_not_found",
            invocation_mode=SQLSOLVER_JAR_MODE,
            jar_path=jar_path.as_posix(),
            sqlsolver_root=root.as_posix() if root else None,
            java_command=resolved_java_command,
            command_shape=SQLSOLVER_COMMAND_SHAPE,
        )
    version = _probe_jar_version(
        java_command=resolved_java_command,
        jar_path=jar_path,
        ld_library_path=ld_library_path,
        root=root,
        timeout_seconds=version_timeout_seconds,
    )
    return SQLSolverAvailability(
        tool_available=True,
        command=(*resolved_java_command, "-jar", jar_path.as_posix()),
        command_path=resolved_java_command[0],
        tool_version=version,
        detection_reason="sqlsolver_jar_available",
        invocation_mode=SQLSOLVER_JAR_MODE,
        jar_path=jar_path.as_posix(),
        sqlsolver_root=root.as_posix() if root else None,
        ld_library_path=ld_library_path,
        java_command=resolved_java_command,
        command_shape=SQLSOLVER_COMMAND_SHAPE,
    )


def _detect_legacy_command(
    command: tuple[str, ...],
    *,
    search_path: str | None,
    version_timeout_seconds: float,
) -> SQLSolverAvailability:
    executable = _resolve_executable(command[0], search_path=search_path)
    if executable is None:
        return SQLSolverAvailability(
            tool_available=False,
            command=None,
            command_path=None,
            tool_version=None,
            detection_reason="sqlsolver_command_not_found",
        )
    version = _probe_version((executable, *command[1:]), timeout_seconds=version_timeout_seconds)
    return SQLSolverAvailability(
        tool_available=True,
        command=(executable, *command[1:]),
        command_path=executable,
        tool_version=version,
        detection_reason="command_available",
    )


def _candidate_commands(
    command: str | Sequence[str] | None,
    env: Mapping[str, str],
    *,
    search_path: str | None,
) -> list[tuple[str, ...]]:
    if command:
        return [_split_command(command)]
    candidates: list[tuple[str, ...]] = []
    for name in SQLSOLVER_ENV_VARS:
        value = env.get(name)
        if value:
            candidates.append(_split_command(value))
    for name in DEFAULT_SQLSOLVER_COMMANDS:
        if shutil.which(name, path=search_path):
            candidates.append((name,))
    return candidates


def _split_command(command: str | Sequence[str]) -> tuple[str, ...]:
    if isinstance(command, str):
        parts = tuple(shlex.split(command))
    else:
        parts = tuple(str(part) for part in command)
    if not parts:
        raise ValueError("SQLSolver command cannot be empty")
    return parts


def _resolve_executable(executable: str, *, search_path: str | None) -> str | None:
    resolved = shutil.which(executable, path=search_path)
    if resolved:
        return resolved
    path = Path(executable)
    if path.exists() and os.access(path, os.X_OK):
        return path.as_posix()
    return None


def _find_sqlsolver_jar(root: Path | None) -> Path | None:
    if root is None or not root.exists():
        return None
    candidates = sorted((root / "build" / "libs").glob("*.jar"))
    if not candidates:
        candidates = sorted(root.glob("*.jar"))
    if not candidates:
        return None
    preferred = [path for path in candidates if "sqlsolver" in path.name.lower()]
    return preferred[0] if preferred else candidates[0]


def _infer_sqlsolver_root_from_jar(jar_path: Path) -> Path | None:
    parts = jar_path.parts
    if len(parts) >= 3 and parts[-3:] and parts[-3] == "build" and parts[-2] == "libs":
        return Path(*parts[:-3])
    for parent in jar_path.parents:
        if (parent / "lib").is_dir() and (parent / "README.md").exists():
            return parent
    return None


def _resolve_ld_library_path(value: str | None, root: Path | None, jar_path: Path) -> str | None:
    candidates: list[Path] = []
    if value:
        for item in value.split(os.pathsep):
            if item:
                candidates.append(Path(item).expanduser())
    if root is not None:
        candidates.append(root / "lib")
    inferred_root = _infer_sqlsolver_root_from_jar(jar_path)
    if inferred_root is not None:
        candidates.append(inferred_root / "lib")
    valid = [path.as_posix() for path in candidates if path.exists()]
    return os.pathsep.join(dict.fromkeys(valid)) if valid else None


def _probe_jar_version(
    *,
    java_command: tuple[str, ...],
    jar_path: Path,
    ld_library_path: str,
    root: Path | None,
    timeout_seconds: float,
) -> str | None:
    env = _sqlsolver_process_env({}, SQLSolverAvailability(
        tool_available=True,
        command=(*java_command, "-jar", jar_path.as_posix()),
        command_path=java_command[0],
        tool_version=None,
        detection_reason="sqlsolver_jar_available",
        invocation_mode=SQLSOLVER_JAR_MODE,
        jar_path=jar_path.as_posix(),
        sqlsolver_root=root.as_posix() if root else None,
        ld_library_path=ld_library_path,
        java_command=java_command,
        command_shape=SQLSOLVER_COMMAND_SHAPE,
    ))
    try:
        completed = subprocess.run(
            [*java_command, "-jar", jar_path.as_posix(), "-help"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout_seconds,
            env=env,
        )
    except Exception:
        return None
    version_text = None
    if root is not None and (root / "version").exists():
        version_text = (root / "version").read_text(encoding="utf-8", errors="replace").strip()
    help_line = (completed.stdout or completed.stderr).strip().splitlines()
    if version_text:
        return f"SQLSolver {version_text}"
    if help_line:
        return help_line[0][:200]
    return None


def _probe_version(command: tuple[str, ...], *, timeout_seconds: float) -> str | None:
    for flag in ("--version", "-version", "-h", "--help"):
        try:
            completed = subprocess.run(
                [*command, flag],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout_seconds,
            )
        except Exception:
            continue
        text = (completed.stdout or completed.stderr).strip()
        if text:
            return text.splitlines()[0][:200]
    return None


def _sqlsolver_process_env(env: Mapping[str, str] | None, availability: SQLSolverAvailability) -> dict[str, str]:
    process_env = dict(os.environ if env is None else env)
    if availability.ld_library_path:
        existing = process_env.get("LD_LIBRARY_PATH")
        process_env["LD_LIBRARY_PATH"] = (
            availability.ld_library_path
            if not existing
            else availability.ld_library_path + os.pathsep + existing
        )
    return process_env


def _strip_sql_comments(sql_text: str) -> SQLSolverCanonicalizationResult:
    output: list[str] = []
    notes: list[str] = []
    categories: list[str] = []
    i = 0
    in_single = False
    in_double = False
    while i < len(sql_text):
        ch = sql_text[i]
        nxt = sql_text[i + 1] if i + 1 < len(sql_text) else ""
        if in_single:
            output.append(ch)
            if ch == "'" and nxt == "'":
                output.append(nxt)
                i += 2
                continue
            if ch == "'":
                in_single = False
            i += 1
            continue
        if in_double:
            output.append(ch)
            if ch == '"' and nxt == '"':
                output.append(nxt)
                i += 2
                continue
            if ch == '"':
                in_double = False
            i += 1
            continue
        if ch == "'":
            in_single = True
            output.append(ch)
            i += 1
            continue
        if ch == '"':
            in_double = True
            output.append(ch)
            i += 1
            continue
        if ch == "-" and nxt == "-":
            categories.append("wrapper_input_format_gap")
            notes.append("line_comment_stripped")
            i += 2
            while i < len(sql_text) and sql_text[i] not in "\r\n":
                i += 1
            output.append("\n")
            continue
        if ch == "/" and nxt == "*":
            categories.append("wrapper_input_format_gap")
            notes.append("block_comment_stripped")
            i += 2
            closed = False
            while i < len(sql_text):
                if sql_text[i] == "*" and i + 1 < len(sql_text) and sql_text[i + 1] == "/":
                    i += 2
                    closed = True
                    break
                i += 1
            if not closed:
                return SQLSolverCanonicalizationResult(
                    canonical_text="",
                    safe_for_sqlsolver=False,
                    guard_categories=("wrapper_input_format_gap",),
                    fail_closed_reason="unterminated_block_comment",
                    notes=("block_comment_unterminated",),
                )
            output.append(" ")
            continue
        output.append(ch)
        i += 1
    if in_single or in_double:
        return SQLSolverCanonicalizationResult(
            canonical_text="",
            safe_for_sqlsolver=False,
            guard_categories=("wrapper_input_format_gap",),
            fail_closed_reason="unterminated_quoted_literal_or_identifier",
            notes=("quote_unterminated",),
        )
    return SQLSolverCanonicalizationResult(
        canonical_text="".join(output),
        safe_for_sqlsolver=True,
        guard_categories=tuple(dict.fromkeys(categories)),
        notes=tuple(dict.fromkeys(notes)),
    )


def _single_statement_without_terminal_semicolon(sql_text: str) -> SQLSolverCanonicalizationResult:
    parts = _split_semicolon_outside_literals(sql_text)
    if parts is None:
        return SQLSolverCanonicalizationResult(
            canonical_text="",
            safe_for_sqlsolver=False,
            guard_categories=("wrapper_input_format_gap",),
            fail_closed_reason="statement_boundary_ambiguous",
            notes=("statement_boundary_ambiguous",),
        )
    nonempty = [part.strip() for part in parts if part.strip()]
    if len(nonempty) != 1:
        return SQLSolverCanonicalizationResult(
            canonical_text="",
            safe_for_sqlsolver=False,
            guard_categories=("wrapper_input_format_gap",),
            fail_closed_reason="expected_exactly_one_sql_statement",
            notes=(f"statement_count:{len(nonempty)}",),
        )
    return SQLSolverCanonicalizationResult(
        canonical_text=nonempty[0],
        safe_for_sqlsolver=True,
        guard_categories=(),
        notes=("terminal_semicolon_normalized",) if sql_text.strip().endswith(";") else (),
    )


def _schema_statements(schema_text: str) -> list[str] | None:
    parts = _split_semicolon_outside_literals(schema_text)
    if parts is None:
        return None
    return [part.strip() for part in parts if part.strip()]


def _split_semicolon_outside_literals(sql_text: str) -> list[str] | None:
    parts: list[str] = []
    current: list[str] = []
    in_single = False
    in_double = False
    i = 0
    while i < len(sql_text):
        ch = sql_text[i]
        nxt = sql_text[i + 1] if i + 1 < len(sql_text) else ""
        if in_single:
            current.append(ch)
            if ch == "'" and nxt == "'":
                current.append(nxt)
                i += 2
                continue
            if ch == "'":
                in_single = False
            i += 1
            continue
        if in_double:
            current.append(ch)
            if ch == '"' and nxt == '"':
                current.append(nxt)
                i += 2
                continue
            if ch == '"':
                in_double = False
            i += 1
            continue
        if ch == "'":
            in_single = True
            current.append(ch)
            i += 1
            continue
        if ch == '"':
            in_double = True
            current.append(ch)
            i += 1
            continue
        if ch == ";":
            parts.append("".join(current))
            current = []
            i += 1
            continue
        current.append(ch)
        i += 1
    if in_single or in_double:
        return None
    parts.append("".join(current))
    return parts


def _collapse_sql_whitespace(sql_text: str) -> str:
    output: list[str] = []
    in_single = False
    in_double = False
    pending_space = False
    i = 0
    while i < len(sql_text):
        ch = sql_text[i]
        nxt = sql_text[i + 1] if i + 1 < len(sql_text) else ""
        if in_single:
            if pending_space and output:
                output.append(" ")
                pending_space = False
            output.append(ch)
            if ch == "'" and nxt == "'":
                output.append(nxt)
                i += 2
                continue
            if ch == "'":
                in_single = False
            i += 1
            continue
        if in_double:
            if pending_space and output:
                output.append(" ")
                pending_space = False
            output.append(ch)
            if ch == '"' and nxt == '"':
                output.append(nxt)
                i += 2
                continue
            if ch == '"':
                in_double = False
            i += 1
            continue
        if ch.isspace():
            pending_space = True
            i += 1
            continue
        if pending_space and output:
            output.append(" ")
        pending_space = False
        if ch == "'":
            in_single = True
        elif ch == '"':
            in_double = True
        output.append(ch)
        i += 1
    return "".join(output).strip()


def _normalize_schema_types(statement: str) -> str:
    import re

    normalized = re.sub(r"\bDOUBLE\s+PRECISION\b", "DOUBLE", statement, flags=re.IGNORECASE)
    normalized = re.sub(r"\bTEXT\b", "VARCHAR", normalized, flags=re.IGNORECASE)
    normalized = re.sub(r"\bTIMESTAMP\s+WITHOUT\s+TIME\s+ZONE\b", "TIMESTAMP", normalized, flags=re.IGNORECASE)
    normalized = re.sub(r"\bNUMERIC\s*\(", "DECIMAL(", normalized, flags=re.IGNORECASE)
    normalized = re.sub(r"\bNUMERIC\b", "DECIMAL", normalized, flags=re.IGNORECASE)
    return normalized


def _classify_query_guards(sql_text: str) -> tuple[str, ...]:
    import re

    categories: list[str] = []
    if re.search(r"\bDENSE_RANK\s*\(", sql_text, flags=re.IGNORECASE):
        categories.append("unsupported_sql_feature")
    if re.search(r"\bINTERVAL\s*'", sql_text, flags=re.IGNORECASE):
        categories.append("unsupported_postgres_dialect")
    if re.search(r"\bNULLS\s+(FIRST|LAST)\b", sql_text, flags=re.IGNORECASE):
        categories.append("unsupported_postgres_dialect")
    if re.search(r"\bDATE\s*'", sql_text, flags=re.IGNORECASE):
        categories.append("query_normalization_gap")
    if re.search(r"\b(EXTRACT|DATE_TRUNC|AGE)\s*\(", sql_text, flags=re.IGNORECASE):
        categories.append("type_or_function_modeling_gap")
    if '"' in sql_text:
        categories.append("unsupported_postgres_dialect")
    if re.search(r"\bWITH\b", sql_text, flags=re.IGNORECASE) and re.search(r"\bOVER\s*\(", sql_text, flags=re.IGNORECASE):
        categories.append("unsupported_sql_feature")
    return tuple(dict.fromkeys(categories))


def _pair_support_scope_decision(
    source_prepared: SQLSolverCanonicalizationResult,
    comparison_prepared: SQLSolverCanonicalizationResult,
) -> SQLSolverSupportScopeDecision:
    for prepared in (source_prepared, comparison_prepared):
        decision = sqlsolver_support_scope_decision(prepared.canonical_text)
        if not decision.sqlsolver_invocation_allowed:
            return decision
    return SQLSolverSupportScopeDecision(
        sqlsolver_invocation_allowed=True,
        family=None,
        normalized_guard_category=None,
        normalized_verdict=None,
        support_scope_verdict=None,
        reason=None,
        notes=(),
    )


def _known_no_support_family(sql_text: str) -> str | None:
    import re

    if '"' in sql_text and re.search(r"\bNULLS\s+(FIRST|LAST)\b", sql_text, flags=re.IGNORECASE):
        return "quoted_identifier_null_ordering"
    dense_rank = re.search(r"\bDENSE_RANK\s*\(", sql_text, flags=re.IGNORECASE)
    window_over = re.search(r"\bOVER\s*\(", sql_text, flags=re.IGNORECASE)
    cte = re.search(r"\bWITH\b", sql_text, flags=re.IGNORECASE)
    if dense_rank or (cte and window_over):
        return "dense_rank_cte_ranking"
    return None


def _read_sql_line(path: Path) -> str:
    text = path.read_text(encoding="utf-8").strip()
    if text.endswith(";"):
        text = text[:-1].strip()
    return " ".join(text.split())


def _normalize_official_result_lines(text: str) -> str | None:
    lines = [line.strip().upper() for line in text.splitlines() if line.strip()]
    if not lines:
        return None
    official = [line for line in lines if line in {"EQ", "NEQ", "UNKNOWN", "TIMEOUT"}]
    if not official:
        return None
    if any(line == "TIMEOUT" for line in official):
        return "timeout"
    if any(line == "NEQ" for line in official):
        return "non_equivalent"
    if any(line == "UNKNOWN" for line in official):
        return "unknown"
    if official and all(line == "EQ" for line in official):
        return "equivalent"
    return None


def _safe_name(value: str) -> str:
    return "".join(ch if ch.isalnum() or ch in {"-", "_"} else "_" for ch in value)[:80] or "pair"


def _log_text(availability: SQLSolverAvailability, pair_count: int) -> str:
    return "\n".join(
        [
            "SQLSolver bounded smoke local diagnostic.",
            f"tool_available={str(availability.tool_available).lower()}",
            f"tool_version={availability.tool_version or 'unknown'}",
            f"detection_reason={availability.detection_reason}",
            f"verifier_mode={availability.invocation_mode}",
            f"command_shape={availability.command_shape}",
            f"jar_path={availability.jar_path or 'none'}",
            f"ld_library_path={availability.ld_library_path or 'none'}",
            f"pairs_planned={pair_count}",
            "official_metric_input=false",
            "leaderboard_input=false",
            "",
        ]
    )


def _report_text(summary: Mapping[str, Any], availability: SQLSolverAvailability) -> str:
    rate = summary.get("semantic_equivalence_rate")
    rate_text = "N.A." if rate is None else str(rate)
    return "\n".join(
        [
            "# SQLSolver Smoke Summary",
            "",
            "This is a bounded local diagnostic smoke only.",
            "",
            f"- Tool available: `{str(availability.tool_available).lower()}`",
            f"- Tool version: `{availability.tool_version or 'unknown'}`",
            f"- Verifier mode: `{availability.invocation_mode}`",
            f"- Command shape: `{availability.command_shape}`",
            f"- Semantic Equivalence Rate: `{rate_text}`",
            f"- N.A. reason: `{summary.get('na_reason') or 'none'}`",
            f"- Decidable pairs: `{summary.get('decidable_count', 0)}`",
            f"- Unknown pairs: `{summary.get('unknown_count', 0)}`",
            f"- Timeout pairs: `{summary.get('timeout_count', 0)}`",
            f"- Unsupported pairs: `{summary.get('unsupported_count', 0)}`",
            f"- Tool-error pairs: `{summary.get('tool_error_count', 0)}`",
            f"- Not-attempted pairs: `{summary.get('not_attempted_count', 0)}`",
            "",
            "Local diagnostic output only; not official metrics, not paper results, not retained evidence, and not leaderboard input.",
            "",
        ]
    )


def _redacted_command(command: Sequence[str]) -> list[str]:
    return [Path(command[0]).name, *command[1:]]
