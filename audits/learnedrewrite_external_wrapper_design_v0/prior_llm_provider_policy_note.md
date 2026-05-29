# Prior LLM Provider Policy Note

## Scope

This note records provider policy for future LLM-dependent prior methods. It does not implement or run R-Bot or LLM-R2.

## Current Status

R-Bot and LLM-R2 remain blocked for execution.

- R-Bot needs retrieval corpus/index, Java rewrite substrate, PostgreSQL dataset mapping, contamination policy, output extraction, and provider control.
- LLM-R2 needs a one-row D035 wrapper, checkpoint/provenance review, native input conversion, output extraction, and provider control.

## Provider Policy For Future Authorized Runs

If R-Bot or LLM-R2 live calls are later authorized, they must use the same Direct LLM API policy:

- `provider = openai_compatible`
- `model = gpt-5.4`
- required live gate: `SQLRB_LLM_ALLOW_LIVE=1`
- env-only secrets through `SQLRB_LLM_API_KEY` or approved aliases
- no API key values printed, written, staged, or committed
- stop on provider auth/access denial rather than retrying repeatedly
- metadata records provider/model/settings but not secret values

GPTSAPI/OpenAI-compatible configuration should match the Direct LLM route unless a separate task explicitly authorizes a different model/provider.

## Reproduction Boundary

R-Bot and LLM-R2 runs using GPTSAPI/gpt-5.4 are adapted local diagnostics. They must be labeled as:

```text
adapted_gpt54_local_diagnostic
```

They are not exact original-paper reproductions, because the provider, model version, prompt/runtime environment, and benchmark wrapper differ from the original papers.

## Evidence Boundary

Future adapted runs must not be mixed with:

- old retained evidence;
- old recovered-output evidence;
- official paper claims;
- leaderboard-like comparisons;
- Direct LLM route metrics.

Any promotion to retained evidence or paper-facing output requires a separate promotion task with role-aware and denominator-aware wording.
