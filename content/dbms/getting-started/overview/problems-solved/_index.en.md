---
type: docs
title: 'Problems Machbase Solves'
weight: 20
toc: true
---

Machbase DBMS is most useful when data keeps flowing in rather than quietly sitting
still. Examples include factory equipment status, application access logs, urban
infrastructure sensor values, and financial market ticks. This data must not only be
stored, but also checked immediately and analyzed again later.

A time-series database does more than store a large number of rows. It must keep up
with fast ingest, make recent and historical data searchable by time, and support an
operational strategy for long-term storage. As raw data ages, systems often summarize
it or apply retention rules so storage growth remains manageable.

Machbase DBMS is useful when the following requirements appear together:

- Devices, sensors, applications, or market data feeds continuously generate data at
  sub-second or second-level intervals.
- Recent data must be queried immediately, while older data must remain available for
  long-term analysis.
- Ingestion performance, SQL, aggregation, joins, and retention policies must work
  together.
- Raw time-series data and reference data must be managed in the same system.
- Sub-second or millisecond raw data and minute, hour, or day-level aggregates often
  need to coexist.

Table types are the interface for separating these problems. LOG handles append-heavy
raw events, TAG handles tag-based measurements, and LOOKUP/RDB handles reference data.

This separation clarifies both ingest paths and query patterns. Raw events can be
appended quickly, tag measurements can be found by tag name and time, and reference
data can be used for joins and interpretation. The value of a time-series system
appears when these parts work together.

## Problem Sample

The following sample stores event-like data in a LOG table and queries it by time. In
an industrial IoT system, this can represent equipment status. In a financial system,
the same pattern can represent an event that a tick was received.

```sql
CREATE TABLE DBMS_GS_EVENTS (
  EVENT_TIME DATETIME,
  DEVICE_ID VARCHAR(20),
  STATUS VARCHAR(20)
);

INSERT INTO DBMS_GS_EVENTS
VALUES (TO_DATE('2026-07-02 09:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'pump01', 'OK');

SELECT DEVICE_ID, STATUS
FROM DBMS_GS_EVENTS
WHERE EVENT_TIME >= TO_DATE('2026-07-02 00:00:00', 'YYYY-MM-DD HH24:MI:SS');

DROP TABLE DBMS_GS_EVENTS;
```

Assuming the SQL above is saved as `/tmp/dbms_gs_events.sql`, run the following command.

```bash
machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER -f /tmp/dbms_gs_events.sql
```

If the result contains `pump01` and `OK`, event storage and time filtering worked.
This pattern is a starting point for data where you need to answer "what happened
when," such as failure histories, service state changes, security events, or tick
receive histories.
If a rerun fails because `DBMS_GS_EVENTS` already exists, run
`DROP TABLE DBMS_GS_EVENTS;` and start again.
