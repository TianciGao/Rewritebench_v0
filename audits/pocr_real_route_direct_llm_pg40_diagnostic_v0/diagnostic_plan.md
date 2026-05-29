# Diagnostic Plan

The runner inventories existing `runs/user/**/candidate_sql` roots, selects exactly one unambiguous Direct LLM original PostgreSQL Common-core 40 candidate root, and uses those candidate SQL files read-only. It builds Stage A prompts from case-local `skills.md`, source SQL, candidate SQL, and positive SQL as comparison evidence only. It then applies transformation-aware Stage B diagnostics and writes row-level audit outputs only.

Selected root: `runs/user/direct_llm_original_track_a_120_canonical_v0__postgres/candidate_sql`.
