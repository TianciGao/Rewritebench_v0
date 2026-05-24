# LearnedRewrite External Runtime Preflight v0

## Summary

This packet records a LearnedRewrite external-runtime availability and preflight audit.

Runtime availability verdict:

- Java is available: yes, `openjdk version "17.0.18" 2026-01-20`.
- `SQLRB_LEARNEDREWRITE_CMD` configured: no.
- `SQLRB_LEARNEDREWRITE_URL` configured: no.
- `SQLRB_LEARNEDREWRITE_ALLOW_RUNTIME=1`: no.
- External LearnedRewrite runtime available for preflight: no configured runtime.
- Synthetic preflight request attempted: no.

Because no runtime command or URL was configured, no request was sent. No Common-core case SQL was sent to any runtime.

## Key Finding

The existing adapter wrapper contract is aligned with the intended external runtime shape at a high level, but it remains fake-mode only. Real command/http runtime support is still a future implementation step. Before any external-runtime user-facade smoke, the project needs either a configured local URL or command wrapper plus a safe synthetic request/response contract test.

## Boundary

- No LearnedRewrite run on Common-core cases occurred.
- No real benchmark run occurred.
- No DB/checker/timing/local_metrics/verifier command occurred.
- No official metrics, paper rendering, retained-evidence promotion, or leaderboard output occurred.
- No upstream source, JAR, dependency JAR, checkpoint, dataset, generated output, or request log was copied.

## Next Safe Action

Keep LearnedRewrite blocked until an external runtime path or local URL is supplied and a synthetic non-benchmark preflight succeeds. If no runtime is available, move to R-Bot / LLM-R2 wrapper planning under the GPTSAPI `gpt-5.4` adapted-local-diagnostic policy.
