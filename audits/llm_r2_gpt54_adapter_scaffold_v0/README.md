# LLM-R2 GPT-5.4 Adapter Scaffold v0

This packet records the fixture-only implementation of
`baselines/llm_r2/adapter.py` and the tiny fake user-facade smoke for
`route_id=llm_r2_gpt54_adapted`.

The route is an adapted GPT-5.4 local diagnostic scaffold. It is not an
original LLM-R2 paper reproduction, does not use the official LLM-R2 runtime,
does not invoke the Java/rule-system path, and does not use checkpoints or a
demonstration selector.

## Result

- Adapter scaffold: implemented.
- Fake runtime tests: passed.
- Fake user-facade smoke: passed for `PERF_0006/postgres` and
  `CONS_0036/postgres`.
- Candidate generation in smoke: 2/2.
- DB/checker/timing/local_metrics/verifier: not run.
- Live LLM/API: not run.
- Rule-system/checkpoint/demo selector: not run.

## Boundary

Old LLM-R2 evidence and recovered-output packets were used only to shape the
wrapper contract and fail-closed behavior. No old outputs, logs, candidates,
metrics, or request/response traces were copied into current canonical outputs.

## Next Safe Action

Authorize a 3-6 row PostgreSQL-only GPT-5.4 adapted live generation or
end-to-end smoke only after reviewing this fake scaffold. Do not run Track A
120 until fake and bounded live smokes pass.
