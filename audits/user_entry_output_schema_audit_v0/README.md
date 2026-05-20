# User-Entry Output Schema Audit v0

## Purpose

This U1 audit reviews the current user-entry output schema, ledger fields, status values, summary/report outputs, and gaps against the local evaluation funnel defined in `project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md`.

This is an audit/design packet only. It does not implement candidate preflight, module splitting, quality reports, tag slices, timing diagnostics, official metrics, paper rendering, retained-evidence integration, reports/results migration, or a reproduction CLI.

## Smoke Inputs

The audit used the public smoke subset selected by `--smoke`:

- `PERF_0006` on `postgres`
- `CONS_0005` on `postgres`

Smoke outputs were generated under:

- `runs/user/u1_schema_dry_run`
- `runs/user/u1_schema_dummy_adapter`

Those local outputs were inspected for schema inventory and then removed before commit.

## Verdict

Verdict: `ready_with_gaps` for U2.

The current schema is adequate for a U2 module split/design task because selection, adapter invocation, candidate capture, local output-root policy, basic ledger rows, failure rows, summary JSON, and report sections already exist.

The schema is not yet complete for the full local evaluation target because candidate preflight fields, explicit DB-attempt fields, source/candidate executable booleans, checker-attempt fields, source-like/nontrivial flags, tag slice fields, quality summary fields, and timing diagnostics are missing or only implicit.

## Local Diagnostic Boundary

All observed user-run outputs are local diagnostics only. They are not official metrics, not paper tables, not retained evidence, not reports/results updates, and not leaderboard rows.

## Key Findings

- Current `ledger.csv` has 35 fields.
- Current `selected_cases.csv` has 8 fields.
- Current `failures.csv` has 8 fields.
- Current `summary.json` has 27 keys.
- Current `report.md` has 10 top-level sections in the smoke runs.
- Existing fields cover selected, adapter-invoked, candidate-generated, non-DB execution/checker status, local exact status, failure bucket, and boundary flags.
- Missing fields block U3/U4/U5 work more than U2: candidate preflight, source-like/no-op classification, denominator-aware quality summaries, tag slices, and timing diagnostics.

## Next Safe Action

Proceed to U2: module split design for resolver, adapter runner, and ledger writer. Keep U2 design-only unless separately authorized for minimal implementation. Do not compute official metrics, render paper tables, update reports/results, promote retained evidence, or create a leaderboard.
