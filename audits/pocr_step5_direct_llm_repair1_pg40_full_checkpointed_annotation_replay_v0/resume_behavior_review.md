# Resume Behavior Review

The full run used a fresh run id and did not reuse the prior two-row checkpointed smoke output.

The checkpointed runner wrote per-row state before provider calls and produced a complete 40-row manifest plus 40-row safe JSONL. No resume command was needed during this full run because the initial checkpointed command exited successfully.

Resume behavior remains covered by `tests/pocr/test_checkpointed_annotation_runner.py`:

- schema-valid rows with matching `candidate_sha256` are skipped;
- failed rows are retried only with explicit retry-failed behavior;
- duplicate JSONL rows fail closed or are deterministically replaced;
- candidate SHA mismatch fails closed without a provider retry.
