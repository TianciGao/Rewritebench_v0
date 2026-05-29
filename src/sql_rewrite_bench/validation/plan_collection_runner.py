"""Fail-closed shared plan collection CLI for v2 case packages."""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

from sql_rewrite_bench.validation.engine_query_runner import main as engine_query_main


def main(argv: Sequence[str] | None = None, *, default_case_dir: Path | None = None) -> int:
    return engine_query_main(
        argv,
        default_case_dir=default_case_dir,
        default_mode="plan_collection",
    )


if __name__ == "__main__":  # pragma: no cover - CLI entrypoint
    raise SystemExit(main())
