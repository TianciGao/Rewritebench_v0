# Command Log

Initial checks:
- `pwd && git branch --show-current && git status -sb --untracked-files=normal`
- Read project control files: MIGRATION_MASTER_PLAN, MIGRATION_STATUS, DECISION_LOG, MIGRATION_RUN_LOG.
- Read required POCR audit packets, candidate inventories, `case_sets/common_core_v0/cases.csv`, `stage_b_row_metrics.py`, `pocr_aggregator.py`, checkpointed annotation/replay modules, and tests.

Metric-definition checkpoint:
- Follows D039.
- POCR@planned and POCR@candidate remain promotion-diagnostic views.
- POCR@curated remains NA / curated_manifest_missing until a predeclared curated manifest exists.
- Macro-average over per-row OC_i is the formula.
- Diagnostic micro-average is not the paper formula.
- Expected atoms come only from operation_atom entries in case-local root-level skills.md.
- semantic_guard_atom is excluded from numerator and denominator.
- Implemented atoms come only from Stage-B transformation-supported operation atoms.
- Stage A annotation alone is not counted.
- candidate/source/positive span presence alone is not enough.
- source-to-candidate transformation evidence is required.
- SQLGlot no-op remains a candidate/control route, not a reference.
- positive SQL is reference evidence, not an atom source.

Readiness and live plan:
- Inventory scripts resolved candidate roots and reusable artifacts.
- Required new live calls were 291, under the 300-call cap.
- Live gate check confirmed `SQLRB_LLM_ALLOW_LIVE=1` and an API key environment variable was present; no key value was printed.

Live annotation:
- Ran checkpointed annotation via `run_checkpointed_annotation` for 8 candidate-present route-engine batches.
- Live calls attempted: 291.
- API key values were not printed, written, staged, or committed.

Offline merge/replay/aggregation:
- Merged five-row tri-engine reusable annotations with new 35-row annotations for Repair-1 and SQLGlot no-op MySQL/Spark.
- Ran `python -m cli.main user pocr-diagnostic ...` for all 12 route-engine combinations.
- Ran `pocr_aggregator.py` over 12 `pocr_stage_b_row_metrics.csv` inputs and wrote `output/results/pocr_aggregate_track_a_120_diagnostic_v0/pocr/aggregates/pocr_route_summary.csv`.

Validation commands are appended in `validation_summary.md` during closeout.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted. POCR@planned and POCR@candidate remain D039 promotion views. POCR@curated remains deferred until a predeclared curated manifest exists. Micro-average is diagnostic only and not the paper formula. Track A 120 is not a leaderboard.
