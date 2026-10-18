<!-- (kommiBo) Source-reviewed SQL learning recipe; synthetic examples only. -->
# Observe deletion inside a transaction and restore it with rollback

Inspect state both before and after rollback. Seeing zero rows inside a transaction is not evidence that the deletion persisted; the source defaults to its rollback branch.

Source: [SP_CreateTables.sql, line 116](../../SP_CreateTables.sql#L116). The source stores a nine-row JOIN glossary and defines a parent/child relation; it does not execute these JOIN exercises.

Run from the repository root:

    python docs/examples/transaction-rollback.py

The [complete example](../examples/transaction-rollback.py) uses the shared [in-memory synthetic fixture](../examples/_fixture.py). Every invocation creates a fresh database, enables foreign keys and closes it. No persistent database or historical user data is used.

Expected result: "inside transaction=0 rows; after rollback=3 rows; original keys preserved".

Dialect: The runnable example uses SQLite, not SQL Server. The relation or query shape is educational; SQL Server execution requires the separate disposable validator.

Limit: This is SQLite DML rollback evidence. SQL Server transactional DDL, TRY/CATCH, @@TRANCOUNT and the original script default require the actual SQL Server validator.

Review evidence should name the source SHA, interpreter/SQLite version, input, query, observed rows and unexecuted scope. Use the [source and validation map](README.md) to distinguish these examples from SQL Server tests.
