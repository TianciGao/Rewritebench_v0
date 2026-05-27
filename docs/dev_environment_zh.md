# 开发环境设置（Ubuntu / WSL Ubuntu）

本文档是 Chinese-first 的开发环境说明，面向想在本机运行 Rewritebench 开发检查、POCR 诊断命令和测试的协作者。这里不会配置 API key，不会启动数据库服务器，不会运行实验，也不会生成 paper-facing metric。

## 推荐版本

- 操作系统：Ubuntu 22.04 / 24.04，或 WSL Ubuntu。
- Python：系统 `python3`，建议 3.10 或更高。
- Java：OpenJDK 17，用于后续可能需要 JVM 的工具链。
- Git：使用当前分支工作流，避免直接在主分支开发。
- PostgreSQL / MySQL：默认只安装客户端 `psql` 和 `mysql`，不安装或启动数据库服务器。

## 一条命令完成安装

在仓库根目录运行：

```bash
bash scripts/setup_dev_env_ubuntu.sh
```

脚本会检查当前系统是否为 Ubuntu / WSL Ubuntu，然后安装常用开发依赖，创建或复用 `.venv`，并安装本仓库的 Python 开发依赖：

```bash
pip install -e ".[sqlglot]"
pip install pytest
```

## 一条命令完成检查

安装完成后运行：

```bash
bash scripts/check_dev_env.sh
```

检查脚本会打印 OS、kernel、Git、Python、pip、Java、`psql`、`mysql` 版本，激活 `.venv`，并运行 CLI 与 POCR 测试检查。检查报告写入本地路径：

```text
output/reports/dev_env_check_<timestamp>/environment_report.txt
```

`output/` 是本地运行输出目录，不应该提交到 Git。换句话说，output/ 是本地运行输出目录，不是 release evidence，也不是 paper-facing reports/results。

## 会安装什么

APT 包：

```text
build-essential git curl wget unzip zip jq ripgrep tree
python3 python3-venv python3-pip
openjdk-17-jdk
postgresql-client mysql-client
```

Python 包：

```text
.[sqlglot]
pytest
```

## 不会安装什么

- 不会配置 API key。
- 不会读取 `.env`。
- 不会安装、初始化或启动 PostgreSQL / MySQL 服务端。
- 不会安装完整 Spark 运行时；Spark 是可选高级设置。
- 不会运行 DB/checker/timing、baseline rerun、POCR annotation/replay/aggregation 或 official POCR。
- 不会更新 top-level `reports/` 或 `results/`。

## API key 默认不配置

本开发环境脚本只安装本地依赖。需要 live API 的任务必须单独授权，并且只能从环境变量读取 API key。不要把 API key 写入文档、脚本、日志、audit packet 或 Git。

## 数据库服务器和 Spark

默认安装的是 PostgreSQL / MySQL 客户端，便于查看版本和连接外部服务。数据库服务器、测试数据加载、Spark local mode 或集群配置都属于可选高级设置，应该在单独任务中说明和验证。

## Git 工作流

- 在指定任务分支上工作，例如 `feature/case-package-v2-external-schema`。
- 开始前运行：

```bash
pwd
git branch --show-current
git status -sb
```

- 不要使用 `git add .`。只 stage 本任务明确允许的文件。
- 不要提交 `output/`、`/tmp` 输出、凭证、API key、数据库密码或本地临时包。
- 如果工作区已有无关未跟踪文件，不要删除或回滚它们；只忽略它们。

## 常用检查命令

```bash
source .venv/bin/activate
PYTHONPATH=src python -m cli.main --help
PYTHONPATH=src python -m cli.main user pocr-diagnostic --help
PYTHONPATH=src python -m cli.main user pocr-aggregate --help
pytest tests/pocr -q
pytest tests/user_entry/test_pocr_optional_user_run_integration.py tests/user_entry/test_cli_facade.py -q
```

## 边界说明

这些脚本只帮助建立和检查开发环境。它们不定义 official POCR，不生成 paper metric，不更新报告结果，也不创建 leaderboard。POCR 相关命令仍然保持 default-off 和 diagnostic-only；任何 paper-facing promotion 都需要单独决策和授权。
