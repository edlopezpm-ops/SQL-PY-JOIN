<!-- (kommiBo) Source-reviewed SQL learning recipe; synthetic examples only. -->
# Preserve both filtered projections with a full outer pattern

Compare active parents with all children. A child can be unmatched to that filtered parent projection even while referential integrity is valid. Combine a left join with only the unmatched right side.

Source: [SP_CreateTables.sql, line 105](../../SP_CreateTables.sql#L105). The source stores a nine-row JOIN glossary and defines a parent/child relation; it does not execute these JOIN exercises.

Run from the repository root:

    python docs/examples/full-outer-projection.py

The [complete example](../examples/full-outer-projection.py) uses the shared [in-memory synthetic fixture](../examples/_fixture.py). Every invocation creates a fresh database, enables foreign keys and closes it. No persistent database or historical user data is used.

Expected result: [(9, None), (7, 1), (7, 2), (None, 3)].

Dialect: SQL Server supports FULL OUTER JOIN directly. The runnable SQLite equivalent uses LEFT JOIN plus an anti-matched UNION ALL branch so it does not depend on newer SQLite FULL JOIN support.

Limit: UNION ALL retains multiplicity. The second branch must include only unmatched rows; otherwise matched pairs appear twice.

Review evidence should name the source SHA, interpreter/SQLite version, input, query, observed rows and unexecuted scope. Use the [source and validation map](README.md) to distinguish these examples from SQL Server tests.
