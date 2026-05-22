# Active Control Files After Hygiene

After this hygiene pass, `project_control/` is reserved for four active durable control files:

- `project_control/MIGRATION_MASTER_PLAN.md`: stable global migration rules.
- `project_control/MIGRATION_STATUS.md`: current snapshot and next safe action.
- `project_control/MIGRATION_RUN_LOG.md`: chronological execution history.
- `project_control/DECISION_LOG.md`: durable policy and roadmap decisions.

No `ACTIVE_KEEP_WITH_REASON` files remain under top-level `project_control/`.
