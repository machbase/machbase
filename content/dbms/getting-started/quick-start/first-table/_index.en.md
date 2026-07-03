---
type: docs
title: 'Create the First Table'
weight: 30
toc: true
---

Start with the simplest LOG table. A LOG table is the default table type for
append-heavy data such as events, logs, and histories.

When designing a time-series table, first ask how you will query it by time later.
For a first LOG table, an event time, event level, and human-readable message are
enough to establish the pattern.

## First Table Sample

```sql
CREATE TABLE DBMS_GS_FIRST_TABLE (
  EVENT_TIME DATETIME,
  LEVEL VARCHAR(10),
  MESSAGE VARCHAR(80)
);

SELECT NAME
FROM M$SYS_TABLES
WHERE NAME = 'DBMS_GS_FIRST_TABLE';

DROP TABLE DBMS_GS_FIRST_TABLE;
```

Assuming the SQL above is saved as `/tmp/dbms_gs_first_table.sql`, run the following command.

```bash
machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER -f /tmp/dbms_gs_first_table.sql
```

If `DBMS_GS_FIRST_TABLE` is printed, table creation and catalog lookup worked.
If a rerun fails because `DBMS_GS_FIRST_TABLE` already exists, run
`DROP TABLE DBMS_GS_FIRST_TABLE;` and start again.
