# Output Contract Conformance

The CLI facade writes through the existing wrapper output contracts:

```text
output/results/<run_id>/verifier/
  verifier_pairs.csv
  verifier_verdicts.jsonl
  semantic_equivalence_summary.json
  tools/
    verieql/
    sqlsolver/

output/logs/<run_id>/verifier.log
output/reports/<run_id>/verifier_summary.md
```

All output remains local-only:

- `local_diagnostic_only=true`
- `official_metric_input=false`
- `paper_result_input=false`
- `retained_evidence_promoted=false`
- `leaderboard_input=false`

The facade rejects top-level `reports/` and `results/` as output roots.

No repository-level `output/` runtime artifacts were committed.
