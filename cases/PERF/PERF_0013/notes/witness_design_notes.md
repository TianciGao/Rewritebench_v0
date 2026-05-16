# PERF_0013 Witness Design Notes

This note summarizes retained witness facts only. The legacy witness profile reports dataset `pg_minimal_witness_v1` with row counts `{'customer': 2, 'orders': 3, 'lineitem': 3, 'supplier': 2, 'nation': 2, 'region': 2}`. The hard-negative discriminator is: region-discriminator rows distinguish the intended regional slice from the negative slice. No DB rerun was performed during migration.
