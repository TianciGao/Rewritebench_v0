# PORT_0022 Migration Notes

Date: 2026-05-16

This canonical migration used a copy-first principle. The legacy repository was read only and unchanged. Historical evidence-mapping pilot artifacts were preserved.

## Portability Boundary

No DB validation was run. No new cross-engine execution result was created. No transfer-speed claim, complete nine-case PORT result claim, or ranking claim was created. No global leaderboard is established. Denominator, paper results, and Common-core membership are unchanged.

## Hard Negative

The hard negative is recorded as `year_filter_literal_changed`. The hard negative changes the creation-year literal from 2010 to 2011, changing the joined input rows counted. This explanation is static-inferred for migration unless separately approved in legacy review records.

## Spark Plan And Log Handling

Spark plan text is retained only through sanitized public copies and do-not-delete raw original mappings. Raw stdout/stderr logs were not copied into public retained evidence.

## Validation Script Caveat

The validation scripts are retained legacy validation assets. They were not executed during migration and are not final public user runners. Future public runner outputs must not write to case-local `runs/` by default.
