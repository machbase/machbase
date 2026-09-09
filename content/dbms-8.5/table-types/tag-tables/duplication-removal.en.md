---
title: 'Automatic Duplicate Removal'
type: docs
weight: 90
---

## Overview

Machbase can automatically detect and remove duplicate sensor readings within a configurable time window, ensuring data quality without manual intervention.

## Configuring Duplicate Removal

When creating the TAG table, the duration for duplicate removal is passed as a table property. The maximum configurable duration for duplicate removal is 43200 minutes (30 days).

```sql
-- If the newly inserted data duplicates existing data within 1440 minutes(one day) from system time those data will be deleted.

CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED) TAG_DUPLICATE_CHECK_DURATION=1440;
```

The property of the duplication removal is shown in the table m$sys_table_property.
```sql
SELECT * FROM m$sys_table_property WHERE id={table_id} AND name = 'TAG_DUPLICATE_CHECK_DURATION';
```

Data insert/select example - duplication removal duration is 1440 minutes(one day)
```sql
-- Use a timestamp inside the duplicate-check window relative to the server clock.
-- DATE_TRUNC('day', NOW) gives the same timestamp for repeated statements on the same day.

INSERT INTO tag VALUES('tag1', DATE_TRUNC('day', NOW), 0);
INSERT INTO tag VALUES('tag1', DATE_TRUNC('day', NOW), 0);

EXEC TABLE_FLUSH(tag);

SELECT * FROM tag WHERE name = 'tag1';
NAME                  TIME                            VALUE
--------------------------------------------------------------------------------------
tag1                  <current day> 00:00:00 000:000:000 0
  
```
## Changing configuration
TAG_DUPLICATE_CHECK_DURATION can be modified as shown below.

```sql
ALTER TABLE {table_name} set TAG_DUPLICATE_CHECK_DURATION={duration in minutes};
```

## Constraints of duplication removal

* The duplication removal setting can be configured on a minute basis, with a maximum limit of 43200 minutes (30 days).
* If the existing input data has already been deleted, any subsequent occurrence of the same data will not be considered as a duplicate for the purpose of duplication removal.

## Checking duplicates via TRACE log
Adding 32(SM_2) to TRACE_LOG_LEVEL outputs deduplication logs.
```sql
-- Check current setting
select name, value from v$property where name = 'TRACE_LOG_LEVEL';

-- Change setting
alter system set TRACE_LOG_LEVEL={current_value + 32};
```

**Configuration Example**
```sql
-- Check current value
Mach> select name, value from v$property where name = 'TRACE_LOG_LEVEL';
name                                                          value
---------------------------------------------------------------------------------------------------------------------------------------------------
TRACE_LOG_LEVEL                                               277
[1] row(s) selected.

-- Add 32 (277 + 32 = 309)
Mach> alter system set TRACE_LOG_LEVEL=309;
Altered successfully.
```

- Log file location: `$MACHBASE_HOME/trc/machbase.trc`
- Quick filter:
  ```bash
  tail -n 50 $MACHBASE_HOME/trc/machbase.trc | grep DUP_DROP
  ```
- Log format: `DUP_DROP Table=<table> TAG=<tag id> TIME=<timestamp> COL<n>=<value> ...`
- Real sample (same TIME for TAG=1, different COL3 values):
  ```
  [2025-11-29 13:50:27 P-151395 T-126344581076672][SM-INFO] DUP_DROP Table=TAG TAG=1 TIME=1998-12-24 09:00:00 000:000:012  COL3=12.000000
  ...
  [2025-11-29 13:50:27 P-151395 T-126344581076672][SM-INFO] DUP_DROP Table=TAG TAG=1 TIME=1998-12-24 09:00:00 000:000:048  COL3=48.000000
  ```
- How to use it
  - Check the TIME field to see which duplicates were dropped at the same timestamp.
  - Add `grep "Table=TAG"` or `grep "TAG=1"` for faster narrowing to a specific table/tag.
- Note: Each line is capped at ~4KB; with very many columns the tail may be truncated, but it won’t crash.
