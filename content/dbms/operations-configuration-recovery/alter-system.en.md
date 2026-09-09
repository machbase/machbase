---
type: docs
title: '13.4 ALTER SYSTEM Operations'
weight: 40
toc: true
---

`ALTER SYSTEM` is an administrative command that can affect the entire instance. Before execution,
check the target instance, privileges, active operations, and rollback or release commands.
For full syntax, see
[System and Session ALTER Syntax](/dbms/reference/sql/syntax/system-session-alter-syntax/).

## Common procedure

1. Verify the current server, database, and release.
2. Record relevant session, statement, backup, and checkpoint states.
3. Check the command's blocking, I/O, and memory impact.
4. Define the maintenance window and failure response.
5. Immediately afterward, check the result, relevant virtual tables, and logs.

<a id="checkpoint"></a>

## CHECKPOINT

```text
ALTER SYSTEM CHECKPOINT;
```

A checkpoint can increase storage I/O. Assess whether one is needed before backup or shutdown,
and observe its effect on concurrent bulk ingestion and queries. Do not run it repeatedly just
because the system is slow.

<a id="check-disk-usage"></a>

## CHECK DISK_USAGE

```text
ALTER SYSTEM CHECK DISK_USAGE;
```

Use this command when file system state and database storage metadata need inspection. Check
free space and mount status beforehand, then review the result logs. Do not edit internal files
to make the figures match.

<a id="install-license"></a>

## INSTALL LICENSE

```text
ALTER SYSTEM INSTALL LICENSE;
ALTER SYSTEM INSTALL LICENSE = '/absolute/path/license.dat';
```

Verify the license file's source, target instance, edition, and expiration date. Restrict its
permissions and do not copy its contents into documentation or logs. After installation, verify
it through `V$LICENSE_INFO` and a new connection.

<a id="kill-cancel-session"></a>

## KILL and CANCEL SESSION

```text
ALTER SYSTEM CANCEL SESSION session_id;
ALTER SYSTEM KILL SESSION session_id;
```

First check the user, client IP, SQL, and state in `V$SESSION` and `V$STMT`. Consider `CANCEL`
when first attempting to stop a running statement, and `KILL` when the connection itself must
end. Check rollback effects and possible duplicates from transactions, Appenders, and application retries.

<a id="freeze-unfreeze"></a>

## FREEZE and UNFREEZE

```text
ALTER SYSTEM FREEZE;
ALTER SYSTEM UNFREEZE;
```

Consider freeze only for file system snapshot procedures that cannot use the public backup
features instead. Define permitted reads and writes and the maximum freeze duration in advance.
Assign an operator and verification steps for `UNFREEZE` on every error path. Do not leave the
session in a frozen state.

<a id="flush-ager"></a>

## FLUSH AGER

```text
ALTER SYSTEM FLUSH AGER;
```

Consider this command when investigating delayed reclamation of deleted space. First check
retention policies, DELETE status, and available storage. Do not repeatedly force normal
background work.

<a id="flush-pvo-cache"></a>

## FLUSH PVO_CACHE

```text
ALTER SYSTEM FLUSH PVO_CACHE;
```

Clearing cached execution plans causes subsequent queries to be parsed and optimized again.
Use this command only to isolate schema or plan issues, and watch for temporary latency spikes
in concurrent queries. Do not use cache flushing as a remedy for persistent performance problems.

<a id="flush-sys-stat"></a>

## FLUSH SYS_STAT

```text
ALTER SYSTEM FLUSH SYS_STAT;
```

Save any required baselines before resetting cumulative statistics. Record the reset time in
monitoring so rate calculations and failure analysis remain accurate.

<a id="flush-page-cache"></a>

## FLUSH PAGE_CACHE

```text
ALTER SYSTEM FLUSH PAGE_CACHE;
```

Flushing the page cache can significantly change I/O and latency for subsequent queries. Use it
only for cold-cache comparisons or limited diagnostics, never at peak production load.

## Privileges and auditing

Use an administrative account with only the required privileges. Audit the command, target,
time, operator, reason, and result. Replace sample session IDs, paths, and configuration values
with the intended production values.
