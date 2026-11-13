<!-- (kommiBo) Source-reviewed repository notice; no runtime or license grant is implied. -->

# Licensing and provenance inventory

Reviewed 2026-11-01.

No root project license has been selected. Neither the learning goal nor public hosting grants a general license to redistribute the SQL script or other project material.

| Component | Evidence and licensing boundary |
|---|---|
| SQL script and repository examples | No root project license; no general reuse grant is introduced. |
| SQL Server container | An external Microsoft distribution; `ACCEPT_EULA=Y` in the validator does not replace the operator's review of the applicable vendor terms. |
| `sqlcmd`, Bash, Docker and Python | External tools with their own notices; they are not relicensed by the project's branding. |

## AEKR provenance has a bounded scope

The [AEKR banner notice](../assets/AEKR-BANNER-LICENSE.txt) is copied unchanged from
the AEKR project-branding scaffold. It records the MIT provenance of that upstream
scaffold and any AEKR banner copied from it. Upstream references inside that verbatim
notice describe the toolkit, not a requirement to add its handbook here. It is not a
license for unrelated project code, data, personal material or third-party marks.

The AEKR footer names the workflow used. It neither transfers copyright to AEKR nor
imports the toolkit's CC BY handbook license into this repository. Where no banner
image is present, retaining its provenance notice does not claim that an image is bundled.

## Before redistributing

Check the actual files and installed dependency versions, preserve their applicable
notices, and obtain any missing permissions. A package name, a public repository,
a passing test or a software bill of materials is not itself a grant. This is a bounded
source inventory, not an exhaustive dependency-license or ownership certification.
The [use notes](../TERMS.md) cannot override a license grant.

Reference: [GitHub's repository licensing guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository).

<!-- (kommiBo) Decision guidance and Git-backed history; no relicensing. -->
## Reuse decisions

| Intended action | Applicable boundary |
|---|---|
| View or fork this public repository on GitHub | GitHub's platform permissions apply; they are not a general project license for off-platform distribution or reuse. |
| Redistribute or adapt `SP_CreateTables.sql` or the learning material | Identify the exact files and intended use, then obtain the missing project permission. The educational purpose is not a license grant. |
| Redistribute a SQL Server image or a validator environment | Review the licenses for the actual external distributions; the validator's EULA flag and a successful test do not grant redistribution rights. |
| Reuse the AEKR scaffold or banner material | Follow the scoped notice above; it does not cover unrelated project files or trademark endorsement. |

For a permission request, identify the repository, commit, exact files, intended use
and distribution. Send that scope to [aekr@aekr.io](mailto:aekr@aekr.io) without personal
inputs or confidential attachments. A request or repository contribution is not an
approval, transfer of ownership or automatic license change.

## Licensing change record

This records changes to license-related files and their effect. Documentation and
terms updates are not presented as a replacement software license.

| Date | Verified change | Effect on project permissions |
|---|---|---|
| 2026-11-01 | [Initial component inventory](https://github.com/edlopezpm-ops/SQL-PY-JOIN/commit/12904ee02ca52d39547ebb9dba090d8fb303a419) and [AEKR notice provenance](https://github.com/edlopezpm-ops/SQL-PY-JOIN/commit/bf32f6eda4d97e0d108d3cff131432a58c8c94f0). | Documented existing scopes; did not add a project-wide grant. |
| 2026-11-02 | [User-responsibility terms](https://github.com/edlopezpm-ops/SQL-PY-JOIN/commit/230573b3167f8166c941fe2914a2c4a51b4016bc). | Preserved existing licenses and non-waivable rights. |
| 2026-11-12 | Added reuse decisions and this source-linked record. | Clarifies the current permission boundaries; does not relicense project material. |

A future license change needs an explicit owner decision, identified files and rights,
the actual replacement text, and consistent documentation. Preserve third-party notices
and distinguish new terms from permissions already granted for earlier copies.
