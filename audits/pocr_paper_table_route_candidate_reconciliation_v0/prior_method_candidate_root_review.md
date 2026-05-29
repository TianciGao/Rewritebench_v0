# Prior-Method Candidate Root Review

## LearnedRewrite

`runs/user/learnedrewrite_pg40_manual_inspection_rerun_v0/candidate_sql` is present but contains only 29 Common-core PostgreSQL candidate files. This matches generated-row behavior, not full PG40 denominator coverage. LearnedRewrite remains unsuitable for full PG40 POCR annotation unless a no-candidate/fail-closed row policy is defined.

## R-Bot Adapted GPT-5.4

`runs/user/rbot_gpt54_pg40_bounded_diagnostic_rerun_v0/candidate_sql` contains 40 Common-core PostgreSQL candidate files. It is suitable for a future PostgreSQL-only PG40 diagnostic annotation generation and user-facing replay task. It is not Track A 120 evidence and is not an original-paper reproduction.

## LLM-R2 Adapted GPT-5.4

`runs/user/llm_r2_gpt54_pg40_manual_inspection_rerun_v0/candidate_sql` contains 40 Common-core PostgreSQL candidate files. It is suitable for a future PostgreSQL-only PG40 diagnostic annotation generation and user-facing replay task. It is adapted GPT-5.4 local diagnostic evidence, not original LLM-R2 paper reproduction.

## Boundary

PG40 prior-method roots can support only PostgreSQL-only diagnostic POCR work. They cannot fill Track A 120 rows and cannot produce official POCR without separate promotion authorization.
