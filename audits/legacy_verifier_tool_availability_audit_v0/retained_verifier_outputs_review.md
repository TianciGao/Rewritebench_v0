# Retained Verifier Outputs Review

## Outputs Found

The legacy repository contains historical verifier support records:

- `reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table9_verifier_support_v1.csv`
- `reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/verifier_support_artifact_audit_v1.csv`
- `reports/evaluation/common_core_v0/12_PORT_VERIFIER_ARTIFACT_MAP_V1/verifier_support_pair_ledger_v1.csv`
- `reports/evaluation/common_core_v0/12_PORT_VERIFIER_ARTIFACT_MAP_V1/verifier_support_pair_ledger_v1.md`
- `docs/_scratch/PRIOR_SUPPORT_EVIDENCE_SUMMARY_SQLSOLVER_VERIEQL_v1.md`
- `docs/_scratch/SQLSOLVER_SUPPORT_SMOKE_CONS_0007_0035_v1.md`
- `docs/_scratch/SQLSOLVER_SUPPORT_SMOKE_ROLLUP_v1.md`
- `docs/_scratch/VERIEQL_SUPPORT_CANARY_v0.md`
- `cases/CONS/CONS_0003/provenance/verieql_calcite_397_159_raw.json`
- `cases/CONS/CONS_0004/provenance/verieql_calcite_397_362_raw.json`

## Classification

These are historical support/provenance artifacts, not reusable tool installations.

- SQLSolver records describe a bounded four-pair support smoke and a retained `3/4` support summary, while noting the clean per-verdict split was not retained in the evaluation folder.
- VeriEQL records describe a bounded `CONS_0035` canary where the positive side is constraint-sensitive and should not be generalized.
- Case provenance JSON files record VeriEQL/Calcite-origin source material for case construction, not new-repo verifier execution output.

## Reuse Boundary

These artifacts must not be converted into official Semantic Equivalence Rate or new release-repo verifier evidence in this task.

Any future use requires a separate retention/evidence mapping task that validates:

- denominator identity,
- pair identity,
- route/tool identity,
- environment/provenance,
- raw stdout/stderr or equivalent retained verifier trace,
- claim boundaries,
- compatibility with the D035 output contract.
