# Final Public Release Closeout Planning v1

Verdict: `ready_for_export_planning`.

This packet records the final public-release closeout planning audit after Common-core 40 case-package closeout, Common-core README normalization, `PERF_0077` / `PERF_0082` source-path follow-up, user-entry U0-U7 closeout, release-surface metadata skeleton and polish, and final metadata readiness review.

Ready surfaces:

- Common-core v0 case-package surface is closed for public v0 planning: 40 cases, pool split 16 PERF + 9 CONS + 9 PORT + 6 LONGTAIL.
- `case_sets/common_core_v0/` remains the governed membership and denominator surface, with 120 Track A same-engine planned rows.
- All 40 Common-core public case READMEs are present.
- Representative v2 case packages expose manifest-governed SQL, schema profile, checker, validation, witness, and external schema references.
- `PERF_0077` and `PERF_0082` source-path caveats are closed as nonblocking provenance uncertainty; no exact JOB source path is claimed.
- User-entry local diagnostics support smoke, adapter capture, candidate preflight, optional PostgreSQL diagnostics/checker, local quality reports, tag slices, readability commands, and MySQL/Spark fail-closed stubs.
- Release metadata surfaces exist: `LICENSE`, `CITATION.cff`, `CONTRIBUTING.md`, `.gitignore`, `benchmark_spec/`, `reports/README.md`, `results/README.md`, and docs index.

Remaining blockers: none for a later export/tag planning task.

Nonblocking caveats:

- The top-level README is currently Chinese; D030 requires English primary or bilingual public entrypoint before final public artifact release.
- `CITATION.cff` remains placeholder-safe and omits DOI and individual author metadata.
- `PERF_0077` and `PERF_0082` retain nonblocking source-path provenance uncertainty.
- `reports/` and `results/` are boundary-only surfaces; no paper tables or official result artifacts were generated.
- Timing, official metrics, paper rendering, retained-evidence integration, reports/results migration, and full paper reproduction remain deferred.
- MySQL and Spark user-entry execution are fail-closed stubs only.
- No release tag or export branch has been created.

No release tag or export branch was created by this task.

Next safe action: run a separate export/tag planning task that decides README language posture, citation finalization requirements, release branch/tag naming, and whether boundary-only `reports/` / `results/` are acceptable for public v0 before any release tag or export branch is created.
