# SQLGlot Optimize Boundary Review

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted. POCR@planned and POCR@candidate remain D039 promotion views. POCR@curated remains deferred until a predeclared curated manifest exists. Track A 120 is not a leaderboard.

SQLGlot optimize remains a schema-aware candidate route separate from SQLGlot no-op. SQLGlot no-op candidates were not used as optimize substitutes.

Missing optimize rows count: 15.

Missing rows by engine:
- mysql: 8
- postgres: 6
- spark: 1

Missing row cause: no deterministic SQLGlot optimize candidate was present for these route-engine-case rows. They remain `skipped_no_candidate` fail-closed rows.

Denominator interpretation:
- POCR@planned keeps the missing rows in the planned denominator with zero contribution.
- POCR@candidate excludes rows where no deterministic candidate is bound.
- The planned/candidate gap is therefore expected and denominator-aware, not evidence of a no-op substitution.

Promotion boundary wording: SQLGlot optimize may enter the promotion review packet only with an explicit missing-candidate boundary: 15 Track A 120 optimize rows are no-candidate fail-closed and no no-op substitutes were used.
