#!/usr/bin/env bash
# MySQL local diagnostic environment template.
#
# The current backend reads SQLRB_MYSQL_* variables for manifest-declared
# cross-dialect source-reference diagnostics.
#
# Usage:
#   cp scripts/env_mysql.example.sh scripts/env_mysql.local.sh
#   # Edit scripts/env_mysql.local.sh for your local password, user, and host.
#   source scripts/env_mysql.local.sh
#
# The configured user must be allowed to create and drop temporary diagnostic
# databases. Do not commit scripts/env_mysql.local.sh or real passwords.

export SQLRB_MYSQL_HOST=127.0.0.1
export SQLRB_MYSQL_PORT=3306
export SQLRB_MYSQL_USER=root
export SQLRB_MYSQL_PASSWORD=change-me

# Legacy aliases for local convenience only. The SQL-RewriteBench backend reads
# SQLRB_MYSQL_*.
export MYSQL_HOST="$SQLRB_MYSQL_HOST"
export MYSQL_PORT="$SQLRB_MYSQL_PORT"
export MYSQL_USER="$SQLRB_MYSQL_USER"
export MYSQL_PASSWORD="$SQLRB_MYSQL_PASSWORD"
