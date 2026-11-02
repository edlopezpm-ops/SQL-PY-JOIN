<!-- (kommiBo) Source-reviewed repository notice; no runtime or license grant is implied. -->

# Privacy — SQL-PY-JOIN

Reviewed 2026-11-01.

## Scope and responsibility

AEKR maintains this project's notices and is the contact for questions at
[aekr@aekr.io](mailto:aekr@aekr.io). This notice covers a SQL Server learning script and isolated join examples, with future SaaS ideas remaining unimplemented.
It does not claim a new legal entity or apply the aekr.io website's analytics,
questionnaire, browser-data email service or retention periods to this repository.

## What the reviewed source does

`SP_CreateTables.sql` operates on `PYDB`, queries `dbo.REGISTER`, and creates or
reloads `dbo.REGISTER_JOIN` inside a transaction. Rows include user/process stamps
and timestamps, and query results are printed to the client. Those fields and SQL
client logs may contain operational information if real values are supplied.

The validation script creates disposable test data and uses a temporary SQL Server
password. Its Docker path removes its own container on exit; the sidecar path leaves
sidecar destruction to the caller. No hosted user account, analytics endpoint or
application retention service is implemented by this repository.

Source evidence: [SQL script](SP_CreateTables.sql), [validator](tests/validate_sql.sh), [transport tests](tests/test_validate_sql.py). This is a source review, not a guarantee about every
dependency, host, historical artifact or future deployment.

## Hosting, requests and retention

GitHub processes repository visits and collaboration activity under its
[privacy statement](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement).
If you serve a local copy over HTTP, that server can log requests. Downloading runtimes
or dependencies contacts their providers. Those operations are distinct from collection
implemented by the project itself. No repository-wide anonymous-visitor or zero-log
guarantee is made here.

Public issues, commits and attachments can be retained in history, forks, caches and
clones. Do not submit secrets, personal records or confidential data. For questions,
corrections, access or removal requests about project-held information, contact AEKR;
use [SECURITY.md](SECURITY.md) for a vulnerability report. Requests are considered under
applicable requirements; this notice promises neither a specific legal outcome nor
deletion of copies controlled by other parties. Local files have the retention described
in the [data-handling guide](docs/data-handling.md).
