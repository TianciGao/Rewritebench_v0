# CONS_0005

## What this case tests

CONS_0005 is a semantic consistency and checker-boundary case from the `CONS` pool. It exercises a Calcite core SQL test pattern involving a correlated `NOT IN` query over `table1` and `table2`, with declared pressure around subquery decorrelation, null semantics, and anti-join behavior.

The package provides the source query, a reference rewrite, executable context, checker configuration, and validation entrypoints so that candidate SQL can be evaluated as a statement-level rewrite, not as an isolated SQL string.

## SQL pattern overview

- Source query: The source query returns rows from `table1` whose `j` value is not in a correlated set of `table2.i` values filtered by `table1.i = table2.j`.
- Reference rewrite: `sql/pos_01.sql` rewrites the correlated `NOT IN` form into a `NOT EXISTS` anti-join with an explicit `NULL` branch for the subquery value.
- Checker control: `sql/neg_01.sql` omits the `NULL` branch, making it a checker control for NULL-sensitive but non-equivalent anti-join rewrites.

## Benchmark role

- Pool: `CONS`
- Common-core member: yes
- Benchmark unit: case package
- Primary pressure: `semantic consistency and checker-boundary pressure`
- Main rewrite opportunity: `subquery_decorrelation`
- Main semantic / portability / robustness risk: null-semantics gaps and anti-join semantics when rewriting correlated `NOT IN`
- Evaluation scope: governed by `case_sets/common_core_v0/` and `manifest.yaml`
- Reporting principle: results should be interpreted with role-aware and denominator-aware reporting

## Package files

- Package index: `manifest.yaml`
- Source query: `sql/source.sql`
- Reference rewrite: `sql/pos_01.sql`
- Hard negative: `sql/neg_01.sql`
- Schema profile: `schema/schema_profile.yaml`
- Checker configuration: `checker/`
- Validation entrypoints:
  - `validation/run_validation.sh`
  - `validation/run_plan_collection.sh`

Executable schema and data details are described by the schema profile and repository-level schema contracts.

Source-family, provenance, taxonomy, checker, and denominator-eligibility details are recorded in `manifest.yaml`.

## How to use this case

Run validation and reproduction commands from the repository root using the documented repository-level workflow.

The case-local validation scripts are entrypoints for this package, but new user or experiment outputs should be written to the documented top-level output location, not committed into the case package.

This README is a human-readable guide. It does not compute metrics, define official paper results, or change denominator membership.

## Interpretation boundary

This case includes a hard negative. Hard negatives are checker controls: they test whether the benchmark validation path rejects plausible but non-equivalent SQL.

They are not method-generated candidates.

Common-core membership, denominator values, metric definitions, and paper-facing results are governed by repository-level case-set, benchmark-spec, ledger, and report artifacts.

This README does not define a leaderboard, winner, speedup claim, full portability closure, transfer-speed claim, or general SQL-equivalence claim.
