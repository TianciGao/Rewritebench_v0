#!/usr/bin/env python3
"""Adapter that fails after writing a diagnostic to stderr."""

from __future__ import annotations

import sys


if __name__ == "__main__":
    print("intentional adapter failure", file=sys.stderr)
    raise SystemExit(7)
