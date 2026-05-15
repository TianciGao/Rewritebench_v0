# PORT_0004 Public Hygiene Fix Report

Date: 2026-05-16

## Scope

This report records the release-repo-only fix for the public hygiene issue found during the first copy-first full case migration pilot for `PORT_0004`.

This is not a new migration, not Common-core 40 migration, not DB validation, and not evidence regeneration.

## Original Failure Cause

Validator v0.2 failed the initial `PORT_0004` full-case pilot because two copied Spark plan files in the release repo contained local temporary-path traces:

- `cases/PORT/PORT_0004/runs/spark/plans/rewrite_neg_02_spark.txt`
- `cases/PORT/PORT_0004/runs/spark/plans/rewrite_pos_02_spark.txt`

The legacy originals remain mapped and do-not-delete. They were not modified.

## Fix Strategy

The fix used the release-repo copied plan files as the sanitization input. No engine was rerun and no legacy file was sanitized in place.

Actions performed:

- Replaced the two release-repo run-plan copies in place with sanitized public-safe content.
- Replaced local temporary-path references with `<LOCAL_TMP_PATH_REDACTED>`.
- Preserved Spark plan structure, operator names, table names, column names, SQL expressions, case labels, and rewrite labels.
- Created canonical sanitized retained-plan evidence under `evidence/retained_plans/`.
- Updated `evidence/runs_retention.yaml` to map three layers: original legacy artifacts, sanitized release run-plan copies, and canonical sanitized retained evidence.

## Sanitized Retained Evidence

| Evidence role | Sanitized public retained evidence |
|---|---|
| hard-negative rejection evidence; plan/failure observability | `cases/PORT/PORT_0004/evidence/retained_plans/rewrite_neg_02_spark.sanitized.txt` |
| positive rewrite plan evidence; plan/failure observability | `cases/PORT/PORT_0004/evidence/retained_plans/rewrite_pos_02_spark.sanitized.txt` |

## SHA256 Before And After

| File | Raw release-copy SHA256 before fix | Sanitized release/canonical SHA256 after fix |
|---|---|---|
| `runs/spark/plans/rewrite_neg_02_spark.txt` | `09579d82601b10ca6a3fd109efe1b053fa7ced9378543f3e3e8f7a309e4ece96` | `300a600e28245e0ad21d6e68c332f3c402d2a958fb70d38ab5d8cc09ea16c8cd` |
| `runs/spark/plans/rewrite_pos_02_spark.txt` | `e1f315df10a95eb21b61c205fec56f93d592a433830a09eaa82965e3e223aad1` | `c55fd557bded085fe90695c1a6f49d28898b13f8f76c73a62ae19d9cddee9a04` |

## Validation Results

Public hygiene scan: pass.

- No forbidden public hygiene patterns remain under `cases/PORT/PORT_0004`.

YAML validation: pass.

- `manifest.yaml` parsed.
- `evidence/runs_retention.yaml` parsed.
- `taxonomy_trial_v0.3.yaml` parsed.

JSON validation: pass.

- JSON files under `provenance/` and `runs/` parsed.

Validator v0.2 full-case result after fix: pass.

- `PORT_0004` now passes `validate_case_package.py --mode full-case`.

Evidence-pilot regression: pass.

- The six prior evidence-pilot slices passed 6/6.

Python compile: pass.

- `scripts/dev/validate_case_package.py` compiled successfully.

## Non-Changes

- Legacy repo modified: no.
- Legacy case files modified: no.
- Legacy runs modified: no.
- Legacy reports/results/scripts/manifests/checkers/validation/evidence artifacts modified: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Common-core 40 migration started: no.
- No DB engines were run.
- No evidence was regenerated.

## Pilot Completion Status

`PORT_0004` is now pilot-complete for the copy-first full case migration pilot scope only.

This does not authorize deletion of the legacy `PORT_0004` case or any legacy evidence. Raw legacy artifacts remain retained through mapping and do-not-delete.

## Git History Note

The previous pushed pilot commit included the raw release copies before this hygiene fix. If the public repository history itself must contain no historical local temporary-path traces, that requires a separate history-cleanup decision and procedure. No history rewrite was performed in this task.

## Next Safe Action

Review the completed `PORT_0004` pilot and decide whether to proceed to a `PORT_0008` full copy-first pilot to test integration with already sanitized evidence mapping.
