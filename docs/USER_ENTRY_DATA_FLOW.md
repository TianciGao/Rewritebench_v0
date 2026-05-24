# 用户入口数据流与文件位置

本文说明当前 user-entry / smoke runner 的数据流。它不是完整论文复现说明，也不定义官方 metrics、paper tables、retained evidence 或 leaderboard。

## 一句话流程

`sqlrb user evaluate` 参数 -> `case_sets/common_core_v0/` -> `cases/{POOL}/{CASE_ID}/sql/source.sql` -> adapter -> internal staging under `runs/user/{run_name}/` -> D035 export under `output/results|logs|reports/{run_name}/`

## 入口文件

| 阶段 | 文件或目录 | 说明 |
|---|---|---|
| public CLI facade | `src/cli/main.py` | `sqlrb user ...` and `python -m cli.main user ...` 的公开入口。 |
| internal runner | `src/sql_rewrite_bench/user_run.py` | 当前实现的 source-run staging pipeline；由 `src/cli/` facade 调用。 |
| output exporter | `src/sql_rewrite_bench/user_output.py` | 将 internal staging 映射到 D035 `output/results|logs|reports/<run_id>/`。 |
| legacy thin wrapper | `scripts/user/run_user_benchmark.py` | 兼容的低层 wrapper；不定义 D035 public output contract。 |
| 示例 adapter | `examples/user/noop_adapter.py` | 公开 smoke 示例 adapter。 |

## case 选择

| 阶段 | 文件或目录 | 说明 |
|---|---|---|
| case selection implementation | `src/sql_rewrite_bench/case_selection.py` | 从 `case_sets/common_core_v0/` 的 case-set CSV 解析选择；不通过扫描 `cases/` 目录决定 membership。 |
| case-set membership file | `case_sets/common_core_v0/cases.csv` | 定义 40 个 Common-core case package 及 package path。 |
| Track A denominator file | `case_sets/common_core_v0/denominator_same_engine_120.csv` | 定义 120 个 planned same-engine case-engine rows。 |

## case package 输入

| 阶段 | 文件或目录 | 说明 |
|---|---|---|
| case package root | `cases/{POOL}/{CASE_ID}/` | 单个 benchmark unit 的 package 根目录。 |
| source SQL | `cases/{POOL}/{CASE_ID}/sql/source.sql` | 通过 `SQLRB_SOURCE_SQL_PATH` 传给 adapter。 |
| package manifest | `cases/{POOL}/{CASE_ID}/manifest.yaml` | 记录 package manifest、provenance、SQL、schema、checker 和 validation references。 |
| schema profile | `cases/{POOL}/{CASE_ID}/schema/schema_profile.yaml` | case-facing schema summary；不是用户输出目录。 |
| external schema package | `schemas/{schema_id}/...` | PostgreSQL DDL/load 从 `schema.external_profile` 和 external profile metadata 解析；不要硬编码固定 schema 文件名。 |

## adapter 合约

Runner 会为每次 adapter 调用提供这些环境变量：

- `SQLRB_SOURCE_SQL_PATH`
- `SQLRB_CANDIDATE_SQL_PATH`
- `SQLRB_WORKSPACE_DIR`
- `SQLRB_RUN_ID`
- `SQLRB_CASE_ID`
- `SQLRB_POOL`
- `SQLRB_ENGINE`
- `SQLRB_CASE_DIR`

Adapter 从 `SQLRB_SOURCE_SQL_PATH` 读取 source SQL，并把 candidate SQL 写到 `SQLRB_CANDIDATE_SQL_PATH`。Candidate 捕获优先级是 workspace `candidate.sql` 优先，stdout 次之。

## User-facing Exported Output

| 输出 | 位置 | 说明 |
|---|---|---|
| result root | `output/results/{run_name}/` | selected rows, ledger, copied candidate SQL, run manifest, local metrics files, and machine-readable diagnostics. |
| log root | `output/logs/{run_name}/` | run config, adapter workspaces, failure-bucket diagnostics, and copied local logs. |
| report root | `output/reports/{run_name}/` | human-readable local summaries and boundary reports. |
| optional PostgreSQL diagnostic helper | `src/sql_rewrite_bench/postgres_execution.py` | opt-in DB diagnostic helper；默认 smoke 不使用。 |
| optional checker helper | `src/sql_rewrite_bench/local_result_checker.py` | opt-in local checker diagnostic helper；默认 smoke 不使用。 |
| output schema / typed row model | `src/sql_rewrite_bench/user_run_schema.py` | 定义 local ledger/status 字段和值域。 |

## Internal Transitional Staging

`runs/user/{run_name}/` is still used by the current implementation as an
internal source-run staging workspace before D035 export. It commonly contains
`selected_cases.csv`, `config.yaml`, `candidate_sql/`, `workspaces/`,
`ledger.csv`, `summary.json`, `failures.csv`, and `report.md`.

This staging path is not the public-facing output contract and must not be
committed. User documentation should point readers to `output/results/<run_id>/`,
`output/logs/<run_id>/`, and `output/reports/<run_id>/` for exported output.

## 可选 PostgreSQL / checker 诊断

- 默认 smoke 不执行 DB query，不运行 checker。
- `--enable-db-execution` 是 opt-in。
- `--enable-checker` 是 opt-in。
- PostgreSQL DDL/load 通过 manifest `schema.external_profile` 和 external schema metadata 解析。
- 缺 metadata 时 fail closed。
- 这些输出仍是本地 diagnostics，不是官方 metrics、paper tables、top-level reports/results 或 leaderboard。

## 边界

- user-entry outputs are local diagnostics only。
- no official metrics。
- no paper table rendering。
- no top-level reports/results updates。
- no retained evidence creation。
- no global leaderboard。
- no full paper reproduction claim。
