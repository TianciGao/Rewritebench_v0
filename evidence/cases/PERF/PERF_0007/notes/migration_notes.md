# PERF_0007 Migration Notes

Migration date: 2026-05-16.

This package was migrated using copy-first release-repo migration. The legacy repository was not modified. Public-safe SQL, schema, witness load scripts, retained controls, and retained plan summaries were copied or mapped into canonical layout. Raw `runs/` was not copied wholesale.

Performance boundary: no timing run was executed, no speedup claim was created, and no ranking, leaderboard, or paper-result claim is created by this migration.

Hard-negative static explanation: `quantity_predicate_boundary_changed`. changes the quantity predicate from a strict less-than boundary to a less-than-or-equal boundary. This expected rejection is based on static SQL inspection and retained result evidence, with approval status recorded in `checker/expected_rejections.yaml`.

Spark plan handling: raw Spark plan text files are mapped as do-not-delete originals and sanitized public copies are retained under `evidence/retained_plans/spark/`.

Validation script caveat: scripts in `validation/` are retained legacy validation assets, were not executed during migration, and future public runner outputs must not write to case-local `runs/` by default.

Denominator unchanged. Paper results unchanged. Case membership unchanged. Raw legacy evidence unchanged.
