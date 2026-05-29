# 开发环境 bootstrap 脚本审计

本审计记录 `dev_environment_bootstrap_scripts_v0`。本任务新增轻量开发环境脚本和 Chinese-first 设置文档，不运行实验，不调用 live API，不运行 DB/checker/timing，不运行 baseline rerun，也不执行 POCR annotation/replay/aggregation。

新增内容：

- `scripts/setup_dev_env_ubuntu.sh`
- `scripts/check_dev_env.sh`
- `docs/dev_environment_zh.md`

边界：

- No official POCR was computed.
- No route-level official POCR score was emitted.
- No paper-facing metric was promoted.
- No reports/results update occurred.
- `output/` 仍然是本地运行输出目录，不提交。
