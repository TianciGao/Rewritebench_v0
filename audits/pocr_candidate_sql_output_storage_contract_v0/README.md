# POCR Candidate SQL Output Storage Contract v0

This packet records Step 2 of D038: the candidate SQL output/storage contract under the D035 user-output layout.

This is documentation and contract work only. No candidate SQL was moved, copied, deleted, normalized, regenerated, or rewritten. No `output/` files were created. No annotation JSONL was generated. No official POCR is computed.

## Files

- `storage_contract.md`: D035-aligned candidate SQL output tree and storage policy.
- `candidate_sql_path_contract.md`: valid and invalid candidate path examples.
- `manifest_schema_contract.csv`: documented manifest field schema.
- `legacy_runs_user_mapping_policy.md`: read-only policy for existing `runs/user` candidate roots.
- `pg40_vs_tracka120_storage_examples.md`: denominator-aware PG40 and Track A 120 examples.
- `table_route_storage_readiness_review.md`: Step 1b Table 1 route readiness summary.
- `protected_path_review.md`: protected-path and no-mutation review.
- `command_log.md`: command log with no live/API/runtime commands.

## Boundary

This contract standardizes future candidate SQL placement under `output/results/<run_id>/candidate_sql/`. It does not promote any candidate SQL to retained evidence, does not fill POCR cells, and does not change paper-facing tables.

PG40 candidate roots cannot fill Track A 120 POCR cells. No official POCR is computed. No paper-facing metric is promoted. No route-level POCR score is emitted.

## Next Safe Action

Implement Step 3: a POCR annotation JSONL artifact contract that uses this candidate SQL storage contract as the candidate identity layer.
