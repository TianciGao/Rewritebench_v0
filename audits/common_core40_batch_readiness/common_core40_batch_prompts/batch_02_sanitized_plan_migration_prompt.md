# FUTURE PROMPT - DO NOT EXECUTE NOW

Task: sanitized-plan canonical migration batch.

Recommended first cases: PERF_0007, PERF_0008, PERF_0013.

Allowed writes: release repo case packages for these cases, per-case audit outputs, validator outputs, and project-control writeback only.

Special rules:
- Generate sanitized public Spark plan copies in evidence/retained_plans/.
- Map raw Spark plan originals in runs_retention.yaml as do-not-delete originals.
- Preserve performance boundary and set speedup_claim_created: false for PERF cases.
- Do not create new timing evidence or benchmark result rows.

FUTURE PROMPT - DO NOT EXECUTE NOW

Hard boundaries:
- Do not modify the legacy repository.
- Do not run DB engines, validation scripts, LLM calls, timing workloads, or evidence regeneration.
- Do not change Common-core membership, denominator, paper results, case admission status, or case_sets/.
- Do not copy raw runs/ wholesale.
- Do not publish raw Spark local-path plans.
- Do not use git add .

Required gates:
- Start with release and legacy repo safety preflight.
- Create canonical case packages only for the listed cases.
- Add evidence/runs_retention.yaml for every migrated case.
- Run public hygiene, YAML/JSON validation, validator v0.3 full-case and canonical-case.
- Append MIGRATION_RUN_LOG.md and update MIGRATION_STATUS.md.
- Commit explicit paths only.

Abort conditions:
- Dirty release repo, missing legacy file, public hygiene failure, SHA256 mismatch, manifest/runs_retention contradiction, validator failure, denominator/paper/membership change, raw legacy mutation, or broad git add.
