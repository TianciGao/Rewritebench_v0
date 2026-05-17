# SQLGlot Non-Timing Projection Report

## Purpose And Scope

This audit step projects approved SQLGlot status evidence into sanitized non-timing CSV files.
It does not fill candidate ledgers, compute metrics, authorize metric input, or read artifact payloads.

## Projection Summary

- Projections created: 2
- Projection rows total: 137
- Parser-ready projections: 2

## Projection Index

- `projection_SGL011_sqlglot_optimize`: 65 rows, parser_ready=true
- `projection_SGL011_sqlglot_noop`: 72 rows, parser_ready=true

## Boundary Confirmation

- Timing/speedup/latency fields are not retained.
- Raw logs, stdout/stderr payloads, prompts, tokens, and model traces are not opened or retained.
- Generated/ready are not inferred from checker artifact path presence.
- Metrics computed: false
