# Verifier Output Directory Contract

Future verifier outputs should use the D035 local output roots:

```text
output/results/<run_id>/verifier/
  verifier_pairs.csv
  verifier_verdicts.jsonl
  semantic_equivalence_summary.json
  tools/
    verieql/
    sqlsolver/
```

Log output:

```text
output/logs/<run_id>/verifier.log
```

Human-readable report:

```text
output/reports/<run_id>/verifier_summary.md
```

Tool-specific raw artifacts:

```text
output/results/<run_id>/verifier/tools/verieql/<pair_id>/
output/results/<run_id>/verifier/tools/sqlsolver/<pair_id>/
```

All verifier artifacts must carry local-only boundary flags:

- `local_diagnostic_only=true`
- `official_metric_input=false`
- `paper_result_input=false`
- `retained_evidence_promoted=false`
- `leaderboard_input=false`

Top-level `reports/` and `results/` remain official/paper-facing surfaces and are not written by verifier local diagnostic tasks.
