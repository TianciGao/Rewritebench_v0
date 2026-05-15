# Static Case Package Validator v0.2

Status: implemented

Validator path: `scripts/dev/validate_case_package.py`

## Purpose

Validator v0.2 extends the static release-repo validator from evidence-pilot checks to a future full-case gate.

It is intended to run before any copy-first full case migration pilot. It checks whether a release-repo case package has the required public structure, metadata, evidence mapping, public hygiene, and claim-boundary fields.

This validator does not migrate any case.

## Modes

### `evidence-pilot`

This is the v0.1 regression mode. It validates completed sanitized evidence-mapping pilot slices such as:

```bash
python scripts/dev/validate_case_package.py \
  --mode evidence-pilot \
  --case cases/PORT/PORT_0008
```

The mode checks case-local `MIGRATION_PILOT.md`, `evidence/runs_retention.yaml`, sanitized retained plan files, formal validation CSVs, and the `PORT_0024` result-check summary.

### `full-case`

This is the new v0.2 mode. It validates the expected shape of a future complete migrated case package:

```bash
python scripts/dev/validate_case_package.py \
  --mode full-case \
  --case cases/PORT/PORT_0004
```

Before any full case exists, use advisory mode:

```bash
python scripts/dev/validate_case_package.py \
  --mode full-case \
  --allow-failures \
  --case cases/PORT/PORT_0008 \
  --out audits/validator_trials/full_case_mode_advisory_results.csv
```

Advisory mode records failures but exits `0`, which allows expected-fail dry runs on partial evidence-only slices.

## Full-Case Checks

Full-case mode checks:

- `manifest.yaml` exists.
- Source SQL exists as `source.sql`, `sql/source.sql`, or a manifest-declared source path.
- Positive rewrite exists as `rewrite_pos_*.sql`, `sql/positives/*.sql`, or a manifest-declared positive path.
- Hard negative exists or the manifest declares a hard-negative not-applicable reason.
- Schema/data context exists through `schema/` or manifest-declared schema paths.
- Checker or normalization config exists through `checker/`, `validation/checker.yaml`, or manifest-declared checker path.
- Validation path exists through `validation/` or manifest-declared validation scripts.
- Provenance exists through `provenance/`, `metadata/provenance.yaml`, or manifest-declared provenance.
- Taxonomy exists through `taxonomy*.yaml`, `metadata/taxonomy.yaml`, or manifest-declared 4+1 taxonomy.
- `evidence/runs_retention.yaml` exists and records required retention semantics.
- README, migration pilot note, or notes directory exists.
- Public-facing files under the case slice pass local-path, host, credential-keyword, and raw stdout/stderr log path scans.
- Sanitized public evidence has mapped original legacy paths, do-not-delete status, public-safe status, and formal validation CSV support when expected.
- No file claims denominator changes, paper-result changes, case-membership changes, global leaderboard status, raw legacy evidence alteration, or completed full migration while required components are missing.

## YAML Handling

The validator uses PyYAML when available. If PyYAML is unavailable, it falls back to conservative text-level checks and reports the fallback in warnings.

No dependency installation is required or allowed.

## Static-Only Boundary

Validator v0.2 does not:

- run DB engines;
- execute validation scripts;
- run timing workloads;
- regenerate plans;
- inspect raw stdout/stderr logs;
- inspect or modify the legacy repository;
- change Common-core membership;
- change denominators;
- change paper results;
- change case admission status;
- certify scientific correctness.

The validator checks package shape, public hygiene, evidence mapping, and claim boundaries only.

## Output

The validator prints a readable console summary.

`--out <csv_path>` writes one row per case. For full-case mode, the CSV includes:

- `case_id`
- `case_path`
- `mode`
- `manifest_exists`
- `source_sql_exists`
- `positive_rewrite_exists`
- `hard_negative_status`
- `schema_context_exists`
- `checker_exists`
- `validation_path_exists`
- `provenance_exists`
- `taxonomy_exists`
- `evidence_runs_retention_exists`
- `runs_retention_parse_ok`
- `sanitized_evidence_scan_ok`
- `no_raw_local_path_ok`
- `no_denominator_change_claim_ok`
- `no_paper_result_change_claim_ok`
- `no_global_leaderboard_claim_ok`
- `full_case_structure_ok`
- `evidence_mapping_ok`
- `overall_status`
- `failure_reasons`
- `warnings`

`--json-out <json_path>` writes machine-readable details. `--json-output` remains available as a backward-compatible alias.

## Expected Behavior

Current evidence-only pilot slices should pass `evidence-pilot` mode and fail `full-case` mode because they are intentionally not complete migrated case packages.

Those failures are expected before full migration and should identify missing full-case components such as manifest, source SQL, rewrite SQL, schema, checker, validation, provenance, and taxonomy.

Future full copy-first migration pilots should pass `full-case` mode before scaling to additional cases.
