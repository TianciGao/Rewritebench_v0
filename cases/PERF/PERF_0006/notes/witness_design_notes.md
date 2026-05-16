# PERF_0006 Witness Design Notes

The retained witness contains four `lineitem` rows. One row is shipped exactly on the frozen cutoff date `1998-08-27`. Source and positive SQL include that row via the less-than-or-equal predicate; the hard negative excludes it via a strict less-than predicate.

The retained source output has two groups. Retained MySQL and Spark positive outputs match the source reference modulo existing text normalization. Retained negative outputs differ in the `A/F` group because the cutoff-date row is absent from the negative input.

This note summarizes existing retained evidence only. No DB validation was run during migration.
