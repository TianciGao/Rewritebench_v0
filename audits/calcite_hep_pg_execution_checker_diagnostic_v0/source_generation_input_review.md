# Source Generation Input Review

The input generation audit is `audits/calcite_hep_pg_bounded_candidate_generation_v0/`.

Input candidate-generation counts:

| input_status | count |
| --- | --- |
| generated | 33 |
| no_candidate | 7 |

Candidate origin counts used by this execution/checker pass:

| candidate_origin | count |
| --- | --- |
| calcite_parse_only_schema_fallback | 4 |
| calcite_rel_to_sql | 29 |
| no_candidate | 7 |

The helper consumed candidate SQL paths from the prior audit CSV. It did not invoke Calcite and did not regenerate candidate SQL. Rows with no prior candidate stayed visible as no-candidate rows.

The prior audit flags remain local-only: `official_metric_input=false` and `paper_result=false`.
