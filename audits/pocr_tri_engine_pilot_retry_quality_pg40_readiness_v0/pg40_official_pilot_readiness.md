# PG40 Official-Pilot Readiness

This is not official POCR.

No route-level official POCR score is emitted.

No paper-facing metric is promoted.

PG40 readiness is design-only. No PG40 live annotation was run in this task.

POCR@planned and POCR@candidate remain D039 promotion views. POCR@curated remains deferred until a predeclared curated manifest exists.

PG40 is the next larger step because the pilot exercised the exporter and aggregator across engines on 30 rows, while PG40 keeps the denominator bounded to PostgreSQL Common-core 40 rows before any Track A 120 expansion. PG40 is not Track A 120.

Route readiness:

- Direct LLM original PG40: candidate rows 40/40, missing `none`, existing annotation `yes`, expected future live calls `0 if existing annotation reused; replay/export only`, readiness `ready_with_existing_annotation`. candidate_root=runs/user/direct_llm_original_track_a_120_canonical_v0__postgres/candidate_sql; source=T1_TRACKA_DIRECT_LLM_ORIGINAL
- Direct LLM + Repair-1 PG40: candidate rows 40/40, missing `none`, existing annotation `yes`, expected future live calls `0 if existing annotation reused; replay/export only`, readiness `ready_with_existing_annotation`. candidate_root=runs/user/direct_llm_repair_1_track_a_120_canonical_v0__postgres/candidate_sql; source=T1_TRACKA_DIRECT_LLM_REPAIR_1
- SQLGlot no-op PG40: candidate rows 40/40, missing `none`, existing annotation `yes`, expected future live calls `0 if existing annotation reused; optional 6 targeted retry calls if quality gate requires fail-closed retry`, readiness `ready_with_existing_annotation`. candidate_root=runs/user/common_core_pg_noop_db_checker/candidate_sql; source=T1_TRACKA_SQLGLOT_NOOP
- SQLGlot optimize PG40: candidate rows 34/40, missing `CONS_0009;PORT_0004;PORT_0013;PORT_0022;PORT_0024;PORT_0025`, existing annotation `no`, expected future live calls `34 candidate-present rows; 6 no-candidate rows fail-closed under POCR@planned`, readiness `partial_candidate_ready_missing_rows_fail_closed_design`. candidate_root=runs/user/sqlglot_optimize_schema_aware_track_a_120_canonical_v0__postgres/candidate_sql; source=T1_TRACKA_SQLGLOT_OPTIMIZE_SCHEMA_AWARE
- R-Bot adapted GPT-5.4 PG40: candidate rows 40/40, missing `none`, existing annotation `no`, expected future live calls `40`, readiness `candidate_root_ready_needs_annotation`. candidate_root=runs/user/rbot_gpt54_pg40_bounded_diagnostic_rerun_v0/candidate_sql; source=T1_PG40_RBOT_GPT54_ADAPTED
- LLM-R2 adapted GPT-5.4 PG40: candidate rows 40/40, missing `none`, existing annotation `no`, expected future live calls `40`, readiness `candidate_root_ready_needs_annotation`. candidate_root=runs/user/llm_r2_gpt54_pg40_manual_inspection_rerun_v0/candidate_sql; source=T1_PG40_LLM_R2_GPT54_ADAPTED
- LearnedRewrite PG40 candidate-present: candidate rows 29/40, missing `PERF_0035;CONS_0009;CONS_0012;CONS_0024;PORT_0004;PORT_0008;PORT_0012;PORT_0013;PORT_0022;PORT_0024;PORT_0025`, existing annotation `no`, expected future live calls `29 candidate-present rows; 11 no-candidate rows fail-closed under POCR@planned`, readiness `partial_candidate_ready_missing_rows_fail_closed_design`. candidate_root=runs/user/learnedrewrite_pg40_manual_inspection_rerun_v0/candidate_sql; source=T1_PG40_LEARNEDREWRITE

Recommended PG40 pilot routes:

- Include Direct LLM original PG40 and Direct LLM + Repair-1 PG40 first because both have complete PostgreSQL candidate roots and existing annotation evidence that can potentially be reused with no new live calls if route identity is accepted.
- Include SQLGlot no-op PG40 as the sanity/control route; either reuse the existing diagnostic annotation with its visible fail-closed rows or separately authorize a bounded targeted retry for the six fail-closed no-op annotations.
- Include SQLGlot optimize PG40 only as a planned-denominator fail-closed design: annotate the 34 actual optimize candidates if later authorized, retain the six missing candidates as fail-closed zero rows for POCR@planned, and do not substitute SQLGlot no-op candidates.
- Treat R-Bot adapted GPT-5.4 and LLM-R2 adapted GPT-5.4 as appendix/diagnostic PG40 routes with 40 expected live calls each if later authorized.
- Treat LearnedRewrite as appendix/diagnostic candidate-present evidence only unless the PG40 planned missing rows are explicitly retained as fail-closed no-candidate rows.

Safety gates before any PG40 run:

- Explicit authorization for live annotation and maximum calls by route.
- Reuse decision for existing Direct LLM original, Repair-1, and no-op annotations.
- No-op over-accept manual review if any no-op Stage B support appears.
- SQLGlot optimize missing rows remain fail-closed unless actual optimize candidates are produced in a separate candidate-capture task.
- No official POCR computation or paper-facing metric promotion until promotion freeze is separately authorized.
