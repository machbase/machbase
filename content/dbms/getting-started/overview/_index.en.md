---
type: docs
title: 'Machbase DBMS Overview'
weight: 10
toc: true
---

Machbase DBMS is a time-series database for processing data that continuously arrives
in time order, such as industrial IoT data and financial tick data. When sensor values
arrive like a factory conveyor belt, or market prices and volumes change in short
intervals, the first design question is where to store that data. In Machbase DBMS,
that starts with choosing a table type that matches the shape and lifecycle of the
data.

Time-series data usually appears in two shapes. The first is regular measurement data,
such as a sensor reporting temperature every second. The second is irregular event
data, such as an order execution, alert, log record, or received tick. Real systems
usually contain both. In industrial IoT, temperature and vibration are measurements,
while alarms and maintenance records are events. In finance, quote and trade ticks
arrive rapidly, while receive status and processing delays remain as events.

## Table Types to Separate First

| Table | Main use | First selection rule |
| --- | --- | --- |
| LOG | Append-heavy events, logs, and histories | Use it for high-volume records such as industrial equipment events or financial tick receive histories that are frequently queried by time. |
| TAG | Sensor, equipment, and measurement values with tag names and time | Use it when queries are centered on tag-based time series and aggregation. |
| LOOKUP | Codes, equipment metadata, and mapping data | Use it for small reference data that must be joined or looked up quickly. |
| RDB | Relational business data, state data, and larger reference or dimension data | Create it with `CREATE RDB TABLE`; it supports row-level `INSERT`, `UPDATE`, `DELETE`, and joins with other table types. |
| VOLATILE | Temporary session data | Use it for in-memory data that may disappear when the server stops. |

LOG and TAG are append-oriented tables for high-volume time-series ingest. They do
not support general `UPDATE`, and deletion must follow each table type's supported
conditions, such as `BEFORE`, `OLDEST`, `EXCEPT`, or tag/time predicates. If row-level
updates are central to the workload, read the RDB, LOOKUP, or VOLATILE documents first.

Table types are like different shelves in the same warehouse. A LOG table receives
records that keep piling up, while a TAG table organizes values by tag name and time
axis. For example, an equipment temperature value naturally fits a TAG table, while an
event saying that a tick was received fits a LOG table. Small reference data belongs
in LOOKUP, and relational business data with important relationships and constraints
belongs in an RDB table. RDB tables are covered in a later chapter.

When designing a time-series system, also think about the lifecycle of the data.
Recent raw data often needs high resolution and fast queries, while older data is
often useful as summarized data. Retention, rollup, downsampling, and compression are
therefore not secondary details; they directly affect operating cost and query
performance.

## Overview Sample

The following sample creates a LOG table, inserts one row, and checks the row count.
When no table type keyword is specified, `CREATE TABLE` creates a LOG table.

```sql
CREATE TABLE DBMS_GS_OVERVIEW (
  TS DATETIME,
  VALUE DOUBLE
);

INSERT INTO DBMS_GS_OVERVIEW
VALUES (TO_DATE('2026-07-02 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 1.5);

SELECT COUNT(*) AS ROW_COUNT FROM DBMS_GS_OVERVIEW;

DROP TABLE DBMS_GS_OVERVIEW;
```

Assuming the SQL above is saved as `/tmp/dbms_gs_overview.sql`, run the following command.

```bash
machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER -f /tmp/dbms_gs_overview.sql
```

If `ROW_COUNT` is `1`, create, insert, query, and drop all worked.
If a rerun fails because `DBMS_GS_OVERVIEW` already exists, run
`DROP TABLE DBMS_GS_OVERVIEW;` and start again.
