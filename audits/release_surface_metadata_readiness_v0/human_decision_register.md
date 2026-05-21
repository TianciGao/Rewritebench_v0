# Human Decision Register

The following decisions must be made by the maintainer/team before implementation of the corresponding release-surface files.

## License Choice

- Choose the repository license for code, data, documentation, and benchmark assets.
- Decide whether one license covers the whole repository or whether code and documentation/data need separate notices.
- Do not create `LICENSE` until this decision is explicit.

## Citation Metadata

- Confirm official project title.
- Confirm authorship and author ordering.
- Confirm version string.
- Confirm preferred paper title and publication status.
- Confirm DOI, URL, or placeholder policy.
- Do not create `CITATION.cff` with guessed author or DOI metadata.

## Contribution Policy Strictness

- Decide whether public pull requests are accepted before release.
- Decide whether external case additions are accepted.
- Decide how changes to `cases/`, `case_sets/`, denominator scaffolds, metrics, reports, and results are governed.
- Decide whether DB/checker/timing contributions require separate validation.

## README Language Policy

- Decide whether top-level `README.md` remains Chinese-only for this branch.
- Decide whether to add a bilingual README, English summary, or language-specific docs split.
- Do not rewrite the README in this audit.

## Benchmark Spec Wording Scope

- Confirm that `benchmark_spec/` should describe Common-core v0, Track A, case-package unit, denominator-aware reporting, no global leaderboard, hard-negative checker controls, and deferred SpeedupTransferRate.
- Confirm whether benchmark spec should include only public v0 scope or also post-release backlog notes.

## Reports / Results Boundary

- Decide whether `reports/` and `results/` should exist as placeholder directories with boundary README files.
- Decide whether any curated paper-facing reports/results will be included later.
- Do not migrate reports/results or render paper tables before separate authorization.

## Release Branch / Tag Policy

- Decide naming and timing for an export branch.
- Decide release tag format.
- Decide whether release artifacts are created from this branch or after merge.
- Do not create a release tag or export branch in this audit.
