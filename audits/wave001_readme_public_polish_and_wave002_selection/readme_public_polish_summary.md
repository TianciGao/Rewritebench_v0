# README Public Polish Summary

## Purpose And Scope

This audit polished the public-facing README files for the two non-Common-core packages completed in the prior standardization batch:

- `cases/PORT/PORT_0002/README.md`
- `cases/PERF/PERF_0029/README.md`

No case migration, case-set membership update, denominator update, metrics computation, paper rendering, reports/results migration, DB validation, timing run, or raw legacy evidence modification was performed.

## Files Reviewed

- `cases/PORT/PORT_0002/README.md`
- `cases/PORT/PORT_0002/manifest.yaml`
- `cases/PORT/PORT_0002/evidence/runs_retention.yaml`
- `cases/PORT/PORT_0002/metadata/provenance.yaml`
- `cases/PORT/PORT_0002/metadata/denominator_eligibility.yaml`
- `cases/PERF/PERF_0029/README.md`
- `cases/PERF/PERF_0029/manifest.yaml`
- `cases/PERF/PERF_0029/evidence/runs_retention.yaml`
- `cases/PERF/PERF_0029/metadata/provenance.yaml`
- `cases/PERF/PERF_0029/metadata/denominator_eligibility.yaml`

## Public-facing Issues Found

The original README files used construction-process wording that is unsuitable for package-facing documentation. The affected wording described the prior batch process rather than the stable public package boundary.

## Wording Removed

- References to the prior overnight batch.
- Internal construction-task wording.
- Process-oriented phrasing about how the package was standardized.

## Replacement README Structure

Both README files now use this public structure:

1. Title.
2. Purpose.
3. Release Scope.
4. Package Contents.
5. Evidence Boundary.
6. Benchmark Boundary.

The replacement wording explains package contents and scope without implying Common-core membership, Track A denominator membership, paper-result contribution, metric computation, or leaderboard output.

## Validation Result

README text checks passed for both files. The forbidden internal terms are absent, release scope is present, evidence boundary is present, benchmark boundary is present, and neither README claims denominator, paper-result, metric, or leaderboard changes.

## Next Safe Action

Review the wave 002 policy questions. If the maintainer approves batch handling of missing retained evidence, archive-mapped unsafe runs, validation-script caveats, and no-copy raw evidence boundaries, run a separately authorized wave 002 migration against the policy-approved queue only.
