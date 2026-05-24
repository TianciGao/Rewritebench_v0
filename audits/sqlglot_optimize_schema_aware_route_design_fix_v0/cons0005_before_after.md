# CONS_0005 Before/After

Before, context-free `sqlglot_optimize` emitted invalid qualification:

PostgreSQL:
```sql
SELECT "table1"."i" AS "i", "table1"."j" AS "j" FROM "table1" AS "table1" WHERE NOT "table1"."j" IN (SELECT "table1"."table2"."i" AS "i" FROM "table2" AS "table2" WHERE "table1"."i" = "table2"."j");
```

MySQL/Spark:
```sql
SELECT `table1`.`i` AS `i`, `table1`.`j` AS `j` FROM `table1` AS `table1` WHERE NOT `table1`.`j` IN (SELECT `table1`.`table2`.`i` AS `i` FROM `table2` AS `table2` WHERE `table1`.`i` = `table2`.`j`);
```

After, `sqlglot_optimize_schema_aware` resolved DDL for `table1` and `table2`, supplied schema context to SQLGlot, and no longer emitted:
- `"table1"."table2"."i"`
- `` `table1`.`table2`.`i` ``

Bounded generation/preflight smoke result for `CONS_0005`:
- PostgreSQL: candidate generated, preflight passed, invalid qualification absent.
- MySQL: candidate generated, preflight passed, invalid qualification absent; SQLGlot emitted an `ARRAY_ANY is unsupported` warning that should be reviewed during DB execution/checker validation.
- Spark: candidate generated, preflight passed, invalid qualification absent.

No DB execution/checker result is claimed by this before/after review.
