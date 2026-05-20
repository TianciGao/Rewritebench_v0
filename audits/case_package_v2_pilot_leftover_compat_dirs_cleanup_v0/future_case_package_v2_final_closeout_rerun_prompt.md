# Future Prompt: case_package_v2_common_core40_final_closeout_rerun_v0

Repository:
- Work only in `/home/tianci_gao/code/Rewritebench_v0`.
- Work only on branch `feature/case-package-v2-external-schema`.
- Do not inspect or modify the legacy repo.

Task:
- Rerun the read-only Common-core 40 v2 final closeout after `case_package_v2_pilot_leftover_compat_dirs_cleanup_v0`.

Required checks:
- Run the static v2 validator for all 40 Common-core cases.
- Confirm clean-template-minimal passes for all 40 cases.
- Confirm retained PORT dialect variants remain under `PORT_0003`, `PORT_0004`, `PORT_0005`, and `PORT_0013`.
- Confirm no `notes/`, `sql/positives/`, or `sql/negatives/` remain in the five pilot cases.
- Confirm `PERF_0077` and `PERF_0082` source-path caveats remain separate and do not block case-package closeout.

Hard boundaries:
- Do not modify case packages, schemas, `case_sets/`, inventory, reports/results, denominators, paper results, official metrics, DB/checker execution, or leaderboard outputs.
- Do not delete dialect variants.

Expected next action after a clean rerun:
- Run a narrow `PERF_0077`/`PERF_0082` source-path provenance follow-up before final public release closeout.
