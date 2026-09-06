---
type: docs
title: '17.4.5 tagmetaimport Command and Options'
weight: 50
toc: true
---

tagmetaimport imports CSV tag names and user metadata through machloader. It is not an automatic
update/upsert tool, and a file is not imported as one transaction.

## Target Selection

For logical TAG table sensor_tag, specify the metadata target _SENSOR_TAG_META with -t.
The wrapper forwards the target; -t sensor_tag does not automatically switch to metadata mode.
Use the storage name only for this tool argument. Perform SQL queries and changes using
sensor_tag METADATA. Specify the target instead of relying on the default.

## Options

```bash
tagmetaimport -h
```

| Option | Meaning |
|---|---|
| -s, --server=SERVER | Server address; default 127.0.0.1 |
| -P, --port=PORT | SQL port; default 5656 |
| -u, --user=USER | User; default SYS |
| -p, --password=PASSWORD | Password; use actual credentials |
| -t, --table=TABLE_NAME | Metadata target, such as _SENSOR_TAG_META |
| -d, --data=DATA_FILE | Input CSV path on the client |
| -l, --log=LOG_FILE | Import log |
| -b, --bad=BAD_FILE | Failed-row output |
| -H, --header | File includes a header row |
| -D, --delimiter=DELIMITER | Field delimiter; default comma |
| -E, --encoding=CHARSET | Input character set; default UTF-8 |
| -I, --silent | Reduced output |
| -h, --help | Help |

The wrapper also accepts machloader options. Do not treat modes that replace data as ordinary
retries; verify their deletion scope before use.

## Table and File Shape

```sql
CREATE TAG TABLE sensor_tag (
    name VARCHAR(64) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) METADATA (
    unit VARCHAR(32),
    location VARCHAR(128)
);
```

Save tag_meta.csv with the tag name and metadata declaration order:

```csv
name,unit,location
sensor_001,celsius,Building-A Floor-1
sensor_002,celsius,Building-A Floor-2
```

```bash
tagmetaimport -s 127.0.0.1 -P 5656 -u SYS -p MANAGER \
    -t _SENSOR_TAG_META -d tag_meta.csv -H -l import.log -b import.bad
```

Omit -H only when the file has no header. Header presence is not automatic column reordering.
For another delimiter or encoding, specify -D or -E according to the actual file.

## Results and Existing Tags

Verify the metadata, not the DATA row count:

```sql
SELECT name, unit, location, _last_update_time
  FROM sensor_tag METADATA ORDER BY name;
```

A duplicate tag is rejected by ordinary METADATA INSERT and counted as a failed row; it is not
silently updated. Check successful/failed counts and bad/log files before retrying.
A file containing both new and duplicate tags may partially succeed.

Existing attributes can be changed with explicit UPDATE or supported SQL UPSERT.
New rows and actual attribute changes receive server-managed timestamps; no-op updates preserve them.
Keep _ID and _LAST_UPDATE_TIME out of CSV and form inputs.

Small registrations can use SQL directly:

```sql
INSERT INTO sensor_tag METADATA (name, unit, location)
VALUES ('sensor_005', 'volt', 'Panel-Room');
```

See [Bulk Metadata Import](../../../tag-table-usage/tagmetaimport/) for a complete first-import,
duplicate-reimport, explicit-update, and cleanup exercise.
