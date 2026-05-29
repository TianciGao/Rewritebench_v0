# Future Final Closeout Prompt

Task title:
Complete public release-surface gaps and rerun final public-release closeout

Purpose:
Finish the public release-surface gaps identified by `audits/final_public_release_closeout_planning_v0/` before any release tag or export branch is created.

Scope:

- Add or confirm public release metadata: `LICENSE`, `CITATION.cff`, and `CONTRIBUTING.md`.
- Add or confirm the public benchmark-spec surface.
- Decide whether curated `reports/` and `results/` are included in the public release; if included, migrate only authorized artifacts.
- Define official metrics and paper-result claim boundaries without computing new metrics unless separately authorized.
- Confirm retained-evidence adapter and reproduction-surface status.
- Run public hygiene checks over the intended export surface.
- Rerun a final read-only public-release closeout audit after the gaps close.

Boundaries:

- Do not modify case package semantics, SQL, manifests, schemas, checker files, validation files, case sets, inventory, denominator scaffolds, paper results, or raw retained evidence unless explicitly authorized by a separate narrow task.
- Do not claim exact JOB source paths for `PERF_0077` or `PERF_0082`.
- Do not compute official metrics, render paper tables, create a global leaderboard, create a release tag, or create an export branch until a final closeout explicitly authorizes it.

Expected outcome:

- Release readiness verdict can move from blocked to ready or ready with only explicitly accepted nonblocking caveats.
- A final closeout packet records protected surfaces, public hygiene, release metadata, reproduction path, metrics/reporting boundaries, and export/tag readiness.
