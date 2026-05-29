# Future Prompt: Remaining Wave C PORT Conversion

Task title:
case_package_v2_common_core40_wave_c_remaining_ports_v0

Repository:
- Work only in `/home/tianci_gao/code/Rewritebench_v0`.
- Work only on branch `feature/case-package-v2-external-schema`.
- Do not modify `main`.
- Do not inspect or modify the legacy repo.

Scope:
- Convert only precleared remaining Wave C PORT cases.
- Recommended next bounded subwave: `PORT_0008`, `PORT_0012`, `PORT_0022`, `PORT_0024`, and `PORT_0025`.
- Keep `PORT_0004` and `PORT_0013` for a later dialect-variant subwave unless explicitly authorized.

Requirements:
- Preserve dialect variants where present.
- Use the repaired semantic manifest contract.
- Use the three-file validation contract: `run_validation.sh`, `run_plan_collection.sh`, and thin-shim `run_engine_queries.py`.
- Use regeneration-first `evidence_policy`; do not create `evidence/cases/`.
- Create per-case external schema packages only after DDL/load verification.
- Do not invent provenance, taxonomy, source identity, draft origin, or dialect semantics.
- Do not modify `case_sets/`, inventory, reports/results, denominators, paper results, official metrics, DB/checker execution, or leaderboard outputs.

Validation:
- Run the v2 validator for each converted case.
- Run validators for already converted cases as regression checks.
- Run `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`.
- Run boundary checks confirming protected surfaces remain unchanged.
