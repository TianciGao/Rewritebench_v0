# Witness Design Notes

This draft package does not include loaded or executed witness data yet.

## Tables

- `schools`

## Minimal Draft Witness

- 4 rows are likely enough.
- Include one positive longitude, one negative longitude, one smaller absolute value, and one `NULL` longitude.
- Use distinct `gsoffered` values so the selected top row is easy to compare without extra normalization.

## Boundary Goal

- The source and positive rewrites should agree on the highest absolute longitude after explicit null handling.
- The hard negative should fail by choosing the wrong row when sort direction or null ordering is mishandled.

## Intended Witness Exposure

- The witness should make the descending absolute-value winner obvious.
- The `NULL` longitude row should remain present so later reviewers can confirm that the draft positive rewrite is not over-claiming null-order portability.
