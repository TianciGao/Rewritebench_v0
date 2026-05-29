# Output Contract Conformance

The wrapper writes D035-shaped verifier output when invoked:

```text
output/results/<run_id>/verifier/
  verifier_pairs.csv
  verifier_verdicts.jsonl
  semantic_equivalence_summary.json
  tools/sqlsolver/
output/logs/<run_id>/
  verifier.log
output/reports/<run_id>/
  verifier_summary.md
```

All summary and verdict records preserve local-only boundary flags:

- `local_diagnostic_only=true`
- `official_metric_input=false`
- `paper_result_input=false`
- `retained_evidence_promoted=false`
- `leaderboard_input=false`

No top-level `reports/` or `results/` files are written by the wrapper.
