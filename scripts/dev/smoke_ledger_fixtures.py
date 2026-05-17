#!/usr/bin/env python3
"""Developer-only smoke wrapper for synthetic ledger fixture validation.

This script is intentionally a thin subprocess wrapper around
``scripts/dev/validate_ledger_fixtures.py``. It preserves the validator's
fixture-only boundary: no production retained evidence is parsed, no adapters
are implemented, and no metrics are computed.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


DEFAULT_FIXTURES_DIR = Path("audits/ledger_schema_validation_fixtures")
DEFAULT_EXTRA_FIXTURES = Path(
    "audits/ledger_fixture_validator_hardening/fixture_hardening_extra_rows.csv"
)
DEFAULT_EXTRA_EXPECTED = Path(
    "audits/ledger_fixture_validator_hardening/fixture_hardening_expected_results.csv"
)
DEFAULT_OUT_DIR = Path("audits/ledger_fixture_dev_smoke")

VALIDATOR_SCRIPT = Path("scripts/dev/validate_ledger_fixtures.py")
VALIDATOR_RESULTS = "ledger_fixture_hardening_validation_results.csv"
VALIDATOR_SUMMARY = "ledger_fixture_hardening_summary.json"
VALIDATOR_REPORT = "ledger_fixture_validator_hardening_report.md"
SMOKE_REPORT = "ledger_fixture_dev_smoke_report.md"
SMOKE_SUMMARY = "ledger_fixture_dev_smoke_summary.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run developer smoke validation for synthetic ledger fixtures."
    )
    parser.add_argument("--fixtures-dir", type=Path, default=DEFAULT_FIXTURES_DIR)
    parser.add_argument("--extra-fixtures", type=Path, default=DEFAULT_EXTRA_FIXTURES)
    parser.add_argument("--extra-expected", type=Path, default=DEFAULT_EXTRA_EXPECTED)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument(
        "--python",
        default=sys.executable,
        help="Python executable used to invoke the fixture validator.",
    )
    return parser.parse_args()


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def build_command(args: argparse.Namespace) -> list[str]:
    command = [
        str(args.python),
        str(VALIDATOR_SCRIPT),
        "--fixtures-dir",
        str(args.fixtures_dir),
        "--out-dir",
        str(args.out_dir),
    ]
    if args.extra_fixtures and args.extra_expected:
        command.extend(
            [
                "--extra-fixtures",
                str(args.extra_fixtures),
                "--extra-expected",
                str(args.extra_expected),
            ]
        )
    return command


def load_summary(summary_path: Path) -> dict[str, object]:
    if not summary_path.exists():
        return {}
    with summary_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def smoke_summary_payload(
    validator_returncode: int, validator_summary: dict[str, object]
) -> dict[str, object]:
    return {
        "smoke_passed": validator_returncode == 0,
        "validator_returncode": validator_returncode,
        "total_fixture_rows_checked": validator_summary.get("total_fixture_rows_checked", 0),
        "expected_valid_passed": validator_summary.get("expected_valid_passed", 0),
        "expected_invalid_failed_as_expected": validator_summary.get(
            "expected_invalid_failed_as_expected", 0
        ),
        "unexpected_pass_count": validator_summary.get("unexpected_pass_count", 0),
        "unexpected_fail_count": validator_summary.get("unexpected_fail_count", 0),
        "production_retained_evidence_parsed": False,
        "adapter_implemented": False,
        "metrics_computed": False,
        "reports_changed": False,
        "results_changed": False,
        "denominator_changed": False,
        "paper_results_changed": False,
        "raw_legacy_evidence_changed": False,
    }


def write_smoke_report(
    path: Path,
    command: list[str],
    args: argparse.Namespace,
    validator_returncode: int,
    validator_summary: dict[str, object],
    smoke_summary: dict[str, object],
) -> None:
    files_read = [
        args.fixtures_dir / "fixture_all_record_types.csv",
        args.fixtures_dir / "fixture_expected_validation_results.csv",
        args.fixtures_dir / "record_type_required_fields_matrix.csv",
        args.fixtures_dir / "allowed_status_values.csv",
        args.fixtures_dir / "fixture_denominator_join_examples.csv",
        args.extra_fixtures,
        args.extra_expected,
        Path("case_sets/common_core_v0/cases.csv"),
        Path("case_sets/common_core_v0/denominator_same_engine_120.csv"),
        Path("case_sets/common_core_v0/controls_360.csv"),
    ]
    files_written = [
        args.out_dir / VALIDATOR_RESULTS,
        args.out_dir / VALIDATOR_SUMMARY,
        args.out_dir / VALIDATOR_REPORT,
        args.out_dir / SMOKE_REPORT,
        args.out_dir / SMOKE_SUMMARY,
    ]
    lines = [
        "# Ledger Fixture Dev Smoke Report",
        "",
        "## Command Run",
        "",
        "```bash",
        " ".join(command),
        "```",
        "",
        "## Files Read",
        "",
    ]
    lines.extend(f"- `{path}`" for path in files_read)
    lines.extend(["", "## Files Written", ""])
    lines.extend(f"- `{path}`" for path in files_written)
    lines.extend(
        [
            "",
            "## Validation Summary",
            "",
            f"- Smoke passed: {str(smoke_summary['smoke_passed']).lower()}",
            f"- Validator return code: {validator_returncode}",
            "- Total fixture rows checked: "
            f"{validator_summary.get('total_fixture_rows_checked', 0)}",
            f"- Expected-valid rows passed: {validator_summary.get('expected_valid_passed', 0)}",
            "- Expected-invalid rows failed as expected: "
            f"{validator_summary.get('expected_invalid_failed_as_expected', 0)}",
            f"- Unexpected pass count: {validator_summary.get('unexpected_pass_count', 0)}",
            f"- Unexpected fail count: {validator_summary.get('unexpected_fail_count', 0)}",
            "- Production retained evidence parsed: false",
            "- Metrics computed: false",
            "- Adapter implemented: false",
            "",
            "## Explicit Non-Goals",
            "",
            "- No production retained evidence was parsed.",
            "- No retained-evidence adapter was implemented.",
            "- No metrics were computed.",
            "- No reports/results were migrated or mutated.",
            "- No DB engines, LLM calls, timing workloads, or paper table renderers were run.",
            "- No denominator values, paper results, case membership, case packages,",
            "  or raw legacy evidence were changed.",
            "",
            "## Next Safe Action",
            "",
            "Use this developer smoke entrypoint for fixture-only validation before",
            "any separately authorized production ledger validation work. Do not",
            "parse production retained evidence, implement adapters, compute metrics,",
            "or render paper tables without explicit authorization.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def print_terminal_summary(summary: dict[str, object]) -> None:
    print(f"fixture rows checked: {summary.get('total_fixture_rows_checked', 0)}")
    print(f"expected-valid passed: {summary.get('expected_valid_passed', 0)}")
    print(
        "expected-invalid failed as expected: "
        f"{summary.get('expected_invalid_failed_as_expected', 0)}"
    )
    print(f"unexpected pass/fail: {summary.get('unexpected_pass_count', 0)}/"
          f"{summary.get('unexpected_fail_count', 0)}")
    print(
        "production_retained_evidence_parsed: "
        f"{summary.get('production_retained_evidence_parsed', False)}"
    )
    print(f"metrics_computed: {summary.get('metrics_computed', False)}")
    print(f"adapter_implemented: {summary.get('adapter_implemented', False)}")


def main() -> int:
    args = parse_args()
    root = repo_root()
    out_dir = root / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    command = build_command(args)
    completed = subprocess.run(command, cwd=root, check=False)

    summary_path = out_dir / VALIDATOR_SUMMARY
    validator_summary = load_summary(summary_path)
    smoke_summary = smoke_summary_payload(completed.returncode, validator_summary)

    smoke_summary_path = out_dir / SMOKE_SUMMARY
    smoke_summary_path.write_text(
        json.dumps(smoke_summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_smoke_report(
        out_dir / SMOKE_REPORT,
        command,
        args,
        completed.returncode,
        validator_summary,
        smoke_summary,
    )

    print_terminal_summary(validator_summary)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
