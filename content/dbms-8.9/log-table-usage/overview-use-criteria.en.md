---
type: docs
title: '7.1 Overview and Use Criteria'
weight: 10
toc: true
---

Data with timestamps does not all need the same table type. Periodic temperature readings and a
device reconnection event require different analysis. When choosing LOG, start with what each row
represents rather than whether it has a time column.

<a id="overview-log-characteristics"></a>

<a id="log의-한-행은-발생한-사건-하나입니다"></a>

## LOG Table Characteristics

LOG suits data that appends individual events, such as application errors, security-device block
records, and job start/end history. An `_arrival_time` column is created automatically in addition
to user columns, and queries can combine time-range predicates with message search.

The following example shows the difference between event time and ingestion time.

```sql
CREATE LOG TABLE ch7_overview (
    event_time DATETIME,
    device     VARCHAR(32),
    message    VARCHAR(128)
);

INSERT INTO ch7_overview VALUES (
    TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'),
    'DEV-01', 'connection restored'
);

SELECT _arrival_time, event_time, device, message FROM ch7_overview;

DROP TABLE ch7_overview;
```

The query returns one row. `event_time` is the fixed timestamp supplied in the example;
`_arrival_time` is assigned automatically during this insert. Running the example on another date
does not change `event_time`. For explicit timestamps and adjustment rules, see
[Time Model](../arrival-time-model/).

<a id="overview-log-use-criteria"></a>

<a id="원본을-쌓고-나중에-찾는-일이-중심이라면"></a>

## Use Criteria

Consider LOG when you frequently search for errors in the last hour, requests from an IP address, or
messages containing timeout, and do not need to update stored rows. Use the Append API for
continuous ingestion and loading tools for initial data or batches of files.

The inability to update rows does not by itself make audit data tamper-proof. Design deletion
privileges, access controls, retention policies, and backups separately.

Pay particular attention to retransmission. Resending an event may store another row. LOG has no
PRIMARY KEY or UNIQUE constraints, so do not expect automatic deduplication. Retain the source event
ID and define retry and duplicate-handling policies during collection.

<a id="overview-log-not-use"></a>

<a id="다른-모델이-더-단순한-경우도-있습니다"></a>

## Comparison with Other Tables

| Main workload | Table to consider first | Decision criteria |
|---|---|---|
| Measurements by sensor name and time-series aggregates | TAG | Name/time-axis queries and ROLLUP |
| Current reference data, such as device names and installation locations | LOOKUP | Query and modify small reference datasets |
| Order status changes, row deletion, and transaction processing | TRANSACTION | Modify rows and process operations as transactions |
| In-memory state that may be lost on restart | VOLATILE | Keep separate from source logs requiring permanent retention |

LOG does not support general `UPDATE` or `DELETE WHERE` with arbitrary predicates. You can append
correction events, but must store the original ID and correction reason and decide in the
application which corrections queries apply. If updates are routine, another table type is a clearer
choice.

<a id="overview-log-design-flow"></a>

<a id="테이블을-만들기-전에-조회할-질문을-정하세요"></a>

## Design Criteria

First distinguish whether analysis requires event time or collection time. Then identify frequently
used predicates, such as device, severity, and IP address. Store these values in separate columns
instead of extracting them from raw messages for every query; this makes SQL easier to understand
and maintain. Define retention at this stage as well. Disk usage continues to grow if you prepare
ingestion but postpone deletion.

The next section, [Schema Design](../table-structure-schema/), translates these requirements into
columns. If the choice is unclear, compare representative events alongside the queries you expect to
run.
