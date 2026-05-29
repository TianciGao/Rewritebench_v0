# External SQLSolver Contract Notes

Source reviewed: SQLSolver upstream README, https://github.com/SJTU-IPADS/SQLSolver, local external clone commit dcc2a91d8971a4c4d30b055f99d7d8428a1b754b; remote README also inspected via raw.githubusercontent.com on 2026-05-24.

## Input Files

SQLSolver's JAR interface accepts separate `-sql1`, `-sql2`, and `-schema` files plus optional `-print` and `-output` arguments. The query files are not free-form SQL scripts. They are line-oriented inputs: each SQL statement is stored on one line, and corresponding lines from `sql1` and `sql2` are matched as the pair to verify.

Design implication: the wrapper must preserve exactly one verifier statement per line. Multi-line SQL can be normalized into one line only after comment handling and statement-boundary handling are known safe. Leading `--` comments cannot be collapsed into the same line as SQL text, because a SQL line-comment may comment out the rest of the line.

## Parser Requirement

The upstream README states that SQLSolver parses SQL through Calcite. Query and schema text therefore need to satisfy Calcite parser syntax, not merely PostgreSQL syntax or the SQL accepted by the local DB/checker. PostgreSQL-specific constructs may need canonicalization or explicit out-of-scope classification before SQLSolver evidence is interpreted.

Design implication: SQLSolver wrapper input should have a separate Calcite-compatible canonicalization layer. It must be visible in metadata and must not alter benchmark source/candidate SQL files.

## Verdict Semantics

SQLSolver exposes four verifier results:

- `EQ`: the pair is proved equivalent.
- `NEQ`: the pair is proved non-equivalent.
- `UNKNOWN`: SQLSolver cannot determine equivalence. The upstream README explicitly includes unsupported SQL features and syntax errors as reasons.
- `TIMEOUT`: SQLSolver does not determine equivalence within the configured time limit.

Design implication: `UNKNOWN` and `TIMEOUT` are verifier-support outcomes, not method failures. They are excluded from any decidable SER denominator and must be reported separately.

## Undecidability Boundary

The upstream README notes that SQL equivalence is undecidable and that SQLSolver may output `NEQ` or `UNKNOWN` for equivalent query pairs. Identity guards are therefore mandatory before interpreting source-candidate results: if source-vs-source or candidate-vs-candidate returns `UNKNOWN`, the actual pair cannot be promoted as semantic equivalence evidence.

## Contract Impact for Current Gaps

The five bounded-pass identity unknown rows violate or stress at least one upstream contract boundary:

- `PERF_0006`: source line comments plus DATE literal syntax make line-shaping/comment handling suspect.
- `PERF_0007`: DATE/INTERVAL arithmetic likely needs Calcite-compatible normalization or exclusion.
- `PORT_0003`: draft DDL with inline comments and `DOUBLE PRECISION` produced parser diagnostics.
- `PORT_0005`: quoted identifiers, `NULLS FIRST`, and draft DDL preamble need policy before broader use.
- `LONGTAIL_0011`: DENSE_RANK/CTE ranking appears to be a SQL feature support gap even without obvious parser stderr.
