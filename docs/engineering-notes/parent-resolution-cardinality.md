<!-- (kommiBo) Source-reviewed SQL learning recipe; synthetic examples only. -->
# Check that parent-name resolution returns exactly one row

The source resolves @InternalNum with a scalar subquery on SCRIPT_NAME. Uniqueness of INTERNAL_NUM alone does not make SCRIPT_NAME unique; inspect cardinality before depending on one resolved parent.

Source: [SP_CreateTables.sql, line 81](../../SP_CreateTables.sql#L81). The source stores a nine-row JOIN glossary and defines a parent/child relation; it does not execute these JOIN exercises.

Run from the repository root:

    python docs/examples/parent-resolution-cardinality.py

The [complete example](../examples/parent-resolution-cardinality.py) uses the shared [in-memory synthetic fixture](../examples/_fixture.py). Every invocation creates a fresh database, enables foreign keys and closes it. No persistent database or historical user data is used.

Expected result: "unique name resolves to 7; duplicate name detected before scalar use".

Dialect: The runnable example uses SQLite, not SQL Server. The relation or query shape is educational; SQL Server execution requires the separate disposable validator.

Limit: SQL Server scalar subqueries raise on multiple rows; SQLite scalar subqueries can choose a first row. The Python cardinality guard makes ambiguity explicit. The source also checks parent 7 before insert; its external REGISTER allocation contract must be preserved.

Review evidence should name the source SHA, interpreter/SQLite version, input, query, observed rows and unexecuted scope. Use the [source and validation map](README.md) to distinguish these examples from SQL Server tests.
