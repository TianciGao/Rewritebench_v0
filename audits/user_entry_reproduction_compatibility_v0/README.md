# User-Entry / Reproduction Compatibility Audit

## Purpose

This packet audits the current user-entry and one-command reproduction prototype after Common-core 40 case-package normalization and public README normalization.

This is a compatibility audit and smoke task only. It does not implement full paper reproduction, compute official metrics, render paper tables, update reports/results, run DB/checker execution, or create a global leaderboard.

## Verdict

The non-DB user-entry adapter-capture path still works with the current Common-core case-package layout.

The optional PostgreSQL DB/checker diagnostic path needs reorganization before it is used with normalized case packages. The code still resolves executable PostgreSQL schema files from case-local `schema/postgres/ddl.sql` and `schema/postgres/load.sql`, but the current case-package layout moved executable schema assets to external `schemas/<SCHEMA_ID>/` packages.

## Current User-Facing Entrypoints

- Module CLI: `PYTHONPATH=src python -m sql_rewrite_bench.user_run`
- Thin wrapper: `python scripts/user/run_user_benchmark.py`
- Optional candidate-generation adapter: `python baselines/sqlglot/sqlglot_user_adapter.py --route noop|optimize`
- Developer/CI smoke: `python scripts/dev/run_user_entry_ci_smoke.py`

## Smoke Summary

- Module CLI help: passed.
- Wrapper CLI help: passed.
- SQLGlot adapter help: passed.
- Non-DB dry run over `PERF_0006` and `CONS_0005`: passed, 2 selected rows, 0 generated candidates, no DB/checker execution.
- Non-DB dummy-adapter capture over `PERF_0006` and `CONS_0005`: passed, 2 selected rows, 2 generated candidates, no DB/checker execution.
- User-entry unit tests: passed, 27 tests run with 1 SQLGlot dependency guard skipped.

Smoke outputs were created only under `runs/user/audit_user_entry_*`, recorded, and removed before commit.

## Compatibility Findings

- Selection is metadata-driven through `case_sets/common_core_v0/` and does not infer membership by scanning `cases/`.
- All 40 Common-core rows resolve to existing `sql/source.sql` files under the normalized case-package layout.
- Generated user outputs are guarded to `runs/user/<run_id>/` and reject case-local, `reports/`, `results/`, absolute, and parent-relative output roots.
- CLI help exposes optional DB/checker flags, but public docs emphasize the non-DB MVP and do not document the optional flags.
- Optional DB/checker mode is not compatible with normalized case packages until it resolves executable schema paths through manifest `schema.external_profile` or the case-package resolver.

## One-Command Smoke Recommendation

The safe public smoke path today is non-DB only. A short-term smoke can use:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --pool PERF \
  --engine postgres \
  --adapter-command "python tests/user_entry/fixtures/dummy_adapter.py" \
  --out runs/user/public_smoke_dry_run \
  --dry-run
```

Before documenting this as a polished public command, move the dummy adapter or a no-op public adapter out of `tests/`, or add a dedicated `--smoke` / `--limit` mode so a tiny case selection does not require a temporary case-list file.

## Deferred Work

- Full paper reproduction CLI.
- Official metrics computation.
- Paper table rendering.
- Retained-evidence adapter and report-output flow.
- DB/checker diagnostic mode repair for external schema packages.
- Public one-command smoke polish.

## Protected Boundary Summary

No source code, tests, docs, README files, cases, manifests, schemas, checker files, validation files, SQL files, case sets, inventory, reports, results, benchmark specs, repository specs, workflows, denominator scaffolds, paper results, or raw retained evidence were modified.

## Next Safe Action

Authorize a narrow user-entry repair task that updates optional DB/checker execution to resolve schemas through the v2 external-schema contract and aligns docs/CLI help around a public non-DB smoke command. Keep official metrics, paper rendering, retained-evidence parsing, reports/results updates, and leaderboard output out of scope.
