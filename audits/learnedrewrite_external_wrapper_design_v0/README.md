# LearnedRewrite External Wrapper Design v0

## Purpose

This packet designs a no-live external-wrapper integration path for LearnedRewrite as the next prior-method candidate. It does not implement an adapter, run LearnedRewrite, run Java, copy upstream source or JARs, run DB/checker/timing, compute metrics, run verifiers, update paper results, or promote retained evidence.

## Why LearnedRewrite Is Next

The prior-method onboarding audit found LearnedRewrite to be the narrowest technical candidate for the next prior-method scaffold because its core path is Java/Calcite and does not require live LLM calls. The official repo exposes an HTTP API shape that can return `rewritten_sql`, and legacy evidence includes bounded PostgreSQL-only prior-method notes that are useful for fixture design.

LearnedRewrite is not ready for execution in the release repo. The current safe step is a wrapper contract and fixture-test scaffold only.

## Reviewed Inputs

- Current release repo project-control files.
- `repository_spec/metrics_contract_v1.md`.
- `audits/prior_methods_onboarding_feasibility_v0/`.
- Current baseline adapter conventions under `baselines/`.
- Current D035 user facade conventions under `src/cli/` and `src/sql_rewrite_bench/`.
- Official LearnedRewrite source reference: `https://github.com/XuanheZhou/LearnedRewrite`.
- Official paper reference recorded by onboarding: `https://dbgroup.cs.tsinghua.edu.cn/ligl/papers/vldb22-query-rewrite.pdf`.
- Legacy read-only references under the old repo clone.

## Feasibility Verdict

Feasible as a future external wrapper, not as vendored source.

The next implementation should create `baselines/learnedrewrite/adapter.py` only after a separate task is authorized. That adapter should shell out to or call an externally installed LearnedRewrite runtime and emit exactly one candidate SQL file per D035 user-facade row, or fail closed.

## Main Blockers

- No repository-level license file was found in the official source clone.
- Official source and packaged JARs must not be copied into this release repo.
- Upstream source has local-path and write-side-effect behavior that needs containment.
- Schema JSON conversion from SQL-RewriteBench case/schema metadata is not implemented.
- PostgreSQL, MySQL, and Spark dialect support is not established.
- Source-like/no-op outputs must remain visible as diagnostics and not be described as optimization success.

## Outputs

- `learnedrewrite_source_hygiene_review.md`
- `learnedrewrite_wrapper_contract.md`
- `learnedrewrite_fixture_io_examples.csv`
- `learnedrewrite_adapter_design.md`
- `learnedrewrite_risk_matrix.csv`
- `learnedrewrite_next_implementation_plan.md`
- `prior_llm_provider_policy_note.md`
- `command_log.txt`
- `validation_notes.md`

## Next Safe Action

Authorize a fixture-only LearnedRewrite adapter scaffold with a fake external runtime. Do not run the real Java runtime until wrapper contract tests, schema JSON fixtures, source-hygiene boundaries, and output extraction guards are stable.
