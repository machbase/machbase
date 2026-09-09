---
type: docs
title: '13.6 Observability and Diagnostics'
weight: 60
toc: true
---

Record the reproduction time and symptoms, then examine server state, sessions and statements,
storage and memory, and relevant logs on the same timeline. `M$` metadata tables describe schemas;
`V$` virtual tables expose current state.

<a id="log-diagnosis-logs"></a>

## Diagnostics and logs

1. Record when the problem started and ended, along with client information.
2. Check server responsiveness with `machadmin -e`.
3. Find relevant operations in `V$SESSION` and `V$STMT`.
4. Inspect virtual tables for the affected area, such as storage, memory, or ROLLUP.
5. Compare server, client, and loader logs from the same time.
6. Save current configuration properties and baselines before making changes.

<a id="configuration-trace-log"></a>
<a id="log-diagnosis-logs-configuration-trace-log"></a>

<a id="trace-log-설정"></a>

## Trace log configuration

Adjust trace levels, file sizes, and retention only as needed for diagnosis. Check property
names, allowed values, and restart requirements for the current release in the
[Configuration Reference](/dbms/reference/configuration/configuration/). Logs may contain
sensitive SQL and data, so set access permissions and retention periods.

<a id="log-server-logs"></a>
<a id="log-diagnosis-logs-log-server-logs"></a>

<a id="server-log"></a>

## Server logs

The default trace directory is `$MACHBASE_HOME/trc`. Inspect the actual directory and settings
instead of assuming fixed filenames.

```bash
ls -lh "$MACHBASE_HOME/trc"
tail -n 200 "$MACHBASE_HOME/trc/machbase.trc"
```

Review the first error, preceding warnings, server startup and shutdown, and checkpoint and
storage events chronologically, rather than merely counting error strings. Do not manually
bulk-delete log files.

<a id="log-logs-machsql"></a>
<a id="log-diagnosis-logs-log-logs-machsql"></a>

<a id="machsql-log"></a>

## machsql logs

`machsql.history` may contain credentials or sensitive SQL. Restrict history file permissions
for production accounts and review the contents before sharing diagnostics. Preserve reproduction
SQL together with the target database, execution time, results, and errors.

<a id="log-logs-machloader"></a>
<a id="log-diagnosis-logs-log-logs-machloader"></a>

<a id="machloader-log"></a>

## machloader logs

For bulk loading, check the process exit code, summary, logs, and rejected-row file together.

- Schema and input column count and order
- Delimiters, quote characters, and encoding
- NULL and DATETIME formats
- First failed row and recurring error codes
- Final successful and failed row counts

Do not blindly replay the entire rejected-row file. Fix the cause, validate a sample, then
reprocess only the failed rows.

<a id="item"></a>

<a id="metadata-table"></a>

## Metadata tables

Inspect the current database schema through `M$SYS_TABLES`, `M$SYS_COLUMNS`, `M$SYS_INDEXES`,
and related tables. Include database, owner, and object IDs in joins instead of joining by
name alone. Avoid application dependencies on reserved object names or internal table structures.

<a id="item-2"></a>

<a id="virtual-table"></a>

## Virtual tables

First check the actual columns in the current release.

```sql
SELECT * FROM V$SESSION LIMIT 1;
SELECT * FROM V$STMT LIMIT 1;
SELECT * FROM V$PROPERTY LIMIT 1;
SELECT * FROM V$STORAGE_USAGE LIMIT 1;
SELECT * FROM V$SYSMEM LIMIT 1;
SELECT * FROM V$ROLLUP LIMIT 1;
SELECT * FROM V$LICENSE_INFO LIMIT 1;
```

For the complete list and column definitions, see the
[System Catalog](/dbms/reference/system-catalog/virtual-table-full/).

<a id="monitoring-capacity"></a>

## Monitoring and capacity management

Base alerts on normal baselines, growth rates, peak workloads, and recovery headroom rather
than fixed thresholds. Review file system and database storage usage together, including
separate space used by backups and exports.

<a id="status-check-state-server"></a>
<a id="monitoring-capacity-status-check-state-server"></a>

<a id="server-상태"></a>

## Server state

```bash
"$MACHBASE_HOME/bin/machadmin" -e
```

A running process alone does not prove server health. Also check a native connection, a
lightweight SQL query, and recent server logs.

<a id="execution-session"></a>
<a id="monitoring-capacity-execution-session"></a>

<a id="session과-실행-sql"></a>

## Sessions and running SQL

```sql
SELECT id, user_name, user_ip, login_time, client_type
FROM V$SESSION
ORDER BY login_time DESC;

SELECT sess_id, id AS stmt_id, state, record_size, query
FROM V$STMT
ORDER BY sess_id, id;
```

A long-running operation is not necessarily an error. Check the workload type, processed rows,
client timeouts, and I/O and CPU state before deciding to cancel or kill it.

<a id="capacity-disk"></a>
<a id="monitoring-capacity-capacity-disk"></a>

<a id="disk-용량"></a>

## Disk capacity

```bash
df -h "$MACHBASE_HOME"
du -sh "$MACHBASE_HOME/dbs"
```

If a separate `DBS_PATH` is configured, check the actual path. Do not directly edit or delete
internal partition files.

<a id="memory-capacity"></a>
<a id="monitoring-capacity-memory-capacity"></a>

<a id="memory"></a>

## Memory

Compare OS available memory and swap with `V$SYSMEM`, cache usage, and query concurrency.
Do not make automation depend on internal manager names.

<a id="validation-backup"></a>
<a id="monitoring-capacity-validation-backup"></a>

<a id="backup-검증"></a>

## Backup validation

Do more than check backup command success. Record the path, size, and completion status, then
mount or restore in an isolated environment and verify key tables, row counts, time ranges,
and sample queries.

<a id="failure"></a>
<a id="monitoring-capacity-failure"></a>

## Collect diagnostic information

- Release and edition
- Incident time and time zone
- Reproduction commands, database, and user
- Server, client, and loader logs
- Relevant virtual table results
- OS CPU, I/O, memory, and disk metrics
- Recent schema, configuration, or deployment changes
- Actions already attempted and their results

Remove credentials, AUTH KEYs, personal information, and sensitive raw data from support materials.
