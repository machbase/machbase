---
type: docs
title: '1.2 10-Minute Quick Start'
weight: 20
toc: true
---

The quick start contains the only SQL sample you run directly in chapter 1. It verifies
server connection, table creation, insert, query, and cleanup in one flow. This page
uses a LOG table, the default table type. TAG, LOOKUP, RDB, and other table types are
covered in the table-design chapter.

## Prerequisites

- Machbase DBMS is running on `127.0.0.1:5656`.
- The `machsql` command is available.
- You connect as user `SYS` with password `MANAGER`.

If the server is not ready yet, start with
[Installation, Deployment, and Upgrade](/dbms/installation-deployment-upgrade/) and
[Linux Standard Edition installation](/dbms/installation-deployment-upgrade/standard-edition/linux/).

## Representative Sample

This sample records one service-start event in a LOG table. When no table type keyword
is specified, `CREATE TABLE` creates a LOG table. LOG tables automatically include
`_arrival_time`, the time when the server receives each row.

Save the SQL file and run it with the following commands.

```bash
cat > /tmp/dbms_gs_quick.sql <<'SQL'
CREATE TABLE DBMS_GS_QUICK (
  EVENT_ID INTEGER,
  EVENT_TIME DATETIME,
  LEVEL VARCHAR(10),
  MESSAGE VARCHAR(40)
);

INSERT INTO DBMS_GS_QUICK
VALUES (
  1,
  TO_DATE('2026-07-02 09:00:00', 'YYYY-MM-DD HH24:MI:SS'),
  'INFO',
  'service started'
);

SELECT _arrival_time, EVENT_ID, EVENT_TIME, LEVEL, MESSAGE
FROM DBMS_GS_QUICK
ORDER BY EVENT_ID;

DROP TABLE DBMS_GS_QUICK;
SQL

machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER -f /tmp/dbms_gs_quick.sql
```

If `service started` is printed, the basic SQL flow is working. `EVENT_TIME` is the
actual event time stored by the application, while `_arrival_time` is the server
receive time automatically recorded by the DBMS.

If a rerun fails because `DBMS_GS_QUICK` already exists, the previous run did not reach
the `DROP TABLE` step. Run `DROP TABLE DBMS_GS_QUICK;` once, then start again.

## What This Sample Checks

| Item | What it verifies |
| --- | --- |
| Server connection | `machsql` connects to `127.0.0.1:5656`. |
| Table creation | Bare `CREATE TABLE` creates a LOG table. |
| Data insert | `INSERT` and `TO_DATE` store event data. |
| Data query | `SELECT` and `ORDER BY` verify the inserted row. |
| Automatic column | LOG table `_arrival_time` is recorded by the server. |
| Cleanup | `DROP TABLE` removes the practice table. |
