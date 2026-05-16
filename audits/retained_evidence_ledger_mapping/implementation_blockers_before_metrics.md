# Implementation Blockers Before Metrics

The following blockers must be resolved before implementing metrics computation, a paper table renderer, a unified reproduction CLI, or public runner output.

## Metrics Computation

- Final metric definitions are pending maintainer/team discussion.
- Exact/executed/timed gates need final wording.
- Parseability, SQL extractability, and runnable SQL definitions are pending.
- Performance regression metric choice is pending: Regression@20 versus quartile/distribution-based reporting or a combined approach.
- Observability metric wording is pending.
- Retained evidence adapters are not implemented.
- Reports/results curated copy is not done.

## Paper Table Renderer

- Old paper tables are comparison targets, not the canonical data model.
- The evidence ledger schema is still draft.
- The metrics contract is still draft.
- No paper result update is authorized.
- Renderer output location and review gates are not approved.

## Unified Reproduction CLI

- User submission format is pending.
- Output root policy is still draft.
- The CLI must not write into case-local `runs/`.
- Public runner scope is unresolved: retained evidence only versus fresh user runs.
- LLM baseline rerun scope is unresolved.
- Script inventory and reproduction path are not implemented.

## Public Runner Output

- Output root convention is pending.
- Run manifest fields are pending.
- Secret and local-path hygiene validation is not implemented.
- Case-local validation scripts remain retained legacy assets and are not final public runners.

## Safe Boundary

Until these blockers are resolved, the only safe next work is review and approval of schemas, contracts, output policy, and adapter design. No metrics, paper tables, denominator values, reports/results, or raw legacy evidence should change.
