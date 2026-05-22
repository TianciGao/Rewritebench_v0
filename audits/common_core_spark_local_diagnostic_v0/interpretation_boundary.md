# Interpretation Boundary

This Spark run is local diagnostic only.

It is not official metrics.

It is not paper results.

It is not timing or speedup.

It is not reports/results migration.

It is not retained evidence promotion.

It is not a leaderboard.

It does not change Common-core membership or denominator.

It does not change paper results, case membership, case packages, SQL files, schema files, checker files, validation files, manifests, inventory, raw retained evidence, release tags, or export branches.

The no-op adapter emits source-like SQL. Exact rows only show that local Spark source/candidate execution and the local checker agreed for those rows in this diagnostic run.

The `unsupported_engine` PORT rows are explicit fail-closed local diagnostic rows. They are not hidden failures and are not official paper results.

The `CONS_0011` mismatch is a local checker/normalization row-order finding. It is not a timing result, speedup result, paper result, or metric input.
