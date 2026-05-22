# Bounded Export Smoke Summary

Source run:

```text
runs/user/timing_sqlglot_noop_postgres_smoke
```

Command shape:

```text
tmpdir=$(mktemp -d)
PYTHONPATH=src python - <<'PY' "$tmpdir"
from pathlib import Path
from sql_rewrite_bench.user_output import export_run_to_output
exported = export_run_to_output(
    Path("runs/user/timing_sqlglot_noop_postgres_smoke"),
    Path("$tmpdir") / "output",
    repo_root=Path.cwd(),
)
PY
rm -rf "$tmpdir"
```

Observed smoke result:

- run id: `timing_sqlglot_noop_postgres_smoke`
- selected case count in manifest: `2`
- route id in manifest: `sqlglot_noop`
- result root created: yes
- log root created: yes
- report root created: yes
- manifest boundary flags: `local_diagnostic_only=true`, `official_metric_input=false`, `paper_result_input=false`
- repository-level `output/` runtime artifacts committed: no

The temporary output root was removed after the smoke.
