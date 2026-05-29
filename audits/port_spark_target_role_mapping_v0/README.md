# PORT Spark Target Role Mapping Audit

Verdict: `completed_with_failures`

This packet records a local-only PORT Spark target-engine role mapping and controlled diagnostic. Four Common-core PORT cases now have explicit Spark target-reference roles from existing Spark dialect variant assets: `PORT_0003`, `PORT_0004`, `PORT_0005`, and `PORT_0013`. Five Common-core PORT cases remain explicit Spark unsupported/fail-closed rows because no safe Spark target reference is declared: `PORT_0008`, `PORT_0012`, `PORT_0022`, `PORT_0024`, and `PORT_0025`.

The controlled Spark target diagnostic selected 4 rows and executed all declared source-reference and Spark target-candidate sides. Results were exact for `PORT_0003` and `PORT_0005`, and checker mismatches for `PORT_0004` and `PORT_0013`. The two mismatches are not schema/load or execution failures: each side produced one row with matching numeric value by inspection, but MySQL source artifacts serialized numeric values as strings while Spark candidate artifacts serialized numbers as floats. The current checker result records `value_mismatch` with decimal-string equivalence not applied.

Unsupported Spark PORT rows failed closed cleanly: 5 selected, 5 generated candidates, 0 source executions, 0 target executions, 0 checker attempts, all `unsupported_engine` with reason `spark_target_reference_not_declared`.

Behavior preservation checks passed:
- PostgreSQL target controlled route: selected/source/candidate/checker/exact/mismatch rows `5/5/5/5/5/0`.
- MySQL target controlled route: selected/source/candidate/checker/exact/mismatch rows `4/4/4/4/4/0`.
- Non-PORT Spark two-case smoke: selected/source/candidate/checker/exact/mismatch rows `2/2/2/2/2/0`.

Boundary:
- Local diagnostic only.
- No official metrics computed.
- No timing or speedup computed.
- No reports/results updated.
- No denominator, paper result, case membership, or raw retained evidence changed.
- No global leaderboard created.
- No release tag or export branch created.

Recommended next safe action: run a narrow audit/fix task for MySQL-source to Spark-target cross-dialect numeric normalization on `PORT_0004` and `PORT_0013`, with explicit PERF/CONS/LONGTAIL same-engine regression checks before any broader Spark PORT trial.
