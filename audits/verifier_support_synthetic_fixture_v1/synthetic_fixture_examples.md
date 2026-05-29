# Synthetic Fixture Examples

The fixture helper can write temp-only D035-shaped verifier output:

```text
output/results/run1/verifier/
  verifier_pairs.csv
  verifier_verdicts.jsonl
  semantic_equivalence_summary.json
  tools/
    verieql/p1/raw_stdout.txt
    verieql/p1/raw_stderr.txt
    sqlsolver/p2/raw_stdout.txt
    sqlsolver/p2/raw_stderr.txt

output/logs/run1/verifier.log
output/reports/run1/verifier_summary.md
```

Example synthetic pair types covered by tests:

- `source_vs_candidate`
- `source_vs_positive`
- `source_vs_hard_negative`

Example synthetic tools:

- `verieql`
- `sqlsolver`

No actual verifier binaries are invoked. Raw stdout/stderr files are placeholder fixture artifacts only.
