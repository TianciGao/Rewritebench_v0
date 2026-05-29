# User Surface D035 Layout Inventory

Task: `user_surface_d035_layout_inventory_v0`

This packet inventories the current user-facing CLI facade, output writer, baseline adapter locations, examples/docs surfaces, user-entry tests, development scripts, and verifier-support wrappers against D035.

This is an audit and layout-hygiene planning task only. It performs no physical migration, no case/case-set/schema/inventory movement, no experiment run, no metrics computation, no paper/report/result update, and no retained-evidence promotion.

Headline verdict:

- `src/cli/` is the current user-facing facade.
- `src/sql_rewrite_bench/` is the internal implementation package.
- baseline adapters are under `baselines/`.
- the user-facing output exporter writes D035-shaped `output/results|logs|reports/<run_id>/` paths.
- internal source-run staging still uses `runs/user/<run_id>/` and should remain transitional until a separately authorized cleanup.
- docs/examples need a future D035 organization pass, especially `docs/guide`, `docs/spec`, and `docs/templates`.
