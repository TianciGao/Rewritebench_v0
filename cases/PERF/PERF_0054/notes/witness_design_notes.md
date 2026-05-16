# PERF_0054 Witness Design Notes

The retained witness is mapped from legacy schema/load files and retained output evidence. Its role is to preserve source/positive equality while exposing the hard-negative divergence.

Hard-negative discriminator: retained witness isolates manufacturer 436 versus 437 rows so the negative output diverges.

No DB validation, timing run, evidence regeneration, or new experimental claim was performed during migration.
