# Profile Matrix

| Profile | Scope | Installs | Checks | Non-goals |
| --- | --- | --- | --- | --- |
| `core` | SQLGlot, Direct LLM adapters, CLI help | `pip install -e ".[sqlglot]"`, `pytest` unless `--no-install` | `sqlglot`, adapter files, `cli.main`, `pocr-diagnostic`, `pocr-aggregate` | No API, no DB, no baseline run |
| `calcite` | Calcite HEP adapter and optional runtime | Optional archive extraction under `~/.local/share/sqlrb/` | Java 17, adapter, runtime root layout | No Calcite build/download, no source vendoring |
| `prior-adapted` | R-Bot / LLM-R2 / LearnedRewrite adapted wrappers | None | adapter files, redacted env variable names | No official upstream runtime install, no model/checkpoint download |
| `all-safe` | Safe checks for all profiles | Core Python deps unless `--no-install` | all above checks | No API, no DB/checker/timing, no Track A 120 |

Old-machine inventory facts incorporated:

- SQLGlot was ready as a Python package route.
- Calcite HEP had a local runtime tree but no active `SQLRB_CALCITE_HEP_*` env wiring.
- R-Bot and LLM-R2 official runtimes were not confirmed.
- LearnedRewrite external HTTP/CMD runtime env was not configured.
- Bulk `output/` / `runs/user` copy is not a deployment default.
