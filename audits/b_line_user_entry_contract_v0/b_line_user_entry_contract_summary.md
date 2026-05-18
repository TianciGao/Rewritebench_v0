# B-line User Entry Contract v0

## Purpose And Scope

This packet starts B-line public workbench construction by defining a user-facing algorithm test entry contract. It is design-only. It does not implement a public runner, reproduction CLI, retained-evidence adapter, metrics computation, paper renderer, case migration, denominator update, case-set membership update, or reports/results migration.

## Current Blocker Context

A-line metric readiness is closed for public v0 planning, and the wave004 blocker packet confirmed that non-Common-core case migration is paused: 97 remaining rows were reviewed, zero were policy-unlocked for migration, 13 remain manual-review, 77 remain backlog-defer, and 7 require orphan/registry review. B-line can proceed on user-entry design because it can operate against existing static case sets and inventories without migrating additional cases.

## User-entry-first Rationale

The public workbench needs a stable way for external users to run their own rewrite algorithm before paper reproduction or retained-evidence rendering is implemented. A user-entry contract establishes case selection, adapter I/O, local output layout, ledger schema, report minimums, and output boundaries. This avoids mixing user experiments with retained paper evidence and keeps future implementation bounded.

## Proposed Command Model

Future command shape:

```bash
python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --pool PERF \
  --engine postgres \
  --adapter-command "python my_rewriter.py" \
  --out runs/user/<run_id>
```

Additional future selectors may include `--pool all`, `--engine all`, and `--case-list path/to/cases.txt`. This task does not implement the command.

## Case Selection Contract

Selection must use release metadata, not physical directory guessing.

- `--case-set common_core_v0` resolves through `case_sets/common_core_v0/manifest.yaml` and `case_sets/common_core_v0/cases.csv`.
- `--pool PERF|CONS|PORT|LONGTAIL|all` filters case rows by registry or case-set pool metadata.
- `--case-list path/to/cases.txt` intersects explicit case ids with the selected case set or registry scope.
- `--engine postgres|mysql|spark|all` expands through denominator or engine-support metadata, with `all` resolving to the approved engine list.
- MVP selection should default to Common-core v0 and Track A same-engine rows only.
- Non-Common-core staged/backlog cases may be selected later only after separate governance and runner-safety authorization.

## Adapter Contract

The future user adapter is a command invoked once per selected case-engine row. The runner supplies case metadata and file paths, and the adapter returns candidate SQL.

Minimum adapter inputs:

- `case_id`
- `pool`
- `engine`
- `source_sql_path`
- schema profile path or engine schema paths when available
- checker config path when available
- run workspace path

Minimum adapter output:

- candidate SQL on stdout or a `candidate.sql` path in the provided workspace
- optional structured status file for diagnostics

Adapter output is local user experiment output. It is not retained paper evidence, does not update reports/results, and does not create a leaderboard.

## Local Output Policy

Future local output root:

```text
runs/user/<run_id>/
  config.yaml
  selected_cases.csv
  candidate_sql/
  ledger.csv
  summary.json
  failures.csv
  report.html or report.md
```

User outputs must not be written into case-local `runs/`. User outputs must not enter `results/retained/`, must not modify `reports/evaluation/`, must not modify case packages, must not update `case_sets/`, and must not create a leaderboard.

## Ledger And Output Schema

The future user-run ledger should use a minimal `user_run_candidate_cell` row grain. MVP columns should include:

`run_id`, `case_id`, `pool`, `engine`, `denominator_id`, `planned`, `selected`, `adapter_invoked`, `candidate_generated`, `candidate_sql_path`, `extraction_status`, `execution_status`, `checker_status`, `exact_status`, `timed_status`, `failure_bucket`, `artifact_path`, and `notes`.

This schema supports diagnostics and later validation. It does not by itself compute official metrics.

## Report And Visualization Contract

The future static report should include:

- run config panel
- selected case, pool, and engine summary
- denominator funnel: planned, selected, generated, executed, exact, timed
- pool breakdown
- engine breakdown
- failure bucket table
- case-level failure drilldown
- artifact links
- no-global-leaderboard warning
- paper-evidence separation warning

The report is local user output. It must not be treated as a paper table or retained result.

## Relationship To Later Paper Reproduction Entry

Paper reproduction is a later B-line task. It should reuse case selection semantics, ledger/report schema, output policy, and report-renderer components where possible. It must remain separate from user-submitted algorithm runs because retained paper evidence has stricter provenance and denominator requirements.

## File Lifecycle Policy

This audit directory is construction evidence and defaults to `MAINTAINER_ARCHIVE`. A future public runner module and public docs may become `PUBLIC_FINAL` only after implementation and validation are separately authorized. Local run outputs under `runs/user/` are local/private runtime artifacts and should not be committed by default.

## Exact Next Safe Action

Authorize `b_line_user_entry_mvp_v0` to implement a minimal non-DB user runner skeleton that resolves Common-core v0 selections, invokes a user adapter in a per-row workspace, captures candidate SQL and diagnostics into `runs/user/<run_id>/`, and validates output boundaries without computing metrics or modifying retained evidence.
