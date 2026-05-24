# LearnedRewrite External Runtime Synthetic Preflight

This packet records one synthetic non-benchmark LearnedRewrite external-runtime preflight using the external runtime candidate:

```text
/tmp/sqlrb_prior_methods_sources/LearnedRewrite/rewriter_java.jar
```

## Result

- Java available: yes.
- JAR candidate exists: yes.
- JAR copied into release repo: no.
- Runtime mode attempted: HTTP server on local port `6336`.
- Synthetic POST attempted: yes, exactly one.
- Common-core SQL sent: no.
- Response parseable: yes.
- Single SQL extractable: no.
- Synthetic preflight succeeded: no.

The runtime returned:

```json
{"message":"Get Error","status":false}
```

The runtime-generated temp request log identified the blocker:

```text
java.io.FileNotFoundException: rules_for_selected/standard.txt (No such file or directory)
```

## Wrapper Verdict

Wrapper compatibility remains blocked. The current release adapter still has fail-closed real runtime hooks, and the external runtime did not produce a candidate SQL under safe temp-working-directory execution.

## Next Safe Action

Authorize a temp-only runtime staging fix for the missing `rules_for_selected/` asset, then rerun one synthetic non-benchmark preflight. Do not send Common-core SQL or run Track A 120 yet.
