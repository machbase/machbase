---
type: docs
title: '1.4 Choose the Next Document'
weight: 40
toc: true
---

After finishing the quick start, you are at the first fork in the road. Users storing
industrial IoT sensor values, users ingesting financial tick data, users analyzing
logs, and users connecting applications all need different next documents. The
Machbase DBMS manual is easiest to read by design question, not by feature name.

Before choosing the next document, ask four questions: how frequently data arrives,
how often it is queried by time range, how long raw data must be retained, and whether
rollup or aggregation is needed. These answers usually reveal which table type and
feature area to study first.

## Next Paths

| What you need to do | Next document |
| --- | --- |
| Store industrial IoT sensor, equipment, or measurement values | [TAG table design](/dbms/tag-table-usage/) |
| Store logs, events, or financial tick receive histories | [LOG table design](/dbms/log-table-usage/) |
| Manage equipment names, codes, or mapping data | [LOOKUP design](/dbms/lookup-table-usage/), and in RDB-supporting versions, [RDB design](/dbms/rdb-table-usage/) and [LOOKUP vs RDB](/dbms/data-modeling-table-design/table-types-selection-type/comparison-rdb-vs-lookup/) |
| Check SQL syntax | [SQL reference](/dbms/reference/sql/), [SQL ingestion](/dbms/data-input-load-export/sql/) |
| Connect applications | [Application integration](/dbms/application-integration/), [Driver guide](/dbms/application-integration/guide-drivers/) |
| Change operational settings | [Operations, configuration, and recovery](/dbms/operations-configuration-recovery/) |

## What to Check Next

- In TAG documents, check how `NAME`, `BASETIME`, and value columns model sensor measurements.
- In LOG documents, check how events and logs are appended in time order.
- In LOOKUP and RDB documents, check how to separate reference data, mappings, and join targets.
- In data ingestion documents, move from practice `INSERT` statements to operational paths such as Append API, machloader, and Collector.
