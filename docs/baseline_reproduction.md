# Baseline 复现手册

本手册说明 SQL-RewriteBench 各类 baseline route 的本地诊断复现路径。它面向第一次下载仓库的用户、审稿人和维护者，帮助他们在 D035 输出结构下复现 candidate SQL 捕获、可选执行/检查状态、可选计时结果，以及本地诊断汇总。

本手册只用于 **local diagnostic reproduction**。它不会创建官方指标，不会更新 paper-facing `reports/` 或 `results/`，不会提升 retained evidence，也不会生成全局排行榜。**No paper-facing metric is promoted. No global leaderboard is produced.**

用户运行输出应使用 D035 风格的输出根目录：

```text
output/results/<run_id>/
output/logs/<run_id>/
output/reports/<run_id>/
```

## 第一次下载与环境准备

克隆并进入仓库：

```bash
git clone https://github.com/TianciGao/Rewritebench_v0.git
cd Rewritebench_v0
git checkout feature/case-package-v2-external-schema
```

使用 Python 3.10 或更高版本，创建并激活虚拟环境：

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .
```

如果要运行 SQLGlot 路线，再安装 SQLGlot 可选依赖：

```bash
python -m pip install -e ".[sqlglot]"
```

命令既可以通过安装后的 `sqlrb` 使用，也可以在源码 checkout 模式下使用：

```bash
sqlrb user show-output-schema
PYTHONPATH=src python -m cli.main user show-output-schema
```

不需要数据库引擎的安全 smoke 命令：

```bash
PYTHONPATH=src python -m cli.main user list-cases \
  --case-set common_core_v0 \
  --engines postgres

PYTHONPATH=src python -m cli.main user explain-selection \
  --case-set common_core_v0 \
  --engines postgres \
  --smoke

PYTHONPATH=src python -m cli.main user show-output-schema

PYTHONPATH=src python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --engines postgres \
  --smoke \
  --adapter-command "python examples/user/noop_adapter.py" \
  --output-root output \
  --run-id smoke_dry_run \
  --dry-run

PYTHONPATH=src python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --engines postgres \
  --smoke \
  --adapter-command "python examples/user/noop_adapter.py" \
  --output-root output \
  --run-id smoke_adapter_capture
```

完整本地诊断需要额外准备：

- PostgreSQL server/client 和 `psql`。
- MySQL server/client。
- Spark / PySpark。
- Spark 和 Calcite 所需的 Java。
- 如需运行 Calcite HEP，需要配置 Calcite 运行环境：
  - `SQLRB_CALCITE_HEP_CMD`
  - `SQLRB_CALCITE_HEP_JAR`
  - `SQLRB_CALCITE_HEP_ROOT`
- 如需运行 SQLGlot 路线，需要安装 SQLGlot 可选依赖。
- 确定性 baseline 不需要 LLM/API 配置，也不应默认使用 LLM/API。

如果你在本地记录 OS 安装命令，请把它们标为 Ubuntu/WSL 示例环境配置，而不是 benchmark 必需命令。

## 预检清单

仓库与 CLI：

```bash
pwd
git branch --show-current
git status -sb
PYTHONPATH=src python -m cli.main user show-output-schema
python - <<'PY'
import sql_rewrite_bench
print("sql_rewrite_bench import ok")
PY
```

如果需要 SQLGlot，检查 SQLGlot 是否可用：

```bash
python - <<'PY'
import sqlglot
print(sqlglot.__version__)
PY
```

PostgreSQL 可用性：

```bash
psql "$SQLRB_POSTGRES_DSN" -c "SELECT 1;"
```

MySQL 可用性：

```bash
mysql -e "SELECT 1;"
```

Spark 可用性：

```bash
python - <<'PY'
from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local[1]").appName("sqlrb-preflight").getOrCreate()
spark.sql("SELECT 1").collect()
spark.stop()
print("spark ok")
PY
```

Java 可用性：

```bash
java -version
```

如需 Calcite，检查 Calcite 运行环境：

```bash
python - <<'PY'
import os
for name in ("SQLRB_CALCITE_HEP_CMD", "SQLRB_CALCITE_HEP_JAR", "SQLRB_CALCITE_HEP_ROOT"):
    print(f"{name}={'set' if os.getenv(name) else 'missing'}")
PY
```

如果数据库引擎不可用，仍可运行 adapter-capture smoke，但不能复现 execution/checker/timing 诊断。如果 Calcite runtime environment 缺失，Calcite HEP 必须报告为 `preflight_blocked`，不能伪造 candidate。

## 用户输出约定

用户侧输出应放在：

```text
output/results/<run_id>/
output/logs/<run_id>/
output/reports/<run_id>/
```

**Do not commit output/.** 不要把本地用户运行输出写入顶层 `reports/` 或顶层 `results/`。不要把新的运行输出写入 case-local `runs/`。

当前实现可能会在内部过渡性使用 `runs/user/<run_id>/` staging，再导出到 D035 风格的 `output/`。对用户而言，`output/` 是公开的用户侧输出表面。

## 通用命令模式

Track A same-engine 复现基于 Common-core v0：

```text
40 cases × PostgreSQL/MySQL/Spark = 120 planned rows
```

确定性 baseline 的通用运行命令：

```bash
PYTHONPATH=src python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --engines postgres,mysql,spark \
  --adapter-command "<adapter command>" \
  --output-root output \
  --run-id <run_id> \
  --enable-db-execution \
  --enable-checker \
  --collect-timing \
  --timing-repetitions 5 \
  --timing-timeout 30
```

多引擎运行时，`user evaluate` 会创建按引擎拆分的 source run ids：

```text
<run_id>__postgres
<run_id>__mysql
<run_id>__spark
```

从这些已有 source runs 聚合非官方本地诊断指标：

```bash
PYTHONPATH=src python -m cli.main user compute-local-metrics \
  --run-id-prefix <run_id> \
  --engines postgres,mysql,spark \
  --aggregate-run-id <run_id> \
  --source-run-root runs/user \
  --output-root output
```

单引擎运行时：

```bash
PYTHONPATH=src python -m cli.main user compute-local-metrics \
  --run-id <run_id> \
  --source-run-root runs/user \
  --output-root output
```

这些都是本地诊断指标。**No paper-facing metric is promoted.**

## Canonical 计时策略

**Performance is interpreted only over exact+timed rows.**

Speedup 方向为：

```text
source median runtime / candidate median runtime
```

canonical SQLGlot 确定性路线使用 5 次 measured repetitions。为了复现 canonical-compatible 本地诊断，请使用：

```bash
--timing-repetitions 5
```

2 次 repetitions 的运行可以用于 pipeline smoke，但不应替代 canonical performance values，因为 timing provenance 不一致。

## Baseline 路线

### Source / Native Controls

Source SQL controls 是 case-local `sql/source.sql` 查询。它们是执行、checker 比较和 source timing 的参考输入，不是 method-generated rewrite candidates。

### Human Positive Controls

Human positive controls 是 case-local positive rewrites，通常为 `sql/pos_01.sql`。它们用于 checker 校准和 POCR control，不是自动重写 baseline，也不应与方法 route 输出合并。

### Hard-Negative Guard

Hard negatives 通常为 `sql/neg_01.sql`，它们是 checker controls。它们不是 method-generated candidates，也不是 POCR baseline。

### SQLGlot No-Op

安装 SQLGlot 支持：

```bash
python -m pip install -e ".[sqlglot]"
```

Adapter command：

```bash
python baselines/sqlglot/sqlglot_user_adapter.py --route noop
```

Track A 120 本地诊断命令示例：

```bash
PYTHONPATH=src python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --engines postgres,mysql,spark \
  --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" \
  --output-root output \
  --run-id sqlglot_noop_track_a_120_local \
  --enable-db-execution \
  --enable-checker \
  --collect-timing \
  --timing-repetitions 5 \
  --timing-timeout 30
```

如果 parse/emit 失败，generated rows 可能少于 120。缺失行必须保留在 manifest 和 failure buckets 中。candidate outputs 和 metrics 只是 local diagnostic，除非后续单独授权提升。

### SQLGlot Optimize Schema-Aware

安装 SQLGlot 支持：

```bash
python -m pip install -e ".[sqlglot]"
```

Adapter command：

```bash
python baselines/sqlglot/sqlglot_user_adapter.py --route optimize_schema_aware
```

Track A 120 本地诊断命令示例：

```bash
PYTHONPATH=src python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --engines postgres,mysql,spark \
  --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route optimize_schema_aware" \
  --output-root output \
  --run-id sqlglot_optimize_schema_aware_track_a_120_local \
  --enable-db-execution \
  --enable-checker \
  --collect-timing \
  --timing-repetitions 5 \
  --timing-timeout 30
```

这条路线不能静默降级成 SQLGlot no-op 或 schema-unaware optimize。missing 和 unsupported rows 必须继续在 manifests 和本地诊断中可见。

### Calcite HEP Fail-Closed

Calcite HEP 需要 Java 和外部 Calcite runtime。仓库 adapter 通过以下环境变量发现 runtime 配置：

- `SQLRB_CALCITE_HEP_CMD`
- `SQLRB_CALCITE_HEP_JAR`
- `SQLRB_CALCITE_HEP_ROOT`
- `SQLRB_CALCITE_HEP_JAVA`
- `SQLRB_CALCITE_HEP_MODE`
- `SQLRB_CALCITE_HEP_TIMEOUT`

Adapter command：

```bash
python baselines/calcite_hep_fail_closed/adapter.py
```

如果 runtime environment 缺失，Calcite HEP 应报告为 `preflight_blocked`。**Do not fabricate missing candidates.**

### Direct LLM Original

Direct LLM original 是 LLM SQL-in/SQL-out baseline route：

```bash
python baselines/direct_llm_original/adapter.py
```

Live generation 需要显式用户侧 LLM/API 配置，以及类似下面这样的显式 live gate：

```text
SQLRB_LLM_ALLOW_LIVE=1
```

不要暴露 API keys。重新运行 LLM route 可能会改变输出，除非 model、prompt、decoding、provider 和 call metadata 都被冻结。已有 candidate SQL artifacts 可能已经存在于本地 `runs/user` 或 D035 `output/` roots。任何 rerun 都只是 local diagnostic，除非单独授权。

### Direct LLM + Repair-1

Direct LLM Repair-1 是 feedback-enhanced LLM route：

```bash
python baselines/direct_llm_repair_1/adapter.py
```

它消耗 explicit original-candidate 和 feedback context。它是独立 route，不应与 Direct LLM original 合并。exact/timed metrics 必须保留 route identity。

### R-Bot Adapted GPT-5.4 PG40

R-Bot adapted GPT-5.4 是本仓库里的 PostgreSQL-only PG40 local diagnostic route。除非使用官方 runtime、RAG、Chroma 和 CalciteRewrite 栈并单独授权，否则它不是 original R-Bot paper reproduction。

**PG40 cannot fill Track A 120.** inventory 中的 candidate roots 可以支持 PostgreSQL-only diagnostic review，但不能替代 tri-engine Track A evidence。

### LLM-R2 Adapted GPT-5.4 PG40

LLM-R2 adapted GPT-5.4 是 PostgreSQL-only PG40 local diagnostic route。除非使用官方 runtime、checkpoint、rule system 和 demonstration selector 并单独授权，否则它不是 original LLM-R2 paper runtime。

**PG40 cannot fill Track A 120.**

### LearnedRewrite PG40

LearnedRewrite 当前是本仓库里的 PostgreSQL-only external wrapper route。当前 inventory 显示相关 manual-inspection rerun 的 PG40 candidate coverage 不完整，只有 29 个 generated candidate files。

**Do not fabricate missing candidates.** 不完整 route 必须保留 missing rows。

### SQLSolver / VeriEQL

SQLSolver 和 VeriEQL 是 verifier support paths，不是 rewrite-generation baselines。它们不会为 POCR 生成 candidate SQL，也不应进入 same-engine speedup 或 POCR baseline tables。

## Baseline Summary Table

| Baseline / route | Role | Scope | Requires DB? | Requires timing? | Requires SQLGlot? | Requires Java/Calcite? | Requires LLM/API? | Can produce candidate SQL? | Can be used for POCR diagnostic? | Paper-facing promotion status |
|---|---|---|---|---|---|---|---|---|---|---|
| Source / native controls | reference source | PG/MySQL/Spark by case | yes for execution | yes for source timing | no | Spark may need Java | no | no | no | reference only |
| Human positive controls | checker/calibration control | case-local | optional | optional | no | no | no | yes, as controls | yes, as controls | not method baseline |
| Hard-negative guard | checker control | case-local | optional | no | no | no | no | no | no | not method output |
| SQLGlot no-op | deterministic baseline | Track A 120 when engines available | yes for full diagnostics | yes for speedup | yes | no | no | yes | yes | local diagnostic unless promoted |
| SQLGlot optimize schema-aware | deterministic baseline | Track A 120 when engines/schema supported | yes for full diagnostics | yes for speedup | yes | no | no | yes | yes | local diagnostic unless promoted |
| Calcite HEP fail-closed | deterministic external baseline | Track A 120 only when runtime configured | yes for full diagnostics | yes for speedup | no | yes | no | yes if runtime succeeds | yes | blocked if runtime env missing |
| Direct LLM original | LLM baseline | route-specific; Track A possible with live config | yes for full diagnostics | yes for speedup | no | no | yes for generation | yes | yes | local diagnostic unless separately authorized |
| Direct LLM + Repair-1 | feedback LLM route | route-specific | yes for full diagnostics | yes for speedup | no | no | yes for generation | yes | yes | separate route only |
| R-Bot adapted GPT-5.4 PG40 | adapted prior method | PostgreSQL PG40 | yes for full diagnostics | yes for speedup | no | no | yes for live adapted route | yes | yes, PG40 only | not original paper reproduction |
| LLM-R2 adapted GPT-5.4 PG40 | adapted prior method | PostgreSQL PG40 | yes for full diagnostics | yes for speedup | no | no | yes for live adapted route | yes | yes, PG40 only | not original paper reproduction |
| LearnedRewrite PG40 | external prior method | PostgreSQL PG40, incomplete | yes for full diagnostics | yes for speedup | no | Java external runtime | no LLM/API in wrapper | partial currently | yes, if complete | incomplete coverage |
| SQLSolver / VeriEQL | verifier support | exact candidate subsets | no DB rerun for existing artifacts | no | no | Java/Python verifier env | no | no | no | support evidence only |

## POCR 关系

Candidate SQL 是 POCR 的输入。Candidate SQL 本身不是 annotation JSONL。annotation JSONL 需要 Stage A annotation。Stage B transformation-aware validation 是 diagnostic operation support 的必要步骤。POCR 仍然是 diagnostic，除非之后单独授权提升。

## 常见问题

`sqlrb` command not found：

- 使用 checkout 模式：`PYTHONPATH=src python -m cli.main user ...`。
- 或重新安装 editable package：`python -m pip install -e .`。

缺少 `PYTHONPATH`：

- 在 checkout 命令前加 `PYTHONPATH=src`。

SQLGlot 未安装：

- 安装可选依赖：`python -m pip install -e ".[sqlglot]"`。

PostgreSQL/MySQL/Spark 不可用：

- adapter-capture smoke 仍可运行。
- full execution/checker/timing reproduction 需要先配置好数据库/引擎。

Calcite runtime 缺失：

- 将 Calcite HEP 报告为 `preflight_blocked`。
- 不要伪造 missing candidates。

Zero generated candidates：

- 检查 run workspace 和 D035 logs 中的 adapter status。
- 所有 missing rows 必须保留在 manifests 和 failure buckets 中。

Timed rows missing：

- timing 是 exact-gated，并且需要同时开启：
  - `--collect-timing`
  - `--enable-db-execution`
  - `--enable-checker`

GM differs from canonical：

- 检查 timing repetitions、timeout、runtime provenance、exact+timed row eligibility 和 engine environment。canonical deterministic SQLGlot timing 使用 5 次 measured repetitions。

`output/` appears untracked：

- 这是本地运行的预期结果。**Do not commit output/.**

POCR replay route mismatch：

- annotation JSONL artifacts 是 route-bound evidence。route mismatch 必须 fail closed，不能静默复用 annotation evidence。

## 边界

- local diagnostic reproduction only.
- No paper-facing metric is promoted.
- No global leaderboard is produced.
- Performance is interpreted only over exact+timed rows.
- PG40 cannot fill Track A 120.
- Do not fabricate missing candidates.
- Do not commit output/.
