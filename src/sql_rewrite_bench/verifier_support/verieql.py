"""Bounded VeriEQL canary support for local diagnostic verifier outputs.

The wrapper is intentionally narrow. It detects either a direct VeriEQL-like
command or a staged VeriEQL source root, can emit VeriEQL JSONL batch input for
bounded pairs, and writes D035-shaped local verifier artifacts. It does not
install dependencies, vendor VeriEQL, compute official metrics, promote
retained evidence, or create leaderboard output.
"""

from __future__ import annotations

import csv
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .pairs import PAIR_FIELDS, validate_pair_record
from .summary import generate_semantic_equivalence_summary
from .verdicts import build_verdict_record

VERIEQL_TOOL = "verieql"
DEFAULT_VERIEQL_COMMANDS = ("verieql", "VeriEQL", "verieql-cli", "veri-eql")
VERIEQL_ENV_VARS = ("SQLRB_VERIEQL_CMD", "SQLRB_VERIEQL_COMMAND", "VERIEQL_COMMAND", "VERIEQL_BIN")
VERIEQL_ROOT_ENV_VARS = ("SQLRB_VERIEQL_ROOT", "VERIEQL_ROOT")
VERIEQL_BATCH_MODULE = "parallel.cli_within_timeout"
VERIEQL_JSONL_INPUT_NAME = "verieql_pairs.jsonl"
VERIEQL_JSONL_OUTPUT_NAME = "verieql_output.jsonl"


@dataclass(frozen=True)
class VeriEQLAvailability:
    tool_available: bool
    command: tuple[str, ...] | None
    command_path: str | None
    tool_version: str | None
    detection_reason: str
    invocation_mode: str = "direct_command"
    verieql_root: str | None = None


@dataclass(frozen=True)
class VeriEQLCanaryOutput:
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
    jsonl_input_path: Path | None = None
    jsonl_output_path: Path | None = None


def detect_verieql(
    command: str | Sequence[str] | None = None,
    *,
    env: Mapping[str, str] | None = None,
    search_path: str | None = None,
    version_timeout_seconds: float = 5.0,
) -> VeriEQLAvailability:
    """Detect a local VeriEQL command or staged VeriEQL root.

    ``SQLRB_VERIEQL_ROOT`` enables the staged-source JSONL batch mode. The root
    check validates source-tree shape only; it does not install or import
    dependencies. Missing dependencies are handled fail-closed at invocation
    time.
    """

    effective_env = dict(os.environ if env is None else env)
    root_value = _first_env_value(effective_env, VERIEQL_ROOT_ENV_VARS)
    if root_value:
        root = Path(root_value)
        if not _is_valid_verieql_root(root):
            return VeriEQLAvailability(
                tool_available=False,
                command=None,
                command_path=None,
                tool_version=None,
                detection_reason="verieql_root_not_found",
                invocation_mode="jsonl_batch",
                verieql_root=root.as_posix(),
            )
        base_command = _batch_base_command(command, effective_env)
        if not _command_executable_available(base_command, search_path=search_path):
            return VeriEQLAvailability(
                tool_available=False,
                command=None,
                command_path=None,
                tool_version=None,
                detection_reason="verieql_batch_command_not_found",
                invocation_mode="jsonl_batch",
                verieql_root=root.as_posix(),
            )
        version = _probe_version(base_command, timeout_seconds=version_timeout_seconds, cwd=root)
        return VeriEQLAvailability(
            tool_available=True,
            command=base_command,
            command_path=base_command[0],
            tool_version=version,
            detection_reason="verieql_root_available",
            invocation_mode="jsonl_batch",
            verieql_root=root.as_posix(),
        )

    for candidate in _candidate_commands(command, effective_env, search_path=search_path):
        executable = shutil.which(candidate[0], path=search_path)
        command_path = executable or candidate[0]
        if not executable and not Path(candidate[0]).exists():
            continue
        version = _probe_version((command_path, *candidate[1:]), timeout_seconds=version_timeout_seconds)
        return VeriEQLAvailability(
            tool_available=True,
            command=(command_path, *candidate[1:]),
            command_path=command_path,
            tool_version=version,
            detection_reason="command_available",
            invocation_mode="direct_command",
        )
    return VeriEQLAvailability(
        tool_available=False,
        command=None,
        command_path=None,
        tool_version=None,
        detection_reason="verieql_command_not_found",
    )


def normalize_verieql_output(
    *,
    stdout: str,
    stderr: str = "",
    returncode: int = 0,
    timed_out: bool = False,
) -> str:
    """Map bounded VeriEQL-like process output to the shared verdict vocabulary."""

    if timed_out:
        return "timeout"
    text = f"{stdout}\n{stderr}".strip().lower()
    compact = text.replace("-", "_").replace(" ", "_")
    if any(token in compact for token in ["timeout", "timed_out", "time_limit_exceeded"]):
        return "timeout"
    if any(token in compact for token in ["unsupported", "not_supported", "unsupported_sql", "unsupported_syntax", "nse"]):
        return "unsupported"
    if any(
        token in compact
        for token in [
            "non_equivalent",
            "not_equivalent",
            "counterexample",
            "counter_example",
            "refute",
            "refuted",
            "refutation",
            "not_valid",
            "invalid",
        ]
    ):
        return "non_equivalent"
    if any(token in compact for token in ["equivalent", "semantically_equivalent", "verified", "proved", "valid"]):
        return "equivalent"
    if any(token in compact for token in ["unknown", "inconclusive", "undecidable"]):
        return "unknown"
    if returncode != 0:
        return "tool_error"
    if text:
        return "tool_error"
    return "unknown"


def normalize_verieql_jsonl_record(record: Mapping[str, Any] | None) -> str:
    """Normalize one VeriEQL JSONL output record to the shared vocabulary."""

    if record is None:
        return "tool_error"
    states = [str(state).strip().upper() for state in _as_list(record.get("states")) if str(state).strip()]
    err = str(record.get("err") or "")
    counterexample = str(record.get("counterexample") or "")
    text = " ".join([err, counterexample, " ".join(states)]).lower()
    if any(state in {"TMO", "TIMEOUT", "TIMED_OUT"} for state in states) or "timeout" in text:
        return "timeout"
    if any(state in {"NSE", "UNSUPPORTED"} for state in states) or any(
        token in text for token in ["not supported", "unsupported", "unsupported feature"]
    ):
        return "unsupported"
    if any(state in {"NEQ", "NON_EQUIVALENT"} for state in states) or any(
        token in text for token in ["not equivalent", "non_equivalent", "counterexample"]
    ):
        return "non_equivalent"
    if states and states[-1] in {"EQU", "EQ", "EQUIVALENT"} and not err:
        return "equivalent"
    if "unknown" in text or "undecidable" in text:
        return "unknown"
    if err:
        return "tool_error"
    return "unknown"


def write_verieql_canary(
    *,
    output_root: str | Path,
    run_id: str,
    pair_records: list[Mapping[str, Any]],
    command: str | Sequence[str] | None = None,
    timeout_seconds: float = 30.0,
    env: Mapping[str, str] | None = None,
    search_path: str | None = None,
    result_consistent_pairs: int | None = None,
    dry_run: bool = False,
) -> VeriEQLCanaryOutput:
    """Run a bounded VeriEQL canary or write fail-closed unavailable outputs."""

    availability = detect_verieql(command=command, env=env, search_path=search_path)
    root = Path(output_root)
    verifier_dir = root / "results" / run_id / "verifier"
    log_dir = root / "logs" / run_id
    report_dir = root / "reports" / run_id
    verifier_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)

    pairs = [_validate_verieql_pair(record) for record in pair_records]
    pairs_path = verifier_dir / "verifier_pairs.csv"
    with pairs_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=PAIR_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(pairs)

    jsonl_input_path: Path | None = None
    jsonl_output_path: Path | None = None
    if availability.tool_available and availability.command:
        if availability.invocation_mode == "jsonl_batch":
            verdict_records, jsonl_input_path, jsonl_output_path = _run_jsonl_batch_pairs(
                pairs=pairs,
                availability=availability,
                verifier_dir=verifier_dir,
                timeout_seconds=timeout_seconds,
                env=env,
                dry_run=dry_run,
            )
        else:
            verdict_records = [
                _run_direct_pair(
                    pair=pair,
                    availability=availability,
                    verifier_dir=verifier_dir,
                    timeout_seconds=timeout_seconds,
                    env=env,
                )
                for pair in pairs
            ]
    else:
        verdict_records = [
            _not_attempted_pair(
                pair=pair,
                verifier_dir=verifier_dir,
                timeout_seconds=timeout_seconds,
                reason=availability.detection_reason,
            )
            for pair in pairs
        ]

    verdicts_path = verifier_dir / "verifier_verdicts.jsonl"
    with verdicts_path.open("w", encoding="utf-8") as handle:
        for record in verdict_records:
            handle.write(json.dumps(record, sort_keys=True) + "\n")

    summary = generate_semantic_equivalence_summary(
        run_id=run_id,
        verdict_rows=verdict_records,
        verifier_tools_requested=[VERIEQL_TOOL],
        pairs_planned=len(pairs),
        result_consistent_pairs=result_consistent_pairs,
    )
    summary["tool_available"] = availability.tool_available
    summary["tool_version"] = availability.tool_version
    summary["detection_reason"] = availability.detection_reason
    summary["invocation_mode"] = availability.invocation_mode
    summary["verieql_root"] = availability.verieql_root
    if jsonl_input_path is not None:
        summary["verieql_jsonl_input_path"] = jsonl_input_path.as_posix()
    if jsonl_output_path is not None:
        summary["verieql_jsonl_output_path"] = jsonl_output_path.as_posix()
    _apply_verieql_na_reason(summary, availability=availability, verdict_records=verdict_records, dry_run=dry_run)

    summary_path = verifier_dir / "semantic_equivalence_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    log_path = log_dir / "verifier.log"
    log_path.write_text(_log_text(availability, len(pairs), dry_run=dry_run), encoding="utf-8")
    report_path = report_dir / "verifier_summary.md"
    report_path.write_text(_report_text(summary, availability), encoding="utf-8")

    return VeriEQLCanaryOutput(
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
        jsonl_input_path=jsonl_input_path,
        jsonl_output_path=jsonl_output_path,
    )


def write_verieql_pair_jsonl(pairs: Sequence[Mapping[str, str]], output_path: Path) -> list[dict[str, Any]]:
    """Write VeriEQL batch JSONL records for already-validated pair rows."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    records = [build_verieql_jsonl_record(pair, index=index) for index, pair in enumerate(pairs, start=1)]
    with output_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=True) + "\n")
    return records


def build_verieql_jsonl_record(pair: Mapping[str, str], *, index: int) -> dict[str, Any]:
    """Build one VeriEQL batch input record from a verifier pair row."""

    source_sql = _read_sql(pair["source_sql_path"])
    comparison_sql = _read_sql(_comparison_sql_path(pair))
    pair_role = _verieql_pair_role(pair["pair_type"])
    case_id = pair["case_id"]
    pair_id = pair["pair_id"]
    return {
        "index": index,
        "file": f"{case_id}:{pair_role}:{pair_id}",
        "name": f"{case_id}:{pair_role}:{pair_id}",
        "benchmark": f"{case_id}:{pair_role}",
        "case_id": case_id,
        "pair_id": pair_id,
        "pair_type": pair["pair_type"],
        "pair_role": pair_role,
        "schema": _schema_from_context(pair.get("schema_context_path", "")),
        "constraint": [],
        "pair": [source_sql, comparison_sql],
    }


def build_verieql_batch_command(
    base_command: Sequence[str],
    *,
    input_jsonl: Path,
    output_jsonl: Path,
    timeout_seconds: float,
) -> list[str]:
    """Build the staged VeriEQL batch CLI command line."""

    return [
        *[str(part) for part in base_command],
        "-f",
        input_jsonl.as_posix(),
        "-t",
        str(int(timeout_seconds) if float(timeout_seconds).is_integer() else timeout_seconds),
        "-o",
        output_jsonl.as_posix(),
    ]


def parse_verieql_output_file(path: Path) -> dict[int, dict[str, Any]]:
    """Parse VeriEQL JSONL output by integer index."""

    parsed: dict[int, dict[str, Any]] = {}
    if not path.exists():
        return parsed
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        try:
            parsed[int(record["index"])] = record
        except (KeyError, TypeError, ValueError):
            continue
    return parsed


def _run_jsonl_batch_pairs(
    *,
    pairs: list[dict[str, str]],
    availability: VeriEQLAvailability,
    verifier_dir: Path,
    timeout_seconds: float,
    env: Mapping[str, str] | None,
    dry_run: bool,
) -> tuple[list[dict[str, Any]], Path, Path]:
    batch_dir = verifier_dir / "tools" / VERIEQL_TOOL / "batch"
    batch_dir.mkdir(parents=True, exist_ok=True)
    input_jsonl = batch_dir / VERIEQL_JSONL_INPUT_NAME
    output_jsonl = batch_dir / VERIEQL_JSONL_OUTPUT_NAME
    shared_stdout_path = batch_dir / "raw_stdout.txt"
    shared_stderr_path = batch_dir / "raw_stderr.txt"
    write_verieql_pair_jsonl(pairs, input_jsonl)
    command = build_verieql_batch_command(
        availability.command or (),
        input_jsonl=input_jsonl,
        output_jsonl=output_jsonl,
        timeout_seconds=timeout_seconds,
    )

    if dry_run:
        shared_stdout_path.write_text("", encoding="utf-8")
        shared_stderr_path.write_text("VeriEQL JSONL dry run: command not executed.\n", encoding="utf-8")
        return (
            [
                _batch_not_attempted_pair(
                    pair=pair,
                    verifier_dir=verifier_dir,
                    timeout_seconds=timeout_seconds,
                    reason="verieql_dry_run_not_executed",
                    command=command,
                    input_jsonl=input_jsonl,
                    output_jsonl=output_jsonl,
                )
                for pair in pairs
            ],
            input_jsonl,
            output_jsonl,
        )

    started = time.monotonic()
    timed_out = False
    try:
        completed = subprocess.run(
            command,
            cwd=availability.verieql_root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=max(timeout_seconds, 1.0) * max(len(pairs), 1) + 5.0,
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
    shared_stdout_path.write_text(stdout, encoding="utf-8")
    shared_stderr_path.write_text(stderr, encoding="utf-8")
    if timed_out:
        return (
            [
                _batch_failure_pair(
                    pair=pair,
                    verifier_dir=verifier_dir,
                    timeout_seconds=timeout_seconds,
                    normalized="timeout",
                    invocation_status="timeout",
                    runtime_ms=runtime_ms,
                    stdout=stdout,
                    stderr=stderr,
                    command=command,
                    input_jsonl=input_jsonl,
                    output_jsonl=output_jsonl,
                    tool_version=availability.tool_version,
                )
                for pair in pairs
            ],
            input_jsonl,
            output_jsonl,
        )
    if returncode != 0 and not output_jsonl.exists():
        dependency_missing = _is_dependency_missing(stderr)
        return (
            [
                _batch_failure_pair(
                    pair=pair,
                    verifier_dir=verifier_dir,
                    timeout_seconds=timeout_seconds,
                    normalized="tool_error",
                    invocation_status="tool_error",
                    runtime_ms=runtime_ms,
                    stdout=stdout,
                    stderr=stderr,
                    command=command,
                    input_jsonl=input_jsonl,
                    output_jsonl=output_jsonl,
                    tool_version=availability.tool_version,
                    dependency_missing=dependency_missing,
                )
                for pair in pairs
            ],
            input_jsonl,
            output_jsonl,
        )

    output_records = parse_verieql_output_file(output_jsonl)
    verdict_records = []
    for index, pair in enumerate(pairs, start=1):
        output_record = output_records.get(index)
        normalized = normalize_verieql_jsonl_record(output_record)
        invocation_status = "completed"
        if normalized in {"timeout", "unsupported", "tool_error"}:
            invocation_status = normalized
        verdict_records.append(
            _batch_output_pair(
                pair=pair,
                verifier_dir=verifier_dir,
                timeout_seconds=timeout_seconds,
                normalized=normalized,
                invocation_status=invocation_status,
                runtime_ms=runtime_ms,
                output_record=output_record,
                stderr=stderr,
                command=command,
                input_jsonl=input_jsonl,
                output_jsonl=output_jsonl,
                tool_version=availability.tool_version,
            )
        )
    return verdict_records, input_jsonl, output_jsonl


def _run_direct_pair(
    *,
    pair: dict[str, str],
    availability: VeriEQLAvailability,
    verifier_dir: Path,
    timeout_seconds: float,
    env: Mapping[str, str] | None,
) -> dict[str, Any]:
    pair_id = pair["pair_id"]
    tool_dir = verifier_dir / "tools" / VERIEQL_TOOL / pair_id
    tool_dir.mkdir(parents=True, exist_ok=True)
    stdout_path = tool_dir / "raw_stdout.txt"
    stderr_path = tool_dir / "raw_stderr.txt"
    comparison_path = _comparison_sql_path(pair)
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
    normalized = normalize_verieql_output(stdout=stdout, stderr=stderr, returncode=returncode, timed_out=timed_out)
    invocation_status = "completed"
    if normalized in {"timeout", "unsupported", "tool_error"}:
        invocation_status = normalized
    return build_verdict_record(
        pair_id=pair_id,
        tool=VERIEQL_TOOL,
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
            "invocation_mode": availability.invocation_mode,
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
    tool_dir = verifier_dir / "tools" / VERIEQL_TOOL / pair_id
    tool_dir.mkdir(parents=True, exist_ok=True)
    stdout_path = tool_dir / "raw_stdout.txt"
    stderr_path = tool_dir / "raw_stderr.txt"
    stdout_path.write_text("", encoding="utf-8")
    stderr_path.write_text(f"VeriEQL not attempted: {reason}\n", encoding="utf-8")
    return build_verdict_record(
        pair_id=pair_id,
        tool=VERIEQL_TOOL,
        raw_verdict="not_attempted",
        invocation_status="not_attempted",
        tool_version="unavailable",
        raw_stdout_path=stdout_path.as_posix(),
        raw_stderr_path=stderr_path.as_posix(),
        runtime_ms=None,
        timeout_seconds=timeout_seconds,
        artifact_paths={"tool_dir": tool_dir.as_posix(), "detection_reason": reason},
    )


def _batch_not_attempted_pair(
    *,
    pair: dict[str, str],
    verifier_dir: Path,
    timeout_seconds: float,
    reason: str,
    command: Sequence[str],
    input_jsonl: Path,
    output_jsonl: Path,
) -> dict[str, Any]:
    pair_id = pair["pair_id"]
    tool_dir = verifier_dir / "tools" / VERIEQL_TOOL / pair_id
    tool_dir.mkdir(parents=True, exist_ok=True)
    stdout_path = tool_dir / "raw_stdout.txt"
    stderr_path = tool_dir / "raw_stderr.txt"
    stdout_path.write_text("", encoding="utf-8")
    stderr_path.write_text(f"VeriEQL not attempted: {reason}\n", encoding="utf-8")
    return build_verdict_record(
        pair_id=pair_id,
        tool=VERIEQL_TOOL,
        raw_verdict="not_attempted",
        invocation_status="not_attempted",
        tool_version="unavailable",
        raw_stdout_path=stdout_path.as_posix(),
        raw_stderr_path=stderr_path.as_posix(),
        runtime_ms=None,
        timeout_seconds=timeout_seconds,
        artifact_paths={
            "tool_dir": tool_dir.as_posix(),
            "command": _redacted_command(command),
            "verieql_jsonl_input": input_jsonl.as_posix(),
            "verieql_jsonl_output": output_jsonl.as_posix(),
            "detection_reason": reason,
            "invocation_mode": "jsonl_batch",
        },
    )


def _batch_failure_pair(
    *,
    pair: dict[str, str],
    verifier_dir: Path,
    timeout_seconds: float,
    normalized: str,
    invocation_status: str,
    runtime_ms: float,
    stdout: str,
    stderr: str,
    command: Sequence[str],
    input_jsonl: Path,
    output_jsonl: Path,
    tool_version: str | None,
    dependency_missing: bool = False,
) -> dict[str, Any]:
    pair_id = pair["pair_id"]
    tool_dir = verifier_dir / "tools" / VERIEQL_TOOL / pair_id
    tool_dir.mkdir(parents=True, exist_ok=True)
    stdout_path = tool_dir / "raw_stdout.txt"
    stderr_path = tool_dir / "raw_stderr.txt"
    stdout_path.write_text(stdout, encoding="utf-8")
    stderr_path.write_text(stderr, encoding="utf-8")
    return build_verdict_record(
        pair_id=pair_id,
        tool=VERIEQL_TOOL,
        raw_verdict=normalized,
        invocation_status=invocation_status,
        tool_version=tool_version or "unknown",
        raw_stdout_path=stdout_path.as_posix(),
        raw_stderr_path=stderr_path.as_posix(),
        runtime_ms=runtime_ms,
        timeout_seconds=timeout_seconds,
        artifact_paths={
            "tool_dir": tool_dir.as_posix(),
            "command": _redacted_command(command),
            "verieql_jsonl_input": input_jsonl.as_posix(),
            "verieql_jsonl_output": output_jsonl.as_posix(),
            "dependency_missing": dependency_missing,
            "invocation_mode": "jsonl_batch",
        },
    )


def _batch_output_pair(
    *,
    pair: dict[str, str],
    verifier_dir: Path,
    timeout_seconds: float,
    normalized: str,
    invocation_status: str,
    runtime_ms: float,
    output_record: Mapping[str, Any] | None,
    stderr: str,
    command: Sequence[str],
    input_jsonl: Path,
    output_jsonl: Path,
    tool_version: str | None,
) -> dict[str, Any]:
    pair_id = pair["pair_id"]
    tool_dir = verifier_dir / "tools" / VERIEQL_TOOL / pair_id
    tool_dir.mkdir(parents=True, exist_ok=True)
    stdout_path = tool_dir / "raw_stdout.txt"
    stderr_path = tool_dir / "raw_stderr.txt"
    stdout_path.write_text(json.dumps(output_record or {}, sort_keys=True), encoding="utf-8")
    stderr_path.write_text(stderr, encoding="utf-8")
    return build_verdict_record(
        pair_id=pair_id,
        tool=VERIEQL_TOOL,
        raw_verdict=normalized,
        invocation_status=invocation_status,
        tool_version=tool_version or "unknown",
        raw_stdout_path=stdout_path.as_posix(),
        raw_stderr_path=stderr_path.as_posix(),
        runtime_ms=runtime_ms,
        timeout_seconds=timeout_seconds,
        artifact_paths={
            "tool_dir": tool_dir.as_posix(),
            "command": _redacted_command(command),
            "verieql_jsonl_input": input_jsonl.as_posix(),
            "verieql_jsonl_output": output_jsonl.as_posix(),
            "invocation_mode": "jsonl_batch",
        },
    )


def _validate_verieql_pair(record: Mapping[str, Any]) -> dict[str, str]:
    pair = validate_pair_record(record)
    if pair["tool"] != VERIEQL_TOOL:
        raise ValueError("VeriEQL canary accepts only verieql pair records")
    return pair


def _comparison_sql_path(pair: Mapping[str, str]) -> str:
    pair_type = pair["pair_type"]
    if pair_type in {"source_vs_candidate", "source_vs_candidate_port_target", "support_pair_smoke"}:
        return pair["candidate_sql_path"]
    if pair_type == "source_vs_positive":
        return pair["positive_sql_path"]
    if pair_type == "source_vs_hard_negative":
        return pair["negative_sql_path"]
    raise ValueError(f"unsupported VeriEQL canary pair type: {pair_type}")


def _verieql_pair_role(pair_type: str) -> str:
    return {
        "source_vs_candidate": "source_candidate",
        "source_vs_candidate_port_target": "source_candidate_port_target",
        "source_vs_positive": "source_positive",
        "source_vs_hard_negative": "source_negative",
        "support_pair_smoke": "support_pair_smoke",
    }[pair_type]


def _candidate_commands(
    command: str | Sequence[str] | None,
    env: Mapping[str, str],
    *,
    search_path: str | None,
) -> list[tuple[str, ...]]:
    if command:
        return [_split_command(command)]
    candidates: list[tuple[str, ...]] = []
    for name in VERIEQL_ENV_VARS:
        value = env.get(name)
        if value:
            candidates.append(_split_command(value))
    for name in DEFAULT_VERIEQL_COMMANDS:
        if shutil.which(name, path=search_path):
            candidates.append((name,))
    return candidates


def _batch_base_command(command: str | Sequence[str] | None, env: Mapping[str, str]) -> tuple[str, ...]:
    raw_command = command
    if raw_command is None:
        raw_command = _first_env_value(env, VERIEQL_ENV_VARS)
    if raw_command is None:
        return (sys.executable, "-m", VERIEQL_BATCH_MODULE)
    parts = _split_command(raw_command)
    if VERIEQL_BATCH_MODULE in parts:
        return parts
    if "-m" in parts:
        return parts
    return (*parts, "-m", VERIEQL_BATCH_MODULE)


def _split_command(command: str | Sequence[str]) -> tuple[str, ...]:
    if isinstance(command, str):
        parts = tuple(shlex.split(command))
    else:
        parts = tuple(str(part) for part in command)
    if not parts:
        raise ValueError("VeriEQL command cannot be empty")
    return parts


def _first_env_value(env: Mapping[str, str], names: Sequence[str]) -> str | None:
    for name in names:
        value = env.get(name)
        if value:
            return value
    return None


def _is_valid_verieql_root(root: Path) -> bool:
    return root.is_dir() and (root / "parallel" / "cli_within_timeout.py").is_file()


def _command_executable_available(command: Sequence[str], *, search_path: str | None) -> bool:
    if not command:
        return False
    executable = command[0]
    return shutil.which(executable, path=search_path) is not None or Path(executable).exists()


def _probe_version(command: tuple[str, ...], *, timeout_seconds: float, cwd: Path | None = None) -> str | None:
    for flag in ("--version", "-version", "-h", "--help"):
        try:
            completed = subprocess.run(
                [*command, flag],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout_seconds,
                cwd=cwd,
            )
        except Exception:
            continue
        text = (completed.stdout or completed.stderr).strip()
        if text:
            return text.splitlines()[0][:200]
    return None


def _read_sql(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def _schema_from_context(path_text: str) -> dict[str, dict[str, str]]:
    if not path_text:
        return {}
    path = Path(path_text)
    if not path.exists() or not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        try:
            loaded = json.loads(text)
        except json.JSONDecodeError:
            return {}
        if isinstance(loaded, dict):
            return {
                str(table).upper(): {str(col).upper(): str(col_type).upper() for col, col_type in columns.items()}
                for table, columns in loaded.items()
                if isinstance(columns, Mapping)
            }
    return _parse_create_table_schema(text)


def _parse_create_table_schema(sql_text: str) -> dict[str, dict[str, str]]:
    schema: dict[str, dict[str, str]] = {}
    pattern = re.compile(r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([`\"A-Za-z0-9_.]+)\s*\((.*?)\)", re.IGNORECASE | re.DOTALL)
    for match in pattern.finditer(sql_text):
        table = match.group(1).strip('`"').split(".")[-1].upper()
        columns: dict[str, str] = {}
        for raw_column in _split_sql_columns(match.group(2)):
            parts = raw_column.strip().split()
            if len(parts) < 2:
                continue
            column_name = parts[0].strip('`",').upper()
            if column_name in {"PRIMARY", "FOREIGN", "UNIQUE", "CONSTRAINT", "CHECK", "KEY"}:
                continue
            columns[column_name] = parts[1].strip(",").upper()
        if columns:
            schema[table] = columns
    return schema


def _split_sql_columns(column_block: str) -> list[str]:
    pieces: list[str] = []
    start = 0
    depth = 0
    for index, char in enumerate(column_block):
        if char == "(":
            depth += 1
        elif char == ")" and depth:
            depth -= 1
        elif char == "," and depth == 0:
            pieces.append(column_block[start:index])
            start = index + 1
    pieces.append(column_block[start:])
    return pieces


def _as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if value is None:
        return []
    return [value]


def _is_dependency_missing(stderr: str) -> bool:
    lower = stderr.lower()
    return "modulenotfounderror" in lower or "no module named" in lower or "importerror" in lower


def _apply_verieql_na_reason(
    summary: dict[str, Any],
    *,
    availability: VeriEQLAvailability,
    verdict_records: Sequence[Mapping[str, Any]],
    dry_run: bool,
) -> None:
    if summary.get("semantic_equivalence_rate") is not None:
        return
    if dry_run:
        summary["na_reason"] = "verieql_dry_run_not_executed"
        return
    if not availability.tool_available:
        summary["na_reason"] = "verieql_unavailable"
        return
    if any(record.get("artifact_paths", {}).get("dependency_missing") for record in verdict_records):
        summary["na_reason"] = "verieql_dependency_missing"
        return
    if all(record.get("normalized_verdict") == "not_attempted" for record in verdict_records):
        summary["na_reason"] = "verieql_unavailable"


def _log_text(availability: VeriEQLAvailability, pair_count: int, *, dry_run: bool) -> str:
    return "\n".join(
        [
            "VeriEQL bounded canary local diagnostic.",
            f"tool_available={str(availability.tool_available).lower()}",
            f"tool_version={availability.tool_version or 'unknown'}",
            f"detection_reason={availability.detection_reason}",
            f"invocation_mode={availability.invocation_mode}",
            f"verieql_root={availability.verieql_root or ''}",
            f"dry_run={str(dry_run).lower()}",
            f"pairs_planned={pair_count}",
            "official_metric_input=false",
            "leaderboard_input=false",
            "",
        ]
    )


def _report_text(summary: Mapping[str, Any], availability: VeriEQLAvailability) -> str:
    rate = summary.get("semantic_equivalence_rate")
    rate_text = "N.A." if rate is None else str(rate)
    return "\n".join(
        [
            "# VeriEQL Canary Summary",
            "",
            "This is a bounded local diagnostic canary only.",
            "",
            f"- Tool available: `{str(availability.tool_available).lower()}`",
            f"- Tool version: `{availability.tool_version or 'unknown'}`",
            f"- Invocation mode: `{availability.invocation_mode}`",
            f"- VeriEQL root: `{availability.verieql_root or 'N.A.'}`",
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
    if not command:
        return []
    return [Path(command[0]).name, *[str(part) for part in command[1:]]]
