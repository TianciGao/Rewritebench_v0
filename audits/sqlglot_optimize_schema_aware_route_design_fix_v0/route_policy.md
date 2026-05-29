# Route Policy

Chosen route:
- `route_id = sqlglot_optimize_schema_aware`
- CLI adapter option: `--route optimize_schema_aware`
- Existing user-entry method grouping: `method_id = sqlglot`

Preserved route:
- `route_id = sqlglot_optimize`
- CLI adapter option: `--route optimize`
- Behavior remains context-free and still calls `optimize(expression)`.

Reason:
- Schema-aware optimize changes the information available to SQLGlot, so it is not comparable to the old context-free optimize route.
- Keeping the names separate prevents silent semantic drift in historical or local diagnostic route cards.

Reporting rule:
- Local diagnostic ledgers should report `sqlglot_optimize_schema_aware` separately from `sqlglot_optimize`.
- Do not merge `noop`, `optimize`, and `optimize_schema_aware` into a single SQLGlot score.
