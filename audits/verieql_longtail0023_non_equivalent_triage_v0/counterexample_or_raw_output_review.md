# Counterexample Or Raw Output Review

VeriEQL reported `states=["EQU","NEQ"]` and `err="Symbolic reasoning: NOT EQUIVALENT."` for:

- source-vs-candidate at bounds 2, 3, and 4
- source-vs-source at bound 4
- candidate-vs-candidate at bound 4

The raw counterexample is present for each `non_equivalent` recheck. The bound-4 source-vs-candidate counterexample includes:

- `POSTLINKS` table with two inserted rows.
- `POSTS` table with two inserted rows.
- A row containing `NULL` values in `POSTLINKS`.
- Generated `TITLE INTEGER` in the counterexample even though the schema DDL declares `Title TEXT`.

The first part of the generated counterexample includes:

```sql
CREATE TABLE POSTLINKS (
  CREATIONDATE INTEGER,
  ID INTEGER,
  LINKTYPEID INTEGER,
  POSTID INTEGER,
  RELATEDPOSTID INTEGER
);
INSERT INTO POSTLINKS VALUES (117, 0, 0, 2, 1);
INSERT INTO POSTLINKS VALUES (NULL, NULL, 0, 2, 2);
```

The same counterexample pattern appears for identity support pairs. An identical SQL query should not be non-equivalent to itself under ordinary SQL semantics.

Interpretation:

- The counterexample is useful as a diagnostic clue for VeriEQL behavior.
- It is not acceptable as paper evidence of SQLGlot-noop candidate drift.
- The likely issue is a VeriEQL modeling/tool-semantics artifact around this CTE/aggregate/outer-join/null shape.
