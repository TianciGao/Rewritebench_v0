# Baseline 复现手册

本手册说明如何在本地复现 SQL-RewriteBench 的各类 baseline 路线。它适合第一次下载仓库的用户、审稿人和维护者使用，目标是帮助你复现以下内容：

- candidate SQL 的生成或捕获；
- 可选的数据库执行结果；
- 可选的 checker 结果一致性判断；
- 可选的计时结果；
- 本地诊断汇总表和报告。

请注意：本手册中的命令用于 **本地诊断复现**。它们不会自动生成论文中的正式结果表，不会更新发布用 `reports/` 或 `results/`，也不会生成任何全局排行榜。

本地运行输出应写入：

```text
output/results/<run_id>/
output/logs/<run_id>/
output/reports/<run_id>/
```

不要提交 `output/` 目录。

---

## 1. 第一次下载与环境准备

克隆仓库并进入工作目录：

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

命令可以通过两种方式运行。

安装后模式：

```bash
sqlrb user show-output-schema
```

源码 checkout 模式：

```bash
PYTHONPATH=src python -m cli.main user show-output-schema
```

如果 `sqlrb` 命令不可用，优先使用 `PYTHONPATH=src python -m cli.main ...`。

---

## 2. 不需要数据库的安全 smoke 命令

下面这些命令不会连接数据库，适合第一次检查仓库和 CLI 是否可用。

列出 case：

```bash
PYTHONPATH=src python -m cli.main user list-cases \
  --case-set common_core_v0 \
  --engines postgres
```

解释选择范围：

```bash
PYTHONPATH=src python -m cli.main user explain-selection \
  --case-set common_core_v0 \
  --engines postgres \
  --smoke
```

查看输出结构：

```bash
PYTHONPATH=src python -m cli.main user show-output-schema
```

dry-run 用户评测：

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

adapter-capture smoke：

```bash
PYTHONPATH=src python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --engines postgres \
  --smoke \
  --adapter-command "python examples/user/noop_adapter.py" \
  --output-root output \
  --run-id smoke_adapter_capture
```

---

## 3. 完整本地诊断需要的外部环境

如果只做 candidate SQL 捕获或 dry-run，不一定需要数据库。

如果要完整复现执行、checker 和计时，需要准备：

- PostgreSQL server/client 和 `psql`；
- MySQL server/client；
- Spark / PySpark；
- Java，供 Spark 和 Calcite 使用；
- SQLGlot，可选，仅用于 SQLGlot 路线；
- Calcite runtime，可选，仅用于 Calcite HEP 路线；
- LLM/API 配置，仅用于 LLM baseline 或 POCR live annotation；确定性 baseline 默认不需要。

Calcite HEP 可能需要这些环境变量：

```text
SQLRB_CALCITE_HEP_CMD
SQLRB_CALCITE_HEP_JAR
SQLRB_CALCITE_HEP_ROOT
SQLRB_CALCITE_HEP_JAVA
SQLRB_CALCITE_HEP_MODE
SQLRB_CALCITE_HEP_TIMEOUT
```

如果 Calcite runtime 缺失，Calcite HEP 应报告为 `preflight_blocked`。不要伪造 candidate SQL。

---

## 4. 预检清单

检查仓库状态：

```bash
pwd
git branch --show-current
git status -sb
PYTHONPATH=src python -m cli.main user show-output-schema
```

检查 Python 包能否导入：

```bash
python - <<'PY'
import sql_rewrite_bench
print("sql_rewrite_bench import ok")
PY
```

如果要运行 SQLGlot，检查 SQLGlot：

```bash
python - <<'PY'
import sqlglot
print(sqlglot.__version__)
PY
```

检查 PostgreSQL：

```bash
psql "$SQLRB_POSTGRES_DSN" -c "SELECT 1;"
```

检查 MySQL：

```bash
mysql -e "SELECT 1;"
```

检查 Spark：

```bash
python - <<'PY'
from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local[1]").appName("sqlrb-preflight").getOrCreate()
spark.sql("SELECT 1").collect()
spark.stop()
print("spark ok")
PY
```

检查 Java：

```bash
java -version
```

检查 Calcite runtime 环境：

```bash
python - <<'PY'
import os
for name in ("SQLRB_CALCITE_HEP_CMD", "SQLRB_CALCITE_HEP_JAR", "SQLRB_CALCITE_HEP_ROOT"):
    print(f"{name}={'set' if os.getenv(name) else 'missing'}")
PY
```

如果数据库不可用，你仍然可以运行 adapter-capture smoke，但不能复现执行、checker 和 timing 诊断。

---

## 5. 用户输出目录约定

本地用户运行输出应放在：

```text
output/results/<run_id>/
output/logs/<run_id>/
output/reports/<run_id>/
```

不要提交：

```text
output/
```

不要把本地用户运行输出写入：

```text
reports/
results/
cases/<POOL>/<CASE_ID>/runs/
```

`reports/` 和 `results/` 这类顶层目录用于论文、发布或人工整理后的结果，不应被普通本地运行自动更新。

当前实现内部可能会临时使用：

```text
runs/user/<run_id>/
```

但用户应把 `output/` 视为主要输出位置。

---

## 6. 通用复现命令模式

Common-core v0 包含 40 个 case。

三引擎同引擎复现范围为：

```text
40 cases × PostgreSQL/MySQL/Spark = 120 planned rows
```

确定性 baseline 的通用运行命令如下：

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

多引擎运行时，`user evaluate` 会创建按引擎拆分的 source run：

```text
<run_id>__postgres
<run_id>__mysql
<run_id>__spark
```

从这些 source run 聚合本地诊断指标：

```bash
PYTHONPATH=src python -m cli.main user compute-local-metrics \
  --run-id-prefix <run_id> \
  --engines postgres,mysql,spark \
  --aggregate-run-id <run_id> \
  --source-run-root runs/user \
  --output-root output
```

单引擎运行时，可以使用：

```bash
PYTHONPATH=src python -m cli.main user compute-local-metrics \
  --run-id <run_id> \
  --source-run-root runs/user \
  --output-root output
```

这些指标是本地诊断指标。它们不会自动更新论文结果表。

---

## 7. 计时策略

性能只在同时满足以下条件的行上解释：

```text
结果一致 exact
并且
计时成功 timed
```

speedup 方向为：

```text
source median runtime / candidate median runtime
```

也就是：

```text
大于 1 表示 candidate 更快
小于 1 表示 candidate 更慢
```

为了复现 canonical-compatible 的确定性 baseline 计时结果，建议使用：

```bash
--timing-repetitions 5
```

2 次 repetitions 可以用于 pipeline smoke，但不应替代 canonical performance values，因为计时波动较大，runtime provenance 不一致。

---

## 8. Baseline 路线

### 8.1 Source / Native Controls

Source SQL controls 是每个 case 的原始查询：

```text
sql/source.sql
```

它们用于数据库执行、checker 比较和 source timing。它们不是方法生成的 rewrite candidate。

---

### 8.2 Human Positive Controls

Human positive controls 是人工确认的正例 rewrite，通常为：

```text
sql/pos_01.sql
```

它们用于 checker 校准和 POCR control。它们不是自动方法 baseline，也不应和自动方法输出合并。

---

### 8.3 Hard-Negative Guard

Hard negatives 通常为：

```text
sql/neg_01.sql
```

它们是 checker control，用于测试 checker 是否会误接受错误 rewrite。

它们不是 method-generated candidate，也不是 POCR baseline。

---

### 8.4 SQLGlot No-Op

安装 SQLGlot：

```bash
python -m pip install -e ".[sqlglot]"
```

Adapter command：

```bash
python baselines/sqlglot/sqlglot_user_adapter.py --route noop
```

三引擎 120 行本地诊断命令示例：

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

如果 parse/emit 失败，generated rows 可能少于 120。缺失行必须保留在 manifest 和 failure buckets 中。

SQLGlot no-op 主要是低变换或基础设施稳定性路线，不应被解释成 optimizer 能力。

---

### 8.5 SQLGlot Optimize Schema-Aware

安装 SQLGlot：

```bash
python -m pip install -e ".[sqlglot]"
```

Adapter command：

```bash
python baselines/sqlglot/sqlglot_user_adapter.py --route optimize_schema_aware
```

三引擎 120 行本地诊断命令示例：

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

这条路线不能静默降级成 SQLGlot no-op，也不能静默降级成 schema-unaware optimize。

如果某些行缺失或不支持，必须在 manifests 和本地诊断中保留。

---

### 8.6 Calcite HEP Fail-Closed

Calcite HEP 需要 Java 和外部 Calcite runtime。

可能需要的环境变量：

```text
SQLRB_CALCITE_HEP_CMD
SQLRB_CALCITE_HEP_JAR
SQLRB_CALCITE_HEP_ROOT
SQLRB_CALCITE_HEP_JAVA
SQLRB_CALCITE_HEP_MODE
SQLRB_CALCITE_HEP_TIMEOUT
```

Adapter command：

```bash
python baselines/calcite_hep_fail_closed/adapter.py
```

如果 runtime environment 缺失，Calcite HEP 应报告为：

```text
preflight_blocked
```

不要伪造 candidate。不要把环境缺失解释成方法结果。

---

### 8.7 Direct LLM Original

Direct LLM original 是 LLM SQL-in/SQL-out baseline route：

```bash
python baselines/direct_llm_original/adapter.py
```

Live generation 需要显式 LLM/API 配置和显式 live gate，例如：

```text
SQLRB_LLM_ALLOW_LIVE=1
```

不要打印、提交或记录 API key。

重新运行 LLM route 可能会改变输出，除非以下信息全部冻结：

- model；
- prompt；
- decoding 参数；
- provider；
- call date；
- extraction rule；
- retry policy。

已有 candidate SQL 可能已经存在于本地 `runs/user` 或 `output/` 中。任何重新运行都只是本地诊断，除非之后单独授权提升。

---

### 8.8 Direct LLM + Repair-1

Direct LLM Repair-1 是带反馈修复的一轮 LLM route：

```bash
python baselines/direct_llm_repair_1/adapter.py
```

它使用 original candidate 和执行/错误反馈上下文。

它是独立 route，不应与 Direct LLM original 合并。exact/timed metrics 必须保留 route identity。

---

### 8.9 R-Bot Adapted GPT-5.4 PG40

R-Bot adapted GPT-5.4 是本仓库中的 PostgreSQL-only PG40 local diagnostic route。

除非使用官方 runtime、RAG、Chroma 和 CalciteRewrite 栈，并且单独授权，否则它不是 original R-Bot paper reproduction。

PG40 只能支持 PostgreSQL-only diagnostic review。

**PG40 cannot fill Track A 120.**

---

### 8.10 LLM-R2 Adapted GPT-5.4 PG40

LLM-R2 adapted GPT-5.4 是 PostgreSQL-only PG40 local diagnostic route。

除非使用官方 runtime、checkpoint、rule system 和 demonstration selector，并且单独授权，否则它不是 original LLM-R2 paper runtime。

PG40 只能支持 PostgreSQL-only diagnostic review。

**PG40 cannot fill Track A 120.**

---

### 8.11 LearnedRewrite PG40

LearnedRewrite 当前是 PostgreSQL-only external wrapper route。

当前 inventory 显示相关 manual-inspection rerun 的 PG40 candidate coverage 不完整，只有 29 个 generated candidate files。

不要为了凑齐 40 个文件而补造 candidate。

**Do not fabricate missing candidates.**

不完整 route 必须保留 missing rows。

---

### 8.12 SQLSolver / VeriEQL

SQLSolver 和 VeriEQL 是 verifier support paths，不是 rewrite-generation baselines。

它们不生成 POCR candidate SQL，也不应进入 same-engine speedup 或 POCR baseline tables。

---

## 9. Baseline Summary Table

| Baseline / route | Role | Scope | Requires DB? | Requires timing? | Requires SQLGlot? | Requires Java/Calcite? | Requires LLM/API? | Can produce candidate SQL? | Can be used for POCR diagnostic? | Promotion status |
|---|---|---|---|---|---|---|---|---|---|---|
| Source / native controls | reference source | PG/MySQL/Spark by case | yes for execution | yes for source timing | no | Spark may need Java | no | no | no | reference only |
| Human positive controls | checker/calibration control | case-local | optional | optional | no | no | no | yes, as controls | yes, as controls | not method baseline |
| Hard-negative guard | checker control | case-local | optional | no | no | no | no | no | no | not method output |
| SQLGlot no-op | deterministic baseline | 40 cases × 3 engines | yes for full diagnostics | yes for speedup | yes | no | no | yes | yes | local diagnostic unless promoted |
| SQLGlot optimize schema-aware | deterministic baseline | 40 cases × 3 engines | yes for full diagnostics | yes for speedup | yes | no | no | yes | yes | local diagnostic unless promoted |
| Calcite HEP fail-closed | deterministic external baseline | 40 cases × 3 engines if runtime configured | yes for full diagnostics | yes for speedup | no | yes | no | yes if runtime succeeds | yes | blocked if runtime env missing |
| Direct LLM original | LLM baseline | route-specific; 40 cases × 3 engines possible | yes for full diagnostics | yes for speedup | no | no | yes for generation | yes | yes | local diagnostic unless separately authorized |
| Direct LLM + Repair-1 | feedback LLM route | route-specific | yes for full diagnostics | yes for speedup | no | no | yes for generation | yes | yes | separate route only |
| R-Bot adapted GPT-5.4 PG40 | adapted prior method | PostgreSQL PG40 | yes for full diagnostics | yes for speedup | no | no | yes for live adapted route | yes | yes, PG40 only | not original paper reproduction |
| LLM-R2 adapted GPT-5.4 PG40 | adapted prior method | PostgreSQL PG40 | yes for full diagnostics | yes for speedup | no | no | yes for live adapted route | yes | yes, PG40 only | not original paper reproduction |
| LearnedRewrite PG40 | external prior method | PostgreSQL PG40, incomplete | yes for full diagnostics | yes for speedup | no | external runtime may be needed | no LLM/API in wrapper | partial currently | yes, if complete | incomplete coverage |
| SQLSolver / VeriEQL | verifier support | supported SQL pairs | no DB rerun for existing artifacts | no | no | verifier env may be needed | no | no | no | support evidence only |

---

## 10. POCR 关系

Candidate SQL 是 POCR 的输入，但 candidate SQL 本身不是 POCR 结果。

POCR diagnostic 链路是：

```text
candidate SQL
→ Stage A annotation JSONL
→ Stage B transformation-aware validation
→ diagnostic rows / summary
```

其中：

- `skills.md` 定义 case 的 operation atoms 和 semantic guard atoms；
- annotation JSONL 是某个 baseline candidate 的 Stage A 标注；
- Stage B transformation-aware validation 用来检查 annotation 的 evidence 是否能支持真实 transformation；
- semantic guard atoms 不进入 operation coverage numerator；
- POCR 目前仍是 diagnostic support，除非以后单独授权提升。

---

## 11. 常见问题

### `sqlrb` command not found

使用 checkout 模式：

```bash
PYTHONPATH=src python -m cli.main user ...
```

或者重新安装 editable package：

```bash
python -m pip install -e .
```

### 缺少 `PYTHONPATH`

在 checkout 命令前加：

```bash
PYTHONPATH=src
```

### SQLGlot 未安装

安装可选依赖：

```bash
python -m pip install -e ".[sqlglot]"
```

### PostgreSQL/MySQL/Spark 不可用

adapter-capture smoke 仍可运行。

完整 execution/checker/timing reproduction 需要先配置数据库和引擎。

### Calcite runtime 缺失

将 Calcite HEP 报告为：

```text
preflight_blocked
```

不要伪造 missing candidates。

### Zero generated candidates

检查 run workspace 和 `output/logs/<run_id>/` 中的 adapter status。

所有 missing rows 必须保留在 manifests 和 failure buckets 中。

### Timed rows missing

timing 是 exact-gated，需要同时开启：

```text
--collect-timing
--enable-db-execution
--enable-checker
```

### GM differs from canonical

检查：

- timing repetitions；
- timeout；
- runtime provenance；
- exact+timed row eligibility；
- engine environment；
- source/candidate runtime 是否来自同一次运行。

canonical deterministic SQLGlot timing 使用 5 次 measured repetitions。

### `output/` appears untracked

这是本地运行的预期结果。

**Do not commit output/.**

### POCR replay route mismatch

annotation JSONL artifacts 是 route-bound evidence。

route mismatch 必须 fail closed，不能静默复用 annotation evidence。

---

## 12. 边界

- local diagnostic reproduction only.
- No paper-facing metric is promoted.
- No global leaderboard is produced.
- Performance is interpreted only over exact+timed rows.
- PG40 cannot fill Track A 120.
- Do not fabricate missing candidates.
- Do not commit output/.
