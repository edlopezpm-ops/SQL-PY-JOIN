#!/usr/bin/env bash
set +x
set -euo pipefail

readonly IMAGE='mcr.microsoft.com/mssql/server:2022-CU26-ubuntu-22.04@sha256:ba4c8329f48fb8f02e1416be6a930ebfd71268caee78aa985f3af4315e457c89'
readonly CONTAINER="sql-py-join-validation-$$"
readonly ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly SQLCMD='/opt/mssql-tools18/bin/sqlcmd'

if [[ -n "${KOMMIBO_SQL_SERVER+x}" || -n "${KOMMIBO_SQL_PASSWORD+x}" ]]; then
  if [[ "${KOMMIBO_SQL_SERVER:-}" != 'sqlserver,1433' || -z "${KOMMIBO_SQL_PASSWORD:-}" ]]; then
    printf '%s\n' 'Contained SQL validation requires the isolated sqlserver,1433 sidecar and its ephemeral password.' >&2
    exit 1
  fi
  if [[ ! -x "$SQLCMD" ]]; then
    printf '%s\n' 'Contained SQL validation requires the local sqlcmd client.' >&2
    exit 1
  fi
  readonly MANAGES_CONTAINER=false
  readonly SA_PASSWORD="$KOMMIBO_SQL_PASSWORD"
else
  readonly MANAGES_CONTAINER=true
  readonly SA_PASSWORD="Aekr!7$(openssl rand -hex 24)"
fi
readonly TEMP_DIR="$(mktemp -d)"

sql_exec() {
  if [[ "$MANAGES_CONTAINER" == true ]]; then
    docker exec --interactive --env SQLCMDPASSWORD="$SA_PASSWORD" "$CONTAINER" \
      "$SQLCMD" -S localhost -U sa -C "$@"
  else
    "$SQLCMD" -S "$KOMMIBO_SQL_SERVER" -U sa -P "$SA_PASSWORD" -C "$@"
  fi
}

# Explicitly flush the final batch for both pipe and regular-file sqlcmd stdin.
# The source file is preserved byte-for-byte; GO is client-side framing only.
sql_file() {
  { cat "$1"; printf '\nGO\n'; } | sql_exec -b -V 16
}

cleanup() {
  if [[ "$MANAGES_CONTAINER" == true ]]; then
    docker rm --force "$CONTAINER" >/dev/null 2>&1 || true
  fi
  rm -rf "$TEMP_DIR"
}
trap cleanup EXIT

if [[ "$MANAGES_CONTAINER" == true ]]; then
  docker run --detach --name "$CONTAINER" \
    --env ACCEPT_EULA=Y \
    --env MSSQL_SA_PASSWORD="$SA_PASSWORD" \
    "$IMAGE" >/dev/null
fi

for attempt in $(seq 1 60); do
  if sql_exec -Q 'SELECT 1' >/dev/null 2>&1; then
    break
  fi
  if [ "$attempt" -eq 60 ]; then
    if [[ "$MANAGES_CONTAINER" == true ]]; then
      docker logs "$CONTAINER"
    fi
    printf '%s\n' 'SQL Server did not become ready.' >&2
    exit 1
  fi
  sleep 2
done

sql_exec -b -V 16 <<'SQL'
CREATE DATABASE PYDB;
GO
USE PYDB;
GO
CREATE TABLE dbo.REGISTER
(
    INTERNAL_NUM int NOT NULL PRIMARY KEY,
    SCRIPT_NAME nvarchar(100) NOT NULL,
    SCRIPT_TYPE nvarchar(50) NOT NULL,
    ACTIVE char(1) NOT NULL,
    USER_STAMP nvarchar(50) NULL,
    PROCESS_STAMP nvarchar(200) NULL,
    DATE_TIME_STAMP datetime NOT NULL
);
INSERT dbo.REGISTER
    (INTERNAL_NUM, SCRIPT_NAME, SCRIPT_TYPE, ACTIVE, USER_STAMP, PROCESS_STAMP, DATE_TIME_STAMP)
VALUES
    (7, 'SP_CreateTables', 'SQL', 'Y', 'TEST', 'VALIDATION_FIXTURE', GETDATE());
GO
SQL

sql_file "$ROOT/SP_CreateTables.sql"

sql_exec -b -V 16 -d PYDB -Q \
  "IF OBJECT_ID('dbo.REGISTER_JOIN', 'U') IS NOT NULL THROW 51000, 'Rollback mode persisted REGISTER_JOIN.', 1;"

sed "s/declare @EjecutarCommit char(1) = 'N'/declare @EjecutarCommit char(1) = 'Y'/" \
  "$ROOT/SP_CreateTables.sql" > "$TEMP_DIR/SP_CreateTables.commit.sql"

for run in 1 2; do
  sql_file "$TEMP_DIR/SP_CreateTables.commit.sql"

  sql_exec -b -V 16 -d PYDB -Q \
    "IF (SELECT COUNT(*) FROM dbo.REGISTER_JOIN) <> 9 THROW 51001, 'Expected exactly nine join rows.', 1;
     IF NOT EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = 'REG_001' AND parent_object_id = OBJECT_ID('dbo.REGISTER_JOIN')) THROW 51002, 'REG_001 is missing.', 1;
     IF NOT EXISTS (SELECT 1 FROM sys.key_constraints WHERE name = 'UQ_REGISTER_INTERNAL_NUM' AND parent_object_id = OBJECT_ID('dbo.REGISTER')) THROW 51003, 'UQ_REGISTER_INTERNAL_NUM is missing.', 1;"
done

printf '%s\n' 'SQL Server validation: PASS'
