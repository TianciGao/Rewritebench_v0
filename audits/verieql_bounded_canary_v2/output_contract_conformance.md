# Output Contract Conformance

The wrapper writes the planned verifier support shape:

```text
output/results/<run_id>/verifier/
  verifier_pairs.csv
  verifier_verdicts.jsonl
  semantic_equivalence_summary.json
  tools/
    verieql/<pair_id>/

output/logs/<run_id>/verifier.log
output/reports/<run_id>/verifier_summary.md
```

Boundary flags are present on verdict and summary records:

- `local_diagnostic_only=true`
- `official_metric_input=false`
- `paper_result_input=false`
- `retained_evidence_promoted=false`
- `leaderboard_input=false`

Prohibited fields:

- no `winner`
- no `best_method`
- no `rank`
- no leaderboard artifact

All output-contract tests use temporary directories. No repository-level `output/` runtime artifacts were committed.
