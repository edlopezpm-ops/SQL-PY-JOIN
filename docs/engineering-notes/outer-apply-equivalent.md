<!-- (kommiBo) Source-reviewed SQL learning recipe; synthetic examples only. -->
# Select an optional latest child while preserving parents

Keep all parents while selecting one latest child. Removing the existence filter from the scalar projection shows the row-preservation difference represented by OUTER APPLY.

Source: [SP_CreateTables.sql, line 109](../../SP_CreateTables.sql#L109). The source stores a nine-row JOIN glossary and defines a parent/child relation; it does not execute these JOIN exercises.

Run from the repository root:

    python docs/examples/outer-apply-equivalent.py

The [complete example](../examples/outer-apply-equivalent.py) uses the shared [in-memory synthetic fixture](../examples/_fixture.py). Every invocation creates a fresh database, enables foreign keys and closes it. No persistent database or historical user data is used.

Expected result: [(7, 'INNER JOIN'), (8, 'LEFT JOIN'), (9, None)].

Dialect: The SQL Server shape is OUTER APPLY (SELECT TOP (1) ... ORDER BY DATE_TIME_STAMP DESC, INTERNAL_REG_NUM DESC) AS chosen. The runnable SQLite scalar-subquery equivalent validates the one-column top-one case only.

Limit: A NULL scalar result can mean no row or a NULL selected value. JOIN_NAME is NOT NULL in the fixture and source, so those cases remain distinguishable here.

Review evidence should name the source SHA, interpreter/SQLite version, input, query, observed rows and unexecuted scope. Use the [source and validation map](README.md) to distinguish these examples from SQL Server tests.
