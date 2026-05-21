# Environment Check

The local machine has a MySQL CLI at `/usr/bin/mysql`.

Required P4 MySQL source-reference environment variables:

- `SQLRB_MYSQL_HOST`
- `SQLRB_MYSQL_PORT`
- `SQLRB_MYSQL_USER`
- `SQLRB_MYSQL_PASSWORD` is optional; when present it is passed through `MYSQL_PWD` and not placed on the command line.

Observed environment:

- `SQLRB_MYSQL_HOST`: not set
- `SQLRB_MYSQL_PORT`: not set
- `SQLRB_MYSQL_USER`: not set
- `SQLRB_MYSQL_PASSWORD`: not reported
- `MYSQL_PWD`: not reported

Live MySQL diagnostic status: not run because required local connection configuration was missing.

No packages were installed and no local database configuration was changed.
