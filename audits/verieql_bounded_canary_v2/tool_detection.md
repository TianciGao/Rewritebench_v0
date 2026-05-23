# Tool Detection

Detection sources:

- explicit command passed to the wrapper
- `SQLRB_VERIEQL_COMMAND`
- `VERIEQL_COMMAND`
- `VERIEQL_BIN`
- common PATH command names:
  - `verieql`
  - `VeriEQL`
  - `verieql-cli`
  - `veri-eql`

Local preflight result:

```text
tool_available=False
tool_version=None
detection_reason=verieql_command_not_found
```

No external tool was installed.

Unavailable behavior:

- no real verifier invocation
- verdict rows use `normalized_verdict=not_attempted`
- summary uses `semantic_equivalence_rate=null`
- summary records `na_reason=verieql_unavailable`
