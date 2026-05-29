# Implementation Summary

Added a small deployment toolkit for online new machines:

- `setup_baseline_adapters.sh` supports `core`, `calcite`, `prior-adapted`, and `all-safe` profiles.
- `check_baseline_adapters.sh` writes a local report under `output/reports/baseline_env_check_<timestamp>/baseline_report.txt`.
- `docs/baseline_deployment_en_ru.md` provides concise English/Russian setup guidance.

The scripts check adapter presence separately from runtime presence. SQLGlot is treated as a Python package route. Calcite HEP is optional/external and can be checked through a runtime root or archive. R-Bot, LLM-R2, and LearnedRewrite are reported as adapted wrappers unless separately reviewed official runtimes are configured.

The scripts do not call APIs, run baselines, run DB/checker/timing, run Track A 120, update top-level reports/results, vendor runtimes, or promote metrics.
