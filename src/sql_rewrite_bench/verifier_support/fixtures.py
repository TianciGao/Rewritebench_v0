"""Synthetic verifier fixture writer for local diagnostic tests."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .pairs import PAIR_FIELDS, boundary_flags_as_csv, validate_pair_record
from .summary import generate_semantic_equivalence_summary
from .verdicts import build_verdict_record


@dataclass(frozen=True)
class SyntheticVerifierFixture:
    output_root: Path
    run_id: str
    result_verifier_dir: Path
    log_dir: Path
    report_dir: Path
    pairs_path: Path
    verdicts_path: Path
    summary_path: Path
    log_path: Path
    report_path: Path


def synthetic_pair_record(
    *,
    pair_id: str,
    run_id: str,
    tool: str,
    case_id: str = "PERF_0006",
    pool: str = "PERF",
    engine: str = "postgres",
    route_id: str = "synthetic_route",
    method_id: str = "synthetic_method",
    pair_type: str = "source_vs_candidate",
    source_sql_path: str = "output/results/synthetic/candidates/source.sql",
    candidate_sql_path: str = "output/results/synthetic/candidates/candidate.sql",
    positive_sql_path: str = "",
    negative_sql_path: str = "",
    schema_context_path: str = "schemas/synthetic/schema_profile.yaml",
    checker_context_path: str = "cases/PERF/PERF_0006/checker",
    denominator_id: str = "synthetic_denominator",
) -> dict[str, str]:
    """Create a valid synthetic pair row for tests and fixture generation."""

    return validate_pair_record(
        {
            "pair_id": pair_id,
            "run_id": run_id,
            "tool": tool,
            "case_id": case_id,
            "pool": pool,
            "engine": engine,
            "route_id": route_id,
            "method_id": method_id,
            "pair_type": pair_type,
            "source_sql_path": source_sql_path,
            "candidate_sql_path": candidate_sql_path,
            "positive_sql_path": positive_sql_path,
            "negative_sql_path": negative_sql_path,
            "schema_context_path": schema_context_path,
            "checker_context_path": checker_context_path,
            "denominator_id": denominator_id,
            **boundary_flags_as_csv(),
        }
    )


def write_synthetic_verifier_fixture(
    *,
    output_root: str | Path,
    run_id: str,
    pair_records: list[dict[str, Any]],
    raw_verdict_rows: list[dict[str, Any]],
    result_consistent_pairs: int | None = None,
) -> SyntheticVerifierFixture:
    """Write contract-shaped synthetic verifier outputs under a temp output root.

    The writer never invokes external verifier binaries. It creates raw-output
    placeholder files so verdict records can point at real local artifacts.
    """

    root = Path(output_root)
    verifier_dir = root / "results" / run_id / "verifier"
    log_dir = root / "logs" / run_id
    report_dir = root / "reports" / run_id
    verifier_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)

    pairs = [validate_pair_record(record) for record in pair_records]
    pairs_by_id = {record["pair_id"]: record for record in pairs}
    if len(pairs_by_id) != len(pairs):
        raise ValueError("synthetic verifier pairs require unique pair_id values")
    pairs_path = verifier_dir / "verifier_pairs.csv"
    with pairs_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=PAIR_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(pairs)

    verdict_records: list[dict[str, Any]] = []
    for raw_row in raw_verdict_rows:
        pair_id = str(raw_row.get("pair_id", ""))
        if pair_id not in pairs_by_id:
            raise ValueError(f"raw verifier verdict references unknown pair_id: {pair_id}")
        pair = pairs_by_id[pair_id]
        tool = str(raw_row.get("tool") or pair["tool"])
        if tool != pair["tool"]:
            raise ValueError(f"raw verifier verdict tool does not match pair tool for {pair_id}")
        tool_dir = verifier_dir / "tools" / tool / pair_id
        tool_dir.mkdir(parents=True, exist_ok=True)
        stdout_path = tool_dir / "raw_stdout.txt"
        stderr_path = tool_dir / "raw_stderr.txt"
        stdout_path.write_text(str(raw_row.get("raw_stdout", "")), encoding="utf-8")
        stderr_path.write_text(str(raw_row.get("raw_stderr", "")), encoding="utf-8")
        record = build_verdict_record(
            pair_id=pair_id,
            tool=tool,
            raw_verdict=raw_row.get("raw_verdict"),
            invocation_status=str(raw_row.get("invocation_status", "completed")),
            tool_version=str(raw_row.get("tool_version", "synthetic")),
            raw_stdout_path=stdout_path.as_posix(),
            raw_stderr_path=stderr_path.as_posix(),
            runtime_ms=raw_row.get("runtime_ms"),
            timeout_seconds=raw_row.get("timeout_seconds"),
            artifact_paths={"tool_dir": tool_dir.as_posix()},
        )
        verdict_records.append(record)

    verdicts_path = verifier_dir / "verifier_verdicts.jsonl"
    with verdicts_path.open("w", encoding="utf-8") as handle:
        for record in verdict_records:
            handle.write(json.dumps(record, sort_keys=True) + "\n")

    summary = generate_semantic_equivalence_summary(
        run_id=run_id,
        verdict_rows=verdict_records,
        verifier_tools_requested=sorted({record["tool"] for record in pairs}),
        pairs_planned=len(pairs),
        result_consistent_pairs=result_consistent_pairs,
    )
    summary_path = verifier_dir / "semantic_equivalence_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    log_path = log_dir / "verifier.log"
    log_path.write_text(
        "Synthetic verifier fixture only. No VeriEQL or SQLSolver binaries were invoked.\n",
        encoding="utf-8",
    )
    report_path = report_dir / "verifier_summary.md"
    report_path.write_text(_summary_report_text(summary), encoding="utf-8")

    return SyntheticVerifierFixture(
        output_root=root,
        run_id=run_id,
        result_verifier_dir=verifier_dir,
        log_dir=log_dir,
        report_dir=report_dir,
        pairs_path=pairs_path,
        verdicts_path=verdicts_path,
        summary_path=summary_path,
        log_path=log_path,
        report_path=report_path,
    )


def _summary_report_text(summary: dict[str, Any]) -> str:
    rate = summary.get("semantic_equivalence_rate")
    rate_text = "N.A." if rate is None else str(rate)
    return "\n".join(
        [
            "# Verifier Summary",
            "",
            "Synthetic verifier fixture output only.",
            "",
            f"- Semantic Equivalence Rate: `{rate_text}`",
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
