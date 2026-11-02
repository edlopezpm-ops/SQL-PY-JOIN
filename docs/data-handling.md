<!-- (kommiBo) Source-reviewed repository notice; no runtime or license grant is implied. -->

# Safe data handling and publication

Reviewed 2026-11-01.

This is an operator checklist for a SQL Server learning script and isolated join examples, with future SaaS ideas remaining unimplemented, not a claim that these controls
are automatically enforced by the code.

1. Use only an isolated disposable SQL Server instance. The checked-in rollback
   switch is a precaution, not permission to run the script on a production database.
2. Keep `@EjecutarCommit` at `N` in the source. A temporary `Y` copy can delete and
   reload `dbo.REGISTER_JOIN`; review that effect and the target database first.
3. Use synthetic values for user/process stamps and inspect captured query results.
   Do not publish connection strings, passwords, customer rows or diagnostic dumps.
4. In sidecar mode, provide only the disposable `sqlserver,1433` target and ephemeral
   password expected by the validator. The runtime must destroy that sidecar afterward.
5. Verify resulting database state as well as client exit codes: the source `CATCH`
   returns error details without rethrowing, so exit zero alone is insufficient.

Container removal is not an erasure guarantee for copied logs, exports, backups or
caller-managed storage. The repository does not impose a universal retention period.

## Review before publishing

Check the complete staged diff and all attachments, not just source extensions. Reject
secrets, real customer records, personal documents and unexplained binary exports.
Use synthetic reproductions in public discussions. If information is already public,
contact AEKR through [the privacy notice](../PRIVACY.md); changing the current file
does not erase Git history or third-party copies. Rotate an exposed credential through
its provider rather than relying on a later Git deletion.
