# Control-layer Next Adapter Recommendation

## Option A: rewrite_candidate_adapter_v0 Planning Or Skeleton

This is the most direct next step after control-layer closeout, but only planning is safe by default. A future bounded implementation would need explicit maintainer authorization for allowed input sources, emitted record types, method scopes, denominator joins, and validation outputs.

Recommended immediate form: `rewrite_candidate_adapter_v0` planning, not full implementation.

## Option B: Retained Paper-summary / Reports-results Triage Continuation

This remains useful for traceability and public release readiness. It is lower risk than candidate parsing if kept as summary/index work, but it does not advance candidate-row ledger coverage directly.

## Option C: Source/Positive/Hard-negative Manual Approval Cleanup

This would reduce later metric blockers by resolving evidence-index and approval caveats, especially hard-negative manual-review rows. It is safe if kept to audit and human-review planning, but should not infer outcomes or compute rates.

## Option D: Public Runner / Reproduction CLI Planning

Planning is safe, but implementation remains premature because candidate adapter boundaries, production ledger validation, and metric-readiness gates are not complete.

## Recommendation

Begin `rewrite_candidate_adapter_v0` planning. Do not implement a full candidate adapter unless the maintainer explicitly authorizes a bounded scope. Do not parse legacy raw retained evidence, compute metrics, render paper tables, emit metric-eligible rows, or consume control-layer rows as metric inputs yet.
