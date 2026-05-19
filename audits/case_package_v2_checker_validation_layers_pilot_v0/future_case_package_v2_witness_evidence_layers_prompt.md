# Future Prompt: case_package_v2_witness_evidence_layers_pilot_v0

Work only in `/home/tianci_gao/code/Rewritebench_v0` on branch `feature/case-package-v2-external-schema`. Do not modify `main` and do not inspect or modify the legacy repository.

This is a branch-only writable pilot for the next folder-order layers after checker/validation conversion:

1. witness
2. evidence

Pilot cases:

- `PERF_0006`
- `PERF_0007`
- `CONS_0005`
- `PORT_0003`
- `LONGTAIL_0011`

Scope:

- Normalize witness policy fields only.
- Add or normalize `evidence_ref` references only.
- Use copy-first externalization planning for evidence; do not delete case-local evidence.
- Do not delete case-local runs.
- Do not convert metadata, notes, runs, README, or validator behavior unless strictly needed for static reference validation.
- Do not run DB/checker execution.
- Do not compute official metrics.
- Do not update reports/results, denominators, paper results, case sets, or inventory.
- Do not create global leaderboard output.

Required validation:

- Run `PYTHONPATH=src python scripts/dev/validate_case_package_v2_refs.py --case <case>` for each pilot case.
- Run `PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`.
- Confirm no case-local runs deletion, no evidence deletion, and no protected benchmark-surface changes.

Stop conditions:

- Any retained evidence deletion.
- Any case-local runs deletion.
- Any sensitive private path, credential, prompt/API trace, or raw debug log proposed for public evidence.
- Any DB/checker execution.
- Any official metric computation.
- Any reports/results, denominator, paper-result, case-set, inventory, or leaderboard change.
