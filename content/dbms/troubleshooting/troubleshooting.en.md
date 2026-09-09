---
type: docs
title: '15.1 Troubleshooting Approach'
weight: 10
toc: true
---

Preserve state and evidence before reproducing a problem, then narrow the cause from the
smallest possible scope.

## Five-step troubleshooting procedure

1. Record the failure time, executed command, complete error message, and `ERR-` code.
2. Use `machadmin -e` and a connection test to distinguish server, network, and authentication failures.
3. Inspect server logs and session/statement state from the same time.
4. Correct one cause at a time and verify again with the same input.
5. Record the cause, action, validation results, and prevention measures.

<a id="symptom"></a>

## Identify symptoms

| Symptom | First checks |
|---|---|
| No server response | `machadmin -e`, process and port, server logs |
| Connection refused | Server state, listening address, firewall, port |
| Authentication failure | User, authentication mode, expiration, AUTH KEY state |
| SQL failure | Full SQL, target database and object, exact error code |
| Slow query | Execution plan, time range, rows scanned, concurrent load |
| Loading stopped | Successful/failed row counts, bad/log files, last successful position |

Restarting the server or changing settings before diagnosis can destroy evidence of the
original cause.

<a id="diagnosis-commands"></a>

## Diagnostic commands

```bash
machadmin -e
tail -100 "$MACHBASE_HOME/trc/machbase.trc"
```

```sql
SELECT * FROM V$VERSION;
SELECT ID, USER_NAME, CLOSED FROM V$SESSION ORDER BY ID;
SELECT ID, SESS_ID, STATE, QUERY FROM V$STMT ORDER BY ID;
SELECT * FROM V$STORAGE_USAGE;
SELECT NAME, VALUE FROM V$PROPERTY ORDER BY NAME;
```

Production results may contain sensitive information such as SQL text, usernames, and paths.
Review them before sharing.

<a id="log-logs"></a>

## Inspect logs

The default server log is `$MACHBASE_HOME/trc/machbase.trc`. Verify the actual path and rotation
settings against `V$PROPERTY` and the installation configuration.

```bash
tail -100 "$MACHBASE_HOME/trc/machbase.trc"
rg -n 'ERR-|ERROR|WARN' "$MACHBASE_HOME/trc/machbase.trc"
```

Before changing log levels or file counts, query the current `TRACE_LOG_LEVEL`,
`TRACE_LOGFILE_SIZE`, `TRACE_LOGFILE_COUNT`, and `TRACE_LOGFILE_PATH`. Excessive diagnostic
logging during an incident can affect disk usage and performance.

<a id="cause-lookup-error-codes"></a>

## Diagnose by error code

Record the exact error code and check its current definition in the
[Error Code Reference](/dbms/reference/error-codes/). If it is absent, collect the full message,
server build, reproduction SQL, and log timestamp.
