# Fix Candidate Plan

This audit does not implement fixes. It records the smallest safe follow-up tasks.

## 1. MySQL ARRAY_ANY fail-closed or dialect fix

Recommended first implementation task:

- Add a narrow MySQL route guard for `sqlglot_optimize_schema_aware` candidates containing SQLGlot-unsupported `ARRAY_ANY` or lambda syntax.
- Emit a fail-closed bucket such as `sqlglot_mysql_array_any_unsupported` before DB execution.
- Keep the candidate row denominator-visible.

Alternative larger task:

- Investigate SQLGlot optimizer/dialect emission for a MySQL-safe rewrite of this `NOT IN` pattern.

Do not do in the adapter without a separate design:

- Generic SQL expression rewriting.
- Case-specific SQL patching.
- Substituting source/checker exactness for failed candidate execution.

## 2. Spark CONS_0005 semantic triage

Recommended next diagnostic:

- Review SQLGlot's Spark rewrite for `NOT IN` with correlated subquery and NULL-containing inner values.
- Confirm whether the `COLLECT_LIST` / `FILTER` rewrite fails to preserve NULL-sensitive `NOT IN` semantics.
- Decide whether the route should fail closed for this pattern or whether a dedicated SQLGlot optimizer fix is available.

This row is not a safe normalization candidate.

## 3. Spark label policy design

Recommended separate policy task:

- Decide whether same-engine Spark explicit aliases may be case-folded for result labels in limited circumstances.
- Keep strict labels as the default.
- Require case/role/config gating before any exactness-changing behavior.

Spark `CONS_0036` can be reclassified only after such a policy exists.

## 4. Rerun sequence

Suggested sequence:

1. Implement MySQL `ARRAY_ANY` fail-closed guard or SQLGlot dialect emission fix.
2. Triage/fix Spark `CONS_0005` NULL-sensitive rewrite behavior.
3. Decide whether Spark label-only normalization should remain diagnostic-only or become a gated exactness policy.
4. Rerun the bounded tri-engine execution/checker smoke.
5. Run exact-gated timing smoke only after blocker movement is understood, unless timing over the existing six exact rows is specifically needed.

