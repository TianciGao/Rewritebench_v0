# Latest Paper Metrics Timing Protocol Alignment

Verdict: `completed_with_pdf_unavailable_caveat`

This audit aligns the latest-paper metric/timing direction recorded in D032 with the existing repository Metrics Contract v1 before any timing or metrics implementation.

No local copy of `Beyond_Faster_SQL (5).pdf` was found under `/home/tianci_gao`, `/mnt/data`, or `/tmp`, so the Table 6 metric extraction in this packet uses the explicit latest-paper scope supplied in D032 and this task context. A future check should re-verify these names/formulas against the PDF when it is available.

## Findings

- The latest-paper scope contains ten primary metrics across Coverage, Correctness, Performance, Interpretability, and Generalization.
- The existing `repository_spec/metrics_contract_v1.md` is historical for the latest-paper line because it still includes `Attribution Coverage` and `Speedup Retention`.
- Latest-paper alignment replaces that explainability/generalization pairing with `Positive Operation Coverage Rate` and `Cross-Engine GM Speedup Ratio`.
- Regression@20 should remain a reporting diagnostic/open question unless the team confirms it as a formal latest-paper metric.
- Generation is candidate emission. Preflight/ready/parseability should remain separate diagnostic status, not folded into Generation Rate.
- Performance must be exact-gated and timed-gated over paired source/candidate timings in the same engine/environment/run context.
- POCR remains deferred until the collaborator's operation-atom script and schema are stable.

## Boundary

This is audit/design only. It does not implement timing, metrics computation, POCR, skill folders, runner behavior, checker behavior, reports/results updates, retained-evidence promotion, paper tables, or leaderboard output.

## Recommended Next Safe Action

Authorize Phase 1: timing artifact schema design, using this packet's timing protocol and schema recommendations as the input. Keep it non-metric and local-diagnostic until retained-evidence/official-metrics promotion is separately approved.
