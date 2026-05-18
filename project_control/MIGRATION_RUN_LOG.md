# SQL-RewriteBench Migration Run Log

Purpose:
This file records each Codex execution round in chronological order.
It is an execution ledger, not a decision log and not a status snapshot.

Rules:
- Append one section after every Codex task.
- Record only what was actually done.
- Always state whether the legacy repo was modified.
- Always state whether denominator, paper results, case membership, or raw evidence changed.
- Link to commit hash and important raw URLs when available.
- Do not store secrets, prompts, API keys, or private logs here.

## Entry format

### YYYY-MM-DD · <commit> · <task title>

Mode:
Legacy repo modified:
Release repo modified:
Commit:
Push:
Scope:

Summary:
- ...

Validation:
- ...

Files created:
- ...

Files modified:
- ...

Paper/denominator impact:
- denominator changed:
- paper results changed:
- case membership changed:
- raw legacy evidence changed:

Next safe action:
- ...

## Backfilled entries

### 2026-05-15 · 1b7fab1 · control-layer bootstrap

Mode: release-repo project-control bootstrap; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Commit: `1b7fab1`
Push: pushed to `origin main`
Scope: Created the initial project-control layer for the clean public release migration.

Summary:
- Created `project_control/MIGRATION_MASTER_PLAN.md`.
- Created `project_control/MIGRATION_STATUS.md`.
- Created `project_control/DECISION_LOG.md`.
- Established GitHub `project_control/` as the shared ChatGPT/Codex status source.

Validation:
- Release repo bootstrap committed and pushed.

Files created:
- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/DECISION_LOG.md`

Files modified:
- none

Paper/denominator impact:
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Next safe action:
- Confirm release repo path, branch, remote, and status; then update migration status.

### 2026-05-15 · 7e78dc5 · update migration status after bootstrap

Mode: release-repo project-control status update; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Commit: `7e78dc5`
Push: pushed to `origin main`
Scope: Updated current migration status after bootstrap.

Summary:
- Updated `MIGRATION_STATUS.md` after bootstrap.
- Recorded release repo path, branch, remote, commit, and legacy repo state.
- Marked B001 as resolved.

Validation:
- Release repo status update committed and pushed.

Files created:
- none

Files modified:
- `project_control/MIGRATION_STATUS.md`

Paper/denominator impact:
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Next safe action:
- Proceed with PORT manual-review resolution using read-only legacy inspection.

### 2026-05-15 · 24f82d9 · PORT manual-review resolution

Mode: release-repo audit output generation; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Commit: `24f82d9`
Push: pushed to `origin main`
Scope: Resolved the first PORT manual-review classification pass.

Summary:
- Created `audits/port_manual_review_resolution/` outputs.
- Reviewed `PORT_0004`, `PORT_0008`, `PORT_0012`, `PORT_0013`, `PORT_0022`, `PORT_0024`, and `PORT_0025`.
- Cleared `PORT_0004`.
- Blocked six PORT cases for physical migration pending sanitization.
- Found no prompt/API/token trace.
- Found no Spark warehouse/parquet/CRC/_SUCCESS residue in checkout.

Validation:
- Audit outputs recorded in the release repo.

Files created:
- `audits/port_manual_review_resolution/` audit outputs

Files modified:
- `project_control/MIGRATION_STATUS.md`

Paper/denominator impact:
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Next safe action:
- Define retention and sanitization policy/templates for PORT manual-review cases.

### 2026-05-15 · 32e3d58 · runs retention and PORT sanitization policy/templates

Mode: release-repo policy/template creation; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Commit: `32e3d58`
Push: pushed to `origin main`
Scope: Added runs-retention policy, case contract, templates, and PORT preview mappings.

Summary:
- Created `repository_spec/runs_retention_policy_v1.md`.
- Created `repository_spec/case_package_contract_v1.md`.
- Created `templates/runs_retention_template.yaml`.
- Created `templates/port_sanitized_plan_mapping_template.yaml`.
- Created seven PORT `runs_retention` preview YAML files.
- Added D013 to `DECISION_LOG.md`.

Validation:
- Policy/template and preview artifacts committed and pushed.

Files created:
- `repository_spec/runs_retention_policy_v1.md`
- `repository_spec/case_package_contract_v1.md`
- `templates/runs_retention_template.yaml`
- `templates/port_sanitized_plan_mapping_template.yaml`
- `audits/port_manual_review_resolution/previews/`

Files modified:
- `project_control/DECISION_LOG.md`
- `project_control/MIGRATION_STATUS.md`

Paper/denominator impact:
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Next safe action:
- Trial-sanitize affected PORT Spark plan evidence without modifying legacy artifacts.

### 2026-05-15 · 0afa485 · trial sanitize PORT Spark plan evidence

Mode: release-repo sanitized trial output generation; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Commit: `0afa485`
Push: pushed to `origin main`
Scope: Generated Route B sanitized trial artifacts for blocked PORT Spark plan evidence.

Summary:
- Created `audits/port_manual_review_resolution/sanitized_trial/` outputs.
- Created 12 sanitized Spark plan trial files for six blocked PORT cases.
- Created `PORT_0024` `result_check.sanitized_summary.json`.
- Created `redaction_manifest.csv`, `redaction_validation.csv`, and `original_to_sanitized_mapping.csv`.
- Trial only; not final retained evidence.

Validation:
- Sanitized trial validation passed.

Files created:
- `audits/port_manual_review_resolution/sanitized_trial/`

Files modified:
- `project_control/MIGRATION_STATUS.md`

Paper/denominator impact:
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Next safe action:
- Promote one approved validated trial output set into a formal case-local evidence mapping pilot.

### 2026-05-15 · 637fd2d · PORT_0008 formal sanitized evidence mapping pilot

Mode: release-repo formal evidence-mapping pilot; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Commit: `637fd2d`
Push: pushed to `origin main`
Scope: Promoted already validated Route B sanitized trial outputs for `PORT_0008` into a formal case-local evidence mapping pilot.

Summary:
- Created `cases/PORT/PORT_0008/MIGRATION_PILOT.md`.
- Created `cases/PORT/PORT_0008/evidence/runs_retention.yaml`.
- Created two sanitized retained Spark plan files.
- Created formal pilot audit report and validation CSV.
- Full case migration: no.

Validation:
- YAML validation passed.
- SHA256 match passed.
- Sanitized scan passed.
- Raw legacy Spark plans were not copied into public retained evidence.

Files created:
- `cases/PORT/PORT_0008/MIGRATION_PILOT.md`
- `cases/PORT/PORT_0008/evidence/runs_retention.yaml`
- `cases/PORT/PORT_0008/evidence/retained_plans/`
- `audits/port_manual_review_resolution/formal_pilots/PORT_0008_formal_mapping_pilot.md`
- `audits/port_manual_review_resolution/formal_pilots/PORT_0008_formal_mapping_validation.csv`

Files modified:
- `project_control/MIGRATION_STATUS.md`

Paper/denominator impact:
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Important raw URLs:
- https://raw.githubusercontent.com/TianciGao/Rewritebench_v0/main/cases/PORT/PORT_0008/MIGRATION_PILOT.md
- https://raw.githubusercontent.com/TianciGao/Rewritebench_v0/main/cases/PORT/PORT_0008/evidence/runs_retention.yaml

Next safe action:
- Review the committed `PORT_0008` pilot slice, then either apply the same evidence-mapping-only pattern to another simple PORT case or continue with approved pilot planning.

### 2026-05-15 · e7ca886 · PORT_0012 formal sanitized evidence mapping pilot

Mode: release-repo formal evidence-mapping pilot; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Commit: e7ca886e532cd043b800e9d7316779c57c05af6e
Push: pushed to origin main successfully (406a333..e7ca886)
Scope: Promoted already validated Route B sanitized trial outputs for `PORT_0012` into a formal case-local evidence mapping pilot.

Summary:
- Created `cases/PORT/PORT_0012/MIGRATION_PILOT.md`.
- Created `cases/PORT/PORT_0012/evidence/runs_retention.yaml`.
- Created two sanitized retained Spark plan files from validated trial outputs.
- Created formal pilot audit report and validation CSV.
- Full case migration: no.

Validation:
- YAML validation passed for `cases/PORT/PORT_0012/evidence/runs_retention.yaml`.
- SHA256 match passed for both formal sanitized plan copies against Route B trial artifacts.
- Sanitized output scan passed for the required formal public files.
- Raw legacy Spark plans were not copied into public retained evidence.

Files created:
- `cases/PORT/PORT_0012/MIGRATION_PILOT.md`
- `cases/PORT/PORT_0012/evidence/runs_retention.yaml`
- `cases/PORT/PORT_0012/evidence/retained_plans/rewrite_neg_01.sanitized.txt`
- `cases/PORT/PORT_0012/evidence/retained_plans/rewrite_pos_01.sanitized.txt`
- `audits/port_manual_review_resolution/formal_pilots/PORT_0012_formal_mapping_pilot.md`
- `audits/port_manual_review_resolution/formal_pilots/PORT_0012_formal_mapping_validation.csv`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Paper/denominator impact:
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Important raw URLs:
- https://raw.githubusercontent.com/TianciGao/Rewritebench_v0/main/cases/PORT/PORT_0012/MIGRATION_PILOT.md
- https://raw.githubusercontent.com/TianciGao/Rewritebench_v0/main/cases/PORT/PORT_0012/evidence/runs_retention.yaml

Next safe action:
- Review the committed `PORT_0012` pilot slice, then either apply the same evidence-mapping-only pattern to another simple PORT case or continue with approved pilot planning.

### 2026-05-15 · 6327458 · PORT_0013 formal sanitized evidence mapping pilot

Mode: release-repo formal evidence-mapping pilot; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Commit: 6327458867d3d4c991efae02e59a894a56a979ac
Push: pushed to origin main successfully (e7ca886..6327458)
Scope: Promoted already validated Route B sanitized trial outputs for `PORT_0013` into a formal case-local evidence mapping pilot.

Summary:
- Corrected the prior `PORT_0012` run-log entry with commit `e7ca886e532cd043b800e9d7316779c57c05af6e` and push result `406a333..e7ca886`.
- Created `cases/PORT/PORT_0013/MIGRATION_PILOT.md`.
- Created `cases/PORT/PORT_0013/evidence/runs_retention.yaml`.
- Created two sanitized retained Spark plan files from validated trial outputs.
- Created formal pilot audit report and validation CSV.
- Full case migration: no.

Validation:
- YAML validation passed for `cases/PORT/PORT_0013/evidence/runs_retention.yaml`.
- SHA256 match passed for both formal sanitized plan copies against Route B trial artifacts.
- Sanitized output scan passed for the required formal public files.
- Raw legacy Spark plans were not copied into public retained evidence.

Files created:
- `cases/PORT/PORT_0013/MIGRATION_PILOT.md`
- `cases/PORT/PORT_0013/evidence/runs_retention.yaml`
- `cases/PORT/PORT_0013/evidence/retained_plans/rewrite_neg_01.sanitized.txt`
- `cases/PORT/PORT_0013/evidence/retained_plans/rewrite_pos_01.sanitized.txt`
- `audits/port_manual_review_resolution/formal_pilots/PORT_0013_formal_mapping_pilot.md`
- `audits/port_manual_review_resolution/formal_pilots/PORT_0013_formal_mapping_validation.csv`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Paper/denominator impact:
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Important raw URLs:
- https://raw.githubusercontent.com/TianciGao/Rewritebench_v0/main/cases/PORT/PORT_0013/MIGRATION_PILOT.md
- https://raw.githubusercontent.com/TianciGao/Rewritebench_v0/main/cases/PORT/PORT_0013/evidence/runs_retention.yaml

Next safe action:
- Review the committed `PORT_0013` pilot slice, then either apply the same evidence-mapping-only pattern to another simple PORT case or continue with approved pilot planning.

### 2026-05-15 · 4dce43b · PORT_0022 formal sanitized evidence mapping pilot

Mode: release-repo formal evidence-mapping pilot; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Commit: 4dce43bc6ad778c1b874509e1235ee96a9660586
Push: pushed to origin main successfully (f029d5c..4dce43b)
Scope: Promoted already validated Route B sanitized trial outputs for `PORT_0022` into a formal case-local evidence mapping pilot.

Summary:
- Verified `MIGRATION_STATUS.md` and `MIGRATION_RUN_LOG.md` already recorded the completed `PORT_0013` formal sanitized evidence-mapping pilot.
- Created `cases/PORT/PORT_0022/MIGRATION_PILOT.md`.
- Created `cases/PORT/PORT_0022/evidence/runs_retention.yaml`.
- Created two sanitized retained Spark plan files from validated trial outputs.
- Created formal pilot audit report and validation CSV.
- Full case migration: no.

Validation:
- YAML validation passed for `cases/PORT/PORT_0022/evidence/runs_retention.yaml`.
- SHA256 match passed for both formal sanitized plan copies against Route B trial artifacts.
- Sanitized output scan passed for the required formal public files.
- Raw legacy Spark plans were not copied into public retained evidence.

Files created:
- `cases/PORT/PORT_0022/MIGRATION_PILOT.md`
- `cases/PORT/PORT_0022/evidence/runs_retention.yaml`
- `cases/PORT/PORT_0022/evidence/retained_plans/rewrite_neg_01.sanitized.txt`
- `cases/PORT/PORT_0022/evidence/retained_plans/rewrite_pos_01.sanitized.txt`
- `audits/port_manual_review_resolution/formal_pilots/PORT_0022_formal_mapping_pilot.md`
- `audits/port_manual_review_resolution/formal_pilots/PORT_0022_formal_mapping_validation.csv`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Paper/denominator impact:
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Important raw URLs:
- https://raw.githubusercontent.com/TianciGao/Rewritebench_v0/main/cases/PORT/PORT_0022/MIGRATION_PILOT.md
- https://raw.githubusercontent.com/TianciGao/Rewritebench_v0/main/cases/PORT/PORT_0022/evidence/runs_retention.yaml

Next safe action:
- Review the committed `PORT_0022` pilot slice, then either apply the same evidence-mapping-only pattern to another simple PORT case or continue with approved pilot planning.

### 2026-05-15 · 74e0c6d · PORT_0025 formal sanitized evidence mapping pilot

Mode: release-repo formal evidence-mapping pilot; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Commit: 74e0c6d19667bd62794da2e3ec119afa4d69f241
Push: pushed to origin main successfully (7696ef9..74e0c6d)
Scope: Promoted already validated Route B sanitized trial outputs for `PORT_0025` into a formal case-local evidence mapping pilot.

Summary:
- Created `cases/PORT/PORT_0025/MIGRATION_PILOT.md`.
- Created `cases/PORT/PORT_0025/evidence/runs_retention.yaml`.
- Created two sanitized retained Spark plan files from validated trial outputs.
- Created formal pilot audit report and validation CSV.
- Full case migration: no.

Validation:
- YAML validation passed for `cases/PORT/PORT_0025/evidence/runs_retention.yaml`.
- SHA256 match passed for both formal sanitized plan copies against Route B trial artifacts.
- Sanitized output scan passed for the required formal public files.
- Raw legacy Spark plans were not copied into public retained evidence.

Files created:
- `cases/PORT/PORT_0025/MIGRATION_PILOT.md`
- `cases/PORT/PORT_0025/evidence/runs_retention.yaml`
- `cases/PORT/PORT_0025/evidence/retained_plans/rewrite_neg_01.sanitized.txt`
- `cases/PORT/PORT_0025/evidence/retained_plans/rewrite_pos_01.sanitized.txt`
- `audits/port_manual_review_resolution/formal_pilots/PORT_0025_formal_mapping_pilot.md`
- `audits/port_manual_review_resolution/formal_pilots/PORT_0025_formal_mapping_validation.csv`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Paper/denominator impact:
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Important raw URLs:
- https://raw.githubusercontent.com/TianciGao/Rewritebench_v0/main/cases/PORT/PORT_0025/MIGRATION_PILOT.md
- https://raw.githubusercontent.com/TianciGao/Rewritebench_v0/main/cases/PORT/PORT_0025/evidence/runs_retention.yaml

Next safe action:
- Review the committed `PORT_0025` pilot slice, then either apply the same evidence-mapping-only pattern to another approved simple PORT case or continue with approved pilot planning.

### 2026-05-15 · a55519f · PORT_0024 formal sanitized evidence mapping pilot

Mode: release-repo formal evidence-mapping pilot with result-check summary; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Commit: a55519f5c8146276d1f10869bff215dca845ca57
Push: pushed to origin main successfully (800d99f..a55519f)
Scope: Promoted already validated Route B sanitized trial outputs for `PORT_0024` into a formal case-local evidence mapping pilot, including summarized Spark result-check evidence.

Summary:
- Created `cases/PORT/PORT_0024/MIGRATION_PILOT.md`.
- Created `cases/PORT/PORT_0024/evidence/runs_retention.yaml`.
- Created two sanitized retained Spark plan files from validated trial outputs.
- Created one sanitized Spark result-check summary from validated trial output.
- Created formal pilot audit report and validation CSV.
- Full case migration: no.

Validation:
- YAML validation passed for `cases/PORT/PORT_0024/evidence/runs_retention.yaml`.
- JSON validation passed for `cases/PORT/PORT_0024/evidence/retained_controls/spark_result_check.sanitized_summary.json`.
- SHA256 match passed for both formal sanitized plan copies and the sanitized result-check summary against Route B trial artifacts.
- Sanitized output scan passed for the required formal public files.
- Raw legacy Spark plans and raw stdout/stderr logs were not copied into public retained evidence.

Files created:
- `cases/PORT/PORT_0024/MIGRATION_PILOT.md`
- `cases/PORT/PORT_0024/evidence/runs_retention.yaml`
- `cases/PORT/PORT_0024/evidence/retained_plans/rewrite_neg_01.sanitized.txt`
- `cases/PORT/PORT_0024/evidence/retained_plans/rewrite_pos_01.sanitized.txt`
- `cases/PORT/PORT_0024/evidence/retained_controls/spark_result_check.sanitized_summary.json`
- `audits/port_manual_review_resolution/formal_pilots/PORT_0024_formal_mapping_pilot.md`
- `audits/port_manual_review_resolution/formal_pilots/PORT_0024_formal_mapping_validation.csv`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Paper/denominator impact:
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Important raw URLs:
- https://raw.githubusercontent.com/TianciGao/Rewritebench_v0/main/cases/PORT/PORT_0024/MIGRATION_PILOT.md
- https://raw.githubusercontent.com/TianciGao/Rewritebench_v0/main/cases/PORT/PORT_0024/evidence/runs_retention.yaml

Next safe action:
- Review the committed `PORT_0024` pilot slice, then close the blocked-PORT evidence-mapping pilot series or continue with approved full-case migration planning.

### 2026-05-15 · 5c133ed · blocked-PORT evidence-mapping closeout

Mode: release-repo closeout verification; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Commit: 5c133edc7aef4ef69bbe47bf843d88aa11c7aa98
Push: pushed to origin main successfully (de21d5c..5c133ed)
Scope: Verified and summarized the six blocked PORT formal sanitized evidence-mapping pilot slices.

Summary:
- Verified closed evidence-mapping pilot slices for `PORT_0008`, `PORT_0012`, `PORT_0013`, `PORT_0022`, `PORT_0025`, and `PORT_0024`.
- Created human-readable closeout report.
- Created closeout CSV and machine-readable checks JSON.
- Created next-actions recommendation comparing validator, copy-first pilot, and reports/results retained-evidence map options.
- Full case migration: no.

Validation:
- YAML validation passed for all six case-local `evidence/runs_retention.yaml` files.
- JSON validation passed for `PORT_0024` sanitized Spark result-check summary.
- Sanitized output scan passed for sanitized plan evidence and `PORT_0024` result-check summary.
- Formal validation CSV review passed for public-safe rows and no raw local path or prompt/API/token traces.
- `MIGRATION_RUN_LOG.md` continuity check passed for all six pilot entries.

Files created:
- `audits/port_manual_review_resolution/blocked_port_mapping_closeout.md`
- `audits/port_manual_review_resolution/blocked_port_mapping_closeout.csv`
- `audits/port_manual_review_resolution/blocked_port_mapping_next_actions.md`
- `audits/port_manual_review_resolution/blocked_port_mapping_closeout_checks.json`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Paper/denominator impact:
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Important raw URLs:
- https://raw.githubusercontent.com/TianciGao/Rewritebench_v0/main/audits/port_manual_review_resolution/blocked_port_mapping_closeout.md
- https://raw.githubusercontent.com/TianciGao/Rewritebench_v0/main/audits/port_manual_review_resolution/blocked_port_mapping_closeout.csv
- https://raw.githubusercontent.com/TianciGao/Rewritebench_v0/main/audits/port_manual_review_resolution/blocked_port_mapping_next_actions.md

Next safe action:
- Choose between full copy-first case migration pilot, preferably `PORT_0004` or `PORT_0008`; case package validator design; or reports/results retained evidence map. Do not start full Common-core 40 migration yet.

### 2026-05-15 · 191a0c8 · static case-package validator v0.1 evidence-pilot

Mode: release-repo static validator implementation and evidence-pilot verification; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Commit: 191a0c88491a0916a8f67ee9494bf2a480ca187c
Push: pushed to origin main successfully (495f268..191a0c8)
Scope: Designed and implemented the first static release-repo validator for completed PORT evidence-pilot slices.

Summary:
- Created `scripts/dev/validate_case_package.py` with validator version `v0.1`.
- Added initial mode `evidence-pilot`.
- Added static checks for required evidence-pilot files, `runs_retention.yaml`, public-safe sanitized evidence, formal validation CSVs, and `PORT_0024` result-check summary handling.
- Created validator specification and audit report.
- Ran the validator across `PORT_0008`, `PORT_0012`, `PORT_0013`, `PORT_0022`, `PORT_0025`, and `PORT_0024`.
- Full case migration: no.

Validation:
- `python -m py_compile scripts/dev/validate_case_package.py` passed.
- `python scripts/dev/validate_case_package.py --mode evidence-pilot ...` passed for all six cases.
- YAML checks passed for all six case-local `evidence/runs_retention.yaml` files.
- Sanitized public evidence scans passed.
- `PORT_0024` sanitized result-check summary JSON and log-reference checks passed.
- Formal validation CSV checks passed.

Files created:
- `scripts/dev/validate_case_package.py`
- `repository_spec/static_case_package_validator_v0_1.md`
- `audits/port_manual_review_resolution/static_case_package_validator_v0_1_report.md`
- `audits/port_manual_review_resolution/static_case_package_validator_v0_1_results.json`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Paper/denominator impact:
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Important raw URLs:
- https://raw.githubusercontent.com/TianciGao/Rewritebench_v0/main/scripts/dev/validate_case_package.py
- https://raw.githubusercontent.com/TianciGao/Rewritebench_v0/main/repository_spec/static_case_package_validator_v0_1.md
- https://raw.githubusercontent.com/TianciGao/Rewritebench_v0/main/audits/port_manual_review_resolution/static_case_package_validator_v0_1_report.md

Next safe action:
- Use validator v0.1 as the evidence-pilot gate, then design a copy-first full-case validator mode before starting a full case migration pilot, preferably `PORT_0004` or `PORT_0008`.

### 2026-05-15 · ea119bc · static case-package validator v0.2 full-case mode

Mode: release-repo static validator enhancement; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Commit: ea119bc924abc598bed86831128eb59dafe6ccfd
Push: pushed to origin main successfully (82c7d40..ea119bc)
Scope: Extended `scripts/dev/validate_case_package.py` with validator `v0.2` and new `full-case` mode for future copy-first full case migration pilots.

Summary:
- Preserved existing `evidence-pilot` mode.
- Added `full-case` mode for future complete migrated case packages.
- Added CSV output with `--out`.
- Added optional JSON output with `--json-out`, while preserving `--json-output`.
- Added advisory expected-fail behavior through `--allow-failures` and `--advisory`.
- Added v0.2 repository spec and validator trial report.
- Full case migration: no.

Validation:
- `python scripts/dev/validate_case_package.py --mode evidence-pilot ... --out audits/validator_trials/evidence_pilot_regression_results.csv` passed 6/6.
- `python scripts/dev/validate_case_package.py --mode full-case --allow-failures ... --out audits/validator_trials/full_case_mode_advisory_results.csv` exited successfully in advisory mode and correctly reported all six current evidence-only pilot slices as not full migrated cases.
- Advisory full-case output identified missing manifest, source SQL, positive rewrite, hard-negative declaration, schema, checker, validation, provenance, and taxonomy components.
- `python -m py_compile scripts/dev/validate_case_package.py` passed.

Files created:
- `repository_spec/static_case_package_validator_v0_2.md`
- `audits/validator_trials/evidence_pilot_regression_results.csv`
- `audits/validator_trials/full_case_mode_advisory_results.csv`
- `audits/validator_trials/static_case_package_validator_v0_2_report.md`

Files modified:
- `scripts/dev/validate_case_package.py`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Paper/denominator impact:
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Important raw URLs:
- https://raw.githubusercontent.com/TianciGao/Rewritebench_v0/main/scripts/dev/validate_case_package.py
- https://raw.githubusercontent.com/TianciGao/Rewritebench_v0/main/repository_spec/static_case_package_validator_v0_2.md
- https://raw.githubusercontent.com/TianciGao/Rewritebench_v0/main/audits/validator_trials/static_case_package_validator_v0_2_report.md

Next safe action:
- Choose first copy-first full case migration pilot, preferably `PORT_0004` for lower risk or `PORT_0008` to test sanitized evidence integration, and run validator v0.2 in advisory mode while assembling the candidate package.

### 2026-05-15 · 988b8fe · PORT_0004 copy-first full case migration pilot

Mode: release-repo full case migration pilot; legacy read-only source copy
Legacy repo modified: no
Release repo modified: yes
Commit: 988b8feb275cc8b92c5e730af72c95268d31a852
Push: pushed to origin main successfully (99b68c2..988b8fe)
Scope: Attempted the first copy-first full case migration pilot for `PORT_0004`.

Summary:
- Copied the legacy `PORT_0004` case package into the release repo using the legacy-compatible layout.
- Created `cases/PORT/PORT_0004/MIGRATION_PILOT.md`.
- Created `cases/PORT/PORT_0004/evidence/runs_retention.yaml`.
- Created full-case migration pilot audit report, file inventory, and validation CSV.
- Ran validator v0.2 full-case mode.
- Pilot completion status: failed validation.

Validation:
- SHA256 copy validation passed for 45 copied files.
- Public hygiene scan failed for two copied Spark plan files containing temporary local-path traces.
- YAML validation passed for manifest, runs-retention, and taxonomy YAML.
- JSON validation passed for 6 JSON files.
- `python scripts/dev/validate_case_package.py --mode full-case --case cases/PORT/PORT_0004 --out audits/full_case_migration_pilots/PORT_0004_validator_full_case_result.csv` failed due public hygiene scan hits.
- Evidence-pilot regression passed for the six prior evidence-pilot slices.
- `python -m py_compile scripts/dev/validate_case_package.py` passed.

Files created:
- `cases/PORT/PORT_0004/`
- `cases/PORT/PORT_0004/MIGRATION_PILOT.md`
- `cases/PORT/PORT_0004/evidence/runs_retention.yaml`
- `audits/full_case_migration_pilots/PORT_0004_full_case_migration_pilot.md`
- `audits/full_case_migration_pilots/PORT_0004_full_case_file_inventory.csv`
- `audits/full_case_migration_pilots/PORT_0004_full_case_validation.csv`
- `audits/full_case_migration_pilots/PORT_0004_validator_full_case_result.csv`
- `audits/full_case_migration_pilots/PORT_0004_evidence_pilot_regression_result.csv`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Paper/denominator impact:
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Important raw URLs:
- https://raw.githubusercontent.com/TianciGao/Rewritebench_v0/main/cases/PORT/PORT_0004/MIGRATION_PILOT.md
- https://raw.githubusercontent.com/TianciGao/Rewritebench_v0/main/cases/PORT/PORT_0004/evidence/runs_retention.yaml
- https://raw.githubusercontent.com/TianciGao/Rewritebench_v0/main/audits/full_case_migration_pilots/PORT_0004_full_case_migration_pilot.md

Next safe action:
- Fix the `PORT_0004` release-repo mapping/hygiene issue only, likely by approving sanitized public copies or archive-only handling for the two affected Spark plan files, then rerun validator v0.2 full-case mode. Do not touch legacy.

### 2026-05-16 · a351e62 · PORT_0004 full case pilot hygiene fix

Mode: release-repo hygiene fix and full-case validator rerun; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Commit: a351e62206c366df858449a18487fefd8eb3a863
Push: pushed to origin main successfully (9208971..a351e62)
Scope: Fixed the release-repo public hygiene issue in the `PORT_0004` copy-first full case migration pilot by sanitizing two copied Spark plan files and adding canonical retained-plan evidence.

Summary:
- Replaced two release-repo Spark plan copies in place with sanitized public-safe content.
- Created canonical sanitized retained-plan copies under `cases/PORT/PORT_0004/evidence/retained_plans/`.
- Updated `cases/PORT/PORT_0004/evidence/runs_retention.yaml` to map original legacy artifacts, sanitized release run-plan copies, and canonical sanitized retained evidence.
- Updated full-case pilot audit outputs and validation summaries.
- Added a hygiene-fix report and validation CSV.
- Added `PORT_0004` formal mapping validation rows for the sanitized retained-plan evidence.
- Pilot completion status: `PORT_0004` pilot-complete after validator v0.2 pass.

Validation:
- Public hygiene scan passed for `cases/PORT/PORT_0004`.
- YAML validation passed for manifest, runs-retention, and taxonomy YAML.
- JSON validation passed for JSON files under `provenance/` and `runs/`.
- `python scripts/dev/validate_case_package.py --mode full-case --case cases/PORT/PORT_0004 --out audits/full_case_migration_pilots/PORT_0004_validator_full_case_result.csv` passed.
- Evidence-pilot regression passed 6/6 for the six prior PORT evidence-pilot slices.
- `python -m py_compile scripts/dev/validate_case_package.py` passed.

Files created:
- `cases/PORT/PORT_0004/evidence/retained_plans/rewrite_neg_02_spark.sanitized.txt`
- `cases/PORT/PORT_0004/evidence/retained_plans/rewrite_pos_02_spark.sanitized.txt`
- `audits/full_case_migration_pilots/PORT_0004_hygiene_fix_report.md`
- `audits/full_case_migration_pilots/PORT_0004_hygiene_fix_validation.csv`
- `audits/port_manual_review_resolution/formal_pilots/PORT_0004_formal_mapping_validation.csv`

Files modified:
- `cases/PORT/PORT_0004/MIGRATION_PILOT.md`
- `cases/PORT/PORT_0004/evidence/runs_retention.yaml`
- `cases/PORT/PORT_0004/runs/spark/plans/rewrite_neg_02_spark.txt`
- `cases/PORT/PORT_0004/runs/spark/plans/rewrite_pos_02_spark.txt`
- `audits/full_case_migration_pilots/PORT_0004_full_case_migration_pilot.md`
- `audits/full_case_migration_pilots/PORT_0004_full_case_file_inventory.csv`
- `audits/full_case_migration_pilots/PORT_0004_full_case_validation.csv`
- `audits/full_case_migration_pilots/PORT_0004_validator_full_case_result.csv`
- `audits/full_case_migration_pilots/PORT_0004_evidence_pilot_regression_result.csv`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Paper/denominator impact:
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Next safe action:
- Review the completed `PORT_0004` pilot, then decide whether to run a `PORT_0008` full copy-first pilot to test sanitized evidence integration. Do not start full Common-core 40 migration.

### 2026-05-16 · 0e4129e · canonical case package layout lock

Mode: release-repo specification/control update; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Commit: 0e4129ed795f24676b455478f2bf82c121de0505
Push: pushed to origin main successfully (40d5fd1..0e4129e)
Scope: Locked the canonical public-release case package layout as target policy for future migrations.

Summary:
- Created `repository_spec/canonical_case_package_layout_v1.md`.
- Created `templates/canonical_case_package_tree_v1.txt`.
- Updated `repository_spec/case_package_contract_v1.md` to reference the canonical layout.
- Added D015, the canonical case package layout policy, to `project_control/DECISION_LOG.md`.
- Updated `project_control/MIGRATION_STATUS.md`.
- No case files were moved, copied, deleted, sanitized, or regenerated.

Validation:
- `python -m py_compile scripts/dev/validate_case_package.py` passed.
- `git diff --check` passed.
- Release repo status checked before commit.

Files created:
- `repository_spec/canonical_case_package_layout_v1.md`
- `templates/canonical_case_package_tree_v1.txt`

Files modified:
- `repository_spec/case_package_contract_v1.md`
- `project_control/DECISION_LOG.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Paper/denominator impact:
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Next safe action:
- Review the completed `PORT_0004` pilot, then decide whether `PORT_0008` should be the canonical-layout full copy-first pilot. Do not start full Common-core 40 migration.

### 2026-05-16 · 29886bb · PORT_0008 canonical-layout migration dry-run plan

Mode: release-repo planning/audit output; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Commit: 29886bb498b794ea184e827e8a1ca802c888137d
Push: pushed to origin main successfully (e5594c4..29886bb)
Scope: Prepared a planning-only canonical-layout full case migration blueprint for `PORT_0008`.

Summary:
- Created the `audits/canonical_layout_planning/PORT_0008/` planning directory.
- Documented why `PORT_0008` should be the next canonical-layout pilot candidate after `PORT_0004`.
- Produced source-to-target mapping, proposed canonical tree, manifest preview, runs-retention preview, validator expectation matrix, public hygiene precheck, risk register, abort conditions, future actual migration prompt, and planning summary JSON.
- Ran optional validator checks on the current `PORT_0008` evidence-only release slice.
- Actual case migration performed: no.
- No files under `cases/PORT/PORT_0008/` were modified.

Validation:
- `PORT_0008` evidence-pilot validator run passed.
- `PORT_0008` full-case advisory run failed as expected because the current release slice is evidence-only.
- `python -m py_compile scripts/dev/validate_case_package.py` passed.
- Planning summary JSON parsed.
- Manifest preview and runs-retention preview YAML parsed.
- `git diff --check` passed.

Files created:
- `audits/canonical_layout_planning/PORT_0008/PORT_0008_canonical_layout_plan.md`
- `audits/canonical_layout_planning/PORT_0008/PORT_0008_canonical_file_mapping.csv`
- `audits/canonical_layout_planning/PORT_0008/PORT_0008_proposed_canonical_tree.txt`
- `audits/canonical_layout_planning/PORT_0008/PORT_0008_manifest_preview.yaml`
- `audits/canonical_layout_planning/PORT_0008/PORT_0008_runs_retention_after_canonical_preview.yaml`
- `audits/canonical_layout_planning/PORT_0008/PORT_0008_validator_expectation_matrix.csv`
- `audits/canonical_layout_planning/PORT_0008/PORT_0008_public_hygiene_precheck.csv`
- `audits/canonical_layout_planning/PORT_0008/PORT_0008_canonical_migration_risk_register.md`
- `audits/canonical_layout_planning/PORT_0008/PORT_0008_abort_conditions.md`
- `audits/canonical_layout_planning/PORT_0008/PORT_0008_future_actual_migration_prompt.md`
- `audits/canonical_layout_planning/PORT_0008/PORT_0008_planning_summary.json`
- `audits/canonical_layout_planning/PORT_0008/PORT_0008_current_evidence_pilot_validator_result.csv`
- `audits/canonical_layout_planning/PORT_0008/PORT_0008_current_full_case_advisory_result.csv`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Paper/denominator impact:
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Next safe action:
- Human review of the `PORT_0008` canonical-layout plan, then decide whether to execute the future actual migration prompt. Do not start Common-core 40 migration.

### 2026-05-16 · 66a1fb9 · PORT_0008 canonical-layout full case migration pilot

Mode: release-repo canonical full case migration pilot; legacy read-only source copy
Legacy repo modified: no
Release repo modified: yes
Commit: 66a1fb9acb2696d1e5d1c08ece15fd14263c8830
Push: pushed to origin main successfully (ed75446..66a1fb9)
Scope: Executed the approved one-case canonical-layout full case migration pilot for `PORT_0008`.

Summary:
- Created canonical `PORT_0008` package structure under `cases/PORT/PORT_0008/`.
- Generated canonical manifest, README, checker metadata, schema/data profiles, stable metadata, package summary, migration notes, and full retention mapping.
- Copied public-safe SQL, schema, witness load, legacy validation assets, notes, and retained JSON/TSV evidence from the legacy case.
- Reused existing formal sanitized Spark plan evidence; raw Spark plan text files were not copied into public retained evidence.
- Raw `runs/` was not copied wholesale.
- Actual case migration performed: yes, for `PORT_0008` only.

Validation:
- SHA256 copy validation passed for 28 copied legacy files.
- Sanitized Spark plan SHA validation passed for 2 reused files.
- Public hygiene scan passed.
- YAML validation passed for 14 files.
- JSON validation passed for 7 files.
- Validator v0.2 full-case mode passed for `PORT_0008`.
- Evidence-pilot regression passed 6/6.
- `python -m py_compile scripts/dev/validate_case_package.py` passed.

Files created:
- `cases/PORT/PORT_0008/README.md`
- `cases/PORT/PORT_0008/manifest.yaml`
- `cases/PORT/PORT_0008/sql/`
- `cases/PORT/PORT_0008/schema/`
- `cases/PORT/PORT_0008/data/`
- `cases/PORT/PORT_0008/checker/`
- `cases/PORT/PORT_0008/validation/`
- `cases/PORT/PORT_0008/evidence/retained_controls/`
- `cases/PORT/PORT_0008/evidence/retained_plans/postgres/`
- `cases/PORT/PORT_0008/evidence/retained_plans/mysql/`
- `cases/PORT/PORT_0008/evidence/hard_negative/`
- `cases/PORT/PORT_0008/evidence/package_validation_summary.json`
- `cases/PORT/PORT_0008/metadata/`
- `cases/PORT/PORT_0008/notes/`
- `audits/full_case_migration_pilots/PORT_0008_canonical_full_case_migration_pilot.md`
- `audits/full_case_migration_pilots/PORT_0008_canonical_full_case_file_inventory.csv`
- `audits/full_case_migration_pilots/PORT_0008_canonical_full_case_validation.csv`
- `audits/full_case_migration_pilots/PORT_0008_validator_full_case_result.csv`
- `audits/full_case_migration_pilots/PORT_0008_evidence_pilot_regression_result.csv`

Files modified:
- `cases/PORT/PORT_0008/evidence/runs_retention.yaml`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Paper/denominator impact:
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Next safe action:
- Review the completed `PORT_0008` canonical-layout pilot, then decide whether to extend validator canonical-layout conformance checks or plan the next single-case pilot. Do not start Common-core 40 migration.

### 2026-05-16 · 5c797e1 · static case-package validator v0.3 canonical-layout mode

Mode: release-repo static validator enhancement; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Commit: 5c797e1d0b4b423a4347864751176c0190a6c11e
Push: pushed to origin main successfully (f86fc3d..5c797e1)
Scope: Added static canonical-layout conformance validation after the completed `PORT_0008` canonical-layout pilot.

Summary:
- Upgraded `scripts/dev/validate_case_package.py` to validator v0.3.
- Added `--mode canonical-case`.
- Preserved `evidence-pilot` and `full-case` modes.
- Added canonical checks for root files, `sql/`, `schema/`, `data/`, `checker/`, `validation/`, `evidence/`, `metadata/`, `notes/`, `runs/` policy, manifest semantics, retention semantics, public hygiene, and claim boundaries.
- Documented v0.3 in `repository_spec/static_case_package_validator_v0_3.md`.
- Generated v0.3 validator trial outputs and report.
- No case migration was performed.

Validation:
- Evidence-pilot regression passed 6/6.
- Full-case regression passed 2/2 for `PORT_0004` and `PORT_0008`.
- Canonical-case strict validation passed for `PORT_0008`.
- Canonical-case advisory validation failed as expected for `PORT_0004`.
- `python -m py_compile scripts/dev/validate_case_package.py` passed.

Files created:
- `repository_spec/static_case_package_validator_v0_3.md`
- `audits/validator_trials/static_case_package_validator_v0_3_report.md`
- `audits/validator_trials/v0_3_evidence_pilot_regression_results.csv`
- `audits/validator_trials/v0_3_full_case_regression_results.csv`
- `audits/validator_trials/v0_3_canonical_case_PORT_0008_results.csv`
- `audits/validator_trials/v0_3_canonical_case_PORT_0004_advisory_results.csv`

Files modified:
- `scripts/dev/validate_case_package.py`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Paper/denominator impact:
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Next safe action:
- Review validator v0.3 results; then decide the next single-case pilot across another pool, or continue case-universe/report/script audits. Do not start Common-core 40 migration.

### 2026-05-16 · d795660 · CONS_0005 canonical-layout migration dry-run plan

Mode: release-repo planning/audit output; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Commit: d795660705ae4974d3244fa4ecb10ce8786be355
Push: pushed to origin main successfully (5b9187f..d795660)
Scope: Created a planning-only canonical-layout migration blueprint for `CONS_0005` without creating or modifying the release case package.

Summary:
- Inspected legacy `cases/CONS/CONS_0005` read-only.
- Created a canonical-layout migration plan for a checker-heavy / hard-negative-heavy CONS case.
- Created source-to-target mapping, proposed canonical tree, manifest preview, runs-retention preview, checker expected-rejections preview, validator expectation matrix, public hygiene precheck, risk register, abort conditions, future actual migration prompt, and planning summary JSON.
- No actual case migration was performed.
- No `cases/CONS/CONS_0005/` release package files were created or modified.

Validation:
- `python -m py_compile scripts/dev/validate_case_package.py` passed.
- Planning summary JSON parsed.
- Preview YAML files parsed when PyYAML was available.
- `git diff --check` passed.

Files created:
- `audits/canonical_layout_planning/CONS_0005/CONS_0005_canonical_layout_plan.md`
- `audits/canonical_layout_planning/CONS_0005/CONS_0005_canonical_file_mapping.csv`
- `audits/canonical_layout_planning/CONS_0005/CONS_0005_proposed_canonical_tree.txt`
- `audits/canonical_layout_planning/CONS_0005/CONS_0005_manifest_preview.yaml`
- `audits/canonical_layout_planning/CONS_0005/CONS_0005_runs_retention_after_canonical_preview.yaml`
- `audits/canonical_layout_planning/CONS_0005/CONS_0005_checker_expected_rejections_preview.yaml`
- `audits/canonical_layout_planning/CONS_0005/CONS_0005_validator_expectation_matrix.csv`
- `audits/canonical_layout_planning/CONS_0005/CONS_0005_public_hygiene_precheck.csv`
- `audits/canonical_layout_planning/CONS_0005/CONS_0005_canonical_migration_risk_register.md`
- `audits/canonical_layout_planning/CONS_0005/CONS_0005_abort_conditions.md`
- `audits/canonical_layout_planning/CONS_0005/CONS_0005_future_actual_migration_prompt.md`
- `audits/canonical_layout_planning/CONS_0005/CONS_0005_planning_summary.json`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Paper/denominator impact:
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no
- actual case migration performed: no

Next safe action:
- Human review of the `CONS_0005` canonical-layout plan, then decide whether to execute the future actual migration prompt. Do not start Common-core 40 migration.

### 2026-05-16 · f779cb2 · CONS_0005 canonical-layout full case migration pilot

Mode: release-repo canonical full case migration pilot; legacy read-only source copy
Legacy repo modified: no
Release repo modified: yes
Commit: f779cb25c64c5c97f07848c8c88929697bbfb30e
Push: pushed to origin main successfully (dbddf60..f779cb2)
Scope: Executed the approved one-case canonical-layout full case migration pilot for `CONS_0005`.

Summary:
- Created canonical `CONS_0005` package structure under `cases/CONS/CONS_0005/`.
- Generated canonical manifest, README, checker YAML, expected-rejection metadata, schema/data profiles, stable metadata, package summary, migration notes, and full retention mapping.
- Copied public-safe SQL, schema, witness load, notes, retained JSON/TSV evidence, and PostgreSQL/MySQL plan evidence from the legacy case.
- Created sanitized public Spark plan evidence from legacy Spark plan text files; raw Spark plan text files were not copied into public retained evidence.
- Recorded the maintainer-approved hard-negative expected rejection reason.
- Raw `runs/` was not copied wholesale.
- Actual case migration performed: yes, for `CONS_0005` only.

Validation:
- SHA256 copy validation passed for 33 copied legacy files.
- Public hygiene scan passed.
- YAML validation passed for 14 files.
- JSON validation passed for 13 files.
- Validator v0.3 full-case mode passed for `CONS_0005`.
- Validator v0.3 canonical-case mode passed for `CONS_0005`.
- Evidence-pilot regression passed 6/6.
- Full-case regression passed 2/2 for `PORT_0004` and `PORT_0008`.
- `python -m py_compile scripts/dev/validate_case_package.py` passed.

Files created:
- `cases/CONS/CONS_0005/`
- `audits/full_case_migration_pilots/CONS_0005_canonical_full_case_migration_pilot.md`
- `audits/full_case_migration_pilots/CONS_0005_canonical_full_case_file_inventory.csv`
- `audits/full_case_migration_pilots/CONS_0005_canonical_full_case_validation.csv`
- `audits/full_case_migration_pilots/CONS_0005_validator_full_case_result.csv`
- `audits/full_case_migration_pilots/CONS_0005_validator_canonical_case_result.csv`
- `audits/full_case_migration_pilots/CONS_0005_evidence_pilot_regression_result.csv`
- `audits/full_case_migration_pilots/CONS_0005_full_case_regression_result.csv`

Files modified:
- `scripts/dev/validate_case_package.py`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Paper/denominator impact:
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Next safe action:
- Review the completed `CONS_0005` canonical-layout pilot, then decide the next single-case pilot or continue case-universe/report/script audits. Do not start Common-core 40 migration.

### 2026-05-16 · 0c91832 · PERF_0006 canonical-layout migration dry-run plan

Mode: release-repo planning/audit output; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Commit: 0c9183280b445c4ae1af37e9a5a9ab36b3c647b4
Push: pushed to origin main successfully (ba6f51d..0c91832)
Scope: Created a planning-only canonical-layout full case migration blueprint for `PERF_0006` without creating or modifying the release case package.

Summary:
- Inspected legacy `cases/PERF/PERF_0006` read-only.
- Created a canonical-layout migration plan for a performance-sensitive analytical PERF case.
- Created source-to-target mapping, proposed canonical tree, manifest preview, runs-retention preview, performance evidence boundary preview, validator expectation matrix, public hygiene precheck, risk register, abort conditions, future actual migration prompt, and planning summary JSON.
- No actual case migration was performed.
- No `cases/PERF/PERF_0006/` release package files were created or modified.

Validation:
- `python -m py_compile scripts/dev/validate_case_package.py` passed.
- Planning summary JSON parsed.
- Manifest preview and runs-retention preview YAML parsed when PyYAML was available.
- `git diff --check` passed.

Files created:
- `audits/canonical_layout_planning/PERF_0006/PERF_0006_canonical_layout_plan.md`
- `audits/canonical_layout_planning/PERF_0006/PERF_0006_canonical_file_mapping.csv`
- `audits/canonical_layout_planning/PERF_0006/PERF_0006_proposed_canonical_tree.txt`
- `audits/canonical_layout_planning/PERF_0006/PERF_0006_manifest_preview.yaml`
- `audits/canonical_layout_planning/PERF_0006/PERF_0006_runs_retention_after_canonical_preview.yaml`
- `audits/canonical_layout_planning/PERF_0006/PERF_0006_performance_evidence_boundary_preview.md`
- `audits/canonical_layout_planning/PERF_0006/PERF_0006_validator_expectation_matrix.csv`
- `audits/canonical_layout_planning/PERF_0006/PERF_0006_public_hygiene_precheck.csv`
- `audits/canonical_layout_planning/PERF_0006/PERF_0006_canonical_migration_risk_register.md`
- `audits/canonical_layout_planning/PERF_0006/PERF_0006_abort_conditions.md`
- `audits/canonical_layout_planning/PERF_0006/PERF_0006_future_actual_migration_prompt.md`
- `audits/canonical_layout_planning/PERF_0006/PERF_0006_planning_summary.json`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Paper/denominator impact:
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no
- actual case migration performed: no

Next safe action:
- Human review of the `PERF_0006` canonical-layout plan, then decide whether to execute the future actual migration prompt. Do not start Common-core 40 migration.

### 2026-05-16 · e332fc4 · PERF_0006 canonical-layout full case migration pilot

Mode: release-repo canonical full case migration pilot; legacy read-only source copy
Legacy repo modified: no
Release repo modified: yes
Commit: e332fc479add0fb8f7908ebc965a9e0fef006f0d
Push: pushed to origin main successfully (343acb5..e332fc4)
Scope: Executed the approved one-case canonical-layout full case migration pilot for `PERF_0006`.

Summary:
- Created canonical `PERF_0006` package structure under `cases/PERF/PERF_0006/`.
- Generated canonical manifest, README, checker YAML, expected-rejection metadata, schema/data profiles, stable metadata, package summary, migration notes, and full retention mapping.
- Copied public-safe SQL, schema, witness load, retained JSON/TSV evidence, and PostgreSQL/MySQL plan evidence from the legacy case.
- Created sanitized public Spark plan evidence from legacy Spark plan text files; raw Spark plan text files were not copied into public retained evidence.
- Preserved the correctness-gated performance boundary with `speedup_claim_created: false` and `timing_evidence_created: false`.
- Raw `runs/` was not copied wholesale.
- Actual case migration performed: yes, for `PERF_0006` only.

Validation:
- SHA256 copy validation passed for copied legacy files.
- Public hygiene scan passed.
- YAML validation passed for 14 files.
- JSON validation passed for 7 files.
- Validator v0.3 full-case mode passed for `PERF_0006`.
- Validator v0.3 canonical-case mode passed for `PERF_0006`.
- Evidence-pilot regression passed 6/6.
- Full-case regression passed 3/3 for `PORT_0004`, `PORT_0008`, and `CONS_0005`.
- `python -m py_compile scripts/dev/validate_case_package.py` passed.

Files created:
- `cases/PERF/PERF_0006/`
- `audits/full_case_migration_pilots/PERF_0006_canonical_full_case_migration_pilot.md`
- `audits/full_case_migration_pilots/PERF_0006_canonical_full_case_file_inventory.csv`
- `audits/full_case_migration_pilots/PERF_0006_canonical_full_case_validation.csv`
- `audits/full_case_migration_pilots/PERF_0006_validator_full_case_result.csv`
- `audits/full_case_migration_pilots/PERF_0006_validator_canonical_case_result.csv`
- `audits/full_case_migration_pilots/PERF_0006_evidence_pilot_regression_result.csv`
- `audits/full_case_migration_pilots/PERF_0006_full_case_regression_result.csv`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Paper/denominator impact:
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no
- speedup/timing claim created: no

Next safe action:
- Review the completed `PERF_0006` canonical-layout pilot, then decide whether to run another bounded single-case pilot or continue case-universe/report/script audits. Do not start Common-core 40 migration.

### 2026-05-16 · 8aedf22 · LONGTAIL_0011 canonical-layout migration dry-run plan

Mode: release-repo planning/audit output; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Commit: 8aedf22cf5d1829eebfb575186e52f90a7e05ff1
Push: pushed to origin main successfully (acf3986..8aedf22)
Scope: Created a planning-only canonical-layout full case migration blueprint for `LONGTAIL_0011` without creating or modifying the release case package.

Summary:
- Inspected legacy `cases/LONGTAIL/LONGTAIL_0011` read-only.
- Created a canonical-layout migration plan for a realistic / structurally complex / long-tail SQL case.
- Created source-to-target mapping, proposed canonical tree, manifest preview, runs-retention preview, long-tail structure boundary preview, validator expectation matrix, public hygiene precheck, risk register, abort conditions, future actual migration prompt, and planning summary JSON.
- No actual case migration was performed.
- No `cases/LONGTAIL/LONGTAIL_0011/` release package files were created or modified.

Validation:
- `python -m py_compile scripts/dev/validate_case_package.py` passed.
- Planning summary JSON parsed.
- Manifest preview and runs-retention preview YAML parsed when PyYAML was available.
- `git diff --check` passed.

Files created:
- `audits/canonical_layout_planning/LONGTAIL_0011/LONGTAIL_0011_canonical_layout_plan.md`
- `audits/canonical_layout_planning/LONGTAIL_0011/LONGTAIL_0011_canonical_file_mapping.csv`
- `audits/canonical_layout_planning/LONGTAIL_0011/LONGTAIL_0011_proposed_canonical_tree.txt`
- `audits/canonical_layout_planning/LONGTAIL_0011/LONGTAIL_0011_manifest_preview.yaml`
- `audits/canonical_layout_planning/LONGTAIL_0011/LONGTAIL_0011_runs_retention_after_canonical_preview.yaml`
- `audits/canonical_layout_planning/LONGTAIL_0011/LONGTAIL_0011_longtail_structure_boundary_preview.md`
- `audits/canonical_layout_planning/LONGTAIL_0011/LONGTAIL_0011_validator_expectation_matrix.csv`
- `audits/canonical_layout_planning/LONGTAIL_0011/LONGTAIL_0011_public_hygiene_precheck.csv`
- `audits/canonical_layout_planning/LONGTAIL_0011/LONGTAIL_0011_canonical_migration_risk_register.md`
- `audits/canonical_layout_planning/LONGTAIL_0011/LONGTAIL_0011_abort_conditions.md`
- `audits/canonical_layout_planning/LONGTAIL_0011/LONGTAIL_0011_future_actual_migration_prompt.md`
- `audits/canonical_layout_planning/LONGTAIL_0011/LONGTAIL_0011_planning_summary.json`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Paper/denominator impact:
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no
- actual case migration performed: no

Next safe action:
- Human review of the `LONGTAIL_0011` canonical-layout plan, then decide whether to execute the future actual migration prompt. Do not start Common-core 40 migration.

### 2026-05-16 · 53a969f · LONGTAIL_0011 canonical-layout full case migration pilot

Mode: release-repo canonical full case migration pilot; legacy read-only source copy
Legacy repo modified: no
Release repo modified: yes
Commit: 53a969f6c26425f0da17acbc377484bbf9743dff
Push: pushed to origin main successfully (438d421..53a969f)
Scope: Executed the approved one-case canonical-layout full case migration pilot for `LONGTAIL_0011`.

Summary:
- Created canonical `LONGTAIL_0011` package structure under `cases/LONGTAIL/LONGTAIL_0011/`.
- Generated canonical README, manifest, checker YAML, expected-rejection metadata, schema/data profiles, stable metadata, package summary, migration notes, and full retention mapping.
- Copied public-safe SQL, schema, witness load, notes, retained JSON/TSV evidence, and PostgreSQL/MySQL plan evidence from the legacy case.
- Adapted validation scripts to canonical paths and removed WSL-local wording while preserving their retained legacy validation-asset role.
- Created sanitized public Spark plan evidence from legacy Spark plan text files; raw Spark plan text files were not copied into public retained evidence.
- Recorded the maintainer-approved hard-negative expected rejection reason for DENSE_RANK to ROW_NUMBER tie-sensitive ranking semantics.
- Preserved the long-tail structural boundary with `workload_frequency_claim_created: false`.
- Raw `runs/` was not copied wholesale.
- Actual case migration performed: yes, for `LONGTAIL_0011` only.

Validation:
- SHA256 copy validation passed for 33 byte-for-byte copied legacy files; six validation scripts were intentionally adapted and one source SQL file was whitespace-normalized in the release copy.
- Public hygiene scan passed.
- YAML validation passed for 14 files.
- JSON validation passed for 14 files.
- Validator v0.3 full-case mode passed for `LONGTAIL_0011`.
- Validator v0.3 canonical-case mode passed for `LONGTAIL_0011`.
- Evidence-pilot regression passed 6/6.
- Full-case regression passed 4/4 for `PORT_0004`, `PORT_0008`, `CONS_0005`, and `PERF_0006`.
- `python -m py_compile scripts/dev/validate_case_package.py` passed.

Files created:
- `cases/LONGTAIL/LONGTAIL_0011/`
- `audits/full_case_migration_pilots/LONGTAIL_0011_canonical_full_case_migration_pilot.md`
- `audits/full_case_migration_pilots/LONGTAIL_0011_canonical_full_case_file_inventory.csv`
- `audits/full_case_migration_pilots/LONGTAIL_0011_canonical_full_case_validation.csv`
- `audits/full_case_migration_pilots/LONGTAIL_0011_validator_full_case_result.csv`
- `audits/full_case_migration_pilots/LONGTAIL_0011_validator_canonical_case_result.csv`
- `audits/full_case_migration_pilots/LONGTAIL_0011_evidence_pilot_regression_result.csv`
- `audits/full_case_migration_pilots/LONGTAIL_0011_full_case_regression_result.csv`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Paper/denominator impact:
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no
- workload-frequency claim created: no

Next safe action:
- Review the completed `LONGTAIL_0011` canonical-layout pilot and all four representative pool pilots, then decide whether to continue case-universe/report/script audits or plan the next bounded single-case pilot. Do not start Common-core 40 migration.

### 2026-05-16 · ed6ad71 · Common-core 40 batch migration readiness audit

Mode: release-repo audit/planning output; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Commit: ed6ad717f334b40bdd20e0230140bf3be16758fc
Push: pushed to origin main successfully (16abb75..ed6ad71)
Scope: Produced a planning-only readiness audit and future migration wave plan for the fixed Common-core v0 40 cases. No actual case migration was performed.

Summary:
- Inspected all 40 fixed Common-core cases in the legacy repository read-only.
- Classified each case by canonical layout fit, public hygiene risk, runs/evidence handling, pool-specific concerns, pilot pattern match, validator expectation, and migration wave.
- Created future batch prompt drafts for low-risk, sanitized-plan, checker-heavy, and complex LONGTAIL migration waves.
- Recommended the next actual migration as a small PERF sanitized-plan batch: `PERF_0007`, `PERF_0008`, and `PERF_0013`; fallback is `PERF_0007` only.
- Actual case migration performed: no.
- Common-core 40 migration started: no.

Validation:
- `python -m py_compile scripts/dev/validate_case_package.py` passed.
- Readiness summary JSON parsed.
- CSV row count checks passed for the 40-row readiness, runs-retention, and pattern-match matrices.
- `git diff --check` passed.

Files created:
- `audits/common_core40_batch_readiness/common_core40_batch_readiness_summary.md`
- `audits/common_core40_batch_readiness/common_core40_case_readiness_matrix.csv`
- `audits/common_core40_batch_readiness/common_core40_wave_plan.md`
- `audits/common_core40_batch_readiness/common_core40_risk_summary.md`
- `audits/common_core40_batch_readiness/common_core40_required_human_approvals.md`
- `audits/common_core40_batch_readiness/common_core40_runs_retention_needs.csv`
- `audits/common_core40_batch_readiness/common_core40_public_hygiene_findings.csv`
- `audits/common_core40_batch_readiness/common_core40_pattern_match.csv`
- `audits/common_core40_batch_readiness/common_core40_next_batch_recommendation.md`
- `audits/common_core40_batch_readiness/common_core40_batch_readiness_summary.json`
- `audits/common_core40_batch_readiness/common_core40_batch_prompts/batch_01_low_risk_canonical_migration_prompt.md`
- `audits/common_core40_batch_readiness/common_core40_batch_prompts/batch_02_sanitized_plan_migration_prompt.md`
- `audits/common_core40_batch_readiness/common_core40_batch_prompts/batch_03_checker_heavy_migration_prompt.md`
- `audits/common_core40_batch_readiness/common_core40_batch_prompts/batch_04_longtail_complex_migration_prompt.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Paper/denominator impact:
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no
- actual case migration performed: no

Next safe action:
- Review the Common-core 40 batch readiness audit, then decide whether to execute the recommended small PERF sanitized-plan batch (`PERF_0007`, `PERF_0008`, `PERF_0013`) or fallback to `PERF_0007` only. Do not start blind Common-core 40 migration.

### 2026-05-16 · f5ddf8e · PERF wave-2 sanitized-plan canonical migration batch 001

Mode: release-repo bounded batch canonical migration; legacy read-only source copy
Legacy repo modified: no
Release repo modified: yes
Commit: f5ddf8e3f6a5c2b19d7b28de2f6155f80bc7d053
Push: pushed to origin main successfully (434499a..f5ddf8e)
Scope: Migrated exactly the bounded PERF wave-2 batch cases `PERF_0007`, `PERF_0008`, and `PERF_0013` into canonical public-release layout.

Summary:
- Created canonical case packages under `cases/PERF/PERF_0007/`, `cases/PERF/PERF_0008/`, and `cases/PERF/PERF_0013/`.
- Used the completed `PERF_0006` canonical PERF pattern for README, manifest, SQL layout, schema/load layout, checker files, evidence layout, metadata, notes, and runs-retention mapping.
- Copied public-safe SQL, schema, witness load scripts, retained controls, hard-negative outputs, PostgreSQL plan evidence, and MySQL plan evidence.
- Adapted validation scripts as retained legacy validation assets with output-policy caveats; they were not executed.
- Created sanitized public Spark plan evidence under each case's `evidence/retained_plans/spark/`; raw Spark plan text files were not copied into public retained evidence.
- Recorded static-inferred hard-negative reasons: `quantity_predicate_boundary_changed`, `customer_segment_predicate_changed`, and `region_predicate_changed`.
- Raw `runs/` was not copied wholesale.
- Actual case migration performed: yes, for `PERF_0007`, `PERF_0008`, and `PERF_0013` only.
- Common-core 40 blind/bulk migration started: no.

Validation:
- SHA256 copy validation passed for byte-for-byte copied legacy files; generated, adapted, and sanitized derivatives are recorded separately.
- Public hygiene scan passed for all three migrated case directories.
- YAML validation passed for 14 YAML files per migrated case.
- JSON validation passed for 7 JSON files per migrated case.
- Validator v0.3 full-case mode passed 3/3 for `PERF_0007`, `PERF_0008`, and `PERF_0013`.
- Validator v0.3 canonical-case mode passed 3/3 for `PERF_0007`, `PERF_0008`, and `PERF_0013`.
- Evidence-pilot regression passed 6/6.
- Full-case regression passed 5/5 for `PORT_0004`, `PORT_0008`, `CONS_0005`, `PERF_0006`, and `LONGTAIL_0011`.
- `python -m py_compile scripts/dev/validate_case_package.py` passed.

Files created:
- `cases/PERF/PERF_0007/`
- `cases/PERF/PERF_0008/`
- `cases/PERF/PERF_0013/`
- `audits/batch_migration_pilots/perf_wave_2_batch_001/`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Paper/denominator impact:
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no
- speedup/timing claim created: no

Next safe action:
- Human review the bounded PERF wave-2 batch. If accepted, choose the next small reviewed wave from the readiness audit; do not start blind full Common-core 40 migration.

### 2026-05-16 · 78b29a3 · PERF wave-2 sanitized-plan canonical migration batch 002

Mode: release-repo bounded batch canonical migration; legacy read-only source copy
Legacy repo modified: no
Release repo modified: yes
Commit: 78b29a3b2f242e89989147a83ef92eac91f6ff9e
Push: pushed to origin main successfully (4b113a7..78b29a3)
Scope: Migrated exactly the bounded PERF wave-2 batch 002 cases `PERF_0017`, `PERF_0019`, and `PERF_0024` into canonical public-release layout.

Summary:
- Created canonical case packages under `cases/PERF/PERF_0017/`, `cases/PERF/PERF_0019/`, and `cases/PERF/PERF_0024/`.
- Used the completed `PERF_0006` canonical PERF pattern and successful PERF wave-2 batch 001 pattern for README, manifest, SQL layout, schema/load layout, checker files, evidence layout, metadata, notes, and runs-retention mapping.
- Copied public-safe SQL, schema, witness load scripts, retained controls, hard-negative outputs, PostgreSQL plan evidence, and MySQL plan evidence.
- Adapted validation scripts as retained legacy validation assets with output-policy caveats; they were not executed.
- Created sanitized public Spark plan evidence under each case's `evidence/retained_plans/spark/`; raw Spark plan text files were not copied into public retained evidence.
- Recorded static-inferred hard-negative reasons: `return_flag_predicate_changed`, `excluded_comment_phrase_changed`, and `part_name_prefix_predicate_changed`.
- Raw `runs/` was not copied wholesale.
- Actual case migration performed: yes, for `PERF_0017`, `PERF_0019`, and `PERF_0024` only.
- Common-core 40 blind/bulk migration started: no.

Validation:
- SHA256 copy validation passed for byte-for-byte copied legacy files; generated, adapted, and sanitized derivatives are recorded separately.
- Public hygiene scan passed for all three migrated case directories.
- YAML validation passed for 14 YAML files per migrated case.
- JSON validation passed for 7 JSON files per migrated case.
- Validator v0.3 full-case mode passed 3/3 for `PERF_0017`, `PERF_0019`, and `PERF_0024`.
- Validator v0.3 canonical-case mode passed 3/3 for `PERF_0017`, `PERF_0019`, and `PERF_0024`.
- Evidence-pilot regression passed 6/6.
- Full-case regression passed 8/8 for `PORT_0004`, `PORT_0008`, `CONS_0005`, `PERF_0006`, `LONGTAIL_0011`, `PERF_0007`, `PERF_0008`, and `PERF_0013`.
- Canonical-case regression passed 7/7 for `PORT_0008`, `CONS_0005`, `PERF_0006`, `LONGTAIL_0011`, `PERF_0007`, `PERF_0008`, and `PERF_0013`.
- `python -m py_compile scripts/dev/validate_case_package.py` passed.

Files created:
- `cases/PERF/PERF_0017/`
- `cases/PERF/PERF_0019/`
- `cases/PERF/PERF_0024/`
- `audits/batch_migration_pilots/perf_wave_2_batch_002/`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Paper/denominator impact:
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no
- speedup/timing claim created: no

Next safe action:
- Human review the bounded PERF wave-2 batch 002. If accepted, choose the next small reviewed wave from the readiness audit; do not start blind full Common-core 40 migration.

### 2026-05-16 · 79c2465 · PERF wave-2 sanitized-plan canonical migration batch 003

Mode: release-repo bounded batch canonical migration; legacy read-only source copy
Legacy repo modified: no
Release repo modified: yes
Commit: 79c24655c3d2f78147f9819ebad6a59450dbf961
Push: pushed to origin main successfully (8fef68b..79c2465)
Scope: Migrated exactly the bounded PERF wave-2 batch 003 cases `PERF_0033`, `PERF_0034`, and `PERF_0035` into canonical public-release layout.

Summary:
- Created canonical case packages under `cases/PERF/PERF_0033/`, `cases/PERF/PERF_0034/`, and `cases/PERF/PERF_0035/`.
- Used the completed `PERF_0006` canonical PERF pattern and successful PERF wave-2 batch 001/002 patterns for README, manifest, SQL layout, schema/load layout, checker files, evidence layout, metadata, notes, and runs-retention mapping.
- Copied public-safe SQL, schema, witness load scripts, retained controls, hard-negative outputs, PostgreSQL plan evidence, and MySQL plan evidence.
- Adapted validation scripts as retained legacy validation assets with output-policy caveats; they were not executed.
- Created sanitized public Spark plan evidence under each case's `evidence/retained_plans/spark/`; raw Spark plan text files were not copied into public retained evidence.
- Recorded static-inferred hard-negative reasons: `manager_id_predicate_changed`, `gmt_offset_predicate_changed`, and `year_filter_predicate_changed`.
- Raw `runs/` was not copied wholesale.
- Actual case migration performed: yes, for `PERF_0033`, `PERF_0034`, and `PERF_0035` only.
- Common-core 40 blind/bulk migration started: no.

Validation:
- SHA256 copy validation passed for byte-for-byte copied legacy files; generated, adapted, and sanitized derivatives are recorded separately.
- Public hygiene scan passed for all three migrated case directories.
- YAML validation passed for migrated case YAML files.
- JSON validation passed for migrated case evidence/metadata JSON files.
- Validator v0.3 full-case mode passed 3/3 for `PERF_0033`, `PERF_0034`, and `PERF_0035`.
- Validator v0.3 canonical-case mode passed 3/3 for `PERF_0033`, `PERF_0034`, and `PERF_0035`.
- Evidence-pilot regression passed 6/6.
- Full-case regression passed 11/11 for `PORT_0004`, `PORT_0008`, `CONS_0005`, `PERF_0006`, `LONGTAIL_0011`, `PERF_0007`, `PERF_0008`, `PERF_0013`, `PERF_0017`, `PERF_0019`, and `PERF_0024`.
- Canonical-case regression passed 10/10 for `PORT_0008`, `CONS_0005`, `PERF_0006`, `LONGTAIL_0011`, `PERF_0007`, `PERF_0008`, `PERF_0013`, `PERF_0017`, `PERF_0019`, and `PERF_0024`.
- `python -m py_compile scripts/dev/validate_case_package.py` passed.

Files created:
- `cases/PERF/PERF_0033/`
- `cases/PERF/PERF_0034/`
- `cases/PERF/PERF_0035/`
- `audits/batch_migration_pilots/perf_wave_2_batch_003/`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Paper/denominator impact:
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no
- speedup/timing claim created: no

Next safe action:
- Human review the bounded PERF wave-2 batch 003. If accepted, choose the next small reviewed wave from the readiness audit; do not start blind full Common-core 40 migration.

### 2026-05-16 · 98fafa4 · PERF wave-2 final sanitized-plan canonical migration batch

Mode: release-repo bounded batch canonical migration; legacy read-only source copy
Legacy repo modified: no
Release repo modified: yes
Commit: 98fafa41ac40ce766dcb3d26bc9eab98c9ff3890
Push: pushed to origin main successfully (2391de3..98fafa4)
Scope: Migrated exactly the bounded PERF wave-2 final batch cases `PERF_0052`, `PERF_0054`, `PERF_0056`, `PERF_0062`, `PERF_0077`, and `PERF_0082` into canonical public-release layout.

Summary:
- Created canonical case packages under `cases/PERF/PERF_0052/`, `cases/PERF/PERF_0054/`, `cases/PERF/PERF_0056/`, `cases/PERF/PERF_0062/`, `cases/PERF/PERF_0077/`, and `cases/PERF/PERF_0082/`.
- Used the completed `PERF_0006` canonical PERF pattern and successful PERF wave-2 batch 001/002/003 patterns for README, manifest, SQL layout, schema/load layout, checker files, evidence layout, metadata, notes, and runs-retention mapping.
- Copied public-safe SQL, schema, witness load scripts, retained controls, hard-negative outputs, PostgreSQL plan evidence, and MySQL plan evidence.
- Adapted validation scripts as retained legacy validation assets with output-policy caveats; they were not executed.
- Created sanitized public Spark plan evidence under each case's `evidence/retained_plans/spark/`; raw Spark plan text files were not copied into public retained evidence.
- Recorded static-inferred hard-negative reasons: `store_state_predicate_changed`, `manufacturer_id_predicate_changed`, `having_count_threshold_changed`, `year_filter_predicate_changed`, `keyword_like_predicate_narrowed`, and `company_type_predicate_changed`.
- Raw `runs/` was not copied wholesale.
- Actual case migration performed: yes, for the six selected final PERF cases only.
- PERF pool canonical migration complete: yes at case-package level.
- Common-core 40 blind/bulk migration started: no.

Validation:
- SHA256 copy validation passed for byte-for-byte copied legacy files; generated, adapted, and sanitized derivatives are recorded separately.
- Public hygiene scan passed for all six migrated case directories.
- YAML validation passed for migrated case YAML files.
- JSON validation passed for migrated case evidence/metadata JSON files.
- Validator v0.3 full-case mode passed 6/6 for `PERF_0052`, `PERF_0054`, `PERF_0056`, `PERF_0062`, `PERF_0077`, and `PERF_0082`.
- Validator v0.3 canonical-case mode passed 6/6 for `PERF_0052`, `PERF_0054`, `PERF_0056`, `PERF_0062`, `PERF_0077`, and `PERF_0082`.
- Evidence-pilot regression passed 6/6.
- Full-case regression passed 20/20 including the six new final PERF cases after migration.
- Canonical-case regression passed 19/19 including the six new final PERF cases after migration.
- `python -m py_compile scripts/dev/validate_case_package.py` passed.

Files created:
- `cases/PERF/PERF_0052/`
- `cases/PERF/PERF_0054/`
- `cases/PERF/PERF_0056/`
- `cases/PERF/PERF_0062/`
- `cases/PERF/PERF_0077/`
- `cases/PERF/PERF_0082/`
- `audits/batch_migration_pilots/perf_wave_2_final_batch/`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Paper/denominator impact:
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no
- speedup/timing claim created: no

Next safe action:
- Human review the completed PERF pool canonical migration. Then choose the next reviewed non-PERF wave from the readiness audit; do not start blind full Common-core 40 migration.

### 2026-05-16 · 1d02937 · CONS hard-negative expected-rejection approval sweep

Mode: release-repo semantic review/audit output; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Commit: 1d02937b3c81a2df4db8e3b978b3d78983921af2
Push: pushed to origin main successfully (c4f246a..1d02937)
Scope: Reviewed CONS Common-core hard-negative semantics for `CONS_0005`, `CONS_0007`, `CONS_0009`, `CONS_0010`, `CONS_0011`, `CONS_0012`, `CONS_0024`, `CONS_0036`, and `CONS_0037`; no case migration was performed.

Summary:
- Used `CONS_0005` as the already migrated and maintainer-approved reference row.
- Prepared approval wording for the eight non-pilot CONS Common-core cases.
- Generated an approval matrix, expected-rejections YAML preview, evidence map, review dossiers, CONS batch recommendation, summary JSON, and two future migration prompt drafts.
- Recommended primary next CONS batch after approval: `CONS_0007`, `CONS_0009`, `CONS_0010`, and `CONS_0011`.
- Recommended fallback batch after approval: `CONS_0007`, `CONS_0009`, and `CONS_0010`.
- Actual case migration performed: no.
- Common-core 40 blind/bulk migration started: no.

Validation:
- `python -m py_compile scripts/dev/validate_case_package.py` passed.
- JSON parse passed for `audits/cons_hard_negative_approval/cons_hard_negative_approval_summary.json`.
- YAML parse passed for `audits/cons_hard_negative_approval/cons_expected_rejections_preview.yaml`.
- CSV row-count check passed: `cons_hard_negative_approval_matrix.csv` has 9 data rows.
- CSV evidence-map check passed: `cons_hard_negative_evidence_map.csv` has 55 data rows.
- `git diff --check` result: passed.

Files created:
- `audits/cons_hard_negative_approval/cons_hard_negative_approval_summary.md`
- `audits/cons_hard_negative_approval/cons_hard_negative_approval_matrix.csv`
- `audits/cons_hard_negative_approval/cons_expected_rejections_preview.yaml`
- `audits/cons_hard_negative_approval/cons_hard_negative_evidence_map.csv`
- `audits/cons_hard_negative_approval/cons_hard_negative_review_dossiers.md`
- `audits/cons_hard_negative_approval/cons_migration_batch_recommendation.md`
- `audits/cons_hard_negative_approval/cons_hard_negative_approval_summary.json`
- `audits/cons_hard_negative_approval/future_prompts/cons_batch_001_canonical_migration_prompt.md`
- `audits/cons_hard_negative_approval/future_prompts/cons_batch_002_canonical_migration_prompt.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Paper/denominator impact:
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Next safe action:
- Maintainer review and approve the expected-rejection wording in `audits/cons_hard_negative_approval/cons_expected_rejections_preview.yaml`; if approved, run the future CONS batch 001 prompt. Do not start blind full Common-core 40 migration.

### 2026-05-16 · f6b31d3 · CONS hard-negative approved canonical migration batch 001

Mode: release-repo bounded CONS canonical migration; legacy read-only source copy
Legacy repo modified: no
Release repo modified: yes
Commit: `f6b31d3665d18d9f34845a47e94db403370de439`
Push: `origin/main` updated `30f0c87..f6b31d3`
Scope: Migrated exactly the bounded CONS batch 001 cases `CONS_0007`, `CONS_0009`, `CONS_0010`, and `CONS_0011` into canonical public-release layout.

Summary:
- Used the completed `CONS_0005` canonical checker/hard-negative pattern and the CONS approval sweep outputs.
- Recorded maintainer-approved expected rejection reasons in `checker/expected_rejections.yaml`, README files, migration notes, and the batch audit report.
- Created canonical case packages under `cases/CONS/CONS_0007/`, `cases/CONS/CONS_0009/`, `cases/CONS/CONS_0010/`, and `cases/CONS/CONS_0011/`.
- Copied public-safe SQL, schema, witness load scripts, retained controls, hard-negative outputs, PostgreSQL plan evidence, and MySQL plan evidence.
- Adapted validation scripts as retained legacy validation assets with output-policy caveats; they were not executed.
- Created sanitized public Spark plan evidence under each case's `evidence/retained_plans/spark/`; raw Spark plan text files were not copied into public retained evidence.
- Raw `runs/` was not copied wholesale.
- Actual case migration performed: yes, for `CONS_0007`, `CONS_0009`, `CONS_0010`, and `CONS_0011` only.
- Common-core 40 blind/bulk migration started: no.

Validation:
- SHA256 copy validation passed for byte-for-byte copied legacy files; generated, adapted, and sanitized derivatives are recorded separately.
- Public hygiene scan passed for all four migrated case directories.
- YAML validation passed for migrated case YAML files.
- JSON validation passed for migrated case evidence/metadata JSON files.
- Validator v0.3 full-case mode passed 4/4 for `CONS_0007`, `CONS_0009`, `CONS_0010`, and `CONS_0011`.
- Validator v0.3 canonical-case mode passed 4/4 for `CONS_0007`, `CONS_0009`, `CONS_0010`, and `CONS_0011`.
- Evidence-pilot regression passed 6/6.
- Full-case regression passed 24/24 including the four new CONS cases after migration.
- Canonical-case regression passed 23/23 including the four new CONS cases after migration.
- `python -m py_compile scripts/dev/validate_case_package.py` passed.
- `git diff --check` result: passed.

Files created:
- `cases/CONS/CONS_0007/`
- `cases/CONS/CONS_0009/`
- `cases/CONS/CONS_0010/`
- `cases/CONS/CONS_0011/`
- `audits/batch_migration_pilots/cons_batch_001/`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Paper/denominator impact:
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Next safe action:
- Human review CONS batch 001. If accepted, consider approved CONS batch 002 for `CONS_0012`, `CONS_0024`, `CONS_0036`, and `CONS_0037`; do not start blind full Common-core 40 migration.

### 2026-05-16 · e21210f · CONS hard-negative approved canonical migration batch 002

Mode: release-repo bounded CONS canonical migration; legacy read-only source copy
Legacy repo modified: no
Release repo modified: yes
Commit: `e21210f1ade3e784f7ce5509e104cad9fda18a1c`
Push: `origin/main` updated `6d2b325..e21210f`
Scope: Migrated exactly the bounded CONS batch 002 cases `CONS_0012`, `CONS_0024`, `CONS_0036`, and `CONS_0037` into canonical public-release layout.

Summary:
- Used the completed `CONS_0005` canonical checker/hard-negative pattern, the CONS approval sweep outputs, and successful CONS batch 001 as the package pattern.
- Recorded maintainer-approved expected rejection reasons in `checker/expected_rejections.yaml`, README files, migration notes, and the batch audit report.
- Created canonical case packages under `cases/CONS/CONS_0012/`, `cases/CONS/CONS_0024/`, `cases/CONS/CONS_0036/`, and `cases/CONS/CONS_0037/`.
- Copied public-safe SQL, schema, witness load scripts, retained controls, hard-negative outputs, PostgreSQL plan evidence, and MySQL plan evidence.
- Adapted validation scripts as retained legacy validation assets with output-policy caveats; they were not executed.
- Created sanitized public Spark plan evidence under each case's `evidence/retained_plans/spark/`; raw Spark plan text files were not copied into public retained evidence.
- Raw `runs/` was not copied wholesale.
- CONS pool canonical migration complete: yes, at canonical-layout case-package level.
- Actual case migration performed: yes, for `CONS_0012`, `CONS_0024`, `CONS_0036`, and `CONS_0037` only.
- Common-core 40 blind/bulk migration started: no.

Validation:
- SHA256 copy validation passed for byte-for-byte copied legacy files; generated, adapted, and sanitized derivatives are recorded separately.
- Public hygiene scan passed for all four migrated case directories.
- YAML validation passed for migrated case YAML files.
- JSON validation passed for migrated case evidence/metadata JSON files.
- Validator v0.3 full-case mode passed 4/4 for `CONS_0012`, `CONS_0024`, `CONS_0036`, and `CONS_0037`.
- Validator v0.3 canonical-case mode passed 4/4 for `CONS_0012`, `CONS_0024`, `CONS_0036`, and `CONS_0037`.
- Evidence-pilot regression passed 6/6.
- Full-case regression passed 28/28 including the four new CONS batch 002 cases after migration.
- Canonical-case regression passed 27/27 including the four new CONS batch 002 cases after migration.
- `python -m py_compile scripts/dev/validate_case_package.py` passed.
- `git diff --check` result: passed.

Files created:
- `cases/CONS/CONS_0012/`
- `cases/CONS/CONS_0024/`
- `cases/CONS/CONS_0036/`
- `cases/CONS/CONS_0037/`
- `audits/batch_migration_pilots/cons_batch_002/`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Paper/denominator impact:
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Next safe action:
- Human review CONS batch 002 and the completed CONS pool canonical migration. Do not start blind full Common-core 40 migration.

### 2026-05-16 · 47b83ad · PORT wave-2 canonical migration batch 001

Mode: release-repo bounded PORT canonical migration; legacy read-only source copy
Legacy repo modified: no
Release repo modified: yes
Commit: `47b83ad1a1594b0ca84b4009f163f11dc3abfa46`
Push: `origin/main` updated `f091824..47b83ad`
Scope: Migrated exactly the bounded PORT wave-2 batch 001 cases `PORT_0003`, `PORT_0005`, `PORT_0012`, and `PORT_0013` into canonical public-release layout.

Summary:
- Used `PORT_0008` as the canonical PORT pattern.
- Kept `PORT_0004` as a legacy-compatible full-case pilot only; it was not used as the canonical template and remains excluded from canonical-case regression.
- Created canonical case packages under `cases/PORT/PORT_0003/` and `cases/PORT/PORT_0005/`.
- Upgraded existing evidence-mapping pilot slices under `cases/PORT/PORT_0012/` and `cases/PORT/PORT_0013/` into canonical case packages while retaining `MIGRATION_PILOT.md` and reusing validated sanitized Spark plan files.
- Copied public-safe SQL, schema, witness load scripts, retained controls, hard-negative outputs, and JSON plan evidence.
- Adapted validation scripts as retained legacy validation assets with output-policy caveats; they were not executed.
- Created or reused sanitized public Spark plan evidence; raw Spark plan text files were not copied into public retained evidence.
- Raw `runs/` was not copied wholesale and raw stdout/stderr logs were not copied into public evidence.
- Actual case migration performed: yes, for `PORT_0003`, `PORT_0005`, `PORT_0012`, and `PORT_0013` only.
- Common-core 40 blind/bulk migration started: no.

Validation:
- SHA256 copy validation passed for byte-for-byte copied legacy files; generated, adapted, and sanitized derivatives are recorded separately.
- Public hygiene scan passed for all four migrated case directories.
- YAML validation passed for migrated case YAML files.
- JSON validation passed for migrated case evidence/metadata JSON files.
- Validator v0.3 full-case mode passed 4/4 for `PORT_0003`, `PORT_0005`, `PORT_0012`, and `PORT_0013`.
- Validator v0.3 canonical-case mode passed 4/4 for `PORT_0003`, `PORT_0005`, `PORT_0012`, and `PORT_0013`.
- Evidence-pilot regression passed 6/6.
- Full-case regression passed 32/32 including the four new PORT batch 001 cases after migration.
- Canonical-case regression passed 31/31 including the four new PORT batch 001 cases after migration and excluding legacy-compatible `PORT_0004`.
- `python -m py_compile scripts/dev/validate_case_package.py` passed.
- `git diff --check` result: passed.

Files created:
- `cases/PORT/PORT_0003/`
- `cases/PORT/PORT_0005/`
- canonical package files under `cases/PORT/PORT_0012/`
- canonical package files under `cases/PORT/PORT_0013/`
- `audits/batch_migration_pilots/port_wave_2_batch_001/`

Files modified:
- `cases/PORT/PORT_0012/evidence/runs_retention.yaml`
- `cases/PORT/PORT_0013/evidence/runs_retention.yaml`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Paper/denominator impact:
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no
- cross-engine result created: no
- full PORT9 claim created: no
- speedup-transfer claim created: no

Next safe action:
- Human review PORT wave-2 batch 001. If accepted, select the next bounded PORT wave from the readiness audit; do not start blind full Common-core 40 migration.

### 2026-05-16 · d96a589 · PORT final bounded canonical migration batch

Mode: release-repo bounded PORT canonical migration and PORT_0004 canonical upgrade; legacy read-only source copy
Legacy repo modified: no
Release repo modified: yes
Commit: `d96a5891296dade425898b3f4d8964f0af9c9737`
Push: `origin/main` updated `3790971..d96a589`
Scope: Upgraded `PORT_0004` from a legacy-compatible full-case pilot to canonical layout and migrated `PORT_0022`, `PORT_0024`, and `PORT_0025` from formal evidence-mapping pilot slices to canonical public-release layout.

Summary:
- Used `PORT_0008` as the canonical PORT pattern and reused successful PORT wave-2 batch 001 structure.
- Preserved `PORT_0004` pilot history in `notes/migration_pilot_history.md`.
- Preserved evidence-mapping pilot artifacts for `PORT_0022`, `PORT_0024`, and `PORT_0025`, including root `MIGRATION_PILOT.md` files for evidence-pilot regression compatibility.
- Reused existing sanitized Spark plan evidence for all four selected cases.
- Reused `PORT_0024` sanitized Spark result-check summary and did not copy raw stdout/stderr logs.
- Copied public-safe SQL, schema, witness load scripts, retained controls, hard-negative outputs, and JSON plan evidence.
- Adapted validation scripts as retained legacy validation assets with output-policy caveats; they were not executed.
- Raw `runs/` was not copied wholesale and raw Spark plan text files were not copied into public retained evidence.
- PORT pool canonical migration complete: yes, at case-package level.
- Actual case migration/upgrades performed: yes, for `PORT_0004`, `PORT_0022`, `PORT_0024`, and `PORT_0025` only.
- Common-core 40 blind/bulk migration started: no.

Validation:
- SHA256 copy validation passed for byte-for-byte copied legacy files; generated, adapted, and sanitized derivatives are recorded separately.
- Public hygiene scan passed for all four migrated/upgraded case directories.
- YAML validation passed for migrated/upgraded case YAML files.
- JSON validation passed for migrated/upgraded case evidence/metadata JSON files.
- Validator v0.3 full-case mode passed 4/4 for `PORT_0004`, `PORT_0022`, `PORT_0024`, and `PORT_0025`.
- Validator v0.3 canonical-case mode passed 4/4 for `PORT_0004`, `PORT_0022`, `PORT_0024`, and `PORT_0025`.
- Evidence-pilot regression passed 6/6.
- Full-case regression passed 35/35.
- Canonical-case regression passed 35/35.
- `python -m py_compile scripts/dev/validate_case_package.py` passed.
- `git diff --check` result: passed after CSV line-ending normalization.

Files created:
- canonical package files under `cases/PORT/PORT_0004/`
- canonical package files under `cases/PORT/PORT_0022/`
- canonical package files under `cases/PORT/PORT_0024/`
- canonical package files under `cases/PORT/PORT_0025/`
- `audits/batch_migration_pilots/port_final_bounded_batch/`

Files modified:
- `cases/PORT/PORT_0004/`
- `cases/PORT/PORT_0022/evidence/runs_retention.yaml`
- `cases/PORT/PORT_0024/evidence/runs_retention.yaml`
- `cases/PORT/PORT_0025/evidence/runs_retention.yaml`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Paper/denominator impact:
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no
- cross-engine result created: no
- full PORT9 result claim created: no
- speedup-transfer claim created: no

Next safe action:
- Human review PORT final bounded batch and completed PORT pool canonical case-package migration, then perform a Common-core case-package migration status audit/closeout before any case-set/report/result update.

### 2026-05-16 · 71178a7 · Common-core case-package migration status closeout

Mode: release-repo closeout/audit output; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Actual case migration performed: no
Commit: `71178a7f34eed73da18e5846a530e073012e8b7f`
Push: `origin/main` updated `44d65d5..71178a7`

Summary:
- Verified the fixed Common-core v0 40-case membership from release-repo package files and validator outputs.
- Confirmed canonical case-package completion counts: PERF 16/16, CONS 9/9, PORT 9/9, LONGTAIL 1/6, total 35/40.
- Confirmed remaining not-yet-canonical cases: LONGTAIL_0012, LONGTAIL_0013, LONGTAIL_0022, LONGTAIL_0023, and LONGTAIL_0024.
- Confirmed Common-core 40 blind/bulk migration is still not started.
- Created closeout audit outputs under `audits/common_core40_case_package_closeout/`.
- Cleaned `project_control/MIGRATION_STATUS.md` into a concise current-state snapshot.
- Did not modify migrated case packages, case sets, reports, results, denominator files, or legacy evidence.

Validation:
- Validator v0.3 full-case closeout: PASS 35/35.
- Validator v0.3 canonical-case closeout: PASS 35/35.
- Python compile, JSON parse, CSV row counts, and git checks: passed.

Paper/denominator impact:
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Next safe action:
- Review this closeout, then plan the remaining LONGTAIL bounded wave; do not touch case_sets, reports, results, denominator files, or paper tables yet.

### 2026-05-16 · 5cd2674 · LONGTAIL final readiness and canonical migration planning wave

Mode: release-repo readiness/planning output; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Actual case migration performed: no
Commit: `5cd26741526ace757538b0479ebb9a2e470fba0b`
Push: `origin/main` updated `e6828e9..5cd2674`

Summary:
- Reviewed remaining LONGTAIL Common-core cases `LONGTAIL_0012`, `LONGTAIL_0013`, `LONGTAIL_0022`, `LONGTAIL_0023`, and `LONGTAIL_0024` from legacy files read-only.
- Prepared hard-negative expected-rejection previews, structural boundary review, public hygiene findings, and future bounded migration prompts under `audits/longtail_final_readiness/`.
- Confirmed Common-core case-package migration remains 35/40; PERF, CONS, and PORT remain canonical complete; `LONGTAIL_0011` remains the completed LONGTAIL canonical reference.
- Recommended a bounded final LONGTAIL batch after maintainer approval, with `LONGTAIL_0012` and `LONGTAIL_0013` as fallback first batch.
- Did not create canonical case packages, copy case files into release cases, update case_sets, update reports/results, change denominator, change paper results, or mutate legacy evidence.

Validation:
- Python compile, JSON parse, YAML parse, CSV row count, and git checks: passed.

Paper/denominator impact:
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Next safe action:
- Maintainer review/approve expected rejection wording in `audits/longtail_final_readiness/longtail_expected_rejections_preview.yaml`, then run the bounded final LONGTAIL canonical migration prompt; do not touch case_sets, reports, results, denominator files, or paper tables yet.

### 2026-05-16 · 6792fd2 · LONGTAIL final bounded canonical migration batch

Mode: release-repo bounded LONGTAIL canonical migration; legacy read-only source copy
Legacy repo modified: no
Release repo modified: yes
Actual case migration performed: yes
Commit: `6792fd2bb542460fe7dd434c2aa181d71f3eb716`
Push: `origin/main` updated `66db267..6792fd2`

Summary:
- Migrated `LONGTAIL_0012`, `LONGTAIL_0013`, `LONGTAIL_0022`, `LONGTAIL_0023`, and `LONGTAIL_0024` into canonical public-release layout.
- Recorded maintainer-approved hard-negative expected rejection reasons in each case package and in `audits/longtail_final_bounded_migration/longtail_expected_rejection_approval_record.yaml`.
- Published public-safe retained controls, hard-negative outputs, JSON plan evidence, and sanitized Spark plan copies.
- Did not copy raw Spark plan text with local path traces into public retained evidence.
- Copied validation scripts only as retained legacy validation assets; they were not executed during migration.
- Common-core case-package migration moved from 35/40 to 40/40 after validator PASS results.
- Common-core 40 blind/bulk migration started: no.

Validation:
- Selected-case validator v0.3 full-case: PASS 5/5.
- Selected-case validator v0.3 canonical-case: PASS 5/5.
- Full Common-core full-case regression: PASS 40/40.
- Full Common-core canonical-case regression: PASS 40/40.
- Public hygiene scan, YAML parse, JSON parse, CSV row checks, and `python -m py_compile scripts/dev/validate_case_package.py`: passed.

Files created:
- canonical package files under `cases/LONGTAIL/LONGTAIL_0012/`
- canonical package files under `cases/LONGTAIL/LONGTAIL_0013/`
- canonical package files under `cases/LONGTAIL/LONGTAIL_0022/`
- canonical package files under `cases/LONGTAIL/LONGTAIL_0023/`
- canonical package files under `cases/LONGTAIL/LONGTAIL_0024/`
- `audits/longtail_final_bounded_migration/`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Paper/denominator impact:
- denominator changed: no
- paper results changed: no
- case membership changed: no
- case_sets changed: no
- reports changed: no
- results changed: no
- raw legacy evidence changed: no

Next safe action:
- Review the final LONGTAIL migration audit, then perform a separate Common-core 40 case-package completion closeout if desired; do not touch case_sets, reports, results, denominator files, or paper tables yet.

### 2026-05-16 · 8ce8dd7 · Common-core 40 canonical case-package final closeout

Mode: release-repo final closeout/audit output; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Actual case migration performed: no
Commit: `8ce8dd7855201a2cf863a49eb6d1f2ca2393b85d`
Push: `origin/main` updated `65810c3..8ce8dd7`

Summary:
- Verified the fixed Common-core v0 40-case membership from release-repo package files and fresh validator v0.3 outputs.
- Confirmed canonical case-package completion counts: PERF 16/16, CONS 9/9, PORT 9/9, LONGTAIL 6/6, total 40/40.
- Created final closeout audit outputs under `audits/common_core40_final_closeout/`.
- Updated `project_control/MIGRATION_STATUS.md` as the concise 40/40 current-state snapshot.
- Did not migrate cases, create evidence, run DB engines, run timing workloads, update case sets, update reports/results, change denominator, change paper results, alter paper tables, or mutate legacy evidence.

Validation:
- Validator v0.3 full-case final closeout: PASS 40/40.
- Validator v0.3 canonical-case final closeout: PASS 40/40.
- Python compile, JSON parse, CSV row counts, and git checks: passed.

Paper/denominator impact:
- denominator changed: no
- paper results changed: no
- case membership changed: no
- case_sets changed: no
- reports changed: no
- results changed: no
- raw legacy evidence changed: no

Next safe action:
- Start a separate bounded task for Common-core 40 case-set, inventory, and registry alignment, or for reports/results retained evidence mapping; do not touch case_sets, reports, results, denominator files, or paper tables without that explicit scope.

### 2026-05-16 · b0f710d · Common-core 40 case-set, inventory, and registry alignment

Mode: release-repo membership and registry alignment; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Commit: `b0f710d492add1738bc360a980231938870f5863`
Push: `origin/main` updated `b60e3a4..b0f710d`

Summary:
- Created `case_sets/common_core_v0/manifest.yaml` for fixed Common-core v0 release membership.
- Created `case_sets/common_core_v0/cases.csv` with 40 fixed Common-core case rows.
- Created `case_sets/common_core_v0/denominator_same_engine_120.csv` with 120 planned same-engine scaffold rows.
- Created `case_sets/common_core_v0/controls_360.csv` with 360 planned source/positive/hard-negative control scaffold rows.
- Created `inventory/case_registry.csv` with 40 Common-core public v0 registry rows.
- Created `inventory/source_registry.csv` with source-family rows inferred from existing migrated case manifests and no new license claims.
- Created registry alignment audit outputs under `audits/common_core40_registry_alignment/`.
- Did not migrate cases, run DB engines, regenerate evidence, rerun timing, update reports/results, change denominator values, change paper results, alter paper tables, or mutate legacy evidence.

Validation:
- Python compile, JSON parse, YAML parse, CSV row counts, git diff check, and scope checks: passed.

Paper/denominator impact:
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no
- reports changed: no
- results changed: no

Next safe action:
- Start a separate bounded reports/results retained evidence map using the aligned Common-core v0 membership and inventory files; do not update result metrics, denominator values, paper tables, or raw legacy evidence without explicit scope.

### 2026-05-16 · d837040 · Common-core reports/results retained evidence map

Mode: release-repo reports/results retained-evidence mapping audit; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Commit: `d837040e18f5e6c3b5c11c7fdcb3072b067884e4`
Push: `origin/main` updated `f09bfe1..d837040`

Summary:
- Inspected legacy `reports/`, `reports/evaluation/common_core_v0/`, `results/`, `results/retained`, `results/local`, and top-level `runs/` read-only.
- Confirmed legacy `results/`, `results/retained`, `results/local`, and top-level `runs/` are absent in the inspected legacy snapshot.
- Created `audits/reports_results_retained_evidence_map/reports_results_artifact_inventory.csv` with static classifications for discovered relevant report artifacts and explicit missing-path records.
- Created `audits/reports_results_retained_evidence_map/retained_evidence_candidate_map.csv` with `copy_now=false` for every retained-evidence candidate.
- Created manual-review, boundary, and future public migration planning notes under `audits/reports_results_retained_evidence_map/`.
- Did not copy reports/results, update release reports/results, recompute metrics, regenerate paper tables, change denominator values, change case membership, or mutate raw legacy evidence.

Validation:
- Python compile, JSON parse, CSV header/row checks, `copy_now=false` check, and git diff check: passed.

Paper/denominator impact:
- reports changed: no
- results changed: no
- denominator changed: no
- paper results changed: no
- raw legacy evidence changed: no

Next safe action:
- Start a separate bounded public reports/results retained-evidence migration planning task that selects a minimal reviewed subset from the retained-evidence map; do not update result metrics, denominator values, paper tables, or raw legacy evidence without explicit scope.

### 2026-05-16 · c150b2b · Workbench redevelopment strategy alignment

Mode: release-repo planning/spec output; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Actual case migration performed: no
Commit: `c150b2b90c27a6d02440e92a156fc093c70f1e28`
Push: `origin/main` updated `fe7a43e..c150b2b`

Summary:
- Recorded decision `D016` in `project_control/DECISION_LOG.md`, shifting the public release project from migration-first work to redevelopment-led public workbench construction.
- Drafted future-facing repository specs for the evidence ledger schema, metrics contract, public runner output policy, and workbench redevelopment plan.
- Created strategy-alignment audit outputs under `audits/workbench_redevelopment_alignment/`.
- Reclassified legacy scripts, reports, results, runs, paper tables, and non-common-core cases as reference inputs, retained evidence sources, adapter targets, comparison targets, or governed backlog rather than architecture to copy wholesale.
- Updated `project_control/MIGRATION_STATUS.md` to mark the current phase as workbench redevelopment.
- Did not migrate cases, copy reports/results, implement scripts, run DB engines, compute metrics, regenerate evidence, update case sets, change denominator values, change paper results, or mutate raw legacy evidence.

Files created:
- `repository_spec/evidence_ledger_schema_v1_draft.md`
- `repository_spec/metrics_contract_v1_draft.md`
- `repository_spec/public_runner_output_policy_v1_draft.md`
- `repository_spec/workbench_redevelopment_plan_v1.md`
- `audits/workbench_redevelopment_alignment/redevelopment_alignment_summary.md`
- `audits/workbench_redevelopment_alignment/legacy_artifact_role_reclassification.md`
- `audits/workbench_redevelopment_alignment/script_redevelopment_roadmap.md`
- `audits/workbench_redevelopment_alignment/retained_evidence_adapter_plan.md`
- `audits/workbench_redevelopment_alignment/open_questions_before_reproduction_interface.md`
- `audits/workbench_redevelopment_alignment/redevelopment_alignment_summary.json`

Files modified:
- `project_control/DECISION_LOG.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- JSON parse and git diff check: passed.

Paper/denominator impact:
- reports changed: no
- results changed: no
- denominator changed: no
- paper results changed: no
- raw legacy evidence changed: no
- metrics finalized: no
- reproduction interface implementation authorized: no

Next safe action:
- Resolve metric-contract and reproduction-interface open questions with the maintainer/team before implementing metrics computation, a unified reproduction CLI, paper table rendering, or public runner outputs.

### 2026-05-16 · 539a2ab · Common-core retained evidence to ledger mapping audit

Mode: release-repo retained-evidence to draft-ledger mapping audit; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Commit: `539a2abebd6515785e066b6ec22e693285031c08`
Push: `origin/main` updated `3707f0c..539a2ab`

Summary:
- Mapped the already-discovered Common-core retained evidence candidate groups to draft evidence ledger fields using `audits/reports_results_retained_evidence_map/retained_evidence_candidate_map.csv` as the primary input.
- Processed 3,439 retained candidate rows as grouped audit input: 3,080 method output references, 276 paper-facing retained evidence rows, 69 paper summary table rows, and 14 denominator or membership reference rows.
- Created ledger field coverage, source inventory, adapter gap, adapter module design, metric dependency, and implementation-blocker outputs under `audits/retained_evidence_ledger_mapping/`.
- Updated `project_control/MIGRATION_STATUS.md` to record that retained evidence to ledger mapping is complete as an audit-only step.
- Did not copy reports/results, create `results/retained`, create `reports/evaluation`, implement scripts, modify `scripts/`, implement `src/`, run DB engines, run validation scripts, run LLM calls, run timing workloads, regenerate evidence, compute metrics, render paper tables, update denominator values, change case membership, modify `case_sets/`, modify migrated case packages, or mutate raw legacy evidence.

Files created:
- `audits/retained_evidence_ledger_mapping/retained_evidence_ledger_mapping_summary.md`
- `audits/retained_evidence_ledger_mapping/retained_evidence_to_ledger_field_map.csv`
- `audits/retained_evidence_ledger_mapping/common_core_ledger_source_inventory.csv`
- `audits/retained_evidence_ledger_mapping/ledger_field_coverage_matrix.csv`
- `audits/retained_evidence_ledger_mapping/retained_evidence_adapter_gap_report.md`
- `audits/retained_evidence_ledger_mapping/adapter_module_design.md`
- `audits/retained_evidence_ledger_mapping/metrics_dependency_matrix.csv`
- `audits/retained_evidence_ledger_mapping/implementation_blockers_before_metrics.md`
- `audits/retained_evidence_ledger_mapping/retained_evidence_ledger_mapping_summary.json`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- JSON parse, CSV checks, git diff check, and git status check: passed.

Paper/denominator impact:
- reports changed: no
- results changed: no
- denominator changed: no
- paper results changed: no
- raw legacy evidence changed: no
- metrics implementation authorized: no
- reproduction interface implementation authorized: no

Next safe action:
- Review and approve evidence ledger field semantics plus adapter row-grain policy before implementing retained evidence adapters, metrics computation, a paper table renderer, unified reproduction CLI, or public runner output.

### 2026-05-16 · ac4e331 · Evidence ledger field semantics and adapter row-grain policy lock

Mode: release-repo ledger semantics and row-grain policy output; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Commit: `ac4e3311ec9a242042565ae69a12fc697e6f3a1d`
Push: `origin/main` updated `586991c..ac4e331`

Summary:
- Created draft policy specs for evidence ledger field semantics, adapter row grain, and record-type boundaries under `repository_spec/`.
- Defined seven draft ledger record types: `control_cell`, `rewrite_candidate_cell`, `plan_observability_artifact`, `portability_candidate_cell`, `verifier_support_pair`, `retained_summary_artifact`, and `user_run_candidate_cell`.
- Reviewed all 28 draft evidence ledger fields in `audits/ledger_semantics_row_grain_policy/ledger_field_semantics_review.csv`.
- Added concrete row-grain examples, denominator role boundary notes, adapter row-grain decisions, and open metric-finalization questions under `audits/ledger_semantics_row_grain_policy/`.
- Updated `project_control/MIGRATION_STATUS.md` to record the policy-only completion.
- Did not implement retained-evidence adapters, metrics computation, runner or reproduction CLI, scripts, source modules, report rendering, reports/results migration, DB validation, timing reruns, evidence regeneration, denominator updates, case membership changes, migrated case package changes, or raw legacy evidence changes.

Files created:
- `repository_spec/evidence_ledger_semantics_v1_draft.md`
- `repository_spec/adapter_row_grain_policy_v1_draft.md`
- `repository_spec/evidence_record_type_policy_v1_draft.md`
- `audits/ledger_semantics_row_grain_policy/ledger_row_grain_policy_summary.md`
- `audits/ledger_semantics_row_grain_policy/ledger_field_semantics_review.csv`
- `audits/ledger_semantics_row_grain_policy/record_type_examples.csv`
- `audits/ledger_semantics_row_grain_policy/denominator_role_boundary_notes.md`
- `audits/ledger_semantics_row_grain_policy/adapter_row_grain_decision_table.csv`
- `audits/ledger_semantics_row_grain_policy/open_questions_for_metric_finalization.md`
- `audits/ledger_semantics_row_grain_policy/ledger_semantics_row_grain_policy_summary.json`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- JSON parse, CSV row/coverage checks, git diff check, and git status check: passed.

Paper/denominator impact:
- reports changed: no
- results changed: no
- denominator changed: no
- paper results changed: no
- raw legacy evidence changed: no
- metrics implementation authorized: no
- adapter implementation authorized: no
- reproduction interface implementation authorized: no

Next safe action:
- Review and approve ledger semantics, record-type policy, adapter row-grain policy, and remaining metric-finalization questions before any retained-evidence adapter, metrics computation, paper renderer, reproduction CLI, or public runner implementation.

### 2026-05-17 · 8572983 · Metrics finalization decision packet for SQL-RewriteBench public workbench

Mode: release-repo metrics decision-packet output; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Commit: `857298304faa8a54201b13e76b6f6b7ed129ea48`
Push: `origin/main` updated `7ce3abf..8572983`

Summary:
- Created a maintainer/team-reviewable metrics decision packet under `audits/metrics_finalization_decision_packet/`.
- Reviewed 17 metric families across stable, clarification-needed, candidate-addition, candidate-change, support-only, and diagnostic roles.
- Organized denominator impact, performance metric options, observability options, parseability/runnable SQL options, failure bucket policy options, and a future metrics contract patch plan.
- Updated `project_control/MIGRATION_STATUS.md` to record that metrics implementation, retained-evidence adapter implementation, unified reproduction interface implementation, public runner implementation, and paper table rendering remain unauthorized.
- Did not implement metrics computation, retained-evidence adapters, runner or reproduction CLI, report rendering, scripts, source modules, reports/results migration, DB validation, LLM calls, timing workloads, evidence regeneration, denominator updates, case membership changes, migrated case package changes, paper table updates, or raw legacy evidence changes.

Files created:
- `audits/metrics_finalization_decision_packet/metrics_finalization_summary.md`
- `audits/metrics_finalization_decision_packet/metric_decision_table.csv`
- `audits/metrics_finalization_decision_packet/denominator_impact_matrix.csv`
- `audits/metrics_finalization_decision_packet/performance_metric_options.md`
- `audits/metrics_finalization_decision_packet/observability_metric_options.md`
- `audits/metrics_finalization_decision_packet/parseability_runnable_sql_options.md`
- `audits/metrics_finalization_decision_packet/failure_bucket_policy_options.md`
- `audits/metrics_finalization_decision_packet/proposed_metrics_contract_patch_plan.md`
- `audits/metrics_finalization_decision_packet/decisions_needed_before_implementation.md`
- `audits/metrics_finalization_decision_packet/metrics_finalization_decision_packet_summary.json`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- JSON parse, CSV decision-table checks, denominator matrix checks, git diff check, and git status check: passed.

Paper/denominator impact:
- reports changed: no
- results changed: no
- denominator changed: no
- paper results changed: no
- raw legacy evidence changed: no
- metrics implementation authorized: no
- adapter implementation authorized: no
- reproduction interface implementation authorized: no
- paper table rendering authorized: no

Next safe action:
- Maintainer/team review of the metric decision packet before implementing retained-evidence adapters, metrics computation, paper table rendering, a unified reproduction CLI, or public runner outputs.

### 2026-05-17 · bd56ca9 · Resolve metrics contract against updated paper scope

Mode: release-repo metrics contract alignment output; legacy untouched
Legacy repo modified: no
Release repo modified: yes
Commit: `bd56ca9372fa374ca40b84b549b60c17840e6b5e`
Push: `origin/main` updated `941bdef..bd56ca9`

Summary:
- Updated `repository_spec/metrics_contract_v1_draft.md` to align with the maintainer-provided updated paper metric scope.
- Created the metrics contract resolution audit under `audits/metrics_contract_resolution/`.
- Recorded the updated metric suite: Generation Rate, Execution Coverage Rate, Result Consistency Rate, Semantic Equivalence Rate, GM_Speedup, Speedup Ratio Percentiles, Attribution Coverage, Cross-Engine Execution, Cross-Engine Consistency, and Speedup Retention.
- Demoted or removed prior primary candidates: Candidate Failure Rate is diagnostic-only via failure buckets, Regression@20 is not primary, extraction/readiness variants are not primary Generation Rate variants, broad observability/PlanFrontier is folded into Attribution Coverage, and Support Layer is folded into correctness/verifier discussion.
- Did not implement metrics computation, retained-evidence adapters, runner or reproduction CLI, report rendering, scripts, source modules, reports/results migration, DB validation, timing workloads, evidence regeneration, denominator updates, case membership changes, migrated case package changes, paper table updates, or raw legacy evidence changes.

Files created:
- `audits/metrics_contract_resolution/metrics_contract_resolution_summary.md`
- `audits/metrics_contract_resolution/resolved_metric_contract_table.csv`
- `audits/metrics_contract_resolution/metric_name_change_log.csv`
- `audits/metrics_contract_resolution/deferred_or_not_computable_metrics.md`
- `audits/metrics_contract_resolution/metrics_contract_patch_notes.md`
- `audits/metrics_contract_resolution/metrics_contract_resolution_summary.json`

Files modified:
- `repository_spec/metrics_contract_v1_draft.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- JSON parse, CSV updated-metric checks, metric change-log checks, implementation-authorization checks, and git diff check: passed.

Paper/denominator impact:
- reports changed: no
- results changed: no
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no
- metrics implementation authorized: no
- adapter implementation authorized: no
- reproduction interface implementation authorized: no
- paper table rendering authorized: no

Next safe action:
- Maintainer/team review and approve the aligned metrics contract draft before implementing retained-evidence adapters, metrics computation, paper table rendering, a unified reproduction CLI, or public runner outputs.

### 2026-05-17 · f8f409f · Whole-case universe governance and non-common-core package readiness audit

Mode: release-repo governance/readiness audit output; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Commit: `f8f409fb6666f14c0e3d3d6f80a20cb8067d7467`
Push: `origin/main` updated `85dac0d..f8f409f`

Summary:
- Indexed the whole legacy case universe under `cases/PERF`, `cases/CONS`, `cases/PORT`, and `cases/LONGTAIL`.
- Detected 197 case-like directories with pool split PERF 105, CONS 40, PORT 28, LONGTAIL 24.
- Reconciled detected directories against the legacy 190-row registry: all 190 registered cases are present, and seven detected directories are not registered.
- Classified the 40 Common-core cases as `common_core_v0` and the 157 non-Common-core cases into staged, backlog, manual-review, and orphan/unregistered governance buckets.
- Created future prompts for staged/backlog membership planning and low-risk non-Common-core batch planning, both marked do-not-execute-now.
- Did not migrate cases, copy non-Common-core packages into the release repo, create staged/backlog membership files, update `case_sets/`, update reports/results, compute metrics, implement scripts, run DB engines, run validation scripts, run LLM calls, run timing workloads, change denominator values, change paper results, change case membership, delete/move `runs/`, or modify raw legacy evidence.

Files created:
- `audits/case_universe_governance/case_universe_governance_summary.md`
- `audits/case_universe_governance/case_universe_index.csv`
- `audits/case_universe_governance/registry_reconciliation_report.md`
- `audits/case_universe_governance/non_common_core_readiness_matrix.csv`
- `audits/case_universe_governance/staged_backlog_candidate_plan.md`
- `audits/case_universe_governance/non_common_core_risk_summary.md`
- `audits/case_universe_governance/post_release_batch_plan.md`
- `audits/case_universe_governance/case_universe_governance_summary.json`
- `audits/case_universe_governance/future_prompts/staged_backlog_membership_planning_prompt.md`
- `audits/case_universe_governance/future_prompts/non_common_core_low_risk_batch_planning_prompt.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- JSON parse, CSV row-count checks, Common-core count check, non-Common-core exclusion check, git diff check, and git status check: passed.

Paper/denominator impact:
- case_sets changed: no
- reports changed: no
- results changed: no
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Next safe action:
- Review the case universe governance audit, then run a separate staged/backlog membership planning task without changing Common-core v0 membership or denominator values.

### 2026-05-17 · 819e26b · Overnight governance and redevelopment investigation bundle

Mode: release-repo read-only governance/redevelopment investigation output; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Commit: `819e26bb5a2c6f12a1829112bc2f1df954468e91`
Push: `origin/main` updated `2212b8c..819e26b`

Summary:
- Refined staged/backlog planning labels for all 157 non-Common-core cases using prior case-universe governance outputs.
- Inspected the seven detected-but-unregistered legacy directories read-only and recorded registry/disposition recommendations.
- Inventoried 123 legacy script/tool files as redevelopment references, not copy-forward architecture.
- Audited 24 intended public release skeleton components and identified missing release/docs/spec/scripts/tests/report/result surfaces.
- Drafted future prompts for staged/backlog membership preview, script redevelopment detailed design, release skeleton bootstrap, and reports/results retained-evidence triage.
- Did not migrate cases, create official staged/backlog membership files, update `case_sets/`, update reports/results, implement scripts, create `src/`, compute metrics, render paper tables, run DB engines, run validation scripts, run LLM calls, run timing workloads, change denominator values, change paper results, change case membership, delete/move `runs/`, or modify raw legacy evidence.

Files created:
- `audits/overnight_investigation_bundle/overnight_investigation_summary.md`
- `audits/overnight_investigation_bundle/proposed_staged_backlog_membership_matrix.csv`
- `audits/overnight_investigation_bundle/unregistered_directory_reconciliation.csv`
- `audits/overnight_investigation_bundle/legacy_script_reference_inventory.csv`
- `audits/overnight_investigation_bundle/legacy_script_redevelopment_recommendation.md`
- `audits/overnight_investigation_bundle/public_release_skeleton_gap_audit.csv`
- `audits/overnight_investigation_bundle/public_release_skeleton_gap_summary.md`
- `audits/overnight_investigation_bundle/next_task_recommendation.md`
- `audits/overnight_investigation_bundle/overnight_investigation_summary.json`
- `audits/overnight_investigation_bundle/future_prompts/staged_backlog_official_membership_preview_prompt.md`
- `audits/overnight_investigation_bundle/future_prompts/legacy_script_redevelopment_detailed_design_prompt.md`
- `audits/overnight_investigation_bundle/future_prompts/public_release_skeleton_bootstrap_prompt.md`
- `audits/overnight_investigation_bundle/future_prompts/reports_results_retained_evidence_triage_prompt.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- JSON parse, CSV row-count checks, non-Common-core ID coverage check, local-path leakage check, git diff check, and git status check: passed.

Paper/denominator impact:
- case_sets changed: no
- reports changed: no
- results changed: no
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Next safe action:
- Review the overnight investigation bundle, then run a bounded benchmark_spec/docs public skeleton formalization task or staged/backlog official membership preview without migration, denominator changes, reports/results updates, metrics implementation, runner implementation, adapter implementation, or raw legacy evidence changes.

### 2026-05-17 · fd2380f · Staged/backlog membership preview for non-Common-core case universe

Mode: release-repo membership preview/governance planning output; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Commit: `fd2380f498320d8f74ee0bd359c2c7a5fae43911`
Push: `origin/main` updated `ccb79a9..fd2380f`

Summary:
- Created a human-reviewable staged/backlog membership preview for all 157 non-Common-core cases using the case-universe governance audit and overnight investigation bundle.
- Split preview rows into 61 proposed staged rows, 76 proposed backlog rows, and 20 manual-review/orphan rows.
- Forced all seven detected-but-unregistered directories into `orphan_or_unregistered_review` until registry reconciliation occurs.
- Created future prompt drafts for official staged/backlog case-set creation, staged low-risk batch migration planning, and manual-review/orphan reconciliation, all marked do-not-execute-now.
- Did not migrate cases, create official `case_sets/staged_v0/` or `case_sets/backlog_v0/`, modify `case_sets/common_core_v0/`, modify inventory, update reports/results, implement scripts, compute metrics, run DB engines, run validation scripts, run LLM calls, run timing workloads, change denominator values, change paper results, change case membership, delete/move `runs/`, or modify raw legacy evidence.

Files created:
- `audits/staged_backlog_membership_preview/staged_backlog_membership_preview_summary.md`
- `audits/staged_backlog_membership_preview/proposed_staged_v0_cases_preview.csv`
- `audits/staged_backlog_membership_preview/proposed_backlog_v0_cases_preview.csv`
- `audits/staged_backlog_membership_preview/manual_review_and_orphan_cases.csv`
- `audits/staged_backlog_membership_preview/staged_backlog_pool_summary.csv`
- `audits/staged_backlog_membership_preview/staged_backlog_membership_preview_checks.csv`
- `audits/staged_backlog_membership_preview/staged_backlog_membership_preview_notes.md`
- `audits/staged_backlog_membership_preview/future_official_membership_files_plan.md`
- `audits/staged_backlog_membership_preview/staged_backlog_membership_preview_summary.json`
- `audits/staged_backlog_membership_preview/future_prompts/create_official_staged_backlog_case_sets_prompt.md`
- `audits/staged_backlog_membership_preview/future_prompts/staged_low_risk_batch_migration_planning_prompt.md`
- `audits/staged_backlog_membership_preview/future_prompts/manual_review_orphan_reconciliation_prompt.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- JSON parse, CSV coverage checks, Common-core exclusion check, unregistered-directory inclusion check, staged/backlog directory absence check, future-prompt marker check, git diff check, and git status check: passed.

Paper/denominator impact:
- official case_sets/staged_v0 created: no
- official case_sets/backlog_v0 created: no
- case_sets changed: no
- reports changed: no
- results changed: no
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Next safe action:
- Maintainer review of staged/backlog preview criteria and unregistered-directory disposition before any official staged/backlog case-set creation, migration planning, denominator changes, reports/results updates, metrics implementation, runner implementation, adapter implementation, or raw legacy evidence changes.

### 2026-05-17 · 6699ccb · Public release clean-export strategy policy

Mode: release-repo policy/release-surface strategy output; legacy untouched
Legacy repo modified: no
Release repo modified: yes
Commit: `6699ccb12f3e7a743a6e8a652445cd0b2f9a4de7`
Push: `origin/main` updated `daa3962..6699ccb`

Summary:
- Added D017 to `project_control/DECISION_LOG.md`, recording that `Rewritebench_v0` is a release construction and migration work repository and that final public v0 should be produced by clean export branch or clean public release repository.
- Created `repository_spec/public_release_surface_policy_v1.md` defining file classification labels: `PUBLIC_FINAL`, `PUBLIC_SUPPORT`, `MAINTAINER_ARCHIVE`, `DROP_BEFORE_V0`, and `PRIVATE_ONLY`.
- Created a public release surface strategy audit with a summary, seed classification table, clean export release plan, and machine-readable summary JSON.
- Did not delete files, rewrite history, create a release branch, create a new public repository, remove audits, remove project-control files, migrate cases, update reports/results, update case sets, implement scripts/source, compute metrics, render paper tables, run DB engines, run LLM calls, run timing workloads, change denominator values, change paper results, change case membership, or modify raw legacy evidence.

Files created:
- `repository_spec/public_release_surface_policy_v1.md`
- `audits/public_release_surface_strategy/public_release_surface_strategy_summary.md`
- `audits/public_release_surface_strategy/public_release_surface_classification_seed.csv`
- `audits/public_release_surface_strategy/clean_export_release_plan.md`
- `audits/public_release_surface_strategy/public_release_surface_policy_summary.json`

Files modified:
- `project_control/DECISION_LOG.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- JSON parse, classification CSV read check, git diff check, and git status check: passed.

Paper/denominator impact:
- files deleted: no
- history rewritten: no
- release branch created: no
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Next safe action:
- Continue redevelopment in the construction repository; before public v0 tagging, run a separate clean-export surface classification and verification task without deleting construction files, rewriting history, creating a release branch, migrating cases, changing denominators, updating reports/results, or modifying raw legacy evidence.

### 2026-05-17 · e0a9907 · Formalize metrics contract v1 from approved paper scope

Mode: release-repo metrics contract formalization/spec output; legacy untouched
Legacy repo modified: no
Release repo modified: yes
Commit: `e0a9907a9f6fd809f3e6f361eb64412c7b42ce3d`
Push: `origin/main` updated `ced9879..e0a9907`

Summary:
- Formalized Metrics Contract v1 from the maintainer/team-approved paper scope in `repository_spec/metrics_contract_v1.md`.
- Marked `repository_spec/metrics_contract_v1_draft.md` as superseded by the formal contract.
- Added `repository_spec/explainability_attribution_policy_v1_draft.md` to define the Attribution Coverage boundary, support/pilot observability boundary, LLM annotation boundary, and no-speedup-without-runtime-evidence rule.
- Created a metrics contract formalization audit with the finalized metric table, formula/denominator table, rename/deprecation log, implementation authorization boundary, and machine-readable summary.
- Added D018 to `project_control/DECISION_LOG.md` because D017 is already used for the clean public release export strategy.
- Did not implement metrics, implement retained-evidence adapters, implement a reproduction CLI, implement public runner outputs, render paper tables, copy reports/results, run DB engines, run LLM calls, run timing workloads, change denominator values, change paper results, change case membership, update case sets, modify case packages, or modify raw legacy evidence.

Files created:
- `repository_spec/metrics_contract_v1.md`
- `repository_spec/explainability_attribution_policy_v1_draft.md`
- `audits/metrics_contract_formalization/metrics_contract_formalization_summary.md`
- `audits/metrics_contract_formalization/finalized_metric_table.csv`
- `audits/metrics_contract_formalization/metric_formula_and_denominator_table.csv`
- `audits/metrics_contract_formalization/metric_rename_and_deprecation_log.csv`
- `audits/metrics_contract_formalization/implementation_authorization_boundary.md`
- `audits/metrics_contract_formalization/metrics_contract_formalization_summary.json`

Files modified:
- `repository_spec/metrics_contract_v1_draft.md`
- `project_control/DECISION_LOG.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- JSON parse, finalized metric table coverage check, implementation-authorization false check, rename/deprecation coverage check, git diff check, and git status check: passed.

Paper/denominator impact:
- reports changed: no
- results changed: no
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Authorization:
- metrics implementation authorized: no
- retained-evidence adapter implementation authorized: no
- reproduction interface implementation authorized: no
- public runner implementation authorized: no
- paper table rendering authorized: no

Next safe action:
- Review Metrics Contract v1 and the attribution policy draft, then plan retained-evidence adapter design and validation gates without computing metrics, rendering paper tables, updating reports/results, changing denominators, or modifying raw legacy evidence.

### 2026-05-17 · 58d843f · Retained-evidence adapter design and validation plan

Mode: release-repo adapter design/spec and validation-plan output; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Commit: `58d843f91cf8a901565b868df812c65c20ef2ebd`
Push: `origin/main` updated `e932114..58d843f`

Summary:
- Created `repository_spec/retained_evidence_adapter_design_v1_draft.md` to define future retained-evidence adapter families, input sources, output ledger record types, row-grain rules, denominator joins, unsupported/N.A. handling, validation gates, implementation sequence, and boundaries against metrics computation and paper rendering.
- Created audit outputs under `audits/retained_evidence_adapter_design/` for adapter source groups, output row examples, validation gates, metric dependencies, unsupported/N.A. policy, implementation sequence, and machine-readable summary.
- Confirmed `project_control/MIGRATION_STATUS.md` was current relative to Metrics Contract v1 and did not require discrepancy reporting.
- Did not implement retained-evidence adapters, implement metrics computation, implement a reproduction CLI, implement public runner outputs, create scripts, create source package files, copy reports/results, render paper tables, run DB engines, run validation scripts, run LLM calls, run timing workloads, change denominator values, change paper results, change case membership, update case sets, modify case packages, or modify raw legacy evidence.

Files created:
- `repository_spec/retained_evidence_adapter_design_v1_draft.md`
- `audits/retained_evidence_adapter_design/retained_evidence_adapter_design_summary.md`
- `audits/retained_evidence_adapter_design/adapter_input_source_matrix.csv`
- `audits/retained_evidence_adapter_design/adapter_output_ledger_row_examples.csv`
- `audits/retained_evidence_adapter_design/adapter_validation_gate_plan.md`
- `audits/retained_evidence_adapter_design/metric_to_adapter_dependency_matrix.csv`
- `audits/retained_evidence_adapter_design/unsupported_or_na_policy.md`
- `audits/retained_evidence_adapter_design/implementation_sequence_plan.md`
- `audits/retained_evidence_adapter_design/retained_evidence_adapter_design_summary.json`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- JSON parse, adapter input source matrix row check, output row example coverage check, metric dependency coverage check, git diff check, and git status check: passed.

Paper/denominator impact:
- reports changed: no
- results changed: no
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Authorization:
- adapter implementation authorized: no
- metrics implementation authorized: no
- reproduction interface implementation authorized: no
- public runner implementation authorized: no
- paper table rendering authorized: no

Next safe action:
- Review the retained-evidence adapter design and validation plan, then formalize a ledger schema model and non-mutating validation fixtures without parsing production retained evidence into a metrics ledger, computing metrics, rendering paper tables, updating reports/results, changing denominators, or modifying raw legacy evidence.

### 2026-05-17 · 18df984 · Ledger schema model and non-mutating validation fixtures skeleton

Mode: release-repo ledger schema/fixture design output; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Commit: `18df9844c35877d26a4c71319d42cd6bd124c3c9`
Push: `origin/main` updated `5949fd0..18df984`

Summary:
- Created draft ledger column schema, validation rules, and fixture policy specs under `repository_spec/`.
- Created synthetic validation fixture outputs under `audits/ledger_schema_validation_fixtures/`.
- Fixture rows cover all seven record types: `control_cell`, `rewrite_candidate_cell`, `plan_observability_artifact`, `portability_candidate_cell`, `verifier_support_pair`, `retained_summary_artifact`, and `user_run_candidate_cell`.
- Included intentionally invalid fixture rows for missing candidate ID, forbidden timing fields on control/verifier rows, missing target engine, metric-eligible retained summary, and missing same-engine denominator ID.
- Did not parse production retained evidence, load the 3,439 retained candidates into a production ledger, implement adapters, implement metrics, implement a reproduction CLI, implement public runner outputs, create scripts, create source package files, copy reports/results, render paper tables, run DB engines, run validation scripts, run LLM calls, run timing workloads, change denominator values, change paper results, change case membership, update case sets, modify case packages, or modify raw legacy evidence.

Files created:
- `repository_spec/evidence_ledger_column_schema_v1_draft.md`
- `repository_spec/evidence_ledger_validation_rules_v1_draft.md`
- `repository_spec/evidence_ledger_fixture_policy_v1_draft.md`
- `audits/ledger_schema_validation_fixtures/ledger_schema_fixture_summary.md`
- `audits/ledger_schema_validation_fixtures/fixture_all_record_types.csv`
- `audits/ledger_schema_validation_fixtures/fixture_expected_validation_results.csv`
- `audits/ledger_schema_validation_fixtures/record_type_required_fields_matrix.csv`
- `audits/ledger_schema_validation_fixtures/allowed_status_values.csv`
- `audits/ledger_schema_validation_fixtures/fixture_denominator_join_examples.csv`
- `audits/ledger_schema_validation_fixtures/ledger_schema_validation_plan.md`
- `audits/ledger_schema_validation_fixtures/ledger_schema_validation_fixtures_summary.json`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- JSON parse, fixture row flag check, required record-type coverage check, required fixture example coverage check, valid/invalid expected-result coverage check, record-type required-field matrix coverage check, allowed-status coverage check, denominator-bearing record-type join example check, git diff check, and git status check: passed.

Paper/denominator impact:
- production retained evidence parsed: no
- reports changed: no
- results changed: no
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Authorization:
- adapter implementation authorized: no
- metrics implementation authorized: no
- reproduction interface implementation authorized: no
- public runner implementation authorized: no
- paper table rendering authorized: no

Next safe action:
- Review the ledger schema model and synthetic validation fixtures, then design or prototype a non-mutating validator that reads only synthetic fixtures without parsing production retained evidence, implementing adapters, computing metrics, rendering paper tables, updating reports/results, changing denominators, or modifying raw legacy evidence.

### 2026-05-17 · 9882090 · Ledger fixture validator skeleton

Mode: release-repo developer validator skeleton for synthetic fixtures only; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Commit: `9882090eb22c98acc193a850e382130e06f4a1fd`
Push: `origin/main` updated `715bc5c..9882090`

Summary:
- Created `scripts/dev/validate_ledger_fixtures.py`, a non-mutating developer validator that reads only synthetic ledger fixture CSVs and static Common-core denominator/control scaffolds.
- Generated fixture validation outputs under `audits/ledger_fixture_validator_skeleton/`.
- Checked required fields for materialized fixture columns, forbidden fields by record type, allowed status values, fixture safety flags, expected valid/invalid fixture outcomes, and denominator join examples.
- Did not parse production retained evidence, implement retained-evidence adapters, implement metrics computation, implement a reproduction CLI, implement public runner outputs, implement paper table rendering, copy reports/results, write case-local runs, run DB engines, run LLM calls, run timing workloads, change denominator values, change paper results, change case membership, modify case sets, modify migrated case packages, or modify raw legacy evidence.

Files created:
- `scripts/dev/validate_ledger_fixtures.py`
- `audits/ledger_fixture_validator_skeleton/ledger_fixture_validation_results.csv`
- `audits/ledger_fixture_validator_skeleton/ledger_fixture_validation_summary.json`
- `audits/ledger_fixture_validator_skeleton/ledger_fixture_validator_report.md`
- `audits/ledger_fixture_validator_skeleton/validator_limitations.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python -m py_compile scripts/dev/validate_ledger_fixtures.py`: passed.
- `python scripts/dev/validate_ledger_fixtures.py --fixtures-dir audits/ledger_schema_validation_fixtures --out-dir audits/ledger_fixture_validator_skeleton`: passed.
- JSON parse and CSV row checks: passed.
- `git diff --check`: passed.
- `git status -sb`: passed before commit.

Paper/denominator impact:
- production retained evidence parsed: no
- reports changed: no
- results changed: no
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Authorization:
- adapter implementation authorized: no
- metrics implementation authorized: no
- reproduction interface implementation authorized: no
- public runner implementation authorized: no
- paper table rendering authorized: no

Next safe action:
- Review the ledger fixture validator skeleton and decide whether to harden synthetic fixture validation or plan production ledger validation gates; do not parse production retained evidence, implement adapters, compute metrics, render paper tables, update reports/results, change denominators, or modify raw legacy evidence without separate authorization.

### 2026-05-17 · f7c613a · Ledger fixture validator hardening and dev-smoke documentation

Mode: release-repo developer validator hardening for synthetic fixtures only; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Commit: `f7c613a904e72a0dc624bb6e1ad0b9683a43545c`
Push: `origin/main` updated `432b217..f7c613a`

Summary:
- Hardened `scripts/dev/validate_ledger_fixtures.py` while preserving fixture-only scope.
- Added optional `--extra-fixtures` and `--extra-expected` inputs for synthetic hardening rows.
- Added duplicate ID checks, stricter safety-flag checks, status and obvious consistency checks, record-type identity checks, direct denominator scaffold joins, and hardening-specific output names.
- Created additional synthetic hardening fixtures and expected outcomes under `audits/ledger_fixture_validator_hardening/`.
- Generated hardening validation outputs and developer smoke documentation.
- Did not parse production retained evidence, read legacy reports/results/runs, implement retained-evidence adapters, implement metrics computation, implement a reproduction CLI, implement public runner outputs, implement paper table rendering, copy reports/results, write case-local runs, run DB engines, run LLM calls, run timing workloads, change denominator values, change paper results, change case membership, modify case sets, modify migrated case packages, or modify raw legacy evidence.

Files created:
- `audits/ledger_fixture_validator_hardening/fixture_hardening_extra_rows.csv`
- `audits/ledger_fixture_validator_hardening/fixture_hardening_expected_results.csv`
- `audits/ledger_fixture_validator_hardening/ledger_fixture_hardening_validation_results.csv`
- `audits/ledger_fixture_validator_hardening/ledger_fixture_hardening_summary.json`
- `audits/ledger_fixture_validator_hardening/ledger_fixture_validator_hardening_report.md`
- `audits/ledger_fixture_validator_hardening/validator_hardening_limitations.md`
- `audits/ledger_fixture_validator_hardening/dev_smoke_usage.md`

Files modified:
- `scripts/dev/validate_ledger_fixtures.py`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python -m py_compile scripts/dev/validate_ledger_fixtures.py`: passed.
- Base fixture validator run: passed.
- Base plus hardening fixture validator run: passed.
- JSON assertions and CSV row/count checks: passed.
- `git diff --check`: passed.
- `git status -sb`: passed before commit.

Hardening result:
- Base fixture rows checked: 20.
- Extra fixture rows checked: 18.
- Expected-valid rows passed: 17/17.
- Expected-invalid rows failed as expected: 21/21.
- Unexpected pass/fail count: 0/0.
- Denominator join examples: 14/14 passed.
- Duplicate record IDs detected as expected: 1.
- Safety flag failures detected as expected: 3.

Paper/denominator impact:
- production retained evidence parsed: no
- reports changed: no
- results changed: no
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Authorization:
- adapter implementation authorized: no
- metrics implementation authorized: no
- reproduction interface implementation authorized: no
- public runner implementation authorized: no
- paper table rendering authorized: no

Next safe action:
- Review the hardened fixture-only validator and dev-smoke documentation, then decide whether to add a developer-only smoke entrypoint or plan separately authorized production ledger validation gates; do not parse production retained evidence, implement adapters, compute metrics, render paper tables, update reports/results, change denominators, or modify raw legacy evidence without separate authorization.

### 2026-05-17 · b212c7a · Developer smoke entrypoint for ledger fixture validator

Mode: release-repo developer smoke entrypoint for synthetic fixtures only; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Commit: `b212c7a6a85bcd367b7f66ac0d4708c46fc6df2f`
Push: `origin/main` updated `6fcbeac..b212c7a`

Summary:
- Created `scripts/dev/smoke_ledger_fixtures.py`, a thin developer-only wrapper around `scripts/dev/validate_ledger_fixtures.py`.
- The wrapper defaults to the base synthetic fixture directory, hardening extra fixture rows, hardening expected results, and `audits/ledger_fixture_dev_smoke/` as its output directory.
- Created developer smoke documentation under `docs/dev/`.
- Generated developer smoke audit outputs under `audits/ledger_fixture_dev_smoke/`.
- Did not parse production retained evidence, read legacy reports/results/runs, implement retained-evidence adapters, implement metrics computation, implement a reproduction CLI, implement public runner outputs, implement paper table rendering, copy reports/results, write case-local runs, run DB engines, run LLM calls, run timing workloads, change denominator values, change paper results, change case membership, modify case sets, modify migrated case packages, or modify raw legacy evidence.

Files created:
- `scripts/dev/smoke_ledger_fixtures.py`
- `docs/dev/LEDGER_FIXTURE_SMOKE.md`
- `audits/ledger_fixture_dev_smoke/ledger_fixture_hardening_validation_results.csv`
- `audits/ledger_fixture_dev_smoke/ledger_fixture_hardening_summary.json`
- `audits/ledger_fixture_dev_smoke/ledger_fixture_validator_hardening_report.md`
- `audits/ledger_fixture_dev_smoke/ledger_fixture_dev_smoke_report.md`
- `audits/ledger_fixture_dev_smoke/ledger_fixture_dev_smoke_summary.json`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python -m py_compile scripts/dev/validate_ledger_fixtures.py`: passed.
- `python -m py_compile scripts/dev/smoke_ledger_fixtures.py`: passed.
- `python scripts/dev/smoke_ledger_fixtures.py`: passed.
- JSON assertions and output existence checks: passed.
- `git diff --check`: passed.
- `git status -sb`: passed before commit.

Smoke result:
- Fixture rows checked: 38.
- Expected-valid rows passed: 17/17.
- Expected-invalid rows failed as expected: 21/21.
- Unexpected pass/fail count: 0/0.
- Production retained evidence parsed: no.
- Metrics computed: no.
- Adapter implemented: no.

Paper/denominator impact:
- production retained evidence parsed: no
- reports changed: no
- results changed: no
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Authorization:
- adapter implementation authorized: no
- metrics implementation authorized: no
- reproduction interface implementation authorized: no
- public runner implementation authorized: no
- paper table rendering authorized: no

Next safe action:
- Review the developer-only smoke entrypoint and decide whether to add CI wiring for synthetic fixture validation or plan separately authorized production ledger validation gates; do not parse production retained evidence, implement adapters, compute metrics, render paper tables, update reports/results, change denominators, or modify raw legacy evidence without separate authorization.

### 2026-05-17 · 25d72ec · CI wiring for synthetic ledger fixture smoke validation

Mode: release-repo CI/dev-smoke wiring for synthetic fixtures only; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Commit: `25d72ece332c6808a0e43d0463bcefe78c29657b`
Push: `origin/main` updated `010ef3d..25d72ec`

Summary:
- Created `.github/workflows/ledger-fixture-smoke.yml`, a lightweight GitHub Actions workflow for synthetic ledger fixture smoke validation.
- Workflow runs `python -m py_compile scripts/dev/validate_ledger_fixtures.py`, `python -m py_compile scripts/dev/smoke_ledger_fixtures.py`, and `python scripts/dev/smoke_ledger_fixtures.py`.
- Workflow triggers on `pull_request`, `push`, and `workflow_dispatch`, uses `ubuntu-latest` with Python 3.11, and uploads synthetic smoke outputs as artifacts.
- Updated `docs/dev/LEDGER_FIXTURE_SMOKE.md` with a CI section.
- Created CI smoke audit outputs under `audits/ledger_fixture_ci_smoke/`.
- Did not parse production retained evidence, read legacy reports/results/runs, implement retained-evidence adapters, implement metrics computation, implement a reproduction CLI, implement public runner outputs, implement paper table rendering, copy reports/results, write case-local runs, run DB engines, run LLM calls, run timing workloads, change denominator values, change paper results, change case membership, modify case sets, modify migrated case packages, or modify raw legacy evidence.

Files created:
- `.github/workflows/ledger-fixture-smoke.yml`
- `audits/ledger_fixture_ci_smoke/ledger_fixture_ci_smoke_summary.md`
- `audits/ledger_fixture_ci_smoke/ledger_fixture_ci_smoke_checks.csv`
- `audits/ledger_fixture_ci_smoke/ledger_fixture_ci_smoke_summary.json`

Files modified:
- `docs/dev/LEDGER_FIXTURE_SMOKE.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python -m py_compile scripts/dev/validate_ledger_fixtures.py`: passed.
- `python -m py_compile scripts/dev/smoke_ledger_fixtures.py`: passed.
- `python scripts/dev/smoke_ledger_fixtures.py`: passed.
- `audits/ledger_fixture_ci_smoke/ledger_fixture_ci_smoke_summary.json` parse and invariant checks: passed.
- `git diff --check`: passed.
- `git status -sb`: passed before commit.

Smoke result:
- Fixture rows checked: 38.
- Expected-valid rows passed: 17/17.
- Expected-invalid rows failed as expected: 21/21.
- Unexpected pass/fail count: 0/0.
- Production retained evidence parsed: no.
- Metrics computed: no.
- Adapter implemented: no.

Paper/denominator impact:
- production retained evidence parsed: no
- reports changed: no
- results changed: no
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Authorization:
- adapter implementation authorized: no
- metrics implementation authorized: no
- reproduction interface implementation authorized: no
- public runner implementation authorized: no
- paper table rendering authorized: no

Next safe action:
- Monitor the ledger fixture smoke workflow on subsequent pushes and pull requests, then plan production ledger validation gates only if separately authorized; do not parse production retained evidence, implement adapters, compute metrics, render paper tables, update reports/results, change denominators, or modify raw legacy evidence without separate authorization.

### 2026-05-17 · 545ea93 · Production ledger validation gates planning

Mode: release-repo validation-gate planning/spec output; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Commit: `545ea93981402acd49be2217ed76eae4f29df3b7`
Push: `origin/main` updated `7096a85..545ea93`

Summary:
- Created `repository_spec/production_ledger_validation_policy_v1_draft.md`, a policy-only future production ledger validation gate plan.
- Created production-ledger validation gate audit outputs under `audits/production_ledger_validation_gates/`.
- Defined 24 proposed gates covering schema, record type, denominator, status/N.A., metric-readiness, public hygiene, mutation boundary, no-global-leaderboard, provenance, and CI-smoke checks.
- Covered all seven evidence ledger record types and all 10 Metrics Contract v1 primary metrics.
- Minimally updated `docs/dev/LEDGER_FIXTURE_SMOKE.md` to point from synthetic fixture smoke to the production gate policy.
- Did not parse production retained evidence, read legacy reports/results/runs as adapter inputs, implement a production ledger validator, implement retained-evidence adapters, implement metrics computation, implement a reproduction CLI, implement public runner outputs, implement paper table rendering, copy reports/results, write case-local runs, run DB engines, run LLM calls, run timing workloads, change denominator values, change paper results, change case membership, modify case sets, modify migrated case packages, or modify raw legacy evidence.

Files created:
- `repository_spec/production_ledger_validation_policy_v1_draft.md`
- `audits/production_ledger_validation_gates/production_ledger_validation_gates_summary.md`
- `audits/production_ledger_validation_gates/production_ledger_gate_matrix.csv`
- `audits/production_ledger_validation_gates/record_type_production_gate_matrix.csv`
- `audits/production_ledger_validation_gates/metric_readiness_gate_matrix.csv`
- `audits/production_ledger_validation_gates/production_ledger_validator_future_cli_design.md`
- `audits/production_ledger_validation_gates/production_ledger_validation_failure_policy.md`
- `audits/production_ledger_validation_gates/production_ledger_validation_gates_summary.json`

Files modified:
- `docs/dev/LEDGER_FIXTURE_SMOKE.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `audits/production_ledger_validation_gates/production_ledger_validation_gates_summary.json` parse and invariant checks: passed.
- CSV checks for gate families, record types, metric coverage, and `can_compute_without_gate=false`: passed.
- `python -m py_compile scripts/dev/validate_ledger_fixtures.py`: passed.
- `python -m py_compile scripts/dev/smoke_ledger_fixtures.py`: passed.
- `python scripts/dev/smoke_ledger_fixtures.py`: passed.
- `git diff --check`: passed.
- `git status -sb`: passed before commit.

Planning result:
- Gates defined: 24.
- Record types covered: 7.
- Metrics covered: 10.
- Production retained evidence parsed: no.
- Production ledger validator implemented: no.

Paper/denominator impact:
- reports changed: no
- results changed: no
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Authorization:
- production ledger validator implemented: no
- adapter implementation authorized: no
- metrics implementation authorized: no
- reproduction interface implementation authorized: no
- public runner implementation authorized: no
- paper table rendering authorized: no

Next safe action:
- Review and approve the production ledger validation gate policy before implementing any production ledger validator or retained-evidence adapter; do not parse production retained evidence, implement adapters, compute metrics, render paper tables, update reports/results, change denominators, or modify raw legacy evidence without separate authorization.

### 2026-05-17 · a231ad9 · retained_summary_adapter_v0

Mode: narrow low-risk adapter skeleton for release-repo summary artifacts only; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Commit: `a231ad95e705165744acc9b60f42a2fe93d09238`
Push: `origin/main` updated `257251b..a231ad9`

Summary:
- Created `scripts/dev/build_retained_summary_ledger.py`, a bounded retained-summary adapter skeleton.
- Adapter scope: `release_repo_summary_only`.
- Allowed emitted record type: `retained_summary_artifact` only.
- Generated `audits/retained_summary_adapter_v0/retained_summary_ledger_v0.csv` with 31 non-metric retained-summary rows.
- Generated adapter summary, checks, report, and limitations under `audits/retained_summary_adapter_v0/`.
- Added concise developer documentation at `docs/dev/RETAINED_SUMMARY_ADAPTER_V0.md`.
- Did not read the legacy repo, parse production retained evidence, parse legacy reports/results/runs, implement a general retained-evidence adapter, compute metrics, implement a reproduction CLI, implement public runner outputs, render paper tables, copy reports/results, create `results/retained`, create `reports/evaluation`, write case-local runs, run DB engines, run LLM calls, run timing workloads, change denominator values, change paper results, change case membership, modify case sets, modify migrated case packages, or modify raw legacy evidence.

Files created:
- `scripts/dev/build_retained_summary_ledger.py`
- `audits/retained_summary_adapter_v0/retained_summary_ledger_v0.csv`
- `audits/retained_summary_adapter_v0/retained_summary_adapter_v0_summary.json`
- `audits/retained_summary_adapter_v0/retained_summary_adapter_v0_report.md`
- `audits/retained_summary_adapter_v0/retained_summary_adapter_v0_checks.csv`
- `audits/retained_summary_adapter_v0/retained_summary_adapter_v0_limitations.md`
- `docs/dev/RETAINED_SUMMARY_ADAPTER_V0.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python -m py_compile scripts/dev/build_retained_summary_ledger.py`: passed.
- `python scripts/dev/build_retained_summary_ledger.py --out-dir audits/retained_summary_adapter_v0`: passed.
- `audits/retained_summary_adapter_v0/retained_summary_adapter_v0_summary.json` parse and invariant checks: passed.
- CSV checks for retained summary rows and adapter checks: passed.
- `python -m py_compile scripts/dev/validate_ledger_fixtures.py`: passed.
- `python -m py_compile scripts/dev/smoke_ledger_fixtures.py`: passed.
- `python scripts/dev/smoke_ledger_fixtures.py`: passed.
- `git diff --check`: passed.
- `git status -sb`: passed before commit.

Adapter result:
- Rows emitted: 31.
- Record types emitted: `retained_summary_artifact`.
- Optional inputs missing: 0.
- Production retained evidence parsed: no.
- Legacy repo read: no.
- Metrics computed: no.
- Metric input authorized: no.

Paper/denominator impact:
- reports changed: no
- results changed: no
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Authorization:
- general retained-evidence adapter implementation authorized: no
- metrics implementation authorized: no
- reproduction interface implementation authorized: no
- public runner implementation authorized: no
- paper table rendering authorized: no

Next safe action:
- Review the retained_summary_adapter_v0 output and production validation gates before authorizing any adapter that parses real retained evidence or emits metric-eligible rows; do not parse production retained evidence, implement general adapters, compute metrics, render paper tables, update reports/results, change denominators, or modify raw legacy evidence without separate authorization.

### 2026-05-17 · 2f231fa · Control-cell adapter v0 with production ledger validator skeleton

Mode: bounded implementation for a non-mutating production ledger validator skeleton and release-case-package-only `control_cell_adapter_v0`; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Commit: `2f231fa5f0156b28e8cd022b735375fffb9bee4a`
Push: `origin/main` updated `3212159..2f231fa`

Summary:
- Created `scripts/dev/validate_ledger_csv.py`, a non-mutating production ledger validator skeleton for ledger-style CSV files.
- Created `scripts/dev/build_control_cell_ledger.py`, a bounded `control_cell_adapter_v0` that reads only Common-core release case-package metadata and scaffolds.
- Generated `audits/control_cell_adapter_v0/control_cell_ledger_v0.csv` with 360 draft `control_cell` rows, matching `controls_360.csv`.
- Generated validator skeleton outputs under `audits/production_ledger_validator_skeleton/`.
- Validated the control-cell adapter output under `audits/control_cell_adapter_v0/ledger_validation/`.
- Added developer documentation at `docs/dev/CONTROL_CELL_ADAPTER_V0.md`.
- Did not read the legacy repo, parse production retained evidence, parse legacy reports/results/runs, implement general retained-evidence adapters, implement metrics computation, implement a reproduction CLI, implement public runner outputs, render paper tables, copy reports/results, create `results/retained`, create `reports/evaluation`, create an official production ledger under `results/`, write case-local runs, run DB engines, run LLM calls, run timing workloads, change denominator values, change paper results, change case membership, modify case sets, modify raw legacy evidence, or modify migrated case packages.

Files created:
- `scripts/dev/validate_ledger_csv.py`
- `scripts/dev/build_control_cell_ledger.py`
- `audits/production_ledger_validator_skeleton/ledger_validation_results.csv`
- `audits/production_ledger_validator_skeleton/ledger_validation_summary.json`
- `audits/production_ledger_validator_skeleton/ledger_validation_report.md`
- `audits/control_cell_adapter_v0/control_cell_ledger_v0.csv`
- `audits/control_cell_adapter_v0/control_cell_adapter_v0_summary.json`
- `audits/control_cell_adapter_v0/control_cell_adapter_v0_report.md`
- `audits/control_cell_adapter_v0/control_cell_adapter_v0_checks.csv`
- `audits/control_cell_adapter_v0/ledger_validation/ledger_validation_results.csv`
- `audits/control_cell_adapter_v0/ledger_validation/ledger_validation_summary.json`
- `audits/control_cell_adapter_v0/ledger_validation/ledger_validation_report.md`
- `docs/dev/CONTROL_CELL_ADAPTER_V0.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python -m py_compile scripts/dev/validate_ledger_csv.py`: passed.
- `python -m py_compile scripts/dev/build_control_cell_ledger.py`: passed.
- `python -m py_compile scripts/dev/validate_ledger_fixtures.py`: passed.
- `python -m py_compile scripts/dev/smoke_ledger_fixtures.py`: passed.
- `python scripts/dev/smoke_ledger_fixtures.py`: passed.
- `python scripts/dev/build_control_cell_ledger.py --case-set case_sets/common_core_v0/cases.csv --controls case_sets/common_core_v0/controls_360.csv --out-dir audits/control_cell_adapter_v0`: passed.
- `python scripts/dev/validate_ledger_csv.py --ledger audits/control_cell_adapter_v0/control_cell_ledger_v0.csv --case-set case_sets/common_core_v0/cases.csv --same-engine-denominator case_sets/common_core_v0/denominator_same_engine_120.csv --controls case_sets/common_core_v0/controls_360.csv --out-dir audits/control_cell_adapter_v0/ledger_validation`: passed.
- `python scripts/dev/validate_ledger_csv.py --ledger audits/control_cell_adapter_v0/control_cell_ledger_v0.csv --case-set case_sets/common_core_v0/cases.csv --same-engine-denominator case_sets/common_core_v0/denominator_same_engine_120.csv --controls case_sets/common_core_v0/controls_360.csv --out-dir audits/production_ledger_validator_skeleton`: passed.
- JSON invariant checks for adapter summary and ledger validation summary: passed.
- CSV checks for 360 `control_cell` rows and adapter checks: passed.
- `git diff --check`: passed.
- `git status -sb`: passed before commit.

Adapter result:
- Rows emitted: 360.
- Record types emitted: `control_cell`.
- `controls_360.csv` coverage: 360/360 planned rows.
- Control route counts: 120 source, 120 positive, 120 hard-negative.
- Adapter validation: passed, 360 rows checked, 0 errors, 0 warnings.
- Fixture smoke: passed, 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, 0 unexpected pass/fail rows.
- Production retained evidence parsed: no.
- Legacy repo read: no.
- Metrics computed: no.
- Metric input authorized: no.

Paper/denominator impact:
- reports changed: no
- results changed: no
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Authorization:
- general retained-evidence adapter implementation authorized: no
- metrics implementation authorized: no
- reproduction interface implementation authorized: no
- public runner implementation authorized: no
- paper table rendering authorized: no

Next safe action:
- Review control_cell_adapter_v0 coverage and validator output before authorizing any adapter that parses real retained evidence, emits metric-eligible rows, or consumes ledger rows for metrics; do not parse production retained evidence, implement general adapters, compute metrics, render paper tables, update reports/results, change denominators, or modify raw legacy evidence without separate authorization.

### 2026-05-17 · a04aa87 · hard_negative_control_detail_adapter_v0

Mode: bounded control-cell detail adapter for hard-negative controls only; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Commit: `a04aa8708f42f6b758e6fdeff721941ae3376f4f`
Push: `origin/main` updated `435122a..a04aa87`

Summary:
- Created `scripts/dev/build_hard_negative_control_detail_ledger.py`, a bounded hard-negative control detail adapter.
- Adapter scope: `release_case_package_only`.
- Allowed emitted record type: `control_cell` only.
- Allowed emitted control route: `hard_negative` only.
- Generated `audits/hard_negative_control_detail_adapter_v0/hard_negative_control_detail_ledger_v0.csv` with 120 hard-negative control detail rows, matching the hard-negative subset of `controls_360.csv`.
- Generated adapter summary, checks, report, limitations, and ledger-validator outputs under `audits/hard_negative_control_detail_adapter_v0/`.
- Added developer documentation at `docs/dev/HARD_NEGATIVE_CONTROL_DETAIL_ADAPTER_V0.md`.
- Did not read the legacy repo, parse production retained evidence, parse legacy reports/results/runs, parse release reports/results as production input, implement method candidate adapters, implement timing adapters, implement portability adapters, implement verifier support adapters, implement metrics computation, compute hard-negative rejection rate, compute false-accept rate, implement a reproduction CLI, implement public runner outputs, render paper tables, copy reports/results, create `results/retained`, create `reports/evaluation`, create an official production ledger under `results/`, write case-local runs, run DB engines, run LLM calls, run timing workloads, change denominator values, change paper results, change case membership, modify case sets, modify raw legacy evidence, or modify migrated case packages.

Files created:
- `scripts/dev/build_hard_negative_control_detail_ledger.py`
- `audits/hard_negative_control_detail_adapter_v0/hard_negative_control_detail_ledger_v0.csv`
- `audits/hard_negative_control_detail_adapter_v0/hard_negative_control_detail_adapter_v0_summary.json`
- `audits/hard_negative_control_detail_adapter_v0/hard_negative_control_detail_adapter_v0_report.md`
- `audits/hard_negative_control_detail_adapter_v0/hard_negative_control_detail_adapter_v0_checks.csv`
- `audits/hard_negative_control_detail_adapter_v0/hard_negative_control_detail_limitations.md`
- `audits/hard_negative_control_detail_adapter_v0/ledger_validation/ledger_validation_results.csv`
- `audits/hard_negative_control_detail_adapter_v0/ledger_validation/ledger_validation_summary.json`
- `audits/hard_negative_control_detail_adapter_v0/ledger_validation/ledger_validation_report.md`
- `docs/dev/HARD_NEGATIVE_CONTROL_DETAIL_ADAPTER_V0.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python -m py_compile scripts/dev/build_hard_negative_control_detail_ledger.py`: passed.
- `python -m py_compile scripts/dev/validate_ledger_csv.py`: passed.
- `python -m py_compile scripts/dev/build_control_cell_ledger.py`: passed.
- `python -m py_compile scripts/dev/validate_ledger_fixtures.py`: passed.
- `python -m py_compile scripts/dev/smoke_ledger_fixtures.py`: passed.
- `python scripts/dev/smoke_ledger_fixtures.py`: passed.
- `python scripts/dev/build_hard_negative_control_detail_ledger.py --case-set case_sets/common_core_v0/cases.csv --controls case_sets/common_core_v0/controls_360.csv --out-dir audits/hard_negative_control_detail_adapter_v0`: passed.
- `python scripts/dev/validate_ledger_csv.py --ledger audits/hard_negative_control_detail_adapter_v0/hard_negative_control_detail_ledger_v0.csv --case-set case_sets/common_core_v0/cases.csv --same-engine-denominator case_sets/common_core_v0/denominator_same_engine_120.csv --controls case_sets/common_core_v0/controls_360.csv --out-dir audits/hard_negative_control_detail_adapter_v0/ledger_validation`: passed.
- JSON invariant checks for adapter summary and ledger validation summary: passed.
- CSV checks for 120 hard-negative `control_cell` rows and adapter checks: passed.
- `git diff --check`: passed.
- `git status -sb`: passed before commit.

Adapter result:
- Rows emitted: 120.
- Record types emitted: `control_cell`.
- Control route emitted: `hard_negative`.
- Hard-negative scaffold coverage: 120/120 planned rows.
- Approval status counts: 45 `maintainer_approved_for_migration`, 72 `migration_planning_static_inference_needs_review_if_not_explicit_in_legacy`, 3 `manual_review_required`.
- Applicable status counts: 120 `planned_control`.
- Evidence-index status counts: 97 `indexed_not_recomputed`, 23 `evidence_not_retained`.
- Adapter validation: passed, 120 rows checked, 0 errors, 0 warnings.
- Fixture smoke: passed, 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, 0 unexpected pass/fail rows.
- Production retained evidence parsed: no.
- Legacy repo read: no.
- Metrics computed: no.
- False-accept-rate computed: no.
- Metric input authorized: no.

Paper/denominator impact:
- reports changed: no
- results changed: no
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Authorization:
- general retained-evidence adapter implementation authorized: no
- metrics implementation authorized: no
- reproduction interface implementation authorized: no
- public runner implementation authorized: no
- paper table rendering authorized: no

Next safe action:
- Review hard_negative_control_detail_adapter_v0 coverage and validator output before authorizing any adapter that parses real retained evidence, infers hard-negative outcomes, computes false-accept rates, emits metric-eligible rows, or consumes ledger rows for metrics; do not parse production retained evidence, implement general adapters, compute metrics, render paper tables, update reports/results, change denominators, or modify raw legacy evidence without separate authorization.

### 2026-05-17 · c74cde6 · source_positive_control_detail_adapter_v0

Mode: bounded control-cell detail adapter for source/positive controls only; legacy read-only
Legacy repo modified: no
Release repo modified: yes
Commit: `c74cde6fbd758607fc96e247d900cad87671ca46`
Push: `origin/main` updated `8663aca..c74cde6`

Summary:
- Created `scripts/dev/build_source_positive_control_detail_ledger.py`, a bounded source/positive control detail adapter.
- Adapter scope: `release_case_package_only`.
- Allowed emitted record type: `control_cell` only.
- Allowed emitted control routes: `source` and `positive` only.
- Generated `audits/source_positive_control_detail_adapter_v0/source_positive_control_detail_ledger_v0.csv` with 240 source/positive control detail rows, matching the source/positive subset of `controls_360.csv`.
- Generated adapter summary, checks, report, limitations, and ledger-validator outputs under `audits/source_positive_control_detail_adapter_v0/`.
- Added developer documentation at `docs/dev/SOURCE_POSITIVE_CONTROL_DETAIL_ADAPTER_V0.md`.
- Did not read the legacy repo, parse production retained evidence, parse legacy reports/results/runs, parse release reports/results as production input, implement method candidate adapters, implement timing adapters, implement portability adapters, implement verifier support adapters, implement metrics computation, compute source-positive pass rates, compute Result Consistency Rate, compute execution coverage, implement a reproduction CLI, implement public runner outputs, render paper tables, copy reports/results, create `results/retained`, create `reports/evaluation`, create an official production ledger under `results/`, write case-local runs, run DB engines, run LLM calls, run timing workloads, change denominator values, change paper results, change case membership, modify case sets, modify raw legacy evidence, or modify migrated case packages.

Files created:
- `scripts/dev/build_source_positive_control_detail_ledger.py`
- `audits/source_positive_control_detail_adapter_v0/source_positive_control_detail_ledger_v0.csv`
- `audits/source_positive_control_detail_adapter_v0/source_positive_control_detail_adapter_v0_summary.json`
- `audits/source_positive_control_detail_adapter_v0/source_positive_control_detail_adapter_v0_report.md`
- `audits/source_positive_control_detail_adapter_v0/source_positive_control_detail_adapter_v0_checks.csv`
- `audits/source_positive_control_detail_adapter_v0/source_positive_control_detail_limitations.md`
- `audits/source_positive_control_detail_adapter_v0/ledger_validation/ledger_validation_results.csv`
- `audits/source_positive_control_detail_adapter_v0/ledger_validation/ledger_validation_summary.json`
- `audits/source_positive_control_detail_adapter_v0/ledger_validation/ledger_validation_report.md`
- `docs/dev/SOURCE_POSITIVE_CONTROL_DETAIL_ADAPTER_V0.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python -m py_compile scripts/dev/build_source_positive_control_detail_ledger.py`: passed.
- `python -m py_compile scripts/dev/build_hard_negative_control_detail_ledger.py`: passed.
- `python -m py_compile scripts/dev/validate_ledger_csv.py`: passed.
- `python -m py_compile scripts/dev/build_control_cell_ledger.py`: passed.
- `python -m py_compile scripts/dev/validate_ledger_fixtures.py`: passed.
- `python -m py_compile scripts/dev/smoke_ledger_fixtures.py`: passed.
- `python scripts/dev/smoke_ledger_fixtures.py`: passed.
- `python scripts/dev/build_source_positive_control_detail_ledger.py --case-set case_sets/common_core_v0/cases.csv --controls case_sets/common_core_v0/controls_360.csv --out-dir audits/source_positive_control_detail_adapter_v0`: passed.
- `python scripts/dev/validate_ledger_csv.py --ledger audits/source_positive_control_detail_adapter_v0/source_positive_control_detail_ledger_v0.csv --case-set case_sets/common_core_v0/cases.csv --same-engine-denominator case_sets/common_core_v0/denominator_same_engine_120.csv --controls case_sets/common_core_v0/controls_360.csv --out-dir audits/source_positive_control_detail_adapter_v0/ledger_validation`: passed.
- JSON invariant checks for adapter summary and ledger validation summary: passed.
- CSV checks for 240 source/positive `control_cell` rows and adapter checks: passed.
- `git diff --check`: passed.
- `git status -sb`: passed before commit.

Adapter result:
- Rows emitted: 240.
- Record types emitted: `control_cell`.
- Control routes emitted: `source`, `positive`.
- Source/positive scaffold coverage: 240/240 planned rows.
- Route counts: 120 source, 120 positive.
- Applicable status counts: 240 `planned_control`.
- Evidence-index status counts: 179 `indexed_not_recomputed`, 61 `evidence_not_retained`.
- Adapter validation: passed, 240 rows checked, 0 errors, 0 warnings.
- Fixture smoke: passed, 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, 0 unexpected pass/fail rows.
- Production retained evidence parsed: no.
- Legacy repo read: no.
- Metrics computed: no.
- Source-positive rate computed: no.
- Result Consistency Rate computed: no.
- Metric input authorized: no.

Paper/denominator impact:
- reports changed: no
- results changed: no
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Authorization:
- general retained-evidence adapter implementation authorized: no
- metrics implementation authorized: no
- reproduction interface implementation authorized: no
- public runner implementation authorized: no
- paper table rendering authorized: no

Next safe action:
- Review source_positive_control_detail_adapter_v0 coverage and validator output before authorizing any adapter that parses real retained evidence, infers source-positive consistency outcomes, computes Result Consistency Rate, emits metric-eligible rows, or consumes ledger rows for metrics; do not parse production retained evidence, implement general adapters, compute metrics, render paper tables, update reports/results, change denominators, or modify raw legacy evidence without separate authorization.

### 2026-05-17 · b14e779 · Control-layer adapter closeout before candidate adapters

Mode: control-layer closeout / audit only; no adapter implementation; legacy not read
Legacy repo modified: no
Release repo modified: yes
Commit: `b14e779aa198a2c71e392d21646d216c3ac9cb90`
Push: `origin/main` updated `3b51474..b14e779`

Summary:
- Created `audits/control_layer_adapter_closeout/` with a control-layer adapter closeout summary, adapter matrix, route-level join check, evidence-index caveat table, closeout checks, machine-readable summary, and next-adapter recommendation.
- Reviewed `control_cell_adapter_v0`, `source_positive_control_detail_adapter_v0`, and `hard_negative_control_detail_adapter_v0`.
- Verified generic control scaffold coverage: 360/360 rows.
- Verified source/positive detail coverage: 240/240 rows.
- Verified hard-negative detail coverage: 120/120 rows.
- Verified combined detail coverage: 360/360 rows.
- Verified source, positive, and hard-negative route coverage: 120/120 each in both generic and detail layers.
- Confirmed all adapter ledger validations passed and fixture smoke still passes.
- Did not implement a new adapter, parse production retained evidence, read the legacy repo, compute metrics, compute false-accept rate, compute source-positive rate, compute Result Consistency Rate, update reports/results, change denominator values, change paper results, change case membership, or modify raw legacy evidence.

Files created:
- `audits/control_layer_adapter_closeout/control_layer_adapter_closeout_summary.md`
- `audits/control_layer_adapter_closeout/control_layer_adapter_closeout_matrix.csv`
- `audits/control_layer_adapter_closeout/control_layer_adapter_join_check.csv`
- `audits/control_layer_adapter_closeout/control_layer_evidence_index_caveats.csv`
- `audits/control_layer_adapter_closeout/control_layer_adapter_closeout_checks.csv`
- `audits/control_layer_adapter_closeout/control_layer_adapter_closeout_summary.json`
- `audits/control_layer_adapter_closeout/control_layer_next_adapter_recommendation.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python scripts/dev/smoke_ledger_fixtures.py`: passed.
- JSON invariant checks for `control_layer_adapter_closeout_summary.json`: passed.
- CSV checks for closeout matrix, join check, checks table, combined detail rows, and no metrics computed: passed.
- `git diff --check`: passed.
- `git status -sb`: passed before commit.

Closeout result:
- Generic control rows: 360.
- Source/positive detail rows: 240.
- Hard-negative detail rows: 120.
- Combined detail rows: 360.
- Route coverage: source 120/120, positive 120/120, hard-negative 120/120.
- Adapter validations: all passed.
- Fixture smoke: passed, 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, 0 unexpected pass/fail rows.
- Evidence-index caveats: source/positive detail has 179 `indexed_not_recomputed` and 61 `evidence_not_retained` rows; hard-negative detail has 97 `indexed_not_recomputed` and 23 `evidence_not_retained` rows; hard-negative approval status includes 45 `maintainer_approved_for_migration`, 72 `migration_planning_static_inference_needs_review_if_not_explicit_in_legacy`, and 3 `manual_review_required` rows.
- Production retained evidence parsed: no.
- Legacy repo read: no.
- Metrics computed: no.
- False-accept-rate computed: no.
- Source-positive rate computed: no.
- Result Consistency Rate computed: no.

Paper/denominator impact:
- reports changed: no
- results changed: no
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Authorization:
- general retained-evidence adapter implementation authorized: no
- metrics implementation authorized: no
- reproduction interface implementation authorized: no
- public runner implementation authorized: no
- paper table rendering authorized: no

Next safe action:
- Begin `rewrite_candidate_adapter_v0` planning only, or request explicit maintainer authorization for a bounded candidate adapter; do not parse production retained evidence, implement general candidate adapters, compute metrics, compute control rates, render paper tables, update reports/results, change denominators, or modify raw legacy evidence without separate authorization.

### 2026-05-17 · c9a7dd9 · rewrite_candidate_adapter_v0 Track-A scaffold

Mode: bounded rewrite-candidate scaffold; no production retained-evidence parsing; legacy not read
Legacy repo modified: no
Release repo modified: yes
Commit: `c9a7dd92a3c9b1e5731a8eb244fbb84fa90df756`
Push: `origin/main` updated `6b74bbe..c9a7dd9`

Summary:
- Updated `scripts/dev/validate_ledger_csv.py` with minimal validation support for `record_type=rewrite_candidate_cell`.
- Created `scripts/dev/build_rewrite_candidate_scaffold_ledger.py`, a bounded Track-A same-engine scaffold adapter.
- Adapter scope: `track_a_same_engine_scaffold_only`.
- Allowed emitted record type: `rewrite_candidate_cell` only.
- Generated `audits/rewrite_candidate_adapter_v0/rewrite_candidate_scaffold_ledger_v0.csv` with 600 planned candidate scaffold rows: 120 same-engine denominator rows x five authorized method routes.
- Generated method scope, summary, checks, report, limitations, and ledger-validator outputs under `audits/rewrite_candidate_adapter_v0/`.
- Added developer documentation at `docs/dev/REWRITE_CANDIDATE_ADAPTER_V0.md`.
- Did not read the legacy repo, parse production retained evidence, parse legacy reports/results/runs, parse release reports/results as production evidence, parse retained-evidence candidate maps as production input, parse method raw outputs, parse timing files, implement timing adapters, implement portability adapters, implement verifier support adapters, compute Generation Rate, compute Execution Coverage Rate, compute Result Consistency Rate, compute Semantic Equivalence Rate, compute GM_Speedup, compute Speedup Ratio Percentiles, compute Attribution Coverage, compute Cross-Engine metrics, implement a reproduction CLI, implement public runner outputs, render paper tables, copy reports/results, create `results/retained`, create `reports/evaluation`, create an official production ledger under `results/`, run DB engines, run LLM calls, run timing workloads, change denominator values, change paper results, change case membership, modify case sets, or modify raw legacy evidence.

Files created:
- `scripts/dev/build_rewrite_candidate_scaffold_ledger.py`
- `audits/rewrite_candidate_adapter_v0/rewrite_candidate_scaffold_ledger_v0.csv`
- `audits/rewrite_candidate_adapter_v0/rewrite_candidate_adapter_v0_method_scope.csv`
- `audits/rewrite_candidate_adapter_v0/rewrite_candidate_adapter_v0_summary.json`
- `audits/rewrite_candidate_adapter_v0/rewrite_candidate_adapter_v0_report.md`
- `audits/rewrite_candidate_adapter_v0/rewrite_candidate_adapter_v0_checks.csv`
- `audits/rewrite_candidate_adapter_v0/rewrite_candidate_adapter_v0_limitations.md`
- `audits/rewrite_candidate_adapter_v0/ledger_validation/ledger_validation_results.csv`
- `audits/rewrite_candidate_adapter_v0/ledger_validation/ledger_validation_summary.json`
- `audits/rewrite_candidate_adapter_v0/ledger_validation/ledger_validation_report.md`
- `docs/dev/REWRITE_CANDIDATE_ADAPTER_V0.md`

Files modified:
- `scripts/dev/validate_ledger_csv.py`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python -m py_compile scripts/dev/build_rewrite_candidate_scaffold_ledger.py`: passed.
- `python -m py_compile scripts/dev/validate_ledger_csv.py`: passed.
- `python -m py_compile scripts/dev/build_control_cell_ledger.py`: passed.
- `python -m py_compile scripts/dev/build_source_positive_control_detail_ledger.py`: passed.
- `python -m py_compile scripts/dev/build_hard_negative_control_detail_ledger.py`: passed.
- `python -m py_compile scripts/dev/validate_ledger_fixtures.py`: passed.
- `python -m py_compile scripts/dev/smoke_ledger_fixtures.py`: passed.
- `python scripts/dev/smoke_ledger_fixtures.py`: passed.
- `python scripts/dev/build_rewrite_candidate_scaffold_ledger.py --case-set case_sets/common_core_v0/cases.csv --denominator case_sets/common_core_v0/denominator_same_engine_120.csv --out-dir audits/rewrite_candidate_adapter_v0`: passed.
- `python scripts/dev/validate_ledger_csv.py --ledger audits/rewrite_candidate_adapter_v0/rewrite_candidate_scaffold_ledger_v0.csv --case-set case_sets/common_core_v0/cases.csv --same-engine-denominator case_sets/common_core_v0/denominator_same_engine_120.csv --controls case_sets/common_core_v0/controls_360.csv --out-dir audits/rewrite_candidate_adapter_v0/ledger_validation`: passed.
- JSON invariant checks for adapter summary and ledger validation summary: passed.
- CSV checks for 600 `rewrite_candidate_cell` rows and adapter checks: passed.
- `git diff --check`: passed.
- `git status -sb`: passed before commit.

Adapter result:
- Rows emitted: 600.
- Record types emitted: `rewrite_candidate_cell`.
- Same-engine denominator coverage: 120/120 denominator rows crossed with five method routes.
- Method routes emitted: `direct_llm_original`, `direct_llm_repair_1`, `sqlglot_optimize`, `sqlglot_noop`, `calcite_hep_fail_closed`.
- Adapter validation: passed, 600 rows checked, 0 errors, 0 warnings.
- Fixture smoke: passed, 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, 0 unexpected pass/fail rows.
- Production retained evidence parsed: no.
- Legacy repo read: no.
- Metrics computed: no.
- Generation Rate computed: no.
- Execution Coverage Rate computed: no.
- Result Consistency Rate computed: no.
- Timing metrics computed: no.
- Metric input authorized: no.

Paper/denominator impact:
- reports changed: no
- results changed: no
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Authorization:
- general retained-evidence adapter implementation authorized: no
- metrics implementation authorized: no
- reproduction interface implementation authorized: no
- public runner implementation authorized: no
- paper table rendering authorized: no

Next safe action:
- Review the `rewrite_candidate_adapter_v0` scaffold row grain and method scope before authorizing any candidate evidence adapter that parses retained method outputs, fills generated/executed/exact/timed statuses, authorizes metric input, or computes metrics; do not parse production retained evidence, implement general candidate adapters, compute metrics, render paper tables, update reports/results, change denominators, or modify raw legacy evidence without separate authorization.

### 2026-05-17 · fae0fca · Candidate evidence input-surface audit for rewrite_candidate_adapter_v1

Mode: input-surface audit / planning only; no adapter implementation; no production retained-evidence parsing; legacy not read
Legacy repo modified: no
Release repo modified: yes
Commit: `fae0fca38d6b9ce92f5768e654918cb5a82bad94`
Push: `origin/main` updated `79dac2b..fae0fca`

Summary:
- Created `audits/rewrite_candidate_input_surface_audit/` with a candidate input-surface summary, method/field-group matrix, route input-surface matrix, field-readiness matrix, risk register, future prompt, and machine-readable summary.
- Confirmed `rewrite_candidate_adapter_v0` scaffold exists and is validated: 600 planned `rewrite_candidate_cell` rows, 5 method routes, saved ledger validation passed with 600 rows checked, 0 errors, and 0 warnings.
- Reviewed five Track-A methods: `direct_llm_original`, `direct_llm_repair_1`, `sqlglot_optimize`, `sqlglot_noop`, and `calcite_hep_fail_closed`.
- Classified safe release-repo inputs as scaffold, denominator, inventory, specs, and audit metadata only.
- Classified generated, ready, executed, exact, timing, plan, and retained artifact fields as requiring later bounded adapters or remaining `N.A.` / `evidence_not_adapted_yet`.
- Recommended a separately authorized non-timing `candidate_status_adapter_v0` as the safest next bounded adapter.
- Did not implement candidate adapters, fill candidate statuses, parse production retained evidence, read the legacy repo, parse legacy reports/results/runs, parse timing files, compute metrics, render paper tables, update reports/results, change denominators, change paper results, change case membership, or modify raw legacy evidence.

Files created:
- `audits/rewrite_candidate_input_surface_audit/rewrite_candidate_input_surface_summary.md`
- `audits/rewrite_candidate_input_surface_audit/rewrite_candidate_input_surface_matrix.csv`
- `audits/rewrite_candidate_input_surface_audit/rewrite_candidate_route_input_surface.csv`
- `audits/rewrite_candidate_input_surface_audit/candidate_field_readiness_matrix.csv`
- `audits/rewrite_candidate_input_surface_audit/candidate_adapter_risk_register.md`
- `audits/rewrite_candidate_input_surface_audit/candidate_status_adapter_v0_future_prompt.md`
- `audits/rewrite_candidate_input_surface_audit/rewrite_candidate_input_surface_summary.json`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python scripts/dev/smoke_ledger_fixtures.py`: passed; 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, and 0 unexpected pass/fail rows.
- JSON invariant checks for `rewrite_candidate_input_surface_summary.json`: passed.
- CSV checks for five methods, exactly five included route rows, required field-readiness rows, and no `metrics_computed=true` rows: passed.
- `git diff --check`: passed.
- `git status -sb`: passed before commit with only intended audit/project-control changes.

Audit result:
- rewrite_candidate_adapter_v0 scaffold confirmed: yes.
- Candidate statuses filled: no.
- Production retained evidence parsed: no.
- Legacy repo read: no.
- Metrics computed: no.
- Generation Rate computed: no.
- Execution Coverage Rate computed: no.
- Result Consistency Rate computed: no.
- Timing metrics computed: no.

Paper/denominator impact:
- reports changed: no
- results changed: no
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Authorization:
- general retained-evidence adapter implementation authorized: no
- metrics implementation authorized: no
- reproduction interface implementation authorized: no
- public runner implementation authorized: no
- paper table rendering authorized: no

Next safe action:
- Request explicit maintainer authorization for a bounded `candidate_status_adapter_v0` that fills only non-timing, non-metric candidate status fields from approved release-repo summaries when row grain is unambiguous; otherwise keep candidate fields `N.A.` or `evidence_not_adapted_yet`. Do not parse legacy raw evidence, read legacy reports/results/runs, compute metrics, authorize metric input, render paper tables, update reports/results, change denominators, or modify raw legacy evidence.

### 2026-05-17 · 7e8dbc7 · candidate_status_adapter_v0 release-summary-only non-timing overlay

Mode: bounded rewrite-candidate status overlay; release-summary-only; no production retained-evidence parsing; legacy not read
Legacy repo modified: no
Release repo modified: yes
Commit: `7e8dbc74cf9fa6eeaa71c67d073711432017529c`
Push: `origin/main` updated `c22c2be..7e8dbc7`

Summary:
- Created `scripts/dev/build_candidate_status_ledger.py`, a bounded release-summary-only non-timing overlay adapter for the existing 600-row Track-A same-engine rewrite candidate scaffold.
- Created `audits/candidate_status_adapter_v0/` with a 600-row `rewrite_candidate_cell` overlay ledger, summary, report, checks, limitations, input-use log, and ledger-validator outputs.
- Created developer documentation at `docs/dev/CANDIDATE_STATUS_ADAPTER_V0.md`.
- Read only the existing scaffold and allowed release-repo audit metadata inputs.
- Did not open legacy paths referenced inside release audit CSVs.
- Emitted 600 rows, preserving the five scaffold method routes: `direct_llm_original`, `direct_llm_repair_1`, `sqlglot_optimize`, `sqlglot_noop`, and `calcite_hep_fail_closed`.
- Filled 0 row-level candidate statuses because no exact case_id x engine x rewrite_method release evidence was available from the allowed metadata.
- Marked 600 rows unresolved with `result_status=evidence_not_adapted_yet`, `metric_input_authorized=false`, and `metrics_computed=false`.
- Detected route-level summary metadata for 600 rows and did not distribute route-level counts/statuses into row-level statuses.
- Did not parse production retained evidence, read the legacy repo, parse legacy reports/results/runs, parse method raw outputs, parse timing files, implement timing adapters, implement portability adapters, implement verifier support adapters, compute Generation Rate, compute Execution Coverage Rate, compute Result Consistency Rate, compute Semantic Equivalence Rate, compute GM_Speedup, compute Speedup Ratio Percentiles, compute Attribution Coverage, compute Cross-Engine metrics, render paper tables, implement a reproduction CLI, copy reports/results, create `results/retained`, create `reports/evaluation`, update denominators, change paper results, change case membership, or modify raw legacy evidence.

Files created:
- `scripts/dev/build_candidate_status_ledger.py`
- `audits/candidate_status_adapter_v0/candidate_status_ledger_v0.csv`
- `audits/candidate_status_adapter_v0/candidate_status_adapter_v0_summary.json`
- `audits/candidate_status_adapter_v0/candidate_status_adapter_v0_report.md`
- `audits/candidate_status_adapter_v0/candidate_status_adapter_v0_checks.csv`
- `audits/candidate_status_adapter_v0/candidate_status_adapter_v0_limitations.md`
- `audits/candidate_status_adapter_v0/candidate_status_input_use_log.csv`
- `audits/candidate_status_adapter_v0/ledger_validation/ledger_validation_results.csv`
- `audits/candidate_status_adapter_v0/ledger_validation/ledger_validation_summary.json`
- `audits/candidate_status_adapter_v0/ledger_validation/ledger_validation_report.md`
- `docs/dev/CANDIDATE_STATUS_ADAPTER_V0.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python -m py_compile scripts/dev/build_candidate_status_ledger.py`: passed.
- `python -m py_compile scripts/dev/build_rewrite_candidate_scaffold_ledger.py`: passed.
- `python -m py_compile scripts/dev/validate_ledger_csv.py`: passed.
- `python -m py_compile scripts/dev/smoke_ledger_fixtures.py`: passed.
- `python scripts/dev/smoke_ledger_fixtures.py`: passed; 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, and 0 unexpected pass/fail rows.
- `python scripts/dev/build_candidate_status_ledger.py --scaffold audits/rewrite_candidate_adapter_v0/rewrite_candidate_scaffold_ledger_v0.csv --out-dir audits/candidate_status_adapter_v0`: passed.
- `python scripts/dev/validate_ledger_csv.py --ledger audits/candidate_status_adapter_v0/candidate_status_ledger_v0.csv --case-set case_sets/common_core_v0/cases.csv --same-engine-denominator case_sets/common_core_v0/denominator_same_engine_120.csv --controls case_sets/common_core_v0/controls_360.csv --out-dir audits/candidate_status_adapter_v0/ledger_validation`: passed, 600 rows checked, 0 errors, 0 warnings.
- JSON invariant checks for adapter summary and ledger validation summary: passed.
- CSV checks for 600 `rewrite_candidate_cell` rows, false safety flags, no timing/speedup values, adapter checks, and validation pass status: passed.
- `git diff --check`: passed.
- `git status -sb`: passed before commit with only intended candidate-status adapter, audit, docs, and project-control changes.

Adapter result:
- Rows emitted: 600.
- Record types emitted: `rewrite_candidate_cell`.
- Row-level status rows filled: 0.
- Unresolved status rows: 600.
- Status fill levels: 600 `release_summary_route_level_only`.
- Input-use log: 10 release metadata files inspected; 0 row-level evidence files found; 4 route-level/group-level metadata files found; `legacy_paths_opened=false` for every row.
- Adapter validation: passed, 600 rows checked, 0 errors, 0 warnings.
- Fixture smoke: passed, 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, 0 unexpected pass/fail rows.
- Production retained evidence parsed: no.
- Legacy repo read: no.
- Metrics computed: no.
- Generation Rate computed: no.
- Execution Coverage Rate computed: no.
- Result Consistency Rate computed: no.
- Timing metrics computed: no.
- Metric input authorized: no.

Paper/denominator impact:
- reports changed: no
- results changed: no
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Authorization:
- general retained-evidence adapter implementation authorized: no
- metrics implementation authorized: no
- reproduction interface implementation authorized: no
- public runner implementation authorized: no
- paper table rendering authorized: no

Next safe action:
- Review `candidate_status_adapter_v0` unresolved overlay rows and input-use log before authorizing any production retained-evidence candidate adapter. Do not parse legacy/raw evidence, fill timing fields, authorize metric input, compute metrics, render paper tables, update reports/results, change denominators, or modify raw legacy evidence without separate authorization.

### 2026-05-17 · a784923 · Candidate retained-evidence parser approval packet

Mode: release-repo audit/design/approval-packet only; no production retained-evidence parsing; legacy not read
Legacy repo modified: no
Release repo modified: yes
Commit: `a78492364b463b5d9c6edec041b025577ac0f4e1`
Push: `origin/main` updated `adf2ba7..a784923`

Summary:
- Created `audits/candidate_retained_evidence_parser_approval_packet/` with an approval summary, unresolved-overlay review, input-use review, candidate field/source plan, route risk matrix, proposed parser scope, validation-gate checklist, and maintainer decision template.
- Reviewed `candidate_status_adapter_v0` unresolved overlay outputs, `rewrite_candidate_input_surface_audit`, `rewrite_candidate_adapter_v0`, retained-evidence adapter design, ledger schema/validation rules, production ledger validation policy, and Metrics Contract v1.
- Confirmed the existing overlay remains unresolved: 600 planned `rewrite_candidate_cell` rows, 600 unresolved rows, five Track-A routes, 0 row-level statuses filled, `result_status=evidence_not_adapted_yet`, and `metric_input_authorized=false`.
- Confirmed the v0 input-use log inspected release-repo metadata only, found no row-level candidate evidence, did not open legacy paths, and did not parse production retained evidence.
- Defined a proposed future non-timing parser scope that must remain separate from timing parsing, metric computation, paper rendering, and production ledger promotion.
- Did not implement a parser, parse production retained evidence, read the legacy repo, fill candidate row statuses, fill timing fields, authorize metric input, compute metrics, update reports/results, change denominators, change paper results, change case membership, or modify raw legacy evidence.

Files created:
- `audits/candidate_retained_evidence_parser_approval_packet/approval_packet_summary.md`
- `audits/candidate_retained_evidence_parser_approval_packet/unresolved_overlay_review.csv`
- `audits/candidate_retained_evidence_parser_approval_packet/input_use_log_review.csv`
- `audits/candidate_retained_evidence_parser_approval_packet/candidate_field_to_source_plan.csv`
- `audits/candidate_retained_evidence_parser_approval_packet/route_risk_matrix.csv`
- `audits/candidate_retained_evidence_parser_approval_packet/proposed_candidate_status_parser_scope_v1.md`
- `audits/candidate_retained_evidence_parser_approval_packet/validation_gate_checklist.csv`
- `audits/candidate_retained_evidence_parser_approval_packet/approval_decision_template.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- CSV readability checks for all five new CSV audit files: passed.
- Markdown sanity checks for the three new Markdown decision/scope/summary files: passed.
- `git diff --check`: passed.
- `git status -sb`: passed before commit with only intended approval-packet and project-control changes.
- `git diff --name-status`: passed before commit with only intended approval-packet and project-control changes.

Audit result:
- Production retained evidence parsed: no.
- Legacy repo read: no.
- Candidate row statuses filled: no.
- Timing fields filled: no.
- Metrics computed: no.
- Metric input authorized: no.

Paper/denominator impact:
- reports changed: no
- results changed: no
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Authorization:
- candidate retained-evidence parser implementation authorized: no
- timing parser authorized: no
- metric input authorization changed: no
- metrics implementation authorized: no
- reproduction interface implementation authorized: no
- public runner implementation authorized: no
- paper table rendering authorized: no

Next safe action:
- Maintainer should review `audits/candidate_retained_evidence_parser_approval_packet/approval_decision_template.md` and choose design-only approval, bounded non-timing parser implementation approval, deferral pending metric/team review, or rejection due to evidence ambiguity. If implementation is approved, require an explicit input manifest and validation gates; do not fill timing fields, authorize metric input, compute metrics, render paper tables, update reports/results, change denominators, change paper results, or modify raw legacy evidence without separate authorization.

### 2026-05-17 · 6988b52 · candidate_status_parser_v0 manifest-first bounded non-timing parser

Mode: bounded non-timing candidate status parser; manifest-first; fail-closed; no timing fields; no metrics
Legacy repo modified: no
Release repo modified: yes
Commit: `6988b5202446c62338e6091de4504971f91678c1`
Push: `origin/main` updated `baa1bfb..6988b52`

Summary:
- Created `scripts/dev/build_candidate_status_parser_input_manifest.py`, a release-metadata-only manifest builder for candidate status parser inputs.
- Created `scripts/dev/parse_candidate_status_from_manifest.py`, a manifest-first non-timing parser for the 600-row Track-A same-engine rewrite candidate scaffold.
- Created `audits/candidate_status_parser_v0/` with a header-only approved input manifest, manifest summary/report/checks, 600-row parsed ledger output, parser summary/report/checks, input rejection log, limitations, and ledger validation outputs.
- Created `docs/dev/CANDIDATE_STATUS_PARSER_V0.md`.
- Inspected release-repo locator/mapping metadata only for manifest generation; no legacy files were opened.
- Approved manifest inputs: 0.
- Parser behavior: fail-closed/no-op; emitted 600 unresolved `rewrite_candidate_cell` rows with `parser_status=no_approved_row_level_inputs`.
- Row-level candidate statuses filled: no, count 0.
- Timing fields filled: no.
- Metric input authorized: no, count 0.
- Metrics computed: no.
- Did not parse production retained evidence, read the legacy repo, copy legacy reports/results/runs, parse raw logs, parse timing arrays, implement timing/portability/verifier adapters, render paper tables, implement reproduction CLI/public runner, update reports/results, change denominators, change paper results, change case membership, or modify raw legacy evidence.

Files created:
- `scripts/dev/build_candidate_status_parser_input_manifest.py`
- `scripts/dev/parse_candidate_status_from_manifest.py`
- `audits/candidate_status_parser_v0/candidate_status_parser_input_manifest.csv`
- `audits/candidate_status_parser_v0/candidate_status_parser_input_manifest_summary.json`
- `audits/candidate_status_parser_v0/candidate_status_parser_input_manifest_report.md`
- `audits/candidate_status_parser_v0/candidate_status_parser_input_manifest_checks.csv`
- `audits/candidate_status_parser_v0/candidate_status_parsed_ledger_v0.csv`
- `audits/candidate_status_parser_v0/candidate_status_parser_v0_summary.json`
- `audits/candidate_status_parser_v0/candidate_status_parser_v0_report.md`
- `audits/candidate_status_parser_v0/candidate_status_parser_v0_checks.csv`
- `audits/candidate_status_parser_v0/candidate_status_parser_input_rejection_log.csv`
- `audits/candidate_status_parser_v0/candidate_status_parser_v0_limitations.md`
- `audits/candidate_status_parser_v0/ledger_validation/ledger_validation_results.csv`
- `audits/candidate_status_parser_v0/ledger_validation/ledger_validation_summary.json`
- `audits/candidate_status_parser_v0/ledger_validation/ledger_validation_report.md`
- `docs/dev/CANDIDATE_STATUS_PARSER_V0.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python -m py_compile scripts/dev/build_candidate_status_parser_input_manifest.py`: passed.
- `python -m py_compile scripts/dev/parse_candidate_status_from_manifest.py`: passed.
- `python -m py_compile scripts/dev/validate_ledger_csv.py`: passed.
- `python -m py_compile scripts/dev/smoke_ledger_fixtures.py`: passed.
- `python scripts/dev/smoke_ledger_fixtures.py`: passed; 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, and 0 unexpected pass/fail rows.
- `python scripts/dev/build_candidate_status_parser_input_manifest.py --out-dir audits/candidate_status_parser_v0`: passed; manifest rows 0, approved parser inputs 0, rejected/deferred metadata candidates 9865.
- `python scripts/dev/parse_candidate_status_from_manifest.py --scaffold audits/rewrite_candidate_adapter_v0/rewrite_candidate_scaffold_ledger_v0.csv --manifest audits/candidate_status_parser_v0/candidate_status_parser_input_manifest.csv --out-dir audits/candidate_status_parser_v0`: passed; 600 rows emitted, 0 row-level statuses filled, 600 unresolved rows.
- `python scripts/dev/validate_ledger_csv.py --ledger audits/candidate_status_parser_v0/candidate_status_parsed_ledger_v0.csv --case-set case_sets/common_core_v0/cases.csv --same-engine-denominator case_sets/common_core_v0/denominator_same_engine_120.csv --controls case_sets/common_core_v0/controls_360.csv --out-dir audits/candidate_status_parser_v0/ledger_validation`: passed; 600 rows checked, 0 errors, 0 warnings.
- JSON invariant checks for manifest summary, parser summary, and ledger validation summary: passed.
- CSV checks for manifest header, 600 parser output rows, `rewrite_candidate_cell` record type, false metric/safety flags, no numeric timing/speedup fields, fail-closed parser status, and ledger validation pass status: passed.
- `git diff --check`: passed.
- `git status -sb`: passed before commit with only intended parser, audit, docs, and project-control changes.
- `git diff --stat`: passed before commit.

Parser result:
- candidate_status_parser_v0 implemented: yes.
- Input manifest created: yes.
- Approved manifest inputs: 0.
- Production retained evidence parsed: no.
- Legacy repo read: no.
- Row-level statuses filled: 0.
- Unresolved rows: 600.
- Timing fields filled: no.
- Metric-input-authorized rows: 0.
- Metrics computed: no.
- Generation Rate computed: no.
- Execution Coverage Rate computed: no.
- Result Consistency Rate computed: no.
- Timing metrics computed: no.
- Parser status summary: `no_approved_row_level_inputs=600`.
- Rejected/deferred input summary: 9865 metadata candidates deferred by the manifest builder; no manifest rows were approved or rejected during parser execution.

Paper/denominator impact:
- reports changed: no
- results changed: no
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Authorization:
- timing adapter authorized: no
- portability adapter authorized: no
- verifier support adapter authorized: no
- metric input authorization changed: no
- metrics implementation authorized: no
- reproduction interface implementation authorized: no
- public runner implementation authorized: no
- paper table rendering authorized: no

Next safe action:
- Review `audits/candidate_status_parser_v0/candidate_status_parser_input_manifest_report.md` and decide whether to curate an explicit row-level non-timing retained-evidence input manifest for a future parser rerun. Keep the 600 candidate parser rows unresolved until exact row-grain input sources are approved; do not fill timing fields, authorize metric input, compute metrics, render paper tables, update reports/results, change denominators, change paper results, change case membership, or modify raw legacy evidence without separate authorization.

### 2026-05-17 · a633402 · Candidate status whitelist triage for manual approval

Mode: manual-review triage; audit/design only; no candidate status parsing; no timing fields; no metrics
Legacy repo modified: no
Release repo modified: yes
Commit: `a633402bae9e2bd30f94057235593204e110a172`
Push: `origin/main` updated `0fac42f..a633402`

Summary:
- Created `audits/candidate_status_whitelist_triage/` with a maintainer-reviewable whitelist proposal for future `candidate_status_parser_v1`.
- Reviewed release metadata and selected legacy inventory paths only at path/header/schema-preview level.
- Produced 19 proposal rows: 4 `approve_header_only_then_parser`, 6 `defer_manual_review`, 8 rejected parser inputs, and 1 reference-only locator row.
- Created a preview manifest with all rows marked `pending_maintainer_review`; no row is approved by maintainer in this task.
- Did not parse candidate statuses, fill generated/ready/executed/exact fields, fill timing fields, compute metrics, create a production ledger, update reports/results, change denominators, change paper results, change case membership, modify the legacy repo, or modify raw legacy evidence.

Files created:
- `audits/candidate_status_whitelist_triage/candidate_status_whitelist_triage_summary.md`
- `audits/candidate_status_whitelist_triage/candidate_status_whitelist_proposal.csv`
- `audits/candidate_status_whitelist_triage/candidate_status_rejected_sources.csv`
- `audits/candidate_status_whitelist_triage/candidate_status_whitelist_review.md`
- `audits/candidate_status_whitelist_triage/candidate_status_parser_v1_input_manifest_preview.csv`
- `audits/candidate_status_whitelist_triage/candidate_status_manual_decision_sheet.csv`
- `audits/candidate_status_whitelist_triage/candidate_status_whitelist_triage_summary.json`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python scripts/dev/smoke_ledger_fixtures.py`: passed; 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, and 0 unexpected pass/fail rows.
- JSON invariant checks for `candidate_status_whitelist_triage_summary.json`: passed.
- CSV readability checks for proposal, manual decision sheet, manifest preview, and rejected-source files: passed.
- `git diff --check`: passed.
- `git status -sb`: only intended audit and project-control changes.
- `git diff --name-status`: only intended project-control tracked changes before staging; new audit files were untracked until explicit add.

Triage result:
- Candidate statuses filled: no.
- Timing fields filled: no.
- Metrics computed: no.
- Production ledger created: no.
- Files reviewed: 28.
- Whitelist proposal rows: 19.
- Proposed approve-header-only count: 4.
- Proposed defer count: 6.
- Rejected count: 8.

Paper/denominator impact:
- reports changed: no
- results changed: no
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Authorization:
- candidate status parsing authorized by this task: no
- timing parser authorized: no
- metric input authorization changed: no
- metrics implementation authorized: no
- reproduction interface implementation authorized: no
- public runner implementation authorized: no
- paper table rendering authorized: no

Next safe action:
- Maintainer reviews `audits/candidate_status_whitelist_triage/candidate_status_manual_decision_sheet.csv` and explicitly approves or rejects proposed candidate status parser inputs before any `candidate_status_parser_v1` manifest is created. Keep all 600 candidate parser rows unresolved until exact row-grain non-timing sources are approved; do not fill timing fields, authorize metric input, compute metrics, render paper tables, update reports/results, change denominators, change paper results, change case membership, or modify raw legacy evidence without separate authorization.

### 2026-05-17 · f763746 · Candidate status parser v1 whitelist approval recording

Mode: approval recording only; no parser implementation; no candidate status parsing; no timing fields; no metrics
Legacy repo modified: no
Release repo modified: yes
Commit: `f763746a89e251fb713022c7d6635716a4de7c43`
Push: `origin/main` updated `02f1f6c..f763746`

Summary:
- Recorded maintainer approval for `candidate_status_parser_v1` to use proposal IDs `P001`, `P002`, `P003`, `P011`, and `P012` only.
- Updated `candidate_status_manual_decision_sheet.csv` with approved fields, rejected fields, and required conditions for the five approved proposal IDs.
- Updated `candidate_status_parser_v1_input_manifest_preview.csv` so only the five approved sources are marked `approved_by_maintainer`.
- Marked `P013` as not approved for parser-v1 use in this approval record because it was not included in the explicit maintainer-approved proposal list.
- Did not implement `candidate_status_parser_v1`, parse candidate statuses, fill generated/ready/executed/exact fields, fill timing fields, authorize metric input, compute metrics, create a production ledger, update reports/results, change denominators, change paper results, change case membership, modify the legacy repo, or modify raw legacy evidence.

Files created:
- none

Files modified:
- `audits/candidate_status_whitelist_triage/candidate_status_manual_decision_sheet.csv`
- `audits/candidate_status_whitelist_triage/candidate_status_parser_v1_input_manifest_preview.csv`
- `audits/candidate_status_whitelist_triage/candidate_status_whitelist_triage_summary.md`
- `audits/candidate_status_whitelist_triage/candidate_status_whitelist_review.md`
- `audits/candidate_status_whitelist_triage/candidate_status_whitelist_triage_summary.json`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- CSV/JSON approval-record checks: passed; approved proposal IDs are exactly P001, P002, P003, P011, and P012.
- `python scripts/dev/smoke_ledger_fixtures.py`: passed; 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, and 0 unexpected pass/fail rows.
- `git diff --check`: passed.
- `git status -sb`: only intended whitelist-triage audit and project-control changes before commit.

Approval result:
- Approved proposal IDs: P001, P002, P003, P011, P012.
- candidate_status_parser_v1 implemented: no.
- Candidate statuses filled: no.
- Timing fields filled: no.
- Metric input authorized: no.
- Metrics computed: no.
- Production ledger created: no.

Paper/denominator impact:
- reports changed: no
- results changed: no
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Authorization:
- candidate_status_parser_v1 implementation authorized by maintainer approval: yes, bounded to the five approved non-timing whitelist entries and fail-closed row-grain validation.
- timing parser authorized: no
- metric input authorization changed: no
- metrics implementation authorized: no
- reproduction interface implementation authorized: no
- public runner implementation authorized: no
- paper table rendering authorized: no

Next safe action:
- Implement `candidate_status_parser_v1` from the five maintainer-approved whitelist entries only: `P001`, `P002`, `P003`, `P011`, and `P012`. The parser must remain non-timing, keep `metric_input_authorized=false`, compute no metrics, fail closed on row-grain ambiguity, leave unmatched rows unresolved, and avoid reports/results updates, denominator changes, paper-result changes, case membership changes, legacy repo mutation, and raw legacy evidence mutation.

### 2026-05-17 · 7769d4b · candidate_status_parser_v1 bounded non-timing approved-source parser

Mode: bounded non-timing approved-source parser; approved legacy CSV status columns only; no timing fields; no metrics
Legacy repo modified: no
Release repo modified: yes
Commit: `7769d4b8943f9035fcd90a6aa7676e6470198d19`
Push: `origin/main` updated `6932967..7769d4b`

Summary:
- Implemented `scripts/dev/build_candidate_status_parser_v1_manifest.py` to build a five-row manifest from maintainer-approved proposal IDs `P001`, `P002`, `P003`, `P011`, and `P012` only.
- Implemented `scripts/dev/parse_candidate_status_v1.py` to parse only approved non-timing status columns from the five approved legacy CSV sources.
- Updated `scripts/dev/validate_ledger_csv.py` so bounded parser-v1 non-timing candidate status values validate while timing, metrics, reports/results, denominator, and paper-result protections remain enforced.
- Created `audits/candidate_status_parser_v1/` with the approved manifest, parsed 600-row audit ledger, summary, report, checks, rejection log, source-use log, limitations, and ledger validation outputs.
- Created `docs/dev/CANDIDATE_STATUS_PARSER_V1.md`.
- Approved manifest inputs: 5.
- Manifest inputs parsed: 5.
- Row-level status rows filled: 175.
- Unresolved rows: 425.
- Production retained evidence parsed: yes, limited to approved legacy CSV status columns.
- Legacy repo read: yes, read-only approved CSV sources only.
- Did not modify the legacy repo, copy reports/results/runs, parse unapproved legacy files, parse raw logs, parse stdout/stderr payloads, parse prompt/token/API/model traces, parse timing arrays, fill timing fields, fill speedup fields, authorize metric input, compute metrics, create a production ledger, update reports/results, change denominators, change paper results, change case membership, or modify raw legacy evidence.

Files created:
- `scripts/dev/build_candidate_status_parser_v1_manifest.py`
- `scripts/dev/parse_candidate_status_v1.py`
- `audits/candidate_status_parser_v1/candidate_status_parser_v1_input_manifest.csv`
- `audits/candidate_status_parser_v1/candidate_status_parsed_ledger_v1.csv`
- `audits/candidate_status_parser_v1/candidate_status_parser_v1_summary.json`
- `audits/candidate_status_parser_v1/candidate_status_parser_v1_report.md`
- `audits/candidate_status_parser_v1/candidate_status_parser_v1_checks.csv`
- `audits/candidate_status_parser_v1/candidate_status_parser_v1_input_rejection_log.csv`
- `audits/candidate_status_parser_v1/candidate_status_parser_v1_source_use_log.csv`
- `audits/candidate_status_parser_v1/candidate_status_parser_v1_limitations.md`
- `audits/candidate_status_parser_v1/ledger_validation/ledger_validation_results.csv`
- `audits/candidate_status_parser_v1/ledger_validation/ledger_validation_summary.json`
- `audits/candidate_status_parser_v1/ledger_validation/ledger_validation_report.md`
- `docs/dev/CANDIDATE_STATUS_PARSER_V1.md`

Files modified:
- `scripts/dev/validate_ledger_csv.py`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python -m py_compile scripts/dev/build_candidate_status_parser_v1_manifest.py`: passed.
- `python -m py_compile scripts/dev/parse_candidate_status_v1.py`: passed.
- `python -m py_compile scripts/dev/validate_ledger_csv.py`: passed.
- `python -m py_compile scripts/dev/smoke_ledger_fixtures.py`: passed.
- `python scripts/dev/smoke_ledger_fixtures.py`: passed; 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, and 0 unexpected pass/fail rows.
- `python scripts/dev/build_candidate_status_parser_v1_manifest.py --out-dir audits/candidate_status_parser_v1`: passed; approved manifest inputs 5 and rejected/deferred inputs 14.
- `python scripts/dev/parse_candidate_status_v1.py --scaffold audits/rewrite_candidate_adapter_v0/rewrite_candidate_scaffold_ledger_v0.csv --manifest audits/candidate_status_parser_v1/candidate_status_parser_v1_input_manifest.csv --out-dir audits/candidate_status_parser_v1`: passed; 600 rows emitted, 175 row-level statuses filled, 425 unresolved rows.
- `python scripts/dev/validate_ledger_csv.py --ledger audits/candidate_status_parser_v1/candidate_status_parsed_ledger_v1.csv --case-set case_sets/common_core_v0/cases.csv --same-engine-denominator case_sets/common_core_v0/denominator_same_engine_120.csv --controls case_sets/common_core_v0/controls_360.csv --out-dir audits/candidate_status_parser_v1/ledger_validation`: passed; 600 rows checked, 0 errors, 0 warnings.
- JSON invariant checks for parser summary and ledger validation summary: passed.
- CSV checks for manifest count, 600 output rows, false metric flags, empty timing/speedup fields, validation pass, and parser checks: passed.
- `git diff --check`: passed.
- `git status -sb`: only intended parser-v1 scripts, audit outputs, docs, validator, and project-control changes before commit.

Parser result:
- candidate_status_parser_v1 implemented: yes.
- Approved manifest inputs: 5.
- Production retained evidence parsed: yes.
- Legacy repo read: yes.
- Row-level statuses filled: 175.
- Unresolved rows: 425.
- Timing fields filled: no.
- Metric-input-authorized rows: 0.
- Metrics computed: no.
- Generation Rate computed: no.
- Execution Coverage Rate computed: no.
- Result Consistency Rate computed: no.
- Timing metrics computed: no.
- Parser status summary: `row_level_status_filled=175`, `unresolved_no_approved_source_match=425`.
- Per-source fill summary: P001 rows_read=120 rows_matched=120; P002 rows_read=26 rows_matched=52; P003 rows_read=19 rows_matched=19; P011 rows_read=27 rows_matched=27; P012 rows_read=2 rows_matched=2.
- Rejected/deferred input summary: 14 non-approved proposal rows recorded in `candidate_status_parser_v1_input_rejection_log.csv`.

Paper/denominator impact:
- reports changed: no
- results changed: no
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Authorization:
- timing parser authorized: no
- metric input authorization changed: no
- metrics implementation authorized: no
- reproduction interface implementation authorized: no
- public runner implementation authorized: no
- paper table rendering authorized: no

Next safe action:
- Review `audits/candidate_status_parser_v1/candidate_status_parser_v1_report.md` and decide whether to authorize a validation-hardening or manual-review cleanup pass for the 425 unresolved rows. Do not authorize metric input, compute metrics, fill timing fields, render paper tables, update reports/results, change denominators, change paper results, change case membership, mutate the legacy repo, or modify raw legacy evidence without separate approval.

### 2026-05-17 · 3e523d8 · candidate_status_parser_v1 closeout and unresolved-row review

Mode: parser closeout and unresolved-row review; release-repo audit outputs only; no new candidate status parsing; no timing fields; no metrics
Legacy repo modified: no
Release repo modified: yes
Commit: `3e523d8fe6c231a0520893878c1f4bf4c5a33e5b`
Push: `origin/main` updated `a37d205..3e523d8`

Summary:
- Created `audits/candidate_status_parser_v1_closeout/` to review the existing `candidate_status_parser_v1` 600-row audit ledger and related parser-v1 audit outputs.
- Confirmed no new candidate status parsing was performed, no additional legacy files were opened, no additional statuses were filled, timing fields remain unfilled, `metric_input_authorized` rows remain 0, and no metrics were computed.
- Confirmed row-level statuses filled by prior parser v1: 175.
- Confirmed unresolved rows: 425.
- Confirmed approved parser-v1 inputs reviewed: P001, P002, P003, P011, and P012.
- Documented source overlap: P001/P002 overlap on 26 Direct LLM original rows, P002/P003 overlap on 19 Repair-1 rows, and P011/P012 Calcite overlap on 0 rows.
- Confirmed the existing parser-v1 ledger validation passed with 600 rows checked, 0 errors, and 0 warnings.

Files created:
- `audits/candidate_status_parser_v1_closeout/candidate_status_parser_v1_closeout_summary.md`
- `audits/candidate_status_parser_v1_closeout/candidate_status_parser_v1_filled_distribution.csv`
- `audits/candidate_status_parser_v1_closeout/candidate_status_parser_v1_unresolved_distribution.csv`
- `audits/candidate_status_parser_v1_closeout/candidate_status_parser_v1_source_contribution.csv`
- `audits/candidate_status_parser_v1_closeout/candidate_status_parser_v1_overlap_conflict_review.csv`
- `audits/candidate_status_parser_v1_closeout/candidate_status_parser_v1_metric_boundary_checks.csv`
- `audits/candidate_status_parser_v1_closeout/candidate_status_parser_v1_next_steps.md`
- `audits/candidate_status_parser_v1_closeout/candidate_status_parser_v1_closeout_summary.json`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python scripts/dev/smoke_ledger_fixtures.py`: passed; 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, and 0 unexpected pass/fail rows.
- JSON invariant checks for `candidate_status_parser_v1_closeout_summary.json`: passed.
- CSV checks for filled distribution, unresolved distribution, source contribution, overlap/conflict review, and metric boundary checks: passed.
- Metric boundary checks: all PASS.
- `git diff --check`: passed.
- `git status -sb`: only intended closeout audit and project-control changes before commit.

Closeout result:
- new candidate status parsing performed: no
- candidate statuses filled by prior parser v1: 175
- unresolved rows: 425
- timing fields filled: no
- metric_input_authorized rows: 0
- metrics computed: no
- Generation Rate computed: no
- Execution Coverage Rate computed: no
- Result Consistency Rate computed: no
- timing metrics computed: no

Paper/denominator impact:
- reports changed: no
- results changed: no
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Next safe action:
- Perform a metric-input readiness review for the 175 filled `candidate_status_parser_v1` audit rows and separately triage row-level evidence for the 425 unresolved rows. Do not authorize metrics, fill timing fields, render paper tables, update reports/results, change denominators, change paper results, change case membership, mutate the legacy repo, or modify raw legacy evidence without separate approval.

### 2026-05-17 · 7f8b894 · candidate_status_parser_v1 closeout and metric-input readiness review

Mode: parser closeout plus metric-input readiness review; release-repo audit outputs only; no new candidate status parsing; no timing fields; no metric-input authorization; no metrics
Legacy repo modified: no
Release repo modified: yes
Commit: `7f8b89414474d8634303b8037dbf6c713f68f1d0`
Push: `origin/main` updated `498db49..7f8b894`

Summary:
- Updated `audits/candidate_status_parser_v1_closeout/` to add audit-only metric-input readiness labels for the 175 filled `candidate_status_parser_v1` rows.
- Confirmed no new candidate status parsing was performed, no additional legacy files were opened, no additional statuses were filled, timing fields remain unfilled, `metric_input_authorized` rows remain 0, and no metrics were computed.
- Confirmed row-level statuses filled by prior parser v1: 175.
- Confirmed unresolved rows: 425.
- Metric-input readiness review completed: yes.
- Readiness labels: `ready_candidate_status_only=130`, `needs_source_overlap_review=45`, `needs_status_normalization=0`, `not_metric_ready=0`.
- Confirmed approved parser-v1 inputs reviewed: P001, P002, P003, P011, and P012.
- Documented source overlap: P001/P002 overlap on 26 Direct LLM original rows, P002/P003 overlap on 19 Repair-1 rows, and P011/P012 Calcite overlap on 0 rows.
- Confirmed the existing parser-v1 ledger validation passed with 600 rows checked, 0 errors, and 0 warnings.

Files created:
- `audits/candidate_status_parser_v1_closeout/candidate_status_metric_input_readiness_review.csv`

Files modified:
- `audits/candidate_status_parser_v1_closeout/candidate_status_parser_v1_closeout_summary.md`
- `audits/candidate_status_parser_v1_closeout/candidate_status_parser_v1_filled_distribution.csv`
- `audits/candidate_status_parser_v1_closeout/candidate_status_parser_v1_unresolved_distribution.csv`
- `audits/candidate_status_parser_v1_closeout/candidate_status_parser_v1_source_contribution.csv`
- `audits/candidate_status_parser_v1_closeout/candidate_status_parser_v1_overlap_conflict_review.csv`
- `audits/candidate_status_parser_v1_closeout/candidate_status_parser_v1_metric_boundary_checks.csv`
- `audits/candidate_status_parser_v1_closeout/candidate_status_parser_v1_next_steps.md`
- `audits/candidate_status_parser_v1_closeout/candidate_status_parser_v1_closeout_summary.json`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python scripts/dev/smoke_ledger_fixtures.py`: passed; 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, and 0 unexpected pass/fail rows.
- JSON invariant checks for `candidate_status_parser_v1_closeout_summary.json`: passed.
- CSV checks for filled distribution, unresolved distribution, source contribution, overlap/conflict review, metric boundary checks, and metric-input readiness review: passed.
- Metric-input readiness review rows: 175, exactly one per filled parser-v1 row.
- Metric boundary checks: all PASS.
- `git diff --check`: passed after normalizing generated CSV line endings to LF.
- `git status -sb`: only intended closeout audit and project-control changes before commit.

Closeout/readiness result:
- new candidate status parsing performed: no
- candidate statuses filled by prior parser v1: 175
- unresolved rows: 425
- timing fields filled: no
- metric_input_authorized rows: 0
- metrics computed: no
- Generation Rate computed: no
- Execution Coverage Rate computed: no
- Result Consistency Rate computed: no
- timing metrics computed: no

Paper/denominator impact:
- reports changed: no
- results changed: no
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Next safe action:
- Review `audits/candidate_status_parser_v1_closeout/candidate_status_metric_input_readiness_review.csv`. If accepted, authorize a separate `metric_input_authorization_overlay_v0` for rows labeled `ready_candidate_status_only` only; separately review overlap rows and unresolved rows. Do not compute metrics, fill timing fields, render paper tables, update reports/results, change denominators, change paper results, change case membership, mutate the legacy repo, or modify raw legacy evidence without separate approval.

### 2026-05-17 · 80f9617 · metric_input_authorization_overlay_v0 for ready candidate-status rows

Mode: bounded metric-input authorization overlay; audit-only; no metrics; no timing; no parser ledger mutation
Legacy repo modified: no
Release repo modified: yes
Commit: `80f9617f1bbf2bd3e6e1e3cd96c6ddae3fa2651d`
Push: `origin/main` updated `8089e86..80f9617`

Summary:
- Created `audits/metric_input_authorization_overlay_v0/` as a separate audit-only metric-input authorization overlay.
- Read `audits/candidate_status_parser_v1_closeout/candidate_status_metric_input_readiness_review.csv`.
- Reviewed 175 filled parser-v1 readiness rows.
- Authorized exactly 130 rows labeled `ready_candidate_status_only` with `metric_input_authorized_overlay=true`.
- Denied exactly 45 rows labeled `needs_source_overlap_review` with `metric_input_authorized_overlay=false`.
- Left the 425 unresolved parser-v1 rows unauthorized and outside the overlay.
- Did not rewrite `audits/candidate_status_parser_v1/candidate_status_parsed_ledger_v1.csv`.
- Did not authorize timing fields, speedup fields, metric computation, paper table rendering, reports/results updates, denominator changes, or paper-result changes.

Files created:
- `audits/metric_input_authorization_overlay_v0/metric_input_authorization_overlay_v0.csv`
- `audits/metric_input_authorization_overlay_v0/metric_input_authorization_overlay_summary.json`
- `audits/metric_input_authorization_overlay_v0/metric_input_authorization_overlay_report.md`
- `audits/metric_input_authorization_overlay_v0/metric_input_authorization_overlay_checks.csv`
- `audits/metric_input_authorization_overlay_v0/metric_input_authorization_denied_rows.csv`
- `audits/metric_input_authorization_overlay_v0/metric_input_authorization_next_steps.md`
- `audits/metric_input_authorization_overlay_v0/metric_input_authorization_overlay_summary.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python scripts/dev/smoke_ledger_fixtures.py`: passed; 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, and 0 unexpected pass/fail rows.
- JSON invariant checks for `metric_input_authorization_overlay_summary.json`: passed.
- CSV checks for overlay rows, denied rows, authorization booleans, forbidden timing/paper/report/denominator flags, and checks CSV: passed.
- Original parser ledger mutation check: passed; `candidate_status_parsed_ledger_v1.csv` absent from `git diff --name-status`.
- `git diff --check`: passed.
- `git status -sb`: only intended overlay audit and project-control changes before commit.

Overlay result:
- authorized metric-input overlay rows: 130
- unauthorized overlap rows: 45
- unresolved rows: 425
- timing authorized: no
- metrics computed: no
- Generation Rate computed: no
- Execution Coverage Rate computed: no
- Result Consistency Rate computed: no
- timing metrics computed: no
- original parser ledger modified: no

Paper/denominator impact:
- reports changed: no
- results changed: no
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Next safe action:
- Do not compute metrics yet. Either perform manual overlap review for the 45 denied rows or prepare a status-only metrics dry-run plan that explicitly handles partial denominator coverage from the 130 authorized overlay rows. Keep timing adapter work separate.

### 2026-05-17 · 0be6d7b · candidate status overlap review and status-only metrics dry-run plan

Mode: release-repo audit/planning only; no new candidate status parsing; no metric input authorization change; no metrics; no timing
Legacy repo modified: no
Release repo modified: yes
Commit: `0be6d7bfb49517fbf927e279b153359fa0c19e19`
Push: `origin/main` updated `646f06b..0be6d7b`

Summary:
- Created `audits/candidate_status_overlap_and_metrics_dryrun_plan/`.
- Reviewed 45 overlap-blocked rows from `metric_input_authorization_overlay_v0`.
- Classified 26 P001/P002 rows as `overlap_resolvable_by_priority_rule`.
- Classified 19 P002/P003 rows as `overlap_requires_manual_source_selection`.
- Kept all overlap rows unauthorized; no actual metric-input authorization changed.
- Planned a future status-only metrics dry run from the 130 currently authorized non-timing candidate-status rows.
- Confirmed 425 unresolved rows remain unauthorized.
- Did not perform new candidate status parsing, read new legacy evidence, fill timing fields, compute metrics, update reports/results, change denominators, change paper results, change case membership, or modify raw legacy evidence.

Files created:
- `audits/candidate_status_overlap_and_metrics_dryrun_plan/candidate_status_overlap_review_summary.md`
- `audits/candidate_status_overlap_and_metrics_dryrun_plan/candidate_status_overlap_review.csv`
- `audits/candidate_status_overlap_and_metrics_dryrun_plan/candidate_status_overlap_policy_options.md`
- `audits/candidate_status_overlap_and_metrics_dryrun_plan/status_only_metric_dryrun_scope.csv`
- `audits/candidate_status_overlap_and_metrics_dryrun_plan/status_only_metrics_dryrun_plan.md`
- `audits/candidate_status_overlap_and_metrics_dryrun_plan/denominator_handling_notes.md`
- `audits/candidate_status_overlap_and_metrics_dryrun_plan/metric_readiness_blockers.md`
- `audits/candidate_status_overlap_and_metrics_dryrun_plan/candidate_status_overlap_and_metrics_dryrun_plan_summary.json`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python scripts/dev/smoke_ledger_fixtures.py`: passed; 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, and 0 unexpected pass/fail rows.
- JSON invariant checks for `candidate_status_overlap_and_metrics_dryrun_plan_summary.json`: passed.
- CSV checks for 45 overlap-review rows, required status-only metric dry-run scope rows, no metrics-computed claims, no metric-input-authorization changes, and no timing metric entries: passed.
- `git diff --check`: passed.
- `git status -sb`: only intended audit and project-control changes before commit.

Task result:
- new candidate status parsing performed: no
- metrics computed: no
- metric input authorization changed: no
- overlap rows reviewed: 45
- currently authorized rows: 130
- unresolved rows: 425
- timing fields filled: no
- Generation Rate computed: no
- Execution Coverage Rate computed: no
- Result Consistency Rate computed: no
- timing metrics computed: no

Paper/denominator impact:
- reports changed: no
- results changed: no
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Next safe action:
- Maintainer reviews `audits/candidate_status_overlap_and_metrics_dryrun_plan/candidate_status_overlap_review.csv` and chooses an overlap policy. Separately authorize any status-only metrics dry-run implementation before computing metrics; keep timing adapter work separate.

### 2026-05-17 · a322b0a · status_only_metrics_dryrun_v0 from authorized candidate-status rows

Mode: bounded audit-only metrics dry-run; status-only candidate rows; no official metrics; no paper tables; no timing
Legacy repo modified: no
Release repo modified: yes
Commit: `a322b0a1b3b4e10b44b390040e46908f176a9d79`
Push: `origin/main` updated `8ad99f5..a322b0a`

Summary:
- Added `scripts/dev/compute_status_only_metrics_dryrun.py`.
- Created `audits/status_only_metrics_dryrun_v0/`.
- Used only 130 rows with `metric_input_authorized_overlay=true` and `readiness_label=ready_candidate_status_only`.
- Excluded 45 unauthorized overlap rows.
- Preserved 425 unresolved rows in denominator/accounting outputs.
- Created audit-only dry-run outputs for Generation Rate, Execution Coverage Rate, and Result Consistency Rate.
- Marked every dry-run row as `dry_run_value_is_official=false` and `paper_result=false`.
- Did not compute official metrics, render paper tables, compute timing metrics, update reports/results, change denominators, change paper results, change case membership, read new legacy evidence, or modify raw legacy evidence.

Files created:
- `scripts/dev/compute_status_only_metrics_dryrun.py`
- `audits/status_only_metrics_dryrun_v0/status_only_metrics_dryrun_table.csv`
- `audits/status_only_metrics_dryrun_v0/status_only_metrics_dryrun_denominator_audit.csv`
- `audits/status_only_metrics_dryrun_v0/status_only_metrics_dryrun_input_rows.csv`
- `audits/status_only_metrics_dryrun_v0/status_only_metrics_dryrun_excluded_rows_summary.csv`
- `audits/status_only_metrics_dryrun_v0/status_only_metrics_dryrun_report.md`
- `audits/status_only_metrics_dryrun_v0/status_only_metrics_dryrun_checks.csv`
- `audits/status_only_metrics_dryrun_v0/status_only_metrics_dryrun_summary.json`
- `audits/status_only_metrics_dryrun_v0/status_only_metrics_dryrun_limitations.md`
- `docs/dev/STATUS_ONLY_METRICS_DRYRUN_V0.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python -m py_compile scripts/dev/compute_status_only_metrics_dryrun.py`: passed.
- `python scripts/dev/smoke_ledger_fixtures.py`: passed; 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, and 0 unexpected pass/fail rows.
- `python scripts/dev/compute_status_only_metrics_dryrun.py ...`: passed; wrote 180 dry-run table rows, 130 authorized input rows, and preserved 425 unresolved rows.
- JSON invariant checks for `status_only_metrics_dryrun_summary.json`: passed.
- CSV checks for required dry-run metrics, official/paper flags, denominator preservation, excluded-row categories, 130 input rows, and all PASS checks: passed.
- `git diff --check`: passed.
- `git status -sb`: only intended dry-run audit, doc, script, and project-control changes before commit.

Task result:
- official metrics computed: no
- audit-only dry-run metrics computed: yes
- paper tables rendered: no
- timing metrics computed: no
- Generation Rate dry-run created: yes
- Execution Coverage Rate dry-run created: yes
- Result Consistency Rate dry-run created: yes
- authorized input rows: 130
- unauthorized overlap rows: 45
- unresolved rows: 425

Paper/denominator impact:
- reports changed: no
- results changed: no
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Next safe action:
- Review `audits/status_only_metrics_dryrun_v0/status_only_metrics_dryrun_table.csv` and its status-normalization caveats. If accepted, separately authorize status normalization and any official metric-computation task; keep overlap resolution and timing adapter work separate.

### 2026-05-17 · c78ba6a · status_field_normalization_v0 for authorized candidate-status rows

Mode: bounded audit-only status normalization; authorized candidate-status rows only; no metrics; no timing
Legacy repo modified: no
Release repo modified: yes
Commit: `c78ba6ab3b47a50268814d660c49f1f1828bc14d`
Push: `origin/main` updated `e6f4420..c78ba6a`

Summary:
- Added `scripts/dev/normalize_candidate_status_fields.py`.
- Created `audits/status_field_normalization_v0/`.
- Processed exactly 130 rows with `metric_input_authorized_overlay=true` and `readiness_label=ready_candidate_status_only`.
- Excluded 45 overlap rows and 425 unresolved rows.
- Normalized non-timing fields only: `generated`, `ready`, `executed`, `exact`, `result_status`, `failure_stage`, `failure_type`, `parse_status`, and `checker_status`.
- Inventoried 28 observed field/raw-value pairs and emitted the mapping table used by the script.
- Rows needing manual mapping: 0.
- Left original parser and authorization ledgers unchanged.
- Did not compute official metrics, render paper tables, fill or modify timing fields, update reports/results, change denominators, change paper results, change case membership, read new legacy evidence, or modify raw legacy evidence.

Files created:
- `scripts/dev/normalize_candidate_status_fields.py`
- `audits/status_field_normalization_v0/normalized_candidate_status_overlay_v0.csv`
- `audits/status_field_normalization_v0/status_normalization_observed_values.csv`
- `audits/status_field_normalization_v0/status_normalization_mapping_table.csv`
- `audits/status_field_normalization_v0/status_normalization_manual_review_rows.csv`
- `audits/status_field_normalization_v0/status_normalization_readiness_by_method.csv`
- `audits/status_field_normalization_v0/status_field_normalization_report.md`
- `audits/status_field_normalization_v0/status_field_normalization_checks.csv`
- `audits/status_field_normalization_v0/status_field_normalization_summary.json`
- `audits/status_field_normalization_v0/status_field_normalization_limitations.md`
- `docs/dev/STATUS_FIELD_NORMALIZATION_V0.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python -m py_compile scripts/dev/normalize_candidate_status_fields.py`: passed.
- `python scripts/dev/smoke_ledger_fixtures.py`: passed; 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, and 0 unexpected pass/fail rows.
- `python scripts/dev/normalize_candidate_status_fields.py ...`: passed; normalized 130 rows, emitted 28 observed-value rows, and found 0 rows needing manual mapping.
- JSON invariant checks for `status_field_normalization_summary.json`: passed.
- CSV checks for 130 normalized overlay rows, observed-value inventory, mapping table, all PASS checks, no metrics-computed rows, no paper-result rows, and timing unchanged flags: passed.
- Original parser ledger mutation check: passed; `candidate_status_parsed_ledger_v1.csv` absent from `git diff --name-status`.
- `git diff --check`: passed.
- `git status -sb`: only intended normalization audit, doc, script, and project-control changes before commit.

Task result:
- rows normalized: 130
- rows needing manual mapping: 0
- official metrics computed: no
- metrics computed: no
- timing fields filled: no
- timing fields modified: no
- paper tables rendered: no
- original parser ledger modified: no

Paper/denominator impact:
- reports changed: no
- results changed: no
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Next safe action:
- Review `audits/status_field_normalization_v0/normalized_candidate_status_overlay_v0.csv` and `audits/status_field_normalization_v0/status_normalization_readiness_by_method.csv`. If accepted, separately authorize a normalized status-only metrics dry-run v1; keep official metrics, overlap resolution, and timing adapter work separate.

### 2026-05-17 · 9be0625 · normalized_status_only_metrics_dryrun_v1 from normalized candidate-status overlay

Mode: bounded audit-only normalized status metrics dry run; authorized normalized candidate-status rows only; no official metrics; no timing; no paper tables
Legacy repo modified: no
Release repo modified: yes
Commit: `9be0625c96dcd46cf648349e2b92b571a11d3fc1`
Push: `origin/main` updated `d67b75c..9be0625`

Summary:
- Added `scripts/dev/compute_normalized_status_only_metrics_dryrun.py`.
- Created `audits/normalized_status_only_metrics_dryrun_v1/`.
- Read the 600-row parser-v1 candidate ledger, the 175-row metric-input authorization overlay, the 130-row normalized candidate-status overlay, and the 120-row same-engine denominator scaffold.
- Used exactly 130 rows with `metric_input_authorized_overlay=true`, `readiness_label=ready_candidate_status_only`, and a matching normalized overlay row.
- Excluded 45 overlap rows and preserved 425 unresolved rows in denominator/accounting outputs.
- Created audit-only dry-run outputs for Generation Rate, Execution Coverage Rate, and Result Consistency Rate using normalized non-timing status fields only.
- Marked every dry-run row as `dry_run_value_is_official=false`, `paper_result=false`, and `audit_only=true`.
- Did not compute official metrics, render paper tables, compute timing metrics, update reports/results, change denominators, change paper results, change case membership, read new legacy evidence, or modify raw legacy evidence.

Files created:
- `scripts/dev/compute_normalized_status_only_metrics_dryrun.py`
- `audits/normalized_status_only_metrics_dryrun_v1/normalized_status_only_metrics_dryrun_table.csv`
- `audits/normalized_status_only_metrics_dryrun_v1/normalized_status_only_denominator_audit.csv`
- `audits/normalized_status_only_metrics_dryrun_v1/normalized_status_only_input_rows.csv`
- `audits/normalized_status_only_metrics_dryrun_v1/normalized_status_only_excluded_rows_summary.csv`
- `audits/normalized_status_only_metrics_dryrun_v1/normalized_status_only_status_caveats.csv`
- `audits/normalized_status_only_metrics_dryrun_v1/normalized_status_only_metrics_dryrun_report.md`
- `audits/normalized_status_only_metrics_dryrun_v1/normalized_status_only_metrics_dryrun_checks.csv`
- `audits/normalized_status_only_metrics_dryrun_v1/normalized_status_only_metrics_dryrun_summary.json`
- `audits/normalized_status_only_metrics_dryrun_v1/normalized_status_only_metrics_dryrun_limitations.md`
- `docs/dev/NORMALIZED_STATUS_ONLY_METRICS_DRYRUN_V1.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python -m py_compile scripts/dev/compute_normalized_status_only_metrics_dryrun.py`: passed.
- `python scripts/dev/smoke_ledger_fixtures.py`: passed; 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, and 0 unexpected pass/fail rows.
- `python scripts/dev/compute_normalized_status_only_metrics_dryrun.py ...`: passed; wrote 180 dry-run table rows, used 130 authorized normalized input rows, and retained 425 unresolved rows in accounting outputs.
- JSON invariant checks for `normalized_status_only_metrics_dryrun_summary.json`: passed.
- CSV checks for required dry-run metrics, official/paper/audit flags, denominator preservation, excluded-row categories, caveat categories, and all PASS checks: passed.
- `git diff --check`: passed.
- `git status -sb`: only intended normalized dry-run audit, doc, script, and project-control changes before commit.

Task result:
- official metrics computed: no
- audit-only dry-run metrics computed: yes
- paper tables rendered: no
- timing metrics computed: no
- Generation Rate dry-run created: yes
- Execution Coverage Rate dry-run created: yes
- Result Consistency Rate dry-run created: yes
- authorized input rows: 130
- unauthorized overlap rows: 45
- unresolved rows: 425
- normalized overlay rows: 130
- rows with manual mapping needed: 0

Paper/denominator impact:
- reports changed: no
- results changed: no
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Next safe action:
- Review `audits/normalized_status_only_metrics_dryrun_v1/normalized_status_only_metrics_dryrun_table.csv` and `audits/normalized_status_only_metrics_dryrun_v1/normalized_status_only_status_caveats.csv`. If accepted, separately authorize official metric computation or additional evidence parsing; keep overlap resolution and timing adapter work separate.

### 2026-05-17 · a674988 · status_inference_policy_v0 and candidate status evidence-gap review

Mode: status-inference policy and evidence-gap review; audit/design only; no official metrics; no timing; no reports/results
Legacy repo modified: no
Release repo modified: yes
Commit: `a674988c82d53a96b4dbd9c1663b265216108b98`
Push: `origin/main` updated `8d4397e..a674988`

Summary:
- Created `repository_spec/status_inference_policy_v1_draft.md`.
- Created `audits/status_inference_policy_v0/`.
- Reviewed parser-v1, metric-input authorization, normalization, and normalized status-only dry-run outputs.
- Defined conservative observed-vs-inferred status rules for R1 ready-implies-generated, R2 exact-implies-executed, R3 failure-stage-derived inference, and R4 unknown-stays-unknown.
- Created a preview-only inferred-status candidate overlay for 94 potential ready-implies-generated rows.
- Confirmed 0 potential exact-implies-executed rows.
- Documented evidence gaps across five Track-A same-engine method routes and nine status fields.
- Did not compute official metrics, change metric-input authorization, modify parser ledgers, modify normalization overlays, fill timing fields, update reports/results, change denominators, change paper results, change case membership, read new legacy evidence, or modify raw legacy evidence.

Files created:
- `repository_spec/status_inference_policy_v1_draft.md`
- `audits/status_inference_policy_v0/status_inference_policy_summary.md`
- `audits/status_inference_policy_v0/status_inference_rule_matrix.csv`
- `audits/status_inference_policy_v0/inferred_status_candidate_overlay_preview.csv`
- `audits/status_inference_policy_v0/status_evidence_gap_matrix.csv`
- `audits/status_inference_policy_v0/status_inference_manual_questions.md`
- `audits/status_inference_policy_v0/status_inference_dryrun_v2_plan.md`
- `audits/status_inference_policy_v0/status_inference_policy_summary.json`
- `audits/status_inference_policy_v0/status_inference_limitations.md`
- `docs/dev/STATUS_INFERENCE_POLICY_V0.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python scripts/dev/smoke_ledger_fixtures.py`: passed; 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, and 0 unexpected pass/fail rows.
- JSON invariant checks for `status_inference_policy_summary.json`: passed.
- CSV checks for R1/R2/R3/R4 coverage, preview-only inference flags, future authorization flags, required evidence-gap fields, and no metric authorization claims: passed.
- `git diff --check`: passed.
- `git status -sb`: only intended status-inference policy audit, spec, doc, and project-control changes before commit.

Task result:
- official metrics computed: no
- audit-only inference preview created: yes
- parser ledgers modified: no
- normalized overlay modified: no
- timing fields filled: no
- potential ready-implies-generated rows: 94
- potential exact-implies-executed rows: 0
- rows requiring future authorization: 94

Paper/denominator impact:
- reports changed: no
- results changed: no
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Next safe action:
- Review `audits/status_inference_policy_v0/status_inference_rule_matrix.csv` and `audits/status_inference_policy_v0/inferred_status_candidate_overlay_preview.csv`. If accepted, separately authorize a status inference overlay or additional evidence parsing; keep official metrics and timing adapter work separate.

### 2026-05-17 · e08b145 · status_inference_overlay_v0 and normalized status-only metrics dry-run v2

Mode: bounded audit-only inference overlay plus normalized status-only metrics dry run; no official metrics; no timing; no reports/results
Legacy repo modified: no
Release repo modified: yes
Commit: `e08b145e35118d322902804f576842dee782639e`
Push: `origin/main` updated `84bf13b..e08b145`

Summary:
- Added `scripts/dev/build_status_inference_overlay.py`.
- Added `scripts/dev/compute_normalized_status_only_metrics_dryrun_v2.py`.
- Created `audits/status_inference_overlay_v0/` with 94 R1 `inferred_generated=true` overlay rows.
- Created `audits/normalized_status_only_metrics_dryrun_v2/`.
- Used exactly 130 authorized candidate-status rows, 130 normalized overlay rows, and 94 inferred-generated rows.
- Kept inferred generated status separate from observed `normalized_generated`; no observed normalized field was overwritten.
- Created audit-only v2 dry-run outputs for Generation Rate, Execution Coverage Rate, and Result Consistency Rate.
- Preserved 45 unauthorized overlap rows and 425 unresolved rows in denominator/accounting outputs.
- Did not compute official metrics, render paper tables, compute timing metrics, update reports/results, change denominators, change paper results, change case membership, read new legacy evidence, or modify raw legacy evidence.

Files created:
- `scripts/dev/build_status_inference_overlay.py`
- `scripts/dev/compute_normalized_status_only_metrics_dryrun_v2.py`
- `audits/status_inference_overlay_v0/status_inference_overlay_v0.csv`
- `audits/status_inference_overlay_v0/status_inference_overlay_summary.json`
- `audits/status_inference_overlay_v0/status_inference_overlay_report.md`
- `audits/status_inference_overlay_v0/status_inference_overlay_checks.csv`
- `audits/normalized_status_only_metrics_dryrun_v2/normalized_status_only_metrics_dryrun_v2_table.csv`
- `audits/normalized_status_only_metrics_dryrun_v2/normalized_status_only_dryrun_v2_denominator_audit.csv`
- `audits/normalized_status_only_metrics_dryrun_v2/normalized_status_only_dryrun_v2_input_rows.csv`
- `audits/normalized_status_only_metrics_dryrun_v2/normalized_status_only_dryrun_v2_delta_vs_v1.csv`
- `audits/normalized_status_only_metrics_dryrun_v2/normalized_status_only_dryrun_v2_caveats.csv`
- `audits/normalized_status_only_metrics_dryrun_v2/normalized_status_only_metrics_dryrun_v2_report.md`
- `audits/normalized_status_only_metrics_dryrun_v2/normalized_status_only_metrics_dryrun_v2_checks.csv`
- `audits/normalized_status_only_metrics_dryrun_v2/normalized_status_only_metrics_dryrun_v2_summary.json`
- `audits/normalized_status_only_metrics_dryrun_v2/normalized_status_only_metrics_dryrun_v2_limitations.md`
- `docs/dev/STATUS_INFERENCE_OVERLAY_AND_DRYRUN_V2.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python -m py_compile scripts/dev/build_status_inference_overlay.py`: passed.
- `python -m py_compile scripts/dev/compute_normalized_status_only_metrics_dryrun_v2.py`: passed.
- `python scripts/dev/smoke_ledger_fixtures.py`: passed; 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, and 0 unexpected pass/fail rows.
- `python scripts/dev/build_status_inference_overlay.py ...`: passed; wrote 94 inferred status overlay rows.
- `python scripts/dev/compute_normalized_status_only_metrics_dryrun_v2.py ...`: passed; used 130 authorized rows and 94 inferred-generated rows.
- JSON invariant checks for overlay and v2 dry-run summaries: passed.
- CSV checks for 94 overlay rows, official/paper/audit flags, required metric families, and v1-v2 inference deltas: passed.
- `git diff --check`: passed.
- `git status -sb`: only intended status inference overlay, v2 dry-run, docs, scripts, and project-control changes before commit.

Task result:
- status inference overlay completed: yes.
- inference overlay rows: 94.
- official metrics computed: no.
- audit-only dry-run metrics computed: yes.
- paper tables rendered: no.
- timing metrics computed: no.
- Generation Rate dry-run created: yes.
- Execution Coverage Rate dry-run created: yes.
- Result Consistency Rate dry-run created: yes.
- authorized input rows: 130.
- unauthorized overlap rows: 45.
- unresolved rows: 425.
- inferred generated rows used: 94.

Paper/denominator impact:
- reports changed: no.
- results changed: no.
- denominator changed: no.
- paper results changed: no.
- case membership changed: no.
- raw legacy evidence changed: no.

Next safe action:
- Review `audits/normalized_status_only_metrics_dryrun_v2/normalized_status_only_dryrun_v2_delta_vs_v1.csv` and `audits/normalized_status_only_metrics_dryrun_v2/normalized_status_only_dryrun_v2_caveats.csv`. If accepted, separately authorize official metric readiness review, additional evidence parsing, or overlap resolution; keep timing and paper rendering separate.

### 2026-05-17 · 849927b · candidate_status_evidence_completion_round1

Mode: targeted evidence-completion triage; audit-only; no candidate status parsing; no metric authorization; no metrics; no timing; no reports/results
Legacy repo modified: no
Release repo modified: yes
Commit: `849927b3d5eb9edab4280e9842f51c2f80f00b85`
Push: `origin/main` updated `7f3f788..849927b`

Summary:
- Reviewed 45 overlap-denied candidate-status rows from `metric_input_authorization_overlay_v0`.
- Proposed overlap resolution policy for 26 `P001|P002` Direct-LLM original rows and 19 `P002|P003` Repair-1 rows.
- Reviewed eight SQLGlot candidate evidence sources at release-metadata and safe header/schema-preview level only.
- Created ten SQLGlot manifest-preview rows, all `approved_for_parser=false` and `approval_status=pending_maintainer_review`.
- Did not fill candidate statuses, change metric-input authorization, parse unapproved legacy evidence into ledger rows, compute metrics, fill timing fields, update reports/results, change denominators, change paper results, change case membership, or modify raw legacy evidence.

Files created:
- `audits/candidate_status_evidence_completion_round1/evidence_completion_round1_summary.md`
- `audits/candidate_status_evidence_completion_round1/overlap_rows_resolution_proposal.csv`
- `audits/candidate_status_evidence_completion_round1/overlap_policy_recommendation.md`
- `audits/candidate_status_evidence_completion_round1/sqlglot_candidate_source_triage.csv`
- `audits/candidate_status_evidence_completion_round1/sqlglot_candidate_manual_decision_sheet.csv`
- `audits/candidate_status_evidence_completion_round1/sqlglot_parser_v1_manifest_preview.csv`
- `audits/candidate_status_evidence_completion_round1/candidate_status_completion_round1_risk_register.md`
- `audits/candidate_status_evidence_completion_round1/candidate_status_completion_round1_next_actions.md`
- `audits/candidate_status_evidence_completion_round1/candidate_status_evidence_completion_round1_summary.json`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python scripts/dev/smoke_ledger_fixtures.py`: passed; 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, and 0 unexpected pass/fail rows.
- JSON invariant checks for `candidate_status_evidence_completion_round1_summary.json`: passed.
- CSV checks for 45 overlap proposal rows, `would_change_metric_input_authorization=false`, SQLGlot headers, no approved manifest-preview rows, and no metric/status-fill claims: passed.
- `git diff --check`: passed.
- `git status -sb`: only intended audit and project-control changes before commit.

Task result:
- candidate statuses filled: no
- metrics computed: no
- timing fields filled: no
- overlap rows reviewed: 45
- SQLGlot candidate sources reviewed: 8
- SQLGlot manifest preview rows: 10

Paper/denominator impact:
- reports changed: no
- results changed: no
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Next safe action:
- Maintainer reviews `audits/candidate_status_evidence_completion_round1/overlap_rows_resolution_proposal.csv` and `audits/candidate_status_evidence_completion_round1/sqlglot_candidate_manual_decision_sheet.csv`; if accepted, separately authorize an overlap-priority authorization overlay v1 and/or a sanitized SQLGlot projection/parser task.

### 2026-05-17 · 2dd7c02 · overlap_priority_overlay_v1 and normalized status-only dry-run v3

Mode: bounded audit-only overlap resolution plus normalized status-only dry run; no official metrics; no timing; no reports/results; no SQLGlot parser
Legacy repo modified: no
Release repo modified: yes
Commit: `2dd7c021b1396cd8615e1abf62f60b67eb32dfce`
Push: `origin/main` updated `ffaa26e..2dd7c02`

Summary:
- Added `scripts/dev/build_overlap_priority_overlay_v1.py`.
- Added `scripts/dev/normalize_overlap_authorized_rows_v1.py`.
- Added `scripts/dev/compute_normalized_status_only_metrics_dryrun_v3.py`.
- Created `audits/overlap_priority_overlay_v1/` outputs.
- Applied maintainer-approved Option B to 45 overlap-denied rows.
- Resolved 45 overlap rows and left 0 overlap rows still blocked.
- Created a combined metric-input authorization overlay v1 with 175 authorized rows.
- Preserved 425 unresolved rows as unauthorized/unresolved denominator/accounting rows.
- Refreshed normalization for 45 newly authorized overlap rows and preserved the existing 130 normalized rows.
- Created `audits/normalized_status_only_metrics_dryrun_v3/` audit-only dry-run outputs for Generation Rate, Execution Coverage Rate, and Result Consistency Rate.
- Did not compute official metrics, render paper tables, compute timing metrics, implement SQLGlot parsing, update reports/results, change denominators, change paper results, change case membership, read new legacy evidence, or modify raw legacy evidence.

Files created:
- `scripts/dev/build_overlap_priority_overlay_v1.py`
- `scripts/dev/normalize_overlap_authorized_rows_v1.py`
- `scripts/dev/compute_normalized_status_only_metrics_dryrun_v3.py`
- `audits/overlap_priority_overlay_v1/overlap_priority_overlay_v1.csv`
- `audits/overlap_priority_overlay_v1/combined_metric_input_authorization_overlay_v1.csv`
- `audits/overlap_priority_overlay_v1/overlap_priority_overlay_v1_summary.json`
- `audits/overlap_priority_overlay_v1/overlap_priority_overlay_v1_report.md`
- `audits/overlap_priority_overlay_v1/overlap_priority_overlay_v1_checks.csv`
- `audits/overlap_priority_overlay_v1/combined_normalized_candidate_status_overlay_v1.csv`
- `audits/overlap_priority_overlay_v1/overlap_normalization_summary.json`
- `audits/overlap_priority_overlay_v1/overlap_normalization_report.md`
- `audits/overlap_priority_overlay_v1/overlap_normalization_checks.csv`
- `audits/normalized_status_only_metrics_dryrun_v3/normalized_status_only_metrics_dryrun_v3_table.csv`
- `audits/normalized_status_only_metrics_dryrun_v3/normalized_status_only_dryrun_v3_denominator_audit.csv`
- `audits/normalized_status_only_metrics_dryrun_v3/normalized_status_only_dryrun_v3_input_rows.csv`
- `audits/normalized_status_only_metrics_dryrun_v3/normalized_status_only_dryrun_v3_delta_vs_v2.csv`
- `audits/normalized_status_only_metrics_dryrun_v3/normalized_status_only_dryrun_v3_caveats.csv`
- `audits/normalized_status_only_metrics_dryrun_v3/normalized_status_only_metrics_dryrun_v3_report.md`
- `audits/normalized_status_only_metrics_dryrun_v3/normalized_status_only_metrics_dryrun_v3_checks.csv`
- `audits/normalized_status_only_metrics_dryrun_v3/normalized_status_only_metrics_dryrun_v3_summary.json`
- `audits/normalized_status_only_metrics_dryrun_v3/normalized_status_only_metrics_dryrun_v3_limitations.md`
- `docs/dev/OVERLAP_PRIORITY_OVERLAY_AND_DRYRUN_V3.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python -m py_compile scripts/dev/build_overlap_priority_overlay_v1.py`: passed.
- `python -m py_compile scripts/dev/normalize_overlap_authorized_rows_v1.py`: passed.
- `python -m py_compile scripts/dev/compute_normalized_status_only_metrics_dryrun_v3.py`: passed.
- `python scripts/dev/smoke_ledger_fixtures.py`: passed; 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, and 0 unexpected pass/fail rows.
- `python scripts/dev/build_overlap_priority_overlay_v1.py ...`: passed; resolved 45 overlap rows, 0 still blocked, 175 combined authorized rows.
- `python scripts/dev/normalize_overlap_authorized_rows_v1.py ...`: passed; preserved 130 existing normalized rows, normalized 45 overlap rows, combined 175 rows, and recorded 27 manual-mapping caveat rows.
- `python scripts/dev/compute_normalized_status_only_metrics_dryrun_v3.py ...`: passed; authorized 175 rows, used 94 inferred-generated rows, preserved 425 unresolved rows.
- JSON invariant checks for overlay, normalization, and v3 dry-run summaries: passed.
- CSV checks for required row counts, official/paper/audit flags, required metric families, no performance metric rows, and v2-v3 deltas: passed.
- Original parser ledger, v0 authorization overlay, v0 normalization overlay, and inference overlay were not modified.
- `git diff --check`: passed.
- `git status -sb`: only intended overlap overlay, dry-run v3, docs, scripts, and project-control changes before commit.

Task result:
- overlap priority overlay completed: yes
- overlap rows reviewed: 45
- newly authorized overlap rows: 45
- still-blocked overlap rows: 0
- v3 authorized input rows: 175
- official metrics computed: no
- audit-only dry-run metrics computed: yes
- paper tables rendered: no
- timing metrics computed: no
- Generation Rate dry-run created: yes
- Execution Coverage Rate dry-run created: yes
- Result Consistency Rate dry-run created: yes
- unresolved rows: 425
- inferred generated rows used: 94

Paper/denominator impact:
- reports changed: no
- results changed: no
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no

Next safe action:
- Review `audits/normalized_status_only_metrics_dryrun_v3/normalized_status_only_dryrun_v3_delta_vs_v2.csv` and `audits/normalized_status_only_metrics_dryrun_v3/normalized_status_only_dryrun_v3_caveats.csv`; if accepted, separately authorize official metric-readiness review or SQLGlot status evidence parsing.

### 2026-05-17 · 84c0c20 · SQLGlot sanitized non-timing projection and parser v1

Mode: bounded SQLGlot non-timing status projection and parser; audit-only dry-run v4; no official metrics; no timing/performance metrics; no reports/results; no paper tables
Legacy repo modified: no
Release repo modified: yes
Commit: `84c0c20c1effc15ddd4118905ad71e4e1786a0c3`
Push: `origin/main` updated `c6922a2..84c0c20`

Summary:
- Built a SQLGlot status source manifest from round1 triage/decision outputs.
- Approved only SGL011 for sanitized non-timing projection/parser use.
- Left P006 pending for deterministic engine expansion approval.
- Rejected or held out P009, SGL012, SGL013, P007, P008, and P010 for mixed-scope, duplicate, raw-log, timing/path, or route-level risks.
- Created two sanitized non-timing SQLGlot projections from SGL011 for `sqlglot_optimize` and `sqlglot_noop`.
- Parsed SQLGlot candidate status rows from sanitized projections only.
- Emitted 240 SQLGlot `rewrite_candidate_cell` audit rows.
- Filled 137 SQLGlot row-level non-timing status rows and left 103 SQLGlot rows unresolved.
- Built combined candidate status overlay v2 with 600 rows, 312 filled rows, and 288 unresolved rows.
- Created normalized status-only dry-run v4 outputs over the combined overlay, preserving the 600 planned candidate denominator.
- Did not compute official metrics, render paper tables, compute timing metrics, update reports/results, change denominators, change paper results, change case membership, modify the legacy repo, or modify raw legacy evidence.

Files created:
- `scripts/dev/build_sqlglot_status_source_manifest.py`
- `scripts/dev/build_sqlglot_non_timing_projection.py`
- `scripts/dev/parse_sqlglot_candidate_status_v1.py`
- `scripts/dev/build_combined_candidate_status_overlay_v2.py`
- `scripts/dev/compute_normalized_status_only_metrics_dryrun_v4.py`
- `audits/sqlglot_status_projection_v1/sqlglot_status_source_manifest.csv`
- `audits/sqlglot_status_projection_v1/sqlglot_status_source_manifest_summary.json`
- `audits/sqlglot_status_projection_v1/sqlglot_status_source_manifest_report.md`
- `audits/sqlglot_status_projection_v1/sqlglot_status_source_manifest_checks.csv`
- `audits/sqlglot_status_projection_v1/sqlglot_non_timing_projection_index.csv`
- `audits/sqlglot_status_projection_v1/projection_SGL011_sqlglot_optimize_non_timing.csv`
- `audits/sqlglot_status_projection_v1/projection_SGL011_sqlglot_noop_non_timing.csv`
- `audits/sqlglot_status_projection_v1/sqlglot_non_timing_projection_summary.json`
- `audits/sqlglot_status_projection_v1/sqlglot_non_timing_projection_report.md`
- `audits/sqlglot_status_projection_v1/sqlglot_non_timing_projection_checks.csv`
- `audits/sqlglot_candidate_status_parser_v1/sqlglot_candidate_status_ledger_v1.csv`
- `audits/sqlglot_candidate_status_parser_v1/sqlglot_candidate_status_parser_v1_summary.json`
- `audits/sqlglot_candidate_status_parser_v1/sqlglot_candidate_status_parser_v1_report.md`
- `audits/sqlglot_candidate_status_parser_v1/sqlglot_candidate_status_parser_v1_checks.csv`
- `audits/sqlglot_candidate_status_parser_v1/sqlglot_candidate_status_parser_v1_source_use_log.csv`
- `audits/sqlglot_candidate_status_parser_v1/sqlglot_candidate_status_parser_v1_limitations.md`
- `audits/sqlglot_candidate_status_parser_v1/ledger_validation/ledger_validation_results.csv`
- `audits/sqlglot_candidate_status_parser_v1/ledger_validation/ledger_validation_summary.json`
- `audits/sqlglot_candidate_status_parser_v1/ledger_validation/ledger_validation_report.md`
- `audits/combined_candidate_status_overlay_v2/combined_candidate_status_ledger_v2.csv`
- `audits/combined_candidate_status_overlay_v2/combined_candidate_status_overlay_v2_summary.json`
- `audits/combined_candidate_status_overlay_v2/combined_candidate_status_overlay_v2_report.md`
- `audits/combined_candidate_status_overlay_v2/combined_candidate_status_overlay_v2_checks.csv`
- `audits/normalized_status_only_metrics_dryrun_v4/normalized_status_only_metrics_dryrun_v4_table.csv`
- `audits/normalized_status_only_metrics_dryrun_v4/normalized_status_only_dryrun_v4_denominator_audit.csv`
- `audits/normalized_status_only_metrics_dryrun_v4/normalized_status_only_dryrun_v4_delta_vs_v3.csv`
- `audits/normalized_status_only_metrics_dryrun_v4/normalized_status_only_dryrun_v4_caveats.csv`
- `audits/normalized_status_only_metrics_dryrun_v4/normalized_status_only_metrics_dryrun_v4_report.md`
- `audits/normalized_status_only_metrics_dryrun_v4/normalized_status_only_metrics_dryrun_v4_checks.csv`
- `audits/normalized_status_only_metrics_dryrun_v4/normalized_status_only_metrics_dryrun_v4_summary.json`
- `audits/normalized_status_only_metrics_dryrun_v4/normalized_status_only_metrics_dryrun_v4_limitations.md`
- `docs/dev/SQLGLOT_STATUS_PROJECTION_AND_DRYRUN_V4.md`

Files modified:
- `scripts/dev/validate_ledger_csv.py`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python -m py_compile scripts/dev/build_sqlglot_status_source_manifest.py`: passed.
- `python -m py_compile scripts/dev/build_sqlglot_non_timing_projection.py`: passed.
- `python -m py_compile scripts/dev/parse_sqlglot_candidate_status_v1.py`: passed.
- `python -m py_compile scripts/dev/build_combined_candidate_status_overlay_v2.py`: passed.
- `python -m py_compile scripts/dev/compute_normalized_status_only_metrics_dryrun_v4.py`: passed.
- `python scripts/dev/smoke_ledger_fixtures.py`: passed; 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, and 0 unexpected pass/fail rows.
- `python scripts/dev/build_sqlglot_status_source_manifest.py ...`: passed; 10 manifest rows, 2 approved projection rows, 2 approved parser rows.
- `python scripts/dev/build_sqlglot_non_timing_projection.py ...`: passed; 2 projections, 137 total projection rows, 2 parser-ready projections.
- `python scripts/dev/parse_sqlglot_candidate_status_v1.py ...`: passed; 240 SQLGlot rows emitted, 137 filled, 103 unresolved.
- `python scripts/dev/validate_ledger_csv.py ...`: passed; 240 rows checked, 0 errors, 0 warnings.
- `python scripts/dev/build_combined_candidate_status_overlay_v2.py ...`: passed; 600 rows, 137 SQLGlot rows filled, 312 total filled rows, 288 unresolved rows.
- `python scripts/dev/compute_normalized_status_only_metrics_dryrun_v4.py ...`: passed; 312 dry-run input rows, 137 SQLGlot projection input rows, 600 planned candidate rows preserved.
- JSON invariant checks: passed.
- CSV checks: passed.
- `git diff --check`: passed.
- `git status -sb`: only intended SQLGlot projection/parser, combined overlay, dry-run v4, docs, scripts, validator-scope, and project-control changes before commit.

Task result:
- SQLGlot status source manifest completed: yes.
- Sanitized non-timing projections created: yes.
- SQLGlot candidate status parser completed: yes.
- SQLGlot rows filled: 137.
- SQLGlot rows unresolved: 103.
- Combined candidate status overlay v2 completed: yes.
- Combined filled rows: 312.
- Combined unresolved rows: 288.
- Official metrics computed: no.
- Audit-only dry-run metrics computed: yes.
- Paper tables rendered: no.
- Timing metrics computed: no.

Paper/denominator impact:
- reports changed: no.
- results changed: no.
- denominator changed: no.
- paper results changed: no.
- case membership changed: no.
- raw legacy evidence changed: no.

Next safe action:
- Review SQLGlot parser coverage and dry-run v4 delta/caveats; then separately decide whether to authorize additional sanitized SQLGlot non-timing sources for the remaining 103 unresolved SQLGlot rows or proceed to official metric-readiness review. Keep timing adapter work, reports/results updates, paper rendering, denominator changes, and paper-result changes separate.

### 2026-05-17 · ba1f3e7 · official_status_metrics_readiness_gate_v0

Mode: readiness-gate and decision packet; no official metrics; no paper tables; no timing/performance metrics; no reports/results
Legacy repo modified: no
Release repo modified: yes
Commit: `ba1f3e7a9d955e55b49f8bc21cfc1fede5e3e025`
Push: `origin/main` updated `6a3357b..ba1f3e7`

Summary:
- Reviewed current audit-only candidate-status evidence after SQLGlot projection/parser v1 and normalized dry-run v4.
- Reviewed combined candidate status overlay v2 with 600 planned rows, 312 filled rows, and 288 unresolved rows.
- Classified Generation Rate readiness as `blocked_needs_policy_decision`.
- Classified Execution Coverage Rate readiness as `ready_with_caveats`.
- Classified Result Consistency Rate readiness as `ready_with_caveats`.
- Created denominator visibility requirements confirming unresolved rows must remain visible, denominator reduction is forbidden, and no global leaderboard is allowed.
- Created official-computation risk register, future implementation scope proposal, and maintainer decision template.
- Did not compute official metrics, render paper tables, compute timing metrics, update reports/results, change denominators, change paper results, change case membership, modify the legacy repo, or modify raw legacy evidence.

Files created:
- `audits/official_status_metrics_readiness_gate_v0/official_status_metrics_readiness_summary.md`
- `audits/official_status_metrics_readiness_gate_v0/status_metric_readiness_matrix.csv`
- `audits/official_status_metrics_readiness_gate_v0/method_status_coverage_matrix.csv`
- `audits/official_status_metrics_readiness_gate_v0/denominator_visibility_plan.csv`
- `audits/official_status_metrics_readiness_gate_v0/official_computation_risk_register.md`
- `audits/official_status_metrics_readiness_gate_v0/official_status_metrics_implementation_scope_proposal.md`
- `audits/official_status_metrics_readiness_gate_v0/official_status_metrics_readiness_decision_template.md`
- `audits/official_status_metrics_readiness_gate_v0/official_status_metrics_readiness_summary.json`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python scripts/dev/smoke_ledger_fixtures.py`: passed; 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, and 0 unexpected pass/fail rows.
- JSON invariant checks: passed.
- CSV checks: passed for required metric families, five method routes, denominator visibility flags, and no official/paper-result claims.
- `git diff --check`: passed.
- `git status -sb`: only intended readiness-gate audit outputs and project-control changes before commit.

Task result:
- official metrics computed: no.
- paper tables rendered: no.
- timing metrics computed: no.
- reports changed: no.
- results changed: no.
- denominator changed: no.
- paper results changed: no.
- raw legacy evidence changed: no.
- combined filled rows: 312.
- combined unresolved rows: 288.
- Generation Rate readiness: blocked_needs_policy_decision.
- Execution Coverage Rate readiness: ready_with_caveats.
- Result Consistency Rate readiness: ready_with_caveats.

Next safe action:
- Review the readiness matrix and decide whether to authorize a limited official status-only metrics implementation with caveats, approve another audit-only dry run, or defer until Generation Rate policy/evidence gaps and unresolved rows are reduced.

### 2026-05-18 · 38c0644 · official_status_metrics_v0_limited_execution_consistency

Mode: limited official status-metrics computation; Execution Coverage Rate and Result Consistency Rate only; Generation Rate blocked; no paper tables; no timing/performance metrics; no reports/results
Legacy repo modified: no
Release repo modified: yes
Commit: `38c0644293aa63754b098972e97a960ef690a0af`
Push: `origin/main` updated `0d60a22..38c0644`

Summary:
- Implemented `scripts/dev/compute_official_status_metrics_limited.py`.
- Computed official limited status metrics only for Execution Coverage Rate and Result Consistency Rate from the authorized normalized status overlay.
- Wrote blocked Generation Rate rows with `official_metric_computed=false` and blocker `inferred_generated_policy_not_official_and_sqlglot_generated_ready_gap`.
- Preserved 600 planned denominator rows, 175 authorized input rows, and 425 unauthorized/unresolved denominator-visible rows.
- Marked metric outputs as `paper_result=false` and guarded against global leaderboard output.
- Did not compute Generation Rate, timing/performance metrics, GM_Speedup, Speedup Ratio Percentiles, Semantic Equivalence Rate, Attribution Coverage, or Cross-Engine metrics.
- Did not render paper tables, update reports/results, change denominators, change paper results, change case membership, modify the legacy repo, or modify raw legacy evidence.

Files created:
- `scripts/dev/compute_official_status_metrics_limited.py`
- `audits/official_status_metrics_v0_limited/official_status_metrics_v0_limited_table.csv`
- `audits/official_status_metrics_v0_limited/official_status_metrics_denominator_audit.csv`
- `audits/official_status_metrics_v0_limited/official_status_metrics_input_rows.csv`
- `audits/official_status_metrics_v0_limited/official_status_metrics_blocked_generation_rate.csv`
- `audits/official_status_metrics_v0_limited/official_status_metrics_v0_limited_report.md`
- `audits/official_status_metrics_v0_limited/official_status_metrics_v0_limited_checks.csv`
- `audits/official_status_metrics_v0_limited/official_status_metrics_v0_limited_summary.json`
- `audits/official_status_metrics_v0_limited/official_status_metrics_v0_limited_limitations.md`
- `docs/dev/OFFICIAL_STATUS_METRICS_V0_LIMITED.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python -m py_compile scripts/dev/compute_official_status_metrics_limited.py`: passed.
- `python scripts/dev/smoke_ledger_fixtures.py`: passed; 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, and 0 unexpected pass/fail rows.
- `python scripts/dev/compute_official_status_metrics_limited.py ...`: passed; 600 planned candidate rows, 175 authorized input rows, 7 execution success rows, 2 consistency success rows, and Generation Rate blocked.
- JSON invariant checks: passed.
- CSV checks: passed for required metric families, blocked Generation Rate rows, no speedup metrics, `paper_result=false`, `no_global_leaderboard=true`, denominator preservation, and denominator reduction/global leaderboard denial.
- `git diff --check`: passed.

Task result:
- official status metrics computed: yes.
- official Generation Rate computed: no.
- official Execution Coverage Rate computed: yes.
- official Result Consistency Rate computed: yes.
- paper tables rendered: no.
- timing metrics computed: no.
- reports changed: no.
- results changed: no.
- denominator changed: no.
- paper results changed: no.
- case membership changed: no.
- raw legacy evidence changed: no.

Next safe action:
- Review the limited official status-metrics outputs, then separately decide whether to authorize SQLGlot metric-input expansion, resolve Generation Rate policy/evidence gaps, or prepare a paper-rendering decision packet.

### 2026-05-18 · 6a502bf · official_status_metrics_v0_limited_closeout_and_paper_rendering_decision_packet

Mode: closeout and decision packet; no new metrics; no paper tables; no timing/performance metrics; no reports/results
Legacy repo modified: no
Release repo modified: yes
Commit: `6a502bf6d74e9a0f54cb34961ffe29f9c35c4e12`
Push: `origin/main` updated `f9afe3e..6a502bf`

Summary:
- Reviewed the existing `official_status_metrics_v0_limited` outputs without recomputing metrics.
- Confirmed official Execution Coverage Rate and official Result Consistency Rate were previously computed in the limited official task.
- Confirmed official Generation Rate remains blocked by `inferred_generated_policy_not_official_and_sqlglot_generated_ready_gap`.
- Confirmed denominator partitions remain visible: 600 planned rows, 175 authorized input rows, and 425 unauthorized/unresolved rows in the limited official output.
- Prepared closeout matrix, denominator review, paper-rendering decision matrix, Generation Rate blocker options, renderer scope proposal, and risk register.
- Did not render paper tables, update reports/results, change denominators, change paper results, change case membership, modify the legacy repo, or modify raw legacy evidence.

Files created:
- `audits/official_status_metrics_v0_limited_closeout/official_status_metrics_v0_limited_closeout_summary.md`
- `audits/official_status_metrics_v0_limited_closeout/limited_status_metrics_closeout_matrix.csv`
- `audits/official_status_metrics_v0_limited_closeout/limited_status_metrics_denominator_review.csv`
- `audits/official_status_metrics_v0_limited_closeout/limited_status_metrics_paper_rendering_decision_matrix.csv`
- `audits/official_status_metrics_v0_limited_closeout/generation_rate_blocker_resolution_options.md`
- `audits/official_status_metrics_v0_limited_closeout/official_status_metrics_report_renderer_scope_proposal.md`
- `audits/official_status_metrics_v0_limited_closeout/official_status_metrics_closeout_risk_register.md`
- `audits/official_status_metrics_v0_limited_closeout/official_status_metrics_v0_limited_closeout_summary.json`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python scripts/dev/smoke_ledger_fixtures.py`: passed; 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, and 0 unexpected pass/fail rows.
- JSON invariant checks: passed.
- CSV checks: passed for required metric families, Generation Rate blocked, limited official status metrics marked previously computed, denominator reduction/global leaderboard denied, paper rendering global leaderboard denied, and no `paper_result=true` rows.
- `git diff --check`: passed.

Task result:
- new metrics computed: no.
- official Generation Rate computed: no.
- official Execution Coverage Rate already computed: yes.
- official Result Consistency Rate already computed: yes.
- paper tables rendered: no.
- reports changed: no.
- results changed: no.
- denominator changed: no.
- paper results changed: no.
- case membership changed: no.
- raw legacy evidence changed: no.

Next safe action:
- Review the closeout paper-rendering decision matrix and decide whether to resolve Generation Rate evidence/policy before any paper-facing main table or authorize a renderer-planning task limited to status-only outputs with blocked Generation Rate and denominator partitions visible.

### 2026-05-18 · ac4be19 · A_line_final_metrics_closure_plan_v0

Mode: A-line final closure planning; no new metrics; no paper tables; no timing/performance implementation; no reports/results
Legacy repo modified: no
Release repo modified: yes
Commit: `ac4be19147710400a33ae044f867af39fc716ecf`
Push: `origin/main` updated `7e7f56c..ac4be19`

Summary:
- Created an A-line final metrics closure planning packet under `audits/a_line_final_metrics_closure_plan_v0/`.
- Classified all ten Metrics Contract v1 primary metrics.
- Classified Execution Coverage Rate and Result Consistency Rate as official limited v0 metrics.
- Classified Generation Rate, Semantic Equivalence Rate, GM_Speedup, and Speedup Ratio Percentiles as blocked by policy/evidence/adapter gaps.
- Classified Speedup Retention as N.A. for v0.
- Classified Attribution Coverage, Cross-Engine Execution, and Cross-Engine Consistency as post-release backlog.
- Recommended three core remaining A-line tasks: Generation Rate blocker decision, non-status metric N.A./backlog closure bundle, and final renderer input package.
- Did not compute new metrics, recompute official metrics, render paper tables, update reports/results, change denominators, change paper results, change case membership, modify the legacy repo, or modify raw legacy evidence.

Files created:
- `audits/a_line_final_metrics_closure_plan_v0/a_line_final_metrics_closure_summary.md`
- `audits/a_line_final_metrics_closure_plan_v0/a_line_metric_state_matrix.csv`
- `audits/a_line_final_metrics_closure_plan_v0/a_line_remaining_task_sequence.csv`
- `audits/a_line_final_metrics_closure_plan_v0/a_line_metric_blocker_register.csv`
- `audits/a_line_final_metrics_closure_plan_v0/a_line_v0_treatment_decision_matrix.csv`
- `audits/a_line_final_metrics_closure_plan_v0/a_line_final_renderer_input_manifest_preview.csv`
- `audits/a_line_final_metrics_closure_plan_v0/a_line_closeout_risk_register.md`
- `audits/a_line_final_metrics_closure_plan_v0/a_line_final_closure_recommendation.md`
- `audits/a_line_final_metrics_closure_plan_v0/a_line_final_metrics_closure_summary.json`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python scripts/dev/smoke_ledger_fixtures.py`: passed; 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, and 0 unexpected pass/fail rows.
- JSON invariant checks: passed.
- CSV checks: passed; both metric-state and v0-treatment matrices include all ten Metrics Contract v1 primary metrics, and the remaining task sequence has task rows.
- `git diff --check`: passed.

Task result:
- new metrics computed: no.
- paper tables rendered: no.
- reports changed: no.
- results changed: no.
- denominator changed: no.
- paper results changed: no.
- case membership changed: no.
- raw legacy evidence changed: no.
- official metrics available count: 2.
- blocked metrics count: 4.
- N.A. metrics count: 1.
- post-release metrics count: 3.

Next safe action:
- Run `generation_rate_blocker_final_decision_v0` as a policy/evidence decision packet with no metric computation, no paper rendering, and no reports/results writes.

### 2026-05-18 · 1a3853a · generation_rate_blocker_final_decision_v0

Mode: policy/evidence decision packet; no metrics computation; no paper tables; no reports/results; no denominator changes
Legacy repo modified: no
Release repo modified: yes
Commit: `1a3853aebc478d8815725f77f83fb6e742459f9f`
Push: `origin/main` updated `2603198..1a3853a`

Summary:
- Created `audits/generation_rate_blocker_final_decision_v0/` decision packet.
- Reviewed Generation Rate blocker state from Metrics Contract v1, status inference policy, official limited status metrics, closeout, A-line closure, inference overlays, and dry-run v4 artifacts.
- Recommended public v0 treatment: `report_as_blocked`.
- Preserved audit-only status for 94 `inferred_generated=true` rows.
- Confirmed Generation Rate was not computed and no official metrics were computed.
- Confirmed no paper tables were rendered and no reports/results were changed.
- Confirmed denominator values, paper results, case membership, and raw legacy evidence were unchanged.

Files created:
- `audits/generation_rate_blocker_final_decision_v0/generation_rate_blocker_decision_summary.md`
- `audits/generation_rate_blocker_final_decision_v0/generation_rate_decision_matrix.csv`
- `audits/generation_rate_blocker_final_decision_v0/generation_rate_evidence_gap_summary.csv`
- `audits/generation_rate_blocker_final_decision_v0/generation_rate_v0_treatment_record.csv`
- `audits/generation_rate_blocker_final_decision_v0/generation_rate_policy_questions_for_team.md`
- `audits/generation_rate_blocker_final_decision_v0/generation_rate_future_resolution_plan.md`
- `audits/generation_rate_blocker_final_decision_v0/generation_rate_blocker_decision_summary.json`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python scripts/dev/smoke_ledger_fixtures.py`: passed; 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, and 0 unexpected pass/fail rows.
- JSON invariant checks: passed.
- CSV checks: passed for Options A/B/C/D, `official_metric_computed_now=false`, no Generation Rate computation claims, no paper-rendering claims, and no global leaderboard allowance.
- `git diff --check`: passed.

Task result:
- Generation Rate computed: no.
- official metrics computed: no.
- paper tables rendered: no.
- reports changed: no.
- results changed: no.
- denominator changed: no.
- paper results changed: no.
- case membership changed: no.
- raw legacy evidence changed: no.
- recommended v0 treatment: `report_as_blocked`.

Next safe action:
- Run `non_status_metric_na_backlog_closure_bundle_v0` to close Semantic Equivalence, performance, attribution, cross-engine, and Speedup Retention as blocked, N.A., or post-release without implementing adapters, computing metrics, rendering paper tables, updating reports/results, changing denominators, or changing paper results.

### 2026-05-18 · c840a5e · non_status_metric_na_backlog_closure_bundle_v0

Mode: A-line non-status metric closure; no new metrics; no adapters; no paper tables; no reports/results
Legacy repo modified: no
Release repo modified: yes
Commit: `c840a5e990b9998ab458fed24261e7a5620827bb`
Push: `origin/main` updated `1a68b7b..c840a5e`

Summary:
- Created `audits/non_status_metric_na_backlog_closure_bundle_v0/` closure packet.
- Reviewed seven non-status Metrics Contract v1 primary metrics not covered by limited official status metrics.
- Classified Semantic Equivalence Rate as audit-only support for v0.
- Classified GM_Speedup and Speedup Ratio Percentiles as blocked for v0.
- Classified Attribution Coverage, Cross-Engine Execution, and Cross-Engine Consistency as post-release backlog.
- Classified Speedup Retention as N.A. for v0.
- Did not compute new metrics, recompute official metrics, implement adapters, render paper tables, update reports/results, change denominators, change paper results, change case membership, modify the legacy repo, or modify raw legacy evidence.

Files created:
- `audits/non_status_metric_na_backlog_closure_bundle_v0/non_status_metric_closure_summary.md`
- `audits/non_status_metric_na_backlog_closure_bundle_v0/non_status_metric_v0_treatment_matrix.csv`
- `audits/non_status_metric_na_backlog_closure_bundle_v0/non_status_metric_blocker_register.csv`
- `audits/non_status_metric_na_backlog_closure_bundle_v0/non_status_metric_na_record.csv`
- `audits/non_status_metric_na_backlog_closure_bundle_v0/non_status_metric_post_release_backlog.csv`
- `audits/non_status_metric_na_backlog_closure_bundle_v0/non_status_metric_audit_support_manifest.csv`
- `audits/non_status_metric_na_backlog_closure_bundle_v0/non_status_metric_renderer_manifest_preview.csv`
- `audits/non_status_metric_na_backlog_closure_bundle_v0/non_status_metric_closure_risk_register.md`
- `audits/non_status_metric_na_backlog_closure_bundle_v0/non_status_metric_closure_summary.json`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python scripts/dev/smoke_ledger_fixtures.py`: passed; 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, and 0 unexpected pass/fail rows.
- JSON invariant checks: passed.
- CSV checks: passed; treatment matrix includes all seven non-status metrics, N.A. record includes Speedup Retention, post-release and renderer preview files have headers, and no row claims new metrics or paper tables.
- `git diff --check`: passed.

Task result:
- new metrics computed: no.
- official metrics computed: no.
- paper tables rendered: no.
- reports changed: no.
- results changed: no.
- denominator changed: no.
- paper results changed: no.
- case membership changed: no.
- raw legacy evidence changed: no.
- non-status metrics reviewed: 7.
- metrics reported blocked: 2.
- metrics reported N.A.: 1.
- metrics deferred post-release: 3.
- metrics retained as audit-only support: 1.

Next safe action:
- Run `a_line_final_renderer_input_package_v0` to package official limited metrics, blocked metrics, N.A. records, audit-only support, and post-release backlog decisions for a future renderer without rendering paper tables, updating reports/results, changing denominators, or changing paper results.

### 2026-05-18 · ab2ba5b · a_line_final_renderer_input_package_v0

Mode: A-line final renderer-input package; no new metrics; no paper tables; no reports/results
Legacy repo modified: no
Release repo modified: yes
Commit: `ab2ba5b1b82507119f34f325c1f824b13820202f`
Push: `origin/main` updated `e35d740..ab2ba5b`

Summary:
- Created `audits/a_line_final_renderer_input_package_v0/` renderer-input package.
- Represented all ten Metrics Contract v1 primary metrics for future renderer planning.
- Packaged two limited official metric inputs: Execution Coverage Rate and Result Consistency Rate.
- Packaged three blocked metric records: Generation Rate, GM_Speedup, and Speedup Ratio Percentiles.
- Packaged one N.A. metric record: Speedup Retention.
- Packaged one audit-only support metric record: Semantic Equivalence Rate.
- Packaged three post-release backlog records: Attribution Coverage, Cross-Engine Execution, and Cross-Engine Consistency.
- Confirmed A-line v0 is ready for B-line handoff after this package.
- Did not compute new metrics, recompute official metrics, render paper tables, update reports/results, change denominators, change paper results, change case membership, modify the legacy repo, or modify raw legacy evidence.

Files created:
- `audits/a_line_final_renderer_input_package_v0/a_line_final_renderer_input_package_summary.md`
- `audits/a_line_final_renderer_input_package_v0/a_line_final_metric_renderer_manifest.csv`
- `audits/a_line_final_renderer_input_package_v0/a_line_official_limited_metric_inputs.csv`
- `audits/a_line_final_renderer_input_package_v0/a_line_blocked_metric_records.csv`
- `audits/a_line_final_renderer_input_package_v0/a_line_na_and_post_release_records.csv`
- `audits/a_line_final_renderer_input_package_v0/a_line_audit_support_records.csv`
- `audits/a_line_final_renderer_input_package_v0/a_line_denominator_and_caveat_package.md`
- `audits/a_line_final_renderer_input_package_v0/a_line_final_renderer_package_validation.csv`
- `audits/a_line_final_renderer_input_package_v0/a_line_final_renderer_next_steps.md`
- `audits/a_line_final_renderer_input_package_v0/a_line_final_renderer_input_package_summary.json`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python scripts/dev/smoke_ledger_fixtures.py`: passed; 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, and 0 unexpected pass/fail rows.
- JSON invariant checks: passed.
- CSV checks: passed; manifest includes all ten Metrics Contract v1 primary metrics, official limited inputs include Execution Coverage Rate and Result Consistency Rate, blocked records include Generation Rate, GM_Speedup, and Speedup Ratio Percentiles, N.A./post-release records include the expected four metrics, audit support includes Semantic Equivalence Rate, validation CSV has no FAIL rows, and no row claims new metrics or paper tables.
- `git diff --check`: passed.

Task result:
- new metrics computed: no.
- paper tables rendered: no.
- reports changed: no.
- results changed: no.
- denominator changed: no.
- paper results changed: no.
- case membership changed: no.
- raw legacy evidence changed: no.
- metrics represented: 10.
- official limited metrics: 2.
- blocked metrics: 3.
- N.A. metrics: 1.
- audit-support metrics: 1.
- post-release metrics: 3.
- A-line ready for B-line handoff: yes.

Next safe action:
- Run `b_line_reproduction_report_renderer_design_v0` to design the reproduction/report renderer boundary and validation gates without rendering paper tables, writing `reports/` or `results/`, computing metrics, changing denominators, or changing paper results.

### 2026-05-18 · de903f7 · overnight_non_common_core_case_package_standardization_wave_001

Mode: bounded non-Common-core case package standardization; no case-set membership update; no metrics; no DB validation; no reports/results
Legacy repo modified: no
Release repo modified: yes
Commit: `de903f7f50c320445481e77fe2db8ec3e858c025`
Push: `origin/main` updated `00bdf2a..de903f7`

Summary:
- Considered 30 non-Common-core candidate cases from existing governance and staged/backlog preview artifacts.
- Attempted two low-risk zero-hygiene-risk cases.
- Created canonical package directories for `PORT_0002` and `PERF_0029`.
- Deferred 28 considered cases because static governance flagged local-path, raw-log/debug, retained-runs, or public-hygiene risk.
- Created wave 001 audit outputs under `audits/overnight_non_common_core_case_package_standardization_wave_001/`.
- Did not update `case_sets/`, `inventory/`, reports, results, denominators, paper results, metrics, Common-core case packages, or raw legacy evidence.

Files created:
- `cases/PORT/PORT_0002/` canonical package directory with 44 files.
- `cases/PERF/PERF_0029/` canonical package directory with 41 files.
- `audits/overnight_non_common_core_case_package_standardization_wave_001/overnight_wave_summary.md`
- `audits/overnight_non_common_core_case_package_standardization_wave_001/overnight_wave_case_queue.csv`
- `audits/overnight_non_common_core_case_package_standardization_wave_001/overnight_wave_completed_cases.csv`
- `audits/overnight_non_common_core_case_package_standardization_wave_001/overnight_wave_deferred_cases.csv`
- `audits/overnight_non_common_core_case_package_standardization_wave_001/overnight_wave_hygiene_findings.csv`
- `audits/overnight_non_common_core_case_package_standardization_wave_001/overnight_wave_runs_retention_index.csv`
- `audits/overnight_non_common_core_case_package_standardization_wave_001/overnight_wave_validation_results.csv`
- `audits/overnight_non_common_core_case_package_standardization_wave_001/overnight_wave_summary.json`
- `audits/overnight_non_common_core_case_package_standardization_wave_001/future_followup_prompt.md`
- `audits/overnight_non_common_core_case_package_standardization_wave_001/canonical_case_validator_results.csv`
- `audits/overnight_non_common_core_case_package_standardization_wave_001/canonical_case_validator_summary.json`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python scripts/dev/validate_case_package.py --mode canonical-case --case cases/PORT/PORT_0002 --case cases/PERF/PERF_0029`: passed, 2/2.
- YAML/JSON/CSV invariant checks: passed.
- Public hygiene scan: passed.
- `python scripts/dev/smoke_ledger_fixtures.py`: passed; 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, and 0 unexpected pass/fail rows.
- `git diff --check`: passed.

Task result:
- cases considered: 30.
- cases attempted: 2.
- cases completed: 2.
- cases deferred: 28.
- completed case ids: `PORT_0002`, `PERF_0029`.
- deferred case ids: `PERF_0002`, `CONS_0031`, `CONS_0034`, `PERF_0009`, `PERF_0010`, `PERF_0011`, `PERF_0012`, `PERF_0014`, `PERF_0015`, `PERF_0016`, `PERF_0018`, `PERF_0020`, `PERF_0021`, `PERF_0022`, `PERF_0023`, `PERF_0025`, `PERF_0026`, `PERF_0036`, `PERF_0038`, `PERF_0043`, `PERF_0044`, `PERF_0047`, `PERF_0050`, `PERF_0053`, `PERF_0063`, `PERF_0065`, `PERF_0066`, `PERF_0076`.
- case_sets changed: no.
- reports changed: no.
- results changed: no.
- denominator changed: no.
- paper results changed: no.
- case membership changed: no.
- raw legacy evidence changed: no.
- metrics computed: no.
- paper tables rendered: no.

Next safe action:
- Review wave 001 completed packages and deferred hygiene dossiers; decide whether to run `overnight_non_common_core_case_package_standardization_wave_002` or separately authorize staged/backlog membership governance without changing Common-core v0 membership, denominators, reports/results, paper results, metrics, or raw legacy evidence.

### 2026-05-18 · d3a4df7 · wave001_readme_public_polish_and_wave002_selection

Mode: public README polish plus wave review/selection; no case migration; no metrics; no reports/results
Legacy repo modified: no
Release repo modified: yes
Commit: `d3a4df7b876d839b0a2db1a5639b23bbc28b71f9`
Push: `origin/main` updated `5023601..d3a4df7`

Summary:
- Rewrote the public-facing README files for `PORT_0002` and `PERF_0029` to remove construction-process wording and describe stable package scope, contents, evidence boundary, and benchmark boundary.
- Reviewed wave 001 completed and deferred dossiers.
- Classified all 28 wave 001 deferred cases as `wave_002_policy_approval_needed`.
- Identified 0 current auto-migration candidates under the existing fail-closed hygiene policy.
- Prepared a wave 002 batch plan, policy questions, candidate selection CSV, and future prompt.
- Did not migrate cases, update `case_sets/`, update reports/results, change denominators, change paper results, compute metrics, render paper tables, modify the legacy repo, or modify raw legacy evidence.

Files created:
- `audits/wave001_readme_public_polish_and_wave002_selection/readme_public_polish_summary.md`
- `audits/wave001_readme_public_polish_and_wave002_selection/readme_public_polish_checks.csv`
- `audits/wave001_readme_public_polish_and_wave002_selection/wave001_review_summary.md`
- `audits/wave001_readme_public_polish_and_wave002_selection/wave001_deferred_reason_groups.csv`
- `audits/wave001_readme_public_polish_and_wave002_selection/wave002_candidate_selection.csv`
- `audits/wave001_readme_public_polish_and_wave002_selection/wave002_batch_plan.md`
- `audits/wave001_readme_public_polish_and_wave002_selection/wave002_policy_approval_questions.md`
- `audits/wave001_readme_public_polish_and_wave002_selection/wave002_selection_summary.json`
- `audits/wave001_readme_public_polish_and_wave002_selection/future_wave002_prompt.md`

Files modified:
- `cases/PORT/PORT_0002/README.md`
- `cases/PERF/PERF_0029/README.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python scripts/dev/smoke_ledger_fixtures.py`: passed; 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, and 0 unexpected pass/fail rows.
- JSON invariant check: passed.
- README forbidden-term checks: passed.
- CSV checks: passed; README check rows are PASS for both files, wave 002 selection covers all 28 deferred cases, and summary counts match the CSV.
- Boundary checks: passed; no files under `case_sets/`, `reports/`, or `results/` changed.
- `git diff --check`: passed.

Task result:
- READMEs polished: `PORT_0002`, `PERF_0029`.
- Wave 001 deferred cases reviewed: 28.
- Wave 002 auto candidates: 0.
- Wave 002 policy approval needed: 28.
- Wave 002 manual review required: 0.
- Wave 002 backlog defer: 0.
- case_sets changed: no.
- reports changed: no.
- results changed: no.
- denominator changed: no.
- paper results changed: no.
- case membership changed: no.
- raw legacy evidence changed: no.
- metrics computed: no.
- paper tables rendered: no.

Next safe action:
- Answer the wave 002 policy approval questions, then authorize `overnight_non_common_core_case_package_standardization_wave_002` only for policy-approved cases while keeping Common-core v0 membership, `case_sets/`, denominators, reports/results, paper results, metrics, paper tables, and raw legacy evidence unchanged.

### 2026-05-18 · dd7f387 · wave002_policy_approval_readme_standardization_and_validation_schema_guard_v0

Mode: policy approval plus README standardization and package-validation schema guard; no case migration; no metrics; no reports/results
Legacy repo modified: no
Release repo modified: yes
Commit: `dd7f387552dfafcf9646c5d74ef7df074423f42f`
Push: `origin/main` updated `ee50168..dd7f387`

Summary:
- Created `repository_spec/case_readme_public_template_v1.md`.
- Created `repository_spec/package_validation_summary_schema_v1.md`.
- Standardized 42 existing case README files under `cases/*/*/README.md`.
- Audited 42 case-local `evidence/package_validation_summary.json` files without modifying them.
- Answered nine wave 002 policy questions in batch.
- Reclassified all 28 wave 001 deferred cases as wave 002 policy-approved candidates for a future separately authorized package generation task.
- Did not migrate cases, update `case_sets/`, update reports/results, change denominators, change paper results, compute metrics, render paper tables, modify the legacy repo, or modify raw legacy evidence.

Files created:
- `repository_spec/case_readme_public_template_v1.md`
- `repository_spec/package_validation_summary_schema_v1.md`
- `audits/wave002_policy_readme_schema_guard_v0/readme_standardization_summary.md`
- `audits/wave002_policy_readme_schema_guard_v0/readme_standardization_checks.csv`
- `audits/wave002_policy_readme_schema_guard_v0/package_validation_summary_audit.csv`
- `audits/wave002_policy_readme_schema_guard_v0/package_validation_summary_schema_guard_report.md`
- `audits/wave002_policy_readme_schema_guard_v0/wave002_policy_approval_record.md`
- `audits/wave002_policy_readme_schema_guard_v0/wave002_policy_approval_matrix.csv`
- `audits/wave002_policy_readme_schema_guard_v0/wave002_candidate_selection_after_policy.csv`
- `audits/wave002_policy_readme_schema_guard_v0/wave002_policy_unlocked_batch_plan.md`
- `audits/wave002_policy_readme_schema_guard_v0/future_wave002_policy_approved_prompt.md`
- `audits/wave002_policy_readme_schema_guard_v0/wave002_policy_readme_schema_guard_summary.json`

Files modified:
- 42 case README files under `cases/*/*/README.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python scripts/dev/smoke_ledger_fixtures.py`: passed; 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, and 0 unexpected pass/fail rows.
- Summary JSON invariant check: passed.
- README forbidden-term and required-section checks: passed for 42 case README files.
- CSV checks: passed; README checks cover every case README, package-validation audit covers all 42 package summaries, after-policy selection covers all 28 deferred wave 001 cases, and the policy matrix records nine decisions.
- Boundary checks: passed; no `case_sets/`, `reports/`, `results/`, denominator, paper-result, raw legacy evidence, or package-validation-summary JSON files were modified.
- JSON parse checks: passed for the new summary JSON and all existing case-local package-validation summaries.
- `git diff --check`: passed.

Task result:
- READMEs standardized: 42.
- package_validation_summary schema guard created: yes.
- package_validation_summary files audited: 42.
- package_validation_summary files modified: no.
- Wave 002 policy questions answered: 9.
- Wave 002 auto/policy-approved candidates: 28.
- Wave 002 manual review required: 0.
- Wave 002 backlog defer: 0.
- case_sets changed: no.
- reports changed: no.
- results changed: no.
- denominator changed: no.
- paper results changed: no.
- case membership changed: no.
- raw legacy evidence changed: no.
- metrics computed: no.
- paper tables rendered: no.

Next safe action:
- Run `overnight_non_common_core_case_package_standardization_wave_002_policy_approved` using the after-policy candidate queue, README template v1, and package_validation_summary schema guard, without changing `case_sets/`, denominators, reports/results, paper results, metrics, paper tables, or raw legacy evidence.

### 2026-05-18 · 5608bba · overnight_non_common_core_case_package_standardization_wave_002_policy_approved

Mode: bounded policy-approved non-Common-core case package standardization; no case-set membership update; no denominator update; no metrics; no reports/results
Legacy repo modified: no
Release repo modified: yes
Commit: `5608bba57ee02943ac8e69594920160fcac9f65d`
Push: `origin/main` updated `9f3b050..5608bba`

Summary:
- Used `audits/wave002_policy_readme_schema_guard_v0/wave002_candidate_selection_after_policy.csv` as the only candidate source.
- Attempted all 28 `wave_002_policy_approved_candidate` cases.
- Completed canonical package standardization for 28 non-Common-core cases: `PERF_0002`, `CONS_0031`, `CONS_0034`, `PERF_0009`, `PERF_0010`, `PERF_0011`, `PERF_0012`, `PERF_0014`, `PERF_0015`, `PERF_0016`, `PERF_0018`, `PERF_0020`, `PERF_0021`, `PERF_0022`, `PERF_0023`, `PERF_0025`, `PERF_0026`, `PERF_0036`, `PERF_0038`, `PERF_0043`, `PERF_0044`, `PERF_0047`, `PERF_0050`, `PERF_0053`, `PERF_0063`, `PERF_0065`, `PERF_0066`, and `PERF_0076`.
- Deferred cases: none.
- Created public-facing case packages with README template v1, package-validation summary schema v1, canonical SQL/schema/checker/evidence/metadata/validation layout, and archive-mapped legacy run retention.
- Did not copy raw legacy run directories wholesale.
- Did not copy raw logs, stdout/stderr/debug payloads, private runtime traces, or raw local-path artifacts.
- Did not update `case_sets/`, update reports/results, change denominators, change paper results, compute metrics, render paper tables, modify the legacy repo, or modify raw legacy evidence.

Files created:
- 28 case package directories under `cases/CONS/` and `cases/PERF/` for the completed wave 002 cases.
- `audits/overnight_non_common_core_case_package_standardization_wave_002_policy_approved/wave002_policy_approved_summary.md`
- `audits/overnight_non_common_core_case_package_standardization_wave_002_policy_approved/wave002_policy_approved_case_queue.csv`
- `audits/overnight_non_common_core_case_package_standardization_wave_002_policy_approved/wave002_policy_approved_completed_cases.csv`
- `audits/overnight_non_common_core_case_package_standardization_wave_002_policy_approved/wave002_policy_approved_deferred_cases.csv`
- `audits/overnight_non_common_core_case_package_standardization_wave_002_policy_approved/wave002_policy_approved_hygiene_findings.csv`
- `audits/overnight_non_common_core_case_package_standardization_wave_002_policy_approved/wave002_policy_approved_runs_retention_index.csv`
- `audits/overnight_non_common_core_case_package_standardization_wave_002_policy_approved/wave002_policy_approved_package_validation_summary_audit.csv`
- `audits/overnight_non_common_core_case_package_standardization_wave_002_policy_approved/wave002_policy_approved_readme_checks.csv`
- `audits/overnight_non_common_core_case_package_standardization_wave_002_policy_approved/wave002_policy_approved_validation_results.csv`
- `audits/overnight_non_common_core_case_package_standardization_wave_002_policy_approved/wave002_policy_approved_summary.json`
- `audits/overnight_non_common_core_case_package_standardization_wave_002_policy_approved/wave003_followup_prompt.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python scripts/dev/validate_case_package.py --mode canonical-case`: passed for 28/28 completed cases.
- `python scripts/dev/smoke_ledger_fixtures.py`: passed; 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, and 0 unexpected pass/fail rows.
- Summary JSON invariant check: passed.
- YAML/JSON parse checks: passed for new package and audit files.
- README forbidden-term checks: passed for 28 completed package READMEs.
- package_validation_summary schema checks: passed for 28 completed package summaries.
- Boundary checks: passed; no `case_sets/`, `reports/`, `results/`, denominator, paper-result, raw legacy evidence, or Common-core package files were modified.
- `git diff --check` and `git diff --cached --check`: passed.

Task result:
- Cases considered: 28.
- Cases attempted: 28.
- Cases completed: 28.
- Cases deferred: 0.
- case_sets changed: no.
- reports changed: no.
- results changed: no.
- denominator changed: no.
- paper results changed: no.
- case membership changed: no.
- raw legacy evidence changed: no.
- metrics computed: no.
- paper tables rendered: no.

Next safe action:
- Review the 28 wave 002 policy-approved standardized non-Common-core packages and decide whether to run a narrower manual-review follow-up, without changing `case_sets/`, denominators, reports/results, paper results, metrics, paper tables, or raw legacy evidence.

### 2026-05-18 · fa62608 · wave002_closeout_and_wave003_selection_v0

Mode: wave closeout and next-wave selection; no case migration; no case-set membership update; no denominator update; no metrics; no reports/results
Legacy repo modified: no
Release repo modified: yes
Commit: `fa6260819e7d724a7157163d76e1f76e16050082`
Push: first SSH attempt failed with `kex_exchange_identification: read: Connection reset by peer`; retry succeeded and updated `origin/main` from `de95c65` to `fa62608`

Summary:
- Reviewed all 28 wave 002 policy-approved standardized non-Common-core packages at static metadata level.
- Confirmed current release package count: 70 packages under `cases/*/*`.
- Confirmed current standardized non-Common-core count: 30 packages, covering `PORT_0002`, `PERF_0029`, and the 28 wave 002 packages.
- Built the 157-row non-Common-core standardization progress matrix from existing governance/preview artifacts.
- Selected 30 `wave_003_policy_approved_candidate` rows for a separately authorized wave 003 package-standardization task.
- Classified remaining rows as 13 manual-review, 77 backlog-defer, and 7 orphan/unregistered review rows.
- Did not migrate cases, modify case packages, update `case_sets/`, update reports/results, change denominators, change paper results, compute metrics, render paper tables, modify the legacy repo, or modify raw legacy evidence.

Files created:
- `audits/wave002_closeout_and_wave003_selection_v0/wave002_closeout_summary.md`
- `audits/wave002_closeout_and_wave003_selection_v0/wave002_completed_package_review.csv`
- `audits/wave002_closeout_and_wave003_selection_v0/non_common_core_standardization_progress.csv`
- `audits/wave002_closeout_and_wave003_selection_v0/wave003_candidate_selection.csv`
- `audits/wave002_closeout_and_wave003_selection_v0/wave003_batch_plan.md`
- `audits/wave002_closeout_and_wave003_selection_v0/wave003_policy_or_manual_questions.md`
- `audits/wave002_closeout_and_wave003_selection_v0/wave003_future_prompt.md`
- `audits/wave002_closeout_and_wave003_selection_v0/wave002_closeout_validation_results.csv`
- `audits/wave002_closeout_and_wave003_selection_v0/wave002_closeout_and_wave003_selection_summary.json`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python scripts/dev/smoke_ledger_fixtures.py`: passed; 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, and 0 unexpected pass/fail rows.
- Summary JSON invariant check: passed.
- CSV checks: passed; wave 002 package review has 28 rows, progress matrix has 157 rows, wave 003 selection has 127 rows, and validation results have no FAIL rows.
- Boundary checks: passed; no files under `case_sets/`, `reports/`, `results/`, or `cases/` changed.
- `git diff --check` and `git diff --cached --check`: passed.

Task result:
- New case migrations performed: no.
- Wave 002 completed cases reviewed: 28.
- Wave 002 review passed: yes.
- Known non-Common-core candidates: 157.
- Standardized non-Common-core count: 30.
- Remaining not-yet-standardized count: 127.
- Wave 003 auto candidates: 0.
- Wave 003 policy-approved candidates: 30.
- Wave 003 manual-review required: 13.
- Wave 003 backlog-defer: 77.
- Orphan/unregistered review: 7.
- case_sets changed: no.
- reports changed: no.
- results changed: no.
- denominator changed: no.
- paper results changed: no.
- case membership changed: no.
- raw legacy evidence changed: no.
- metrics computed: no.
- paper tables rendered: no.

Next safe action:
- Run a separately authorized `overnight_non_common_core_case_package_standardization_wave_003` task using only `wave_003_policy_approved_candidate` rows from `audits/wave002_closeout_and_wave003_selection_v0/wave003_candidate_selection.csv`, while keeping `case_sets/`, denominators, reports/results, paper results, metrics, paper tables, and raw legacy evidence unchanged.

### 2026-05-18 · e58e2c9 · overnight_non_common_core_case_package_standardization_wave_003_policy_approved

Mode: bounded policy-approved non-Common-core case package standardization; no Common-core migration; no case-set membership update; no denominator update; no metrics; no reports/results
Legacy repo modified: no
Release repo modified: yes
Commit: `e58e2c935dec48baa2d50ce7b7327c9c20a1ded2`
Push: succeeded; updated `origin/main` from `872b8cc` to `e58e2c9`

Summary:
- Used `audits/wave002_closeout_and_wave003_selection_v0/wave003_candidate_selection.csv` as the only candidate source.
- Attempted all 30 eligible `wave_003_policy_approved_candidate` cases.
- Completed canonical package standardization for 30 non-Common-core cases: `PERF_0027`, `PERF_0028`, `PERF_0030`, `PERF_0031`, `PERF_0032`, `PERF_0037`, `PERF_0039`, `PERF_0040`, `PERF_0041`, `PERF_0042`, `PERF_0045`, `PERF_0049`, `PERF_0051`, `PERF_0055`, `PERF_0057`, `PERF_0058`, `PERF_0059`, `PERF_0060`, `PERF_0061`, `PERF_0064`, `PERF_0067`, `PERF_0068`, `PERF_0069`, `PERF_0070`, `PERF_0071`, `PERF_0072`, `PERF_0073`, `PERF_0074`, `PERF_0075`, and `PORT_0006`.
- Deferred cases: none.
- Created public-facing case packages with README template v1, package-validation summary schema v1, canonical SQL/schema/checker/evidence/metadata/validation layout, and archive-mapped legacy run retention.
- Did not copy raw legacy run directories wholesale.
- Did not copy raw logs, stdout/stderr/debug payloads, private runtime traces, or raw local-path artifacts.
- Did not update `case_sets/`, update reports/results, change denominators, change paper results, compute metrics, render paper tables, modify the legacy repo, or modify raw legacy evidence.

Files created:
- 30 case package directories under `cases/PERF/` and `cases/PORT/` for the completed wave 003 cases.
- `audits/overnight_non_common_core_case_package_standardization_wave_003_policy_approved/wave003_policy_approved_summary.md`
- `audits/overnight_non_common_core_case_package_standardization_wave_003_policy_approved/wave003_policy_approved_case_queue.csv`
- `audits/overnight_non_common_core_case_package_standardization_wave_003_policy_approved/wave003_policy_approved_completed_cases.csv`
- `audits/overnight_non_common_core_case_package_standardization_wave_003_policy_approved/wave003_policy_approved_deferred_cases.csv`
- `audits/overnight_non_common_core_case_package_standardization_wave_003_policy_approved/wave003_policy_approved_hygiene_findings.csv`
- `audits/overnight_non_common_core_case_package_standardization_wave_003_policy_approved/wave003_policy_approved_runs_retention_index.csv`
- `audits/overnight_non_common_core_case_package_standardization_wave_003_policy_approved/wave003_policy_approved_package_validation_summary_audit.csv`
- `audits/overnight_non_common_core_case_package_standardization_wave_003_policy_approved/wave003_policy_approved_readme_checks.csv`
- `audits/overnight_non_common_core_case_package_standardization_wave_003_policy_approved/wave003_policy_approved_validation_results.csv`
- `audits/overnight_non_common_core_case_package_standardization_wave_003_policy_approved/wave003_policy_approved_summary.json`
- `audits/overnight_non_common_core_case_package_standardization_wave_003_policy_approved/wave004_followup_prompt.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python scripts/dev/validate_case_package.py --mode canonical-case`: passed for 30/30 completed cases.
- `python scripts/dev/smoke_ledger_fixtures.py`: passed; 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, and 0 unexpected pass/fail rows.
- Summary JSON invariant check: passed.
- YAML/JSON parse checks: passed for new package and audit files.
- README forbidden-term checks: passed for 30 completed package READMEs.
- package_validation_summary schema checks: passed for 30 completed package summaries.
- Boundary checks: passed; no `case_sets/`, `reports/`, `results/`, denominator, paper-result, raw legacy evidence, or Common-core package files were modified.
- `git diff --check`: passed before staging and commit.

Task result:
- Cases considered: 30.
- Cases attempted: 30.
- Cases completed: 30.
- Cases deferred: 0.
- case_sets changed: no.
- reports changed: no.
- results changed: no.
- denominator changed: no.
- paper results changed: no.
- case membership changed: no.
- raw legacy evidence changed: no.
- metrics computed: no.
- paper tables rendered: no.

Next safe action:
- Review the 30 wave 003 policy-approved standardized non-Common-core packages and prepare a separately authorized wave 004 selection/closeout packet from the remaining non-Common-core backlog, while keeping `case_sets/`, denominators, reports/results, paper results, metrics, paper tables, and raw legacy evidence unchanged.

### 2026-05-18 · df2249c · wave003_closeout_and_wave004_selection_v0

Mode: wave closeout and next-wave selection; no case migration; no case-set membership update; no denominator update; no metrics; no reports/results
Legacy repo modified: no
Release repo modified: yes
Commit: `df2249c42e30a6c9ffea27a394c93f6247013a79`
Push: succeeded; updated `origin/main` from `cd9d1d6` to `df2249c`

Summary:
- Reviewed all 30 wave 003 policy-approved standardized non-Common-core packages at static metadata level.
- Recomputed current release package count from `cases/*/*`: 100.
- Recomputed standardized non-Common-core package count from release packages minus Common-core membership: 60.
- Built the 157-row post-wave003 non-Common-core standardization progress matrix.
- Classified the remaining 97 rows for wave 004 planning.
- Determined that no row is safe for immediate auto or policy-approved wave 004 migration under current wave 002/003 guardrails.
- Classified wave 004 rows as 0 auto candidates, 0 policy-approved candidates, 13 manual-review rows, 77 backlog-defer rows, and 7 orphan/unregistered review rows.
- Did not migrate cases, modify case packages, update `case_sets/`, update reports/results, change denominators, change paper results, compute metrics, render paper tables, modify the legacy repo, or modify raw legacy evidence.

Files created:
- `audits/wave003_closeout_and_wave004_selection_v0/wave003_closeout_summary.md`
- `audits/wave003_closeout_and_wave004_selection_v0/wave003_completed_package_review.csv`
- `audits/wave003_closeout_and_wave004_selection_v0/non_common_core_standardization_progress_after_wave003.csv`
- `audits/wave003_closeout_and_wave004_selection_v0/wave004_candidate_selection.csv`
- `audits/wave003_closeout_and_wave004_selection_v0/wave004_batch_plan.md`
- `audits/wave003_closeout_and_wave004_selection_v0/wave004_policy_or_manual_questions.md`
- `audits/wave003_closeout_and_wave004_selection_v0/wave004_future_prompt.md`
- `audits/wave003_closeout_and_wave004_selection_v0/wave003_closeout_validation_results.csv`
- `audits/wave003_closeout_and_wave004_selection_v0/wave003_closeout_and_wave004_selection_summary.json`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python scripts/dev/smoke_ledger_fixtures.py`: passed; 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, and 0 unexpected pass/fail rows.
- Summary JSON invariant check: passed.
- CSV checks: passed; wave 003 package review has 30 rows, progress matrix has 157 rows, wave 004 selection has 97 rows, and validation results have no FAIL rows.
- Boundary checks: passed; no files under `case_sets/`, `reports/`, `results/`, or `cases/` changed.
- `git diff --check`: passed before staging and commit.

Task result:
- New case migrations performed: no.
- Wave 003 completed cases reviewed: 30.
- Wave 003 review passed: yes.
- Known non-Common-core candidates: 157.
- Standardized non-Common-core count: 60.
- Remaining not-yet-standardized count: 97.
- Wave 004 auto candidates: 0.
- Wave 004 policy-approved candidates: 0.
- Wave 004 manual-review required: 13.
- Wave 004 backlog-defer: 77.
- Orphan/unregistered review: 7.
- case_sets changed: no.
- reports changed: no.
- results changed: no.
- denominator changed: no.
- paper results changed: no.
- case membership changed: no.
- raw legacy evidence changed: no.
- metrics computed: no.
- paper tables rendered: no.

Next safe action:
- Prepare a separately authorized wave 004 blocker-resolution packet for the remaining manual-review, missing-checker backlog, and orphan/unregistered rows before any further package migration, while keeping `case_sets/`, denominators, reports/results, paper results, metrics, paper tables, and raw legacy evidence unchanged.

### 2026-05-18 · 886a2ff · wave004_blocker_resolution_packet_v0

Mode: blocker-resolution and next-wave policy packet; no case migration; no case-set membership update; no denominator update; no metrics; no reports/results
Legacy repo modified: no
Release repo modified: yes
Commit: `886a2ff410353f10d7685ec1b1597d60561fd8b3`
Push: succeeded; updated `origin/main` from `6dd4f7c` to `886a2ff`

Summary:
- Reviewed all 97 remaining non-Common-core rows from `audits/wave003_closeout_and_wave004_selection_v0/wave004_candidate_selection.csv`.
- Reviewed 7 policy questions covering missing checker, missing retained evidence, hard-negative review, schema/load gaps, orphan/unregistered registry reconciliation, public hygiene, and minimum package policy.
- Recommended 0 policy-unlocked wave004 migration candidates.
- Kept 13 rows in manual review, 77 rows in backlog defer, and 7 rows in orphan/registry review.
- Did not migrate cases, modify case packages, update `case_sets/`, update reports/results, change denominators, change paper results, compute metrics, render paper tables, modify the legacy repo, or modify raw legacy evidence.

Files created:
- `audits/wave004_blocker_resolution_packet_v0/wave004_blocker_resolution_summary.md`
- `audits/wave004_blocker_resolution_packet_v0/wave004_remaining_case_blocker_matrix.csv`
- `audits/wave004_blocker_resolution_packet_v0/wave004_policy_resolution_matrix.csv`
- `audits/wave004_blocker_resolution_packet_v0/wave004_policy_unlocked_candidates.csv`
- `audits/wave004_blocker_resolution_packet_v0/wave004_manual_review_cases.csv`
- `audits/wave004_blocker_resolution_packet_v0/wave004_backlog_defer_cases.csv`
- `audits/wave004_blocker_resolution_packet_v0/wave004_orphan_registry_review_cases.csv`
- `audits/wave004_blocker_resolution_packet_v0/wave004_candidate_selection_after_blocker_resolution.csv`
- `audits/wave004_blocker_resolution_packet_v0/wave004_batch_plan_after_blocker_resolution.md`
- `audits/wave004_blocker_resolution_packet_v0/future_wave004_policy_approved_prompt.md`
- `audits/wave004_blocker_resolution_packet_v0/wave004_blocker_resolution_summary.json`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python scripts/dev/smoke_ledger_fixtures.py`: passed; 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, and 0 unexpected pass/fail rows.
- Summary JSON invariant check: passed.
- CSV reconciliation checks: passed; blocker matrix and after-resolution selection each cover all 97 remaining candidates, manual/backlog/orphan counts reconcile to 13/77/7, and policy-unlocked candidates count is 0.

Task result:
- New case migrations performed: no.
- Remaining candidates reviewed: 97.
- Policy-unlocked candidates: 0.
- Manual review cases: 13.
- Backlog defer cases: 77.
- Orphan/registry review cases: 7.
- case_sets changed: no.
- reports changed: no.
- results changed: no.
- denominator changed: no.
- paper results changed: no.
- case membership changed: no.
- raw legacy evidence changed: no.
- metrics computed: no.
- paper tables rendered: no.

Next safe action:
- Prepare a manual checker/schema/hard-negative and orphan registry reconciliation packet before any wave004 migration; do not migrate cases until source/positive/checker core assets and registry identity are resolved, while keeping `case_sets/`, denominators, reports/results, paper results, metrics, paper tables, and raw legacy evidence unchanged.

### 2026-05-18 · 807037c · b_line_user_entry_contract_v0

Mode: B-line public workbench design and user-entry contract; design-only; no public runner implementation; no reproduction CLI implementation; no metrics; no paper tables; no case migration
Legacy repo modified: no
Release repo modified: yes
Commit: `807037cf2fef63ca9c6f33a07320ae0a507d3a5c`
Push: succeeded; updated `origin/main` from `fa3138f` to `807037c`

Summary:
- Defined the future user-facing command model for running external SQL rewrite algorithms against selected benchmark cases.
- Defined case selection semantics for `--case-set`, `--pool`, `--case-list`, and `--engine` using `case_sets/` and inventory metadata rather than physical directory guessing.
- Defined the user algorithm adapter contract, local output policy, user-run ledger/output schema, report/visualization minimum contents, and no-global-leaderboard/paper-evidence separation boundaries.
- Classified proposed B-line files by lifecycle class.
- Drafted the next MVP implementation task and future prompt.
- Did not implement a public runner, implement a reproduction CLI, compute metrics, render paper tables, migrate cases, update `case_sets/`, update reports/results, change denominators, change paper results, modify the legacy repo, or modify raw legacy evidence.

Files created:
- `audits/b_line_user_entry_contract_v0/b_line_user_entry_contract_summary.md`
- `audits/b_line_user_entry_contract_v0/user_entry_case_selection_contract.csv`
- `audits/b_line_user_entry_contract_v0/user_algorithm_adapter_contract.csv`
- `audits/b_line_user_entry_contract_v0/user_run_output_schema.csv`
- `audits/b_line_user_entry_contract_v0/user_run_report_contract.csv`
- `audits/b_line_user_entry_contract_v0/b_line_file_lifecycle_matrix.csv`
- `audits/b_line_user_entry_contract_v0/user_entry_mvp_task_plan.md`
- `audits/b_line_user_entry_contract_v0/future_b_line_user_entry_mvp_prompt.md`
- `audits/b_line_user_entry_contract_v0/b_line_user_entry_contract_summary.json`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python scripts/dev/smoke_ledger_fixtures.py`: passed; 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, and 0 unexpected pass/fail rows.
- Summary JSON invariant check: passed.
- CSV checks: passed; all required CSV files have headers, lifecycle classes are represented, `ledger.csv` and `summary.json` are present in the output schema, and CSV rows do not claim metric computation, paper table rendering, or retained-result updates.
- Boundary checks: passed; no files under `cases/`, `case_sets/`, `inventory/`, `reports/`, or `results/` changed.
- `git diff --check`: passed before staging and commit.

Task result:
- Case migration performed: no.
- Public runner implemented: no.
- Reproduction CLI implemented: no.
- Metrics computed: no.
- Paper tables rendered: no.
- case_sets changed: no.
- reports changed: no.
- results changed: no.
- denominator changed: no.
- paper results changed: no.
- raw legacy evidence changed: no.

Next safe action:
- Authorize b_line_user_entry_mvp_v0 to implement a minimal non-DB user runner skeleton that writes only to `runs/user/<run_id>/` and keeps case packages, `case_sets/`, inventory, denominators, reports/results, paper results, retained evidence, and raw legacy evidence unchanged.

### 2026-05-18 · a469ab8 · b_line_user_entry_mvp_v0

Mode: B-line user entry MVP implementation; minimal non-DB public runner skeleton; no DB execution; no checker execution; no timing; no official metrics; no paper tables; no case migration
Legacy repo modified: no
Release repo modified: yes
Commit: `a469ab8a824c850655f2b318cac487d652305923`
Push: succeeded; updated `origin/main` from `5b088ca` to `a469ab8`

Summary:
- Implemented a module-first user runner skeleton under `src/sql_rewrite_bench/`.
- Implemented Common-core v0 metadata selection from `case_sets/common_core_v0/cases.csv` and `case_sets/common_core_v0/denominator_same_engine_120.csv`.
- Implemented `--pool`, `--case-list`, and `--engine` filtering without physical directory membership guessing.
- Implemented adapter invocation with `shell=False`, environment-variable context, per-row workspaces, stdout/stderr capture, and candidate SQL capture from workspace `candidate.sql` or stdout.
- Implemented local outputs under `runs/user/<run_id>/`: `config.yaml`, `selected_cases.csv`, `candidate_sql/`, `workspaces/`, `ledger.csv`, `summary.json`, `failures.csv`, and `report.md`.
- Added `runs/.gitignore` so local smoke/user outputs are not committed by default.
- Added standard-library tests and dummy/empty adapters under `tests/user_entry/`.
- Did not execute SQL, run database engines, run checkers, collect timing, compute official metrics, render paper tables, implement paper reproduction, implement retained-evidence adapters, migrate cases, update `case_sets/`, update inventory, update reports/results, change denominators, change paper results, modify the legacy repo, or modify raw legacy evidence.

Files created:
- `src/sql_rewrite_bench/__init__.py`
- `src/sql_rewrite_bench/case_selection.py`
- `src/sql_rewrite_bench/user_run_schema.py`
- `src/sql_rewrite_bench/user_run.py`
- `tests/user_entry/test_case_selection.py`
- `tests/user_entry/test_user_run_outputs.py`
- `tests/user_entry/fixtures/dummy_adapter.py`
- `tests/user_entry/fixtures/empty_adapter.py`
- `runs/.gitignore`
- `audits/b_line_user_entry_mvp_v0/b_line_user_entry_mvp_summary.md`
- `audits/b_line_user_entry_mvp_v0/b_line_user_entry_mvp_validation_results.csv`
- `audits/b_line_user_entry_mvp_v0/b_line_user_entry_mvp_summary.json`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `PYTHONPATH=src python -m unittest discover -s tests/user_entry -q`: passed; 6 tests.
- Dummy adapter smoke run: passed; 2 selected rows and 2 captured candidate SQL files under ignored `runs/user/smoke_user_entry_mvp/`.
- Smoke output checks: passed; `config.yaml`, `selected_cases.csv`, `ledger.csv`, `summary.json`, `failures.csv`, and `report.md` generated.
- `python scripts/dev/smoke_ledger_fixtures.py`: passed; 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, and 0 unexpected pass/fail rows.
- Summary JSON invariant check: passed.
- Boundary checks: passed; no files under `cases/`, `case_sets/`, `inventory/`, `reports/`, or `results/` changed.

Task result:
- Case migration performed: no.
- Public runner skeleton implemented: yes.
- Non-DB MVP only: yes.
- DB execution implemented: no.
- Checker execution implemented: no.
- Official metrics computed: no.
- Paper tables rendered: no.
- Reproduction CLI implemented: no.
- Retained-evidence adapter implemented: no.
- case_sets changed: no.
- inventory changed: no.
- reports changed: no.
- results changed: no.
- denominator changed: no.
- paper results changed: no.
- raw legacy evidence changed: no.

Next safe action:
- Authorize a B-line user-entry hardening task to add packaging/CLI documentation, stable tests, output hygiene checks, and optional dry-run mode while keeping DB execution, checker execution, timing, official metrics, paper reproduction, retained evidence, reports/results, denominators, case sets, and raw legacy evidence unchanged.

### 2026-05-18 · 7114c51 · b_line_user_entry_hardening_v0

Mode: B-line user entry hardening; non-DB MVP only; dry-run and usability hardening; no DB execution; no checker execution; no timing; no official metrics; no paper tables; no case migration
Legacy repo modified: no
Release repo modified: yes
Commit: `7114c51e5081b21a9560578780c738b25306b887`
Push: succeeded; updated `origin/main` from `c241311` to `7114c51`

Summary:
- Added or verified `--dry-run` for the non-DB user-entry MVP.
- Added `scripts/user/run_user_benchmark.py` as a thin wrapper around `sql_rewrite_bench.user_run`.
- Strengthened output-root guard messaging for invalid output paths outside `runs/user/<run_id>/`.
- Expanded tests for candidate file output, stdout output, nonzero adapter exit, empty adapter output, timeout handling, dry-run rows, and invalid output roots.
- Improved `report.md` with command summary, dry-run flag, selected row count, pool and engine breakdowns, adapter/candidate counts, failure table, artifact links, and local/no-paper/no-metrics/no-leaderboard warnings.
- Added a user-guide preview under the hardening audit directory.
- Did not execute SQL, run database engines, run checkers, collect timing, compute official metrics, render paper tables, implement paper reproduction, implement retained-evidence adapters, migrate cases, update `case_sets/`, update inventory, update reports/results, change denominators, change paper results, modify the legacy repo, or modify raw legacy evidence.

Files created:
- `scripts/user/run_user_benchmark.py`
- `tests/user_entry/fixtures/stdout_adapter.py`
- `tests/user_entry/fixtures/failing_adapter.py`
- `tests/user_entry/fixtures/slow_adapter.py`
- `audits/b_line_user_entry_hardening_v0/b_line_user_entry_hardening_summary.md`
- `audits/b_line_user_entry_hardening_v0/b_line_user_entry_hardening_validation_results.csv`
- `audits/b_line_user_entry_hardening_v0/b_line_user_entry_hardening_summary.json`
- `audits/b_line_user_entry_hardening_v0/user_guide_preview.md`

Files modified:
- `src/sql_rewrite_bench/user_run.py`
- `src/sql_rewrite_bench/user_run_schema.py`
- `tests/user_entry/test_user_run_outputs.py`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests/user_entry -q`: passed; 10 tests.
- Dry-run smoke: passed; 2 selected rows, 0 adapter invocations, 0 candidate rows, `skipped_dry_run` extraction status.
- Dummy adapter success smoke: passed; 2 selected rows and 2 captured candidate SQL files.
- Thin wrapper help command: passed.
- `python scripts/dev/smoke_ledger_fixtures.py`: passed; 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, and 0 unexpected pass/fail rows.
- Summary JSON invariant check: passed.
- `git diff --check`: passed before staging.

Task result:
- Public runner skeleton implemented: yes.
- Hardening task: yes.
- Dry-run mode added or verified: yes.
- Non-DB MVP only: yes.
- DB execution implemented: no.
- Checker execution implemented: no.
- Official metrics computed: no.
- Paper tables rendered: no.
- Reproduction CLI implemented: no.
- Retained-evidence adapter implemented: no.
- case_sets changed: no.
- inventory changed: no.
- reports changed: no.
- results changed: no.
- denominator changed: no.
- paper results changed: no.
- raw legacy evidence changed: no.

Next safe action:
- Authorize documentation and packaging stabilization for the B-line user-entry MVP, or separately authorize a future DB/checker execution design packet while keeping case packages, `case_sets/`, inventory, denominators, reports/results, paper results, retained evidence, and raw legacy evidence unchanged.

### 2026-05-18 · pending · b_line_user_entry_packaging_docs_v0

Mode: B-line user entry packaging/docs stabilization; non-DB MVP only; no DB execution; no checker execution; no timing; no official metrics; no paper tables; no reproduction CLI; no retained-evidence adapter
Legacy repo modified: no
Release repo modified: yes
Commit: pending
Push: pending

Summary:
- Promoted the hardening user-guide preview into `docs/USER_BENCHMARK_GUIDE.md`.
- Created `docs/RUN_ARTIFACT_POLICY.md` to document user-run output placement and retained-evidence/report/result boundaries.
- Added minimal `pyproject.toml` metadata for editable local use with `src` package discovery and no runtime dependencies.
- Added a short README pointer to the user benchmark guide and current non-DB MVP limitations.
- Kept `scripts/user/run_user_benchmark.py` as a thin wrapper and validated module and wrapper `--help` behavior.
- Extended user-entry tests for module help, wrapper help, and documented CLI option alignment.
- Did not execute SQL, run database engines, run checkers, collect timing, compute official metrics, render paper tables, implement SQLGlot/Calcite/R-Bot baselines, implement paper reproduction, implement retained-evidence adapters, migrate cases, update `case_sets/`, update inventory, update reports/results, change denominators, change paper results, modify the legacy repo, or modify raw legacy evidence.

Files created:
- `pyproject.toml`
- `docs/USER_BENCHMARK_GUIDE.md`
- `docs/RUN_ARTIFACT_POLICY.md`
- `audits/b_line_user_entry_packaging_docs_v0/b_line_user_entry_packaging_docs_summary.md`
- `audits/b_line_user_entry_packaging_docs_v0/b_line_user_entry_packaging_docs_validation_results.csv`
- `audits/b_line_user_entry_packaging_docs_v0/b_line_user_entry_packaging_docs_summary.json`
- `audits/b_line_user_entry_packaging_docs_v0/user_entry_public_surface_matrix.csv`

Files modified:
- `README.md`
- `tests/user_entry/test_user_run_outputs.py`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests/user_entry -q`: passed; 12 tests.
- `python -m pytest tests/user_entry -q`: not run as primary validation because pytest is not installed in this environment.
- Module help check: passed.
- Wrapper help check: passed.
- Dry-run smoke: passed; 2 selected rows, 0 adapter invocations, 0 candidate rows, `skipped_dry_run` extraction status.
- Dummy adapter success smoke: passed; 2 selected rows and 2 captured candidate SQL files.
- `pyproject.toml` parse/check: passed.
- `python scripts/dev/smoke_ledger_fixtures.py`: passed; 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, and 0 unexpected pass/fail rows.
- Summary JSON invariant check: passed.
- `git diff --check`: passed before staging.

Task result:
- Packaging/docs task: yes.
- Public runner skeleton implemented: yes.
- Non-DB MVP only: yes.
- DB execution implemented: no.
- Checker execution implemented: no.
- Official metrics computed: no.
- Paper tables rendered: no.
- Reproduction CLI implemented: no.
- Retained-evidence adapter implemented: no.
- case_sets changed: no.
- inventory changed: no.
- reports changed: no.
- results changed: no.
- denominator changed: no.
- paper results changed: no.
- raw legacy evidence changed: no.

Next safe action:
- Authorize a B-line user-entry release-smoke task to verify editable install behavior and local output hygiene in a fresh checkout, or separately authorize a future DB/checker execution design packet while keeping case packages, `case_sets/`, inventory, denominators, reports/results, paper results, retained evidence, and raw legacy evidence unchanged.
