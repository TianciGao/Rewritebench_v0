# PORT wave-2 batch 001 migration report

Date: 2026-05-16

## Scope

This bounded batch migrated exactly `PORT_0003`, `PORT_0005`, `PORT_0012`, and `PORT_0013` into canonical public-release case-package layout. It is not blind Common-core 40 migration, not full Common-core 40 migration, not DB validation, not evidence regeneration, and not a timing rerun.

## Pattern

The batch follows the canonical `PORT_0008` pattern. `PORT_0004` remains a legacy-compatible pilot and was not used as the canonical template. Existing formal evidence-mapping pilot artifacts for `PORT_0012` and `PORT_0013` were retained and reused.

## Per-case migration result

- `PORT_0003`: completed; canonical package created from legacy read-only source; Spark `rewrite_pos_02_spark` and `rewrite_neg_02_spark` plan text sanitized into public retained evidence.
- `PORT_0005`: completed; canonical package created from legacy read-only source; Spark `rewrite_pos_02_spark` and `rewrite_neg_02_spark` plan text sanitized into public retained evidence.
- `PORT_0012`: completed; evidence-mapping pilot files retained; existing sanitized Spark plans reused; directory upgraded to canonical package.
- `PORT_0013`: completed; evidence-mapping pilot files retained; existing sanitized Spark plans reused; directory upgraded to canonical package.

## Hard-negative reasons

- `PORT_0003`: `order_limit_direction_changed`.
- `PORT_0005`: `order_direction_boundary_changed`.
- `PORT_0012`: `year_filter_literal_changed`.
- `PORT_0013`: `gender_filter_literal_changed`.

All four are static-inferred for migration and recorded as needing review if not explicit in legacy.

## Sanitized Spark plan handling

- `PORT_0003` and `PORT_0005`: generated sanitized public Spark plan copies from raw legacy Spark plan text.
- `PORT_0012` and `PORT_0013`: reused existing validated formal evidence-mapping sanitized Spark plan files unchanged.
- Raw Spark plan text files were not copied into public retained evidence.

## Raw log handling

Raw stdout/stderr logs were not copied into public evidence. Public evidence is limited to public-safe retained TSV/JSON summaries and sanitized plan text; raw run artifacts remain mapped as do-not-delete originals.

## Portability boundary

No DB rerun was performed, no new cross-engine execution result was created, no transfer-speed claim was created, no complete PORT pool closure claim was created, and no leaderboard was introduced.

## Validation script caveat

Copied validation scripts are retained legacy validation assets. They were not executed during migration and are not final public user runners. Future public runner output must not write to case-local `runs/` by default.

## Validation results

- SHA256 copy validation: PASS.
- Public hygiene scan: PASS.
- YAML validation: PASS.
- JSON validation: PASS.
- Validator v0.3 full-case for new batch: PASS 4/4.
- Validator v0.3 canonical-case for new batch: PASS 4/4.
- Evidence-pilot regression: PASS 6/6.
- Full-case regression: PASS 32/32, including the four new PORT batch cases.
- Canonical-case regression: PASS 31/31, excluding legacy-compatible `PORT_0004`.

## Denominator and paper boundary

Denominator unchanged. Paper results unchanged. Common-core membership unchanged. Case membership unchanged. Raw legacy evidence unchanged.

## Failed or deferred cases

None.

## Next safe action

Human review this PORT wave-2 batch 001 output. If accepted, select the next bounded PORT wave from the readiness audit; do not start blind full Common-core 40 migration.
