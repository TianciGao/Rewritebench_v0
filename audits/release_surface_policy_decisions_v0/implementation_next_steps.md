# Implementation Next Steps

The next task should be metadata-only and should use `project_control/RELEASE_SURFACE_POLICY_DECISIONS.md` as its governing policy input.

Safe skeleton candidates for a future task:

- Create repository-level `LICENSE` using Apache-2.0.
- Create `CITATION.cff` with safe placeholders only where final metadata is unavailable.
- Create `CONTRIBUTING.md` with a conservative benchmark-governance contribution policy.
- Create `benchmark_spec/` skeleton files limited to public v0 scope and documented claim boundaries.
- Create `reports/README.md` and `results/README.md` as boundary documentation only, without generating or migrating results.

Future skeleton task boundaries:

- No official metrics implementation.
- No paper table rendering.
- No reports/results migration.
- No retained-evidence promotion.
- No denominator change.
- No paper-result change.
- No case membership change.
- No release tag.
- No export branch.
- No global leaderboard.

If maintainer metadata details remain unavailable, the future task should use explicit `TBD` placeholders rather than inventing author, DOI, paper, or release metadata.
