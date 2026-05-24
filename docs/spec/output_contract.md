# D035 User Output Contract

This contract describes local user-facing diagnostic output. It does not define
official metrics, paper tables, retained evidence, or leaderboard output.

## Exported Output Roots

Each user-facing run is exported under:

```text
output/results/<run_id>/
output/logs/<run_id>/
output/reports/<run_id>/
```

`output/results/<run_id>/` contains machine-readable run artifacts such as
selected rows, ledgers, copied candidate SQL, run manifests, local diagnostic
summaries, and optional verifier/timing/metrics support files.

`output/logs/<run_id>/` contains local logs, copied adapter workspaces,
configuration, and failure-bucket diagnostics.

`output/reports/<run_id>/` contains human-readable local diagnostic summaries
and boundary reports.

## Internal Transitional Staging

The current implementation may create:

```text
runs/user/<run_id>/
```

This path is internal source-run staging used before export. It may contain
candidate SQL captures, per-row workspaces, ledgers, summaries, and local
diagnostic files. It is not the public-facing output contract and must not be
committed.

## Official Surfaces

Top-level `reports/` and top-level `results/` are official/paper/release
surfaces. Ordinary user-run tasks must not write there. Promotion to those
surfaces requires separate authorization.

## Disallowed User-run Destinations

User-run artifacts must not be written to:

- `cases/`
- case-local `runs/`
- `case_sets/`
- `schemas/`
- `inventory/`
- top-level `reports/`
- top-level `results/`
- retained evidence directories

## Boundary Flags

Local user-output manifests should preserve these boundaries:

- `local_diagnostic_only: true`
- `official_metric_input: false`
- `paper_result_input: false`
- `retained_evidence_promoted: false`
- `leaderboard_input: false`

## Physical Migration Boundary

D035 targets a future public `benchmarks/` layout, but the physical migration is
not complete. Current `cases/`, `case_sets/`, `schemas/`, and `inventory/`
paths remain valid until a separately authorized migration updates resolvers,
tests, docs, and exports.
