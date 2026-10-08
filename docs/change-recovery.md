<!-- (kommiBo) Operator-assisted maintenance; source-reviewed documentation. -->
# Disposable SQL validation: change boundaries and recovery

The default branch is `practice/sql-python-saas`, not `main`; resolve it again before opening a recovery PR.

| Artifact | Recovery boundary |
| --- | --- |
| `SP_CreateTables.sql` | Preserve its rollback default and the `dbo.REGISTER` prerequisite contract. |
| `tests/validate_sql.sh` | Docker owns its own container; sidecar mode does not remove external containers. |
| `tests/test_validate_sql_sidecar.sh` | Validates a committed `git archive HEAD`, including the invalid-SQL negative case. Uncommitted edits are not included in that snapshot. |

A Git revert reverses source changes only. It does not undo rows changed by a separate manual commit-mode execution against a persistent database. Preserve that distinction in any incident report, and do not use the disposable validator as a production recovery script.

## Recover through a reviewed PR

1. Read the current default branch and preserve the failing PR URL, its head SHA, and the relevant CI log. Distinguish an infrastructure failure from a changed project contract.
2. Create a separate recovery branch from the latest default branch. Inspect the original change and later dependent commits before choosing a corrective edit or `git revert`.
3. For a squash commit, revert that commit on the recovery branch. For a merge commit, inspect its parents and deliberately select the mainline; do not blindly copy a `-m` value. Resolve conflicts explicitly and preserve unrelated later work.
4. Run the [repository validation](validation-guide.md), inspect the diff, and open a recovery PR. Record the reason and the original PR/commit it compensates for.
5. Require the configured CI and separate reviewer approval on the current head. If the head changes, verify its checks and review again. Merge through the normal branch rules without bypass.
6. Verify the merge SHA on GitHub and the resulting default-branch validation. A successful local command or PR creation is not proof of merge completion.

Do not force-push the default branch or delete pre-existing files as a recovery shortcut. If kommiBo reports an uncertain effect, preserve its operation/run identity and reconcile it before submitting duplicate work. Writer and reviewer accounts are separate technical actors under one HOC; this is not an independent audit.
