# No-Op Substitution Guard

SQLGlot no-op candidates must not be used as SQLGlot optimize candidates.

No fallback to no-op is allowed.

If only no-op exists for a case, the SQLGlot optimize row remains missing or failed for this route.

Any future POCR annotation for SQLGlot optimize must use actual SQLGlot optimize candidate SQL only. Unrelated PostgreSQL controls, reference roots, Direct LLM roots, Repair-1 roots, Calcite roots, R-Bot roots, LLM-R2 roots, and SQLGlot no-op roots are rejected as substitutes.
