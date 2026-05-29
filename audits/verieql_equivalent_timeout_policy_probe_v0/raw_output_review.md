# Raw Output Review

Runtime output root:

```text
/tmp/sqlrb_verieql_equivalent_timeout_policy_probe_v0
```

For each timeout, VeriEQL wrote a JSONL output row.

30 seconds:

```text
states=["EQU" repeated 18 times, "TMO"]
err=null
elapsed_seconds=30.535
```

120 seconds:

```text
states=["EQU" repeated 19 times, "TMO"]
err=null
elapsed_seconds=120.464
```

300 seconds:

```text
states=["EQU" repeated 20 times, "TMO"]
err=null
elapsed_seconds=300.498
```

Observed behavior:

- Increasing the timeout allowed one additional `EQU` state at each longer bound.
- No run ended with a clean final `EQU` state.
- Every run ended with `TMO`.
- No unsupported-feature error, dependency error, Python traceback, or non-equivalent counterexample was produced.

This supports the interpretation that the equivalent path reaches progressively deeper successful subchecks but still hits an internal or configured timeout before a clean final equivalent verdict.
