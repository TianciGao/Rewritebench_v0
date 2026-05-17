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

### 2026-05-17 · pending · Candidate retained-evidence parser approval packet

Mode: release-repo audit/design/approval-packet only; no production retained-evidence parsing; legacy not read
Legacy repo modified: no
Release repo modified: yes
Commit: `pending`
Push: `pending`

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
