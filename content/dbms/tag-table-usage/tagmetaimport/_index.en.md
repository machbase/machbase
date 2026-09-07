---
title: '5.12 tagmetaimport and Metadata Bulk Import'
weight: 120
toc: true
---

<a id="metadata-import-tagmetaimport-tag"></a>

## Register Metadata with tagmetaimport

`tagmetaimport` imports tag names and user metadata from CSV. Distinguish the logical TAG name
used in SQL from the tool's `-t` target. The current wrapper forwards `-t` to machloader.
For logical table `ch5_meta_import`, the metadata target is `_CH5_META_IMPORT_META`.
Passing `-t ch5_meta_import` does not automatically select metadata.

Use that name for tool target selection. Query and mutate through `ch5_meta_import METADATA`;
this is not a procedure for modifying storage objects directly. Always specify `-t`.

## 1. Prepare the Table

Use an exercise database where the name is unused.

```sql
CREATE TAG TABLE ch5_meta_import (
    name VARCHAR(40) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE
) METADATA (
    location VARCHAR(40),
    status VARCHAR(20)
);
```

## 2. Prepare the CSV

Save the following as `ch5_metadata.csv` on the client.

```csv
name,location,status
TEMP_001,Building-A/F1,READY
TEMP_002,Building-A/F2,STOP
TEMP_003,Building-B/F3,READY
```

Values follow the tag name and METADATA declaration order. Exclude DATA time/value columns and
system columns `_ID` and `_LAST_UPDATE_TIME`. Use `-H` for a header; do not assume a header
automatically reorders arbitrary input columns.

## 3. Import and Verify

Adjust credentials and use the `MACHBASE_HOME` and library environment of the intended 8.7.0 package.

```bash
tagmetaimport -s 127.0.0.1 -P 5656 -u SYS -p MANAGER \
  -t _CH5_META_IMPORT_META -d ch5_metadata.csv -H \
  -l ch5_import.log -b ch5_import.bad
```

The first run should report 3 successful and 0 failed rows. Metadata returns three rows, while
the DATA count is 0: registering tags does not insert observations.

```sql
SELECT name, location, status, _last_update_time
  FROM ch5_meta_import METADATA ORDER BY name;
SELECT COUNT(*) FROM ch5_meta_import;
```

## 4. Existing Tags and Reimport

Reimport does not automatically update existing tags. The current path uses ordinary METADATA
INSERTs, so duplicates count as failed rows. The second run should report 0 successes and 3 failures
with existing attributes unchanged. Check counts and bad/log files, not just the process status.

A mixed valid/invalid file is not one atomic transaction. Inspect imported tags and fix only failed
rows for retry. Use explicit UPDATE or supported SQL UPSERT to change existing data.

```sql
UPDATE ch5_meta_import METADATA SET status = 'DONE' WHERE name = 'TEMP_001';
INSERT INTO ch5_meta_import METADATA VALUES ('TEMP_002', 'Building-C/F2', 'READY')
ON DUPLICATE KEY UPDATE;
SELECT name, location, status FROM ch5_meta_import METADATA ORDER BY name;
```

TEMP_001 changes to DONE; TEMP_002 changes to Building-C/F2 and READY. Actual changes refresh the
metadata timestamp, while no-op updates preserve it. This does not imply an automatic UPSERT option
in tagmetaimport.

## Cleanup and Related Documents

Remove this exercise table with `DROP TABLE ch5_meta_import;` after validation.
Retain CSV/log/bad files until recovery or retry is no longer needed.

See [Command Options](../../reference/command-line-tools/dictionary-tagmetaimport/) and
[TAG Metadata](../tag-metadata/).
