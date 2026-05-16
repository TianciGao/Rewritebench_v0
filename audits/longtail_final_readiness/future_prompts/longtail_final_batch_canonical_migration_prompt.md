# FUTURE PROMPT — DO NOT EXECUTE NOW

Task title: LONGTAIL final bounded canonical migration batch

Selected cases:
- LONGTAIL_0012
- LONGTAIL_0013
- LONGTAIL_0022
- LONGTAIL_0023
- LONGTAIL_0024

This is a future bounded five-case LONGTAIL canonical migration prompt. It is not authorized by the readiness task that created this draft.

Hard boundaries:
- Do not modify the legacy repository.
- Do not run DB engines, validation scripts, LLM calls, timing workloads, or evidence regeneration.
- Do not update case_sets, reports, results, denominator files, paper tables, or case membership.
- Do not create workload-frequency, production-frequency, timing, speedup, ranking, leaderboard, or paper-result claims.
- Do not use git add .

Preconditions:
- Maintainer has approved expected rejection reasons from audits/longtail_final_readiness/longtail_expected_rejections_preview.yaml.
- Release repo is clean and current.
- Legacy repo is inspected read-only only.

Migration requirements:
- Use LONGTAIL_0011 as the primary canonical package pattern.
- Record approved expected rejections in checker/expected_rejections.yaml, README.md, notes/migration_notes.md, and the batch audit.
- Sanitize Spark plan text files with file:/tmp or local path traces before public retention.
- Map raw Spark plan originals in evidence/runs_retention.yaml as do-not-delete original legacy artifacts.
- Treat validation scripts as retained legacy validation assets and add output-policy caveats.
- Preserve structural robustness boundary and set workload_frequency_claim_created: false.

Validation requirements:
- SHA256 validation for copied files.
- Public hygiene scan.
- YAML validation.
- JSON validation.
- Validator v0.3 full-case for selected cases.
- Validator v0.3 canonical-case for selected cases.
- Full-case and canonical-case regression over existing canonical packages plus new cases.
- python -m py_compile scripts/dev/validate_case_package.py.
- git diff --check and git status -sb.

Project-control writeback:
- Update project_control/MIGRATION_STATUS.md.
- Append project_control/MIGRATION_RUN_LOG.md entry.
- Record denominator changed: no; paper results changed: no; case membership changed: no; raw legacy evidence changed: no.

Commit rules:
- Add only explicit selected case directories, the batch audit directory, and project-control writeback files.
- Do not use git add .
- Commit only after required validation passes or after clearly documenting failed/deferred cases.

Abort conditions:
- Any selected case lacks required legacy SQL/schema/witness/evidence.
- Any hard-negative approval is missing or disputed.
- Any public hygiene pattern remains after sanitization.
- Any validator v0.3 failure occurs.
- Any denominator, paper-result, case-set, report/result, case-membership, or legacy mutation is detected.
