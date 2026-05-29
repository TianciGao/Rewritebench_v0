# Recommended Reorganization Plan

## 1. Preserve the Working Non-DB Path

Keep `sql_rewrite_bench.user_run` and `scripts/user/run_user_benchmark.py` as the stable public user-entry path for local adapter capture. The current path resolves Common-core metadata, finds `sql/source.sql`, invokes adapters, and writes local diagnostics under `runs/user/<run_id>/`.

## 2. Repair Optional DB/Checker Diagnostics

Update optional PostgreSQL execution to resolve executable schema assets through the v2 case-package contract:

- Load the case manifest.
- Resolve `schema.external_profile`.
- Read the external schema profile engine section.
- Use the external `postgres/ddl.sql` and `postgres/load.sql` paths when engine is `postgres`.
- Fail closed if the manifest or external schema profile is missing, malformed, or lacks a supported engine path.
- Keep outputs under `runs/user/<run_id>/`.
- Keep all DB/checker output local diagnostic only, not retained evidence and not official metrics.

## 3. Align Docs and CLI Help

Split the documented user surface into clear layers:

- Supported public smoke: non-DB dry-run / adapter capture.
- Experimental local diagnostics: DB/checker mode after external-schema repair.
- Deferred: full paper reproduction, official metrics, paper rendering, retained-evidence parsing, reports/results updates, and leaderboard output.

## 4. Add a Public Smoke Convenience

Avoid requiring users to create a temporary case-list file for the smallest smoke. Recommended options:

- Add a committed public smoke case-list under a docs/examples or scripts/examples path.
- Move the deterministic dummy adapter out of `tests/` into a public examples namespace.
- Alternatively add a `--limit` or `--smoke` option that selects a deterministic tiny Common-core subset.

## 5. Keep Release Boundaries Explicit

Any repair task should continue to state:

- No denominator changes.
- No case membership changes.
- No paper result changes.
- No raw legacy evidence changes.
- No official metrics.
- No paper tables.
- No global leaderboard.
