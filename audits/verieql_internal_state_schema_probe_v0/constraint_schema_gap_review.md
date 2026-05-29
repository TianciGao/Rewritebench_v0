# Constraint And Schema Gap Review

## Schema Requirements

VeriEQL requires a `FROM` clause and table schema for the batch path. Synthetic `SELECT 1` pairs failed as unsupported because the query lacked a `FROM` clause. Synthetic `SELECT a FROM T` pairs reached symbolic reasoning once a table schema was supplied.

## Constraints

The environment supports constraints including:

- primary key
- foreign key
- inclusion
- not-null
- range and comparison constraints
- membership constraints

The timeout runner applies constraints only when a JSONL record supplies them and the record is not marked as containing unsupported constraints.

## Did Missing Constraints Cause EQU+TMO?

Possibly, but not conclusively.

The identical synthetic pair `SELECT a FROM T` vs `SELECT a FROM T` should be equivalent without additional key or range constraints. The observed `EQU...TMO` is better explained by timeout-mode finite-bound progression than by a schema encoding failure.

Constraints can still matter for real cases:

- Missing primary-key or foreign-key metadata can change SQL equivalence obligations.
- Missing finite-domain/range constraints can increase solver difficulty.
- Unsupported constraints can force a fail-closed or not-supported path.

## Wrapper Adjustment Need

No immediate wrapper-side schema adjustment is required for the existing timeout-mode JSONL path. The wrapper should continue recording schema and constraint availability, but a separate task is needed before treating any constraint-enriched output as official evidence.

## Future Gap To Close

If clean equivalent verifier evidence is needed from VeriEQL, a future task should compare:

- timeout-mode batch runner behavior,
- bound-limited batch runner behavior through `parallel.cli_within_bound`,
- direct finite-bound API behavior used by VeriEQL's own tests,
- and constraint-rich built-in examples.

That comparison should remain local-only until evidence promotion is separately authorized.
