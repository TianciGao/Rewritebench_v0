# PERF_0006 Canonical Migration Risk Register

Date: 2026-05-16

| Risk | Severity | Affected files | Mitigation | Blocks actual migration |
|---|---:|---|---|---|
| Performance/timing evidence may be misread as a new speedup claim | High | manifest, README, metadata, audit report | Record `speedup_claim_created: false`; avoid timing metrics and leaderboard language | Yes if unresolved |
| Spark plan artifacts contain local temporary paths | High | `runs/spark/plans/rewrite_pos_01.txt`, `runs/spark/plans/rewrite_neg_01.txt` | Sanitize into public retained copies or map as private/archive-only | Yes for raw publication |
| Validation scripts write to case-local `runs/` | Medium | `validation/run_*` scripts | Publish as retained legacy assets with output-policy caveat; future public runners must write outside case-local `runs/` | No if caveated |
| Raw `runs/` retention ambiguity | Medium | `runs/` | Do not copy wholesale; map every retained artifact through `evidence/runs_retention.yaml` | Yes if raw runs would be copied wholesale |
| Legacy taxonomy and engine metadata contain TODO fields | Medium | `taxonomy_trial_v0.2.yaml`, `metadata/engine_metadata.yaml` | Generate conservative metadata and mark human-review caveats; do not overclaim validation | No if caveated |
| PostgreSQL source plan exists but MySQL/Spark source outputs are not retained as full same-engine set | Medium | retained controls and plans | Preserve cross-dialect reference model; do not imply complete same-engine evidence beyond retained files | No if accurately described |
| Public hygiene scan failure | High | public-facing copied files | Stop actual migration or sanitize/archive affected artifacts | Yes |
| Overclaiming denominator or paper results | High | manifest, README, reports, status | Lock `denominator_changed: false` and `paper_results_changed: false` | Yes |
