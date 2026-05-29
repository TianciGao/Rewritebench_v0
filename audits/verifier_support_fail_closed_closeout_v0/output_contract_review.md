# Output Contract Review

Verifier outputs use the D035 local output layout:

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

Required local-only flags:

- `local_diagnostic_only=true`
- `official_metric_input=false`
- `paper_result_input=false`
- `retained_evidence_promoted=false`
- `leaderboard_input=false`

Closeout status:

- Contract is implemented for synthetic fixtures and bounded wrapper outputs.
- Real tool output remains unvalidated because neither tool is locally available.
- No top-level `reports/` or `results/` files were updated.
- No `output/` runtime artifacts are committed.
