#!/usr/bin/env bash
# Exercise native sqlcmd stdin as used by kommiBo; containment is tested upstream.
set +x
set -euo pipefail

readonly IMAGE='mcr.microsoft.com/mssql/server:2022-CU26-ubuntu-22.04@sha256:ba4c8329f48fb8f02e1416be6a930ebfd71268caee78aa985f3af4315e457c89'
readonly CONTAINER="sql-py-join-sidecar-test-$$"
readonly ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly SNAPSHOT="$(mktemp -d)"
export MSSQL_SA_PASSWORD="Aekr!7$(openssl rand -hex 24)"
export KOMMIBO_SQL_PASSWORD="$MSSQL_SA_PASSWORD"
export SQLCMDPASSWORD="$MSSQL_SA_PASSWORD"
trap 'docker rm --force "$CONTAINER" >/dev/null 2>&1 || true; rm -rf "$SNAPSHOT"' EXIT

# Export tracked content, never the checkout .git directory or its credentials.
git -C "$ROOT" archive HEAD | tar -x -C "$SNAPSHOT"
chmod 755 "$SNAPSHOT"

docker run --detach --name "$CONTAINER" --hostname sqlserver \
  --log-driver none \
  --env ACCEPT_EULA=Y --env MSSQL_SA_PASSWORD \
  --mount "type=bind,source=$SNAPSHOT,target=/workspace,readonly" \
  "$IMAGE" >/dev/null

docker exec --env KOMMIBO_SQL_SERVER=sqlserver,1433 --env KOMMIBO_SQL_PASSWORD \
  "$CONTAINER" bash /workspace/tests/validate_sql.sh

# A server-side SQL error must remain a nonzero result through the same pipe.
if printf '%s\n' 'SELECT * FROM dbo.TABLE_THAT_MUST_NOT_EXIST;' GO | \
  docker exec --interactive --env SQLCMDPASSWORD "$CONTAINER" \
    /opt/mssql-tools18/bin/sqlcmd -S sqlserver,1433 -U sa -C -b -V 16 -d PYDB; then
  printf '%s\n' 'Invalid SQL unexpectedly succeeded.' >&2
  exit 1
fi
printf '%s\n' 'Native sqlcmd sidecar transport: PASS'
