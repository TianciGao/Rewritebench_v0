# Canonical Metrics Readiness

Canonical metrics are not ready yet.

This task intentionally did not run timing and did not run
`compute-local-metrics`.

Required sequence before canonical local metrics:

1. Run exact-gated timing over the 81 exact rows from this diagnostic.
2. Run the canonical user metrics path only after timing output exists:
   `python -m cli.main user compute-local-metrics`.
3. Review canonical `local_metrics.py` outputs, not hand-computed route cards.

This execution/checker packet is a source diagnostic for the next timing gate,
not a metrics artifact.
