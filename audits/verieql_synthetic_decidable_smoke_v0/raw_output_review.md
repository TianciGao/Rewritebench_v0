# Raw Output Review

Runtime output root:

```text
/tmp/sqlrb_verieql_synthetic_decidable_smoke_v0
```

Files created under the temporary root:

```text
input/select_1_a.sql
input/select_1_b.sql
input/select_2.sql
logs/verieql_synthetic_decidable_smoke_v0/verifier.log
reports/verieql_synthetic_decidable_smoke_v0/verifier_summary.md
results/verieql_synthetic_decidable_smoke_v0/verifier/semantic_equivalence_summary.json
results/verieql_synthetic_decidable_smoke_v0/verifier/verifier_pairs.csv
results/verieql_synthetic_decidable_smoke_v0/verifier/verifier_verdicts.jsonl
results/verieql_synthetic_decidable_smoke_v0/verifier/tools/verieql/batch/raw_stdout.txt
results/verieql_synthetic_decidable_smoke_v0/verifier/tools/verieql/batch/raw_stderr.txt
results/verieql_synthetic_decidable_smoke_v0/verifier/tools/verieql/batch/verieql_pairs.jsonl
results/verieql_synthetic_decidable_smoke_v0/verifier/tools/verieql/batch/verieql_output.jsonl
```

Batch stdout:

```text
Namespace(file='/tmp/sqlrb_verieql_synthetic_decidable_smoke_v0/results/verieql_synthetic_decidable_smoke_v0/verifier/tools/verieql/batch/verieql_pairs.jsonl', bound_size=999999999, timeout=30, mode='train', cores=32, integrity_constraint=1, out_file='/tmp/sqlrb_verieql_synthetic_decidable_smoke_v0/results/verieql_synthetic_decidable_smoke_v0/verifier/tools/verieql/batch/verieql_output.jsonl')
```

Batch stderr:

```text
Progress-bar output only; no Python traceback or dependency error was emitted.
```

VeriEQL output JSONL:

```json
{"index":1,"states":["NSE"],"counterexample":null,"err":"Not supported feature: Query must have a FROM clause","file":"SYNTHETIC_SELECT1_EQUIVALENT:support_pair_smoke:synthetic_select1_equivalent"}
{"index":2,"states":["NSE"],"counterexample":null,"err":"Not supported feature: Query must have a FROM clause","file":"SYNTHETIC_SELECT1_NONEQUIVALENT:support_pair_smoke:synthetic_select1_nonequivalent"}
```

Interpretation:

- The staged environment and JSONL wrapper path worked.
- The synthetic `SELECT`-without-`FROM` shape is unsupported by VeriEQL.
- No dependency, command, or wrapper failure was observed.
