# FUTURE PROMPT - DO NOT EXECUTE NOW

Task: complex LONGTAIL canonical migration batch.

Candidate cases after structural review: LONGTAIL_0012, LONGTAIL_0013, LONGTAIL_0022, LONGTAIL_0023, LONGTAIL_0024.

Precondition: every case must have reviewed structural-boundary notes and hard-negative semantics, if applicable.

Special rules:
- Record long-tail structure as structural characterization only.
- Do not create workload-frequency or production-frequency claims.
- Stop if long-tail classification or hard-negative semantics are ambiguous.

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
