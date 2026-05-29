# Command Log

Commands run for inspection and validation, with no secrets printed:

```bash
pwd
git branch --show-current
git status -sb
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,220p' project_control/MIGRATION_STATUS.md
sed -n '1,220p' project_control/DECISION_LOG.md
tail -n 80 project_control/MIGRATION_RUN_LOG.md
sed -n '1,220p' cases/LONGTAIL/LONGTAIL_0011/sql/source.sql
sed -n '1,220p' cases/LONGTAIL/LONGTAIL_0011/sql/pos_01.sql
sed -n '1,220p' cases/LONGTAIL/LONGTAIL_0011/sql/neg_01.sql
sed -n '1,260p' cases/LONGTAIL/LONGTAIL_0011/skills.md
sed -n '1,220p' cases/LONGTAIL/LONGTAIL_0011/manifest.yaml
find cases/LONGTAIL/LONGTAIL_0011/checker -maxdepth 2 -type f -print
sed -n '1,200p' cases/LONGTAIL/LONGTAIL_0011/checker/checker.yaml
sed -n '1,200p' cases/LONGTAIL/LONGTAIL_0011/checker/compare_config.yaml
sed -n '1,200p' cases/LONGTAIL/LONGTAIL_0011/checker/expected_rejections.yaml
sed -n '1,200p' cases/LONGTAIL/LONGTAIL_0011/checker/normalization.yaml
sed -n '1,120p' case_sets/common_core_v0/cases.csv
sed -n '1,200p' cases/LONGTAIL/LONGTAIL_0011/validation/run_validation.sh
git diff -- cases/LONGTAIL/LONGTAIL_0011/sql/pos_01.sql
rg -n "ORDER BY p\\.Score DESC|AS PostRank|MaxRank|rp\\.PostRank = mr\\.MaxPostRank|ORDER BY p\\.Score ASC|WorstRank|rp\\.WorstRank = 1" cases/LONGTAIL/LONGTAIL_0011/sql/pos_01.sql
git diff --name-status -- cases
git diff --name-status -- cases/LONGTAIL/LONGTAIL_0011/sql/source.sql cases/LONGTAIL/LONGTAIL_0011/sql/neg_01.sql cases/LONGTAIL/LONGTAIL_0011/skills.md cases/LONGTAIL/LONGTAIL_0011/manifest.yaml cases/LONGTAIL/LONGTAIL_0011/checker case_sets/common_core_v0/cases.csv
rg -n "ORDER BY p\\.Score DESC|AS PostRank|MaxRank|rp\\.PostRank = mr\\.MaxPostRank" cases/LONGTAIL/LONGTAIL_0011/sql/pos_01.sql
rg -n "ORDER BY p\\.Score ASC|WorstRank|rp\\.WorstRank = 1" cases/LONGTAIL/LONGTAIL_0011/sql/pos_01.sql
find audits/longtail_0011_positive_sql_correction_v0 -type f -name '*.md' -print0 | xargs -0 -I{} sh -c 'test -s "$1" || exit 1' sh {}
git diff --check
git diff --name-status
git status -sb
git diff --stat
```

Additional closeout validation commands are recorded by their effects in `validation_scope_review.md` and the project-control run log.
