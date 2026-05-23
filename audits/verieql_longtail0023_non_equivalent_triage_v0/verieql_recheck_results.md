# VeriEQL Recheck Results

Runtime root:

- `/tmp/sqlrb_verieql_longtail0023_non_equivalent_triage_v0/`

Policy:

- `verifier_tool=verieql`
- `verifier_mode=finite_bound`
- `timeout_seconds=30`
- `cores=1`

Recheck matrix:

| Recheck | Bound | Raw states | Normalized verdict | Counterexample |
| --- | ---: | --- | --- | --- |
| source vs candidate | 1 | `EQU` | `equivalent` | no |
| source vs candidate | 2 | `EQU|NEQ` | `non_equivalent` | yes |
| source vs candidate | 3 | `EQU|NEQ` | `non_equivalent` | yes |
| source vs candidate | 4 | `EQU|NEQ` | `non_equivalent` | yes |
| source vs source | 4 | `EQU|NEQ` | `non_equivalent` | yes |
| candidate vs candidate | 4 | `EQU|NEQ` | `non_equivalent` | yes |

The full recheck matrix is recorded in `recheck_matrix.csv`.

Interpretation:

- Source-vs-candidate still returns `non_equivalent` at the same bound-4 policy used by the all-exact attempt.
- Source-vs-source also returns `non_equivalent` at bound 4.
- Candidate-vs-candidate also returns `non_equivalent` at bound 4.
- Since the identity support pairs fail, the source-candidate `non_equivalent` verdict should not be treated as candidate semantic drift.
