# Output Shape Review

D035-shaped output was written under the temp runtime root only:

- `/tmp/sqlrb_calcite_hep_track_a_120_execution_checker_diagnostic_v0/output/results/calcite_hep_track_a_120_execution_checker_v0__postgres/`
- `/tmp/sqlrb_calcite_hep_track_a_120_execution_checker_diagnostic_v0/output/results/calcite_hep_track_a_120_execution_checker_v0__mysql/`
- `/tmp/sqlrb_calcite_hep_track_a_120_execution_checker_diagnostic_v0/output/results/calcite_hep_track_a_120_execution_checker_v0__spark/`
- matching `output/logs/<run_id>/` directories
- matching `output/reports/<run_id>/` directories

The source user-run staging directories are under ignored local
`runs/user/<run_id>/` paths and are not staged or committed.

No repository-level `output/`, top-level `reports/`, or top-level `results`
artifact was staged.
