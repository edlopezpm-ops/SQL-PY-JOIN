<!-- (kommiBo) Source-reviewed SQL learning recipe; synthetic examples only. -->
# Explain RIGHT JOIN by reversing a LEFT JOIN

A RIGHT JOIN preserves the relation on its right. Reverse table order to express that preservation as LEFT JOIN, and put the parent ACTIVE condition in ON so excluded parent projections become NULL.

Source: [SP_CreateTables.sql, line 104](../../SP_CreateTables.sql#L104). The source stores a nine-row JOIN glossary and defines a parent/child relation; it does not execute these JOIN exercises.

Run from the repository root:

    python docs/examples/right-join-by-reversal.py

The [complete example](../examples/right-join-by-reversal.py) uses the shared [in-memory synthetic fixture](../examples/_fixture.py). Every invocation creates a fresh database, enables foreign keys and closes it. No persistent database or historical user data is used.

Expected result: [(7, 1), (7, 2), (None, 3)]. All child rows survive.

Dialect: The SQL Server shape is REGISTER p RIGHT JOIN REGISTER_JOIN j ON p.INTERNAL_NUM=j.INTERNAL_NUM AND p.ACTIVE='Y'. The runnable equivalent reverses this into LEFT JOIN and does not require SQLite RIGHT JOIN support.

Limit: Parent 8 exists but its synthetic ACTIVE value is N. NULL means no match to the filtered parent relation, not a broken foreign key.

Review evidence should name the source SHA, interpreter/SQLite version, input, query, observed rows and unexecuted scope. Use the [source and validation map](README.md) to distinguish these examples from SQL Server tests.
