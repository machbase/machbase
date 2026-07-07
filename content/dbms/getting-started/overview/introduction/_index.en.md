---
type: docs
title: 'Introduction to Machbase DBMS'
weight: 10
toc: true
---

Machbase DBMS is a time-series database designed to process time-series data such as
industrial IoT data and financial tick data as quickly and conveniently as possible.
Users still create tables and query data with SQL, but ingestion, storage, and query
behavior depend on the table type.

Traditional business data is often centered on finding and updating individual
records or joining business tables. Time-series data is different: it is usually
append-heavy, queried by time range, and interpreted through aggregations such as
average, maximum, minimum, and sum. Typical questions include "how did temperature
change during the last 10 minutes," "how many ticks arrived near market close," and
"which hours had the most equipment alarms last month."

## Core View

- Start with a LOG table when data continuously arrives, such as application logs,
  event histories, equipment status records, or financial tick receive logs.
- Start with a TAG table when the data clearly has tag name, time, and value columns.
- Start with LOOKUP for small, read-heavy reference data.
- Read the RDB-oriented documents for relational business entities and reference data
  where updates and relationships matter.
- Use VOLATILE tables for temporary working data.

This point of view matters when learning Machbase. The basic unit is not only "one
current value," but a flow of values over time. When designing a schema, consider
ingest rate, time predicates, aggregation interval, retention period, and reference
data relationships together.

## Introduction Sample

The following sample verifies that the SQL session can list tables in Machbase DBMS.

```sql
SHOW TABLES;
```

Assuming the SQL above is saved as `/tmp/dbms_gs_show_tables.sql`, run the following command.

```bash
machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER -f /tmp/dbms_gs_show_tables.sql
```

If at least one table exists, the result prints columns such as `USER_NAME`, `DB_NAME`,
`TABLE_NAME`, and `TABLE_TYPE` with table rows. In a freshly created empty database,
there may be no user-table rows. `KEYVALUE` tables whose names start with `_TAG_DATA_`
are internal tables managed by the DBMS for TAG tables, so they are not a first design
choice.
