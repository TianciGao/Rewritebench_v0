# CONS_0007 Support-Candidate Review

## Classification

`CONS_0007` was marked:

- `recommended_status`: `support_candidate`
- `sqlsolver_support_risk`: `medium`
- `verieql_support_risk`: `medium`
- `support_usefulness`: `high`

Reason recorded by the old readiness scaffold:

```text
Compact Calcite-derived consistency case is the best bounded first support candidate for verifier-style analysis.
```

## Available Legacy Inputs

The adjacent VeriEQL bootstrap notes record these files:

- `cases/CONS/CONS_0007/source.sql`
- `cases/CONS/CONS_0007/rewrite_pos_01.sql`
- `cases/CONS/CONS_0007/rewrite_neg_01.sql`
- `cases/CONS/CONS_0007/schema/ddl_pg.sql`

The legacy generated VeriEQL JSONL pair shape used:

- `index`
- `file`
- `name`
- `benchmark`
- `case_id`
- `pair_role`
- `schema`
- `constraint`
- `pair`

For `CONS_0007`, the schema mapping was a single table:

```text
TMP_EMPS(EMPID, DEPTNO, NAME, SALARY, COMMISSION)
```

## Caveat

Historical VeriEQL output outside `baseline_smoke` reports `Not supported feature: EXISTS` for both `CONS_0007` source-positive and source-negative pairs. That makes `CONS_0007` a useful first compatibility canary, not a guaranteed proof/refutation candidate for VeriEQL.

## Current Recommendation

Use `CONS_0007` as the first bounded support candidate when the goal is to test adapter wiring, pair generation, output placement, and fail-closed behavior. Treat actual equivalent/non-equivalent proof support as tool-dependent and not assumed.
