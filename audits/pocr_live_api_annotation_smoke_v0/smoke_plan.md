# Smoke Plan

## Purpose

This smoke checks whether the POCR Stage A prompt and live OpenAI-compatible annotation client can produce schema-conformant JSON for a tiny set of real Common-core `skills.md` contracts.

It does not compute official Positive Operation Coverage Rate and does not aggregate a route-level POCR value.

## Selected Cases

The authorized fixture set was:

- `PERF_0006`
- `CONS_0005`
- `PORT_0003`
- `LONGTAIL_0011`

All four were selected because each has a root-level `skills.md`, source SQL, and an existing local candidate SQL file under the route-labeled run:

```text
runs/user/common_core_pg_noop_db_checker/candidate_sql/
```

## Candidate Input Boundary

The candidate SQL files were pre-existing local artifacts. They were used read-only as candidate text for Stage A annotation. The task did not run or rerun `examples/user/noop_adapter.py`, SQLGlot, Direct LLM, LearnedRewrite, R-Bot, LLM-R2, or any other baseline.

No synthetic method candidate was created.

## API Boundary

The smoke required both:

- local environment gate `SQLRB_LLM_ALLOW_LIVE=1`;
- explicit command flag `--live-enabled`.

Only safe provider metadata was recorded: provider label, model label, host label, environment variable name used for the key, prompt hash, candidate/source hashes, timestamps, token counts when returned, and status.

No API key value, raw prompt, or raw provider response was written.

## Stage B Boundary

Stage B received no independent evidence. Therefore schema-valid annotations must remain `insufficient_evidence`; a malformed Stage A annotation must remain `schema_invalid`.

LLM rationale, speedup, runtime behavior, taxonomy tags, and candidate/source SQL text alone are not Stage B evidence.
