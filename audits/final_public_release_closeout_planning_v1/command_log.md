# Command Log

Commands run before editing:

```bash
git status -sb
git branch --show-current
git log --oneline -20
```

Context read:

- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/DECISION_LOG.md`
- `project_control/MIGRATION_RUN_LOG.md` tail
- `project_control/RELEASE_SURFACE_POLICY_DECISIONS.md`
- `project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md`
- `audits/final_public_release_metadata_readiness_v0/README.md`
- `audits/final_public_release_metadata_readiness_v0/readiness_matrix.csv`
- `audits/final_public_release_metadata_readiness_v0/remaining_blockers.md`
- `audits/user_entry_local_evaluation_phase_closeout_v0/README.md`
- `audits/release_surface_metadata_polish_v0/README.md`
- `audits/perf_0077_0082_source_path_followup_v0/README.md`
- `audits/case_package_v2_common_core40_final_closeout_rerun_v0/common_core40_final_closeout_rerun_summary.md`

Current release surface inspected:

- `README.md`
- `LICENSE`
- `CITATION.cff`
- `CONTRIBUTING.md`
- `.gitignore`
- `benchmark_spec/`
- `docs/`
- `examples/`
- `src/`
- `scripts/`
- `tests/`
- `.github/workflows/`
- `case_sets/common_core_v0/`
- representative Common-core cases
- `reports/README.md`
- `results/README.md`

Lightweight validation already run:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run --help
python scripts/user/run_user_benchmark.py --help
PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine postgres --smoke --explain-selection
PYTHONPATH=src python -m sql_rewrite_bench.user_run --show-output-schema
PYTHONPATH=src pytest tests/user_entry
PYTHONPATH=src python scripts/dev/validate_case_package_v2_refs.py --case <each Common-core case path>
```

Observed outcomes:

- User-entry tests: 70 passed, 1 skipped.
- Smoke selection explanation: 2 selected rows, 2 unique cases, no adapter invoked, no run outputs created.
- V2 reference validator: 40 Common-core cases checked, 0 failures.
- Legacy `validate_case_package.py --mode canonical-case` is not applicable to the current v2 clean-template package layout and failed as expected in advisory inspection.

Final validation commands:

```bash
git diff --check
python - <<'PY'
from pathlib import Path
import yaml
yaml.safe_load(Path("CITATION.cff").read_text(encoding="utf-8"))
PY
python - <<'PY'
from pathlib import Path
import csv
import json
base = Path("audits/final_public_release_closeout_planning_v1")
for name in ["closeout_readiness_matrix.csv", "validation_results.csv"]:
    list(csv.DictReader((base / name).open(newline="", encoding="utf-8")))
json.loads((base / "readiness_summary.json").read_text(encoding="utf-8"))
PY
```

Additional validation:

- Markdown sanity checks for public metadata and new audit markdown files passed.
- `.gitignore` policy check passed: `runs/user/` is ignored and all of `runs/` is not ignored.
- Protected-surface diff check passed.

Final validation result: passed.
