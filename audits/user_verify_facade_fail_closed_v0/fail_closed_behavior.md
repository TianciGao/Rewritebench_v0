# Fail-Closed Behavior

When the selected verifier tool is unavailable:

- The command still writes contract-shaped local verifier outputs.
- `verifier_pairs.csv` records the planned synthetic smoke pair or pairs.
- `verifier_verdicts.jsonl` records `not_attempted` rows.
- `semantic_equivalence_summary.json` records:
  - `semantic_equivalence_rate=null`
  - `semantic_equivalence_rate_status=not_applicable`
  - `na_reason=verieql_unavailable` or `sqlsolver_unavailable`
- No equivalent or non-equivalent verdict is fabricated.
- Local result-checker exactness is not used as verifier evidence.

Synthetic smoke scope:

- VeriEQL: one pair, `SELECT 1` vs `SELECT 1`.
- SQLSolver: two pairs, `SELECT 1` vs `SELECT 1` and `SELECT 1` vs `SELECT 2`.

If an explicit tool command is provided and is available, the same bounded synthetic-smoke scope is used.
