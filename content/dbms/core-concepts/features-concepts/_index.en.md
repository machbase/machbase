---
type: docs
title: '2.3 Feature Concepts and Distinctions'
weight: 30
toc: true
aliases:
  - /dbms/core-concepts/terminology-distinction/
---

This section explains the roles and selection criteria of ROLLUP, Retention Policy, Backup,
Restore, and Mount for long-term data management in Machbase DBMS. Their detailed documents
provide creation syntax and operational procedures.

Raw data lets you reexamine individual events or measurements. Aggregates summarize many raw
records for recurring queries. Retention policies determine what to delete and when, while
backups provide material for recovery after a failure. Distinguishing these purposes helps
avoid deleting necessary raw data merely because aggregates exist, or omitting backups because
replication is configured.

- **[The Role of ROLLUP Statistics](#role-statistics-rollup)** — Reduce the cost of recurring
  aggregate queries.
- **[The Role of Retention Policy](#role-retention-policy)** — Automatically remove data based
  on its age.
- **[Backup, Restore, and Mount](#concepts-backup-restore-mount)** — Distinguish data protection,
  recovery, and inspection.

<a id="role-statistics-rollup"></a>

## The Role of ROLLUP Statistics

Repeatedly aggregating long TAG histories from raw rows becomes more expensive as the query
range grows. ROLLUP aggregates specified numeric columns and other supported values from
time-axis TAG data into intervals for recurring queries. Its definition determines the columns
and aggregation methods.

Default ROLLUP creates second (SEC), minute (MIN), and hour (HOUR) levels. Specify `WITH ROLLUP`
when creating a table, or use ordinary `CREATE ROLLUP` to select intervals and conditions.
Manage these objects through the public ROLLUP SQL rather than depending on generated object
names or internal storage structures.

### Selection Criteria

| Query pattern | Starting point |
|---|---|
| Repeated minute or hourly statistics over long periods | Consider default ROLLUP |
| Explicit aggregation intervals or filter conditions | Consider ordinary ROLLUP with the required interval and conditions |
| Store the results of your own aggregate SELECT in a separate TAG table | Consider Custom ROLLUP in Standard Edition |
| First or last values are needed | Consider extended ROLLUP |
| Most queries read raw values, or aggregates are rarely queried | Start without ROLLUP and measure execution time |

ROLLUP is not a retention policy that replaces raw data. Design raw-data retention separately
using Retention Policy, and check whether the relevant ROLLUP range must be rebuilt after
correcting TAG data.

### Interpreting Aggregates

Aggregation reduces detail. Keeping only a one-minute average cannot recover a brief anomaly
or the order of individual measurements within that minute. Keeping minima and maxima also
preserves the range, but still does not preserve every detail of the raw data.

Averaging averages from several intervals can differ from the overall average. For example,
if two observations average 10 and eight observations average 20, the overall average is
`(2 × 10 + 8 × 20) / 10 = 18`, not the unweighted average of 15. Use the necessary statistics,
such as sums and valid counts, when aggregating again, and follow the supported ROLLUP query
functions.

ROLLUP processing takes place separately from raw-data ingestion, so the newest raw rows and
their aggregates may become available at different times. For late arrivals or corrected
values, check the raw range, aggregation progress, and whether rebuilding is necessary.

See [TAG ROLLUP](/dbms/tag-rollup-usage/) for detailed creation syntax, query functions, and
rebuilding procedures.

<a id="role-retention-policy"></a>
<a id="retention-vs-delete-truncate"></a>

## The Role of Retention Policy

Retention Policy periodically removes LOG or TAG data past its retention period. It manages
storage for continuously growing tables without requiring operators to repeat deletion
commands manually.

| Requirement | Method |
|---|---|
| Continuously remove data older than a defined period | Retention Policy |
| Immediately remove a specific range of incorrect input | `DELETE`, within the table type's supported conditions |
| Empty all data from a supported table | `TRUNCATE TABLE` |

Attaching a retention policy does not mean all old data disappears immediately. Check the
execution interval, supported table types, and actual deletion state. Manage the lifecycle
of LOOKUP, VOLATILE, and TRANSACTION data using the explicit DML supported by those tables.

Retention and ingestion volume together determine storage needs. Multiplying rows per second
by the retention period in seconds estimates the raw row count, but actual disk use also
depends on data types, compression, indexes, replication, and backups. Before deleting raw
data, check aggregate coverage and retention, and the detail needed for auditing or reanalysis.
Creating ROLLUP does not automatically change raw-data retention.

See [Data Retention Policy](/dbms/operations-configuration-recovery/policy-data-retention/) for
creation, attachment, detachment, and operational checks.

<a id="concepts-backup-restore-mount"></a>
<a id="backup-vs-restore-mount"></a>

## Backup, Restore, and Mount

All three work with backup data, but their outcomes differ.

| Feature | Purpose | Production server | Result |
|---|---|---|---|
| Backup | Create a copy for recovery | Can run while the server is running | A backup in a separate location |
| Instance Restore | Recover an instance from a backup | Requires an offline procedure | The production database is recovered |
| Mount | Inspect a backup read-only | Can run while the server is running | The backup is queryable under a separate name |

Separately, `RESTORE DATABASE` SQL restores a logical database on a running server.
Distinguish its target and procedure from offline instance restoration.

A successful Backup does not by itself validate the recovery procedure. On a supporting
Edition, inspect the contents with Mount or test Restore in an isolated environment. Also
manage backup-path permissions and retention. Mount does not restore data into the production
database, and mounted data cannot be written. Restore and Mount are Standard Edition features;
in Cluster, follow that Edition's backup and failure-recovery procedures.

Define a recovery point objective (RPO), the acceptable window of data loss, and a recovery
time objective (RTO), the time allowed to restore service. RPO guides review of backup and
replication intervals; RTO guides review of the data to recover and the measured restoration
time. An Edition or backup schedule alone does not guarantee either objective. An incorrect
deletion can also reach replicas, so distinguish replication from backups.

See [Backup, Restore, and Mount](/dbms/operations-configuration-recovery/backup-restore-mount/)
for commands, permissions, Edition support, and recovery sequences. If you operate several
logical databases, also see
[Multi-Database Operations](/dbms/operations-configuration-recovery/multi-database/).

<a id="machloader-vs-csvimport-csvexport-tagmetaimport"></a>
<a id="load-data-infile-vs-machloader"></a>
<a id="ingestion-sdk-append-vs-sql-collector"></a>

## Comparing Input Paths

Consider `INSERT` for small SQL exercises, a supported SDK's Append API for continuous
application ingestion, and tools such as `machloader` for file loading. Supported tables,
input formats, and failure checks differ by tool, so similar names do not make them
interchangeable.

For selection criteria covering SQL, SDKs, file-loading tools, and Collector, see
[Data Input and Export](/dbms/development-tools-integration/data-input-load-export/#machloader-vs-csvimport-csvexport-tagmetaimport).
