<!-- (kommiBo) Source-reviewed SQL learning recipe; synthetic examples only. -->
# SQL engineering recipes

Reviewed baseline: 10b7ab82eddc1f5ac4acf0c920bd3b823535aa4f. [SP_CreateTables.sql](../../SP_CreateTables.sql) is a SQL Server glossary loader. It requires PYDB and an external dbo.REGISTER table; its committed switch defaults to rollback. The nine JOIN descriptions are data, not executed JOIN queries.

| Artifact | Responsibility | Evidence boundary |
| --- | --- | --- |
| [Loader](../../SP_CreateTables.sql) | Create/reload REGISTER_JOIN, resolve parent, add constraints and commit/rollback | CATCH returns error details without rethrowing; inspect database state, not only process exit. |
| [SQL validator](../../tests/validate_sql.sh) | Disposable SQL Server, rollback/commit assertions, nine rows and named constraints | Docker or fixed disposable sidecar with ephemeral credentials; requires its actual runtime. |
| [Transport tests](../../tests/test_validate_sql.py) | Mock command dispatch, final-batch GO framing and failure propagation | Simulated transport is separate from SQL execution. |
| [Recipe fixture](../examples/_fixture.py) | Small synthetic parent/child relations in SQLite memory | Educational semantics only; not SQL Server type, identity, collation, transaction or catalog validation. |

The fixture deliberately includes three parents, an inactive parent/child and a day-boundary timestamp. It retains only columns needed for the exercises; it is not the external REGISTER contract or a replacement for the loader. Every script closes its database; no server connection is opened.

Documentation patterns adapt provenance, responsibility maps, separate evidence denominators and bounded acceptance from [checktimecardandgivefeedback at 235a70f](https://github.com/edlopezpm-ops/checktimecardandgivefeedback/tree/235a70f1613f9a7c19515b3a579d7539dcff6b47): [entry](https://github.com/edlopezpm-ops/checktimecardandgivefeedback/blob/235a70f1613f9a7c19515b3a579d7539dcff6b47/00-START-HERE.md), [architecture](https://github.com/edlopezpm-ops/checktimecardandgivefeedback/blob/235a70f1613f9a7c19515b3a579d7539dcff6b47/01-architecture-and-stack.md), [evidence](https://github.com/edlopezpm-ops/checktimecardandgivefeedback/blob/235a70f1613f9a7c19515b3a579d7539dcff6b47/07-security-privacy-quality-and-evidence.md), and [review shape](https://github.com/edlopezpm-ops/checktimecardandgivefeedback/blob/235a70f1613f9a7c19515b3a579d7539dcff6b47/09-improvement-review-guide-and-open-decisions.md). SQL source remains authoritative here; no timeKER runtime claims transfer.

Run recipes with Python's standard library from the repository root. Record source SHA, Python/SQLite versions, command, rows and failure cases. Report SQLite examples, mocked transport tests and actual SQL Server validator results separately. A passing SQLite recipe does not establish SQL Server validation, a production migration, deployment or user acceptance. Keep the existing [validation guide](../validation-guide.md) and [recovery guide](../change-recovery.md) for operational details.

## Recipes

- [Match parent and child records with INNER JOIN](inner-join.md)
- [Preserve parents with no children using LEFT JOIN](left-join.md)
- [Explain RIGHT JOIN by reversing a LEFT JOIN](right-join-by-reversal.md)
- [Preserve both filtered projections with a full outer pattern](full-outer-projection.md)
- [Predict Cartesian-product size before CROSS JOIN](cross-join-cardinality.md)
- [Compare glossary rows without mirrored self pairs](self-join-pairs.md)
- [Select one latest child for parents with a match](cross-apply-equivalent.md)
- [Select an optional latest child while preserving parents](outer-apply-equivalent.md)
- [Keep optional children optional when filtering ACTIVE](outer-join-filter-placement.md)
- [Count child records without counting NULL placeholders](group-counts.md)
- [Reject an orphan child and preserve existing rows](foreign-key-negative-case.md)
- [Observe deletion inside a transaction and restore it with rollback](transaction-rollback.md)
- [Reload a glossary transactionally and compare logical rows](transactional-reload.md)
- [Select a calendar interval with an exclusive upper bound](half-open-date-range.md)
