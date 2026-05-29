# Dry Run Report

This packet records a bounded no-live Repair-1 fake-provider dry run over the actionable Direct LLM original non-exact frontier.

Only 13 rows were selected because the frontier review marked `mismatch` and `candidate_execution_failed` rows as actionable for Repair-1:

- mismatch rows selected: 10
- candidate_execution_failed rows selected: 3
- total selected rows: 13

The five `unsupported_engine` Spark boundary rows were excluded because the Repair-1 scaffold treats them as support-policy boundary rows rather than repair candidates.

Dry-run summary:

- facade commands run: 3 engine-scoped commands
- selected rows: 13
- adapter-invoked rows: 13
- generated repaired candidates: 13
- candidate preflight passed rows: 13
- fail-closed rows: 0
- live LLM calls: 0
- DB execution/checker/timing/local_metrics/verifier commands: 0
- official metrics/paper rendering: 0

This is prompt, feedback-ingestion, extraction, candidate-generation, and metadata-writing evidence only. It is not correctness evidence, performance evidence, official metric evidence, paper-facing evidence, retained evidence, or a Track A 120 Repair-1 run.

Next safe action: authorize a tiny bounded live Repair-1 smoke over 3-6 actionable rows. Do not run Repair-1 Track A 120 until a bounded live smoke passes.
