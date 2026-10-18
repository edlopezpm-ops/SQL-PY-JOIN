<!-- (kommiBo) Source-reviewed SQL learning recipe; synthetic examples only. -->
# Count child records without counting NULL placeholders

Aggregate a parent-preserving report with COUNT(child identity). COUNT(*) counts joined output rows, including the single NULL-extended placeholder for an empty parent.

Source: [SP_CreateTables.sql, line 112](../../SP_CreateTables.sql#L112). The source stores a nine-row JOIN glossary and defines a parent/child relation; it does not execute these JOIN exercises.

Run from the repository root:

    python docs/examples/group-counts.py

The [complete example](../examples/group-counts.py) uses the shared [in-memory synthetic fixture](../examples/_fixture.py). Every invocation creates a fresh database, enables foreign keys and closes it. No persistent database or historical user data is used.

Expected result: [(7, 2, 2), (8, 1, 1), (9, 1, 0)]; total children is 3.

Dialect: The runnable example uses SQLite, not SQL Server. The relation or query shape is educational; SQL Server execution requires the separate disposable validator.

Limit: These counts apply to this one-to-many relation. Joining another detail relation can multiply rows again and require preaggregation before counting.

Review evidence should name the source SHA, interpreter/SQLite version, input, query, observed rows and unexecuted scope. Use the [source and validation map](README.md) to distinguish these examples from SQL Server tests.
