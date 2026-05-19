# v2 Batch Conversion Algorithm

## Input Assumptions

- The converter runs only on `feature/case-package-v2-external-schema` unless a later task explicitly changes branch policy.
- Input cases are explicitly listed by case id and pool.
- The converter has no authority to change `case_sets/`, inventory, denominator files, paper results, reports/results, or leaderboard outputs.
- DB/checker execution, timing, official metrics, and paper rendering are out of scope.
- The converter must be able to produce a read-only plan before performing writes.

## Phase A: Read-only Inventory

For each case:

1. Parse `manifest.yaml`.
2. List known case-local directories and files.
3. Classify SQL assets, checker assets, schema assets, evidence assets, metadata assets, notes, validation scripts, and runs.
4. Detect sensitive/private evidence patterns such as credentials, local absolute paths, prompt traces, token traces, API/model traces, stdout/stderr/debug dumps, and raw logs.
5. Build a file disposition plan.
6. Write no case files, schema files, evidence files, project-control files, or reports/results.

Stop if source SQL, required checker config, evidence classification, or retained runs classification is unclear.

## Phase B: Non-destructive Conversion

Allowed writes in a separately authorized converter implementation:

1. Create direct `sql/pos_NN.sql` and `sql/neg_NN.sql` copies when v1 nested SQL exists.
2. Create or normalize `manifest.yaml` canonical fields.
3. Create `schema_ref` and copy schema assets into `schemas/<SCHEMA_ID>/`.
4. Create `evidence_ref` and copy public-safe evidence into `evidence/cases/<POOL>/<CASE_ID>/`.
5. Create thin validation wrappers when missing.
6. Record legacy paths under `compatibility.*`.

Forbidden during Phase B:

- deleting compatibility files
- editing case-set membership
- editing denominator files
- editing reports/results
- running DB/checker execution
- collecting timing
- computing official metrics
- creating leaderboard output
- writing to case-local `runs/`

## Phase C: Validation

Required gates:

1. YAML parse for all changed manifests.
2. v2 reference validator.
3. internal format validator.
4. external schema path checks.
5. external evidence path and public hygiene checks.
6. validation wrapper existence and mode checks.
7. protected-path checks for `case_sets/`, inventory, reports, results, denominator files, and paper-result files.
8. git diff checks.

Optional gates:

- Non-mutating runner compatibility smoke.
- Read-only diff review for generated conversion plan.

## Phase D: Cleanup

Cleanup is separate from initial conversion. It may delete only:

- empty directories proven empty
- placeholder-only `runs/`
- duplicated nested SQL directories after direct SQL refs validate
- wrapper-equivalent engine-specific validation scripts after wrappers pass
- case-local schema only after schema_ref runner and validator compatibility is approved
- case-local evidence only after copy-first externalization and retention mapping are approved

Never delete:

- non-empty retained runs without mapping
- evidence with uncertain sensitivity
- raw retained evidence without explicit approval
- paper retained results

## Phase E: Batch Commit

Commit strategy:

1. Use explicit `git add` only.
2. Stage only intended case, schema, evidence, audit, and project-control files.
3. Never use `git add .`.
4. Commit each bounded batch with a clear task title.
5. Push only the feature branch unless a later merge task is explicitly authorized.
6. If run-log commit/push fields need finalization, use one small follow-up project-control commit.

## Rollback Strategy

If validation fails before commit:

- leave files in place for inspection if useful
- record the failure in audit outputs
- do not continue to the next case
- do not delete evidence or compatibility files

If a committed batch must be reverted:

- revert the conversion commit with a normal non-interactive git revert
- do not use destructive reset
- preserve audit trail
- document which validation gate failed

## Stop Conditions

Stop immediately on:

- missing `sql/source.sql`
- missing required positive or negative SQL
- missing checker config
- unresolved `schema_ref`
- missing external schema file after copy-first
- evidence classification uncertain
- non-empty `runs/` without retention mapping
- sensitive trace detected
- validator failure
- protected path changes
- denominator or paper-result change
- global leaderboard output
