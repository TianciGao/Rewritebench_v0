# Rerun Versus Prior PG40 Review

Prior audit path: `audits/rbot_gpt54_pg40_bounded_local_diagnostic_v0/`.

Prior evaluate-layer facts:

- selected: `40`
- generated: `40`
- executable: `38`
- exact: `37`
- timed: `33`
- mismatch: `1`, `PORT_0013`
- execution failed: `2`, `PERF_0013` and `LONGTAIL_0011`
- prior canonical local_metrics outputs: none; the aggregate command shape failed before outputs.

Current rerun facts from run artifacts and local_metrics outputs:

- selected: `40`
- generated: `40`
- executable: `38`
- exact: `37`
- timed: `33`
- mismatch: `1`
- candidate execution failed: `2`

Previous and current frontier rows:

- `PORT_0013`: failure_bucket=`mismatch`, candidate_execution=`candidate_execution_success`, checker=`checker_mismatch`, exact_status=`mismatch`, timing_status=`not_eligible`
- `PERF_0013`: failure_bucket=`none`, candidate_execution=`candidate_execution_success`, checker=`checker_success`, exact_status=`exact`, timing_status=`timed`
- `LONGTAIL_0011`: failure_bucket=`candidate_execution_failed`, candidate_execution=`candidate_execution_failed`, checker=`checker_not_enabled`, exact_status=`not_exact_due_to_execution_failure`, timing_status=`not_eligible`
- `PERF_0008`: failure_bucket=`candidate_execution_failed`, candidate_execution=`candidate_execution_failed`, checker=`checker_not_enabled`, exact_status=`not_exact_due_to_execution_failure`, timing_status=`not_eligible`

Live reruns may differ because GPT-5.4 generation can drift. In this rerun, `PERF_0013` recovered to exact/timed, while `PERF_0008` became a candidate execution failure. `PORT_0013` remains the mismatch row and `LONGTAIL_0011` remains a candidate execution failure.

If accepted, the current rerun is the canonical PG40 local diagnostic metrics source because it was processed by single-run `local_metrics.py` output generation.
