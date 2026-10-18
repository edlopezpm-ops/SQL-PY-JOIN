<!-- (kommiBo) Source-reviewed SQL learning recipe; synthetic examples only. -->
# Predict Cartesian-product size before CROSS JOIN

A CROSS JOIN makes every combination. Predict its cardinality from the two inputs before interpreting it as a relationship or using it to generate a report grid.

Source: [SP_CreateTables.sql, line 106](../../SP_CreateTables.sql#L106). The source stores a nine-row JOIN glossary and defines a parent/child relation; it does not execute these JOIN exercises.

Run from the repository root:

    python docs/examples/cross-join-cardinality.py

The [complete example](../examples/cross-join-cardinality.py) uses the shared [in-memory synthetic fixture](../examples/_fixture.py). Every invocation creates a fresh database, enables foreign keys and closes it. No persistent database or historical user data is used.

Expected result: "3 parents x 3 children = 9 combinations" and endpoints (7, 1), (9, 3).

Dialect: The runnable example uses SQLite, not SQL Server. The relation or query shape is educational; SQL Server execution requires the separate disposable validator.

Limit: A Cartesian pair does not establish a foreign-key relationship. Large input sets multiply; use an explicit relation when combinations are not intended.

Review evidence should name the source SHA, interpreter/SQLite version, input, query, observed rows and unexecuted scope. Use the [source and validation map](README.md) to distinguish these examples from SQL Server tests.
