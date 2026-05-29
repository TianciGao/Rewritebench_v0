# VeriEQL Synthetic Decidable Smoke V0

Task: `verieql_synthetic_decidable_smoke_v0`

Branch: `feature/case-package-v2-external-schema`

Verdict: `synthetic_smoke_ran_unsupported_no_decidable_verdict`

This task ran a minimal local VeriEQL synthetic smoke through the existing staged-root JSONL wrapper. It used temporary SQL files and temporary output only:

```text
/tmp/sqlrb_verieql_synthetic_decidable_smoke_v0
```

Pairs executed:

- `synthetic_select1_equivalent`: `SELECT 1` vs `SELECT 1`
- `synthetic_select1_nonequivalent`: `SELECT 1` vs `SELECT 2`

Both pairs reached VeriEQL and produced tool-native output rows. Both returned:

```text
states=["NSE"]
err="Not supported feature: Query must have a FROM clause"
```

The wrapper normalized both rows to:

```text
unsupported
```

Summary:

- `pairs_planned=2`
- `pairs_attempted=2`
- `unsupported_count=2`
- `decidable_count=0`
- `semantic_equivalence_rate=null`
- `semantic_equivalence_rate_status=not_applicable`
- `result_checker_exactness_used=false`

This confirms the staged environment and wrapper can run the synthetic batch path, but it does not confirm clean decidable verdicts for `SELECT`-without-`FROM` queries.

Boundary: local verifier-support smoke only; not Common-core evidence, not official Semantic Equivalence Rate, not paper evidence, not retained evidence, and not leaderboard input.
