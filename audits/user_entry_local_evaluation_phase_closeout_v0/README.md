# User-Entry Local Evaluation Phase Closeout v0

## Verdict

Verdict: `complete_with_deferred_items`.

The user-entry local diagnostic harness has completed the planned U0-U7 phase. It now supports a bounded public smoke path, metadata-driven Common-core case selection, adapter capture, candidate preflight, optional PostgreSQL local diagnostics, local result checking, ledger/failure accounting, local quality summaries, tag-aware local slices, readability commands, and an engine router with fail-closed MySQL/Spark stubs.

The harness remains a local diagnostic workbench. It does not compute official metrics, render paper tables, update `reports/` or `results/`, promote retained evidence, compute timing/speedup, or create a global leaderboard.

## Supported Capabilities

- `--smoke` selects the deterministic tiny Common-core subset for the requested engine.
- `--list-cases` lists Common-core membership from `case_sets/common_core_v0/` without scanning `cases/`.
- `--explain-selection` explains selected case-engine rows without invoking adapters when used alone.
- `--show-output-schema` describes local user-run output files and boundaries.
- Adapter capture uses the public adapter contract and writes outputs under `runs/user/{run_name}/`.
- Candidate preflight provides a conservative DB-before text-level readiness and safety check.
- PostgreSQL optional DB/checker diagnostics are implemented as local diagnostics only.
- MySQL and Spark fail closed explicitly; they do not execute SQL or fall back to PostgreSQL.
- `quality_summary.json`, `quality_report.md`, and `tag_slices.csv` are generated for user runs.

## Deferred Work

- Live MySQL execution.
- Live Spark execution.
- Timing diagnostics and speedup.
- Official metrics.
- Paper table rendering.
- Retained-evidence adapter integration.
- Reports/results migration.
- Full paper reproduction CLI.
- SpeedupTransferRate.
- Global leaderboard.

## Recommendation

Pause further user-entry implementation after U0-U7 and return to release-surface metadata work unless a maintainer explicitly authorizes timing protocol design. U8 should not be an implementation task without prior timing protocol approval. If U8 is authorized, it should be design-only and cover exact + timed eligibility, warmup/repetition/timeout/cache policy, raw timing sample ownership, engine version capture, and official-metric boundaries.
