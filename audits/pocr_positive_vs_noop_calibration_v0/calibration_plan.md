# Calibration Plan

The calibration compares two candidate classes on the same four cases: `positive_control` uses case-local `sql/pos_01.sql`, while `noop_control` uses existing no-op candidate SQL under `runs/user/common_core_pg_noop_db_checker/candidate_sql/`. Both classes are annotated with the same aligned Stage A prompt and checked by the same conservative static Stage B validator. No official POCR or route-level aggregation is produced.
