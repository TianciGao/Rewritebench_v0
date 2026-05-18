# B-line User Entry Release Smoke v0

## Purpose And Scope

This task verifies the already implemented, hardened, and documented non-DB B-line user-entry MVP from a fresh-checkout and editable-install perspective.

This task is verification-only. It does not implement features, execute SQL, run DB engines, run checkers, collect timing, compute official metrics, render paper tables, implement SQLGlot/Calcite/R-Bot adapters, implement paper reproduction, implement retained-evidence adapters, migrate cases, update `case_sets/`, update inventory, update reports/results, change denominators, change paper results, or modify raw legacy evidence.

## Fresh-checkout Method Used

The smoke used a temporary local clone outside the release repo:

```text
/tmp/sqlrb_user_entry_release_smoke/Rewritebench_v0_smoke
```

The clone was created from:

```text
/home/tianci_gao/code/Rewritebench_v0
```

A temporary venv was created at `.venv-smoke/` inside the temporary clone.

## Editable Install Result

Editable install passed with:

```bash
.venv-smoke/bin/python -m pip install -e .
```

No DB, SQLGlot, Calcite, Java, LLM, timing, checker, or retained-evidence runtime dependency was introduced by the project package.

## Module Help Result

Module help passed:

```bash
.venv-smoke/bin/python -m sql_rewrite_bench.user_run --help
```

The help output exposed the expected user-entry options including `--case-set`, `--pool`, `--engine`, `--case-list`, `--adapter-command`, `--out`, `--adapter-timeout`, and `--dry-run`.

## Wrapper Help Result

Wrapper help passed:

```bash
.venv-smoke/bin/python scripts/user/run_user_benchmark.py --help
```

The wrapper remained a thin entrypoint to the same module implementation.

## Dry-run Smoke Result

Dry-run smoke passed with two Common-core PERF cases:

- selected rows: 2
- adapter-invoked rows: 0
- candidate-generated rows: 0
- extraction status: `skipped_dry_run`
- failure bucket: `none`

## Dummy Adapter Smoke Result

Dummy adapter smoke passed with two Common-core PERF cases:

- selected rows: 2
- adapter-invoked rows: 2
- candidate-generated rows: 2
- extraction status: `captured_from_candidate_file`
- failure bucket: `none`

## Output Hygiene Result

Expected run files were present for both smoke runs under:

- `runs/user/release_smoke_dry_run/`
- `runs/user/release_smoke_adapter/`

No case package, `case_sets/`, inventory, reports, results, denominator, paper-result, retained-evidence, or raw legacy evidence surface was modified.

## Git-ignore / Unstaged-output Result

In the temporary clone, `git status --short runs/user` produced no tracked changes. `git status --short --ignored runs/user` showed the smoke output as ignored local output.

The editable-install environment created expected temporary clone-local artifacts such as `.venv-smoke/`, package egg-info, bytecode cache, and `tmp_smoke_cases.txt`; these were outside the release repo and not staged.

## Boundaries Preserved

- Public runner skeleton implemented: yes.
- Non-DB MVP only: yes.
- DB execution implemented: no.
- Checker execution implemented: no.
- Official metrics computed: no.
- Paper tables rendered: no.
- Reproduction CLI implemented: no.
- Retained-evidence adapter implemented: no.
- `case_sets/` changed: no.
- Inventory changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Raw legacy evidence changed: no.

## Remaining Unsupported Features

- DB execution remains unsupported.
- Checker execution remains unsupported.
- Timing collection remains unsupported.
- Official metrics remain unsupported for user runs.
- Paper table rendering remains unsupported.
- Paper reproduction CLI remains unsupported.
- Retained-evidence adapter implementation remains unsupported.
- SQLGlot, Calcite, and R-Bot adapters are not implemented.
- User outputs remain local experiment outputs only and do not create retained evidence or a leaderboard.

## Exact Next Safe Action

Authorize a B-line user-entry publication-surface closeout or CI smoke wiring task. Keep case packages, `case_sets/`, inventory, denominators, reports/results, paper results, retained evidence, and raw legacy evidence unchanged unless a separate task explicitly authorizes those surfaces.
