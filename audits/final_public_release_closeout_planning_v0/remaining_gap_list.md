# Remaining Gap List

## Release-Blocking Gaps

- Missing public release metadata: `LICENSE`, `CITATION.cff`, and `CONTRIBUTING.md` are not present.
- Missing public benchmark specification surface: `benchmark_spec/` is not present.
- Missing or unauthorized public results surfaces: curated `reports/` and `results/` are not present as release surfaces.
- Official metrics and paper-table rendering remain unauthorized for this task and were not produced.
- General retained-evidence adapter coverage and paper-reproduction output flow are not complete enough to support public output claims.
- Clean export/tag procedure has not run; no release tag or export branch was created.

## Nonblocking Caveats

- `PERF_0077` and `PERF_0082` retain source-path provenance uncertainty. This is public-safe only if release materials avoid claiming exact JOB source paths for those cases.
- `PORT_0003`, `PORT_0004`, `PORT_0005`, and `PORT_0013` retain dialect variants as semantic PORT assets.
- User-facing execution paths are documented within current boundaries, but this audit does not promote local smoke outputs to official metrics or paper results.
- Construction audits and project-control history remain in this branch; a clean public export-surface decision is still required.

## Case-Package Gaps

No Common-core 40 case-package blocker remains in the latest final closeout rerun. The remaining gaps are public release-surface, metadata, reporting, reproduction, and export/tag gaps.

## Next Safe Action

Authorize a bounded public release-surface completion task covering release metadata, benchmark-spec, reports/results policy, reproduction/metrics claim boundaries, and export/tag readiness. Do not create a release tag until those gaps are closed and a final read-only closeout passes.
