# Known Policy Rows

## MySQL ARRAY_ANY

`CONS_0005/mysql` remained fail-closed before candidate DB execution with bucket:

`mysql_unsupported_array_any`

Source execution was recorded through the MySQL source-only diagnostic path. Candidate execution stayed disabled.

## Spark CONS_0005

`CONS_0005/spark` remained a semantic mismatch. The known source/candidate row-count mismatch was not normalized and was not reclassified.

## Spark CONS_0036

`CONS_0036/spark` remained a label-only mismatch under the current strict-label policy. No checker normalization was implemented.

## Boundary

These rows behaved according to the current policy:

- unsupported MySQL lambda output fails closed;
- Spark semantic mismatch remains mismatch;
- Spark strict-label mismatch remains mismatch until a separate checker-normalization policy is authorized.
