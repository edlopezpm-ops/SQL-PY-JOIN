<!-- (kommiBo) Source-reviewed SQL learning recipe; synthetic examples only. -->
# Reload a glossary transactionally and compare logical rows

The source deletes existing glossary rows before reloading nine definitions. Compare logical content and count after repeated loads while recognizing that generated identities can change.

Source: [SP_CreateTables.sql, line 30](../../SP_CreateTables.sql#L30). The source stores a nine-row JOIN glossary and defines a parent/child relation; it does not execute these JOIN exercises.

Run from the repository root:

    python docs/examples/transactional-reload.py

The [complete example](../examples/transactional-reload.py) uses the shared [in-memory synthetic fixture](../examples/_fixture.py). Every invocation creates a fresh database, enables foreign keys and closes it. No persistent database or historical user data is used.

Expected result: "two committed loads; nine equal logical rows each; generated identities advanced".

Dialect: The runnable example uses SQLite, not SQL Server. The relation or query shape is educational; SQL Server execution requires the separate disposable validator.

Limit: The names are read from the source but direction, timestamp and notes are synthetic. Logical idempotence does not mean stable identity values, a non-destructive merge or SQL Server execution.

Review evidence should name the source SHA, interpreter/SQLite version, input, query, observed rows and unexecuted scope. Use the [source and validation map](README.md) to distinguish these examples from SQL Server tests.
