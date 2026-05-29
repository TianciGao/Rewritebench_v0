# Synthetic Regression Tests

## Focused Tests

Command:

```bash
pytest tests/user_entry/test_verieql_support.py -q
```

Result:

```text
18 passed in 0.17s
```

Coverage added:

- schema identifier canonicalization;
- finite-bound staged-root detection;
- finite-bound command construction;
- JSONL generation for `SELECT a FROM T` vs `SELECT a FROM T`;
- JSONL generation for `SELECT a FROM T` vs `SELECT b FROM T`;
- normalization of `EQU`, `EQU,EQU`, `NEQ`, `EQU,TMO`, `NSE`, and `OTE`;
- fail-closed behavior remains covered by existing unavailable-root tests;
- fake finite-bound root writes one `equivalent` and one `non_equivalent` row.

## Full User-Entry Tests

Command:

```bash
pytest tests/user_entry -q
```

Result:

```text
216 passed, 1 skipped, 12 subtests passed in 4.10s
```

## Optional Real Synthetic Smoke

Runtime root:

`/tmp/sqlrb_verieql_finite_bound_wrapper_mode_v0/`

Result:

- finite-bound mode: `finite_bound`
- bound size: 10
- timeout seconds: 30
- `synthetic_from_equivalent`: `equivalent`, raw states `EQU` repeated 10 times
- `synthetic_from_nonequivalent`: `non_equivalent`, raw state `NEQ`
- local synthetic summary: `semantic_equivalence_rate=0.5`, `decidable_count=2`, `verifier_decidability_rate=1.0`

This smoke is local synthetic tool behavior only, not Common-core or paper evidence.
