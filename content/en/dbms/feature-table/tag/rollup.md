---
title : Creating and Selecting in Rollup Table
type: docs
weight: 40
---

## Creating Rollup Table

When user create tag table, Rollup does not created default, user must create by themselves. Syntax is as follow.

![create-rollup](../create-rollup.png)

* rollup name : rollup table's name (Can be freely created with string up to 40)
* source table name : Name of source table which rollup will aggregate data.
* *number sec/min/hour : time and time unit for aggregate
* src_table_column : rollup target data column name
    * Only numeric type columns are allowed
    * If the source table is a rollup table, it is ommited and automatically designated as the rollup target column of the source table
 * ex) 1 sec aggregate : 1 sec
   ex) 30 seconds aggregate : 30 sec
   ex) 1 minute aggregate : 1 min
   ex) 1 hour aggregate : 1 hour
* constraint
    * Source table for aggregation can specify only tag table or rollup table
    * Only one rollup table can be exist to source table for aggregation
    * If source table for aggregation is rollup table, time for rollup table must be bigger than time for source table. And it must be multiple.


Example for Creating rollup table

```bash
Mach> CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE, strvalue VARCHAR(20));
Executed successfully.
 
-- creating 1 second rollup for tag table
Mach> CREATE ROLLUP _tag_rollup_sec ON tag(value) INTERVAL 1 SEC;
  
-- creating 1 minute rollup for tag table
Mach> CREATE ROLLUP _tag_rollup_min ON tag(value) INTERVAL 1 MIN;
  
-- creating 1 hour rollup for tag table
Mach> CREATE ROLLUP _tag_rollup_hour ON tag(value) INTERVAL 1 HOUR;
  
-- creating 30 seconds rollup for tag table
Mach> CREATE ROLLUP _tag_rollup_30sec ON tag(value) INTERVAL 30 SEC;
  
-- creating 10 minutes rollup for roll up table above
Mach> CREATE ROLLUP _tag_rollup_10min ON _tag_rollup_30sec INTERVAL 10 MIN;
 
-- Error when creating rollup for non-numeric type columns
Mach> CREATE ROLLUP _tag_rollup_sec ON tag(strvalue) INTERVAL 1 SEC;
[ERR-02671: Invalid type for ROLLUP column (STRVALUE).]
```

### Automatically create a ROLLUP table

A roll-up table can be automatically generated using the keyword `with ROLLUP (time_unit)`

```sql
CREATE TAG TABLE tagtbl (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED) WITH ROLLUP (time_unit)
 
time_unit := {SEC|MIN|HOUR}
```

If the time_unit is not specified as below, it will proceed based on SEC.

```sql
CREATE TAG TABLE tagtbl (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED) WITH ROLLUP
```

The name of the automatically generated rollup is generated in the following format. (`tagtbl` contains tag table name.)
* _`tagtbl`_ROLLUP_SEC
* _`tagtbl`_ROLLUP_MIN
* _`tagtbl`_ROLLUP_HOUR

```sql
Mach> CREATE TAG TABLE tagtbl (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED) WITH ROLLUP (SEC)
 
Mach> SHOW TABLES;
USER_NAME             DB_NAME                                             TABLE_NAME                                          TABLE_TYPE 
-----------------------------------------------------------------------------------------------------------------------------------------------
SYS                   MACHBASEDB                                          TAGTBL                                              TAGDATA    
SYS                   MACHBASEDB                                          _TAGTBL_DATA_0                                      KEYVALUE   
SYS                   MACHBASEDB                                          _TAGTBL_DATA_1                                      KEYVALUE   
SYS                   MACHBASEDB                                          _TAGTBL_DATA_2                                      KEYVALUE   
SYS                   MACHBASEDB                                          _TAGTBL_DATA_3                                      KEYVALUE   
SYS                   MACHBASEDB                                          _TAGTBL_META                                        LOOKUP     
SYS                   MACHBASEDB                                          _TAGTBL_ROLLUP_HOUR                                 KEYVALUE   
SYS                   MACHBASEDB                                          _TAGTBL_ROLLUP_MIN                                  KEYVALUE   
SYS                   MACHBASEDB                                          _TAGTBL_ROLLUP_SEC                                  KEYVALUE   
[9] row(s) selected.
Elapsed time: 0.001
Mach>
```

The criteria entered in time_unit are viewed as the smallest criteria and even the upper time unit is automatically generated.

> When a rollup table name conflict occurs, all rollup table creation fails and only tag tables are generated.

## Start/Stop Rollup Table

When rollup is created, rollup thread is automatically started, and the user can start/stop rollup thread arbitrarily.

```sql
-- Start specific rollup
EXEC ROLLUP_START(rollup_name)
 
-- Stop specific rollup
EXEC ROLLUP_STOP(rollup_name)
```


## Collect Rollup Instantly

rollup basically aggregate data in set time unit.

* ex) If it is 1 hour rollup, it aggregate data once in hour and rest in rest time.
User can aggregate data in force.

```sql
-- Execute specific rollup flush immediately
EXEC ROLLUP_FORCE(rollup_name)
```


## Drop Rollup

Drop Rollup.

```sql
DROP ROLLUP rollup_name
```

* rollup_name : Name of rollup
* constraint: if there is an rollup table that reference rollup table that will be deleted as source tree, it will cause error. User must delete it in reverse order.

```bash
mach> create tag table tag (name varchar(20) primary key, time datetime basetime, value double summarized);
mach> create rollup _tag_rollup_1 on tag(value) interval 1 sec;
mach> create rollup _tag_rollup_2 on _tag_rollup_1 interval 1 min;
mach> create rollup _tag_rollup_3 on _tag_rollup_2 interval 1 hour;
  
When created as above, the reference order is as follows.
  
tag -> _tag_rollup_1 -> _tag_rollup_2 -> _tag_rollup_3
  
At this time, if you try to delete the tag table or rollup in the middle, an error occurs.
  
mach> drop rollup tag
> [ERR-02651: Dependent ROLLUP table exists.]
mach> drop rollup _tag_rollup_1
> [ERR-02651: Dependent ROLLUP table exists.]
  
User must delete them in the following order to delete them normally.
  
mach> drop rollup _tag_rollup_3;
mach> drop rollup _tag_rollup_2;
mach> drop rollup _tag_rollup_1;
mach> drop table tag;
```
### When deleting the TAG table, delete the ROLLUP table together
When deleting a tag table using the `CASCADE` keyword, you can also delete a roll-up table that is dependent on the tag table.
```sql
DROP TABLE TAG CASCADE;
```
```sql
Mach> SHOW TABLES;
USER_NAME             DB_NAME                                             TABLE_NAME                                          TABLE_TYPE 
-----------------------------------------------------------------------------------------------------------------------------------------------
SYS                   MACHBASEDB                                          TAGTBL                                              TAGDATA    
SYS                   MACHBASEDB                                          _TAGTBL_DATA_0                                      KEYVALUE   
SYS                   MACHBASEDB                                          _TAGTBL_DATA_1                                      KEYVALUE   
SYS                   MACHBASEDB                                          _TAGTBL_DATA_2                                      KEYVALUE   
SYS                   MACHBASEDB                                          _TAGTBL_DATA_3                                      KEYVALUE   
SYS                   MACHBASEDB                                          _TAGTBL_META                                        LOOKUP     
SYS                   MACHBASEDB                                          _TAGTBL_ROLLUP_HOUR                                 KEYVALUE   
SYS                   MACHBASEDB                                          _TAGTBL_ROLLUP_MIN                                  KEYVALUE   
SYS                   MACHBASEDB                                          _TAGTBL_ROLLUP_SEC                                  KEYVALUE   
[9] row(s) selected.
Elapsed time: 0.001
Mach>

Mach> DROP TABLE tagtbl CASCADE;
Dropped successfully.
 
Mach> show tables;
USER_NAME             DB_NAME                                             TABLE_NAME                                          TABLE_TYPE 
-----------------------------------------------------------------------------------------------------------------------------------------------
[0] row(s) selected.
```

## Syntax

```sql
SELECT TIME ROLLUP 3 SECOND, AVG(VALUE) FROM TAG WHERE ...;
```

As above, if the ROLLUP clause is appended after the Datetime type column specified as the BASETIME attribute, the rollup table is selected.

```sql
[BASETIME_COLUMN] ROLLUP [PERIOD] [TIME_UNIT]
```

* BASETIME_COLUMN : Datetime column of the TAG table specified by the BASETIME attribute
* PERIOD : DATE_TRUNC() can specify a range for each unit of time available. (see below)
* TIME_UNIT : Any time unit available in the DATE_TRUNC() function can be used. (see below)

Depending on the selection of TIME_UNIT, the searched rollup table is different.

|unit of time(Abbreviation)|range of time|rollup table|
|--|--|--|
|nanosecond (nsec)|1000000000 (1 sec)|SECOND|
|microsecond (usec)|60000000 (60 sec)|SECOND|
|milisecond (msec)|60000 (60 sec)|SECOND|
|second (sec)|86400 (1 day)|SECOND|
|minute (min)|1440 (1 day)|MINUTE|
|hour|24 (1 day)|HOUR|
|day|1|HOUR|
|month|1|HOUR|
|year|1|HOUR|

Since using the ROLLUP clause directly performs a rollup table lookup, to use an aggregate function, it has the following characteristics.

* **The aggregate function must be called on the numeric type column**. However, only the six aggregate functions (SUM, COUNT, MIN, MAX, AVG, SUMSQ) supported by the rollup table are supported.
* **GROUP BY must be done directly with the BASETIME column to be ROLLUP.**
    * You can use the ROLLUP clause with the same meaning as it is.
    * Alternatively, an alias may be attached to the ROLLUP clause, and the alias may be written in GROUP BY.

```sql
SELECT   time rollup 3 sec mtime, avg(value)
FROM     TAG
GROUP BY time rollup 3 sec mtime;
 
-- or
SELECT   time rollup 3 sec mtime, avg(value)
FROM     TAG
GROUP BY mtime;
```


## Data Sample

Below is sample data for rollup test.

```sql
create tag table TAG (name varchar(20) primary key, time datetime basetime, value double summarized);
 
insert into tag metadata values ('TAG_0001');
 
insert into tag values('TAG_0001', '2018-01-01 01:00:01 000:000:000', 1);
insert into tag values('TAG_0001', '2018-01-01 01:00:02 000:000:000', 2);
insert into tag values('TAG_0001', '2018-01-01 01:01:01 000:000:000', 3);
insert into tag values('TAG_0001', '2018-01-01 01:01:02 000:000:000', 4);
insert into tag values('TAG_0001', '2018-01-01 01:02:01 000:000:000', 5);
insert into tag values('TAG_0001', '2018-01-01 01:02:02 000:000:000', 6);
 
insert into tag values('TAG_0001', '2018-01-01 02:00:01 000:000:000', 1);
insert into tag values('TAG_0001', '2018-01-01 02:00:02 000:000:000', 2);
insert into tag values('TAG_0001', '2018-01-01 02:01:01 000:000:000', 3);
insert into tag values('TAG_0001', '2018-01-01 02:01:02 000:000:000', 4);
insert into tag values('TAG_0001', '2018-01-01 02:02:01 000:000:000', 5);
insert into tag values('TAG_0001', '2018-01-01 02:02:02 000:000:000', 6);
 
insert into tag values('TAG_0001', '2018-01-01 03:00:01 000:000:000', 1);
insert into tag values('TAG_0001', '2018-01-01 03:00:02 000:000:000', 2);
insert into tag values('TAG_0001', '2018-01-01 03:01:01 000:000:000', 3);
insert into tag values('TAG_0001', '2018-01-01 03:01:02 000:000:000', 4);
insert into tag values('TAG_0001', '2018-01-01 03:02:01 000:000:000', 5);
insert into tag values('TAG_0001', '2018-01-01 03:02:02 000:000:000', 6);
```

For one tag, different values ​​in seconds were input for 3 hours.



## Get ROLLUP AVG

Below is the case of getting average of seconds, minutes, hours of tag table.

```bash
Mach> SELECT time rollup 1 sec mtime, avg(value) FROM TAG WHERE name = 'TAG_0001' group by mtime order by mtime;
mtime                           avg(value)
---------------------------------------------------------------
2018-01-01 01:00:01 000:000:000 1
2018-01-01 01:00:02 000:000:000 2
2018-01-01 01:01:01 000:000:000 3
2018-01-01 01:01:02 000:000:000 4
2018-01-01 01:02:01 000:000:000 5
2018-01-01 01:02:02 000:000:000 6
2018-01-01 02:00:01 000:000:000 1
2018-01-01 02:00:02 000:000:000 2
2018-01-01 02:01:01 000:000:000 3
2018-01-01 02:01:02 000:000:000 4
2018-01-01 02:02:01 000:000:000 5
2018-01-01 02:02:02 000:000:000 6
2018-01-01 03:00:01 000:000:000 1
2018-01-01 03:00:02 000:000:000 2
2018-01-01 03:01:01 000:000:000 3
2018-01-01 03:01:02 000:000:000 4
2018-01-01 03:02:01 000:000:000 5
2018-01-01 03:02:02 000:000:000 6
[18] row(s) selected.
 
Mach> SELECT time rollup 1 min mtime, avg(value) FROM TAG WHERE name = 'TAG_0001' group by mtime order by mtime;
mtime                           avg(value)
---------------------------------------------------------------
2018-01-01 01:00:00 000:000:000 1.5
2018-01-01 01:01:00 000:000:000 3.5
2018-01-01 01:02:00 000:000:000 5.5
2018-01-01 02:00:00 000:000:000 1.5
2018-01-01 02:01:00 000:000:000 3.5
2018-01-01 02:02:00 000:000:000 5.5
2018-01-01 03:00:00 000:000:000 1.5
2018-01-01 03:01:00 000:000:000 3.5
2018-01-01 03:02:00 000:000:000 5.5
[9] row(s) selected.
 
Mach> SELECT time rollup 1 hour mtime, avg(value) FROM TAG WHERE name = 'TAG_0001' group by mtime order by mtime;
mtime                           avg(value)
---------------------------------------------------------------
2018-01-01 01:00:00 000:000:000 3.5
2018-01-01 02:00:00 000:000:000 3.5
2018-01-01 03:00:00 000:000:000 3.5
[3] row(s) selected.
```


## Get ROLLUP MIN/MAX Value

Below is the case of getting min/max value of seconds, minutes, hours of tag table. The difference between others, you can get minimum value and maximum value at the same time with just one query.

```bash
Mach> SELECT time rollup 1 hour mtime, min(value), max(value) FROM TAG WHERE name = 'TAG_0001' group by mtime order by mtime;
mtime                           min(value)                  max(value)
--------------------------------------------------------------------------------------------
2018-01-01 01:00:00 000:000:000 1                           6
2018-01-01 02:00:00 000:000:000 1                           6
2018-01-01 03:00:00 000:000:000 1                           6
[3] row(s) selected.
 
Mach> SELECT time rollup 1 min mtime, min(value), max(value) FROM TAG WHERE name = 'TAG_0001' group by mtime order by mtime;
mtime                           min(value)                  max(value)
--------------------------------------------------------------------------------------------
2018-01-01 01:00:00 000:000:000 1                           2
2018-01-01 01:01:00 000:000:000 3                           4
2018-01-01 01:02:00 000:000:000 5                           6
2018-01-01 02:00:00 000:000:000 1                           2
2018-01-01 02:01:00 000:000:000 3                           4
2018-01-01 02:02:00 000:000:000 5                           6
2018-01-01 03:00:00 000:000:000 1                           2
2018-01-01 03:01:00 000:000:000 3                           4
2018-01-01 03:02:00 000:000:000 5                           6
[9] row(s) selected.
```


## Get ROLLUP SUM/COUNT

Below is the case of getting sum/count value. Also you can get  sum value and count value at the same time with just one query.

```bash
Mach> SELECT time rollup 1 min  mtime, sum(value), count(value) FROM TAG WHERE name = 'TAG_0001' group by mtime order by mtime;
mtime                           sum(value)                  count(value)
-------------------------------------------------------------------------------------
2018-01-01 01:00:00 000:000:000 3                           2
2018-01-01 01:01:00 000:000:000 7                           2
2018-01-01 01:02:00 000:000:000 11                          2
2018-01-01 02:00:00 000:000:000 3                           2
2018-01-01 02:01:00 000:000:000 7                           2
2018-01-01 02:02:00 000:000:000 11                          2
2018-01-01 03:00:00 000:000:000 3                           2
2018-01-01 03:01:00 000:000:000 7                           2
2018-01-01 03:02:00 000:000:000 11                          2
[9] row(s) selected.
```


## Get ROLLUP Sum of Squares

Below is the case of getting sum of squares in rollup.

```bash
Mach> SELECT time ROLLUP 1 SEC mtime, SUMSQ(value) FROM tag GROUP BY mtime ORDER BY mtime;
mtime                           SUMSQ(value)               
---------------------------------------------------------------
2018-01-01 01:00:01 000:000:000 1                          
2018-01-01 01:00:02 000:000:000 4                          
2018-01-01 01:01:01 000:000:000 9                          
2018-01-01 01:01:02 000:000:000 16                         
2018-01-01 01:02:01 000:000:000 25                         
2018-01-01 01:02:02 000:000:000 36                         
2018-01-01 02:00:01 000:000:000 1                          
2018-01-01 02:00:02 000:000:000 4                          
2018-01-01 02:01:01 000:000:000 9                          
2018-01-01 02:01:02 000:000:000 16                         
2018-01-01 02:02:01 000:000:000 25                         
2018-01-01 02:02:02 000:000:000 36                         
2018-01-01 03:00:01 000:000:000 1                          
2018-01-01 03:00:02 000:000:000 4                          
2018-01-01 03:01:01 000:000:000 9                          
2018-01-01 03:01:02 000:000:000 16                         
2018-01-01 03:02:01 000:000:000 25                         
2018-01-01 03:02:02 000:000:000 36                         
[18] row(s) selected.
 
Mach> SELECT time ROLLUP 1 MIN mtime, SUMSQ(value) FROM tag GROUP BY mtime ORDER BY mtime;
mtime                           SUMSQ(value)               
---------------------------------------------------------------
2018-01-01 01:00:00 000:000:000 5                          
2018-01-01 01:01:00 000:000:000 25                         
2018-01-01 01:02:00 000:000:000 61                         
2018-01-01 02:00:00 000:000:000 5                          
2018-01-01 02:01:00 000:000:000 25                         
2018-01-01 02:02:00 000:000:000 61                         
2018-01-01 03:00:00 000:000:000 5                          
2018-01-01 03:01:00 000:000:000 25                         
2018-01-01 03:02:00 000:000:000 61                         
[9] row(s) selected.
```

## Grouping at Various Time Intervals

The advantage of the ROLLUP clause is that it is not necessary to intentionally use DATE_TRUNC() to vary the time interval.

To get the sum of the 3-second interval and the number of data, you can do as follows.
Since the example time range is only 0 sec, 1 sec, and 2 sec, it can be seen that they all converge to 0 sec. As a result, it matches the 'rollup by minute' query result.

```bash
Mach> SELECT time rollup 3 sec  mtime, sum(value), count(value) FROM TAG WHERE name = 'TAG_0001' GROUP BY mtime ORDER BY mtime;
mtime                           sum(value)                  count(value)
-------------------------------------------------------------------------------------
2018-01-01 01:00:00 000:000:000 3                           2
2018-01-01 01:01:00 000:000:000 7                           2
2018-01-01 01:02:00 000:000:000 11                          2
2018-01-01 02:00:00 000:000:000 3                           2
2018-01-01 02:01:00 000:000:000 7                           2
2018-01-01 02:02:00 000:000:000 11                          2
2018-01-01 03:00:00 000:000:000 3                           2
2018-01-01 03:01:00 000:000:000 7                           2
2018-01-01 03:02:00 000:000:000 11                          2
```


## Using ROLLUP for JSON type

Starting from version 7.5, ROLLUP can be used for JSON types.
You can create by adding the JSON PATH and OPERATOR at create statement.
A ROLLUP can be created for each PATH in one JSON column.

```sql
-- create tag table
CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, jval JSON);
  
-- insert data
insert into tag values ('tag-01', '2022-09-01 01:01:01', "{ \"x\": 1, \"y\": 1.1}");
insert into tag values ('tag-01', '2022-09-01 01:01:02', "{ \"x\": 2, \"y\": 1.2}");
insert into tag values ('tag-01', '2022-09-01 01:01:03', "{ \"x\": 3, \"y\": 1.3}");
insert into tag values ('tag-01', '2022-09-01 01:01:04', "{ \"x\": 4, \"y\": 1.4}");
insert into tag values ('tag-01', '2022-09-01 01:01:05', "{ \"x\": 5, \"y\": 1.5}");
insert into tag values ('tag-01', '2022-09-01 01:02:00', "{ \"x\": 6, \"y\": 1.6}");
insert into tag values ('tag-01', '2022-09-01 01:03:00', "{ \"x\": 7, \"y\": 1.7}");
insert into tag values ('tag-01', '2022-09-01 01:04:00', "{ \"x\": 8, \"y\": 1.8}");
insert into tag values ('tag-01', '2022-09-01 01:05:00', "{ \"x\": 9, \"y\": 1.9}");
insert into tag values ('tag-01', '2022-09-01 01:06:00', "{ \"x\": 10, \"y\": 2.0}");
  
-- create rollup
CREATE ROLLUP _tag_rollup_jval_x_sec ON tag(jval->'$.x') INTERVAL 1 SEC;
CREATE ROLLUP _tag_rollup_jval_y_sec ON tag(jval->'$.y') INTERVAL 1 SEC;
```

You can also use selecting ROLLUP in the same way.

```bash
Mach> SELECT time ROLLUP 2 SEC mtime, MIN(jval->'$.x'), MAX(jval->'$.x'), SUM(jval->'$.x'), COUNT(jval->'$.x'), SUMSQ(jval->'$.x') FROM tag GROUP BY mtime ORDER BY mtime;
mtime                           min(jval->'$.x')            max(jval->'$.x')            sum(jval->'$.x')            count(jval->'$.x')   sumsq(jval->'$.x')        
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
2022-09-01 01:01:00 000:000:000 1                           1                           1                           1                    1                         
2022-09-01 01:01:02 000:000:000 2                           3                           5                           2                    13                        
2022-09-01 01:01:04 000:000:000 4                           5                           9                           2                    41                        
2022-09-01 01:02:00 000:000:000 6                           6                           6                           1                    36                        
2022-09-01 01:03:00 000:000:000 7                           7                           7                           1                    49                        
2022-09-01 01:04:00 000:000:000 8                           8                           8                           1                    64                        
2022-09-01 01:05:00 000:000:000 9                           9                           9                           1                    81                        
2022-09-01 01:06:00 000:000:000 10                          10                          10                          1                    100                       
[8] row(s) selected.
  
Mach> SELECT time ROLLUP 2 SEC mtime, MIN(jval->'$.y'), MAX(jval->'$.y'), SUM(jval->'$.y'), COUNT(jval->'$.y'), SUMSQ(jval->'$.y') FROM tag GROUP BY mtime ORDER BY mtime
mtime                           min(jval->'$.y')            max(jval->'$.y')            sum(jval->'$.y')            count(jval->'$.y')   sumsq(jval->'$.y')        
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
2022-09-01 01:01:00 000:000:000 1.1                         1.1                         1.1                         1                    1.21                      
2022-09-01 01:01:02 000:000:000 1.2                         1.3                         2.5                         2                    3.13                      
2022-09-01 01:01:04 000:000:000 1.4                         1.5                         2.9                         2                    4.21                      
2022-09-01 01:02:00 000:000:000 1.6                         1.6                         1.6                         1                    2.56                      
2022-09-01 01:03:00 000:000:000 1.7                         1.7                         1.7                         1                    2.89                      
2022-09-01 01:04:00 000:000:000 1.8                         1.8                         1.8                         1                    3.24                      
2022-09-01 01:05:00 000:000:000 1.9                         1.9                         1.9                         1                    3.61                      
2022-09-01 01:06:00 000:000:000 2                           2                           2                           1                    4                         
[8] row(s) selected.
```
