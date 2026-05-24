# Prior Methods Onboarding Feasibility v0

## Summary

This audit reviews onboarding feasibility for three prior SQL rewrite methods:

- R-Bot / LLM4Rewrite
- LLM-R2
- LearnedRewrite

The review covered the current release repo conventions, legacy branch references, official source repositories, and official papers/READMEs. No adapters were implemented and no experiments were run.

## Key Findings

- R-Bot has the richest legacy evidence, including PG15 execution/timing and formal substrate-freeze planning, but it is an LLM/RAG method with retrieval-index, provider, Java, PostgreSQL, and contamination-policy blockers.
- LLM-R2 has official source with a TPCH selector checkpoint and legacy PG9/PG6 evidence, but it needs a one-row D035 wrapper, strict route separation between original and recovered extraction, and provider-contract cleanup.
- LearnedRewrite is technically the narrowest first adapter candidate because the core path is Java/Calcite and no-live, but it has license ambiguity, schema conversion work, and upstream source hygiene risks.

## Recommended Next Method

Recommended next method: LearnedRewrite, but only for a no-live external-wrapper design and fixture-test task. It should not proceed directly to DB/checker/timing or Track A 120.

## Blocked Methods

R-Bot is blocked for execution by retrieval/corpus/index/provider substrate work.

LLM-R2 is blocked for execution by row-scoped wrapper, checkpoint/provenance, native input conversion, and strict output extraction work.

LearnedRewrite is blocked for runtime by license/source hygiene and schema/dialect adapter design, but it is the best candidate for a deterministic no-live scaffold.

## Legacy Evidence Use

Legacy evidence is useful for:

- fixture design;
- failure bucket planning;
- expected bounded subset definitions;
- route-boundary wording;
- source-like/no-op diagnostics.

Legacy evidence is not sufficient for:

- current canonical local metrics;
- Track A 120 promotion;
- official metrics;
- paper result updates;
- retained evidence promotion;
- leaderboard input.

## Outputs

- `method_source_inventory.csv`
- `legacy_repo_evidence_inventory.csv`
- `method_runtime_entrypoints.csv`
- `benchmark_role_mapping.md`
- `integration_risk_matrix.csv`
- `proposed_sequence.md`
- `command_log.txt`
- `validation_notes.md`

## Boundary

No R-Bot, LLM-R2, LearnedRewrite, live LLM, DB execution, checker execution, timing, local metrics, SQLSolver, VeriEQL, official metrics, paper rendering, retained evidence promotion, or leaderboard generation occurred.

Next safe action: authorize a LearnedRewrite no-live external-wrapper design and fixture-test task, after confirming the source/license boundary.
