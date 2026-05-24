# Synthetic Preflight Review

## Attempted

No.

## Reason

No external LearnedRewrite runtime was configured:

- `SQLRB_LEARNEDREWRITE_CMD` present: no.
- `SQLRB_LEARNEDREWRITE_URL` present: no.

The task did not probe an arbitrary localhost port and did not send a synthetic request without an explicit configured runtime. This avoids accidental interaction with unrelated local services.

## Result

```json
{
  "runtime_available": false,
  "synthetic_preflight_attempted": false,
  "synthetic_preflight_result": "not_attempted_no_runtime_configured",
  "common_core_sql_sent": false
}
```

## Next Requirement

Provide either:

- `SQLRB_LEARNEDREWRITE_URL` pointing to a local external LearnedRewrite `/rewriter` endpoint; or
- `SQLRB_LEARNEDREWRITE_CMD` pointing to a narrow external command wrapper with a documented synthetic request mode.

Then rerun this preflight before any user-facade external-runtime smoke.
