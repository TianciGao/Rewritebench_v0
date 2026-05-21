# Nonblocking Caveats

These caveats do not block export planning, but they must remain visible before any actual release tag or export branch.

## README Language Posture

The current top-level README is Chinese. D030 permits this on the construction branch, but an English primary README or bilingual public entrypoint is required before the final public artifact release.

## Citation Metadata

`CITATION.cff` is valid and placeholder-safe. DOI, final paper metadata, and individual author metadata remain unset and must not be invented.

## PERF_0077 / PERF_0082 Provenance

`PERF_0077` and `PERF_0082` retain nonblocking source-path provenance uncertainty. Public release text must not claim exact JOB source paths for those cases.

## Reports/Results Boundary

`reports/` and `results/` currently contain boundary README files only. No paper tables, official result artifacts, retained-evidence migration, or reports/results regeneration was performed.

## Deferred Timing, Metrics, Paper Rendering, and Reproduction

Timing/speedup diagnostics, official metrics, paper table rendering, retained-evidence adapter integration, reports/results migration, and full paper reproduction remain deferred and unauthorized.

## MySQL/Spark Execution Status

The user-entry engine router includes MySQL and Spark fail-closed stubs only. PostgreSQL is the only implemented local diagnostic DB backend.

## Release Mechanics

No release tag or export branch has been created. A later export/tag planning task must decide branch/tag naming and exact release mechanics before any release action.
