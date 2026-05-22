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

### 2026-05-18 · a12af20 · b_line_user_entry_packaging_docs_v0

Mode: B-line user entry packaging/docs stabilization; non-DB MVP only; no DB execution; no checker execution; no timing; no official metrics; no paper tables; no reproduction CLI; no retained-evidence adapter
Legacy repo modified: no
Release repo modified: yes
Commit: `a12af20f28c47d3ba01171ed09ca2276df02bed7`
Push: succeeded; updated `origin/main` from `ccb3bb2` to `a12af20`

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

### 2026-05-18 · fe76808 · b_line_user_entry_release_smoke_v0

Mode: B-line user entry release-smoke verification; fresh-checkout editable-install smoke; no feature implementation; no DB execution; no checker execution; no timing; no official metrics; no paper tables
Legacy repo modified: no
Release repo modified: yes
Commit: `fe7680824243209a74e362d28b062b361ae9d180`
Push: succeeded; updated `origin/main` from `6971a8d` to `fe76808`

Summary:
- Created a temporary local clone at `/tmp/sqlrb_user_entry_release_smoke/Rewritebench_v0_smoke`.
- Created `.venv-smoke/` in the temporary clone and ran editable install with `.venv-smoke/bin/python -m pip install -e .`.
- Verified module help with `.venv-smoke/bin/python -m sql_rewrite_bench.user_run --help`.
- Verified wrapper help with `.venv-smoke/bin/python scripts/user/run_user_benchmark.py --help`.
- Ran dry-run smoke on `PERF_0006` and `PERF_0007`; selected 2 rows, invoked 0 adapters, generated 0 candidates, and wrote expected local run files.
- Ran dummy adapter smoke on `PERF_0006` and `PERF_0007`; selected 2 rows, invoked 2 adapters, generated 2 candidates, and wrote expected local run files.
- Confirmed smoke outputs are under `runs/user/`, ignored/unstaged in the temporary clone, and protected paths `cases/`, `case_sets/`, `inventory/`, `reports/`, and `results/` had no changes.
- Did not implement features, execute SQL, run database engines, run checkers, collect timing, compute official metrics, render paper tables, implement SQLGlot/Calcite/R-Bot baselines, implement paper reproduction, implement retained-evidence adapters, migrate cases, update `case_sets/`, update inventory, update reports/results, change denominators, change paper results, modify the legacy repo, or modify raw legacy evidence.

Files created:
- `audits/b_line_user_entry_release_smoke_v0/b_line_user_entry_release_smoke_summary.md`
- `audits/b_line_user_entry_release_smoke_v0/b_line_user_entry_release_smoke_validation_results.csv`
- `audits/b_line_user_entry_release_smoke_v0/b_line_user_entry_release_smoke_summary.json`
- `audits/b_line_user_entry_release_smoke_v0/release_smoke_command_log.md`
- `audits/b_line_user_entry_release_smoke_v0/release_smoke_output_manifest.csv`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- Fresh-checkout smoke passed: yes.
- Editable install passed: yes.
- Module help passed: yes.
- Wrapper help passed: yes.
- Dry-run smoke passed: yes.
- Dummy adapter smoke passed: yes.
- Output hygiene passed: yes.
- `python scripts/dev/smoke_ledger_fixtures.py`: passed; 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, and 0 unexpected pass/fail rows.
- Summary JSON invariant check: passed.
- `git diff --check`: passed before staging.

Task result:
- Release-smoke task: yes.
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
- Authorize a B-line user-entry publication-surface closeout or CI smoke wiring task, or separately authorize a future DB/checker execution design packet while keeping case packages, `case_sets/`, inventory, denominators, reports/results, paper results, retained evidence, and raw legacy evidence unchanged.

### 2026-05-18 · c8a9476 · b_line_user_entry_ci_smoke_v0

Mode: B-line user entry CI/dev-smoke wiring; lightweight public-surface guard; no feature implementation; no DB execution; no checker execution; no timing; no official metrics; no paper tables
Legacy repo modified: no
Release repo modified: yes
Commit: `c8a9476e09925f33317e166da48740f977443625`
Push: succeeded; updated `origin/main` from `ae3cd3e` to `c8a9476`

Summary:
- Added `scripts/dev/run_user_entry_ci_smoke.py` as a current-checkout dev-smoke for the non-DB B-line user-entry MVP.
- Added `.github/workflows/user_entry_smoke.yml` to run editable install, the user-entry dev-smoke, the synthetic ledger fixture smoke, whitespace diff checks, and protected-path checks on push, pull request, and manual dispatch.
- The dev-smoke verifies module help, wrapper help, user-entry tests, dry-run smoke, dummy-adapter smoke, expected local output files, `runs/user` output hygiene, and clean protected paths.
- Did not implement new runner features, execute SQL, run database engines, run checkers, collect timing, compute official metrics, render paper tables, implement SQLGlot/Calcite/R-Bot baselines, implement paper reproduction, implement retained-evidence adapters, migrate cases, update `case_sets/`, update inventory, update reports/results, change denominators, change paper results, modify the legacy repo, or modify raw legacy evidence.

Files created:
- `.github/workflows/user_entry_smoke.yml`
- `scripts/dev/run_user_entry_ci_smoke.py`
- `audits/b_line_user_entry_ci_smoke_v0/b_line_user_entry_ci_smoke_summary.md`
- `audits/b_line_user_entry_ci_smoke_v0/b_line_user_entry_ci_smoke_validation_results.csv`
- `audits/b_line_user_entry_ci_smoke_v0/b_line_user_entry_ci_smoke_summary.json`
- `audits/b_line_user_entry_ci_smoke_v0/ci_smoke_command_log.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `PYTHONPATH=src python scripts/dev/run_user_entry_ci_smoke.py`: passed; module help, wrapper help, user-entry tests, dry-run smoke, dummy adapter smoke, output hygiene, protected-path checks, and unstaged `runs/user` checks passed.
- `python scripts/dev/smoke_ledger_fixtures.py`: passed; 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, and 0 unexpected pass/fail rows.
- Workflow YAML parse: passed with PyYAML.
- Summary JSON invariant check: passed.
- `git diff --check`: passed before staging.

Task result:
- CI/dev-smoke wiring task: yes.
- Local dev-smoke passed: yes.
- Fixture smoke passed: yes.
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
- Use the B-line user-entry smoke workflow as a push/PR guard, or separately authorize a B-line publication-surface closeout or DB/checker execution design packet while keeping case packages, `case_sets/`, inventory, denominators, reports/results, paper results, retained evidence, and raw legacy evidence unchanged.

### 2026-05-18 · 2e39ab5 · b_line_sqlglot_adapter_mvp_v0

Mode: B-line SQLGlot non-DB adapter MVP; candidate SQL generation only; no DB execution; no checker execution; no timing; no official metrics; no paper tables; no retained-evidence parsing
Legacy repo modified: no
Release repo modified: yes
Commit: `2e39ab57fc660bdd03a7db437db185e63b5f2e2c`
Push: succeeded; updated `origin/main` from `af3df38` to `2e39ab5`

Summary:
- Added optional SQLGlot user-entry adapters under `baselines/sqlglot/`.
- Added `sqlglot_noop` route via `python baselines/sqlglot/sqlglot_user_adapter.py --route noop`.
- Added `sqlglot_optimize` route via `python baselines/sqlglot/sqlglot_user_adapter.py --route optimize`.
- The adapter reads source SQL from `SQLRB_SOURCE_SQL_PATH`, infers dialect from `SQLRB_ENGINE`, writes candidate SQL to `SQLRB_CANDIDATE_SQL_PATH`, and exits nonzero on missing environment, missing source, unsupported engine, missing SQLGlot dependency, parse failure, or emit failure.
- Added optional SQLGlot extra metadata in `pyproject.toml`; SQLGlot remains optional and was not installed by this task.
- Updated `docs/USER_BENCHMARK_GUIDE.md` with optional SQLGlot adapter usage examples and boundaries.
- Added user-entry tests for adapter help, missing environment variables, route validation, missing dependency guard, dry-run compatibility, and conditional real SQLGlot no-op/optimize smoke when the dependency is available.
- Did not modify the user-runner core, execute SQL, run database engines, run checkers, collect timing, compute official metrics, compute speedup, render paper tables, implement paper reproduction, implement retained-evidence adapters, parse candidate status retained evidence, migrate cases, update `case_sets/`, update inventory, update reports/results, change denominators, change paper results, create a global leaderboard, modify the legacy repo, or modify raw legacy evidence.

Files created:
- `baselines/sqlglot/README.md`
- `baselines/sqlglot/sqlglot_user_adapter.py`
- `tests/user_entry/test_sqlglot_adapter.py`
- `audits/b_line_sqlglot_adapter_mvp_v0/b_line_sqlglot_adapter_mvp_summary.md`
- `audits/b_line_sqlglot_adapter_mvp_v0/b_line_sqlglot_adapter_mvp_validation_results.csv`
- `audits/b_line_sqlglot_adapter_mvp_v0/b_line_sqlglot_adapter_mvp_summary.json`
- `audits/b_line_sqlglot_adapter_mvp_v0/sqlglot_adapter_command_log.md`
- `audits/b_line_sqlglot_adapter_mvp_v0/sqlglot_adapter_smoke_manifest.csv`

Files modified:
- `docs/USER_BENCHMARK_GUIDE.md`
- `pyproject.toml`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `python baselines/sqlglot/sqlglot_user_adapter.py --help`: passed.
- `PYTHONPATH=src python -m unittest discover -s tests/user_entry -v`: passed; 19 tests run, 2 skipped because SQLGlot is not installed.
- `python -m py_compile baselines/sqlglot/sqlglot_user_adapter.py tests/user_entry/test_sqlglot_adapter.py`: passed.
- Missing SQLGlot dependency guard: passed with expected nonzero exit and clear dependency message.
- Route validation: passed with expected nonzero exit for invalid route.
- SQLGlot dry-run user-run compatibility: passed with 1 selected row, 0 adapter invocations, and 0 candidates.
- Real SQLGlot no-op smoke: skipped because SQLGlot is not installed.
- Real SQLGlot optimize smoke: skipped because SQLGlot is not installed.
- `PYTHONPATH=src python scripts/dev/run_user_entry_ci_smoke.py`: passed.
- `python scripts/dev/smoke_ledger_fixtures.py`: passed; 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected.
- Summary JSON invariant check: passed.
- `git diff --check`: passed before staging.

Task result:
- SQLGlot adapter MVP: yes.
- SQLGlot dependency available: no.
- Real SQLGlot smoke passed/skipped: skipped.
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
- Optionally authorize a SQLGlot-enabled environment smoke that installs `.[sqlglot]` and runs real no-op and optimize adapter routes without DB execution, checker execution, official metrics, paper rendering, retained-evidence updates, reports/results updates, denominator changes, paper-result changes, or leaderboard output.

### 2026-05-18 · 26e8849 · b_line_sqlglot_enabled_smoke_v0

Mode: B-line SQLGlot enabled smoke; optional dependency verification and real non-DB SQLGlot adapter smoke only; no DB execution; no checker execution; no timing; no official metrics; no paper tables; no retained-evidence parsing
Legacy repo modified: no
Release repo modified: yes
Commit: `26e8849d2ed99c962df9ebeb973e99e795d714f6`
Push: succeeded; updated `origin/main` from `33d80f5` to `26e8849`

Summary:
- Created an isolated temporary clone under `/tmp/sqlrb_sqlglot_enabled_smoke/Rewritebench_v0_sqlglot_smoke`.
- Created a temporary virtual environment and installed the release package with `python -m pip install -e ".[sqlglot]"`.
- Confirmed SQLGlot import with observed version `30.8.0`.
- Confirmed SQLGlot adapter help works.
- Ran user-entry dry-run with the SQLGlot no-op adapter command over `PERF_0006` and `PERF_0007` postgres rows.
- Ran real non-DB SQLGlot no-op and optimize adapter smokes over `PERF_0006` and `PERF_0007` postgres rows.
- Verified candidate SQL files were generated under temporary-clone `runs/user/<run_id>/candidate_sql/`.
- Verified real smoke ledgers reported `candidate_generated=true` and preserved `not_run_non_db_mvp`, `not_evaluated_non_db_mvp`, and `not_timed_non_db_mvp` status boundaries.
- Verified temporary smoke outputs stayed under ignored `runs/user/` and protected paths were unchanged.
- Did not implement features, execute SQL, run database engines, run checkers, collect timing, compute official metrics, render paper tables, implement paper reproduction, implement retained-evidence adapters, migrate cases, update `case_sets/`, update inventory, update reports/results, change denominators, change paper results, create a global leaderboard, modify the legacy repo, or modify raw legacy evidence.

Files created:
- `audits/b_line_sqlglot_enabled_smoke_v0/b_line_sqlglot_enabled_smoke_summary.md`
- `audits/b_line_sqlglot_enabled_smoke_v0/b_line_sqlglot_enabled_smoke_validation_results.csv`
- `audits/b_line_sqlglot_enabled_smoke_v0/b_line_sqlglot_enabled_smoke_summary.json`
- `audits/b_line_sqlglot_enabled_smoke_v0/sqlglot_enabled_smoke_command_log.md`
- `audits/b_line_sqlglot_enabled_smoke_v0/sqlglot_enabled_smoke_output_manifest.csv`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- Temporary clone and virtual environment creation: passed.
- `python -m pip install -e ".[sqlglot]"`: passed.
- SQLGlot import: passed with version `30.8.0`.
- `python baselines/sqlglot/sqlglot_user_adapter.py --help`: passed.
- SQLGlot no-op dry-run user-run smoke: passed with 2 selected rows, 0 adapter invocations, and 0 candidates.
- Real SQLGlot no-op user-run smoke: passed with 2 selected rows and 2 candidate SQL files.
- Real SQLGlot optimize user-run smoke: passed with 2 selected rows and 2 candidate SQL files.
- Candidate SQL, summary, and ledger checks: passed.
- Temporary clone protected-path and `runs/user` output hygiene checks: passed.
- `PYTHONPATH=src python scripts/dev/run_user_entry_ci_smoke.py`: passed.
- `python scripts/dev/smoke_ledger_fixtures.py`: passed.
- Summary JSON invariant check: passed.
- `git diff --check`: passed before staging.

Task result:
- SQLGlot enabled smoke task: yes.
- SQLGlot extra install passed: yes.
- SQLGlot dependency available: yes.
- SQLGlot import passed: yes.
- Adapter help passed: yes.
- Dry-run smoke passed: yes.
- Real SQLGlot no-op smoke passed: yes.
- Real SQLGlot optimize smoke passed: yes.
- Candidate SQL generated: yes.
- Non-DB statuses preserved: yes.
- Output hygiene passed: yes.
- Smoke outputs staged: no.
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
- Use the SQLGlot-enabled smoke result as validation that optional candidate-generation adapters can plug into the non-DB user-entry runner; separately authorize any DB execution, checker execution, timing, official metrics, retained-evidence integration, paper reproduction, or leaderboard design before implementation.

### 2026-05-18 · 3c16980 · b_line_db_checker_execution_design_v0

Mode: B-line DB/checker execution design only; no DB execution implementation; no checker execution implementation; no timing; no official metrics; no paper tables; no retained-evidence adapter; no reports/results updates
Legacy repo modified: no
Release repo modified: yes
Commit: `3c16980d3a3d53d38456eda0f0716891843e3a88`
Push: succeeded; updated `origin/main` from `c4aa1cd` to `3c16980`

Summary:
- Designed a future local DB/checker execution layer for user-run outputs.
- Defined a conservative future MVP scope: Common-core v0 only, postgres only, 1-2 PERF cases first, SQLGlot no-op candidate first, local `runs/user/<run_id>/` output only, no timing, no official metrics, no retained evidence, no reports/results updates, no denominator changes, and no leaderboard.
- Defined engine runner boundaries for connection config, schema setup, source execution, candidate execution, timeout policy, result capture, error capture, cleanup, and local artifact directories.
- Defined checker invocation inputs and outputs, including source/candidate result artifacts, checker config, normalization config, compare config, mismatch summaries, normalized result artifacts, and fail-closed behavior.
- Defined result-normalization expectations for row ordering, duplicates, numeric tolerance, NULL rendering, date/time values, string/case rules, and engine-specific caveats.
- Defined future ledger extension fields with `local_execution_only=true`, `official_metric_input=false`, and `retained_evidence_input=false` for the user-run MVP.
- Defined execution/checker/exact status vocabularies, failure buckets, output policy, implementation safety gates, SQLGlot/Calcite/R-Bot relationship, and official metrics boundaries.
- Reviewed representative Common-core case structures read-only for `PERF_0006`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.
- Did not implement DB execution, run DB engines, implement checker execution, run checkers, collect timing, compute official metrics, render paper tables, implement paper reproduction, implement retained-evidence adapters, evaluate SQLGlot outputs, migrate cases, update `case_sets/`, update inventory, update reports/results, change denominators, change paper results, create a global leaderboard, modify the legacy repo, or modify raw legacy evidence.

Files created:
- `audits/b_line_db_checker_execution_design_v0/b_line_db_checker_execution_design_summary.md`
- `audits/b_line_db_checker_execution_design_v0/db_checker_execution_contract.csv`
- `audits/b_line_db_checker_execution_design_v0/db_checker_ledger_extension.csv`
- `audits/b_line_db_checker_execution_design_v0/db_checker_status_vocabulary.csv`
- `audits/b_line_db_checker_execution_design_v0/db_checker_output_policy.csv`
- `audits/b_line_db_checker_execution_design_v0/db_checker_safety_gates.csv`
- `audits/b_line_db_checker_execution_design_v0/future_b_line_db_checker_execution_mvp_prompt.md`
- `audits/b_line_db_checker_execution_design_v0/b_line_db_checker_execution_design_summary.json`
- `audits/b_line_db_checker_execution_design_v0/db_checker_execution_design_command_log.md`
- `audits/b_line_db_checker_execution_design_v0/db_checker_representative_case_structure_review.csv`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `PYTHONPATH=src python scripts/dev/run_user_entry_ci_smoke.py`: passed.
- `python scripts/dev/smoke_ledger_fixtures.py`: passed.
- Summary JSON invariant check: passed.
- CSV header/content checks: passed.
- Protected-path checks: passed; no files under `cases/`, `case_sets/`, `inventory/`, `reports/`, `results/`, or `runs/user` changed.
- `git diff --check`: passed before staging.

Task result:
- Design-only task: yes.
- DB/checker execution design completed: yes.
- DB execution implemented: no.
- Checker execution implemented: no.
- Timing implemented: no.
- Official metrics computed: no.
- Paper tables rendered: no.
- Reproduction CLI implemented: no.
- Retained-evidence adapter implemented: no.
- Global leaderboard created: no.
- case_sets changed: no.
- inventory changed: no.
- reports changed: no.
- results changed: no.
- denominator changed: no.
- paper results changed: no.
- raw legacy evidence changed: no.

Next safe action:
- Authorize `b_line_db_checker_execution_mvp_v0` only if a bounded postgres-only Common-core PERF local execution/checker MVP is desired, keeping outputs under `runs/user/` and preserving all official-metric, retained-evidence, reports/results, denominator, paper-result, and leaderboard boundaries.

### 2026-05-18 · c236710 · b_line_db_checker_execution_mvp_v0

Mode: bounded B-line DB/checker execution MVP environment preflight; blocked audit packet only; no DB execution implementation; no checker execution implementation; no timing; no official metrics; no paper tables; no retained-evidence adapter; no reports/results updates
Legacy repo modified: no
Release repo modified: yes
Commit: `c23671084c30743523c58a3ecb8a1983bf484532`
Push: succeeded; updated `origin/main` from `fcc32ce` to `c236710`

Summary:
- Attempted the bounded postgres-only Common-core PERF DB/checker MVP preflight.
- Confirmed `psql` is available with observed version `psql (PostgreSQL) 16.13 (Ubuntu 16.13-0ubuntu0.24.04.1)`.
- Confirmed no allowed Postgres connection configuration was present: `SQLRB_POSTGRES_DSN`, `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`, and `PGPASSWORD` were unset.
- Reviewed `PERF_0006` package assets read-only and confirmed the intended future smoke case has source SQL, positive SQL, checker config, normalization config, compare config, and Postgres schema/load files.
- Failed closed before implementation as required by task policy. No DB/checker code, tests, runner flags, ledger extensions, live DB smoke outputs, or fake execution artifacts were created.
- Did not modify the legacy repo, case packages, `case_sets/`, inventory, reports/results, denominators, paper results, retained evidence, raw legacy evidence, or case-local `runs/`.
- Did not compute official metrics, collect timing, render paper tables, implement paper reproduction, implement retained-evidence adapters, or create a global leaderboard.

Files created:
- `audits/b_line_db_checker_execution_mvp_v0/b_line_db_checker_execution_mvp_summary.md`
- `audits/b_line_db_checker_execution_mvp_v0/b_line_db_checker_execution_mvp_validation_results.csv`
- `audits/b_line_db_checker_execution_mvp_v0/b_line_db_checker_execution_mvp_summary.json`
- `audits/b_line_db_checker_execution_mvp_v0/db_checker_execution_mvp_command_log.md`
- `audits/b_line_db_checker_execution_mvp_v0/db_checker_execution_mvp_smoke_manifest.csv`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- Environment preflight: blocked because no allowed Postgres connection configuration was available.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests/user_entry -v`: passed, with two SQLGlot dependency smokes skipped because SQLGlot is not installed in the base environment.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python scripts/dev/run_user_entry_ci_smoke.py`: passed.
- `PYTHONDONTWRITEBYTECODE=1 python scripts/dev/smoke_ledger_fixtures.py`: passed.
- Summary JSON invariant check: passed.
- Protected-path checks: passed; no files under `cases/`, `case_sets/`, `inventory/`, `reports/`, `results/`, or `runs/user` changed or were staged by this task.
- `git diff --check`: passed before staging.

Task result:
- DB/checker execution MVP: blocked.
- Postgres-only: yes.
- Common-core PERF only: yes.
- Live Postgres smoke attempted: no.
- Live Postgres smoke passed: N.A.
- Source/candidate/checker artifacts captured: N.A.
- Local execution only: yes.
- Official metrics computed: no.
- Timing implemented: no.
- Paper tables rendered: no.
- Reproduction CLI implemented: no.
- Retained-evidence adapter implemented: no.
- Global leaderboard created: no.
- case_sets changed: no.
- inventory changed: no.
- reports changed: no.
- results changed: no.
- denominator changed: no.
- paper results changed: no.
- raw legacy evidence changed: no.

Next safe action:
- Provide local Postgres connection configuration through `SQLRB_POSTGRES_DSN` or libpq environment variables in the same shell, verify connection without logging secrets, then rerun or reauthorize `b_line_db_checker_execution_mvp_v0`.

### 2026-05-18 · 13433bd · b_line_db_checker_execution_mvp_v0_rerun

Mode: bounded B-line DB/checker execution MVP implementation; postgres-only local execution; local checker only; no timing; no official metrics; no paper tables; no retained-evidence adapter; no reports/results updates
Legacy repo modified: no
Release repo modified: yes
Commit: `13433bd64d2cb18a37a3d9495009ad3a8830cf21`
Push: succeeded; updated `origin/main` from `9256c54` to `13433bd`

Summary:
- Reauthorized the bounded postgres-only Common-core PERF DB/checker MVP after local Postgres preflight became available in the same shell.
- Implemented explicit opt-in user-run flags for local DB/checker behavior: `--enable-db-execution`, `--enable-checker`, `--postgres-dsn-env`, `--execution-timeout-sec`, and `--db-schema-prefix`.
- Added `src/sql_rewrite_bench/postgres_execution.py`, using the `psql` CLI and per-row local schemas to set up Postgres assets, run source SQL, run candidate SQL, capture JSONL results, and clean up schemas.
- Added `src/sql_rewrite_bench/local_result_checker.py`, a conservative local JSONL checker that requires case-local checker, normalization, and compare configs and writes local diagnostics only.
- Extended `ledger.csv` row grain with local DB/checker diagnostic fields while preserving non-DB defaults and setting `local_execution_only=true`, `official_metric_input=false`, and `retained_evidence_input=false`.
- Ran a bounded live smoke for `PERF_0006` using SQLGlot no-op candidate generation and local Postgres execution/checker output under `runs/user/db_checker_postgres_perf0006_smoke/`.
- Captured source result, candidate result, checker result, normalized result artifacts, and a successful local exact checker result.
- Did not modify the legacy repo, case packages, `case_sets/`, inventory, reports/results, denominators, paper results, retained evidence, raw legacy evidence, or case-local `runs/`.
- Did not compute official metrics, collect timing, render paper tables, implement paper reproduction, implement retained-evidence adapters, or create a global leaderboard.

Files created:
- `src/sql_rewrite_bench/postgres_execution.py`
- `src/sql_rewrite_bench/local_result_checker.py`
- `tests/user_entry/test_db_checker_execution_mvp.py`

Files modified:
- `src/sql_rewrite_bench/user_run_schema.py`
- `src/sql_rewrite_bench/user_run.py`
- `audits/b_line_db_checker_execution_mvp_v0/b_line_db_checker_execution_mvp_summary.md`
- `audits/b_line_db_checker_execution_mvp_v0/b_line_db_checker_execution_mvp_validation_results.csv`
- `audits/b_line_db_checker_execution_mvp_v0/b_line_db_checker_execution_mvp_summary.json`
- `audits/b_line_db_checker_execution_mvp_v0/db_checker_execution_mvp_command_log.md`
- `audits/b_line_db_checker_execution_mvp_v0/db_checker_execution_mvp_smoke_manifest.csv`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- Postgres preflight: passed with `psql -c "select 1;"`; connection source recorded only as redacted libpq environment state.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests/user_entry -v`: passed, 27 tests run with one SQLGlot missing-dependency guard skipped because SQLGlot is installed.
- Bounded live Postgres smoke: passed for `PERF_0006` with source execution success, candidate execution success, checker success, and local exact status.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python scripts/dev/run_user_entry_ci_smoke.py`: passed.
- `PYTHONDONTWRITEBYTECODE=1 python scripts/dev/smoke_ledger_fixtures.py`: passed.
- Summary JSON invariant check: passed.
- Protected-path checks: passed; no files under `cases/`, `case_sets/`, `inventory/`, `reports/`, `results/`, or tracked `runs/user` changed.
- `git diff --check`: passed before staging.

Task result:
- DB/checker execution MVP: yes.
- Postgres-only: yes.
- Common-core PERF only: yes.
- Live Postgres smoke attempted: yes.
- Live Postgres smoke passed: yes.
- Source execution result captured: yes.
- Candidate execution result captured: yes.
- Checker result captured: yes.
- Local execution only: yes.
- Official metrics computed: no.
- Timing implemented: no.
- Paper tables rendered: no.
- Reproduction CLI implemented: no.
- Retained-evidence adapter implemented: no.
- Global leaderboard created: no.
- case_sets changed: no.
- inventory changed: no.
- reports changed: no.
- results changed: no.
- denominator changed: no.
- paper results changed: no.
- raw legacy evidence changed: no.

Next safe action:
- Authorize a DB/checker MVP hardening or release-smoke task that reruns the postgres-only local execution/checker path in a fresh environment, then optionally expands only to `PERF_0007` under the same local-only boundaries.

### 2026-05-19 · 4d5de7c · b_line_db_checker_execution_release_smoke_v0

Mode: B-line DB/checker execution release-smoke; fresh-checkout editable-install verification only; no new feature implementation; no timing; no official metrics; no paper tables; no retained-evidence adapter; no reports/results updates
Legacy repo modified: no
Release repo modified: yes
Commit: `4d5de7c516c9849aabab1d9763c1a4d06d54449b`
Push: succeeded; updated `origin/main` from `1679bc9` to `4d5de7c`

Summary:
- Verified the bounded postgres-only DB/checker execution MVP from a fresh local clone under `/tmp/sqlrb_db_checker_release_smoke/Rewritebench_v0_db_smoke`.
- Created a temporary virtual environment and installed the package with `python -m pip install -e ".[sqlglot]"`.
- Confirmed SQLGlot import in the temporary environment with observed version `30.8.0`.
- Confirmed Postgres connectivity with `psql -c "select 1;"` in both the release repo and temporary clone, without logging DB passwords, full DSNs, or environment values.
- Ran the bounded smoke for `PERF_0006` only, `postgres` only, SQLGlot no-op adapter only, local output only under `runs/user/db_checker_release_smoke_perf0006/`.
- Confirmed source execution result, candidate execution result, and checker result artifacts were captured.
- Confirmed the temporary smoke ledger had `source_execution_status=source_execution_success`, `candidate_execution_status=candidate_execution_success`, `checker_status=checker_success`, `exact_status=exact`, `failure_bucket=none`, `local_execution_only=true`, `official_metric_input=false`, and `retained_evidence_input=false`.
- Confirmed smoke output remained ignored/untracked under `runs/user/` and protected benchmark surfaces were unchanged.
- Did not modify source implementation files, tests, docs, pyproject, case packages, `case_sets/`, inventory, reports/results, denominators, paper results, retained evidence, raw legacy evidence, or the legacy repo.
- Did not compute official metrics, collect timing, render paper tables, implement paper reproduction, implement retained-evidence adapters, implement MySQL/Spark execution, implement Calcite/R-Bot adapters, or create a global leaderboard.

Files created:
- `audits/b_line_db_checker_execution_release_smoke_v0/b_line_db_checker_execution_release_smoke_summary.md`
- `audits/b_line_db_checker_execution_release_smoke_v0/b_line_db_checker_execution_release_smoke_validation_results.csv`
- `audits/b_line_db_checker_execution_release_smoke_v0/b_line_db_checker_execution_release_smoke_summary.json`
- `audits/b_line_db_checker_execution_release_smoke_v0/db_checker_execution_release_smoke_command_log.md`
- `audits/b_line_db_checker_execution_release_smoke_v0/db_checker_execution_release_smoke_manifest.csv`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- Release repo preflight: passed.
- Temporary clone creation: passed.
- Temporary venv creation: passed.
- Editable install with SQLGlot extra: passed.
- SQLGlot import: passed.
- Postgres connectivity: passed.
- Fresh-checkout DB/checker smoke: passed.
- Source/candidate/checker artifact checks: passed.
- Ledger local-only field checks: passed.
- Temporary clone output hygiene and protected-path checks: passed.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python scripts/dev/run_user_entry_ci_smoke.py`: passed.
- `PYTHONDONTWRITEBYTECODE=1 python scripts/dev/smoke_ledger_fixtures.py`: passed.
- Summary JSON invariant check: passed.
- `git diff --check`: passed before staging.

Task result:
- DB/checker release-smoke task: yes.
- Fresh-checkout smoke passed: yes.
- Editable install passed: yes.
- SQLGlot import passed: yes.
- Postgres connectivity passed: yes.
- DB/checker smoke passed: yes.
- Source execution result captured: yes.
- Candidate execution result captured: yes.
- Checker result captured: yes.
- Ledger local-only fields verified: yes.
- Output hygiene passed: yes.
- Smoke outputs staged: no.
- Local execution only: yes.
- Official metrics computed: no.
- Timing implemented: no.
- Paper tables rendered: no.
- Reproduction CLI implemented: no.
- Retained-evidence adapter implemented: no.
- Global leaderboard created: no.
- case_sets changed: no.
- inventory changed: no.
- reports changed: no.
- results changed: no.
- denominator changed: no.
- paper results changed: no.
- raw legacy evidence changed: no.

Next safe action:
- Authorize a bounded DB/checker hardening task under the same local-only boundaries, or authorize a separate narrowly scoped `PERF_0007` expansion smoke.

### 2026-05-19 · 35a30dd · b_line_db_checker_batch_plan_v0

Mode: B-line DB/checker batch expansion planning; design/selection only; no batch execution; no DB/checker execution; no timing; no official metrics; no paper tables; no retained-evidence adapter; no reports/results updates
Legacy repo modified: no
Release repo modified: yes
Commit: `35a30dd66c3a36ecaec681c4f4cf9c73d5a5bf20`
Push: succeeded; updated `origin/main` from `e3a76e1` to `35a30dd`

Summary:
- Planned the first bounded postgres PERF DB/checker batch expansion after the successful `PERF_0006` MVP and release smoke.
- Built the candidate universe from `case_sets/common_core_v0/cases.csv` and `case_sets/common_core_v0/denominator_same_engine_120.csv`, filtering to Common-core PERF postgres rows only.
- Static-readiness reviewed all 16 Common-core PERF candidates for source SQL, postgres DDL/load, checker config, normalization config, compare config, and denominator-eligibility file presence without modifying case packages.
- Marked `PERF_0006` as the prior canary verified by DB/checker release smoke and excluded it from the new batch selection.
- Recommended a four-case first batch: `PERF_0007`, `PERF_0008`, `PERF_0013`, and `PERF_0017`.
- Drafted a future `b_line_postgres_perf_batch_smoke_v0` prompt that executes only selected rows under `runs/user/` with SQLGlot no-op, postgres only, no timing, no official metrics, no retained evidence, no reports/results updates, no denominator changes, no paper-result changes, and no leaderboard.
- Did not run DB execution, run checkers, collect timing, compute official metrics, render paper tables, implement paper reproduction, implement retained-evidence adapters, update reports/results, update `case_sets/`, update inventory, change denominators, change paper results, modify case packages, modify the legacy repo, or modify raw legacy evidence.

Files created:
- `audits/b_line_db_checker_batch_plan_v0/b_line_db_checker_batch_plan_summary.md`
- `audits/b_line_db_checker_batch_plan_v0/common_core_perf_postgres_candidate_readiness.csv`
- `audits/b_line_db_checker_batch_plan_v0/postgres_perf_batch_selection.csv`
- `audits/b_line_db_checker_batch_plan_v0/postgres_perf_batch_stop_conditions.csv`
- `audits/b_line_db_checker_batch_plan_v0/future_b_line_postgres_perf_batch_smoke_prompt.md`
- `audits/b_line_db_checker_batch_plan_v0/b_line_db_checker_batch_plan_summary.json`
- `audits/b_line_db_checker_batch_plan_v0/db_checker_batch_plan_command_log.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python scripts/dev/run_user_entry_ci_smoke.py`: passed.
- `PYTHONDONTWRITEBYTECODE=1 python scripts/dev/smoke_ledger_fixtures.py`: passed.
- Summary JSON invariant check: passed.
- CSV content checks: passed; readiness covers all 16 Common-core PERF postgres candidates, selected batch size is 4, `PERF_0006` is prior canary and not selected, selected rows have required assets, and required stop-condition families are present.
- Protected-path checks: passed; no files under `cases/`, `case_sets/`, `inventory/`, `reports/`, `results/`, or tracked `runs/user` changed.
- `git diff --check`: passed.

Task result:
- Batch plan task: yes.
- Design-only task: yes.
- Batch execution performed: no.
- Candidate universe: Common-core PERF postgres.
- Recommended batch size: 4.
- Recommended batch case IDs: `PERF_0007`, `PERF_0008`, `PERF_0013`, and `PERF_0017`.
- Prior canary case IDs: `PERF_0006`.
- DB execution implemented by this task: no.
- Checker execution implemented by this task: no.
- Timing implemented: no.
- Official metrics computed: no.
- Paper tables rendered: no.
- Reproduction CLI implemented: no.
- Retained-evidence adapter implemented: no.
- Global leaderboard created: no.
- case_sets changed: no.
- inventory changed: no.
- reports changed: no.
- results changed: no.
- denominator changed: no.
- paper results changed: no.
- raw legacy evidence changed: no.

Next safe action:
- Authorize `b_line_postgres_perf_batch_smoke_v0` to execute only the selected postgres PERF SQLGlot no-op batch under `runs/user/`, with no timing, official metrics, retained evidence, reports/results updates, denominator changes, paper-result changes, or leaderboard output.

### 2026-05-19 · e3f598a · b_line_postgres_perf_batch_smoke_v0

Mode: bounded B-line Postgres PERF DB/checker batch smoke; local user-run output only; SQLGlot no-op adapter command only; no timing; no official metrics; no paper tables; no retained-evidence adapter; no reports/results updates
Legacy repo modified: no
Release repo modified: yes
Commit: `e3f598a0837303161d49f1ed5be1802643330ceb`
Push: succeeded; updated `origin/main` from `272899f` to `e3f598a`

Summary:
- Executed the first bounded local Postgres PERF DB/checker batch after the `PERF_0006` canary and release smoke.
- Used exactly four Common-core PERF postgres cases: `PERF_0007`, `PERF_0008`, `PERF_0013`, and `PERF_0017`.
- Used the existing method-agnostic user runner with adapter command `python baselines/sqlglot/sqlglot_user_adapter.py --route noop`.
- Wrote local run output only under `runs/user/postgres_perf_sqlglot_noop_batch_smoke/`; this output remained ignored and unstaged.
- Confirmed all four rows generated candidate SQL, captured source execution results, captured candidate execution results, ran the local checker, and recorded local exact results.
- Did not modify source implementation files, tests, docs, pyproject, case packages, `case_sets/`, inventory, reports/results, denominators, paper results, retained evidence, raw legacy evidence, or the legacy repo.
- Did not compute official metrics, collect timing, render paper tables, implement paper reproduction, implement retained-evidence adapters, or create a global leaderboard.

Files created:
- `audits/b_line_postgres_perf_batch_smoke_v0/postgres_perf_batch_cases.txt`
- `audits/b_line_postgres_perf_batch_smoke_v0/b_line_postgres_perf_batch_smoke_summary.md`
- `audits/b_line_postgres_perf_batch_smoke_v0/b_line_postgres_perf_batch_smoke_results.csv`
- `audits/b_line_postgres_perf_batch_smoke_v0/b_line_postgres_perf_batch_smoke_validation_results.csv`
- `audits/b_line_postgres_perf_batch_smoke_v0/b_line_postgres_perf_batch_smoke_summary.json`
- `audits/b_line_postgres_perf_batch_smoke_v0/postgres_perf_batch_smoke_command_log.md`
- `audits/b_line_postgres_perf_batch_smoke_v0/postgres_perf_batch_smoke_manifest.csv`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- Postgres preflight: passed with `psql --version` and `psql -c "select 1;"`; DB credentials and environment values were not recorded.
- SQLGlot import: passed.
- Batch runner command: passed; selected rows 4 and candidate-generated rows 4.
- Row verification: passed; source/candidate/checker artifacts exist for all four selected rows.
- Ledger local-only checks: passed; every row has `local_execution_only=true`, `official_metric_input=false`, and `retained_evidence_input=false`.
- Status vocabulary and failure buckets: passed; all four rows recorded source/candidate execution success, checker success, exact, and failure bucket `none`.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python scripts/dev/run_user_entry_ci_smoke.py`: passed.
- `PYTHONDONTWRITEBYTECODE=1 python scripts/dev/smoke_ledger_fixtures.py`: passed.
- Summary JSON invariant check: passed.
- CSV checks: passed; results CSV has exactly four data rows, selected case IDs match, local-only flags are correct, and no timing/speedup columns were introduced.
- Protected-path checks: passed; no files under `cases/`, `case_sets/`, `inventory/`, `reports/`, `results/`, or tracked `runs/user` changed.
- `git diff --check`: passed.

Task result:
- Batch execution performed: yes.
- Selected case IDs: `PERF_0007`, `PERF_0008`, `PERF_0013`, and `PERF_0017`.
- Selected rows: 4.
- Candidate-generated rows: 4.
- Source execution success rows: 4.
- Candidate execution success rows: 4.
- Checker success rows: 4.
- Checker mismatch rows: 0.
- Exact rows local: 4.
- Mismatch rows local: 0.
- Local execution only: yes.
- Official metrics computed: no.
- Timing implemented: no.
- Paper tables rendered: no.
- Reproduction CLI implemented: no.
- Retained-evidence adapter implemented: no.
- Global leaderboard created: no.
- case_sets changed: no.
- inventory changed: no.
- reports changed: no.
- results changed: no.
- denominator changed: no.
- paper results changed: no.
- raw legacy evidence changed: no.

Next safe action:
- Review the four-row local batch smoke. If acceptable, authorize a separate bounded follow-up for either another small PERF postgres batch or DB/checker hardening, still with local `runs/user/` output only and no timing, official metrics, retained evidence, reports/results updates, denominator changes, paper-result changes, or leaderboard output.

### 2026-05-19 · 58eb7d6 · case_package_v2_external_schema_branch_pilot_v0

Branch: `feature/case-package-v2-external-schema`
Mode: major case package standard upgrade branch pilot; PERF_0006 only; external schema copy-first adoption; B-line user-entry development frozen; no DB execution; no checker execution; no timing; no official metrics; no reports/results updates
Legacy repo modified: no
Release repo modified: yes
Commit: `58eb7d694fbdd4ea9ff72cfdaa52f77f8827a2a7`
Push: succeeded; pushed branch `feature/case-package-v2-external-schema` to origin

Summary:
- Created and worked on branch `feature/case-package-v2-external-schema` from updated `main`.
- Recorded decision D019 in `project_control/DECISION_LOG.md`, freezing further B-line user-entry/DB-checker expansion while case package v2 external-schema adoption is piloted.
- Pilot-converted only `PERF_0006` to the branch-pilot v2 direction.
- Added direct SQL copies `sql/pos_01.sql` and `sql/neg_01.sql` while retaining legacy `sql/positives/` and `sql/negatives/` paths for compatibility.
- Created external schema package `schemas/tpch_common_core_v0/` with copied postgres, mysql, and spark DDL/load files plus `schema_profile.yaml`.
- Added `schema_ref` to `PERF_0006` manifest while retaining the case-local `schema/` directory and marking it as a compatibility copy.
- Created `witness/data_profile.yaml` and `witness/correct_result.csv` from existing public-safe witness metadata and retained PostgreSQL source output; no DB run was performed.
- Added generic `validation/run_validation.sh` and `validation/run_plan_collection.sh` wrappers that do not execute DB engines or write case-local `runs/` during the branch pilot.
- Did not delete case-local `runs/`, delete case-local schema assets, modify any case besides `PERF_0006`, update `case_sets/`, update inventory, update reports/results, change denominators, change paper results, modify raw legacy evidence, compute metrics, render paper tables, or create leaderboard output.

Files created:
- `cases/PERF/PERF_0006/sql/pos_01.sql`
- `cases/PERF/PERF_0006/sql/neg_01.sql`
- `cases/PERF/PERF_0006/witness/data_profile.yaml`
- `cases/PERF/PERF_0006/witness/correct_result.csv`
- `cases/PERF/PERF_0006/validation/run_validation.sh`
- `cases/PERF/PERF_0006/validation/run_plan_collection.sh`
- `schemas/tpch_common_core_v0/schema_profile.yaml`
- `schemas/tpch_common_core_v0/postgres/ddl.sql`
- `schemas/tpch_common_core_v0/postgres/load.sql`
- `schemas/tpch_common_core_v0/mysql/ddl.sql`
- `schemas/tpch_common_core_v0/mysql/load.sql`
- `schemas/tpch_common_core_v0/spark/ddl.sql`
- `schemas/tpch_common_core_v0/spark/load.sql`
- `audits/case_package_v2_external_schema_branch_pilot_v0/case_package_v2_branch_pilot_summary.md`
- `audits/case_package_v2_external_schema_branch_pilot_v0/case_package_v2_path_crosswalk.csv`
- `audits/case_package_v2_external_schema_branch_pilot_v0/external_schema_mapping_pilot.csv`
- `audits/case_package_v2_external_schema_branch_pilot_v0/pilot_case_conversion_manifest.csv`
- `audits/case_package_v2_external_schema_branch_pilot_v0/case_package_v2_validation_results.csv`
- `audits/case_package_v2_external_schema_branch_pilot_v0/future_case_package_v2_common_core_pilot_prompt.md`
- `audits/case_package_v2_external_schema_branch_pilot_v0/case_package_v2_branch_pilot_summary.json`
- `audits/case_package_v2_external_schema_branch_pilot_v0/case_package_v2_branch_command_log.md`

Files modified:
- `cases/PERF/PERF_0006/README.md`
- `cases/PERF/PERF_0006/manifest.yaml`
- `cases/PERF/PERF_0006/checker/checker.yaml`
- `cases/PERF/PERF_0006/checker/expected_rejections.yaml`
- `cases/PERF/PERF_0006/schema/schema_profile.yaml`
- `project_control/DECISION_LOG.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- Branch check: passed; current branch is `feature/case-package-v2-external-schema`.
- YAML parse checks: passed for `PERF_0006` manifest, external schema profile, and witness data profile.
- Static path checks: passed for direct SQL, witness, checker, runs-retention, and external schema files.
- Optional non-DB user-entry CI smoke: help/tests/dry-run/dummy-adapter portions passed, then expectedly failed the protected-path guard because this branch intentionally modifies `cases/PERF/PERF_0006`; no runner patch was made.
- Protected-boundary checks: passed; `case_sets/`, inventory, reports/results, denominator files, paper result files, and raw legacy evidence were not changed.
- `git diff --check`: passed.

Task result:
- Major decision recorded: yes.
- B-line user-entry development frozen: yes.
- Case package v2 external schema pilot performed: yes.
- Pilot case IDs: `PERF_0006`.
- Cases modified: `PERF_0006` only.
- Schemas created: `schemas/tpch_common_core_v0/`.
- External schema refs added: yes.
- Old case-local schema deleted: no.
- Case-local runs deleted: no.
- case_sets changed: no.
- inventory changed: no.
- reports/results changed: no.
- denominator changed: no.
- paper results changed: no.
- raw legacy evidence changed: no.
- official metrics computed: no.
- paper tables rendered: no.
- global leaderboard created: no.

Next safe action:
- Review the `PERF_0006` v2 external-schema branch pilot. If accepted, authorize a branch-only expansion to `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011` without merging to `main` until v2 validator and runner `schema_ref` compatibility is approved.

### 2026-05-19 · 18f85c7 · case_package_v2_masterplan_assets_strategy_v0

Branch: `feature/case-package-v2-external-schema`
Mode: case package v2 master plan and assets strategy; policy/spec-only; no case conversion; no DB execution; no checker execution; no timing; no official metrics; no reports/results migration
Legacy repo modified: no
Release repo modified: yes
Commit: `18f85c76e42bd96f73790e817cfdeb40b7e6bfe7`
Push: succeeded; pushed branch `feature/case-package-v2-external-schema` to origin

Summary:
- Recorded the case package v2 assets strategy after the `PERF_0006` external-schema branch pilot.
- Updated `project_control/MIGRATION_MASTER_PLAN.md` with a v2 target addendum that keeps v1 as compatibility context and defines v2 target case-local layout, external schema layout, external evidence layout, `schema_ref`, `evidence_ref`, validation entrypoints, source-as-oracle witness policy, artifact boundaries, and branch-only adoption roadmap.
- Added decision log entries D020 through D024 for v2 target layout, external schema strategy, external evidence strategy, validation entrypoint consolidation, and runtime source-as-oracle witness policy.
- Created repository spec drafts for the v2 case package contract, external schema contract, external evidence contract, validation entrypoint policy, and runtime witness policy.
- Created audit outputs for asset boundaries, manifest references, migration roadmap, open questions, future runner/validator compatibility prompt, summary JSON, and command log.
- Did not modify case packages, schema asset contents, `case_sets/`, inventory, reports/results, denominator files, paper result files, raw legacy evidence, or the legacy repo.

Files created:
- `repository_spec/case_package_contract_v2_draft.md`
- `repository_spec/external_schema_contract_v1_draft.md`
- `repository_spec/external_evidence_contract_v1_draft.md`
- `repository_spec/validation_entrypoint_policy_v1_draft.md`
- `repository_spec/runtime_witness_policy_v1_draft.md`
- `audits/case_package_v2_masterplan_assets_strategy_v0/case_package_v2_assets_strategy_summary.md`
- `audits/case_package_v2_masterplan_assets_strategy_v0/v2_asset_boundary_matrix.csv`
- `audits/case_package_v2_masterplan_assets_strategy_v0/v2_manifest_reference_model.csv`
- `audits/case_package_v2_masterplan_assets_strategy_v0/v2_migration_roadmap.csv`
- `audits/case_package_v2_masterplan_assets_strategy_v0/v2_open_questions.csv`
- `audits/case_package_v2_masterplan_assets_strategy_v0/future_case_package_v2_runner_validator_compatibility_prompt.md`
- `audits/case_package_v2_masterplan_assets_strategy_v0/case_package_v2_assets_strategy_summary.json`
- `audits/case_package_v2_masterplan_assets_strategy_v0/case_package_v2_assets_strategy_command_log.md`

Files modified:
- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/DECISION_LOG.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- Branch check: passed; current branch is `feature/case-package-v2-external-schema`.
- Master-plan addendum check: passed; `MIGRATION_MASTER_PLAN.md` contains the case package v2 target addendum.
- Decision-log check: passed; D020-D024 are present.
- Repository spec existence check: passed; all five draft specs exist.
- Audit CSV header check: passed.
- Summary JSON parse check: passed.
- Protected-boundary checks: passed; no files under `cases/`, `schemas/`, `case_sets/`, inventory, reports, or results changed.
- `git diff --check`: passed.

Task result:
- Master plan updated: yes.
- Decision log updated: yes.
- Repository spec drafts created: yes.
- Case package v2 strategy recorded: yes.
- External schema strategy recorded: yes.
- External evidence strategy recorded: yes.
- Validation consolidation strategy recorded: yes.
- Runtime witness policy recorded: yes.
- Case files modified: no.
- Schemas modified: no.
- case_sets changed: no.
- inventory changed: no.
- reports/results changed: no.
- denominator changed: no.
- paper results changed: no.
- raw legacy evidence changed: no.
- official metrics computed: no.
- paper tables rendered: no.
- global leaderboard created: no.

Next safe action:
- Authorize `case_package_v2_runner_validator_compatibility_v0` on `feature/case-package-v2-external-schema` to add non-destructive `schema_ref` and `evidence_ref` validation and recheck `PERF_0006` without bulk case conversion.

### 2026-05-19 · df3ad37 · case_package_v2_runner_validator_compatibility_v0

Branch: `feature/case-package-v2-external-schema`
Mode: branch-only non-destructive v2 resolver and validator compatibility; `PERF_0006` recheck only; no case conversion; no DB/checker execution; no timing; no official metrics
Legacy repo modified: no
Release repo modified: yes
Commit: `df3ad375e953c4a568b2d760abeada9d254b89e5`
Push: succeeded; pushed branch `feature/case-package-v2-external-schema` to origin

Summary:
- Added `src/sql_rewrite_bench/case_package_v2_resolver.py`, a static resolver for v2 direct SQL paths, checker references, `schema_ref`, optional `evidence_ref`, witness metadata paths, and validation entrypoints.
- Added `scripts/dev/validate_case_package_v2_refs.py`, a developer validator that performs path existence, path safety, and internal-format checks without executing DB engines, running checkers, parsing retained evidence, computing metrics, or writing into case packages.
- Added unit tests under `tests/case_package_v2/` for valid synthetic v2 manifests, missing schema paths, optional witness warnings, absolute path failure, and read-only `PERF_0006` validation.
- Rechecked `PERF_0006` only in read-only mode. Required references resolved safely and existed; internal-format compatibility findings were warning-only.
- Generated audit outputs under `audits/case_package_v2_runner_validator_compatibility_v0/`.
- Did not modify any case package files, schema asset files, `case_sets/`, inventory, reports/results, denominators, paper results, raw legacy evidence, or the legacy repo.

Files created:
- `src/sql_rewrite_bench/case_package_v2_resolver.py`
- `scripts/dev/validate_case_package_v2_refs.py`
- `tests/case_package_v2/test_case_package_v2_resolver.py`
- `audits/case_package_v2_runner_validator_compatibility_v0/v2_runner_validator_compatibility_summary.md`
- `audits/case_package_v2_runner_validator_compatibility_v0/v2_ref_validation_results.csv`
- `audits/case_package_v2_runner_validator_compatibility_v0/perf0006_v2_ref_check.csv`
- `audits/case_package_v2_runner_validator_compatibility_v0/v2_internal_format_contract.csv`
- `audits/case_package_v2_runner_validator_compatibility_v0/perf0006_internal_format_check.csv`
- `audits/case_package_v2_runner_validator_compatibility_v0/v2_format_inconsistency_findings.csv`
- `audits/case_package_v2_runner_validator_compatibility_v0/perf0006_directory_classification.csv`
- `audits/case_package_v2_runner_validator_compatibility_v0/v2_compatibility_gaps.csv`
- `audits/case_package_v2_runner_validator_compatibility_v0/future_case_package_v2_multi_pool_pilot_prompt.md`
- `audits/case_package_v2_runner_validator_compatibility_v0/v2_runner_validator_compatibility_summary.json`
- `audits/case_package_v2_runner_validator_compatibility_v0/v2_runner_validator_command_log.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`: passed, 5 tests.
- `PYTHONPATH=src python scripts/dev/validate_case_package_v2_refs.py --case cases/PERF/PERF_0006`: passed.
- `PERF_0006` recheck status: pass; 17 resolved references, 40 internal checks, 19 warning-only format findings.
- Summary JSON parse and boundary assertions: passed.
- Protected-boundary checks: passed; no files under `cases/`, `schemas/`, `case_sets/`, inventory, reports, or results changed.
- Case-local runs deletion check: passed; no case-local `runs/` files were created, modified, or deleted by this task.
- DB/checker execution output check: passed; no DB/checker execution outputs were created.
- Leaderboard output check: passed; no leaderboard output was created.
- `git diff --check`: passed.

Task result:
- Resolver created: yes.
- Validator created: yes.
- `PERF_0006` rechecked: yes.
- Internal format guard added: yes.
- Case files modified: no.
- Schemas modified: no.
- case_sets changed: no.
- inventory changed: no.
- reports/results changed: no.
- denominator changed: no.
- paper results changed: no.
- raw legacy evidence changed: no.
- official metrics computed: no.
- DB/checker execution run: no.
- paper tables rendered: no.
- global leaderboard created: no.

Next safe action:
- Authorize a branch-only `case_package_v2_multi_pool_pilot_v0` using the new static validator, optionally first normalizing `PERF_0006` manifest internal shape to canonical v2, then pilot-converting only `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011` without merging to `main`.

### 2026-05-19 · 974e892 · case_package_v2_perf0006_format_normalization_v0

Branch: `feature/case-package-v2-external-schema`
Mode: branch-only PERF_0006 manifest/internal-format normalization; no multi-case conversion; no schema/evidence deletion; no DB/checker execution; no timing; no official metrics
Legacy repo modified: no
Release repo modified: yes
Commit: `974e8926e22715b7a4212353696b0274dc48dffe`
Push: succeeded; pushed branch `feature/case-package-v2-external-schema` to origin

Summary:
- Normalized only `cases/PERF/PERF_0006/manifest.yaml` to the canonical v2 internal reference shape.
- Converted `sql.positives` and `sql.negatives` from mapping entries to direct string paths.
- Converted `schema_ref` to `schema_ref.engines.<engine>.ddl/load`.
- Converted `checker.checker` to canonical `checker.config`.
- Added canonical witness policy fields for source-as-oracle runtime checking.
- Added `evidence_ref` with pending copy-first externalization status and required case-local compatibility evidence references.
- Moved legacy SQL metadata, case-local schema references, and engine-specific validation scripts into one top-level `compatibility` block.
- Updated `PERF_0006` README wording to describe the canonical manifest status and retained compatibility boundaries.
- Aligned the static v2 validator/test with the required `compatibility` top-level block after the normalized manifest exposed a false positive.
- Did not modify schemas, delete case-local schema/evidence/runs, change `case_sets/`, change inventory, update reports/results, change denominators, change paper results, modify raw legacy evidence, compute metrics, run DB/checker execution, or create leaderboard output.

Files created:
- `audits/case_package_v2_perf0006_format_normalization_v0/perf0006_format_normalization_summary.md`
- `audits/case_package_v2_perf0006_format_normalization_v0/perf0006_manifest_format_before_after.csv`
- `audits/case_package_v2_perf0006_format_normalization_v0/perf0006_remaining_compatibility_warnings.csv`
- `audits/case_package_v2_perf0006_format_normalization_v0/perf0006_format_validation_results.csv`
- `audits/case_package_v2_perf0006_format_normalization_v0/perf0006_format_normalization_summary.json`
- `audits/case_package_v2_perf0006_format_normalization_v0/perf0006_format_normalization_command_log.md`

Files modified:
- `cases/PERF/PERF_0006/manifest.yaml`
- `cases/PERF/PERF_0006/README.md`
- `src/sql_rewrite_bench/case_package_v2_resolver.py`
- `tests/case_package_v2/test_case_package_v2_resolver.py`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- Manifest canonical-shape assertion: passed.
- `PYTHONPATH=src python scripts/dev/validate_case_package_v2_refs.py --case cases/PERF/PERF_0006`: passed with `overall_status=pass` and `format_findings=0`.
- `PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`: passed, 5 tests.
- Summary JSON parse and boundary assertions: passed.
- Protected-boundary checks: passed; no files under `schemas/`, `case_sets/`, inventory, reports, or results changed.
- `git diff --check`: passed.

Task result:
- PERF_0006 manifest normalized: yes.
- Cases modified: `PERF_0006` only.
- Schemas modified: no.
- Case-local schema/evidence/runs deleted: no.
- case_sets/inventory/reports/results changed: no.
- denominator/paper results changed: no.
- raw legacy evidence changed: no.
- official metrics computed: no.
- DB/checker execution run: no.
- global leaderboard created: no.

Next safe action:
- Authorize a branch-only multi-pool v2 pilot using normalized `PERF_0006` as the canonical example, limited to `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`, without merging to `main`.

### 2026-05-19 · 3ba7d95 · case_package_v2_conversion_rulebook_v0

Branch: `feature/case-package-v2-external-schema`
Mode: branch-only case package v2 conversion rulebook; no case conversion; no schema modification; no DB/checker execution; no official metrics; no paper rendering
Legacy repo modified: no
Release repo modified: yes
Commit: `3ba7d95533c390380ec7f44fff2544d2c9f76722`
Push: succeeded; pushed branch `feature/case-package-v2-external-schema` to origin

Summary:
- Created a detailed v2 conversion rulebook for turning v1 and v1-compatible case packages into the v2 template shape.
- Recorded final v2 case-local target structure, external schema target, external evidence target, user-run output boundary, and paper retained/reporting boundary.
- Recorded file disposition rules for current package paths including SQL, checker, schema, data/witness, validation, evidence, metadata, notes, runs, reports, and results.
- Recorded canonical manifest field contract, validation wrapper consolidation policy, evidence/runs cleanup policy, batch conversion algorithm, stop conditions, and future converter dry-run prompt.
- Did not modify case files, schemas, `case_sets/`, inventory, reports/results, denominators, paper results, raw legacy evidence, DB/checker execution code, or leaderboard outputs.

Files created:
- `repository_spec/case_package_v2_conversion_rulebook_draft.md`
- `audits/case_package_v2_conversion_rulebook_v0/case_package_v2_conversion_rulebook_summary.md`
- `audits/case_package_v2_conversion_rulebook_v0/v2_file_disposition_matrix.csv`
- `audits/case_package_v2_conversion_rulebook_v0/v2_manifest_field_contract.csv`
- `audits/case_package_v2_conversion_rulebook_v0/v2_validation_consolidation_matrix.csv`
- `audits/case_package_v2_conversion_rulebook_v0/v2_evidence_runs_disposition_matrix.csv`
- `audits/case_package_v2_conversion_rulebook_v0/v2_batch_conversion_algorithm.md`
- `audits/case_package_v2_conversion_rulebook_v0/future_case_package_v2_batch_converter_plan_prompt.md`
- `audits/case_package_v2_conversion_rulebook_v0/case_package_v2_conversion_rulebook_summary.json`
- `audits/case_package_v2_conversion_rulebook_v0/case_package_v2_conversion_rulebook_command_log.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- Branch check: passed.
- Required rulebook file existence check: passed.
- CSV header checks: passed.
- Summary JSON parse and boundary assertions: passed.
- Protected-boundary checks: passed; no files under `cases/`, `schemas/`, `case_sets/`, inventory, reports, or results changed.
- `git diff --check`: passed.

Task result:
- Conversion rulebook created: yes.
- Validation consolidation policy recorded: yes.
- Evidence/runs disposition recorded: yes.
- Manifest field contract recorded: yes.
- Batch conversion algorithm recorded: yes.
- Case files modified: no.
- Schemas modified: no.
- case_sets/inventory/reports/results changed: no.
- denominator/paper results changed: no.
- official metrics computed: no.
- DB/checker execution run: no.
- global leaderboard created: no.

Next safe action:
- Authorize `case_package_v2_batch_converter_plan_v0` as a read-only converter dry-run over `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011` before any additional writable conversion.

### 2026-05-19 · 813171f · case_package_v2_batch_converter_plan_v0

Branch: `feature/case-package-v2-external-schema`
Mode: branch-only read-only converter dry-run planning; no writable case conversion; no cleanup; no schema/evidence deletion; no DB/checker execution; no official metrics
Legacy repo modified: no
Release repo modified: yes
Commit: `813171f9bbe75c7b77fd1f3c3aaae1b7624329b6`
Push: succeeded; pushed branch `feature/case-package-v2-external-schema` to origin

Summary:
- Produced a read-only v2 batch conversion plan for `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.
- Classified SQL, schema, checker, witness/data, evidence/runs, metadata/notes, validation scripts, and manifest conversion needs for each pilot case.
- Identified `PERF_0006` as the normalized reference case and the other four cases as requiring manual-review blockers before writable conversion.
- Proposed external schema ids and evidence targets without creating or modifying schema/evidence files.
- Recorded stop conditions for schema externalization, direct SQL copies, wrapper creation, dialect variants, evidence externalization, source-as-oracle manifest fields, and validation scripts that write to case-local runs.
- Did not modify any files under `cases/`, `schemas/`, `case_sets/`, inventory, reports, results, denominators, paper results, or raw legacy evidence.

Files created:
- `audits/case_package_v2_batch_converter_plan_v0/case_package_v2_batch_converter_plan_summary.md`
- `audits/case_package_v2_batch_converter_plan_v0/v2_batch_case_readiness.csv`
- `audits/case_package_v2_batch_converter_plan_v0/v2_batch_file_disposition_plan.csv`
- `audits/case_package_v2_batch_converter_plan_v0/v2_batch_manifest_conversion_plan.csv`
- `audits/case_package_v2_batch_converter_plan_v0/v2_batch_schema_externalization_plan.csv`
- `audits/case_package_v2_batch_converter_plan_v0/v2_batch_evidence_runs_plan.csv`
- `audits/case_package_v2_batch_converter_plan_v0/v2_batch_validation_consolidation_plan.csv`
- `audits/case_package_v2_batch_converter_plan_v0/v2_batch_converter_stop_conditions.csv`
- `audits/case_package_v2_batch_converter_plan_v0/future_case_package_v2_batch_conversion_pilot_prompt.md`
- `audits/case_package_v2_batch_converter_plan_v0/case_package_v2_batch_converter_plan_summary.json`
- `audits/case_package_v2_batch_converter_plan_v0/case_package_v2_batch_converter_plan_command_log.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- Branch check: passed.
- Required output existence check: passed.
- CSV header checks: passed.
- Summary JSON parse and boundary assertions: passed.
- Protected-boundary checks: passed; no files under `cases/`, `schemas/`, `case_sets/`, inventory, reports, or results changed.
- `git diff --check`: passed.

Task result:
- Read-only dry-run: yes.
- Pilot cases: `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.
- Cases modified: no.
- Schemas modified: no.
- case_sets/inventory/reports/results changed: no.
- denominator/paper results changed: no.
- official metrics computed: no.
- DB/checker execution run: no.
- global leaderboard created: no.

Next safe action:
- Resolve manual-review blockers in `audits/case_package_v2_batch_converter_plan_v0/v2_batch_converter_stop_conditions.csv` before authorizing a writable `case_package_v2_batch_conversion_pilot_v0`.

### 2026-05-19 · 2364b12 · case_package_v2_rulebook_refinement_folder_order_v0

Branch: `feature/case-package-v2-external-schema`
Mode: branch-only v2 rulebook refinement and folder-ordered conversion planning; no case conversion; no schema modification; no DB/checker execution; no official metrics; no paper rendering
Legacy repo modified: no
Release repo modified: yes
Commit: `2364b12289886773317da1ff285d0f471696421e`
Push: succeeded; pushed branch `feature/case-package-v2-external-schema` to origin

Summary:
- Refined the v2 master plan and repository specs before writable conversion.
- Recorded that clean v2 retains case-local `schema/` only for `schema/schema_profile.yaml`, while executable DDL/load remain external under `schemas/<SCHEMA_ID>/<engine>/`.
- Added decision log entries for case-local schema profile-only policy and shared checker/validation modules.
- Recorded that case-local `checker/` stores configuration only and shared logic belongs under `src/sql_rewrite_bench/`.
- Recorded the folder-ordered conversion sequence: `manifest -> sql -> schema -> checker -> validation -> witness -> evidence -> metadata -> notes -> runs -> README/validator`.
- Created audit outputs for folder order, schema profile policy, shared module policy, validation call graph, future folder-ordered prompt, and summary JSON.
- Did not modify case files, schemas, `case_sets/`, inventory, reports/results, denominators, paper results, raw legacy evidence, DB/checker execution code, or leaderboard outputs.

Files created:
- `audits/case_package_v2_rulebook_refinement_folder_order_v0/v2_rulebook_refinement_summary.md`
- `audits/case_package_v2_rulebook_refinement_folder_order_v0/v2_folder_order_conversion_sequence.csv`
- `audits/case_package_v2_rulebook_refinement_folder_order_v0/v2_schema_profile_policy.csv`
- `audits/case_package_v2_rulebook_refinement_folder_order_v0/v2_shared_checker_validation_modules.csv`
- `audits/case_package_v2_rulebook_refinement_folder_order_v0/v2_validation_call_graph.md`
- `audits/case_package_v2_rulebook_refinement_folder_order_v0/future_case_package_v2_folder_ordered_conversion_prompt.md`
- `audits/case_package_v2_rulebook_refinement_folder_order_v0/v2_rulebook_refinement_summary.json`
- `audits/case_package_v2_rulebook_refinement_folder_order_v0/v2_rulebook_refinement_command_log.md`

Files modified:
- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/DECISION_LOG.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`
- `repository_spec/case_package_contract_v2_draft.md`
- `repository_spec/external_schema_contract_v1_draft.md`
- `repository_spec/validation_entrypoint_policy_v1_draft.md`
- `repository_spec/external_evidence_contract_v1_draft.md`

Validation:
- Branch check: passed.
- Master-plan schema profile-only policy check: passed.
- Repository spec shared-module checks: passed.
- CSV header and folder-order checks: passed.
- Summary JSON parse and boundary assertions: passed.
- Protected-boundary checks: passed; no files under `cases/`, `schemas/`, `case_sets/`, inventory, reports, or results changed.
- `git diff --check`: passed.

Task result:
- Schema profile-only policy recorded: yes.
- Shared checker/validation module plan recorded: yes.
- Folder-ordered conversion sequence recorded: yes.
- Case files modified: no.
- Schemas modified: no.
- case_sets/inventory/reports/results changed: no.
- denominator/paper results changed: no.
- official metrics computed: no.
- DB/checker execution run: no.
- global leaderboard created: no.

Next safe action:
- Authorize a branch-only folder-ordered writable pilot that starts with manifest and SQL layers, then adds `schema/schema_profile.yaml` plus external schema references before converting checker, validation, witness, evidence, metadata, notes, runs, README, or validator expectations.

### 2026-05-19 · a727de5 · case_package_v2_folder_ordered_conversion_pilot_v0

Branch: `feature/case-package-v2-external-schema`
Mode: branch-only writable v2 pilot conversion for first three layers only; manifest, sql, and schema; no checker conversion; no validation conversion; no witness/evidence/metadata/notes/runs cleanup; no DB/checker execution; no official metrics
Legacy repo modified: no
Release repo branch modified: yes
Commit: `a727de5f81dd5080cafd4fd081b2dfd3a42671f0`
Push: succeeded; pushed branch `feature/case-package-v2-external-schema` to origin

Summary:
- Converted exactly the first three v2 folder-order layers for `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.
- Normalized manifests to canonical direct SQL paths and profile-first `schema_ref` with only `schema_id` and `profile`.
- Created or verified direct SQL paths `sql/source.sql`, `sql/pos_01.sql`, and `sql/neg_01.sql`.
- Created or normalized case-local `schema/schema_profile.yaml` files as case-facing schema summaries.
- Reused `schemas/tpch_common_core_v0/` for `PERF_0006`.
- Created copy-first external schema packages for `tpch_perf0007_v0`, `calcite_core_sql_tests_cons0005_v0`, `parrot_bird_port0003_v0`, and `sqlstorm_stackoverflow_longtail0011_v0`.
- Preserved old nested SQL paths, case-local per-engine schema files, evidence, metadata, notes, validation scripts, checker files, witness files, and case-local runs.
- Did not modify `case_sets/`, inventory, reports/results, denominators, paper results, raw legacy evidence, DB/checker execution code, or leaderboard outputs.

Files created:
- Direct SQL aliases for `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.
- External schema packages under `schemas/tpch_perf0007_v0/`, `schemas/calcite_core_sql_tests_cons0005_v0/`, `schemas/parrot_bird_port0003_v0/`, and `schemas/sqlstorm_stackoverflow_longtail0011_v0/`.
- `audits/case_package_v2_folder_ordered_conversion_pilot_v0/folder_ordered_conversion_pilot_summary.md`
- `audits/case_package_v2_folder_ordered_conversion_pilot_v0/pilot_case_layer_conversion_status.csv`
- `audits/case_package_v2_folder_ordered_conversion_pilot_v0/pilot_manifest_conversion_results.csv`
- `audits/case_package_v2_folder_ordered_conversion_pilot_v0/pilot_sql_conversion_results.csv`
- `audits/case_package_v2_folder_ordered_conversion_pilot_v0/pilot_schema_conversion_results.csv`
- `audits/case_package_v2_folder_ordered_conversion_pilot_v0/pilot_manual_review_blockers.csv`
- `audits/case_package_v2_folder_ordered_conversion_pilot_v0/pilot_protected_boundary_checks.csv`
- `audits/case_package_v2_folder_ordered_conversion_pilot_v0/future_case_package_v2_checker_validation_layers_prompt.md`
- `audits/case_package_v2_folder_ordered_conversion_pilot_v0/folder_ordered_conversion_pilot_summary.json`
- `audits/case_package_v2_folder_ordered_conversion_pilot_v0/folder_ordered_conversion_pilot_command_log.md`

Files modified:
- `cases/PERF/PERF_0006/manifest.yaml`
- `cases/PERF/PERF_0006/schema/schema_profile.yaml`
- `cases/PERF/PERF_0007/manifest.yaml`
- `cases/PERF/PERF_0007/schema/schema_profile.yaml`
- `cases/CONS/CONS_0005/manifest.yaml`
- `cases/CONS/CONS_0005/schema/schema_profile.yaml`
- `cases/PORT/PORT_0003/manifest.yaml`
- `cases/PORT/PORT_0003/schema/schema_profile.yaml`
- `cases/LONGTAIL/LONGTAIL_0011/manifest.yaml`
- `cases/LONGTAIL/LONGTAIL_0011/schema/schema_profile.yaml`
- `schemas/tpch_common_core_v0/schema_profile.yaml`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- Manifest/SQL/schema sanity check: passed for all five cases.
- Protected later-layer directory check: passed; checker, validation, witness, evidence, metadata, notes, and runs directories were not modified.
- Protected repository surface check: passed; no files under `case_sets/`, inventory, reports, or results changed.
- Existing v2 validator: ran for all five cases and returned expected failures because it still requires `schema_ref.engines` and later validation wrappers are intentionally not converted.
- Existing case_package_v2 unit tests: ran; one existing `PERF_0006` read-only validator-status assertion failed because profile-first `schema_ref` is not yet supported by the validator/test expectation.
- Summary JSON parse and boundary assertions: passed.
- Protected path checks for `case_sets/`, inventory, reports, results, evidence, and case-local runs: passed.
- `git diff --check`: passed.

Task result:
- Writable conversion pilot: yes.
- Converted layers: manifest, sql, schema.
- Pilot cases: `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.
- Cases converted: all five.
- Cases deferred: none.
- Checker/validation/witness/evidence/metadata/notes untouched: yes.
- Runs deleted: no.
- case_sets/inventory/reports/results changed: no.
- denominator/paper results changed: no.
- official metrics computed: no.
- DB/checker execution run: no.
- global leaderboard created: no.

Next safe action:
- Authorize `case_package_v2_profile_first_validator_compatibility_v0` to update the static resolver/tests for profile-first `schema_ref` before checker/validation layer conversion.

### 2026-05-19 · dc07170 · case_package_v2_profile_first_validator_compatibility_v0

Branch: `feature/case-package-v2-external-schema`
Mode: branch-only validator/resolver compatibility task; no case conversion; no schema modification; no DB/checker execution; no official metrics
Legacy repo modified: no
Release repo branch modified: yes
Commit: `dc07170d9b2776aeff17ffebdce0b5239b181ca3`
Push: succeeded; pushed branch `feature/case-package-v2-external-schema` to origin

Summary:
- Updated the static v2 resolver to support profile-first `schema_ref` by loading `schema_ref.profile` and resolving engine DDL/load paths from external `schemas/<SCHEMA_ID>/schema_profile.yaml`.
- Preserved legacy `schema_ref.engines.<engine>.ddl/load` as compatibility input for existing validation context.
- Added case-local `schema/schema_profile.yaml` validation.
- Changed missing validation wrapper references to warning-only findings because checker/validation layers are intentionally not converted yet.
- Updated the dev validator output to record profile-first support.
- Updated v2 resolver tests for profile-first resolution, legacy compatibility, missing profile failures, missing external engine path failures, absolute path rejection, optional witness warnings, and all five pilot cases.
- Revalidated `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.
- Did not modify case files, schemas, `case_sets/`, inventory, reports/results, denominators, paper results, raw legacy evidence, DB/checker execution outputs, or leaderboard outputs.

Files created:
- `audits/case_package_v2_profile_first_validator_compatibility_v0/profile_first_validator_compatibility_summary.md`
- `audits/case_package_v2_profile_first_validator_compatibility_v0/profile_first_ref_validation_results.csv`
- `audits/case_package_v2_profile_first_validator_compatibility_v0/profile_first_validator_test_results.csv`
- `audits/case_package_v2_profile_first_validator_compatibility_v0/profile_first_compatibility_gaps.csv`
- `audits/case_package_v2_profile_first_validator_compatibility_v0/future_case_package_v2_checker_validation_layers_prompt.md`
- `audits/case_package_v2_profile_first_validator_compatibility_v0/profile_first_validator_compatibility_summary.json`
- `audits/case_package_v2_profile_first_validator_compatibility_v0/profile_first_validator_command_log.md`

Files modified:
- `src/sql_rewrite_bench/case_package_v2_resolver.py`
- `scripts/dev/validate_case_package_v2_refs.py`
- `tests/case_package_v2/test_case_package_v2_resolver.py`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- Unit tests passed: `PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`.
- Static validator passed for all five pilot cases.
- Summary JSON parse and boundary assertions passed.
- Protected path checks passed; no files under `cases/`, `schemas/`, `case_sets/`, inventory, reports, or results changed.
- `git diff --check`: passed.

Task result:
- Profile-first schema_ref supported: yes.
- Resolver updated: yes.
- Validator updated: yes.
- Tests updated: yes.
- Pilot cases revalidated: `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.
- Case files modified: no.
- Schemas modified: no.
- case_sets/inventory/reports/results changed: no.
- denominator/paper results changed: no.
- official metrics computed: no.
- DB/checker execution run: no.
- global leaderboard created: no.

Next safe action:
- Authorize `case_package_v2_checker_validation_layers_pilot_v0` to convert only checker and validation layers for the five pilot cases on the feature branch, without DB/checker execution or protected benchmark-surface changes.

### 2026-05-19 · b272c09 · case_package_v2_checker_validation_layers_pilot_v0

Branch: `feature/case-package-v2-external-schema`
Mode: branch-only writable v2 pilot conversion for checker and validation layers only; no witness/evidence/metadata/notes/runs cleanup; no DB/checker execution; no official metrics
Legacy repo modified: no
Release repo branch modified: yes
Commit: `b272c0928bfa68f51fd2e57ee2aa7088bc185738`
Push: succeeded; pushed branch `feature/case-package-v2-external-schema` to origin

Summary:
- Converted or verified the checker and validation layers for `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.
- Ensured each pilot case has canonical checker refs for `checker/checker.yaml`, `checker/normalization.yaml`, `checker/compare_config.yaml`, and `checker/expected_rejections.yaml`.
- Aligned stale checker SQL references to direct v2 paths where they remained, while preserving old nested SQL paths as explicit compatibility metadata.
- Added canonical manifest validation refs where missing.
- Added or normalized `validation/run_validation.sh` and `validation/run_plan_collection.sh` as thin fail-closed wrappers.
- Retained all old engine-specific validation and plan-collection scripts as compatibility assets.
- Added no per-case Python checker implementations.
- Did not modify witness, evidence, metadata, notes, runs, sql, schema, `schemas/`, `case_sets/`, inventory, reports/results, denominators, paper results, raw legacy evidence, DB/checker execution outputs, or leaderboard outputs.

Files created:
- `cases/PERF/PERF_0007/validation/run_validation.sh`
- `cases/PERF/PERF_0007/validation/run_plan_collection.sh`
- `cases/CONS/CONS_0005/validation/run_validation.sh`
- `cases/CONS/CONS_0005/validation/run_plan_collection.sh`
- `cases/PORT/PORT_0003/validation/run_validation.sh`
- `cases/PORT/PORT_0003/validation/run_plan_collection.sh`
- `cases/LONGTAIL/LONGTAIL_0011/validation/run_validation.sh`
- `cases/LONGTAIL/LONGTAIL_0011/validation/run_plan_collection.sh`
- `audits/case_package_v2_checker_validation_layers_pilot_v0/checker_validation_layers_pilot_summary.md`
- `audits/case_package_v2_checker_validation_layers_pilot_v0/checker_layer_conversion_results.csv`
- `audits/case_package_v2_checker_validation_layers_pilot_v0/validation_layer_conversion_results.csv`
- `audits/case_package_v2_checker_validation_layers_pilot_v0/checker_validation_manual_review_blockers.csv`
- `audits/case_package_v2_checker_validation_layers_pilot_v0/checker_validation_protected_boundary_checks.csv`
- `audits/case_package_v2_checker_validation_layers_pilot_v0/future_case_package_v2_witness_evidence_layers_prompt.md`
- `audits/case_package_v2_checker_validation_layers_pilot_v0/checker_validation_layers_pilot_summary.json`
- `audits/case_package_v2_checker_validation_layers_pilot_v0/checker_validation_layers_pilot_command_log.md`

Files modified:
- `cases/PERF/PERF_0006/validation/run_validation.sh`
- `cases/PERF/PERF_0006/validation/run_plan_collection.sh`
- `cases/PERF/PERF_0007/manifest.yaml`
- `cases/PERF/PERF_0007/checker/checker.yaml`
- `cases/PERF/PERF_0007/checker/expected_rejections.yaml`
- `cases/CONS/CONS_0005/manifest.yaml`
- `cases/CONS/CONS_0005/checker/expected_rejections.yaml`
- `cases/PORT/PORT_0003/manifest.yaml`
- `cases/PORT/PORT_0003/checker/checker.yaml`
- `cases/PORT/PORT_0003/checker/compare_config.yaml`
- `cases/PORT/PORT_0003/checker/expected_rejections.yaml`
- `cases/LONGTAIL/LONGTAIL_0011/manifest.yaml`
- `cases/LONGTAIL/LONGTAIL_0011/checker/checker.yaml`
- `cases/LONGTAIL/LONGTAIL_0011/checker/expected_rejections.yaml`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- Static validator passed for all five pilot cases.
- Unit tests passed: `PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`.
- Summary JSON parse and boundary assertions passed.
- Protected path checks passed; no `case_sets/`, inventory, reports/results, denominator, paper-result, evidence deletion, case-local runs deletion, DB/checker output, or leaderboard change was detected.
- `git diff --check`: passed.

Task result:
- Writable conversion pilot: yes.
- Converted layers: checker, validation.
- Pilot cases: `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.
- Cases converted: all five.
- Cases deferred: none.
- Witness/evidence/metadata/notes/runs untouched: yes.
- Runs deleted: no.
- Per-case Python checker scripts added: no.
- case_sets/inventory/reports/results changed: no.
- denominator/paper results changed: no.
- official metrics computed: no.
- DB/checker execution run: no.
- global leaderboard created: no.

Next safe action:
- Authorize `case_package_v2_witness_evidence_layers_pilot_v0` to convert only witness and evidence references for the five pilot cases on the feature branch, without DB/checker execution, evidence deletion, case-local runs deletion, or protected benchmark-surface changes.

### 2026-05-19 · 3f60021 · case_package_v2_witness_evidence_layers_pilot_v0

Branch: `feature/case-package-v2-external-schema`
Mode: branch-only writable v2 pilot conversion for witness and evidence-reference layers only; no metadata conversion; no notes conversion; no runs cleanup; no DB/checker execution; no official metrics
Legacy repo modified: no
Release repo branch modified: yes
Commit: `3f60021d9fa9f4895486e5c70f0bbd60e12a20e0`
Push: succeeded after one transient SSH retry; pushed branch `feature/case-package-v2-external-schema` to origin

Summary:
- Converted the witness and evidence-reference layers for `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.
- Added canonical source-as-oracle witness policy fields to all five manifests.
- Added lightweight `witness/witness_profile.yaml` files for all five pilot cases.
- Added or normalized `evidence_ref` to point to top-level `evidence/cases/<POOL>/<CASE_ID>/` packets.
- Copy-first externalized public-safe case-local evidence into top-level `evidence/cases/`.
- Preserved case-local `evidence/` and case-local `runs/`; no deletion was performed.
- Did not modify metadata, notes, runs cleanup surfaces, SQL, schema, schemas, checker, validation, `case_sets/`, inventory, reports/results, denominators, paper results, raw legacy evidence, DB/checker execution outputs, or leaderboard outputs.

Files created:
- `cases/PERF/PERF_0006/witness/witness_profile.yaml`
- `cases/PERF/PERF_0007/witness/witness_profile.yaml`
- `cases/CONS/CONS_0005/witness/witness_profile.yaml`
- `cases/PORT/PORT_0003/witness/witness_profile.yaml`
- `cases/LONGTAIL/LONGTAIL_0011/witness/witness_profile.yaml`
- Top-level evidence packets under `evidence/cases/PERF/PERF_0006/`, `evidence/cases/PERF/PERF_0007/`, `evidence/cases/CONS/CONS_0005/`, `evidence/cases/PORT/PORT_0003/`, and `evidence/cases/LONGTAIL/LONGTAIL_0011/`.
- `audits/case_package_v2_witness_evidence_layers_pilot_v0/witness_evidence_layers_pilot_summary.md`
- `audits/case_package_v2_witness_evidence_layers_pilot_v0/witness_layer_conversion_results.csv`
- `audits/case_package_v2_witness_evidence_layers_pilot_v0/evidence_layer_conversion_results.csv`
- `audits/case_package_v2_witness_evidence_layers_pilot_v0/evidence_artifact_copy_manifest.csv`
- `audits/case_package_v2_witness_evidence_layers_pilot_v0/witness_evidence_manual_review_blockers.csv`
- `audits/case_package_v2_witness_evidence_layers_pilot_v0/witness_evidence_protected_boundary_checks.csv`
- `audits/case_package_v2_witness_evidence_layers_pilot_v0/future_case_package_v2_metadata_notes_runs_layers_prompt.md`
- `audits/case_package_v2_witness_evidence_layers_pilot_v0/witness_evidence_layers_pilot_summary.json`
- `audits/case_package_v2_witness_evidence_layers_pilot_v0/witness_evidence_layers_pilot_command_log.md`

Files modified:
- `cases/PERF/PERF_0006/manifest.yaml`
- `cases/PERF/PERF_0007/manifest.yaml`
- `cases/CONS/CONS_0005/manifest.yaml`
- `cases/PORT/PORT_0003/manifest.yaml`
- `cases/LONGTAIL/LONGTAIL_0011/manifest.yaml`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- Static v2 validator passed for all five pilot cases.
- Unit tests passed: `PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`.
- Summary JSON parse and boundary assertions passed.
- Protected path checks passed; no `case_sets/`, inventory, reports/results, denominator, paper-result, case-local evidence deletion, case-local runs deletion, DB/checker output, or leaderboard change was detected.
- Unsafe evidence scan passed; only curated public-safe evidence was copied.
- `git diff --check`: passed.

Task result:
- Writable conversion pilot: yes.
- Converted layers: witness, evidence.
- Pilot cases: `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.
- Cases converted: all five.
- Cases deferred: none.
- Witness modified: yes.
- Evidence_ref modified: yes.
- External evidence created: yes.
- Metadata/notes/runs untouched: yes.
- Case-local evidence/runs deleted: no.
- case_sets/inventory/reports/results changed: no.
- denominator/paper results changed: no.
- official metrics computed: no.
- DB/checker execution run: no.
- global leaderboard created: no.

Next safe action:
- Authorize `case_package_v2_metadata_notes_runs_layers_pilot_v0` to handle only metadata, notes, and runs cleanup for the same five pilot cases on the feature branch, without DB/checker execution, retained-evidence deletion without mapping, protected benchmark-surface changes, official metrics, or leaderboard output.

### 2026-05-19 · c3deaa9 · case_package_v2_metadata_notes_runs_layers_pilot_v0

Branch: `feature/case-package-v2-external-schema`
Mode: branch-only writable v2 pilot conversion for metadata, notes, and runs classification only; no README/validator closeout; no DB/checker execution; no official metrics
Legacy repo modified: no
Release repo branch modified: yes
Commit: `c3deaa9e1061a68b8c01969d28a965635044032c`
Push: succeeded; pushed branch `feature/case-package-v2-external-schema` to origin

Summary:
- Classified metadata, notes, and runs layers for `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.
- Added `compatibility.metadata_legacy`, `compatibility.notes_legacy`, and `compatibility.runs_legacy` mappings to the five manifests.
- Copy-first copied public-safe case-local notes into `evidence/cases/<POOL>/<CASE_ID>/notes/`.
- Classified all five case-local `runs/` directories as `placeholder_only` with one tracked `runs/README.md`.
- Deleted no metadata files, no case-local notes, no case-local evidence, and no runs files.
- Did not modify README files, validator code, SQL, schema, schemas, checker, validation, witness, `case_sets/`, inventory, reports/results, denominators, paper results, raw legacy evidence, DB/checker execution outputs, or leaderboard outputs.

Files created:
- Public-safe note copies under `evidence/cases/PERF/PERF_0006/notes/`, `evidence/cases/PERF/PERF_0007/notes/`, `evidence/cases/CONS/CONS_0005/notes/`, `evidence/cases/PORT/PORT_0003/notes/`, and `evidence/cases/LONGTAIL/LONGTAIL_0011/notes/`.
- `audits/case_package_v2_metadata_notes_runs_layers_pilot_v0/metadata_notes_runs_layers_pilot_summary.md`
- `audits/case_package_v2_metadata_notes_runs_layers_pilot_v0/metadata_layer_conversion_results.csv`
- `audits/case_package_v2_metadata_notes_runs_layers_pilot_v0/notes_layer_conversion_results.csv`
- `audits/case_package_v2_metadata_notes_runs_layers_pilot_v0/runs_layer_classification_results.csv`
- `audits/case_package_v2_metadata_notes_runs_layers_pilot_v0/metadata_notes_runs_manual_review_blockers.csv`
- `audits/case_package_v2_metadata_notes_runs_layers_pilot_v0/metadata_notes_runs_protected_boundary_checks.csv`
- `audits/case_package_v2_metadata_notes_runs_layers_pilot_v0/future_case_package_v2_readme_validator_closeout_prompt.md`
- `audits/case_package_v2_metadata_notes_runs_layers_pilot_v0/metadata_notes_runs_layers_pilot_summary.json`
- `audits/case_package_v2_metadata_notes_runs_layers_pilot_v0/metadata_notes_runs_layers_pilot_command_log.md`

Files modified:
- `cases/PERF/PERF_0006/manifest.yaml`
- `cases/PERF/PERF_0007/manifest.yaml`
- `cases/CONS/CONS_0005/manifest.yaml`
- `cases/PORT/PORT_0003/manifest.yaml`
- `cases/LONGTAIL/LONGTAIL_0011/manifest.yaml`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- Static v2 validator passed for all five pilot cases.
- Unit tests passed: `PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`.
- Summary JSON parse and boundary assertions passed.
- Protected path checks passed; no `case_sets/`, inventory, reports/results, denominator, paper-result, case-local evidence deletion, non-empty runs deletion, DB/checker output, README/validator conversion, or leaderboard change was detected.
- `git diff --check`: passed.

Task result:
- Writable conversion pilot: yes.
- Converted layers: metadata, notes, runs.
- Pilot cases: `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.
- Cases converted: all five.
- Cases deferred: none.
- Metadata modified: yes.
- Notes modified: yes.
- Runs classified: yes.
- Runs deleted: no.
- Non-empty runs deleted: no.
- Case-local evidence deleted: no.
- README/validator modified: no.
- case_sets/inventory/reports/results changed: no.
- denominator/paper results changed: no.
- official metrics computed: no.
- DB/checker execution run: no.
- global leaderboard created: no.

Next safe action:
- Authorize `case_package_v2_readme_validator_closeout_pilot_v0` to update README wording and validator expectations only for the same five pilot cases on the feature branch, without DB/checker execution, retained-evidence deletion, non-empty runs deletion, protected benchmark-surface changes, official metrics, or leaderboard output.

### 2026-05-19 · 2ddc824 · case_package_v2_readme_validator_closeout_pilot_v0

Branch: `feature/case-package-v2-external-schema`
Mode: branch-only README/validator closeout for five v2 pilot cases; no structural conversion; no DB/checker execution; no official metrics
Legacy repo modified: no
Release repo branch modified: yes
Commit: `2ddc8242dc531763160999e5cbfdbcd6c4231277`
Push: succeeded; pushed branch `feature/case-package-v2-external-schema` to origin

Summary:
- Updated README wording for `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011` to document the finalized v2 pilot structure and compatibility boundaries.
- Rechecked the static v2 validator for all five pilot cases without changing validator code or tests.
- Confirmed direct SQL paths, profile-first schema refs, case-local `schema/schema_profile.yaml`, checker config refs, validation wrappers, witness policy, evidence refs, and case-local runs boundaries pass static validation.
- Did not modify SQL, schema, external schemas, checker config, validation wrappers, witness files, evidence files, metadata files, notes files, case-local runs, `case_sets/`, inventory, reports/results, denominators, paper results, raw legacy evidence, DB/checker execution outputs, or leaderboard outputs.

Files created:
- `audits/case_package_v2_readme_validator_closeout_pilot_v0/readme_validator_closeout_summary.md`
- `audits/case_package_v2_readme_validator_closeout_pilot_v0/readme_closeout_results.csv`
- `audits/case_package_v2_readme_validator_closeout_pilot_v0/validator_closeout_results.csv`
- `audits/case_package_v2_readme_validator_closeout_pilot_v0/pilot_case_clean_v2_gap_matrix.csv`
- `audits/case_package_v2_readme_validator_closeout_pilot_v0/readme_validator_protected_boundary_checks.csv`
- `audits/case_package_v2_readme_validator_closeout_pilot_v0/future_case_package_v2_pilot_closeout_or_common_core40_plan_prompt.md`
- `audits/case_package_v2_readme_validator_closeout_pilot_v0/readme_validator_closeout_summary.json`
- `audits/case_package_v2_readme_validator_closeout_pilot_v0/readme_validator_closeout_command_log.md`

Files modified:
- `cases/PERF/PERF_0006/README.md`
- `cases/PERF/PERF_0007/README.md`
- `cases/CONS/CONS_0005/README.md`
- `cases/PORT/PORT_0003/README.md`
- `cases/LONGTAIL/LONGTAIL_0011/README.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- Static v2 validator passed for all five pilot cases.
- Unit tests passed: `PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`.
- Summary JSON parse and boundary assertions passed.
- Protected path checks passed; no `case_sets/`, inventory, reports/results, denominator, paper-result, case-local evidence deletion, case-local runs deletion, DB/checker output, structural layer reconversion, or leaderboard change was detected.
- `git diff --check`: passed.

Task result:
- README/validator closeout: yes.
- Pilot cases: `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.
- Readmes updated: yes.
- Validator rechecked: yes.
- Validator code changed: no.
- Tests changed: no.
- Structural layers modified: no.
- case_sets/inventory/reports/results changed: no.
- denominator/paper results changed: no.
- official metrics computed: no.
- DB/checker execution run: no.
- global leaderboard created: no.

Next safe action:
- Review and accept the five-case v2 pilot closeout on `feature/case-package-v2-external-schema`; if accepted, authorize a branch-only Common-core 40 conversion plan using the folder-ordered rulebook, without merging to `main`, protected benchmark-surface changes, DB/checker execution, official metrics, paper rendering, or leaderboard output.

### 2026-05-19 · 15afa8c · case_package_v2_template_parity_gap_review_v0

Branch: `feature/case-package-v2-external-schema`
Mode: branch-only read-only template parity and clean-v2 gap review; no case conversion; no cleanup; no DB/checker execution; no official metrics
Legacy repo modified: no
Release repo branch modified: yes
Commit: `15afa8c2ea69b9dd70f7dc8b8b09df2ae5a1eb48`
Push: succeeded; pushed branch `feature/case-package-v2-external-schema` to origin

Summary:
- Compared `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011` against the clean v2 case-local template.
- Confirmed every clean-template-required asset is present for all five pilot cases.
- Classified optional witness assets, externalized schema/evidence assets, temporary v1 compatibility directories, retained evidence, placeholder runs, cleanup readiness, and manual-review blockers.
- Confirmed all five pilot cases still pass the static v2 validator.
- Did not modify case packages, schemas, evidence, runs, `case_sets/`, inventory, reports/results, denominators, paper results, raw legacy evidence, DB/checker execution outputs, or leaderboard outputs.

Files created:
- `audits/case_package_v2_template_parity_gap_review_v0/template_parity_gap_review_summary.md`
- `audits/case_package_v2_template_parity_gap_review_v0/template_parity_case_summary.csv`
- `audits/case_package_v2_template_parity_gap_review_v0/template_parity_path_gap_matrix.csv`
- `audits/case_package_v2_template_parity_gap_review_v0/template_parity_witness_gap_matrix.csv`
- `audits/case_package_v2_template_parity_gap_review_v0/template_parity_evidence_runs_gap_matrix.csv`
- `audits/case_package_v2_template_parity_gap_review_v0/template_parity_cleanup_readiness.csv`
- `audits/case_package_v2_template_parity_gap_review_v0/future_case_package_v2_clean_template_cleanup_pilot_prompt.md`
- `audits/case_package_v2_template_parity_gap_review_v0/template_parity_gap_review_summary.json`
- `audits/case_package_v2_template_parity_gap_review_v0/template_parity_gap_review_command_log.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- Static v2 validator passed for all five pilot cases.
- Summary JSON parse and boundary assertions passed.
- CSV header checks passed.
- Protected path checks passed; no cases, schemas, evidence, runs, `case_sets/`, inventory, reports/results, denominator, paper-result, DB/checker output, or leaderboard changes were detected.
- `git diff --check`: passed.

Task result:
- Template parity gap review: yes.
- Pilot cases: `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.
- Cases modified: no.
- Schemas modified: no.
- Evidence modified: no.
- Runs deleted: no.
- case_sets/inventory/reports/results changed: no.
- denominator/paper results changed: no.
- official metrics computed: no.
- DB/checker execution run: no.
- global leaderboard created: no.

Next safe action:
- Authorize `case_package_v2_clean_template_cleanup_pilot_v0` only for cleanup actions marked `ready_for_cleanup=true`, with explicit path staging, no retained-evidence deletion without mapping, and no protected benchmark-surface changes.

### 2026-05-19 · aa78272 · case_package_v2_clean_template_cleanup_pilot_v0

Branch: `feature/case-package-v2-external-schema`
Mode: branch-only clean-template cleanup pilot for five v2 pilot cases; cleanup limited to `ready_for_cleanup=true` candidates; no retained-evidence deletion; no DB/checker execution; no official metrics
Legacy repo modified: no
Release repo branch modified: yes
Commit: `aa7827279a321bc826b72abe12aa808f58b34356`
Push: succeeded; pushed branch `feature/case-package-v2-external-schema` to origin

Summary:
- Reviewed cleanup candidates marked `ready_for_cleanup=true` in `audits/case_package_v2_template_parity_gap_review_v0/template_parity_cleanup_readiness.csv`.
- Considered only nested SQL compatibility directories, copied case-local notes, and placeholder-only case-local `runs/` for `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.
- Removed no files because live manifest, README, checker, metadata, validation-script, or dev-script references still point at those compatibility paths.
- Skipped 15 cleanup candidates and recorded required future compatibility-reference cleanup actions.
- Did not delete retained evidence, case-local evidence, schema engine files, metadata, data fixtures, validation engine-specific scripts, non-empty runs, `case_sets/`, inventory, reports/results, denominators, paper results, DB/checker outputs, or leaderboard outputs.

Files created:
- `audits/case_package_v2_clean_template_cleanup_pilot_v0/clean_template_cleanup_pilot_summary.md`
- `audits/case_package_v2_clean_template_cleanup_pilot_v0/cleanup_candidate_manifest.csv`
- `audits/case_package_v2_clean_template_cleanup_pilot_v0/files_removed_manifest.csv`
- `audits/case_package_v2_clean_template_cleanup_pilot_v0/cleanup_skipped_manifest.csv`
- `audits/case_package_v2_clean_template_cleanup_pilot_v0/cleanup_validation_results.csv`
- `audits/case_package_v2_clean_template_cleanup_pilot_v0/post_cleanup_v2_validator_results.csv`
- `audits/case_package_v2_clean_template_cleanup_pilot_v0/future_case_package_v2_pilot_acceptance_or_common_core40_plan_prompt.md`
- `audits/case_package_v2_clean_template_cleanup_pilot_v0/clean_template_cleanup_pilot_summary.json`
- `audits/case_package_v2_clean_template_cleanup_pilot_v0/clean_template_cleanup_command_log.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- Static v2 validator passed for all five pilot cases.
- Unit tests passed: `PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`.
- Summary JSON parse and boundary assertions passed.
- Protected path checks passed; no cases, schemas, evidence, runs, `case_sets/`, inventory, reports/results, denominator, paper-result, DB/checker output, retained-evidence deletion, or leaderboard changes were detected.
- `git diff --check`: passed.

Task result:
- Clean-template cleanup pilot: yes.
- Cleanup limited to `ready_for_cleanup=true`: yes.
- Pilot cases: `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.
- Files removed: none.
- Files skipped: 15 cleanup candidates.
- Retained evidence deleted: no.
- Case-local evidence deleted without mapping: no.
- Schema engine files deleted: no.
- Metadata deleted: no.
- Data fixtures deleted: no.
- Validation engine-specific scripts deleted: no.
- case_sets/inventory/reports/results changed: no.
- denominator/paper results changed: no.
- official metrics computed: no.
- DB/checker execution run: no.
- global leaderboard created: no.

Next safe action:
- Authorize a narrow compatibility-reference cleanup planning task before deleting the ready template paths, or authorize a cleanup task that can update manifest/README/checker/metadata/validation references before removing now-unreferenced compatibility paths.

### 2026-05-19 · dbc5ace · case_package_v2_reference_cleanup_plan_v0

Branch: `feature/case-package-v2-external-schema`
Mode: branch-only compatibility-reference cleanup planning; no deletion; no case conversion; no DB/checker execution; no official metrics
Legacy repo modified: no
Release repo branch modified: yes
Commit: `dbc5ace1dcbe53656a988a045514fdbd72bb6167`
Push: succeeded; pushed branch `feature/case-package-v2-external-schema` to origin

Summary:
- Reviewed the 15 skipped cleanup candidates from `case_package_v2_clean_template_cleanup_pilot_v0`.
- Built a reference matrix for nested SQL compatibility dirs, copied case-local notes, and placeholder-only `runs/` across `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.
- Classified 50 live reference blockers and 30 historical/documentation exclusions.
- Classified 10 candidates as deletion-ready after reference update and 5 placeholder-runs candidates as deletion-ready only after retained-runs mapping/approval handling.
- Did not modify cases, schemas, evidence, runs, `case_sets/`, inventory, reports/results, denominators, paper results, DB/checker outputs, metrics, or leaderboard outputs.

Files created:
- `audits/case_package_v2_reference_cleanup_plan_v0/reference_cleanup_plan_summary.md`
- `audits/case_package_v2_reference_cleanup_plan_v0/skipped_cleanup_candidate_reference_matrix.csv`
- `audits/case_package_v2_reference_cleanup_plan_v0/cleanup_unblock_plan.csv`
- `audits/case_package_v2_reference_cleanup_plan_v0/historical_reference_exclusions.csv`
- `audits/case_package_v2_reference_cleanup_plan_v0/deletion_readiness_after_reference_cleanup.csv`
- `audits/case_package_v2_reference_cleanup_plan_v0/future_case_package_v2_reference_cleanup_execution_prompt.md`
- `audits/case_package_v2_reference_cleanup_plan_v0/reference_cleanup_plan_summary.json`
- `audits/case_package_v2_reference_cleanup_plan_v0/reference_cleanup_plan_command_log.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- Static v2 validator passed for all five pilot cases.
- Summary JSON parse and boundary assertions passed.
- CSV headers parsed successfully.
- Protected path checks passed; no cases, schemas, evidence, runs, `case_sets/`, inventory, reports/results, denominator, paper-result, DB/checker output, or leaderboard changes were detected.
- `git diff --check`: passed.

Task result:
- Reference cleanup plan: yes.
- Skipped candidates reviewed: 15.
- Live reference blockers found: 50.
- Historical references excluded: 30.
- Deletion-ready after reference update count: 10.
- Deletion-ready after retention mapping count: 5.
- Manual-review remaining count: 0 for the skipped ready candidates.
- Cases modified: no.
- Schemas modified: no.
- Evidence modified: no.
- Runs deleted: no.
- case_sets/inventory/reports/results changed: no.
- denominator/paper results changed: no.
- official metrics computed: no.
- DB/checker execution run: no.
- global leaderboard created: no.

Next safe action:
- Authorize `case_package_v2_reference_cleanup_execution_v0` to update live compatibility references and delete only candidates classified as `deletion_ready_after_reference_update`, while keeping retained evidence and protected benchmark surfaces out of scope.

### 2026-05-19 · 9c546eb · case_package_v2_reference_cleanup_execution_v0

Branch: `feature/case-package-v2-external-schema`
Mode: branch-only writable compatibility-reference cleanup execution; deletes only candidates classified as `deletion_ready_after_reference_update`; no retained-evidence deletion; no runs cleanup; no schema cleanup; no metadata source-of-truth cleanup; no validation engine-specific script deletion; no DB/checker execution; no official metrics
Legacy repo modified: no
Release repo branch modified: yes
Commit: `9c546ebdb127361731cebfa9a0afa0d3afd2b874`
Push: succeeded; pushed branch `feature/case-package-v2-external-schema` to origin

Summary:
- Selected exactly 10 cleanup candidates from the reference cleanup plan: nested SQL compatibility directories and copied case-local notes for `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.
- Updated 62 live manifest, README, checker, metadata, and validation-script references away from deleted compatibility paths.
- Deleted only the selected nested SQL compatibility directories and copied case-local notes candidates.
- Skipped 5 placeholder-only case-local `runs/` candidates because they require later mapping/approval handling and are out of scope for this execution task.
- Did not delete retained evidence, case-local evidence, case-local runs, schema engine files, metadata files, data fixtures, validation engine-specific scripts, `case_sets/`, inventory, reports/results, denominator inputs, paper-result inputs, DB/checker outputs, or leaderboard outputs.

Files created:
- `audits/case_package_v2_reference_cleanup_execution_v0/reference_cleanup_execution_summary.md`
- `audits/case_package_v2_reference_cleanup_execution_v0/reference_updates_applied.csv`
- `audits/case_package_v2_reference_cleanup_execution_v0/cleanup_deletions_executed.csv`
- `audits/case_package_v2_reference_cleanup_execution_v0/cleanup_execution_skipped.csv`
- `audits/case_package_v2_reference_cleanup_execution_v0/post_reference_cleanup_validator_results.csv`
- `audits/case_package_v2_reference_cleanup_execution_v0/reference_cleanup_execution_protected_boundary_checks.csv`
- `audits/case_package_v2_reference_cleanup_execution_v0/future_case_package_v2_post_cleanup_parity_review_prompt.md`
- `audits/case_package_v2_reference_cleanup_execution_v0/reference_cleanup_execution_summary.json`
- `audits/case_package_v2_reference_cleanup_execution_v0/reference_cleanup_execution_command_log.md`

Files modified:
- Five pilot case `manifest.yaml` files.
- Five pilot case `README.md` files.
- Selected checker config files for `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.
- Selected metadata artifact-path files for `PERF_0006`, `PERF_0007`, `CONS_0005`, and `PORT_0003`.
- Selected validation compatibility scripts for `PERF_0006`, `PERF_0007`, `CONS_0005`, and `LONGTAIL_0011`.
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Files deleted:
- Selected `sql/positives/` and `sql/negatives/` compatibility files for all five pilot cases.
- Selected copied case-local `notes/` files for all five pilot cases.

Validation:
- Static v2 validator passed for all five pilot cases.
- Unit tests passed: `PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`.
- Summary JSON parse and boundary assertions passed.
- Protected path checks passed; no retained evidence, runs, evidence, schema engine files, metadata files, data fixtures, validation engine-specific scripts, `case_sets/`, inventory, reports/results, denominator, paper-result, DB/checker output, or leaderboard deletion/change was detected.
- `git diff --check`: passed.

Task result:
- Reference cleanup execution: yes.
- Pilot cases: `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.
- Selected candidates count: 10.
- References updated count: 62.
- Deleted candidates count: 10.
- Skipped candidates count: 5.
- Retained evidence deleted: no.
- Runs deleted: no.
- Evidence deleted: no.
- Schema engine files deleted: no.
- Metadata deleted: no.
- Data deleted: no.
- Validation engine-specific scripts deleted: no.
- case_sets/inventory/reports/results changed: no.
- denominator/paper results changed: no.
- official metrics computed: no.
- DB/checker execution run: no.
- global leaderboard created: no.

Next safe action:
- Authorize `case_package_v2_post_cleanup_parity_review_v0` to re-run a read-only parity/gap review after the first safe compatibility-reference cleanup.

### 2026-05-19 · 2f4a9e7 · case_package_v2_post_cleanup_parity_review_v0

Branch: `feature/case-package-v2-external-schema`
Mode: branch-only read-only post-cleanup parity review; no cleanup execution; no case conversion; no DB/checker execution; no official metrics
Legacy repo modified: no
Release repo branch modified: yes
Commit: `2f4a9e7fac59d3b3cd1d490a08d14d4631832a02`
Push: succeeded; pushed branch `feature/case-package-v2-external-schema` to origin

Summary:
- Re-ran clean-template parity review after `case_package_v2_reference_cleanup_execution_v0`.
- Confirmed the previous cleanup removed tracked nested SQL compatibility paths and tracked copied case-local notes for all five pilot cases.
- Confirmed all five pilot cases still have every clean-template-required v2 asset and pass the static v2 validator.
- Classified 66 remaining tracked extra path groups and 10 retention blockers.
- Classified the five-case pilot as acceptable for functional v2 planning but not clean-template-minimal.
- Recommended a read-only Common-core 40 conversion plan as the next safe action.
- Did not modify case packages, schemas, evidence, runs, `case_sets/`, inventory, reports/results, denominators, paper results, DB/checker outputs, official metrics, or leaderboard outputs.

Files created:
- `audits/case_package_v2_post_cleanup_parity_review_v0/post_cleanup_parity_review_summary.md`
- `audits/case_package_v2_post_cleanup_parity_review_v0/post_cleanup_template_parity_case_summary.csv`
- `audits/case_package_v2_post_cleanup_parity_review_v0/post_cleanup_path_gap_matrix.csv`
- `audits/case_package_v2_post_cleanup_parity_review_v0/post_cleanup_evidence_runs_gap_matrix.csv`
- `audits/case_package_v2_post_cleanup_parity_review_v0/post_cleanup_remaining_action_plan.csv`
- `audits/case_package_v2_post_cleanup_parity_review_v0/future_case_package_v2_common_core40_plan_prompt.md`
- `audits/case_package_v2_post_cleanup_parity_review_v0/post_cleanup_parity_review_summary.json`
- `audits/case_package_v2_post_cleanup_parity_review_v0/post_cleanup_parity_review_command_log.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- Static v2 validator passed for all five pilot cases.
- Summary JSON parse and boundary assertions passed.
- CSV header and row checks passed.
- Protected path checks passed; no cases, schemas, evidence, runs, `case_sets/`, inventory, reports/results, denominator, paper-result, DB/checker output, or leaderboard changes were detected.
- `git diff --check`: passed.

Task result:
- Post-cleanup parity review: yes.
- Pilot cases: `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.
- Cases modified: no.
- Schemas modified: no.
- Evidence modified: no.
- Runs deleted: no.
- Remaining extra path groups: 66.
- Remaining retention blockers: 10.
- Functional v2 acceptance status: accepted with retained compatibility gaps.
- Clean-template parity status: not clean-template-minimal.
- Ready for Common-core 40 plan: yes, planning only.
- case_sets/inventory/reports/results changed: no.
- denominator/paper results changed: no.
- official metrics computed: no.
- DB/checker execution run: no.
- global leaderboard created: no.

Next safe action:
- Authorize `case_package_v2_common_core40_conversion_plan_v0` as a read-only planning task using the five-case pilot as a functional v2 template.

### 2026-05-19 · a053cf5 · case_package_v2_clean_template_gap_closure_execution_v0

Branch: `feature/case-package-v2-external-schema`
Mode: branch-only writable clean-template gap closure for five v2 pilot cases; no Common-core 40 conversion; no DB/checker execution; no official metrics
Legacy repo modified: no
Release repo branch modified: yes
Commit: `a053cf5a2129879fd58cf9bf738edb3c773f92cb`
Push: succeeded to `origin/feature/case-package-v2-external-schema` (`e8d3a61..a053cf5`)

Summary:
- Closed safe clean-template gaps for `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.
- Started from 61 remaining extra path groups from the post-empty-runs parity review.
- Deleted 10 safe case-local compatibility path groups: `metadata/` and `data/` for each of the five pilot cases.
- Skipped 51 path groups: schema engine compatibility directories, case-local evidence, old engine-specific validation scripts, and `PORT_0003` dialect variants.
- Verified external schema copies and external evidence copies before deciding which directories could be deleted or must be blocked.
- Updated manifests and READMEs to remove stale metadata/data/runs compatibility references and document remaining blockers.
- Did not delete retained evidence or unsafe evidence.
- Did not modify `case_sets/`, inventory, reports/results, denominator inputs, paper-result inputs, DB/checker outputs, official metrics, or leaderboard outputs.

Files created:
- `audits/case_package_v2_clean_template_gap_closure_execution_v0/clean_template_gap_closure_summary.md`
- `audits/case_package_v2_clean_template_gap_closure_execution_v0/gap_closure_candidate_matrix.csv`
- `audits/case_package_v2_clean_template_gap_closure_execution_v0/gap_closure_deletions_manifest.csv`
- `audits/case_package_v2_clean_template_gap_closure_execution_v0/gap_closure_skipped_manifest.csv`
- `audits/case_package_v2_clean_template_gap_closure_execution_v0/post_gap_closure_parity_case_summary.csv`
- `audits/case_package_v2_clean_template_gap_closure_execution_v0/post_gap_closure_path_gap_matrix.csv`
- `audits/case_package_v2_clean_template_gap_closure_execution_v0/gap_closure_validator_results.csv`
- `audits/case_package_v2_clean_template_gap_closure_execution_v0/gap_closure_protected_boundary_checks.csv`
- `audits/case_package_v2_clean_template_gap_closure_execution_v0/future_case_package_v2_common_core40_plan_or_second_cleanup_prompt.md`
- `audits/case_package_v2_clean_template_gap_closure_execution_v0/clean_template_gap_closure_summary.json`
- `audits/case_package_v2_clean_template_gap_closure_execution_v0/clean_template_gap_closure_command_log.md`

Files modified:
- `cases/PERF/PERF_0006/README.md`
- `cases/PERF/PERF_0006/manifest.yaml`
- `cases/PERF/PERF_0007/README.md`
- `cases/PERF/PERF_0007/manifest.yaml`
- `cases/CONS/CONS_0005/README.md`
- `cases/CONS/CONS_0005/manifest.yaml`
- `cases/PORT/PORT_0003/README.md`
- `cases/PORT/PORT_0003/manifest.yaml`
- `cases/LONGTAIL/LONGTAIL_0011/README.md`
- `cases/LONGTAIL/LONGTAIL_0011/manifest.yaml`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Files deleted:
- Case-local `metadata/` directories for the five pilot cases.
- Case-local `data/` directories for the five pilot cases.

Validation:
- Static v2 validator passed for all five pilot cases.
- Unit tests passed: `PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`.
- Summary JSON parse and boundary assertions passed.
- `git diff --check`: passed.

Task result:
- Clean-template gap closure execution: yes.
- Pre-task extra path count: 61.
- Deleted paths count: 10.
- Skipped paths count: 51.
- Post-task extra path count: 51.
- Post-task blockers count: 51.
- Clean-template-minimal achieved: no.
- Retained evidence deleted: no.
- Unsafe evidence deleted: no.
- case_sets/inventory/reports/results changed: no.
- denominator/paper results changed: no.
- official metrics computed: no.
- DB/checker execution run: no.
- global leaderboard created: no.

Next safe action:
- Run a second targeted cleanup/planning task for checker/witness evidence references and legacy validation script migration before deleting case-local evidence or schema engine directories; otherwise proceed with Common-core 40 planning only with explicit blockers accepted.

### 2026-05-19 · 0ce5325 · case_package_v2_runs_reality_audit_and_policy_update_v0

Branch: `feature/case-package-v2-external-schema`
Mode: branch-only case-local runs reality audit and v2 policy refinement; no cleanup execution; no runs deletion; no DB/checker execution; no official metrics
Legacy repo modified: no
Release repo branch modified: yes
Commit: `0ce5325f458acc3f43226309244682be01a25354`
Push: succeeded; pushed branch `feature/case-package-v2-external-schema` to origin

Summary:
- Inspected all 100 current case-package directories under `cases/<POOL>/<CASE_ID>/`.
- Classified 1 case as `runs/` absent and 99 cases as placeholder-only `runs/`.
- Found 0 empty `runs/` directories, 0 retained-evidence-present `runs/` directories, 0 sensitive/private/raw-trace `runs/` directories, and 0 manual-review `runs/` directories.
- Performed a v2 policy update because placeholder-only `runs/` directories are common in the current branch.
- Added D027 and refined the v2 master plan/specs so empty or placeholder-only case-local `runs/` is not automatically retained evidence, while D005 remains valid for non-empty, uncertain, retained-evidence-present, sensitive/private, or raw-trace runs candidates.
- Did not modify case packages, delete runs, delete evidence, modify schemas, change `case_sets/`, inventory, reports/results, denominators, paper results, DB/checker outputs, official metrics, or leaderboard outputs.

Files created:
- `audits/case_package_v2_runs_reality_audit_v0/runs_reality_audit_summary.md`
- `audits/case_package_v2_runs_reality_audit_v0/case_local_runs_inventory.csv`
- `audits/case_package_v2_runs_reality_audit_v0/runs_classification_summary.csv`
- `audits/case_package_v2_runs_reality_audit_v0/runs_policy_refinement_matrix.csv`
- `audits/case_package_v2_runs_reality_audit_v0/future_case_package_v2_empty_runs_cleanup_prompt.md`
- `audits/case_package_v2_runs_reality_audit_v0/runs_reality_audit_summary.json`
- `audits/case_package_v2_runs_reality_audit_v0/runs_reality_audit_command_log.md`

Files modified:
- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/DECISION_LOG.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`
- `repository_spec/case_package_contract_v2_draft.md`
- `repository_spec/external_evidence_contract_v1_draft.md`

Validation:
- Summary JSON parse and boundary assertions passed.
- Protected path checks passed; no cases, runs, evidence, schemas, `case_sets/`, inventory, reports/results, denominator, paper-result, DB/checker output, official metrics, or leaderboard changes were detected.
- `git diff --check`: passed.

Task result:
- Runs reality audit: yes.
- Total cases inspected: 100.
- Runs absent count: 1.
- Runs empty count: 0.
- Runs placeholder-only count: 99.
- Runs retained-evidence-present count: 0.
- Runs sensitive/private/raw count: 0.
- Manual-review count: 0.
- Policy update performed: yes.
- Case files modified: no.
- Runs deleted: no.
- Evidence deleted: no.
- case_sets/inventory/reports/results changed: no.
- denominator/paper results changed: no.
- official metrics computed: no.
- DB/checker execution run: no.
- global leaderboard created: no.

Next safe action:
- Authorize `case_package_v2_empty_runs_cleanup_v0` only to delete audited empty or placeholder-only case-local `runs/` directories after policy acceptance, with no retained-evidence deletion.

### 2026-05-19 · 356c7fb · case_package_v2_empty_runs_cleanup_v0

Branch: `feature/case-package-v2-external-schema`
Mode: branch-only cleanup limited to audited placeholder-only case-local `runs/` directories; no retained-evidence deletion; no DB/checker execution; no official metrics
Legacy repo modified: no
Release repo branch modified: yes
Commit: `356c7fbe56089574869da1bd322827a61c75c2ad`
Push: succeeded to `origin/feature/case-package-v2-external-schema` (`6f139cc..356c7fb`)

Summary:
- Read the accepted runs reality audit and D027 policy refinement.
- Selected only 99 case-local `runs/` directories classified as `placeholder_only` in `audits/case_package_v2_runs_reality_audit_v0/case_local_runs_inventory.csv`.
- Reconfirmed each selected directory existed and contained only placeholder/README/marker content before deletion.
- Deleted 99 placeholder-only case-local `runs/` directories.
- Skipped 0 placeholder-only candidates. The audited absent `PORT_0008/runs/` path was not a deletion candidate and remained absent.
- Did not delete retained evidence, case-local evidence, schemas, reports, results, `case_sets/`, inventory, denominator inputs, paper-result inputs, DB/checker outputs, official metrics, or leaderboard outputs.

Files created:
- `audits/case_package_v2_empty_runs_cleanup_v0/empty_runs_cleanup_summary.md`
- `audits/case_package_v2_empty_runs_cleanup_v0/empty_runs_cleanup_candidates.csv`
- `audits/case_package_v2_empty_runs_cleanup_v0/empty_runs_deleted_manifest.csv`
- `audits/case_package_v2_empty_runs_cleanup_v0/empty_runs_cleanup_skipped.csv`
- `audits/case_package_v2_empty_runs_cleanup_v0/post_empty_runs_cleanup_validation_results.csv`
- `audits/case_package_v2_empty_runs_cleanup_v0/future_case_package_v2_post_empty_runs_parity_review_prompt.md`
- `audits/case_package_v2_empty_runs_cleanup_v0/empty_runs_cleanup_summary.json`
- `audits/case_package_v2_empty_runs_cleanup_v0/empty_runs_cleanup_command_log.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Files deleted:
- 99 tracked `cases/<POOL>/<CASE_ID>/runs/README.md` placeholder files, removing the corresponding placeholder-only case-local `runs/` directories from tracked content.

Validation:
- Static v2 validator passed for all five pilot cases.
- Unit tests passed: `PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`.
- Summary JSON parse and boundary assertions passed.
- Protected path checks passed; no retained evidence, evidence, schemas, `case_sets/`, inventory, reports/results, denominator, paper-result, DB/checker output, official metrics, or leaderboard changes were detected.
- `git diff --check`: passed.

Task result:
- Empty runs cleanup: yes.
- Audited placeholder-only runs candidates: 99.
- Runs deleted count: 99.
- Runs skipped count: 0.
- Retained evidence deleted: no.
- Evidence deleted: no.
- Schemas deleted: no.
- case_sets/inventory/reports/results changed: no.
- denominator/paper results changed: no.
- official metrics computed: no.
- DB/checker execution run: no.
- global leaderboard created: no.

Next safe action:
- Authorize `case_package_v2_post_empty_runs_parity_review_v0` as a read-only parity review after placeholder-only case-local `runs/` cleanup.

### 2026-05-19 · 4bc6eb0 · case_package_v2_post_empty_runs_parity_review_v0

Branch: `feature/case-package-v2-external-schema`
Mode: branch-only read-only parity review after placeholder-only case-local `runs/` cleanup; no cleanup execution; no case conversion; no DB/checker execution; no official metrics
Legacy repo modified: no
Release repo branch modified: yes
Commit: `4bc6eb0e0dda5f100b56a85d83c00c0b97abba68`
Push: succeeded to `origin/feature/case-package-v2-external-schema` (`cb52be3..4bc6eb0`)

Summary:
- Re-ran clean-template parity review for `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011` after audited placeholder-only case-local `runs/` cleanup.
- Confirmed all five pilot cases retain every clean-template-required asset and pass static v2 validation.
- Confirmed no tracked case-local `runs/` files remain for the five pilot cases.
- Recalculated remaining tracked extra path groups at 61.
- Recalculated remaining retention blockers at 5, all from case-local `evidence/`.
- Classified all five pilot cases as functional v2 with compatibility gaps, not clean-template-minimal.
- Confirmed Common-core 40 conversion planning is safe as a read-only planning task using the five-case pilot as a functional v2 template.
- Did not modify cases, schemas, evidence, runs, `case_sets/`, inventory, reports/results, denominators, paper results, DB/checker outputs, official metrics, or leaderboard outputs.

Files created:
- `audits/case_package_v2_post_empty_runs_parity_review_v0/post_empty_runs_parity_review_summary.md`
- `audits/case_package_v2_post_empty_runs_parity_review_v0/post_empty_runs_template_parity_case_summary.csv`
- `audits/case_package_v2_post_empty_runs_parity_review_v0/post_empty_runs_path_gap_matrix.csv`
- `audits/case_package_v2_post_empty_runs_parity_review_v0/post_empty_runs_evidence_schema_metadata_gap_matrix.csv`
- `audits/case_package_v2_post_empty_runs_parity_review_v0/post_empty_runs_remaining_action_plan.csv`
- `audits/case_package_v2_post_empty_runs_parity_review_v0/future_case_package_v2_clean_template_or_common_core40_plan_prompt.md`
- `audits/case_package_v2_post_empty_runs_parity_review_v0/post_empty_runs_parity_review_summary.json`
- `audits/case_package_v2_post_empty_runs_parity_review_v0/post_empty_runs_parity_review_command_log.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- Static v2 validator passed for all five pilot cases.
- Unit tests passed: `PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`.
- Summary JSON parse and boundary assertions passed.
- Protected path checks passed; no cases, schemas, evidence, runs deletion, `case_sets/`, inventory, reports/results, denominator, paper-result, DB/checker output, official metrics, or leaderboard changes were detected.
- `git diff --check`: passed.

Task result:
- Post-empty-runs parity review: yes.
- Pilot case IDs: `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.
- Cases modified: no.
- Remaining extra path groups: 61.
- Remaining retention blockers: 5.
- Clean-template-minimal status: not clean-template-minimal.
- Functional v2 status: accepted with compatibility gaps.
- Ready for Common-core 40 plan: yes, planning only.
- case_sets/inventory/reports/results changed: no.
- denominator/paper results changed: no.
- official metrics computed: no.
- DB/checker execution run: no.
- global leaderboard created: no.

Next safe action:
- Authorize `case_package_v2_common_core40_conversion_plan_v0` as a read-only planning task using the five-case pilot as a functional v2 template.

### 2026-05-19 · 2d8605b · case_package_v2_validation_evidence_unblock_v0

Branch: `feature/case-package-v2-external-schema`
Mode: branch-only targeted validation/evidence reference unblock; no deletion; no DB/checker execution; no official metrics
Legacy repo modified: no
Release repo branch modified: yes
Commit: `2d8605b1ec72dce0ca9a0815dc665dbc43f7fa50`
Push: succeeded to `origin/feature/case-package-v2-external-schema` (`17d9d74..2d8605b`)

Summary:
- Updated the five v2 pilot cases: `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.
- Updated 10 v2 validation wrappers to fail closed with future shared-runner messaging and no delegation to old engine-specific scripts.
- Confirmed wrappers do not reference case-local `schema/<engine>/` paths and still refuse case-local `runs/` outputs.
- Retargeted live manifest/checker/witness evidence references to external `evidence/cases/<POOL>/<CASE_ID>/` packages.
- Updated README wording so case-local evidence, schema engine dirs, and old validation scripts are compatibility-only cleanup candidates, not current required assets.
- Did not delete schema engine dirs, case-local evidence, metadata, data, old validation scripts, dialect variants, retained evidence, reports/results, or protected benchmark surfaces.

Files created:
- `audits/case_package_v2_validation_evidence_unblock_v0/validation_evidence_unblock_summary.md`
- `audits/case_package_v2_validation_evidence_unblock_v0/validation_reference_unblock_results.csv`
- `audits/case_package_v2_validation_evidence_unblock_v0/evidence_reference_unblock_results.csv`
- `audits/case_package_v2_validation_evidence_unblock_v0/schema_cleanup_readiness_after_unblock.csv`
- `audits/case_package_v2_validation_evidence_unblock_v0/legacy_validation_script_cleanup_readiness.csv`
- `audits/case_package_v2_validation_evidence_unblock_v0/validation_evidence_unblock_remaining_blockers.csv`
- `audits/case_package_v2_validation_evidence_unblock_v0/validation_evidence_unblock_protected_boundary_checks.csv`
- `audits/case_package_v2_validation_evidence_unblock_v0/future_case_package_v2_second_clean_template_cleanup_prompt.md`
- `audits/case_package_v2_validation_evidence_unblock_v0/validation_evidence_unblock_summary.json`
- `audits/case_package_v2_validation_evidence_unblock_v0/validation_evidence_unblock_command_log.md`

Files modified:
- Five pilot `manifest.yaml` files.
- Five pilot `README.md` files.
- Ten pilot v2 validation wrapper files.
- Checker config YAML files with stale case-local evidence references.
- `cases/PERF/PERF_0006/witness/data_profile.yaml`.
- `project_control/MIGRATION_STATUS.md`.
- `project_control/MIGRATION_RUN_LOG.md`.

Validation:
- Static v2 validator passed for all five pilot cases.
- Unit tests passed: `PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`.
- External evidence reference existence check passed for 371 references.
- Summary JSON parse and boundary assertions passed.
- `git diff --check`: passed.

Task result:
- Validation/evidence unblock: yes.
- Validation wrappers updated: yes.
- Evidence references updated: yes.
- Schema dirs deleted: no.
- Case-local evidence deleted: no.
- Metadata deleted: no.
- Data deleted: no.
- Old validation scripts deleted: no.
- Dialect variants deleted: no.
- case_sets/inventory/reports/results changed: no.
- denominator/paper results changed: no.
- official metrics computed: no.
- DB/checker execution run: no.
- global leaderboard created: no.

Next safe action:
- Authorize `case_package_v2_second_clean_template_cleanup_v0` to delete only readiness-marked legacy validation scripts, case-local schema engine dirs after legacy script deletion, and case-local evidence after final external mapping check; keep `PORT_0003` dialect variants unless separately approved.

### 2026-05-19 · fe8616f · case_package_v2_second_clean_template_cleanup_v0

Branch: `feature/case-package-v2-external-schema`
Mode: branch-only writable second clean-template cleanup; no DB/checker execution; no official metrics
Legacy repo modified: no
Release repo branch modified: yes
Commit: `fe8616f0`
Push: succeeded to `origin/feature/case-package-v2-external-schema` (`57091ec..fe8616f`)

Summary:
- Deleted 50 readiness-marked compatibility paths for `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.
- Deleted 30 legacy engine-specific validation scripts after confirming v2 wrappers do not call them.
- Deleted 15 case-local `schema/<engine>/` directories after verifying external schema DDL/load replacements.
- Deleted 5 case-local `evidence/` compatibility directories after verifying byte-for-byte external evidence mappings.
- Updated manifest and README compatibility wording to stop treating deleted paths as retained current assets.
- Retained `PORT_0003/sql/dialect_variants/` as an optional v2 semantic asset.
- Protected surfaces unchanged: no `case_sets/`, inventory, reports/results, denominator, paper result, official metric, DB/checker execution, or leaderboard changes.

Files created:
- `audits/case_package_v2_second_clean_template_cleanup_v0/second_clean_template_cleanup_summary.md`
- `audits/case_package_v2_second_clean_template_cleanup_v0/second_cleanup_candidate_matrix.csv`
- `audits/case_package_v2_second_clean_template_cleanup_v0/second_cleanup_deletions_manifest.csv`
- `audits/case_package_v2_second_clean_template_cleanup_v0/second_cleanup_skipped_manifest.csv`
- `audits/case_package_v2_second_clean_template_cleanup_v0/second_cleanup_reference_updates.csv`
- `audits/case_package_v2_second_clean_template_cleanup_v0/second_cleanup_post_parity_case_summary.csv`
- `audits/case_package_v2_second_clean_template_cleanup_v0/second_cleanup_post_path_gap_matrix.csv`
- `audits/case_package_v2_second_clean_template_cleanup_v0/second_cleanup_validator_results.csv`
- `audits/case_package_v2_second_clean_template_cleanup_v0/second_cleanup_protected_boundary_checks.csv`
- `audits/case_package_v2_second_clean_template_cleanup_v0/future_case_package_v2_pilot_acceptance_or_third_cleanup_prompt.md`
- `audits/case_package_v2_second_clean_template_cleanup_v0/second_clean_template_cleanup_summary.json`
- `audits/case_package_v2_second_clean_template_cleanup_v0/second_cleanup_command_log.md`

Files modified:
- Five pilot `manifest.yaml` files.
- Five pilot `README.md` files.
- `project_control/MIGRATION_STATUS.md`.
- `project_control/MIGRATION_RUN_LOG.md`.

Files deleted:
- 30 legacy engine-specific validation scripts.
- 15 case-local schema engine DDL/load directory groups.
- 5 case-local evidence compatibility directory groups.

Validation:
- Static v2 validator passed for all five pilot cases.
- Unit tests passed: `PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`.
- Summary JSON parse and boundary assertions passed.
- `git diff --check`: passed.

Task result:
- Second clean-template cleanup: yes.
- Selected candidates count: 50.
- Deleted paths count: 50.
- Skipped paths count: 1 optional retained dialect-variant group.
- Post-task extra path count: 1 optional dialect-variant group.
- Post-task blockers count: 0.
- Clean-template-minimal achieved: yes, with optional dialect variants retained.
- Retained evidence deleted: no.
- Unsafe evidence deleted: no.
- Dialect variants deleted: no.

Next safe action:
- Authorize pilot acceptance or a read-only Common-core 40 conversion plan; keep `PORT_0003` dialect variants unless a future portability review approves cleanup.

### 2026-05-19 · 5b045f4 · case_package_v2_evidence_surface_removal_policy_v0

Branch: `feature/case-package-v2-external-schema`
Mode: branch-only policy revision and reference-removal planning; no evidence deletion; no DB/checker execution; no official metrics
Legacy repo modified: no
Release repo branch modified: yes
Commit: `5b045f4e`
Push: succeeded to `origin/feature/case-package-v2-external-schema`

Summary:
- Revised v2 policy so static evidence directories are not required in the final clean v2 public case surface.
- Added D028: static evidence directories are not required in clean v2 public case surface.
- Updated the v2 case package contract, external evidence contract, and runtime witness policy for regeneration-first evidence.
- Updated static validator behavior to accept `evidence_policy.static_case_evidence: not_required` and not fail when `evidence_ref` is absent.
- Added tests for regeneration-first evidence policy and invalid evidence-policy values.
- Built a five-case reference-removal plan for live `evidence_ref` and `evidence/cases/<POOL>/<CASE_ID>/` references.
- No case files or evidence files were modified or deleted.

Files created:
- `audits/case_package_v2_evidence_surface_removal_policy_v0/evidence_surface_removal_policy_summary.md`
- `audits/case_package_v2_evidence_surface_removal_policy_v0/evidence_reference_inventory.csv`
- `audits/case_package_v2_evidence_surface_removal_policy_v0/evidence_policy_manifest_contract.csv`
- `audits/case_package_v2_evidence_surface_removal_policy_v0/evidence_surface_deletion_readiness.csv`
- `audits/case_package_v2_evidence_surface_removal_policy_v0/future_case_package_v2_evidence_reference_removal_execution_prompt.md`
- `audits/case_package_v2_evidence_surface_removal_policy_v0/evidence_surface_removal_policy_summary.json`
- `audits/case_package_v2_evidence_surface_removal_policy_v0/evidence_surface_removal_policy_command_log.md`

Files modified:
- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/DECISION_LOG.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`
- `repository_spec/case_package_contract_v2_draft.md`
- `repository_spec/external_evidence_contract_v1_draft.md`
- `repository_spec/runtime_witness_policy_v1_draft.md`
- `src/sql_rewrite_bench/case_package_v2_resolver.py`
- `tests/case_package_v2/test_case_package_v2_resolver.py`

Validation:
- Unit tests passed: `PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`.
- Static v2 validator passed for `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.
- Summary JSON parse and boundary assertions passed.
- `git diff --check`: passed.

Task result:
- Evidence surface policy revision: yes.
- Static evidence required for clean v2: no.
- Case-local evidence deletion performed: no.
- Top-level evidence deletion performed: no.
- Validator policy updated: yes.
- Tests updated: yes.
- Case files modified: no.
- Evidence deleted: no.
- reports/results changed: no.
- denominator/paper results changed: no.
- official metrics computed: no.
- DB/checker execution run: no.
- global leaderboard created: no.

Next safe action:
- Authorize `case_package_v2_evidence_reference_removal_execution_v0` to replace live five-case static evidence references with regeneration-first `evidence_policy` and delete only unreferenced static evidence surfaces after protected-boundary checks.

### 2026-05-19 · 6198b7df · case_package_v2_evidence_reference_removal_execution_v0

Branch: `feature/case-package-v2-external-schema`
Mode: branch-only writable evidence-reference removal and static evidence cleanup; no DB/checker execution; no official metrics
Legacy repo modified: no
Release repo branch modified: yes
Commit: `6198b7df`
Push: succeeded to `origin/feature/case-package-v2-external-schema`

Summary:
- Updated the five pilot manifests from mandatory `evidence_ref` to regeneration-first `evidence_policy`.
- Updated README evidence wording for all five pilot cases.
- Updated checker/witness YAML files that contained live static evidence paths.
- Deleted only the five pilot top-level static evidence packages under `evidence/cases/`.
- Case-local `evidence/` directories were already absent for all five pilot cases.
- No audits, reports/results, denominator, paper result, official metric, DB/checker execution, leaderboard, `case_sets/`, or inventory changes were made.

Files created:
- `audits/case_package_v2_evidence_reference_removal_execution_v0/evidence_reference_removal_execution_summary.md`
- `audits/case_package_v2_evidence_reference_removal_execution_v0/evidence_live_reference_updates.csv`
- `audits/case_package_v2_evidence_reference_removal_execution_v0/evidence_policy_conversion_results.csv`
- `audits/case_package_v2_evidence_reference_removal_execution_v0/evidence_surfaces_deleted_manifest.csv`
- `audits/case_package_v2_evidence_reference_removal_execution_v0/evidence_surfaces_skipped_manifest.csv`
- `audits/case_package_v2_evidence_reference_removal_execution_v0/post_evidence_removal_validator_results.csv`
- `audits/case_package_v2_evidence_reference_removal_execution_v0/evidence_removal_protected_boundary_checks.csv`
- `audits/case_package_v2_evidence_reference_removal_execution_v0/future_case_package_v2_post_evidence_removal_parity_review_prompt.md`
- `audits/case_package_v2_evidence_reference_removal_execution_v0/evidence_reference_removal_execution_summary.json`
- `audits/case_package_v2_evidence_reference_removal_execution_v0/evidence_reference_removal_execution_command_log.md`

Files modified:
- Five pilot `manifest.yaml` files.
- Five pilot `README.md` files.
- Pilot checker YAML files with live static evidence references.
- `cases/PERF/PERF_0006/witness/data_profile.yaml`.
- `project_control/MIGRATION_STATUS.md`.
- `project_control/MIGRATION_RUN_LOG.md`.

Files deleted:
- `evidence/cases/PERF/PERF_0006/`
- `evidence/cases/PERF/PERF_0007/`
- `evidence/cases/CONS/CONS_0005/`
- `evidence/cases/PORT/PORT_0003/`
- `evidence/cases/LONGTAIL/LONGTAIL_0011/`

Validation:
- Static v2 validator passed for `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.
- Unit tests passed: `PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`.
- Summary JSON parse and boundary assertions passed.
- `git diff --check`: passed.

Task result:
- Evidence reference removal execution: yes.
- Manifests updated to evidence_policy: yes.
- Live refs updated count: 24.
- Case-local evidence deleted count: 0.
- Top-level `evidence/cases/` deleted count: 5.
- Audits deleted: no.
- reports/results changed: no.
- denominator/paper results changed: no.
- official metrics computed: no.
- DB/checker execution run: no.
- global leaderboard created: no.
- `case_sets/` changed: no.
- inventory changed: no.

Next safe action:
- Run `case_package_v2_post_evidence_removal_parity_review_v0` as a read-only parity review before Common-core 40 planning.

### 2026-05-19 · a4de62b7 · case_package_v2_post_evidence_removal_parity_review_v0

Branch: `feature/case-package-v2-external-schema`
Mode: branch-only read-only parity review after static evidence reference removal; no cleanup execution; no DB/checker execution; no official metrics
Legacy repo modified: no
Release repo branch modified: yes
Commit: `a4de62b7`
Push: succeeded to `origin/feature/case-package-v2-external-schema`

Summary:
- Rechecked the five v2 pilot cases after `evidence_ref` was replaced with regeneration-first `evidence_policy` and the five top-level static evidence packages were deleted.
- Confirmed all five pilot cases have required tracked clean-template assets.
- Confirmed all five manifests have `evidence_policy` and omit `evidence_ref`.
- Confirmed case-local evidence and the five pilot top-level `evidence/cases/` packages are absent.
- Confirmed the only counted tracked extra path group is `cases/PORT/PORT_0003/sql/dialect_variants/spark/`, retained as an optional semantic v2 asset.
- Confirmed zero remaining blockers before Common-core 40 planning.
- No case files, schemas, evidence, `case_sets/`, inventory, reports/results, denominators, paper results, official metrics, DB/checker execution, or leaderboard outputs were changed.

Files created:
- `audits/case_package_v2_post_evidence_removal_parity_review_v0/post_evidence_removal_parity_review_summary.md`
- `audits/case_package_v2_post_evidence_removal_parity_review_v0/post_evidence_removal_case_summary.csv`
- `audits/case_package_v2_post_evidence_removal_parity_review_v0/post_evidence_removal_path_gap_matrix.csv`
- `audits/case_package_v2_post_evidence_removal_parity_review_v0/post_evidence_removal_clean_template_acceptance.csv`
- `audits/case_package_v2_post_evidence_removal_parity_review_v0/future_case_package_v2_common_core40_plan_prompt.md`
- `audits/case_package_v2_post_evidence_removal_parity_review_v0/post_evidence_removal_parity_review_summary.json`
- `audits/case_package_v2_post_evidence_removal_parity_review_v0/post_evidence_removal_parity_review_command_log.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- Static v2 validator passed for `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.
- Unit tests passed: `PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`.
- Summary JSON parse and boundary assertions passed.
- `git diff --check`: passed.

Task result:
- Post evidence removal parity review: yes.
- Clean-template-minimal achieved: yes.
- Remaining tracked extra path groups: 1.
- Remaining blockers count: 0.
- Optional dialect variants retained: yes.
- Ready for Common-core 40 plan: yes.
- Cases modified: no.
- Evidence modified: no.
- `case_sets/` changed: no.
- Inventory changed: no.
- Reports/results changed: no.
- Denominator/paper results changed: no.
- Official metrics computed: no.
- DB/checker execution run: no.
- Global leaderboard created: no.

Next safe action:
- Authorize `case_package_v2_common_core40_conversion_plan_v0` as a read-only Common-core 40 planning task before any wider conversion execution.

### 2026-05-19 · 51aebd6a · case_package_v2_common_core40_conversion_plan_v0

Branch: `feature/case-package-v2-external-schema`
Mode: branch-only read-only Common-core 40 v2 conversion planning; no writable conversion; no DB/checker execution; no official metrics
Legacy repo modified: no
Release repo branch modified: yes
Commit: `51aebd6a`
Push: succeeded to `origin/feature/case-package-v2-external-schema`

Summary:
- Planned clean-template-minimal v2 conversion for all 40 Common-core cases using the five accepted pilot cases as the canonical template.
- Reviewed `case_sets/common_core_v0/cases.csv`, `denominator_same_engine_120.csv`, `controls_360.csv`, and `inventory/case_registry.csv`.
- Confirmed 40 Common-core cases reviewed and five accepted pilots used.
- Classified 5 cases as already converted pilots, 5 cases as Wave A auto clean-template conversion, 22 cases as Wave B schema-grouped conversion, 1 case as Wave C manual schema/dialect review, and 7 PORT cases as blocked manual review.
- Defined folder-order plan: `manifest -> sql -> schema -> checker -> validation -> witness -> evidence_policy -> metadata -> notes -> runs -> README/validator`.
- Defined schema grouping and regeneration-first evidence-policy plans.
- Drafted future Wave A prompt for only `PERF_0008`, `PERF_0013`, `PERF_0017`, `PERF_0019`, and `PERF_0024`.
- No case files, schemas, evidence, runs, `case_sets/`, inventory, reports/results, denominators, paper results, official metrics, DB/checker execution, or leaderboard outputs were changed.

Files created:
- `audits/case_package_v2_common_core40_conversion_plan_v0/common_core40_v2_conversion_plan_summary.md`
- `audits/case_package_v2_common_core40_conversion_plan_v0/common_core40_v2_case_readiness.csv`
- `audits/case_package_v2_common_core40_conversion_plan_v0/common_core40_v2_folder_order_plan.csv`
- `audits/case_package_v2_common_core40_conversion_plan_v0/common_core40_schema_grouping_plan.csv`
- `audits/case_package_v2_common_core40_conversion_plan_v0/common_core40_evidence_policy_plan.csv`
- `audits/case_package_v2_common_core40_conversion_plan_v0/common_core40_conversion_waves.csv`
- `audits/case_package_v2_common_core40_conversion_plan_v0/common_core40_manual_review_blockers.csv`
- `audits/case_package_v2_common_core40_conversion_plan_v0/future_case_package_v2_common_core40_wave_a_prompt.md`
- `audits/case_package_v2_common_core40_conversion_plan_v0/common_core40_v2_conversion_plan_summary.json`
- `audits/case_package_v2_common_core40_conversion_plan_v0/common_core40_v2_conversion_plan_command_log.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- Summary JSON parse and boundary assertions passed.
- CSV headers parse passed.
- `git diff --check`: passed.

Task result:
- Read-only Common-core 40 v2 plan: yes.
- Common-core cases reviewed: 40.
- Pilot cases used: `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, `LONGTAIL_0011`.
- Clean-template-minimal gate used: yes.
- Planned future wave count: 3.
- Wave A case count: 5.
- Wave B case count: 22.
- Wave C/manual-review count: 8.
- Case files modified: no.
- Schemas modified: no.
- Evidence modified: no.
- Runs deleted: no.
- `case_sets/` changed: no.
- Inventory changed: no.
- Reports/results changed: no.
- Denominator/paper results changed: no.
- Official metrics computed: no.
- DB/checker execution run: no.
- Global leaderboard created: no.

Next safe action:
- Authorize `case_package_v2_common_core40_wave_a_v0` as a bounded writable Wave A conversion for `PERF_0008`, `PERF_0013`, `PERF_0017`, `PERF_0019`, and `PERF_0024` only.

### 2026-05-19 · 15385da0 · case_package_v2_common_core40_wave_a_v0

Branch: `feature/case-package-v2-external-schema`
Mode: branch-only bounded writable Common-core Wave A v2 conversion; no DB/checker execution; no official metrics; no reports/results migration
Legacy repo modified: no
Release repo branch modified: yes
Commit: `15385da0`
Push: succeeded to `origin/feature/case-package-v2-external-schema`

Summary:
- Converted exactly five Wave A Common-core cases: `PERF_0008`, `PERF_0013`, `PERF_0017`, `PERF_0019`, and `PERF_0024`.
- Used the accepted clean-template-minimal pilot cases as the canonical manifest and case-local structure examples.
- Normalized manifests to canonical v2 shape with direct SQL path lists, profile-first `schema_ref`, config-only checker refs, thin validation wrappers, source-as-oracle witness policy, and regeneration-first `evidence_policy`.
- Created case-specific external schema packages after verifying Wave A DDL/load assets differed by case.
- Removed clean-template-disallowed compatibility surfaces from the five Wave A case packages after references and validators were updated.
- Did not modify pilot cases, `case_sets/`, inventory, reports/results, denominator values, paper results, official metrics, DB/checker execution, or leaderboard outputs.

Files created:
- Direct SQL files, thin validation wrappers, and witness profiles under the five Wave A case packages.
- External schema packages under `schemas/tpch_perf0008_v0/`, `schemas/tpch_perf0013_v0/`, `schemas/tpch_perf0017_v0/`, `schemas/tpch_perf0019_v0/`, and `schemas/tpch_perf0024_v0/`.
- Audit outputs under `audits/case_package_v2_common_core40_wave_a_v0/`.

Files modified/deleted:
- Modified only the five Wave A case packages, the five new external schema packages, Wave A audit outputs, and project-control files.
- Deleted nested SQL compatibility directories, case-local engine schema directories, case-local evidence/metadata/notes/data compatibility directories, and old engine-specific validation scripts for the five Wave A cases.

Validation:
- Static v2 validators passed for all five Wave A cases.
- Static v2 validators passed for the five accepted pilot cases.
- `PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`: passed.
- Summary JSON assertion passed.
- Audit CSV header parse check passed.
- Protected boundary checks passed.
- `git diff --check`: passed.

Task result:
- Common-core 40 Wave A conversion: yes.
- Converted case IDs: `PERF_0008`, `PERF_0013`, `PERF_0017`, `PERF_0019`, `PERF_0024`.
- Deferred case IDs: none.
- Clean-template-minimal cases: all five Wave A cases.
- Manifest consistency passed: yes.
- Schemas created/reused: `tpch_perf0008_v0`, `tpch_perf0013_v0`, `tpch_perf0017_v0`, `tpch_perf0019_v0`, `tpch_perf0024_v0`.
- Case files modified: yes.
- Schemas modified: yes.
- Evidence modified: no top-level evidence changes.
- `evidence/cases/` created: no.
- Runs deleted/absent: all five Wave A case-local `runs/` directories absent.
- `case_sets/` changed: no.
- Inventory changed: no.
- Reports/results changed: no.
- Denominator/paper results changed: no.
- Official metrics computed: no.
- DB/checker execution run: no.
- Global leaderboard created: no.

Next safe action:
- Run `case_package_v2_common_core40_wave_a_post_conversion_parity_review_v0` as a bounded read-only review before authorizing Wave B or wider Common-core conversion.

### 2026-05-20 · 4c5afe5d · case_package_v2_common_core40_wave_a_post_conversion_parity_review_v0

Branch: `feature/case-package-v2-external-schema`
Mode: branch-only read-only Wave A post-conversion parity review; no writable conversion; no DB/checker execution; no official metrics
Legacy repo modified: no
Release repo branch modified: yes
Commit: `4c5afe5d`
Push: succeeded to `origin/feature/case-package-v2-external-schema`

Summary:
- Reviewed exactly five converted Wave A cases: `PERF_0008`, `PERF_0013`, `PERF_0017`, `PERF_0019`, and `PERF_0024`.
- Rechecked accepted pilot cases for validator non-regression: `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.
- Confirmed Wave A clean-template-minimal case-local structure with no remaining Wave A gaps.
- Confirmed Wave A manifest consistency: direct SQL refs, profile-first schema refs, canonical checker/validation refs, source-as-oracle witness policy, regeneration-first `evidence_policy`, and no mandatory `evidence_ref`.
- Confirmed schema policy: case-local `schema/schema_profile.yaml` only, with external schema package refs resolving for all five case-specific schema IDs.
- Did not modify case files, schemas, `case_sets/`, inventory, reports/results, denominators, paper results, official metrics, DB/checker outputs, or leaderboard outputs.

Files created:
- `audits/case_package_v2_common_core40_wave_a_post_conversion_parity_review_v0/wave_a_post_conversion_parity_review_summary.md`
- `audits/case_package_v2_common_core40_wave_a_post_conversion_parity_review_v0/wave_a_post_conversion_case_summary.csv`
- `audits/case_package_v2_common_core40_wave_a_post_conversion_parity_review_v0/wave_a_manifest_consistency_recheck.csv`
- `audits/case_package_v2_common_core40_wave_a_post_conversion_parity_review_v0/wave_a_clean_template_gap_matrix.csv`
- `audits/case_package_v2_common_core40_wave_a_post_conversion_parity_review_v0/wave_a_schema_policy_recheck.csv`
- `audits/case_package_v2_common_core40_wave_a_post_conversion_parity_review_v0/wave_a_protected_boundary_checks.csv`
- `audits/case_package_v2_common_core40_wave_a_post_conversion_parity_review_v0/future_case_package_v2_common_core40_wave_b_prompt.md`
- `audits/case_package_v2_common_core40_wave_a_post_conversion_parity_review_v0/wave_a_post_conversion_parity_review_summary.json`
- `audits/case_package_v2_common_core40_wave_a_post_conversion_parity_review_v0/wave_a_post_conversion_parity_review_command_log.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- Static v2 validators passed for all five Wave A cases.
- Static v2 validators passed for all five accepted pilot cases.
- `PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`: passed, 11 tests.
- Summary JSON parse and assertions passed.
- CSV header parse passed.
- Protected boundary checks passed.
- Generated CSV line endings normalized to LF after initial diff-check warning.
- `git diff --check`: passed.

Task result:
- Wave A post-conversion parity review: yes.
- Wave A clean-template-minimal passed: yes.
- Manifest consistency passed: yes.
- Remaining Wave A gaps: none.
- Ready for Wave B: yes.
- Case files modified: no.
- Schemas modified: no.
- `case_sets/` changed: no.
- Inventory changed: no.
- Reports/results changed: no.
- Denominator/paper results changed: no.
- Official metrics computed: no.
- DB/checker execution run: no.
- Global leaderboard created: no.

Next safe action:
- Authorize a bounded `case_package_v2_common_core40_wave_b_v0` conversion for schema-grouped non-PORT Wave B cases only.

### 2026-05-20 · 42ef2462 · case_package_v2_common_core40_wave_b_v0

Branch: `feature/case-package-v2-external-schema`
Mode: branch-only bounded writable Common-core Wave B v2 conversion; no DB/checker execution; no official metrics; no reports/results migration
Legacy repo modified: no
Release repo branch modified: yes
Commit: `42ef2462`
Push: succeeded to `origin/feature/case-package-v2-external-schema`

Summary:
- Converted exactly 22 Wave B Common-core cases: `PERF_0033`, `PERF_0034`, `PERF_0035`, `PERF_0052`, `PERF_0054`, `PERF_0056`, `PERF_0062`, `PERF_0077`, `PERF_0082`, `CONS_0007`, `CONS_0009`, `CONS_0010`, `CONS_0011`, `CONS_0012`, `CONS_0024`, `CONS_0036`, `CONS_0037`, `LONGTAIL_0012`, `LONGTAIL_0013`, `LONGTAIL_0022`, `LONGTAIL_0023`, and `LONGTAIL_0024`.
- Used the accepted clean-template-minimal pilot cases and Wave A cases as canonical templates.
- Normalized manifests to canonical v2 shape with direct SQL path lists, profile-first `schema_ref`, config-only checker refs, thin validation wrappers, source-as-oracle witness policy, and regeneration-first `evidence_policy`.
- Created 22 case-specific external schema packages because exact Wave B DDL/load assets differed by case; no unsafe grouped schema reuse was performed.
- Removed clean-template-disallowed compatibility surfaces from only the 22 Wave B case packages after direct paths, external schemas, and policy references were established.
- Did not modify pilot cases, Wave A cases, PORT manual-review cases, `case_sets/`, inventory, reports/results, denominator values, paper results, official metrics, DB/checker execution, or leaderboard outputs.

Files created:
- Direct SQL files, thin validation wrappers, and witness profiles under the 22 Wave B case packages.
- External schema packages under the 22 new Wave B schema IDs.
- Audit outputs under `audits/case_package_v2_common_core40_wave_b_v0/`.

Files modified/deleted:
- Modified only the 22 Wave B case packages, new external schema packages, Wave B audit outputs, and project-control files.
- Deleted nested SQL compatibility directories, case-local engine schema directories, case-local evidence/metadata/notes/data compatibility directories, and old engine-specific validation scripts for the 22 Wave B cases.

Validation:
- Static v2 validators passed for all 22 Wave B cases.
- Static v2 validators passed for the five accepted pilot cases.
- Static v2 validators passed for the five Wave A cases.
- `PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`: passed, 11 tests.
- Summary JSON assertion passed.
- Protected boundary checks passed.
- `git diff --check`: passed.

Task result:
- Common-core 40 Wave B conversion: yes.
- Converted case IDs: all 22 target cases.
- Deferred case IDs: none.
- Clean-template-minimal cases: all 22 target cases.
- Manifest consistency passed: yes.
- Schemas created/reused: 22 case-specific external schema packages.
- Case files modified: yes.
- Schemas modified: yes.
- Evidence modified: no top-level evidence changes.
- `evidence/cases/` created: no.
- Runs deleted/absent: case-local runs absent or removed for clean v2.
- `case_sets/` changed: no.
- Inventory changed: no.
- Reports/results changed: no.
- Denominator/paper results changed: no.
- Official metrics computed: no.
- DB/checker execution run: no.
- Global leaderboard created: no.

Next safe action:
- Run `case_package_v2_common_core40_wave_b_post_conversion_review_v0` as a bounded read-only review before authorizing Wave C/manual-review conversion.

### 2026-05-20 · 9d6310d8 · case_package_v2_common_core40_wave_b_post_conversion_review_v0

Branch: `feature/case-package-v2-external-schema`
Mode: branch-only read-only Common-core Wave B post-conversion parity review; no writable conversion; no DB/checker execution; no official metrics
Legacy repo modified: no
Release repo branch modified: yes
Commit: `9d6310d8`
Push: succeeded to `origin/feature/case-package-v2-external-schema`

Summary:
- Reviewed exactly 22 converted Wave B cases: `PERF_0033`, `PERF_0034`, `PERF_0035`, `PERF_0052`, `PERF_0054`, `PERF_0056`, `PERF_0062`, `PERF_0077`, `PERF_0082`, `CONS_0007`, `CONS_0009`, `CONS_0010`, `CONS_0011`, `CONS_0012`, `CONS_0024`, `CONS_0036`, `CONS_0037`, `LONGTAIL_0012`, `LONGTAIL_0013`, `LONGTAIL_0022`, `LONGTAIL_0023`, and `LONGTAIL_0024`.
- Rechecked accepted pilot cases for validator non-regression: `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.
- Rechecked Wave A cases for validator non-regression: `PERF_0008`, `PERF_0013`, `PERF_0017`, `PERF_0019`, and `PERF_0024`.
- Confirmed Wave B clean-template-minimal structure, manifest consistency, schema policy, evidence policy, and absence of v1 compatibility surfaces for all 22 Wave B cases.
- Confirmed remaining Wave B gaps: none.
- Did not modify case files, schemas, `case_sets/`, inventory, reports/results, denominators, paper results, official metrics, DB/checker execution, or leaderboard outputs.

Files created:
- `audits/case_package_v2_common_core40_wave_b_post_conversion_review_v0/wave_b_post_conversion_review_summary.md`
- `audits/case_package_v2_common_core40_wave_b_post_conversion_review_v0/wave_b_post_conversion_case_summary.csv`
- `audits/case_package_v2_common_core40_wave_b_post_conversion_review_v0/wave_b_manifest_consistency_recheck.csv`
- `audits/case_package_v2_common_core40_wave_b_post_conversion_review_v0/wave_b_clean_template_gap_matrix.csv`
- `audits/case_package_v2_common_core40_wave_b_post_conversion_review_v0/wave_b_schema_policy_recheck.csv`
- `audits/case_package_v2_common_core40_wave_b_post_conversion_review_v0/wave_b_non_mutation_recheck.csv`
- `audits/case_package_v2_common_core40_wave_b_post_conversion_review_v0/wave_b_protected_boundary_checks.csv`
- `audits/case_package_v2_common_core40_wave_b_post_conversion_review_v0/future_case_package_v2_wave_c_manual_review_prompt.md`
- `audits/case_package_v2_common_core40_wave_b_post_conversion_review_v0/wave_b_post_conversion_review_summary.json`
- `audits/case_package_v2_common_core40_wave_b_post_conversion_review_v0/wave_b_post_conversion_review_command_log.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- Static v2 validators passed for all 22 Wave B cases.
- Static v2 validators passed for all five accepted pilot cases.
- Static v2 validators passed for all five Wave A cases.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`: passed, 11 tests.
- Summary JSON assertion: pending final run.
- `git diff --check`: pending final run.

Task result:
- Wave B post-conversion review: yes.
- Wave B clean-template-minimal passed: yes.
- Manifest consistency passed: yes.
- Remaining Wave B gaps: none.
- Ready for Wave C planning: yes.
- Case files modified: no.
- Schemas modified: no.
- `case_sets/` changed: no.
- Inventory changed: no.
- Reports/results changed: no.
- Denominator/paper results changed: no.
- Official metrics computed: no.
- DB/checker execution run: no.
- Global leaderboard created: no.

Next safe action:
- Authorize `case_package_v2_common_core40_wave_c_manual_review_plan_v0` as a bounded planning task before any Wave C/PORT manual-review conversion execution.

### 2026-05-20 · f32456b0 · case_package_v2_manifest_contract_repair_v0

Branch: `feature/case-package-v2-external-schema`
Mode: branch-only writable manifest semantic-contract repair; no Wave C conversion; no DB/checker execution; no official metrics
Legacy repo modified: no
Release repo branch modified: yes
Commit: `f32456b0`
Push: succeeded to `origin/feature/case-package-v2-external-schema`

Summary:
- Repaired `manifest.yaml` for 32 already converted v2 cases: five accepted pilots, five Wave A cases, and 22 Wave B cases.
- Restored taxonomy for all 32 cases from branch history/deleted metadata, not README-only wording.
- Replaced old list-shaped manifest semantics with colleague-style semantic sections while preserving clean-template physical paths.
- Required object-form `sql.positive_rewrites` and `sql.hard_negatives`, `schema.profile`, `schema.external_profile`, config-only checker paths, v2 validation wrappers, source-as-oracle witness policy, and regeneration-first `evidence_policy`.
- Retained `manual_review_required` status for 17 cases where explicit draft origin or original source path could not be recovered safely without invention.
- Updated the static v2 validator and tests to require taxonomy, source family, status, object-form SQL entries, schema profile fields, checker paths, validation paths, and `evidence_policy`, and to reject required `evidence_ref`, `schema_ref.engines`, absolute/local paths, and deleted compatibility path references.
- Did not restore case-local schema engine directories, evidence, runs, metadata, notes, data, old validation scripts, or per-case Python checker scripts.
- Did not modify `case_sets/`, inventory, reports/results, denominator values, paper results, official metrics, DB/checker execution, or leaderboard outputs.

Files created:
- `audits/case_package_v2_manifest_contract_repair_v0/manifest_contract_repair_summary.md`
- `audits/case_package_v2_manifest_contract_repair_v0/manifest_repair_case_status.csv`
- `audits/case_package_v2_manifest_contract_repair_v0/manifest_taxonomy_recovery_matrix.csv`
- `audits/case_package_v2_manifest_contract_repair_v0/manifest_semantic_field_completeness.csv`
- `audits/case_package_v2_manifest_contract_repair_v0/manifest_format_consistency_audit.csv`
- `audits/case_package_v2_manifest_contract_repair_v0/manifest_repair_manual_review_blockers.csv`
- `audits/case_package_v2_manifest_contract_repair_v0/manifest_repair_validator_results.csv`
- `audits/case_package_v2_manifest_contract_repair_v0/manifest_repair_protected_boundary_checks.csv`
- `audits/case_package_v2_manifest_contract_repair_v0/future_case_package_v2_wave_c_or_manifest_repair_followup_prompt.md`
- `audits/case_package_v2_manifest_contract_repair_v0/manifest_contract_repair_summary.json`
- `audits/case_package_v2_manifest_contract_repair_v0/manifest_contract_repair_command_log.md`

Validation:
- Static v2 validators passed for all 32 repaired cases.
- `PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`: passed, 15 tests.
- Summary JSON assertion: pending final run.
- `git diff --check`: pending final run.

Task result:
- Manifest contract repair: yes.
- Cases targeted: 32.
- Cases repaired: 32.
- Cases retaining manual-review caveats: 17.
- Taxonomy restored count: 32.
- Semantic fields restored count: 621 safe field instances.
- Validator updated: yes.
- Tests updated: yes.
- Case files modified: yes, manifest files only for the already converted v2 cases.
- `case_sets/` changed: no.
- Inventory changed: no.
- Reports/results changed: no.
- Denominator/paper results changed: no.
- Official metrics computed: no.
- DB/checker execution run: no.
- Global leaderboard created: no.

Next safe action:
- Resolve manifest manual-review provenance caveats in a bounded follow-up, or run Wave C planning without inventing unrecovered source fields.

### 2026-05-20 · 151b8e4 · case_package_v2_manifest_caveat_closeout_v0

Branch: `feature/case-package-v2-external-schema`
Mode: branch-only manifest caveat closeout; no Wave C conversion; no new case conversion; no DB/checker execution; no official metrics
Legacy repo modified: no
Release repo branch modified: yes
Commit: `151b8e4`
Push: succeeded to `origin/feature/case-package-v2-external-schema`

Summary:
- Reviewed the 32 already converted v2 manifests from the accepted pilots, Wave A, and Wave B.
- Reviewed 19 retained provenance caveat rows from `case_package_v2_manifest_contract_repair_v0`.
- Reclassified 17 draft-origin fallback caveats as accepted non-blocking release caveats without inventing a distinct draft artifact.
- Applied 1 safe field-level repair: `PORT_0003` `draft_origin.origin_id` now uses the branch-history `source_entry_pointer` fallback instead of the literal `manual_review_required` placeholder.
- Retained 2 manual-review caveats for `PERF_0077` and `PERF_0082` `source_path`; branch-history provenance leaves `source_entry` blank and records only legacy case-local source materialization.
- Did not update validator code or tests.
- Did not restore deleted schema/evidence/runs/metadata/notes/data directories, case-local evidence, top-level `evidence/cases/`, old validation scripts, or per-case Python checker scripts.
- Did not modify `case_sets/`, inventory, reports/results, denominator values, paper results, official metrics, DB/checker execution, or leaderboard outputs.

Files created:
- `audits/case_package_v2_manifest_caveat_closeout_v0/manifest_caveat_closeout_summary.md`
- `audits/case_package_v2_manifest_caveat_closeout_v0/manifest_caveat_inventory.csv`
- `audits/case_package_v2_manifest_caveat_closeout_v0/manifest_caveat_repair_actions.csv`
- `audits/case_package_v2_manifest_caveat_closeout_v0/manifest_caveat_remaining_manual_review.csv`
- `audits/case_package_v2_manifest_caveat_closeout_v0/manifest_caveat_nonblocking_acceptance.csv`
- `audits/case_package_v2_manifest_caveat_closeout_v0/manifest_caveat_validator_results.csv`
- `audits/case_package_v2_manifest_caveat_closeout_v0/manifest_caveat_protected_boundary_checks.csv`
- `audits/case_package_v2_manifest_caveat_closeout_v0/future_case_package_v2_wave_c_or_caveat_followup_prompt.md`
- `audits/case_package_v2_manifest_caveat_closeout_v0/manifest_caveat_closeout_summary.json`
- `audits/case_package_v2_manifest_caveat_closeout_v0/manifest_caveat_closeout_command_log.md`

Validation:
- Static v2 validators passed for all 32 target cases.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`: passed, 15 tests.
- Summary JSON assertion: passed.
- CSV header/row parse check: passed.
- `git diff --check`: passed.
- Boundary checks found no `case_sets/`, inventory, reports/results, schema, evidence, denominator, paper-result, official-metric, DB/checker execution, or leaderboard changes.

Task result:
- Manifest caveat closeout: yes.
- Cases reviewed: 32.
- Caveats reviewed: 19.
- Caveats repaired: 1.
- Caveats accepted nonblocking: 17.
- Caveats remaining manual review: 2.
- Wave C allowed after closeout: yes.
- Case files modified: yes, manifest files only for 17 target cases.
- Validator updated: no.
- Tests updated: no.
- `case_sets/` changed: no.
- Inventory changed: no.
- Reports/results changed: no.
- Denominator/paper results changed: no.
- Official metrics computed: no.
- DB/checker execution run: no.
- Global leaderboard created: no.

Next safe action:
- Authorize `case_package_v2_common_core40_wave_c_manual_review_plan_v0` for remaining PORT/manual-review planning, with a separate narrow source-path provenance follow-up for `PERF_0077` and `PERF_0082` before final public source-path closeout.

### 2026-05-20 · case_package_v2_common_core40_wave_c_manual_review_plan_v0

Branch: `feature/case-package-v2-external-schema`
Mode: branch-only read-only Wave C/manual-review planning; no writable conversion; no PORT conversion execution; no DB/checker execution; no official metrics
Legacy repo modified: no
Release repo branch modified: yes, audit/project-control files only

Summary:
- Identified the exact Wave C/manual-review Common-core case list from `common_core40_conversion_waves.csv`, `common_core40_manual_review_blockers.csv`, `common_core40_v2_case_readiness.csv`, and `case_sets/common_core_v0/cases.csv`.
- Reviewed 8 remaining PORT/manual-review cases: `PORT_0004`, `PORT_0005`, `PORT_0008`, `PORT_0012`, `PORT_0013`, `PORT_0022`, `PORT_0024`, and `PORT_0025`.
- Confirmed the 8-case Wave C set equals the Common-core 40 set minus the 32 already converted/repaired v2 cases.
- Classified readiness: ready for conversion now = 0; ready after manifest review = 0; ready after dialect/schema review = 1 (`PORT_0005`); deferred manual review = 7 D008 cases.
- Recorded that `PERF_0077` and `PERF_0082` source-path caveats are already converted Wave B caveats, do not block Wave C planning, and require a separate narrow provenance follow-up before final public source-path closeout.
- Recommended a read-only Wave C preclearance packet before any writable Wave C conversion.
- Did not modify case packages, schemas, `case_sets/`, inventory, reports/results, denominator values, paper results, official metrics, DB/checker execution, or leaderboard outputs.

Files created:
- `audits/case_package_v2_common_core40_wave_c_manual_review_plan_v0/wave_c_manual_review_plan_summary.md`
- `audits/case_package_v2_common_core40_wave_c_manual_review_plan_v0/wave_c_case_readiness.csv`
- `audits/case_package_v2_common_core40_wave_c_manual_review_plan_v0/wave_c_manifest_risk_matrix.csv`
- `audits/case_package_v2_common_core40_wave_c_manual_review_plan_v0/wave_c_schema_and_dialect_plan.csv`
- `audits/case_package_v2_common_core40_wave_c_manual_review_plan_v0/wave_c_execution_wave_plan.csv`
- `audits/case_package_v2_common_core40_wave_c_manual_review_plan_v0/wave_c_deferred_or_manual_review.csv`
- `audits/case_package_v2_common_core40_wave_c_manual_review_plan_v0/perf0077_perf0082_source_path_followup_plan.csv`
- `audits/case_package_v2_common_core40_wave_c_manual_review_plan_v0/future_case_package_v2_common_core40_wave_c_execution_prompt.md`
- `audits/case_package_v2_common_core40_wave_c_manual_review_plan_v0/wave_c_manual_review_plan_summary.json`
- `audits/case_package_v2_common_core40_wave_c_manual_review_plan_v0/wave_c_manual_review_plan_command_log.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- Summary JSON assertion: passed.
- CSV parse/header checks: passed.
- `git diff --check`: passed.
- Boundary checks confirmed no `cases/`, schemas, `case_sets/`, inventory, reports/results, denominator, paper-result, official-metric, DB/checker execution, or leaderboard changes.

Task result:
- Wave C manual-review plan: yes.
- Read-only plan: yes.
- Wave C cases reviewed: 8.
- Ready for conversion count: 0.
- Ready after manifest review count: 0.
- Ready after dialect review count: 1.
- Deferred manual-review count: 7.
- `PERF_0077`/`PERF_0082` follow-up recorded: yes.
- Case files modified: no.
- Schemas modified: no.
- `case_sets/` changed: no.
- Inventory changed: no.
- Reports/results changed: no.
- Denominator/paper results changed: no.
- Official metrics computed: no.
- DB/checker execution run: no.
- Global leaderboard created: no.

Next safe action:
- Authorize `case_package_v2_common_core40_wave_c_preclearance_v0` to resolve D008 public-safety, dialect-variant, and schema decisions for the eight PORT Wave C cases before any writable Wave C conversion execution.

### 2026-05-20 · case_package_v2_common_core40_wave_c_preclearance_v0

Branch: `feature/case-package-v2-external-schema`
Mode: branch-only read-only Wave C preclearance; no writable conversion; no PORT case conversion; no DB/checker execution; no official metrics
Legacy repo modified: no
Release repo branch modified: yes, audit/project-control files only

Summary:
- Reviewed 8 Wave C PORT cases: `PORT_0004`, `PORT_0005`, `PORT_0008`, `PORT_0012`, `PORT_0013`, `PORT_0022`, `PORT_0024`, and `PORT_0025`.
- Resolved D008/public-safety preclearance for future v2 conversion: public-safe count 8, public-safe-after-redaction count 0, D008-blocked count 0.
- Confirmed no literal secrets, prompt/API/token/model traces, raw stdout/stderr payloads, or private host/user paths in the inspected release case surfaces; findings were sanitized placeholders or environment-variable based validation-script references.
- Decided that existing Spark dialect variants must be retained for `PORT_0004`, `PORT_0005`, and `PORT_0013`; deletion is not allowed by Wave C conversion.
- Precleared per-case schema strategy for all 8 cases with proposed schema ids `parrot_bird_port0004_v0`, `parrot_bird_port0005_v0`, `parrot_bird_port0008_v0`, `parrot_bird_port0012_v0`, `parrot_bird_port0013_v0`, `parrot_bird_port0022_v0`, `parrot_bird_port0024_v0`, and `parrot_bird_port0025_v0`.
- Precleared manifest semantics for all 8 cases; future conversion must retain explicit non-blocking draft-origin caveats where exact draft ids are absent and must not invent source/provenance/taxonomy/dialect semantics.
- Recommended writable subwaves: `PORT_0005` first, then D008-cleared cases without current dialect variants, then D008-cleared cases with retained Spark dialect variants.
- Recorded again that `PERF_0077` and `PERF_0082` are already converted Wave B cases, do not block Wave C conversion, and still require a separate narrow source-path provenance follow-up before final public source-path closeout.
- Did not modify case packages, schemas, `case_sets/`, inventory, reports/results, denominator values, paper results, official metrics, DB/checker execution, evidence directories, dialect variants, or leaderboard outputs.

Files created:
- `audits/case_package_v2_common_core40_wave_c_preclearance_v0/wave_c_preclearance_summary.md`
- `audits/case_package_v2_common_core40_wave_c_preclearance_v0/wave_c_public_safety_preclearance.csv`
- `audits/case_package_v2_common_core40_wave_c_preclearance_v0/wave_c_dialect_variant_decisions.csv`
- `audits/case_package_v2_common_core40_wave_c_preclearance_v0/wave_c_schema_preclearance.csv`
- `audits/case_package_v2_common_core40_wave_c_preclearance_v0/wave_c_manifest_preclearance.csv`
- `audits/case_package_v2_common_core40_wave_c_preclearance_v0/wave_c_subwave_recommendations.csv`
- `audits/case_package_v2_common_core40_wave_c_preclearance_v0/wave_c_deferred_after_preclearance.csv`
- `audits/case_package_v2_common_core40_wave_c_preclearance_v0/perf0077_perf0082_source_path_followup_reminder.csv`
- `audits/case_package_v2_common_core40_wave_c_preclearance_v0/future_case_package_v2_wave_c_subwave_execution_prompt.md`
- `audits/case_package_v2_common_core40_wave_c_preclearance_v0/wave_c_preclearance_summary.json`
- `audits/case_package_v2_common_core40_wave_c_preclearance_v0/wave_c_preclearance_command_log.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- Summary JSON assertion: passed.
- CSV parse/header checks: passed.
- `git diff --check`: passed.
- Boundary checks confirmed no `cases/`, schemas, `case_sets/`, inventory, reports/results, denominator, paper-result, official-metric, DB/checker execution, evidence, dialect-variant, or leaderboard changes.

Task result:
- Wave C preclearance: yes.
- Read-only preclearance: yes.
- Wave C cases reviewed: 8.
- Public-safe count: 8.
- Public-safe-after-redaction count: 0.
- D008-blocked count: 0.
- Dialect-variant retain count: 3.
- Schema precleared count: 8.
- Manifest precleared count: 8.
- Ready for writable conversion count: 8.
- Deferred manual-review count: 0.
- `PERF_0077`/`PERF_0082` follow-up recorded: yes.
- Case files modified: no.
- Schemas modified: no.
- `case_sets/` changed: no.
- Inventory changed: no.
- Reports/results changed: no.
- Denominator/paper results changed: no.
- Official metrics computed: no.
- DB/checker execution run: no.
- Global leaderboard created: no.

Next safe action:
- Authorize `case_package_v2_common_core40_wave_c_subwave_1_port0005_v0` as a bounded writable conversion for `PORT_0005` only, preserving Spark dialect variants and all protected surfaces before broader Wave C subwaves.

### 2026-05-20 · case_package_v2_validation_contract_repair_v0

Branch: `feature/case-package-v2-external-schema`
Mode: branch-only validation contract repair for 32 already converted v2 cases; no Wave C conversion; no DB/checker execution; no official metrics
Legacy repo modified: no
Release repo branch modified: yes, target validation files/manifests, shared validation modules, validator/tests/specs, audit/project-control files only

Summary:
- Adopted the three-file clean v2 validation contract: `validation/run_validation.sh`, `validation/run_plan_collection.sh`, and thin `validation/run_engine_queries.py`.
- Added 32 uniform case-local `run_engine_queries.py` shims for already converted v2 cases only.
- Updated 32 manifests to include `validation.run_engine_queries`.
- Replaced 32 target shell wrappers with thin pass-through wrappers that delegate to the local shim and shared fail-closed runner.
- Created shared fail-closed runner modules under `src/sql_rewrite_bench/validation/`.
- Updated the static v2 resolver and tests so the three-file contract is required and copied per-case engine implementation markers are rejected.
- Updated validation and case-package spec drafts to document the three-file thin-entrypoint contract.
- Did not modify Wave C cases, `case_sets/`, inventory, reports/results, denominators, paper results, official metrics, DB/checker execution, or leaderboard outputs.

Files created:
- `src/sql_rewrite_bench/validation/__init__.py`
- `src/sql_rewrite_bench/validation/engine_query_runner.py`
- `src/sql_rewrite_bench/validation/plan_collection_runner.py`
- 32 target `validation/run_engine_queries.py` thin shims.
- `audits/case_package_v2_validation_contract_repair_v0/validation_contract_repair_summary.md`
- `audits/case_package_v2_validation_contract_repair_v0/validation_contract_case_status.csv`
- `audits/case_package_v2_validation_contract_repair_v0/validation_contract_manifest_update.csv`
- `audits/case_package_v2_validation_contract_repair_v0/validation_shared_runner_files.csv`
- `audits/case_package_v2_validation_contract_repair_v0/validation_contract_test_results.csv`
- `audits/case_package_v2_validation_contract_repair_v0/validation_contract_protected_boundary_checks.csv`
- `audits/case_package_v2_validation_contract_repair_v0/future_case_package_v2_wave_c_after_validation_contract_prompt.md`
- `audits/case_package_v2_validation_contract_repair_v0/validation_contract_repair_summary.json`
- `audits/case_package_v2_validation_contract_repair_v0/validation_contract_repair_command_log.md`

Files modified:
- 32 target `manifest.yaml` files, validation sections only.
- 32 target `validation/run_validation.sh` wrappers.
- 32 target `validation/run_plan_collection.sh` wrappers.
- `src/sql_rewrite_bench/case_package_v2_resolver.py`
- `tests/case_package_v2/test_case_package_v2_resolver.py`
- `repository_spec/validation_entrypoint_policy_v1_draft.md`
- `repository_spec/case_package_contract_v2_draft.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- 32/32 target v2 static validators passed.
- Unit tests passed: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`, 19 tests.
- JSON assertion passed.
- `git diff --check` passed.
- Boundary checks confirmed no Wave C case changes, no `case_sets/`, inventory, reports/results, denominator, paper-result, official-metric, DB/checker execution, case-local runs restoration, evidence/cases restoration, old validation script restoration, or leaderboard changes.

Task result:
- Validation contract repair: yes.
- Three-file validation contract adopted: yes.
- Target cases count: 32.
- Target cases updated: 32.
- Wave C cases modified: no.
- Shared runner files created: 3.
- `run_engine_queries.py` shims added: 32.
- Manifests updated: 32.
- Validator updated: yes.
- Tests updated: yes.
- DB/checker execution run: no.
- Official metrics computed: no.
- Reports/results changed: no.
- Denominator/paper results changed: no.
- `case_sets/` changed: no.
- Inventory changed: no.
- Global leaderboard created: no.

Next safe action:
- Run a read-only post-repair validation contract review for the 32 converted cases, or authorize the first Wave C writable conversion subwave using the repaired three-file validation contract, starting with `PORT_0005` only.

### 2026-05-20 · case_package_v2_common_core40_wave_c_subwave_1_port0005_v0

Branch: `feature/case-package-v2-external-schema`
Mode: branch-only bounded writable Wave C subwave conversion; `PORT_0005` only; no DB/checker execution; no official metrics
Legacy repo modified: no
Release repo branch modified: yes, `PORT_0005`, `schemas/parrot_bird_port0005_v0/`, audit/project-control files only

Summary:
- Converted exactly `PORT_0005` to clean-template-minimal v2 using the repaired semantic manifest contract and repaired three-file validation contract.
- Preserved `cases/PORT/PORT_0005/sql/dialect_variants/spark/` as an optional semantic PORT asset.
- Created per-case external schema package `schemas/parrot_bird_port0005_v0/` by copy-first extraction from case-local DDL/load files.
- Removed only `PORT_0005` v1 compatibility surfaces after reference repair: nested SQL positive/negative dirs, case-local engine schema dirs, case-local evidence, metadata, notes, data, and legacy engine-specific validation scripts.
- Updated `PORT_0005` manifest, README, checker configs, schema profile, validation entrypoints, and witness profile.
- Did not convert or modify other Wave C cases.
- Did not modify already converted pilot, Wave A, or Wave B cases except read-only validator checks.
- Did not modify `case_sets/`, inventory, reports/results, denominator values, paper results, official metrics, DB/checker execution, or leaderboard outputs.

Files created:
- `schemas/parrot_bird_port0005_v0/schema_profile.yaml`
- `schemas/parrot_bird_port0005_v0/postgres/ddl.sql`
- `schemas/parrot_bird_port0005_v0/postgres/load.sql`
- `schemas/parrot_bird_port0005_v0/mysql/ddl.sql`
- `schemas/parrot_bird_port0005_v0/mysql/load.sql`
- `schemas/parrot_bird_port0005_v0/spark/ddl.sql`
- `schemas/parrot_bird_port0005_v0/spark/load.sql`
- `cases/PORT/PORT_0005/sql/pos_01.sql`
- `cases/PORT/PORT_0005/sql/neg_01.sql`
- `cases/PORT/PORT_0005/validation/run_validation.sh`
- `cases/PORT/PORT_0005/validation/run_plan_collection.sh`
- `cases/PORT/PORT_0005/validation/run_engine_queries.py`
- `cases/PORT/PORT_0005/witness/witness_profile.yaml`
- `audits/case_package_v2_common_core40_wave_c_subwave_1_port0005_v0/port0005_conversion_summary.md`
- `audits/case_package_v2_common_core40_wave_c_subwave_1_port0005_v0/port0005_manifest_consistency_audit.csv`
- `audits/case_package_v2_common_core40_wave_c_subwave_1_port0005_v0/port0005_dialect_variant_retention.csv`
- `audits/case_package_v2_common_core40_wave_c_subwave_1_port0005_v0/port0005_schema_conversion_results.csv`
- `audits/case_package_v2_common_core40_wave_c_subwave_1_port0005_v0/port0005_cleanup_deletions_manifest.csv`
- `audits/case_package_v2_common_core40_wave_c_subwave_1_port0005_v0/port0005_validator_results.csv`
- `audits/case_package_v2_common_core40_wave_c_subwave_1_port0005_v0/port0005_protected_boundary_checks.csv`
- `audits/case_package_v2_common_core40_wave_c_subwave_1_port0005_v0/future_case_package_v2_wave_c_port0005_post_conversion_review_prompt.md`
- `audits/case_package_v2_common_core40_wave_c_subwave_1_port0005_v0/port0005_conversion_summary.json`
- `audits/case_package_v2_common_core40_wave_c_subwave_1_port0005_v0/port0005_conversion_command_log.md`

Files deleted:
- `PORT_0005` nested SQL compatibility dirs: `sql/positives/`, `sql/negatives/`.
- `PORT_0005` case-local engine schema dirs: `schema/postgres/`, `schema/mysql/`, `schema/spark/`.
- `PORT_0005` case-local `evidence/`, `metadata/`, `notes/`, and `data/` directories.
- `PORT_0005` legacy engine-specific validation scripts.

Validation:
- `PYTHONPATH=src python scripts/dev/validate_case_package_v2_refs.py --case cases/PORT/PORT_0005`: passed.
- Static validators for all 32 previously converted cases: passed.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`: passed, 19 tests.
- Summary JSON assertion: passed.
- CSV parse/header checks: passed.
- `git diff --check`: passed.
- Boundary checks confirmed only `PORT_0005` changed under `cases/`, no other Wave C case changes, no pilot/Wave A/Wave B case changes, no `case_sets/`, inventory, reports/results, denominator, paper-result, official-metric, DB/checker execution, `evidence/cases/`, or leaderboard changes.

Task result:
- Wave C subwave 1 PORT_0005 conversion: yes.
- Converted case ID: `PORT_0005`.
- Deferred: no.
- Clean-template-minimal achieved: yes.
- Dialect variants retained: yes.
- Manifest consistency passed: yes.
- Validation three-file contract passed: yes.
- Schema created/reused: `parrot_bird_port0005_v0`.
- Case files modified: yes.
- Schemas modified: yes.
- `evidence/cases/` created: no.
- `case_sets/` changed: no.
- Inventory changed: no.
- Reports/results changed: no.
- Denominator/paper results changed: no.
- Official metrics computed: no.
- DB/checker execution run: no.
- Global leaderboard created: no.

Next safe action:
- Run `case_package_v2_wave_c_port0005_post_conversion_review_v0` as a read-only parity review for `PORT_0005`, then proceed to the next precleared Wave C subwave only if the review passes.

### 2026-05-20 · case_package_v2_wave_c_port0005_post_conversion_review_v0

Branch: `feature/case-package-v2-external-schema`
Mode: branch-only read-only post-conversion review for `PORT_0005`; no further Wave C conversion; no DB/checker execution; no official metrics
Legacy repo modified: no
Release repo branch modified: yes, audit/project-control files only

Summary:
- Reviewed `PORT_0005` after the bounded Wave C subwave conversion.
- Confirmed the v2 validator passes for `PORT_0005`.
- Confirmed clean-template-minimal case-local structure: `README.md`, `manifest.yaml`, direct SQL files, retained `sql/dialect_variants/spark/`, `schema/schema_profile.yaml`, checker YAML configs, three validation entrypoints, and optional witness profile.
- Confirmed forbidden compatibility surfaces are absent: case-local `evidence/`, `runs/`, `metadata/`, `notes/`, `data/`, case-local schema engine dirs, old engine-specific validation scripts, per-case checker scripts, and `__pycache__/`.
- Confirmed the semantic manifest contract is present, with object-form SQL rewrite metadata, schema profile/external profile fields, source-as-oracle witness policy, regeneration-first evidence policy, and no mandatory static `evidence_ref`.
- Confirmed `schemas/parrot_bird_port0005_v0/schema_profile.yaml` exists and case-local schema engine dirs remain absent.
- Confirmed dialect variants are retained as optional semantic PORT v2 assets, not blockers.
- Ran static validator regression checks for all 32 previously converted pilot/Wave A/Wave B cases; all passed.
- Did not modify any case package or schema in this review.
- Did not modify `case_sets/`, inventory, reports/results, denominators, paper results, official metrics, DB/checker execution, or leaderboard outputs.

Validation:
- `PYTHONPATH=src python scripts/dev/validate_case_package_v2_refs.py --case cases/PORT/PORT_0005`: passed.
- Static validators for all 32 previously converted cases: passed.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`: passed, 19 tests.
- Summary JSON assertion: passed.
- CSV parse/header checks: passed.
- `git diff --check`: passed.

Task result:
- PORT_0005 post-conversion review: yes.
- Case reviewed: `PORT_0005`.
- Validator passed: yes.
- Clean-template-minimal passed: yes.
- Manifest consistency passed: yes.
- Dialect variants retained: yes.
- Validation three-file contract passed: yes.
- Ready for next Wave C subwave: yes.
- Case files modified: no.
- Schemas modified: no.
- `case_sets/` changed: no.
- Inventory changed: no.
- Reports/results changed: no.
- Denominator/paper results changed: no.
- Official metrics computed: no.
- DB/checker execution run: no.
- Global leaderboard created: no.

Next safe action:
- Authorize a bounded writable next Wave C subwave for precleared remaining PORT cases, preferably `PORT_0008`, `PORT_0012`, `PORT_0022`, `PORT_0024`, and `PORT_0025`, while preserving dialect variants where present and keeping all protected surfaces unchanged.

### 2026-05-20 · case_package_v2_common_core40_wave_c_subwave_2_remaining_ports_v0

Branch: `feature/case-package-v2-external-schema`
Mode: branch-only bounded writable Wave C subwave conversion; target five PORT cases only; no DB/checker execution; no official metrics
Legacy repo modified: no
Release repo branch modified: yes, target five PORT cases, corresponding external schema packages, audit/project-control files only

Summary:
- Converted exactly `PORT_0008`, `PORT_0012`, `PORT_0022`, `PORT_0024`, and `PORT_0025` to clean-template-minimal v2.
- Did not convert or modify `PORT_0004`, `PORT_0013`, `PORT_0005`, pilot cases, Wave A cases, or Wave B cases.
- Created direct `sql/pos_01.sql` and `sql/neg_01.sql` paths from existing nested rewrite SQL before deleting nested compatibility dirs.
- Created per-case external schema packages: `parrot_bird_port0008_v0`, `parrot_bird_port0012_v0`, `parrot_bird_port0022_v0`, `parrot_bird_port0024_v0`, and `parrot_bird_port0025_v0`.
- Removed target-case local schema engine dirs after copy-first external schema verification.
- Repaired target manifests to the semantic v2 contract using recovered/precleared provenance and explicit non-blocking draft-origin caveats where needed.
- Repaired checker configs to config-only direct SQL paths and regeneration-first evidence policy.
- Adopted the repaired three-file validation contract in all five target cases.
- Added source-as-oracle witness profiles and regeneration-first `evidence_policy`.
- Removed target-case compatibility surfaces: nested SQL dirs, case-local engine schema dirs, case-local static evidence, metadata, notes, data, legacy validation scripts, and legacy migration pilot notes.
- Did not create `evidence/cases/`.
- Did not modify `case_sets/`, inventory, reports/results, denominator values, paper results, official metrics, DB/checker execution, or leaderboard outputs.

Validation:
- Static validators for `PORT_0008`, `PORT_0012`, `PORT_0022`, `PORT_0024`, and `PORT_0025`: passed.
- Static validators for all already converted pilot, Wave A, Wave B, and `PORT_0005` cases: passed.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`: passed, 19 tests.
- Summary JSON assertion: passed.
- CSV parse/header checks: passed.
- Boundary checks confirmed no `PORT_0004`, `PORT_0013`, `PORT_0005`, pilot, Wave A, Wave B, `case_sets/`, inventory, reports/results, denominator, paper-result, official-metric, DB/checker execution, `evidence/cases/`, or leaderboard changes.
- `git diff --check`: passed.

Task result:
- Wave C subwave 2 remaining PORT conversion: yes.
- Target case IDs: `PORT_0008`, `PORT_0012`, `PORT_0022`, `PORT_0024`, and `PORT_0025`.
- Converted case IDs: all five.
- Deferred case IDs: none.
- Clean-template-minimal cases count: 5.
- Manifest consistency passed: yes.
- Validation three-file contract passed: yes.
- Schemas created/reused: `parrot_bird_port0008_v0`, `parrot_bird_port0012_v0`, `parrot_bird_port0022_v0`, `parrot_bird_port0024_v0`, and `parrot_bird_port0025_v0`.
- Case files modified: yes.
- Schemas modified: yes.
- `evidence/cases/` created: no.
- `case_sets/` changed: no.
- Inventory changed: no.
- Reports/results changed: no.
- Denominator/paper results changed: no.
- Official metrics computed: no.
- DB/checker execution run: no.
- Global leaderboard created: no.

Next safe action:
- Run `case_package_v2_common_core40_wave_c_subwave2_post_conversion_review_v0` as a read-only parity review for the five converted subwave 2 PORT cases before authorizing the final dialect-variant Wave C subwave for `PORT_0004` and `PORT_0013`.

### 2026-05-20 · case_package_v2_common_core40_wave_c_subwave2_post_conversion_review_v0

Branch: `feature/case-package-v2-external-schema`
Mode: branch-only read-only post-conversion review for Wave C subwave 2; no further conversion; no DB/checker execution; no official metrics
Legacy repo modified: no
Release repo branch modified: yes, audit/project-control files only

Summary:
- Reviewed exactly `PORT_0008`, `PORT_0012`, `PORT_0022`, `PORT_0024`, and `PORT_0025` after the Wave C subwave 2 conversion.
- Confirmed the static v2 validator passes for all five reviewed cases.
- Confirmed clean-template-minimal case-local structure for all five reviewed cases.
- Confirmed repaired semantic manifest contract, object-form SQL metadata, profile-first schema contract, checker config-only paths, source-as-oracle witness policy, regeneration-first `evidence_policy`, and three-file validation contract.
- Confirmed forbidden compatibility paths are absent: case-local `evidence/`, `runs/`, `metadata/`, `notes/`, `data/`, case-local schema engine dirs, old engine-specific validation scripts, per-case checker scripts, and `__pycache__/`.
- Confirmed external schema profiles resolve for `parrot_bird_port0008_v0`, `parrot_bird_port0012_v0`, `parrot_bird_port0022_v0`, `parrot_bird_port0024_v0`, and `parrot_bird_port0025_v0`.
- Confirmed shell validation wrappers do not call old engine scripts, require case-local schema engine dirs, or write case-local `runs/`.
- Ran static validator regression checks for all already converted pilot, Wave A, Wave B, and `PORT_0005` cases; all passed.
- Did not modify any case package or schema in this review.
- Did not modify `case_sets/`, inventory, reports/results, denominators, paper results, official metrics, DB/checker execution, `evidence/cases/`, or leaderboard outputs.

Validation:
- Static validators for `PORT_0008`, `PORT_0012`, `PORT_0022`, `PORT_0024`, and `PORT_0025`: passed.
- Static validators for all already converted pilot, Wave A, Wave B, and `PORT_0005` cases: passed.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`: passed, 19 tests.
- Summary JSON assertion: passed.
- CSV parse/header checks: passed.
- Protected-surface diff check for `cases`, `schemas`, `case_sets`, inventory, reports/results, and `evidence/cases`: passed with no output.
- `git diff --check`: passed.

Task result:
- Wave C subwave 2 post-conversion review: yes.
- Reviewed case IDs: `PORT_0008`, `PORT_0012`, `PORT_0022`, `PORT_0024`, and `PORT_0025`.
- Validator passed count: 5.
- Clean-template-minimal passed count: 5.
- Manifest consistency passed: yes.
- Validation three-file contract passed: yes.
- Ready for final dialect-variant PORT cases: yes.
- Case files modified: no.
- Schemas modified: no.
- `case_sets/` changed: no.
- Inventory changed: no.
- Reports/results changed: no.
- Denominator/paper results changed: no.
- Official metrics computed: no.
- DB/checker execution run: no.
- Global leaderboard created: no.

Next safe action:
- Authorize a bounded writable final Wave C dialect-variant PORT conversion for `PORT_0004` and `PORT_0013`, preserving existing `sql/dialect_variants/` as semantic v2 assets and keeping all protected surfaces unchanged.

### 2026-05-20 · case_package_v2_common_core40_wave_c_final_dialect_ports_v0

Branch: `feature/case-package-v2-external-schema`
Mode: branch-only bounded writable final Wave C dialect-variant PORT conversion; target two PORT cases only; no DB/checker execution; no official metrics
Legacy repo modified: no
Release repo branch modified: yes, `PORT_0004`, `PORT_0013`, corresponding external schema packages, audit/project-control files only

Summary:
- Converted exactly `PORT_0004` and `PORT_0013` to clean-template-minimal v2.
- Did not convert or modify `PORT_0005`, Wave C subwave 2 cases, pilot cases, Wave A cases, or Wave B cases.
- Preserved existing Spark dialect variants under both target case-local `sql/dialect_variants/spark/` directories and recorded them as optional semantic PORT v2 assets.
- Created direct `sql/pos_01.sql` and `sql/neg_01.sql` paths from existing nested rewrite SQL before deleting nested compatibility dirs.
- Created per-case external schema packages: `parrot_bird_port0004_v0` and `parrot_bird_port0013_v0`.
- Removed target-case local schema engine dirs after copy-first external schema verification.
- Repaired target manifests to the semantic v2 contract using recovered/precleared provenance and explicit non-blocking caveats where needed.
- Repaired checker configs to config-only direct SQL paths and regeneration-first evidence policy.
- Adopted the repaired three-file validation contract in both target cases.
- Added source-as-oracle witness profiles and regeneration-first `evidence_policy`.
- Removed target-case compatibility surfaces: nested SQL dirs, case-local engine schema dirs, case-local static evidence, metadata, notes, data, legacy validation scripts, and legacy sidecar files.
- Did not create `evidence/cases/`.
- Did not modify `case_sets/`, inventory, reports/results, denominator values, paper results, official metrics, DB/checker execution, or leaderboard outputs.

Validation:
- Static validators for `PORT_0004` and `PORT_0013`: passed.
- Static validators for all already converted pilot, Wave A, Wave B, `PORT_0005`, and Wave C subwave 2 cases: passed.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`: passed, 19 tests.
- Summary JSON assertion: passed.
- CSV parse/header checks: passed.
- Dialect variant retention checks passed for `PORT_0004` and `PORT_0013`.
- Boundary checks confirmed no other PORT, pilot, Wave A, Wave B, `case_sets/`, inventory, reports/results, denominator, paper-result, official-metric, DB/checker execution, `evidence/cases/`, or leaderboard changes.

Task result:
- Final Wave C dialect PORT conversion: yes.
- Target case IDs: `PORT_0004`, `PORT_0013`.
- Converted case IDs: both.
- Deferred case IDs: none.
- Clean-template-minimal cases count: 2.
- Dialect variants retained: yes.
- Manifest consistency passed: yes.
- Validation three-file contract passed: yes.
- Schemas created/reused: `parrot_bird_port0004_v0` and `parrot_bird_port0013_v0`.
- Case files modified: yes.
- Schemas modified: yes.
- `evidence/cases/` created: no.
- `case_sets/` changed: no.
- Inventory changed: no.
- Reports/results changed: no.
- Denominator/paper results changed: no.
- Official metrics computed: no.
- DB/checker execution run: no.
- Global leaderboard created: no.

Next safe action:
- Run a read-only Common-core 40 v2 final closeout covering all converted Common-core v2 cases, with special checks for retained PORT dialect variants in `PORT_0003`, `PORT_0004`, `PORT_0005`, and `PORT_0013`.

### 2026-05-20 · case_package_v2_common_core40_final_closeout_v0

Branch: `feature/case-package-v2-external-schema`
Mode: branch-only read-only Common-core 40 v2 final closeout; no case conversion; no cleanup execution; no DB/checker execution; no official metrics
Legacy repo modified: no
Release repo branch modified: yes, audit/project-control files only

Summary:
- Reviewed all 40 Common-core v0 cases after pilot, Wave A, Wave B, Wave C PORT conversions, semantic manifest repair, validation three-file contract repair, evidence-policy migration, and clean-template cleanup.
- Ran the static v2 validator for all 40 Common-core cases; all passed.
- Confirmed manifest semantic contract pass for all 40 cases.
- Confirmed validation three-file contract pass for all 40 cases.
- Confirmed schema external profiles resolve for all 40 cases and case-local schema engine dirs are absent.
- Confirmed regeneration-first `evidence_policy` for all 40 cases and did not create `evidence/cases/`.
- Confirmed retained dialect variants for `PORT_0003`, `PORT_0004`, `PORT_0005`, and `PORT_0013`; dialect variants are semantic optional PORT assets and were not deleted.
- Found clean-template-minimal blockers in five pilot cases: `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.
- Remaining blockers are 15 forbidden path entries: each blocked pilot still has `notes/`, `sql/positives/`, and `sql/negatives/`.
- Recorded `PERF_0077` and `PERF_0082` source-path caveats as separate follow-up items. They do not block case-package validator pass, but they do block final public source-path closeout.
- Did not modify any case package or schema in this read-only audit.
- Did not modify `case_sets/`, inventory, reports/results, denominators, paper results, official metrics, DB/checker execution, or leaderboard outputs.

Validation:
- Static v2 validators for all 40 Common-core cases: passed.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`: passed, 19 tests.
- Summary JSON assertion: passed.
- CSV parse/header checks: passed.
- `git diff --check`: passed.

Task result:
- Common-core 40 final closeout: yes, audit completed with blockers.
- Common-core cases reviewed: 40.
- Validators passed count: 40.
- Clean-template-minimal passed count: 35.
- Manifest semantic contract passed count: 40.
- Validation three-file contract passed count: 40.
- Dialect variant cases retained: `PORT_0003`, `PORT_0004`, `PORT_0005`, and `PORT_0013`.
- Remaining blockers count: 15 path entries across five pilot cases.
- `PERF_0077`/`PERF_0082` follow-up required: yes.
- Ready for release closeout after source-path follow-up: no, because structural pilot cleanup blockers remain.
- Case files modified: no.
- Schemas modified: no.
- `case_sets/` changed: no.
- Inventory changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Official metrics computed: no.
- DB/checker execution run: no.
- Global leaderboard created: no.

Next safe action:
- Run a narrow writable cleanup for leftover empty pilot compatibility directories (`notes/`, `sql/positives/`, and `sql/negatives/`) in `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`; rerun this final closeout; then perform the `PERF_0077`/`PERF_0082` source-path provenance follow-up before public release closeout.

### 2026-05-20 · case_package_v2_pilot_leftover_compat_dirs_cleanup_v0

Branch: `feature/case-package-v2-external-schema`
Mode: branch-only narrow writable cleanup for five pilot cases; no case conversion; no DB/checker execution; no official metrics
Legacy repo modified: no
Release repo branch modified: yes, directory-only cleanup under five pilot case paths plus audit/project-control files

Summary:
- Cleaned exactly the leftover pilot compatibility directory blockers reported by `case_package_v2_common_core40_final_closeout_v0`.
- Target cases: `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.
- Candidate directories checked: 15.
- Deleted 15 empty directories: `notes/`, `sql/positives/`, and `sql/negatives/` for each target case.
- Skipped directories: 0.
- Confirmed every candidate directory was empty before deletion.
- Confirmed no live target case-local references to `notes/`, `sql/positives/`, or `sql/negatives/`.
- Confirmed direct `sql/pos_01.sql` and `sql/neg_01.sql` replacements exist for every target case.
- Did not delete or modify `PORT_0003/sql/dialect_variants/`.
- Did not modify schemas, `case_sets/`, inventory, reports/results, denominator values, paper results, official metrics, DB/checker execution, `evidence/cases/`, or leaderboard outputs.

Validation:
- Static validators for the five target pilot cases: passed.
- Static validators for all 40 Common-core cases: passed.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`: passed, 19 tests.
- Summary JSON assertion: passed.
- `git diff --check`: passed.

Task result:
- Pilot leftover compatibility dirs cleanup: yes.
- Target case IDs: `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.
- Candidate dirs checked: 15.
- Dirs deleted count: 15.
- Dirs skipped count: 0.
- Case files modified: yes, directory-only cleanup under target case paths; no tracked case file content changed.
- Schemas modified: no.
- `case_sets/` changed: no.
- Inventory changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Official metrics computed: no.
- DB/checker execution run: no.
- Global leaderboard created: no.
- `evidence/cases/` created: no.
- Dialect variants deleted: no.

Next safe action:
- Rerun the read-only Common-core 40 v2 final closeout. If clean-template-minimal passes for all 40 cases, perform the separate `PERF_0077`/`PERF_0082` source-path provenance follow-up before public release closeout.

### 2026-05-20 · case_package_v2_common_core40_final_closeout_rerun_v0

Branch: `feature/case-package-v2-external-schema`
Mode: branch-only read-only Common-core 40 v2 final closeout rerun; no case conversion; no cleanup execution; no source-path provenance follow-up; no DB/checker execution; no official metrics
Legacy repo modified: no
Release repo branch modified: yes, audit/project-control files only

Summary:
- Reran the Common-core 40 v2 final closeout after `case_package_v2_pilot_leftover_compat_dirs_cleanup_v0`.
- Reviewed all 40 Common-core v0 cases.
- Confirmed static validators pass for all 40 cases.
- Confirmed clean-template-minimal passes for all 40 cases after the 15 leftover empty pilot compatibility directories were removed.
- Confirmed manifest semantic contract passes for all 40 cases.
- Confirmed validation three-file contract passes for all 40 cases.
- Confirmed retained dialect variants for `PORT_0003`, `PORT_0004`, `PORT_0005`, and `PORT_0013` remain present and are treated as semantic optional PORT assets, not blockers.
- Confirmed regeneration-first `evidence_policy` for all 40 cases and did not create `evidence/cases/`.
- Confirmed schema external profiles resolve for all 40 cases and case-local schema engine dirs are absent.
- Recorded `PERF_0077` and `PERF_0082` source-path caveats as the remaining separate provenance follow-up. These do not block Common-core 40 v2 case-package closeout, but do block final public source-path closeout until resolved or explicitly closed.
- Did not modify any case package or schema in this read-only rerun.
- Did not modify `case_sets/`, inventory, reports/results, denominators, paper results, official metrics, DB/checker execution, or leaderboard outputs.

Validation:
- Static v2 validators for all 40 Common-core cases: passed.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`: passed, 19 tests.
- Summary JSON assertion: passed.
- CSV parse/header checks: passed.
- `git diff --check`: passed.

Task result:
- Common-core 40 final closeout rerun: yes.
- Common-core cases reviewed: 40.
- Validators passed count: 40.
- Clean-template-minimal passed count: 40.
- Manifest semantic contract passed count: 40.
- Validation three-file contract passed count: 40.
- Dialect variant cases retained: `PORT_0003`, `PORT_0004`, `PORT_0005`, and `PORT_0013`.
- Remaining blockers count: 0.
- `PERF_0077`/`PERF_0082` follow-up required: yes.
- Ready for release closeout after source-path follow-up: yes.
- Case files modified: no.
- Schemas modified: no.
- `case_sets/` changed: no.
- Inventory changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Official metrics computed: no.
- DB/checker execution run: no.
- Global leaderboard created: no.

Next safe action:
- Run the narrow `PERF_0077`/`PERF_0082` source-path provenance follow-up. After it resolves or explicitly closes those source-path caveats, proceed to final public-release closeout planning.

### 2026-05-20 · Pilot public-facing case README template on 4 representative Common-core cases

Mode: README documentation pilot only; no case conversion; no cleanup execution; no source-path provenance follow-up; no DB/checker execution; no official metrics
Legacy repo modified: no
Release repo modified: yes

Summary:
- Applied the maintainer-approved public-facing case README template to exactly four representative Common-core case packages: `PERF_0006`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.
- Used each target case manifest as the source of truth for source family, rewrite opportunity, semantic or portability risk, hard-negative presence, and dialect-variant presence.
- Removed construction-history wording from the four README bodies and reframed each README as a stable public benchmark case-package guide.
- Did not modify manifests, schema profiles, checker files, validation files, SQL files, case sets, inventory, reports/results, denominator files, paper-facing results, raw evidence, scripts, tests, benchmark specs, repository specs, `MIGRATION_MASTER_PLAN.md`, or `DECISION_LOG.md`.
- Did not run DB/checker execution, compute official metrics, render paper outputs, or create a leaderboard.

Files created:
- None.

Files modified:
- `cases/PERF/PERF_0006/README.md`
- `cases/CONS/CONS_0005/README.md`
- `cases/PORT/PORT_0003/README.md`
- `cases/LONGTAIL/LONGTAIL_0011/README.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- `git diff --check`: passed.
- Banned internal-term grep over the four target README files: no matches.
- Template-placeholder grep over the four target README files: no matches.
- Static v2 validators for the four target case packages: passed.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`: passed, 19 tests.

Commit hash:
- `fd233cf` (`docs(cases): pilot public-facing case README template`)

Push result:
- Pushed to `origin/feature/case-package-v2-external-schema` (`3c26a51..fd233cf`).

Task result:
- Public-facing case README pilot: yes.
- Target README files modified: four.
- Non-README case files modified: no.
- Manifest/schema/checker/validation/sql files modified: no.
- `case_sets/` changed: no.
- Inventory changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Official metrics computed by this task: no.
- DB/checker execution run by this task: no.
- Global leaderboard created: no.

Next safe action:
- Human review of the four pilot READMEs. If accepted, authorize a separate README-only batch for all Common-core 40 cases.

### 2026-05-20 · Patch four pilot public case READMEs with SQL pattern overview

Mode: README-only pilot patch; no case conversion; no cleanup execution; no source-path provenance follow-up; no DB/checker execution; no official metrics
Legacy repo modified: no
Release repo modified: yes

Summary:
- Added a short `## SQL pattern overview` section to exactly four representative Common-core public-facing case READMEs: `PERF_0006`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.
- Used each target case manifest and direct SQL files as source material for the source-query, reference-rewrite, checker-control, or portability-focus bullets.
- Did not modify manifests, schema profiles, checker files, validation files, SQL files, case sets, inventory, reports/results, denominator files, paper-facing results, raw evidence, scripts, tests, benchmark specs, repository specs, `MIGRATION_MASTER_PLAN.md`, or `DECISION_LOG.md`.
- Did not run DB/checker execution, compute official metrics, render paper outputs, parse retained evidence, or create a leaderboard.

Files created:
- None.

Files modified:
- `cases/PERF/PERF_0006/README.md`
- `cases/CONS/CONS_0005/README.md`
- `cases/PORT/PORT_0003/README.md`
- `cases/LONGTAIL/LONGTAIL_0011/README.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- `git diff --check`: passed.
- Banned internal-term grep over the four target README files: no matches.
- Template-placeholder grep over the four target README files: no matches.
- SQL pattern overview section count: exactly one section in each target README.
- Static v2 validators for the four target case packages: passed.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`: passed, 19 tests.

Commit hash:
- `fa8f55e` (`docs(cases): add SQL pattern overview to README pilot`)

Push result:
- Pushed to `origin/feature/case-package-v2-external-schema` (`bbb11a4..fa8f55e`).

Task result:
- SQL pattern overview README pilot patch: yes.
- Target README files modified: four.
- Non-README case files modified: no.
- Manifest/schema/checker/validation/sql files modified: no.
- `case_sets/` changed: no.
- Inventory changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Official metrics computed by this task: no.
- DB/checker execution run by this task: no.
- Global leaderboard created: no.

Next safe action:
- Human review of the four patched pilot READMEs. If accepted, authorize a separate README-only batch for all Common-core 40 cases using the finalized public README template.

### 2026-05-20 · Pilot README Markdown structure cleanup

Mode: formatting-only README patch; no case conversion; no case content change; no DB/checker execution; no official metrics
Legacy repo modified: no
Release repo modified: yes

Summary:
- Reformatted exactly four representative Common-core public-facing case READMEs: `PERF_0006`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.
- Kept case content, SQL pattern descriptions, benchmark boundaries, package file references, and interpretation boundaries unchanged.
- Normalized Markdown readability by keeping headings on their own lines, preserving blank lines after headings, keeping bullets renderable, and splitting compressed long paragraphs into readable paragraphs.
- Did not modify manifests, schema profiles, checker files, validation files, SQL files, case sets, inventory, reports/results, denominator files, paper-facing results, raw evidence, scripts, tests, benchmark specs, repository specs, `MIGRATION_MASTER_PLAN.md`, or `DECISION_LOG.md`.
- Did not run DB/checker execution, compute official metrics, render paper outputs, parse retained evidence, or create a leaderboard.

Files created:
- None.

Files modified:
- `cases/PERF/PERF_0006/README.md`
- `cases/CONS/CONS_0005/README.md`
- `cases/PORT/PORT_0003/README.md`
- `cases/LONGTAIL/LONGTAIL_0011/README.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- `git diff --check`: passed.
- Exact heading-count grep for the required seven README headings in each target README: passed.
- Banned internal-term grep over the four target README files: no matches.
- Template-placeholder grep over the four target README files: no matches.
- Static v2 validators for the four target case packages: passed.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`: passed, 19 tests.

Commit hash:
- `726f598` (`docs(cases): fix pilot README markdown structure`)

Push result:
- Pushed to `origin/feature/case-package-v2-external-schema` (`39a0dfb..726f598`).

Task result:
- Pilot README Markdown structure cleanup: yes.
- Target README files modified: four.
- Non-README case files modified: no.
- Manifest/schema/checker/validation/sql files modified: no.
- `case_sets/` changed: no.
- Inventory changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Official metrics computed by this task: no.
- DB/checker execution run by this task: no.
- Global leaderboard created: no.

Next safe action:
- Human review of the formatted four pilot READMEs. If accepted, authorize a separate README-only batch for all Common-core 40 cases using the finalized public README template.

### 2026-05-20 · Apply finalized public-facing case README template to all Common-core 40 cases

Mode: README-only documentation batch; no case conversion; no cleanup execution; no source-path provenance follow-up; no DB/checker execution; no official metrics
Legacy repo modified: no
Release repo modified: yes

Summary:
- Applied the finalized public-facing case README template v1.1 to all 40 Common-core case README files listed in `case_sets/common_core_v0/cases.csv`.
- Confirmed the target count was exactly 40 before editing.
- Used each case manifest and direct SQL files as source material for public source-query, reference-rewrite, checker-control, or portability-focus summaries.
- Kept the four accepted pilot README files in the same public-facing structure and normalized the remaining 36 Common-core README files to match.
- Did not modify manifests, schema profiles, checker files, validation files, SQL files, case sets, inventory, reports/results, denominator files, paper-facing results, raw evidence, scripts, tests, benchmark specs, repository specs, `MIGRATION_MASTER_PLAN.md`, or `DECISION_LOG.md`.
- Did not run DB/checker execution, compute official metrics, render paper outputs, parse retained evidence, or create a leaderboard.

Files created:
- None.

Files modified:
- 40 Common-core case `README.md` files listed by `case_sets/common_core_v0/cases.csv`.
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- Common-core README target count: 40.
- `git diff --check`: passed.
- Banned internal-term grep over the 40 target README files: no matches.
- Template-placeholder grep over the 40 target README files: no matches.
- Required heading check: exactly one required heading set in each target README.
- Markdown compression check: passed.
- Static v2 validators for all 40 Common-core case packages: passed.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`: passed, 19 tests.

Commit hash:
- `b708627` (`docs(cases): normalize common-core public case READMEs`)

Push result:
- Pushed to `origin/feature/case-package-v2-external-schema` (`bbee477..b708627`).

Task result:
- Common-core public README batch: yes.
- README targets considered: 40.
- Non-README case files modified: no.
- Manifest/schema/checker/validation/sql files modified: no.
- `case_sets/` changed: no.
- Inventory changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Official metrics computed by this task: no.
- DB/checker execution run by this task: no.
- Global leaderboard created: no.

Next safe action:
- Human spot-check of the 40 public README batch, then run the narrow `PERF_0077`/`PERF_0082` source-path provenance follow-up before final public-release closeout planning.

### 2026-05-20 · Resolve narrow PERF_0077/PERF_0082 source-path provenance follow-up

Mode: narrow provenance follow-up; no README task; no case migration; no DB/checker execution; no official metrics; no release closeout
Legacy repo modified: no
Release repo modified: yes

Summary:
- Reviewed the two remaining Common-core source-path provenance caveats for `PERF_0077` and `PERF_0082`.
- Checked current manifests, current source SQL comments, deleted branch-history `metadata/provenance.yaml`, pre-v2 branch-history manifests, manifest caveat closeout outputs, Wave C follow-up records, final closeout rerun source-path records, `inventory/case_registry.csv`, `inventory/source_registry.csv`, and `case_sets/common_core_v0/cases.csv`.
- Confirmed branch-history provenance records `source_entry: ''` and `source_materialization: legacy case-local source.sql` for both cases.
- Did not infer precise paths from query text, JOB query identity comments, or draft markers.
- No exact source path or source-entry pointer was safely recovered for either case.
- Closed both cases as retained nonblocking source-path provenance uncertainty for public release closeout; no exact JOB source path is claimed.
- Did not modify manifests because no safe source-path field repair was supported by repository evidence.
- Did not modify README, SQL, schema, checker, validation, case-set, inventory, reports/results, denominator, paper-result, case-membership, or raw retained-evidence files.
- Did not run DB/checker execution, compute official metrics, render paper outputs, parse retained evidence, or create a leaderboard.

Files created:
- `audits/perf_0077_0082_source_path_followup_v0/README.md`
- `audits/perf_0077_0082_source_path_followup_v0/source_path_followup_summary.csv`
- `audits/perf_0077_0082_source_path_followup_v0/source_path_followup_summary.json`
- `audits/perf_0077_0082_source_path_followup_v0/command_log.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- `git diff --check`: passed.
- YAML parse check for both target manifests: passed.
- Audit summary JSON parse/assertion: passed.
- Audit summary CSV parse/header check: passed.
- Static v2 validators for `PERF_0077` and `PERF_0082`: passed.
- Static v2 validators for all 40 Common-core case packages: passed.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`: passed, 19 tests.
- Protected-surface diff check: passed.

Commit hash:
- `c0573cb` (`docs(provenance): close PERF source-path follow-up`)

Push result:
- Pushed to `origin/feature/case-package-v2-external-schema` (`0ec57aa..c0573cb`).

Task result:
- Target cases reviewed: `PERF_0077`, `PERF_0082`.
- Source-path repairs made: none.
- Remaining caveats: explicit nonblocking source-path provenance uncertainty retained for both cases; exact source paths are not claimed.
- Safe for public source-path closeout: yes, with retained nonblocking provenance uncertainty.
- README files modified: no.
- SQL/schema/checker/validation files modified: no.
- Manifest files modified: no.
- `case_sets/` changed: no.
- Inventory changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Official metrics computed by this task: no.
- DB/checker execution run by this task: no.
- Global leaderboard created: no.

Next safe action:
- Proceed to final public-release closeout planning, carrying the explicit note that `PERF_0077` and `PERF_0082` retain nonblocking source-path provenance uncertainty and no exact JOB source path is claimed.

### 2026-05-20 · Final public-release closeout planning audit

Mode: read-only planning/readiness audit; no release tag; no export branch; no history rewrite; no case-file changes; no metrics; no paper rendering; no global leaderboard
Legacy repo modified: no
Release repo modified: yes

Summary:
- Created a final public-release closeout planning packet under `audits/final_public_release_closeout_planning_v0/`.
- Reviewed Common-core 40 final closeout rerun, Common-core README batch project-control records, and the `PERF_0077`/`PERF_0082` source-path follow-up packet.
- Confirmed case-package readiness inputs: Common-core 40 closed out, all 40 public case READMEs normalized, semantic manifests and three-file validation contract closed out, dialect variants retained as semantic PORT assets, and `PERF_0077`/`PERF_0082` source-path caveats explicitly retained as nonblocking provenance uncertainty.
- Recorded release readiness verdict: blocked for actual public release/export because public release-surface gaps remain.
- Remaining blockers recorded: missing `LICENSE`, `CITATION.cff`, `CONTRIBUTING.md`, missing `benchmark_spec/`, missing or unauthorized curated `reports/` and `results/`, incomplete official metrics/paper rendering/reproduction and retained-evidence release-output flow, and no export branch or release tag.
- Did not modify cases, manifests, schemas, SQL, checker files, validation files, case sets, inventory, reports, results, benchmark specs, repository specs, scripts, tests, source files, or raw retained evidence.
- Did not compute official metrics, run DB/checker execution, render paper tables, create a leaderboard, create a release tag, or create an export branch.

Files created:
- `audits/final_public_release_closeout_planning_v0/README.md`
- `audits/final_public_release_closeout_planning_v0/release_readiness_matrix.csv`
- `audits/final_public_release_closeout_planning_v0/release_readiness_summary.json`
- `audits/final_public_release_closeout_planning_v0/remaining_gap_list.md`
- `audits/final_public_release_closeout_planning_v0/protected_surface_check.md`
- `audits/final_public_release_closeout_planning_v0/command_log.md`
- `audits/final_public_release_closeout_planning_v0/future_final_closeout_prompt.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- `release_readiness_summary.json` parse/assertion: passed.
- `release_readiness_matrix.csv` parse/header/count check: passed, 18 readiness dimensions.
- `git diff --check`: passed.
- Static v2 validators for all 40 Common-core case packages: passed.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`: passed, 19 tests.
- Protected-surface diff check: passed.

Commit hash:
- `2c3e57d` (`docs(release): add final public release closeout planning audit`)

Push result:
- Pushed to `origin/feature/case-package-v2-external-schema` (`ef5d87a..2c3e57d`).

Task result:
- Release readiness verdict: blocked.
- Remaining nonblocking caveats: `PERF_0077` and `PERF_0082` retain source-path provenance uncertainty; PORT dialect variants remain semantic assets.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Official metrics computed by this task: no.
- DB/checker execution run by this task: no.
- Global leaderboard created: no.

Next safe action:
- Complete missing public release-surface metadata/spec/reporting/reproduction/export readiness items in a separate bounded task, then rerun final public-release closeout before any release tag or export branch.

### 2026-05-20 · Audit user-entry and one-command reproduction compatibility after case-package changes

Mode: compatibility audit and lightweight smoke; no full paper reproduction CLI; no official metrics; no paper rendering; no reports/results update; no global leaderboard
Legacy repo modified: no
Release repo modified: yes

Summary:
- Audited current user-entry and reproduction prototype compatibility after Common-core 40 case-package normalization and public README normalization.
- Inspected module CLI, thin wrapper, optional SQLGlot adapter, user-entry docs, case selection, PostgreSQL execution helper, local checker, user-run schema constants, tests, CI workflows, packaging metadata, Common-core case-set metadata, and representative case-package paths.
- Confirmed Common-core v0 remains 40 cases with pool split 16 PERF / 9 CONS / 9 PORT / 6 LONGTAIL; same-engine denominator remains 120 rows; controls remain 360 rows.
- Confirmed selection remains metadata-driven through `case_sets/common_core_v0/` and all 40 Common-core rows resolve to existing `sql/source.sql`.
- Ran module CLI help, wrapper CLI help, and SQLGlot adapter help successfully.
- Ran two-case non-DB dry-run smoke over `PERF_0006` and `CONS_0005`: passed, selected_rows=2, candidate_generated_rows=0.
- Ran two-case non-DB dummy-adapter smoke over `PERF_0006` and `CONS_0005`: passed, selected_rows=2, candidate_generated_rows=2.
- Recorded and removed local smoke outputs under `runs/user/audit_user_entry_*`; removed unit-test local outputs under `runs/user/unittest_*`.
- Determined optional PostgreSQL DB/checker mode needs reorganization because it still expects case-local `schema/postgres/ddl.sql` and `schema/postgres/load.sql`, which are absent from normalized Common-core packages.
- Determined docs and behavior are partially aligned: non-DB path is documented and works, while optional DB/checker flags are exposed in CLI help but underdocumented and incompatible with external schema layout.
- Did not modify source code, tests, docs, README files, cases, manifests, schemas, checker files, validation files, SQL files, case sets, inventory, reports, results, benchmark specs, repository specs, workflows, denominator scaffolds, paper results, or raw retained evidence.
- Did not run DB/checker execution, compute official metrics, render paper tables, update retained evidence, update reports/results, or create a leaderboard.

Files created:
- `audits/user_entry_reproduction_compatibility_v0/README.md`
- `audits/user_entry_reproduction_compatibility_v0/entrypoint_inventory.csv`
- `audits/user_entry_reproduction_compatibility_v0/smoke_results.csv`
- `audits/user_entry_reproduction_compatibility_v0/compatibility_matrix.csv`
- `audits/user_entry_reproduction_compatibility_v0/gap_list.md`
- `audits/user_entry_reproduction_compatibility_v0/recommended_reorganization_plan.md`
- `audits/user_entry_reproduction_compatibility_v0/command_log.md`
- `audits/user_entry_reproduction_compatibility_v0/future_user_entry_repair_prompt.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- Audit CSV parse/header checks: passed.
- `git diff --check`: passed.
- Protected-surface diff check: passed.
- User-entry unit tests: passed, 27 tests with 1 skipped.
- Required smoke commands: passed.

Commit hash:
- `f978607` (`docs(audit): assess user-entry reproduction compatibility`)

Push result:
- Pushed to `origin/feature/case-package-v2-external-schema` (`d99cfc8..f978607`).

Task result:
- Non-DB dry-run smoke result: passed.
- Non-DB adapter-capture smoke result: passed.
- Optional DB/checker mode status: needs reorganization; not run.
- Documentation alignment verdict: partial.
- Full paper reproduction status: deferred/not implemented.
- Source code modified: no.
- Docs modified: no.
- Cases/manifests/schema/checker/validation/sql modified: no.
- `case_sets/` changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Official metrics computed by this task: no.
- DB/checker execution run by this task: no.
- Global leaderboard created: no.

Next safe action:
- Authorize a narrow user-entry repair task for external-schema-aware optional DB/checker diagnostics and public smoke-command polish, with full paper reproduction, official metrics, paper rendering, retained-evidence parsing, reports/results updates, and leaderboard output explicitly out of scope.

### 2026-05-20 · Repair user-entry external-schema compatibility and public smoke command

Mode: narrow user-entry repair; no full paper reproduction; no official metrics; no paper rendering; no reports/results update; no retained-evidence parsing; no global leaderboard
Legacy repo modified: no
Release repo modified: yes

Summary:
- Preserved the existing non-DB user-entry adapter-capture path.
- Added `--smoke` to select deterministic Common-core smoke cases `PERF_0006` and `CONS_0005` without a temporary case-list file.
- Added public example adapter `examples/user/noop_adapter.py` for smoke commands.
- Repaired optional PostgreSQL DB/checker diagnostic schema resolution to use manifest `schema.external_profile` and external profile `engines.postgres.ddl/load`.
- Added fail-closed behavior when external schema metadata or PostgreSQL schema assets are missing.
- Updated `docs/USER_BENCHMARK_GUIDE.md` to separate supported non-DB smoke, optional local PostgreSQL diagnostics, and deferred full paper reproduction/official metrics/reporting.
- Added/updated user-entry tests for smoke selection, runs/user output containment, external schema resolution, and fail-closed diagnostic behavior.
- Ran module help, wrapper help, public smoke dry-run, public smoke adapter-capture, user-entry unit tests, CSV checks, and `git diff --check`.
- Live DB/checker execution was not run.
- Removed local smoke and unit-test outputs under `runs/user/` after recording outcomes.
- Did not modify cases, manifests, SQL, schemas, checker files, validation files, case sets, inventory, reports, results, denominator scaffolds, paper results, raw retained evidence, `MIGRATION_MASTER_PLAN.md`, or `DECISION_LOG.md`.

Files created:
- `examples/user/noop_adapter.py`
- `audits/user_entry_external_schema_repair_v0/README.md`
- `audits/user_entry_external_schema_repair_v0/smoke_results.csv`
- `audits/user_entry_external_schema_repair_v0/external_schema_resolution_tests.md`
- `audits/user_entry_external_schema_repair_v0/protected_surface_check.md`
- `audits/user_entry_external_schema_repair_v0/command_log.md`

Files modified:
- `src/sql_rewrite_bench/case_selection.py`
- `src/sql_rewrite_bench/user_run.py`
- `src/sql_rewrite_bench/postgres_execution.py`
- `docs/USER_BENCHMARK_GUIDE.md`
- `tests/user_entry/test_case_selection.py`
- `tests/user_entry/test_db_checker_execution_mvp.py`
- `tests/user_entry/test_user_run_outputs.py`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --help`: passed.
- `python scripts/user/run_user_benchmark.py --help`: passed.
- Public smoke dry-run: passed, selected_rows=2, candidate_generated_rows=0.
- Public smoke adapter-capture: passed, selected_rows=2, candidate_generated_rows=2.
- User-entry unit tests: passed, 33 tests with 1 skipped.
- Audit CSV parse/header check: passed.
- `git diff --check`: passed.
- Protected-surface diff check: passed.

Commit hash:
- `b93f84a` (`feat(user-entry): repair external-schema smoke path`)

Push result:
- First push attempt failed with an SSH connection reset before repository update; retry succeeded to `origin/feature/case-package-v2-external-schema` (`5c0fd8d..b93f84a`).

Task result:
- Public smoke command added: yes.
- Public example adapter added: yes.
- Optional DB/checker external-schema compatibility: repaired.
- Live DB/checker execution run by this task: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Official metrics computed by this task: no.
- Paper tables rendered by this task: no.
- Global leaderboard created: no.

Next safe action:
- Human review of the repaired public smoke and external-schema-aware optional diagnostic path, then continue bounded release-surface metadata work without claiming full paper reproduction.

### 2026-05-20 · Rewrite top-level README as Chinese public entrypoint

Mode: documentation-only; no source-code changes; no case changes; no full paper reproduction; no official metrics; no paper rendering; no reports/results update; no global leaderboard
Legacy repo modified: no
Release repo modified: yes

Summary:
- Rewrote top-level `README.md` in Chinese as a concise public entrypoint for SQL-RewriteBench.
- Documented the current public scope: `Common-core v0` has 40 case packages, pool split 16 PERF / 9 CONS / 9 PORT / 6 LONGTAIL, and `Track A` same-engine evaluation has 120 planned rows over PostgreSQL, MySQL, and Spark SQL.
- Documented the safe public smoke path using `--smoke` and `examples/user/noop_adapter.py`.
- Documented the user adapter contract, optional local PostgreSQL diagnostics, case-package reading guidance, repository directory roles, and benchmark interpretation boundaries.
- Explicitly preserved the no-global-leaderboard boundary and stated that smoke outputs are local diagnostics only.
- Did not claim full paper reproduction, official metrics, report/result regeneration, global leaderboard creation, or exact JOB source paths for `PERF_0077` / `PERF_0082`.
- Did not modify source code, tests, examples, cases, manifests, SQL, schemas, checker files, validation files, case sets, inventory, reports, results, denominator scaffolds, paper results, raw retained evidence, `MIGRATION_MASTER_PLAN.md`, or `DECISION_LOG.md`.

Files created:
- `audits/top_level_readme_zh_entrypoint_v0/README.md`
- `audits/top_level_readme_zh_entrypoint_v0/smoke_results.csv`
- `audits/top_level_readme_zh_entrypoint_v0/command_log.md`
- `audits/top_level_readme_zh_entrypoint_v0/protected_surface_check.md`

Files modified:
- `README.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --help`: passed.
- `python scripts/user/run_user_benchmark.py --help`: passed.
- Documented public smoke dry-run: passed, selected_rows=2, candidate_generated_rows=0.
- Documented public smoke adapter-capture: passed, selected_rows=2, candidate_generated_rows=2.
- `pytest tests/user_entry`: failed during collection because the src-layout package is not importable without installation or `PYTHONPATH`.
- `PYTHONPATH=src pytest tests/user_entry`: passed, 32 tests with 1 skipped.
- Common-core scaffold count check: passed, 40 cases and 120 denominator rows.
- `git diff --check`: passed.
- Protected-surface diff check: passed.
- Local smoke outputs and pytest cache outputs created by this task were removed.

Commit hash:
- `4d91563` (`docs: rewrite top-level README in Chinese`)

Push result:
- Pushed to `origin/feature/case-package-v2-external-schema` (`fef2ca2..4d91563`).

Task result:
- README language: Chinese.
- Source code modified: no.
- Tests modified: no.
- Examples modified: no.
- Cases/manifests/schema/checker/validation/sql modified: no.
- `case_sets/` changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Official metrics computed by this task: no.
- Paper tables rendered by this task: no.
- DB/checker execution run by this task: no.
- Global leaderboard created: no.

Next safe action:
- Human review of the Chinese top-level README, then continue bounded release-surface metadata work without claiming full paper reproduction or official metrics.

### 2026-05-20 · Add user-entry data-flow file map to Chinese top-level README

Mode: documentation-only; no source-code changes; no script changes; no test changes; no case changes; no full paper reproduction; no official metrics; no paper rendering; no reports/results update; no global leaderboard
Legacy repo modified: no
Release repo modified: yes

Summary:
- Added a new Chinese section `用户入口数据流与文件位置` to the top-level `README.md`.
- Documented the current user-entry data flow from CLI parameters through Common-core metadata selection, case source SQL, adapter environment variables, candidate SQL capture, local ledger/summary/report outputs, and optional PostgreSQL/checker diagnostics.
- Mapped user-facing files and directories including `src/sql_rewrite_bench/user_run.py`, `scripts/user/run_user_benchmark.py`, `case_sets/common_core_v0/cases.csv`, `case_sets/common_core_v0/denominator_same_engine_120.csv`, `cases/<POOL>/<CASE_ID>/`, `examples/user/noop_adapter.py`, and `runs/user/<run_name>/...`.
- Reiterated that `runs/user/<run_name>/...` outputs are local diagnostics only: not official metrics, not paper tables, not reports/results updates, not retained evidence, and not leaderboard rows.
- Reiterated that default smoke does not execute DB queries or run checkers; PostgreSQL/checker diagnostics are opt-in local diagnostics only.
- Did not claim full paper reproduction, official metrics, report/result regeneration, global leaderboard creation, or exact JOB source paths for `PERF_0077` / `PERF_0082`.
- Did not modify source code, scripts, tests, examples, docs other than top-level `README.md`, cases, manifests, SQL, schemas, checker files, validation files, case sets, inventory, reports, results, denominator scaffolds, paper results, raw retained evidence, `MIGRATION_MASTER_PLAN.md`, or `DECISION_LOG.md`.

Files created:
- `audits/top_level_readme_user_entry_file_map_v0/README.md`
- `audits/top_level_readme_user_entry_file_map_v0/smoke_results.csv`
- `audits/top_level_readme_user_entry_file_map_v0/command_log.md`
- `audits/top_level_readme_user_entry_file_map_v0/protected_surface_check.md`

Files modified:
- `README.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --help`: passed.
- `python scripts/user/run_user_benchmark.py --help`: passed.
- Documented public smoke dry-run: passed, selected_rows=2, candidate_generated_rows=0.
- Documented public smoke adapter-capture: passed, selected_rows=2, candidate_generated_rows=2.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src pytest tests/user_entry`: passed, 32 tests with 1 skipped.
- Common-core scaffold count check: passed, 40 cases and 120 denominator rows.
- `git diff --check`: passed.
- Protected-surface diff check: passed.
- Local smoke outputs and pytest cache outputs created by this task were removed.

Commit hash:
- `0a3f736` (`docs: add user-entry file map to README`) after rebasing onto remote commits `cd6a77b` and `7c537fe`.

Push result:
- Pending final run-log push after second rebase validation.

Task result:
- README data-flow file map added: yes.
- Source code modified: no.
- Scripts modified: no.
- Tests modified: no.
- Examples modified: no.
- Cases/manifests/schema/checker/validation/sql modified: no.
- `case_sets/` changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Official metrics computed by this task: no.
- Paper tables rendered by this task: no.
- DB/checker execution run by this task: no.
- Global leaderboard created: no.

Next safe action:
- Human review of the README file map, then continue bounded release-surface metadata work without claiming full paper reproduction or official metrics.

### 2026-05-20 · Move detailed user-entry file map from README to docs

Mode: documentation-only; no source-code changes; no script changes; no test changes; no example changes; no case changes; no full paper reproduction; no official metrics; no paper rendering; no reports/results update; no global leaderboard
Legacy repo modified: no
Release repo modified: yes

Summary:
- Simplified the top-level Chinese `README.md` by replacing the detailed `用户入口数据流与文件位置` table with a concise `运行后看哪里` section.
- Created `docs/USER_ENTRY_DATA_FLOW.md` as the dedicated detailed user-entry data-flow and file-location guide.
- Used `{POOL}`, `{CASE_ID}`, `{run_name}`, and `{schema_id}` placeholders in the detailed guide to avoid ambiguous Markdown rendering of angle-bracket placeholder paths.
- Reiterated that `runs/user/{run_name}/...` outputs are local diagnostics only: not official metrics, not paper tables, not reports/results updates, not retained evidence, and not leaderboard rows.
- Reiterated that default smoke does not execute DB queries or run checkers; PostgreSQL/checker diagnostics are opt-in local diagnostics only.
- Did not modify source code, scripts, tests, examples, cases, manifests, SQL, schemas, checker files, validation files, case sets, inventory, reports, results, denominator scaffolds, paper results, raw retained evidence, `MIGRATION_MASTER_PLAN.md`, or `DECISION_LOG.md`.

Files created:
- `docs/USER_ENTRY_DATA_FLOW.md`
- `audits/user_entry_data_flow_doc_v0/README.md`
- `audits/user_entry_data_flow_doc_v0/smoke_results.csv`
- `audits/user_entry_data_flow_doc_v0/command_log.md`
- `audits/user_entry_data_flow_doc_v0/protected_surface_check.md`

Files modified:
- `README.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- `git diff --check`: passed.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --help`: passed.
- `python scripts/user/run_user_benchmark.py --help`: passed.
- Documented public smoke dry-run: passed, selected_rows=2, candidate_generated_rows=0.
- Documented public smoke adapter-capture: passed, selected_rows=2, candidate_generated_rows=2.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src pytest tests/user_entry`: passed, 32 tests with 1 skipped.
- Placeholder path check: passed; no `cases///`, `runs/user//`, `schemas//`, or angle-bracket case/schema placeholder paths remain in public README/data-flow docs.
- README large-table check: passed; detailed 20+ row file-location table removed from top-level `README.md`.
- Protected-surface diff check: passed.
- Local smoke outputs and Python cache outputs created by this task were removed.

Commit hash:
- `6ce1a29` (`docs(user-entry): move detailed file map to guide`)

Push result:
- Pushed to `origin/feature/case-package-v2-external-schema` (`3bd95dd..6ce1a29`).

Task result:
- Top-level README simplified: yes.
- Data-flow doc created: yes.
- Source code modified: no.
- Scripts modified: no.
- Tests modified: no.
- Examples modified: no.
- Cases/manifests/schema/checker/validation/sql modified: no.
- `case_sets/` changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Official metrics computed by this task: no.
- Paper tables rendered by this task: no.
- DB/checker execution run by this task: no.
- Global leaderboard created: no.

Next safe action:
- Human review of the split README and detailed user-entry data-flow doc, then continue bounded release-surface metadata work without claiming full paper reproduction or official metrics.

### 2026-05-20 · Add user-entry local evaluation architecture plan to project_control

Mode: project-control architecture planning only; no source-code changes; no script changes; no test changes; no docs outside `project_control/`; no case changes; no implementation of candidate preflight, quality reports, tag slicing, timing, metrics, paper rendering, reproduction CLI, retained-evidence adapter integration, reports/results migration, or global leaderboard
Legacy repo modified: no
Release repo modified: yes

Summary:
- Created `project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md`.
- Defined the local diagnostic user-entry architecture from CLI args through case selection, case package resolution, adapter runner, candidate preflight, engine execution routing, engine-specific execution, local result checking, ledger/failure-bucket writing, local quality reports, tag-aware slices, and future timing diagnostics.
- Recorded module ownership for current and proposed modules including `user_run.py`, `case_selection.py`, proposed `case_package_resolver.py`, proposed `adapter_runner.py`, proposed `candidate_preflight.py`, proposed `engine_execution.py`, `postgres_execution.py`, future `mysql_execution.py`, future `spark_execution.py`, `local_result_checker.py`, proposed `user_ledger.py`, proposed `user_quality_report.py`, proposed `tag_slices.py`, future `timing_diagnostic.py`, and `user_run_schema.py`.
- Recorded D029, `User-entry local evaluation architecture before paper reproduction`, as the durable architecture-boundary decision.
- Did not modify source code, scripts, tests, docs outside `project_control/`, examples, cases, manifests, SQL, schemas, checker files, validation files, case sets, inventory, reports, results, benchmark specs, repository specs, raw retained evidence, or `MIGRATION_MASTER_PLAN.md`.

Files created:
- `project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md`

Files modified:
- `project_control/DECISION_LOG.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- `git diff --check`: passed.
- Markdown heading sanity check for `project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md`: passed, all 16 required headings present.
- Protected-surface diff check: passed; only project-control files changed.
- Source/scripts/tests/docs outside `project_control`/cases/case_sets/reports/results changes: none.

Commit hash:
- `ad522c0` (`docs(project-control): add user-entry evaluation architecture plan`)

Push result:
- Pushed to `origin/feature/case-package-v2-external-schema` (`afd8a34..ad522c0`).

Task result:
- Plan file created: yes.
- Decision log updated: yes, D029 `User-entry local evaluation architecture before paper reproduction`.
- Source code modified: no.
- Scripts modified: no.
- Tests modified: no.
- Docs outside `project_control/` modified: no.
- Cases/manifests/schema/checker/validation/sql modified: no.
- `case_sets/` changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Official metrics computed by this task: no.
- DB/checker execution run by this task: no.
- Global leaderboard created: no.

Next safe action:
- U1 output schema and ledger-field audit.

### 2026-05-20 · U1 audit user-entry output schema and ledger fields

Mode: audit/design only; no source-code changes; no script changes; no test changes; no docs outside `project_control/`; no example changes; no case changes; no candidate preflight implementation; no quality report implementation; no tag slicing; no timing; no metrics; no paper rendering; no reproduction CLI; no reports/results update; no global leaderboard
Legacy repo modified: no
Release repo modified: yes

Summary:
- Created `audits/user_entry_output_schema_audit_v0/` as the U1 output schema and ledger-field audit packet.
- Ran module help, wrapper help, public smoke dry-run, public smoke adapter-capture, and lightweight user-entry tests.
- Inventoried current user-run output files, `ledger.csv` fields, `summary.json` keys, `failures.csv` fields, `report.md` sections, and status values from `user_run_schema.py`.
- Compared current fields to the target local-evaluation funnel in `project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md`.
- Produced a target funnel gap matrix, proposed future user-run row schema, proposed local diagnostic failure-bucket policy, gap list, and future U2 prompt.
- Verdict: `ready_with_gaps` for U2. Current schema is sufficient to design the resolver / adapter-runner / ledger-writer split, but preflight, quality-report, tag-slice, explicit DB-attempt, executable, source-like, and timing fields remain gaps for later phases.
- Removed local smoke outputs `runs/user/u1_schema_dry_run` and `runs/user/u1_schema_dummy_adapter` after schema inspection.
- Did not modify source code, scripts, tests, docs outside `project_control/`, examples, cases, manifests, SQL, schemas, checker files, validation files, case sets, inventory, reports, results, benchmark specs, repository specs, raw retained evidence, `MIGRATION_MASTER_PLAN.md`, `DECISION_LOG.md`, or `USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md`.

Files created:
- `audits/user_entry_output_schema_audit_v0/README.md`
- `audits/user_entry_output_schema_audit_v0/current_output_files.csv`
- `audits/user_entry_output_schema_audit_v0/current_ledger_fields.csv`
- `audits/user_entry_output_schema_audit_v0/current_summary_fields.csv`
- `audits/user_entry_output_schema_audit_v0/current_failure_fields.csv`
- `audits/user_entry_output_schema_audit_v0/status_value_inventory.csv`
- `audits/user_entry_output_schema_audit_v0/target_funnel_gap_matrix.csv`
- `audits/user_entry_output_schema_audit_v0/proposed_user_run_row_schema.csv`
- `audits/user_entry_output_schema_audit_v0/proposed_failure_bucket_policy.md`
- `audits/user_entry_output_schema_audit_v0/output_schema_gap_list.md`
- `audits/user_entry_output_schema_audit_v0/future_u2_prompt.md`
- `audits/user_entry_output_schema_audit_v0/command_log.md`
- `audits/user_entry_output_schema_audit_v0/protected_surface_check.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --help`: passed.
- `python scripts/user/run_user_benchmark.py --help`: passed.
- Public smoke dry-run: passed, selected_rows=2, candidate_generated_rows=0.
- Public smoke adapter-capture: passed, selected_rows=2, candidate_generated_rows=2.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src pytest tests/user_entry`: passed, 32 tests with 1 skipped.
- `git diff --check`: passed.
- CSV parse checks: passed for 7 new CSV files.
- Markdown sanity checks: passed for 6 new audit Markdown files.
- Protected-surface diff check: passed.
- Smoke output cleanup check: passed; U1 smoke output directories removed before commit.

Commit hash:
- `0010ea1` (`docs(audit): assess user-entry output schema`).

Push result:
- Pushed `0010ea1` to `origin/feature/case-package-v2-external-schema` (`7a62862..0010ea1`).

Task result:
- U1 audit packet created: yes.
- Audit verdict: `ready_with_gaps`.
- Current output files inventoried: yes.
- Current ledger fields inventoried: yes.
- Current summary fields inventoried: yes.
- Current failure/status fields inventoried: yes.
- Target funnel gap matrix created: yes.
- Proposed row schema created: yes.
- Future U2 prompt created: yes.
- Source code modified: no.
- Scripts modified: no.
- Tests modified: no.
- Docs outside `project_control/` modified: no.
- Examples modified: no.
- Cases/manifests/schema/checker/validation/sql modified: no.
- `case_sets/` changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Official metrics computed by this task: no.
- DB/checker execution run by this task: no.
- Paper tables rendered by this task: no.
- Global leaderboard created: no.

Next safe action:
- U2 module split design for resolver, adapter runner, and ledger writer.

### 2026-05-21 · U2 design user-entry resolver, adapter-runner, and ledger-writer split

Mode: audit/design only; no source-code changes; no script changes; no test changes; no docs outside `project_control/`; no example changes; no case changes; no candidate preflight implementation; no quality report implementation; no tag slicing; no timing; no metrics; no paper rendering; no reproduction CLI; no reports/results update; no global leaderboard
Legacy repo modified: no
Release repo modified: yes

Summary:
- Created `audits/user_entry_module_split_design_v0/` as the U2 module split design packet.
- Designed future modules `case_package_resolver.py`, `adapter_runner.py`, and `user_ledger.py`.
- Defined resolver inputs, fail-closed behavior, package asset outputs, and future tag/engine interactions.
- Defined adapter environment variables, `shell=False` invocation contract, workspace layout, candidate capture priority, and adapter status outputs.
- Defined ledger row construction, local failure-bucket priority handoff, local-only boundary flags, and CSV output responsibilities.
- Produced a behavior-preserving migration plan from current `user_run.py`, typed interface plan, failure bucket handoff matrix, validation plan, risk register, and future minimal split prompt.
- Verdict: `ready_for_minimal_split`.
- Did not modify source code, scripts, tests, docs outside `project_control/`, examples, cases, manifests, SQL, schemas, checker files, validation files, case sets, inventory, reports, results, benchmark specs, repository specs, raw retained evidence, `MIGRATION_MASTER_PLAN.md`, `DECISION_LOG.md`, or `USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md`.
- No DB/checker execution was run and no `runs/user/` outputs were created.

Files created:
- `audits/user_entry_module_split_design_v0/README.md`
- `audits/user_entry_module_split_design_v0/module_responsibility_matrix.csv`
- `audits/user_entry_module_split_design_v0/case_package_resolver_design.md`
- `audits/user_entry_module_split_design_v0/adapter_runner_design.md`
- `audits/user_entry_module_split_design_v0/user_ledger_design.md`
- `audits/user_entry_module_split_design_v0/user_run_migration_plan.md`
- `audits/user_entry_module_split_design_v0/typed_interface_plan.csv`
- `audits/user_entry_module_split_design_v0/failure_bucket_handoff_matrix.csv`
- `audits/user_entry_module_split_design_v0/validation_plan.md`
- `audits/user_entry_module_split_design_v0/risk_register.md`
- `audits/user_entry_module_split_design_v0/future_u2_minimal_split_prompt.md`
- `audits/user_entry_module_split_design_v0/command_log.md`
- `audits/user_entry_module_split_design_v0/protected_surface_check.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- `git diff --check`: passed.
- CSV parse checks: passed for 3 new CSV files.
- Markdown sanity checks: passed for 10 new audit Markdown files.
- Protected-surface diff check: passed.
- Run-output check: passed; no U2 `runs/user/` output directories were created.

Commit hash:
- `2cd3475` (`docs(audit): design user-entry module split`).

Push result:
- Pushed `2cd3475` to `origin/feature/case-package-v2-external-schema` (`187d3e8..2cd3475`).

Task result:
- U2 design packet created: yes.
- U2 verdict: `ready_for_minimal_split`.
- Modules designed: `case_package_resolver.py`, `adapter_runner.py`, `user_ledger.py`.
- Migration plan created: yes.
- Typed interface plan created: yes.
- Failure bucket handoff matrix created: yes.
- Future minimal split prompt created: yes.
- Source code modified: no.
- Scripts modified: no.
- Tests modified: no.
- Docs outside `project_control/` modified: no.
- Examples modified: no.
- Cases/manifests/schema/checker/validation/sql modified: no.
- `case_sets/` changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Official metrics computed by this task: no.
- DB/checker execution run by this task: no.
- Paper tables rendered by this task: no.
- Global leaderboard created: no.

Next safe action:
- Authorize U2 minimal behavior-preserving implementation of resolver, adapter runner, and ledger writer split.

### 2026-05-21 · U2 minimal implementation of user-entry resolver, adapter-runner, and ledger-writer split

Mode: refactor-only implementation; behavior-preserving user-entry module split; no candidate preflight; no quality reports; no tag slicing; no timing; no official metrics; no paper rendering; no reproduction CLI; no reports/results update; no retained-evidence parsing; no global leaderboard
Legacy repo modified: no
Release repo modified: yes

Summary:
- Added `src/sql_rewrite_bench/case_package_resolver.py` to resolve selected case package assets without inferring Common-core membership or scanning `cases/`.
- Added `src/sql_rewrite_bench/adapter_runner.py` to own adapter environment construction, `shell=False` invocation, repository-root cwd, stdout/stderr capture, timeout handling, and candidate capture priority.
- Added `src/sql_rewrite_bench/user_ledger.py` to own current ledger row construction, dry-run row construction, failure row construction, and `ledger.csv` / `failures.csv` writing without changing columns.
- Updated `src/sql_rewrite_bench/user_run.py` only to delegate existing behavior to those modules.
- Added `tests/user_entry/test_u2_module_split.py` for resolver, adapter-runner, ledger-writer, and public smoke dry-run behavior preservation.
- Created `audits/user_entry_u2_minimal_split_v0/`.
- Preserved current user-entry output schema, public smoke behavior, summary JSON, report Markdown, and optional PostgreSQL/checker orchestration.
- Did not implement candidate preflight, local quality reports, tag-aware slices, timing diagnostics, official metrics, paper rendering, reports/results updates, retained-evidence parsing, or leaderboard output.

Files created:
- `src/sql_rewrite_bench/case_package_resolver.py`
- `src/sql_rewrite_bench/adapter_runner.py`
- `src/sql_rewrite_bench/user_ledger.py`
- `tests/user_entry/test_u2_module_split.py`
- `audits/user_entry_u2_minimal_split_v0/README.md`
- `audits/user_entry_u2_minimal_split_v0/module_split_summary.csv`
- `audits/user_entry_u2_minimal_split_v0/behavior_preservation_results.csv`
- `audits/user_entry_u2_minimal_split_v0/test_results.md`
- `audits/user_entry_u2_minimal_split_v0/protected_surface_check.md`
- `audits/user_entry_u2_minimal_split_v0/command_log.md`

Files modified:
- `src/sql_rewrite_bench/user_run.py`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- `git diff --check`: passed.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --help`: passed.
- `python scripts/user/run_user_benchmark.py --help`: passed.
- Public smoke dry-run: passed, selected_rows=2, candidate_generated_rows=0.
- Public smoke adapter-capture: passed, selected_rows=2, candidate_generated_rows=2.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src pytest tests/user_entry -q`: passed, 39 tests with 1 skipped.
- CSV parse checks: passed for 2 new CSV files.
- Markdown sanity checks: passed for 4 new audit Markdown files.
- Protected-surface diff check: passed.
- Run-output cleanup check: passed; `runs/user/u2_split_dry_run` and `runs/user/u2_split_dummy_adapter` removed before commit.

Commit hash:
- `b757ed5` (`refactor(user-entry): split resolver adapter and ledger modules`).

Push result:
- Pushed `b757ed5` to `origin/feature/case-package-v2-external-schema` (`79e429c..b757ed5`).

Task result:
- U2 minimal split implemented: yes.
- Modules added: `case_package_resolver.py`, `adapter_runner.py`, `user_ledger.py`.
- `user_run.py` behavior-preserving delegation completed: yes.
- Tests added/updated: `tests/user_entry/test_u2_module_split.py`.
- Scripts modified: no.
- Docs modified: no.
- Examples modified: no.
- Cases/manifests/schema/checker/validation/sql modified: no.
- `case_sets/` changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Official metrics computed by this task: no.
- Paper tables rendered by this task: no.
- DB/checker execution run by this task: no.
- Global leaderboard created: no.

Next safe action:
- Human review of the U2 split, then authorize U3 candidate preflight v0 as a separate local-diagnostic task.

### 2026-05-21 · U3 implement candidate preflight v0 for user-entry local diagnostics

Mode: local-diagnostic implementation; DB-before candidate SQL preflight only; no quality reports; no tag slicing; no timing; no official metrics; no paper rendering; no retained-evidence parsing; no reports/results update; no global leaderboard
Legacy repo modified: no
Release repo modified: yes

Summary:
- Added `src/sql_rewrite_bench/candidate_preflight.py` for conservative text-level candidate readiness checks after adapter capture and before optional DB/checker diagnostics.
- Integrated preflight into `src/sql_rewrite_bench/user_run.py` for generated candidates only; dry-run rows and missing-candidate rows do not run preflight.
- Added ledger fields `candidate_preflight_status`, `candidate_preflight_passed`, `candidate_preflight_failure_class`, `candidate_safety_status`, `candidate_parse_status`, and `source_like_status`.
- Added local failure bucket `candidate_preflight_failed` for generated candidates that fail preflight.
- Added tests under `tests/user_entry/test_candidate_preflight.py` for preflight rules, source-like diagnostics, behavior preservation, and mocked DB/checker skip on preflight failure.
- Created `audits/user_entry_candidate_preflight_v0/`.

Files created:
- `src/sql_rewrite_bench/candidate_preflight.py`
- `tests/user_entry/test_candidate_preflight.py`
- `audits/user_entry_candidate_preflight_v0/README.md`
- `audits/user_entry_candidate_preflight_v0/preflight_rule_summary.csv`
- `audits/user_entry_candidate_preflight_v0/ledger_field_changes.csv`
- `audits/user_entry_candidate_preflight_v0/behavior_preservation_results.csv`
- `audits/user_entry_candidate_preflight_v0/test_results.md`
- `audits/user_entry_candidate_preflight_v0/protected_surface_check.md`
- `audits/user_entry_candidate_preflight_v0/command_log.md`

Files modified:
- `src/sql_rewrite_bench/user_run.py`
- `src/sql_rewrite_bench/user_ledger.py`
- `src/sql_rewrite_bench/user_run_schema.py`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- `git diff --check`: passed.
- `PYTHONPATH=src python -m py_compile src/sql_rewrite_bench/candidate_preflight.py src/sql_rewrite_bench/user_run.py src/sql_rewrite_bench/user_ledger.py src/sql_rewrite_bench/user_run_schema.py`: passed.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --help`: passed.
- `python scripts/user/run_user_benchmark.py --help`: passed.
- Public smoke dry-run: passed, selected_rows=2, candidate_generated_rows=0.
- Public smoke adapter-capture: passed, selected_rows=2, candidate_generated_rows=2.
- `PYTHONPATH=src pytest tests/user_entry`: passed, 52 tests with 1 skipped.
- CSV parse checks: passed for 3 new CSV files.
- Protected-surface diff check: passed.
- Run-output cleanup check: passed; `runs/user/u3_preflight_dry_run` and `runs/user/u3_preflight_dummy_adapter` removed before commit.

Commit hash:
- `d4e0074` (`feat(user-entry): add candidate preflight diagnostics`).

Push result:
- Pushed `d4e0074` to `origin/feature/case-package-v2-external-schema` (`a5cbb0b..d4e0074`).

Task result:
- U3 candidate preflight implemented: yes.
- Module added: `src/sql_rewrite_bench/candidate_preflight.py`.
- `user_run.py` integration completed: yes.
- Scripts modified: no.
- Docs modified: no.
- Examples modified: no.
- Cases/manifests/schema/checker/validation/sql modified: no.
- `case_sets/` changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Official metrics computed by this task: no.
- Paper tables rendered by this task: no.
- Live DB/checker execution run by this task: no.
- Global leaderboard created: no.

Next safe action:
- Human review of U3 preflight fields and failure-bucket behavior, then authorize U4 local quality report v0 only if accepted.

### 2026-05-21 · U4 implement local quality report v0 for user-entry diagnostics

Mode: local-diagnostic implementation; local quality summary/report only; no tag slicing; no timing; no official metrics; no paper rendering; no retained-evidence parsing; no reports/results update; no global leaderboard
Legacy repo modified: no
Release repo modified: yes

Summary:
- Added `src/sql_rewrite_bench/user_quality_report.py` to build and write local diagnostic quality summaries from current user-run ledger rows.
- Integrated quality output generation into `src/sql_rewrite_bench/user_run.py` after `ledger.csv`, `failures.csv`, `summary.json`, and `report.md` are written.
- Added `quality_summary.json` and `quality_report.md` to every user-run output under `runs/user/{run_name}/`.
- Added `tests/user_entry/test_quality_report.py` covering dry-run smoke, adapter-capture smoke, local boundary flags, funnel counts, absent tag slices, and no official/timing metric fields.
- Created `audits/user_entry_local_quality_report_v0/`.

Files created:
- `src/sql_rewrite_bench/user_quality_report.py`
- `tests/user_entry/test_quality_report.py`
- `audits/user_entry_local_quality_report_v0/README.md`
- `audits/user_entry_local_quality_report_v0/quality_summary_schema.md`
- `audits/user_entry_local_quality_report_v0/quality_report_sections.md`
- `audits/user_entry_local_quality_report_v0/funnel_count_mapping.csv`
- `audits/user_entry_local_quality_report_v0/behavior_preservation_results.csv`
- `audits/user_entry_local_quality_report_v0/test_results.md`
- `audits/user_entry_local_quality_report_v0/protected_surface_check.md`
- `audits/user_entry_local_quality_report_v0/command_log.md`

Files modified:
- `src/sql_rewrite_bench/user_run.py`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- `git diff --check`: passed.
- `PYTHONPATH=src python -m py_compile src/sql_rewrite_bench/user_quality_report.py src/sql_rewrite_bench/user_run.py src/sql_rewrite_bench/user_ledger.py src/sql_rewrite_bench/user_run_schema.py`: passed.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --help`: passed.
- `python scripts/user/run_user_benchmark.py --help`: passed.
- Public smoke dry-run: passed, selected_rows=2, candidate_generated_rows=0.
- Public smoke adapter-capture: passed, selected_rows=2, candidate_generated_rows=2.
- Quality output inspection: passed for `quality_summary.json` and `quality_report.md`.
- `PYTHONPATH=src pytest tests/user_entry`: passed, 55 tests with 1 skipped.
- CSV parse checks: passed for 2 new CSV files.
- Protected-surface diff check: passed.
- Run-output cleanup check: passed; `runs/user/u4_quality_dry_run` and `runs/user/u4_quality_dummy_adapter` removed before commit.

Commit hash:
- `880b971046919aa80da1b07640031d317e8514c9`

Push result:
- Pushed to `origin/feature/case-package-v2-external-schema` (`aec2cf5..880b971`).

Task result:
- U4 local quality report implemented: yes.
- Module added: `src/sql_rewrite_bench/user_quality_report.py`.
- Output files added to user runs: `quality_summary.json`, `quality_report.md`.
- `user_run.py` integration completed: yes.
- Scripts modified: no.
- Docs modified: no.
- Examples modified: no.
- Cases/manifests/schema/checker/validation/sql modified: no.
- `case_sets/` changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Official metrics computed by this task: no.
- Paper tables rendered by this task: no.
- Live DB/checker execution run by this task: no.
- Tag slices created by this task: no.
- Timing/speedup computed by this task: no.
- Global leaderboard created: no.

Next safe action:
- Human review of U4 quality outputs, then authorize U5 tag-aware slices v0 only if accepted.

### 2026-05-21 · U5 implement tag-aware slices v0 for user-entry diagnostics

Mode: local-diagnostic implementation; tag-aware slices only; no timing; no speedup; no official metrics; no paper rendering; no retained-evidence parsing; no reports/results update; no full paper reproduction CLI; no global leaderboard
Legacy repo modified: no
Release repo modified: yes

Summary:
- Added `src/sql_rewrite_bench/tag_slices.py` to load retained manifest taxonomy tags and build local diagnostic tag-slice counts from current user-run ledger rows.
- Integrated `tag_slices.csv` generation into `src/sql_rewrite_bench/user_run.py` after local quality report generation.
- Updated `src/sql_rewrite_bench/user_quality_report.py` so quality outputs record that tag slices are available as local diagnostics.
- Added `tests/user_entry/test_tag_slices.py` and updated U4 quality-report tests for U5 tag-slice availability.
- Created `audits/user_entry_tag_slices_v0/`.

Files created:
- `src/sql_rewrite_bench/tag_slices.py`
- `tests/user_entry/test_tag_slices.py`
- `audits/user_entry_tag_slices_v0/README.md`
- `audits/user_entry_tag_slices_v0/tag_source_inventory.csv`
- `audits/user_entry_tag_slices_v0/tag_slice_schema.md`
- `audits/user_entry_tag_slices_v0/tag_slice_count_mapping.csv`
- `audits/user_entry_tag_slices_v0/behavior_preservation_results.csv`
- `audits/user_entry_tag_slices_v0/test_results.md`
- `audits/user_entry_tag_slices_v0/protected_surface_check.md`
- `audits/user_entry_tag_slices_v0/command_log.md`

Files modified:
- `src/sql_rewrite_bench/user_run.py`
- `src/sql_rewrite_bench/user_quality_report.py`
- `tests/user_entry/test_quality_report.py`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- `git diff --check`: passed.
- `PYTHONPATH=src python -m py_compile src/sql_rewrite_bench/tag_slices.py src/sql_rewrite_bench/user_run.py src/sql_rewrite_bench/user_quality_report.py src/sql_rewrite_bench/case_package_resolver.py`: passed.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --help`: passed.
- `python scripts/user/run_user_benchmark.py --help`: passed.
- Public smoke dry-run: passed, selected_rows=2, candidate_generated_rows=0, `tag_slices.csv` present.
- Public smoke adapter-capture: passed, selected_rows=2, candidate_generated_rows=2, `tag_slices.csv` present.
- Tag-slice output inspection: passed for `tag_slices.csv` and local-only boundary flags.
- Quality output inspection: passed for `tag_slices_included=true`.
- `PYTHONPATH=src pytest tests/user_entry`: passed, 59 passed and 1 skipped.
- CSV parse checks: passed for 3 new CSV files.
- Protected-surface diff check: passed.
- Run-output cleanup check: passed; `runs/user/u5_tags_dry_run` and `runs/user/u5_tags_dummy_adapter` removed before commit.

Commit hash:
- `18998112936fbb1293102f8d225dc54c1d241f9d`

Push result:
- Pushed to `origin/feature/case-package-v2-external-schema` (`b87de5c..1899811`).

Task result:
- U5 tag-aware slices implemented: yes.
- Module added: `src/sql_rewrite_bench/tag_slices.py`.
- Output files added to user runs: `tag_slices.csv`.
- Tag source used: retained `manifest.yaml` taxonomy metadata via resolved case packages.
- `user_run.py` integration completed: yes.
- Scripts modified: no.
- Docs modified: no.
- Examples modified: no.
- Cases/manifests/schema/checker/validation/sql modified: no.
- `case_sets/` changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Official metrics computed by this task: no.
- Paper tables rendered by this task: no.
- Live DB/checker execution run by this task: no.
- Timing/speedup computed by this task: no.
- Tag score/ranking created by this task: no.
- Global leaderboard created: no.

Next safe action:
- Human review of U5 tag slices, then authorize U6 user readability enhancements or defer to the next approved user-entry phase.

### 2026-05-21 · U6 add user-entry readability commands for case listing, selection explanation, and output schema

Mode: user-readability implementation; command-only inspection helpers; no timing; no speedup; no official metrics; no paper rendering; no retained-evidence parsing; no reports/results update; no full paper reproduction CLI; no global leaderboard
Legacy repo modified: no
Release repo modified: yes

Summary:
- Added `--list-cases` to list Common-core cases from `case_sets/common_core_v0/` metadata without scanning `cases/`.
- Added `--explain-selection` to explain selected case-engine rows, pool/engine distribution, smoke state, case-list filtering, and missing/outside-case-set IDs.
- Added `--show-output-schema` to print local user-run output schema descriptions and local-only boundaries.
- Added `src/sql_rewrite_bench/user_output_schema.py`.
- Updated `README.md` and `docs/USER_BENCHMARK_GUIDE.md` with concise command documentation.
- Added `tests/user_entry/test_readability_commands.py`.
- Created `audits/user_entry_readability_v0/`.

Files created:
- `src/sql_rewrite_bench/user_output_schema.py`
- `tests/user_entry/test_readability_commands.py`
- `audits/user_entry_readability_v0/README.md`
- `audits/user_entry_readability_v0/command_examples.md`
- `audits/user_entry_readability_v0/behavior_preservation_results.csv`
- `audits/user_entry_readability_v0/test_results.md`
- `audits/user_entry_readability_v0/protected_surface_check.md`
- `audits/user_entry_readability_v0/command_log.md`

Files modified:
- `src/sql_rewrite_bench/user_run.py`
- `src/sql_rewrite_bench/case_selection.py`
- `README.md`
- `docs/USER_BENCHMARK_GUIDE.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- `git diff --check`: passed.
- `PYTHONPATH=src python -m py_compile src/sql_rewrite_bench/user_run.py src/sql_rewrite_bench/case_selection.py src/sql_rewrite_bench/user_run_schema.py src/sql_rewrite_bench/user_output_schema.py`: passed.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --help`: passed.
- `python scripts/user/run_user_benchmark.py --help`: passed.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --list-cases`: passed.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --pool PERF --list-cases`: passed.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine postgres --smoke --explain-selection`: passed.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --show-output-schema`: passed.
- Public smoke dry-run: passed, selected_rows=2, candidate_generated_rows=0.
- Public smoke adapter-capture: passed, selected_rows=2, candidate_generated_rows=2.
- Quality/tag output inspection: passed for `quality_summary.json` and `tag_slices.csv`.
- `PYTHONPATH=src pytest tests/user_entry`: passed, 65 passed and 1 skipped.
- CSV parse checks: passed for 1 new CSV file.
- Protected-surface diff check: passed.
- Run-output cleanup check: passed; `runs/user/u6_readability_dry_run` and `runs/user/u6_readability_dummy_adapter` removed before commit.
- Command-only helper output check: passed; no run output directories created by `--list-cases`, `--explain-selection`, or `--show-output-schema`.

Commit hash:
- `d37f44122d39bd408c76714ed11825214fd382ea`

Push result:
- Pushed to `origin/feature/case-package-v2-external-schema` (`15d913e..d37f441`).

Task result:
- U6 readability enhancements implemented: yes.
- Commands added: `--list-cases`, `--explain-selection`, `--show-output-schema`.
- Scripts modified: no.
- Examples modified: no.
- Cases/manifests/schema/checker/validation/sql modified: no.
- `case_sets/` changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Official metrics computed by this task: no.
- Paper tables rendered by this task: no.
- Live DB/checker execution run by this task: no.
- Timing/speedup computed by this task: no.
- Tag score/ranking created by this task: no.
- Global leaderboard created: no.

Next safe action:
- Human review of U6 readability command output, then authorize U7 engine execution router and MySQL/Spark fail-closed interface design if accepted.

### 2026-05-21 · Triage and fix user-entry-smoke GitHub Actions failure

Mode: CI-smoke triage and hygiene fix; no U7 work; no user-entry runtime behavior change; no official metrics; no paper rendering; no reports/results update; no global leaderboard
Legacy repo modified: no
Release repo modified: yes

Summary:
- Inspected the public GitHub Actions run metadata for run `26206722303`; job `B-line user-entry smoke` failed at the `Run B-line user-entry smoke` step. Full job logs were not accessible without repository admin rights from this environment.
- Reproduced the CI-only failure locally in a fresh editable-install virtual environment without PyYAML: U5 tag-slice tests failed because retained manifest taxonomy parsing did not have full YAML semantics.
- Confirmed fresh editable install with `pytest` and `PyYAML` passes `scripts/dev/run_user_entry_ci_smoke.py`.
- Updated `.github/workflows/user_entry_smoke.yml` to install `pytest` and `PyYAML` for the CI smoke job.
- Updated `scripts/dev/run_user_entry_ci_smoke.py` to verify U4/U5 output files and remove `runs/user/ci_smoke_dry_run` plus `runs/user/ci_smoke_adapter` before checking `runs/user` cleanliness.
- Created `audits/user_entry_ci_smoke_failure_fix_v0/`.

Files created:
- `audits/user_entry_ci_smoke_failure_fix_v0/README.md`
- `audits/user_entry_ci_smoke_failure_fix_v0/command_log.md`
- `audits/user_entry_ci_smoke_failure_fix_v0/protected_surface_check.md`

Files modified:
- `.github/workflows/user_entry_smoke.yml`
- `scripts/dev/run_user_entry_ci_smoke.py`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- `python scripts/dev/run_user_entry_ci_smoke.py`: passed.
- Fresh editable-install venv with `pytest PyYAML`: passed.
- `git diff --check`: passed.
- `python -m py_compile scripts/dev/run_user_entry_ci_smoke.py`: passed.
- `PYTHONPATH=src pytest tests/user_entry`: passed, 65 passed and 1 skipped.
- Protected-surface diff check: passed.
- CI smoke outputs cleanup: passed; `runs/user/ci_smoke_dry_run` and `runs/user/ci_smoke_adapter` were removed by the smoke script.

Task result:
- CI smoke failure triaged and fixed: yes.
- CI smoke outputs were not the reproduced root cause, but cleanup was hardened.
- Denominator changed: no.
- Paper results changed: no.
- Reports/results changed: no.
- Global leaderboard created: no.

Next safe action:
- Push the CI-smoke fix and observe or rerun GitHub Actions; do not continue U7 until `user-entry-smoke` is green.

### 2026-05-21 · U7 design engine execution router and MySQL/Spark fail-closed interfaces

Mode: design/audit only; no engine router implementation; no MySQL/Spark execution implementation; no live DB/checker execution; no timing; no official metrics; no paper rendering; no reports/results update; no global leaderboard
Legacy repo modified: no
Release repo modified: yes

Summary:
- Created `audits/user_entry_engine_router_design_v0/`.
- Designed a future `src/sql_rewrite_bench/engine_execution.py` router as dispatcher only.
- Defined a common local `EngineExecutionResult` interface.
- Documented how current `src/sql_rewrite_bench/postgres_execution.py` maps to the common interface.
- Documented fail-closed future MySQL and Spark execution interface plans.
- Documented checker and ledger handoffs.
- Documented timing/speedup and official-metric boundaries.
- Drafted a future minimal router implementation prompt.

Files created:
- `audits/user_entry_engine_router_design_v0/README.md`
- `audits/user_entry_engine_router_design_v0/engine_router_design.md`
- `audits/user_entry_engine_router_design_v0/engine_execution_interface.csv`
- `audits/user_entry_engine_router_design_v0/postgres_mapping.md`
- `audits/user_entry_engine_router_design_v0/mysql_fail_closed_plan.md`
- `audits/user_entry_engine_router_design_v0/spark_fail_closed_plan.md`
- `audits/user_entry_engine_router_design_v0/checker_handoff.md`
- `audits/user_entry_engine_router_design_v0/ledger_handoff_matrix.csv`
- `audits/user_entry_engine_router_design_v0/timing_boundary.md`
- `audits/user_entry_engine_router_design_v0/future_u7_minimal_router_prompt.md`
- `audits/user_entry_engine_router_design_v0/command_log.md`
- `audits/user_entry_engine_router_design_v0/protected_surface_check.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- `git diff --check`: passed.
- CSV parse checks for all new CSV files: passed.
- Markdown heading sanity checks for all new audit markdown files: passed.
- Protected-surface diff check: passed; only the U7 audit packet and project-control files changed.
- Run-output check: passed; no `runs/user/` outputs created.

Task result:
- U7 design packet created: yes.
- U7 verdict: ready_for_minimal_router.
- Engine router designed: yes.
- Common engine execution interface designed: yes.
- PostgreSQL mapping documented: yes.
- MySQL fail-closed plan documented: yes.
- Spark fail-closed plan documented: yes.
- Checker handoff documented: yes.
- Ledger handoff documented: yes.
- Timing boundary documented: yes.
- Future minimal router prompt created: yes.
- Implementation performed: no.
- Source code modified: no.
- Scripts modified: no.
- Tests modified: no.
- Docs outside project_control modified: no.
- Cases/manifests/schema/checker/validation/sql modified: no.
- `case_sets/` changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Official metrics computed: no.
- DB/checker execution run: no.
- Paper tables rendered: no.
- Timing/speedup computed: no.
- Global leaderboard created: no.

Next safe action:
- Human review of U7 design; if accepted, authorize a separate minimal router implementation limited to `engine_execution.py` plus fail-closed MySQL/Spark stubs while preserving PostgreSQL behavior.

### 2026-05-21 · U7 minimal implementation of user-entry engine execution router and fail-closed MySQL/Spark stubs

Mode: minimal behavior-preserving local-diagnostic implementation; no live MySQL/Spark execution; no timing; no official metrics; no paper rendering; no reports/results update; no global leaderboard
Legacy repo modified: no
Release repo modified: yes

Summary:
- Added `src/sql_rewrite_bench/engine_execution.py` as a router for optional user-entry local DB diagnostics.
- Added fail-closed `src/sql_rewrite_bench/mysql_execution.py` and `src/sql_rewrite_bench/spark_execution.py` stubs.
- Updated `src/sql_rewrite_bench/user_run.py` to call the router instead of directly calling PostgreSQL execution.
- Preserved PostgreSQL behavior by delegating `postgres` rows to the existing `postgres_execution.py` path.
- Added tests for PostgreSQL router dispatch, MySQL/Spark fail-closed behavior, unsupported-engine fail-closed behavior, and user-run MySQL fail-closed ledger behavior.
- Created `audits/user_entry_u7_minimal_router_v0/`.

Files created:
- `src/sql_rewrite_bench/engine_execution.py`
- `src/sql_rewrite_bench/mysql_execution.py`
- `src/sql_rewrite_bench/spark_execution.py`
- `tests/user_entry/test_engine_execution_router.py`
- `audits/user_entry_u7_minimal_router_v0/README.md`
- `audits/user_entry_u7_minimal_router_v0/router_implementation_summary.csv`
- `audits/user_entry_u7_minimal_router_v0/fail_closed_stub_summary.csv`
- `audits/user_entry_u7_minimal_router_v0/behavior_preservation_results.csv`
- `audits/user_entry_u7_minimal_router_v0/test_results.md`
- `audits/user_entry_u7_minimal_router_v0/protected_surface_check.md`
- `audits/user_entry_u7_minimal_router_v0/command_log.md`

Files modified:
- `src/sql_rewrite_bench/user_run.py`
- `tests/user_entry/test_candidate_preflight.py`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- `git diff --check`: passed.
- Python compile for router/stub/user-run modules: passed.
- Module help: passed.
- Wrapper help: passed.
- Readability commands: passed.
- Public smoke dry-run: passed.
- Public smoke adapter-capture: passed.
- `PYTHONPATH=src pytest tests/user_entry`: passed, 70 passed and 1 skipped.
- Protected-surface diff check: passed.
- Run-output cleanup: passed.

Task result:
- U7 minimal router implemented: yes.
- PostgreSQL behavior preserved: yes.
- MySQL fail-closed stub added: yes.
- Spark fail-closed stub added: yes.
- Live MySQL/Spark execution run: no.
- DB/checker execution run by this task: no live DB/checker.
- Timing/speedup computed by this task: no.
- Official metrics computed by this task: no.
- Paper tables rendered by this task: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Global leaderboard created: no.

Commit hash:
- Pending until commit.

Push result:
- Pending until push.

Next safe action:
- Human review of U7 router/stub behavior, then authorize U8 timing diagnostic design only if desired.

### 2026-05-21 · Close out user-entry local evaluation phase U0-U7

Mode: read-only/project-control closeout audit; no source implementation; no live DB/checker execution; no timing; no official metrics; no paper rendering; no reports/results update; no global leaderboard
Legacy repo modified: no
Release repo modified: yes

Summary:
- Created `audits/user_entry_local_evaluation_phase_closeout_v0/`.
- Reviewed U0 architecture plan, U1 output schema audit, U2 design and minimal split, U3 candidate preflight, U4 local quality report, U5 tag-aware slices, U6 readability commands, CI smoke fix, U7 design, and U7 minimal router implementation.
- Confirmed current supported user-entry capabilities: public smoke, metadata-driven Common-core selection, adapter capture, candidate preflight, optional PostgreSQL local diagnostics/checker, ledger/failure accounting, local quality report, tag-aware slices, readability commands, and engine router with fail-closed MySQL/Spark stubs.
- Confirmed deferred work: live MySQL/Spark execution, timing/speedup, official metrics, paper table rendering, retained-evidence adapter integration, reports/results migration, full paper reproduction CLI, SpeedupTransferRate, and global leaderboard.
- Recommendation: pause user-entry implementation after U0-U7 and return to release-surface metadata readiness unless timing protocol design is explicitly authorized.

Files created:
- `audits/user_entry_local_evaluation_phase_closeout_v0/README.md`
- `audits/user_entry_local_evaluation_phase_closeout_v0/phase_capability_matrix.csv`
- `audits/user_entry_local_evaluation_phase_closeout_v0/current_command_surface.csv`
- `audits/user_entry_local_evaluation_phase_closeout_v0/current_output_surface.csv`
- `audits/user_entry_local_evaluation_phase_closeout_v0/deferred_work_register.md`
- `audits/user_entry_local_evaluation_phase_closeout_v0/timing_readiness_review.md`
- `audits/user_entry_local_evaluation_phase_closeout_v0/closeout_validation_results.csv`
- `audits/user_entry_local_evaluation_phase_closeout_v0/protected_surface_check.md`
- `audits/user_entry_local_evaluation_phase_closeout_v0/command_log.md`
- `audits/user_entry_local_evaluation_phase_closeout_v0/future_next_step_prompt.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- `git diff --check`: passed.
- Module help: passed.
- Wrapper help: passed.
- Readability commands: passed.
- Public smoke dry-run: passed.
- Public smoke adapter-capture: passed.
- Smoke output inspection: passed for `quality_summary.json`, `quality_report.md`, and `tag_slices.csv`.
- `PYTHONPATH=src pytest tests/user_entry`: passed, 70 passed and 1 skipped.
- Protected-surface diff check: passed.
- Run-output cleanup: passed.

Task result:
- Closeout verdict: complete_with_deferred_items.
- Source code modified: no.
- Scripts modified: no.
- Tests modified: no.
- Docs outside `project_control` modified: no.
- Cases/manifests/schema/checker/validation/sql modified: no.
- `case_sets/` changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Official metrics computed by this task: no.
- Paper tables rendered by this task: no.
- DB/checker execution run by this task: no live DB/checker.
- Timing/speedup computed by this task: no.
- Tag score/ranking created by this task: no.
- Global leaderboard created: no.

Next safe action:
- Pause user-entry implementation and run release-surface metadata readiness work, unless a maintainer explicitly authorizes U8 timing protocol design.

### 2026-05-21 · Audit release-surface metadata readiness after user-entry closeout

Mode: readiness audit and planning only; no metadata implementation; no source changes; no metrics; no paper rendering; no reports/results update; no release tag/export branch; no global leaderboard
Legacy repo modified: no
Release repo modified: yes

Summary:
- Created `audits/release_surface_metadata_readiness_v0/`.
- Audited public release-surface metadata after user-entry U0-U7 closeout.
- Confirmed ready surfaces: top-level Chinese `README.md`, user docs, user-entry smoke/local diagnostics, Common-core v0 case packages, case-set/denominator scaffolds, external schemas, repository specs, tests, and CI smoke workflows.
- Confirmed missing or policy-dependent surfaces: `LICENSE`, `CITATION.cff`, `CONTRIBUTING.md`, `benchmark_spec/`, `reports/`, `results/`, root `.gitignore`, README language posture, reports/results public boundary, and release branch/tag policy.
- Verdict: `ready_with_policy_decisions`.
- Recommendation: collect maintainer decisions before creating license/citation/contribution/release-policy files; separately authorize low-risk metadata skeletons for benchmark spec and placeholder boundary docs after policy scope is accepted.

Files created:
- `audits/release_surface_metadata_readiness_v0/README.md`
- `audits/release_surface_metadata_readiness_v0/release_surface_inventory.csv`
- `audits/release_surface_metadata_readiness_v0/metadata_blocker_matrix.csv`
- `audits/release_surface_metadata_readiness_v0/human_decision_register.md`
- `audits/release_surface_metadata_readiness_v0/low_risk_skeleton_plan.md`
- `audits/release_surface_metadata_readiness_v0/license_options_note.md`
- `audits/release_surface_metadata_readiness_v0/benchmark_spec_skeleton_outline.md`
- `audits/release_surface_metadata_readiness_v0/reports_results_boundary_note.md`
- `audits/release_surface_metadata_readiness_v0/release_surface_next_phase_prompt.md`
- `audits/release_surface_metadata_readiness_v0/command_log.md`
- `audits/release_surface_metadata_readiness_v0/protected_surface_check.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- `git diff --check`: passed.
- CSV parse checks for all new CSV files: passed.
- Markdown sanity checks for new Markdown files: passed.
- Protected-surface diff check: passed.
- No `runs/user/` outputs created.

Task result:
- Readiness verdict: ready_with_policy_decisions.
- Source code modified: no.
- Scripts modified: no.
- Tests modified: no.
- Docs modified: no.
- Examples modified: no.
- Cases/manifests/schema/checker/validation/sql modified: no.
- `case_sets/` changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Official metrics computed by this task: no.
- Paper tables rendered by this task: no.
- DB/checker execution run by this task: no.
- Timing/speedup computed by this task: no.
- Global leaderboard created: no.
- Release tag/export branch created: no.

Next safe action:
- Collect maintainer policy decisions for license, citation, contribution policy, README language posture, benchmark-spec wording, reports/results boundary, and release branch/tag policy before metadata skeleton implementation.

### 2026-05-21 · Record release-surface policy decisions before metadata skeleton implementation

Mode: project-control policy recording only; no metadata skeleton creation; no source changes; no metrics; no paper rendering; no reports/results update; no release tag/export branch; no global leaderboard
Legacy repo modified: no
Release repo modified: yes

Summary:
- Created `project_control/RELEASE_SURFACE_POLICY_DECISIONS.md`.
- Recorded Apache-2.0 as the initial repository license policy.
- Recorded citation, contribution, README language, benchmark_spec, reports/results, release branch/tag, timing, metrics, and reproduction boundaries.
- Added durable decision D030 to `project_control/DECISION_LOG.md`.
- Created `audits/release_surface_policy_decisions_v0/`.
- No `LICENSE`, `CITATION.cff`, `CONTRIBUTING.md`, `benchmark_spec/`, `reports/`, or `results/` files were created or modified.

Files created:
- `project_control/RELEASE_SURFACE_POLICY_DECISIONS.md`
- `audits/release_surface_policy_decisions_v0/README.md`
- `audits/release_surface_policy_decisions_v0/decision_summary.csv`
- `audits/release_surface_policy_decisions_v0/implementation_next_steps.md`
- `audits/release_surface_policy_decisions_v0/protected_surface_check.md`
- `audits/release_surface_policy_decisions_v0/command_log.md`

Files modified:
- `project_control/DECISION_LOG.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- `git diff --check`: passed.
- Markdown sanity checks: passed.
- CSV parse checks: passed.
- Protected-surface diff check: passed.

Task result:
- Policy decisions file created: yes.
- Decision log updated: yes, D030 `Release-surface metadata policy decisions before skeleton implementation`.
- License decision recorded: Apache-2.0.
- Citation decision recorded: placeholder-safe; no DOI/author details invented.
- Contribution policy decision recorded: conservative.
- README language posture recorded: Chinese acceptable on construction branch; English or bilingual entrypoint required before final public artifact.
- benchmark_spec scope decision recorded: public v0 only.
- reports/results boundary decision recorded: boundary README only in future skeleton task; no result generation or migration.
- Release branch/tag decision recorded: no tag/export branch yet.
- Source code modified: no.
- Scripts modified: no.
- Tests modified: no.
- Docs outside `project_control` modified: no.
- Examples modified: no.
- Cases/manifests/schema/checker/validation/sql modified: no.
- `case_sets/` changed: no.
- Reports/results changed: no.
- benchmark_spec changed: no.
- LICENSE/CITATION/CONTRIBUTING created: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Official metrics computed by this task: no.
- Paper tables rendered by this task: no.
- DB/checker execution run by this task: no.
- Timing/speedup computed by this task: no.
- Global leaderboard created: no.
- Release tag/export branch created: no.
- Commit hash: pending at commit time; final hash reported in task closeout.
- Push result: pending at commit time; final push result reported in task closeout.

Next safe action:
- Authorize metadata-only skeleton implementation for `LICENSE`, placeholder-safe `CITATION.cff`, conservative `CONTRIBUTING.md`, public-v0 `benchmark_spec/`, and reports/results boundary README files.

### 2026-05-21 · Implement metadata-only release-surface skeleton

Mode: metadata/skeleton only; no metrics; no paper rendering; no reports/results migration; no release tag/export branch; no global leaderboard
Legacy repo modified: no
Release repo modified: yes

Summary:
- Created the low-risk public release-surface metadata skeleton governed by `project_control/RELEASE_SURFACE_POLICY_DECISIONS.md`.
- Added Apache-2.0 `LICENSE` with placeholder-safe `SQL-RewriteBench contributors` copyright holder.
- Added placeholder-safe `CITATION.cff` without DOI or invented individual author metadata.
- Added conservative `CONTRIBUTING.md`.
- Added narrow root `.gitignore` that ignores `runs/user/` but not all of `runs/`.
- Added public-v0 `benchmark_spec/` skeleton files.
- Added boundary README files for `reports/` and `results/`.
- Added `docs/README.md` as a documentation index.

Files created:
- `LICENSE`
- `CITATION.cff`
- `CONTRIBUTING.md`
- `.gitignore`
- `benchmark_spec/README.md`
- `benchmark_spec/scope.md`
- `benchmark_spec/case_package_contract.md`
- `benchmark_spec/denominator_policy.md`
- `benchmark_spec/reporting_policy.md`
- `reports/README.md`
- `results/README.md`
- `docs/README.md`
- `audits/release_surface_metadata_skeleton_v0/README.md`
- `audits/release_surface_metadata_skeleton_v0/created_files_inventory.csv`
- `audits/release_surface_metadata_skeleton_v0/policy_traceability_matrix.csv`
- `audits/release_surface_metadata_skeleton_v0/protected_surface_check.md`
- `audits/release_surface_metadata_skeleton_v0/command_log.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- `git diff --check`: passed.
- `CITATION.cff` YAML syntax check: passed.
- CSV parse checks: passed.
- Markdown sanity checks: passed.
- Protected-surface diff check: passed.

Task result:
- Metadata skeleton implemented: yes.
- LICENSE created: yes.
- CITATION.cff created: yes.
- CONTRIBUTING.md created: yes.
- benchmark_spec created: yes.
- reports/results boundary READMEs created: yes.
- .gitignore created/updated: yes.
- Source code modified: no.
- Scripts modified: no.
- Tests modified: no.
- Examples modified: no.
- Cases/manifests/schema/checker/validation/sql modified: no.
- `case_sets/` changed: no.
- Existing reports/results data changed beyond README boundaries: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Official metrics computed by this task: no.
- Paper tables rendered by this task: no.
- DB/checker execution run by this task: no.
- Timing/speedup computed by this task: no.
- Global leaderboard created: no.
- Release tag/export branch created: no.
- Commit hash: pending at commit time; final hash reported in task closeout.
- Push result: pending at commit time; final push result reported in task closeout.

Next safe action:
- Run final public-release metadata/readiness review before any release tag or export branch.

### 2026-05-21 · Polish release-surface metadata skeleton and run lightweight readiness check

Mode: metadata/readability polish only; no source changes; no case changes; no metrics; no paper rendering; no reports/results migration; no release tag/export branch; no global leaderboard
Legacy repo modified: no
Release repo modified: yes

Summary:
- Performed a fast polish pass over the release-surface metadata skeleton.
- Canonicalized `LICENSE` formatting by moving the conservative copyright line outside the Apache-2.0 terms body.
- Kept `CITATION.cff` placeholder-safe and Apache-2.0 aligned.
- Checked public Markdown skeleton readability and removed task-oriented wording from small boundary passages.
- Checked `.gitignore` local-output policy: `runs/user/` ignored; all of `runs/` not ignored.

Files created:
- `audits/release_surface_metadata_polish_v0/README.md`
- `audits/release_surface_metadata_polish_v0/polished_files_inventory.csv`
- `audits/release_surface_metadata_polish_v0/readability_check.md`
- `audits/release_surface_metadata_polish_v0/license_citation_check.md`
- `audits/release_surface_metadata_polish_v0/protected_surface_check.md`
- `audits/release_surface_metadata_polish_v0/command_log.md`

Files modified:
- `LICENSE`
- `benchmark_spec/scope.md`
- `reports/README.md`
- `results/README.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- `git diff --check`: passed.
- `CITATION.cff` YAML syntax check: passed.
- Markdown sanity checks: passed.
- `.gitignore` policy check: passed.
- Protected-surface diff check: passed.

Task result:
- Metadata skeleton polish completed: yes.
- LICENSE canonicalized: yes.
- CITATION.cff valid: yes.
- Markdown readability check: passed.
- .gitignore check: passed.
- Source code modified: no.
- Scripts modified: no.
- Tests modified: no.
- Examples modified: no.
- Cases/manifests/schema/checker/validation/sql modified: no.
- `case_sets/` changed: no.
- Existing reports/results data changed beyond README boundaries: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Official metrics computed by this task: no.
- Paper tables rendered by this task: no.
- DB/checker execution run by this task: no.
- Timing/speedup computed by this task: no.
- Global leaderboard created: no.
- Release tag/export branch created: no.
- Commit hash: pending at commit time; final hash reported in task closeout.
- Push result: pending at commit time; final push result reported in task closeout.

Next safe action:
- Run final public-release metadata/readiness review before any release tag or export branch.

### 2026-05-21 · Final public-release metadata and readiness review

Mode: audit/review only; no source changes; no case changes; no metrics; no paper rendering; no reports/results migration; no release tag/export branch; no global leaderboard
Legacy repo modified: no
Release repo modified: yes

Summary:
- Created `audits/final_public_release_metadata_readiness_v0/`.
- Reviewed top-level README, LICENSE, CITATION, CONTRIBUTING, `.gitignore`, benchmark_spec, docs, examples, case_sets, cases, schemas, source/scripts/tests/workflows, reports/results boundary READMEs, and packaging metadata.
- Confirmed Common-core v0 remains 40 cases with pool split 16 PERF + 9 CONS + 9 PORT + 6 LONGTAIL.
- Confirmed Track A same-engine denominator remains 120 planned rows.
- Confirmed all 40 Common-core READMEs are present.
- Confirmed 40 external schema package directories are present.
- Verdict: `ready_for_final_closeout_planning`.

Files created:
- `audits/final_public_release_metadata_readiness_v0/README.md`
- `audits/final_public_release_metadata_readiness_v0/readiness_matrix.csv`
- `audits/final_public_release_metadata_readiness_v0/remaining_blockers.md`
- `audits/final_public_release_metadata_readiness_v0/public_surface_inventory.csv`
- `audits/final_public_release_metadata_readiness_v0/readiness_summary.json`
- `audits/final_public_release_metadata_readiness_v0/protected_surface_check.md`
- `audits/final_public_release_metadata_readiness_v0/command_log.md`
- `audits/final_public_release_metadata_readiness_v0/future_final_closeout_prompt.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- `git diff --check`: passed.
- `CITATION.cff` YAML syntax check: passed.
- Markdown sanity checks: passed.
- CSV/JSON parse checks: passed.
- `.gitignore` policy check: passed.
- Protected-surface diff check: passed.

Task result:
- Final metadata/readiness review completed: yes.
- Verdict: ready_for_final_closeout_planning.
- Remaining blockers to final closeout planning: none.
- Nonblocking caveats: Chinese README language posture before final public artifact; placeholder citation metadata; reports/results boundary-only status; deferred metrics/paper/timing/reproduction work; no release tag/export branch yet.
- Source code modified: no.
- Scripts modified: no.
- Tests modified: no.
- Docs modified: no.
- Examples modified: no.
- Cases/manifests/schema/checker/validation/sql modified: no.
- `case_sets/` changed: no.
- Existing reports/results data changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Official metrics computed by this task: no.
- Paper tables rendered by this task: no.
- DB/checker execution run by this task: no.
- Timing/speedup computed by this task: no.
- Global leaderboard created: no.
- Release tag/export branch created: no.
- Commit hash: pending at commit time; final hash reported in task closeout.
- Push result: pending at commit time; final push result reported in task closeout.

Next safe action:
- Run final public-release closeout planning before any release tag or export branch.

### 2026-05-21 · Final public-release closeout planning after metadata readiness

Mode: final closeout planning audit only; no source changes; no case changes; no metrics; no paper rendering; no reports/results migration; no release tag/export branch; no global leaderboard
Legacy repo modified: no
Release repo modified: yes

Summary:
- Created `audits/final_public_release_closeout_planning_v1/`.
- Reviewed Common-core 40 closeout rerun, `PERF_0077`/`PERF_0082` source-path follow-up, user-entry U0-U7 closeout, release-surface metadata polish, and final metadata readiness.
- Inspected current public release surface: top-level README, LICENSE, CITATION, CONTRIBUTING, `.gitignore`, benchmark_spec, docs, examples, source/scripts/tests/workflows, case_sets, representative cases, reports/results boundary READMEs, and packaging metadata.
- Confirmed Common-core v0 remains 40 cases with pool split 16 PERF + 9 CONS + 9 PORT + 6 LONGTAIL.
- Confirmed Track A same-engine denominator remains 120 planned rows.
- Verdict: `ready_for_export_planning`.

Files created:
- `audits/final_public_release_closeout_planning_v1/README.md`
- `audits/final_public_release_closeout_planning_v1/closeout_readiness_matrix.csv`
- `audits/final_public_release_closeout_planning_v1/nonblocking_caveats.md`
- `audits/final_public_release_closeout_planning_v1/deferred_work_register.md`
- `audits/final_public_release_closeout_planning_v1/export_readiness_recommendation.md`
- `audits/final_public_release_closeout_planning_v1/validation_results.csv`
- `audits/final_public_release_closeout_planning_v1/protected_surface_check.md`
- `audits/final_public_release_closeout_planning_v1/readiness_summary.json`
- `audits/final_public_release_closeout_planning_v1/future_export_planning_prompt.md`
- `audits/final_public_release_closeout_planning_v1/command_log.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- User-entry module help: passed.
- User-entry wrapper help: passed.
- `--explain-selection` smoke readability check: passed.
- `--show-output-schema` readability check: passed.
- `tests/user_entry`: passed with 70 passed and 1 skipped.
- Common-core v2 reference validator: passed for 40/40 cases.
- Legacy `validate_case_package.py --mode canonical-case`: not applicable to the current v2 clean-template package layout.
- `git diff --check`: passed.
- `CITATION.cff` YAML syntax check: passed.
- Markdown sanity checks: passed.
- CSV/JSON parse checks: passed.
- `.gitignore` policy check: passed.
- Protected-surface diff check: passed.

Task result:
- Final closeout planning packet created: yes.
- Verdict: ready_for_export_planning.
- Remaining blockers: none for export planning.
- Nonblocking caveats: Chinese README posture before final public artifact; placeholder citation metadata; `PERF_0077`/`PERF_0082` source-path provenance uncertainty; reports/results boundary-only status; deferred timing/official metrics/paper rendering/reproduction; MySQL/Spark fail-closed stubs only; no release tag/export branch yet.
- Source code modified: no.
- Scripts modified: no.
- Tests modified: no.
- Docs modified: no.
- Examples modified: no.
- Cases/manifests/schema/checker/validation/sql modified: no.
- `case_sets/` changed: no.
- Existing reports/results data changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Official metrics computed by this task: no.
- Paper tables rendered by this task: no.
- DB/checker execution run by this task: no live DB/checker.
- Timing/speedup computed by this task: no.
- Tag score/ranking created by this task: no.
- Global leaderboard created: no.
- Release tag/export branch created: no.
- Commit hash: pending at commit time; final hash reported in task closeout.
- Push result: pending at commit time; final push result reported in task closeout.

Next safe action:
- Run a separately authorized export/tag planning task before any release tag or export branch is created.

### 2026-05-21 · Run PostgreSQL Common-core local diagnostic trial with no-op adapter

Mode: bounded PostgreSQL-only user-entry local diagnostic trial; no official metrics; no timing/speedup; no paper rendering; no reports/results migration; no release tag/export branch; no global leaderboard
Legacy repo modified: no
Release repo modified: yes

Summary:
- Ran Common-core v0 PostgreSQL local diagnostic trial using `examples/user/noop_adapter.py`.
- Output path: `runs/user/common_core_pg_noop_db_checker/`.
- PostgreSQL environment ready: yes; `psql` available, required libpq env present, and `select 1` probe succeeded.
- Selected rows: 40.
- Candidate generated rows: 40.
- Candidate preflight passed rows: 40.
- Source-like rows: 40.
- Source executable rows: 35.
- Candidate executable rows: 35.
- Checker attempted rows: 35.
- Exact rows: 35.
- Mismatch rows: 0.
- Failure buckets: `none=35`, `source_execution_failed=5`.
- Failed cases: `PORT_0004`, `PORT_0013`, `PORT_0022`, `PORT_0024`, `PORT_0025`.
- Failure note: the five failures were PostgreSQL source execution failures on backtick-quoted dialect SQL; candidate execution and checker comparison were not attempted for those rows.

Files created:
- `audits/user_entry_common_core_pg_local_diagnostic_v0/README.md`
- `audits/user_entry_common_core_pg_local_diagnostic_v0/run_summary.json`
- `audits/user_entry_common_core_pg_local_diagnostic_v0/funnel_counts.csv`
- `audits/user_entry_common_core_pg_local_diagnostic_v0/failure_bucket_summary.csv`
- `audits/user_entry_common_core_pg_local_diagnostic_v0/tag_slice_summary.csv`
- `audits/user_entry_common_core_pg_local_diagnostic_v0/environment_check.md`
- `audits/user_entry_common_core_pg_local_diagnostic_v0/command_log.md`
- `audits/user_entry_common_core_pg_local_diagnostic_v0/protected_surface_check.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- `git diff --check`: passed.
- CSV/JSON parse checks for new audit files: passed.
- Markdown sanity checks for audit Markdown files: passed.
- Protected-surface diff check: passed.
- Local run output staging check: passed; `runs/user/common_core_pg_noop_db_checker/` is ignored local output and was not staged.

Task result:
- PostgreSQL Common-core local diagnostic trial completed: yes.
- Local diagnostic only: yes.
- Official metrics computed by this task: no.
- Timing/speedup computed by this task: no.
- Paper tables rendered by this task: no.
- Reports/results updated by this task: no.
- Global leaderboard created: no.
- Cases/manifests/schema/checker/validation/sql modified: no.
- `case_sets/` changed: no.
- Existing reports/results data changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Local run outputs committed: no; `runs/user/common_core_pg_noop_db_checker/` remains ignored local diagnostic output.
- Commit hash: pending at commit time; final hash reported in task closeout.
- Push result: pending at commit time; final push result reported in task closeout.

Next safe action:
- Inspect and triage the five PORT PostgreSQL source-execution failures as a future local diagnostic compatibility task; do not treat this run as official metrics or paper results.

### 2026-05-21 · Triage five PORT PostgreSQL source-execution failures from Common-core local diagnostic run

Mode: local diagnostic triage/audit only; no case SQL edits; no manifest/schema/checker/validation edits; no official metrics; no timing/speedup; no paper rendering; no reports/results migration; no release tag/export branch; no global leaderboard
Legacy repo modified: no
Release repo modified: yes

Summary:
- Reviewed target cases: `PORT_0004`, `PORT_0013`, `PORT_0022`, `PORT_0024`, and `PORT_0025`.
- PostgreSQL environment ready: yes; `psql` available and libpq environment probe passed.
- Targeted five-case run completed under ignored local path `runs/user/port_pg_source_failure_triage/`.
- Selected rows: 5.
- Candidate generated rows: 5.
- Candidate preflight passed rows: 5.
- Source executable rows: 0.
- Candidate executable rows: 0.
- Checker attempted rows: 0.
- Exact rows: 0.
- Mismatch rows: 0.
- Failure buckets: `source_execution_failed=5`.
- Root cause summary: the retained PORT `sql/source.sql` files are `mysql_like_candidate` SQL with backtick quoting and related dialect syntax, while the current PostgreSQL local diagnostic runner executes `sql/source.sql` directly without engine-aware source/dialect variant selection.
- PostgreSQL dialect variants: no target case has `sql/dialect_variants/postgres/...`; `PORT_0004` and `PORT_0013` have Spark-only dialect variants; all five have PostgreSQL-like `pos_01.sql` files declared as positive rewrites rather than PostgreSQL source-oracle variants.

Files created:
- `audits/user_entry_port_pg_source_failure_triage_v0/README.md`
- `audits/user_entry_port_pg_source_failure_triage_v0/case_failure_triage.csv`
- `audits/user_entry_port_pg_source_failure_triage_v0/variant_inventory.csv`
- `audits/user_entry_port_pg_source_failure_triage_v0/targeted_run_summary.json`
- `audits/user_entry_port_pg_source_failure_triage_v0/error_excerpt_log.md`
- `audits/user_entry_port_pg_source_failure_triage_v0/root_cause_analysis.md`
- `audits/user_entry_port_pg_source_failure_triage_v0/future_variant_selection_prompt.md`
- `audits/user_entry_port_pg_source_failure_triage_v0/protected_surface_check.md`
- `audits/user_entry_port_pg_source_failure_triage_v0/command_log.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- `git diff --check`: passed.
- CSV parse checks for audit CSV files: passed.
- JSON parse check for `targeted_run_summary.json`: passed.
- Markdown sanity checks for audit Markdown files: passed.
- Protected-surface diff/status check: passed.
- Local run output cleanup check: passed; `runs/user/port_pg_source_failure_triage/` is absent and not staged.

Task result:
- Five PORT PostgreSQL source-execution failures triaged: yes.
- Failures reproduced: yes.
- Recommended next safe action: design engine-aware source/dialect variant selection or explicit manifest source-role metadata before implementation or case edits.
- Source code modified: no.
- Scripts modified: no.
- Tests modified: no.
- Docs modified: no.
- Examples modified: no.
- Cases/manifests/schema/checker/validation/sql modified: no.
- `case_sets/` changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Official metrics computed by this task: no.
- Timing/speedup computed by this task: no.
- Global leaderboard created: no.
- Local run outputs committed: no.
- Commit hash: pending at commit time; final hash reported in task closeout.
- Push result: pending at commit time; final push result reported in task closeout.

Next safe action:
- Create a design-only engine-aware source/dialect variant selection packet for user-entry PostgreSQL PORT diagnostics, then seek maintainer approval before any source code or manifest/case changes.

### 2026-05-21 · Record PORT cross-dialect diagnostic execution subplan and policy decision

Mode: project-control planning and decision recording only; no source code changes; no case/manifest/source edits; no MySQL/Spark implementation; no official metrics; no timing/speedup; no paper rendering; no reports/results migration; no release tag/export branch; no global leaderboard
Legacy repo modified: no
Release repo modified: yes

Summary:
- Recorded `project_control/PORT_CROSS_DIALECT_DIAGNOSTIC_EXECUTION_PLAN.md`.
- Added decision D031: `PORT cross-dialect diagnostics require explicit manifest roles and fail-closed runner behavior`.
- Plan records that PORT cross-dialect local diagnostics require explicit manifest role metadata and must not infer roles from file names or SQL text.
- Plan records that `pos_01.sql` must not be used as a PostgreSQL source oracle unless explicitly declared by manifest metadata or separately approved policy.
- Plan records same-engine local diagnostic behavior as the default for cases without cross-dialect metadata.
- Plan records MySQL source-side execution as future required implementation for MySQL-like PORT source reference diagnostics.
- Plan records Spark execution as deferred unless separately authorized.
- Plan records protection for PERF / CONS / LONGTAIL same-engine behavior and regression coverage expectations.

Files created:
- `project_control/PORT_CROSS_DIALECT_DIAGNOSTIC_EXECUTION_PLAN.md`
- `audits/port_cross_dialect_diagnostic_execution_plan_v0/README.md`
- `audits/port_cross_dialect_diagnostic_execution_plan_v0/execution_subplan_summary.csv`
- `audits/port_cross_dialect_diagnostic_execution_plan_v0/decision_traceability.md`
- `audits/port_cross_dialect_diagnostic_execution_plan_v0/protected_surface_check.md`
- `audits/port_cross_dialect_diagnostic_execution_plan_v0/command_log.md`

Files modified:
- `project_control/DECISION_LOG.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- `git diff --check`: passed.
- CSV parse check for `execution_subplan_summary.csv`: passed.
- Markdown sanity checks for new project-control and audit Markdown files: passed.
- Protected-surface status check: passed.
- `runs/user/` check: no output created by this task; existing ignored local output remains untracked and unstaged.

Task result:
- PORT cross-dialect diagnostic execution subplan recorded: yes.
- Decision log updated: yes, D031.
- No implementation performed: yes.
- No case/manifest/source changes performed: yes.
- MySQL execution remains future implementation: yes.
- Spark remains deferred: yes.
- Source code modified: no.
- Scripts modified: no.
- Tests modified: no.
- Docs outside `project_control` modified: no.
- Examples modified: no.
- Cases/manifests/schema/checker/validation/sql modified: no.
- `case_sets/` changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Official metrics computed by this task: no.
- DB/checker execution run by this task: no.
- Timing/speedup computed by this task: no.
- Global leaderboard created: no.
- Release tag/export branch created: no.
- Commit hash: pending at commit time; final hash reported in task closeout.
- Push result: pending at commit time; final push result reported in task closeout.

Next safe action:
- Design exact manifest role metadata and validation expectations for PORT cross-dialect local diagnostics before any manifest or runner edits.

### 2026-05-21 · P1 design PORT-wide cross-dialect manifest role metadata

Mode: design/audit only; no source code changes; no case/manifest/source edits; no MySQL/Spark implementation; no live DB/checker execution; no official metrics; no timing/speedup; no paper rendering; no reports/results migration; no release tag/export branch; no global leaderboard
Legacy repo modified: no
Release repo modified: yes

Summary:
- Reviewed all 9 Common-core PORT cases: `PORT_0003`, `PORT_0004`, `PORT_0005`, `PORT_0008`, `PORT_0012`, `PORT_0013`, `PORT_0022`, `PORT_0024`, and `PORT_0025`.
- Classified 4 cases as same-engine compatible for PostgreSQL local diagnostics: `PORT_0003`, `PORT_0005`, `PORT_0008`, and `PORT_0012`.
- Classified 5 cases as cross-dialect reference required: `PORT_0004`, `PORT_0013`, `PORT_0022`, `PORT_0024`, and `PORT_0025`.
- Designed additive `local_diagnostic` manifest role metadata with explicit `diagnostic_mode`, `source_reference`, `target_candidate`, optional `target_reference`, checker comparison, and local-only boundary fields.
- Recorded strict non-guessing policy: no role inference from file names, SQL text, or pool name; `pos_01.sql` must not become a source oracle unless explicitly declared by policy/metadata.
- Preserved MySQL source-side execution as future required implementation for MySQL-like PORT source references.
- Preserved Spark execution as deferred.
- Recorded non-PORT regression protection for PERF / CONS / LONGTAIL same-engine behavior.

Files created:
- `audits/port_cross_dialect_manifest_role_design_v0/README.md`
- `audits/port_cross_dialect_manifest_role_design_v0/port_case_role_matrix.csv`
- `audits/port_cross_dialect_manifest_role_design_v0/proposed_manifest_schema.md`
- `audits/port_cross_dialect_manifest_role_design_v0/field_definition_matrix.csv`
- `audits/port_cross_dialect_manifest_role_design_v0/validation_expectations.md`
- `audits/port_cross_dialect_manifest_role_design_v0/runner_consumption_contract.md`
- `audits/port_cross_dialect_manifest_role_design_v0/non_port_regression_protection.md`
- `audits/port_cross_dialect_manifest_role_design_v0/five_failure_mapping.md`
- `audits/port_cross_dialect_manifest_role_design_v0/future_p2_manifest_patch_prompt.md`
- `audits/port_cross_dialect_manifest_role_design_v0/protected_surface_check.md`
- `audits/port_cross_dialect_manifest_role_design_v0/command_log.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- `git diff --check`: passed.
- CSV parse checks for new audit CSV files: passed.
- Markdown sanity checks for new audit Markdown files: passed.
- Protected-surface diff/status check: passed.
- `runs/user/` check: no output created by this task.

Task result:
- P1 PORT-wide manifest role design completed: yes.
- All 9 PORT cases reviewed: yes.
- Verdict: `ready_for_manifest_metadata_patch`.
- Proposed manifest schema created: yes.
- Field definition matrix created: yes.
- Validation expectations created: yes.
- Runner consumption contract created: yes.
- Non-PORT regression protection created: yes.
- Future P2 manifest patch prompt created: yes.
- Source code modified: no.
- Scripts modified: no.
- Tests modified: no.
- Docs outside `project_control` modified: no.
- Examples modified: no.
- Cases/manifests/schema/checker/validation/sql modified: no.
- `case_sets/` changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Official metrics computed by this task: no.
- DB/checker execution run by this task: no.
- Timing/speedup computed by this task: no.
- Global leaderboard created: no.
- Release tag/export branch created: no.
- Commit hash: pending at commit time; final hash reported in task closeout.
- Push result: pending at commit time; final push result reported in task closeout.

Next safe action:
- Authorize P2 metadata-only manifest patches for all 9 Common-core PORT cases after reviewing this design; do not edit SQL, runner code, metrics, reports/results, or denominators in P2.

### 2026-05-21 · P2 add PORT local-diagnostic role metadata to all Common-core PORT manifests

Mode: metadata-only manifest patching; no SQL edits; no source code changes; no MySQL/Spark implementation; no cross-dialect runner behavior implementation; no live DB/checker execution; no official metrics; no timing/speedup; no paper rendering; no reports/results migration; no release tag/export branch; no global leaderboard
Legacy repo modified: no
Release repo modified: yes

Summary:
- Patched all 9 Common-core PORT manifests with additive `local_diagnostic` role metadata.
- Assigned `diagnostic_mode: same_engine` to `PORT_0003`, `PORT_0005`, `PORT_0008`, and `PORT_0012`.
- Assigned `diagnostic_mode: cross_dialect_reference` to `PORT_0004`, `PORT_0013`, `PORT_0022`, `PORT_0024`, and `PORT_0025`.
- Cross-dialect cases declare `source_reference.engine: mysql`, `source_reference.query: sql/source.sql`, `target_candidate.engine: postgres`, and optional `target_reference` as PostgreSQL `positive_reference` / sanity control only.
- Same-engine cases declare PostgreSQL source-reference and target-candidate roles and omit `target_reference`.
- `pos_01.sql` was not made a source oracle.
- MySQL source-side execution remains future required implementation for MySQL-like source references.
- Spark remains deferred.

Manifest files modified:
- `cases/PORT/PORT_0003/manifest.yaml`
- `cases/PORT/PORT_0004/manifest.yaml`
- `cases/PORT/PORT_0005/manifest.yaml`
- `cases/PORT/PORT_0008/manifest.yaml`
- `cases/PORT/PORT_0012/manifest.yaml`
- `cases/PORT/PORT_0013/manifest.yaml`
- `cases/PORT/PORT_0022/manifest.yaml`
- `cases/PORT/PORT_0024/manifest.yaml`
- `cases/PORT/PORT_0025/manifest.yaml`

Files created:
- `audits/port_cross_dialect_manifest_metadata_patch_v0/README.md`
- `audits/port_cross_dialect_manifest_metadata_patch_v0/patched_port_manifest_summary.csv`
- `audits/port_cross_dialect_manifest_metadata_patch_v0/manifest_diff_review.md`
- `audits/port_cross_dialect_manifest_metadata_patch_v0/non_port_regression_check.md`
- `audits/port_cross_dialect_manifest_metadata_patch_v0/future_p3_runner_consumption_prompt.md`
- `audits/port_cross_dialect_manifest_metadata_patch_v0/protected_surface_check.md`
- `audits/port_cross_dialect_manifest_metadata_patch_v0/command_log.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- `git diff --check`: passed.
- YAML parse checks for all 9 patched manifests: passed.
- Static local-diagnostic semantic checks for all 9 patched manifests: passed.
- Static v2 case-package validator: 31/40 Common-core cases passed; the 9 patched PORT cases failed only because the current validator does not yet whitelist the new top-level `local_diagnostic` block (`local_diagnostic: unapproved top-level key`). Source/test validator updates are deferred because P2 is metadata-only.
- Legacy canonical-case validator: non-applicable to the current clean v2 layout; it still expects v1-era paths intentionally absent from clean v2 packages.
- Changed-file checks passed: exactly 9 PORT manifests changed; no SQL files changed; no non-PORT manifests changed; `case_sets/`, reports/results, and denominator scaffolds unchanged.
- CSV and Markdown checks for audit files: passed.
- Protected-surface status check: passed.
- `runs/user/` check: no output created by this task.

Task result:
- P2 PORT manifest metadata patch completed: yes.
- All 9 PORT manifests patched: yes.
- SQL files modified: no.
- Runner/source code modified: no.
- Non-PORT manifests modified: no.
- `case_sets/` changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Official metrics computed by this task: no.
- DB/checker execution run by this task: no.
- Timing/speedup computed by this task: no.
- Global leaderboard created: no.
- Commit hash: pending at commit time; final hash reported in task closeout.
- Push result: pending at commit time; final push result reported in task closeout.

Next safe action:
- Authorize P3 runner metadata consumption and static validator support as a separate fail-closed task; do not implement MySQL execution, SQL edits, official metrics, timing, reports/results, or leaderboard unless separately approved.

## 2026-05-21 - port_cross_dialect_runner_metadata_consumption_v0

P3 runner metadata consumption and validator support completed on branch `feature/case-package-v2-external-schema`.

Summary:
- Static v2 validators now accept and validate top-level `local_diagnostic` metadata.
- All 9 Common-core PORT manifests validate with `local_diagnostic`.
- Resolver exposes diagnostic role metadata.
- User-entry runner/router consumes `diagnostic_mode`.
- Five cross-dialect PORT cases fail closed with missing MySQL source-reference backend instead of PostgreSQL source syntax failures.
- PERF/CONS/LONGTAIL same-engine defaults remain unaffected.
- MySQL/Spark live execution remains unimplemented.
- No SQL edits, manifest edits, case_set changes, reports/results changes, denominator changes, paper result changes, case membership changes, or raw legacy evidence changes.
- No official metrics, timing/speedup, paper rendering, or leaderboard.

Validation:
- Targeted P3 tests passed.
- `tests/user_entry` passed.
- `tests/case_package_v2` passed.
- All 9 PORT static v2 validators passed.
- All 40 Common-core static v2 validators passed.
- Targeted five-case local diagnostic produced `cross_dialect_backend_missing=5` and no PostgreSQL source syntax errors.

Next safe action:
- Decide whether to authorize a narrow MySQL source-reference local diagnostic backend task; otherwise keep declared cross-dialect PORT rows fail-closed and local-only.

## 2026-05-21 - port_cross_dialect_mysql_backend_v0

P4 bounded MySQL source-reference local diagnostic backend completed on branch `feature/case-package-v2-external-schema`.

Summary:
- Implemented MySQL source-reference execution for manifest-declared cross-dialect PORT diagnostics using the `mysql` CLI and explicit local environment configuration.
- MySQL schema assets resolve only from `engines.mysql` external schema metadata; PostgreSQL schema assets are not used for MySQL.
- Cross-dialect runner behavior now executes MySQL source-reference first, then PostgreSQL target candidate only after source success.
- Same-engine MySQL remains fail-closed; Spark remains deferred.
- Targeted five-case run with missing MySQL config produced `mysql_config_missing=5` / `cross_dialect_backend_missing=5` and no PostgreSQL source syntax failures.
- Live MySQL diagnostic was not run because `SQLRB_MYSQL_HOST`, `SQLRB_MYSQL_PORT`, and `SQLRB_MYSQL_USER` were not configured.
- No SQL edits, manifest edits, schema/checker/validation edits, case_set changes, reports/results changes, denominator changes, paper result changes, case membership changes, or raw legacy evidence changes.
- No official metrics, timing/speedup, paper rendering, or leaderboard.

Validation:
- `git diff --check` passed.
- Py_compile for modified source files passed.
- Help/readability commands passed.
- Public smoke dry-run and adapter-capture passed; run outputs removed.
- `PYTHONPATH=src pytest tests/user_entry` passed with 80 passed and 1 skipped.
- PORT local-diagnostic metadata validation test passed.

Next safe action:
- Configure a local MySQL environment and run a targeted live source-reference diagnostic, or test a controlled PostgreSQL-target adapter for cross-dialect PORT rows; do not compute metrics, timing, reports/results, or leaderboard outputs.

## 2026-05-21 - local_engine_env_setup_v0

Local engine environment setup layer completed on branch `feature/case-package-v2-external-schema`.

Mode: environment setup/documentation helper only; no DB execution backend changes; no case/manifest/source edits; no Spark execution implementation; no live diagnostic run beyond the local environment checker; no official metrics; no timing/speedup; no reports/results updates; no release tag/export branch; no global leaderboard.

Summary:
- Added `docs/LOCAL_ENGINE_SETUP.md` with PostgreSQL, MySQL, Spark, security, and local-only boundary documentation.
- Added PostgreSQL/MySQL/Spark example environment templates and an all-engine convenience source template.
- Added `scripts/dev/check_local_engine_env.py`, a non-mutating local environment checker that reports client/config readiness and optionally probes configured PostgreSQL/MySQL clients without printing passwords.
- Updated `.gitignore` narrowly for `scripts/env_*.local.sh`, `.env`, and `.env.local`; preserved `runs/user/` as ignored local output and did not ignore all of `runs/`.
- Created audit packet `audits/local_engine_env_setup_v0/`.
- MySQL live diagnostic still requires a local user to copy/edit `scripts/env_mysql.local.sh` and provide a user with create/drop permissions for temporary diagnostic databases.
- Spark remains deferred/fail-closed.
- No source DB execution logic under `src/` was modified.
- No cases, manifests, SQL, schemas, checkers, validation files, `case_sets/`, reports/results, benchmark specs, repository specs, raw evidence, denominators, paper results, official metrics, timing/speedup, or leaderboard changed.

Files created:
- `docs/LOCAL_ENGINE_SETUP.md`
- `scripts/env_postgres.example.sh`
- `scripts/env_mysql.example.sh`
- `scripts/env_spark.example.sh`
- `scripts/env_all.example.sh`
- `scripts/dev/check_local_engine_env.py`
- `audits/local_engine_env_setup_v0/README.md`
- `audits/local_engine_env_setup_v0/env_files_inventory.csv`
- `audits/local_engine_env_setup_v0/engine_env_check_result.md`
- `audits/local_engine_env_setup_v0/protected_surface_check.md`
- `audits/local_engine_env_setup_v0/command_log.md`

Files modified:
- `.gitignore`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `git diff --check`: passed.
- `bash -n scripts/env_postgres.example.sh`: passed.
- `bash -n scripts/env_mysql.example.sh`: passed.
- `bash -n scripts/env_spark.example.sh`: passed.
- `bash -n scripts/env_all.example.sh`: passed.
- `PYTHONPATH=src python -m py_compile scripts/dev/check_local_engine_env.py`: passed.
- `python scripts/dev/check_local_engine_env.py`: passed; reported missing PostgreSQL/MySQL config as optional local setup state and Spark as deferred/fail-closed.
- `.gitignore` checks passed: `runs/user/` ignored, whole `runs/` not ignored, and `scripts/env_mysql.local.sh` ignored.
- Protected-surface check passed.
- `runs/user/` outputs created by this task: no.

Task result:
- Local engine env setup added: yes.
- Env example files created: yes.
- Local engine check helper created: yes.
- `.gitignore` updated: yes.
- Source execution code modified: no.
- Cases/manifests/SQL/schema/checker/validation modified: no.
- `case_sets/` changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Raw legacy evidence changed: no.
- Official metrics computed: no.
- Timing/speedup computed: no.
- Global leaderboard created: no.
- Commit hash: pending at commit time; final hash reported in task closeout.
- Push result: pending at commit time; final push result reported in task closeout.

Next safe action:
- Copy the relevant `scripts/env_*.example.sh` file to `scripts/env_*.local.sh`, edit local credentials, source it, and run `python scripts/dev/check_local_engine_env.py`; any subsequent live MySQL source-reference diagnostic must remain local-only with no metrics, timing, reports/results, or leaderboard outputs.

## 2026-05-21 - port_cross_dialect_mysql_live_diagnostic_v0

Live MySQL source-reference diagnostic completed on branch `feature/case-package-v2-external-schema`.

Mode: bounded local diagnostic only; no official metrics; no timing/speedup; no reports/results updates; no retained-evidence promotion; no release tag/export branch; no global leaderboard.

Summary:
- Target cases: `PORT_0004`, `PORT_0013`, `PORT_0022`, `PORT_0024`, and `PORT_0025`.
- PostgreSQL environment ready: yes.
- MySQL environment ready: yes.
- Spark status: deferred/fail-closed.
- Local run output path: `runs/user/port_mysql_source_reference_live/`.
- Selected rows: 5.
- Candidate generated rows: 5.
- Candidate preflight passed rows: 5.
- MySQL source-reference attempted rows: 5.
- MySQL source-reference executable rows: 5.
- MySQL source-reference failed rows: 0.
- PostgreSQL target-candidate attempted rows: 5.
- PostgreSQL target-candidate executable rows: 0.
- PostgreSQL target-candidate failed rows: 5.
- Checker attempted rows: 0.
- Exact rows: 0.
- Mismatch rows: 0.
- Failure buckets: `candidate_execution_failed=5`.
- Failure classification: target-related only; no connection, config, schema, source-reference, or checker failures were observed.
- Interpretation: the no-op adapter emitted source-like MySQL SQL, so target PostgreSQL candidate failure is a local diagnostic outcome and not an official method failure.

Files created:
- `audits/port_cross_dialect_mysql_live_diagnostic_v0/README.md`
- `audits/port_cross_dialect_mysql_live_diagnostic_v0/environment_check.md`
- `audits/port_cross_dialect_mysql_live_diagnostic_v0/live_run_summary.json`
- `audits/port_cross_dialect_mysql_live_diagnostic_v0/source_reference_execution_summary.csv`
- `audits/port_cross_dialect_mysql_live_diagnostic_v0/target_candidate_outcome_summary.csv`
- `audits/port_cross_dialect_mysql_live_diagnostic_v0/failure_bucket_summary.csv`
- `audits/port_cross_dialect_mysql_live_diagnostic_v0/artifact_inventory.csv`
- `audits/port_cross_dialect_mysql_live_diagnostic_v0/command_log.md`
- `audits/port_cross_dialect_mysql_live_diagnostic_v0/protected_surface_check.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- JSON parse check for audit summary: passed.
- CSV parse checks for audit CSVs: passed.
- Markdown sanity checks for audit Markdown files: passed.
- Protected-surface diff check: passed.
- `git diff --check`: passed.
- Local run outputs under `runs/user/port_mysql_source_reference_live/` remained ignored and unstaged.

Task result:
- Live diagnostic run completed: yes.
- Local run outputs committed: no.
- Source code modified: no.
- Cases/manifests/SQL/schema/checker/validation modified: no.
- `case_sets/` changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Official metrics computed: no.
- Timing/speedup computed: no.
- Global leaderboard created: no.

Next safe action:
- Run a controlled PostgreSQL-target adapter diagnostic for these five cross-dialect PORT rows, or close the MySQL source-reference diagnostic path as locally validated; do not compute metrics, timing, reports/results, or leaderboard outputs.

## 2026-05-21 - port_cross_dialect_pg_target_reference_diagnostic_v0

Controlled PostgreSQL target-reference diagnostic completed on branch `feature/case-package-v2-external-schema`.

Mode: bounded local diagnostic only; controlled adapter is not a user method, not a benchmark baseline, not a source oracle, and not a metric or paper-result input. No official metrics; no timing/speedup; no reports/results updates; no retained-evidence promotion; no release tag/export branch; no global leaderboard.

Summary:
- Target cases: `PORT_0004`, `PORT_0013`, `PORT_0022`, `PORT_0024`, and `PORT_0025`.
- Controlled adapter added: `examples/user/port_postgres_target_reference_adapter.py`.
- Adapter behavior: reads `SQLRB_CASE_DIR` and `SQLRB_CANDIDATE_SQL_PATH`, requires cross-dialect `local_diagnostic.target_reference` metadata, and copies only the manifest-declared PostgreSQL positive target reference query.
- PostgreSQL environment ready: yes.
- MySQL environment ready: yes.
- Spark status: deferred/fail-closed.
- Local run output path: `runs/user/port_pg_target_reference_controlled/`.
- Selected rows: 5.
- Candidate generated rows: 5.
- Candidate preflight passed rows: 5.
- MySQL source-reference attempted rows: 5.
- MySQL source-reference executable rows: 5.
- MySQL source-reference failed rows: 0.
- PostgreSQL target-candidate attempted rows: 5.
- PostgreSQL target-candidate executable rows: 5.
- PostgreSQL target-candidate failed rows: 0.
- Checker attempted rows: 5.
- Exact rows: 1.
- Mismatch rows: 4.
- Failure buckets: `mismatch=4`, `none=1`.
- Failure classification: no source, target, schema, connection, or config failures; observed mismatches are checker/normalization comparison outcomes after both DB executions succeeded.

Files created:
- `examples/user/port_postgres_target_reference_adapter.py`
- `tests/user_entry/test_port_target_reference_adapter.py`
- `audits/port_cross_dialect_pg_target_reference_diagnostic_v0/README.md`
- `audits/port_cross_dialect_pg_target_reference_diagnostic_v0/environment_check.md`
- `audits/port_cross_dialect_pg_target_reference_diagnostic_v0/controlled_adapter_summary.md`
- `audits/port_cross_dialect_pg_target_reference_diagnostic_v0/live_run_summary.json`
- `audits/port_cross_dialect_pg_target_reference_diagnostic_v0/source_reference_execution_summary.csv`
- `audits/port_cross_dialect_pg_target_reference_diagnostic_v0/target_candidate_execution_summary.csv`
- `audits/port_cross_dialect_pg_target_reference_diagnostic_v0/checker_outcome_summary.csv`
- `audits/port_cross_dialect_pg_target_reference_diagnostic_v0/failure_bucket_summary.csv`
- `audits/port_cross_dialect_pg_target_reference_diagnostic_v0/artifact_inventory.csv`
- `audits/port_cross_dialect_pg_target_reference_diagnostic_v0/command_log.md`
- `audits/port_cross_dialect_pg_target_reference_diagnostic_v0/protected_surface_check.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation:
- `PYTHONPATH=src python -m py_compile examples/user/port_postgres_target_reference_adapter.py`: passed.
- `PATH=/tmp/sqlrb_pytest_venv/bin:$PATH PYTHONPATH=src pytest tests/user_entry/test_port_target_reference_adapter.py`: passed, 3 tests.
- `PATH=/tmp/sqlrb_pytest_venv/bin:$PATH PYTHONPATH=src pytest tests/user_entry`: passed, 82 passed and 2 skipped after installing `pytest` and `PyYAML` in a temporary `/tmp` virtualenv.
- JSON parse check for audit summary: passed.
- CSV parse checks for audit CSVs: passed.
- Markdown sanity checks for audit Markdown files: passed.
- Protected-surface diff check: passed.
- `git diff --check`: passed.
- Local run outputs under `runs/user/port_pg_target_reference_controlled/` remained ignored and unstaged.

Task result:
- Controlled diagnostic run completed: yes.
- Local run outputs committed: no.
- Source code under `src/` modified: no.
- Cases/manifests/SQL/schema/checker/validation modified: no.
- `case_sets/` changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Official metrics computed: no.
- Timing/speedup computed: no.
- Global leaderboard created: no.

Next safe action:
- Review checker normalization/column-label policy for cross-dialect result comparison before any checker behavior changes; do not compute metrics, timing, reports/results, or leaderboard outputs from this diagnostic.

## 2026-05-21 - port_cross_dialect_checker_normalization_audit_v0

Cross-dialect checker normalization audit completed on branch `feature/case-package-v2-external-schema`.

Mode: audit/triage only. No checker behavior changed. No SQL, manifests, cases, schemas, checker configs, validation files, source code, reports/results, denominator scaffolds, paper results, case membership, raw legacy evidence, timing/speedup, official metrics, or leaderboard outputs were changed.

Summary:
- Audited cases: `PORT_0004`, `PORT_0013`, `PORT_0022`, `PORT_0024`, and `PORT_0025`.
- Controlled diagnostic artifacts available: yes; rerun required: no.
- PostgreSQL environment ready: yes.
- MySQL environment ready: yes.
- Prior controlled run outcome: source-reference execution 5/5, target-candidate execution 5/5, checker attempted 5, exact 1, mismatch 4.
- `PORT_0004`: column-label normalization policy gap; row counts 1/1 and scalar values match after ignoring labels.
- `PORT_0013`: column-label normalization policy gap; row counts 1/1 and scalar values match after ignoring labels.
- `PORT_0022`: column-label plus decimal-string normalization policy gap; row counts 1/1 and scalar values are decimal-equivalent.
- `PORT_0024`: column-label plus decimal-string normalization policy gap; row counts 1/1 and scalar values are decimal-equivalent.
- `PORT_0025`: exact comparison explained by matching `account_id` column label and value `2`.
- No inspected mismatch is classified as a source, target, schema, connection, date/time, boolean, null, row-order, or multiset issue.
- Audit packet created under `audits/port_cross_dialect_checker_normalization_audit_v0/`.
- Local run outputs under `runs/user/port_pg_target_reference_controlled/` remained ignored and unstaged.

Validation:
- `git diff --check`: passed.
- CSV parse checks for audit CSV files: passed.
- Markdown sanity checks for audit Markdown files: passed.
- Protected-surface diff check: passed.
- Local run outputs not staged: confirmed.

Next safe action:
- Authorize a narrow future checker-normalization task only if desired. It should add explicit opt-in cross-dialect comparison policy and tests proving PERF, CONS, and LONGTAIL same-engine behavior remains unaffected; do not compute metrics, timing, reports/results, or leaderboard outputs.

## 2026-05-21 - port_cross_dialect_checker_normalization_v0

Opt-in cross-dialect checker normalization completed on branch `feature/case-package-v2-external-schema`.

Mode: local diagnostic checker behavior only. No official metrics, timing/speedup, reports/results updates, retained-evidence promotion, denominator changes, paper-result changes, case membership changes, raw legacy evidence changes, release tag/export branch, or leaderboard outputs.

Implementation summary:
- Added resolved manifest checker comparison metadata to `case_package_resolver.py`.
- `user_run.py` enables cross-dialect checker normalization only when `local_diagnostic.diagnostic_mode == cross_dialect_reference` and `local_diagnostic.checker.comparison == source_reference_result_to_target_candidate_result`.
- `local_result_checker.py` keeps strict JSON object equality as the default path.
- For the explicit opt-in path only, the checker compares values by artifact column position after row/column count checks and treats decimal-equivalent numeric strings as equal.
- Checker details now record whether cross-dialect normalization was active, positional comparison was used, decimal string equivalence was used, and the remaining mismatch reason if any.

Controlled diagnostic outcome:
- Local run output path: `runs/user/port_pg_target_reference_normalized/`.
- Selected rows: 5.
- MySQL source-reference executable rows: 5.
- PostgreSQL target-candidate executable rows: 5.
- Checker attempted rows: 5.
- Exact rows: 5.
- Mismatch rows: 0.
- The four prior normalization-gap mismatches (`PORT_0004`, `PORT_0013`, `PORT_0022`, `PORT_0024`) became exact under the opt-in policy; `PORT_0025` remained exact.

Regression and validation:
- Targeted checker/metadata tests: 28 passed.
- Full `tests/user_entry`: 95 passed and 2 skipped using the existing `/tmp/sqlrb_pytest_venv` pytest/PyYAML environment.
- Current v2 static case-package reference validation: passed for all 40 Common-core case paths.
- Legacy `validate_case_package.py --mode canonical-case/full-case` remains non-applicable to the current clean v2 package layout because it expects v1-era paths.
- `git diff --check`, py_compile, environment check, help commands, CSV/JSON/Markdown sanity checks, protected-surface check, and local run-output staging check passed.

Changed files:
- `src/sql_rewrite_bench/local_result_checker.py`
- `src/sql_rewrite_bench/case_package_resolver.py`
- `src/sql_rewrite_bench/user_run.py`
- `tests/user_entry/test_cross_dialect_checker_normalization.py`
- `audits/port_cross_dialect_checker_normalization_v0/*`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected surfaces:
- SQL files modified: no.
- Manifest files modified: no.
- Checker config files modified: no.
- Schema/validation files modified: no.
- `case_sets/` changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Raw legacy evidence changed: no.
- Local run outputs committed: no.

Next safe action:
- Review the opt-in checker details and controlled rerun artifacts; keep this local-diagnostic exactness separate from official metrics, timing, reports/results, paper results, and leaderboard outputs.

## 2026-05-21 - port_cross_dialect_local_diagnostic_closeout_v0

PORT cross-dialect local diagnostic closeout completed on branch `feature/case-package-v2-external-schema`.

Mode: audit/closeout only. Verdict: `closed_for_current_user_entry_phase`.

Summary:
- All 9 Common-core PORT cases are covered by explicit `local_diagnostic` metadata.
- Same-engine PORT cases remain `PORT_0003`, `PORT_0005`, `PORT_0008`, and `PORT_0012`.
- Cross-dialect PORT cases remain `PORT_0004`, `PORT_0013`, `PORT_0022`, `PORT_0024`, and `PORT_0025`.
- The five cross-dialect cases have MySQL source-reference live validation, controlled PostgreSQL target-candidate validation, and checker exact 5/5 in the normalized controlled diagnostic.
- Opt-in checker normalization remains gated to cross-dialect local diagnostics; PERF, CONS, LONGTAIL, and same-engine PORT defaults remain protected.
- Deferred work: real PORT user-adapter evaluation, Spark live execution, timing/speedup, official metrics, paper rendering, reports/results migration, retained-evidence integration, and release tag/export branch work.

Boundary:
- Checker behavior changed: no.
- Source code changed: no.
- SQL, manifest, case, schema, checker config, and validation files changed: no.
- `case_sets/` changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Official metrics computed: no.
- Timing/speedup computed: no.
- Global leaderboard created: no.
- Release tag/export branch created: no.
- `runs/user/` outputs created or committed by closeout: no.

Validation:
- `git diff --check`: passed.
- CSV/JSON parse checks for new audit files: passed.
- Markdown sanity checks for new audit files: passed.
- Protected-surface diff check: passed.
- Local run outputs not staged: confirmed.

Next safe action:
- Return to the main user-entry roadmap; authorize any MySQL same-engine backend or real PORT adapter evaluation separately, without timing, official metrics, reports/results updates, retained-evidence promotion, leaderboard output, denominator changes, paper-result changes, or release tag/export branch creation.

## 2026-05-21 - mysql_same_engine_backend_v0

MySQL same-engine backend completed on branch `feature/case-package-v2-external-schema`.

Mode: local diagnostic backend implementation only.

Summary:
- Same-engine `--engine mysql` rows now execute source SQL and adapter-generated candidate SQL through the MySQL backend.
- MySQL schema assets are resolved explicitly from manifest external schema metadata under `engines.mysql`; PostgreSQL schema assets are not used as fallback.
- Same-engine MySQL artifacts are written under `execution/mysql_same_engine/` with redacted metadata.
- Existing PORT cross-dialect MySQL source-reference artifacts remain under `execution/mysql_source/`.
- Spark remains deferred/fail-closed.

Live smoke:
- PostgreSQL environment ready: yes.
- MySQL environment ready: yes.
- Selected live smoke cases: `PERF_0006`, `CONS_0005`.
- MySQL same-engine source executable rows: 2.
- MySQL same-engine candidate executable rows: 2.
- Checker attempted rows: 2.
- Exact rows: 2.
- Mismatch rows: 0.
- Failure buckets: `none=2`.

Regression and validation:
- PORT cross-dialect controlled regression preserved: MySQL source-reference executable 5, PostgreSQL target-candidate executable 5, checker attempted 5, exact 5, mismatch 0.
- PostgreSQL public smoke dry-run and adapter-capture checks passed.
- Targeted MySQL/router/checker tests passed: 31 passed.
- Full `tests/user_entry` passed: 102 passed, 2 skipped.
- Common-core v2 static case-package reference validation passed for 40/40 case paths.

Boundary:
- SQL files modified: no.
- Manifest files modified: no.
- Schema, checker, and validation files modified: no.
- `case_sets/` changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw retained evidence changed: no.
- Official metrics computed: no.
- Timing/speedup computed: no.
- Global leaderboard created: no.
- Local `runs/user/` outputs committed: no.

Next safe action:
- Review the MySQL same-engine backend and audit packet; authorize any broader live MySQL coverage separately, keeping timing, official metrics, paper rendering, reports/results updates, retained-evidence promotion, and leaderboard output out of scope.

## 2026-05-21 - common_core_mysql_local_diagnostic_v0

Common-core MySQL local diagnostic trial completed on branch `feature/case-package-v2-external-schema`.

Mode: local diagnostic run and audit only.

Run:
- Case set: `common_core_v0`.
- Engine: `mysql`.
- Adapter: `python examples/user/noop_adapter.py`.
- Local output path: `runs/user/common_core_mysql_noop_db_checker/`.
- MySQL environment ready: yes.
- PostgreSQL environment ready: yes, but not used for execution in this `--engine mysql` run.
- Spark status: deferred/fail-closed.

Outcome:
- Selected rows: 40.
- Candidate generated rows: 40.
- Candidate preflight passed rows: 40.
- MySQL source execution attempted rows: 35.
- MySQL source executable rows: 31.
- MySQL candidate execution attempted rows: 31.
- MySQL candidate executable rows: 31.
- Checker attempted rows: 31.
- Exact rows: 31.
- Mismatch rows: 0.
- Source-like rows: 40.
- Failure buckets: `none=31`, `source_execution_failed=4`, `unsupported_engine=5`.
- Diagnostic modes: `same_engine=35`, `cross_dialect_reference=5`.

Failure interpretation:
- Four same-engine PORT rows (`PORT_0003`, `PORT_0005`, `PORT_0008`, `PORT_0012`) failed at MySQL source execution because retained source SQL used PostgreSQL-style syntax rejected by MySQL.
- Five cross-dialect PORT rows (`PORT_0004`, `PORT_0013`, `PORT_0022`, `PORT_0024`, `PORT_0025`) were selected as MySQL rows but are manifest-declared MySQL-source to PostgreSQL-target diagnostics; the runner failed closed with `unsupported_engine` rather than changing roles or using target-reference SQL.

Boundary:
- Source code modified: no.
- Scripts/tests/docs/examples modified: no.
- Cases/manifests/SQL/schema/checker/validation files modified: no.
- `case_sets/` changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw retained evidence changed: no.
- Official metrics computed: no.
- Timing/speedup computed: no.
- Global leaderboard created: no.
- Local `runs/user/` outputs committed: no.

Validation:
- `git diff --check`: passed.
- CSV/JSON parse checks for audit files: passed.
- Markdown sanity checks for audit files: passed.
- Protected-surface diff check: passed.
- Local run outputs not staged: confirmed.

Next safe action:
- Review the four PORT MySQL source-execution failures and five cross-dialect `engine=mysql` fail-closed rows before authorizing any broader MySQL/PORT follow-up; keep official metrics, timing, paper rendering, reports/results updates, retained-evidence promotion, and leaderboard output out of scope.

## 2026-05-21 - mysql_same_engine_source_failure_triage_v0

Four MySQL same-engine source-execution failures from the Common-core MySQL local diagnostic trial were triaged on branch `feature/case-package-v2-external-schema`.

Mode: local diagnostic triage and audit only.

Environment:
- MySQL environment ready: yes.
- PostgreSQL environment ready: yes, but not used by the targeted MySQL rerun.
- Spark status: deferred/fail-closed.

Targeted rerun:
- Case set: `common_core_v0`.
- Engine: `mysql`.
- Adapter: `python examples/user/noop_adapter.py`.
- Case list: `PORT_0003`, `PORT_0005`, `PORT_0008`, `PORT_0012`.
- Local output path: `runs/user/mysql_source_failure_triage/`.
- Selected rows: 4.
- Candidate generated rows: 4.
- Candidate preflight passed rows: 4.
- MySQL source execution attempted/executable/failed rows: 4/0/4.
- MySQL candidate execution attempted/executable rows: 0/0.
- Checker attempted/exact/mismatch rows: 0/0/0.
- Failure buckets: `source_execution_failed=4`.

Triage:
- Verdict: `legacy_mapping_gap`.
- The four current `sql/source.sql` files are PostgreSQL-like and fail when executed directly in MySQL.
- Current MySQL schema/load assets are present and the targeted rerun reached source query execution, so the observed failures are not schema setup, load, candidate execution, checker handoff, output conversion, permission, or backend export failures.
- Legacy branch `artifact/case-package-contract-alignment-clean` was used as read-only reference only. It contains PostgreSQL source artifacts and MySQL `rewrite_pos_01` target-positive artifacts for the four cases, but no MySQL `source.sql` execution artifacts were found.
- The old retained evidence therefore suggests PostgreSQL-source to MySQL-target cross-dialect role mapping, not fresh direct MySQL source execution for these four cases.

Boundary:
- Source code modified: no.
- Scripts/tests/docs/examples modified: no.
- Cases/manifests/SQL/schema/checker/validation files modified: no.
- `case_sets/` changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw retained evidence changed: no.
- Legacy repository modified: no.
- Official metrics computed: no.
- Timing/speedup computed: no.
- Global leaderboard created: no.
- Local `runs/user/` outputs committed: no.

Next safe action:
- Authorize a narrow PORT role-mapping/routing design task for `PORT_0003`, `PORT_0005`, `PORT_0008`, and `PORT_0012` before any implementation; do not edit SQL/schema/case assets or compute metrics/timing/reports-results/leaderboard output in that follow-up.

## 2026-05-21 - port_target_engine_role_mapping_v0

Target-engine-aware PORT local diagnostic role mapping was implemented on branch `feature/case-package-v2-external-schema`.

Mode: local diagnostic metadata, runner/validator support, tests, and audit only.

Implementation:
- All 9 Common-core PORT manifests now declare `local_diagnostic.schema_version: port_target_engine_diagnostic_v0`.
- Each PORT manifest has explicit `engine_roles` for `postgres`, `mysql`, and fail-closed `spark`.
- The resolver and runner consume the selected target engine role metadata instead of relying on one case-level diagnostic mode.
- `PORT_0004`, `PORT_0013`, `PORT_0022`, `PORT_0024`, and `PORT_0025` preserve MySQL-source to PostgreSQL-target controlled diagnostic behavior.
- `PORT_0003`, `PORT_0005`, `PORT_0008`, and `PORT_0012` now resolve as PostgreSQL-source to MySQL-target reverse cross-dialect roles under `--engine mysql`, but fail closed with `cross_dialect_route_unsupported` until that route is separately implemented.
- Non-PORT and cases without target-engine-aware metadata keep the existing same-engine default path.

Validation:
- Local engine environment check: PostgreSQL ok, MySQL ok, Spark deferred/fail-closed.
- YAML parse for all 9 PORT manifests: passed.
- Python compile for modified source files: passed.
- Help/readability commands: passed.
- User-entry unittest discovery: passed, 107 tests with 2 skipped.
- Case-package v2 unittest discovery: passed, 24 tests.
- Common-core v2 static validator loop: passed, 40/40.
- Targeted PostgreSQL controlled PORT diagnostic for 5 MySQL-source to PostgreSQL-target rows: exact 5/5.
- Targeted MySQL reverse-role guard for 4 PostgreSQL-source to MySQL-target rows: fail-closed `unsupported_engine=4`, with no wrong-engine source execution.
- Targeted MySQL same-engine sanity case `PORT_0004`: exact 1/1.
- `pytest` entrypoint was unavailable in the local environment, so equivalent `python -m unittest` validation was used.

Boundary:
- SQL files modified: no.
- Schema/checker/validation files modified: no.
- `case_sets/` changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Official metrics computed: no.
- Timing/speedup computed: no.
- Global leaderboard created: no.
- Local `runs/user/` outputs committed: no.

Next safe action:
- Review the explicit reverse PostgreSQL-source to MySQL-target role mapping and separately authorize a narrow backend route if live reverse cross-dialect execution is desired; keep official metrics, timing, reports/results, paper rendering, retained-evidence promotion, and leaderboard output out of scope.

## 2026-05-22 - port_reverse_cross_dialect_mysql_target_diagnostic_v0

Reverse PORT PostgreSQL-source to MySQL-target controlled diagnostic completed on branch `feature/case-package-v2-external-schema`.

Mode: local diagnostic runner support, controlled adapter, tests, and audit only.

Implementation:
- Added controlled adapter `examples/user/port_mysql_target_reference_adapter.py`.
- The adapter reads `SQLRB_CASE_DIR`, `SQLRB_CANDIDATE_SQL_PATH`, and `SQLRB_ENGINE`, requires `SQLRB_ENGINE=mysql`, resolves `local_diagnostic.engine_roles.mysql.target_reference.query`, and copies only that declared MySQL target reference query into the candidate path.
- The adapter fails closed for missing/malformed/non-MySQL metadata and does not infer `pos_01.sql` by filename.
- The engine router now supports the manifest-declared reverse route by executing PostgreSQL source-reference artifacts first and MySQL target-candidate artifacts second.
- The route does not execute PostgreSQL-like `source.sql` directly in MySQL and does not use `target_reference` as a checker oracle.

Controlled diagnostic:
- Case list: `PORT_0003`, `PORT_0005`, `PORT_0008`, `PORT_0012`.
- Engine: `mysql`.
- Adapter: `python examples/user/port_mysql_target_reference_adapter.py`.
- Local output path: `runs/user/port_mysql_target_reference_controlled/`.
- Selected rows: 4.
- Candidate generated rows: 4.
- PostgreSQL source-reference attempted/executable/failed rows: 4/4/0.
- MySQL target-candidate attempted/executable/failed rows: 4/4/0.
- Checker attempted/exact/mismatch rows: 4/4/0.
- Failure buckets: `none=4`.

Regression:
- Forward MySQL-source to PostgreSQL-target controlled path remained exact 5/5.
- Public non-DB smoke capture selected 2 rows and generated 2 candidates.
- Non-PORT same-engine behavior remains covered by user-entry tests.

Validation:
- Local engine environment check: PostgreSQL ok, MySQL ok, Spark deferred/fail-closed.
- `git diff --check`: passed.
- Python compile for modified source and new adapter: passed.
- `PYTHONPATH=src pytest tests/user_entry`: unavailable because `pytest` is not installed in this local environment.
- `PYTHONPATH=src python -m unittest discover -s tests/user_entry -p 'test_*.py'`: passed, 111 tests with 2 skipped.
- `PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -p 'test_*.py'`: passed, 24 tests.
- Common-core v2 static validator loop: passed, 40/40.

Boundary:
- SQL files modified: no.
- Manifest files modified: no.
- Schema/checker/validation files modified: no.
- `case_sets/` changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Official metrics computed: no.
- Timing/speedup computed: no.
- Global leaderboard created: no.
- Local `runs/user/` outputs committed: no.

Next safe action:
- Run a narrow bidirectional PORT controlled-diagnostic closeout or return to the main user-entry roadmap; keep real user-adapter evaluation, timing, official metrics, reports/results updates, paper rendering, retained-evidence promotion, and leaderboard output out of scope.

## 2026-05-22 - port_bidirectional_cross_dialect_closeout_v0

Bidirectional PORT cross-dialect local diagnostic closeout completed on branch `feature/case-package-v2-external-schema`.

Mode: audit-only closeout.

Verdict:
- `closed_for_current_user_entry_phase`.

Closeout summary:
- All 9 Common-core PORT cases have target-engine-aware `local_diagnostic` role metadata.
- The resolver and runner consume selected-engine role metadata and do not infer roles from filenames, SQL text, or pool name alone.
- Forward route validated: MySQL source-reference to PostgreSQL target-candidate for `PORT_0004`, `PORT_0013`, `PORT_0022`, `PORT_0024`, and `PORT_0025`, controlled exact 5/5.
- Reverse route validated: PostgreSQL source-reference to MySQL target-candidate for `PORT_0003`, `PORT_0005`, `PORT_0008`, and `PORT_0012`, controlled exact 4/4.
- Opt-in checker normalization remains gated to cross-dialect local diagnostics.
- Same-engine defaults remain protected for PERF, CONS, LONGTAIL, and same-engine PORT routes.

Deferred:
- Real user PORT adapter evaluation, Spark live execution, timing/speedup, official metrics, paper rendering, reports/results migration, retained evidence integration, release tag/export branch creation, and any leaderboard remain deferred.

Boundary:
- Source code modified: no.
- Scripts/tests/docs/examples modified: no.
- Cases/manifests/SQL/schema/checker/validation files modified: no.
- `case_sets/` changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw retained evidence changed: no.
- Official metrics computed: no.
- Timing/speedup computed: no.
- Global leaderboard created: no.
- Release tag/export branch created: no.
- Local `runs/user/` outputs created or committed: no.

Next safe action:
- Return to the main user-entry roadmap; any real PORT user-adapter evaluation, broader MySQL coverage, timing, official metrics, reports/results updates, paper rendering, retained-evidence promotion, leaderboard output, or release export requires separate authorization.

## 2026-05-22 - user_entry_pg_mysql_local_diagnostic_closeout_v0

PostgreSQL/MySQL user-entry local diagnostic closeout completed on branch `feature/case-package-v2-external-schema`.

Mode: audit-only closeout.

Verdict:
- `pg_mysql_local_diagnostic_ready_with_deferred_items`.

Capability summary:
- PostgreSQL same-engine local diagnostics are implemented and live validated through the Common-core PostgreSQL no-op diagnostic and subsequent PORT controlled forward repair.
- MySQL same-engine local diagnostics are implemented and live smoke validated on `PERF_0006` and `CONS_0005`; the Common-core MySQL no-op diagnostic reached 31 exact executed rows and exposed PORT role-routing findings now addressed by bidirectional PORT diagnostics.
- PORT bidirectional cross-dialect controlled diagnostics are validated: MySQL source-reference to PostgreSQL target-candidate exact 5/5, and PostgreSQL source-reference to MySQL target-candidate exact 4/4.
- The user-entry harness produces local ledgers, quality summaries, quality reports, and tag slices; these remain local diagnostic artifacts only.
- Spark remains deferred/fail-closed.

Boundary:
- Source code modified: no.
- Scripts/tests/docs/examples modified: no.
- Cases/manifests/SQL/schema/checker/validation files modified: no.
- `case_sets/` changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw retained evidence changed: no.
- Official metrics computed: no.
- Timing/speedup computed: no.
- Global leaderboard created: no.
- Release tag/export branch created: no.
- Local `runs/user/` outputs created or committed: no.

Deferred:
- Real user PORT adapter evaluation, Spark live execution, timing/speedup, official metrics, paper rendering, reports/results migration, retained evidence integration, release tag/export branch creation, and any leaderboard remain deferred.

Next safe action:
- Run a bounded PostgreSQL+MySQL local diagnostic rerun only if it remains local-only and non-metric, or continue release/paper planning; do not start timing implementation or official metrics from this closeout.

## 2026-05-22 - user_entry_pg_mysql_current_diagnostic_rerun_v0

Bounded PostgreSQL/MySQL current local diagnostic rerun completed on branch `feature/case-package-v2-external-schema`.

Mode: local diagnostic rerun and audit only.

Environment:
- PostgreSQL probe: ok.
- MySQL probe: ok.
- Spark: deferred/fail-closed.

Run summary:
- PostgreSQL run output: `runs/user/bounded_pg_noop_db_checker_current/`.
- PostgreSQL selected rows: 40.
- PostgreSQL candidate generated rows: 40.
- PostgreSQL source-reference executable rows: 40.
- PostgreSQL target-candidate executable rows: 35.
- PostgreSQL checker attempted/exact/mismatch rows: 35/35/0.
- PostgreSQL failure buckets: `none=35`, `candidate_execution_failed=5`.
- MySQL run output: `runs/user/bounded_mysql_noop_db_checker_current/`.
- MySQL selected rows: 40.
- MySQL candidate generated rows: 40.
- MySQL source-reference executable rows: 40.
- MySQL target-candidate executable rows: 36.
- MySQL checker attempted/exact/mismatch rows: 36/36/0.
- MySQL failure buckets: `none=36`, `candidate_execution_failed=4`.

Interpretation:
- The no-op adapter is source-like and is not a valid target-generating adapter for cross-dialect PORT exactness.
- The remaining failures are expected target-candidate execution failures on PORT cross-dialect rows after successful source-reference execution.
- Controlled PORT target-reference diagnostics remain the evidence for cross-dialect target execution and checker handoff: forward exact 5/5 and reverse exact 4/4.

Boundary:
- Source code modified: no.
- Scripts/tests/docs/examples modified: no.
- Cases/manifests/SQL/schema/checker/validation files modified: no.
- `case_sets/` changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw retained evidence changed: no.
- Official metrics computed: no.
- Timing/speedup computed: no.
- Global leaderboard created: no.
- Release tag/export branch created: no.
- Local `runs/user/` outputs committed: no.

Next safe action:
- Treat this as the current PostgreSQL/MySQL no-op diagnostic snapshot; real adapter evaluation, Spark work, timing, official metrics, paper rendering, reports/results updates, retained-evidence promotion, leaderboard output, or release export requires separate authorization.

## 2026-05-22 - spark_fail_closed_skeleton_v0

Spark fail-closed skeleton/environment detector completed on branch `feature/case-package-v2-external-schema`.

Mode: local diagnostic infrastructure only.

Implementation:
- `src/sql_rewrite_bench/spark_execution.py` now detects Spark readiness signals without starting Spark or importing the Spark runtime.
- Spark-selected DB execution rows fail closed with explicit local statuses and `unsupported_engine` bucket.
- Spark execution writes per-row `spark_environment_status.json` metadata only; it does not create source/candidate result artifacts.
- `scripts/dev/check_local_engine_env.py` now reports `spark-sql`, `SPARK_LOCAL_IP`, `SPARK_HOME`, `PYSPARK_PYTHON`, and `pyspark` import availability, and states that Spark is fail-closed/not live implemented.
- `docs/LOCAL_ENGINE_SETUP.md` and `scripts/env_spark.example.sh` clarify that Spark settings are preparatory only.

Validation:
- Environment checker: PostgreSQL ok, MySQL ok, Spark fail-closed/not configured.
- Spark fail-closed smoke selected 2 rows, generated 2 candidates, produced `unsupported_engine=2`, and did not run checkers.
- PostgreSQL two-case DB/checker smoke: exact 2/2.
- MySQL two-case DB/checker smoke: exact 2/2.
- User-entry unittest suite passed: 115 tests, 2 skipped. `pytest` was unavailable, so unittest was used.
- Common-core v2 reference validator loop passed: 40/40.

Boundary:
- Spark live execution implemented: no.
- Source code modified: yes, Spark skeleton only.
- Scripts/docs/tests modified: yes, environment checker/template/docs and user-entry tests only.
- SQL files modified: no.
- Manifest files modified: no.
- Schema/checker/validation files modified: no.
- `case_sets/` changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Official metrics computed: no.
- Timing/speedup computed: no.
- Global leaderboard created: no.
- Release tag/export branch created: no.
- Local `runs/user/` outputs committed: no.

Next safe action:
- Authorize only a narrow Spark schema/load resolver or mocked Spark execution contract task, or keep Spark deferred while continuing release planning; live Spark execution, timing, official metrics, reports/results updates, paper rendering, retained-evidence promotion, leaderboard output, or release export requires separate authorization.

## 2026-05-22 - spark_backend_design_v0

Spark local diagnostic backend design completed on branch `feature/case-package-v2-external-schema`.

Mode: design/audit only.

Verdict:
- `ready_for_fail_closed_skeleton`.

Main design decisions:
- `spark_execution.py` should own Spark environment detection, session startup, per-case namespace isolation, Spark schema/load execution, source/candidate execution, JSONL result export, metadata/error artifacts, and cleanup.
- `engine_execution.py` should keep routing, selected-engine role sequencing, common `EngineExecutionResult` handoff, and fail-closed behavior for missing/unsupported roles.
- Spark schema assets must be resolved only through manifest `schema.external_profile` and external `engines.spark.ddl` / `engines.spark.load` metadata; PostgreSQL/MySQL assets must not be substituted.
- `pyspark` local mode is recommended over `spark-sql` for stable result export and session control.
- `SPARK_LOCAL_IP` alone is not enough to enable Spark execution; a future skeleton should require explicit local Spark opt-in and runtime availability checks.
- Spark result artifacts should match the existing JSONL object shape consumed by `local_result_checker.py`.
- Same-engine checker behavior remains strict unless case-local config says otherwise; no Spark-specific checker normalization is authorized.
- All 9 Common-core PORT manifests currently declare Spark roles as unsupported/manual-review, so `--engine spark` must fail closed for PORT until a future task explicitly approves roles.

Boundary:
- Spark execution implemented: no.
- Spark live run performed: no.
- Source code modified: no.
- Scripts/tests/docs/examples modified: no.
- Cases/manifests/SQL/schema/checker/validation files modified: no.
- `case_sets/` changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw retained evidence changed: no.
- Official metrics computed: no.
- Timing/speedup computed: no.
- Global leaderboard created: no.
- Release tag/export branch created: no.
- Local `runs/user/` outputs created or committed: no.

Next safe action:
- Authorize only a narrow Spark fail-closed skeleton/environment-detector task, or keep Spark deferred and continue release planning; live Spark execution, timing, official metrics, reports/results updates, paper rendering, retained-evidence promotion, leaderboard output, and release export require separate authorization.

## 2026-05-22 - user_entry_pg_mysql_bounded_local_diagnostic_rerun_v0

Bounded PostgreSQL/MySQL local diagnostic rerun completed on branch `feature/case-package-v2-external-schema`.

Mode: local diagnostic rerun and audit only.

Environment:
- PostgreSQL probe: ok.
- MySQL probe: ok.
- Spark: deferred/fail-closed.

Run summary:
- PostgreSQL run output: `runs/user/bounded_pg_noop_db_checker_current/`.
- PostgreSQL selected rows: 40.
- PostgreSQL candidate generated rows: 40.
- PostgreSQL source-reference executable rows: 40.
- PostgreSQL target-candidate executable rows: 35.
- PostgreSQL checker attempted/exact/mismatch rows: 35/35/0.
- PostgreSQL failure buckets: `candidate_execution_failed=5`, `none=35`.
- MySQL run output: `runs/user/bounded_mysql_noop_db_checker_current/`.
- MySQL selected rows: 40.
- MySQL candidate generated rows: 40.
- MySQL source-reference executable rows: 40.
- MySQL target-candidate executable rows: 36.
- MySQL checker attempted/exact/mismatch rows: 36/36/0.
- MySQL failure buckets: `candidate_execution_failed=4`, `none=36`.
- Tag-slice summaries were created for both engines.

Interpretation:
- The no-op adapter is source-like and is not a valid target-generating adapter for cross-dialect PORT exactness.
- PostgreSQL's five remaining failures are target-candidate failures for MySQL-source to PostgreSQL-target PORT rows after MySQL source-reference execution succeeded.
- MySQL's four remaining failures are target-candidate failures for PostgreSQL-source to MySQL-target PORT rows after PostgreSQL source-reference execution succeeded.
- Controlled PORT target-reference diagnostics remain the evidence for cross-dialect target execution and checker handoff: forward exact 5/5 and reverse exact 4/4.

Boundary:
- Source code modified: no.
- Scripts/tests/docs/examples modified: no.
- Cases/manifests/SQL/schema/checker/validation files modified: no.
- `case_sets/` changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw retained evidence changed: no.
- Official metrics computed: no.
- Timing/speedup computed: no.
- Global leaderboard created: no.
- Release tag/export branch created: no.
- Local `runs/user/` outputs committed: no.

Next safe action:
- Treat this as the current PostgreSQL/MySQL no-op diagnostic snapshot; real adapter evaluation, Spark work, timing, official metrics, paper rendering, reports/results updates, retained-evidence promotion, leaderboard output, or release export requires separate authorization.

## 2026-05-22 - user_entry_engine_backend_closeout_v0

User-entry engine backend closeout completed on branch `feature/case-package-v2-external-schema`.

Mode: audit/closeout only.

Verdict:
- `engine_backend_phase_closed_with_deferred_items`.

Status summary:
- PostgreSQL backend: implemented and live rerun; latest bounded no-op rerun selected 40 rows, source executable 40, candidate executable 35, checker exact 35, mismatch 0, with 5 expected PORT no-op target-candidate failures.
- MySQL backend: implemented and live rerun; latest bounded no-op rerun selected 40 rows, source executable 40, candidate executable 36, checker exact 36, mismatch 0, with 4 expected PORT no-op target-candidate failures.
- PORT cross-dialect: bidirectional controlled local diagnostics closed; forward MySQL-source to PostgreSQL-target exact 5/5 and reverse PostgreSQL-source to MySQL-target exact 4/4.
- Spark backend: fail-closed skeleton and environment detector implemented; live Spark SQL execution remains deferred.
- Local output surface: `quality_summary.json`, `quality_report.md`, `tag_slices.csv`, ledger statuses, and failure buckets are available for local diagnostics.

Deferred work:
- Spark live execution.
- Real user adapter evaluation.
- Timing/speedup.
- Official metrics.
- Paper table rendering.
- Reports/results migration.
- Retained-evidence integration.
- Release export/tagging.
- Global leaderboard output.

Boundary:
- Source code modified: no.
- Scripts/tests/docs/examples modified: no.
- Cases/manifests/SQL/schema/checker/validation files modified: no.
- `case_sets/` changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Official metrics computed: no.
- Timing/speedup computed: no.
- Global leaderboard created: no.
- Release tag/export branch created: no.
- Local `runs/user/` outputs created or committed: no.

Next safe action:
- Return to release/paper planning, or separately authorize a narrow real-adapter local diagnostic evaluation under local-only non-metric boundaries. Spark live execution, timing, official metrics, reports/results updates, paper rendering, retained-evidence promotion, leaderboard output, and release export remain separate authorization boundaries.

## 2026-05-22 - spark_live_backend_v0

Spark live local diagnostic backend v0 completed on branch `feature/case-package-v2-external-schema`.

Mode: local diagnostic infrastructure only.

Status summary:
- Spark backend: upgraded from fail-closed skeleton to PySpark-backed local diagnostic execution when PySpark is available.
- Schema/load: resolves manifest external schema metadata `engines.spark.ddl` and `engines.spark.load`; PostgreSQL/MySQL schema assets are not used for Spark.
- Execution/artifacts: same-engine Spark source and candidate SQL run in an isolated diagnostic namespace, with local `source_result.jsonl`, `candidate_result.jsonl`, query copies, errors, and Spark metadata under the row workspace.
- Checker handoff: existing local checker consumes Spark JSONL artifacts when both source and candidate execute.
- Fail-closed statuses: environment, schema, session, setup, source, candidate, timeout, and internal Spark failures are explicit local diagnostic statuses.
- Live Spark smoke: not run because local Spark/PySpark is not configured (`spark-sql` missing, Spark env unset, `pyspark` unavailable).
- Validation: py_compile passed; environment checker passed; help/readability commands passed; user-entry unittest suite passed (119 tests, 2 skipped); 40/40 Common-core validators passed; Spark fail-closed smoke selected 2 rows and failed closed without crashing; PostgreSQL and MySQL two-case DB/checker smokes each reached exact 2/2.

Boundary:
- Official metrics computed: no.
- Timing/speedup computed: no.
- Paper tables rendered: no.
- Reports/results updated: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Global leaderboard created: no.
- Release tag/export branch created: no.

Next safe action:
- Configure a local PySpark environment and rerun the two-case Spark live smoke (`PERF_0006`, `CONS_0005`) before authorizing any broader Common-core Spark local diagnostic trial.

## 2026-05-22 - spark_live_two_case_smoke_v0

Spark two-case live local diagnostic smoke completed on branch `feature/case-package-v2-external-schema`.

Mode: local diagnostic smoke and audit only.

Environment:
- PostgreSQL probe: ok.
- MySQL probe: ok.
- Spark readiness: PySpark import available, `PYSPARK_PYTHON` set, `SQLRB_SPARK_MASTER` set, live local diagnostic backend available through PySpark.
- No secrets printed.

Run summary:
- Local run output: `runs/user/spark_live_smoke/`.
- Selected rows: 2.
- Candidate generated rows: 2.
- Candidate preflight passed rows: 2.
- Spark source execution attempted rows: 2.
- Spark source executable rows: 2.
- Spark candidate execution attempted rows: 2.
- Spark candidate executable rows: 2.
- Checker attempted/exact/mismatch rows: 2/2/0.
- Failure buckets: `none=2`.
- `PERF_0006`: Spark source/candidate executed through PySpark, source rows 2, candidate rows 2, checker exact.
- `CONS_0005`: Spark source/candidate executed through PySpark, source rows 0, candidate rows 0, checker exact.

Interpretation:
- The two-case Spark live backend smoke is validated for this subset.
- A preliminary sandboxed Spark attempt failed to bind a local Py4J socket and was discarded as a sandbox-only blocker before the accepted local-socket run.
- The no-op adapter remains a diagnostic adapter; this is not official paper evidence and not official metrics.

Boundary:
- Source code modified: no.
- Scripts/tests/docs/examples modified: no.
- Cases/manifests/SQL/schema/checker/validation files modified: no.
- `case_sets/` changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw retained evidence changed: no.
- Official metrics computed: no.
- Timing/speedup computed: no.
- Global leaderboard created: no.
- Release tag/export branch created: no.
- Local `runs/user/spark_live_smoke/` outputs committed: no.

Next safe action:
- If Spark work continues, authorize a bounded Common-core Spark local diagnostic trial under the same local-only, non-metric, no timing, no reports/results, and no leaderboard boundaries.

## 2026-05-22 - common_core_spark_local_diagnostic_v0

Common-core Spark local diagnostic trial completed on branch `feature/case-package-v2-external-schema`.

Mode: local diagnostic trial and audit only.

Environment:
- PostgreSQL probe: ok.
- MySQL probe: ok.
- Spark readiness: PySpark import available, `PYSPARK_PYTHON` set, `SQLRB_SPARK_MASTER` set, live local diagnostic backend available through PySpark.
- No secrets printed.

Run summary:
- Local run output: `runs/user/common_core_spark_noop_db_checker/`.
- Selected rows: 40.
- Candidate generated rows: 40.
- Candidate preflight passed rows: 40.
- Spark source execution attempted rows: 31.
- Spark source executable rows: 31.
- Spark candidate execution attempted rows: 31.
- Spark candidate executable rows: 31.
- Checker attempted/exact/mismatch rows: 31/30/1.
- Source-like rows: 40.
- Failure buckets: `none=30`, `mismatch=1`, `unsupported_engine=9`.
- Diagnostic modes: `same_engine=31`, `unsupported=9`.
- Tag-slice summary created: yes.

Failure summary:
- `CONS_0011`: checker/normalization row-order mismatch; source result rows were `ALICE`, `BOB`, while candidate rows were `BOB`, `ALICE`.
- PORT cases `PORT_0003`, `PORT_0004`, `PORT_0005`, `PORT_0008`, `PORT_0012`, `PORT_0013`, `PORT_0022`, `PORT_0024`, and `PORT_0025`: explicit Spark local diagnostic roles remain unsupported/fail-closed; no source, target, target_reference, or checker fallback was attempted.

Boundary:
- Source code modified: no.
- Scripts/tests/docs/examples modified: no.
- Cases/manifests/SQL/schema/checker/validation files modified: no.
- `case_sets/` changed: no.
- Inventory changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw retained evidence changed: no.
- Official metrics computed: no.
- Timing/speedup computed: no.
- Global leaderboard created: no.
- Release tag/export branch created: no.
- Local `runs/user/common_core_spark_noop_db_checker/` outputs committed: no.

Next safe action:
- Review the `CONS_0011` row-order checker behavior and keep PORT Spark roles fail-closed unless a separate Spark PORT role task is authorized; any broader Spark, timing, official metrics, reports/results, retained-evidence, leaderboard, or release-export work remains separate authorization.

## 2026-05-22 - cons0011_spark_row_order_triage_v0

`CONS_0011` Spark row-order mismatch triage completed on branch `feature/case-package-v2-external-schema`.

Mode: local diagnostic audit only.

Result:
- Existing Common-core Spark local diagnostic artifacts were available; no `CONS_0011` rerun was needed.
- Source/candidate row counts: 2/2.
- Column labels equal: yes, `ENAME`.
- Values match after sorting rows: yes.
- Source SQL `ORDER BY`: absent.
- Positive rewrite SQL `ORDER BY`: absent.
- Workspace source and candidate SQL: identical unordered no-op diagnostic query.
- Checker order policy: current local checker preserves row order unless a recognized top-level `sort_rows: true` is present in `checker/normalization.yaml`; `CONS_0011` does not declare that setting, and `compare_config.yaml` declares semantic equivalence without an order policy.
- Verdict: `case_level_compare_config_gap`.
- Likely root cause: order-insensitive case semantics/configuration gap surfaced by Spark nondeterministic row order, not a true semantic mismatch.

Boundary:
- Source code modified: no.
- Scripts/tests/docs/examples modified: no.
- Cases/manifests/SQL/schema/checker/validation files modified: no.
- `case_sets/` changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw retained evidence changed: no.
- Official metrics computed: no.
- Timing/speedup computed: no.
- Global leaderboard created: no.
- Local run outputs committed: no.

Next safe action:
- Authorize a narrow `CONS_0011` case-local order-insensitive checker policy fix, preferably through the repository-supported `sort_rows` setting or a separately authorized compare-config support task, with representative PERF/CONS/LONGTAIL and hard-negative/control regression checks.

## 2026-05-22 - cons0011_order_insensitive_policy_fix_v0

`CONS_0011` order-insensitive checker policy fix completed on branch `feature/case-package-v2-external-schema`.

Mode: case-local local diagnostic checker policy fix only.

Change:
- Added top-level `sort_rows: true` only to `cases/CONS/CONS_0011/checker/normalization.yaml`.
- Preserved existing normalization rules.
- SQL files modified: no.
- Manifest files modified: no.
- Global checker/source behavior modified: no.
- Other case checker configs modified: no.

Validation:
- Environment check: PostgreSQL probe ok, MySQL probe ok, Spark PySpark import available, live local diagnostic backend available through PySpark.
- `CONS_0011` Spark rerun at `runs/user/cons0011_spark_order_fix/`: selected/source/candidate/checker/exact/mismatch rows 1/1/1/1/1/0; failure buckets `none=1`.
- Two-case Spark regression at `runs/user/spark_two_case_regression_after_cons0011_fix/`: selected/source/candidate/checker/exact/mismatch rows 2/2/2/2/2/0; failure buckets `none=2`.
- Common-core Spark rerun at `runs/user/common_core_spark_after_cons0011_order_fix/`: selected/source/candidate/checker/exact/mismatch rows 40/31/31/31/31/0; failure buckets `none=31`, `unsupported_engine=9`; PORT Spark rows remained explicit fail-closed.
- YAML parse check for modified normalization config: passed.
- Case-package v2 reference validator over all 40 Common-core cases: passed 40/40.
- `PYTHONPATH=src pytest tests/user_entry`: passed, 118 passed and 1 skipped.
- `git diff --check`: passed.

Boundary:
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw retained evidence changed: no.
- Official metrics computed: no.
- Timing/speedup computed: no.
- Global leaderboard created: no.
- Local `runs/user/` outputs committed: no.

Next safe action:
- Use the fixed `CONS_0011` policy in future local Spark diagnostics; any broader checker-policy migration, official metrics, timing/speedup, reports/results update, retained-evidence promotion, leaderboard, or release-export work remains separate authorization.

## 2026-05-22 - port_spark_target_role_mapping_v0

PORT Spark target-engine role mapping completed with failures on branch `feature/case-package-v2-external-schema`.

Summary:
- Spark target roles declared: 4 (`PORT_0003`, `PORT_0004`, `PORT_0005`, `PORT_0013`).
- Spark unsupported/fail-closed roles: 5 (`PORT_0008`, `PORT_0012`, `PORT_0022`, `PORT_0024`, `PORT_0025`).
- Controlled Spark target diagnostic at `runs/user/port_spark_target_reference_controlled/`: selected/source-reference executable/Spark target-candidate executable/checker/exact/mismatch rows `4/4/4/4/2/2`.
- Failure summary: `none=2`, `mismatch=2`; mismatches are `PORT_0004` and `PORT_0013` checker-normalization outcomes for MySQL string numeric values versus Spark numeric float values after both sides executed.
- Unsupported Spark role check at `runs/user/port_spark_unsupported_role_check/`: selected 5, `unsupported_engine=5`, no source/target/checker fallback.
- PG/MySQL behavior preservation: PostgreSQL target route exact `5/5`; MySQL target route exact `4/4`.
- Non-PORT Spark behavior preservation: two-case Spark smoke exact `2/2`.

Boundary:
- Local diagnostic only.
- No SQL changes.
- No schema/checker/validation changes.
- No `case_sets/` changes.
- No reports/results changes.
- No denominator, paper result, case membership, or raw retained evidence changes.
- No official metrics computed.
- No timing/speedup computed.
- No global leaderboard created.
- Local `runs/user/` outputs committed: no.

Next safe action:
- Audit/fix the MySQL-source to Spark-target numeric normalization gap for `PORT_0004` and `PORT_0013`, with PERF/CONS/LONGTAIL same-engine regression checks before any broader Spark PORT diagnostic.

## 2026-05-22 - port_spark_numeric_normalization_v0

Mode: narrow local-diagnostic checker fix only.

Legacy repo modified: no.
Release repo modified: yes.

Files created:
- `audits/port_spark_numeric_normalization_v0/README.md`
- `audits/port_spark_numeric_normalization_v0/normalization_change_summary.md`
- `audits/port_spark_numeric_normalization_v0/before_after_summary.csv`
- `audits/port_spark_numeric_normalization_v0/diagnostic_rerun_summary.json`
- `audits/port_spark_numeric_normalization_v0/preservation_results.csv`
- `audits/port_spark_numeric_normalization_v0/test_results.md`
- `audits/port_spark_numeric_normalization_v0/protected_surface_check.md`
- `audits/port_spark_numeric_normalization_v0/command_log.md`

Files modified:
- `src/sql_rewrite_bench/local_result_checker.py`
- `src/sql_rewrite_bench/user_run.py`
- `tests/user_entry/test_cross_dialect_checker_normalization.py`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- Root cause confirmed for `PORT_0004` and `PORT_0013`: MySQL string numeric values vs Spark JSON numeric values.
- Spark PORT controlled rerun moved from exact/mismatch `2/2` to `4/0`.
- Unsupported Spark role check remained `unsupported_engine=5`.
- PostgreSQL PORT target route remained exact `5/5`.
- MySQL PORT target route remained exact `4/4`.
- Non-PORT Spark two-case smoke remained exact `2/2`.
- Focused checker tests passed: 18 tests.
- `PYTHONPATH=src pytest tests/user_entry -q` passed: 130 passed, 1 skipped, 12 subtests.
- Common-core case-package validator passed 40/40.
- Environment check passed for PostgreSQL/MySQL probes and Spark PySpark readiness.
- `git diff --check` passed.

Commit hash: pending at project-control writeback time; final report records the pushed commit hash.
Push result: pending at project-control writeback time; final report records the push result.

Denominator changed: no.
Paper results changed: no.
Case membership changed: no.
Raw legacy evidence changed: no.

Next safe action:
- Optionally rerun a broader Spark local diagnostic snapshot, keeping PORT role outputs local-only and separate from official metrics, timing/speedup, reports/results, paper results, retained-evidence promotion, and leaderboard surfaces.

## 2026-05-22 - tri_engine_user_entry_local_diagnostic_closeout_v0

Mode: audit-only local diagnostic closeout.

Legacy repo modified: no.
Release repo modified: yes.

Metadata correction note:
- Prior task `port_spark_numeric_normalization_v0` final code/audit commit hash: `8f7b2f8`.
- Prior task push result: pushed to `origin/feature/case-package-v2-external-schema`.

Files created:
- `audits/tri_engine_user_entry_local_diagnostic_closeout_v0/README.md`
- `audits/tri_engine_user_entry_local_diagnostic_closeout_v0/engine_capability_matrix.csv`
- `audits/tri_engine_user_entry_local_diagnostic_closeout_v0/port_controlled_path_matrix.csv`
- `audits/tri_engine_user_entry_local_diagnostic_closeout_v0/role_class_summary.csv`
- `audits/tri_engine_user_entry_local_diagnostic_closeout_v0/closeout_summary.json`
- `audits/tri_engine_user_entry_local_diagnostic_closeout_v0/deferred_work.md`
- `audits/tri_engine_user_entry_local_diagnostic_closeout_v0/source_audit_inventory.csv`
- `audits/tri_engine_user_entry_local_diagnostic_closeout_v0/protected_surface_check.md`
- `audits/tri_engine_user_entry_local_diagnostic_closeout_v0/command_log.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- Passed project-control readability, audit CSV/JSON/Markdown sanity, `git diff --check`, and protected-surface diff checks.
- Closeout uses committed audit packets; no new local diagnostic reruns were performed.
- PostgreSQL no-op local diagnostic snapshot: exact/mismatch `35/0`.
- MySQL no-op local diagnostic snapshot: exact/mismatch `36/0`.
- PORT controlled paths: PostgreSQL target `5/5`, MySQL target `4/4`, Spark target `4/4`, Spark unsupported/fail-closed `5`.

Denominator changed: no.
Paper results changed: no.
Case membership changed: no.
Raw legacy evidence changed: no.
Reports/results changed: no.
Official metrics computed: no.
Timing/speedup computed: no.
Leaderboard created: no.
Release/export/tag created: no.

Next safe action:
- Authorize a separate real user-adapter evaluation plan if desired, keeping timing, official metrics, paper rendering, reports/results migration, retained-evidence integration, and release/export/tag work separately scoped.

## 2026-05-22 - real_user_adapter_evaluation_plan_v0

Mode: audit/design-only real user-adapter local diagnostic planning.

Legacy repo modified: no.
Release repo modified: yes.

Files created:
- `audits/real_user_adapter_evaluation_plan_v0/README.md`
- `audits/real_user_adapter_evaluation_plan_v0/adapter_contract.md`
- `audits/real_user_adapter_evaluation_plan_v0/trial_scope_matrix.csv`
- `audits/real_user_adapter_evaluation_plan_v0/status_interpretation.csv`
- `audits/real_user_adapter_evaluation_plan_v0/output_policy.md`
- `audits/real_user_adapter_evaluation_plan_v0/evaluation_sequence.md`
- `audits/real_user_adapter_evaluation_plan_v0/baseline_summary.json`
- `audits/real_user_adapter_evaluation_plan_v0/protected_surface_check.md`
- `audits/real_user_adapter_evaluation_plan_v0/command_log.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- Passed project-control readability, audit CSV/JSON/Markdown sanity, `git diff --check`, and protected-surface diff checks.
- No real user adapter run was performed.
- No local diagnostic rerun was performed.

Denominator changed: no.
Paper results changed: no.
Case membership changed: no.
Raw legacy evidence changed: no.
Reports/results changed: no.
Official metrics computed: no.
Timing/speedup computed: no.
Leaderboard created: no.
Release/export/tag created: no.
Real user adapter run performed: no.

Next safe action:
- Authorize one bounded real adapter smoke with an explicit adapter command, explicit case lists, local `runs/user/` output, and no timing, official metrics, reports/results, retained-evidence promotion, leaderboard, release export, or tag work.

## 2026-05-22 - sqlglot_user_adapter_bounded_smoke_v0

Mode: bounded local diagnostic user-entry adapter smoke.

Legacy repo modified: no.
Release repo modified: yes.

Files created:
- `audits/sqlglot_user_adapter_bounded_smoke_v0/README.md`
- `audits/sqlglot_user_adapter_bounded_smoke_v0/route_summary.csv`
- `audits/sqlglot_user_adapter_bounded_smoke_v0/status_summary.json`
- `audits/sqlglot_user_adapter_bounded_smoke_v0/command_log.md`
- `audits/sqlglot_user_adapter_bounded_smoke_v0/protected_surface_check.md`
- `audits/sqlglot_user_adapter_bounded_smoke_v0/boundary_checklist.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- Passed project-control readability, audit CSV/JSON/Markdown sanity, `git diff --check`, and protected-surface diff checks.
- SQLGlot dependency available: yes, version `30.2.1`; no install required.
- Engine readiness passed for PostgreSQL, MySQL, and Spark.
- Phase A adapter-capture: noop and optimize each selected 2 PostgreSQL rows and generated/preflight-passed 2 candidates with DB/checker disabled.
- Phase B same-engine smoke: noop exact `2/2` on PostgreSQL, MySQL, and Spark; optimize exact `1/2` on PostgreSQL, MySQL, and Spark with `CONS_0005` candidate execution failed on each engine.
- Phase C PORT probe: noop PostgreSQL target probe `PORT_0004` adapter parse failed before candidate generation; noop MySQL target probe `PORT_0003` checker mismatched after source/candidate execution; optimize PORT probe skipped because optimize Phase B did not fully succeed.

Denominator changed: no.
Paper results changed: no.
Case membership changed: no.
Raw retained evidence changed: no.
Reports/results changed: no.
Official metrics computed: no.
Timing/speedup computed: no.
Leaderboard created: no.
Release/export/tag created: no.
Retained evidence promoted: no.
`runs/user/` outputs committed: no.

Next safe action:
- Triage `sqlglot_optimize` on `CONS_0005` before any broader optimize-route trial; keep PORT real-adapter probes separate from controlled target-reference diagnostics and continue to avoid timing, official metrics, reports/results, retained-evidence promotion, leaderboard, release export, or tag work.

## 2026-05-22 - sqlglot_optimize_cons0005_triage_v0

Mode: audit-only SQLGlot optimize failure triage.

Legacy repo modified: no.
Release repo modified: yes.

Files created:
- `audits/sqlglot_optimize_cons0005_triage_v0/README.md`
- `audits/sqlglot_optimize_cons0005_triage_v0/reproducer.md`
- `audits/sqlglot_optimize_cons0005_triage_v0/emitted_candidates.csv`
- `audits/sqlglot_optimize_cons0005_triage_v0/failure_shape.json`
- `audits/sqlglot_optimize_cons0005_triage_v0/experimental_variants.md`
- `audits/sqlglot_optimize_cons0005_triage_v0/recommendation.md`
- `audits/sqlglot_optimize_cons0005_triage_v0/protected_surface_check.md`
- `audits/sqlglot_optimize_cons0005_triage_v0/command_log.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- Passed project-control readability, audit CSV/JSON/Markdown sanity, `git diff --check`, and protected-surface diff checks.
- Confirmed `CONS_0005` optimize candidates for PostgreSQL, MySQL, and Spark fail only at candidate execution due invalid `table1.table2.i` qualification shape.
- Standalone SQLGlot reproducer confirmed parse/emit succeeds, context-free optimize emits the invalid qualification shape, and schema-aware optimize experiments avoid the specific invalid reference while changing route semantics.
- No `user_run` rerun was performed.
- No broader optimize trial was performed.

Denominator changed: no.
Paper results changed: no.
Case membership changed: no.
Raw retained evidence changed: no.
Reports/results changed: no.
Official metrics computed: no.
Timing/speedup computed: no.
Leaderboard created: no.
Release/export/tag created: no.
Retained evidence promoted: no.
`runs/user/` outputs committed: no.

Next safe action:
- Decide whether to document the context-free `sqlglot_optimize` limitation or authorize a separately named schema-aware SQLGlot route design; do not silently change the existing optimize route.

## 2026-05-22 - sqlglot_context_free_optimize_doc_warning_v0

Mode: documentation/audit only.

Legacy repo modified: no.
Release repo modified: yes.

Metadata correction note:
- Preflight found that `project_control/MIGRATION_STATUS.md` and `project_control/MIGRATION_RUN_LOG.md` already contained `sqlglot_optimize_cons0005_triage_v0` entries.
- Those prior entries did not explicitly record final triage commit/push metadata.
- Non-destructive metadata note for the prior triage: final commit `98b4e9e`; push result `pushed to origin/feature/case-package-v2-external-schema`.

Files created:
- `audits/sqlglot_context_free_optimize_doc_warning_v0/README.md`
- `audits/sqlglot_context_free_optimize_doc_warning_v0/documentation_change_summary.md`
- `audits/sqlglot_context_free_optimize_doc_warning_v0/protected_surface_check.md`
- `audits/sqlglot_context_free_optimize_doc_warning_v0/command_log.md`
- `audits/sqlglot_context_free_optimize_doc_warning_v0/boundary_checklist.md`

Files modified:
- `baselines/sqlglot/README.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- Passed project-control readability, Markdown sanity checks for the updated SQLGlot README and audit files, `git diff --check`, and protected-surface checks.
- Confirmed no `src/`, tests, cases, manifests, SQL, schemas, checker configs, validation scripts, `case_sets/`, reports/results, retained evidence, adapter-code, or `runs/user/` outputs were changed or committed.

Denominator changed: no.
Paper results changed: no.
Case membership changed: no.
Raw retained evidence changed: no.
Reports/results changed: no.
Official metrics computed: no.
Timing/speedup computed: no.
Leaderboard created: no.
Release/export/tag created: no.
Retained evidence promoted: no.
`runs/user/` outputs committed: no.
Adapter behavior changed: no.
Schema-aware route added: no.
Broader SQLGlot trial performed: no.

Next safe action:
- Keep the current context-free optimize route fail-visible, or authorize a separately named schema-aware SQLGlot route design; do not silently change the existing optimize route.

## 2026-05-22 - common_core_tri_engine_sqlglot_noop_local_diagnostic_snapshot_v0

Mode: full-chain local diagnostic snapshot only.

Legacy repo modified: no.
Release repo modified: yes.

Adapter command:
- `python baselines/sqlglot/sqlglot_user_adapter.py --route noop`

Run paths:
- `runs/user/common_core_sqlglot_noop_postgres_snapshot`
- `runs/user/common_core_sqlglot_noop_mysql_snapshot`
- `runs/user/common_core_sqlglot_noop_spark_snapshot`

Files created:
- `audits/common_core_tri_engine_sqlglot_noop_local_diagnostic_snapshot_v0/README.md`
- `audits/common_core_tri_engine_sqlglot_noop_local_diagnostic_snapshot_v0/route_summary.csv`
- `audits/common_core_tri_engine_sqlglot_noop_local_diagnostic_snapshot_v0/engine_summary.csv`
- `audits/common_core_tri_engine_sqlglot_noop_local_diagnostic_snapshot_v0/failure_buckets.csv`
- `audits/common_core_tri_engine_sqlglot_noop_local_diagnostic_snapshot_v0/status_summary.json`
- `audits/common_core_tri_engine_sqlglot_noop_local_diagnostic_snapshot_v0/tag_slice_summary.csv`
- `audits/common_core_tri_engine_sqlglot_noop_local_diagnostic_snapshot_v0/command_log.md`
- `audits/common_core_tri_engine_sqlglot_noop_local_diagnostic_snapshot_v0/protected_surface_check.md`
- `audits/common_core_tri_engine_sqlglot_noop_local_diagnostic_snapshot_v0/boundary_checklist.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- Passed project-control readability, audit Markdown/CSV/JSON sanity checks, `git diff --check`, and protected-surface checks.
- Confirmed no `src/`, tests, `baselines/sqlglot/`, cases, manifests, SQL files, schemas, checker configs, validation scripts, `case_sets/`, reports/results, retained evidence, or committed `runs/user/` outputs changed.

Diagnostic result:
- Overall planned/selected rows: 120.
- Overall funnel: adapter invoked 120, candidate generated 115, preflight passed 115, source executable 110, candidate executable 101, checker attempted 101, exact 91, mismatch 10, source-like/no-op 6, unsupported/fail-closed 5.
- PostgreSQL: selected 40, generated 35, source/candidate/checker/exact/mismatch 35/35/35/35/0; failure buckets `adapter_failed=5`, `none=35`.
- MySQL: selected 40, generated 40, source/candidate/checker/exact/mismatch 40/39/39/31/8; failure buckets `candidate_execution_failed=1`, `mismatch=8`, `none=31`.
- Spark: selected 40, generated 40, source/candidate/checker/exact/mismatch 35/27/27/25/2; failure buckets `candidate_execution_failed=8`, `mismatch=2`, `none=25`, `unsupported_engine=5`.
- Tag slices generated: yes, for all three runs.

Denominator changed: no.
Paper results changed: no.
Case membership changed: no.
Raw retained evidence changed: no.
Reports/results changed: no.
Official metrics computed: no.
Timing/speedup computed: no.
Leaderboard created: no.
Release/export/tag created: no.
Retained evidence promoted: no.
`runs/user/` outputs committed: no.
SQLGlot optimize route run: no.
Adapter behavior changed: no.

Next safe action:
- Triage the fail-visible SQLGlot noop failures before any broader real-adapter interpretation, keeping same-engine rows, real PORT adapter rows, controlled target-reference rows, and unsupported/fail-closed rows separate.

## 2026-05-22 - common_core_sqlglot_noop_failure_triage_v0

Mode: audit-only failure triage.

Legacy repo modified: no.
Release repo modified: yes.

Files created:
- `audits/common_core_sqlglot_noop_failure_triage_v0/README.md`
- `audits/common_core_sqlglot_noop_failure_triage_v0/failure_triage_matrix.csv`
- `audits/common_core_sqlglot_noop_failure_triage_v0/per_engine_failure_summary.csv`
- `audits/common_core_sqlglot_noop_failure_triage_v0/port_vs_nonport_summary.csv`
- `audits/common_core_sqlglot_noop_failure_triage_v0/candidate_examples.md`
- `audits/common_core_sqlglot_noop_failure_triage_v0/recommendation.md`
- `audits/common_core_sqlglot_noop_failure_triage_v0/protected_surface_check.md`
- `audits/common_core_sqlglot_noop_failure_triage_v0/command_log.md`
- `audits/common_core_sqlglot_noop_failure_triage_v0/boundary_checklist.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- Passed project-control readability, audit Markdown/CSV sanity checks, `git diff --check`, protected-surface checks, and `runs/user/` uncommitted-output check.
- Confirmed no `src/`, tests, `baselines/sqlglot/`, cases, manifests, SQL files, schemas, checker configs, validation scripts, `case_sets/`, reports/results, retained evidence, or committed `runs/user/` outputs changed.

Triage result:
- PostgreSQL: 5 PORT SQLGlot parse/emit failures before candidate generation.
- MySQL: 1 PORT candidate execution syntax/runtime failure, 3 PORT real-adapter semantic mismatches, and 5 checker/normalization gap candidates where values matched but expression labels differed.
- Spark: 6 non-PORT same-engine candidate execution/preflight-backend investigation candidates rejected as not exactly one statement, 2 PORT target candidate execution failures, 2 PORT real-adapter semantic mismatches, and 5 expected unsupported/fail-closed PORT rows.
- Source execution issue found: no.
- SQLGlot optimize run: no.
- Full Common-core rerun: no.

Denominator changed: no.
Paper results changed: no.
Case membership changed: no.
Raw retained evidence changed: no.
Reports/results changed: no.
Official metrics computed: no.
Timing/speedup computed: no.
Leaderboard created: no.
Release/export/tag created: no.
Retained evidence promoted: no.
`runs/user/` outputs committed: no.
Benchmark code patched: no.
SQLGlot adapter behavior changed: no.
Checker normalization patched: no.
Engine backends patched: no.

Next safe action:
- Keep failures visible; separately authorize SQLGlot PORT route/dialect documentation, same-engine checker label-policy triage, or Spark statement/preflight investigation if desired.

## 2026-05-22 - spark_sqlglot_noop_statement_preflight_triage_v0

Mode: audit-only Spark statement-boundary triage.

Legacy repo modified: no.
Release repo modified: yes.

Files created:
- `audits/spark_sqlglot_noop_statement_preflight_triage_v0/README.md`
- `audits/spark_sqlglot_noop_statement_preflight_triage_v0/affected_rows.csv`
- `audits/spark_sqlglot_noop_statement_preflight_triage_v0/candidate_statement_examples.md`
- `audits/spark_sqlglot_noop_statement_preflight_triage_v0/root_cause_matrix.csv`
- `audits/spark_sqlglot_noop_statement_preflight_triage_v0/recommendation.md`
- `audits/spark_sqlglot_noop_statement_preflight_triage_v0/protected_surface_check.md`
- `audits/spark_sqlglot_noop_statement_preflight_triage_v0/command_log.md`
- `audits/spark_sqlglot_noop_statement_preflight_triage_v0/boundary_checklist.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- Passed project-control readability, audit Markdown/CSV sanity checks, `git diff --check`, protected-surface checks, and `runs/user/` uncommitted-output check.
- Confirmed no `src/`, tests, `baselines/sqlglot/`, cases, manifests, SQL files, schemas, checker configs, validation scripts, `case_sets/`, reports/results, retained evidence, or committed `runs/user/` outputs changed.

Triage result:
- Affected rows: `PERF_0008`, `PERF_0013`, `PERF_0017`, `PERF_0019`, `PERF_0024`, and `PERF_0082`.
- All six candidates passed user-entry preflight and all six sources executed successfully.
- All six candidates failed Spark candidate execution at the local diagnostic statement-count guard with `Spark diagnostic query must contain exactly one statement`.
- Root cause category: Spark local diagnostic statement splitter / preflight consistency gap.
- SQLGlot noop emitted one query with leading `/* ... */` block comments and a trailing semicolon. The block comments preserve metadata/provenance semicolons.
- Candidate preflight ignores semicolons inside block comments, but the Spark splitter currently strips only full-line `--` comments and splits on semicolons inside block comments.

Denominator changed: no.
Paper results changed: no.
Case membership changed: no.
Raw retained evidence changed: no.
Reports/results changed: no.
Official metrics computed: no.
Timing/speedup computed: no.
Leaderboard created: no.
Release/export/tag created: no.
Retained evidence promoted: no.
`runs/user/` outputs committed: no.
Code/checker/backend patched: no.
Common-core rerun performed: no.
SQLGlot optimize run: no.

Commit hash:
- Pending.

Push result:
- Pending.

Next safe action:
- Keep rows fail-visible or authorize a narrow Spark statement-boundary/preflight patch with regression coverage for block-comment semicolons, string-literal semicolons, trailing semicolon handling, and genuine multi-statement rejection.

## 2026-05-22 - spark_statement_boundary_comment_aware_patch_v0

Mode: narrow local-diagnostic infrastructure consistency patch.

Legacy repo modified: no.
Release repo modified: yes.

Files created:
- `audits/spark_statement_boundary_comment_aware_patch_v0/README.md`
- `audits/spark_statement_boundary_comment_aware_patch_v0/patch_summary.md`
- `audits/spark_statement_boundary_comment_aware_patch_v0/regression_tests.md`
- `audits/spark_statement_boundary_comment_aware_patch_v0/affected_rows_before_after.csv`
- `audits/spark_statement_boundary_comment_aware_patch_v0/command_log.md`
- `audits/spark_statement_boundary_comment_aware_patch_v0/protected_surface_check.md`
- `audits/spark_statement_boundary_comment_aware_patch_v0/boundary_checklist.md`

Files modified:
- `src/sql_rewrite_bench/candidate_preflight.py`
- `src/sql_rewrite_bench/spark_execution.py`
- `tests/user_entry/test_candidate_preflight.py`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- Passed focused candidate-preflight/Spark statement-boundary tests, full `tests/user_entry` suite, Python compile checks, environment check, targeted six-row Spark SQLGlot noop rerun, Spark two-case SQLGlot noop smoke, project-control readability, audit Markdown/CSV sanity checks, `git diff --check`, protected-surface checks, and `runs/user/` uncommitted-output check.
- Confirmed no `baselines/sqlglot/`, cases, manifests, SQL files, schemas, checker configs, validation scripts, `case_sets/`, reports/results, retained evidence, or committed `runs/user/` outputs changed.

Patch result:
- Root cause addressed: Spark statement splitting now reuses candidate preflight's comment-aware statement splitter.
- Block comments containing semicolons, line comments containing semicolons, string-literal semicolons, double-quoted identifier semicolons, and backtick identifier semicolons are treated as part of a single statement.
- Genuine multi-statement SQL remains rejected.
- Existing Spark full-line `--` comment normalization remains in place.

Targeted affected-row rerun:
- Run path: `runs/user/spark_sqlglot_noop_statement_boundary_after_patch`.
- Selected rows: 6.
- Candidate generated rows: 6.
- Candidate preflight passed rows: 6.
- Source/candidate executable rows: 6/6.
- Checker attempted/exact/mismatch rows: 6/6/0.

Spark smoke:
- Run path: `runs/user/spark_sqlglot_noop_two_case_smoke_after_statement_patch`.
- Cases: `PERF_0006`, `CONS_0005`.
- Source/candidate executable rows: 2/2.
- Checker attempted/exact/mismatch rows: 2/2/0.

Denominator changed: no.
Paper results changed: no.
Case membership changed: no.
Raw retained evidence changed: no.
Reports/results changed: no.
Official metrics computed: no.
Timing/speedup computed: no.
Leaderboard created: no.
Release/export/tag created: no.
Retained evidence promoted: no.
`runs/user/` outputs committed: no.
SQLGlot adapter behavior changed: no.
Checker normalization changed: no.
Full Common-core rerun performed: no.
SQLGlot optimize run: no.

Commit hash:
- Pending.

Push result:
- Pending.

Next safe action:
- Optionally authorize a broader Common-core Spark SQLGlot noop local diagnostic snapshot to confirm aggregate failure-bucket movement while keeping PORT real-adapter and unsupported/fail-closed rows separate.

## 2026-05-22 - common_core_spark_sqlglot_noop_after_statement_patch_v0

Mode: Spark-only Common-core SQLGlot noop local diagnostic snapshot.

Legacy repo modified: no.
Release repo modified: yes.

Metadata correction:
- The prior `spark_statement_boundary_comment_aware_patch_v0` entry still recorded commit hash and push result as pending.
- Non-destructive correction: prior task final commit was `b62c41c`, pushed to `origin/feature/case-package-v2-external-schema`.

Files created:
- `audits/common_core_spark_sqlglot_noop_after_statement_patch_v0/README.md`
- `audits/common_core_spark_sqlglot_noop_after_statement_patch_v0/aggregate_comparison.csv`
- `audits/common_core_spark_sqlglot_noop_after_statement_patch_v0/affected_statement_rows.csv`
- `audits/common_core_spark_sqlglot_noop_after_statement_patch_v0/remaining_failures.csv`
- `audits/common_core_spark_sqlglot_noop_after_statement_patch_v0/status_summary.json`
- `audits/common_core_spark_sqlglot_noop_after_statement_patch_v0/command_log.md`
- `audits/common_core_spark_sqlglot_noop_after_statement_patch_v0/protected_surface_check.md`
- `audits/common_core_spark_sqlglot_noop_after_statement_patch_v0/boundary_checklist.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- Passed audit Markdown/CSV/JSON sanity checks, project-control readability checks, `git diff --check`, protected-surface checks, and `runs/user/` uncommitted-output check.
- Confirmed no `src/`, tests, `baselines/sqlglot/`, cases, manifests, SQL files, schemas, checker configs, validation scripts, `case_sets/`, reports/results, retained evidence, or committed `runs/user/` outputs changed.

Run path:
- `runs/user/common_core_spark_sqlglot_noop_after_statement_patch`

Diagnostic result:
- Selected rows: 40.
- Candidate generated/preflight passed rows: 40/40.
- Source/candidate/checker rows: 35/33/33.
- Exact/mismatch rows: 31/2.
- Failure buckets: `none=31`, `candidate_execution_failed=2`, `mismatch=2`, `unsupported_engine=5`.
- Diagnostic modes: `same_engine=31`, `cross_dialect_reference=4`, `unsupported=5`.

Before/after movement:
- Previous Spark snapshot source/candidate/checker rows: 35/27/27; after: 35/33/33.
- Previous exact/mismatch rows: 25/2; after: 31/2.
- Previous candidate execution failed rows: 8; after: 2.
- Previous unsupported rows: 5; after: 5.
- Statement-boundary rows resolved: `PERF_0008`, `PERF_0013`, `PERF_0017`, `PERF_0019`, `PERF_0024`, and `PERF_0082`.

Remaining failures:
- Candidate execution failed: `PORT_0003`, `PORT_0013`.
- Mismatch: `PORT_0004`, `PORT_0005`.
- Unsupported/fail-closed: `PORT_0008`, `PORT_0012`, `PORT_0022`, `PORT_0024`, `PORT_0025`.

Denominator changed: no.
Paper results changed: no.
Case membership changed: no.
Raw retained evidence changed: no.
Reports/results changed: no.
Official metrics computed: no.
Timing/speedup computed: no.
Leaderboard created: no.
Release/export/tag created: no.
Retained evidence promoted: no.
`runs/user/` outputs committed: no.
PostgreSQL engine snapshot run: no.
MySQL engine snapshot run: no.
SQLGlot optimize run: no.

Commit hash:
- Pending.

Push result:
- Pending.

Next safe action:
- Keep remaining PORT SQLGlot noop failures fail-visible, or separately authorize PORT real-adapter route/dialect triage without mixing real-adapter rows with controlled target-reference diagnostics.

## 2026-05-22 - sqlglot_noop_common_core_local_diagnostic_closeout_v0

Mode: audit-only local diagnostic closeout.

Legacy repo modified: no.
Release repo modified: yes.

Files created:
- `audits/sqlglot_noop_common_core_local_diagnostic_closeout_v0/README.md`
- `audits/sqlglot_noop_common_core_local_diagnostic_closeout_v0/engine_current_summary.csv`
- `audits/sqlglot_noop_common_core_local_diagnostic_closeout_v0/remaining_failure_matrix.csv`
- `audits/sqlglot_noop_common_core_local_diagnostic_closeout_v0/spark_before_after_patch_summary.csv`
- `audits/sqlglot_noop_common_core_local_diagnostic_closeout_v0/closeout_status.json`
- `audits/sqlglot_noop_common_core_local_diagnostic_closeout_v0/recommendation.md`
- `audits/sqlglot_noop_common_core_local_diagnostic_closeout_v0/protected_surface_check.md`
- `audits/sqlglot_noop_common_core_local_diagnostic_closeout_v0/command_log.md`
- `audits/sqlglot_noop_common_core_local_diagnostic_closeout_v0/boundary_checklist.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- Passed project-control readability checks, audit Markdown/CSV/JSON sanity checks, `git diff --check`, protected-surface checks, and `runs/user/` uncommitted-output check.
- Confirmed no `src/`, tests, `baselines/sqlglot/`, cases, manifests, SQL files, schemas, checker configs, validation scripts, `case_sets/`, reports/results, retained evidence, or committed `runs/user/` outputs changed.

Closeout result:
- Verdict: `closed_with_fail_visible_limitations`.
- PostgreSQL current status: selected 40, generated/preflight 35/35, source/candidate/checker 35/35/35, exact/mismatch 35/0, with five PORT adapter parse/emit failures.
- MySQL current status: selected 40, generated/preflight 40/40, source/candidate/checker 40/39/39, exact/mismatch 31/8, with one PORT candidate execution failure, three PORT real-adapter semantic mismatches, and five label-only checker/normalization candidates including `PERF_0062`.
- Spark current status after statement-boundary patch: selected 40, generated/preflight 40/40, source/candidate/checker 35/33/33, exact/mismatch 31/2.
- Spark non-PORT same-engine status: exact 31/31.
- Six prior Spark statement-boundary false failures are exact: `PERF_0008`, `PERF_0013`, `PERF_0017`, `PERF_0019`, `PERF_0024`, and `PERF_0082`.
- Remaining Spark failures are PORT-only or explicit unsupported/fail-closed roles.

Combined current funnel:
- Selected rows: 120.
- Candidate generated/preflight passed rows: 115/115.
- Source/candidate/checker rows: 110/107/107.
- Exact/mismatch rows: 97/10.
- Failure buckets: `adapter_failed=5`, `candidate_execution_failed=3`, `mismatch=10`, `none=97`, `unsupported_engine=5`.

Reruns performed:
- PostgreSQL: no.
- MySQL: no.
- Spark: no.
- SQLGlot optimize: no.

Denominator changed: no.
Paper results changed: no.
Case membership changed: no.
Raw retained evidence changed: no.
Reports/results changed: no.
Official metrics computed: no.
Timing/speedup computed: no.
Leaderboard created: no.
Release/export/tag created: no.
Retained evidence promoted: no.
`runs/user/` outputs committed: no.
Code/checker/backend patched: no.

Commit hash:
- Pending.

Push result:
- Pending.

Next safe action:
- Choose whether to authorize MySQL label-policy triage, SQLGlot noop PORT limitation documentation, a target-aware SQLGlot route design, or pause the SQLGlot line.

## 2026-05-22 - mysql_label_policy_triage_v0

Mode: audit-only MySQL SQLGlot noop label-policy triage.

Legacy repo modified: no.
Release repo modified: yes.

Files created:
- `audits/mysql_label_policy_triage_v0/README.md`
- `audits/mysql_label_policy_triage_v0/label_policy_triage_matrix.csv`
- `audits/mysql_label_policy_triage_v0/value_vs_label_examples.md`
- `audits/mysql_label_policy_triage_v0/recommendation.md`
- `audits/mysql_label_policy_triage_v0/protected_surface_check.md`
- `audits/mysql_label_policy_triage_v0/command_log.md`
- `audits/mysql_label_policy_triage_v0/boundary_checklist.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- Passed project-control readability checks, audit Markdown/CSV sanity checks, `git diff --check`, protected-surface checks, and `runs/user/` uncommitted-output checks.
- Confirmed no `src/`, tests, `baselines/sqlglot/`, cases, manifests, SQL files, schemas, checker configs, validation scripts, `case_sets/`, reports/results, retained evidence, or committed `runs/user/` outputs changed.

Triage result:
- Rows inspected: `PERF_0062`, `PORT_0004`, `PORT_0013`, `PORT_0022`, and `PORT_0024`.
- All five rows had source/candidate execution success and checker mismatch in `runs/user/common_core_sqlglot_noop_mysql_snapshot`.
- Source/candidate values matched positionally for every inspected row.
- Row counts were equal, row ordering was not implicated, duplicate/multiplicity differences were not observed, and numeric/string/null normalization differences were not observed.
- The only observed differences were MySQL expression result labels: aggregate function label case for `PERF_0062`, and expression whitespace/formatting labels for the PORT rows.
- Classification: `PERF_0062` is a same-engine non-PORT label-only mismatch candidate; `PORT_0004`, `PORT_0013`, `PORT_0022`, and `PORT_0024` are same-engine PORT label-only mismatch candidates in the SQLGlot noop real-adapter surface.

Denominator changed: no.
Paper results changed: no.
Case membership changed: no.
Reports/results changed: no.
Raw retained evidence changed: no.
Official metrics computed: no.
Timing/speedup computed: no.
Leaderboard created: no.
Release/export/tag created: no.
Retained evidence promoted: no.
`runs/user/` outputs committed: no.
Checker behavior changed: no.
SQLGlot adapter behavior changed: no.
Common-core rerun performed: no.
SQLGlot optimize run: no.

Commit hash:
- Pending.

Push result:
- Pending.

Next safe action:
- Keep these rows fail-visible unless a separate task authorizes a narrow checker label-policy design/patch with PERF, CONS, LONGTAIL, same-engine PORT, and controlled PORT regression coverage.

## 2026-05-22 - checker_label_policy_design_v0

Mode: design/audit-only checker label-policy planning.

Legacy repo modified: no.
Release repo modified: yes.

Files created:
- `audits/checker_label_policy_design_v0/README.md`
- `audits/checker_label_policy_design_v0/current_behavior.md`
- `audits/checker_label_policy_design_v0/inspected_examples.md`
- `audits/checker_label_policy_design_v0/proposed_policy.md`
- `audits/checker_label_policy_design_v0/patch_options.md`
- `audits/checker_label_policy_design_v0/regression_plan.md`
- `audits/checker_label_policy_design_v0/risk_assessment.md`
- `audits/checker_label_policy_design_v0/protected_surface_check.md`
- `audits/checker_label_policy_design_v0/command_log.md`
- `audits/checker_label_policy_design_v0/boundary_checklist.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- Passed project-control readability checks, audit Markdown sanity checks, `git diff --check`, protected-surface checks, and `runs/user/` uncommitted-output checks.
- Confirmed no `src/`, tests, cases, checker configs, SQL files, `baselines/`, `case_sets/`, reports/results, retained evidence, or committed `runs/user/` outputs changed.

Design result:
- Current checker label behavior: same-engine comparison preserves JSON object keys and compares full normalized row dictionaries; result-column labels are part of exactness implicitly.
- Labels are not controlled by an explicit same-engine `compare_column_labels` or `label_policy` config today.
- Cross-dialect positional comparison is already manifest/role-gated and should remain separate from same-engine label policy.
- Proposed first patch: behavior-preserving label-only diagnostics that report `value_exact`, `label_exact`, and `label_only_mismatch` without changing `exact_status`.
- Explicit aliases should remain strict by default.
- Generated-expression labels should not be ignored unless case config or provenance explicitly says they are non-semantic.
- Any exactness-changing policy should be case/role opt-in only, with PERF, CONS, LONGTAIL, same-engine PORT, and controlled PORT regression coverage.

Denominator changed: no.
Paper results changed: no.
Case membership changed: no.
Reports/results changed: no.
Raw retained evidence changed: no.
Official metrics computed: no.
Timing/speedup computed: no.
Leaderboard created: no.
Release/export/tag created: no.
Retained evidence promoted: no.
`runs/user/` outputs committed: no.
Checker behavior changed: no.
Exact counts changed: no.
Common-core rerun performed: no.

Commit hash:
- Pending.

Push result:
- Pending.

Next safe action:
- Authorize a behavior-preserving checker label-only diagnostics patch, or pause with strict-label fail-visible behavior documented.

## 2026-05-22 - checker_label_only_diagnostics_patch_v0

Mode: behavior-preserving local diagnostic checker diagnostics patch.

Legacy repo modified: no.
Release repo modified: yes.

Metadata correction:
- `checker_label_policy_design_v0` final commit was `6236ba8` and was pushed to `origin/feature/case-package-v2-external-schema`; the previous run-log entry remains non-destructively preserved with pending metadata.

Files created:
- `audits/checker_label_only_diagnostics_patch_v0/README.md`
- `audits/checker_label_only_diagnostics_patch_v0/patch_summary.md`
- `audits/checker_label_only_diagnostics_patch_v0/regression_tests.md`
- `audits/checker_label_only_diagnostics_patch_v0/targeted_rows_before_after.csv`
- `audits/checker_label_only_diagnostics_patch_v0/diagnostic_fields_schema.md`
- `audits/checker_label_only_diagnostics_patch_v0/command_log.md`
- `audits/checker_label_only_diagnostics_patch_v0/protected_surface_check.md`
- `audits/checker_label_only_diagnostics_patch_v0/boundary_checklist.md`

Files modified:
- `src/sql_rewrite_bench/local_result_checker.py`
- `src/sql_rewrite_bench/user_quality_report.py`
- `tests/user_entry/test_cross_dialect_checker_normalization.py`
- `tests/user_entry/test_quality_report.py`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- Passed focused checker/quality-report tests, full `tests/user_entry`, project-control readability check, audit Markdown/CSV sanity checks, `git diff --check`, protected-surface checks, and `runs/user/` uncommitted-output checks.
- Confirmed no cases, manifests, SQL files, schemas, checker configs, validation scripts, `baselines/sqlglot/`, `case_sets/`, inventory, reports/results, retained evidence, or committed `runs/user/` outputs changed.

Patch result:
- Added behavior-preserving label-only mismatch diagnostics to local checker details and mismatch artifacts.
- Added local quality-summary diagnostic count `label_only_mismatch_rows`.
- Exact/mismatch semantics did not change.
- Label-only mismatches are not converted to exact.
- Strict labels remain the default policy.
- No case-local label policy was added.
- No global label-ignore behavior was introduced.
- Existing controlled cross-dialect role gates, including MySQL-source to Spark-target numeric normalization, remain preserved.

Targeted rerun:
- Run path: `runs/user/mysql_label_only_diagnostics_patch_check`.
- Case list: `PERF_0062`, `PORT_0004`, `PORT_0013`, `PORT_0022`, `PORT_0024`.
- Selected rows: 5.
- Candidate generated/preflight passed rows: 5/5.
- Source/candidate executable rows: 5/5.
- Checker attempted rows: 5.
- Exact/mismatch rows: 0/5.
- Label-only diagnostic rows: 5.
- Exact/mismatch changed: no.

Denominator changed: no.
Paper results changed: no.
Case membership changed: no.
Reports/results changed: no.
Raw retained evidence changed: no.
Official metrics computed: no.
Timing/speedup computed: no.
Leaderboard created: no.
Release/export/tag created: no.
Retained evidence promoted: no.
`runs/user/` outputs committed: no.
SQLGlot adapter behavior changed: no.
Checker normalization relaxed: no.
Common-core rerun performed: no, except targeted five-row diagnostic rerun.

Commit hash:
- Pending.

Push result:
- Pending.

Next safe action:
- Use label-only diagnostics to decide whether to keep these rows fail-visible, document the limitation, or separately authorize a case-local exactness-changing label policy patch.

## 2026-05-22 - strict_label_policy_documentation_v0

Mode: documentation-only user-entry checker policy clarification.

Legacy repo modified: no.
Release repo modified: yes.

Files created:
- `docs/user_entry_checker_policy.md`
- `audits/strict_label_policy_documentation_v0/README.md`
- `audits/strict_label_policy_documentation_v0/documentation_change_summary.md`
- `audits/strict_label_policy_documentation_v0/protected_surface_check.md`
- `audits/strict_label_policy_documentation_v0/command_log.md`
- `audits/strict_label_policy_documentation_v0/boundary_checklist.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- Passed Markdown sanity checks, project-control readability check, `git diff --check`, protected-surface checks, and `runs/user/` uncommitted-output checks.
- Confirmed no `src/`, tests, cases, checker configs, SQL files, `baselines/`, `case_sets/`, inventory, reports/results, retained evidence, or committed `runs/user/` outputs changed.

Documentation result:
- Created a dedicated user-entry checker policy document because no existing checker-policy document existed under `docs/`.
- Documented strict default `local_result_checker.py` behavior.
- Documented that same-engine JSONL result column labels/object keys are part of exactness.
- Documented that label-only mismatches remain `checker_mismatch`, `exact_status=mismatch`, and `failure_bucket=mismatch`.
- Documented diagnostic fields: `value_exact`, `label_exact`, `label_only_mismatch`, `label_policy`, `label_mismatch_class`, and `value_mismatch_reason`.
- Documented that `label_only_mismatch=true` is diagnostic visibility only, not a correctness relaxation.
- Documented that explicit alias differences remain strict and generated-expression labels are not automatically ignored.
- Documented that PORT real-adapter rows remain separate from controlled PORT target-reference diagnostics.
- Documented that any exactness-changing label policy requires separate case/role/config-gated authorization.

Denominator changed: no.
Paper results changed: no.
Case membership changed: no.
Reports/results changed: no.
Raw retained evidence changed: no.
Official metrics computed: no.
Timing/speedup computed: no.
Leaderboard created: no.
Release/export/tag created: no.
Retained evidence promoted: no.
`runs/user/` outputs committed: no.
Checker behavior changed: no.
Exact/mismatch semantics changed: no.
Case-local label policy added: no.
Global label-ignore behavior added: no.
Common-core rerun performed: no.

Commit hash:
- Pending.

Push result:
- Pending.

Next safe action:
- Keep label-only rows fail-visible under the documented strict policy unless a separate task authorizes a case- or role-gated exactness-changing label policy.

## 2026-05-22 - metrics_timing_skill_adapter_decision_record_v0

Mode: decision-recording and audit-only metrics/timing/skill-adapter planning.

Legacy repo modified: no.
Release repo modified: yes.

Files created:
- `audits/metrics_timing_skill_adapter_decision_record_v0/README.md`
- `audits/metrics_timing_skill_adapter_decision_record_v0/decision_summary.md`
- `audits/metrics_timing_skill_adapter_decision_record_v0/latest_paper_metric_scope.md`
- `audits/metrics_timing_skill_adapter_decision_record_v0/deferred_skill_adapter_scope.md`
- `audits/metrics_timing_skill_adapter_decision_record_v0/implementation_sequence.md`
- `audits/metrics_timing_skill_adapter_decision_record_v0/boundary_checklist.md`
- `audits/metrics_timing_skill_adapter_decision_record_v0/protected_surface_check.md`
- `audits/metrics_timing_skill_adapter_decision_record_v0/command_log.md`

Files modified:
- `project_control/DECISION_LOG.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- Passed project-control readability check, audit Markdown sanity check, `git diff --check`, protected-surface checks, and `runs/user/` uncommitted-output checks.
- Confirmed no `src/`, tests, scripts, cases, manifests, SQL files, schemas, checker configs, validation scripts, `baselines/`, `case_sets/`, inventory, reports/results, retained evidence, `repository_spec/`, `benchmark_spec/`, or committed `runs/user/` outputs changed.

Decision result:
- Added D032: `Latest paper metrics/timing phase and external skill-adapter deferral`.
- Recorded that user-entry local diagnostics are complete enough to support a transition to metrics/timing protocol alignment and performance-layer planning.
- Recorded latest-paper Table 6 target metric names and formulas from task context.
- Recorded that performance metrics are exact-gated and timed-gated.
- Recorded that timing artifacts must preserve source/candidate paired timing in the same engine/environment/run context before metrics scripts can compute performance.
- Recorded that Regression@20 remains a reporting diagnostic / open question unless separately confirmed as a formal latest-paper metric.
- Recorded that Positive Operation Coverage Rate and `skill/` integration are deferred until the collaborator's external operation-atom script and schema are stable.
- Recorded that operation atoms must not be inferred from taxonomy tags, SQL text, or `positive.sql` in the current phase.
- Recorded that D018 and `repository_spec/metrics_contract_v1.md` remain historical context requiring a latest-paper metrics contract delta/audit before implementation.

Paper/PDF note:
- No local copy of `Beyond_Faster_SQL (5).pdf` was found under `/home/tianci_gao`; latest-paper metric scope was recorded from the task context.

Implementation sequence recorded:
1. latest paper metrics/timing protocol alignment audit
2. timing artifact schema design
3. exact-gated local timing diagnostic implementation
4. non-official local metrics calculator for Coverage/Correctness/Performance/Generalization
5. external skill-adapter integration for POCR after collaborator script is ready
6. retained-evidence adapter / official metrics promotion
7. paper table renderer

Denominator changed: no.
Paper results changed: no.
Case membership changed: no.
Reports/results changed: no.
Raw retained evidence changed: no.
Official metrics computed: no.
Timing/speedup computed: no.
Metrics implementation performed: no.
Timing implementation performed: no.
POCR implemented: no.
Skill folders created: no.
Operation atoms inferred: no.
Paper tables rendered: no.
Leaderboard created: no.
Release/export/tag created: no.
Retained evidence promoted: no.
`runs/user/` outputs committed: no.

Commit hash:
- Pending.

Push result:
- Pending.

Next safe action:
- Run a latest-paper metrics/timing protocol alignment audit comparing D032/Table 6 to the existing metrics contract before any timing schema or metrics implementation work.

## 2026-05-22 - latest_paper_metrics_timing_protocol_alignment_v0

Mode: audit/design-only latest-paper metrics and timing protocol alignment.

Legacy repo modified: no.
Release repo modified: yes.

Files created:
- `audits/latest_paper_metrics_timing_protocol_alignment_v0/README.md`
- `audits/latest_paper_metrics_timing_protocol_alignment_v0/paper_table6_metric_extraction.md`
- `audits/latest_paper_metrics_timing_protocol_alignment_v0/repo_contract_delta.md`
- `audits/latest_paper_metrics_timing_protocol_alignment_v0/denominator_set_definitions.md`
- `audits/latest_paper_metrics_timing_protocol_alignment_v0/timing_protocol_alignment.md`
- `audits/latest_paper_metrics_timing_protocol_alignment_v0/proposed_timing_artifact_schema.md`
- `audits/latest_paper_metrics_timing_protocol_alignment_v0/proposed_metrics_input_schema.md`
- `audits/latest_paper_metrics_timing_protocol_alignment_v0/proposed_metrics_output_schema.md`
- `audits/latest_paper_metrics_timing_protocol_alignment_v0/pocr_external_skill_adapter_boundary.md`
- `audits/latest_paper_metrics_timing_protocol_alignment_v0/implementation_phase_plan.md`
- `audits/latest_paper_metrics_timing_protocol_alignment_v0/open_questions_for_human.md`
- `audits/latest_paper_metrics_timing_protocol_alignment_v0/protected_surface_check.md`
- `audits/latest_paper_metrics_timing_protocol_alignment_v0/command_log.md`
- `audits/latest_paper_metrics_timing_protocol_alignment_v0/boundary_checklist.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- Passed project-control readability check, audit Markdown sanity check, `git diff --check`, protected-surface checks, and `runs/user/` uncommitted-output checks.
- Confirmed no `src/`, tests, scripts, cases, manifests, SQL files, schemas, checker configs, validation scripts, `baselines/`, `case_sets/`, inventory, reports/results, retained evidence, `repository_spec/`, `benchmark_spec/`, `project_control/DECISION_LOG.md`, or committed `runs/user/` outputs changed.

Audit result:
- Verdict: `completed_with_pdf_unavailable_caveat`.
- No local `Beyond_Faster_SQL (5).pdf` was found under `/home/tianci_gao`, `/mnt/data`, or `/tmp`; latest Table 6 extraction uses D032/task context and should be rechecked against the PDF when available.
- Extracted latest-paper scope: Generation Rate, Execution Coverage Rate, Result Consistency Rate, Semantic Equivalence Rate, GM Speedup Ratio, Speedup Ratio Percentiles, Positive Operation Coverage Rate, Cross-Engine Execution Coverage Rate, Cross-Engine Result Consistency Rate, and Cross-Engine GM Speedup Ratio.
- Compared latest-paper metrics against `repository_spec/metrics_contract_v1.md` and `metrics_contract_v1_draft.md`.
- Identified key deltas: Attribution Coverage -> POCR; Speedup Retention -> Cross-Engine GM Speedup Ratio; Regression@20 remains diagnostic/open; generation is candidate emission separate from preflight/readiness; execution coverage and result consistency denominator semantics need human confirmation; Semantic Equivalence should report N.A./unknown where verifier evidence is absent; local diagnostics remain non-official.
- Defined denominator sets: `N_S`, `G_r`, `E_r`, `X_r`, `M_r`, `C_r`, `N_PORT`, `E_tgt_r`, `X_tgt_r`, and `M_tgt_r`.
- Proposed timing defaults: paired source/candidate timing, same engine/environment/run context, exact-gated eligibility, configurable warmup/repetitions/timeouts, median runtime, sample arrays, N.A. policy, cache/session metadata, and environment metadata.
- Proposed future timing artifact schema and metrics input/output schemas.
- Marked POCR and skill-adapter integration as deferred per D032.
- Recommended phases: timing artifact schema design, exact-gated local timing diagnostic, non-official local metrics calculator, POCR external skill-adapter integration after collaborator script readiness, retained-evidence/official metrics promotion, and paper table renderer.

Open questions surfaced:
- Regression@20 status.
- Candidate generation vs preflight/ready reporting.
- Execution Coverage numerator semantics.
- Semantic Equivalence N.A. policy.
- `C_r` selection/versioning for POCR.
- Stage B POCR evidence.
- Whether Cross-Engine GM Speedup Ratio fully replaces Speedup Retention.
- Target-engine source/reference timing requirements.
- Whether local timing diagnostics are allowed before official promotion.
- Promotion gate for local timing artifacts to official paper evidence.

Denominator changed: no.
Paper results changed: no.
Case membership changed: no.
Reports/results changed: no.
Raw retained evidence changed: no.
Official metrics computed: no.
Timing/speedup computed: no.
Metrics implementation performed: no.
Timing implementation performed: no.
POCR implemented: no.
Skill folders created: no.
Operation atoms inferred: no.
Paper tables rendered: no.
Leaderboard created: no.
Release/export/tag created: no.
Retained evidence promoted: no.
`runs/user/` outputs committed: no.

Commit hash:
- Pending.

Push result:
- Pending.

Next safe action:
- Authorize Phase 1 timing artifact schema design, still non-metric and local-diagnostic only.

## 2026-05-22 - timing_artifact_schema_design_v0

Mode: schema/design-only Phase 1 timing artifact design for exact-gated local timing diagnostics.

Legacy repo modified: no.
Release repo modified: yes.

Files created:
- `audits/timing_artifact_schema_design_v0/README.md`
- `audits/timing_artifact_schema_design_v0/timing_row_schema.md`
- `audits/timing_artifact_schema_design_v0/timing_policy_schema.md`
- `audits/timing_artifact_schema_design_v0/timing_environment_metadata_schema.md`
- `audits/timing_artifact_schema_design_v0/timing_status_and_na_policy.md`
- `audits/timing_artifact_schema_design_v0/exact_gating_and_denominator_policy.md`
- `audits/timing_artifact_schema_design_v0/local_vs_official_timing_boundary.md`
- `audits/timing_artifact_schema_design_v0/integration_points_with_user_run.md`
- `audits/timing_artifact_schema_design_v0/future_metrics_join_plan.md`
- `audits/timing_artifact_schema_design_v0/open_questions_for_human.md`
- `audits/timing_artifact_schema_design_v0/protected_surface_check.md`
- `audits/timing_artifact_schema_design_v0/command_log.md`
- `audits/timing_artifact_schema_design_v0/boundary_checklist.md`
- `repository_spec/timing_artifact_schema_v0_draft.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- Pending at writeback time; final validation recorded in the audit command log and final report.

Audit result:
- Verdict: `completed_with_metadata_correction`.
- D032 was present in `project_control/DECISION_LOG.md`.
- Prior latest-paper alignment commit `469b2b2` and `audits/latest_paper_metrics_timing_protocol_alignment_v0/` were present.
- Metadata correction: the prior `latest_paper_metrics_timing_protocol_alignment_v0` final commit was `469b2b2` and was pushed to `origin/feature/case-package-v2-external-schema`, although its older run-log entry still says pending.
- Designed exact-gated timing row schema, timing policy schema, timing environment metadata schema, timing status/N.A. policy, denominator-preserving eligibility policy, local-vs-official timing boundary, user-run integration points, and future metrics join plan.
- Created draft repository spec `repository_spec/timing_artifact_schema_v0_draft.md` as a design-only artifact.

Open questions surfaced:
- Whether local timing diagnostics are allowed for non-official user adapter runs before retained-evidence promotion.
- Whether timing sample arrays should live inline as JSON arrays or in per-row files referenced by path.
- Whether timing artifacts should store source/candidate SQL hashes.
- Whether source timing must be remeasured for every candidate route or can be reused within one local run under identical schema/session/cache policy.
- Default cache policy for local diagnostics.
- Partial timing sample failure policy.
- Label-only mismatch timing eligibility under strict current policy.
- Target-engine timing representation for Cross-Engine GM Speedup Ratio.
- Promotion gate from local timing artifacts to official retained timing evidence.
- Route-mixing prevention in future summaries.

Denominator changed: no.
Paper results changed: no.
Case membership changed: no.
Reports/results changed: no.
Raw retained evidence changed: no.
Official metrics computed: no.
Timing/speedup computed: no.
Timing implementation performed: no.
Metrics implementation performed: no.
POCR implemented: no.
Skill folders created: no.
Operation atoms inferred: no.
Paper tables rendered: no.
Leaderboard created: no.
Release/export/tag created: no.
Retained evidence promoted: no.
`runs/user/` outputs committed: no.

Commit hash:
- Pending.

Push result:
- Pending.

Next safe action:
- Review and approve the timing artifact schema and open questions before authorizing an exact-gated local timing diagnostic implementation task.

## 2026-05-22 - timing_schema_open_questions_resolution_v0

Mode: decision/audit-only timing schema open-question resolution.

Legacy repo modified: no.
Release repo modified: yes.

Files created:
- `audits/timing_schema_open_questions_resolution_v0/README.md`
- `audits/timing_schema_open_questions_resolution_v0/resolved_open_questions.md`
- `audits/timing_schema_open_questions_resolution_v0/approved_timing_defaults.md`
- `audits/timing_schema_open_questions_resolution_v0/phase2_implementation_requirements.md`
- `audits/timing_schema_open_questions_resolution_v0/remaining_risks.md`
- `audits/timing_schema_open_questions_resolution_v0/protected_surface_check.md`
- `audits/timing_schema_open_questions_resolution_v0/command_log.md`
- `audits/timing_schema_open_questions_resolution_v0/boundary_checklist.md`

Files modified:
- `repository_spec/timing_artifact_schema_v0_draft.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- Pending at writeback time; final validation recorded in the audit command log and final report.

Audit result:
- Verdict: `completed`.
- D032 was present in `project_control/DECISION_LOG.md`; `DECISION_LOG.md` was not modified because D032 already records the durable project-level timing/metrics and POCR deferral decision.
- Local `Beyond_Faster_SQL (5).pdf` was not found under `/home/tianci_gao`, `/mnt/data`, or `/tmp`; defaults were resolved from D032, the latest-paper alignment audit, and the timing artifact schema design packet.
- Metadata correction: prior `timing_artifact_schema_design_v0` final commit was `032fc2e` and was pushed to `origin/feature/case-package-v2-external-schema`, although its older run-log entry still says pending.
- Resolved Phase 2 defaults: local timing allowed before retained-evidence promotion only under local-only claim-boundary flags; inline sample arrays in v0 row JSON; required source/candidate SQL hashes; no cross-route source timing reuse in v0; default local policy warmup 1, measured repetitions 5, timeout 30 seconds, median statistic; cache/session/schema/execution-order policies recorded as metadata; partial timing failures visible with null speedup; strict label-only mismatches timing-ineligible; cross-engine timing requires target-engine paired source/reference and candidate timing in the same target-engine context; promotion requires a separate retained-evidence/official timing task; route mixing disallowed; POCR deferred.
- Updated `repository_spec/timing_artifact_schema_v0_draft.md` with a small approved-defaults note.

Denominator changed: no.
Paper results changed: no.
Case membership changed: no.
Reports/results changed: no.
Raw retained evidence changed: no.
Official metrics computed: no.
Timing/speedup computed: no.
Timing implementation performed: no.
Metrics implementation performed: no.
POCR implemented: no.
Skill folders created: no.
Paper tables rendered: no.
Leaderboard created: no.
Retained evidence promoted: no.
`runs/user/` outputs committed: no.

Commit hash:
- Pending.

Push result:
- Pending.

Next safe action:
- Authorize a narrow exact-gated local timing diagnostic implementation using these v0 defaults, still local-only and non-official.

## 2026-05-22 - exact_gated_local_timing_diagnostic_v0

Mode: local-diagnostic timing implementation only.

Legacy repo modified: no.
Release repo modified: yes.

Files created:
- `src/sql_rewrite_bench/local_timing.py`
- `tests/user_entry/test_local_timing.py`
- `audits/exact_gated_local_timing_diagnostic_v0/README.md`
- `audits/exact_gated_local_timing_diagnostic_v0/implementation_summary.md`
- `audits/exact_gated_local_timing_diagnostic_v0/timing_artifact_examples.md`
- `audits/exact_gated_local_timing_diagnostic_v0/bounded_timing_smoke_summary.csv`
- `audits/exact_gated_local_timing_diagnostic_v0/timing_status_counts.json`
- `audits/exact_gated_local_timing_diagnostic_v0/regression_tests.md`
- `audits/exact_gated_local_timing_diagnostic_v0/protected_surface_check.md`
- `audits/exact_gated_local_timing_diagnostic_v0/command_log.md`
- `audits/exact_gated_local_timing_diagnostic_v0/boundary_checklist.md`

Files modified:
- `src/sql_rewrite_bench/user_run.py`
- `src/sql_rewrite_bench/user_ledger.py`
- `src/sql_rewrite_bench/user_run_schema.py`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- Pending at writeback time; final validation recorded in the audit command log and final report.

Implementation result:
- Verdict: `completed`.
- Added opt-in `--collect-timing` plus `--timing-warmup`, `--timing-repetitions`, and `--timing-timeout`.
- Default timing policy: warmup 1, measured repetitions 5, timeout 30 seconds, median statistic.
- Timing remains disabled by default and requires DB execution plus checker.
- Exact-gated timing eligibility requires candidate generation, preflight success, source execution success, candidate execution success, checker success, strict exact status, no failure bucket, no label-only mismatch, and supported same-engine diagnostic mode.
- Per-row timing artifacts are written under `runs/user/{run_name}/timing/rows/`; `timing_policy.json`, `environment_metadata.json`, and `timing_summary.json` are written under `runs/user/{run_name}/timing/`.
- Non-exact, label-only mismatch, unsupported/fail-closed, and partial-failure rows remain visible with explicit `timing_na_reason` and null `speedup_ratio`.
- Per-row `speedup_ratio` is local diagnostic only and is present only for complete exact timed rows.

Bounded local timing smoke:
- Adapter: `python baselines/sqlglot/sqlglot_user_adapter.py --route noop`.
- Cases: `PERF_0006`, `CONS_0005`.
- PostgreSQL: selected 2, exact 2, timing eligible 2, timed 2.
- MySQL: selected 2, exact 2, timing eligible 2, timed 2.
- Spark: selected 2, exact 2, timing eligible 2, timed 2.
- Local run outputs remain under `runs/user/` and were not staged or committed.

Metadata correction:
- Prior `timing_schema_open_questions_resolution_v0` final commit was `b3ad644` and was pushed to `origin/feature/case-package-v2-external-schema`, although its older run-log entry still says pending.

Denominator changed: no.
Paper results changed: no.
Case membership changed: no.
Reports/results changed: no.
Raw retained evidence changed: no.
Official metrics computed: no.
Route-level metrics computed: no.
Local timing artifacts produced: yes, under ignored `runs/user/` output.
Local per-row diagnostic `speedup_ratio` produced for exact timed rows: yes.
Timing implementation performed: yes.
Metrics calculator implemented: no.
POCR implemented: no.
Skill folders created: no.
Operation atoms inferred: no.
Paper tables rendered: no.
Leaderboard created: no.
Release/export/tag created: no.
Retained evidence promoted: no.
`runs/user/` outputs committed: no.

Commit hash:
- Pending.

Push result:
- Pending.

Next safe action:
- Review the local timing artifacts and implementation, then separately authorize timing hardening or a non-official local metrics calculator if desired.

## 2026-05-22 - exact_gated_local_timing_artifact_review_v0

Mode: audit/review-only local timing artifact review.

Legacy repo modified: no.
Release repo modified: yes.

Files created:
- `audits/exact_gated_local_timing_artifact_review_v0/README.md`
- `audits/exact_gated_local_timing_artifact_review_v0/timing_artifact_schema_conformance.md`
- `audits/exact_gated_local_timing_artifact_review_v0/timing_row_field_check.csv`
- `audits/exact_gated_local_timing_artifact_review_v0/bounded_smoke_artifact_inventory.csv`
- `audits/exact_gated_local_timing_artifact_review_v0/exact_gating_review.md`
- `audits/exact_gated_local_timing_artifact_review_v0/local_vs_official_boundary_review.md`
- `audits/exact_gated_local_timing_artifact_review_v0/recommendation.md`
- `audits/exact_gated_local_timing_artifact_review_v0/protected_surface_check.md`
- `audits/exact_gated_local_timing_artifact_review_v0/command_log.md`
- `audits/exact_gated_local_timing_artifact_review_v0/boundary_checklist.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- Pending at writeback time; final validation recorded in the audit command log and final report.

Review result:
- Verdict: `completed`.
- Required prior commit `858511a9723f8648af4acea493f458e353bf0a92` was present.
- Project-control writeback for `exact_gated_local_timing_diagnostic_v0` was present.
- Metadata correction: prior `exact_gated_local_timing_diagnostic_v0` final commit was `858511a9723f8648af4acea493f458e353bf0a92` and was pushed to `origin/feature/case-package-v2-external-schema`, although its older run-log entry still says pending.
- Reviewed existing bounded SQLGlot noop timing smoke artifacts under `runs/user/timing_sqlglot_noop_postgres_smoke/`, `runs/user/timing_sqlglot_noop_mysql_smoke/`, and `runs/user/timing_sqlglot_noop_spark_smoke/`.
- Each reviewed run contained `timing_policy.json`, `environment_metadata.json`, `timing_summary.json`, and two per-row timing JSON artifacts.
- All six timing row artifacts contained the required v0 identity, exactness, timing, SQL hash, artifact path, and claim-boundary fields.
- All reviewed timing artifacts kept `local_diagnostic_only=true`, `official_metric_input=false`, `paper_result_input=false`, `retained_evidence_promoted=false`, and `leaderboard_input=false`.
- Bounded smoke exact rows were timed; non-exact, label-only mismatch, unsupported/fail-closed, and partial-failure behavior remains covered by committed regression tests and prior implementation audit.
- No schema-blocking gap was found.

Denominator changed: no.
Paper results changed: no.
Case membership changed: no.
Reports/results changed: no.
Raw retained evidence changed: no.
Official metrics computed: no.
Route-level metrics computed: no.
Timing/speedup newly computed: no, except reviewing existing local timing smoke artifacts.
Metrics calculator implemented: no.
POCR implemented: no.
Skill folders created: no.
Paper tables rendered: no.
Leaderboard created: no.
Retained evidence promoted: no.
`runs/user/` outputs committed: no.

Commit hash:
- Pending.

Push result:
- Pending.

Next safe action:
- Separately authorize a non-official local metrics calculator only if route-aware, denominator-aware, exact/timed-gated, and local-only boundaries remain explicit.

## 2026-05-22 - local_metrics_v0_final_formula_decision_v0

Mode: decision/audit-only local metrics formula decision.

Legacy repo modified: no.
Release repo modified: yes.

Files created:
- `audits/local_metrics_v0_final_formula_decision_v0/README.md`
- `audits/local_metrics_v0_final_formula_decision_v0/formula_decision_summary.md`
- `audits/local_metrics_v0_final_formula_decision_v0/metric_scope_v0.md`
- `audits/local_metrics_v0_final_formula_decision_v0/deferred_metrics.md`
- `audits/local_metrics_v0_final_formula_decision_v0/boundary_checklist.md`
- `audits/local_metrics_v0_final_formula_decision_v0/command_log.md`
- `audits/local_metrics_v0_final_formula_decision_v0/protected_surface_check.md`

Files modified:
- `project_control/DECISION_LOG.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- Pending at writeback time; final validation recorded in the audit command log and final report.

Decision result:
- Verdict: `completed`.
- Decision number used: D033.
- Regression@20 removed from formal local metrics v0 implementation scope; it may remain legacy/reporting diagnostic only.
- Generation Rate: `candidate_generated / selected`.
- `preflight_passed` remains a funnel diagnostic, not part of Generation Rate.
- Execution Coverage Rate: `candidate_executable / selected`.
- `source_executable` remains a diagnostic/environment guard, not a numerator condition.
- Result Consistency Rate: `exact / selected`.
- Semantic Equivalence Rate is `N.A.` unless formal verifier evidence exists; local result checker output is not a substitute.
- GM Speedup Ratio and Speedup Ratio Percentiles are computed only over strict exact + timed rows.
- `label_only_mismatch` remains mismatch and timing-ineligible under the strict-label policy.
- Cross-Engine GM Speedup Ratio replaces old Speedup Retention in latest-paper alignment, but is `N.A.` unless target-engine paired timing exists.
- POCR remains deferred pending collaborator external skill script and stable `skill/` schema.
- No skill folders or operation atoms are authorized now.
- Local paper PDF was not found locally; this matches prior latest-paper alignment audit caveats.

Denominator changed: no.
Paper results changed: no.
Case membership changed: no.
Reports/results changed: no.
Raw retained evidence changed: no.
Official metrics computed: no.
Route-level metrics computed: no.
Metrics calculator implemented: no.
Timing/speedup newly computed: no.
Common-core run performed: no.
POCR implemented: no.
Skill folders created: no.
Operation atoms inferred: no.
Paper tables rendered: no.
Leaderboard created: no.
Retained evidence promoted: no.
`runs/user/` outputs committed: no.

Commit hash:
- Pending.

Push result:
- Pending.

Next safe action:
- Authorize a non-official local metrics calculator v0 implementation for local diagnostic Coverage, Result Consistency, and exact+timed Performance only, preserving route/denominator/timing-policy boundaries and local-only claims.

## 2026-05-22 - non_official_local_metrics_calculator_v0

Mode: local-only non-official metrics calculator implementation.

Legacy repo modified: no.
Release repo modified: yes.

Files created:
- `src/sql_rewrite_bench/local_metrics.py`
- `scripts/dev/compute_local_user_metrics.py`
- `tests/user_entry/test_local_metrics.py`
- `audits/non_official_local_metrics_calculator_v0/README.md`
- `audits/non_official_local_metrics_calculator_v0/implementation_summary.md`
- `audits/non_official_local_metrics_calculator_v0/metric_definitions_used.md`
- `audits/non_official_local_metrics_calculator_v0/local_metrics_output_schema.md`
- `audits/non_official_local_metrics_calculator_v0/bounded_metrics_smoke_summary.md`
- `audits/non_official_local_metrics_calculator_v0/validation_results.md`
- `audits/non_official_local_metrics_calculator_v0/protected_surface_check.md`
- `audits/non_official_local_metrics_calculator_v0/command_log.md`
- `audits/non_official_local_metrics_calculator_v0/boundary_checklist.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- Pending at writeback time; final validation recorded in the audit command log and final report.

Implementation result:
- Verdict: `completed`.
- D033 preflight passed: commit `2990340ec5a0d4682288e125606caf85d146d558` was present and D033 was recorded in `project_control/DECISION_LOG.md`.
- Metadata correction: prior `local_metrics_v0_final_formula_decision_v0` final commit was `2990340ec5a0d4682288e125606caf85d146d558` and was pushed to `origin/feature/case-package-v2-external-schema`, although its older run-log entry still says pending.
- Implemented local-only calculator outputs under `runs/user/{run_name}/metrics/`: `local_metrics_summary.json`, `local_metrics_by_engine.csv`, `local_metrics_by_pool.csv`, `local_timing_speedup_rows.csv`, and `local_metrics_boundary.md`.
- Implemented Generation Rate as `candidate_generated / selected`.
- Kept `preflight_passed` as a funnel diagnostic, not a Generation Rate numerator condition.
- Implemented Execution Coverage Rate as `candidate_executable / selected`.
- Kept `source_executable` as a diagnostic/environment guard, not an Execution Coverage numerator condition.
- Implemented Result Consistency Rate as `exact / selected`.
- Implemented GM Speedup Ratio and Speedup Ratio Percentiles P10/P25/P50/P75/P90 only over strict exact + timed rows.
- Kept label-only mismatches as mismatch and timing-ineligible.
- Semantic Equivalence Rate, Cross-Engine GM Speedup Ratio, POCR, and Regression@20 remain N.A./deferred/not implemented under D033.
- No winner, best-method, ranking, or leaderboard output is emitted.

Bounded local metrics smoke:
- Input runs: `runs/user/timing_sqlglot_noop_postgres_smoke/`, `runs/user/timing_sqlglot_noop_mysql_smoke/`, and `runs/user/timing_sqlglot_noop_spark_smoke/`.
- PostgreSQL: selected 2, candidate_generated 2, candidate_executable 2, exact 2, timed 2, speedup denominator 2, local GM speedup 0.9958493720356396.
- MySQL: selected 2, candidate_generated 2, candidate_executable 2, exact 2, timed 2, speedup denominator 2, local GM speedup 1.0001388459335048.
- Spark: selected 2, candidate_generated 2, candidate_executable 2, exact 2, timed 2, speedup denominator 2, local GM speedup 1.0296001429221677.
- Metrics smoke outputs remain under ignored `runs/user/*/metrics/` and were not staged or committed.

Denominator changed: no.
Paper results changed: no.
Case membership changed: no.
Reports/results changed: no.
Raw retained evidence changed: no.
Official metrics computed: no.
Local diagnostic metrics computed: yes.
Route-level paper metrics computed: no.
Timing/speedup official: no.
Metrics calculator implemented: yes.
POCR implemented: no.
Skill folders created: no.
Operation atoms inferred: no.
Paper tables rendered: no.
Leaderboard created: no.
Retained evidence promoted: no.
`runs/user/` outputs committed: no.

Commit hash:
- Pending.

Push result:
- Pending.

Next safe action:
- Review the non-official local metrics output shape, then separately authorize broader local diagnostic projection only if local-only and non-official boundaries remain explicit.

## 2026-05-22 - local_metrics_output_shape_review_v0

Mode: audit/review-only local metrics output-shape review.

Legacy repo modified: no.
Release repo modified: yes.

Files created:
- `audits/local_metrics_output_shape_review_v0/README.md`
- `audits/local_metrics_output_shape_review_v0/output_file_inventory.csv`
- `audits/local_metrics_output_shape_review_v0/summary_json_shape_review.md`
- `audits/local_metrics_output_shape_review_v0/csv_shape_review.md`
- `audits/local_metrics_output_shape_review_v0/boundary_flags_review.md`
- `audits/local_metrics_output_shape_review_v0/route_denominator_guard_review.md`
- `audits/local_metrics_output_shape_review_v0/issues_and_recommendations.md`
- `audits/local_metrics_output_shape_review_v0/protected_surface_check.md`
- `audits/local_metrics_output_shape_review_v0/command_log.md`
- `audits/local_metrics_output_shape_review_v0/boundary_checklist.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- Pending at writeback time; final validation recorded in the audit command log and final report.

Review result:
- Verdict: `completed_with_minor_output_shape_note`.
- Required prior commit `39d3bb43d96a138e3446b56a4ded1ce2b0b5f111` was present.
- Project-control writeback for `non_official_local_metrics_calculator_v0` was present.
- Metadata correction: prior `non_official_local_metrics_calculator_v0` final commit was `39d3bb43d96a138e3446b56a4ded1ce2b0b5f111` and was pushed to `origin/feature/case-package-v2-external-schema`, although its older run-log entry still says pending.
- Reviewed existing bounded SQLGlot noop metrics outputs under `runs/user/timing_sqlglot_noop_postgres_smoke/metrics/`, `runs/user/timing_sqlglot_noop_mysql_smoke/metrics/`, and `runs/user/timing_sqlglot_noop_spark_smoke/metrics/`.
- All 15 expected output files exist.
- `local_metrics_summary.json` shape is complete for all three runs.
- `local_metrics_by_engine.csv` and `local_metrics_by_pool.csv` expose required local metric, diagnostic, deferred status, and boundary fields.
- `local_timing_speedup_rows.csv` remains row-grained and does not rank methods or select winners.
- Performance summaries use strict exact + timed rows only.
- Minor output-shape note: the literal token `leaderboard` appears only in explicit false boundary/prohibited-output fields, not as a leaderboard artifact or ranking output.

Denominator changed: no.
Paper results changed: no.
Case membership changed: no.
Reports/results changed: no.
Raw retained evidence changed: no.
Official metrics computed: no.
New local diagnostic metrics computed: no, existing outputs reviewed only.
Route-level paper metrics computed: no.
Timing/speedup newly computed: no.
Metrics calculator changed: no.
POCR implemented: no.
Skill folders created: no.
Operation atoms inferred: no.
Paper tables rendered: no.
Leaderboard created: no.
Retained evidence promoted: no.
`runs/user/` outputs committed: no.

Commit hash:
- Pending.

Push result:
- Pending.

Next safe action:
- Authorize broader local diagnostic projection only if the explicit false leaderboard boundary vocabulary is accepted; otherwise authorize a narrow output-vocabulary patch first.

## 2026-05-22 - common_core_sqlglot_noop_local_metrics_projection_v0

Mode: local diagnostic metrics projection over existing Common-core SQLGlot noop snapshots.

Legacy repo modified: no.
Release repo modified: yes.

Files created:
- `audits/common_core_sqlglot_noop_local_metrics_projection_v0/README.md`
- `audits/common_core_sqlglot_noop_local_metrics_projection_v0/input_run_inventory.csv`
- `audits/common_core_sqlglot_noop_local_metrics_projection_v0/projected_metrics_summary.csv`
- `audits/common_core_sqlglot_noop_local_metrics_projection_v0/projected_metrics_by_engine.csv`
- `audits/common_core_sqlglot_noop_local_metrics_projection_v0/projected_metrics_by_pool.csv`
- `audits/common_core_sqlglot_noop_local_metrics_projection_v0/performance_na_review.md`
- `audits/common_core_sqlglot_noop_local_metrics_projection_v0/boundary_flags_review.md`
- `audits/common_core_sqlglot_noop_local_metrics_projection_v0/command_log.md`
- `audits/common_core_sqlglot_noop_local_metrics_projection_v0/protected_surface_check.md`
- `audits/common_core_sqlglot_noop_local_metrics_projection_v0/boundary_checklist.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- Pending at writeback time; final validation recorded in the audit command log and final report.

Projection result:
- Verdict: `completed_with_fail_visible_limitations`.
- Required prior commits `a91884b4778d3acd348026421ac59bc19c9aa838` and `39d3bb43d96a138e3446b56a4ded1ce2b0b5f111` were present.
- D033 was present in `project_control/DECISION_LOG.md`.
- Project-control writeback for `local_metrics_output_shape_review_v0` was present.
- Metadata correction: prior `local_metrics_output_shape_review_v0` final commit was `a91884b4778d3acd348026421ac59bc19c9aa838` and was pushed to `origin/feature/case-package-v2-external-schema`, although its older run-log entry still says pending.
- Input runs used: `runs/user/common_core_sqlglot_noop_postgres_snapshot`, `runs/user/common_core_sqlglot_noop_mysql_snapshot`, and `runs/user/common_core_spark_sqlglot_noop_after_statement_patch`.
- PostgreSQL projection: selected 40, candidate generated 35, candidate executable 35, exact 35, mismatch 0, Generation Rate 0.875, Execution Coverage Rate 0.875, Result Consistency Rate 0.875.
- MySQL projection: selected 40, candidate generated 40, candidate executable 39, exact 31, mismatch 8, Generation Rate 1.0, Execution Coverage Rate 0.975, Result Consistency Rate 0.775.
- Spark projection: selected 40, candidate generated 40, candidate executable 33, exact 31, mismatch 2, unsupported/fail-closed 5, Generation Rate 1.0, Execution Coverage Rate 0.825, Result Consistency Rate 0.775.
- Performance metrics are N.A. for all three projections because no Common-core snapshot timing artifacts are present.
- The current Common-core MySQL snapshot predates the label-only diagnostics patch, so projected `label_only_mismatch=0` even though later audits identify label-only candidates.

Denominator changed: no.
Paper results changed: no.
Case membership changed: no.
Reports/results changed: no.
Raw retained evidence changed: no.
Official metrics computed: no.
Local diagnostic metrics projected: yes.
New timing collected: no.
Route-level paper metrics computed: no.
POCR implemented: no.
Skill folders created: no.
Operation atoms inferred: no.
Paper tables rendered: no.
Leaderboard created: no.
Retained evidence promoted: no.
`runs/user/` outputs committed: no.

Commit hash:
- Pending.

Push result:
- Pending.

Next safe action:
- Review the non-official Common-core SQLGlot noop local metrics projection; if label-only diagnostics are required at Common-core scope, separately authorize a bounded post-label-diagnostics refresh rather than inferring those fields into old snapshots.

## 2026-05-22 - local_evaluation_workbench_v0_closeout

Mode: audit-only local evaluation workbench v0 closeout.

Legacy repo modified: no.
Release repo modified: yes.

Files created:
- `audits/local_evaluation_workbench_v0_closeout/README.md`
- `audits/local_evaluation_workbench_v0_closeout/component_summary.csv`
- `audits/local_evaluation_workbench_v0_closeout/local_timing_and_metrics_summary.csv`
- `audits/local_evaluation_workbench_v0_closeout/deferred_scope.md`
- `audits/local_evaluation_workbench_v0_closeout/closeout_status.json`
- `audits/local_evaluation_workbench_v0_closeout/protected_surface_check.md`
- `audits/local_evaluation_workbench_v0_closeout/command_log.md`
- `audits/local_evaluation_workbench_v0_closeout/boundary_checklist.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- Pending at writeback time; final validation recorded in the audit command log and final report.

Closeout result:
- Verdict: `closed_for_local_evaluation_workbench_v0`.
- User-entry local diagnostic surface is complete for v0: adapter entry, candidate capture, preflight, tri-engine local execution for supported roles, checker handoff, ledgers, failure buckets, quality summaries, and tag slices.
- Checker/failure explanations are recorded, including SQLGlot noop fail-visible rows and Spark statement-boundary repair closeout.
- Strict label policy is documented; behavior-preserving label-only diagnostics are available and do not change exact/mismatch semantics.
- Exact-gated local timing is implemented and bounded smoke passed over `PERF_0006` and `CONS_0005` on PostgreSQL, MySQL, and Spark with 2 timed rows per engine.
- Non-official local metrics calculator is implemented and projected over existing Common-core SQLGlot noop snapshots.
- Common-core SQLGlot noop local projection remains: PostgreSQL selected/generated/candidate-executable/exact/mismatch 40/35/35/35/0; MySQL 40/40/39/31/8; Spark 40/40/33/31/2 with 5 unsupported/fail-closed rows.
- Common-core projection performance is N.A. because no timing artifacts are present in those snapshots.
- POCR and skill adapter integration remain deferred pending external operation-atom script/schema.
- Official metrics, retained-evidence promotion, paper rendering, reports/results migration, leaderboard output, broader timing, and exactness-changing label policy remain deferred.
- Metadata correction: prior `common_core_sqlglot_noop_local_metrics_projection_v0` final commit was `e83bd232cc65c59bb118f94fb139d9661c9cd2d5` and was pushed to `origin/feature/case-package-v2-external-schema`, although its older run-log entry still says pending.

Denominator changed: no.
Paper results changed: no.
Case membership changed: no.
Reports/results changed: no.
Raw retained evidence changed: no.
Official metrics computed: no.
New timing collected: no.
Retained evidence promoted: no.
Leaderboard created: no.
`runs/user/` outputs committed: no.

Commit hash:
- Pending.

Push result:
- Pending.

Next safe action:
- Pause the local evaluation workbench line or separately authorize one of bounded post-label-diagnostics refresh, timing hardening, retained-evidence/official promotion design, or public-release packaging.

## 2026-05-22 - project_control_hygiene_and_next_phase_roadmap_v0

Mode: hygiene / audit / decision-recording only.

Legacy repo modified: no.
Release repo modified: yes.

Files created:
- `audits/project_control_hygiene_v0/README.md`
- `audits/project_control_hygiene_v0/project_control_inventory_before.csv`
- `audits/project_control_hygiene_v0/project_control_classification.csv`
- `audits/project_control_hygiene_v0/project_control_archive_manifest.csv`
- `audits/project_control_hygiene_v0/project_control_inventory_after.csv`
- `audits/project_control_hygiene_v0/active_control_files_after.md`
- `audits/project_control_hygiene_v0/moved_or_archived_files.md`
- `audits/project_control_hygiene_v0/protected_surface_check.md`
- `audits/project_control_hygiene_v0/command_log.md`
- `audits/project_control_hygiene_v0/boundary_checklist.md`

Files modified:
- `project_control/DECISION_LOG.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`
- archived `project_control/PORT_CROSS_DIALECT_DIAGNOSTIC_EXECUTION_PLAN.md` to `audits/project_control_hygiene_v0/retired_project_control_docs/PORT_CROSS_DIALECT_DIAGNOSTIC_EXECUTION_PLAN.md`
- archived `project_control/RELEASE_SURFACE_POLICY_DECISIONS.md` to `audits/project_control_hygiene_v0/retired_project_control_docs/RELEASE_SURFACE_POLICY_DECISIONS.md`
- archived `project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md` to `audits/project_control_hygiene_v0/retired_project_control_docs/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md`

Validation result:
- Pending at writeback time; final validation recorded in the audit command log and final report.

Result:
- Verdict: `completed`.
- `project_control/` now contains only the active core files: `MIGRATION_MASTER_PLAN.md`, `MIGRATION_STATUS.md`, `MIGRATION_RUN_LOG.md`, and `DECISION_LOG.md`.
- Added D034, recording project-control hygiene policy and next-phase execution order.
- Next-phase roadmap order: project-control reset; `output/<run_id>/` contract and user-facing CLI/interface contract; user-facing entry facade; failure bucket and tag-slice report surfaces; VeriEQL and SQLSolver verifier support; route-aware Common-core baseline routes; broader local exact-gated timing and non-official local metrics after interfaces stabilize; official evidence promotion, reports/results, and paper rendering only after local runs and verifier/baseline routes stabilize.
- Legacy evidence fallback policy recorded: new-repo clean evidence is preferred, legacy retained evidence is emergency fallback only and requires retention, denominator, route identity, environment/provenance, and claim-boundary mapping.
- POCR and skill integration remain deferred pending the collaborator external script/schema.

Denominator changed: no.
Paper results changed: no.
Case membership changed: no.
Reports/results changed: no.
Raw retained evidence changed: no.
Official metrics computed: no.
Timing/speedup computed: no.
Verifier implemented: no.
`output/` implemented: no.
CLI implemented: no.
POCR implemented: no.
Skill folders created: no.
Operation atoms inferred: no.
Leaderboard created: no.
Retained evidence promoted: no.
`runs/user/` outputs committed: no.

Commit hash:
- Pending.

Push result:
- Pending.

Next safe action:
- Authorize Step 1 of D034: define the `output/<run_id>/` run-output contract and user-facing CLI/interface contract.

## 2026-05-22 - final_public_layout_target_decision_v0

Mode: decision / spec / audit only.

Legacy repo modified: no.
Release repo modified: yes.

Files created:
- `audits/final_public_layout_target_decision_v0/README.md`
- `audits/final_public_layout_target_decision_v0/final_layout_target.md`
- `audits/final_public_layout_target_decision_v0/current_vs_target_layout_delta.md`
- `audits/final_public_layout_target_decision_v0/migration_timing_recommendation.md`
- `audits/final_public_layout_target_decision_v0/next_step_1_contract_adjustment.md`
- `audits/final_public_layout_target_decision_v0/protected_surface_check.md`
- `audits/final_public_layout_target_decision_v0/command_log.md`
- `audits/final_public_layout_target_decision_v0/boundary_checklist.md`

Files modified:
- `project_control/DECISION_LOG.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- Pending at writeback time; final validation recorded in the audit command log and final report.

Result:
- Verdict: `completed`.
- Added D035, recording the final public repository layout target and delayed physical migration policy.
- Final target layout records `benchmarks/` for cases, case sets, schemas, and inventory; `baselines/`; `docs/guide`, `docs/spec`, and `docs/templates`; `examples/`; `output/results`, `output/logs`, and `output/reports`; `src/sql_rewrite_bench`; `src/cli`; `src/dev`; and root public metadata files.
- Physical migration is deferred; current working paths remain valid until a separate migration/export task.
- Output contract adjustment recorded: future user-run output should use `output/results/<run_id>/`, `output/logs/<run_id>/`, and `output/reports/<run_id>/`.
- CLI location decision recorded: `src/cli` is preferred for the public-facing facade; `src/sql_rewrite_bench` remains internal implementation.

Denominator changed: no.
Paper results changed: no.
Case membership changed: no.
Reports/results changed: no.
Raw retained evidence changed: no.
Physical layout migration performed: no.
Official metrics computed: no.
Timing/speedup computed: no.
Output writer implemented: no.
CLI implemented: no.
Verifier implemented: no.
Leaderboard created: no.
Retained evidence promoted: no.
`runs/user/` outputs committed: no.

Commit hash:
- Pending.

Push result:
- Pending.

Next safe action:
- Authorize D034/D035 Step 1: design the `output/results|logs|reports/<run_id>/` contract and user-facing CLI/interface contract without moving current repository directories.

## 2026-05-22 - user_output_and_cli_contract_v0

Mode: contract / design only.

Legacy repo modified: no.
Release repo modified: yes.

Files created:
- `audits/user_output_and_cli_contract_v0/README.md`
- `audits/user_output_and_cli_contract_v0/output_directory_contract.md`
- `audits/user_output_and_cli_contract_v0/run_manifest_schema.md`
- `audits/user_output_and_cli_contract_v0/result_artifact_contract.md`
- `audits/user_output_and_cli_contract_v0/log_artifact_contract.md`
- `audits/user_output_and_cli_contract_v0/report_artifact_contract.md`
- `audits/user_output_and_cli_contract_v0/failure_bucket_and_tag_slice_reporting.md`
- `audits/user_output_and_cli_contract_v0/verifier_output_placeholder.md`
- `audits/user_output_and_cli_contract_v0/user_cli_contract.md`
- `audits/user_output_and_cli_contract_v0/facade_policy.md`
- `audits/user_output_and_cli_contract_v0/local_vs_official_output_boundary.md`
- `audits/user_output_and_cli_contract_v0/transition_notes_runs_user_to_output.md`
- `audits/user_output_and_cli_contract_v0/final_layout_alignment.md`
- `audits/user_output_and_cli_contract_v0/protected_surface_check.md`
- `audits/user_output_and_cli_contract_v0/command_log.md`
- `audits/user_output_and_cli_contract_v0/boundary_checklist.md`
- `repository_spec/user_output_contract_v0_draft.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- Pending at writeback time; final validation recorded in the audit command log and final report.

Result:
- Verdict: `completed`.
- D034 and D035 were present; `project_control/` contained only the four active core files.
- Defined output contract: `output/results/<run_id>/`, `output/logs/<run_id>/`, and `output/reports/<run_id>/`.
- Defined `run_manifest.json` schema with local-only boundary flags.
- Defined result/log/report artifact responsibilities.
- Defined failure bucket and tag-slice placements in both machine-readable results and human-readable reports.
- Defined future verifier output placement for VeriEQL and SQLSolver as support tools, not rewrite baselines.
- Defined public CLI contract centered on `sqlrb user evaluate` and convenience commands.
- Defined facade policy: public facade target `src/cli`, internal package `src/sql_rewrite_bench`, developer tools `src/dev`.
- Defined transition policy from legacy/development `runs/user/` to future user-facing `output/`.

Denominator changed: no.
Paper results changed: no.
Case membership changed: no.
Reports/results changed: no.
Raw retained evidence changed: no.
Physical layout migration performed: no.
Official metrics computed: no.
Timing/speedup computed: no.
Verifier implemented: no.
Output writer implemented: no.
CLI implemented: no.
POCR implemented: no.
Skill folders created: no.
Operation atoms inferred: no.
Leaderboard created: no.
Retained evidence promoted: no.
`runs/user/` outputs committed: no.
Output runtime artifacts committed: no.

Commit hash:
- Pending.

Push result:
- Pending.

Next safe action:
- Authorize implementation planning for the user-facing output writer and `src/cli` facade, still without physical layout migration.

## 2026-05-22 - user_output_writer_cli_facade_implementation_plan_v0

Mode: implementation planning only.

Legacy repo modified: no.
Release repo modified: yes.

Files created:
- `audits/user_output_writer_cli_facade_implementation_plan_v0/README.md`
- `audits/user_output_writer_cli_facade_implementation_plan_v0/current_output_inventory.md`
- `audits/user_output_writer_cli_facade_implementation_plan_v0/output_writer_plan.md`
- `audits/user_output_writer_cli_facade_implementation_plan_v0/cli_facade_plan.md`
- `audits/user_output_writer_cli_facade_implementation_plan_v0/phase2_implementation_slices.md`
- `audits/user_output_writer_cli_facade_implementation_plan_v0/transition_strategy_runs_user_to_output.md`
- `audits/user_output_writer_cli_facade_implementation_plan_v0/test_plan.md`
- `audits/user_output_writer_cli_facade_implementation_plan_v0/risk_assessment.md`
- `audits/user_output_writer_cli_facade_implementation_plan_v0/protected_surface_check.md`
- `audits/user_output_writer_cli_facade_implementation_plan_v0/command_log.md`
- `audits/user_output_writer_cli_facade_implementation_plan_v0/boundary_checklist.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- Pending at writeback time; final validation recorded in the audit command log and final report.

Metadata correction:
- The prior `user_output_and_cli_contract_v0` entry records commit and push as pending, but the branch contains final commit `9b12239` (`docs(spec): define user output and CLI contract`) and it was pushed to `origin/feature/case-package-v2-external-schema`.

Result:
- Verdict: `completed`.
- D034 and D035 were present; `project_control/` contained only the four active core files.
- `audits/user_output_and_cli_contract_v0/` and `repository_spec/user_output_contract_v0_draft.md` were present.
- Current `runs/user/` artifacts were inventoried and mapped to the future D035 output surface.
- Planned a future `src/sql_rewrite_bench/user_output.py` output writer with run manifest, result/log/report export, boundary report, failure bucket report, tag-slice report, and metrics summary report responsibilities.
- Planned a future `src/cli` facade centered on `sqlrb user evaluate`, plus list, explain, schema, local metrics, summarize, and boundary commands.
- Defined Phase 2A output writer skeleton, Phase 2B CLI core, and Phase 2C metrics/summary facade slices.

Denominator changed: no.
Paper results changed: no.
Case membership changed: no.
Reports/results changed: no.
Raw retained evidence changed: no.
Physical layout migration performed: no.
Output writer implemented: no.
CLI implemented: no.
Verifier implemented: no.
Official metrics computed: no.
Timing/speedup computed: no.
POCR implemented: no.
Skill folders created: no.
Leaderboard created: no.
Retained evidence promoted: no.
`runs/user/` outputs committed: no.
Output runtime artifacts committed: no.

Commit hash:
- Pending.

Push result:
- Pending.

Next safe action:
- Authorize Phase 2A output writer skeleton and bounded-smoke export path only, preserving `runs/user/` compatibility and local-only boundaries.

## 2026-05-22 - user_output_writer_phase2a_v0

Mode: implementation, local output writer only.

Legacy repo modified: no.
Release repo modified: yes.

Files created:
- `src/sql_rewrite_bench/user_output.py`
- `tests/user_entry/test_user_output.py`
- `audits/user_output_writer_phase2a_v0/README.md`
- `audits/user_output_writer_phase2a_v0/implementation_summary.md`
- `audits/user_output_writer_phase2a_v0/exported_output_shape.md`
- `audits/user_output_writer_phase2a_v0/run_manifest_example.md`
- `audits/user_output_writer_phase2a_v0/boundary_report_example.md`
- `audits/user_output_writer_phase2a_v0/test_results.md`
- `audits/user_output_writer_phase2a_v0/bounded_export_smoke_summary.md`
- `audits/user_output_writer_phase2a_v0/protected_surface_check.md`
- `audits/user_output_writer_phase2a_v0/command_log.md`
- `audits/user_output_writer_phase2a_v0/boundary_checklist.md`

Files modified:
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- Pending at writeback time; final validation recorded in the audit command log and final report.

Result:
- Verdict: `completed`.
- Added a narrow internal output writer/exporter in `src/sql_rewrite_bench/user_output.py`.
- The exporter maps existing `runs/user/<run_id>/` artifacts into `output/results/<run_id>/`, `output/logs/<run_id>/`, and `output/reports/<run_id>/`.
- The exporter writes `run_manifest.json`, `boundary.md`, `summary.md`, failure bucket CSV/Markdown, tag-slice Markdown, metrics summary or N.A. report, verifier N.A. summary/status, and log summaries.
- The exporter copies existing ledger, quality summary, tag slices, candidates, execution, checker, timing, and metrics artifacts when present.
- Source `runs/user/` directories are not deleted, moved, or mutated.
- Bounded export smoke used `runs/user/timing_sqlglot_noop_postgres_smoke` and a temporary output root only.
- Focused output writer tests and the full user-entry suite passed.

Denominator changed: no.
Paper results changed: no.
Case membership changed: no.
Reports/results changed: no.
Raw retained evidence changed: no.
Physical layout migration performed: no.
Output writer implemented: yes.
CLI implemented: no.
Verifier implemented: no.
Official metrics computed: no.
Timing/speedup computed: no.
Metrics computed: no.
POCR implemented: no.
Skill folders created: no.
Operation atoms inferred: no.
Leaderboard created: no.
Retained evidence promoted: no.
`runs/user/` outputs committed: no.
Output runtime artifacts committed: no.

Commit hash:
- Pending.

Push result:
- Pending.

Next safe action:
- Authorize Phase 2B CLI facade parsing and `sqlrb user evaluate` wrapper over existing internals and this exporter, still bounded to smoke validation and local-only output.

## 2026-05-23 - user_cli_facade_phase2b_v0

Mode: implementation, CLI facade only.

Legacy repo modified: no.
Release repo modified: yes.

Files created:
- `src/cli/__init__.py`
- `src/cli/__main__.py`
- `src/cli/main.py`
- `tests/user_entry/test_cli_facade.py`
- `audits/user_cli_facade_phase2b_v0/README.md`
- `audits/user_cli_facade_phase2b_v0/implementation_summary.md`
- `audits/user_cli_facade_phase2b_v0/cli_command_contract.md`
- `audits/user_cli_facade_phase2b_v0/bounded_cli_smoke_summary.md`
- `audits/user_cli_facade_phase2b_v0/test_results.md`
- `audits/user_cli_facade_phase2b_v0/protected_surface_check.md`
- `audits/user_cli_facade_phase2b_v0/command_log.md`
- `audits/user_cli_facade_phase2b_v0/boundary_checklist.md`

Files modified:
- `pyproject.toml`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- Pending at writeback time; final validation recorded in the audit command log and final report.

Result:
- Verdict: `completed`.
- Added the thin `src/cli` public facade package and `sqlrb` console-script entry point.
- Implemented `sqlrb user evaluate`, `list-cases`, `explain-selection`, `show-output-schema`, `show-boundary`, `compute-local-metrics`, and `summarize`.
- `evaluate` delegates to the existing user-run pipeline and then exports through the Phase 2A output writer into `output/results/<run_id>/`, `output/logs/<run_id>/`, and `output/reports/<run_id>/`.
- Bounded PostgreSQL SQLGlot noop CLI smoke over `PERF_0006` and `CONS_0005` selected/generated/source-executable/candidate-executable/checker/exact/mismatch rows 2/2/2/2/2/2/0 with timing disabled.
- Verifier flags fail closed; VeriEQL and SQLSolver integration remains deferred.

Denominator changed: no.
Paper results changed: no.
Case membership changed: no.
Reports/results changed: no.
Raw retained evidence changed: no.
Physical layout migration performed: no.
Output writer changed only as needed: no.
CLI implemented: yes.
Verifier implemented: no.
Official metrics computed: no.
Timing/speedup computed: no.
Metrics computed: no.
POCR implemented: no.
Skill folders created: no.
Operation atoms inferred: no.
Leaderboard created: no.
Retained evidence promoted: no.
`runs/user/` outputs committed: no.
Output runtime artifacts committed: no.

Commit hash:
- Pending.

Push result:
- Pending.

Next safe action:
- Review Phase 2B CLI facade and then authorize Phase 2C summary/local-metrics facade hardening or verifier output contract planning.

## 2026-05-23 - user_cli_facade_phase2b_review_v0

Mode: review/hardening, CLI facade only.

Legacy repo modified: no.
Release repo modified: yes.

Files created:
- `audits/user_cli_facade_phase2b_review_v0/README.md`
- `audits/user_cli_facade_phase2b_review_v0/command_review_matrix.csv`
- `audits/user_cli_facade_phase2b_review_v0/help_text_review.md`
- `audits/user_cli_facade_phase2b_review_v0/output_path_review.md`
- `audits/user_cli_facade_phase2b_review_v0/verifier_fail_closed_review.md`
- `audits/user_cli_facade_phase2b_review_v0/local_metrics_summarize_review.md`
- `audits/user_cli_facade_phase2b_review_v0/bounded_cli_smoke_summary.md`
- `audits/user_cli_facade_phase2b_review_v0/protected_surface_check.md`
- `audits/user_cli_facade_phase2b_review_v0/command_log.md`
- `audits/user_cli_facade_phase2b_review_v0/boundary_checklist.md`

Files modified:
- `src/cli/main.py`
- `tests/user_entry/test_cli_facade.py`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Validation result:
- Pending at writeback time; final validation recorded in the audit command log and final report.

Result:
- Verdict: `completed_with_hardening`.
- Reviewed `sqlrb user evaluate`, `list-cases`, `explain-selection`, `show-output-schema`, `show-boundary`, `compute-local-metrics`, and `summarize`.
- Hardened command-level help so every implemented command carries the local-only boundary: no official metrics, paper results, retained-evidence promotion, or leaderboard output.
- Hardened verifier fail-closed behavior so `--verifier verieql` and `--verifier sqlsolver` fail before evaluation and state Semantic Equivalence Rate remains `N.A.` without verifier evidence.
- Hardened `evaluate` and `compute-local-metrics` to validate protected output roots before invoking internal runner or local metrics calculator.
- Bounded PostgreSQL SQLGlot noop CLI smoke over `PERF_0006` and `CONS_0005` selected/generated/source-executable/candidate-executable/checker/exact/mismatch rows 2/2/2/2/2/2/0 with timing disabled.
- Metadata correction: `user_cli_facade_phase2b_v0` final commit was `5344770` and was pushed to `origin/feature/case-package-v2-external-schema`, although its older run-log entry still says pending.

Denominator changed: no.
Paper results changed: no.
Case membership changed: no.
Reports/results changed: no.
Raw retained evidence changed: no.
Physical migration performed: no.
CLI reviewed/hardened: yes.
Verifier implemented: no.
Official metrics computed: no.
Timing/speedup computed: no.
Metrics computed: no, except no real local-metrics smoke was needed.
POCR implemented: no.
Skill folders created: no.
Operation atoms inferred: no.
Leaderboard created: no.
Retained evidence promoted: no.
`runs/user/` outputs committed: no.
Output runtime artifacts committed: no.

Commit hash:
- Pending.

Push result:
- Pending.

Next safe action:
- Authorize Phase 2C summary/local-metrics facade hardening or future verifier output contract planning.
