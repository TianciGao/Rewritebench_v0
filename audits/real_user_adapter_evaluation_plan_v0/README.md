# Real User-Adapter Evaluation Plan v0

Verdict: `ready_for_bounded_local_diagnostic_trial`

This packet is an audit/design-only plan for a first real user-adapter local diagnostic evaluation after the tri-engine user-entry local diagnostic closeout. No real user method was run for this task.

## Boundary

- Local diagnostic only.
- User method output is candidate SQL.
- Adapter results are not official metrics.
- Timing and speedup remain absent.
- Reports/results must not be updated.
- Paper tables must not be rendered.
- Retained evidence must not be promoted.
- No leaderboard, release export, release branch, or release tag may be created.

## Baseline

- PostgreSQL local diagnostic backend: live; latest no-op snapshot exact/mismatch `35/0`, with 5 PORT no-op target-candidate failures documented as adapter limitations.
- MySQL local diagnostic backend: live; latest no-op snapshot exact/mismatch `36/0`, with 4 PORT no-op target-candidate failures documented as adapter limitations.
- Spark local diagnostic backend: PySpark local mode available; same-engine Spark snapshot exact `31/31`; controlled Spark target route exact `4/4`; 5 Spark PORT rows explicit fail-closed.
- PORT controlled routes: PostgreSQL target `5/5`, MySQL target `4/4`, Spark target `4/4`, Spark unsupported `5` fail-closed.

## Recommended Evaluation Shape

The first real adapter evaluation should be a staged local diagnostic, not a full benchmark claim:

1. Run a non-DB adapter-capture dry-run on the proposed smoke rows to confirm the command, environment, candidate capture, stdout/stderr artifacts, and timeout behavior.
2. Run a DB/checker-enabled PostgreSQL bounded smoke.
3. Run a DB/checker-enabled MySQL bounded smoke.
4. Run a DB/checker-enabled Spark same-engine bounded smoke only if the local Spark readiness check passes.
5. Run any PORT cross-dialect real-adapter rows separately from controlled target-reference diagnostics and label them as real user-adapter candidate rows, not controlled target-reference rows.

Controlled target-reference adapters remain diagnostic controls. They should not be mixed into real user-adapter exact/mismatch summaries.

## Next Safe Action

Authorize a bounded real user-adapter smoke using an explicit adapter command, explicit case lists, local `runs/user/{run_name}/` output, DB/checker enabled only where the local engine readiness check passes, and no timing, official metrics, reports/results, retained-evidence promotion, leaderboard, or release/export/tag work.
