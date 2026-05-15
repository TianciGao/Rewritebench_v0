# PORT_0004 Copy-First Full Case Migration Pilot

Date: 2026-05-15

## Scope

This task attempted the first copy-first full case migration pilot for `PORT_0004`.

This is one case only. It is not Common-core 40 migration, not batch migration, not evidence regeneration, not a DB rerun, and not authorization to delete or clean legacy files.

Pilot completion status: pilot-complete after release-repo hygiene fix.

The initial release-repo case package was copied and mapped, but validator v0.2 full-case mode did not pass because two copied Spark plan files contained public hygiene scan hits. A follow-up release-repo-only hygiene fix sanitized those copied plan files in place and created canonical sanitized retained-plan evidence under `evidence/retained_plans/`. Validator v0.2 full-case mode now passes for `PORT_0004`.

## Why PORT_0004 Was Selected First

`PORT_0004` was selected because the prior PORT manual-review resolution cleared it for evidence-index normalization and physical migration pilot. It was the lowest-risk PORT candidate and was not part of the six blocked cases requiring formal sanitized Spark plan evidence mapping.

## Legacy State Snapshot

- legacy pwd: `/home/tianci_gao/code/sql-rewrite-bench-artifact-clean`
- legacy branch: `artifact/case-package-contract-alignment-clean`
- legacy HEAD: `7e438b5d767922007a1ca456fed0bf2e237a8952`
- legacy status: `## artifact/case-package-contract-alignment-clean...origin/artifact/case-package-contract-alignment-clean [behind 7]`
- legacy diff name-status:
  - `M reports/evaluation/common_core_v0/REVIEWER_REPRODUCTION_V1/deterministic/deterministic_reproduction_log_v1.txt`
  - `M reports/evaluation/common_core_v0/REVIEWER_REPRODUCTION_V1/deterministic/deterministic_reproduction_plan_v1.md`
  - `M reports/evaluation/common_core_v0/REVIEWER_REPRODUCTION_V1/deterministic/deterministic_reproduction_status_v1.csv`
  - `M reports/evaluation/common_core_v0/REVIEWER_REPRODUCTION_V1/reviewer_reproduction_log_v1.txt`
  - `M reports/evaluation/common_core_v0/scripts/render_speedup_slice_summary_v1.py`
- legacy log:
  - `7e438b5d docs: rewrite README for common-core reproducibility`
  - `6eefb7c2 docs: rewrite README for common-core reproducibility`
  - `c1cc0ff1 artifacts: add common-core reproduction input bundle`

The legacy repo was known to be behind origin by 7 from prior status. The dirty report files listed above were pre-existing. This task did not alter them.

## Copied File Groups

The copy preserved the legacy-compatible case layout under `cases/PORT/PORT_0004`.

Copied groups:

- `README.md`
- `source.sql`
- `rewrite_pos_*.sql`
- `rewrite_neg_*.sql`
- `manifest.yaml`
- `risk_notes.md`
- `witness_design_notes.md`
- `taxonomy_trial*.yaml`
- `data/`
- `provenance/`
- `schema/`
- `validation/`
- `runs/`

Copied file count: 45.

Copied category counts:

- retained plan evidence: 11
- schema/data context: 10
- retained control evidence: 7
- provenance: 5
- hard-negative evidence: 4
- validation scripts: 4
- checker/normalization: 2
- static references: 1
- taxonomy: 1

## Files Intentionally Not Copied

The copy was limited to the legacy case directory `cases/PORT/PORT_0004`.

The following were not copied:

- files outside `cases/PORT/PORT_0004`;
- hidden OS/editor files;
- `__pycache__/`;
- `*.pyc`;
- `.DS_Store`;
- temporary editor swap files;
- untracked scratch files outside the case directory.

No excluded hidden/cache/editor files were found in the legacy `PORT_0004` case tree.

## Runs Handling

The legacy `runs/` tree was copied byte-for-byte into the release case package as part of this pilot attempt.

All copied run artifacts are mapped in `cases/PORT/PORT_0004/evidence/runs_retention.yaml` with:

- original legacy path;
- public release path;
- SHA256 for legacy source and public copy;
- evidence role;
- do-not-delete-original status;
- public-safe status where the file passed hygiene scan.

Two copied Spark plan files did not pass the initial public hygiene scan:

- `cases/PORT/PORT_0004/runs/spark/plans/rewrite_neg_02_spark.txt`
- `cases/PORT/PORT_0004/runs/spark/plans/rewrite_pos_02_spark.txt`

They were sanitized in the release repo only. The current release-repo `runs/spark/plans/*.txt` copies are sanitized public release copies, not raw legacy artifacts.

Canonical sanitized retained-plan evidence was also created:

- `cases/PORT/PORT_0004/evidence/retained_plans/rewrite_neg_02_spark.sanitized.txt`
- `cases/PORT/PORT_0004/evidence/retained_plans/rewrite_pos_02_spark.sanitized.txt`

The raw legacy originals remain mapped, do-not-delete, and unchanged.

## Evidence Mapping

Created:

- `cases/PORT/PORT_0004/MIGRATION_PILOT.md`
- `cases/PORT/PORT_0004/evidence/runs_retention.yaml`

The retention mapping records:

- full case migration scope is `PORT_0004_only`;
- denominator changed: false;
- paper results changed: false;
- Common-core membership changed: false;
- raw legacy evidence changed: false;
- raw legacy files remain do-not-delete and mapped;
- copied release files remain traceable to legacy source paths and SHA256 values.

## Validation Results

SHA256 copy validation: pass.

- 45 copied files checked.
- All copied files match the corresponding legacy source SHA256.

Initial public hygiene scan: fail.

- `runs/spark/plans/rewrite_neg_02_spark.txt` contains a temporary local-path trace.
- `runs/spark/plans/rewrite_pos_02_spark.txt` contains a temporary local-path trace.

Public hygiene scan after fix: pass.

- No forbidden public hygiene patterns remain under `cases/PORT/PORT_0004`.

YAML validation: pass.

- `manifest.yaml` parsed.
- `evidence/runs_retention.yaml` parsed.
- `taxonomy_trial_v0.3.yaml` parsed.

JSON validation: pass.

- 6 JSON files under `provenance/` and `runs/` parsed.

Initial validator v0.2 full-case result: fail.

- Failure reason: public hygiene scan hit in the two copied Spark plan files above.

Validator v0.2 full-case result after fix: pass.

Evidence-pilot regression: pass.

- The six prior evidence-pilot slices passed 6/6.

Python compile: pass.

- `scripts/dev/validate_case_package.py` compiled successfully.

## Non-Changes

- Legacy repo modified: no.
- Legacy case files modified: no.
- Legacy runs modified: no.
- Legacy reports/results/scripts/manifests/checkers/validation/evidence artifacts modified: no.
- Common-core 40 migration started: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- No DB engines were run.
- No evidence was regenerated.

## What Remains Before Expanding

Before proceeding to another full case migration pilot, the release team should review the completed `PORT_0004` pilot and confirm that the sanitized retained-plan mapping is acceptable.

Safe next options:

- proceed to a `PORT_0008` full copy-first pilot to test integration with an already sanitized evidence-mapping case;
- continue reviewing `PORT_0004` retained evidence and validator output before expanding;
- do not weaken the public hygiene scan and do not rewrite legacy artifacts.

Do not start full Common-core 40 migration yet.
