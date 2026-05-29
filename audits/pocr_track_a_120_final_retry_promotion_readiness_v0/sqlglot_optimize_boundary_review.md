# SQLGlot Optimize Boundary Review

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted. POCR@planned and POCR@candidate remain D039 promotion views. POCR@curated remains deferred until a predeclared curated manifest exists. Micro-average is diagnostic only and not the paper formula. Track A 120 is not a leaderboard.

SQLGlot optimize remains a separate route from SQLGlot no-op. No no-op substitutions were used.

Candidate-present rows by engine:
- mysql: candidate_present=32, no_candidate=8, schema_valid=32, fail_closed=8
- postgres: candidate_present=34, no_candidate=6, schema_valid=33, fail_closed=7
- spark: candidate_present=39, no_candidate=1, schema_valid=38, fail_closed=2

Missing rows are retained fail-closed for POCR@planned and excluded from POCR@candidate where no deterministic candidate exists.

Final diagnostic interpretation: the planned-vs-candidate gap is expected because 15 Track A SQLGlot optimize rows remain no-candidate fail-closed. These values are diagnostic only and not paper-facing metrics.
