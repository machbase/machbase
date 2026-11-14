---
type: docs
title: '5.12 tagmetaimport and Bulk Metadata Registration'
weight: 120
toc: true
---

<a id="metadata-import-tagmetaimport-tag"></a>

## Register Metadata with tagmetaimport

`tagmetaimport` imports tag names and user metadata from CSV. Distinguish
the logical TAG name used in SQL from the `-t` input target. The current
wrapper passes `-t` to machloader. For logical table `ch5_meta_import`,
the metadata input target is `_CH5_META_IMPORT_META`. Do not assume
`-t ch5_meta_import` automatically selects METADATA.

Use that name only to specify the tool target. Use `ch5_meta_import METADATA`
for SQL queries/changes; do not extend this into direct modification of
internal storage objects. Specify `-t` instead of relying on a default.

## 1. Prepare the Table

Run this SQL in an exercise database without conflicting objects.

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

## 2. Prepare CSV

Save the following as `ch5_metadata.csv` on the client.

```csv
name,location,status
TEMP_001,Building-A/F1,READY
TEMP_002,Building-A/F2,STOP
TEMP_003,Building-B/F3,READY
```

After the tag name, list values in METADATA declaration order. Omit DATA
time/value and system columns `_ID`/`_LAST_UPDATE_TIME`. Use `-H` for a
header; do not assume headers automatically map arbitrary column orders.

## 3. Import and Verify

Adjust the address/account to the exercise server and run with the
`MACHBASE_HOME` and library environment of the installed 8.7.0 package.

```bash
tagmetaimport -s 127.0.0.1 -P 5656 -u SYS -p MANAGER \
  -t _CH5_META_IMPORT_META -d ch5_metadata.csv -H \
  -l ch5_import.log -b ch5_import.bad
```

Expect 3 successes and 0 failures on the first run. The METADATA query
below returns three rows and DATA COUNT is 0. Registering metadata is
separate from inserting measurements.

```sql
SELECT name, location, status, _last_update_time
  FROM ch5_meta_import METADATA ORDER BY name;
SELECT COUNT(*) FROM ch5_meta_import;
```

## 4. Existing Tags and Reruns

Reimporting the same file does not automatically update existing tags.
This path uses ordinary METADATA INSERT, so duplicate tags count as failed
rows. Expect 0 successes and 3 failures on the second run, with existing
attributes unchanged. Check success/failure counts and bad/log files,
not just exit status.

Do not assume a file containing valid new rows and invalid rows forms one
transaction. Check registered tags, correct failed rows, and reprocess only
those rows. Change existing attributes with explicit UPDATE or supported UPSERT.

```sql
UPDATE ch5_meta_import METADATA SET status = 'DONE' WHERE name = 'TEMP_001';
INSERT INTO ch5_meta_import METADATA VALUES ('TEMP_002', 'Building-C/F2', 'READY')
ON DUPLICATE KEY UPDATE;
SELECT name, location, status FROM ch5_meta_import METADATA ORDER BY name;
```

TEMP_001 changes to DONE; TEMP_002 changes to Building-C/F2 and READY.
Actual value changes update modification time; same-value no-ops preserve
it. Do not interpret this as an automatic UPSERT option in `tagmetaimport`.

## Cleanup and Related Documentation

After checking results, run `DROP TABLE ch5_meta_import;` to remove only
the exercise table. Remove CSV, log, and bad files after confirming they
are no longer needed for reprocessing.

See the [tagmetaimport Reference](../../reference/command-line-tools/tagmetaimport/)
for options and [TAG Metadata](../tag-metadata/) for SQL registration and change rules.
