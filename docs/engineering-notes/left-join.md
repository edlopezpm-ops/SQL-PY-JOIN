<!-- (kommiBo) Source-reviewed SQL learning recipe; synthetic examples only. -->
# Preserve parents with no children using LEFT JOIN

Start from the complete parent set when a report must display records with no detail. A missing child is represented by NULL, which Python sqlite3 returns as None.

Source: [SP_CreateTables.sql, line 103](../../SP_CreateTables.sql#L103). The source stores a nine-row JOIN glossary and defines a parent/child relation; it does not execute these JOIN exercises.

Run from the repository root:

    python docs/examples/left-join.py

The [complete example](../examples/left-join.py) uses the shared [in-memory synthetic fixture](../examples/_fixture.py). Every invocation creates a fresh database, enables foreign keys and closes it. No persistent database or historical user data is used.

Expected result: four rows, including (9, None).

Dialect: The runnable example uses SQLite, not SQL Server. The relation or query shape is educational; SQL Server execution requires the separate disposable validator.

Limit: The synthetic third parent exists to demonstrate absence. The source loader resolves one parent for all nine glossary rows; it does not create this multi-parent fixture.

Review evidence should name the source SHA, interpreter/SQLite version, input, query, observed rows and unexecuted scope. Use the [source and validation map](README.md) to distinguish these examples from SQL Server tests.
