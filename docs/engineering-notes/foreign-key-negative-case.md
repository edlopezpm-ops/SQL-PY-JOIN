<!-- (kommiBo) Source-reviewed SQL learning recipe; synthetic examples only. -->
# Reject an orphan child and preserve existing rows

Exercise the parent/child invariant with a deliberately missing parent. Explicitly enable SQLite enforcement before assuming that a foreign-key declaration protects an insert.

Source: [SP_CreateTables.sql, line 75](../../SP_CreateTables.sql#L75). The source stores a nine-row JOIN glossary and defines a parent/child relation; it does not execute these JOIN exercises.

Run from the repository root:

    python docs/examples/foreign-key-negative-case.py

The [complete example](../examples/foreign-key-negative-case.py) uses the shared [in-memory synthetic fixture](../examples/_fixture.py). Every invocation creates a fresh database, enables foreign keys and closes it. No persistent database or historical user data is used.

Expected result: "orphan rejected; three original children remain; foreign_key_check empty".

Dialect: The runnable example uses SQLite, not SQL Server. The relation or query shape is educational; SQL Server execution requires the separate disposable validator.

Limit: This verifies SQLite enforcement on the synthetic schema. SQL Server constraint existence and behavior still belong to tests/validate_sql.sh and its disposable SQL Server instance.

Review evidence should name the source SHA, interpreter/SQLite version, input, query, observed rows and unexecuted scope. Use the [source and validation map](README.md) to distinguish these examples from SQL Server tests.
