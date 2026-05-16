# PERF_0056 Schema Notes

Schema files were copied into the canonical engine-specific layout from the legacy case package. Witness load files were copied into matching `schema/<engine>/load.sql` files.

Required tables from static legacy metadata: customer_address, customer, store_sales, date_dim, item.

No schema execution was performed during migration.
