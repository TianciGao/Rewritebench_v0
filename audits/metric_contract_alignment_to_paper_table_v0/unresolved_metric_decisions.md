# Unresolved Metric Decisions

## Result Consistency Denominator

Mismatch:

- D032/latest paper table: Result Consistency Rate is `|X_r| / N_S`.
- D033/local metrics v0: `exact / selected`.
- `repository_spec/metrics_contract_v1.md`: `result_consistent_cases / executed_candidate_cases`.
- `src/sql_rewrite_bench/local_metrics.py`: `exact / selected`.

Decision needed: update or supersede the repository metric contract before any paper-facing result rendering so it no longer conflicts with the latest paper table and D033 local diagnostic formula.

## POCR vs Attribution Coverage

Mismatch:

- D032/latest paper table: Positive Operation Coverage Rate.
- `metrics_contract_v1.md`: Attribution Coverage.
- `local_metrics.py`: `positive_operation_coverage_rate` remains deferred with `external_skill_adapter_pending`.
- `tag_slices.py`: retained taxonomy diagnostics only; it does not define operation atoms.

Decision needed: define POCR operation atom schema and external skill-adapter contract, or explicitly keep Attribution Coverage as a separate non-Table-6 concept. Do not infer POCR from tags or SQL text.

## Cross-Engine GM Speedup Ratio vs Speedup Retention

Mismatch:

- D032/latest paper table: Cross-Engine GM Speedup Ratio over target-engine result-consistent timed rows.
- `metrics_contract_v1.md`: Speedup Retention over paired source-engine and target-engine timing evidence.
- `local_metrics.py`: `cross_engine_gm_speedup_ratio` is `N.A.` until target-engine paired timing exists.

Decision needed: decide whether the public paper-facing name and formula should be Cross-Engine GM Speedup Ratio, Speedup Retention, or both with one demoted to diagnostic/support status.

## Paper-Facing SER Promotion Policy

Mismatch/gap:

- SER policy is conceptually aligned around formal verifier evidence.
- Current verifier support status vocabulary is `computed` or `not_applicable`.
- Required policy vocabulary is `computed`, `coverage_limited`, or `N.A.`.
- Pair construction eligibility for source-vs-candidate rows must be enforced outside the pair-schema validator.

Decision needed: define the paper-facing promotion gate for SER, including verifier tool approval, exact-row pair construction, coverage reporting, status vocabulary, and treatment of routes with no verifier support.
