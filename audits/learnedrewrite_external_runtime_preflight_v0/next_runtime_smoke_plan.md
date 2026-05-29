# Next Runtime Smoke Plan

## Current Verdict

LearnedRewrite external runtime is blocked because no command or URL is configured.

## If Runtime Becomes Available

After `SQLRB_LEARNEDREWRITE_URL` or `SQLRB_LEARNEDREWRITE_CMD` is configured, rerun this preflight with one synthetic non-benchmark request.

Required pass conditions:

- runtime is reachable;
- request uses only synthetic SQL and schema;
- response parses as JSON or another explicitly documented format;
- exactly one SQL statement is extractable;
- no upstream source/JAR/dependency/checkpoint/dataset/generated-output copy occurs;
- no Common-core SQL is sent.

If that succeeds, authorize a 1-2 row LearnedRewrite external-runtime user-facade smoke:

- PostgreSQL only;
- no DB execution;
- no checker;
- no timing;
- no local metrics;
- no verifier;
- temporary `/tmp` output root;
- no top-level reports/results update;
- no retained-evidence or paper promotion.

## If Runtime Remains Unavailable

Keep LearnedRewrite blocked. Recommended options:

1. Provide an external runtime setup outside this repo and rerun preflight.
2. Keep LearnedRewrite at fake-wrapper status and move to R-Bot / LLM-R2 wrapper planning under the GPTSAPI `gpt-5.4` adapted-local-diagnostic policy.

## Not Recommended Yet

Do not run Track A 120. Do not run DB/checker/timing. Do not compute local metrics. Do not treat Java availability as a successful LearnedRewrite runtime preflight.
