# verieql_finite_bound_wrapper_mode_v0

Audit date: 2026-05-23

Branch: `feature/case-package-v2-external-schema`

## Verdict

Implemented a local-only VeriEQL finite-bound wrapper mode on top of the existing staged-root JSONL path. The wrapper now supports `parallel.cli_within_bound`, VeriEQL-compatible schema identifier canonicalization, strict all-`EQU` bounded-equivalent normalization, bound metadata in outputs, and focused synthetic regression tests.

## Scope

Changed only:

- `src/sql_rewrite_bench/verifier_support/verieql.py`
- `tests/user_entry/test_verieql_support.py`
- this audit packet
- project-control status and run log

No Common-core run, method-generated candidate evaluation, official Semantic Equivalence Rate, official metrics, top-level reports/results update, retained-evidence promotion, leaderboard output, dependency install, VeriEQL source patch, denominator change, case membership change, or paper result change occurred.

## Optional Smoke

An optional local-only synthetic finite-bound smoke ran under:

`/tmp/sqlrb_verieql_finite_bound_wrapper_mode_v0/`

It used the staged VeriEQL root and external venv. Results:

- `SELECT a FROM T` vs `SELECT a FROM T`: `equivalent`, raw states all `EQU` at bound 10.
- `SELECT a FROM T` vs `SELECT b FROM T`: `non_equivalent`, raw state `NEQ`.

These results are local synthetic tool-behavior evidence only.
