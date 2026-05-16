# PERF_0056 Witness Design Notes

The retained witness is mapped from legacy schema/load files and retained output evidence. Its role is to preserve source/positive equality while exposing the hard-negative divergence.

Hard-negative discriminator: retained witness includes a group at the count boundary so the negative output diverges.

No DB validation, timing run, evidence regeneration, or new experimental claim was performed during migration.
