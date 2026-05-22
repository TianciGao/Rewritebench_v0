#!/usr/bin/env python3
"""Compute non-official local metrics for user-run diagnostics."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from sql_rewrite_bench.local_metrics import compute_and_write_local_metrics  # noqa: E402


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compute local-only diagnostic metrics from runs/user/<run>/ artifacts. "
            "This does not compute official metrics, update reports/results, "
            "promote retained evidence, render paper tables, or create leaderboard output."
        )
    )
    parser.add_argument(
        "--run",
        dest="runs",
        action="append",
        required=True,
        help="Path to a runs/user/<run_name> local diagnostic output directory. May be repeated.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    for raw_run in args.runs:
        run_dir = Path(raw_run)
        if not run_dir.exists():
            raise SystemExit(f"run directory not found: {run_dir}")
        outputs = compute_and_write_local_metrics(run_dir)
        print(f"local metrics written: {outputs.metrics_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
