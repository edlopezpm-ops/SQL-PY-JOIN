<!-- (kommiBo) Source-reviewed SQL learning recipe; synthetic examples only. -->
# Compare glossary rows without mirrored self pairs

Use two aliases for the same table to find rows with equal direction text. A strict identity comparison removes both a row matched to itself and mirrored duplicates.

Source: [SP_CreateTables.sql, line 107](../../SP_CreateTables.sql#L107). The source stores a nine-row JOIN glossary and defines a parent/child relation; it does not execute these JOIN exercises.

Run from the repository root:

    python docs/examples/self-join-pairs.py

The [complete example](../examples/self-join-pairs.py) uses the shared [in-memory synthetic fixture](../examples/_fixture.py). Every invocation creates a fresh database, enables foreign keys and closes it. No persistent database or historical user data is used.

Expected result: [('JOIN', 'INNER JOIN')].

Dialect: The runnable example uses SQLite, not SQL Server. The relation or query shape is educational; SQL Server execution requires the separate disposable validator.

Limit: Equal description text demonstrates comparison only. It is not a normalized category key or proof that two SQL operations have interchangeable behavior.

Review evidence should name the source SHA, interpreter/SQLite version, input, query, observed rows and unexecuted scope. Use the [source and validation map](README.md) to distinguish these examples from SQL Server tests.
