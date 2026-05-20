"""Fail-closed shared engine query runner CLI for v2 case packages.

This module validates invocation shape and manifest paths only. It does not
open database connections, execute SQL, collect plans, write reports/results,
compute metrics, or create leaderboard artifacts.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from sql_rewrite_bench.case_package_v2_resolver import load_yaml_file


ENGINE_CHOICES = ("postgres", "mysql", "spark", "all")
TARGET_CHOICES = ("source", "positive", "negative", "all")
MODE_CHOICES = ("validation", "plan_collection")


def _repo_root_from_case_dir(case_dir: Path) -> Path:
    try:
        return case_dir.resolve().parents[2]
    except IndexError as exc:
        raise ValueError(f"cannot infer repository root from case directory: {case_dir}") from exc


def _manifest_schema_profile(manifest: dict[str, object]) -> str | None:
    schema = manifest.get("schema")
    if isinstance(schema, dict) and isinstance(schema.get("external_profile"), str):
        return schema["external_profile"]
    schema_ref = manifest.get("schema_ref")
    if isinstance(schema_ref, dict) and isinstance(schema_ref.get("profile"), str):
        return schema_ref["profile"]
    return None


def _validate_case_inputs(case_dir: Path, out_dir: Path | None) -> list[str]:
    errors: list[str] = []
    manifest_path = case_dir / "manifest.yaml"
    if not manifest_path.exists():
        return [f"manifest not found: {manifest_path}"]

    try:
        manifest = load_yaml_file(manifest_path)
    except Exception as exc:
        return [f"manifest could not be loaded: {exc}"]

    for rel in ("sql/source.sql", "sql/pos_01.sql", "sql/neg_01.sql"):
        if not (case_dir / rel).exists():
            errors.append(f"required SQL path missing: {rel}")

    profile = _manifest_schema_profile(manifest)
    if not profile:
        errors.append("schema.external_profile or schema_ref.profile is required")
    else:
        repo_root = _repo_root_from_case_dir(case_dir)
        profile_path = (repo_root / profile).resolve()
        if not profile_path.exists():
            errors.append(f"external schema profile missing: {profile}")

    if out_dir is None:
        errors.append("--out is required; use an explicit output directory such as runs/user/<run_id>/")
    else:
        resolved_out = out_dir.resolve()
        case_runs = (case_dir / "runs").resolve()
        if resolved_out == case_runs or case_runs in resolved_out.parents:
            errors.append("case-local runs/ is not an allowed validation output root")
    return errors


def build_parser(default_mode: str = "validation") -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fail-closed v2 engine query runner entrypoint.",
    )
    parser.add_argument("--case", type=Path, help="Case package directory. Defaults to the shim case.")
    parser.add_argument("--mode", choices=MODE_CHOICES, default=default_mode)
    parser.add_argument("--engine", choices=ENGINE_CHOICES, default="all")
    parser.add_argument("--target", choices=TARGET_CHOICES, default="all")
    parser.add_argument("--out", type=Path, help="Explicit output directory outside case-local runs/.")
    return parser


def main(
    argv: Sequence[str] | None = None,
    *,
    default_case_dir: Path | None = None,
    default_mode: str = "validation",
) -> int:
    parser = build_parser(default_mode=default_mode)
    args = parser.parse_args(argv)
    case_dir = (args.case or default_case_dir)
    if case_dir is None:
        parser.error("--case is required when no default case directory is provided")
    case_dir = case_dir.resolve()

    errors = _validate_case_inputs(case_dir, args.out)
    if errors:
        for error in errors:
            print(f"v2 validation runner refused execution: {error}", file=sys.stderr)
        return 2

    print(
        "shared v2 validation runner not implemented; "
        "DB/checker execution was not run.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":  # pragma: no cover - CLI entrypoint
    raise SystemExit(main())
