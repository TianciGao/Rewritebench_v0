# Calcite HEP Baseline Layout Contract

Task: `calcite_hep_baseline_layout_contract_v0`

Verdict: layout corrected to D035.

The Calcite HEP fail-closed adapter is route-specific baseline code, not reusable core implementation. It was moved from `src/sql_rewrite_bench/calcite_hep_fail_closed_adapter.py` to `baselines/calcite_hep_fail_closed/adapter.py`.

No compatibility shim was left under `src/sql_rewrite_bench/`. The only core-source change is route identity recognition in `src/sql_rewrite_bench/local_timing.py`, so D035 user-output manifests still resolve `route_id=calcite_hep_fail_closed` and `method_id=calcite_hep_fail_closed`.

Tiny validation with the new path selected `CONS_0036`, `CONS_0037`, and `PERF_0006`; all three rows remained fail-closed with `no_candidate_sql`, and D035 output was written only under `/tmp/sqlrb_calcite_hep_baseline_layout_contract_v0/`.

This task did not run full Common-core, all 120 Track-A rows, MySQL/Spark, LLM baselines, verifier passes, official metrics, Semantic Equivalence Rate, timing/speedup, reports/results updates, retained-evidence promotion, leaderboard output, denominator changes, case membership changes, paper-result changes, or Calcite vendoring.
