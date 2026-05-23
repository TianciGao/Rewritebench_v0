# Raw Output Review

Runtime output root:

```text
/tmp/sqlrb_verieql_cons0007_one_pair_canary_v0
```

Files created by the canary under the temporary root:

```text
logs/verieql_cons0007_one_pair_canary_v0/verifier.log
reports/verieql_cons0007_one_pair_canary_v0/verifier_summary.md
results/verieql_cons0007_one_pair_canary_v0/verifier/semantic_equivalence_summary.json
results/verieql_cons0007_one_pair_canary_v0/verifier/verifier_pairs.csv
results/verieql_cons0007_one_pair_canary_v0/verifier/verifier_verdicts.jsonl
results/verieql_cons0007_one_pair_canary_v0/verifier/tools/verieql/batch/raw_stdout.txt
results/verieql_cons0007_one_pair_canary_v0/verifier/tools/verieql/batch/raw_stderr.txt
results/verieql_cons0007_one_pair_canary_v0/verifier/tools/verieql/batch/verieql_pairs.jsonl
results/verieql_cons0007_one_pair_canary_v0/verifier/tools/verieql/batch/verieql_output.jsonl
results/verieql_cons0007_one_pair_canary_v0/verifier/tools/verieql/CONS_0007_source_vs_positive_pos_01/raw_stdout.txt
results/verieql_cons0007_one_pair_canary_v0/verifier/tools/verieql/CONS_0007_source_vs_positive_pos_01/raw_stderr.txt
```

Batch stdout:

```text
Namespace(file='/tmp/sqlrb_verieql_cons0007_one_pair_canary_v0/results/verieql_cons0007_one_pair_canary_v0/verifier/tools/verieql/batch/verieql_pairs.jsonl', bound_size=999999999, timeout=30, mode='train', cores=32, integrity_constraint=1, out_file='/tmp/sqlrb_verieql_cons0007_one_pair_canary_v0/results/verieql_cons0007_one_pair_canary_v0/verifier/tools/verieql/batch/verieql_output.jsonl')
```

Batch stderr:

```text
Progress-bar output only; no Python traceback or dependency error was emitted.
```

VeriEQL output JSONL relevant fields:

```json
{
  "index": 1,
  "states": ["NSE"],
  "counterexample": null,
  "err": "Not supported feature: EXISTS",
  "file": "CONS_0007:source_positive:CONS_0007_source_vs_positive_pos_01",
  "times": [[0.06867, null]]
}
```

Interpretation:

- VeriEQL reached the batch verifier and produced a tool-native output row.
- The row is not a dependency failure or command failure.
- The tool declared the source query unsupported because it contains `EXISTS`.
- This is a verifier-support limitation, not an observed semantic mismatch.

Input JSONL note:

- The generated JSONL pair used the manifest-declared source and positive SQL.
- The generated JSONL schema was derived from the PostgreSQL DDL context.
- The schema parser currently records a partial column map for this DDL; no patch was made in this task because the observed tool-native blocker was the unsupported `EXISTS` feature.
