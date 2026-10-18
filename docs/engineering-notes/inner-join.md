<!-- (kommiBo) Source-reviewed SQL learning recipe; synthetic examples only. -->
# Match parent and child records with INNER JOIN

Join on INTERNAL_NUM rather than on the child identity or display name. The fixture has parents 7, 8 and 9; two children belong to 7, one to 8 and none to 9.

Source: [SP_CreateTables.sql, line 102](../../SP_CreateTables.sql#L102). The source stores a nine-row JOIN glossary and defines a parent/child relation; it does not execute these JOIN exercises.

Run from the repository root:

    python docs/examples/inner-join.py

The [complete example](../examples/inner-join.py) uses the shared [in-memory synthetic fixture](../examples/_fixture.py). Every invocation creates a fresh database, enables foreign keys and closes it. No persistent database or historical user data is used.

Expected result: [(7, 'JOIN'), (7, 'INNER JOIN'), (8, 'LEFT JOIN')]. Parent 9 is absent.

Dialect: The runnable example uses SQLite, not SQL Server. The relation or query shape is educational; SQL Server execution requires the separate disposable validator.

Limit: A parent can produce multiple result rows. The actual source foreign key is named REG_001; the SQLite fixture uses equivalent referential intent, not the SQL Server catalog.

Review evidence should name the source SHA, interpreter/SQLite version, input, query, observed rows and unexecuted scope. Use the [source and validation map](README.md) to distinguish these examples from SQL Server tests.
