# Raw Output Review

Runtime output root:

```text
/tmp/sqlrb_verieql_perf0062_one_pair_canary_v0
```

Files created by the canary under the temporary root:

```text
logs/verieql_perf0062_one_pair_canary_v0/verifier.log
reports/verieql_perf0062_one_pair_canary_v0/verifier_summary.md
results/verieql_perf0062_one_pair_canary_v0/verifier/semantic_equivalence_summary.json
results/verieql_perf0062_one_pair_canary_v0/verifier/verifier_pairs.csv
results/verieql_perf0062_one_pair_canary_v0/verifier/verifier_verdicts.jsonl
results/verieql_perf0062_one_pair_canary_v0/verifier/tools/verieql/batch/raw_stdout.txt
results/verieql_perf0062_one_pair_canary_v0/verifier/tools/verieql/batch/raw_stderr.txt
results/verieql_perf0062_one_pair_canary_v0/verifier/tools/verieql/batch/verieql_pairs.jsonl
results/verieql_perf0062_one_pair_canary_v0/verifier/tools/verieql/batch/verieql_output.jsonl
results/verieql_perf0062_one_pair_canary_v0/verifier/tools/verieql/PERF_0062_source_vs_positive_pos_01/raw_stdout.txt
results/verieql_perf0062_one_pair_canary_v0/verifier/tools/verieql/PERF_0062_source_vs_positive_pos_01/raw_stderr.txt
```

Batch stdout:

```text
Namespace(file='/tmp/sqlrb_verieql_perf0062_one_pair_canary_v0/results/verieql_perf0062_one_pair_canary_v0/verifier/tools/verieql/batch/verieql_pairs.jsonl', bound_size=999999999, timeout=30, mode='train', cores=32, integrity_constraint=1, out_file='/tmp/sqlrb_verieql_perf0062_one_pair_canary_v0/results/verieql_perf0062_one_pair_canary_v0/verifier/tools/verieql/batch/verieql_output.jsonl')
```

Batch stderr:

```text
Progress-bar output only; no Python traceback or dependency error was emitted.
The progress log reached the configured 30 second timeout.
```

VeriEQL output JSONL relevant fields:

```json
{
  "index": 1,
  "states": ["EQU", "TMO"],
  "counterexample": null,
  "err": null,
  "file": "PERF_0062:source_positive:PERF_0062_source_vs_positive_pos_01",
  "times": [[5.721523, 0.146445], null]
}
```

Interpretation:

- VeriEQL reached the batch verifier and produced a tool-native output row.
- The row is not an unsupported-feature result and not a dependency failure.
- The row contains `TMO`, so the wrapper treats it as a timeout rather than a decidable `equivalent` verdict.
- This remains local verifier-support evidence only.
