# 实现摘要

本任务添加两个顶层开发脚本：

- `scripts/setup_dev_env_ubuntu.sh`：要求 Ubuntu / WSL Ubuntu，安装基础 apt 包、Python venv、`.[sqlglot]` 和 `pytest`，最后打印后续命令。
- `scripts/check_dev_env.sh`：激活 `.venv`，打印 OS/kernel/git/python/pip/java/psql/mysql 版本，运行 CLI help 和 POCR/user-entry 测试，并把本地检查报告写入 `output/reports/dev_env_check_<timestamp>/environment_report.txt`。

同时新增 `docs/dev_environment_zh.md`，用中文优先说明推荐版本、一键安装、一键检查、安装与不安装内容、API key 边界、可选数据库/Spark 设置、`output/` 不提交、不要使用 `git add .`、协作者分支工作流。

本任务不修改 POCR metric 语义，不新增实验入口，不读取 API key，不更新 top-level `reports/` 或 `results/`。
