# Future Prompt: case_package_v2_clean_template_or_common_core40_plan_v0

Repository:
- Work only in `/home/tianci_gao/code/Rewritebench_v0`.
- Work only on branch `feature/case-package-v2-external-schema`.
- Do not modify `main`.
- Do not inspect or modify the legacy repo.

Task title: `case_package_v2_common_core40_conversion_plan_v0`

This is a read-only planning task. Do not convert cases, delete files, run DB/checker execution, compute official metrics, update reports/results, change denominators, render paper tables, or create leaderboard output.

Goal:
- Use the five-case v2 pilot as a functional v2 template for planning Common-core 40 conversion.
- Treat the pilot as functionally accepted but not clean-template-minimal.
- Preserve separate cleanup tracks for retained evidence, case-local schema engine copies, metadata, data/profile files, validation legacy scripts, and PORT dialect variants.

Required inputs:
- `audits/case_package_v2_post_empty_runs_parity_review_v0/`
- prior v2 rulebooks and pilot audits
- current Common-core 40 case list and case packages

Plan requirements:
- Produce a case-by-case Common-core 40 conversion readiness matrix.
- Identify cases eligible for folder-ordered v2 conversion.
- Identify schema externalization reuse opportunities.
- Identify retained evidence and cleanup blockers without deleting anything.
- Confirm no denominator, case-set, report/result, paper-result, metric, DB/checker, or leaderboard changes.

Exact next safe action after the plan:
- Maintainer review of Common-core 40 v2 conversion plan before any writable conversion.
