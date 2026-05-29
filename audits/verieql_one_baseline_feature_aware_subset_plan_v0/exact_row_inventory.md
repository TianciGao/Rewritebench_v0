# Exact Row Inventory

Exact row inventory file:
- `exact_row_inventory.csv`

Inventory rule:
- A row enters the exact inventory only when it is selected, source executable, candidate generated, candidate executable, checker-successful, and `exact_status=exact`.

Counts:
- Exact candidate rows: 35.
- Rows excluded as not exact: 5.

Primary eligibility labels:

| label | count |
| --- | ---: |
| verifier_eligible_candidate | 1 |
| blocked_ddl_parser | 1 |
| blocked_like_not_implemented | 4 |
| blocked_exists_or_subquery | 17 |
| blocked_function_or_datetime | 10 |
| blocked_dialect_syntax | 2 |

CSV row count:
- Header rows: 1.
- Data rows: 35.

The inventory intentionally keeps source SQL, candidate SQL, schema context, checker context, denominator ID, feature labels, and local-only planning notes visible per row.

