# Common-core MySQL Local Diagnostic v0

Verdict: `completed_with_failures`.

This packet summarizes a bounded Common-core v0 MySQL local diagnostic trial using the public no-op adapter.

Run output path: `runs/user/common_core_mysql_noop_db_checker/`.

## Summary

- Case set: `common_core_v0`.
- Engine filter: `mysql`.
- Adapter: `python examples/user/noop_adapter.py`.
- Selected rows: 40.
- Candidate generated rows: 40.
- Candidate preflight passed rows: 40.
- MySQL source execution attempted rows: 35.
- MySQL source executable rows: 31.
- MySQL candidate execution attempted rows: 31.
- MySQL candidate executable rows: 31.
- Checker attempted rows: 31.
- Exact rows: 31.
- Mismatch rows: 0.
- Source-like rows: 40.

Failure buckets:

- `none=31`
- `source_execution_failed=4`
- `unsupported_engine=5`

Diagnostic mode distribution:

- `same_engine=35`
- `cross_dialect_reference=5`

## Failure Interpretation

The 31 non-PORT rows reached MySQL source execution, MySQL candidate execution, checker handoff, and exact comparison under the no-op adapter.

The four same-engine PORT rows `PORT_0003`, `PORT_0005`, `PORT_0008`, and `PORT_0012` failed at MySQL source execution. The local error excerpts show MySQL syntax rejection for PostgreSQL-style double-quoted identifiers, `NULLS FIRST/LAST`, or PostgreSQL-oriented functions in the retained source SQL. Candidate execution and checker comparison were not attempted for those rows.

The five cross-dialect PORT rows `PORT_0004`, `PORT_0013`, `PORT_0022`, `PORT_0024`, and `PORT_0025` were selected as MySQL rows but are manifest-declared `cross_dialect_reference` diagnostics whose target candidate engine is PostgreSQL. The runner failed closed with `unsupported_engine` rather than silently changing roles or substituting target-reference SQL.

## Boundary

This is local diagnostic output only. It is not official metrics, not timing or speedup, not paper reproduction, not a reports/results update, not retained-evidence promotion, and not a leaderboard input.

No source code, scripts, tests, examples, cases, manifests, SQL, schemas, checker configs, validation files, `case_sets/`, reports/results, denominators, paper results, case membership, raw retained evidence, release tags, or branches were changed by this audit task.

## Recommended Next Safe Action

Review the four same-engine PORT MySQL source-execution failures and the five cross-dialect `--engine mysql` fail-closed rows as local diagnostic routing/source-compatibility findings. Any follow-up should be separately authorized and should not compute timing, official metrics, reports/results, paper results, retained evidence, or leaderboard output.
