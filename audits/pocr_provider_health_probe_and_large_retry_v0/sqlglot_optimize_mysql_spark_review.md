# SQLGlot Optimize MySQL/Spark Review

SQLGlot optimize MySQL:
- candidate-bound rows: 32
- schema-valid rows: 30
- fail-closed rows: 10
- supported atoms: 26

SQLGlot optimize Spark:
- candidate-bound rows: 39
- schema-valid rows: 30
- fail-closed rows: 10
- supported atoms: 29

The planned/candidate gap remains expected because SQLGlot optimize has missing candidate rows that are retained fail-closed for POCR@planned. No SQLGlot no-op substitutions were used. The route is safe to keep as a diagnostic route with explicit fail-closed missing rows, but it is not ready for paper-facing promotion without resolving remaining fail-closed rows or accepting a documented fail-closed boundary.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted. No blind full retry is run. POCR@planned and POCR@candidate remain D039 promotion views. POCR@curated remains deferred until a predeclared curated manifest exists. Track A 120 is not a leaderboard.
