# Canonical Case Package Layout v1

Status: locked target policy for future public-release case migration

This document defines the canonical target layout for SQL-RewriteBench public-release case packages. It is a migration target, not a statement that the legacy repository already follows this layout.

`PORT_0004` was migrated as a legacy-compatible copy-first pilot. That pilot proves the copy-first process and validator gate can work, but it does not redefine the canonical public-release layout. `PORT_0008` should be considered the first canonical-layout pilot candidate if a later task approves a canonical-layout full-case migration pilot.

This layout policy does not authorize file movement, case migration, evidence regeneration, Common-core migration, denominator changes, paper-result changes, or case membership changes.

## Layout Labels

- `[MUST]`: required for a migrated public-release case package.
- `[SHOULD]`: strongly recommended for public-release clarity, review, and validation.
- `[OPTIONAL]`: permitted when useful, but not required for all cases.
- `[LOCAL]`: local runtime output; should not be committed as default public evidence.
- `[DEFER]`: allowed to remain incomplete during staged migration, with explicit notes.
- `[PRIVATE]`: private or external archive reference only; raw contents are not public by default.

## Canonical Tree

```text
cases/<POOL>/<CASE_ID>/
  README.md                                      [SHOULD]
  manifest.yaml                                  [MUST]

  sql/                                           [MUST]
    source.sql                                   [MUST]
    positives/                                   [MUST when positive rewrites exist]
      pos_01.sql
    negatives/                                   [MUST when hard negatives apply]
      neg_01.sql
    dialect_variants/                            [OPTIONAL]
      postgres/
      mysql/
      spark/

  schema/                                        [MUST]
    postgres/                                    [SHOULD when PostgreSQL is supported]
      ddl.sql
      load.sql
    mysql/                                       [SHOULD when MySQL is supported]
      ddl.sql
      load.sql
    spark/                                       [SHOULD when Spark is supported]
      ddl.sql
      load.sql
    schema_profile.yaml                          [SHOULD]

  data/                                          [SHOULD]
    data_profile.yaml                            [SHOULD]
    witness_profile.yaml                         [SHOULD when witness data is used]
    fixtures/                                    [OPTIONAL]

  checker/                                       [MUST when result comparison is used]
    checker.yaml
    normalization.yaml
    compare_config.yaml
    expected_rejections.yaml                     [SHOULD when hard negatives apply]

  validation/                                    [SHOULD]
    run_postgres_validation.sh                   [SHOULD when PostgreSQL is supported]
    run_mysql_validation.sh                      [SHOULD when MySQL is supported]
    run_spark_validation.sh                      [SHOULD when Spark is supported]
    run_postgres_plan_collection.sh              [OPTIONAL]
    run_mysql_plan_collection.sh                 [OPTIONAL]
    run_spark_plan_collection.sh                 [OPTIONAL]

  evidence/                                      [MUST]
    runs_retention.yaml                          [MUST]
    retained_controls/                           [SHOULD when controls are retained]
    retained_plans/                              [SHOULD when plans are retained]
    hard_negative/                               [SHOULD when hard negatives apply]
    package_validation_summary.json              [SHOULD]

  metadata/                                      [MUST]
    provenance.yaml                              [MUST]
    taxonomy.yaml                                [MUST]
    engine_support.yaml                          [MUST]
    denominator_eligibility.yaml                 [MUST for frozen-set candidates]
    artifact_paths.yaml                          [SHOULD]

  notes/                                         [SHOULD]
    witness_design_notes.md                      [OPTIONAL]
    risk_notes.md                                [OPTIONAL]
    migration_notes.md                           [SHOULD during migration]

  runs/                                          [DEFER legacy retained evidence only]
```

## Directory Semantics

### `manifest.yaml`

`manifest.yaml` is the primary machine-readable case index. It should point to source SQL, rewrites, schema/data context, checker configuration, validation commands, retained evidence, provenance, taxonomy, engine support, artifact paths, denominator eligibility, and migration notes.

Manifest fields must not change denominator, paper results, Common-core membership, case admission, or benchmark claims unless a separate approved decision says so.

### `sql/`

`sql/` contains case SQL only. It is not a location for method outputs, generated result files, engine logs, timing outputs, or ad hoc scratch artifacts.

Use:

- `sql/source.sql` for the canonical source query.
- `sql/positives/` for positive rewrites or approved target adaptations.
- `sql/negatives/` for hard negatives when applicable.
- `sql/dialect_variants/` only for explicit dialect variants that are part of the case package, not method-generated outputs.

### `schema/`

`schema/` contains engine-specific DDL/load assets and a schema profile. It should be sufficient for users and validators to understand the data context without treating local run residue as source truth.

### `data/`

`data/` contains profiles, witness descriptions, and optional public fixtures. Large private datasets, local DB dumps, and raw runtime directories are not canonical case-package contents unless separately approved and mapped.

### `checker/`

`checker/` contains comparison, normalization, and expected-rejection configuration. Hard negatives are checker controls; they are not method-generated failures and must not be reported as global leaderboard outcomes.

### `validation/`

`validation/` contains public validation and plan-collection entrypoints. These scripts may create local outputs when a user runs them, but new run outputs must not be written into case-local `runs/` by default.

### `evidence/`

`evidence/` is the public retained-evidence index surface. `evidence/runs_retention.yaml` is mandatory for migrated public cases, including cases with legacy `runs/`.

Evidence must distinguish:

- public-safe retained controls;
- public-safe retained plans;
- sanitized public copies;
- hard-negative evidence summaries;
- private/original archive references;
- external archive references;
- do-not-delete original legacy artifacts.

Raw local path traces, raw stdout/stderr log paths, credentials, prompt/API traces, and private runtime state must not appear in public retained evidence.

### `metadata/`

`metadata/` holds stable machine-readable case metadata. `denominator_eligibility.yaml` records denominator and frozen-set eligibility boundaries; it must not by itself add a case to Common-core or change paper results.

### `notes/`

`notes/` contains human-readable design, risk, and migration notes. Notes must not override manifest, case-set, or evidence-retention metadata.

### `runs/`

`runs/` is legacy retained evidence only. It is not the default location for new outputs.

Rules:

- Existing legacy run evidence may be retained during migration only through `evidence/runs_retention.yaml`.
- New public runner output should be written outside case-local `runs/`.
- Raw legacy `runs/` files that are not public-safe must be sanitized, summarized, archived, or excluded from public retained evidence through explicit mapping.
- No deletion or cleanup of legacy `runs/` is authorized by this layout policy.

## Case-Set Membership

`case_sets/` controls Common-core, backlog, and release membership. Physical case package layout must not be used to duplicate cases across denominators or imply membership changes.

This policy does not change:

- Common-core 40 membership;
- Track A denominator;
- paper results;
- case admission status;
- any benchmark claim.

## Reporting Boundary

The public release must not introduce a global leaderboard. Reports must remain role-aware and denominator-aware. Performance claims remain limited to exact and timed eligible rows.

## Migration Use

Future full-case migration prompts should reference this document before copying or restructuring any case package.

Validator v0.2 checks full-case completeness and hygiene, but it does not yet enforce all canonical layout paths. A later validator version should add canonical-layout conformance checks after the first canonical-layout pilot is approved.
