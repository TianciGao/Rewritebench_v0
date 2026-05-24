# Track A 120 Readiness

Current verdict:
- Ready for exact-gated timing smoke over the 6 exact rows from this bounded diagnostic.
- Not ready for full Track A 120 local diagnostic rerun.

Evidence supporting timing smoke:
- All 9 rows generated candidates and passed preflight.
- All 9 source rows executed.
- 8 candidates executed.
- 6 rows were exact/result-consistent.

Blockers before broader Track A use:
- MySQL `CONS_0005` candidate execution failure from `ARRAY_ANY`/lambda-style output.
- Spark `CONS_0005` semantic mismatch.
- Spark `CONS_0036` strict-label mismatch.
- No route-card/timing projection has been produced for this route.
- PORT source-role behavior remains untested for this route and must remain separate.

Recommended next step:
- Run exact-gated timing smoke over the 6 exact rows only, or first triage MySQL `ARRAY_ANY` and Spark mismatch behavior if the priority is broader exact coverage.
