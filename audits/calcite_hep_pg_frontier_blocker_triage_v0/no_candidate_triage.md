# No-Candidate Triage

No-candidate rows: 7.

All seven are PORT rows where the external Calcite command exited successfully but emitted no candidate SQL. The adapter correctly preserved fail-closed behavior.

Rows blocked by quoted-identifier parse handling:

- `PORT_0003`
- `PORT_0005`
- `PORT_0008`
- `PORT_0012`

Rows blocked by DATETIME/type syntax handling:

- `PORT_0004`
- `PORT_0022`
- `PORT_0025`

Primary conclusion:

- The quoted-identifier rows are plausible adapter/runtime fix candidates.
- The DATETIME rows need type/syntax mapping work before candidate generation can be expected.
- Because all seven are PORT rows, broader tri-engine interpretation also needs route/source-role policy review before expansion.
