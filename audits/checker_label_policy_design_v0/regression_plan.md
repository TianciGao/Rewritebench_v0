# Regression Plan

Any future patch should include focused unit tests and bounded local diagnostics.

## Unit Tests

Add checker-level tests for:

- strict exact: identical labels and values pass;
- strict label mismatch: same values but different labels remains mismatch;
- label-only diagnostics: same values and different labels records `label_only_mismatch: true`;
- value mismatch: same labels but different values is not label-only;
- row-count mismatch is not label-only;
- column-count mismatch is not label-only;
- duplicate/multiplicity differences are not hidden;
- explicit alias mismatch remains strict by default, e.g. `SELECT 1 AS a` versus `SELECT 1 AS b`;
- generated expression label candidates are diagnostics only unless explicit config says otherwise;
- cross-dialect controlled positional comparison remains role-gated;
- MySQL-to-Spark mixed numeric equivalence remains limited to the existing resolved role predicate.

## Fixture Rows

Use small synthetic JSONL fixtures for deterministic unit tests:

- `{"a": 1}` versus `{"a": 1}`;
- `{"a": 1}` versus `{"b": 1}`;
- `{"a": 1}` versus `{"a": 2}`;
- `{"avg(x)": "1.0000"}` versus `{"AVG(x)": "1.0000"}`;
- `{"alias_a": "same"}` versus `{"alias_b": "same"}`.

## Local Diagnostic Preservation

Before any exactness-changing patch, rerun or preserve:

- `PERF_0062` MySQL SQLGlot noop label-only row;
- `PORT_0004`, `PORT_0013`, `PORT_0022`, `PORT_0024` MySQL SQLGlot noop rows;
- representative same-engine exact rows: `PERF_0006`, `CONS_0005`, one LONGTAIL row;
- a known value-mismatch row, if available, to prove it remains mismatch;
- controlled PORT PostgreSQL target route exact 5/5;
- controlled PORT MySQL target route exact 4/4;
- controlled PORT Spark target route exact 4/4;
- Spark same-engine smoke exact 2/2.

## Output Checks

Validate that:

- no timing fields are introduced;
- no official metrics are computed;
- no reports/results files are written;
- `runs/user/` remains uncommitted;
- any new details appear only in local diagnostic artifacts and ledger/report surfaces explicitly owned by user-entry diagnostics.
