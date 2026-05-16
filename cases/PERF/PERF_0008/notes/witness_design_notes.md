# PERF_0008 Witness Design Notes

This note summarizes retained witness facts only. The legacy witness profile reports dataset `pg_minimal_witness_v1` with row counts `{'customer': 3, 'orders': 3, 'lineitem': 3}`. The hard-negative discriminator is: segment-discriminator rows distinguish the intended customer slice from the negative slice. No DB rerun was performed during migration.
