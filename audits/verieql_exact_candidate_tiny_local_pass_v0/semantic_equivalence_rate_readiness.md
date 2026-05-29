# Semantic Equivalence Rate Readiness

Readiness result: partially ready for a bounded one-baseline exact-candidate local verifier subset; not ready for a full Common-core exact-candidate verifier pass.

What worked:
- Existing exact local diagnostic rows can be selected from `runs/user/common_core_pg_noop_db_checker`.
- Source-vs-candidate pair construction worked using source SQL, candidate SQL, and external PostgreSQL DDL paths.
- Finite-bound VeriEQL wrapper execution worked on real candidate rows.
- One real exact row, `CONS_0036`, produced a clean `equivalent` verdict.
- Local result checker exactness was not used as verifier equivalence evidence.

New blockers and risks:
- `PERF_0077` and `PERF_0082` both returned `NIE` on `LIKE` predicate shapes, now surfaced as `not_implemented`.
- The DDL parser should be hardened for parameterized types before broader use.
- A broader pass needs feature-aware selection/reporting so non-decidable rows remain visible and do not distort the decidable denominator.

Policy:
- `local_tiny_semantic_equivalence_rate=1.0` was computable because one of three attempted exact rows was decidable and equivalent.
- `verifier_decidability_rate=1/3` must be reported alongside the rate.
- Unknown, timeout, unsupported, syntax error, not implemented, out of memory, tool error, and not-attempted rows remain excluded from the decidable denominator and separately visible.
- Full Common-core exact-candidate verifier pass remains blocked until feature gates and DDL/schema parsing are hardened.

Recommended next safe action:
- Run a bounded one-baseline exact-candidate verifier planning task that defines a feature-aware row selector, keeps non-decidable rows visible, and optionally patches the DDL parser for parameterized types before expanding beyond this tiny pass.

