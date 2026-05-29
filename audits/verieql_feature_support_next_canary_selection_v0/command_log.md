# Command Log

Commands were read-only except for creating this audit packet and project-control writeback.

```bash
git status -sb && git branch --show-current
git status -sb
rg -n "D034|D035" project_control/DECISION_LOG.md
sed -n '1,180p' cases/PERF/PERF_0062/sql/source.sql
sed -n '1,180p' cases/PERF/PERF_0062/sql/pos_01.sql
sed -n '1,180p' cases/PORT/PORT_0024/sql/source.sql
sed -n '1,180p' cases/PORT/PORT_0024/sql/pos_01.sql
sed -n '1,220p' cases/CONS/CONS_0036/sql/source.sql
sed -n '1,220p' cases/CONS/CONS_0036/sql/pos_01.sql
sed -n '1,80p' case_sets/common_core_v0/cases.csv
python - <<'PY'
# Static Common-core source_vs_positive feature scan printed CSV to stdout.
PY
rg -n "NotSupportedError|Not supported feature|EXISTS|OVER|Subquery|TIMESTAMPDIFF|Interval|stddev|var_pop|var_samp|IFNULL|COUNT" /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL -g '*.py'
sed -n '1,220p' /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL/README.md
sed -n '1,160p' audits/verieql_cons0007_one_pair_canary_v0/raw_output_review.md
sed -n '1,160p' audits/verieql_cons0007_one_pair_canary_v0/normalized_verdict_review.md
```

No command in this task invoked VeriEQL verification. No SQLSolver command was run. No database execution was run.

Validation commands:

```bash
git diff --check
python - <<'PY'
# Check audit Markdown files are non-empty.
PY
python - <<'PY'
# Read candidate_pair_scan.csv with csv.DictReader and assert 40 rows.
PY
python - <<'PY'
# Inspect git diff/untracked paths and assert no protected-surface paths changed.
PY
git status -sb
```
