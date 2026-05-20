#!/usr/bin/env python3
"""Public no-op adapter example for SQL-RewriteBench user-entry smoke runs.

The adapter copies the source SQL into the candidate path supplied by the
runner. It performs no database execution, checking, scoring, or metric work.
"""

from __future__ import annotations

import os
from pathlib import Path


def main() -> int:
    source_path = Path(os.environ["SQLRB_SOURCE_SQL_PATH"])
    candidate_path = Path(os.environ["SQLRB_CANDIDATE_SQL_PATH"])
    candidate_path.parent.mkdir(parents=True, exist_ok=True)
    candidate_path.write_text(source_path.read_text(encoding="utf-8"), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
