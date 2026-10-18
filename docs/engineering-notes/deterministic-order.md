<!-- (kommiBo) Source-reviewed SQL learning recipe; synthetic examples only. -->
# Use a unique tie-breaker for latest-row selection

A SELECT without ORDER BY does not promise display order. Add a unique identity after the timestamp when top-one selection or pagination must be repeatable.

Source: [SP_CreateTables.sql, line 113](../../SP_CreateTables.sql#L113). The source stores a nine-row JOIN glossary and defines a parent/child relation; it does not execute these JOIN exercises.

Run from the repository root:

    python docs/examples/deterministic-order.py

The [complete example](../examples/deterministic-order.py) uses the shared [in-memory synthetic fixture](../examples/_fixture.py). Every invocation creates a fresh database, enables foreign keys and closes it. No persistent database or historical user data is used.

Expected result: "equal timestamps ordered by unique ID descending: 2 then 1; latest=2".

Dialect: The runnable SQLite example uses LIMIT 1. SQL Server uses SELECT TOP (1) with the same ORDER BY timestamp and unique identity.

Limit: An identity is a deterministic tie-breaker, not a business timestamp or proof of event chronology. Source SELECT * statements are visual inspection, not ordered pagination.

Review evidence should name the source SHA, interpreter/SQLite version, input, query, observed rows and unexecuted scope. Use the [source and validation map](README.md) to distinguish these examples from SQL Server tests.
