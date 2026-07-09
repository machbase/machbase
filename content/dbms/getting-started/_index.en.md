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
tables and the Append API. Here, append means continuously adding new rows rather than
frequently modifying existing rows. The representative sample in this chapter is for
practice and small-input checks; production ingest paths are covered in the data
ingestion documents.

This chapter first explains what Machbase is for, then uses one representative
`machsql` sample to verify server connectivity, table creation, insert, query, and
cleanup.

The representative sample assumes that Machbase DBMS is running on `127.0.0.1:5656`
and that `machsql` is available in `PATH`. It can be run as user `SYS` with password
`MANAGER`.
If you need to prepare the server first, start from
[Installation, Deployment, and Upgrade](/dbms/installation-deployment-upgrade/) and
[Linux Standard Edition installation](/dbms/installation-deployment-upgrade/standard-edition/#linux).

## Verify the Prerequisites

- Machbase DBMS is running on `127.0.0.1:5656`.
- The `machsql` command is available.
- You can save the representative SQL file under `/tmp`.

If the representative sample fails at `CREATE TABLE` because the table already
exists, the previous run did not reach its final `DROP TABLE`. Run
`DROP TABLE DBMS_GS_QUICK;` once, then start again. The server used to verify this chapter
does not support `DROP TABLE IF EXISTS`.

## What You Will Check

1. How Machbase DBMS is designed for time-series data such as industrial IoT and financial tick data.
2. How to connect to port 5656 with `machsql`.
3. The two common shapes of time-series data: event-like records and measurements.
4. The first rule of thumb: LOG for event-like data, TAG for tag-based measurements.
5. How to create a table, insert rows, and query them.
6. Which document to read next for your workload.

## Reading Order

1. Start with [Machbase DBMS Overview](./overview/) to separate time-series data shapes and table types.
2. Use [10-Minute Quick Start](./quick-start/) to verify `machsql`, table creation, inserts, and queries.
3. Review [Basic Command Cheatsheet](./command-cheatsheet/) for the commands used most often.
4. Choose a next path from [Choose the Next Document](./choose-next-doc/) for TAG, LOG, LOOKUP, or RDB.

The only SQL you run directly in this chapter is the representative sample in
[10-Minute Quick Start](./quick-start/). The other pages explain the concepts and the
next reading path without repeating the same SQL pattern.
