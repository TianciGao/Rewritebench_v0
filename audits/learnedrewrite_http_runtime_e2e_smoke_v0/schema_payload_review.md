# Schema Payload Review

Selected row:

- `CONS_0036 / postgres`

Schema source:

```text
schemas/verieql_cons0036_v0/postgres/ddl.sql
```

DDL:

```sql
CREATE TABLE DEPT (NAME VARCHAR(32));
```

Adapter serialization:

- parsed one table: `DEPT`
- parsed one column: `NAME`
- normalized `VARCHAR(32)` to `varchar`
- emitted a LearnedRewrite-compatible schema JSON-array string
- schema payload SHA-256 recorded in metadata:
  `3594ea42c5a3df5aaa56810befe5846b543d709aea6eacfed839bbc7cbae0788`

Observed runtime request shape:

```json
{
  "sql": "SELECT NAME AS NAME, COUNT(*) AS C FROM DEPT GROUP BY NAME HAVING NAME = 'Charlie'",
  "schema": "[{\"table\":\"DEPT\",\"rows\":1000,\"columns\":[{\"name\":\"NAME\",\"type\":\"varchar\"}]}]"
}
```

Limitations:

- only PostgreSQL DDL serialization is enabled for the smoke path;
- no MySQL or Spark runtime smoke was attempted;
- complex TPC-H schemas and date-heavy SQL remain for a later bounded
  diagnostic;
- no case or schema file was modified.
