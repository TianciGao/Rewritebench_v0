# Static Case Package Validator v0.1

Status: implemented for evidence-mapping pilots

Command:

```bash
python scripts/dev/validate_case_package.py --mode evidence-pilot --case cases/PORT/PORT_0008
```

## Scope

Validator v0.1 is a static release-repo gate for case-package evidence pilots. It does not validate database semantics and does not inspect or modify the legacy repository.

Initial supported mode:

- `evidence-pilot`

Initial target scope:

- `PORT_0008`
- `PORT_0012`
- `PORT_0013`
- `PORT_0022`
- `PORT_0025`
- `PORT_0024`

## Checks

For each case, the validator checks:

- case path exists under `cases/PORT/<CASE_ID>`;
- `MIGRATION_PILOT.md` exists and states the evidence-pilot boundary;
- `evidence/runs_retention.yaml` exists and parses as YAML;
- `runs_retention.yaml` declares formal evidence-mapping status and no full case migration;
- denominator and paper-result flags remain false;
- formal pilot approval is recorded;
- original Spark plans are mapped with `do_not_delete_original: true`;
- sanitized public Spark plan copies exist and are public-safe;
- sanitized public files do not contain forbidden local path, host, or credential-keyword traces;
- formal pilot validation CSV exists and records public-safe rows;
- no raw `.log` files are present under the release case slice.

For `PORT_0024`, it also checks:

- `evidence/retained_controls/spark_result_check.sanitized_summary.json` exists;
- the summary parses as JSON;
- stdout/stderr log references use placeholders;
- raw stdout/stderr log path patterns are absent.

## Non-Goals

Validator v0.1 does not:

- run DB engines;
- execute case validation scripts;
- regenerate plans or result checks;
- inspect raw stdout/stderr logs;
- inspect or write the legacy repository;
- change denominator, paper results, Common-core membership, route evidence, or case admission status;
- certify a full migrated case package.

## Exit Codes

- `0`: all requested cases passed.
- `1`: one or more requested cases failed.
- `2`: argparse usage error.

## Future Extensions

Future validator modes should cover full copy-first case packages, manifest/schema/checker completeness, reports/results retained-evidence references, and Common-core denominator invariants before any broad migration.
