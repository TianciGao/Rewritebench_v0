# Checkpoint State Review

Checkpoint state file: `output/results/pocr_annotation_sqlglot_noop_pg40_sanity_control_v0/pocr/annotations/sqlglot_noop/sqlglot_noop_pg40_pocr_sanity_control/postgres/checkpoint_state.json`

The checkpointed runner wrote manifest/checkpoint state before provider calls and safe JSONL rows after responses were parsed or represented as fail-closed diagnostic rows.

Final checkpoint counts: `{"malformed_json": 5, "provider_call_failed": 1, "schema_valid": 34}`.

Rows attempted: 40. Live calls attempted: 40. Safe JSONL rows: 40.

No API key value is present in the checkpoint, manifest, logs, reports, or audit packet.
