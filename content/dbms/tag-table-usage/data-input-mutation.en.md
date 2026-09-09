---
type: docs
title: '5.4 Data Ingestion and Changes'
weight: 40
toc: true
---
Ingest TAG data with SQL `INSERT`, Append APIs, or file-loading tools. Use SQL examples
to check features and load small amounts; consider Append APIs first for continuous collection.

<a id="original-85-inserting-data"></a>

## SQL INSERT

This example creates time-axis and distance-axis TAG tables, verifies data,
and cleans up. Ensure exercise names do not conflict with existing tables.
Time-axis names identify sensors; distance-axis names identify inspection
subjects or runs.

```sql
CREATE TAG TABLE ch5_input_time (
    name  VARCHAR(32) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE
);

INSERT INTO ch5_input_time
VALUES ('TEMP_001', TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 25.5);
INSERT INTO ch5_input_time
VALUES ('TEMP_001', TO_DATE('2026-01-01 10:01:00', 'YYYY-MM-DD HH24:MI:SS'), 25.7);

CREATE TAG TABLE ch5_input_distance (
    name     VARCHAR(32) PRIMARY KEY,
    distance DOUBLE BASEDISTANCE,
    value    DOUBLE,
    quality  INTEGER
);

INSERT INTO ch5_input_distance VALUES ('PIPE_A', 0.0, 10.1, 100);
INSERT INTO ch5_input_distance VALUES ('PIPE_A', 500.5, 11.2, 100);

EXEC TABLE_FLUSH(ch5_input_time);
EXEC TABLE_FLUSH(ch5_input_distance);

SELECT name, time, value FROM ch5_input_time ORDER BY time;
SELECT name, distance, value, quality
  FROM ch5_input_distance
 ORDER BY distance;

SELECT COUNT(*) FROM ch5_input_time;
SELECT COUNT(*) FROM ch5_input_distance;

DROP TABLE ch5_input_distance;
DROP TABLE ch5_input_time;
```

Each table returns two rows. Time-axis values are 25.5 and 25.7; distance-axis
positions are 0.0 and 500.5. Tags were not preregistered, so the first DATA
input registers each name automatically. The application manages actual event
times and retransmission status.

Use `TABLE_FLUSH` in validation or operational procedures that explicitly need
to flush pending storage/input buffers. It is not a transaction commit or a
query-visibility guarantee. Do not execute it per row in ordinary collection
loops. See the [EXEC Procedure Reference](/dbms/reference/sql/syntax/execute-procedure-syntax/#table-flush)
for arguments and errors.

## Ingest with Metadata

A TAG table with user metadata can automatically register new tags through
DATA-only input. If attributes such as location and units must be set first,
register with `INSERT ... METADATA` before DATA input. Supported syntax can
also send DATA and metadata together. Do not assume ordinary DATA input
updates existing attributes every time. Omit system-managed columns from input lists.

See [TAG Metadata](../tag-metadata/) for metadata registration, updates, and deletion.

## Choose an Input Path

| Path | Suitable for | Checks |
| --- | --- | --- |
| SQL `INSERT` | Feature checks, low-frequency input | Per-statement parsing and round-trip cost |
| SDK Append | Continuous high-throughput input | Batch size, flush, error handling |
| `csvimport` / `machloader` | Bulk client-file loads | Column order, date format, bad files |
| `LOAD DATA INFILE` | Server-accessible files | Server paths/permissions, error policy |

See [Development Integration](/dbms/development-tools-integration/) for SDK
connections and Append examples, and
[Data Ingestion and Export](/dbms/development-tools-integration/data-input-load-export/)
for file formats and commands.

## Correct Data

TAG data UPDATE in Standard Edition requires both tag selection and BASETIME
ranges. Tag names, axes, and metadata columns are not ordinary data UPDATE
targets. Existing ROLLUP results do not change automatically after correction;
rebuild the affected range explicitly. See [ROLLUP_REBUILD](../../tag-rollup-usage/rollup-rebuild/).

Check success responses, failure counts, and retry policies in the selected
API. Distinguish SQL NULL, SDK NULL representations, and numeric 0, and define
a duplicate policy for retransmitting observations. For numeric ARRAY and
sparse input, use the
[ARRAY Append Examples](../../development-tools-integration/data-input-load-export/array-append/).

See [TAG Data Correction](../tag-data-update-correction/) for detailed procedures.
