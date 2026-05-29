# Calcite HEP Readiness Note

Calcite HEP was readiness-only in this task. It was not annotated, replayed, aggregated, or used as POCR method evidence.

- postgres: `runs/user/calcite_hep_track_a_120_canonical_v0__postgres/candidate_sql` exists; candidate rows present 33/40; missing cases: PORT_0003, PORT_0004, PORT_0005, PORT_0008, PORT_0012, PORT_0022, PORT_0025
- mysql: `runs/user/calcite_hep_track_a_120_canonical_v0__mysql/candidate_sql` exists; candidate rows present 33/40; missing cases: PORT_0003, PORT_0004, PORT_0005, PORT_0008, PORT_0012, PORT_0022, PORT_0025
- spark: `runs/user/calcite_hep_track_a_120_canonical_v0__spark/candidate_sql` exists; candidate rows present 33/40; missing cases: PORT_0003, PORT_0004, PORT_0005, PORT_0008, PORT_0012, PORT_0022, PORT_0025

Calcite HEP can be considered for a later separately authorized POCR run, but it should retain missing rows explicitly fail-closed and should not use blocked local runtime results as method evidence.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted.
