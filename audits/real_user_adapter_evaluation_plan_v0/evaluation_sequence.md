# Recommended Evaluation Sequence

## Step 1: Preflight Readiness

- Confirm clean worktree or only ignored local outputs.
- Source local engine environment as needed.
- Run `PYTHONPATH=src python scripts/dev/check_local_engine_env.py`.
- Record readiness without printing secrets.

## Step 2: Adapter-Capture Dry Run

Use the proposed smoke rows with DB execution disabled. This isolates command invocation, environment variables, workspace writes, stdout/stderr capture, and candidate SQL capture.

Recommended starting rows:

- PostgreSQL dry run: `PERF_0006`, `CONS_0005`, `PORT_0004`.
- MySQL dry run: `PERF_0006`, `CONS_0005`, `PORT_0003`.
- Spark dry run: `PERF_0006` if the adapter supports Spark-target SQL generation.

## Step 3: DB/Checker Smoke

Run small DB/checker-enabled engine-specific smokes only after dry-run capture succeeds:

- PostgreSQL: `PERF_0006`, `CONS_0005`, `PORT_0004`.
- MySQL: `PERF_0006`, `CONS_0005`, `PORT_0003`.
- Spark same-engine: `PERF_0006`, `CONS_0005` only if Spark readiness passes.

## Step 4: Controlled Route Preservation

If cross-dialect real-adapter rows are interpreted, preserve the controlled route baselines separately:

- MySQL-source to PostgreSQL-target controlled route exact `5/5`.
- PostgreSQL-source to MySQL-target controlled route exact `4/4`.
- Manifest-declared Spark target controlled route exact `4/4`.
- Spark unsupported roles remain 5 explicit fail-closed.

Do not combine controlled target-reference rows with real user-adapter rows in one exact/mismatch summary.

## Step 5: Bounded Expansion

Only after smoke triage is clean, expand one engine at a time with an explicit case list. Record adapter failures, preflight failures, source execution failures, candidate execution failures, checker mismatches, source-like rows, unsupported rows, and exact rows separately.

Do not compute official metrics, timing, speedup, paper results, reports/results tables, retained-evidence promotion, leaderboard output, release exports, or tags.
