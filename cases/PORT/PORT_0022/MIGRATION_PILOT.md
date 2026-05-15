# PORT_0022 Migration Pilot

Date: 2026-05-15

## Scope

This is an evidence-mapping pilot only.

This is not a complete migrated case package. Source SQL, schema, checker, validation scripts, provenance, taxonomy, manifest, and raw runs remain in the legacy repo.

No legacy evidence was modified, sanitized in place, moved, deleted, renamed, overwritten, or copied as raw public retained evidence.

## Evidence Promoted

Sanitized retained Spark plan copies were promoted from already validated Route B sanitized trial outputs:

- `cases/PORT/PORT_0022/evidence/retained_plans/rewrite_neg_01.sanitized.txt`
- `cases/PORT/PORT_0022/evidence/retained_plans/rewrite_pos_01.sanitized.txt`

The original Spark plan artifacts remain do-not-delete and mapped:

- `cases/PORT/PORT_0022/runs/spark/plans/rewrite_neg_01.txt`
- `cases/PORT/PORT_0022/runs/spark/plans/rewrite_pos_01.txt`

## Non-Changes

This pilot does not change denominator, paper results, Common-core membership, route evidence, case admission, or benchmark claims.

This pilot does not migrate the full case package and does not run database engines, validation scripts, timing workloads, plan regeneration, or LLM calls.
