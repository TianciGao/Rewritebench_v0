# PERF_0077 Witness Design Notes

The retained witness is mapped from legacy schema/load files and retained output evidence. Its role is to preserve source/positive equality while exposing the hard-negative divergence.

Hard-negative discriminator: retained witness includes a keyword that satisfies the contains predicate but not the prefix predicate.

No DB validation, timing run, evidence regeneration, or new experimental claim was performed during migration.
