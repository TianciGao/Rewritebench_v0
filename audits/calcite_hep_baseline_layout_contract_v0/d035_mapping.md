# D035 Mapping

D035 layout mapping:

| Surface | D035 role | Calcite HEP placement |
| --- | --- | --- |
| `baselines/` | baseline adapters and routes | `baselines/calcite_hep_fail_closed/adapter.py` |
| `src/sql_rewrite_bench/` | reusable core implementation | route identity detection in `local_timing.py` |
| `src/cli/` | user-facing facade | unchanged; existing `user evaluate --adapter-command` remains the facade |
| `output/results/<run_id>/` | user-facing local results | preserved by D035 export smoke under `/tmp/.../d035_output/results/` |
| `output/logs/<run_id>/` | user-facing local logs | preserved by D035 export smoke under `/tmp/.../d035_output/logs/` |
| `output/reports/<run_id>/` | user-facing local reports | preserved by D035 export smoke under `/tmp/.../d035_output/reports/` |
| top-level `reports/`, `results/` | official/paper surfaces | unchanged |

No new top-level route folders were created.

No Calcite binaries, JARs, build outputs, source checkouts, Gradle caches, or native libraries were added.
