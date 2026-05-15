# PORT_0013 Formal Evidence Mapping Pilot

Status: formal sanitized evidence-mapping pilot only

This is an evidence-mapping pilot only for PORT_0013. It is not a complete migrated case package.

## Scope

This pilot promotes already validated Route B sanitized trial outputs into case-local retained plan evidence for the release repository.

Created public evidence slice:

- `evidence/runs_retention.yaml`
- `evidence/retained_plans/rewrite_neg_01.sanitized.txt`
- `evidence/retained_plans/rewrite_pos_01.sanitized.txt`

## Non-Scope

This pilot does not migrate or create:

- source SQL
- positive or negative rewrite SQL
- schema or witness data
- checker files
- validation scripts
- manifest files
- raw run directories
- provenance or taxonomy files

Those remain future case migration work.

## Legacy Evidence Handling

Source SQL, schema, checker, validation scripts, provenance, taxonomy, manifest, and raw runs remain in the legacy repository. No legacy evidence was modified, moved, deleted, overwritten, or sanitized in place.

The sanitized retained plan copies were promoted from validated Route B trial outputs. Original Spark plan artifacts remain do-not-delete and mapped through `evidence/runs_retention.yaml`.

Raw local path traces are not included in the public retained plan copies.

## Scientific Scope

This pilot does not change denominator, paper results, Common-core membership, route evidence, case admission status, benchmark claims, or result interpretation.
