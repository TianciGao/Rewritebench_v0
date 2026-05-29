# Local Metrics Integration Plan

Current local metrics behavior remains unchanged:

- Semantic Equivalence Rate is `N.A.` without verifier evidence.
- Local result checker exactness is Result Consistency, not formal semantic equivalence.
- POCR remains deferred pending external skill-adapter integration.

Future integration:

- Local metrics may read `output/results/<run_id>/verifier/semantic_equivalence_summary.json`.
- Semantic Equivalence Rate may be populated only when `decidable_count > 0`.
- Unknown, timeout, unsupported, and tool-error counts must remain visible.
- Metrics summaries must keep local-only boundary flags.
- Verifier evidence should strengthen correctness interpretation but must not gate exact-gated performance reporting.

Do not confuse:

- `exact` / Result Consistency Rate from `local_result_checker`
- `equivalent` / Semantic Equivalence Rate from VeriEQL or SQLSolver evidence

No official metrics or paper tables are authorized by this plan.
