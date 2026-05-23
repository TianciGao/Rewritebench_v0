"""Bounded VeriEQL canary support for local diagnostic verifier outputs.

The wrapper is intentionally narrow. It detects an available VeriEQL command,
can run explicitly supplied bounded pairs, and writes D035-shaped local verifier
artifacts. It does not implement broad user-facing verifier execution, SQLSolver
support, official metrics, retained-evidence promotion, or leaderboard output.
"""

from __future__ import annotations

import csv
import json
import os
import shlex
import shutil
import subprocess
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
VERIEQL_ENV_VARS = ("SQLRB_VERIEQL_COMMAND", "VERIEQL_COMMAND", "VERIEQL_BIN")


@dataclass(frozen=True)
class VeriEQLAvailability:
    tool_available: bool
    command: tuple[str, ...] | None
    command_path: str | None
    tool_version: str | None
    detection_reason: str


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


def detect_verieql(
    command: str | Sequence[str] | None = None,
    *,
    env: Mapping[str, str] | None = None,
    search_path: str | None = None,
    version_timeout_seconds: float = 5.0,
) -> VeriEQLAvailability:
    """Detect a local VeriEQL command without installing anything."""

    effective_env = dict(os.environ if env is None else env)
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
    if any(token in compact for token in ["unsupported", "not_supported", "unsupported_sql", "unsupported_syntax"]):
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
        verifier_tools_requested=[VERIEQL_TOOL],
        pairs_planned=len(pairs),
        result_consistent_pairs=result_consistent_pairs,
    )
    summary["tool_available"] = availability.tool_available
    summary["tool_version"] = availability.tool_version
    if not availability.tool_available:
        summary["na_reason"] = "verieql_unavailable"
    summary_path = verifier_dir / "semantic_equivalence_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    log_path = log_dir / "verifier.log"
    log_path.write_text(_log_text(availability, len(pairs)), encoding="utf-8")
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
    )


def _run_available_pair(
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


def _split_command(command: str | Sequence[str]) -> tuple[str, ...]:
    if isinstance(command, str):
        parts = tuple(shlex.split(command))
    else:
        parts = tuple(str(part) for part in command)
    if not parts:
        raise ValueError("VeriEQL command cannot be empty")
    return parts


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


def _log_text(availability: VeriEQLAvailability, pair_count: int) -> str:
    return "\n".join(
        [
            "VeriEQL bounded canary local diagnostic.",
            f"tool_available={str(availability.tool_available).lower()}",
            f"tool_version={availability.tool_version or 'unknown'}",
            f"detection_reason={availability.detection_reason}",
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
