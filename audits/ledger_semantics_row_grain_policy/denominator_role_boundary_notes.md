# Denominator And Role Boundary Notes

## Track A Same-engine 120 Planned Rows

Track A same-engine denominator remains 40 Common-core cases x 3 engines = 120 planned rows. These rows are represented by `case_sets/common_core_v0/denominator_same_engine_120.csv`.

Same-engine rewrite candidate rows may reference these denominator IDs only when the row represents a case, engine, method role, route, and candidate that belongs to the same-engine Track A scope.

## Controls 360 Scaffold

`case_sets/common_core_v0/controls_360.csv` records planned source, positive, and hard-negative control routes for each case and engine. Controls support package integrity and checker behavior. They are not rewrite method performance rows.

## Hard Negatives

Hard negatives are checker controls. A rejected hard negative is expected evidence that the checker can reject a deliberately incorrect rewrite. It must not be reported as a method-generated failure and must not enter same-engine speedup denominators.

## Verifier Support

Verifier support rows represent external support evidence from SQLSolver, VeriEQL, or similar tools. They can support confidence in equivalence or rejection boundaries, but they are not rewrite-generation baselines and must not enter same-engine speedup denominators.

## Plan Artifacts

Plan artifacts are observability evidence. They can support PlanAvailability or PlanFrontier-style metrics after wording is finalized, but they do not represent candidate correctness or speedup rows by themselves.

## PORT Portability Rows

PORT portability rows carry cross-engine or cross-dialect semantics. They must remain separate from Track A same-engine rewrite rows. Cross-engine executable or consistency rates require separate denominator definitions and must remain bounded to retained evidence and paper protocol.

## No Global Leaderboard

The ledger must preserve route, method role, record type, denominator, timing eligibility, and support-only boundaries. A global leaderboard would collapse incomparable evidence classes.

## Generated, Executed, Exact, Timed

These states must remain separate:

- `generated`: candidate SQL exists or was generated.
- `ready`: candidate reached the downstream gate.
- `executed`: engine execution occurred.
- `exact`: correctness gate passed.
- `timed`: usable timing evidence exists.
- `timing_eligible`: row is eligible for performance interpretation.

Performance interpretation is limited to exact and timed eligible rows after the metrics contract is finalized.
