# Unsupported Engine Rows

These 5 Spark rows failed closed as unsupported engine boundary rows. Repair-1 should not attempt them unless a separate Spark/PORT support-policy change makes the source row executable.

| case_id | pool | engine | source_executable | candidate_executable | exact | failure bucket | likely feedback type | attempt |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PORT_0008 | PORT | spark | false | false | false | unsupported_engine | unsupported_engine_boundary_feedback | no |
| PORT_0012 | PORT | spark | false | false | false | unsupported_engine | unsupported_engine_boundary_feedback | no |
| PORT_0022 | PORT | spark | false | false | false | unsupported_engine | unsupported_engine_boundary_feedback | no |
| PORT_0024 | PORT | spark | false | false | false | unsupported_engine | unsupported_engine_boundary_feedback | no |
| PORT_0025 | PORT | spark | false | false | false | unsupported_engine | unsupported_engine_boundary_feedback | no |

Boundary rule: Repair-1 repairs candidate SQL. It should not mask unsupported source-engine status or turn unsupported source rows into apparent model failures.
