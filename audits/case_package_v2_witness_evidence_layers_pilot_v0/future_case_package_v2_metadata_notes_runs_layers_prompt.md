# Future Prompt: case_package_v2_metadata_notes_runs_layers_pilot_v0

Work only in `/home/tianci_gao/code/Rewritebench_v0` on branch `feature/case-package-v2-external-schema`. Do not modify `main` and do not inspect or modify the legacy repository.

This is a branch-only writable pilot for the next folder-order layers after witness/evidence conversion:

1. metadata
2. notes
3. runs cleanup classification

Pilot cases:

- `PERF_0006`
- `PERF_0007`
- `CONS_0005`
- `PORT_0003`
- `LONGTAIL_0011`

Scope:

- Merge durable governance metadata into canonical manifest fields or `compatibility.metadata_legacy`.
- Classify notes for public-safe README/manifest/evidence-note placement.
- Classify case-local `runs/` as empty, placeholder-only, retained evidence, or manual-review.
- Delete only empty or placeholder-only `runs/` if explicitly authorized by the task prompt and validated.
- Do not delete retained evidence without retention mapping.
- Do not run DB/checker execution.
- Do not compute official metrics.
- Do not update reports/results, denominators, paper results, case sets, inventory, or leaderboard outputs.

Required validation:

- Run `PYTHONPATH=src python scripts/dev/validate_case_package_v2_refs.py --case <case>` for each pilot case.
- Run `PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`.
- Confirm no protected benchmark-surface changes and no unsafe evidence publication.

Stop conditions:

- Any non-empty retained `runs/` deletion without retention mapping.
- Any sensitive private path, credential, prompt/API trace, or raw debug log proposed for public evidence.
- Any DB/checker execution.
- Any official metric computation.
- Any reports/results, denominator, paper-result, case-set, inventory, or leaderboard change.
