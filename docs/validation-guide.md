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

## HOC review note — 2026-10-09

At the HOC's request, this note records Friday's maintenance review in repository history. The date uses America/New_York.

Automated baseline validation passed at [`fd41c5e90cdc`](https://github.com/edlopezpm-ops/SQL-PY-JOIN/commit/fd41c5e90cdcc370f830b9443d077ffcec906a90). The enabled documentation maintenance rules returned `NO_ACTION`: no eligible change was found.

The SQL check passed against a disposable SQL Server instance, including rollback and commit-state assertions; it did not run against a persistent database.

<details>
<summary>67 test · Friday lab 🤖</summary>

(kommiBo) HOC-requested, one-off contribution-count experiment for 2026-10-09 (America/New_York). These are jokes, not additional test cases or engineering review evidence. Operator-assisted delivery; the scheduled maintenance rules are unchanged.

- 01. 🤝 Two tables met for an INNER JOIN. — kommiBo 🤖
- 02. ↩️ ROLLBACK is the database version of just kidding. — kommiBo 🤖
- 03. 🔑 The foreign key brought a plus-one with referential integrity. — kommiBo 🤖
- 04. 🧹 The disposable database cleans up after the party. — kommiBo 🤖
- 05. 🦆 SELECT DISTINCT: fewer ducks in this row. — kommiBo 🤖
- 06. ☕ COMMIT only after the coffee and the assertions. — kommiBo 🤖

</details>
