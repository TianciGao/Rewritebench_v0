# Raw Output Review

Runtime output root:

```text
/tmp/sqlrb_verieql_synthetic_from_clause_smoke_v0
```

Files created under the temporary root:

```text
input/schema.json
input/select_a_candidate.sql
input/select_a_source.sql
input/select_b_candidate.sql
logs/verieql_synthetic_from_clause_smoke_v0/verifier.log
reports/verieql_synthetic_from_clause_smoke_v0/verifier_summary.md
results/verieql_synthetic_from_clause_smoke_v0/verifier/semantic_equivalence_summary.json
results/verieql_synthetic_from_clause_smoke_v0/verifier/tools/verieql/batch/raw_stdout.txt
results/verieql_synthetic_from_clause_smoke_v0/verifier/tools/verieql/batch/raw_stderr.txt
results/verieql_synthetic_from_clause_smoke_v0/verifier/tools/verieql/batch/verieql_pairs.jsonl
results/verieql_synthetic_from_clause_smoke_v0/verifier/tools/verieql/batch/verieql_output.jsonl
results/verieql_synthetic_from_clause_smoke_v0/verifier/tools/verieql/synthetic_from_equivalent/raw_stderr.txt
results/verieql_synthetic_from_clause_smoke_v0/verifier/tools/verieql/synthetic_from_equivalent/raw_stdout.txt
results/verieql_synthetic_from_clause_smoke_v0/verifier/tools/verieql/synthetic_from_nonequivalent/raw_stderr.txt
results/verieql_synthetic_from_clause_smoke_v0/verifier/tools/verieql/synthetic_from_nonequivalent/raw_stdout.txt
results/verieql_synthetic_from_clause_smoke_v0/verifier/verifier_pairs.csv
results/verieql_synthetic_from_clause_smoke_v0/verifier/verifier_verdicts.jsonl
```

Batch stdout:

```text
Namespace(file='/tmp/sqlrb_verieql_synthetic_from_clause_smoke_v0/results/verieql_synthetic_from_clause_smoke_v0/verifier/tools/verieql/batch/verieql_pairs.jsonl', bound_size=999999999, timeout=30, mode='train', cores=32, integrity_constraint=1, out_file='/tmp/sqlrb_verieql_synthetic_from_clause_smoke_v0/results/verieql_synthetic_from_clause_smoke_v0/verifier/tools/verieql/batch/verieql_output.jsonl')
```

Batch stderr:

```text
Progress-bar output only; no Python traceback or dependency error was emitted.
```

VeriEQL output JSONL summary:

```text
synthetic_from_equivalent: states included repeated EQU states followed by TMO; err=null.
synthetic_from_nonequivalent: states=["NEQ"]; err="Symbolic reasoning: NOT EQUIVALENT."
```

Interpretation:

- The staged VeriEQL environment and JSONL wrapper path worked.
- A minimal FROM-clause query avoids the earlier no-FROM unsupported error.
- The non-equivalent synthetic pair produced a decidable refutation.
- The equivalent synthetic pair did not produce a clean decidable equivalent verdict at the 30 second bound because the row ended with `TMO`.
