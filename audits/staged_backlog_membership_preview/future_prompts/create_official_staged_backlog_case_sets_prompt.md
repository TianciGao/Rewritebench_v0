FUTURE PROMPT — DO NOT EXECUTE NOW

This is a future task prompt draft. It must not be executed as part of the staged/backlog membership preview task.

Hard boundaries:
- Do not modify the legacy repository.
- Do not migrate cases unless a future task explicitly authorizes bounded migration.
- Do not change Common-core v0 membership or denominator values.
- Do not update reports/results or paper tables.
- Do not run DB engines, validation scripts, LLM calls, or timing workloads.
- Do not use `git add .`.

# Create Official Staged/Backlog Case Sets

Goal: after maintainer approval, create official non-denominator governance files under `case_sets/staged_v0/` and `case_sets/backlog_v0/` using the preview audit as input.

Inputs:
- `audits/staged_backlog_membership_preview/`
- Maintainer-approved criteria and unregistered-directory dispositions.

Required outputs:
- `case_sets/staged_v0/manifest.yaml`
- `case_sets/staged_v0/cases.csv`
- `case_sets/backlog_v0/manifest.yaml`
- `case_sets/backlog_v0/cases.csv`
- audit summary proving denominator and Common-core membership unchanged.

Abort if approval is missing for criteria or unregistered-directory handling.
