# Failure Frontier Policy

PG40 frontier from the canonical rerun:

- exact: `37`
- mismatch: `1`
- mismatch row: `PORT_0013`
- candidate_execution_failed: `2`
- candidate execution failed rows: `PERF_0008`, `LONGTAIL_0011`
- fail-closed rows: `0`

Interpretation:

- These failures are adapted-route behavior diagnostics for the R-Bot GPT-5.4 local diagnostic path.
- They are not hard-negative checker controls.
- They are not verifier failures.
- They are not SQLSolver or VeriEQL outcomes.
- They remain denominator-visible PG40 local diagnostic rows and must not be hidden or silently replaced.

`LONGTAIL_0011` retains the nested-window execution boundary observed in earlier smoke/PG40 work and should remain visible in future R-Bot summaries. `PORT_0013` remains the mismatch row. `PERF_0008` is a live-rerun drift frontier row, while prior `PERF_0013` recovered to exact/timed in the rerun.
