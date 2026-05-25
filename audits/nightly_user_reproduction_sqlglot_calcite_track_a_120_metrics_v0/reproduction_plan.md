# Reproduction Plan

Scope: Common-core v0 Track A 120 for three deterministic routes: SQLGlot no-op, SQLGlot optimize schema-aware, and Calcite HEP fail-closed.

The plan used the existing user-side evaluation pipeline with DB execution, checker execution, and timing enabled only for these routes. Local diagnostic metrics were produced with the existing compute-local-metrics path.

No live LLM/API call was made. No API key was read. No POCR annotation JSONL or Stage B validation was generated. No top-level reports/results were updated.

Outputs were exported to D035-style local user paths under `output/results/<run_id>/`, `output/logs/<run_id>/`, and `output/reports/<run_id>/`. The `output/` tree remains local and uncommitted.
