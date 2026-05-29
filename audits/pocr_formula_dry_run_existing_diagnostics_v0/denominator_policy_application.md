# Denominator Policy Application

D039 defines POCR@planned and POCR@candidate as the first two promotion views.

For this dry-run, the planned denominator for each included route is PG40 PostgreSQL: 40 Common-core cases x one engine. All 40 rows are planned POCR-eligible rows.

POCR@planned includes planned rows and applies fail-closed zero contribution for no candidate, generation failure, extraction failure, route mismatch, candidate mismatch, annotation missing, or schema-invalid after retry.

POCR@candidate includes candidate-bound rows with deterministic case, engine, method, route, and candidate identity. In these two dry-run routes, every planned row is candidate-bound, so POCR@planned and POCR@candidate use the same row set.

SQLGlot no-op has six schema-invalid or provider-failed annotation rows in the replay artifact. Under D039, those rows remain planned and candidate-bound, and their `OC_i` is zero because fail-closed status is deterministic.

Rows with no expected operation atoms would be recorded as `not_applicable_no_expected_operation_atoms`; none were observed in the two included PG40 routes.

Candidate mismatch and route mismatch rows would fail closed. Both included routes have zero route mismatch rows and zero candidate mismatch rows.

Unsupported rows would be retained as explicit status rows. None were observed in these two PostgreSQL PG40 replay artifacts.

POCR@curated remains deferred until a predeclared curated manifest exists.

Macro-average over per-row OC_i is the D039 formula. Do not replace macro-average with total supported atoms divided by total expected atoms.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted.
