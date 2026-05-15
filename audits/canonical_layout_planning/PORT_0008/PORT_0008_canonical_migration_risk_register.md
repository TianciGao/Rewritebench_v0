# PORT_0008 Canonical Migration Risk Register

| Risk | Severity | Affected files | Mitigation | Blocks actual migration? |
|---|---|---|---|---|
| Raw Spark plan local paths are not public-safe | high | `runs/spark/plans/rewrite_neg_01.txt`, `runs/spark/plans/rewrite_pos_01.txt` | Do not copy raw files into public retained evidence; reuse existing sanitized plan copies; map originals do-not-delete/private/archive | yes if raw files would be public |
| Validation scripts write to case-local `runs/` | medium | `validation/run_*`, `validation/run_*_plan_collection.sh` | Do not run scripts during migration; document output policy; later refactor public runners to external output directory | no for static migration, yes before public runner endorsement |
| No legacy checker directory exists | medium | generated `checker/*.yaml` | Generate checker metadata from retained result evidence; require human review | yes if checker metadata is not generated |
| Legacy README contains stale draft wording | medium | `README.md` | Generate public README from manifest and migration plan rather than copying byte-for-byte | no if generated README is used |
| Manifest path conversion may contradict runs-retention mapping | high | `manifest.yaml`, `evidence/runs_retention.yaml`, `metadata/artifact_paths.yaml` | Generate together from the same mapping CSV and validate path consistency | yes |
| Raw `runs/` wholesale copy would reintroduce public hygiene risks | high | `runs/` | Promote public-safe evidence into `evidence/`; keep raw `runs/` reference-only/private/archive mapped | yes |
| Existing evidence-pilot files may be overwritten accidentally | medium | current `cases/PORT/PORT_0008/evidence/*` | Treat as existing public evidence and verify SHA256 before/after | yes if SHA mismatch or overwrite occurs |
| Common-core/denominator wording drift | high | manifest, README, metadata, status docs | Keep denominator/paper/membership flags false and reference `case_sets/` only | yes |
| Legacy repo dirty/behind state confuses source-of-truth assumptions | medium | legacy repo state | Inspect read-only and record; do not mutate legacy; use explicit legacy HEAD in audit | no if recorded and read-only |
