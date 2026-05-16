# Witness Design Notes

This draft package now includes draft-only witness planning rows, but they have not been loaded or executed.

## Tables

- `drivers`

## Minimal Draft Witness

- 4 rows are likely enough.
- Include one `NULL` `dob` plus three non-null `dob` values in different years.
- Keep the earliest and latest non-null `dob` rows mapped to distinct `nationality` values.

## Boundary Goal

- The source and positive rewrites should agree on the earliest non-null `dob`.
- The hard negative should fail by selecting the latest non-null row when ordering direction changes.
- The `NULL` row is retained as a conservative guard row, even though the query filters `dob IS NOT NULL` before ordering.
