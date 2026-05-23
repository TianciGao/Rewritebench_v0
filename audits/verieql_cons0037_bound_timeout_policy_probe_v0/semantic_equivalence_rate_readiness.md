# Semantic Equivalence Rate Readiness

This task did not compute official Semantic Equivalence Rate.

Readiness observations:
- `CONS_0037` is decidable as `equivalent` at bounds 1, 2, 3, and 4.
- `CONS_0037` is non-decidable as `timeout` at bounds 5 and 10 under both 30-second and 120-second timeout settings tested here.
- The DDL/parser blocker remains resolved because the lower-bound runs reached VeriEQL with `DEPT` and `EMP` schema metadata.

Local diagnostic implications:
- A future local diagnostic subset can use a uniform smaller bound and report that bound as part of the verifier policy.
- A future `bound_size=10` subset should treat `CONS_0037` as timeout-prone and either exclude it or record it as non-decidable.
- Mixing lower-bound equivalent rows with higher-bound timeout rows in one denominator remains disallowed unless separately decided.

Full Common-core readiness:
- Not ready.
- Current evidence supports only a small feature-aware subset with explicit bound/timeout policy.

