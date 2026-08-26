---
type: docs
title: '11.10 Data Input and Export'
weight: 100
toc: true
aliases:
  - /dbms/application-integration/data-input-load-export/
---

Choose SQL, an Append API, or a file tool according to data volume and operational requirements.
Use the linked SQL and tool references for the complete option set.

<a id="selection-input-method"></a>
<a id="selection-input-method-table-types-type"></a>

## Choose an input method

| Method | Suitable workload | Verify |
|---|---|---|
| Single INSERT | Low volume and immediate error handling | Affected rows and generated ID |
| Prepared batch | Repeated execution of the same SQL | Per-item result and failure position |
| Append API | Continuous high-volume TAG or LOG input | Ack and success/failure counts |
| `LOAD DATA INFILE` | A file readable by the server | Server permissions and input count |
| `machloader` or `csvimport` | A client-side file | Log, bad file, input and failure counts |

<a id="machloader-vs-csvimport-csvexport-tagmetaimport"></a>
<a id="load-data-infile-vs-machloader"></a>
<a id="ingestion-sdk-append-vs-sql-collector"></a>

### Compare paths and tools

| Path or tool | Primary use |
|---|---|
| SDK Append | Continuous multi-row TAG or LOG input from an application |
| SQL INSERT | Low-volume input and general SQL integration |
| `LOAD DATA INFILE` | A file readable by the server process |
| `machloader` | Client files with explicit mapping, logs, and bad rows |
| `csvimport` and `csvexport` | Simple CSV wrappers |
| `tagmetaimport` | Bulk TAG metadata registration and changes |
| Collector | Repeated FILE or SFTP source collection |

Choose the table type first: TAG or LOG for retained time-series and event data, TRANSACTION for
relational changes, LOOKUP for small reference data, and VOLATILE for rebuildable in-memory data.
Then choose the input path based on volume, latency, retry unit, and duplicate policy.

<a id="sql"></a>
<a id="insert"></a>
<a id="sql-insert"></a>

## SQL INSERT

The following example can be run from creation through cleanup.

```sql
CREATE LOG TABLE integration_insert_demo (
    event_time DATETIME,
    sensor_id  VARCHAR(32),
    value      DOUBLE
);

INSERT INTO integration_insert_demo
VALUES (TO_DATE('2026-01-01 00:00:00'), 'TEMP-01', 25.3);

SELECT sensor_id, value FROM integration_insert_demo;
DROP TABLE integration_insert_demo;
```

Bind application values as prepared parameters and check the returned affected-row count.

<a id="append"></a>
<a id="sql-append"></a>

## Append API

Append opens a table through the selected SDK, sends multiple rows, then flushes and closes the
handle. Match column order and types to the schema, and keep query and Append connections separate.
Use the SDK pages in this chapter for complete code.

<a id="load-data-infile"></a>
<a id="sql-load-data-infile"></a>

## LOAD DATA INFILE

`LOAD DATA INFILE` reads a path from the server process. Confirm that the file exists on the server,
the server account can read it, format options match the source, and failed rows have a log and bad
file. See [LOAD DATA INFILE](../../reference/sql/syntax-dictionary-sql/load-data-infile-syntax/).

<a id="file"></a>
<a id="file-csv"></a>
<a id="file-file-csv"></a>

## Prepare CSV files

Keep a consistent column count and order. Test headers, NULL and empty values, quoted delimiters,
line breaks, encoding, and DATETIME formats with a small sample before loading the full file.

<a id="import-machloader"></a>
<a id="file-import-machloader"></a>

## Import with machloader

```bash
"$MACHBASE_HOME/bin/machloader" \
  -s 127.0.0.1 -P 5656 -u APP_USER -p "$MACH_SAMPLE_PASSWORD" \
  -i -t SENSOR_LOG -d /data/sensor.csv \
  -l /data/sensor.log -b /data/sensor.bad
```

Use `-H` for a header, `-D` for a non-comma delimiter, and `-F` for a different date format. See
[machloader](../../reference/command-line-tools/dictionary-machloader/) for all options.

<a id="import-csvimport"></a>
<a id="file-import-csvimport"></a>

## Import with csvimport

```bash
"$MACHBASE_HOME/bin/csvimport" \
  -s 127.0.0.1 -P 5656 -u APP_USER -p "$MACH_SAMPLE_PASSWORD" \
  -t SENSOR_LOG -d /data/sensor.csv -H \
  -l /data/sensor.log -b /data/sensor.bad
```

Automatic table creation with `-C` may not select the intended business types. Create and verify the
production schema explicitly before importing.

<a id="export"></a>

## Choose an export method

| Method | Suitable workload |
|---|---|
| `SAVE DATA INTO` | Produce a server-side file from a SQL projection and condition |
| `machloader -o` | Table export with detailed options |
| `csvexport` | Simple CSV export |
| SDK SELECT | Transform or stream rows in an application |

`SAVE DATA INTO` paths use the server process's filesystem and permissions. machloader and
csvexport paths use the account running the tool. Prefer absolute paths and check overwrite policy
and disk capacity first.

<a id="export-sql-save-data-into"></a>
<a id="export-export-sql-save-data-into"></a>

## SAVE DATA INTO

Validate file creation, encoding, and headers with a small result in a dedicated path. See
[SAVE DATA INTO](../../reference/sql/syntax-dictionary-sql/save-data-into-syntax/) for syntax.

<a id="export-machloader"></a>
<a id="export-export-machloader"></a>

## Export with machloader

```bash
"$MACHBASE_HOME/bin/machloader" \
  -s 127.0.0.1 -P 5656 -u APP_USER -p "$MACH_SAMPLE_PASSWORD" \
  -o -t SENSOR_LOG -d /data/sensor-export.csv -H \
  -l /data/sensor-export.log
```

<a id="export-csvexport"></a>
<a id="export-export-csvexport"></a>

## Export with csvexport

```bash
"$MACHBASE_HOME/bin/csvexport" \
  -s 127.0.0.1 -P 5656 -u APP_USER -p "$MACH_SAMPLE_PASSWORD" \
  -t SENSOR_LOG -d /data/sensor-export.csv -H \
  -l /data/sensor-export.log
```

<a id="error-handling"></a>
<a id="batch"></a>
<a id="error-handling-batch"></a>

## Batch and bulk errors

- Load-test batch size with representative row sizes and latency requirements.
- Record the source offset and target success count for each batch.
- Separate and retry failed rows instead of replaying an entire successful batch.
- Check tool exit status, summary counts, logs, and bad files.
- After retry, verify the final row count, time range, and representative rows.

Restrict access and retention for logs and bad files because they may contain credentials or source
data.
