<!-- (kommiBo) Source-reviewed SQL learning recipe; synthetic examples only. -->
# Select one latest child for parents with a match

Model the CROSS APPLY glossary entry as a correlated top-one selection. Order by timestamp and a unique identity to make ties deterministic, and omit parents that have no child.

Source: [SP_CreateTables.sql, line 108](../../SP_CreateTables.sql#L108). The source stores a nine-row JOIN glossary and defines a parent/child relation; it does not execute these JOIN exercises.

Run from the repository root:

    python docs/examples/cross-apply-equivalent.py

The [complete example](../examples/cross-apply-equivalent.py) uses the shared [in-memory synthetic fixture](../examples/_fixture.py). Every invocation creates a fresh database, enables foreign keys and closes it. No persistent database or historical user data is used.

Expected result: [(7, 'INNER JOIN'), (8, 'LEFT JOIN')]. Parent 9 is omitted.

Dialect: The source describes SQL Server CROSS APPLY. A SQL Server exercise can use CROSS APPLY (SELECT TOP (1) ... ORDER BY DATE_TIME_STAMP DESC, INTERNAL_REG_NUM DESC) AS chosen. SQLite here uses a correlated scalar subquery with LIMIT 1 plus EXISTS; no APPLY query was executed.

Limit: This example models a scalar top-one projection. General APPLY can return multiple columns and rows per parent; this scalar equivalent does not cover those cases.

Review evidence should name the source SHA, interpreter/SQLite version, input, query, observed rows and unexecuted scope. Use the [source and validation map](README.md) to distinguish these examples from SQL Server tests.
