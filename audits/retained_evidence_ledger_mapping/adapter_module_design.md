# Adapter Module Design Draft

Status: future implementation only. Do not create these modules in this task.

## Proposed Package Modules

Future modules:

- `src/sql_rewrite_bench/evidence/ledger_schema.py`
- `src/sql_rewrite_bench/evidence/legacy_reports_adapter.py`
- `src/sql_rewrite_bench/evidence/case_runs_adapter.py`
- `src/sql_rewrite_bench/evidence/ledger_builder.py`
- `src/sql_rewrite_bench/evidence/ledger_validation.py`

These modules should be designed against canonical case packages, aligned case sets, inventory, and the approved evidence ledger schema.

## Proposed Script Entrypoints

Future script entrypoints:

- `scripts/reproduce/build_retained_ledger.py`
- `scripts/metrics/compute_metrics_from_ledger.py`

These files are not created by this audit. The metrics script must not be implemented until the metrics contract is finalized.

## Module Responsibilities

`ledger_schema.py` should define the approved ledger row model, allowed enums, field-level validation, and serialization rules.

`legacy_reports_adapter.py` should read curated legacy report/result mappings and parse selected artifacts into ledger rows without copying reports/results or recomputing metrics.

`case_runs_adapter.py` should read canonical case package `evidence/runs_retention.yaml` files and public-safe retained evidence summaries. It must not write into case-local `runs/`.

`ledger_builder.py` should join adapter outputs with `case_sets/common_core_v0/`, `inventory/case_registry.csv`, denominator scaffolds, and control scaffolds.

`ledger_validation.py` should check row grain, required fields, denominator consistency, public hygiene boundaries, and unresolved states.

## Adapter Row-grain Rules

Adapters should emit one row per case, engine, route, method role, candidate/control, denominator row, and evidence source where possible.

If an artifact is only a paper summary, archive reference, or mixed-scope index, the adapter should emit reference rows or skip ledger emission until a curator approves row-grain parsing.

## Required Non-goals

Adapters must not:

- recompute metrics;
- update paper tables;
- change denominator values;
- change case membership;
- copy raw reports/results wholesale;
- expose raw logs or local paths;
- treat old paper tables as the canonical data model;
- write user outputs into case-local `runs/`.

## Implementation Gate

Future implementation should wait for:

- approved evidence ledger schema;
- approved metrics contract;
- approved runner output policy;
- selected retained-evidence public copy plan;
- tests for denominator-aware and role-aware row validation.
