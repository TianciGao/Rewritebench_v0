# Smoke Scope

Run id:

```text
direct_llm_repair_1_fake_provider_user_facade_smoke_v0
```

Facade path:

```text
python -m cli.main user evaluate
```

Selection:

- Case set: `common_core_v0`
- Case list: temporary `/tmp` file containing `CONS_0005` and `LONGTAIL_0012`
- Engines: `spark`
- Planned rows: 2

Fixture feedback types:

- `CONS_0005 / spark`: `checker_mismatch_feedback`
- `LONGTAIL_0012 / spark`: `candidate_execution_error_feedback`

Execution boundary:

- `--enable-db-execution` was not used.
- `--enable-checker` was not used.
- `--collect-timing` was not used.
- `compute-local-metrics` was not run.
- SQLSolver and VeriEQL were not run.
- No live provider gate or API key was used.

This smoke verifies facade invocation, fixture context injection, fake-provider
candidate generation, candidate capture, and secret-free adapter metadata only.
It makes no correctness, performance, official metric, SER, or paper-result
claim.
