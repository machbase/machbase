---
title : Delete tag data
type: docs
weight: 30
---

## Tag data deletion constraints

Machbase only supports deletion of data before a specific time.

Unsupported tag data deletion condition

* Delete data for a specific time range

Supported tag data deletion condition

* Delete specific tag data
* Delete data before a specific time for a specific tag
* Delete specific time range data for a specific tag
* Delete all tags before a specific time
* Delete all data

## Execute the DELETE statement

### Delete specific tag data

When a specific tag is specified, all data associated with that tag is deleted.

```sql
DELETE FROM TAG WHERE NAME = 'TAG-ID';
```

```sql
## Original Data
Mach> select * from tag;
NAME                  TIME                            VALUE
--------------------------------------------------------------------------------------
TAG_0001              2024-01-01 10:00:00 000:000:000 1
TAG_0001              2024-01-01 10:00:01 000:000:000 1
TAG_0001              2024-01-01 10:00:04 000:000:000 1
TAG_0001              2024-01-01 10:00:06 000:000:000 1
TAG_0001              2024-01-01 10:00:09 000:000:000 1
TAG_0001              2024-01-01 10:00:10 000:000:000 1
TAG_0002              2024-01-01 10:00:02 000:000:000 1
TAG_0002              2024-01-01 10:00:03 000:000:000 1
TAG_0002              2024-01-01 10:00:05 000:000:000 1
TAG_0002              2024-01-01 10:00:07 000:000:000 1
TAG_0002              2024-01-01 10:00:08 000:000:000 1
[11] row(s) selected.

Mach> delete from tag where name = 'TAG_0002';
5 row(s) deleted.

Mach> select * from tag;
NAME                  TIME                            VALUE
--------------------------------------------------------------------------------------
TAG_0001              2024-01-01 10:00:00 000:000:000 1
TAG_0001              2024-01-01 10:00:01 000:000:000 1
TAG_0001              2024-01-01 10:00:04 000:000:000 1
TAG_0001              2024-01-01 10:00:06 000:000:000 1
TAG_0001              2024-01-01 10:00:09 000:000:000 1
TAG_0001              2024-01-01 10:00:10 000:000:000 1
[6] row(s) selected.
```


### Delete data before a specific time for a specific tag

When a specific tag and time are specified, data associated with that tag before the specified time is deleted.

```sql
DELETE FROM TAG WHERE NAME = 'TAG-ID' AND TIME <= 'Time-string';
```

```sql
## Original Data
Mach> select * from tag;
NAME                  TIME                            VALUE
--------------------------------------------------------------------------------------
TAG_0001              2024-01-01 10:00:00 000:000:000 1
TAG_0001              2024-01-01 10:00:01 000:000:000 1
TAG_0001              2024-01-01 10:00:04 000:000:000 1
TAG_0001              2024-01-01 10:00:06 000:000:000 1
TAG_0001              2024-01-01 10:00:09 000:000:000 1
TAG_0001              2024-01-01 10:00:10 000:000:000 1
TAG_0002              2024-01-01 10:00:02 000:000:000 1
TAG_0002              2024-01-01 10:00:03 000:000:000 1
TAG_0002              2024-01-01 10:00:05 000:000:000 1
TAG_0002              2024-01-01 10:00:07 000:000:000 1
TAG_0002              2024-01-01 10:00:08 000:000:000 1
[11] row(s) selected.

Mach> delete from tag where name = 'TAG_0002' and time <= '2024-01-01 10:00:05';
3 row(s) deleted.

Mach> select * from tag;
NAME                  TIME                            VALUE
--------------------------------------------------------------------------------------
TAG_0001              2024-01-01 10:00:00 000:000:000 1
TAG_0001              2024-01-01 10:00:01 000:000:000 1
TAG_0001              2024-01-01 10:00:04 000:000:000 1
TAG_0001              2024-01-01 10:00:06 000:000:000 1
TAG_0001              2024-01-01 10:00:09 000:000:000 1
TAG_0001              2024-01-01 10:00:10 000:000:000 1
TAG_0002              2024-01-01 10:00:07 000:000:000 1
TAG_0002              2024-01-01 10:00:08 000:000:000 1
[8] row(s) selected.
```


### Delete specific time range data for a specific tag

When a specific tag and time range are specified, data associated with that tag within the specified time range is deleted.

```sql
DELETE FROM TAG WHERE NAME = 'TAG-ID' AND TIME >= 'Time-string' AND TIME <= 'Time-string';
```

```sql
## Original Data
Mach> select * from tag;
NAME                  TIME                            VALUE
--------------------------------------------------------------------------------------
TAG_0001              2024-01-01 10:00:00 000:000:000 1
TAG_0001              2024-01-01 10:00:01 000:000:000 1
TAG_0001              2024-01-01 10:00:04 000:000:000 1
TAG_0001              2024-01-01 10:00:06 000:000:000 1
TAG_0001              2024-01-01 10:00:09 000:000:000 1
TAG_0001              2024-01-01 10:00:10 000:000:000 1
TAG_0002              2024-01-01 10:00:02 000:000:000 1
TAG_0002              2024-01-01 10:00:03 000:000:000 1
TAG_0002              2024-01-01 10:00:05 000:000:000 1
TAG_0002              2024-01-01 10:00:07 000:000:000 1
TAG_0002              2024-01-01 10:00:08 000:000:000 1
[11] row(s) selected.

Mach> delete from tag where name = 'TAG_0002' and time >= '2024-01-01 10:00:04' and time <= '2024-01-01 10:00:08';
3 row(s) deleted.

Mach> select * from tag;
NAME                  TIME                            VALUE
--------------------------------------------------------------------------------------
TAG_0001              2024-01-01 10:00:00 000:000:000 1
TAG_0001              2024-01-01 10:00:01 000:000:000 1
TAG_0001              2024-01-01 10:00:04 000:000:000 1
TAG_0001              2024-01-01 10:00:06 000:000:000 1
TAG_0001              2024-01-01 10:00:09 000:000:000 1
TAG_0001              2024-01-01 10:00:10 000:000:000 1
TAG_0002              2024-01-01 10:00:02 000:000:000 1
TAG_0002              2024-01-01 10:00:03 000:000:000 1
[8] row(s) selected.
```
### Delete all tags before a specific time

When a time is specified in the BEFORE clause, all tags before that time are deleted.

```sql
DELETE FROM TAG BEFORE TO_DATE('Time-string');
```

```bash
## Original Data
Mach> select * from tag;
NAME TIME VALUE
--------------------------------------------------------------------------------------
TAG_0001 2018-01-01 01:00:00 000:000:000 1
TAG_0001 2018-01-02 02:00:00 000:000:000 2
TAG_0001 2018-01-03 03:00:00 000:000:000 3
TAG_0001 2018-01-04 04:00:00 000:000:000 4
TAG_0001 2018-01-05 05:00:00 000:000:000 5
TAG_0001 2018-01-06 06:00:00 000:000:000 6
TAG_0001 2018-01-07 07:00:00 000:000:000 7
TAG_0001 2018-01-08 08:00:00 000:000:000 8
TAG_0001 2018-01-09 09:00:00 000:000:000 9
TAG_0001 2018-01-10 10:00:00 000:000:000 10
TAG_0002 2018-02-01 01:00:00 000:000:000 11
TAG_0002 2018-02-02 02:00:00 000:000:000 12
TAG_0002 2018-02-03 03:00:00 000:000:000 13
TAG_0002 2018-02-04 04:00:00 000:000:000 14
TAG_0002 2018-02-05 05:00:00 000:000:000 15
TAG_0002 2018-02-06 06:00:00 000:000:000 16
TAG_0002 2018-02-07 07:00:00 000:000:000 17
TAG_0002 2018-02-08 08:00:00 000:000:000 18
TAG_0002 2018-02-09 09:00:00 000:000:000 19
TAG_0002 2018-02-10 10:00:00 000:000:000 20
[20] row(s) selected.
 
Mach> delete from tag before to_date('2018-02-01');
10 row(s) deleted.
 
Mach> select * from tag;
NAME TIME VALUE
--------------------------------------------------------------------------------------
TAG_0002 2018-02-01 01:00:00 000:000:000 11
TAG_0002 2018-02-02 02:00:00 000:000:000 12
TAG_0002 2018-02-03 03:00:00 000:000:000 13
TAG_0002 2018-02-04 04:00:00 000:000:000 14
TAG_0002 2018-02-05 05:00:00 000:000:000 15
TAG_0002 2018-02-06 06:00:00 000:000:000 16
TAG_0002 2018-02-07 07:00:00 000:000:000 17
TAG_0002 2018-02-08 08:00:00 000:000:000 18
TAG_0002 2018-02-09 09:00:00 000:000:000 19
TAG_0002 2018-02-10 10:00:00 000:000:000 20
[10] row(s) selected.
```

### Delete all data

If there are no conditions, all data is deleted.

```bash
## Original Data
Mach> select * from tag;
NAME TIME VALUE
--------------------------------------------------------------------------------------
TAG_0001 2018-01-01 01:00:00 000:000:000 1
TAG_0001 2018-01-02 02:00:00 000:000:000 2
TAG_0001 2018-01-03 03:00:00 000:000:000 3
TAG_0001 2018-01-04 04:00:00 000:000:000 4
TAG_0001 2018-01-05 05:00:00 000:000:000 5
TAG_0001 2018-01-06 06:00:00 000:000:000 6
TAG_0001 2018-01-07 07:00:00 000:000:000 7
TAG_0001 2018-01-08 08:00:00 000:000:000 8
TAG_0001 2018-01-09 09:00:00 000:000:000 9
TAG_0001 2018-01-10 10:00:00 000:000:000 10
TAG_0002 2018-02-01 01:00:00 000:000:000 11
TAG_0002 2018-02-02 02:00:00 000:000:000 12
TAG_0002 2018-02-03 03:00:00 000:000:000 13
TAG_0002 2018-02-04 04:00:00 000:000:000 14
TAG_0002 2018-02-05 05:00:00 000:000:000 15
TAG_0002 2018-02-06 06:00:00 000:000:000 16
TAG_0002 2018-02-07 07:00:00 000:000:000 17
TAG_0002 2018-02-08 08:00:00 000:000:000 18
TAG_0002 2018-02-09 09:00:00 000:000:000 19
TAG_0002 2018-02-10 10:00:00 000:000:000 20
[20] row(s) selected.
 
Mach> delete from tag;
20 row(s) deleted.
 
Mach> select * from tag;
NAME TIME VALUE
--------------------------------------------------------------------------------------
[0] row(s) selected.
```


## Delete ROLLUP Data

Example of deleting rollup data

```sql
DELETE FROM TAG ROLLUP BEFORE TO_DATE('Time-string');
```

if you specify the time of the BEFORE statement, all rollup data before that time are deleted.

if you don't specify the  time of the BEFORE statement, all rollup data is deleted.

