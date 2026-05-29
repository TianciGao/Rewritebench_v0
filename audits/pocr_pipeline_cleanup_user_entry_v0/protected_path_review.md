# Protected Path Review

本任务只清理 POCR pipeline docs 和 user entry。POCR 不是 official paper metric。POCR@planned 和 POCR@candidate 仍然是 D039 promotion views。POCR@curated 暂缓。Track A 120 不是 leaderboard。

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted.

确认边界：

- no reports/results updated
- no paper files modified
- no cases/ modified
- no skills.md modified
- no candidate SQL modified
- no runs/user modified
- no output/ staged or committed
- no /tmp output staged or committed
- no denominator changed
- no case membership changed
- no paper results changed
- no raw legacy evidence changed

仅允许 staging：

- changed docs
- changed source/CLI files
- changed/added tests
- `audits/pocr_pipeline_cleanup_user_entry_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`
