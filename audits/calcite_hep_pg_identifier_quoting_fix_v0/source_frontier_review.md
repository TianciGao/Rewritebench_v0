# Source Frontier Review

Input frontier: `audits/calcite_hep_pg_frontier_blocker_triage_v0/frontier_inventory.csv`.

The prior frontier triage classified 9 rows as `calcite_identifier_quoting_blocker`:

| case_id | prior stage | candidate origin | validation target |
| --- | --- | --- | --- |
| PORT_0003 | no_candidate | no_candidate | generation only |
| PORT_0005 | no_candidate | no_candidate | generation only |
| PORT_0008 | no_candidate | no_candidate | generation only |
| PORT_0012 | no_candidate | no_candidate | generation only |
| CONS_0036 | candidate_execution_failed | calcite_rel_to_sql | generation plus execution/checker |
| CONS_0037 | candidate_execution_failed | calcite_rel_to_sql | generation plus execution/checker |
| LONGTAIL_0011 | candidate_execution_failed | calcite_rel_to_sql | generation plus execution/checker |
| LONGTAIL_0012 | candidate_execution_failed | calcite_rel_to_sql | generation plus execution/checker |
| LONGTAIL_0013 | candidate_execution_failed | calcite_rel_to_sql | generation plus execution/checker |

The four PORT rows fail before candidate emission because the external runtime rejects double-quoted source identifiers. This adapter-side candidate postprocess cannot repair a candidate that does not exist, so those rows remain visible as no-candidate blockers.

The five generated-candidate rows previously failed PostgreSQL candidate execution because Calcite emitted quoted identifiers that did not match unquoted PostgreSQL DDL folding.
