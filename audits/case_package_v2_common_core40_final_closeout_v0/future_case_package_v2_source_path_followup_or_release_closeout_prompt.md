# Future Prompt: case_package_v2_source_path_followup_or_release_closeout_v0

Repository:
- Work only in /home/tianci_gao/code/Rewritebench_v0.
- Work only on branch feature/case-package-v2-external-schema.
- Do not inspect or modify the legacy repo unless a separately authorized provenance task explicitly permits it.

Purpose:
- First resolve the final closeout blockers reported by `case_package_v2_common_core40_final_closeout_v0`: leftover empty pilot compatibility directories in `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.
- Rerun the Common-core 40 v2 final closeout after that cleanup.
- If no structural blockers remain, run a narrow `PERF_0077`/`PERF_0082` source-path provenance follow-up.
- Only after source-path provenance is closed or explicitly accepted should final public-release closeout planning proceed.

Hard boundaries:
- Do not change Common-core membership, denominators, paper results, reports/results, official metrics, DB/checker execution, or leaderboard policy.
- Do not delete retained dialect variants under `PORT_0003`, `PORT_0004`, `PORT_0005`, or `PORT_0013`.
- Do not create `evidence/cases/`.

Expected outputs:
- A targeted blocker-resolution audit if cleanup is authorized.
- A source-path provenance follow-up audit for `PERF_0077` and `PERF_0082`.
- A final public-release closeout plan only after the above gates pass.
