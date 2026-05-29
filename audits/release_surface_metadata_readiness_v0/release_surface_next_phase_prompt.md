# Future Next-Phase Prompt

Task title:
Collect public release metadata policy decisions

Purpose:
Collect maintainer/team decisions required before creating public release metadata files such as `LICENSE`, `CITATION.cff`, `CONTRIBUTING.md`, `benchmark_spec/`, `reports/README.md`, `results/README.md`, root `.gitignore`, release tag policy, or export branch policy.

Scope:
Decision collection only. Do not implement files yet unless explicitly authorized in a follow-up task.

Questions to resolve:

1. License choice for code, documentation, data, and benchmark assets.
2. Citation metadata: title, authors, version, DOI/URL, and preferred citation.
3. Contribution policy: external PRs, case additions, denominator changes, metrics/report changes, and validation requirements.
4. README language policy: Chinese-only, bilingual top-level, or language-specific split.
5. Benchmark spec scope and wording.
6. Reports/results boundary: placeholders only versus curated artifacts later.
7. Release branch and tag policy.

Boundaries:

- No official metrics.
- No paper table rendering.
- No reports/results migration.
- No retained-evidence promotion.
- No denominator change.
- No paper-result change.
- No case membership change.
- No live DB/checker execution.
- No timing/speedup.
- No global leaderboard.
- No release tag or export branch.

Output:

- project-control decision packet or decision-log update, as appropriate
- future prompt for a metadata-only skeleton creation task after decisions are recorded
