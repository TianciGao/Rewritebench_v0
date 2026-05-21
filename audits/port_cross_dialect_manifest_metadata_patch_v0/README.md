# P2 PORT Local-Diagnostic Manifest Metadata Patch

## Verdict

`metadata_patch_complete_with_caveats`

All 9 Common-core PORT manifests now include additive `local_diagnostic` role metadata according to the P1 design. The patch is metadata-only: no SQL files, runner/source code, schema files, checker files, validation files, case sets, reports, results, denominators, paper results, or raw legacy evidence were changed.

## Patched Cases

Same-engine PostgreSQL local diagnostic metadata was added to:

- `PORT_0003`
- `PORT_0005`
- `PORT_0008`
- `PORT_0012`

Cross-dialect MySQL source-reference to PostgreSQL target-candidate metadata was added to:

- `PORT_0004`
- `PORT_0013`
- `PORT_0022`
- `PORT_0024`
- `PORT_0025`

## Caveats

- The five cross-dialect cases still require a future MySQL backend and future runner metadata consumption before they can complete source-reference diagnostics.
- Spark remains deferred; Spark variant files remain retained metadata where already present, but this task does not use or implement Spark execution.
- `PORT_0003` remains conservative: its manifest already has a recovered source path but lacks an explicit `source_dialect`; P1 classified its current `sql/source.sql` as PostgreSQL-compatible, so this patch records same-engine metadata without adding a fabricated dialect claim.
- `pos_01.sql` is not made a source oracle in any case. It is omitted for same-engine cases and marked `positive_reference` / sanity control only for cross-dialect cases.
- The existing v2 static reference validator does not yet whitelist the new top-level `local_diagnostic` block, so it fails the 9 patched PORT manifests with `local_diagnostic: unapproved top-level key`. Updating that validator is intentionally deferred because P2 does not authorize source/test changes.

## Boundaries

- No SQL edits.
- No runner/source changes.
- No MySQL/Spark implementation.
- No cross-dialect execution behavior implementation.
- No official metrics.
- No timing/speedup.
- No reports/results updates.
- No denominator, paper result, case membership, or raw legacy evidence changes.
- No global leaderboard.

## Next Safe Action

Design or implement P3 runner metadata consumption and static validator recognition as a separate fail-closed task. P3 should consume explicit manifest roles and fail closed while MySQL remains unavailable; it must not implement MySQL execution unless separately authorized.
