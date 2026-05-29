# verieql_synthetic_from_clause_smoke_v0

Audit verdict: bounded local synthetic VeriEQL smoke completed.

This task ran a minimal synthetic smoke through the staged VeriEQL JSONL wrapper using SQL pairs with a `FROM` clause and a simple two-column schema context. The output is local verifier-support evidence only. It is not Common-core evidence, not official Semantic Equivalence Rate, not paper evidence, not retained evidence, and not leaderboard input.

Result summary:

- Tool: VeriEQL only.
- Runtime root: `/tmp/sqlrb_verieql_synthetic_from_clause_smoke_v0`.
- Schema: table `T(a integer, b integer)`.
- Pair `synthetic_from_equivalent`: `SELECT a FROM T` vs `SELECT a FROM T`.
- Pair `synthetic_from_nonequivalent`: `SELECT a FROM T` vs `SELECT b FROM T`.
- Raw invocation status: VeriEQL batch CLI completed and wrote output JSONL.
- Normalized verdicts: `timeout` for the equivalent pair, `non_equivalent` for the non-equivalent pair.
- Local synthetic summary: `decidable_count=1`, `timeout_count=1`, `semantic_equivalence_rate=0.0`.

The local synthetic summary was produced by the existing verifier-support output schema and boundary flags. It must not be interpreted as official benchmark Semantic Equivalence Rate.

Boundary status:

- No Common-core, PERF, CONS, PORT, or LONGTAIL cases were run.
- No SQLSolver run occurred.
- No timing or speedup was computed.
- No official metrics were computed.
- No top-level `reports/` or `results/` were updated.
- No retained evidence was promoted.
- No output runtime artifacts were committed.
