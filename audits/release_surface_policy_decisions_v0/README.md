# Release Surface Policy Decisions v0

This packet records the policy decisions required before release-surface metadata skeleton implementation.

Verdict: ready for metadata skeleton implementation under recorded policy boundaries.

Decisions recorded:

- Initial repository license policy: `Apache-2.0`.
- Citation policy: later `CITATION.cff` may use placeholders; no DOI, author order, or institutional metadata may be invented.
- Contribution policy: conservative; external contributions must not silently change benchmark membership, denominators, metrics, reports/results, retained evidence, or benchmark claims.
- README language posture: Chinese can remain on this construction branch; English or bilingual public entrypoint is required before final public artifact release.
- `benchmark_spec/` scope: public v0 only, preserving Common-core v0 denominator and claim boundaries.
- `reports/` and `results/` boundary: boundary documentation only in the next skeleton phase; no report/result generation or migration.
- Release mechanics: no release tag or export branch until final public-release closeout passes.

No skeleton files were created by this task. No source code, cases, case sets, reports, results, benchmark specs, repository specs, README, LICENSE, CITATION, or CONTRIBUTING files were modified.

Next safe action: implement the metadata skeleton in a separate bounded task using these policy decisions.
