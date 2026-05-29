# Command Log

Preflight:

```bash
git status -sb
git branch --show-current
git status --porcelain -- runs/user output reports results
test -d audits/sqlglot_noop_pg_current_route_card_refresh_v0
test -d audits/calcite_hep_pg_post_quoting_chain_rerun_v0
test -f audits/sqlglot_noop_pg_current_route_card_refresh_v0/route_card.json
test -f audits/sqlglot_noop_pg_current_route_card_refresh_v0/route_card.csv
test -f audits/calcite_hep_pg_post_quoting_chain_rerun_v0/route_card.json
test -f audits/calcite_hep_pg_post_quoting_chain_rerun_v0/route_card.csv
rg -n "D033|D034|D035" project_control/DECISION_LOG.md
git fetch origin main feature/case-package-v2-external-schema
git merge-base --is-ancestor 35a97d620eee82cdd0235bb941f9ee4b3a8c47bf HEAD
git merge-base --is-ancestor b261ee0bde85856ae57bc4e310eadb0fcbdc6cf2 HEAD
```

Input reads:

```bash
sed -n '1,220p' audits/sqlglot_noop_pg_current_route_card_refresh_v0/route_card.json
sed -n '1,240p' audits/calcite_hep_pg_post_quoting_chain_rerun_v0/route_card.json
sed -n '1,120p' audits/sqlglot_noop_pg_current_route_card_refresh_v0/route_card.csv
sed -n '1,120p' audits/calcite_hep_pg_post_quoting_chain_rerun_v0/route_card.csv
sed -n '1,220p' audits/sqlglot_noop_pg_current_route_card_refresh_v0/non_exact_frontier.md
sed -n '1,240p' audits/calcite_hep_pg_post_quoting_chain_rerun_v0/non_exact_frontier.md
```

Validation:

```bash
python -m json.tool audits/calcite_vs_sqlglot_noop_pg_local_comparison_v0/comparison_summary.json
python - <<'PY'
import csv
from pathlib import Path
path=Path('audits/calcite_vs_sqlglot_noop_pg_local_comparison_v0/comparison_table.csv')
with path.open(newline='') as f:
    rows=list(csv.DictReader(f))
assert len(rows)==2
required={'route_id','method_id','engine','selected_rows','generated_candidate_rows','no_candidate_rows','execution_attempted_rows','source_executable_rows','candidate_executable_rows','checker_attempted_rows','exact_rows','timed_exact_rows','timing_failed_rows','local_generation_rate','local_execution_coverage_rate','local_result_consistency_rate','diagnostic_gm_speedup','diagnostic_speedup_p10','diagnostic_speedup_p25','diagnostic_speedup_p50','diagnostic_speedup_p75','diagnostic_speedup_p90','frontier_summary','official_metric_input','paper_result','leaderboard_output_created'}
assert required.issubset(rows[0].keys())
PY
find audits/calcite_vs_sqlglot_noop_pg_local_comparison_v0 -type f -name "*.md" -print0 | xargs -0 -I{} sh -c 'test -s "$1" || echo empty:$1' sh {}
git status --porcelain -- runs/user output reports results src tests baselines cases case_sets
git diff --check
git status -sb
```

Validation result:

- `comparison_summary.json` parses.
- `comparison_table.csv` has 2 rows and required headers.
- Audit Markdown files are non-empty.
- Protected runtime/source/test/baseline/case surfaces showed no changes.
