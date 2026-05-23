# Command Log

Commands were read-only except for creating this audit packet and project-control writeback.

## Preflight

```bash
git status -sb
rg -n "D034|D035" project_control/DECISION_LOG.md
test -d audits/verieql_cons0007_one_pair_canary_v0
test -d audits/verieql_perf0062_one_pair_canary_v0
test -d audits/verieql_synthetic_decidable_smoke_v0
test -d audits/verieql_synthetic_from_clause_smoke_v0
test -d audits/verieql_equivalent_timeout_policy_probe_v0
test -d /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL
test -x /home/tianci_gao/.venvs/sqlrb-verieql/bin/python
git -C /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL status -sb
```

## Release Repo Reads

```bash
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,220p' project_control/MIGRATION_STATUS.md
sed -n '1,220p' project_control/MIGRATION_RUN_LOG.md
sed -n '1,220p' project_control/DECISION_LOG.md
sed -n '1,220p' repository_spec/verifier_support_output_contract_v0_draft.md
sed -n '1,220p' audits/verieql_cons0007_one_pair_canary_v0/README.md
sed -n '1,220p' audits/verieql_perf0062_one_pair_canary_v0/README.md
sed -n '1,220p' audits/verieql_synthetic_decidable_smoke_v0/README.md
sed -n '1,220p' audits/verieql_synthetic_from_clause_smoke_v0/README.md
sed -n '1,220p' audits/verieql_equivalent_timeout_policy_probe_v0/README.md
sed -n '1,260p' src/sql_rewrite_bench/verifier_support/verieql.py
sed -n '1,220p' src/sql_rewrite_bench/verifier_support/verdicts.py
sed -n '1,220p' src/sql_rewrite_bench/verifier_support/summary.py
```

## VeriEQL Source Reads

```bash
sed -n '1,260p' README.md
nl -ba constants.py | sed -n '70,100p'
nl -ba errors.py | sed -n '1,140p'
nl -ba parallel/cli_within_timeout.py | sed -n '1,190p'
nl -ba parallel/cli_within_timeout.py | sed -n '300,360p'
nl -ba parallel/cli_within_bound.py | sed -n '1,180p'
nl -ba utils.py | sed -n '1,180p'
nl -ba environment.py | sed -n '1,260p'
nl -ba parsers/constraint_parser.py | sed -n '1,220p'
nl -ba __main__.py | sed -n '1,180p'
nl -ba test/test_spj.py | sed -n '1,220p'
find benchmarks -maxdepth 3 -type f | sort
find experiments -name '*.out' -type f | sort
rg -n "NotSupportedError|EXISTS|TIMEOUT|STATE\\.EQUIV|STATE\\.TIMEOUT|bound_size|contain_unsupported_constraints" .
```

## Validation Commands

```bash
rg -n "verieql_internal_state_schema_probe_v0" project_control/MIGRATION_STATUS.md project_control/MIGRATION_RUN_LOG.md
find audits/verieql_internal_state_schema_probe_v0 -name '*.md' -type f -size 0 -print
git diff --check
git diff --name-only
git status -sb
git -C /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL status -sb
```
