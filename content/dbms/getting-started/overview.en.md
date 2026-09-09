---
type: docs
title: '1.1 Machbase DBMS Overview'
weight: 10
toc: true
---

Machbase DBMS is a time-series database for storing and analyzing data that accumulates over time,
such as sensor measurements, equipment events, and application logs. You choose
tables to match the structure of your data and how you update and query it, and manage historical
records together with the reference data needed to interpret them.

<a id="introduction"></a>

## Introduction to Machbase DBMS

### What a Database and SQL Do

A database stores application data in a defined structure so that different tasks can reuse it.
A database management system, or DBMS, is the software that manages requests to read and write
that data, user permissions, and storage space.

A table groups records with the same structure. A row can represent one event or measurement.
Columns hold individual attributes, such as a timestamp, equipment name, or measured value.
Each column has a data type, such as a number, string, or date and time. This defined structure
is called a schema.

For example, a temperature history might look like this. The times and values below are
illustrative.

| Measurement target | Measurement time | Temperature |
|---|---|---:|
| Equipment A temperature sensor | 09:00:00 | 23.1 |
| Equipment A temperature sensor | 09:00:01 | 23.5 |
| Equipment B temperature sensor | 09:00:01 | 18.0 |

SQL is the language used to work with this data. `CREATE` creates a table, `INSERT` adds rows,
and `SELECT` reads the rows and columns you need. `WHERE` specifies selection conditions,
`GROUP BY` defines aggregation groups, and `ORDER BY` controls result ordering.
Although the SQL language is shared, supported changes and storage behavior depend on the
table type.

### Current State and Historical Records

“What is the current temperature of equipment A?” and “How did its temperature change over the
past hour?” are different questions. Repeatedly overwriting one current value loses the history.
Storing each measurement as a new row with a timestamp lets you analyze trends, maximum values,
and when an abnormal condition occurred.

These histories keep growing in a time-series system. In addition to ingestion speed, you must
decide which targets and time ranges you will query and how long you need to keep raw data.
Measurements do not necessarily arrive at regular intervals. Network delays, equipment outages,
and retransmission can produce late or missing readings.

### Measurements, Events, and Reference Data

A measurement describes the value of a particular target at a particular time. An event records
something that happened, such as an alarm, an equipment stop, or a service starting. Equipment
names, installation locations, and units of measurement are reference data used to interpret
those records.

A system often needs all three. Investigating an abnormal temperature may require the temperature
history, alarms from the same period, and the sensor's installation location. SQL joins
(`JOIN`) connect historical records with reference data through a shared value, such as an
equipment identifier.

<a id="problems-solved"></a>

## Problems Machbase Solves

Machbase's time-series features can be used together for the following tasks.

| Task | Example | Related features |
|---|---|---|
| Collect raw history | Continuously store sensor readings and equipment events | TAG and LOG tables, SQL input, and SDK Append |
| Query a relevant range | Inspect equipment A's temperature changes over the past hour | Tag and time conditions, indexes, and execution plans |
| Query recurring statistics | Compare minute or hourly trends over long periods | TAG ROLLUP |
| Interpret data | Associate sensor codes with equipment names and locations | Reference data and JOIN |
| Manage retention periods | Remove raw records past their retention period | Retention Policy on supported tables |
| Protect data against failures | Verify backup and recovery procedures | Edition-specific backup and recovery features |

ROLLUP computes statistics over ranges of raw data. Compression reduces the space needed to
store data, while a Retention Policy deletes old records. These features serve different purposes;
having aggregates does not by itself mean that it is appropriate to delete the raw data.

Performance requirements depend on data types, ingestion volume, concurrent queries, retention
periods, and server resources. Learn the workflow with a small example, then measure throughput
and latency using actual data and query conditions.
[Core Concepts](../../core-concepts/) explains the roles of these features in more detail.

## Choosing a Table for Your Data

| Table | Main use | What to check when choosing |
|---|---|---|
| TAG | Measurement histories organized by tag name and a time or distance axis | Whether queries focus on ranges and aggregates for specific tags. |
| LOG | Event and log histories with multiple attributes | Whether you continuously add records and read them using time or search conditions. |
| LOOKUP | Persistent reference data, such as equipment codes and mappings | The size and update pattern of the reference data loaded into memory. |
| TRANSACTION | Business data requiring row-level changes and transactions | Whether you need relational DML and transactions in Standard Edition. |
| VOLATILE | Shared state that can be recreated after a restart | Whether you can rebuild the data when it is lost at server shutdown. |

In Machbase DBMS 8.7.0, explicitly use `CREATE LOG TABLE` to create a LOG table. A bare
`CREATE TABLE` creates a TRANSACTION table, which is supported in Standard Edition.

An industry label alone does not determine the table type. For the final choice, including
update, join, and retention requirements, see
[Table Type Selection](/dbms/data-modeling-table-design/table-types-selection-type/).

Next, store one event and read it back in [10-Minute Quick Start](../quick-start/).
