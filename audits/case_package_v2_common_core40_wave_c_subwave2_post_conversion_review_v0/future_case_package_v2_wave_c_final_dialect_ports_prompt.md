# Future Prompt: case_package_v2_common_core40_wave_c_final_dialect_ports_v0

Repository:
- Work only in `/home/tianci_gao/code/Rewritebench_v0`.
- Work only on branch `feature/case-package-v2-external-schema`.
- Do not modify `main`.
- Do not inspect or modify the legacy repo.

Task:
Convert only the final Wave C dialect-variant PORT cases:
- `PORT_0004`
- `PORT_0013`

Do not convert or modify any other case.

Required constraints:
- Preserve existing `sql/dialect_variants/` as semantic PORT v2 assets.
- Use the repaired semantic manifest contract with object-form SQL metadata.
- Use regeneration-first `evidence_policy`.
- Use the repaired three-file validation contract: `run_validation.sh`, `run_plan_collection.sh`, and thin `run_engine_queries.py`.
- Create per-case external schema packages only for the two approved schema IDs: `parrot_bird_port0004_v0` and `parrot_bird_port0013_v0`.
- Do not create `evidence/cases/`.
- Do not modify `case_sets/`, inventory, reports/results, denominator values, paper results, official metrics, DB/checker execution, or leaderboard outputs.

Stop conditions:
- Any required semantic manifest field cannot be recovered or explicitly caveated without invention.
- Any dialect variant has unclear semantic status.
- Any external schema copy-first verification fails.
- Any validator fails after conversion.

Validation:
- Run the static v2 validator for `PORT_0004` and `PORT_0013`.
- Run regression validators for all already converted cases.
- Run `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`.
- Confirm protected surfaces remain unchanged.
