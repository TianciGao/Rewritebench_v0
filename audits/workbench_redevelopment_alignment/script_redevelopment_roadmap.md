# Script Redevelopment Roadmap

Date: 2026-05-16

## Purpose

This roadmap proposes future module and script organization for the public workbench. It does not create implementation files.

## Proposed Python Package Modules

`src/sql_rewrite_bench/cases/`

- case-set loading;
- case package discovery;
- manifest parsing;
- denominator scaffold loading.

`src/sql_rewrite_bench/evidence/`

- evidence ledger schema;
- retained evidence adapters;
- runs-retention readers;
- public hygiene checks.

`src/sql_rewrite_bench/metrics/`

- metrics contract validation;
- denominator-aware aggregations;
- role-aware metric rendering;
- correctness, timing, and observability gates.

`src/sql_rewrite_bench/runners/`

- user candidate runner;
- engine execution wrappers;
- checker invocation boundaries;
- output root management.

`src/sql_rewrite_bench/reports/`

- report renderer;
- retained evidence summaries;
- paper-table comparison helpers;
- public report validation.

## Proposed Script Entrypoints

`scripts/user/`

- stable user-facing runner commands;
- candidate submission helpers;
- output-root setup.

`scripts/reproduce/`

- retained evidence reproduction commands;
- static package verification;
- report rendering from approved ledgers.

`scripts/metrics/`

- metric-contract validation;
- approved metric rendering;
- denominator-aware summaries.

`scripts/dev/`

- migration helpers;
- validators;
- development-only audits;
- non-user-facing maintenance scripts.

## Sequencing

1. Finalize evidence ledger schema.
2. Finalize public runner output policy.
3. Finalize metrics contract after maintainer/team review.
4. Implement retained evidence adapter.
5. Implement static CLI smoke commands.
6. Implement user candidate runner.
7. Implement report renderer.
8. Add tests/CI smoke.

## Non-Goals For This Task

- No implementation files are created.
- No legacy scripts are copied.
- No DB engines are run.
- No metrics are computed.
- No reports/results are updated.
