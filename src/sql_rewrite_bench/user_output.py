"""User-facing output export for local diagnostic runs.

This module maps existing ``runs/user/<run_id>`` artifacts into the D035
``output/results|logs|reports/<run_id>`` shape. It is an exporter only: it
does not invoke adapters, execute databases, run checkers, collect timing,
compute metrics, update official reports/results, promote retained evidence,
or create leaderboard output.
"""

from __future__ import annotations

import csv
import json
import shutil
import subprocess
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path
from typing import Any

from .local_timing import route_identity

OUTPUT_CONTRACT_VERSION = "v0"

BOUNDARY_FLAGS = {
    "local_diagnostic_only": True,
    "official_metric_input": False,
    "paper_result_input": False,
    "retained_evidence_promoted": False,
    "leaderboard_input": False,
}

FAILURE_BUCKET_FIELDS = [
    "failure_bucket",
    "count",
    "engines",
    "pools",
    "representative_cases",
    "explanation",
]

VERIFIER_STATUS_SCHEMA_VERSION = "user_output_verifier_status_v0"
VERIFIER_STATUS_NA = "N.A."
VERIFIER_STATUS_COVERAGE_LIMITED = "coverage_limited"
VERIFIER_STATUS_COMPUTED_LOCAL_SUPPORT = "computed_local_support"
VERIFIER_STATUS_VALUES = {
    VERIFIER_STATUS_NA,
    VERIFIER_STATUS_COVERAGE_LIMITED,
    VERIFIER_STATUS_COMPUTED_LOCAL_SUPPORT,
}


@dataclass(frozen=True)
class UserOutputPaths:
    output_root: Path
    result_root: Path
    log_root: Path
    report_root: Path


@dataclass(frozen=True)
class ExportedUserOutput:
    run_id: str
    paths: UserOutputPaths
    run_manifest_path: Path
    copied_files: tuple[Path, ...]
    generated_files: tuple[Path, ...]


def build_output_paths(
    output_root: str | Path,
    run_id: str,
    *,
    repo_root: Path | None = None,
) -> UserOutputPaths:
    """Build D035 output roots for a run id."""

    _validate_run_id(run_id)
    output_root_path = Path(output_root)
    _validate_output_root(output_root_path, repo_root=repo_root)
    return UserOutputPaths(
        output_root=output_root_path,
        result_root=output_root_path / "results" / run_id,
        log_root=output_root_path / "logs" / run_id,
        report_root=output_root_path / "reports" / run_id,
    )


def export_run_to_output(
    run_dir: str | Path,
    output_root: str | Path,
    *,
    run_id: str | None = None,
    repo_root: Path | None = None,
    git_commit: str | None = None,
) -> ExportedUserOutput:
    """Export one existing local user-run directory into the output contract."""

    source_run_dir = Path(run_dir)
    if not source_run_dir.exists() or not source_run_dir.is_dir():
        raise ValueError(f"source run directory does not exist: {source_run_dir}")

    config = _read_config(source_run_dir / "config.yaml")
    summary = _read_json(source_run_dir / "summary.json")
    selected_cases = _read_csv(source_run_dir / "selected_cases.csv")
    ledger_rows = _read_csv(source_run_dir / "ledger.csv")
    effective_run_id = run_id or _text(config.get("run_id")) or _text(summary.get("run_id")) or source_run_dir.name
    paths = build_output_paths(output_root, effective_run_id, repo_root=repo_root)
    _ensure_roots(paths)

    copied: list[Path] = []
    generated: list[Path] = []
    verifier_status = _build_verifier_status(source_run_dir, effective_run_id)

    copied.extend(_export_results(source_run_dir, paths))
    verifier_copied, verifier_generated = _export_verifier_artifacts(source_run_dir, paths, verifier_status)
    copied.extend(verifier_copied)
    generated.extend(verifier_generated)
    failure_bucket_rows = _write_failure_buckets_csv(
        paths.result_root / "failure_buckets.csv",
        ledger_rows=ledger_rows,
        failure_rows=_read_csv(source_run_dir / "failures.csv"),
    )
    generated.append(paths.result_root / "failure_buckets.csv")

    manifest_path = write_run_manifest(
        source_run_dir=source_run_dir,
        paths=paths,
        config=config,
        selected_cases=selected_cases,
        ledger_rows=ledger_rows,
        verifier_status=verifier_status,
        git_commit=git_commit or _git_commit(repo_root),
    )
    generated.append(manifest_path)

    generated.extend(_write_logs(source_run_dir, paths, config, failure_bucket_rows, verifier_status))
    generated.extend(
        _write_reports(
            source_run_dir=source_run_dir,
            paths=paths,
            manifest_path=manifest_path,
            summary=summary,
            quality_summary=_read_json(source_run_dir / "quality_summary.json"),
            failure_bucket_rows=failure_bucket_rows,
            verifier_status=verifier_status,
        )
    )
    return ExportedUserOutput(
        run_id=effective_run_id,
        paths=paths,
        run_manifest_path=manifest_path,
        copied_files=tuple(copied),
        generated_files=tuple(generated),
    )


def write_run_manifest(
    *,
    source_run_dir: Path,
    paths: UserOutputPaths,
    config: dict[str, Any],
    selected_cases: list[dict[str, str]],
    ledger_rows: list[dict[str, str]],
    verifier_status: dict[str, Any] | None = None,
    git_commit: str | None = None,
) -> Path:
    """Write ``run_manifest.json`` for an exported local diagnostic run."""

    run_id = paths.result_root.name
    adapter_command = _text(config.get("adapter_command"))
    route_id, method_id = route_identity(adapter_command) if adapter_command else ("", "")
    selected_case_ids = sorted({_text(row.get("case_id")) for row in selected_cases or ledger_rows if _text(row.get("case_id"))})
    selected_engines = sorted({_text(row.get("engine")) for row in selected_cases or ledger_rows if _text(row.get("engine"))})
    denominator_ids = sorted({_text(row.get("denominator_id")) for row in selected_cases or ledger_rows if _text(row.get("denominator_id"))})
    timing_policy = _read_json(source_run_dir / "timing" / "timing_policy.json")
    verifier_status = verifier_status or _build_verifier_status(source_run_dir, run_id)
    manifest = {
        "schema_version": "user_output_run_manifest_v0",
        "run_id": run_id,
        "created_at": _utc_now_iso(),
        "source_run_dir": source_run_dir.as_posix(),
        "result_root": paths.result_root.as_posix(),
        "log_root": paths.log_root.as_posix(),
        "report_root": paths.report_root.as_posix(),
        "git_commit": git_commit,
        "benchmark_version": None,
        "workbench_version": _workbench_version(),
        "case_set": _text(config.get("case_set")) or None,
        "selected_cases": selected_case_ids,
        "selected_case_count": len(selected_case_ids),
        "selected_engines": selected_engines,
        "adapter_command": adapter_command or None,
        "route_id": route_id or None,
        "method_id": method_id or None,
        "denominator_id": denominator_ids[0] if len(denominator_ids) == 1 else denominator_ids,
        "denominator_ids": denominator_ids,
        "timing_enabled": _bool_like(config.get("timing_enabled")) or (source_run_dir / "timing").exists(),
        "timing_policy_id": timing_policy.get("timing_policy_id") if timing_policy else None,
        "verifier_enabled": bool(verifier_status.get("verifier_enabled")),
        "verifier_tools_requested": verifier_status.get("verifier_tools_requested", []),
        "verifier_tools_completed": verifier_status.get("verifier_tools_completed", []),
        "semantic_equivalence_rate_status": verifier_status.get("semantic_equivalence_rate_status", VERIFIER_STATUS_NA),
        "official_SER": bool(verifier_status.get("official_SER", False)),
        "output_contract_version": OUTPUT_CONTRACT_VERSION,
        **BOUNDARY_FLAGS,
    }
    path = paths.result_root / "run_manifest.json"
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def write_boundary_report(report_root: Path) -> Path:
    """Write the local-only boundary report."""

    path = report_root / "boundary.md"
    path.write_text(
        "\n".join(
            [
                "# Local Output Boundary",
                "",
                "This is local diagnostic output only.",
                "",
                "- It is not official metrics.",
                "- It is not paper results.",
                "- It is not retained evidence.",
                "- It is not leaderboard input.",
                "- It does not update top-level `reports/` or `results/`.",
                "- Promotion to top-level `reports/`, `results/`, or retained evidence requires a separate authorized task.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return path


def write_summary_report(
    *,
    report_root: Path,
    manifest: dict[str, Any],
    summary: dict[str, Any],
    quality_summary: dict[str, Any],
) -> Path:
    """Write the human-readable run summary."""

    funnel = quality_summary.get("funnel_counts", {}) if isinstance(quality_summary, dict) else {}
    lines = [
        "# User Output Summary",
        "",
        "This is local diagnostic output only.",
        "",
        "## Run",
        "",
        f"- Run id: `{manifest.get('run_id', '')}`",
        f"- Case set: `{manifest.get('case_set') or 'unknown'}`",
        f"- Selected cases: `{manifest.get('selected_case_count', 0)}`",
        f"- Engines: `{', '.join(manifest.get('selected_engines') or []) or 'unknown'}`",
        f"- Route id: `{manifest.get('route_id') or 'unknown'}`",
        "",
        "## Funnel",
        "",
    ]
    if funnel:
        for key, value in funnel.items():
            lines.append(f"- {key}: {value}")
    elif summary:
        for key in [
            "selected_rows",
            "candidate_generated_rows",
            "candidate_preflight_passed_rows",
            "source_executable_rows",
            "candidate_executable_rows",
            "checker_attempted_rows",
            "exact_rows",
            "mismatch_rows",
        ]:
            if key in summary:
                lines.append(f"- {key}: {summary[key]}")
    else:
        lines.append("- not available in this source run")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- Official metrics computed: `false`",
            "- Paper results updated: `false`",
            "- Retained evidence promoted: `false`",
            "- Leaderboard input: `false`",
            "",
        ]
    )
    path = report_root / "summary.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def write_failure_bucket_report(report_root: Path, rows: list[dict[str, str]]) -> Path:
    """Write a human-readable failure bucket report."""

    lines = [
        "# Failure Buckets",
        "",
        "This report is derived from local diagnostic ledger/failure artifacts.",
        "",
    ]
    if not rows:
        lines.append("No failure buckets were present in this source run.")
    else:
        lines.extend(["| failure_bucket | count | engines | pools | representative_cases |", "| --- | ---: | --- | --- | --- |"])
        for row in rows:
            lines.append(
                f"| `{row['failure_bucket']}` | {row['count']} | {row['engines']} | {row['pools']} | {row['representative_cases']} |"
            )
    lines.extend(["", "This is not official metrics and not leaderboard input.", ""])
    path = report_root / "failure_buckets.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def write_tag_slice_report(source_tag_slices: Path, report_root: Path) -> Path:
    """Write a human-readable tag-slice report from an existing CSV if present."""

    path = report_root / "tag_slices.md"
    rows = _read_csv(source_tag_slices)
    lines = [
        "# Tag Slices",
        "",
        "This report is derived from source-run `tag_slices.csv` when available.",
        "",
    ]
    if not rows:
        lines.append("Tag slices are not available in this source run.")
    else:
        lines.append(f"Rows available: `{len(rows)}`.")
        lines.extend(["", "| axis | tag | selected | exact | mismatch |", "| --- | --- | ---: | ---: | ---: |"])
        for row in rows[:20]:
            axis = _text(row.get("axis") or row.get("tag_axis"))
            tag = _text(row.get("tag"))
            selected = _text(row.get("selected_rows") or row.get("selected"))
            exact = _text(row.get("exact_rows") or row.get("exact"))
            mismatch = _text(row.get("mismatch_rows") or row.get("mismatch"))
            lines.append(f"| {axis} | {tag} | {selected} | {exact} | {mismatch} |")
        if len(rows) > 20:
            lines.append(f"| ... | ... | ... | ... | {len(rows) - 20} additional rows omitted |")
    lines.extend(["", "This is local diagnostic tag-slice output only.", ""])
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def write_metrics_summary_report(source_metrics_dir: Path, report_root: Path) -> Path:
    """Write a metrics summary report, or an explicit N.A. report if absent."""

    path = report_root / "metrics_summary.md"
    summary = _read_json(source_metrics_dir / "local_metrics_summary.json")
    lines = [
        "# Local Metrics Summary",
        "",
    ]
    if not summary:
        lines.extend(
            [
                "Local metrics were not computed for this source run.",
                "",
                "- Generation/Execution/Result Consistency: `N.A.`",
                "- Performance: `N.A.`",
                "- Semantic Equivalence Rate: `N.A.` without verifier evidence",
                (
                    "- POCR: optional diagnostic support via `pocr-diagnostic` and "
                    "`pocr-aggregate`; not an official paper metric unless separately promoted"
                ),
                "",
            ]
        )
    else:
        lines.extend(
            [
                "This summarizes existing non-official local metrics artifacts.",
                "",
                f"- Schema version: `{summary.get('schema_version', '')}`",
                f"- Route ids: `{', '.join(summary.get('route_ids') or [])}`",
                f"- Method ids: `{', '.join(summary.get('method_ids') or [])}`",
            ]
        )
        overall = summary.get("overall")
        if isinstance(overall, dict) and "counts" in overall:
            counts = overall["counts"]
            rates = overall.get("rates", {})
            lines.extend(
                [
                    f"- Selected: `{counts.get('selected')}`",
                    f"- Candidate generated: `{counts.get('candidate_generated')}`",
                    f"- Candidate executable: `{counts.get('candidate_executable')}`",
                    f"- Exact: `{counts.get('exact')}`",
                    f"- Generation Rate: `{rates.get('generation_rate')}`",
                    f"- Execution Coverage Rate: `{rates.get('execution_coverage_rate')}`",
                    f"- Result Consistency Rate: `{rates.get('result_consistency_rate')}`",
                ]
            )
        lines.extend(["", "These are local diagnostic metrics only, not official metrics.", ""])
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def _export_results(source_run_dir: Path, paths: UserOutputPaths) -> list[Path]:
    copied: list[Path] = []
    for source_name, target_name in [
        ("ledger.csv", "ledger.csv"),
        ("quality_summary.json", "quality_summary.json"),
        ("tag_slices.csv", "tag_slices.csv"),
    ]:
        src = source_run_dir / source_name
        if src.exists():
            dst = paths.result_root / target_name
            _copy_file(src, dst)
            copied.append(dst)
    for source_name, target_name in [
        ("candidate_sql", "candidates"),
        ("timing", "timing"),
        ("metrics", "metrics"),
    ]:
        src = source_run_dir / source_name
        if src.exists():
            dst = paths.result_root / target_name
            _copy_tree(src, dst)
            copied.append(dst)
    _export_workspace_subdirs(source_run_dir / "workspaces", paths.result_root / "execution", "execution", copied)
    _export_workspace_subdirs(source_run_dir / "workspaces", paths.result_root / "checker", "checker", copied)
    return copied


def _export_workspace_subdirs(workspaces_dir: Path, target_root: Path, subdir_name: str, copied: list[Path]) -> None:
    if not workspaces_dir.exists():
        return
    for src in sorted(workspaces_dir.glob(f"*/*/{subdir_name}")):
        if not src.is_dir():
            continue
        try:
            relative_parent = src.relative_to(workspaces_dir).parent
        except ValueError:
            continue
        dst = target_root / relative_parent
        _copy_tree(src, dst)
        copied.append(dst)


def _build_verifier_status(source_run_dir: Path, run_id: str) -> dict[str, Any]:
    source_verifier_dir = source_run_dir / "verifier"
    source_status = _read_json(source_verifier_dir / "verifier_status.json")
    semantic_summary = _read_json(source_verifier_dir / "semantic_equivalence_summary.json")
    verifier_enabled = source_verifier_dir.exists() and source_verifier_dir.is_dir() and bool(source_status or semantic_summary)
    raw_status = (
        _text(source_status.get("semantic_equivalence_rate_status"))
        or _text(source_status.get("SER_status"))
        or _text(semantic_summary.get("semantic_equivalence_rate_status"))
        or _text(semantic_summary.get("SER_status"))
    )
    status = _normalize_verifier_status(raw_status, verifier_enabled=verifier_enabled, semantic_summary=semantic_summary)
    requested = _list_value(source_status.get("verifier_tools_requested")) or _list_value(
        semantic_summary.get("verifier_tools_requested")
    )
    completed = _list_value(source_status.get("verifier_tools_completed")) or _list_value(
        semantic_summary.get("verifier_tools_completed")
    )
    tool_summaries = source_status.get("tool_summaries")
    if not isinstance(tool_summaries, list) or not tool_summaries:
        tool_summaries = _tool_summaries_from_semantic_summary(semantic_summary, requested=requested)
    reason = _text(source_status.get("reason"))
    if status == VERIFIER_STATUS_NA and not reason:
        reason = _text(semantic_summary.get("na_reason")) or "formal_verifier_evidence_missing"
    boundary_notes = source_status.get("boundary_notes")
    if not isinstance(boundary_notes, list):
        boundary_notes = []
    boundary_notes = [str(note) for note in boundary_notes]
    for note in [
        "local diagnostic verifier support only",
        "official_SER=false",
        "local checker exactness is not SER evidence",
        "no paper result input",
    ]:
        if note not in boundary_notes:
            boundary_notes.append(note)
    payload = {
        "schema_version": VERIFIER_STATUS_SCHEMA_VERSION,
        "run_id": run_id,
        "verifier_enabled": verifier_enabled,
        "verifier_tools_requested": requested,
        "verifier_tools_completed": completed,
        "semantic_equivalence_rate_status": status,
        "official_SER": False,
        "result_checker_exactness_used": False,
        "local_diagnostic_only": True,
        "paper_result_input": False,
        "retained_evidence_promoted": False,
        "leaderboard_input": False,
        "tool_summaries": tool_summaries,
        "boundary_notes": boundary_notes,
        "source_artifacts_present": verifier_enabled,
    }
    if reason:
        payload["reason"] = reason
    for optional_key in [
        "semantic_equivalence_rate",
        "bounded_verifier_support_ratio_if_decidable",
        "decidable_actual_pairs",
        "selected_pairs",
        "eligible_exact_pairs",
        "actual_attempted_pairs",
    ]:
        if optional_key in source_status:
            payload[optional_key] = source_status[optional_key]
        elif optional_key in semantic_summary:
            payload[optional_key] = semantic_summary[optional_key]
    return payload


def _normalize_verifier_status(
    status: str,
    *,
    verifier_enabled: bool,
    semantic_summary: dict[str, Any],
) -> str:
    normalized = status.strip()
    normalized_lower = normalized.lower().replace("-", "_").replace(" ", "_")
    if normalized in VERIFIER_STATUS_VALUES:
        return normalized
    if normalized_lower in {"n.a.", "n_a", "na", "not_applicable", "not_available"}:
        return VERIFIER_STATUS_NA
    if normalized_lower in {"coverage_limited", "limited", "computed_bounded_support"}:
        return VERIFIER_STATUS_COVERAGE_LIMITED
    if normalized_lower in {"computed", "computed_local_support", "local_support"}:
        return VERIFIER_STATUS_COMPUTED_LOCAL_SUPPORT
    if not verifier_enabled:
        return VERIFIER_STATUS_NA
    if _has_non_decidable_verifier_counts(semantic_summary):
        return VERIFIER_STATUS_COVERAGE_LIMITED
    if semantic_summary.get("semantic_equivalence_rate") is not None:
        return VERIFIER_STATUS_COMPUTED_LOCAL_SUPPORT
    return VERIFIER_STATUS_COVERAGE_LIMITED


def _has_non_decidable_verifier_counts(summary: dict[str, Any]) -> bool:
    for key in [
        "unknown_count",
        "timeout_count",
        "unsupported_count",
        "syntax_error_count",
        "not_implemented_count",
        "out_of_memory_count",
        "tool_error_count",
        "not_attempted_count",
        "no_verifier_support",
        "no_verifier_support_count",
    ]:
        if _int_like(summary.get(key)) > 0:
            return True
    return False


def _tool_summaries_from_semantic_summary(
    semantic_summary: dict[str, Any],
    *,
    requested: list[str],
) -> list[dict[str, Any]]:
    if not semantic_summary:
        return []
    tool_value = _text(semantic_summary.get("tool"))
    tools = [tool_value] if tool_value else requested or _list_value(semantic_summary.get("verifier_tools_requested"))
    if not tools:
        tools = ["unknown"]
    selected = _first_present(semantic_summary, ["selected_pairs", "pairs_planned"])
    attempted = _first_present(semantic_summary, ["actual_attempted_pairs", "pairs_attempted"])
    decidable = _first_present(semantic_summary, ["decidable_actual_pairs", "decidable_count"])
    return [
        {
            "tool": tool,
            "selected_pairs": selected,
            "eligible_pairs": _first_present(semantic_summary, ["eligible_exact_pairs", "result_consistent_pairs"]),
            "attempted_pairs": attempted,
            "decidable_pairs": decidable,
            "equivalent": _first_present(semantic_summary, ["equivalent", "equivalent_count"]),
            "non_equivalent": _first_present(semantic_summary, ["non_equivalent", "non_equivalent_count"]),
            "unknown": _first_present(semantic_summary, ["unknown", "unknown_count"]),
            "timeout": _first_present(semantic_summary, ["timeout", "timeout_count"]),
            "unsupported": _first_present(semantic_summary, ["unsupported", "unsupported_count"]),
            "no_verifier_support": _first_present(
                semantic_summary,
                ["no_verifier_support", "no_verifier_support_count"],
            ),
            "tool_error": _first_present(semantic_summary, ["tool_error", "tool_error_count"]),
        }
        for tool in tools
    ]


def _verifier_summary_text(verifier_status: dict[str, Any]) -> str:
    status = _text(verifier_status.get("semantic_equivalence_rate_status")) or VERIFIER_STATUS_NA
    lines = [
        "# Verifier Summary",
        "",
        "This is local diagnostic verifier-support output only.",
        "",
        f"- SER status: `{status}`",
        f"- official_SER: `{str(bool(verifier_status.get('official_SER'))).lower()}`",
        f"- result_checker_exactness_used: `{str(bool(verifier_status.get('result_checker_exactness_used'))).lower()}`",
        f"- local_diagnostic_only: `{str(bool(verifier_status.get('local_diagnostic_only'))).lower()}`",
        f"- paper_result_input: `{str(bool(verifier_status.get('paper_result_input'))).lower()}`",
        "",
    ]
    if status == VERIFIER_STATUS_NA:
        lines.extend(
            [
                "Verifier support was not run.",
                "",
                "Verifier evidence unavailable.",
                "",
                f"- Reason: `{verifier_status.get('reason') or 'formal_verifier_evidence_missing'}`",
                "- Semantic Equivalence Rate: `N.A.`",
                "",
            ]
        )
    elif status == VERIFIER_STATUS_COVERAGE_LIMITED:
        lines.extend(
            [
                "Coverage-limited verifier support is present.",
                "",
                "Non-decidable verifier outcomes are reported separately and excluded from the decidable denominator.",
                "",
            ]
        )
    elif status == VERIFIER_STATUS_COMPUTED_LOCAL_SUPPORT:
        lines.extend(
            [
                "Computed local bounded verifier support is present.",
                "",
                "This is not official SER and must not be promoted to paper results.",
                "",
            ]
        )
    tool_summaries = verifier_status.get("tool_summaries")
    if isinstance(tool_summaries, list) and tool_summaries:
        lines.extend(
            [
                "## Tool Summaries",
                "",
                "| tool | selected | eligible | attempted | decidable | equivalent | non_equivalent | unknown | timeout | unsupported | no_verifier_support | tool_error |",
                "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
            ]
        )
        for row in tool_summaries:
            if not isinstance(row, dict):
                continue
            lines.append(
                "| "
                + " | ".join(
                    [
                        _text(row.get("tool") or "unknown"),
                        _summary_value(row.get("selected_pairs")),
                        _summary_value(row.get("eligible_pairs")),
                        _summary_value(row.get("attempted_pairs")),
                        _summary_value(row.get("decidable_pairs")),
                        _summary_value(row.get("equivalent")),
                        _summary_value(row.get("non_equivalent")),
                        _summary_value(row.get("unknown")),
                        _summary_value(row.get("timeout")),
                        _summary_value(row.get("unsupported")),
                        _summary_value(row.get("no_verifier_support")),
                        _summary_value(row.get("tool_error")),
                    ]
                )
                + " |"
            )
        lines.append("")
    lines.extend(
        [
            "## Boundary",
            "",
            "- SQLSolver and VeriEQL are verifier/support tools, not rewrite baselines.",
            "- `coverage_limited`, `no_verifier_support`, `unsupported`, `unknown`, `timeout`, and `tool_error` are verifier-support statuses, not method failure buckets.",
            "- Local checker exactness remains Result Consistency evidence only, not SER evidence.",
            "- No official SER is produced by this export.",
            "",
        ]
    )
    return "\n".join(lines)


def _verifier_log_text(verifier_status: dict[str, Any]) -> str:
    status = _text(verifier_status.get("semantic_equivalence_rate_status")) or VERIFIER_STATUS_NA
    tools = ", ".join(_list_value(verifier_status.get("verifier_tools_completed")) or []) or "none"
    return (
        "Verifier output export log\n\n"
        f"SER status: {status}\n"
        f"official_SER: {str(bool(verifier_status.get('official_SER'))).lower()}\n"
        f"verifier tools completed: {tools}\n"
        "Boundary: local diagnostic verifier support only; not official metrics; not paper results.\n"
    )


def _list_value(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item)]
    if isinstance(value, tuple):
        return [str(item) for item in value if str(item)]
    if isinstance(value, str) and value:
        return [value]
    return []


def _first_present(mapping: dict[str, Any], keys: list[str]) -> Any:
    for key in keys:
        if key in mapping:
            return mapping[key]
    return None


def _summary_value(value: Any) -> str:
    return "" if value is None else _text(value)


def _int_like(value: Any) -> int:
    try:
        if value is None or value == "":
            return 0
        return int(value)
    except (TypeError, ValueError):
        return 0


def _write_logs(
    source_run_dir: Path,
    paths: UserOutputPaths,
    config: dict[str, Any],
    failure_bucket_rows: list[dict[str, str]],
    verifier_status: dict[str, Any],
) -> list[Path]:
    generated: list[Path] = []
    command_log = paths.log_root / "command.log"
    command_log.write_text(
        "\n".join(
            [
                "User output export command log",
                "",
                f"Source run dir: {source_run_dir.as_posix()}",
                f"Result root: {paths.result_root.as_posix()}",
                f"Log root: {paths.log_root.as_posix()}",
                f"Report root: {paths.report_root.as_posix()}",
                f"Adapter command: {_text(config.get('adapter_command')) or 'not available'}",
                "Boundary: local diagnostic only; not official metrics; not retained evidence; not leaderboard input.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    generated.append(command_log)
    for log_name, glob_pattern in [
        ("adapter_stdout.log", "workspaces/*/*/adapter_stdout.txt"),
        ("adapter_stderr.log", "workspaces/*/*/adapter_stderr.txt"),
    ]:
        path = paths.log_root / log_name
        _write_aggregated_text_log(path, sorted(source_run_dir.glob(glob_pattern)))
        generated.append(path)
    engine_env = paths.log_root / "engine_env.json"
    timing_env = _read_json(source_run_dir / "timing" / "environment_metadata.json")
    payload = timing_env or {
        "status": "not_available_in_source_run",
        "secret_redaction_policy": "no secrets or full environment dumps recorded",
        **BOUNDARY_FLAGS,
    }
    engine_env.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    generated.append(engine_env)
    failures_log = paths.log_root / "failures.log"
    if failure_bucket_rows:
        failures_log.write_text(
            "\n".join(
                f"{row['failure_bucket']}: {row['count']} ({row['representative_cases']})"
                for row in failure_bucket_rows
            )
            + "\n",
            encoding="utf-8",
        )
    else:
        failures_log.write_text("No failure buckets were present in this source run.\n", encoding="utf-8")
    generated.append(failures_log)
    timing_log = paths.log_root / "timing.log"
    timing_summary = _read_json(source_run_dir / "timing" / "timing_summary.json")
    if timing_summary:
        timing_log.write_text(json.dumps(timing_summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    else:
        timing_log.write_text("Timing artifacts are not available in this source run.\n", encoding="utf-8")
    generated.append(timing_log)
    verifier_log = paths.log_root / "verifier.log"
    verifier_log.write_text(_verifier_log_text(verifier_status), encoding="utf-8")
    generated.append(verifier_log)
    return generated


def _write_reports(
    *,
    source_run_dir: Path,
    paths: UserOutputPaths,
    manifest_path: Path,
    summary: dict[str, Any],
    quality_summary: dict[str, Any],
    failure_bucket_rows: list[dict[str, str]],
    verifier_status: dict[str, Any],
) -> list[Path]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    generated = [
        write_summary_report(
            report_root=paths.report_root,
            manifest=manifest,
            summary=summary,
            quality_summary=quality_summary,
        ),
        write_failure_bucket_report(paths.report_root, failure_bucket_rows),
        write_tag_slice_report(source_run_dir / "tag_slices.csv", paths.report_root),
        write_metrics_summary_report(source_run_dir / "metrics", paths.report_root),
        _write_verifier_summary(paths.report_root, verifier_status),
        write_boundary_report(paths.report_root),
    ]
    return generated


def _write_verifier_summary(report_root: Path, verifier_status: dict[str, Any]) -> Path:
    path = report_root / "verifier_summary.md"
    path.write_text(_verifier_summary_text(verifier_status), encoding="utf-8")
    return path


def _export_verifier_artifacts(
    source_run_dir: Path,
    paths: UserOutputPaths,
    verifier_status: dict[str, Any],
) -> tuple[list[Path], list[Path]]:
    copied: list[Path] = []
    generated: list[Path] = []
    source_verifier_dir = source_run_dir / "verifier"
    verifier_dir = paths.result_root / "verifier"
    if source_verifier_dir.exists() and source_verifier_dir.is_dir():
        _copy_tree(source_verifier_dir, verifier_dir)
        copied.append(verifier_dir)
    else:
        verifier_dir.mkdir(parents=True, exist_ok=True)
    path = verifier_dir / "verifier_status.json"
    path.write_text(json.dumps(verifier_status, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    generated.append(path)
    return copied, generated


def _write_failure_buckets_csv(
    path: Path,
    *,
    ledger_rows: list[dict[str, str]],
    failure_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    source_rows = ledger_rows or failure_rows
    grouped: dict[str, dict[str, set[str] | Counter[str]]] = {}
    counts: Counter[str] = Counter()
    for row in source_rows:
        bucket = _text(row.get("failure_bucket"))
        if bucket in {"", "none"}:
            continue
        counts[bucket] += 1
        entry = grouped.setdefault(
            bucket,
            {
                "engines": set(),
                "pools": set(),
                "cases": set(),
            },
        )
        cast_sets = entry
        cast_sets["engines"].add(_text(row.get("engine")) or "unknown")  # type: ignore[union-attr]
        cast_sets["pools"].add(_text(row.get("pool")) or "unknown")  # type: ignore[union-attr]
        cast_sets["cases"].add(_text(row.get("case_id")) or "unknown")  # type: ignore[union-attr]
    rows = []
    for bucket, count in sorted(counts.items()):
        entry = grouped[bucket]
        cases = sorted(entry["cases"])  # type: ignore[arg-type]
        rows.append(
            {
                "failure_bucket": bucket,
                "count": str(count),
                "engines": ";".join(sorted(entry["engines"])),  # type: ignore[arg-type]
                "pools": ";".join(sorted(entry["pools"])),  # type: ignore[arg-type]
                "representative_cases": ";".join(cases[:10]),
                "explanation": _failure_bucket_explanation(bucket),
            }
        )
    _write_csv(path, rows, FAILURE_BUCKET_FIELDS)
    return rows


def _failure_bucket_explanation(bucket: str) -> str:
    explanations = {
        "adapter_failed": "Adapter command failed before candidate SQL was available.",
        "no_candidate_sql": "Adapter completed without a captured candidate SQL artifact.",
        "candidate_preflight_failed": "Candidate SQL failed local preflight checks.",
        "source_execution_failed": "Source/reference SQL failed local execution.",
        "candidate_execution_failed": "Candidate SQL failed local execution.",
        "mismatch": "Checker comparison completed but strict exactness failed.",
        "unsupported_engine": "Manifest or backend marked this row unsupported/fail-closed.",
        "execution_timeout": "Local diagnostic execution timed out.",
    }
    return explanations.get(bucket, "Local diagnostic failure bucket from source ledger.")


def _ensure_roots(paths: UserOutputPaths) -> None:
    for root in [paths.result_root, paths.log_root, paths.report_root]:
        root.mkdir(parents=True, exist_ok=True)


def _copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def _copy_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def _write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _write_aggregated_text_log(path: Path, sources: list[Path]) -> None:
    lines: list[str] = []
    if not sources:
        lines.append("No source log artifacts were available.")
    for source in sources:
        lines.extend([f"## {source.as_posix()}", ""])
        text = source.read_text(encoding="utf-8", errors="replace")
        lines.append(text.rstrip() if text else "(empty)")
        lines.append("")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _read_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    config: dict[str, Any] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or ":" not in stripped:
            continue
        key, raw_value = stripped.split(":", 1)
        config[key.strip()] = _parse_scalar(raw_value.strip())
    return config


def _parse_scalar(value: str) -> Any:
    if value == "":
        return ""
    if value in {"true", "false"}:
        return value == "true"
    if value.startswith('"') and value.endswith('"'):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value.strip('"')
    return value


def _validate_run_id(run_id: str) -> None:
    if not run_id or run_id in {".", ".."}:
        raise ValueError("run_id must be non-empty")
    if "/" in run_id or "\\" in run_id or ".." in Path(run_id).parts:
        raise ValueError("run_id must be a single path component")


def _validate_output_root(output_root: Path, *, repo_root: Path | None) -> None:
    if ".." in output_root.parts:
        raise ValueError("output_root must not contain '..'")
    if not output_root.is_absolute() and output_root.parts[:1] in [("reports",), ("results",)]:
        raise ValueError("output_root must not target top-level reports/ or results/")
    if repo_root is None:
        return
    resolved = (repo_root / output_root).resolve() if not output_root.is_absolute() else output_root.resolve()
    protected_roots = [(repo_root / "reports").resolve(), (repo_root / "results").resolve()]
    for protected in protected_roots:
        if resolved == protected or protected in resolved.parents:
            raise ValueError("output_root must not resolve under top-level reports/ or results/")


def _git_commit(repo_root: Path | None) -> str | None:
    if repo_root is None:
        return None
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            text=True,
            capture_output=True,
            check=False,
        )
    except OSError:
        return None
    if completed.returncode != 0:
        return None
    return completed.stdout.strip() or None


def _workbench_version() -> str | None:
    for package in ["sql-rewrite-bench", "sql_rewrite_bench"]:
        try:
            return metadata.version(package)
        except metadata.PackageNotFoundError:
            continue
    return None


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _bool_like(value: object) -> bool:
    return _text(value).strip().lower() in {"true", "1", "yes"}


def _text(value: object) -> str:
    return "" if value is None else str(value)
