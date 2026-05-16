# LONGTAIL_0011 Canonical Migration Risk Register

Planning status: planning only. No actual migration was performed.

| Risk | Severity | Affected files | Mitigation | Blocks actual migration |
|---|---:|---|---|---|
| Long-tail structure is overclaimed as workload-frequency evidence. | High | README, manifest, metadata/taxonomy.yaml, audit report | State that long-tail classification is structural only and set `workload_frequency_claim_created: false`. | Yes, if overclaim remains. |
| Spark plan artifacts contain local temporary paths. | High | `runs/spark/plans/source.txt`, `runs/spark/plans/rewrite_pos_01.txt`, `runs/spark/plans/rewrite_neg_01.txt` | Sanitize `file:/tmp...` and `/tmp/...` before public copy, or keep raw Spark plans private/archive-only. | Yes, if raw traces are published. |
| Spark validation scripts contain WSL-local wording. | Medium | `validation/run_spark_validation.sh`, `validation/run_spark_plan_collection.sh` | Adapt comments to neutral wording during future migration or document public runner caveat. | Yes, if public hygiene scan fails. |
| Validation scripts write to case-local `runs/`. | Medium | All validation and plan collection scripts | Mark copied scripts as retained legacy validation assets and add output-policy caveat. Future user runners should write outside case-local `runs/` by default. | No, if caveat is explicit and validator accepts it. |
| Raw `runs/` retention is ambiguous. | High | `runs/` tree and `evidence/runs_retention.yaml` | Do not copy raw `runs/` wholesale. Promote only public-safe evidence and map original legacy artifacts as do-not-delete. | Yes, if raw runs are copied without mapping. |
| Hard-negative expected reason remains ambiguous. | Medium | `checker/expected_rejections.yaml`, README, audit report | Encode tie-handling reason from static evidence and request human review of exact reason string before actual migration. | Yes, if checker reason is missing or contradictory. |
| Copied file differs from legacy source unexpectedly. | High | All copy-as-is or copy-and-rename files | Run SHA256 validation for every copied legacy file. | Yes. |
| Manifest and runs-retention fields conflict. | High | `manifest.yaml`, `evidence/runs_retention.yaml` | Cross-check denominator, paper-result, membership, raw-evidence, migration-scope, and public-safe fields. | Yes. |
| Public hygiene scan detects local path, API/prompt/token wording, or raw log trace in current tree. | High | Any public case file | Abort and fix release repo only; do not modify legacy. | Yes. |
| Denominator, paper results, or case membership are changed by migration. | Critical | `case_sets/`, paper reports, project controls | Do not modify denominator, paper-result, membership, or report result files. | Yes. |
| Raw legacy evidence is modified. | Critical | Legacy `cases/LONGTAIL/LONGTAIL_0011/` | Keep legacy repo read-only. | Yes. |
