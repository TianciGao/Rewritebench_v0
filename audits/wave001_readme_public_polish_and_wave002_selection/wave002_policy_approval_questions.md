# Wave 002 Policy Approval Questions

These questions determine whether the 28 deferred wave 001 cases can be migrated efficiently in a second batch without copying unsafe legacy evidence.

1. Can cases with static-inferred hard-negative reason be migrated if the checker boundary is marked `needs_review` and no metric or paper claim is created?
2. Can validation scripts be retained as legacy assets with a standard output-policy caveat, provided they are not executed during migration and do not imply DB validation?
3. Can Spark plan local-path artifacts and other local-path evidence be archive-mapped in `evidence/runs_retention.yaml` rather than copied into the public package?
4. Can raw stdout/stderr/debug logs remain excluded from public packages if their existence is recorded as private/original retained evidence only?
5. Can missing retained evidence be represented as `evidence_not_retained` when source SQL, positive rewrite, negative rewrite, schema, and checker assets are complete?
6. Can schema-only or evidence-index gaps be marked `manual_review_required` in metadata rather than blocking package creation, as long as the case remains outside Common-core v0 and Track A denominators?
7. Can cases with legacy `runs/` present be standardized with no raw run copy if `runs_retention.yaml` records original legacy paths as do-not-delete references?
8. Can wave 002 use a batch no-global-leaderboard, no-denominator-change, no-paper-result caveat for all migrated non-Common-core packages?

Recommended decision:

Approve a narrow batch policy for wave 002 that allows public-safe core package creation while requiring unsafe legacy evidence to remain archive-mapped or excluded from the public package. Deny any migration that requires copying raw runs, raw logs, prompt/token/API traces, or local-path artifacts.
