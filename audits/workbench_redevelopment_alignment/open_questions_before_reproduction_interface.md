# Open Questions Before Reproduction Interface

Date: 2026-05-16

The following questions must be resolved before implementing a unified reproduction CLI, paper table renderer, or metric computation path.

## Metric Definitions

- Final metric definitions are pending maintainer/team discussion.
- Which current paper metrics are frozen exactly as retained?
- Which candidate future metrics are allowed for public v0?
- Which metric names should be user-facing versus internal?

## Fallback / Regression Reporting

- Is fallback/regression still Regression@20?
- Should fallback/regression move to quantile, quartile, or distribution-based reporting?
- Should degradation be reported per engine, per route, per method role, or all three?

## Parseability / Extractability / Runnable SQL

- What is the exact definition of parseability?
- What is the exact definition of SQL extractability?
- What is the exact definition of runnable SQL?
- Are these metrics, status fields, or diagnostic annotations?
- How do they interact with execution readiness and correctness?

## Observability Metrics

- What is the final wording for plan observability?
- Which plan artifact types count toward observability?
- Should observability be reported as coverage, attribution, case-study support, or multiple fields?

## User Submission Format

- Should user submissions be a single SQL file, a manifest, or a directory?
- How are candidates mapped to `candidate_id`?
- How are method role and route declared?
- How should unsupported or partial submissions be represented?

## Output Root Location

- Should public runs default to `runs/local/<run_id>/`, `reports/user_runs/<run_id>/`, or `results/local/<run_id>/`?
- Which paths are ignored by git?
- Which outputs are safe to publish?

## LLM Baseline Scope

- Is public v0 retained-evidence only for LLM baselines?
- Are LLM baseline reruns in scope?
- If reruns are in scope, what model/version/prompt policy is allowed?
- Should any LLM dependency be optional and excluded from startup requirements?

## Paper Table Renderer

- Should renderer output reproduce retained paper tables exactly or produce release-native summaries?
- What comparison tolerance or mismatch policy is acceptable?
- Who approves any divergence from retained paper values?

## Implementation Gate

Do not implement the reproduction interface until these questions are resolved and the metrics contract is approved.
