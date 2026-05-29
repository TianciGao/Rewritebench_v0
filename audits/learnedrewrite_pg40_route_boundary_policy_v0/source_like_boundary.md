# Source-Like Boundary

Source packet: `audits/learnedrewrite_pg40_bounded_local_diagnostic_v0/source_like_review.md`.

PG40 source-like diagnostic counts:

- generated candidates reviewed: 29
- source-like/no-op diagnostic count: 2
- nontrivial generated candidates: 27
- unclear: 0

Source-like rows recorded in the PG40 diagnostic:

- `CONS_0036`
- `CONS_0037`

Policy:

- Source-like classification is diagnostic only.
- Source-like classification is not POCR.
- Source-like classification is not SER.
- Source-like classification is not a ranking metric.
- Source-like classification must not be used as a proxy for operation-atom coverage.
- Nontrivial string difference does not imply semantic improvement; local checker exactness remains result-consistency evidence only.

Any future interpretability claim for LearnedRewrite requires the separately deferred POCR external operation-atom evidence path.
