---
title: '5.4 Data Input and Mutation'
weight: 40
toc: true
---

Use SQL INSERT for small functional checks, supported SDK Append for continuous ingestion, and
file tools for bulk input. A successful API call, storage flush, and completed index/statistics
processing represent different stages.

<a id="original-85-inserting-data"></a>

## SQL Input

Create these independent fixtures in an unused namespace. Names identify a sensor in the time
example and one inspection subject/run in the distance example.

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


Both tables contain two rows before cleanup. Time values are 25.5 and 25.7; distances are 0.0 and
500.5. No metadata was preregistered, so the first DATA input automatically creates each tag.

TABLE_FLUSH explicitly processes pending storage/input buffers. It is not a transaction commit or
a general query-visibility guarantee, and should not run once per input row in a collection loop.
See [EXEC Procedures](../../reference/sql/syntax-dictionary-sql/execute-procedure-syntax/#table-flush).

## Input with Metadata

DATA-only input can automatically register tags even when user metadata columns exist. If location
and units must be defined first, insert METADATA before observations. Supported input forms can
also supply data and metadata together. Do not assume ordinary DATA input continually updates
existing attributes. Keep system-managed columns out of input lists.

See [TAG Metadata](../tag-metadata/) for registration, updates, and deletion.

## Choose an Input Path

| Path | Use | Check |
|---|---|---|
| SQL INSERT | Low-frequency input and exercises | Per-statement processing and round trips |
| SDK Append | Continuous collection | Batching, completion, and failure counts |
| csvimport / machloader | Client-side files | Column order, date formats, and bad files |
| LOAD DATA INFILE | Server-accessible files | Server paths, permissions, and errors |

See [SDK Guides](../../development-tools-integration/) and
[Input and Export](../../development-tools-integration/data-input-load-export/).
Distinguish SQL/SDK NULL from numeric zero and define retries and duplicate handling.
[ARRAY Append (Korean)](/kr/dbms/development-tools-integration/data-input-load-export/array-append/) covers
dense and sparse values.

## Corrections

TAG DATA UPDATE requires Standard Edition and tag plus BASETIME conditions. The tag name, axis,
and metadata columns are not ordinary DATA SET targets. Rebuild affected ROLLUP ranges when
aggregate queries must reflect corrections. See [Data Corrections](../tag-data-update-correction/).
