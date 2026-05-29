# Runtime Environment Probe

## Environment Presence

No sensitive or private values were printed.

| Check | Result |
|---|---|
| `SQLRB_LEARNEDREWRITE_CMD` present | no |
| `SQLRB_LEARNEDREWRITE_URL` present | no |
| `SQLRB_LEARNEDREWRITE_MODE` present | no |
| `SQLRB_LEARNEDREWRITE_ALLOW_RUNTIME=1` | no |
| Java available | yes |
| Java version | `openjdk version "17.0.18" 2026-01-20` |
| Configured runtime appears reachable | not checked; no runtime command or URL configured |
| Runtime configured | no |

## Interpretation

The local environment can run Java, but no external LearnedRewrite runtime is configured through the wrapper variables. Because neither command mode nor URL mode is configured, this task did not attempt a synthetic request.

## Safety

No command value, URL value, private path, API key, or secret was printed. No `SQLRB_LEARNEDREWRITE_ALLOW_RUNTIME=1` gate was set.
