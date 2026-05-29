# Boundary Checklist

- Full Track A 120 run: no.
- Canonical metrics run: no.
- `compute-local-metrics`: no.
- Timing: no.
- SQLSolver / VeriEQL: no.
- SQLGlot or LLM baselines: no.
- Official metrics: no.
- Official Semantic Equivalence Rate: no.
- Formal Regression@20: no.
- Paper reports/results update: no.
- Retained evidence promotion: no.
- Leaderboard output: no.
- Denominator change: no.
- Case membership change: no.
- Case SQL changes: no.
- Schema changes: no.
- Release-repo external Calcite artifact commit: no.
- Runtime artifact commit: no.

Allowed repository changes used:

- `baselines/calcite_hep_fail_closed/adapter.py`
- `baselines/calcite_hep_fail_closed/README.md`
- `tests/user_entry/test_calcite_hep_fail_closed_route.py`
- `audits/calcite_hep_target_dialect_runtime_mode_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Allowed external staging used:

- `/home/tianci_gao/.local/share/sqlrb/calcite_hep/src/CalciteHepRewriteSmoke.java`
- `/home/tianci_gao/.local/share/sqlrb/calcite_hep/classes/`
