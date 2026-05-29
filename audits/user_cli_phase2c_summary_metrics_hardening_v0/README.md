# user_cli_phase2c_summary_metrics_hardening_v0

Verdict: completed.

This task hardens the existing `sqlrb user` summary/report commands before verifier integration.

Commands hardened:

- `sqlrb user summarize`
- `sqlrb user compute-local-metrics`
- `sqlrb user show-boundary`

Summary behavior:

- `summarize` now reads the D035 output contract roots under `output/results/<run_id>/`, `output/logs/<run_id>/`, and `output/reports/<run_id>/`.
- It prints a composite local diagnostic summary with run summary, failure buckets, tag slices, local metrics, verifier status, and boundary sections.
- If optional reports are missing, it prints explicit `N.A.` messages instead of failing silently.

Local metrics behavior:

- `compute-local-metrics` remains local-only and delegates to the existing non-official local metrics calculator.
- It reports the user-facing metrics output path and `metrics_summary.md` path.
- It states that Semantic Equivalence Rate is `N.A.` without verifier evidence and POCR remains deferred.

Boundary behavior:

- `show-boundary` now explicitly states not official metrics, not paper results, not retained evidence, and not leaderboard input.
- It also states Semantic Equivalence Rate is `N.A.` until formal VeriEQL or SQLSolver evidence exists and POCR is deferred.

No VeriEQL or SQLSolver integration was implemented. No full Common-core run, SQLGlot optimize run, timing collection, official metrics, top-level reports/results update, retained-evidence promotion, paper rendering, or leaderboard output occurred.
