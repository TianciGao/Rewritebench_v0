# PORT final bounded batch migration report

Date: 2026-05-16

## Scope

This bounded batch upgraded `PORT_0004` from a legacy-compatible full-case pilot to canonical layout and migrated `PORT_0022`, `PORT_0024`, and `PORT_0025` from formal evidence-mapping pilot slices to canonical public-release case packages. It is not blind Common-core 40 migration, not full Common-core 40 migration, not DB validation, not evidence regeneration, and not a timing rerun.

## Pattern

The batch follows the canonical `PORT_0008` pattern and the successful PORT wave-2 batch 001 pattern. Existing formal evidence-mapping pilot artifacts for `PORT_0022`, `PORT_0024`, and `PORT_0025` were retained and reused. `PORT_0004` historical pilot context was preserved in `notes/migration_pilot_history.md`.

## Per-case migration result

- `PORT_0004`: completed; upgraded to canonical layout; existing sanitized Spark plans retained; raw release `runs/` copies removed from the canonical public tree after public-safe evidence promotion.
- `PORT_0022`: completed; migrated to canonical layout; existing sanitized Spark plans reused.
- `PORT_0024`: completed; migrated to canonical layout; existing sanitized Spark plans and `spark_result_check.sanitized_summary.json` reused; raw stdout/stderr logs were not copied.
- `PORT_0025`: completed; migrated to canonical layout; existing sanitized Spark plans reused.

## Hard-negative reasons

- `PORT_0004`: `year_filter_literal_changed`.
- `PORT_0022`: `year_filter_literal_changed`.
- `PORT_0024`: `boolean_filter_literal_changed`.
- `PORT_0025`: `order_direction_boundary_changed`.

All four are static-inferred for migration and recorded as needing review if not explicit in legacy.

## Sanitized Spark plan and raw log handling

Existing sanitized Spark plan evidence was reused for all four cases. Raw Spark plan text files were not copied into public retained evidence. `PORT_0024` uses the existing sanitized Spark result-check summary; raw stdout/stderr logs and raw log path references were not copied into public evidence.

## Portability boundary

No DB rerun was performed, no new cross-engine execution result was created, no transfer-speed claim was created, no complete nine-case PORT result claim was created, and no leaderboard was introduced.

## PORT pool status

All nine Common-core PORT cases now have canonical public-release case packages that pass validator v0.3 full-case and canonical-case modes. This is a case-package migration completion statement only; it does not create new cross-engine results, denominator changes, paper-result changes, or benchmark result rows.

## Validation script caveat

Copied validation scripts are retained legacy validation assets. They were not executed during migration and are not final public user runners. Future public runner output must not write to case-local `runs/` by default.

## Validation results

- SHA256 copy validation: PASS.
- Public hygiene scan: PASS.
- YAML validation: PASS.
- JSON validation: PASS.
- Validator v0.3 full-case for new/upgraded batch: PASS 4/4.
- Validator v0.3 canonical-case for new/upgraded batch: PASS 4/4.
- Evidence-pilot regression: PASS 6/6.
- Full-case regression: PASS 35/35.
- Canonical-case regression: PASS 35/35.
- Python compile: PASS.

## Denominator and paper boundary

Denominator unchanged. Paper results unchanged. Common-core membership unchanged. Case membership unchanged. Raw legacy evidence unchanged.

## Failed or deferred cases

None.

## Next safe action

Human review this PORT final bounded batch output. If accepted, perform a Common-core case-package migration status audit/closeout across PERF, CONS, PORT, and LONGTAIL before any case-set/report/result update.
