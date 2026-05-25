# Replay Plan

- Annotation JSONL: `audits/pocr_real_route_direct_llm_pg40_diagnostic_v0/safe_annotation_outputs.jsonl`
- Candidate root: `runs/user/direct_llm_original_track_a_120_canonical_v0__postgres/candidate_sql`
- Run ID: `pocr_user_replay_direct_llm_pg40_v0`
- Method ID: `direct_llm_original`
- Replay route ID: `direct_llm_original_pg40_user_replay`
- Engine: `postgres`
- Temp output root: `/tmp/sqlrb_pocr_user_replay_direct_llm_pg40_v0/output`

Mapping policy: exact case ID and engine match are required; method/route mismatches are reported and fail closed; duplicates fail closed; malformed rows fail closed; missing rows remain annotation_missing.

Boundary: diagnostic-only replay; no official POCR, no route-level aggregation, no user-output default change, no paper metric promotion.
