# Verifier Output Placeholder

Future verifier support should write under:

```text
output/results/<run_id>/verifier/
  verifier_pairs.csv
  verifier_verdicts.jsonl
  semantic_equivalence_summary.json
  tools/
    verieql/
    sqlsolver/
```

Both VeriEQL and SQLSolver are future verifier/support tools. They are not rewrite baselines.

Semantic Equivalence Rate remains `N.A.` until formal verifier evidence exists. The local result checker is result-consistency evidence, not formal semantic-equivalence verification.

Verifier outputs should remain separate from:

- method-generated candidate failures;
- hard-negative checker controls;
- local result checker mismatches;
- timing artifacts;
- non-official local metrics.

Verifier integration is not implemented by this task.
