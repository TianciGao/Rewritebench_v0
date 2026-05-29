# Spark SQLGlot Noop Statement Preflight Triage

Verdict: `spark_statement_splitter_comment_gap`.

This audit triages the six non-PORT Spark same-engine rows from the Common-core SQLGlot noop local diagnostic snapshot that failed candidate execution with:

`Spark diagnostic query must contain exactly one statement`

Affected rows:

- `PERF_0008`
- `PERF_0013`
- `PERF_0017`
- `PERF_0019`
- `PERF_0024`
- `PERF_0082`

## Summary

All six rows were selected in the Spark Common-core SQLGlot noop snapshot, adapter invocation succeeded, candidate SQL was generated, user-entry candidate preflight passed, and source execution succeeded. Candidate execution then failed before Spark SQL execution because the Spark diagnostic executor's statement splitter returned more than one statement fragment.

The emitted SQLGlot noop candidates are not genuinely multiple executable statements. They are one query preceded by SQLGlot-emitted block comments. Those comments preserve metadata text containing semicolons. The current candidate preflight semicolon scan is comment-aware and ignores semicolons inside block comments, but the Spark diagnostic statement splitter strips only full-line `--` comments and does not ignore `/* ... */` block comments. That mismatch causes the Spark backend guard to classify these candidates as multiple statements.

## Local Boundary

This is a local diagnostic triage only. No benchmark code, SQLGlot adapter behavior, cases, SQL files, checker configuration, manifests, case sets, reports/results, denominator scaffolds, paper results, retained evidence, timing/speedup, official metrics, release export, tag, or leaderboard output changed.

No Common-core rerun was performed. The audit used existing local run artifacts under `runs/user/common_core_sqlglot_noop_spark_snapshot/`.

## Interpretation

- SQLGlot noop emitted one candidate query with leading block comments and a trailing semicolon.
- The block comments contain semicolons copied from source metadata or provenance comments.
- User-entry preflight passed because it ignores semicolons inside line and block comments.
- Spark candidate execution failed because its statement splitter treated semicolons inside block comments as statement separators.
- The rejection occurs before Spark parser execution, so this audit does not classify these rows as Spark SQL parser failures.

## Recommended Next Safe Action

Authorize a narrow Spark local diagnostic preflight/backend patch, if desired, to make the Spark statement splitter ignore semicolons inside SQL comments and string literals consistently with candidate preflight. The patch should include targeted regression coverage for these six rows or reduced statement-boundary fixtures, plus preservation checks for Spark same-engine smoke and PORT fail-closed behavior. Until then, keep the rows fail-visible.
