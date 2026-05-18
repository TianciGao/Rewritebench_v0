#!/usr/bin/env python3
"""Adapter that sleeps long enough to exercise timeout handling."""

from __future__ import annotations

import time


if __name__ == "__main__":
    time.sleep(5)
    raise SystemExit(0)
