# Metrics Reconciliation: SQLGlot/Calcite User Reproduction

This packet reconciles the new D035-style user-side reproduction outputs against prior canonical/local diagnostic evidence for SQLGlot no-op, SQLGlot optimize schema-aware, and Calcite HEP fail-closed Track A 120 routes.

No rerun, DB/checker/timing execution, baseline run, live API call, POCR annotation, POCR Stage B validation, official metric promotion, paper table update, or leaderboard was performed.

## Findings

- SQLGlot no-op counts match prior canonical evidence exactly: planned 120, generated 115, executable 107, exact 97, timed 97. GM differs: prior 0.9798350077258852 vs new 1.0580321436582178.
- SQLGlot optimize schema-aware counts match prior canonical evidence exactly: planned 120, generated 105, executable 91, exact 66, timed 66. GM differs: prior 1.020315612310745 vs new 0.9893206632563172.
- For both SQLGlot routes, exact+timed row sets are identical. Speedup arrays differ because runtimes were freshly measured, and the new nightly reproduction used two measured repetitions while prior canonical runs used five.
- Calcite HEP does not reconcile as a replacement: prior canonical evidence had generated 99, exact 81, timed 80, GM 0.9852158585899714; the new reproduction was blocked by missing Calcite runtime and generated 0 candidates.
- Failure bucket vocabulary is compatible. Bucket counts match for both SQLGlot routes and differ for Calcite because of the blocked runtime environment.

The new user-side reproduction can be accepted as local diagnostic reproduction evidence with boundary for SQLGlot routes. It cannot update paper-facing tables without separate authorization, and the Calcite new output should be treated as blocked-runtime smoke only.
