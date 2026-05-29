# Timing Environment Metadata Schema

Timing rows should reference one environment metadata artifact per local run or per engine context. This avoids duplicating environment details in every row while preserving enough context for local interpretation.

Suggested local path:

```text
runs/user/{run_name}/timing/environment_metadata.json
```

## Required Fields

| Field | Type | Notes |
| --- | --- | --- |
| `schema_version` | string | Suggested value: `timing_environment_metadata_v0`. |
| `environment_metadata_id` | string | Referenced by timing rows. |
| `created_at_utc` | string | ISO-8601 timestamp. |
| `host_fingerprint` | string/null | Non-secret local host fingerprint, if available. |
| `os_name` | string/null | Operating system name. |
| `os_version` | string/null | Operating system/kernel version. |
| `cpu_model` | string/null | CPU model if safely available. |
| `cpu_count_logical` | integer/null | Logical CPU count. |
| `memory_total_mb` | integer/null | Total memory if safely available. |
| `python_version` | string | Python runtime version. |
| `package_versions` | object | Relevant package versions, for example PySpark or SQLGlot. |
| `engine` | string | Engine for this metadata context. |
| `engine_version` | string/null | Database/engine version. |
| `engine_connection_mode` | string | Local, container, socket, TCP, Spark master, or equivalent. |
| `engine_settings_redacted` | object | Non-secret settings only. |
| `schema_setup_mode` | string | Fresh load, reused schema, temp schema, or equivalent. |
| `cache_policy` | string | Recorded timing policy cache setting. |
| `connection_session_policy` | string | Recorded timing policy session setting. |
| `source_candidate_pairing_policy` | string | Mirrors timing policy. |
| `env_vars_redacted` | object | Only non-secret, relevant variables. |
| `secret_redaction_policy` | string | Must state that secrets are omitted. |
| `claim_boundary` | string | `local_diagnostic_only`. |

## Secret Handling

Environment metadata must not include passwords, private DSNs, tokens, usernames when sensitive, local secret paths, or full environment dumps. It should record enough to interpret local timing without making the artifact publishable as official retained evidence.

## Spark-Specific Fields

Spark local timing metadata should record:

- `spark_master` if non-secret, for example local mode;
- `spark_app_name`;
- PySpark version;
- Java version if safely available;
- driver/executor memory settings if configured and non-secret;
- whether the Spark session was reused across source/candidate timing pairs.

## PostgreSQL/MySQL Fields

PostgreSQL and MySQL metadata should record:

- engine version;
- connection mode with secrets redacted;
- schema/database setup mode;
- whether a single connection/session was reused for the row;
- transaction/reset behavior;
- cache policy as declared by timing policy, not inferred.
