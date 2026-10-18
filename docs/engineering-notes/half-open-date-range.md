<!-- (kommiBo) Source-reviewed SQL learning recipe; synthetic examples only. -->
# Select a calendar interval with an exclusive upper bound

Use greater-than-or-equal at the start and less-than at the next boundary. This includes all represented times in the day without guessing a last millisecond.

Source: [SP_CreateTables.sql, line 25](../../SP_CreateTables.sql#L25). The source stores a nine-row JOIN glossary and defines a parent/child relation; it does not execute these JOIN exercises.

Run from the repository root:

    python docs/examples/half-open-date-range.py

The [complete example](../examples/half-open-date-range.py) uses the shared [in-memory synthetic fixture](../examples/_fixture.py). Every invocation creates a fresh database, enables foreign keys and closes it. No persistent database or historical user data is used.

Expected result: "January 1 includes child IDs 1 and 2; exact January 2 boundary excluded".

Dialect: SQLite stores these synthetic timestamps as text with parameter placeholders ?. A SQL Server query should compare typed datetime parameters using the same >= start and < next-start shape.

Limit: The fixture uses uniformly formatted ISO text, so lexical comparison works here. SQL Server uses datetime and GETDATE, which supplies server-local time without a timezone offset; choose an explicit timezone contract before real reporting.

Review evidence should name the source SHA, interpreter/SQLite version, input, query, observed rows and unexecuted scope. Use the [source and validation map](README.md) to distinguish these examples from SQL Server tests.
