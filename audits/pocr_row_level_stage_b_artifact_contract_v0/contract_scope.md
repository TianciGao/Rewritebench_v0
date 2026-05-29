# Contract Scope

Row-level Stage B artifacts are needed because D039 uses macro-average over per-row `OC_i`. A route-level aggregate count cannot reconstruct a macro-average when rows have different expected operation atom counts.

Aggregate counts are insufficient for D039 macro-average because `total_supported_atoms / total_expected_atoms` is a diagnostic micro-average only. Total supported atoms divided by total expected atoms is diagnostic micro-average only. It must not replace macro-average over per-row `OC_i`.

The dry-run showed that local `/tmp` replay artifacts were decisive for Repair-1 macro computation. `/tmp` replay files are not durable enough for official metric promotion because they are local, uncommitted, easy to delete, and not part of a stable D035 output contract.

This task therefore precedes reusable aggregator implementation. The aggregator needs a stable row-level input contract before any formula implementation can be trusted, tested, or reviewed at PG40 or Track A 120 scale.

Aggregator must not rely on /tmp replay artifacts.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted.
