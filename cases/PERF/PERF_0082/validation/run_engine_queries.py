#!/usr/bin/env python3
from pathlib import Path

from sql_rewrite_bench.validation.engine_query_runner import main


if __name__ == "__main__":
    raise SystemExit(main(default_case_dir=Path(__file__).resolve().parents[1]))
