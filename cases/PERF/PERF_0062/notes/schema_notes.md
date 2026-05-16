# PERF_0062 Schema Notes

Schema files were copied into the canonical engine-specific layout from the legacy case package. Witness load files were copied into matching `schema/<engine>/load.sql` files.

Required tables from static legacy metadata: store_sales, store, customer_demographics, household_demographics, customer_address, date_dim.

No schema execution was performed during migration.
