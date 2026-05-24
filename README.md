# SQL-RewriteBench

SQL-RewriteBench 是一个面向 statement-level SQL rewrite 的 benchmark / workbench。它评估的是方法最终输出的完整 SQL 语句，而不是优化器内部 AST、规则 trace，或仅 parser-level 的转换结果。

## 当前公开范围

- 当前主公开分母是 `Common-core v0`。
- `Common-core v0` 包含 40 个 `case package`。
- Pool split: 16 PERF + 9 CONS + 9 PORT + 6 LONGTAIL。
- `Track A` same-engine evaluation 展开到 `PostgreSQL` / `MySQL` / `Spark SQL`，共 120 planned rows。
- `case package` 是 benchmark unit。
- 结果解释必须 role-aware 和 denominator-aware。

## Quick Smoke Run

This is the safe user-facing smoke path. It uses the `src/cli/` facade,
selects a tiny deterministic subset with `--smoke`, calls
`examples/user/noop_adapter.py`, and exports local diagnostic output to the
D035 user-output shape:

- `output/results/<run_id>/`
- `output/logs/<run_id>/`
- `output/reports/<run_id>/`

The current implementation also creates internal transitional staging under
`runs/user/<run_id>/` before export. Treat that staging directory as an
implementation detail, not the public output contract. The smoke does not
execute DB queries, run checkers, compute official metrics, update paper
results, or create leaderboard output.

Dry-run smoke:

```bash
PYTHONPATH=src python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --engines postgres \
  --smoke \
  --adapter-command "python examples/user/noop_adapter.py" \
  --output-root output \
  --run-id smoke_dry_run \
  --dry-run
```

Adapter-capture smoke:

```bash
PYTHONPATH=src python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --engines postgres \
  --smoke \
  --adapter-command "python examples/user/noop_adapter.py" \
  --output-root output \
  --run-id smoke_dummy_adapter
```

## View Cases And Output Schema

在运行 adapter 之前，可以先查看受控 case-set、解释本次选择，或查看本地输出 schema：

```bash
PYTHONPATH=src python -m cli.main user list-cases --case-set common_core_v0 --engines postgres
PYTHONPATH=src python -m cli.main user explain-selection --case-set common_core_v0 --engines postgres --smoke
PYTHONPATH=src python -m cli.main user show-output-schema
```

这些命令只读取 case-set metadata 或打印本地输出说明，不调用 adapter，不创建 user-run staging 或 exported output，不执行 DB/checker，也不计算官方指标。

## 用户算法适配器

- runner 通过环境变量把 source SQL 路径、case 信息和 candidate 输出路径传给 adapter。
- adapter 写出 candidate SQL，或把 candidate SQL 打印到 stdout。
- 示例 adapter 位于 `examples/user/noop_adapter.py`。
- adapter capture 只记录候选输出，不代表语义正确、性能提升或官方结果。

## After A Run

The user-facing output is exported under:

- `output/results/<run_id>/`: selected rows, ledgers, manifests, candidate SQL, and machine-readable local diagnostics.
- `output/logs/<run_id>/`: run configuration, adapter logs, failure-bucket diagnostics, and copied local logs.
- `output/reports/<run_id>/`: human-readable local summaries and boundary reports.

`runs/user/<run_id>/` may still exist as internal transitional staging created by
the current implementation before export. Do not treat it as the public output
root and do not commit it. More complete data-flow details are in
[`docs/USER_ENTRY_DATA_FLOW.md`](docs/USER_ENTRY_DATA_FLOW.md).

## 可选本地 PostgreSQL 诊断

- 可选 DB/checker diagnostics 是 opt-in。
- 使用 `--enable-db-execution` 和可选 `--enable-checker`。
- 当前路径是 external-schema aware：PostgreSQL DDL/load 通过 `manifest.yaml` 中的 `schema.external_profile` 解析。
- 这是本地诊断，不是完整论文复现，不是官方 metrics，不写 top-level `reports/` 或 `results/`。

## 如何阅读一个 case package

一个 `case package` 通常包含：

- `README.md`
- `manifest.yaml`
- `sql/source.sql`
- `sql/pos_01.sql`
- `sql/neg_01.sql` when declared
- `schema/schema_profile.yaml`
- `checker/`
- `validation/`

`manifest.yaml` 是 package manifest，记录 source-family、provenance、taxonomy、SQL 路径、schema profile、checker、validation entrypoint 和证据策略等信息。`Common-core v0` membership 由 `case_sets/` 管理，而不是由物理目录或 case README 单独定义。

## 仓库主要目录

- `cases/`: case packages。
- `case_sets/`: 受控 case membership、denominator 和 control scaffolds。
- `schemas/`: external schema profiles 与 engine-specific DDL/load assets。
- `src/`: Python package implementation。
- `scripts/`: developer/user entry scripts。
- `examples/`: public examples, including user adapter smoke examples。
- `docs/`: user-facing and maintainer-facing documentation。
- `audits/`: release-construction audit packets and planning records。
- `project_control/`: release construction status and decision control files。
- `runs/`: internal transitional user-run staging or retained legacy evidence depending on location and policy。

User-facing exported output should use `output/results/<run_id>/`,
`output/logs/<run_id>/`, and `output/reports/<run_id>/`. Ordinary user-run
tasks must not write to top-level `reports/` or `results/`; those remain
official/paper surfaces that require separate authorization. Current
`cases/`, `case_sets/`, `schemas/`, and `inventory/` paths remain valid working
paths until a separately authorized physical migration moves them toward the
final public `benchmarks/` target.

## 重要边界

- `Common-core v0` 是受控覆盖面，不是生产 SQL 频率样本。
- hard negatives 是 checker controls，不是 method-generated candidates。
- performance 只能在 exact + timed rows 上解释。
- PORT bounded evidence 不能写成 full PORT9 closure。
- `SpeedupTransferRate` 当前不计算。
- verifier support 不是 rewrite-generation baseline。
- 本仓库不提供全局 leaderboard。
- user smoke outputs 只是本地 diagnostics。
- `PERF_0077` 和 `PERF_0082` 保留 nonblocking source-path provenance uncertainty；不要声称恢复了 exact JOB source paths。

## 更多文档

- [User benchmark guide](docs/USER_BENCHMARK_GUIDE.md)
- [User quickstart](docs/guide/user_quickstart.md)
- [Output contract](docs/spec/output_contract.md)
- [CLI contract](docs/spec/cli_contract.md)
- [Common-core v0 case set](case_sets/common_core_v0/)
- [Project control](project_control/)
