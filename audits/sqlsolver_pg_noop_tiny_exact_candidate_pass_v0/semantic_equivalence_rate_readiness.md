# Semantic Equivalence Rate Readiness

SQLSolver is ready for a bounded one-baseline exact-candidate subset attempt from a tooling perspective:

- External SQLSolver JAR is available.
- The wrapper executed real exact candidate rows.
- Identity sanity gates worked as intended.
- SQLSolver produced clean `EQ` evidence for `CONS_0036`, `CONS_0037`, and `LONGTAIL_0023`.
- SQLSolver exposed `UNKNOWN` identity behavior for `PORT_0003` and `PORT_0005`, keeping those rows out of the corrected denominator.

Paper-facing Semantic Equivalence Rate remains blocked:

- The pass covered only five selected SQLGlot-noop PostgreSQL rows.
- `UNKNOWN` identity failures remain visible.
- No full baseline or Common-core verifier pass was run.
- No official metric promotion was authorized.

Next readiness step:

- Plan a bounded SQLSolver one-baseline exact-candidate subset with identity guard, explicit feature/SQL-shape labels, and coverage reporting.
