# Future Export Planning Prompt

Task title:
Plan public v0 export/tag mechanics after final closeout planning

Purpose:
Use `audits/final_public_release_closeout_planning_v1/` to plan the exact public v0 export/tag mechanics. This future task is planning only unless the maintainer explicitly authorizes a tag or export branch in that later turn.

Required decisions before any release action:

- Decide whether the top-level README becomes English primary or bilingual.
- Decide whether placeholder-safe `CITATION.cff` metadata is acceptable for the intended release stage.
- Decide whether boundary-only `reports/` and `results/` are acceptable for public v0.
- Decide release branch and tag naming.
- Decide whether construction audit/project-control surfaces remain in the public branch or require a separate curated export surface.

Boundaries:

- Do not create a release tag unless explicitly authorized in the same future task.
- Do not create an export branch unless explicitly authorized in the same future task.
- Do not merge branches or rewrite history.
- Do not compute official metrics.
- Do not render paper tables.
- Do not migrate reports/results.
- Do not update denominators.
- Do not modify case membership.
- Do not modify raw retained evidence.
- Do not create a global leaderboard.

Expected output:

- A release/export plan with exact branch/tag policy, public surface inclusion policy, README language decision, citation readiness decision, protected-surface checks, and final authorization gates.
