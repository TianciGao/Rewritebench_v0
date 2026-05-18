# Future Prompt: overnight_non_common_core_case_package_standardization_wave_002

You are working on SQL-RewriteBench clean public release migration / redevelopment.

Task title:
overnight_non_common_core_case_package_standardization_wave_002

Use:

- `audits/wave001_readme_public_polish_and_wave002_selection/wave002_candidate_selection.csv`
- `audits/wave001_readme_public_polish_and_wave002_selection/wave002_policy_approval_questions.md`
- `audits/wave001_readme_public_polish_and_wave002_selection/wave002_batch_plan.md`

Authorization boundary:

- Migrate only cases marked `wave_002_auto_migration_candidate`.
- If the maintainer explicitly approves the policy questions, also migrate approved cases marked `wave_002_policy_approval_needed`.
- Skip any case that requires raw run copying, raw logs, prompt/token/API traces, local-path artifacts, DB execution, evidence regeneration, timing reruns, metric computation, paper rendering, reports/results updates, denominator changes, paper-result changes, or case-set membership changes.

Required boundaries:

- Keep `case_sets/` unchanged.
- Keep denominators unchanged.
- Keep paper results unchanged.
- Keep reports/results unchanged.
- Do not modify raw legacy evidence.
- Do not compute metrics.
- Do not render paper tables.
- Create deferred dossiers for unsafe cases rather than partially migrating them.

Expected efficient path:

After policy approval, attempt the 28 policy-approved deferred cases as a single batch. Create canonical packages only from public-safe core assets and evidence-retention mappings; do not copy raw legacy runs wholesale.
