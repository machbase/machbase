---
type: docs
title: 'SYSTEM/SESSION/ALTER SYSTEM'
weight: 210
toc: true
---

`ALTER SYSTEM` manages server-wide resources. `ALTER SESSION` sets parameters
for the current session only.

> **Privileges:** `ALTER SYSTEM` requires the `SYS` account or privileges
> granted with `GRANT ALTER ON DATABASE database_name TO user_name;`.

---

## ALTER SYSTEM {#alter-system}

### Command List

| Command | Description |
|--------|------|
| `KILL SESSION n` | Forcibly terminates a session |
| `CANCEL SESSION n` | Cancels the current query while retaining the session |
| `CHECKPOINT` | Immediately synchronizes memory buffers to disk |
| `FREEZE` | Pauses all DML for backup preparation |
| `UNFREEZE` | Resumes DML paused by FREEZE |
| `FLUSH AGER` | Immediately runs the Ager to clean expired data |
| `FLUSH SYS_STAT` | Refreshes optimizer system statistics |
| `FLUSH PVO_CACHE` | Clears the PVO Statement cache |
| `FLUSH PAGE_CACHE` | Forcibly releases the OS page cache |
| `FLUSH TAG_CACHE` | Clears the TAG metadata cache |
| `INSTALL LICENSE` | Installs the license file from the default path |
| `INSTALL LICENSE = 'path'` | Installs the license file from a specified path |
| `CHECK DISK_USAGE` | Recalculates LOG table disk usage |
| `SET property = value` | Changes system properties dynamically |

---

### KILL SESSION / CANCEL SESSION

```sql
alter_system_kill_session_stmt   ::= 'ALTER SYSTEM KILL SESSION'   session_id
alter_system_cancel_session_stmt ::= 'ALTER SYSTEM CANCEL SESSION' session_id
```

```sql
-- Inspect current sessions
SELECT id, user_id, client_type FROM v$session;

-- Force session termination (disconnect and transaction rollback)
ALTER SYSTEM KILL SESSION 12;

-- Cancel only the running query (retain connection)
ALTER SYSTEM CANCEL SESSION 6;
```

- `KILL SESSION`: SYS only; terminates the target session immediately.
- `CANCEL SESSION`: Same user or SYS only; retains the session and stops only its current SQL.

---

### CHECKPOINT

```sql
alter_system_checkpoint_stmt ::= 'ALTER SYSTEM CHECKPOINT'
```

Immediately synchronizes memory-buffered data to disk.

```sql
ALTER SYSTEM CHECKPOINT;
```

---

### FREEZE / UNFREEZE

```sql
alter_system_freeze_stmt   ::= 'ALTER SYSTEM FREEZE'
alter_system_unfreeze_stmt ::= 'ALTER SYSTEM UNFREEZE'
```

Pauses all DML when consistency is required, such as during backup preparation.

```sql
ALTER SYSTEM FREEZE;
-- (Perform backup or inspection)
ALTER SYSTEM UNFREEZE;
```

---

### FLUSH

```sql
alter_system_flush_stmt ::=
    'ALTER SYSTEM FLUSH'
    ( 'AGER'
    | 'SYS_STAT'
    | 'PVO_CACHE'
    | 'PAGE_CACHE'
    | 'TAG_CACHE' )
```

```sql
-- Run Ager immediately (clean expired data)
ALTER SYSTEM FLUSH AGER;

-- Refresh optimizer statistics
ALTER SYSTEM FLUSH SYS_STAT;

-- Clear PVO Statement cache
ALTER SYSTEM FLUSH PVO_CACHE;

-- Force OS page-cache release
ALTER SYSTEM FLUSH PAGE_CACHE;

-- Clear TAG metadata cache
ALTER SYSTEM FLUSH TAG_CACHE;
```

---

### INSTALL LICENSE

```sql
-- Default path ($MACHBASE_HOME/conf/license.dat)
alter_system_install_license_stmt ::= 'ALTER SYSTEM INSTALL LICENSE'

-- Specified path
alter_system_install_license_path_stmt ::= 'ALTER SYSTEM INSTALL LICENSE' '=' "'" path "'"
```

```sql
-- Install from the default path
ALTER SYSTEM INSTALL LICENSE;

-- Install from a specified path
ALTER SYSTEM INSTALL LICENSE = '/tmp/new_license.dat';
```

---

### CHECK DISK_USAGE

```sql
alter_system_check_disk_stmt ::= 'ALTER SYSTEM CHECK DISK_USAGE'
```

Recalculates `DC_TABLE_FILE_SIZE` in `V$STORAGE` from the filesystem. Use when
usage figures are inaccurate after a process failure or power outage.

```sql
ALTER SYSTEM CHECK DISK_USAGE;
```

---

### SET (Dynamic System Properties)

```sql
alter_system_set_stmt ::=
    'ALTER SYSTEM SET' property_name '=' value_expr

value_expr ::=
    value
  | property_name '|'  number   -- Bitwise OR (add flags)
  | property_name '&' '~' number -- Bitwise AND NOT (remove flags)
```

Dynamically changeable properties:

| Property | Description |
|------|------|
| `QUERY_PARALLEL_FACTOR` | Query parallelism thread count |
| `DEFAULT_DATE_FORMAT` | Default date format, such as `'YYYY-MM-DD HH24:MI:SS'` |
| `TRACE_LOG_LEVEL` | Trace log level (bit flags) |
| `DISK_COLUMNAR_PAGE_CACHE_MAX_SIZE` | Maximum disk columnar page-cache size |
| `MAX_SESSION_COUNT` | Maximum sessions |
| `SESSION_IDLE_TIMEOUT_SEC` | Session idle timeout (seconds) |
| `PROCESS_MAX_SIZE` | Maximum process memory size |
| `TAG_CACHE_MAX_MEMORY_SIZE` | Maximum TAG cache memory |
| `PVO_CACHE_ENABLE` | Enable PVO cache (0/1) |
| `PVO_CACHE_MAX_MEMORY_SIZE` | Maximum PVO cache memory |

```sql
-- Set values directly
ALTER SYSTEM SET TRACE_LOG_LEVEL = 3;
ALTER SYSTEM SET DEFAULT_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS';
-- Check current values before changing
SELECT NAME, VALUE, MIN, MAX
  FROM V$PROPERTY
 WHERE NAME = 'MAX_SESSION_COUNT';

-- Add bit flags (OR)
ALTER SYSTEM SET TRACE_LOG_LEVEL = TRACE_LOG_LEVEL | 0x00000004;

-- Remove bit flags (AND NOT)
ALTER SYSTEM SET TRACE_LOG_LEVEL = TRACE_LOG_LEVEL & ~0x00000001;

-- Set hexadecimal value
ALTER SYSTEM SET TRACE_LOG_LEVEL = 0x00000003;
```

---

## ALTER SESSION {#alter-session}

Changes session-level parameters.

```sql
alter_session_stmt ::=
    'ALTER SESSION SET' session_property_name '=' value
```

### SET SQL_LOGGING

```sql
ALTER SESSION SET SQL_LOGGING = flag
-- flag: Bitwise OR combination
-- 0x1: Parsing, validation, and optimization logs
-- 0x2: DDL execution result logs
```

```sql
ALTER SESSION SET SQL_LOGGING = 3;  -- Parsing + DDL logs
ALTER SESSION SET SQL_LOGGING = 0;  -- Disable logging
```

### SET DEFAULT_DATE_FORMAT

```sql
ALTER SESSION SET DEFAULT_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS';
ALTER SESSION SET DEFAULT_DATE_FORMAT = 'YYYYMMDD';
```

### SET SHOW_HIDDEN_COLS

Controls whether `SELECT *` includes hidden columns (`_arrival_time`).

```sql
ALTER SESSION SET SHOW_HIDDEN_COLS = 1;  -- Show hidden columns
ALTER SESSION SET SHOW_HIDDEN_COLS = 0;  -- Hide hidden columns (default)
```

### SET FEEDBACK_APPEND_ERROR

Controls whether Append API error messages are sent to the client.

```sql
ALTER SESSION SET FEEDBACK_APPEND_ERROR = 1;  -- Send error messages
ALTER SESSION SET FEEDBACK_APPEND_ERROR = 0;  -- Do not send error messages (default)
```

### SET MAX_QPX_MEM

Maximum memory in bytes for GROUP BY, DISTINCT, and ORDER BY in one SQL statement.

```sql
ALTER SESSION SET MAX_QPX_MEM = 1073741824;  -- 1GB
```

### SET DDL_LOCK_TIMEOUT

In Standard Edition, sets DDL lock wait time in seconds. Default `0`; range
`0`–`1000000`. At `0`, conflicting DDL returns
`ERR-02031: Resource busy (<object>)` immediately without waiting.

```sql
ALTER SESSION SET DDL_LOCK_TIMEOUT = 10;  -- Wait up to 10 seconds
```

Changing this setting does not alter a running DDL wait. The new value applies
to subsequent DDL. Check per-session values in `V$SESSION.DDL_LOCK_TIMEOUT`.

```sql
SELECT id, user_name, ddl_lock_timeout
  FROM v$session
 WHERE closed = 0
 ORDER BY id;
```

See [DDL Concurrency and Locks](../ddl-syntax/#ddl-concurrency) for conflict
scope and error handling.

### SET SESSION_IDLE_TIMEOUT_SEC

Maximum idle-session connection lifetime in seconds.

```sql
ALTER SESSION SET SESSION_IDLE_TIMEOUT_SEC = 300;  -- 5 minutes
```

### SET QUERY_TIMEOUT

Maximum query execution wait in seconds. Queries are cancelled automatically
when it expires.

```sql
ALTER SESSION SET QUERY_TIMEOUT = 60;  -- 60 seconds
```

---

## Related Views

| View | Description |
|----|------|
| `v$session` | Connected sessions and per-session parameters |
| `v$storage` | Disk usage, including `DC_TABLE_FILE_SIZE` |
| `v$license_info` | Installed license information |
| `v$property` | System properties and current values |

```sql
-- List sessions
SELECT id, user_id, client_type, login_time FROM v$session;

-- Check system properties
SELECT name, value FROM v$property WHERE name = 'TRACE_LOG_LEVEL';
```

---

## Related Documentation

- [ALTER SYSTEM Operations Guide](../../../../operations-configuration-recovery/alter-system/) – Procedures and command behavior
- [GRANT/REVOKE](../user-auth-syntax/#grant-revoke) – ALTER SYSTEM privileges
