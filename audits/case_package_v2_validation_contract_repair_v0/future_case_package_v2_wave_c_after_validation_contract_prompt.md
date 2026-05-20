# Future Prompt: case_package_v2_wave_c_after_validation_contract_v0

Repository:
- Work only in `/home/tianci_gao/code/Rewritebench_v0`.
- Work only on branch `feature/case-package-v2-external-schema`.
- Do not modify `main` or inspect the legacy repo.

Task title:
case_package_v2_wave_c_after_validation_contract_v0

Use the repaired three-file validation contract as the canonical target for future Wave C conversion:

```text
validation/run_validation.sh
validation/run_plan_collection.sh
validation/run_engine_queries.py
```

Convert only precleared Wave C cases authorized by the maintainer. Preserve dialect variants where semantically needed, do not invent provenance/taxonomy/source fields, and do not modify `case_sets/`, inventory, reports/results, denominators, paper results, official metrics, DB/checker execution, or leaderboard output. Keep shared logic under `src/sql_rewrite_bench/validation/`; case-local `run_engine_queries.py` files must remain thin shims.
