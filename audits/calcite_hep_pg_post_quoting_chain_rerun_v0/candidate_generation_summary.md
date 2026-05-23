# Candidate Generation Summary

Candidate generation was rerun over all 40 Common-core v0 PostgreSQL rows.

| field | count |
| --- | ---: |
| selected_rows | 40 |
| generated_candidate_rows | 33 |
| no_candidate_rows | 7 |
| calcite_rel_to_sql candidates | 29 |
| calcite_parse_only_schema_fallback candidates | 4 |

No-candidate rows:

- `PORT_0003`
- `PORT_0004`
- `PORT_0005`
- `PORT_0008`
- `PORT_0012`
- `PORT_0022`
- `PORT_0025`

The no-candidate rows remain parser/input blockers. Four are still quoted-source PORT parse failures and three are DATETIME/TIMESTAMP parse/type failures.

Generated candidate postprocess:

- The PostgreSQL identifier-folding postprocess was active on generated candidates.
- Generated candidate count did not change from the pre-fix route card: 33 before, 33 after.
- The fix changes candidate SQL shape for DDL-backed quoted identifiers but does not make rows generate when the external runtime emits no candidate.
