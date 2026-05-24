# Command Log

Preflight:

```bash
git status -sb
git branch --show-current
git status --porcelain -- runs/user output reports results
rg -n "D033|D034|D035" project_control/DECISION_LOG.md
git fetch origin main feature/case-package-v2-external-schema
git show origin/main:project_control/MIGRATION_MASTER_PLAN.md
git show origin/main:project_control/MIGRATION_STATUS.md
git show origin/main:project_control/DECISION_LOG.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_MASTER_PLAN.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_STATUS.md
git show origin/feature/case-package-v2-external-schema:project_control/DECISION_LOG.md
```

Evidence reads:

```bash
sed -n '1,220p' audits/calcite_vs_sqlglot_noop_pg_local_comparison_v0/comparison_summary.json
sed -n '1,220p' audits/verifier_user_facing_rerun_contract_v0/open_gaps_before_final_rerun.md
sed -n '1,220p' audits/sqlsolver_pg_noop_all_exact_identity_guard_pass_v0/diagnostic_summary.json
sed -n '1,220p' audits/verieql_bound4_pg_noop_support_closeout_v0/verieql_pg_noop_support_summary.json
sed -n '1,220p' audits/user_surface_d035_layout_inventory_v0/current_user_surface_inventory.md
sed -n '1,220p' audits/common_core_tri_engine_sqlglot_noop_local_diagnostic_snapshot_v0/README.md
sed -n '1,220p' audits/sqlglot_noop_common_core_local_diagnostic_closeout_v0/README.md
sed -n '1,220p' audits/sqlglot_user_adapter_bounded_smoke_v0/README.md
sed -n '1,220p' audits/sqlglot_optimize_cons0005_triage_v0/README.md
sed -n '1,220p' audits/sqlglot_context_free_optimize_doc_warning_v0/README.md
sed -n '1,220p' baselines/sqlglot/README.md
sed -n '1,220p' baselines/calcite_hep_fail_closed/README.md
```

Validation:

```bash
python - <<'PY'
import csv
from pathlib import Path
m=Path('audits/track_a_120_rerun_readiness_plan_v0/track_a_route_engine_readiness_matrix.csv')
s=Path('audits/track_a_120_rerun_readiness_plan_v0/track_a_route_summary.csv')
with m.open(newline='') as f:
    rows=list(csv.DictReader(f))
required=['route_id','method_id','engine','planned_rows','adapter_ready','runtime_ready','user_cli_ready','candidate_generation_ready','execution_ready','checker_ready','timing_ready','local_metrics_projection_ready','verifier_rerun_ready','readiness_status','blockers','next_safe_action']
assert rows and list(rows[0].keys()) == required
assert len(rows)==21
with s.open(newline='') as f:
    rows2=list(csv.DictReader(f))
required2=['route_id','method_id','role','postgres_status','mysql_status','spark_status','all_120_ready','main_blockers','recommended_next_task']
assert rows2 and list(rows2[0].keys()) == required2
assert len(rows2)==7
PY
find audits/track_a_120_rerun_readiness_plan_v0 -type f -name "*.md" -print0 | xargs -0 -I{} sh -c 'test -s "$1" || echo empty:$1' sh {}
git status --porcelain -- runs/user output reports results src tests baselines cases case_sets schemas inventory
git diff --check
git status -sb
```

Validation result:

- `track_a_route_engine_readiness_matrix.csv` has required headers and 21 rows.
- `track_a_route_summary.csv` has required headers and 7 rows.
- Audit Markdown files are non-empty.
- Protected runtime/source/test/baseline/case/schema/inventory surfaces showed no changes.
