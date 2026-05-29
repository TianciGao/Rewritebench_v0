# Future Final Closeout Prompt

Task title:
Final public-release closeout planning after metadata readiness

Purpose:
Run a final public-release closeout planning audit after the metadata/readiness review verdict `ready_for_final_closeout_planning`.

Scope:
This is planning/audit only. Do not create a release tag. Do not create an export branch. Do not compute metrics. Do not render paper tables. Do not migrate reports/results. Do not modify cases. Do not create a global leaderboard.

Required review inputs:

- `audits/final_public_release_metadata_readiness_v0/`
- `audits/final_public_release_closeout_planning_v0/` if still relevant
- latest project-control status and run log
- Common-core case package closeout packets
- user-entry local evaluation closeout packet
- release-surface metadata skeleton and polish packets

Questions to answer:

- Is the repository ready for a separately authorized release export/tag task?
- Does the top-level README language posture need to be resolved before export?
- Are `CITATION.cff` placeholders acceptable for the intended public artifact, or must paper metadata be finalized first?
- Are reports/results boundary README files sufficient for public v0, or must curated artifacts be authorized first?
- Are any protected surfaces dirty or stale?

Boundaries:

- No denominator change.
- No paper result change.
- No case membership change.
- No raw legacy evidence change.
- No official metrics computation.
- No paper table rendering.
- No reports/results migration.
- No release tag or export branch without separate explicit authorization.
