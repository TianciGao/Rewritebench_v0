# Wave 003 Follow-up Prompt

Task title: overnight_non_common_core_case_package_standardization_wave_003_manual_review

Use `audits/overnight_non_common_core_case_package_standardization_wave_002_policy_approved/wave002_policy_approved_deferred_cases.csv` as the input queue. Migrate only cases that receive explicit manual approval after concrete unsafe or missing assets are resolved. Keep `case_sets/`, denominators, reports/results, paper results, metrics, paper tables, and raw legacy evidence unchanged. Skip any case requiring DB execution, timing rerun, LLM call, raw log copy, private runtime trace copy, or local-path artifact copy.
