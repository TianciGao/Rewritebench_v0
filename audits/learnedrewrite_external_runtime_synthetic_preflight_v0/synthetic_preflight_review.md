# Synthetic Preflight Review

## Scope

Exactly one synthetic non-benchmark POST was sent to the temporary LearnedRewrite server:

- SQL: `SELECT COUNT(*) FROM tiny_orders WHERE amount > 10`
- Schema: synthetic `tiny_orders(order_id integer, amount numeric)`
- Common-core SQL sent: no
- Benchmark schema sent: no

## Runtime Mode

- Mode used: HTTP server
- Server command: `java -jar <external_learnedrewrite_runtime_candidate>/rewriter_java.jar`
- Bound port observed: `6336`
- Custom port support observed: not confirmed; the `--server.port=26336` diagnostic did not bind the requested port.
- Server stopped after preflight: yes

## Result

The runtime returned:

```json
{"message":"Get Error","status":false}
```

HTTP status was `200`, and the JSON response was parseable. It did not contain `data.rewritten_sql` or another candidate SQL field.

## Runtime Error Clue

The temp working directory contained a runtime-generated `request.txt` with the synthetic request and this error:

```text
java.io.FileNotFoundException: rules_for_selected/standard.txt (No such file or directory)
```

This indicates the JAR expects relative runtime assets in the working directory. The JAR itself contains `rules_for_selected/standard.txt`, but the server appears to resolve it as a filesystem-relative path at runtime.

## Single-SQL Extraction

Single SQL extractable: no.

Reason:

- no `rewritten_sql` field in response;
- response status was false;
- runtime failed before producing a candidate.

## Fail-Closed Behavior

For the release wrapper, this response should fail closed as `runtime_failed` or `no_rewritten_sql`, with a more specific setup blocker of `runtime_missing_workdir_asset`.

## Safety

The JAR and upstream files remained outside the release repo. The generated runtime `request.txt` stayed under `/tmp/sqlrb_learnedrewrite_external_runtime_synthetic_preflight_v0/runtime_preflight/` and was not copied into the repository.
