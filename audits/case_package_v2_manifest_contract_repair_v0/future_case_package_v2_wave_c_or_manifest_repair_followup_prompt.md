# Future Prompt: case_package_v2_wave_c_or_manifest_repair_followup_v0

Repository:
- Work only in /home/tianci_gao/code/Rewritebench_v0.
- Work only on branch feature/case-package-v2-external-schema.
- Do not inspect or modify the legacy repo.

Goal:
Resolve only the manual-review manifest provenance caveats recorded in `audits/case_package_v2_manifest_contract_repair_v0/manifest_repair_manual_review_blockers.csv`, or plan Wave C conversion only after those caveats are accepted as non-blocking.

Hard boundaries:
- Do not modify case_sets/, inventory/, reports/, results/, denominator values, paper results, official metrics, DB/checker execution, or leaderboard outputs.
- Do not restore case-local schema engine dirs, evidence/, runs/, metadata/, notes/, data/, old validation scripts, or per-case Python checkers.
- Do not invent taxonomy, source provenance, or draft origin values.

Required behavior:
- For each manual blocker, recover the exact field from current manifests, branch history, deleted metadata/provenance files, registry/case_set identity facts, or maintainer-provided source.
- If a value remains unrecoverable, keep `status: manual_review_required` and document the blocker.
- Re-run the semantic v2 validator for all 32 converted cases after any manifest edits.
