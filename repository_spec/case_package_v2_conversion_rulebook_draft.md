# Case Package v2 Conversion Rulebook Draft

Status: branch-only draft for `feature/case-package-v2-external-schema`

This rulebook defines how current v1 and v1-compatible case packages should be converted to the v2 template. It is a conversion policy, not authorization for bulk migration, DB/checker execution, official metrics, paper rendering, denominator changes, case-set changes, retained-evidence deletion, reports/results updates, or leaderboard output.

## Final v2 Case-local Target

The intended clean case-local package is:

```text
cases/<POOL>/<CASE_ID>/
  README.md
  manifest.yaml
  sql/
    source.sql
    pos_01.sql
    neg_01.sql
  checker/
    checker.yaml
    normalization.yaml
    compare_config.yaml
    expected_rejections.yaml
  validation/
    run_validation.sh
    run_plan_collection.sh
```

Optional or compatibility-only case-local directories:

- `runs/`: only when non-empty retained evidence remains unmapped.
- `witness/`: only when lightweight human-readable witness metadata or a public-safe static witness is useful.

Not required case-local in v2:

- `schema/`
- `data/`
- `evidence/`
- `metadata/`
- `notes/`
- `sql/positives/`
- `sql/negatives/`
- engine-specific validation scripts

## External Asset Targets

Reusable schemas live under:

```text
schemas/<SCHEMA_ID>/
  schema_profile.yaml
  postgres/ddl.sql
  postgres/load.sql
  mysql/ddl.sql
  mysql/load.sql
  spark/ddl.sql
  spark/load.sql
```

Case evidence lives under:

```text
evidence/cases/<POOL>/<CASE_ID>/
  package_validation_summary.json
  runs_retention.yaml
  retained_controls/
  hard_negative/
  plans/
  notes/
```

Local user-run outputs stay under:

```text
runs/user/<run_id>/
```

Paper retained/reporting surfaces remain separate:

```text
results/retained/
reports/
```

## Manifest Field Contract

Canonical required fields:

- `case_id`
- `pool`
- `sql.source`
- `sql.positives` when positive rewrites exist
- `sql.negatives` when hard negatives exist
- `schema_ref.schema_id`
- `schema_ref.profile`
- `schema_ref.engines.<engine>.ddl`
- `schema_ref.engines.<engine>.load`
- `checker.config`
- `checker.normalization`
- `checker.compare_config`
- `checker.expected_rejections` when negatives exist
- `witness.mode`
- `witness.data_profile_status`
- `witness.correct_result_status`
- `evidence_ref.externalization_status`
- `evidence_ref.package_validation_summary`
- `evidence_ref.runs_retention`
- `validation.run_validation`
- `validation.run_plan_collection`

Canonical optional fields:

- `evidence_ref.retained_controls`
- `evidence_ref.hard_negative`
- `evidence_ref.plans`
- `witness.data_profile`
- `witness.correct_result`

Compatibility-only fields live under `compatibility.*`. They must not be scattered through canonical sections once a case is normalized.

## Conversion Rules

Keep case-local:

- `README.md`
- `manifest.yaml`
- `sql/source.sql`
- direct `sql/pos_XX.sql` and `sql/neg_XX.sql`
- `checker/`
- `validation/run_validation.sh`
- `validation/run_plan_collection.sh`

Move or copy-first externalize:

- `schema/schema_profile.yaml` to `schemas/<SCHEMA_ID>/schema_profile.yaml`
- `schema/<engine>/ddl.sql` to `schemas/<SCHEMA_ID>/<engine>/ddl.sql`
- `schema/<engine>/load.sql` to `schemas/<SCHEMA_ID>/<engine>/load.sql`
- `evidence/package_validation_summary.json` to `evidence/cases/<POOL>/<CASE_ID>/package_validation_summary.json`
- `evidence/runs_retention.yaml` to `evidence/cases/<POOL>/<CASE_ID>/runs_retention.yaml`
- `evidence/retained_controls/` to `evidence/cases/<POOL>/<CASE_ID>/retained_controls/`
- `evidence/hard_negative/` to `evidence/cases/<POOL>/<CASE_ID>/hard_negative/`
- `evidence/retained_plans/` to `evidence/cases/<POOL>/<CASE_ID>/plans/`
- stable notes to `evidence/cases/<POOL>/<CASE_ID>/notes/` or manifest compatibility notes

Merge into manifest:

- provenance, denominator eligibility, taxonomy, engine-support, artifact-path, source-family, and migration metadata
- legacy SQL path metadata
- case-local schema compatibility metadata
- validation legacy script metadata
- evidence externalization status

Optional/generated/external:

- `data_profile.yaml`
- `correct_result.csv`
- static witness files

Delete only after audit:

- empty case-local `runs/`
- placeholder-only case-local `runs/`
- duplicated `sql/positives/` and `sql/negatives/` after canonical direct paths and all references validate
- engine-specific validation scripts after wrappers and shared logic fully replace them
- case-local `schema/` after `schema_ref` runner and validator compatibility is accepted
- case-local `evidence/` after evidence is copy-first externalized and retention-mapped

Retain until mapped:

- non-empty case-local `runs/`
- public-safe retained evidence not yet externalized
- any evidence directory with uncertain privacy, provenance, or retention status

## Validation Script Consolidation

Each v2 case package converges to exactly two public entrypoints:

```text
validation/run_validation.sh
validation/run_plan_collection.sh
```

They are thin wrappers. They must accept:

- `--engine postgres|mysql|spark`
- `--target source|positive|negative|all`

They must resolve SQL, schema, checker, and evidence references through `manifest.yaml`; call shared logic under `scripts/` or `src/`; write only to user-specified local output roots; never write new outputs to case-local `runs/`; never store credentials; never compute official metrics; never create paper results; and never create leaderboard output.

Old engine-specific scripts are compatibility assets. If they are empty or wrapper-equivalent, delete after the new wrappers pass validation. If they contain unique logic, move that logic to shared `scripts/` or `src/` or archive public-safe notes under evidence notes, then delete only after validation. If uncertain, keep a compatibility copy and mark `manual_review_required`.

## Data Profile and Correct Result Policy

`data_profile.yaml` is not required case-local v2 content. It may be represented by `schemas/<SCHEMA_ID>/schema_profile.yaml`, generated by validation tooling, or stored as lightweight witness metadata.

`correct_result.csv` is not required case-local v2 content. The default runtime checker oracle is source SQL result versus candidate SQL result in the declared schema context. Static retained correct results may be stored under `evidence/cases/<POOL>/<CASE_ID>/` when public-safe and available. Absence of static `correct_result.csv` must not block user-run DB/checker execution if source-as-oracle execution is available.

## Evidence and Runs Cleanup Rules

Empty or placeholder-only case-local `runs/` may be deleted after audit. Non-empty retained evidence must be copy-first externalized or retention-mapped before deletion. Sensitive raw logs, private local paths, prompt traces, token traces, API/model traces, stdout/stderr/debug dumps, and credentials must not be copied to public evidence.

Case-local `evidence/` follows the same copy-first externalization rule. `evidence/cases/` is not `results/retained/`; it is not `runs/user/`; and it does not create official metric inputs unless separately authorized.

## Batch Converter Algorithm

Phase A, read-only inventory:

- scan the case package
- classify assets
- build a file disposition plan
- perform no writes

Phase B, non-destructive conversion:

- create direct SQL paths
- create `schema_ref`
- create `evidence_ref`
- create validation wrappers
- copy-first externalize schema assets
- copy-first externalize public-safe evidence
- retain compatibility files

Phase C, validation:

- run v2 reference validator
- run internal format validator
- run protected-path checks
- optionally run non-mutating runner compatibility smoke

Phase D, cleanup:

- delete only empty, placeholder, or duplicated compatibility assets
- never delete retained evidence without mapping

Phase E, batch commit:

- use explicit `git add`
- stage only intended conversion outputs
- never change denominator, paper result, report/result, inventory, or case-set files unless a separate task authorizes it

## Stop Conditions

Stop conversion if any of these occur:

- missing `sql/source.sql`
- missing required positive SQL for a positive case
- missing required checker config
- unresolved `schema_ref`
- uncertain evidence classification
- non-empty `runs/` without retention mapping
- sensitive trace or private local path detected
- validator failure
- protected path change
- denominator or paper-result change
- global leaderboard output

## Next Safe Action

Plan a converter dry run over `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011` that produces file disposition plans only, without converting all files yet.
