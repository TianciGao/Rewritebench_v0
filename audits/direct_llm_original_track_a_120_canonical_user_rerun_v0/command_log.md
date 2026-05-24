# Command Log

Preflight:

```text
git status -sb
git branch --show-current
git fetch origin
git merge-base --is-ancestor 0e07e08 HEAD
git merge-base --is-ancestor 0e07e08 origin/feature/case-package-v2-external-schema
git show origin/main:<project-control files>
git show origin/feature/case-package-v2-external-schema:<project-control files>
rg for D033/D034/D035
python scripts/dev/check_local_engine_env.py
tracked-file secret scan
staged protected-artifact check
```

Preflight summary:

```text
branch=feature/case-package-v2-external-schema
0e07e08_in_HEAD=yes
0e07e08_in_origin_feature=yes
origin_feature_D033_D034_D035=yes
origin_main_D033_D034_D035=no
postgres_available=yes
mysql_available=yes
spark_available=yes
tracked_secret_scan=passed
staged_protected_runtime_artifacts=no
```

Provider health check:

```text
status_code=200
classification=success
code_1010_detected=false
```

Evaluate:

```text
started_at=2026-05-24T15:10:16Z
ended_at=2026-05-24T15:23:15Z
exit_code=0
adapter_status_files=120
```

Canonical local metrics:

```text
local aggregate metrics written: runs/user/direct_llm_original_track_a_120_canonical_v0/metrics
source runs aggregated: postgres, mysql, spark
boundary: local diagnostic metrics only
```

Validation:

```text
metrics_parse=passed
d035_output_shape=passed
```
