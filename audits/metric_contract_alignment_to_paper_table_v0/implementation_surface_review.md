# Implementation Surface Review

Reviewed surfaces:

- `repository_spec/metrics_contract_v1.md`
- `src/sql_rewrite_bench/local_metrics.py`
- `src/sql_rewrite_bench/tag_slices.py`
- `src/sql_rewrite_bench/verifier_support/`
- `audits/direct_llm_original_track_a_120_canonical_user_rerun_v0/`
- `audits/direct_llm_original_non_exact_frontier_review_v0/`

Local metrics implementation facts:

- Writes `local_metrics_summary.json`, `local_metrics_by_engine.csv`, `local_metrics_by_pool.csv`, `local_timing_speedup_rows.csv`, and `local_metrics_boundary.md`.
- Emits local-only boundary flags and prohibits official metric, paper result, retained-evidence, and leaderboard interpretation.
- Implements `generation_rate = candidate_generated / selected`.
- Implements `execution_coverage_rate = candidate_executable / selected`.
- Implements `result_consistency_rate = exact / selected`.
- Implements GM speedup and speedup percentiles over strict exact + timed rows.
- Defers SER, POCR, and cross-engine GM speedup when required evidence is missing.

Verifier-support implementation facts:

- Validates verifier pairs and verdict records with local-only boundary flags.
- Normalizes verifier outcomes into equivalent, non-equivalent, unknown, timeout, unsupported, syntax error, not implemented, out of memory, tool error, and not attempted.
- Computes SER only from equivalent and non-equivalent verifier outcomes.
- Records unknown/timeout/unsupported/not-implemented/tool-error/not-attempted counts separately.
- Records `result_checker_exactness_used=false`.

Tag-slice implementation facts:

- Emits retained manifest taxonomy slices as local diagnostic counts.
- Explicitly marks tag slices as not official metrics and not leaderboard input.
- Provides useful support counts but no primary metric denominator.
