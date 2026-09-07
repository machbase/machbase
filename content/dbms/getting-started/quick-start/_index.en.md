---
type: docs
title: '1.2 10-Minute Quick Start'
weight: 20
toc: true
---

Connect to a running server, store one service-start event, and read it back. This example uses
a LOG table for append-oriented event data and explains the SQL results and the two time columns.
The estimated time does not include installing the server.

## Prerequisites

- Machbase DBMS is running on `127.0.0.1:5656`.
- The `machsql` command is available.
- You can connect with a practice account that can create, insert into, query, and drop tables.
- The commands below use the initial practice account `SYS` and password `MANAGER`. If the
  password has been changed, substitute its current value.
- You can save a SQL file under `/tmp`, and the practice table name `DBMS_GS_QUICK` is available.

Use a practice environment where this name does not conflict with a business table.
The final `DROP TABLE` deletes the practice table and the data inserted into it.

If the server is not ready yet, start with
[Installation, Deployment, and Upgrade](/dbms/installation-deployment-upgrade/) and
[Linux Standard Edition Installation](/dbms/installation-deployment-upgrade/standard-edition/#linux).

## Representative Sample

This sample records one service-start event in a LOG table. Explicitly create it with
`CREATE LOG TABLE`; the `_arrival_time` column is added automatically.

Save the SQL file and run it with the following commands.

```bash
cat > /tmp/dbms_gs_quick.sql <<'SQL'
CREATE LOG TABLE DBMS_GS_QUICK (
  EVENT_ID INTEGER,
  EVENT_TIME DATETIME,
  LEVEL VARCHAR(10),
  MESSAGE VARCHAR(40)
);

INSERT INTO DBMS_GS_QUICK (EVENT_ID, EVENT_TIME, LEVEL, MESSAGE)
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

### Check the Results

Check each SQL step for errors. The SELECT result should contain one row with `EVENT_ID`
equal to `1`, `LEVEL` equal to `INFO`, and `MESSAGE` equal to `service started`.
`EVENT_TIME` is the event timestamp supplied by the application. In this example,
`_arrival_time` is the server arrival timestamp recorded automatically by the DBMS.
Its value therefore changes each time you run the example and need not equal `EVENT_TIME`.

`CREATE LOG TABLE` defines the structure, and `INSERT` adds one row. `SELECT` specifies the
columns to read, while `ORDER BY EVENT_ID` specifies result ordering. If the final
`DROP TABLE` succeeds, the practice table is removed. To inspect the data further, omit the
final DROP statement before running the script, then remove only that practice table when
you finish.

If a rerun fails because `DBMS_GS_QUICK` already exists, a previous run may not have reached
the `DROP TABLE` step. Inspect it with `DESC DBMS_GS_QUICK;`. Only if it is the table from
your previous practice run should you execute `DROP TABLE DBMS_GS_QUICK;` and retry.
For a connection error, first check the server address, port, running state, and account details.

## What This Sample Checks

| Item | What it verifies |
|---|---|
| Server connection | `machsql` connects to `127.0.0.1:5656`. |
| Table creation | `CREATE LOG TABLE` explicitly creates a LOG table. |
| Data input | `INSERT` and `TO_DATE` store event data. |
| Data query | `SELECT` and `ORDER BY` verify the inserted row. |
| Automatic column | The server automatically records the LOG table's `_arrival_time`. |
| Cleanup | `DROP TABLE` removes the practice table. |
