# POCR Candidate Resolver And Draft Runner v0

This packet records the implementation scaffold and diagnostic dry-run for a bounded POCR candidate-source resolver and row-level draft runner.

Implemented modules:

- `src/sql_rewrite_bench/pocr/candidate_resolver.py`
- `src/sql_rewrite_bench/pocr/draft_runner.py`
- `src/sql_rewrite_bench/pocr/json_output_guard.py`

Implemented tests:

- `tests/pocr/test_candidate_resolver.py`
- `tests/pocr/test_draft_runner.py`
- `tests/pocr/test_json_output_guard.py`

Diagnostic dry-run input:

- Candidate root: `runs/user/common_core_pg_noop_db_checker/candidate_sql/`
- Method ID: `noop_adapter`
- Route ID: `common_core_pg_noop_db_checker`
- Engine: `postgres`

Dry-run result:

- Candidate rows inspected: 40
- Candidate rows resolved: 40
- Diagnostic POCR draft rows emitted: 40
- Stage A annotation present: 0 rows
- Stage B status: `annotation_missing` for all rows
- Validated operation atoms: 0
- Official POCR computed: no
- Route-level POCR aggregated: no

Boundaries:

- No live API call.
- No API key read.
- No DB/checker/timing run.
- No baseline rerun.
- No official Positive Operation Coverage Rate computation.
- No route-level POCR aggregation.
- No user-output integration.
- No paper-facing reports/results update.
- No case package or `skills.md` modification.

Next safe action: review the diagnostic draft runner, then decide whether to add a bounded Stage B static evidence validator or a controlled user-output facade.
