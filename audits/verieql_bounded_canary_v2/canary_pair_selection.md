# Canary Pair Selection

Real bounded canary execution status:

- skipped because VeriEQL was unavailable locally.

Safe future canary candidate:

- `CONS_0005`
- source SQL present: yes
- positive SQL present: yes
- hard-negative SQL present: yes
- candidate pair types that may be used after VeriEQL availability is confirmed:
  - `source_vs_positive`
  - `source_vs_hard_negative`

Executed smoke in this task:

- temp-only fail-closed support-pair smoke
- one synthetic `support_pair_smoke` pair
- one `not_attempted` verdict row

No Common-core run, no all-CONS run, and no method-generated candidate audit was performed.
