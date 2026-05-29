# Baseline And POCR Shared Config Plan

Direct LLM original, Direct LLM Repair-1, adapted R-Bot, adapted LLM-R2, and POCR Stage A annotation should converge on one shared LLM configuration loader in a future implementation task.

The shared loader should resolve:

- provider label
- base URL
- API key environment variable name
- model label
- timeout
- max tokens
- temperature
- response format
- live gate status
- safe provider metadata

The shared loader must not merge:

- route IDs
- method IDs
- prompt templates
- output schemas
- denominator scopes
- candidate identities
- annotation evidence status
- timing/checker metrics

This task does not implement live calls or change baseline behavior. Direct LLM original and Repair-1 remain separate route identities, and POCR annotation remains diagnostic-only.

Annotation JSONL is diagnostic evidence only. No official POCR is computed. No paper-facing metric is promoted. No global leaderboard is produced.
