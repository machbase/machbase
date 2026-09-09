---
type: docs
title: '11.10 Data Ingestion and Export'
weight: 100
toc: true
aliases:
  - /dbms/application-integration/data-input-load-export/
---

Choose SQL, Append APIs, or file tools according to data volume and operational needs.
This page covers selection and verification; see tool and SQL references for full options.

<a id="selection-input-method"></a>

## Choose an Input Method

<a id="selection-input-method-table-types-type"></a>

| Method | Suitable for | Main checks |
|------|-------------|-------------|
| Single INSERT | Small inputs, immediate error checks | Affected rows, generated ID |
| Prepared batch | Repeated execution of one SQL statement | Per-item results, failure position |
| Append API | Continuous bulk TAG/LOG collection | Server responses, success/failure counts |
| `LOAD DATA INFILE` | Loading server-accessible files | Server file permissions, input count |
| `machloader`/`csvimport` | Loading client files | Logs, error-row files, input/failure counts |

<a id="machloader-vs-csvimport-csvexport-tagmetaimport"></a>
<a id="load-data-infile-vs-machloader"></a>

### Compare Paths and Tools

| Path/tool | Execution location and purpose |
|---|---|
| SDK Append | Application continuously sends multiple TAG/LOG rows |
| SQL INSERT | Small inputs and ordinary SQL integration |
| `LOAD DATA INFILE` | SQL loads a file accessible to the server |
| `machloader` | Detailed control of client file mapping, logs, and error-row files |
| `csvimport`/`csvexport` | Simple CSV input/output wrappers |
| `tagmetaimport` | Bulk registration and updates of TAG metadata |

`tagmetaimport` does not ingest TAG measurements. See
[Command-Line Tools](/dbms/reference/command-line-tools/) for exact options.

<a id="selection-input-method-selection-input-method-guide"></a>

Use TAG or LOG for time-series/events requiring preservation of original data. Use
TRANSACTION for relational changes, LOOKUP for small reference data, and VOLATILE
for rebuildable in-memory caches. After choosing a table, select the input method
based on expected counts, latency tolerance, retry scope, and duplicate policy.

<a id="sql"></a>
<a id="insert"></a>
<a id="sql-insert"></a>

## SQL INSERT

Run this example in order, from creation through cleanup:

```sql
CREATE LOG TABLE integration_insert_demo (
    event_time DATETIME,
    sensor_id  VARCHAR(32),
    value      DOUBLE
);

INSERT INTO integration_insert_demo
VALUES (TO_DATE('2026-01-01 00:00:00'), 'TEMP-01', 25.3);

SELECT sensor_id, value
FROM integration_insert_demo;

DROP TABLE integration_insert_demo;
```

In applications, bind values as prepared parameters and check returned affected-row counts.

<a id="append"></a>
<a id="sql-append"></a>

## Append API

Append opens a table through an SDK-specific API, sends multiple rows, then flushes
and closes. Match column order and types to the schema, and use a separate connection
from ordinary queries. See SDK pages for complete language-specific examples.

Machbase DBMS 8.7.0 can select input columns or `ARRAY` elements at Append Open. Use
SDK sparse ARRAY objects when positions vary by row. See
[Sparse ARRAY and Selected-Column Append API](array-append/) for selection criteria,
APIs, and validation examples.

<a id="load-data-infile"></a>
<a id="sql-load-data-infile"></a>

## LOAD DATA INFILE

`LOAD DATA INFILE` loads server-accessible files through SQL. Paths are interpreted
from the server process, so check:

- The file exists on the server host.
- The server process account can read it.
- Delimiters, quoting, encoding, and date format match the source.
- Log/error-row file locations are defined for identifying failed rows.

See [LOAD DATA INFILE](/dbms/reference/sql/syntax/load-data-infile-syntax/) for syntax
and supported options.

<a id="file"></a>
<a id="file-csv"></a>
<a id="file-file-csv"></a>

## Prepare CSV Files

Decide whether the first row is a header, and keep column count and order consistent.
Test NULLs, empty strings, strings with delimiters, line breaks, and DATETIME formats
using sample files. Validate schemas and conversion rules on a small sample before
loading a large file.

<a id="import-machloader"></a>
<a id="file-import-machloader"></a>

## Import with machloader

Basic syntax:

```bash
"$MACHBASE_HOME/bin/machloader"   -s 127.0.0.1 -P 5656   -u APP_USER -p "$MACH_SAMPLE_PASSWORD"   -i -t SENSOR_LOG -d /data/sensor.csv   -l /data/sensor.log -b /data/sensor.bad
```

Use `-H` for headers, `-D` for a non-comma delimiter, and `-F` for a different date
format. See [machloader](/dbms/reference/command-line-tools/machloader/) for all options.

<a id="import-csvimport"></a>
<a id="file-import-csvimport"></a>

## Import with csvimport

`csvimport` simplifies commonly used machloader CSV options.

```bash
"$MACHBASE_HOME/bin/csvimport"   -s 127.0.0.1 -P 5656   -u APP_USER -p "$MACH_SAMPLE_PASSWORD"   -t SENSOR_LOG -d /data/sensor.csv -H   -l /data/sensor.log -b /data/sensor.bad
```

Automatic creation with `-C` may not assign the intended business type to every
column. For production loads, create the table explicitly and verify its schema first.

<a id="export"></a>

## Choose an Export Method

| Method | Suitable for |
|------|-------------|
| `SAVE DATA INTO` | Create server files with SQL filters and selected columns |
| `machloader -o` | Table exports with detailed options |
| `csvexport` | Simple CSV export |
| SDK SELECT | Application transforms or transmits rows |

<a id="export-ownership"></a>
<a id="export-export-ownership"></a>

## File Ownership and Paths

`SAVE DATA INTO` paths and permissions are relative to the server process. Files from
machloader and csvexport use the OS account running the tool. Avoid relative paths,
and check overwrite policy and available disk space first.

<a id="export-sql-save-data-into"></a>
<a id="export-export-sql-save-data-into"></a>

## SAVE DATA INTO

Use this to export filtered SQL results. Before running against a production path,
verify file creation, encoding, and headers with small results in a separate test
location. See [SAVE DATA INTO](/dbms/reference/sql/syntax/save-data-into-syntax/) for full syntax.

<a id="export-machloader"></a>
<a id="export-export-machloader"></a>

## Export with machloader

```bash
"$MACHBASE_HOME/bin/machloader"   -s 127.0.0.1 -P 5656   -u APP_USER -p "$MACH_SAMPLE_PASSWORD"   -o -t SENSOR_LOG -d /data/sensor-export.csv -H   -l /data/sensor-export.log
```

<a id="export-csvexport"></a>
<a id="export-export-csvexport"></a>

## Export with csvexport

```bash
"$MACHBASE_HOME/bin/csvexport"   -s 127.0.0.1 -P 5656   -u APP_USER -p "$MACH_SAMPLE_PASSWORD"   -t SENSOR_LOG -d /data/sensor-export.csv -H   -l /data/sensor-export.log
```

<a id="error-handling"></a>
<a id="batch"></a>
<a id="error-handling-batch"></a>

## Batch Processing

- Load-test batch sizes against row size and latency requirements.
- Record each batch's source offset and successful target count.
- On partial failure, isolate and retry failed rows instead of the whole batch.
- Define business keys and duplicate policies for safe row retransmission.

<a id="error-handling-bulk"></a>
<a id="error-handling-error-handling-bulk"></a>

## Handle Bulk Ingestion Errors

1. Check the tool exit code and summary counts.
2. Find the server error code and first failure cause in logs.
3. Compare error-row column counts, types, NULLs, date formats, and encoding with the source.
4. Retest a small corrected file, then reload only failed rows.
5. Verify final table counts, time ranges, and sample rows.

Logs and error-row files may contain credentials or raw sensitive data. Set access
permissions and retention periods.
