---
type: docs
title: 'First INSERT and SELECT'
weight: 40
toc: true
---

After creating a table, insert data with `INSERT` and verify it with `SELECT`. This
sample inserts two rows and uses `ORDER BY` so that the result order is stable.

For time-series data, insert order and query order matter. Data such as financial
ticks or equipment events may arrive in large bursts, so reproducible ordering makes
analysis and verification much easier.

## INSERT and SELECT Sample

```sql
CREATE TABLE DBMS_GS_SAMPLE (
  EVENT_ID INTEGER,
  LEVEL VARCHAR(10),
  MESSAGE VARCHAR(80)
);

INSERT INTO DBMS_GS_SAMPLE VALUES (1, 'INFO', 'service started');
INSERT INTO DBMS_GS_SAMPLE VALUES (2, 'WARN', 'queue depth high');

SELECT EVENT_ID, LEVEL, MESSAGE
FROM DBMS_GS_SAMPLE
ORDER BY EVENT_ID;

DROP TABLE DBMS_GS_SAMPLE;
```

Assuming the SQL above is saved as `/tmp/dbms_gs_insert_query.sql`, run the following command.

```bash
machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER -f /tmp/dbms_gs_insert_query.sql
```

A successful run prints two rows: `service started` and `queue depth high`.
If a rerun fails because `DBMS_GS_SAMPLE` already exists, run
`DROP TABLE DBMS_GS_SAMPLE;` and start again.
