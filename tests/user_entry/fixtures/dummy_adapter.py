#!/usr/bin/env python3
"""Dummy user adapter for non-DB user-run MVP tests."""

from __future__ import annotations

import os
from pathlib import Path


def main() -> int:
    case_id = os.environ["SQLRB_CASE_ID"]
    engine = os.environ["SQLRB_ENGINE"]
    candidate_path = Path(os.environ["SQLRB_CANDIDATE_SQL_PATH"])
    candidate_path.parent.mkdir(parents=True, exist_ok=True)
    candidate_path.write_text(
        f"-- dummy candidate for {case_id} on {engine}\n"
        f"select * from source_query_for_{case_id.lower()}_{engine};\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
