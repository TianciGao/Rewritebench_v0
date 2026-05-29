# Manifest Contract Repair Summary

## Purpose and Scope

This task repaired `manifest.yaml` semantic structure for the 32 already converted v2 cases on branch `feature/case-package-v2-external-schema`. It preserved the clean-template physical paths and did not convert any Wave C/manual-review cases.

## Targeted Cases

Targeted cases: 32. Repaired manifests: 32. Cases retaining `manual_review_required` caveats: 17.

## Repair Result

All 32 manifests now use the colleague-style semantic contract with `primary_pool`, `package_path`, source provenance fields, `taxonomy`, object-form `sql.positive_rewrites` and `sql.hard_negatives`, clean `schema.profile` plus `schema.external_profile`, config-only checker paths, v2 validation wrappers, source-as-oracle witness policy, and regeneration-first `evidence_policy`.

Taxonomy was restored for all 32 cases from branch history/deleted `metadata/taxonomy.yaml` files. The repair did not use README text as the sole taxonomy source.

## Manual Review Caveats

Manual review remains required where provenance could not be recovered safely without invention. The retained blockers are listed in `manifest_repair_manual_review_blockers.csv`.

- Explicit draft origin was not recoverable for 17 cases.
- Original source path was not recoverable for 2 cases.

The manifests for those cases still pass structural validation because the missing facts are explicitly marked `manual_review_required` rather than fabricated.

## Validator Update

The v2 validator now enforces the semantic manifest contract. It fails on missing taxonomy, missing source family/status, malformed SQL rewrite entries, missing schema profile references, missing checker/validation paths, missing `evidence_policy`, required `evidence_ref`, absolute/local paths, and references to deleted compatibility surfaces.

## Protected Boundaries

No `case_sets/`, inventory, reports/results, denominator, paper-result, official-metric, DB/checker execution, or leaderboard surfaces were changed.

## Validation

Static v2 validation passed for all 32 repaired cases. Unit tests passed for `tests/case_package_v2`.

## Exact Next Safe Action

Run a bounded `case_package_v2_manifest_contract_repair_followup_v0` or Wave C planning task to resolve the remaining manual provenance caveats before using these semantic fields for public documentation or broader conversion policy.
