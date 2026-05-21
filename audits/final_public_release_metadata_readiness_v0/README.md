# Final Public Release Metadata Readiness v0

Verdict: `ready_for_final_closeout_planning`.

The public release metadata surface is now complete enough to proceed to a final public-release closeout planning audit. The previous metadata blockers have been addressed by the policy decision packet, metadata skeleton, and metadata polish pass.

Ready surfaces:

- Top-level README describes SQL-RewriteBench, Common-core v0, smoke commands, user adapters, local output boundaries, optional PostgreSQL diagnostics, and benchmark boundaries.
- `LICENSE` exists with Apache-2.0 text and conservative contributor copyright.
- `CITATION.cff` exists with valid placeholder-safe metadata.
- `CONTRIBUTING.md` exists with conservative benchmark-governance boundaries.
- `.gitignore` ignores local user outputs under `runs/user/` without ignoring all of `runs/`.
- `benchmark_spec/` documents public v0 scope, case package contract, denominator policy, and reporting policy.
- `reports/README.md` and `results/README.md` exist as boundary files only.
- Common-core v0 case-set metadata, 40 Common-core case READMEs, external schemas, user-entry docs, tests, and CI smoke workflows are present.

Remaining blockers to final closeout planning: none identified.

Nonblocking caveats for final release/export:

- The current top-level README is Chinese; the recorded policy requires an English primary README or bilingual public entrypoint before final public artifact release.
- `CITATION.cff` intentionally uses placeholder-safe metadata and omits DOI and individual author metadata until finalized.
- `reports/` and `results/` are boundary directories only; no paper tables or official result artifacts were generated.
- Official metrics, timing/speedup, retained-evidence integration, paper rendering, and full paper reproduction remain deferred and unauthorized.
- No release tag or export branch has been created.

Next safe action: run final public-release closeout planning. Do not create a release tag or export branch until a separately authorized final closeout passes.
