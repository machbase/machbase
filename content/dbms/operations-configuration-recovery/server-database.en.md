---
type: docs
title: '13.1 Server and Database Operations'
weight: 10
toc: true
---

`machadmin` starts and stops server instances, creates and drops physical databases, installs
licenses, and performs offline restores. Distinguish logical databases created with SQL
`CREATE DATABASE` from the physical instance database created with `machadmin -c`.

<a id="주요-option-확인"></a>

## Check the main options

```bash
"$MACHBASE_HOME/bin/machadmin" -h
```

Use the help for the installed release to check options and their effects.

<a id="start-server"></a>

<a id="server-시작과-종료"></a>

## Start and stop the server

You can safely run the status check.

```bash
"$MACHBASE_HOME/bin/machadmin" -e
```

Use one consistent method to start and stop the server: a service manager or your operations runbook.

- Before startup, check the configuration, license, data paths, and free space.
- After startup, check `machadmin -e`, a connection on port 5656, a lightweight SQL query, and server logs.
- Before a normal shutdown, block new connections and ingestion, and check active transactions,
  backups, and Appenders.
- Use a forced shutdown only after normal shutdown repeatedly fails and you have assessed the
  recovery impact.
- Do not force a recovery mode arbitrarily. Check the error and documented recovery procedure.

Command output can vary by release. Do not make automation depend on a complete success message.
Check both the process exit code and an actual connection.

<a id="create-delete-database"></a>

<a id="physical-instance-database"></a>

## Physical instance database

`machadmin -c` and `machadmin -d` create and delete physical instance data in `DBS_PATH`.
For logical databases, use the SQL described in [Multiple Databases](../multi-database/).

Deleting or initializing a physical database is destructive and can lose all instance data.
Do not delete and recreate a database to resolve a server startup error. Diagnose the error
first, then choose a recovery method that preserves the existing data.

Before execution, verify:

1. The absolute paths of the target `MACHBASE_HOME` and `DBS_PATH`.
2. That the service and processes have fully stopped.
3. A recent backup and a verified restore in an isolated environment.
4. The configuration, licenses, and logs to preserve.
5. Whether rollback is possible and the expected recovery time.
6. That two operators have cross-checked the instance and paths.

Do not manually create, move, or delete internal files or metadata in the data directory.

<a id="license"></a>

<a id="license-설치와-확인"></a>

## Install and verify a license

Treat license files as secrets. Do not copy their contents or actual keys into documentation,
support requests, or logs.

| State | Method |
|------|------|
| Install with the server stopped | The `machadmin` license option for the current release |
| Install with the server running | `ALTER SYSTEM INSTALL LICENSE` |
| Verify installation | `machadmin` license information and `V$LICENSE_INFO` |

```sql
SELECT *
FROM V$LICENSE_INFO;
```

Before installation, check the target instance, edition, validity period, and file permissions.
For online installation, the server process must be able to read the path. After renewal, verify
a new connection and the required edition features, and apply your retention policy to the
original license file.

## Information needed to diagnose failures

- `machadmin -e` output and exit code
- Release, edition, and `MACHBASE_HOME`
- Actual configuration and data paths
- Server startup and shutdown times
- Server logs around the first error
- File system free space and permissions
- Recent configuration, license, or storage changes

Do not delete the physical database or start with an initialization-based recovery merely
because the server will not start. Preserve backups while diagnosing the cause.
