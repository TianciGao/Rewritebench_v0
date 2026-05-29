# Remaining Blockers

## Must Fix Before Final Closeout Planning

None identified.

## Nonblocking Caveats

- The current top-level README is Chinese. D030 permits this on the construction branch, but an English primary README or bilingual public entrypoint is required before final public artifact release.
- `CITATION.cff` is valid and placeholder-safe, but DOI, individual author metadata, and final paper metadata remain unset.
- `reports/` and `results/` contain boundary README files only. No curated paper reports or official result artifacts were generated.
- `PERF_0077` and `PERF_0082` retain explicit nonblocking source-path provenance uncertainty. The README correctly avoids claiming exact JOB source paths.
- CI workflows exist and were previously repaired, but this metadata audit does not rerun GitHub Actions remotely.

## Post-Release Backlog

- Live MySQL execution.
- Live Spark execution.
- Timing diagnostics.
- Full paper reproduction CLI.
- Broader non-Common-core public release expansion.
- Optional English/Chinese documentation split refinement after the final release posture is chosen.

## Explicitly Deferred Paper/Reproduction Work

- Official metrics implementation.
- Paper table rendering.
- Reports/results migration or regeneration.
- Retained-evidence adapter integration.
- Timing/speedup computation.
- `SpeedupTransferRate`.
- Global leaderboard creation.

These deferred items are not blockers to final closeout planning because they remain explicitly unauthorized for this release-surface metadata phase.
