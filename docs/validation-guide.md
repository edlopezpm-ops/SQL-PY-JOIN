<!-- (kommiBo) Operator-assisted maintenance; source-reviewed documentation. -->
# Disposable SQL validation: validation and diagnosis

Run from the repository root:

```shell
bash tests/validate_sql.sh
```

Run the Docker path on a machine with Bash, Docker, and OpenSSL. The [validator](../tests/validate_sql.sh) selects a digest-pinned SQL Server image, generates a temporary credential, creates `PYDB`, and removes its own container and temporary directory on exit.

| Check | Expected observation |
| --- | --- |
| Default script execution | `dbo.REGISTER_JOIN` does not persist after rollback. |
| Temporary commit-mode copy, run twice | Exactly nine join rows after each run. |
| Schema after each commit-mode run | Foreign key `REG_001` and unique constraint `UQ_REGISTER_INTERNAL_NUM` exist. |
| Sidecar negative case in CI | Invalid SQL exits nonzero through the native `sqlcmd` pipe. |

The temporary commit-mode copy does not modify [SP_CreateTables.sql](../SP_CreateTables.sql). Keep its committed `@EjecutarCommit` default at `N`. The script's `CATCH` returns an error result set without rethrowing; a process exit code alone is therefore insufficient. Preserve the database-state assertions.

The contained route requires the exact disposable `sqlserver,1433` sidecar, an ephemeral `KOMMIBO_SQL_PASSWORD`, and `/opt/mssql-tools18/bin/sqlcmd`. If either environment variable is set incompletely, validation rejects the configuration. The caller owns sidecar cleanup; do not aim this route at a persistent database.

For `SQL Server did not become ready`, inspect the disposable container startup and available runner resources. For `PYDB` already existing, check that a fresh disposable instance was used. For final-batch errors, retain the explicit `GO` framing in `sql_file`; do not edit the SQL artifact to compensate for transport behavior.

The Python transport tests use simulated commands. They supplement, and cannot replace, the real Docker and native-sidecar stages in [CI](../.github/workflows/validation.yml).

See [change and recovery guidance](change-recovery.md) before merging a correction.
