# Contributing to SQL-PY-JOIN

<!-- (kommiBo) Repository-specific contribution and validation guidance. -->

## Describe the database behavior

Include the commit, SQL Server version, exact command, transaction mode, expected state
and observed state. Use a minimal synthetic example. The default rollback mode still
executes mutations and can acquire locks; use an authorized disposable database.
Do not attach connection secrets, production dumps or operational records. Report
security-sensitive issues through [SECURITY.md](SECURITY.md).

Files expressly listed in [LICENSE](LICENSE) are available under the standard
[MIT License](LICENSES/MIT.txt), without a separate approval or website-terms
condition. External runtimes and unlisted material retain their own terms. Submit
only material you are authorized to provide; this guide creates no additional
contributor agreement. See the [licensing inventory](docs/licensing.md) and
[use boundaries](TERMS.md).

## Run the appropriate validation

From the repository root, the transport tests require Python 3 and Bash:

```shell
python3 -m unittest discover -s tests -p 'test_validate_sql.py' -v
```

These tests simulate external commands and verify transport and failure handling. They
do not run SQL Server. For SQL behavior, use the existing disposable-container checks
with Bash, Docker and access to the pinned Microsoft image:

```shell
bash tests/validate_sql.sh
bash tests/test_validate_sql_sidecar.sh
```

Review the external software terms before using the container. The first command
checks rollback, explicit commit, repeat execution, rows and keys. The second exports
the committed `HEAD` into a disposable sidecar, exercises native `sqlcmd` and rejects
invalid SQL; commit the intended proposal on its branch before using that check.
Neither command should be pointed at a persistent database. See the
[validation guide](docs/validation-guide.md) for the runtime boundaries.

## Submit evidence, not only an exit code

The SQL script catches errors and returns a result set without rethrowing. Explain the
database assertions that establish success; do not rely only on the client exit code.
For a bug fix, include the smallest regression case that fails before the fix and passes
after it. Mark unexecuted checks explicitly, particularly when Docker is unavailable.

Target the actual default branch, `practice/sql-python-saas`, through the existing PR,
validation and separate-review process. Keep SQL, transport and documentation changes
bounded and reviewable. Recover a merged code change with a revert PR; reverting Git
does not undo changes already committed to an external database.
