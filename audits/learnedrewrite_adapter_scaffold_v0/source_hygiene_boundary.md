# Source Hygiene Boundary

LearnedRewrite remains an external runtime only.

This task did not copy:

- upstream LearnedRewrite source code;
- `rewriter_java.jar`;
- Calcite dependency JARs;
- Java class files;
- checkpoints;
- datasets;
- generated outputs;
- request logs;
- legacy runtime outputs.

The release repo contains only:

- a Python adapter scaffold written for SQL-RewriteBench;
- a README documenting the external-wrapper boundary;
- fixture-only tests;
- audit/project-control documentation.

The upstream source-hygiene issue noted in earlier audits remains handled by not copying upstream source content or secret-looking values into this repository.
