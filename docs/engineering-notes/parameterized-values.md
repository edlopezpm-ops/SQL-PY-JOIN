<!-- (kommiBo) Source-reviewed SQL learning recipe; synthetic examples only. -->
# Bind query values instead of interpolating text

The project plans future Python integration. Practice value binding using the existing JOIN_NAME column while keeping schema identifiers fixed and the connection in memory.

Source: [SP_CreateTables.sql, line 83](../../SP_CreateTables.sql#L83). The source stores a nine-row JOIN glossary and defines a parent/child relation; it does not execute these JOIN exercises.

Run from the repository root:

    python docs/examples/parameterized-values.py

The [complete example](../examples/parameterized-values.py) uses the shared [in-memory synthetic fixture](../examples/_fixture.py). Every invocation creates a fresh database, enables foreign keys and closes it. No persistent database or historical user data is used.

Expected result: "known value matched once; SQL-looking value treated as data; three rows remain".

Dialect: The runnable sqlite3 DB-API uses ?. SQL Server parameter syntax depends on the chosen driver or sp_executesql; do not paste this transport syntax into sqlcmd and assume equivalence.

Limit: Parameters bind values, not table/column names or SQL keywords. The repository currently has no Python database integration; this example does not add one.

Review evidence should name the source SHA, interpreter/SQLite version, input, query, observed rows and unexecuted scope. Use the [source and validation map](README.md) to distinguish these examples from SQL Server tests.
