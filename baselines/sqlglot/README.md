# SQLGlot User-entry Adapters

This directory contains optional non-DB SQLGlot adapters for the B-line user-entry runner.

The adapters expose two candidate-generation routes:

- `sqlglot_noop`: invoked as `--route noop`
- `sqlglot_optimize`: invoked as `--route optimize`

Both routes read the source SQL path provided by the user-entry runner, use the selected engine to infer a SQLGlot dialect, and write candidate SQL to `SQLRB_CANDIDATE_SQL_PATH`.

## Usage

Example adapter command for the user-entry runner:

```bash
python baselines/sqlglot/sqlglot_user_adapter.py --route noop
```

or:

```bash
python baselines/sqlglot/sqlglot_user_adapter.py --route optimize
```

These commands are intended to be passed through `--adapter-command` on `python -m sql_rewrite_bench.user_run`.

## Known Context-free Optimize Limitation

`--route noop` and `--route optimize` are separate user-entry adapter routes. Do not merge their local diagnostic outcomes into a single SQLGlot score.

The current `--route optimize` implementation is context-free: it reads the source SQL, parses it using the selected engine dialect, calls SQLGlot `optimize(expression)` without case schema or catalog context, and emits candidate SQL.

Because it has no case schema/catalog context, context-free optimize may emit invalid qualification for some correlated subqueries. A bounded local diagnostic found this on `CONS_0005`, where SQLGlot emitted invalid three-part references:

- PostgreSQL: `"table1"."table2"."i"`
- MySQL/Spark: `` `table1`.`table2`.`i` ``

That failure is fail-visible adapter behavior. It is not a database backend failure, checker failure, timing issue, official metric, or benchmark code failure.

Users should not interpret bounded local diagnostic SQLGlot route results as official retained baseline evidence. A future schema-aware SQLGlot route would need a separately named route and separate authorization because it changes route semantics and comparability.

## Boundaries

- This is a non-DB user-entry adapter.
- It only emits candidate SQL.
- It does not execute SQL.
- It does not run checkers.
- It does not collect timing.
- It does not compute official metrics or speedup.
- It does not update retained evidence.
- It does not update reports or results.
- It does not change denominators or case membership.
- It does not create global leaderboard output.
- Outputs belong under local `runs/user/<run_id>/` directories created by the user-entry runner.

## Dependency

SQLGlot is optional. Install optional SQLGlot support before using these adapters:

```bash
python -m pip install -e ".[sqlglot]"
```

If SQLGlot is unavailable, the adapter exits nonzero with a clear dependency error. It does not silently fall back to raw source SQL.
