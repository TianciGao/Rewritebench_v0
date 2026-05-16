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
Commit: 98fafa46f2c9c98f2381f2299704af533bf59964
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
