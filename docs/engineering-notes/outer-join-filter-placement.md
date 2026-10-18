<!-- (kommiBo) Source-reviewed SQL learning recipe; synthetic examples only. -->
# Keep optional children optional when filtering ACTIVE

Put an optional child condition in ON when empty parents must remain visible. A WHERE condition on the child rejects the NULL-extended rows after the join.

Source: [SP_CreateTables.sql, line 23](../../SP_CreateTables.sql#L23). The source stores a nine-row JOIN glossary and defines a parent/child relation; it does not execute these JOIN exercises.

Run from the repository root:

    python docs/examples/outer-join-filter-placement.py

The [complete example](../examples/outer-join-filter-placement.py) uses the shared [in-memory synthetic fixture](../examples/_fixture.py). Every invocation creates a fresh database, enables foreign keys and closes it. No persistent database or historical user data is used.

Expected result: ON retains (9, None); WHERE returns only (7, 1) and (8, 3).

Dialect: The runnable example uses SQLite, not SQL Server. The relation or query shape is educational; SQL Server execution requires the separate disposable validator.

Limit: The source seeds ACTIVE=Y in every glossary row. The synthetic fixture includes an N child to expose filtering; it does not imply that an ACTIVE check constraint exists.

Review evidence should name the source SHA, interpreter/SQLite version, input, query, observed rows and unexecuted scope. Use the [source and validation map](README.md) to distinguish these examples from SQL Server tests.
