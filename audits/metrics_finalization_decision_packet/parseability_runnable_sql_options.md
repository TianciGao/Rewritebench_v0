# Parseability And Runnable SQL Options

This file defines candidate distinctions for parseability, extractability, and runnable SQL status. It does not finalize metrics.

## SQL Extraction Success

Meaning:

- A method output or user submission contains a recoverable SQL candidate string.

Possible statuses:

- `extracted`
- `not_extracted`
- `multiple_candidates`
- `empty_output`
- `unknown`

Boundary:

- Extraction is before parser acceptance and before engine execution.

## Parseability

Meaning:

- The extracted SQL is accepted by an agreed parser or dialect parser.

Possible statuses:

- `parsed`
- `parse_failed`
- `not_applicable`
- `unknown`

Open question:

- Which parser or dialect parser governs this field?

Boundary:

- Parser acceptance is not engine execution and not semantic correctness.

## Syntactic Validity

Meaning:

- SQL appears syntactically valid under the selected dialect.

Open question:

- Should syntactic validity be identical to parseability or a separate manual/static status?

## Engine-parse Success

Meaning:

- The target DB engine accepts the SQL for planning or execution.

Boundary:

- Engine parsing may fail after static parser acceptance.

## Executable SQL

Meaning:

- SQL can be submitted to the target engine with required schema/data context.

Possible blockers:

- unsupported syntax;
- missing function;
- dialect mismatch;
- schema mismatch;
- missing candidate;
- preflight blocked.

## Runnable SQL

Meaning:

- Candidate reached the execution stage and can be run under the public or retained protocol.

Open question:

- Is runnable defined before execution or only after a successful execution attempt?

Recommended direction:

- Use `ready` for execution-ready and `executed` for actual execution.
- Add a future explicit `runnable_sql_status` if needed.

## Source-like / No-op Candidate

Meaning:

- Candidate is equivalent to the source text or an unmeaningful no-op transformation for the route being evaluated.

Boundary:

- Source-like/no-op can be parseable and executable but still needs separate status for method evaluation.

## Preflight Blocked

Meaning:

- Candidate did not reach execution because a deterministic preflight gate blocked it.

Boundary:

- Preflight blocked should not be counted as execution failure.

## Unsupported

Meaning:

- The route, engine, syntax, or feature is outside supported scope.

Boundary:

- Unsupported should remain separate from parse failure and semantic mismatch.

## Generation Failed

Meaning:

- No usable candidate was generated.

Boundary:

- Generation failure is before SQL extraction, parsing, and execution.

## Required Distinctions

The final contract must distinguish:

- parser acceptance;
- engine execution;
- semantic exactness;
- timed eligibility.

None of these should imply another without explicit ledger fields.
