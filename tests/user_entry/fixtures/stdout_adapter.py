#!/usr/bin/env python3
"""Adapter that emits candidate SQL on stdout."""

from __future__ import annotations

import os


def main() -> int:
    case_id = os.environ["SQLRB_CASE_ID"]
    engine = os.environ["SQLRB_ENGINE"]
    print(f"-- stdout candidate for {case_id} on {engine}")
    print(f"select * from stdout_candidate_for_{case_id.lower()}_{engine};")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
