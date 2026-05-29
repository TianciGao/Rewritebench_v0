# Tag Failure Boundary

- Tag-aware failure slices are diagnostic/support only.
- `tag_slices` are not primary metrics.
- `tag_slices` are not POCR.
- `tag_slices` are not SER.
- `tag_slices` are not leaderboard inputs.
- Failure buckets are method behavior diagnostics, not package hard-negative controls.
- Package hard-negative controls remain separate from method-generated candidate failures.
- Local checker exactness remains Result Consistency evidence only, not SER evidence.
- No official paper result is changed.
- No operation atoms are inferred and no skill folders are created.
- Verifier absence is reported as absent evidence, not as method failure.
