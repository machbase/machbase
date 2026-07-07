---
type: docs
title: '1. Getting Started'
weight: 10
toc: true
---

Machbase is an innovative time-series database designed to process time-series data
such as industrial IoT data and financial tick data as quickly and conveniently as
possible. This is the starting point for chapter 1. Understanding Machbase means
understanding how rapidly accumulating time-series data is received, stored, and
analyzed again.

In a time-series database, time is not just another column. It is the primary axis of
the data. A sensor value loses much of its meaning without the time it was measured,
and a financial tick is useful only when its order and interval are preserved.
Therefore, time-series systems place high-ingest writes, time-range queries,
aggregation, downsampling, retention, and compression near the center of the design.

High-volume ingest performance comes from the append-oriented structure of TAG/LOG
tables and the Append API. The `INSERT` samples in this chapter are for practice and
small-input checks; production ingest paths are covered in the data ingestion
documents.

This chapter helps a first-time Machbase DBMS user verify server connectivity, run SQL
through `machsql`, create the first table, insert rows, and query them back.

The examples assume that Machbase DBMS is running on `127.0.0.1:5656` and that
`machsql` is available in `PATH`. Every SQL example can be run as user `SYS` with
password `MANAGER`.
If you need to prepare the server first, start from
[Installation, Deployment, and Upgrade](/dbms/installation-deployment-upgrade/) and
[Linux Standard Edition installation](/dbms/installation-deployment-upgrade/standard-edition/linux/).

## Verify the Prerequisites

- Machbase DBMS is running on `127.0.0.1:5656`.
- The `machsql` command is available.
- The SQL files used in the examples are already saved under `/tmp`.

If a sample that creates a table fails at `CREATE TABLE` because the table already
exists, the previous run did not reach its final `DROP TABLE`. Run that sample's final
`DROP TABLE table_name;` once, then start again. The server used to verify this chapter
does not support `DROP TABLE IF EXISTS`.

## What You Will Check

1. How Machbase DBMS is designed for time-series data such as industrial IoT and financial tick data.
2. How to connect to port 5656 with `machsql`.
3. The two common shapes of time-series data: event-like records and measurements.
4. The first rule of thumb: LOG for event-like data, TAG for tag-based measurements.
5. How to create a table, insert rows, and query them.
6. Which document to read next for your workload.

## First Check

The first SQL statement is like a handshake. Whether the source is an industrial
sensor stream or financial ticks, processing begins only after the database session
can communicate with the server. The following SQL checks how many tables are
registered in the current database.

```sql
SELECT COUNT(*) AS TABLE_COUNT FROM M$SYS_TABLES;
```

Assuming the SQL above is saved as `/tmp/dbms_gs_check.sql`, run the following command.

```bash
machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER -f /tmp/dbms_gs_check.sql
```

A successful run prints one row with the `TABLE_COUNT` value.
