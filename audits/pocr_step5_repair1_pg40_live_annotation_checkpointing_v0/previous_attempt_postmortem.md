# Previous Attempt Postmortem

The previous `pocr_step5_direct_llm_repair1_pg40_annotation_replay_v0` attempt selected `runs/user/direct_llm_repair_1_track_a_120_canonical_v0__postgres/candidate_sql` and resolved 40/40 Common-core PostgreSQL candidate rows.

The recorded command shape was an inline bounded live annotation subprocess: `python - <<'PY' ... bounded live annotation generation attempt ... PY`. The command log also records `kill <annotation-subprocess-pid>` and a later search for the expected output tree.

Observed postmortem facts:

- stdout/stderr were not captured as per-row auditable artifacts.
- A structured exit code was not recorded in the audit packet.
- The visible termination mode was manual subprocess termination after the live attempt produced no auditable manifest or safe JSONL.
- No partial provider response was committed or preserved as a safe annotation row.
- No row-level manifest existed before provider calls, so an interruption could leave no durable per-row status.
- User replay was correctly not executed because `safe_annotation_outputs.jsonl` was absent.

The new checkpointed runner changes this by writing `call_status=pending` before each provider call, writing manifest/checkpoint/provider files after every status change, and appending or replacing safe JSONL only after a row has a schema-valid annotation or a fail-closed safe error object.
