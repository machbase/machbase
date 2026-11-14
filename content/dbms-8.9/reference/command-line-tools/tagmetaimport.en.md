---
type: docs
title: '16.4.5 tagmetaimport'
weight: 50
toc: true
---

`tagmetaimport` imports TAG table metadata in bulk from CSV. Use it to register large numbers of tag
names and metadata values. It does not automatically update existing tags or
apply the entire file as one transaction.

## Options

```bash
tagmetaimport -h
```

| Option | Description |
|------|------|
| `-s`, `--server=SERVER` | Server IP address (default: 127.0.0.1) |
| `-P`, `--port=PORT` | Server port (default: 5656) |
| `-u`, `--user=USER` | Username (default: SYS) |
| `-p`, `--password=PASSWORD` | User password (default: MANAGER) |
| `-t`, `--table=TABLE_NAME` | Target metadata storage table. For logical table sensor_tag, specify _SENSOR_TAG_META |
| `-d`, `--data=DATA_FILE` | Metadata CSV path |
| `-l`, `--log=LOG_FILE` | Log file path |
| `-b`, `--bad=BAD_FILE` | File for failed input records |
| `-H`, `--header` | Treat the first CSV row as a header |
| `-D`, `--delimiter=DELIMITER` | Field delimiter (default: `,`) |
| `-E`, `--encoding=CHARSET` | File encoding (default: UTF8) |
| `-I`, `--silent` | Reduce progress output. Check success/failure counts in the completion summary |
| `-h`, `--help` | Display options |

## Input File Format

Arrange CSV columns in the same order as the TAG table's metadata columns.

Example TAG table definition:

```sql
CREATE TAG TABLE sensor_tag (
    name   VARCHAR(64) PRIMARY KEY,
    time   DATETIME    BASETIME,
    value  DOUBLE      SUMMARIZED
) METADATA (
    unit   VARCHAR(32),
    location VARCHAR(128)
);
```

Metadata CSV for this table (`tag_meta.csv`):

```
name,unit,location
sensor_001,celsius,Building-A Floor-1
sensor_002,celsius,Building-A Floor-2
sensor_003,bar,Boiler-Room
sensor_004,rpm,Motor-Section
```

Data without a header:

```
sensor_001,celsius,Building-A Floor-1
sensor_002,celsius,Building-A Floor-2
```

## Examples

### Basic Import

```bash
tagmetaimport -s 127.0.0.1 -P 5656 -u SYS -p MANAGER \
    -t _SENSOR_TAG_META -d tag_meta.csv -H
```

### Importing CSV with a Header

```bash
tagmetaimport -s 127.0.0.1 -P 5656 -u SYS -p MANAGER \
    -t _SENSOR_TAG_META -d tag_meta.csv -H
```

### Importing to a Remote Server

```bash
tagmetaimport -s 192.168.0.10 -P 5656 -u SYS -p MANAGER \
    -t _SENSOR_TAG_META -d tag_meta.csv -H
```

### Tab-delimited Files

```bash
tagmetaimport -s 127.0.0.1 -P 5656 -u SYS -p MANAGER \
    -t _SENSOR_TAG_META -d tag_meta.tsv -D '\t' -H
```

### EUC-KR Files

```bash
tagmetaimport -s 127.0.0.1 -P 5656 -u SYS -p MANAGER \
    -t _SENSOR_TAG_META -d tag_meta_kr.csv -E MS949 -H
```

## Behavior

- `-t` does not automatically convert a logical TAG table to its METADATA target. For logical table sensor_tag,
  specify `_SENSOR_TAG_META`. Use this name only to select the tool's ingestion target.
- Existing tag names cause ordinary METADATA INSERT errors. Check failure counts and the bad/log files.
- This tool is efficient for adding metadata after data has already been ingested.
- For small amounts of metadata, use SQL INSERT or enter statements directly in `machsql`.

```sql
-- Insert metadata directly in machsql
INSERT INTO sensor_tag METADATA (name, unit, location)
VALUES ('sensor_005', 'volt', 'Panel-Room');
```

## Notes

- Create the TAG table before importing.
- CSV column order must match the TAG table's metadata column order.
- Exclude the `BASETIME` column (`time`) and `SUMMARIZED` column (`value`) from the metadata file.

Change existing values with `UPDATE sensor_tag METADATA ...` or an explicit SQL UPSERT.
For reproducible examples of new ingestion and duplicate ingestion failures, see
[Bulk Metadata Registration](../../../tag-table-usage/tagmetaimport/).
The server maintains `_LAST_UPDATE_TIME` when new metadata is inserted or values actually change.
