# Error Excerpt Log

Short excerpts from `runs/user/mysql_source_failure_triage/` are redacted to omit secrets and private host details. No passwords or connection strings were present in these excerpts.

## PORT_0003

```text
ERROR 1064 (42000) at line 6: syntax error near '"schools" ORDER BY ABS( "longitude" ) DESC NULLS LAST LIMIT 1'
```

## PORT_0005

```text
ERROR 1064 (42000) at line 6: syntax error near '"drivers" WHERE NOT "dob" IS NULL ORDER BY "dob" ASC NULLS FIRST LIMIT 1'
```

## PORT_0008

```text
ERROR 1064 (42000) at line 2: syntax error near '."admemail1" , "t2"."admemail2" FROM "frpm" AS "t1"'
```

## PORT_0012

```text
ERROR 1064 (42000) at line 2: syntax error near '"patient" WHERE "diagnosis" = 'RA' AND TO_CHAR( CAST( "birthday" AS TIMESTAMP )'
```
