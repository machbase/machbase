---
type: docs
title: '17.1.6 Complete SQL Reference'
weight: 95
toc: true
tocSort: true
---


## datatypes


# Index

* [Data Type Table](#data-type-table)
* [SQL DataType Table](#sql-datatype-table)

## Data Type Table

|Type Name|Description|Value Range|NULL Value|
|--|--|--|--|
|short|16-bit signed integer data type|-32767 ~ 32767|-32768|
|ushort|16-bit unsigned integer type data type|0 ~ 65534|65535|
|integer|32-bit signed integer data type|-2147483647 ~ 2147483647|-2147483648|
|uinteger|32-bit unsigned integer data type|0 ~ 4294967294|4294967295|
|long|64-bit signed integer data type|-9223372036854775807 ~ 9223372036854775807|-9223372036854775808|
|ulong|64-bit unsigned integer data type|0~18446744073709551614|18446744073709551615|
|float|32-bit floating point data type|-|-|
|double|64-bit floating point data type|-|-|
|datetime|Time and date|1970-01-01 00:00:00 000:000:000 ~ 2262-04-11 23:47:16.854:775:807|-|
|varchar|Variable-length character strings (UTF-8)|Length : 1 ~ 32768 (32K)|-|
|ipv4|Version 4 Internet address type (4 bytes)|"0.0.0.0" ~ "255.255.255.255"|-|
|ipv6|Version 6 Internet address type (16 bytes)|"0000:0000:0000:0000:0000:0000:0000:0000" ~ "FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF"|-|
|text|Text data type (keyword index can be generated)|Length : 0 ~ 64M|-|
|binary|Binary (Log: 0~64M) / Tag fixed-length (1~32K-1)|Log: 0 ~ 64M<br>Tag: 1 ~ 32767 bytes|-|
|json|json data type|json data length : 1 ~ 32768 (32K)<br><br>json path length : 1 ~ 512|-|

### short

This is the same as the 16-bit signed integer data of the C language. For the minimum negative value, it is recognized as NULL. May be displayed as "int16".

### integer

This is the same as 32-bit signed integer data in C language. For the minimum negative value, it is recognized as NULL. May be displayed as "int32" or "int".

### long

This is the same as 64-bit signed integer data in C language. For the minimum negative value, it is recognized as NULL. May be displayed as "int64".

### float

This is equivalent to the C 32-bit floating-point data type float. For a positive maximum value, it is recognized as NULL.

### double

This is equivalent to the 64-bit floating-point data type double of C language. For a positive maximum value, it is recognized as NULL.

### datetime

In Machbase, this type maintains the nano value of the time elapsed since midnight January 1, 1970.

Thus, Machbase provides the ability to process values ​​up to nano units for all datetime type related functions.

### varchar

This is a variable string data type and can be generated up to 32K bytes in length.

This length criterion is based on one character in English, so it is different from the actual number of characters to be output in UTF-8 and should be set to an appropriate length.

### IPv4

This type is a type that can store addresses used in Internet Protocol version 4.

It is internally represented using 4 bytes, and can be expressed from "0.0.0.0" to "255.255.255.255".

### IPv6

This type is a type that can store addresses used in Internet Protocol version 6.

16 bytes are internally represented and can be expressed from "0000: 0000: 0000: 0000: 0000: 0000: 0000: 0000" to "FFFF: FFFF: FFFF: FFFF: FFFF: FFFF: FFFF: FFFF" .
Since the abbreviation type is also supported when inputting data, it can be expressed as follows using the symbol :.

* ":: FFFF: 1232": all leading with zeros
* ":: FFFF: 192.168.0.3": Support for IPv4 type compatibility
* ":: 192.168.3.1": Support for deprecated IPv4 type compatibility

### text

This type is a data type for storing text or documents beyond the size of a VARCHAR.

This data type can be searched through keyword indexes and can store up to 64 megabytes of text.
This type is mainly used to store and retrieve large text files as separate columns.

### binary

Binary columns in log tables store unstructured data such as images or
documents. Up to 64 megabytes can be stored (same as TEXT). Lookup and Volatile
tables do not accept `BINARY` columns.

Tag-table `BINARY(n)` is a fixed-length variant for sensor frames.
Valid sizes are 1 to 32K-1 (32767) bytes. SQL accepts `X'...'`, `B'...'`, and
`O'...'` binary literals, including lowercase prefixes. String input in the
legacy form `'0x...'` is still supported for compatibility. If the input exceeds
the target `BINARY(n)` length, insertion fails regardless of the source kind with
`[ERR-02233: Error occurred at column (n): (Invalid insert value.)]`.
Metadata reports the declared byte length, while SQL `LENGTH(binary_col)` and
machsql text output exclude trailing zero padding added for shorter inputs.
machsql displays uppercase hex without the `0x` prefix. This fixed-length
`BINARY(n)` is accepted only in Tag tables. For detailed input formats, see
[Binary Columns](/dbms/tag-table-usage/table-structure-schema/#original-85-binary-columns).

### json

This type is a data type for storing json data.

Json is a format to store data object, consisting of "Key-Value" pairs, into text format.

The maximum size of data is 32K bytes which is same as varchar type.


## SQL Datatype Table

The following table shows the SQL data types and C data types corresponding to the mark base data types.

|Machbase Datatype|Machbase CLI Datatype|SQL Datatype|C Datatype|Basic types for C|Description|
|--|--|--|--|--|--|
|short|SQL_SMALLINT|SQL_SMALLINT|SQL_C_SSHORT|int16_t (short)|16-bit signed integer data type|
|ushort|SQL_USMALLINT|SQL_SMALLINT|SQL_C_USHORT|uint16_t (unsigned short)|16-bit unsigned integer type data type|
|integer|SQL_INTEGER|SQL_INTEGER|SQL_C_SLONG|int32_t (int)|32-bit signed integer data type|
|uinteger|SQL_UINTEGER|SQL_INTEGER|SQL_C_ULONG|uint32_t (unsigned int)|32-bit unsigned integer data type|
|long|SQL_BIGINT|SQL_BIGINT|SQL_C_SBIGINT|int64_t (long long)|64-bit signed integer data type|
|ulong|SQL_UBIGINT|SQL_BIGINT|SQL_C_UBIGINT|uint64_t (unsigned long long)|64-bit unsigned integer data type|
|float|SQL_FLOAT|SQL_REAL|SQL_C_FLOAT|float|32-bit floating point data type|
|double|SQL_DOUBLE|SQL_FLOAT, SQL_DOUBLE|SQL_C_DOUBLE|double|64-bit floating point data type|
|datetime|SQL_TIMESTAMP<br><br>SQL_TIME|SQL_TYPE_TIMESTAMP<br><br>SQL_BIGINT<br><br>SQL_TYPE_TIME|SQL_C_TYPE_TIMESTAMP<br><br>SQL_C_UBIGINT<br><br>SQL_C_TIME|char * (YYYY-MM-DD HH24:MI:SS)<br><br>int64_t (timestamp: nano seconds)<br>struct tm|Time and date|
|varchar|SQL_VARCHAR|SQL_VARCHAR|SQL_C_CHAR|char *|String|
|ipv4|SQL_IPV4|SQL_VARCHAR|SQL_C_CHAR|char * (enter ip string)<br><br>unsigned char[4]|Version 4 Internet address type|
|ipv6|SQL_IPV6|SQL_VARCHAR|SQL_C_CHAR|char * (enter ip string)<br><br>unsigned char[16]|Version 6 Internet address type|
|text|SQL_TEXT|SQL_LONGVARCHAR|SQL_C_CHAR|char *|Text|
|binary|SQL_BINARY|SQL_BINARY|SQL_C_BINARY|char *|Binary data|
|json|SQL_JSON|SQL_JSON|SQL_C_CHAR|json_t|json data type|

## ddl


> **Note**: From Machbase 8.5 or later, a normal user may need database-scoped privileges on `MACHBASEDB` to run the `CREATE` and `DROP` statements described on this page. For privilege details, see [GRANT/REVOKE](#grantrevoke).

## CREATE TABLE

### Syntax

**create_table_stmt:**

![create_table_stmt](/images/sql/ddl/create_table_stmt.png)

**column_list:**

![column_list](/images/sql/ddl/column_list.png)

**column_property_list:**

![column_property_list](/images/sql/ddl/column_property_list.png)


**table_property_list:**

![table_property_list](/images/sql/ddl/table_property_list.png)


**column_type:**

![column_type](/images/sql/ddl/column_type.png)


**with_rollup:**

![with_rollup](/images/sql/ddl/with_rollup_opt.png)

#### Create LOG table

```sql
-- create ctest LOG table with 5 columns
CREATE TABLE ctest (id INTEGER, name VARCHAR(20), sipv4 IPV4, dipv6 IPV6, comment TEXT);
```

#### Create TAG table

TAG tables must have a `PRIMARY KEY` column and an axis column. A time axis uses `DATETIME BASETIME` or `DATETIME BASE TIME`, and a distance axis uses `DOUBLE`, `LONG`, or `ULONG` with `BASE DISTANCE` or `BASEDISTANCE`. `SUMMARIZED` is optional and should be used on value columns that need rollup/statistical tracking.

```sql
-- create TAG table
CREATE TAG TABLE tag_time (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED);
CREATE TAG TABLE tag_time_ext (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED, value2 FLOAT, int_column INT);
CREATE TAG TABLE tag_distance (name VARCHAR(20) PRIMARY KEY, distance_m DOUBLE BASE DISTANCE, value DOUBLE, quality INT);
CREATE TAG TABLE tag_distance_meta (name VARCHAR(20) PRIMARY KEY, distance_m LONG BASEDISTANCE, value DOUBLE) METADATA (route_id VARCHAR(20));
```

Distance-axis columns allow only `DOUBLE`, `LONG`, and `ULONG`. `WITH ROLLUP` is available only for time-axis tag tables.
For `JSON` metadata columns and `JSON INDEX(...)` declarations in TAG metadata, see [Tag Metadata](/dbms/tag-table-usage/tag-metadata/#original-85-tag-metadata).

#### Rules for naming tables or columns

Table names or column names consist of alphanumeric characters. Use double quotation marks (`"`) to use special characters.

```sql
CREATE TABLE special_tbl ( "with.dot" INTEGER );
```

#### IF NOT EXISTS

Prevents an error from occurring if the table exists. However, there is no verification that the existing table has a structure identical to that indicated by the CREATE TABLE statement.

This function only takes effect when the types of tables are equal.

### Table Type

|Table Type|Description|
|--|--|
|LOG|If there is no keyword between CREATE TABLE, a log table is created.|
|VOLATILE|VOLATILE_TABLE is a temporary table in which all data resides in temporary memory and joins the log table to improve the results,<br>The Machbase server disappears as soon as it is shut down.|
|LOOKUP|Like VOLATILE_TABLE, LOOKUP_TABLE can perform fast query processing by storing all the data in memory.|


### Table Property

Specifies the attributes for the table.

|**Property Name**|**Available Table Types**|
|--|--|
|TAG_PARTITION_COUNT|TAG table |
|TAG_DATA_PART_SIZE|TAG table |
|TAG_STAT_ENABLE|TAG table |
|TAG_DUPLICATE_CHECK_DURATION| TAG table |
|VARCHAR_FIXED_LENGTH_MAX| TAG table |

#### TAG_PARTITION_COUNT(Default:4)
A supported attribute for the TAG table, determines how many partition tables will store the TAG table internally. It should be set according to the number of tags or the performance of the server.

#### TAG_DATA_PART_SIZE(Default:16MB)
A supported attribute for the TAG table, determines the data size for each partition table.

#### TAG_STAT_ENABLE(Default:1)
A supported attribute for the TAG Table, determines whether to store statistical information for each TAG ID.

#### TAG_DUPLICATE_CHECK_DURATION(Default:0, Max:43200)
A supported attribute for the TAG Table, the period within which duplicates can be removed is set in minutes based on the current system time. Duplicates can be deleted only for data within this specified period from the current system time. If the set period is 0, duplicate removal will not be performed.

#### VARCHAR_FIXED_LENGTH_MAX (Default: 15, Max: 127)

Specifies the length of the maximum varchar column to be stored in the internal file.

### Column Property

Specifies the attribute for the column.

|**Property Name**|**Available Table Types**|
|--|--|
|PART_PAGE_COUNT|LOG TABLE|
|PAGE_VALUE_COUNT|LOG TABLE|
|MAX_CACHE_PART_COUNT|LOG TABLE|
|MINMAX_CACHE_SIZE|LOG TABLE|

**PART_PAGE_COUNT**
This property represents the number of pages a partition has. The number of values ​​that a partition has is PART_PAGE_COUNT * PAGE_VALUE_COUNT.

**PAGE_VALUE_COUNT**
This property represents the number of values ​​that a page has.

**MAX_CACHE_PART_COUNT (Default : 0)**
This property sets the cache area for performance.
When Machbase accesses a partition, it first looks for a structure that contains the meta information of that partition in memory. It determines how many partition information it contains in memory. Larger size will help performance, but memory usage will increase. The minimum value is 1 and the maximum value is 65535.

**MINMAX_CACHE_SIZE (Default : 10240)**
This property specifies how much cache memory to use for the MINMAX of the corresponding column. The default is 100MB for _ARRIVAL_TIME, the 0th hidden column. However, other columns are specified as 10KB by default. This size can be changed after the creation of the table through the "ALTER TABLE MODIFY" statement.

**NOT NULL Constraint**
Specifies NOT NULL if the column value does not allow NULL, and omit it if it is allowed (Default).
You can change the constraint with the ALTER TABLE MODIFY COLUMN command to drop or add this constraint defined after the creation of the table.

```sql
-- Column c1 is not null and c2 is created without not null constraint.
CREATE TABLE t1(c1 INTEGER NOT NULL, c2 VARCHAR(200));
```

**Pre-defined System Columns**
When you create a table using the Create Table statement, the system creates two additional predefined system columns. _ARRIVAL_TIME and _RID columns.

The _ARRIVAL_TIME column is inserted into the DATETIME column based on the system time at which data is inserted into the INSERT statement or AppendData, and the value can be used as the unique key of the generated record. The value of this column can be inserted by specifying the value in the machloader or INSERT statement if the order is guaranteed (in the order of past-present). When data is retrieved using the DURATION conditional expression, data is retrieved based on the value of this column.
The _RID column is created by the system as a unique value for a particular record. The data type of this column is a 64-bit integer. For this column, the user can not specify a value and can not create an index. It is automatically generated at the time of data INSERT. You can retrieve records by the value of the _RID column.

```sql
create volatile table t1111 (i1 integer);
Created successfully.
Mach> desc t1111;

----------------------------------------------------------------
NAME                          TYPE                LENGTH
----------------------------------------------------------------
_ARRIVAL_TIME                 datetime            8
I1                            integer             4

Mach>insert into t1111 values (1);
1 row(s) inserted.
Mach>select _rid from t1111;
_rid
-----------------------
0
[1] row(s) inserted.

Mach>select i1 from t1111 where _rid = 0;
i1
--------------
1
[1] row(s) selected.
```

### Min Max Cache

#### The Concept of Min-Max Cache

In general, in the Disk DBMS, when a specific value is searched using the index, the disk is accessed to access the disk area including the index, and the final disk page including the corresponding value is searched.

On the other hand, Machbase is a chronologically partitioned structure in order to maintain time series information, which means that a particular piece of index information is divided into chunks of files in chronological order. Therefore, when a Machbase index is used, an index file fragmented by such a partition is sequentially searched.
If the range of data to be searched is divided into 1000 partitions, it means that 1000 files should be opened and retrieved every time. Although it is designed as an efficient columnar database structure, the MINMAX_CACHE structure is a way to improve the performance because the I/O cost is proportional to the number of index partitions.
MINMAX_CACHE is a structure that holds the index file information of the partition in memory, and is a contiguous memory space that keeps the minimum and maximum values ​​of the column in memory. By maintaining such structure, when a partition containing a specific value is searched, if the value is smaller than the minimum value of the index or is larger than the maximum value, the corresponding partition can be skipped altogether, thereby enabling high-performance data analysis.

![When you find a value "85"](/images/sql/ddl/whenyoufindavalue85.png)

As shown in the figure above, to find the value 85, only the partitions 1 and 5 included in MIN/MAX among the 5 partitions are actually searched, and the partitions 2, 3 and 4 are skipped altogether.

#### Min-Max Cache Column

You can decide whether to use MINMAX Cache for a particular column when creating the table.

If the minmax_cache_size is set to a value other than 0, the MINMAX Cache will be active when the index is searched for that column and will not be active if  MINMAX_CACHE_SIZE = 0.
Please note the following when using this MINMAX Cache.

1. MINMAX Cache does not need to explicitly create an index on the column.
2. As default for all columns, MINMAX_CACHE_SIZE is set to 10KB and the Alter Table syntax can be used to reset the memory size to a reasonable size.
3. The hidden column _arrival_time is 100MB by default and automatically uses MINMAX Cache memory.
4. In the case of VARCHAR type, MINMAX Cache is not covered. Therefore, if you explicitly specify whether the VARCHAR type is cached, an error will occur.
5. When the corresponding table is created, the MINMAX_CACHE_SIZE maximum memory can be used as much as the property is set. As the number of partitions grows, the memory grows gradually and increases by the maximum memory above.
6. If there are no records in the table, MINMAX Cache memory is not allocated at all.

Below is an example of table creation using actual MINMAX.

```sql

-- MINMAX_CACHE_SIZE = 0 for VARCHAR is allowed semantically.
CREATE TABLE ctest (id INTEGER, name VARCHAR(100) PROPERTY(MINMAX_CACHE_SIZE = 0));
Created successfully.
Mach>

-- Cache applied to id column.
CREATE TABLE ctest2 (id INTEGER PROPERTY(MINMAX_CACHE_SIZE = 10240), name VARCHAR(100) PROPERTY(MINMAX_CACHE_SIZE = 0));
Created successfully.
Mach>

-- Applied to id1, id2, and id3.
CREATE TABLE ctest3 (id1 INTEGER PROPERTY(MINMAX_CACHE_SIZE = 10240), name VARCHAR(100) PROPERTY(MINMAX_CACHE_SIZE = 0), id2 LONG PROPERTY(MINMAX_CACHE_SIZE = 1024), id3 IPV4 PROPERTY(MINMAX_CACHE_SIZE = 1024), id4 SHORT);
Created successfully.
Mach>

-- MINMAX_CACHE_SIZE is specified in column units or set to 0.
CREATE TABLE ctest4 (id1 INTEGER PROPERTY(MINMAX_CACHE_SIZE=10240), name VARCHAR(100) PROPERTY(MINMAX_CACHE_SIZE=0), id2 LONG PROPERTY(MINMAX_CACHE_SIZE=10240), id3 IPV4 PROPERTY(MINMAX_CACHE_SIZE=0), id4 SHORT);
Created successfully.
Mach>
```

### Primary Key

This is a constraint that can be assigned to a Volatile/Lookup table column. A
Lookup table must have a primary key. A Volatile table can omit the primary key,
but `INSERT ... ON DUPLICATE KEY UPDATE` can be used only when the target table
has a primary key.

When a primary key is assigned, a red-black tree index corresponding to the primary key is generated.

### Sequence Column

#### SEQUENCE for Lookup Table

Sequence was added to generate a unique record of the Lookup table and determine the order in which the data is entered.

This feature was added to solve problems such as difficulty in distinguishing the order of records if the datetime values overlap in the lookup table and application errors due to data duplication.

#### Configuring Sequence when Creating Lookup Tables

When creating a lookup table with a CreateTable SQL statement, simply specify that you want to set the Sequence by adding a PROPERTY clause to the column to be used as the Sequence.

The columns to be set in Sequence only support LONG datatype (64bit, unsigned) and no other.

In addition, the start value of Sequence can be set, but if it is set to 1, Sequence starts from 1. (No support for 0 or negative numbers)

```sql
CREATE LOOKUP TABLE table_name (v1 LONG PROPERTY(SEQUENCE=1) PRIMARY KEY, v2 VARCHAR(10));
```

#### Use of sequence column

The Sequence column of the Lookup table is basically the same as a regular Long column and when used in this way, the Sequence value does not automatically increase.

It is allowed to enter values directly into the Sequence column, and even duplicate values can be entered.

Instead, if you want to use the Sequence function, you should use a newly added Sequence-only function called nextval to increase the Sequence value.

Internally, it stores the largest value of a column set to Sequence, so when you enter it later using nextval Function, the largest value of the Sequence column value +1 is stored.

**Example of Sequence column**
```sql
-- Insert the following Sequence value using nextval Function in the Sequence column.
INSERT INTO table_name (v1, v2) values (nextval(v1), 'aaaa');

-- Insert a value directly into the Sequence column
INSERT INTO table_name (v1, v2) values (100, 'aaaa');

-- Insert a the computational value in the Sequence column.
INSERT INTO table_name (v1, v2) values (100 + 1, 'aaaa');

-- Success Select of Lookup Tables with Sequence Columns
SELECT v1, v2 FROM table_name;

-- Invalid Select for Sequence column (nextval column can only be used in insert query)
SELECT nextval(v1), v2 FROM table_name;
```

## CREATE VIEW / DROP VIEW

VIEW stores a `SELECT` definition as a named logical object for reuse.
Unlike a table, a VIEW does not store data separately. When queried, the stored
definition SQL is expanded and executed internally.

```sql
CREATE VIEW v_example AS
SELECT id, name
FROM t1;

DROP VIEW v_example;
```

For the full description including `CREATE OR REPLACE VIEW`, `DROP VIEW IF EXISTS`,
`SHOW VIEWS`, `M$SYS_VIEWS`, performance/limits, and Tag / `BINARY` examples,
see [VIEW](#view).

## DROP TABLE

**drop_table_stmt:**

![drop_table_stmt](/images/sql/ddl/drop_table_stmt.png)

```sql
drop_table_stmt ::= 'DROP TABLE' table_name
```

Deletes the specified table. However, if there is another session in which the table is being searched, it fails with an error.

```sql
-- Example
DROP TABLE TableName;
```

## CREATE TABLESPACE

**create_tablespace_stmt:**

![create_tablespace_stmt](/images/sql/ddl/create_tablespace_stmt.png)

**datadisk_list:**

![datadisk_list](/images/sql/ddl/datadisk_list.png)

**data_disk:**

![data_disk](/images/sql/ddl/data_disk.png)

**data_disk_property:**

![data_disk_property](/images/sql/ddl/data_disk_property.png)

```sql
create_tablespace_stmt ::= 'CREATE TABLESPACE' tablespace_name 'DATADISK' datadisk_list
datadisk_list ::= data_disk ( ',' data_disk )*
data_disk ::= disk_name data_disk_property
data_disk_property ::= '(' 'DISK_PATH' '=' '"' path '"' ( ',' 'PARALLEL_IO' '=' number )? ')'
```

```sql
-- Example
create tablespace tbs1 datadisk disk1 (disk_path=""); -- $MACHBASE_HOME/dbs/  (Create in $MACHBASE_HOME/dbs/)
create tablespace tbs1 datadisk disk1 (disk_path="tbs1_disk1"); -- $MACHBASE_HOME/dbs/tbs1_disk1  (Created in $MACHBASE_HOME/dbs/tbs1_disk1. tbs1_disk1 folder must exist)
create tablespace tbs2 datadisk disk1 (disk_path="tbs2_disk1", parallel_io = 5);
create tablespace tbs1 datadisk disk1 (disk_path="tbs1_disk1", parallel_io = 10), disk2 (disk_path="tbs1_disk2"), disk3 (disk_path="tbs1_disk3");
```

The CREATE TABLESPACE statement creates a tablespace in $MACHBASE_HOME/dbs/ where the indexes of the log table or log table will be stored.

Tablespace can have multiple disks. When each Partition File that stores data of Table and Index is stored, it is distributed and stored in Data Disks belonging to Tablespace.
If two or more disks are used, the index and table files are distributed and stored on each disk, and I/O is performed in parallel on each device. As the number of disks increases, disk I / O throughput increases, and a large amount of data can be stored on the disk quickly
Also, if tables and index tablespace are separately created and different disks are defined, I/O of table and index can be logically separated without reconfiguration of physical disk.

### DATA DISK

Defines disk belonging to a tablespace. Each Disk has the following properties.

|Property|Description|
|--|--|
|data_disk_property|Specifies the attributes of the disk.|
|disk_name|Specifies the name of the Disk object. It is used to change the attributes of the Disk object through Alter Tablespace syntax later.|
|disk_path|Specifies the Directory Path of the disk. This Directory must be created. When a path is specified as a relative path, PATH is searched based on $MACHBASE_HOME/dbs. For example, if PATH = 'disk1', Disk Path is recognized as $MACHBASE_HOME/dbs/disk1.|
|parallel_io|Determines how many disk IO requests are allowed to be paralleled. (DEF: 3, MIN: 1, MAX: 128)|


## DROP TABLESPACE

**drop_tablespace_stmt:**

![drop_tablespace_stmt](/images/sql/ddl/drop_tablespace_stmt.png)

```sql
drop_table_stmt ::= 'DROP TABLESPACE' tablespace_name
```

Deletes the specified tablespace. However, if the object created in Tablespace exists, deletion fails.

```sql
-- Example
DROP TABLESPACE TablespaceName;
```


## CREATE INDEX

**create_index_stmt:**

![create_index_stmt](/images/sql/ddl/create_index_stmt.png)

**index_type:**

![index_type](/images/sql/ddl/index_type.png)

**table_space:**

![table_space](/images/sql/ddl/table_space.png)

**index_property_list:**

![index_property_list](/images/sql/ddl/index_property_list.png)

```sql
create_index_stmt ::= 'CREATE' 'INDEX' index_name 'ON' table_name '(' column_name ')' index_type? table_space? index_property_list?
index_type ::= 'INDEX_TYPE' ( 'LSM' | 'KEYWORD' | 'BITMAP' | 'REDBLACK' )
table_space ::= 'TABLESPACE' table_space_name
index_property_list ::= ( 'MAX_LEVEL' | 'PAGE_SIZE' | 'BITMAP_ENCODE' | 'PART_VALUE_COUNT' ) '=' value
```

### Index Type

Specifies the Index Type to be created. If it is not Keyword Index, Index Type is created as Default Index Type according to Table Type if Index Type is not specified.

|Table Type|Default Index Type|
|--|--|
|Volatile Table|REDBLACK|
|Lookup Table|REDBLACK|
|Log Table|LSM|

### KEYWORD Index

This can be created only for varchar and text column of log table. It can be created for only one column.

### LSM Index

LSM (Log Structure Merge) Index is an index optimized for storing and searching Big Data. The partitions of the LSM indexes are maintained for each level, and the lower level partitions are merged to move to the upper level. Lower partitions used to create a higher level partition are deleted.

This Index Level Partition Building is performed by Background Thread. The upper level partitions are merged with the lower level partitions and are created as one partition, so there are the following advantages when searching through the index.

1. If the key is duplicated, the disk space for key storage is saved because it is stored only once.

2. Searching for multiple partitions reduces the cost of opening and closing the file when searching for one index partition, and the number of index pages accessed is also reduced.

### LSM Index Property

|Item|Description|
|--|--|
|MAX_LEVEL<br>(DEFAULT = 3, MIN = 0, MAX = 3 )|The maximum level of the LSM Index, and the current value of 3 is the maximum value. And the maximum number of records of one partition can not exceed 200 million. The partition size of each level is the number of values ​​of the previous partition * 10. For example, if MAX_LEVEL = 3 and PART_VALUE_COUNT is 100,000, then Level 0 = 100,000, Level 1 = 1,000,0000, Level 2 = 10,000,000, and Level 3 = 100,000,000. If the Partition Size of the last level exceeds 200 million, index creation will fail.|
|PAGE_SIZE<br>(DEFAULT = 512 * 1024, MIN = 32 * 1024,MAX = 1 * 1024 * 1024)|Specifies the size of the page in which the index key value and bitmap value are stored. Default is 512K.|
|BITMAP_ENCODE<br>(DEFAULT = EQUAL, RANGE)|Sets the bitmap type of the index.<br>If BITMAP_ENCODE = EQUAL (default), generates a bitmap for the same value as the key value. If BITMAP = RANGE, generates a bitmap according to the range of the key value.<br>It is better to set as BITMAP_ENCODE = EQUAL when using = as the query condition, and BITMAP_ENCODE = RANGE when using the specific range value as the query condition.<br>In the case of BITMAP = RANGE, the cost of creation increases slightly compared to EQUAL.|

### BITMAP Index

This is an index for data analysis and can be created only in the log table. It can be created on all columns except varchar, text, and binary, and can only be created on a single column.

### RED-BLACK Index

This is a memory index for real-time data retrieval. It can be created only in the Volatile/Lookup table. It can be created in all columns of this table and can only be created for a single column.

### Index Property

The properties that can be applied in the LSM Index are as follows.

**PART_VALUE_COUNT**
Indicates the number of rows stored in the Partition of Index.

```sql
-- Example
-- Index applied to c1 column.
CREATE INDEX index1 on table1 ( c1 );
-- LSM index applied explicitly.
CREATE INDEX index_lsm on table1 ( c1 ) INDEX_TYPE LSM;
-- Keyword index applied to var_column of varchar type, and page_size unit is 100000.
CREATE INDEX index2 on table1 (var_column) INDEX_TYPE KEYWORD PAGE_SIZE=100000;
```

##### JSON path indexes

When creating an index on a member of a JSON column, you can use both the existing JSONPath arrow syntax and JSON dot shorthand.

```sql
CREATE TAG TABLE tag_log (
    name  VARCHAR(40) PRIMARY KEY,
    time  DATETIME BASETIME,
    value JSON
);

-- JSON dot shorthand
CREATE INDEX tag_log_sensor_idx ON tag_log (value.sensor.name);

-- Existing JSONPath arrow syntax
CREATE INDEX tag_log_metric_idx ON tag_log (value->'$.metric');

-- Array index and double quoted key
CREATE INDEX tag_log_item_idx ON tag_log (value.items[0]."product-id");
```

The existing arrow DDL syntax also remains available when the JSON column name is double quoted or is a keyword column name.

```sql
CREATE TAG TABLE tag_log_q (
    name    VARCHAR(40) PRIMARY KEY,
    time    DATETIME BASETIME,
    "value" JSON
);

CREATE INDEX tag_log_q_idx ON tag_log_q ("value"->'$.sensor.name');

CREATE TAG TABLE tag_log_kw (
    name   VARCHAR(40) PRIMARY KEY,
    time   DATETIME BASETIME,
    "LEFT" JSON
);

CREATE INDEX tag_log_kw_idx ON tag_log_kw (left->'$.sensor.name');
```

String comparison predicates can use JSON path indexes. Predicates with numeric or boolean meaning are not used as JSON path index range predicates because string ordering and numeric ordering can differ.

For TAGDATA metadata JSON path indexes, see [Tag Metadata](/dbms/tag-table-usage/tag-metadata/#original-85-tag-metadata) and [Tag Table Indexes](/dbms/tag-table-usage/index-performance/#original-85-tag-indexes).

## DROP INDEX

**drop_index_stmt:**

![drop_index_stmt](/images/sql/ddl/drop_index_stmt.png)

```sql
drop_index_stmt ::= 'DROP INDEX' index_name
```

Deletes the specified index. However, if there is another session in which the table is being searched, it fails with an error.

```sql
-- Example
DROP INDEX IndexName;
```

## ALTER TABLE

The ALTER TABLE statement is used to change the schema information of the specified table.

- Most ALTER TABLE operations are available only for Log Tables
- RENAME COLUMN operation is available for both Log Tables and Tag Tables

### ALTER TABLE SET

This syntax changes the properties of a table. Currently there are no dynamically changeable properties.

### ALTER TABLE ADD COLUMN

**alter_table_add_stmt:**

![alter_table_add_stmt](/images/sql/ddl/alter_table_add_stmt.png)

```sql
alter_table_add_stmt ::= 'ALTER TABLE' table_name 'ADD COLUMN' '(' column_name column_type ( 'DEFAULT' value )? ')'
```

This syntax is the ability to add a specific column to the table in real time. You can add the name and type of the column, and set the default data values ​​through the DEFAULT clause.

```sql
-- Example-1
alter table atest2 add column (id4 float);

-- Example-2
alter table atest2 add column (id6 double  default 5);
alter table atest2 add column (id7 ipv4  default '192.168.0.1');
alter table atest2 add column (id8 varchar(4) default 'hello');
```

### ALTER TABLE DROP COLUMN

**alter_table_drop_stmt:**

![alter_table_drop_stmt](/images/sql/ddl/alter_table_drop_stmt.png)

```sql
alter_table_drop_stmt ::= 'ALTER TABLE' table_name 'DROP COLUMN' '(' column_name ')'
```

This syntax is to delete a specific column in the table in real time.

```
-- Example
alter table atest2 drop column (id4);
alter table atest2 drop column (id8);
```

### ALTER TABLE METADATA ADD COLUMN

**alter_table_metadata_add_stmt:**

```sql
alter_table_metadata_add_stmt ::= 'ALTER TABLE' table_name 'METADATA ADD COLUMN' '(' column_name column_type ( 'DEFAULT' value )? ')'
```

This syntax adds a metadata column to a TAG table. Metadata columns store tag-specific information that doesn't change frequently with each data point.

> **Note**: This operation is only available for TAG tables.

```sql
-- Example: Add metadata columns to a TAG table
ALTER TABLE altertbl METADATA ADD COLUMN (m1 DOUBLE);
ALTER TABLE altertbl METADATA ADD COLUMN (m2 VARCHAR(100));
ALTER TABLE altertbl METADATA ADD COLUMN (m3 INTEGER DEFAULT 0);
```

### ALTER TABLE METADATA DROP COLUMN

**alter_table_metadata_drop_stmt:**

```sql
alter_table_metadata_drop_stmt ::= 'ALTER TABLE' table_name 'METADATA DROP COLUMN' '(' column_name ')'
```

This syntax removes a metadata column from a TAG table.

> **Note**: This operation is only available for TAG tables.

```sql
-- Example: Drop metadata columns from a TAG table
ALTER TABLE altertbl METADATA DROP COLUMN (m1);
ALTER TABLE altertbl METADATA DROP COLUMN (m2);
```

### ALTER TABLE RENAME COLUMN

**alter_table_column_rename_stmt:**

![alter_table_column_rename_stmt](/images/sql/ddl/alter_table_column_rename_stmt.png)

```sql
alter_table_column_rename_stmt ::= 'ALTER TABLE' table_name 'RENAME COLUMN' old_column_name 'TO' new_column_name
```

This syntax is a function that changes a specific column name in a table. This operation is available for both Log Tables and Tag Tables.

```sql
-- Example for Log Table
alter table atest2 rename column id7 to id7_rename;

-- Example for Tag Table
alter table tag rename column v0001 to vmax;
```

> **Note**: For Tag Tables, you can rename any column including additional value columns, but PRIMARY KEY, BASETIME, and METADATA column names can also be changed. However, if the tag table has ROLLUP tables defined, renaming columns may be restricted.

> **Note**: RENAME COLUMN operation for Tag Tables is supported from Machbase version 8.0.50 or later.

### ALTER TABLE MODIFY COLUMN

**alter_table_modify_stmt:**

![alter_table_modify_stmt](/images/sql/ddl/alter_table_modify_stmt.png)

```sql
alter_table_modify_stmt ::= 'ALTER TABLE' table_name 'MODIFY COLUMN' ( '(' column_name 'VARCHAR' '(' new_size ')' ')' | column_name ( 'NOT'? 'NULL' | 'SET' 'MINMAX_CACHE_SIZE' '=' value ) )
```

This syntax changes the properties of a particular column of a table. Currently it is possible to modify MINMAX CACHE attributes and NOT NULL constraints for column lengths and other types of VARCHAR types.

**VARCHAR SIZE**

This syntax supports changing the column length of VARCHAR type only. This operation can not be reduced in length to preserve existing data, and should always be increased.

```sql
ALTER TABLE table_name MODIFY COLUMN (column_name VARCHAR(new_size));
```

```sql
-- Example: Assume TABLE is created like this.
-- create table atest5 (id integer, name varchar(5), id3 double, id4 float);

-- Error occurred: Can not change to another type,
alter table atest5 modify column (id varchar(10));

-- Error occurred: VARCHAR length can not be made smaller.
alter table atest5 modify column (name varchar(3));

-- Error occurred: Maximum size of VARCHAR can not exceed 32767.
alter table atest5 modify column (name varchar(32768));

-- Success
alter table atest5 modify column (name varchar(128));
```

**MINMAX_CACHE_SIZE**

This syntax changes MINMAX_CACHE_SIZE for a particular column.

```sql
ALTER TABLE table_name MODIFY COLUMN column_name SET MINMAX_CACHE_SIZE=value;
```

```sql
-- Example: Assume TABLE is created like this.
create table atest9 (id integer, name varchar(100));

-- Error: Does not apply to VARCHAR.
alter table atest9 modify column name set minmax_cache_size=0;
[ERR-02139 : MINMAX CACHE is not allowed for VARCHAR column(NAME).]

-- Change success
alter table atest9 modify column id set minmax_cache_size=10240;
```

**NOT NULL**

Adds a NOT NULL constraint to the column. If you add a NOT NULL constraint, the DDL operation fails for columns with NULL values.
If you want to allow NULL values ​​in a column, use the MODIFY COLUMN NULL command in the next section.

```sql
ALTER TABLE table_name MODIFY COLUMN column_name NOT NULL;
```

```sql
-- Add NOT NULL constraint to t1.c1.
alter table t1 modify column c1 not null;
```

**NULL**

Releases the NOT NULL constraint. Performance improvement due to min_max cache of LSM index can not be obtained. NULL values ​​can be input.

```sql
ALTER TABLE table_name MODIFY COLUMN column_name NULL;
```

```sql
-- Release NOT NULL constraint at t1.c1.
alter table t1 modify column c1 null;
```


### ALTER TABLE RENAME TO

**alter_table_rename_stmt:**

![alter_table_rename_stmt](/images/sql/ddl/alter_table_rename_stmt.png)

```sql
alter_table_rename_stmt ::= 'ALTER TABLE' table_name 'RENAME TO' new_name
```

Changes the name of the table.

Metatables can not be renamed, and you can not use the $ character in the name to be changed. Table renaming is only possible for Log tables.

```sql
-- Change the name of worker table to employee.
ALTER TABLE worker RENAME TO employee;
```

### ALTER TABLE ADD RETENTION

**alter_table_add_retention_stmt:**

```sql
alter_table_add_retention_stmt ::=  'ALTER TABLE' table_name 'ADD RETENTION' policy_name
```

![alter_table_add_retention_stmt](/images/sql/ddl/alter_table_add_retention_stmt.png)

```sql
ALTER TABLE tag ADD RETENTION policy_1d_1h;
```


### ALTER TABLE DROP RETENTION

**alter_table_drop_retention_stmt:**

```sql
alter_table_drop_retention_stmt ::=  'ALTER TABLE' table_name 'DROP RETENTION'
```

![alter_table_drop_retention_stmt](/images/sql/ddl/alter_table_drop_retention_stmt.png)

```sql
ALTER TABLE tag DROP RETENTION;
```


## ALTER TABLESPACE

The ALTER TABLESPACE statement is used to change the information associated with the specified tablespace.

### ALTER TABLESPACE MODIFY DATADISK

This syntax is used to change the properties of DATADISK in Tablespace.

**alter_tablespace_stmt:**

![alter_tablespace_stmt](/images/sql/ddl/alter_tablespace_stmt.png)

```sql
alter_tablespace_stmt ::= 'ALTER TABLESPACE' table_name 'MODIFY DATADISK' disk_name 'SET' 'PARALLEL_IO' '=' value
```

```sql
-- Example
ALTER TABLESPACE tbs1 MODIFY DATADISK disk1 SET PARALLEL_IO = 10;
```

## TRUNCATE TABLE

**truncate_table_stmt:**

![truncate_table_stmt](/images/sql/ddl/truncate_table_stmt.png)

```sql
truncate_table_stmt ::= 'TRUNCATE TABLE' table_name
```

```sql
-- Delete all data in ctest table.
Mach> truncate table ctest;
Truncated successfully.
```

Deletes all data in the specified table. However, if there is another session in which the table is being searched, it fails with an error.



## CREATE ROLLUP

**create_rollup_stmt:**

![create_rollup_stmt](/images/sql/ddl/create_rollup_stmt.png)

```sql
create_rollup_stmt ::= 'CREATE ROLLUP' rollup_name 'ON' src_table_name '('src_table_column')' 'INTERVAL' number ('SEC' | 'MIN' | 'HOUR')
```

```sql
-- Creates a rollup targeting the value column of the tag table.
Mach> CREATE ROLLUP _rollup_tag_value_sec ON tag(value) INTERVAL 1 SEC;
Executed successfully
```

When using a member of a JSON column as the rollup target value, you can use both the existing JSONPath arrow syntax and JSON dot shorthand.

```sql
CREATE TAG TABLE tag_json (
    name  VARCHAR(40) PRIMARY KEY,
    time  DATETIME BASETIME,
    value JSON
);

-- JSON dot shorthand
CREATE ROLLUP tag_json_metric_ru
ON tag_json (value.metric)
INTERVAL 1 SEC;

-- Existing JSONPath arrow syntax
CREATE ROLLUP tag_json_metric_arrow_ru
ON tag_json (value->'$.metric')
INTERVAL 1 SEC;

-- Array index and double quoted key
CREATE ROLLUP tag_json_item_ru
ON tag_json (value.items[0]."metric-id")
INTERVAL 1 SEC;
```

Quoted column names and keyword column names are also still supported with the existing arrow syntax.

```sql
CREATE TAG TABLE tag_json_q (
    name    VARCHAR(40) PRIMARY KEY,
    time    DATETIME BASETIME,
    "value" JSON
);

CREATE ROLLUP tag_json_q_ru
ON tag_json_q ("value"->'$.metric')
INTERVAL 1 SEC;

CREATE TAG TABLE tag_json_kw (
    name   VARCHAR(40) PRIMARY KEY,
    time   DATETIME BASETIME,
    "LEFT" JSON
);

CREATE ROLLUP tag_json_kw_ru
ON tag_json_kw (left->'$.metric')
INTERVAL 1 SEC;
```

> If corrected source data requires existing rollup results to be rebuilt, see [Rollup Rebuild Guide](/dbms/tag-rollup-usage/rollup-rebuild/#original-85-rollup-rebuild).

```sql
create_conditional_rollup_stmt ::= 'CREATE ROLLUP' rollup_name
                                   ( 'ON' src_table_name '('src_table_column')'
                                   | 'FROM' src_rollup_table_name )
                                   'INTERVAL' number ('SEC' | 'MIN' | 'HOUR')
                                   'WHERE' predicate
```

```sql
-- Conditional rollup: aggregates only rows where value2 = 0
Mach> CREATE ROLLUP _rollup_tag_value_min_ok
      ON tag(value)
      INTERVAL 1 MIN
      WHERE value2 = 0;
Executed successfully
```

```sql
create_custom_rollup_stmt ::= 'CREATE ROLLUP' rollup_name
                              'INTO' '(' dest_table_name ')'
                              'AS' '(' select_stmt ')'
                              'INTERVAL' number ('SEC' | 'MIN' | 'HOUR')
                              [ 'WAKEUP INTERVAL' number ('SEC' | 'MIN' | 'HOUR') ]
```

```sql
-- Creates a custom rollup that stores user-defined aggregation into a TAG table.
Mach> CREATE ROLLUP rollup_stock_1m
      INTO (stock_rollup_1m)
      AS (
        SELECT code,
               DATE_TRUNC('minute', time) AS time,
               SUM(price)                 AS sum_price,
               COUNT(*)                   AS cnt
          FROM stock_tick
         GROUP BY code, time
      )
      INTERVAL 1 MIN;
Executed successfully
```

Notes
- Use conditional rollup `WHERE` with the `ON/FROM` rollup syntax.
- For Custom Rollup, use `WHERE` only inside the `SELECT`.
- External `INTERVAL ... WHERE ...` is not supported for Custom Rollup syntax.
- For full constraints and query patterns, see [Custom Rollup: User-Defined Aggregation](/dbms/tag-rollup-usage/custom-rollup/#original-85-rollup-custom).


## DROP ROLLUP

**drop_rollup_stmt:**

![drop_rollup_stmt](/images/sql/ddl/drop_rollup_stmt.png)

```sql
drop_rollup_stmt ::= 'DROP ROLLUP' rollup_name
```

```
-- drop rollup.
Mach> DROP ROLLUP _rollup_tag_value_sec;
Executed successfully
```

## ALTER ROLLUP

Control rollup workers and their wakeup schedule.

```sql
alter_rollup_start_stop_stmt ::= 'ALTER ROLLUP' rollup_name ( 'START' | 'STOP' )
alter_rollup_force_stmt      ::= 'ALTER ROLLUP' rollup_name 'FORCE'
alter_rollup_wakeup_stmt     ::= 'ALTER ROLLUP' rollup_name 'WAKEUP'
alter_rollup_wakeup_int_stmt ::= 'ALTER ROLLUP' rollup_name 'SET WAKEUP INTERVAL' number ( 'SEC' | 'MIN' | 'HOUR' )
```

Examples
```sql
-- Start/stop a rollup thread
ALTER ROLLUP _rollup_tag_value_sec START;
ALTER ROLLUP _rollup_tag_value_sec STOP;

-- Wake the thread now (non-blocking)
ALTER ROLLUP _rollup_tag_value_sec WAKEUP;

-- Run immediately and wait for completion
ALTER ROLLUP _rollup_tag_value_sec FORCE;

-- Tighten the wakeup interval (must divide the rollup interval)
ALTER ROLLUP _rollup_tag_value_sec SET WAKEUP INTERVAL 1 SEC;
```

Rules
- Wakeup interval must be > 0, not larger than the rollup interval, and must evenly divide the rollup interval; otherwise an error is returned.
- `WAKEUP` only pokes the thread and returns immediately. Use `FORCE` when you need to block until catch-up finishes.

## CREATE RETENTION

**create_retention_stmt:**

![create_retention_stmt](/images/sql/ddl/create_retention_stmt.png)

```sql
create_retention_stmt ::= 'CREATE RETENTION' policy_name 'DURATION' duration ( 'MONTH' | 'DAY' ) 'INTERVAL' interval ( 'DAY' | 'HOUR' )
```

```sql
Mach> CREATE RETENTION policy_1d_1h DURATION 1 DAY INTERVAL 1 HOUR;
Executed successfully
```

## DROP RETENTION

**drop_retention_stmt:**

![drop_retention_stmt](/images/sql/ddl/drop_retention_stmt.png)

```sql
drop_retention_stmt ::= 'DROP RETENTION' policy_name
```

```sql
Mach> DROP RETENTION policy_1d_1h;
Executed successfully
```

## dml


## INSERT

**insert_stmt:**

![insert_stmt](/images/sql/dml/insert_stmt.png)

**insert_column_list:**

![insert_column_list](/images/sql/dml/insert_column_list.png)

**value_list:**

![value_list](/images/sql/dml/value_list.png)

**set_list:**

![set_list](/images/sql/dml/set_list.png)

```sql
insert_stmt ::= 'INSERT INTO' table_name ( '(' insert_column_list ')' )? 'METADATA'? 'VALUES' '(' value_list ')' ( 'ON DUPLICATE KEY UPDATE' ( 'SET' set_list )? )?
insert_column_list ::= column_name ( ',' column_name )*
value_list ::= value ( ',' value )*
set_list ::= column_name '=' value ( ',' column_name '=' value )*
```

```sql
create table test (number int,name varchar(20));
Created successfully.
insert into test values (1,"test");
1 row(s) inserted.
insert into test(name,number) values ("test",2);
1 row(s) inserted.
```

This is the syntax for entering values ​​into a specific table. One unusual thing is that columns not specified in Column_List are all filled with NULL values. This is a policy considering the characteristics of log files adopted for convenience of input and efficiency of storage space.
METADATA is only available for tag tables.

### INSERT ON DUPLICATE KEY UPDATE

Machbase supports syntax similar to the commonly known UPSERT function.

A special syntax that can be used when entering a value into a Lookup/Volatile table with a primary key specified. If the table already contains data with a duplicate primary key value, the value of the existing data is changed.
Of course, when there is no duplicated key value data, it is inserted as new data.

To use this syntax, the primary key must be specified in the volatile table.

If the column value of the inserted data is different from the column value of the updated data, or if it is desired to update a column value other than the column value of the inserted data, the SET clause can be further input.

* The SET clause consists of 'column = value', each separated by a comma.
* You must not change the default key value in the SET clause.


## INSERT SELECT

insert_select_stmt:

![insert_select_stmt](/images/sql/dml/insert_select_stmt.png)

```sql
insert_select_stmt ::= 'INSERT INTO' table_name ( '(' insert_column_list ')' )? select_stmt
```

This statement inserts the result of the SELECT statement on a specific table. In basic, it is similar to other DBMSs, but with the following differences.
1. The _ARRIVAL_TIME column value is entered as the time value at the time the INSERT SELECT statement is executed unless specified in the select and INSERT column lists.
2. If the input value to be inserted for a VARCHAR type column is greater than the maximum length of the column, the maximum length of the corresponding column is entered without error.
3. If type conversion is possible (numeric -> numeric), it is inserted according to the input column value.
4. ROLLBACK does not occur if an error occurs during execution.
5. If you insert a value in the _ARRIVAL_TIME column, the new value will not be entered if it has a time before the existing value.

```sql
create table t1 (i1 integer, i2 varchar(60), i3 varchar(5));
Created successfully.

insert into t1 values (1, 'a', 'ddd' );
1 row(s) inserted.
insert into t1 values (2, 'kkkkkkkkkkkkkkkkkkkkk', 'c');
1 row(s) inserted.

insert into t1 select * from t1;
2 row(s) inserted.
create table t2 (i1 integer, i2 varchar(60), i3 varchar(5));

insert into t2 (_arrival_time, i1, i2, i3) select _arrival_time, * from t1;
4 row(s) inserted.
```


## UPDATE

* This function is available from 5.5.

**update_stmt:**

![update_stmt](/images/sql/dml/update_stmt.png)


**update_expr_list:**

![update_expr_list](/images/sql/dml/update_expr_list.png)


**update_expr:**

![update_expr](/images/sql/dml/update_expr.png)

```sql
update_stmt ::= 'UPDATE' table_name ( 'METADATA' )? 'SET' update_expr_list 'WHERE' primary_key_column '=' value
update_expr_list ::= update_expr ( ',' update_expr)*
update_expr ::= column '=' value
```

INSERT ON DUPLICATE UPDATE syntax is also provided, rather than UPSERT via a KEY UPDATE.
You can also use the Primary Key to enter values ​​into the specified Lookup/Volatile table. In the WHERE clause, you must create a matching predicate for the primary key.

### UPDATE METADATA

Only for the TAGDATA table, when you want to update the metadata.

```sql
UPDATE TAG METADATA SET ...
```

* The metadata of the TAGDATA table can not be entered/modified through INSERT ON DUPLICATE KEY UPDATE.
* `TAG METADATA` now allows metadata predicates as well as `WHERE NAME = ...`.
* Data columns such as `TIME` and `VALUE` cannot be updated through `UPDATE ... METADATA`.
* Only `NAME` and metadata columns can be updated.

```sql
UPDATE sensors METADATA
   SET status = 'DONE'
 WHERE status = 'READY';
```


## DELETE

**delete_stmt:**

![delete_stmt](/images/sql/dml/delete_stmt.png)


**time_unit:**

![time_unit](/images/sql/dml/time_unit.png)

```sql
delete_stmt ::= 'DELETE FROM' table_name ( 'OLDEST' number 'ROWS' | 'EXCEPT' number ( 'ROWS' | time_unit ) | 'BEFORE' datetime_expression )? 'NO WAIT'?
time_unit ::= 'DURATION' number time_unit ( ( 'BEFORE' | 'AFTER' ) number time_unit )?
```

The DELETE statement in Machbase can be performed on the log table. In addition, it is not possible to delete data in an arbitrary position in the middle, and it is possible to erase consecutively from the arbitrary position to the last (oldest log) record.

This is a policy that takes advantage of the characteristics of log data. It is a DB format representation of the act of deleting a file in order to secure space when it is entered once.

The syntax of DURATION, OLDEST, and EXCEPT cannot be used for TAG and Rollup tables.

```sql
-- Delete all.
DELETE FROM devices;

-- Delete oldest last N rows.
DELETE FROM devices OLDEST N ROWS;

-- Delete all except recent N rows.
DELETE FROM devices EXCEPT N ROWS;

-- Delete all except N matches from now on.
DELETE FROM devices EXCEPT N DAY;

-- Delete all data from before June 1, 2014.
DELETE FROM devices BEFORE TO_DATE('2014-06-01', 'YYYY-MM-DD');

-- Delete tag data from before June 1, 2014.
DELETE FROM tag BEFORE TO_DATE('2014-06-01', 'YYYY-MM-DD');

-- Delete tag rollup data from before June 1, 2014.
DELETE FROM tag ROLLUP BEFORE TO_DATE('2014-06-01', 'YYYY-MM-DD');
```


## DELETE WHERE

**delete_where_stmt:**

![delete_where_stmt](/images/sql/dml/delete_where_stmt.png)

```sql
delete_where_stmt ::= 'DELETE FROM' table_name 'WHERE' column_name '=' value
```

```sql
create volatile table t1 (i1 int primary key, i2 int);
Created successfully.
insert into t1 values (2,2);
1 row(s) inserted.
delete from t1 where i1 = 2;
1 row(s) deleted.
```

* You can delete records that match the conditions created in the WHERE clause for volatile tables and lookup tables.
* The primary key can only be performed on the specified volatile or lookup table.
* The WHERE clause allows only conditions of (primary key column) = (value), and can not be created with other conditions.
* You can not use a column other than the primary key column in the condition.

### DELETE FROM TAG METADATA

Metadata of a TAGDATA table can be deleted through `DELETE FROM TAG METADATA`.
If the `WHERE` clause is omitted, all metadata rows in the TAGDATA table are deleted.

```sql
DELETE FROM tag METADATA;
DELETE FROM tag METADATA WHERE name = 'tag-1';
DELETE FROM tag METADATA WHERE status = 'STOP';
```

Notes:

- Metadata predicates as well as `WHERE NAME = ...` are allowed.
- If any matched tag still has data rows, the whole statement fails.
- Metadata of tags that are still in use cannot be deleted.
- Even for a full metadata delete, if any target tag is still in use, the whole statement fails
  without partially deleting metadata rows.
- The same syntax is supported for TAGDATA tables whose tag name column is not named `name`.

**delete_from_tag_where_stmt:**

![delete_from_tag_where_stmt](/images/sql/dml/delete_from_tag_where_stmt.png)

```sql
delete_from_tag_where_stmt ::= 'DELETE FROM' table_name 'ROLLUP'? 'WHERE' predicate
```

A Tag or Rollup table supports constrained DELETE predicates by tag name, by tag name plus time, or by time only.

Supported time predicates include `=`, `<`, `<=`, and `BETWEEN`.

```sql
-- Delete by tag name
DELETE FROM tag WHERE tag_name = 'my_tag_2021';

-- Delete by tag name and tag time
DELETE FROM tag WHERE tag_name = 'my_tag_2021' AND tag_time < TO_DATE('2021-07-01', 'YYYY-MM-DD');
DELETE FROM tag WHERE tag_name = 'my_tag_2021' AND tag_time BETWEEN TO_DATE('2021-07-01', 'YYYY-MM-DD') AND TO_DATE('2021-07-02', 'YYYY-MM-DD');

-- Delete by time only
DELETE FROM tag WHERE tag_time <= TO_DATE('2021-07-01', 'YYYY-MM-DD');

-- Delete rollup by tag name
DELETE FROM tag ROLLUP WHERE tag_name = 'my_tag_2021';

-- Delete rollup by tag name and tag time
DELETE FROM tag ROLLUP WHERE tag_name = 'my_tag_2021' AND tag_time < TO_DATE('2021-07-01', 'YYYY-MM-DD');

-- Delete rollup by time only
DELETE FROM tag ROLLUP WHERE tag_time BETWEEN TO_DATE('2021-07-01', 'YYYY-MM-DD') AND TO_DATE('2021-07-02', 'YYYY-MM-DD');
```

* The time it takes for the deleted row to be physically deleted from the storage space after the deletion query is executed may vary depending on the situation of the DBMS.


## LOAD DATA INFILE

**load_data_infile_stmt:**

![load_data_infile_stmt](/images/sql/dml/load_data_infile_stmt.png)

```sql
load_data_infile_stmt: 'LOAD DATA INFILE' file_name 'INTO TABLE' table_name ( 'TABLESPACE' tbs_name )? ( 'AUTO' ( 'BULKLOAD' | 'HEADUSE' | 'HEADUSE_ESCAPE' ) )? ( ( 'FIELDS' | 'COLUMNS' ) ( 'TERMINATED BY' char )? ( 'ENCLOSED BY' char )? )? ( 'TRIM' ( 'ON' | 'OFF' ) )? ( 'IGNORE' number ( 'LINES' | 'ROWS' ) )? ( 'MAX_LINE_LENGTH' number )? ( 'ENCODED BY' coding_name )? ( 'ON ERROR' ( 'STOP' | 'IGNORE' ) )?
```

CSV format data files are read directly from the server, and tables and columns are created directly from the server according to the options and input them.
Each option is explained as follows

|Options|Description|
|--|--|
|AUTO mode_string<br><br>mode_string =<br><br>(BULKLOAD \| HEADUSE \| HEADUSE_ESCAPE)|Creates the corresponding table and automatically generates the column type (varchar type for automatic creation) and the column name.<br>BULKLOAD: Enters one row of data as one column. It is used for data that can not be divided into columns.<br>HEADUSE: Uses the column name as described in the first line of the data file as the column name of the table, and creates as many columns as there are in the line.<br>HEADUSE_ESCAPE: Similar to the HEADUSE option, but appends a '_' character to the front and back of the column name to avoid errors that can occur if the column name is the same as the reserved word in the DB. If a special character exists in the column name, changes it to '_'.|
|(FIELDS\|COLUMNS) TERMINATED BY 'term_char'<br><br>ENCLOSED BY 'enclose_char'|Specifies the delimiter (`term_char`) and enclosing character (`enclose_char`) for parsing the data line. For common CSV files, the delimiter is `,` and the enclosing character is `"`.|
|ENCODED BY coding_name<br>coding_name =<br>{ UTF8(default) \| MS949 \| KSC5601 \| EUCJP \| SHIFTJIS \| BIG5 \| GB231280 }|Specifies the encoding options for the data file. The default value is UTF-8.|
|TRIM (ON \| OFF)|Removes or maintains the empty space of the column. The default is ON.|
|IGNORE number (LINES \| ROWS)|Ignores data for a specified number of lines or lines. It is used to ignore header of CSV format file or ignore VCF header.|
|MAX_LINE_LENGTH|Specifies the maximum length of one line. The default value is 512K. If the data is larger, you can specify a larger value.|
|ON ERROR (STOP \| IGNORE)|Specifies the action to take when an error occurs during input. If it is STOP, input is stopped. If it is IGNORE, the line where error occurred is skipped and input is continued.<br>The default is IGNORE.|

```sql
-- Use default field delimiter(,)  field encloser (") to input data.
LOAD DATA INFILE '/tmp/aaa.csv' INTO TABLE Sample_data ;

-- Create NEWTABLE with one column and enter one line as one column.
LOAD DATA INFILE '/tmp/bbb.csv' INTO TABLE NEWTABLE AUTO BULKLOAD;

-- Create NEWTABLE using first line of csv as column information, and input it into table.
LOAD DATA INFILE '/tmp/bbb.csv' INTO TABLE NEWTABLE AUTO HEADUSE;

-- First line is ignored and field delimiter is ; and enclosing character is specified by '.
LOAD DATA INFILE '/tmp/ccc.csv' INTO TABLE Sample_data FIELDS TERMINATED BY ';' ENCLOSED BY '\'' IGNORE 1 LINES ON ERROR IGNORE;
```

* If the AUTO option is not used, all columns of the table must be created as VARCHAR or TEXT types.

## select


## Index

* [SELECT Syntax](#select-syntax)
* [SELECT without FROM](#select-without-from)
* [SET OPERATOR](#set-operator)
* [TARGET LIST](#target-list)
    * [CASE statement](#case-statement)
* [FROM](#from)
    * [SUBQUERY(INLINE VIEW)](#subqueryinline-view)
    * [STORED VIEW](#stored-view)
    * [JOIN(INNER JOIN)](#joininner-join)
    * [INNER JOIN and OUTER JOIN](#inner-join-and-outer-join)
    * [PIVOT](#pivot)
* [WHERE](#where)
    * [Use of SUBQUERY](#use-of-subquery)
    * [SEARCH Statement](#search-statement)
    * [ESEARCH Statement](#esearch-statement)
    * [NOT SEARCH Statement](#not-search-statement)
    * [REGEXP Statement](#regexp-statement)
    * [IN Statement](#in-statement)
    * [Use In Statement and SUBQUERY](#use-in-statement-and-subquery)
    * [BETWEEN Statement](#between-statement)
    * [RANGE Statement](#range-statement)
* [GROUP BY / HAVING](#group-by--having)
* [ORDER BY](#order-by)
* [SERIES BY](#series-by)
* [LIMIT](#limit)
* [DURATION](#duration)
* [SAVE DATA](#save-data)


SELECT is a syntax used to find, filter, and manipulate data from various tables in Machbase.

## SELECT Syntax

```sql
select_stmt UNION ALL select_stmt
```

```sql
SELECT target_list [FROM table_list]
[WHERE condition_expr]
[GROUP BY expr] [HAVING expr]
[ORDER BY expr [DESC]] [SERIES BY expr]
[LIMIT n[,n]]
[DURATION duration_expr];
```

In general, a `SELECT` statement uses a `FROM` clause. However, simple expressions can
also be executed without a `FROM` clause.

## SELECT without FROM

A `SELECT` statement without `FROM` does not read from a table. It returns one row for
constants, string literals, arithmetic expressions, and simple function results. This is
useful for quick connectivity checks or simple calculations.

```sql
select 1;
select 'alive';
select 1 + 2;
select abs(-7);
```

Each query returns a single row.

The following extended forms are not supported.

```sql
select distinct 1;
select 1 where 1 = 1;
select 1 order by 1;
select count(*);
select *;
```

Unsupported forms typically return the following error.

```text
ERR-02362: This statement is not supported.
```

`select *;` may return the following error.

```text
ERR-02039: No table specified in the target list.
```

`SELECT` without `FROM` is intended for single-row expression queries only. Aggregate
functions, sorting, conditions, periodic options, and hints are not supported.

## SET OPERATOR

Used when receiving the results of multiple Select queries as a single query result.
Machbase supports only the `UNION ALL` set operator. The set operator can be executed
only if the left and right Select statements are (1) the same or compatible types, (2)
the number of query results is the same, and if any of the two conditions does not match,
they are treated as errors.

Data type conversion and compatibility verification are performed based on the following criteria.
* Signed integer types and unsigned integer types are not compatible.
* The integer type is compatible with the real type, and the query result is converted to the real type and returned.
* Character types are compatible with different lengths.
* IPv6 type and IPv4 type are not compatible.
* Of the two SELECT statements, the column name of the left query is always used.

Examples

```sql
SELECT i1, i2 FROM table_1
UNION ALL
SELECT c1, c2 FROM table_2
```


## TARGET LIST

This is a **list of columns or subqueries** targeted by the Select statement .

The subquery used in the target list is treated as an error if it has two or more values ​​or two or more result columns, such as a subquery used in the WHERE clause.

```sql
SELECT i1, i2 ...
SELECT i1 (Select avg(c1) FROM t1), i2 ...
```

## CASE statement

```sql
CASE <simple_case_expression|searched_case_expression> [else_clause] END

simple_case_expression ::=
    expr WHEN comparison_expr THEN return_expr
        [WHEN comparison_expr THEN return_expr ...]

searched_case_expression ::=
    WHEN condtion_expr THEN return EXPR [WHEN condtion_expr THEN return EXPR ...]

else_clause ::=
    ELSE else_value_expr
```

This is an expression that supports the IF ... THEN ... ELSE block of a typical programming language. simple_case_expression is executed in the form of return_expr when one column or expression is equal to the value of comparison_expr followed by when, and this when ... then clause can be repeated as many times as desired.

searched_case_expression does not specify an expression after CASE but describes a conditional clause that includes a comparison operator in the when clause. If the result of each comparison operation is true, then the value of the then clause is returned. The else clause returns else_value if the value of the when clause is not satisfied (even if the expression is NULL).

```sql
select * from t1;
I1          I2
---------------------------
2           2
1           1
[2] row(s) selected.

select case i1 when 1 then 100 end from t1;
case i1 when 1 then 100 end
------------------------------
NULL
100
[2] row(s) selected.
```

In the simple_case_expression example, if the value of the i1 column is 2, NULL is returned.

```
select case when i1 > 0 then 100 when i1 > 1 then 200 end from t1;
case when i1 > 0 then 100 when i1 > 1 then 200 end
------------------------------------------
100
100
[2] row(s) selected.
```

Since searched_case_expression returns the first condition that satisfies the condition, 100 is returned, and the second condition is not executed.


## FROM

You can specify a table name or an Inline view in the FROM clause. To perform a join between tables, lists the table or Inline view separated by a comma (,).

```sql
FROM table_name
```

Retrieves data in the table specified by table_name.

### SUBQUERY(INLINE VIEW)

```sql
FROM (Select statement)
```

Retrievse data for the contents of the subquery enclosed in parentheses.

* Machbase server does not support correlated subqueries, so you can not reference columns in a subquery in an outer query.

### STORED VIEW

The `FROM` clause can also use the name of a stored VIEW created in advance with
`CREATE VIEW`. Unlike an inline view, a stored VIEW is a named logical object and
its metadata can be inspected with `DESC`, `SHOW VIEWS`, and `M$SYS_VIEWS`.

```sql
SELECT *
FROM v_customer
WHERE id = 100;
```

For creation, deletion, metadata, performance/limits, and Tag / `BINARY` examples,
see [VIEW](#view).

### JOIN(INNER JOIN)

```sql
JOIN(INNER JOIN)
```

Joins two tables, table_1 and table_2. An INNER JOIN can be used when three or more tables are listed, and both the search condition and the conditional clause are described in the WHERE clause.

```sql
SELECT t1.i1, t2.i1 FROM t1, t2 WHERE t1.i1 = t2.i1 AND t1.i1 > 1 AND t2.i2 = 3;
```

### INNER JOIN and OUTER JOIN

Supports ANSI style INNER JOIN, LEFT OUTER JOIN, and RIGHT OUTER JOIN. FULL OUTER JOIN is not supported.

```sql
FROM TABLE_1 [INNER|LEFT OUTER|RIGHT OUTER] JOIN TABLE_2 ON expression
```

The ON clause of the ANSI-style JOIN clause uses the conditional clause that is performed by the JOIN. If the WHERE clause in the OUTER JOIN query has a clause for an inner table (a table that is filled with NULL if the condition of the ON clause is not satisfied), the query is converted to an INNER JOIN.

```sql
SELECT t1.i1, t2.i1 FROM t1 LEFT OUTER JOIN t2 ON (t1.i1 = t2.i1) WHERE t2.i2 = 1;
```

The above query is converted to an INNER JOIN by the condition t2.i2 = 1 in the WHERE clause.

### PIVOT

* The PIVOT syntax is supported from Machbase version 5.6.

**pivot_clause:**

![pivot_clause](/images/sql/select/pivot_clause.png)


The PIVOT statement shows the aggregated results of GROUP BY output as ROW, rearranged into columns.

It is used in conjunction with the Inline view and is performed as follows.
* Performs GROUP BY on columns that are not used in the PIVOT clause of the inline view, and then performs aggregate functions on the values ​​listed in the PIVOT IN clause.
* The resulting grouping column and the aggregation result are rotated and displayed as columns.

For example, aggregate the value of each device from the data collected from various sensors.
The query that should be performed through the CASE statement can be expressed simply through the PIVOT statement.

```sql
-- w/o PIVOT
SELECT * FROM (
    SELECT
             regtime,
             SUM(CASE WHEN tagid = 'FRONT_AXIS_TORQUE' THEN dvalue ELSE 0 END)  AS front_axis_torque,
             SUM(CASE WHEN tagid = 'REAR_AXIS_TORQUE' THEN dvalue ELSE 0 END)  AS rear_axis_torque,
             SUM(CASE WHEN tagid = 'HOIST_AXIS_TORQUE' THEN dvalue ELSE 0 END)  AS hoist_axis_torque,
             SUM(CASE WHEN tagid = 'SLIDE_AXIS_TORQUE' THEN dvalue ELSE 0 END)  AS slide_axis_torque
    FROM     result_d
    WHERE    regtime BETWEEN TO_DATE('2018-12-07 00:00:00') AND TO_DATE('2018-12-08 05:00:00')
    GROUP BY regtime
) WHERE front_axis_torque >= 40 AND rear_axis_torque >= 20;

-- w/ PIVOT
SELECT * FROM (
    SELECT regtime, tagid, dvalue FROM result_d
    WHERE  regtime BETWEEN TO_DATE('2018-12-07 00:00:00') AND TO_DATE('2018-12-08 05:00:00')
) PIVOT (SUM(dvalue) FOR tagid IN ('FRONT_AXIS_TORQUE', 'REAR_AXIS_TORQUE', 'HOIST_AXIS_TORQUE', 'SLIDE_AXIS_TORQUE'))
WHERE front_axis_torque >= 40 AND rear_axis_torque >= 20;

-- Result
regtime                         'FRONT_AXIS_TORQUE'         'REAR_AXIS_TORQUE'          'HOIST_AXIS_TORQUE'         'SLIDE_AXIS_TORQUE'
------------------------------------------------------------------------------------------------------------------------------------------------------
2018-12-07 16:42:29 840:000:000 12158                       7244                        NULL                        NULL
2018-12-07 14:56:26 220:000:000 3308                        663                         NULL                        NULL
2018-12-07 12:20:13 844:000:000 3804                        113                         NULL                        NULL
2018-12-07 11:10:01 957:000:000 8729                        5384                        NULL                        NULL
2018-12-07 17:46:57 812:000:000 7500                        4559                        NULL                        NULL
2018-12-07 14:30:06 138:000:000 5080                        6817                        NULL                        -429
2018-12-07 13:09:20 464:000:000 5233                        1869                        -7253                       NULL
2018-12-07 15:43:03 539:000:000 7491                        4453                        NULL                        NULL
...
```


## WHERE

### Use of SUBQUERY

Subquery can be used for conditional statements. If the subquery returns more than one record in a clause except the IN clause, or if there is more than one result column in the subquery, it is not supported.

```sql
WHERE i1 = (SELECT MAX(c2) FROM T1)
```

Uses subquery by surrounding parentheses to the right of the conditional operator.

* Machbase server does not support correlated subqueries, so you can not reference columns in a subquery in an outer query.

### SEARCH Statement

The syntax is the same as for a regular database. However, a keyword index must be registered, and an additional search operation is possible by adding "SEARCH" as an operator keyword for text search.

```sql
-- drop table realdual;
create table realdual (id1 integer, id2 varchar(20), id3 varchar(20));

create keyword index idx1 on realdual (id2);
create keyword index idx2 on realdual (id3);

insert into realdual values(1, 'time time2', 'series series2');

select * from realdual;

select * from realdual where id2 search 'time';
select * from realdual where id3 search 'series' ;
select * from realdual where id2 search 'time' and id3 search 'series';
```

The results are as follows.

```sql
Mach> create table realdual (id1 integer, id2 varchar(20), id3 varchar(20));
Created successfully.

Mach> create keyword index idx1 on realdual (id2);
Created successfully.

Mach> create keyword index idx2 on realdual (id3);
Created successfully.

Mach> insert into realdual values(1, 'time time2', 'series series2');
1 row(s) inserted.

Mach> select * from realdual;
ID1         ID2                   ID3
------------------------------------------------------------
1           time time2            series series2
[1] row(s) selected.

Mach> select * from realdual where id2 search 'time';
ID1         ID2                   ID3
------------------------------------------------------------
1           time time2            series series2
[1] row(s) selected.

Mach> select * from realdual where id3 search 'series';
ID1         ID2                   ID3
------------------------------------------------------------
1           time time2            series series2
[1] row(s) selected.

Mach> select * from realdual where id2 search 'time' and id3 search 'series';
ID1         ID2                   ID3
------------------------------------------------------------
1           time time2            series series2
[1] row(s) selected.
```

### ESEARCH Statement

The ESEARCH statement is a search keyword that enables extended searches on ASCII text. For this extension, search for the desired pattern is performed using the % character. In this Like operation, if all the records are checked before the %, the advantage of ESEARCH is that the words can be found quickly even in this case. This feature can be very useful when looking for a part of an English string (an error string or code).

```sql
-- Example

select id2 from realdual where id2 esearch 'bbb%';
id2
--------------------------------------------
bbb ccc1
aaa bbb1

[2] row(s) selected.

-- Search pattern 'bbb%' also includes bbb1 in search results.


select id3 from realdual where id3 esearch '%cd%';
id3
--------------------------------------------
cdf def1
bcd/cdf1ad
abc, bcd1
[3] row(s) selected.

-- % character works in middle of search pattern as well as beginning and end.

select id3 from realdual where id3 esearch '%cd%';
id3
--------------------------------------------
cdf def1
bcd/cdf1ad
abc, bcd1
[3] row(s) selected.
```

### NOT SEARCH Statement

NOT SEARCH is a statement that returns true for records other than those found in the SEARCH statement.

NOT ESEARCH can not be used.

```sql
create table t1 (id integer, i2 varchar(10));
create keyword index t1_i2 on t1(i2);
insert into t1 values (1, 'aaaa');
insert into t1 values (2, 'bbbb');

select id from t1 where i2 not search 'aaaa';

id
--------------------------------------------
2
[1] row(s) selected.
```

### REGEXP Statement

The REGEXP statement is used to perform searches on data using regular expressions. In general, patterns of a particular column are filtered using regular expressions.

One thing to keep in mind is that you can not use indexes when using the REGEXP clause, so you must lower the overall search cost by putting index conditions on other columns in order to reduce the overall search scope.
If you want to check a specific pattern, use index by SEARCH or ESEARCH, and then use REGEXP again in a state where the total number of data is small, it helps to improve the efficiency of the whole system.

```sql
Mach>
create table realdual (id1 integer, id2 varchar(20), id3 varchar(20));
create table dual (id integer);
insert into dual values(1);
insert into realdual values(1, 'time1', 'series1 series21');
insert into realdual values(1, 'time2', 'series2 series22');
insert into realdual values(1, 'time3', 'series3 series32');


Mach> select * from realdual where id2 REGEXP 'time' ;
ID1         ID2                   ID3
------------------------------------------------------------
1           time3                 series3 series32
1           time2                 series2 series22
1           time1                 series1 series21
[3] row(s) selected.

Mach> select * from realdual where id2 REGEXP 'time[12]' ;
ID1         ID2                   ID3
------------------------------------------------------------
1           time2                 series2 series22
1           time1                 series1 series21
[2] row(s) selected.

Mach> select * from realdual where id2 REGEXP 'time[13]' ;
ID1         ID2                   ID3
------------------------------------------------------------
1           time3                 series3 series32
1           time1                 series1 series21
[2] row(s) selected.

Mach> select * from realdual where id2 regexp 'time[13]' and id3 regexp 'series[12]';
ID1         ID2                   ID3
------------------------------------------------------------
1           time1                 series1 series21
[1] row(s) selected.

Mach> select * from realdual where id2 NOT REGEXP 'time[12]';
ID1         ID2                   ID3
------------------------------------------------------------
1           time3                 series3 series32
[1] row(s) selected.

Mach> SELECT 'abcde' REGEXP 'a[bcd]{1,10}e' from dual;
'abcde' REGEXP 'a[bcd]{1,10}e'
---------------------------------
1
[1] row(s) selected.
```

### IN Statement

```sql
column_name IN (value1, value2,...)
```

The IN statement returns TRUE if it is satisfied in the value list. It is the same as the syntax linked by OR.

### Use In Statement and SUBQUERY

You can use a subquery to the right of the IN statement in the conditional statement. However, if you specify more than one column on the left side of the IN condition, it treats it as an error and checks whether the result set returned from the right subquery exists in the left column value.

```sql
WHERE i1 IN (Select c1 from ...)
```

* Machbase server does not support correlated subqueries, so you can not reference columns in a subquery in an outer query.

### BETWEEN Statement

```sql
column_name BETWEEN value1 AND value2
```

The BETWEEN statement returns TRUE if the value of column is in the range of value1 and value2.

### RANGE Statement

```sql
column_name RANGE duration_spec;

-- duration_spec : integer (YEAR | WEEK | HOUR | MINUTE | SECOND);
```

Provides a Range operator that allows you to easily specify a time condition for a given column. The Range operator specifies the time range from the current time as the target of the operation, rather than specifying a specific time (as specified by the BEFORE keyword). With this operator, you can easily retrieve result records within a desired time range.

```sql
select * from test where id < 2 and c1 range 1 hour;
ID          C1
-----------------------------------------------
1           2014-07-25 09:28:53 706:707:001
[1] row(s) selected.
```


## GROUP BY / HAVING

The GROUP BY clause is used to group the results of a SELECT statement on a specific column. It is used when sorting by group or by aggregating functions by using aggregate functions. Group means records having the same column value for the column specified in the GROUP BY clause.You can combine the HAVING clause after the GROUP BY clause to set the conditional expression for group selection. That is, of all the groups constituted by the GROUP BY clause, only the group satisfying the conditional expression specified in the HAVING clause is inquired.

```sql
SELECT ...
GROUP BY { col_name | expr } ,...[ HAVING <search_condition> ]

select id1, avg(id2) from exptab where id2 group by id1 order by id1;
Obtain average value of id2 based on id1 column.
```


## ORDER BY

The ORDER BY clause sorts the query results in ascending or descending order. If no sorting options such as ASC or DESC are specified, the ORDER BY clause sorts by default in ascending order. If the ORDER BY clause is not specified, the order of the records to be queried depends on the query.

```sql
SELECT ...
ORDER BY {col_name | expr} [ASC | DESC]

select id1, avg(id2) from exptab where id2 group by id1 order by id1;
Obtain average value of id2 based on id1 column.
```


## SERIES BY

The SERIES BY clause extracts the sorted result set as successive result values ​​satisfying the SERIES BY condition. If the ORDER BY clause is not specified, it generates the sorted result using the _ARRIVAL_TIME column value. Therefore, if you use the GROUP BY clause or the query for a volatile table or lookup table that does not have the _ARRIVAL_TIME column, you must use the ORDER BY clause do.

The result values ​​that satisfy the conditional clause will have the return value of the same SERIESNUM () function.

```sql
For example, for the following data

CREATE TABLE T1 (C1 INTEGER, C2 INTEGER);
INSERT INTO T1 VALUES (0, 1);

INSERT INTO T1 VALUES (1, 2);

INSERT INTO T1 VALUES (2, 3);

INSERT INTO T1 VALUES (3, 2);

INSERT INTO T1 VALUES (4, 1);

INSERT INTO T1 VALUES (5, 2);

INSERT INTO T1 VALUES (6, 3);

INSERT INTO T1 VALUES (7, 1);


The following query produces the following output:

SELECT C1,C2 FROM T1 ORDER BY C1 SERIES BY C2>1;
C1          C2
---------------------------
1           2
2           3
3           2
5           2
6           3

If you want to know the RANGE value of C1 where the value of the C2 column is larger than 1, you can determine the range by outputting to which group each record is included with the SERIESNUM function.
```


## LIMIT

The LIMIT clause is used to limit the number of records to be output. You can specify an integer to output from the first row to the last row of the result set

```sql
LIMIT [offset,] row_count

select id1, avg(id2) from exptab where id2 group by id1 order by id1 LIMIT 10;
```


## DURATION

DURATION is a keyword that allows you to easily determine the data retrieval scope based on _arrival_time. Used with the BEFORE statement to set a specific range of data at a specific point in time. By using this DURATION, search performance can be dramatically increased and the system load can be dramatically reduced. For more detailed usage, please refer to the following.

```sql
DURATION Number TimeSpec [BEFORE/AFTER Number TimeSpec]
DURATION FROM expr TO expr
TimeSpec : YEAR | MONTH | WEEK |  DAY | HOUR | MINUTE | SECOND
```

`DURATION FROM expr TO expr` selects an explicit `_arrival_time` range. `expr` can be a
datetime expression such as `TO_DATE(value, format)`.

```sql
create table t8(i1 integer);
insert into t8 values(1);
insert into t8 values(2);

select i1 from t8;

-- Without BEFORE clause
select i1 from t8 duration 2 second;
select i1 from t8 duration 1 minute;
select i1 from t8 duration 1 hour;
select i1 from t8 duration 1 day;
select i1 from t8 duration 1 week;
select i1 from t8 duration 1 month;
select i1 from t8 duration 1 year;

-- Using full DURATION statement
select i1 from t8 duration 1 second before 1 day;
select i1 from t8 duration 1 minute before 1 day;
select i1 from t8 duration 1 hour before 1 day;
select i1 from t8 duration 1 day before 1 day;
select i1 from t8 duration 1 week before 1 day;
select i1 from t8 duration 1 month before 1 day;
select i1 from t8 duration 1 year before 1 day;

-- Using explicit range
select i1 from t8
duration from to_date('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
       to to_date('2030-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

The results are as follows.

```sql
Mach> create table t8(i1 integer);
Created successfully.

Mach> insert into t8 values(1);
1 row(s) inserted.

Mach> insert into t8 values(2);
1 row(s) inserted.

Mach> select i1 from t8;
i1
--------------
2
1
[2] row(s) selected.

## BEFORE 절 없이
Mach> select i1 from t8 duration 2 second;
i1
--------------
2
1
[2] row(s) selected.

Mach> select i1 from t8 duration 1 minute;
i1
--------------
2
1
[2] row(s) selected.

Mach> select i1 from t8 duration 1 hour;
i1
--------------
2
1
[2] row(s) selected.

Mach> select i1 from t8 duration 1 day;
i1
--------------
2
1
[2] row(s) selected.

Mach> select i1 from t8 duration 1 week;
i1
--------------
2
1
[2] row(s) selected.

Mach> select i1 from t8 duration 1 month;
i1
--------------
2
1
[2] row(s) selected.

Mach> select i1 from t8 duration 1 year;
i1
--------------
2
1
[2] row(s) selected.

-- Using full DURATION statement
Mach> select i1 from t8 duration 1 second before 1 day;
i1
--------------
[0] row(s) selected.

Mach> select i1 from t8 duration 1 minute before 1 day;
i1
--------------
[0] row(s) selected.

Mach> select i1 from t8 duration 1 hour before 1 day;
i1
--------------
[0] row(s) selected.

Mach> select i1 from t8 duration 1 day before 1 day;
i1
--------------
[0] row(s) selected.

Mach> select i1 from t8 duration 1 week before 1 day;
i1
--------------
[0] row(s) selected.

Mach> select i1 from t8 duration 1 month before 1 day;
i1
--------------
[0] row(s) selected.

Mach> select i1 from t8 duration 1 year before 1 day;
i1
--------------
[0] row(s) selected.
```


## SAVE DATA

Saves the results of the query directly into the CSV data file.

```sql
SAVE DATA INTO 'file_name.csv' [HEADER ON|OFF] [(FIELDS | COLUMNS) [TERMINATED BY 'char'] [ENCLOSED BY 'char']] [ENCODED BY coding_name] AS select query;
```

The options are described below.

|Options|Description|
|--|--|
|HEADER (ON\|OFF)|Decides whether to write column names on the first line of the CSV file. The default is OFF.|
|(FIELDS\|COLUMNS) TERMINATED BY 'term_char'<br><br>ENCLOSED BY 'enclose_char'|Specifies the field delimiter and enclosing character of the CSV file to be created.|
|ENCODED BY coding_name<br><br>coding_name = ( UTF8, MS949, KSC5601, EUCJP, SHIFTJIS, BIG5, GB231280 )|Specifies the encoding format of the output data file. The default value is UTF8.|

```sql
SAVE DATA INTO '/tmp/aaa.csv' AS select * from t1;
-- Execute select statement and write result to '/tmp/aaa.csv' file in csv format.

SAVE DATA INTO '/tmp/ccc.csv' HEADER ON FIELDS TERMINATED BY ';' ENCLOSED BY '\'' ENCODED BY MS949 AS select * from t1 where i1 > 100;
-- Execute select statement and write result to /tmp/ccc.csv file. Specify field delimiter and enclosing character, and set encoding of stored data to MS949.
```

## select-hint


# Index

* [Introduction](#overview)
* [PARALLEL](#parallel)
* [NOPARALLEL](#noparallel)
* [FULL](#full)
* [NO_INDEX](#no_index)
* [ROLLUP_TABLE](#rollup_table)
* [RID_RANGE](#rid_range)
* [SCAN_FORWARD, SCAN_BACKWARD](#scan_forward-scan_backward)


Hints that can be used in a SELECT queries are described.

##  PARALLEL

Specifies parallel factor for parallel query execution.

```sql
SELECT /*+ PARALLEL(table_name, parallel_factor) */ ...
```

```sql
Mach> CREATE TABLE log_parallel_test (sensor VARCHAR(32), frequency DOUBLE, value DOUBLE, ts DATETIME);
Mach> CREATE INDEX idx_ts ON log_parallel_test (ts);

Mach> EXPLAIN SELECT /*+ PARALLEL(log_parallel_test, 8) */ sensor, frequency, avg(value)
      FROM log_parallel_test
      WHERE ts >= TO_DATE('2007-07-01', 'YYYY-MM-DD') and ts <= TO_DATE('2007-07-31', 'YYYY-MM-DD')
      GROUP BY sensor, frequency;

PLAN
------------------------------------------------------------------------------------
 PROJECT
  GROUP AGGREGATE
   PARALLEL INDEX SCAN
    *BITMAP RANGE (table id:3, column id:4, index id:4)
    [KEY RANGE]
     * ts >= TO_DATE('2007-07-01', 'YYYY-MM-DD')
     * ts <= TO_DATE('2007-07-31', 'YYYY-MM-DD')
[7] row(s) selected.
```


##  NOPARALLEL

Does not perform in parallel.

```sql
SELECT /*+ NOPARALLEL(table_name) */ ...
```

```sql
Mach> CREATE TABLE log_parallel_test (sensor VARCHAR(32), frequency DOUBLE, value DOUBLE, ts DATETIME);
Mach> CREATE INDEX idx_ts ON log_parallel_test (ts);

Mach> EXPLAIN SELECT /*+ NOPARALLEL(log_parallel_test) */ sensor, frequency, avg(value)
      FROM log_parallel_test
      WHERE ts >= TO_DATE('2007-07-01', 'YYYY-MM-DD') and ts <= TO_DATE('2007-07-31', 'YYYY-MM-DD')
      GROUP BY sensor, frequency;

PLAN
------------------------------------------------------------------------------------
 PROJECT
  GROUP AGGREGATE
   INDEX SCAN
    *BITMAP RANGE (table id:5, column id:4, index id:6)
    [KEY RANGE]
     * ts >= TO_DATE('2007-07-01', 'YYYY-MM-DD')
     * ts <= TO_DATE('2007-07-31', 'YYYY-MM-DD')
[7] row(s) selected.
```


##  FULL

Does not use INDEX SCAN.

```sql
SELECT /*+ FULL(table_name) */ ...
```

```sql
Mach> CREATE TABLE log_full_test (sensor VARCHAR(32), I1 INTEGER);
Mach> CREATE INDEX idx_I1 ON log_full_test (I1);

Mach> EXPLAIN SELECT * FROM log_full_test WHERE I1 = 1;
PLAN
------------------------------------------------------------------------------------
 PROJECT
  INDEX SCAN
   *BITMAP RANGE (table id:14, column id:2, index id:15)
   [KEY RANGE]
    * I1 = 1
[5] row(s) selected.

Mach> EXPLAIN SELECT /*+ FULL(log_full_test) */ * FROM log_full_test WHERE I1 = 1;
PLAN
------------------------------------------------------------------------------------
 PROJECT
  FULL SCAN
[2] row(s) selected.
```


##  NO_INDEX

Does not use the corresponding INDEX.

```sql
SELECT /*+ NO_INDEX(table_name,index_name) */ ...
```

```sql
Mach> CREATE TABLE log_no_index_test (sensor VARCHAR(32), I1 INTEGER, I2 INTEGER);
Mach> CREATE INDEX idx_I1 ON log_no_index_test (I1);
Mach> CREATE INDEX idx_I2 ON log_no_index_test (I2);

Mach> EXPLAIN SELECT * FROM log_no_index_test WHERE I1 = 1;
PLAN
------------------------------------------------------------------------------------
 PROJECT
  INDEX SCAN
   *BITMAP RANGE (t:7, c:1, i:8) with BLOOMFILTER
   [KEY RANGE]
    * I1 = 1
[5] row(s) selected.

Mach> EXPLAIN SELECT /*+ NO_INDEX(log_no_index_test,idx_I1) */ * FROM log_no_index_test WHERE I1 = 1;
PLAN
------------------------------------------------------------------------------------
 PROJECT
  FULL SCAN
[2] row(s) selected.

Mach> EXPLAIN SELECT * FROM log_no_index_test WHERE I1 = 1 or I2 = 2;
PLAN
------------------------------------------------------------------------------------
 PROJECT
  INDEX SCAN
   INDEX (OR)
    *BITMAP RANGE (table id:21, column id:2, index id:22)
    *BITMAP RANGE (table id:21, column id:3, index id:23)
   [KEY RANGE]
    * I1 = 1 or I2 = 2
[7] row(s) selected.

Mach> EXPLAIN SELECT /*+ NO_INDEX(log_no_index_test, idx_I1) */ * FROM log_no_index_test WHERE I1 = 1 or I2 = 2;
PLAN
------------------------------------------------------------------------------------
 PROJECT
  FULL SCAN
[2] row(s) selected.

Mach> EXPLAIN SELECT * FROM log_no_index_test WHERE I1 = 1 and I2 = 2;
PLAN
------------------------------------------------------------------------------------
 PROJECT
  INDEX SCAN
   *BITMAP RANGE (table id:21, column id:2, index id:22)
   *BITMAP RANGE (table id:21, column id:3, index id:23)
   [KEY RANGE]
    * I1 = 1
    * I2 = 2
[7] row(s) selected.

Mach> EXPLAIN SELECT /*+ NO_INDEX(log_no_index_test, idx_I1) */ * FROM log_no_index_test WHERE I1 = 1 and I2 = 2;

PLAN
------------------------------------------------------------------------------------
 PROJECT
  INDEX SCAN
   *BITMAP RANGE (table id:21, column id:3, index id:23)
   [KEY RANGE]
    * I2 = 2
   [FILTER]
    * I1 = 1
[7] row(s) selected.
Elapsed time: 0.001
Mach>
Mach>
Mach> EXPLAIN SELECT /*+ NO_INDEX(log_no_index_test, idx_I2) */ * FROM log_no_index_test WHERE I1 = 1 and I2 = 2;

PLAN
------------------------------------------------------------------------------------
 PROJECT
  INDEX SCAN
   *BITMAP RANGE (table id:21, column id:2, index id:22)
   [KEY RANGE]
    * I1 = 1
   [FILTER]
    * I2 = 2
[7] row(s) selected.
```


##  ROLLUP_TABLE

Forces a specific rollup table when multiple rollups match. If the hint is present, it always takes precedence over automatic selection.

```sql
SELECT /*+ ROLLUP_TABLE(rollup_table_name) */ ...
```

- Without the hint, the engine prefers an unfiltered rollup among candidates with the same interval/value column/JSON path.
- Use the hint when a filtered rollup must be selected.
- When using `FIRST()`/`LAST()`, point the hint to an `EXTENSION` rollup.

```sql
SELECT /*+ ROLLUP_TABLE(_tag_rollup_cond_1s) */
       rollup('sec', 30, time) AS rt, AVG(value), COUNT(value)
FROM   tag_bulk
WHERE  name = 'dev9'
  AND  time BETWEEN '2020-01-02 00:00:00' AND '2020-01-02 00:10:00'
GROUP BY rt
ORDER BY rt;
```


##  RID_RANGE

Runs within RID range.

```sql
SELECT /*+ RID_RANGE(table_name,number,number) */ ...
```

```sql
Mach> SELECT /*+ RID_RANGE(TEST,45,50) */ _RID, * FROM TEST;
_RID                 I1
------------------------------------
49                   1
48                   1
47                   1
46                   1
45                   1
[5] row(s) selected.
```


##  SCAN_FORWARD, SCAN_BACKWARD

It specifies the direction of scanning for LOG table. With SCAN_FORWARD, the oldest record input is retrived first, whereas with SCAN_BACKWARD, the newest record input is retrieved first.

It affects LOG tables in standard edition only.

```sql
SELECT /*+ SCAN_FORWARD(table_name) */ ...
SELECT /*+ SCAN_BACKWARD(table_name) */ ...
```

```sql
Mach> SELECT /*+ SCAN_FORWARD(mytbl) */  _ARRIVAL_TIME, VALUE FROM mytbl LIMIT 10;
_ARRIVAL_TIME                   VALUE
----------------------------------------------------------------
2017-01-01 00:00:49 500:000:000 0
2017-01-01 00:01:39 500:000:000 1
2017-01-01 00:02:29 500:000:000 2
2017-01-01 00:03:19 500:000:000 3
2017-01-01 00:04:09 500:000:000 4
2017-01-01 00:04:59 500:000:000 5
2017-01-01 00:05:49 500:000:000 6
2017-01-01 00:06:39 500:000:000 7
2017-01-01 00:07:29 500:000:000 8
2017-01-01 00:08:19 500:000:000 9
[10] row(s) selected.

Mach> SELECT /*+ SCAN_BACKWARD(mytbl) */ _ARRIVAL_TIME, VALUE FROM mytbl LIMIT 10;
_ARRIVAL_TIME                   VALUE
----------------------------------------------------------------
2017-02-27 20:53:19 500:000:000 9
2017-02-27 20:52:29 500:000:000 8
2017-02-27 20:51:39 500:000:000 7
2017-02-27 20:50:49 500:000:000 6
2017-02-27 20:49:59 500:000:000 5
2017-02-27 20:49:09 500:000:000 4
2017-02-27 20:48:19 500:000:000 3
2017-02-27 20:47:29 500:000:000 2
2017-02-27 20:46:39 500:000:000 1
2017-02-27 20:45:49 500:000:000 0
[10] row(s) selected.
```

## time-expressions


## Overview

Relative time expressions let you describe offsets from a known timestamp directly inside SQL statements. They are designed for operators who need to filter recent telemetry, schedule future jobs, or align time series windows without calling helper functions.

> **Note**: This feature is supported from Machbase version 8.0.50 or later.

## Quick Start

1. Find records from the last hour:
   ```sql
   SELECT * FROM sensor_log WHERE event_time > now - 1h;
   ```
2. Look ahead two days and six hours:
   ```sql
   SELECT * FROM maintenance_plan WHERE planned_at < now + 2d6h;
   ```
3. Combine segments for sub-second precision:
   ```sql
   SELECT to_char(now + 3s125ms10us4ns, 'YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn');
   ```

## Syntax Summary

- A literal is one or more `<number><unit>` segments written back-to-back with no spaces.
- Units are lowercase. Separate magnitudes by concatenation: `2h30m`.
- Prefix with `+` or `-`, or use arithmetic (`now - 90m`, `sample_time + 15s`).
- When a numeric literal lacks a unit, Machbase treats the value as nanoseconds.
- Relative literals evaluate to an `INTERVAL`. Adding or subtracting them to/from a `DATETIME` produces another `DATETIME`.

## Supported Units

| Suffix | Meaning          | Example | Equivalent duration |
|--------|------------------|---------|---------------------|
| `ns`   | nanoseconds      | `500ns` | 500 nanoseconds     |
| `us`   | microseconds     | `20us`  | 0.00002 seconds     |
| `ms`   | milliseconds     | `15ms`  | 0.015 seconds       |
| `s`    | seconds          | `45s`   | 45 seconds          |
| `m`    | minutes          | `30m`   | 30 minutes          |
| `h`    | hours            | `12h`   | 12 hours            |
| `d`    | days             | `7d`    | 7 days              |
| `w`    | weeks            | `2w`    | 14 days             |

> **Note**: Months and years are not supported because their length is not constant. Using unsupported suffixes (for example, `1y`, `1mo`) raises an invalid time expression error (`ERR-02034`).

## Building Compound Literals

- Write the largest unit first to improve readability: `5d4h30m`.
- Omit segments that are zero; `4h15m` is preferred over `4h15m0s`.
- Segment order can vary, but consistent ordering reduces mistakes. `1h30m` and `30m1h` evaluate to the same interval.
- For long intervals, consider grouping with underscores for readability when possible inside SQL string literals: `'1d12h_30m'` is not allowed as a literal, but you can add a comment (`/* +1d12h30m */`) or store the literal in a SQL variable for documentation.

## Usage Patterns

### Filtering Windows of Time

```sql
-- Records in the most recent 24 hours
SELECT *
  FROM rtrollup
 WHERE time BETWEEN now - 1d AND now;

-- Alerts raised within the last 10 minutes
SELECT alert_id, level, occurred_at
  FROM alert_log
 WHERE occurred_at >= sysdate - 10m;
```

### Scheduling Future Operations

```sql
-- Tasks to execute in the next business day plus two hours
SELECT job_id, scheduled_at
  FROM job_queue
 WHERE scheduled_at <= now + 1d2h;

-- Insert maintenance schedule 30 minutes from now
INSERT INTO device_schedule (device_id, maintenance_due)
VALUES ('device-001', now + 30m);
```

### Time-based Filtering and Joins

```sql
-- Select data within a specific time window
SELECT device_id, ts, value
  FROM metrics_stream
 WHERE ts BETWEEN now - 15m AND now
   AND device_id = 'sensor-01';

-- Join two sources using relative offsets
SELECT a.ts, a.value AS raw_value, b.value AS calibrated
  FROM raw_metrics a
  JOIN calibration b
    ON b.ts BETWEEN a.ts - 500ms AND a.ts + 500ms;
```

### DATETIME Values and Casting

```sql
SELECT to_char(to_date('2024-05-01', 'YYYY-MM-DD') + 3d,
               'YYYY-MM-DD');                              -- 2024-05-04
SELECT to_char(to_date('2024-05-01 08:00:00',
                       'YYYY-MM-DD HH24:MI:SS') - 4h15m,
               'YYYY-MM-DD HH24:MI:SS');                   -- 2024-05-01 03:45:00
SELECT to_char(to_date('2024-05-01', 'YYYY-MM-DD') + 2h30m45s250ms,
               'YYYY-MM-DD HH24:MI:SS mmm');               -- 2024-05-01 02:30:45 250
```

String literals are not implicitly cast to `DATETIME` for interval arithmetic. Convert
them with `TO_DATE` first.

### Mixing with Plain Numbers

```sql
-- Adds one exact second because numeric literal defaults to nanoseconds
SELECT event_time + 1000000000 AS event_time_plus_1s
  FROM events;

-- Subtracts 250 nanoseconds
SELECT event_time - 250 AS event_time_minus_250ns
  FROM events;
```

## Behaviour and Limitations

- Precision is capped at nanoseconds. Values beyond 64-bit range overflow.
- Arithmetic follows standard precedence: parentheses first, multiplication/division, then addition/subtraction. Use parentheses when chaining multiple operations.
- Comparisons involving intervals use the resulting `DATETIME` values. Intervals alone cannot appear in `ORDER BY` clauses.
- The feature is available in standard edition builds. Check release notes for availability in older versions.

## Error Handling

| Scenario                               | Error Code                | Resolution                                   |
|----------------------------------------|---------------------------|----------------------------------------------|
| Unsupported suffix (`1y`, `5mo`)       | `ERR-02034` invalid time expression | Replace with supported units (`30d`, etc.).  |
| Missing unit (`now + 10`)              | Interpreted as nanoseconds | Add explicit suffix if minutes or seconds intended. |
| Overflowing literal (`1000000d`)       | `ERR_OVERFLOW_INTERVAL`   | Reduce magnitude or break the logic into loops. |
| Non-numeric characters (`1h3xm`)       | Invalid time expression   | Fix the typo (`1h3m`).                       |

## Best Practices

- Standardize on lowercase suffixes across your team scripts.
- Store frequently used offsets in configuration tables for reuse and auditing.
- Comment complex expressions to aid future maintenance (`-- subtract 1 business week`).
- Validate application inputs when constructing literals dynamically to avoid injection of unsupported suffixes.

## Troubleshooting Checklist

- **Unexpected range**: Print both `now` and the computed boundary to verify the offset.
- **Wrong unit**: Remember plain numbers are nanoseconds; append `s`, `m`, or `h` for human-readable units.
- **Function interaction**: When combining with window functions or aggregate filters, evaluate the literal in a subquery to ensure it resolves once per statement.

## Frequently Asked Questions

- **Can I chain relative literals with `ADD_TIME`?** Yes. `ADD_TIME(now, '0/0/0 0:15:0') + 30s` combines function-based and literal offsets.
- **Can I store literals in variables?** Relative time literals are evaluated at query execution time and cannot be stored in variables. However, you can use them directly in repeated queries.
- **How do I subtract business days?** Relative literals operate on absolute durations. Implement business-day rules in application logic or reference calendar tables.

## Reference Cheat Sheet

```
Pattern          Meaning
--------------  --------------------------------------------
now - 5m        Timestamp exactly five minutes ago
sysdate + 1d    Tomorrow (24 hours after system timestamp)
col_ts + 90s    Column value shifted by 90 seconds
TO_DATE('2024-01-01','YYYY-MM-DD') + 2w  Adds 14 days to the date value
value + 250     Adds 250 nanoseconds to `value`
```

Relative time expressions offer precise, readable temporal arithmetic without helper functions. Use them wherever expressions are supported—`WHERE` clauses, computed columns, projections, or procedural code—to keep your Machbase analytics concise and maintainable.

## user-manage


# Index

* [CREATE USER](#create-user)
* [DROP USER](#drop-user)
* [ALTER USER](#alter-user)
* [PASSWORD POLICY](#password-policy)
* [Generate AUTH KEY Files](#generate-auth-key-files)
* [Create a User with AUTH KEY](#create-a-user-with-auth-key)
* [Manage AUTH KEY](#manage-auth-key)
* [Query AUTH KEY Metadata](#query-auth-key-metadata)
* [CONNECT](#connect)
* [GRANT/REVOKE](#grantrevoke)
* [Managing User Example](#managing-user-example)


## CREATE USER

**create_user_stmt:**

![create_user_stmt](/images/sql/user/create_user_stmt.png)

```sql
create_user_stmt ::= 'CREATE USER' user_name 'IDENTIFIED BY' password
```

The syntax for creating a user is:

```sql
-- Example
CREATE USER new_user IDENTIFIED BY password
```

To specify a password policy at the same time, use the extended syntax below.

```sql
CREATE USER user_name IDENTIFIED BY password PASSWORD POLICY { NONE | LOW | HIGH }
```

Examples:

```sql
CREATE USER app_user IDENTIFIED BY "Aa!StrongPwd1" PASSWORD POLICY LOW;
CREATE USER ops_user IDENTIFIED BY "Bb@StrongPwd2" PASSWORD POLICY HIGH;
```
User names are converted to uppercase when they are created. For example,
`CREATE USER app_user ...` is stored and displayed as `APP_USER` in metadata tables and
`V$` views. Later connection and privilege statements refer to the same user name.


## DROP USER

**drop_user_stmt:**

![drop_user_stmt](/images/sql/user/drop_user_stmt.png)

```sql
drop_user_stmt ::= 'DROP USER' user_name
```

The syntax for deleting a user is as follows. The SYS user can not be deleted, and if there is a table already created by the user to be deleted, an error is displayed.

```sql
-- Example
DROP USER old_user
```


## ALTER USER

**alter_user_pwd_stmt:**

![alter_user_pwd_stmt](/images/sql/user/alter_user_pwd_stmt.png)

```sql
alter_user_pwd_stmt ::= 'ALTER USER' user_name 'IDENTIFIED BY' password
```

The user can change the password through the following syntax.

```sql
-- Example
ALTER USER user1 IDENTIFIED BY password
```

You can also change the password policy while changing the password.

```sql
ALTER USER user_name IDENTIFIED BY password PASSWORD POLICY { NONE | LOW | HIGH }
```

When changing the policy, specify a new password together with the policy. A policy-only statement such as `ALTER USER user_name PASSWORD POLICY HIGH` is not allowed.


## PASSWORD POLICY

Password policy validates password strength for `CREATE USER` and `ALTER USER ... IDENTIFIED BY ...`. If no policy is specified, `NONE` is used for backward compatibility.

Policy levels:

- `NONE`
  - No password strength restriction is applied.
  - Password expiration time (`VALID_BEFORE`) is `NULL`.
- `LOW`
  - The password must be at least 10 characters long.
  - The password must include uppercase letters, lowercase letters, and special characters.
  - Five or more contiguous digits, increasing or decreasing digit sequences, and keyboard sequences are not allowed.
  - Password expiration time (`VALID_BEFORE`) is `NULL`.
- `HIGH`
  - All `LOW` rules are applied.
  - The current password and the most recent 24 historical passwords cannot be reused.
  - The expiration time (`VALID_BEFORE`) is automatically set to 90 days after the password is set.

Policy examples:

```sql
CREATE USER user1 IDENTIFIED BY "Aa!StrongPwd1";
CREATE USER user2 IDENTIFIED BY "Bb@StrongPwd2" PASSWORD POLICY LOW;
CREATE USER user3 IDENTIFIED BY "Cc#StrongPwd3" PASSWORD POLICY HIGH;

ALTER USER user2 IDENTIFIED BY "Dd$NewPwd44";
ALTER USER user2 IDENTIFIED BY "Ee%NewPwd55" PASSWORD POLICY LOW;
ALTER USER user3 IDENTIFIED BY "Ff#NewPwd66" PASSWORD POLICY NONE;
```

Notes:

- `ALTER USER ... IDENTIFIED BY ...` validates the new password with the policy currently stored for that user.
- `ALTER USER ... IDENTIFIED BY ... PASSWORD POLICY ...` validates the new password with the new policy.
- When a policy is set to `HIGH`, or when the password of a `HIGH` policy user is changed, `VALID_BEFORE` is updated to 90 days from the current time.
- When a policy is set to `LOW` or `NONE`, `VALID_BEFORE` is updated to `NULL`.
- An expired account cannot log in, so the user cannot change the password with that account. Reset the password from an administrator account.

You can check the policy and expiration time in `M$SYS_USERS`.

```sql
SELECT USER_ID, NAME, PWD_POLICY_LEVEL, VALID_BEFORE
FROM M$SYS_USERS;
```

`PWD_POLICY_LEVEL` means `0 = NONE`, `1 = LOW`, and `2 = HIGH`. `VALID_BEFORE` is displayed in `YYYY-MM-DD` format when it has a value.
## Generate AUTH KEY Files

> **Note**: The following behavior is supported from Machbase 8.5 or later.

AUTH KEY authentication uses a client-side private key file and a public key registered
to the Machbase user. In normal operation, generate the key pair with `openssl`, keep the
private key on the client host, and register only the public key in Machbase.

Supported algorithms and key sizes are as follows.

| Public key algorithm | Supported key parameters | Supported signature scheme | Hash |
| --- | --- | --- | --- |
| ECDSA | P-256, P-384, P-521 | `ECDSA` | SHA-256 |
| RSA | 2048, 3072, 4096 bits | `RSA_PKCS1_V15` | SHA-256 |
| RSA | 2048, 3072, 4096 bits | `RSA_PSS` | SHA-256 |

If `AUTH_SIG_SCHEME` is omitted, Machbase uses the default scheme for the key algorithm.

- ECDSA key: `ECDSA`
- RSA key: `RSA_PKCS1_V15`

To use RSA-PSS, specify `AUTH_SIG_SCHEME=RSA_PSS` in the client connection options.
Authentication fails if the registered public key type does not match the requested
signature scheme.

ECDSA P-256 key example:

```bash
openssl ecparam -name prime256v1 -genkey -noout -out app_user_ecdsa.key
openssl ec -in app_user_ecdsa.key -pubout -out app_user_ecdsa.pub
chmod 600 app_user_ecdsa.key
```

ECDSA P-384 and P-521 key examples:

```bash
openssl ecparam -name secp384r1 -genkey -noout -out app_user_ecdsa_p384.key
openssl ec -in app_user_ecdsa_p384.key -pubout -out app_user_ecdsa_p384.pub

openssl ecparam -name secp521r1 -genkey -noout -out app_user_ecdsa_p521.key
openssl ec -in app_user_ecdsa_p521.key -pubout -out app_user_ecdsa_p521.pub
```

RSA 2048-bit key example:

```bash
openssl genrsa -out app_user_rsa.key 2048
openssl rsa -in app_user_rsa.key -pubout -out app_user_rsa.pub
chmod 600 app_user_rsa.key
```

To use a 3072-bit or 4096-bit RSA key, pass `3072` or `4096` as the last argument of
`openssl genrsa`.

To embed the public key in SQL, convert the PEM file into a single SQL string with
escaped line breaks.

```bash
awk '{printf "%s\\n", $0}' app_user_ecdsa.pub
```

Use the command output as the `key` value in `CREATE USER ... WITH AUTH KEY` or
`ALTER USER ... ADD AUTH KEY`.

The following example creates a registration SQL file from the generated public key.

```bash
KEY_ESCAPED=$(awk '{printf "%s\\n", $0}' app_user_ecdsa.pub)

cat > add_app_user_key.sql <<EOF
ALTER USER app_user ADD AUTH KEY (
    key='${KEY_ESCAPED}',
    valid_before='2047-12-31',
    comment='openssl generated ecdsa key'
);
EOF
```

## Create a User with AUTH KEY

> **Note**: The following behavior is supported from Machbase 8.5 or later.

Machbase can register an AUTH KEY for public-key challenge authentication together with password
authentication.

```sql
CREATE USER app_user IDENTIFIED BY 'App#1234'
WITH AUTH KEY (
    key='-----BEGIN PUBLIC KEY-----\nMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEshxcrSmtosaqWjhRkOoAw4v3QWqL\ns3OFN2jbJrustEc12uAn/IdtTG94KK69bY7DWl80pzQ48dNL+ENXe8PT3g==\n-----END PUBLIC KEY-----\n',
    valid_before='2047-12-31',
    comment='initial key'
);
```

Notes:

- `key` must contain a PEM public key.
- In SQL text, PEM line breaks can be written as `\n`.
- `valid_before` uses the `YYYY-MM-DD` format.
- `valid_before` does not accept a datetime value with a time portion such as
  `YYYY-MM-DD HH24:MI:SS`.
- `comment` is required by the current AUTH KEY syntax.
- The first key created by `CREATE USER ... WITH AUTH KEY` is registered as active
  (`ACTIVATED=1`).
- A user may own both a password and one or more AUTH KEY entries. The actual
  authentication method is chosen by the client's `AUTH_MODE`, and there is no automatic
  fallback from one method to the other on failure.

## Manage AUTH KEY

### Add AUTH KEY

```sql
ALTER USER app_user ADD AUTH KEY (
    key='-----BEGIN RSA PUBLIC KEY-----\nMIIBCgKCAQEAqO+tddiAQzsT8iajPy5QJPamIlyq2zB01wgHSTs3OOrvw0uKoFQD\ncqKaDzRya73LETXIEev3nwhGCnG4SjedMHj3EH9/rRJphFtv/dzw0OHum/UhVulR\nIXUYzrTbKPTQ+qyjS8UXTteMncf9OOh4AQyS4+iJW+U344fxymR8USRgZ25N9jhf\n2gkKnn5YSPZHf8ZHQGeA7OXANBwPmH5dQwfqghXRa7Nk1hmkIAnQQXCBJW/Lin+x\nwQfqv8DVwNaiziz77voPwaeD5akq1JYWvcPlOnh+NN3tpu5gudke/t/In4NFJ3W9\n4unVcYIfxcdDSoht3AMObGmuDazOjQJFGQIDAQAB\n-----END RSA PUBLIC KEY-----\n',
    valid_before='2048-01-31',
    comment='rollover candidate'
);
```

An added key is created as active immediately (`ACTIVATED=1`). During key rollover, a user
can have multiple active AUTH KEY entries.

### Activate / Deactivate AUTH KEY

```sql
ALTER USER app_user DEACTIVATE AUTH KEY ID 3;
ALTER USER app_user ACTIVATE AUTH KEY ID 3;
```

- A deactivated key cannot be used for challenge authentication.
- A user can own multiple AUTH KEY entries.

### Change AUTH KEY Expiration

```sql
ALTER USER app_user ALTER AUTH KEY ID 3 VALID_BEFORE='2048-06-30';
```

- A key past `VALID_BEFORE` cannot be used for authentication.
- The input format is `YYYY-MM-DD`, and a datetime value with a time portion is not
  accepted.

### Drop AUTH KEY

```sql
ALTER USER app_user DROP AUTH KEY ID 3;
```

- A dropped key cannot be used for authentication immediately.
- When a user is dropped, the user's AUTH KEY metadata is also removed.

## Query AUTH KEY Metadata

Registered AUTH KEY metadata can be queried from `V$USER_AUTH_KEYS`.

Major columns:

- `KEY_ID`: AUTH KEY identifier
- `USER_NAME`: owner of the AUTH KEY
- `KEY_ALGO`: key algorithm (`RSA`, `ECDSA`)
- `KEY_PARAM`: key parameter
  - RSA key: bit length such as `2048`
  - EC key: curve name such as `P-256`, `P-384`, `P-521`
- `ACTIVATED`: whether the key is active
- `VALID_AFTER`, `VALID_BEFORE`: validity period
- `COMMENT`: user note
- `PUBKEY`: PEM public key body

```sql
SELECT key_id, user_name, key_algo, key_param, activated, valid_before, comment
  FROM V$USER_AUTH_KEYS
 WHERE user_name='APP_USER'
 ORDER BY key_id;
```

To inspect the public key body, query the `PUBKEY` column.

```sql
SELECT key_id, user_name, pubkey
  FROM V$USER_AUTH_KEYS
 WHERE user_name='APP_USER'
 ORDER BY key_id;
```


## CONNECT

**user_connect_stmt:**

![user_connect_stmt](/images/sql/user/user_connect_stmt.png)

```sql
user_connect_stmt: 'CONNECT' user_name '/' password
```

The user can reconnect to another user via the following syntax without terminating the application.

```sql
-- Example
CONNECT user1/password;
```


## GRANT/REVOKE

![grant_stmt](/images/sql/user/grant_stmt.png)

![revoke_stmt](/images/sql/user/revoke_stmt.png)

![priv_value](/images/sql/user/priv_value.png)

Use `GRANT` to give privileges to a user and `REVOKE` to remove previously granted privileges.

Basic examples:

```sql
-- Grant user1 SELECT privileges on mytable
GRANT SELECT ON mytable TO user1;

-- Grant user1 all privileges on mytable
GRANT ALL ON mytable TO user1;
```

```sql
-- Revoke UPDATE privilege on mytable granted to user1
REVOKE UPDATE ON mytable FROM user1;

-- Revoke all privileges on mytable granted to user1
REVOKE ALL ON mytable FROM user1;
```

### Table Privileges

Use the following target formats when you grant privileges on a table:

- `table`
- `user.table`
- `db.user.table`

Available table privileges:

- `SELECT`
- `INSERT`
- `DELETE`
- `UPDATE`
- `ALL`

Examples:

```sql
GRANT SELECT ON sensor_log TO reader;
GRANT SELECT, INSERT ON sys.sensor_log TO writer;
REVOKE INSERT ON sys.sensor_log FROM writer;
GRANT ALL ON machbasedb.sys.sensor_log TO app_user;
```

### Machbase 8.5+: Database Privileges

> **Note**: The following behavior is supported from Machbase 8.5 or later.

From Machbase 8.5, you can grant database-scoped privileges by using `MACHBASEDB` as the target.

```sql
GRANT CREATE ON machbasedb TO ddl_user;
GRANT DROP ON machbasedb TO ddl_user;
GRANT ALTER ON machbasedb TO ops_user;
GRANT BACKUP ON machbasedb TO backup_user;
GRANT MOUNT ON machbasedb TO mount_user;
GRANT DDL ON machbasedb TO deploy_user;
GRANT ALL ON machbasedb TO admin_user;
```

Available database-scoped privileges:

- `CREATE`
- `DROP`
- `ALTER`
- `MOUNT`
- `BACKUP`
- `DDL`
- `ALL`

Here, `DDL` means the combined `CREATE + DROP` privilege.

### Meaning of `ALL`

> **Note**: The following behavior is supported from Machbase 8.5 or later.

`ALL` does not always mean the same thing. Its meaning depends on the target.

- `GRANT ALL ON machbasedb TO user1`
  - Grants the full set of database-scoped privileges.
- `GRANT ALL ON sys.table1 TO user1`
  - Grants the full set of DML privileges on that table.

In other words, `ALL` on `MACHBASEDB` and `ALL` on a table use the same keyword, but they serve different purposes.

### DML Privileges Cannot Be Granted Directly on `MACHBASEDB`

> **Note**: The following behavior is supported from Machbase 8.5 or later.

You cannot directly grant `SELECT`, `INSERT`, `DELETE`, or `UPDATE` on the database name `MACHBASEDB`.

```sql
GRANT SELECT ON machbasedb TO user1;
GRANT INSERT ON machbasedb TO user1;
REVOKE DELETE ON machbasedb FROM user1;
REVOKE UPDATE ON machbasedb FROM user1;
```

These statements fail with:

```sql
[ERR-02186: Invalid database name.]
```

To grant read or write access, specify a table instead.

```sql
GRANT SELECT ON sys.sensor_log TO user1;
GRANT INSERT ON sys.sensor_log TO user1;
```

### Use `MACHBASEDB` as the Database Target

> **Note**: The following behavior is supported from Machbase 8.5 or later.

Use `MACHBASEDB` when you grant database-scoped privileges.

```sql
GRANT BACKUP ON machbasedb TO backup_user;
REVOKE BACKUP ON machbasedb FROM backup_user;
```

If you use an invalid database name, the statement fails.

```sql
GRANT BACKUP ON typo TO backup_user;
```

```sql
[ERR-02186: Invalid database name.]
```

### Operations That Require Database Privileges

> **Note**: The following behavior is supported from Machbase 8.5 or later.

The following operations require database-scoped privileges on `MACHBASEDB`, not table-level privileges.

- `CREATE TABLE`, `DROP TABLE`
- `CREATE VIEW`, `DROP VIEW`
- `CREATE INDEX`, `DROP INDEX`
- `CREATE ROLLUP`, `DROP ROLLUP`
- `CREATE TABLESPACE`, `DROP TABLESPACE`
- `CREATE RETENTION`, `DROP RETENTION`
- `ALTER SYSTEM`
- `BACKUP DATABASE`
- `MOUNT DATABASE`, `UNMOUNT DATABASE`

For example, if a normal user needs to run `CREATE VIEW`, grant `CREATE` on `MACHBASEDB`.

```sql
GRANT CREATE ON machbasedb TO user1;
```

### Default Privileges for a New User

When a new user is created, the following privileges are granted by default.

- `SELECT`
- `INSERT`
- `DELETE`
- `UPDATE`
- `CREATE`
- `DROP`

The following privileges are not included by default and must be granted explicitly when needed.

- `ALTER`
- `MOUNT`
- `BACKUP`

### Privileges Do Not Override Table-Type Restrictions

Even with privileges, the built-in restrictions of each table type still apply.

- `LOG` and `TAG` tables do not support `UPDATE`.
- `VOLATILE` and `LOOKUP` tables support all DML operations, but `WHERE` clauses for query, update, and delete operations must be based on the primary key.

In other words, granting privileges does not enable unsupported DML behavior.

### Common Grant Examples

```sql
-- Allow read-only access to a specific table
GRANT SELECT ON sys.sensor_log TO reader;

-- Allow read and insert on a specific table
GRANT SELECT, INSERT ON sys.sensor_log TO writer;

-- Allow only DDL operations for a normal user
GRANT DDL ON machbasedb TO deploy_user;

-- Allow ALTER SYSTEM
GRANT ALTER ON machbasedb TO ops_user;

-- Allow backup
GRANT BACKUP ON machbasedb TO backup_user;

-- Allow mount and unmount
GRANT MOUNT ON machbasedb TO mount_user;
```


## Managing User Example

Here is an example of the above query and its results.

```
############################################
## Connect with SYS account
############################################
Mach> create user demo identified by 'demo';
Created successfully.

Mach> drop user demo;
Dropped successfully.

Mach> create user demo1 identified by 'demo1';
Created successfully.

Mach> create user demo2 identified by 'demo2';
Created successfully.

Mach> alter user demo2 identified by 'demo22';
Altered successfully.

Mach> create table demo1_table (id integer);
Created successfully.

Mach> create bitmap index demo1_table_index1 on demo1_table(id);
Created successfully.

Mach> insert into demo1_table values(99991);
1 row(s) inserted.

Mach> insert into demo1_table values(99992);
1 row(s) inserted.

Mach> insert into demo1_table values(99993);
1 row(s) inserted.

Mach> select * from demo1_table;
ID
--------------
99993
99992
99991
[3] row(s) selected.

#Error: Can't drop the user connected.
Mach> drop user SYS;
[ERR-02083 : Drop user error. You cannot drop yourself(SYS).]

############################################
## Connect DEMO1
############################################
Mach> connect demo1/demo1;
Connected successfully.

#Error: can't alter other's account password
Mach> alter user demo2 identified by 'demo22';
[ERR-02085 : ALTER user error. The user(DEMO2) does not have ALTER privileges.]

Mach> alter user demo1 identified by demo11;
Altered successfully.

#Error: wrong password
Mach> connect demo1/demo11234;
[ERR-02081 : User authentication error. Invalid password (DEMO11234).]

## Correct password
Mach> connect demo1/demo11;
Connected successfully.

Mach> create table demo1_table (id integer);
Created successfully.

Mach> create bitmap index demo1_table_index1 on demo1_table(id);
Created successfully.

Mach> insert into demo1_table values(1);
1 row(s) inserted.

Mach> insert into demo1_table values(2);
1 row(s) inserted.

Mach> insert into demo1_table values(3);
1 row(s) inserted.

Mach> select * from demo1_table;
ID
--------------
3
2
1
[3] row(s) selected.

Mach> select * from demo1.demo1_table;
ID
--------------
3
2
1
[3] row(s) selected.

############################################
## Connect SYS again
############################################
Mach> connect SYS/MANAGER;
Connected successfully.

Mach> select * from demo1_table;
ID
--------------
99993
99992
99991
[3] row(s) selected.

Mach> select * from demo1.demo1_table;
ID
--------------
3
2
1
[3] row(s) selected.

Mach> drop user demo1;
[ERR-02084 : DROP user error. The user's tables still exist. Drop those tables first.]

Mach> connect demo1/demo11;
Connected successfully.

Mach> drop table demo1_table;
Dropped successfully.

Mach> connect SYS/MANAGER;
Connected successfully.

Mach> drop user demo1;
Dropped successfully.
```

## sys-session-manage


# Index

* [ALTER SYSTEM](#alter-system)
    * [KILL SESSION](#kill-session)
    * [CANCEL SESSION](#cancel-session)
    * [CHECK DISK_USAGE](#check-disk_usage)
    * [INSTALL LICENSE](#install-license)
    * [INSTALL LICENSE (PATH)](#install-license-path)
    * [SET](#set)
    * [SET PVO CACHE](#set-pvo-cache)
    * [FLUSH PVO_CACHE](#flush-pvo_cache)
* [ALTER SESSION](#alter-session)
    * [SET SQL_LOGGING](#set-sql_logging)
    * [SET DEFAULT_DATE_FORMAT](#set-default_date_format)
    * [SET SHOW_HIDDEN_COLS](#set-show_hidden_cols)
    * [SET FEEDBACK_APPEND_ERROR](#set-feedback_append_error)
    * [SET MAX_QPX_MEM](#set-max_qpx_mem)
    * [SET SESSION_IDLE_TIMEOUT_SEC](#set-session_idle_timeout_sec)
    * [SET QUERY_TIMEOUT](#set-query_timeout)


## ALTER SYSTEM

This statement is the syntax for managing system-wide resources or changing settings.

> **Note**: From Machbase 8.5 or later, a normal user must have `ALTER` privilege on `MACHBASEDB` to run `ALTER SYSTEM`. See [GRANT/REVOKE](#grantrevoke) for details.

### KILL SESSION

**alter_system_kill_session_stmt:**

![alter_system_kill_session_stmt](/images/sql/sys/alter_system_kill_session_stmt.png)

```sql
alter_system_kill_session_stmt: 'ALTER SYSTEM KILL SESSION' number
```

Terminates a specific session with a SessionID.

- Only `SYS` can execute this statement; self-kill or non-SYS attempts return `[ERR-03025: Not enough privileges to manipulate the session. (<sid>)]`.
- If the session does not exist, an `ERR_MM_SESSION_ID_NOT_FOUND` error is returned.
- Use this when you need to drop the connection entirely; the target session is disconnected and any in-flight transaction is rolled back.

Example
```sql
-- As SYS
SELECT id, user_id, client_type FROM v$session;
ALTER SYSTEM KILL SESSION 12;
```

### CANCEL SESSION

**alter_system_cancel_session_stmt:**

![alter_system_cancel_session_stmt](/images/sql/sys/alter_system_cancel_session_stmt.png)

```sql
alter_system_cancel_session_stmt ::= 'ALTER SYSTEM CANCEL SESSION' number
```

Cancels a specific session with a SessionID.

- Cancels only the currently running statement and leaves the connection alive; the target session receives `[ERR-03027: This statement has been canceled.]`.
- Allowed for the same user or `SYS`. Different users get `[ERR-03026: You should log in with the same user name in the target session. Now (<me>) Target(<them>)]`.
- Self-cancel is rejected with the privilege error `[ERR-03025: Not enough privileges to manipulate the session. (<sid>)]`.
- If the session ID is not found, an `ERR_MM_SESSION_ID_NOT_FOUND` error is returned.

Example
```sql
-- Session A: find target SID
SELECT id, user_id, client_type FROM v$session;

-- Session B (same user or SYS): cancel the running statement on SID 6
ALTER SYSTEM CANCEL SESSION 6;
```

### CHECK DISK_USAGE

**alter_system_check_disk_stmt:**

![alter_system_check_disk_stmt](/images/sql/sys/alter_system_check_disk_stmt.png)

```sql
alter_system_check_disk_stmt ::= 'ALTER SYSTEM CHECK DISK_USAGE'
```

Corrects the value of DC_TABLE_FILE_SIZE, which indicates the disk usage of the log table in V$STORAGE.

Disk usage may be inaccurate when process failures or power failures occur. This command reads the correct value from the file system. However, it should be avoided because it can put a considerable load on the file system.

### INSTALL LICENSE

**alter_system_install_license_stmt:**

![alter_system_install_license_stmt](/images/sql/sys/alter_system_install_license_stmt.png)

```sql
alter_system_install_license_stmt ::= 'ALTER SYSTEM INSTALL LICENSE'
```

Installs the license file in the default location of the license file ($MACHBASE_HOME/conf/license.dat).

It is installed after determining whether the license is suitable for installation.

### INSTALL LICENSE (PATH)

**alter_system_install_license_path_stmt:**

![alter_system_install_license_path_stmt](/images/sql/sys/alter_system_install_license_path_stmt.png)

```sql
alter_system_install_license_path_stmt: ::= 'ALTER SYSTEM INSTALL LICENSE' '=' "'" path "'"
```

Installs the license file in a specific location.

An error occurs when you enter a license file that does not exist at that location or is incorrect. The path must be an absolute path. It is installed after determining whether the license is suitable for installation.

### SET

**alter_system_set_stmt:**

![alter_system_set_stmt](/images/sql/sys/alter_system_set_stmt.png)

```sql
alter_system_set_stmt ::= 'ALTER SYSTEM SET' prop_name '=' value
```

The list of properties that can be modified is as follows.
* QUERY_PARALLEL_FACTOR
* DEFAULT_DATE_FORMAT
* TRACE_LOG_LEVEL
* DISK_COLUMNAR_PAGE_CACHE_MAX_SIZE
* MAX_SESSION_COUNT
* SESSION_IDLE_TIMEOUT_SEC
* PROCESS_MAX_SIZE
* TAG_CACHE_MAX_MEMORY_SIZE

For numeric properties, extended expression syntax is supported.

Supported syntax
- Direct assignment (numeric or string):
  - `ALTER SYSTEM SET <name> = <value>;`
- Flag add (bitwise OR):
  - `ALTER SYSTEM SET <name> = <name> | <number>;`
  - `ALTER SYSTEM SET <name> = <number> | <name>;`
- Flag remove (bitwise AND + NOT):
  - `ALTER SYSTEM SET <name> = <name> & ~<number>;`
  - `ALTER SYSTEM SET <name> = ~<number> & <name>;`

Literal rules
- `<number>` accepts decimal (`123`) or hexadecimal (`0x7B`, `0X7B`).
- Bitwise expressions are allowed only for numeric properties. Non-numeric properties return an error.
- If you need a literal string such as `0xABCD`, use quotes:
  - `ALTER SYSTEM SET <name> = '0xABCD';`

Notes
- In bitwise expressions, the property name in the expression must match the left-hand side.
- Existing non-expression behavior remains unchanged.

Example
```sql
-- Set TRACE_LOG_LEVEL to a hex value
ALTER SYSTEM SET TRACE_LOG_LEVEL=0x00000003;
SELECT VALUE FROM V$PROPERTY WHERE NAME='TRACE_LOG_LEVEL';

-- Add flags (bitwise OR)
ALTER SYSTEM SET TRACE_LOG_LEVEL = TRACE_LOG_LEVEL | 0x00000004;
SELECT VALUE FROM V$PROPERTY WHERE NAME='TRACE_LOG_LEVEL';

ALTER SYSTEM SET TRACE_LOG_LEVEL = 0x00000008 | TRACE_LOG_LEVEL;
SELECT VALUE FROM V$PROPERTY WHERE NAME='TRACE_LOG_LEVEL';

ALTER SYSTEM SET TRACE_LOG_LEVEL = 16 | TRACE_LOG_LEVEL;
SELECT VALUE FROM V$PROPERTY WHERE NAME='TRACE_LOG_LEVEL';

-- Remove flags (bitwise AND + NOT)
ALTER SYSTEM SET TRACE_LOG_LEVEL = TRACE_LOG_LEVEL & ~0x00000001;
SELECT VALUE FROM V$PROPERTY WHERE NAME='TRACE_LOG_LEVEL';

ALTER SYSTEM SET TRACE_LOG_LEVEL = ~0x00000002 & TRACE_LOG_LEVEL;
SELECT VALUE FROM V$PROPERTY WHERE NAME='TRACE_LOG_LEVEL';

ALTER SYSTEM SET TRACE_LOG_LEVEL = ~4 & TRACE_LOG_LEVEL;
SELECT VALUE FROM V$PROPERTY WHERE NAME='TRACE_LOG_LEVEL';

-- Non-numeric properties are not allowed in bitwise expressions (error)
ALTER SYSTEM SET TRACE_LOG_LEVEL = 1 | DEFAULT_DATE_FORMAT;
ALTER SYSTEM SET DEFAULT_DATE_FORMAT = DEFAULT_DATE_FORMAT | 1;

-- Decimal assignment
ALTER SYSTEM SET TRACE_LOG_LEVEL=277;
```

### SET PVO CACHE

Adjusts global PVO statement cache properties at runtime (Standard edition only). `PVO_CACHE_ENABLE`, `PVO_CACHE_MAX_MEMORY_SIZE`, `PVO_CACHE_MAX_PLANS_PER_SQL`, and `PVO_CACHE_MAX_SQL_ENTRIES` apply immediately. `PVO_CACHE_SHARD_COUNT` is initialized at startup, so changing it requires a server restart. Memory and entry limits are distributed across shards.

```sql
ALTER SYSTEM SET PVO_CACHE_ENABLE = 1;
ALTER SYSTEM SET PVO_CACHE_MAX_MEMORY_SIZE = 268435456;
ALTER SYSTEM SET PVO_CACHE_MAX_PLANS_PER_SQL = 512;
ALTER SYSTEM SET PVO_CACHE_MAX_SQL_ENTRIES = 0;
```

### FLUSH PVO_CACHE

Flushes only the PVO statement cache. It operates independently from `FLUSH RESULT_CACHE`, and successful DDL execution internally flushes the PVO cache as well.

```sql
ALTER SYSTEM FLUSH PVO_CACHE;
```


## ALTER SESSION

This is the syntax for managing resources or changing settings on a per-session basis.

### SET SQL_LOGGING

**alter_session_sql_logging_stmt:**

![alter_session_sql_logging_stmt](/images/sql/sys/alter_session_sql_logging_stmt.png)

```sql
alter_session_sql_logging_stmt ::= 'ALTER SESSION SET SQL_LOGGING' '=' flag
```

Determines whether to leave a message in the Trace Log of the session.

You can use this message as a Bit Flag with the following values:
* 0x1: Parsing, Validation, Optimization.
* 0x2: It leaves the result of performing DDL.

That is, when the value of the corresponding flag is 2, only the DDL is logged, and when the flag is 3, the error and DDL are logged together.
Below is an example of changing the logging flag of the session and leaving error logging.

```sql
Mach> alter session set SQL_LOGGING=1;
Altered successfully.
Mach> exit
```

### SET DEFAULT_DATE_FORMAT

**alter_session_set_defalut_dateformat_stmt:**

![alter_session_set_defalut_dateformat_stmt](/images/sql/sys/alter_session_set_defalut_dateformat_stmt.png)

```sql
alter_session_set_defalut_dateformat_stmt ::= 'ALTER SESSION SET DEFAULT_DATE_FORMAT' '=' date_format
```
Sets the default format for Datetime data types for this session.

When the server is started, the property **DEFAULT_DATE_FORMAT** is set to the session attribute.
If the property of the property has not changed, the value of the session will also be "YYYY-MM-DD HH24: MI: SS mmm: uuu: nnn".
Use this command to modify the default format of a datetime datatype for a specific user, regardless of the system.
V$session has a default date format set for each session and can be checked. Below is an example of checking and changing the value of the session.

```sql
Mach> CREATE TABLE time_table (time datetime);
Created successfully.

Mach> SELECT DEFAULT_DATE_FORMAT from v$session;
default_date_format
-----------------------------------------------
YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn
[1] row(s) selected.

Mach> INSERT INTO time_table VALUES(TO_DATE('2016/11/12'));
[ERR-00300: Invalid date value.(2016/11/12)]

Mach> ALTER SESSION SET DEFAULT_DATE_FORMAT='YYYY/MM/DD';
Altered successfully.

Mach> SELECT DEFAULT_DATE_FORMAT from v$session;

default_date_format
----------------------------------------------
YYYY/MM/DD
[1] row(s) selected.

Mach> INSERT INTO time_table VALUES(TO_DATE('2016/11/12'));
1 row(s) inserted.

Mach> SELECT * FROM time_table;

TIME
----------------------------------
2016/11/12

[1] row(s) selected.
```

### SET SHOW_HIDDEN_COLS

**alter_session_set_hidden_column_stmt:**

![alter_session_set_hidden_column_stmt](/images/sql/sys/alter_session_set_hidden_column_stmt.png)

```sql
alter_session_set_hidden_column_stmt ::= 'ALTER SESSION SET SHOW_HIDDEN_COLS' '=' ( '0' | '1' )
```

Decides whether to output the hidden column (_arrival_time) in the column represented by * when executing the select of the session.

When the server is started, the value of the global property SHOW_HIDDEN_COLS is set to 0 for the session attribute.
If you want to change the default behavior of your session, you can set this value to 1.
V$session has a SHOW_HIDDEN_COLS value set for each session.


```sql
Mach> SELECT * FROM  v$session;
ID                   CLOSED      USER_ID     LOGIN_TIME                      SQL_LOGGING SHOW_HIDDEN_COLS
-----------------------------------------------------------------------------------------------------------------
DEFAULT_DATE_FORMAT                                                               HASH_BUCKET_SIZE
------------------------------------------------------------------------------------------------------
1                    0           1           2015-04-29 17:23:56 248:263:000 3           0
YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn                                                 20011
[1] row(s) selected.
Mach> ALTER SESSION SET SHOW_HIDDEN_COLS=1;
Altered successfully.
Mach> SELECT * FROM v$session;
_ARRIVAL_TIME                   ID                   CLOSED      USER_ID     LOGIN_TIME                      SQL_LOGGING
--------------------------------------------------------------------------------------------------------------------------------
SHOW_HIDDEN_COLS DEFAULT_DATE_FORMAT                                                               HASH_BUCKET_SIZE
------------------------------------------------------------------------------------------------------------------------
1970-01-01 09:00:00 000:000:000 1                    0           1           2015-04-29 17:23:56 248:263:000 3
1           YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn                                                 20011
[1] row(s) selected.
```

### SET FEEDBACK_APPEND_ERROR

**alter_session_set_feedback_append_err_stmt:**

![alter_session_set_feedback_append_err_stmt](/images/sql/sys/alter_session_set_feedback_append_err_stmt.png)

```sql
alter_session_set_feedback_append_err_stmt ::= 'ALTER SESSION SET FEEDBACK_APPEND_ERROR' '=' ( '0' | '1' )
```

Sets whether to send the session's Append error message to the client program.

Use the following values ​​for the error message.
* 0 = Do not send an error message.
* 1 = Send an error message.
Below is an example of use.

```sql
mach> ALTER SESSION SET FEEDBACK_APPEND_ERROR=0;
Altered successfully.
```

### SET MAX_QPX_MEM

**alter_session_set_max_qpx_mem_stmt:**

![alter_session_set_max_qpx_mem_stmt](/images/sql/sys/alter_session_set_max_qpx_mem_stmt.png)

```sql
alter_session_set_max_qpx_mem_stmt ::= 'ALTER SESSION SET MAX_QPX_MEM' '=' value
```

Specifies the maximum amount of memory that a single SQL statement in the session will use when performing GROUP BY, DISTINCT, ORDER BY operations.

If you try to allocate more memory than the maximum memory, the system cancels the execution of the SQL statement and treats it as an error.
In case of error, record the error code and error message in machbase.trc including the query.

```sql
Mach> ALTER SESSION SET MAX_QPX_MEM=1073741824;
Altered successfully.

Mach> SELECT * FROM v$session;
ID                   CLOSED      USER_ID     LOGIN_TIME                      CLIENT_TYPE
---------------------------------------------------------------------------------------------------------------------------------------------------------------------
USER_NAME                                                                         USER_IP                                                                           SQL_LOGGING SHOW_HIDDEN_COLS
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
FEEDBACK_APPEND_ERROR DEFAULT_DATE_FORMAT                                                               HASH_BUCKET_SIZE MAX_QPX_MEM          RS_CACHE_ENABLE      RS_CACHE_TIME_BOUND_MSEC
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
RS_CACHE_MAX_MEMORY_PER_QUERY RS_CACHE_MAX_RECORD_PER_QUERY RS_CACHE_APPROXIMATE_RESULT_ENABLE IDLE_TIMEOUT         QUERY_TIMEOUT
-----------------------------------------------------------------------------------------------------------------------------------------------
14                   0           1           2021-03-08 16:33:01 503:181:809 CLI
NULL                                                                              192.168.0.194                                                                     11          0
1                     YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn                                                 20011            1073741824           1                    1000
16777216                      50000                         0                                  0                    0
[1] row(s) selected.
Elapsed time: 0.001
```

- trc error when using more than the maximum memory size in an SQL statement

```sql
[2021-03-08 16:36:32 P-69000 T-140515328653056][INFO] DML FAILURE (2E10000084:Memory allocation error (alloc'd: 1048595, max: 1048576).)
```

- machsql error message when using more than the maximum memory size in an SQL statement

```sql
Mach> select * from tag order by value DESC, time ASC;
NAME                  TIME                            VALUE
--------------------------------------------------------------------------------------
[ERR-00132: Memory allocation error (alloc'd: 1048595, max: 1048576).]
[0] row(s) selected.
Elapsed time: 0.447
```

### SET SESSION_IDLE_TIMEOUT_SEC

**alter_session_set_session_idle_timeout_sec_stmt:**

![alter_session_set_session_idle_timeout_sec_stmt](/images/sql/sys/alter_session_set_session_idle_timeout_sec_stmt.png)

```sql
alter_session_set_session_idle_timeout_sec_stmt ::= 'ALTER SESSION SET SESSION_IDLE_TIMEOUT_SEC' '=' value
```

Specifies the duration of the connection when the session is idle.
It is specified in seconds, and the session is terminated when the set time in the idle state elapses.
You can inquire the idle timeout time set in the session in v$session.

```sql
Mach> ALTER SESSION SET SESSION_IDLE_TIMEOUT_SEC=200;
Altered successfully.


Mach> SELECT IDLE_TIMEOUT FROM V$SESSION;
IDLE_TIMEOUT
-----------------------
200
[1] row(s) selected.
```

### SET QUERY_TIMEOUT

**alter_session_set_query_timeout_stmt:**

![alter_session_set_query_timeout_stmt](/images/sql/sys/alter_session_set_query_timeout_stmt.png)

```sql
alter_session_set_query_timeout_stmt ::= 'ALTER SESSION SET QUERY_TIMEOUT' '=' value
```

This is the time to wait for a response from the server when performing query in the session.
It is specified in seconds, and when the response from the server exceeds the specified time after executing the query, the query is terminated.
You can inquire the QUERY_TIME in the session in v$session

```sql
Mach> ALTER SESSION SET QUERY_TIMEOUT=200;
Altered successfully.

Mach> SELECT QUERY_TIMEOUT FROM V$SESSION;
QUERY_TIMEOUT
-----------------------
200
[1] row(s) selected.
```

## view


## Index

* [What is a Stored VIEW?](#what-is-a-stored-view)
* [Why Use VIEW in Machbase?](#why-use-view-in-machbase)
* [Basic Syntax](#basic-syntax)
* [Basic Examples](#basic-examples)
* [How Column Names Are Determined](#how-column-names-are-determined)
* [Supported VIEW Shapes](#supported-view-shapes)
* [Machbase-Specific Examples](#machbase-specific-examples)
* [Metadata and Operational Checks](#metadata-and-operational-checks)
* [Performance and Limits](#performance-and-limits)
* [Common Failure Cases](#common-failure-cases)

## What is a Stored VIEW?

This document describes a **stored VIEW** created with `CREATE VIEW`, not an inline
view written as `FROM (SELECT ...)`.

A VIEW stores a `SELECT` definition as a named logical object so that it can be reused.

* A VIEW does not store data separately.
* When queried, the stored VIEW definition SQL is expanded and executed internally.
* A VIEW can be used as a `SELECT` target like a table, but it is not a physical storage feature.
* The behaviors covered in this document are `CREATE VIEW`, `DROP VIEW`, `SELECT`,
  `DESC`, `SHOW VIEWS`, `M$SYS_VIEWS`, and `EXPLAIN`.

In practice, a VIEW should be understood as "a reusable named query" rather than
"copied data stored in another object".

## Why Use VIEW in Machbase?

VIEW is especially useful in Machbase in the following situations.

* When you want to reuse the same query under a simple name
* When you want to share complex `JOIN`, `GROUP BY`, `CASE`, or `UNION ALL` logic
* When you want to expose decoded `BINARY` values from Tag tables as logical columns
* When you want to inspect metadata and execution plans with `SHOW VIEWS`, `DESC`,
  `M$SYS_VIEWS`, and `EXPLAIN`

The characteristics of the base table still matter under a VIEW.

* VIEWs over Lookup / Volatile tables still depend on efficient primary-key-based predicates.
* VIEWs over Tag tables should still be checked with `name`, `time`, and `EXPLAIN`.
* Because a VIEW reuses the base query and optimizer path, its performance follows the base query.

## Basic Syntax

### Create a VIEW

```sql
CREATE VIEW view_name AS
SELECT ...
FROM ...;
```

```sql
CREATE VIEW view_name (col1, col2, ...) AS
SELECT ...
FROM ...;
```

```sql
CREATE OR REPLACE VIEW view_name AS
SELECT ...
FROM ...;
```

* `view_name` may also be schema-qualified, such as `db.user.view_name`.
* `CREATE OR REPLACE VIEW` replaces the existing VIEW definition.
* If an object with the same name already exists and it is not a VIEW, replacement fails.
* In the currently validated implementation, `CREATE OR REPLACE VIEW` keeps the same object id.
* If validation of the new definition fails, the old VIEW definition remains unchanged.

### Drop a VIEW

```sql
DROP VIEW view_name;
DROP VIEW IF EXISTS view_name;
```

* `DROP VIEW IF EXISTS` succeeds even when the target does not exist.
* If another VIEW depends on the target VIEW, `DROP VIEW` is blocked.
* `DROP TABLE view_name` cannot be used to remove a VIEW.

### Metadata Queries

```sql
SHOW VIEWS;
DESC view_name;

SELECT USER_NAME, DB_NAME, VIEW_NAME, VIEW_SQL
FROM M$SYS_VIEWS;
```

## Basic Examples

The following example shows a simple Lookup-based VIEW.

```sql
CREATE LOOKUP TABLE customer (
    id INTEGER PRIMARY KEY,
    name VARCHAR(20),
    city VARCHAR(20),
    amount INTEGER
);

CREATE VIEW v_customer AS
SELECT id, name, city, amount
FROM customer;

SELECT name, city
FROM v_customer
WHERE id = 100;
```

You can also define the exposed column names explicitly.

```sql
CREATE VIEW v_customer_short (cust_id, cust_name) AS
SELECT id, name
FROM customer;

SELECT cust_id, cust_name
FROM v_customer_short
WHERE cust_id = 100;
```

To change an existing VIEW definition, use `CREATE OR REPLACE VIEW`.

```sql
CREATE VIEW v_customer_amount AS
SELECT id, amount
FROM customer;

CREATE OR REPLACE VIEW v_customer_amount AS
SELECT id, amount * 10 AS amount
FROM customer
WHERE id <= 10;
```

## How Column Names Are Determined

### When an Explicit Column List Is Given

```sql
CREATE VIEW v_sales (sales_id, sales_name) AS
SELECT id, name
FROM t_sales;
```

In this case, the official VIEW column names are `sales_id` and `sales_name`.

### When No Explicit Column List Is Given

Column names are determined in the following order.

1. `SELECT` alias
2. Original column name for a simple column reference
3. Auto-generated names such as `EXPR1`, `EXPR2`, ...

```sql
CREATE VIEW v_expr AS
SELECT id,
       name AS user_name,
       val + 10
FROM t1;
```

The resulting column names are in the form of `ID`, `USER_NAME`, and `EXPR3`.

### Column Names in `UNION ALL` VIEWs

A `UNION ALL` VIEW uses the target names from the left-most `SELECT`.

```sql
CREATE VIEW v_union AS
SELECT id FROM t1
UNION ALL
SELECT id FROM t2;
```

Therefore `DESC v_union` shows `ID`, and `SELECT id FROM v_union` works normally.

## Supported VIEW Shapes

The currently validated VIEW shapes include:

* Simple projection and predicates
* Expressions, functions, constants, and `CASE`
* `JOIN`
* VIEWs containing subqueries
* Nested VIEWs
* `GROUP BY`, `HAVING`
* `DISTINCT`
* `UNION ALL`

Examples:

```sql
CREATE VIEW v_expr_case AS
SELECT id,
       CASE WHEN amount >= 100 THEN 'VIP' ELSE 'NORMAL' END AS grade,
       UPPER(city) AS city_upper
FROM customer;
```

```sql
CREATE VIEW v_city_sum AS
SELECT city, SUM(amount) AS total_amount
FROM customer
GROUP BY city
HAVING SUM(amount) >= 100;
```

```sql
CREATE VIEW v_union AS
SELECT id FROM customer WHERE city = 'SEOUL'
UNION ALL
SELECT id FROM customer WHERE city = 'BUSAN';
```

```sql
CREATE VIEW v_nested AS
SELECT id, total_amount
FROM v_city_sum
JOIN (
    SELECT city AS city_name, COUNT(*) AS city_cnt
    FROM customer
    GROUP BY city
) x
ON v_city_sum.city = x.city_name;
```

## Machbase-Specific Examples

### Decoding Tag / BINARY Data

One of the most practical Machbase VIEW patterns is exposing decoded values from
a Tag table `BINARY` column as logical columns.

```sql
CREATE TAG TABLE dam (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    frame BINARY(16)
);

CREATE VIEW damdata AS
SELECT name,
       time,
       extract_bit(frame, 0) AS bit0,
       extract_ulong(frame, 0, 16) AS u16,
       extract_long(frame, 0, 16) AS s16,
       extract_float(frame, 0) AS f32,
       extract_scaled_double(frame, 0, 12, 0, 0.5, 0.5) AS sd12
FROM dam;
```

```sql
SELECT name, time, bit0, u16, s16, f32, sd12
FROM damdata
WHERE name = 'main'
  AND time >= TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
  AND time <  TO_DATE('2024-01-01 00:01:00', 'YYYY-MM-DD HH24:MI:SS')
ORDER BY time;
```

For this type of VIEW, it is still important to check `name`, `time`, and `EXPLAIN`
just as you would on the base Tag table.

### Schema-Qualified and Quoted Names

VIEW names may be schema-qualified and may also use quoted identifiers.

```sql
CREATE VIEW machbasedb.sys.v_local AS
SELECT id, val
FROM other_user.v_src
WHERE id >= 2;

CREATE VIEW "V_QUOTED" AS
SELECT id, val
FROM t1;

CREATE VIEW v_dep AS
SELECT id
FROM "V_QUOTED"
WHERE val >= 20;
```

* VIEWs with the same simple name in different schemas are distinguished by schema-qualified names.
* If a dependent VIEW references a quoted VIEW, `DROP VIEW` is blocked.

## Metadata and Operational Checks

### `SHOW VIEWS`

`SHOW VIEWS` lists the visible VIEWs and their definition SQL.

The output columns are:

* `USER_NAME`
* `DB_NAME`
* `VIEW_NAME`
* `VIEW_SQL`

```sql
SHOW VIEWS;
```

### `M$SYS_VIEWS`

`M$SYS_VIEWS` is the public metadata interface for checking VIEW definition SQL.

```sql
SELECT USER_NAME, DB_NAME, VIEW_NAME, VIEW_SQL
FROM M$SYS_VIEWS
WHERE VIEW_NAME = 'V_CUSTOMER';
```

Typical uses:

* Listing VIEWs
* Checking the definition SQL of a specific VIEW
* Confirming the new definition after `CREATE OR REPLACE VIEW`

### `DESC`, `M$SYS_TABLES`, `M$SYS_COLUMNS`

```sql
DESC v_customer;

SELECT ID, NAME, TYPE
FROM M$SYS_TABLES
WHERE TYPE = 7;

SELECT TABLE_ID, ID, NAME, TYPE, LENGTH
FROM M$SYS_COLUMNS
WHERE TABLE_ID = (
    SELECT ID
    FROM M$SYS_TABLES
    WHERE TYPE = 7
      AND NAME = 'V_CUSTOMER'
);
```

* `DESC` shows the exposed column names and types of the VIEW.
* `M$SYS_TABLES` shows VIEW entries as `TYPE = 7`.
* `M$SYS_COLUMNS` shows the exposed VIEW columns.
* After `CREATE OR REPLACE VIEW`, `M$SYS_TABLES.ID` is preserved while
  `M$SYS_VIEWS.VIEW_SQL` is updated.

### `EXPLAIN`

Because a VIEW does not own physical data, actual performance depends on the base
query and the optimizer path. In production, `EXPLAIN` should be checked first.

```sql
EXPLAIN
SELECT *
FROM v_customer
WHERE id = 3;
```

## Performance and Limits

### Index Usage and Predicate Pushdown

The following cases are more likely to use the base-table index path:

* A simple projection VIEW exposing base columns directly
* A VIEW that only renames columns
* A VIEW with a simple filter where the outer predicate maps directly to base columns

The following cases may fall back to a full scan, so `EXPLAIN` is important:

* An outer predicate on top of a `DISTINCT` VIEW
* A predicate on an expression-derived column such as `id + 1 AS id2`

### Simple Stored-VIEW Optimizations

In the currently validated implementation, simple stored VIEWs may use:

* A path that prunes unused projection targets
* A fast path for `COUNT(*)` when the outer predicate can be pushed down

By contrast, `SELECT *`, `DISTINCT`, `GROUP BY`, `HAVING`, set-op, window, and
join-heavy shapes may use the full projection path.

### VIEW Definition SQL Length Limit

In the current implementation, the VIEW definition SQL after `AS` is supported up to `256KB`.

Overflow returns an error in the following family.

```text
ERR-02010: Syntax error: near token (VIEW_SQL_TOO_LONG).
```

### Drop and Dependency Rules

* `DROP VIEW` is blocked when a dependent VIEW exists.
* Dependency resolution is based on real referenced objects.
* A name appearing only in a string literal or alias is not treated as a dependency.

## Common Failure Cases

### Column Count Mismatch

```sql
CREATE VIEW v_bad (c1, c2, c3) AS
SELECT id, val
FROM t1;
```

### Direct Recursive VIEW

```sql
CREATE VIEW v_recursive AS
SELECT id
FROM v_recursive;
```

### Duplicate Column Names and `_RID`

```sql
CREATE VIEW v_dup AS
SELECT id AS c1, val AS c1
FROM t1;

CREATE VIEW v_rid (_RID) AS
SELECT id
FROM t1;
```

### Replacing a Non-VIEW Object with `CREATE OR REPLACE VIEW`

```sql
CREATE OR REPLACE VIEW t1 AS
SELECT id
FROM src_t1;
```

### Reserved Names or Invalid Paths

```sql
CREATE VIEW v$bad AS
SELECT id
FROM t1;

CREATE VIEW _tag_bad AS
SELECT id
FROM t1;

CREATE VIEW no_such_db.sys.v_bad AS
SELECT id
FROM t1;
```

### Dropping a VIEW with `DROP TABLE`

```sql
DROP TABLE v_customer;
```

In this case the VIEW is not removed and an error is returned.

## Related Documents

* [DDL](#ddl)
* [SELECT](#select)

## functions


## Error Handling

|Error Type|Code|When it occurs|
|---|---|---|
|Argument type error|`ERR-02036`, `ERR-02037`|A non-numeric value is passed, or an argument is passed to `PI`|
|Runtime error|`ERR-02317`|Negative input to `SQRT`, division by zero in `MOD`, invalid base/value in `LOG`, overflow in `EXP`/`POWER`, and similar cases|

If the input is `NULL`, the result is also `NULL`.

## ABS

This function works on a numeric column, converts it to a positive value, and returns the value as a real number.

```sql
ABS(column_expr)
```

```sql
Mach> CREATE TABLE abs_table (c1 INTEGER, c2 DOUBLE, c3 VARCHAR(10));
Created successfully.

Mach> INSERT INTO abs_table VALUES(1, 1.0, '');
1 row(s) inserted.

Mach> INSERT INTO abs_table VALUES(2, 2.0, 'sqltest');
1 row(s) inserted.

Mach> INSERT INTO abs_table VALUES(3, 3.0, 'sqltest');
1 row(s) inserted.

Mach> SELECT ABS(c1), ABS(c2) FROM abs_table;
SELECT ABS(c1), ABS(c2) from abs_table;
ABS(c1)                     ABS(c2)
-----------------------------------------------------------
3                           3
2                           2
1                           1
[3] row(s) selected.
```


## ADD_TIME

This function performs a date and time operation on a given datetime column. Supports increment/decrement operations up to year, month, day, hour, minute, and second, and does not support operations on milli, micro, and nanoseconds. The Diff format is: "Year/Month/Day Hour:Minute:Second". Each item has a positive or negative value.

```sql
ADD_TIME(column,time_diff_format)
```

```sql
Mach> CREATE TABLE add_time_table (id INTEGER, dt DATETIME);
Created successfully.

Mach> INSERT INTO  add_time_table VALUES(1, TO_DATE('1999-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  add_time_table VALUES(2, TO_DATE('2000-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  add_time_table VALUES(3, TO_DATE('2012-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  add_time_table VALUES(4, TO_DATE('2013-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  add_time_table VALUES(5, TO_DATE('2014-12-30 11:22:33 444:555:666'));
1 row(s) inserted.

Mach> INSERT INTO  add_time_table VALUES(6, TO_DATE('2014-12-30 23:22:33 444:555:666'));
1 row(s) inserted.

Mach> SELECT ADD_TIME(dt, '1/0/0 0:0:0') FROM add_time_table;
ADD_TIME(dt, '1/0/0 0:0:0')
----------------------------------
2015-12-30 23:22:33 444:555:666
2015-12-30 11:22:33 444:555:666
2014-11-11 01:02:03 004:005:006
2013-11-11 01:02:03 004:005:006
2001-11-11 01:02:03 004:005:006
2000-11-11 01:02:03 004:005:006
[6] row(s) selected.

Mach> SELECT ADD_TIME(dt, '0/0/0 1:1:1') FROM add_time_table;
ADD_TIME(dt, '0/0/0 1:1:1')
----------------------------------
2014-12-31 00:23:34 444:555:666
2014-12-30 12:23:34 444:555:666
2013-11-11 02:03:04 004:005:006
2012-11-11 02:03:04 004:005:006
2000-11-11 02:03:04 004:005:006
1999-11-11 02:03:04 004:005:006
[6] row(s) selected.

Mach> SELECT ADD_TIME(dt, '1/1/1 0:0:0') FROM add_time_table;
ADD_TIME(dt, '1/1/1 0:0:0')
----------------------------------
2016-01-31 23:22:33 444:555:666
2016-01-31 11:22:33 444:555:666
2014-12-12 01:02:03 004:005:006
2013-12-12 01:02:03 004:005:006
2001-12-12 01:02:03 004:005:006
2000-12-12 01:02:03 004:005:006
[6] row(s) selected.

Mach> SELECT ADD_TIME(dt, '-1/0/0 0:0:0') FROM add_time_table;
ADD_TIME(dt, '-1/0/0 0:0:0')
----------------------------------
2013-12-30 23:22:33 444:555:666
2013-12-30 11:22:33 444:555:666
2012-11-11 01:02:03 004:005:006
2011-11-11 01:02:03 004:005:006
1999-11-11 01:02:03 004:005:006
1998-11-11 01:02:03 004:005:006
[6] row(s) selected.

Mach> SELECT ADD_TIME(dt, '0/0/0 -1:-1:-1') FROM add_time_table;
ADD_TIME(dt, '0/0/0 -1:-1:-1')
----------------------------------
2014-12-30 22:21:32 444:555:666
2014-12-30 10:21:32 444:555:666
2013-11-11 00:01:02 004:005:006
2012-11-11 00:01:02 004:005:006
2000-11-11 00:01:02 004:005:006
1999-11-11 00:01:02 004:005:006
[6] row(s) selected.

Mach> SELECT ADD_TIME(dt, '-1/-1/-1 0:0:0') FROM add_time_table;
ADD_TIME(dt, '-1/-1/-1 0:0:0')
----------------------------------
2013-11-29 23:22:33 444:555:666
2013-11-29 11:22:33 444:555:666
2012-10-10 01:02:03 004:005:006
2011-10-10 01:02:03 004:005:006
1999-10-10 01:02:03 004:005:006
1998-10-10 01:02:03 004:005:006
[6] row(s) selected.

Mach> SELECT * FROM add_time_table WHERE dt > ADD_TIME(TO_DATE('2014-12-30 11:22:33 444:555:666'), '-1/-1/-1 0:0:0');
ID          DT
-----------------------------------------------
6           2014-12-30 23:22:33 444:555:666
5           2014-12-30 11:22:33 444:555:666
[2] row(s) selected.

Mach> SELECT * FROM add_time_table WHERE dt > ADD_TIME(TO_DATE('2014-12-30 11:22:33 444:555:666'), '-1/-2/-1 0:0:0');
ID          DT
-----------------------------------------------
6           2014-12-30 23:22:33 444:555:666
5           2014-12-30 11:22:33 444:555:666
4           2013-11-11 01:02:03 004:005:006
[3] row(s) selected.

Mach> SELECT ADD_TIME(TO_DATE('2000-12-01 00:00:00 000:000:001'), '-1/0/0 0:0:-1') FROM add_time_table;
ADD_TIME(TO_DATE('2000-12-01 00:00:00 000:000:001'), '-1/0/0 0:0:-1')
------------------------------------------
1999-11-30 23:59:59 000:000:001
1999-11-30 23:59:59 000:000:001
1999-11-30 23:59:59 000:000:001
1999-11-30 23:59:59 000:000:001
1999-11-30 23:59:59 000:000:001
1999-11-30 23:59:59 000:000:001
[6] row(s) selected.

Mach> SELECT * FROM add_time_table WHERE dt > ADD_TIME(TO_DATE('2014-12-30 11:22:33 444:555:666'), '-1/-2/-1 0:0:0');
ID          DT
-----------------------------------------------
6           2014-12-30 23:22:33 444:555:666
5           2014-12-30 11:22:33 444:555:666
4           2013-11-11 01:02:03 004:005:006
[3] row(s) selected.
```


## APPROX_PERCENTILE {#approx_percentile-family}

```
APPROX_PERCENTILE
APPROX_MEDIAN
APPROX_P05
APPROX_P10
APPROX_P90
APPROX_P95
```

These aggregate functions estimate percentiles while keeping a bounded summary instead of sorting every raw value. They are useful when the input is very large and a small approximation error is acceptable.

```sql
APPROX_PERCENTILE(value, ratio)
APPROX_MEDIAN(value)
APPROX_P05(value)
APPROX_P10(value)
APPROX_P90(value)
APPROX_P95(value)
```

- `value` must be numeric.
- `ratio` must be a constant in the range `0.0` to `1.0`.
- Return type is `DOUBLE`.
- `NULL` values are ignored.

`APPROX_MEDIAN(value)` is an approximate 50th percentile. `APPROX_P05`, `APPROX_P10`, `APPROX_P90`, and `APPROX_P95` are convenience forms for fixed percentile points.

```sql
SELECT APPROX_PERCENTILE(latency_ms, 0.95) AS ap95,
       APPROX_MEDIAN(latency_ms) AS amedian,
       APPROX_P05(latency_ms) AS ap05
FROM api_log;
```


## AREA {#area}

`AREA(y, x)` is an exact aggregate function that calculates the area under a curve formed by `(x, y)` pairs.

```sql
AREA(y, x)
```

- Both arguments must be numeric.
- The function ignores rows where either argument is `NULL`.
- At least two valid points are required. Otherwise, the result is `NULL`.
- The result type is `DOUBLE`.

```sql
SELECT AREA(power_kw, sample_sec)
FROM power_log;
```


## AVG

This function is an aggregate function that operates on a numeric column and prints the average value of that column.

```sql
AVG(column_name)
```

```sql
Mach> CREATE TABLE avg_table (id1 INTEGER, id2 INTEGER);
Created successfully.

Mach> INSERT INTO avg_table VALUES(1, 1);
1 row(s) inserted.

Mach> INSERT INTO avg_table VALUES(1, 2);
1 row(s) inserted.

Mach> INSERT INTO avg_table VALUES(1, 3);
1 row(s) inserted.

Mach> INSERT INTO avg_table VALUES(2, 1);
1 row(s) inserted.

Mach> INSERT INTO avg_table VALUES(2, 2);
1 row(s) inserted.

Mach> INSERT INTO avg_table VALUES(2, 3);
1 row(s) inserted.

Mach> INSERT INTO avg_table VALUES(null, 4);
1 row(s) inserted.

Mach> SELECT id1, AVG(id2) FROM avg_table GROUP BY id1;
id1         AVG(id2)
-------------------------------------------
2                2
NULL             4
1                2
```


## BITAND / BITOR

This function converts two input values ​​to a 64-bit signed integer and returns the result of bitwise and/or. The input value must be an integer and the output value is a 64-bit signed integer.

For integer values ​​less than 0, it is recommended to use only uinteger and ushort types, because different results may be obtained depending on the platform.

```sql
BITAND (<expression1>, <expression2>)
BITOR (<expression1>, <expression2>)
```

```sql
Mach> CREATE TABLE bit_table (i1 INTEGER, i2 UINTEGER, i3 FLOAT, i4 DOUBLE, i5 SHORT, i6 VARCHAR(10));
Created successfully.

Mach> INSERT INTO bit_table VALUES (-1, 1, 1, 1, 2, 'aaa');
1 row(s) inserted.

Mach> INSERT INTO bit_table VALUES (-2, 2, 2, 2, 3, 'bbb');
1 row(s) inserted.

Mach> SELECT BITAND(i1, i2) FROM bit_table;
BITAND(i1, i2)
-----------------------
2
1
[2] row(s) selected.

Mach> SELECT * FROM bit_table WHERE BITAND(i2, 1) = 1;
I1          I2          I3                          I4                          I5          I6
---------------------------------------------------------------------------------------------------------------
-1          1           1                           1                           2           aaa
[1] row(s) selected.

Mach> SELECT BITOR(i5, 1) FROM bit_table WHERE BITOR(i5, 1) = 3;
BITOR(i5, 1)
-----------------------
3
3
[2] row(s) selected.

Mach> SELECT * FROM bit_table WHERE BITOR(i2, 1) = 1;
I1          I2          I3                          I4                          I5          I6
---------------------------------------------------------------------------------------------------------------
-1          1           1                           1                           2           aaa
[1] row(s) selected.

Mach> SELECT * FROM bit_table WHERE BITAND(i3, 1) = 1;
I1          I2          I3                          I4                          I5          I6
---------------------------------------------------------------------------------------------------------------
[ERR-02037 : Function [BITAND] argument data type is mismatched.]
[0] row(s) selected.

Mach> SELECT * FROM bit_table WHERE BITAND(i4, 1) = 1;
I1          I2          I3                          I4                          I5          I6
---------------------------------------------------------------------------------------------------------------
[ERR-02037 : Function [BITAND] argument data type is mismatched.]
[0] row(s) selected.

Mach> SELECT BITAND(i5, 1) FROM bit_table WHERE BITAND(i5, 1) = 1;
BITAND(i5, 1)
-----------------------
1
[1] row(s) selected.

Mach> SELECT * FROM bit_table WHERE BITOR(i6, 1) = 1;
I1          I2          I3                          I4                          I5          I6
---------------------------------------------------------------------------------------------------------------
[ERR-02037 : Function [BITOR] argument data type is mismatched.]
[0] row(s) selected.

Mach> SELECT BITOR(i1, i2) FROM bit_table;
BITOR(i1, i2)
-----------------------
-2
-1
[2] row(s) selected.

Mach> SELECT BITAND(i1, i3) FROM bit_table;
BITAND(i1, i3)
-----------------------
[ERR-02037 : Function [BITAND] argument data type is mismatched.]
[0] row(s) selected.

Mach> SELECT BITOR(i1, i6) FROM bit_table;
BITOR(i1, i6)
-----------------------
[ERR-02037 : Function [BITOR] argument data type is mismatched.]
[0] row(s) selected.
```


## COUNT

This function is an aggregate function that obtains the number of records in a given column.

```sql
COUNT(column_name)
```

```sql
Mach> CREATE TABLE count_table (id1 INTEGER, id2 INTEGER);
Created successfully.

Mach> INSERT INTO count_table VALUES(1, 1);
1 row(s) inserted.

Mach> INSERT INTO count_table VALUES(1, 2);
1 row(s) inserted.

Mach> INSERT INTO count_table VALUES(1, 3);
1 row(s) inserted.

Mach> INSERT INTO count_table VALUES(2, 1);
1 row(s) inserted.

Mach> INSERT INTO count_table VALUES(2, 2);
1 row(s) inserted.

Mach> INSERT INTO count_table VALUES(2, 3);
1 row(s) inserted.

Mach> INSERT INTO count_table VALUES(null, 4);
1 row(s) inserted.

Mach> SELECT COUNT(*) FROM count_table;
COUNT(*)
-----------------------
7
[1] row(s) selected.

Mach> SELECT COUNT(id1) FROM count_table;
COUNT(id1)
-----------------------
6
[1] row(s) selected.
```


## CUME_DIST {#cume_dist}

`CUME_DIST(value, threshold)` returns the cumulative ratio of rows whose `value` is less than or equal to the given threshold.

```sql
CUME_DIST(value, threshold)
```

- This is an aggregate function, not a window function.
- Both arguments must be numeric.
- `threshold` must be a constant.
- The return value is a `DOUBLE` between `0.0` and `1.0`.

```sql
SELECT CUME_DIST(latency_ms, 100)
FROM api_log;
```


## DATE_TRUNC

This function returns a given datetime value as a new datetime value that is displayed only up to 'time unit' and 'time range'.

```sql
DATE_TRUNC (field, date_val [, count])
```

```sql
Mach> CREATE TABLE trunc_table (i1 INTEGER, i2 DATETIME);
Created successfully.

Mach> INSERT INTO trunc_table VALUES (1, TO_DATE('1999-11-11 1:2:0 4:5:1'));
1 row(s) inserted.

Mach> INSERT INTO trunc_table VALUES (2, TO_DATE('1999-11-11 1:2:0 5:5:2'));
1 row(s) inserted.

Mach> INSERT INTO trunc_table VALUES (3, TO_DATE('1999-11-11 1:2:1 6:5:3'));
1 row(s) inserted.

Mach> INSERT INTO trunc_table VALUES (4, TO_DATE('1999-11-11 1:2:1 7:5:4'));
1 row(s) inserted.

Mach> INSERT INTO trunc_table VALUES (5, TO_DATE('1999-11-11 1:2:2 8:5:5'));
1 row(s) inserted.

Mach> INSERT INTO trunc_table VALUES (6, TO_DATE('1999-11-11 1:2:2 9:5:6'));
1 row(s) inserted.

Mach> INSERT INTO trunc_table VALUES (7, TO_DATE('1999-11-11 1:2:3 10:5:7'));
1 row(s) inserted.

Mach> INSERT INTO trunc_table VALUES (8, TO_DATE('1999-11-11 1:2:3 11:5:8'));
1 row(s) inserted.

Mach> SELECT COUNT(*), DATE_TRUNC('second', i2) tm FROM trunc_table group by tm ORDER BY 2;
COUNT(*)             tm
--------------------------------------------------------
2                    1999-11-11 01:02:00 000:000:000
2                    1999-11-11 01:02:01 000:000:000
2                    1999-11-11 01:02:02 000:000:000
2                    1999-11-11 01:02:03 000:000:000
[4] row(s) selected.

Mach> SELECT COUNT(*), DATE_TRUNC('second', i2, 2) tm FROM trunc_table group by tm ORDER BY 2;
COUNT(*)             tm
--------------------------------------------------------
4                    1999-11-11 01:02:00 000:000:000
4                    1999-11-11 01:02:02 000:000:000
[2] row(s) selected.

Mach> SELECT COUNT(*), DATE_TRUNC('nanosecond', i2, 2) tm FROM trunc_table group by tm ORDER BY 2;
COUNT(*)             tm
--------------------------------------------------------
1                    1999-11-11 01:02:00 004:005:000
1                    1999-11-11 01:02:00 005:005:002
1                    1999-11-11 01:02:01 006:005:002
1                    1999-11-11 01:02:01 007:005:004
1                    1999-11-11 01:02:02 008:005:004
1                    1999-11-11 01:02:02 009:005:006
1                    1999-11-11 01:02:03 010:005:006
1                    1999-11-11 01:02:03 011:005:008
[8] row(s) selected.

Mach> SELECT COUNT(*), DATE_TRUNC('nsec', i2, 1000000000) tm FROM trunc_table group by tm ORDER BY 2; //Same as DATE_TRUNC('sec', i2, 1)
COUNT(*)             tm
--------------------------------------------------------
2                    1999-11-11 01:02:00 000:000:000
2                    1999-11-11 01:02:01 000:000:000
2                    1999-11-11 01:02:02 000:000:000
2                    1999-11-11 01:02:03 000:000:000
[4] row(s) selected.
```

The allowable time ranges for time units and time units are as follows.

* nanosecond, microsecond, and milisecond units and abbreviations can be used starting from 5.5.6.
* week is start from Sunday.

|Time Unit|Time Range|
|--|--|
|nanosecond (nsec)|1000000000 (1 second)|
|microsecond (usec)|60000000 (60 seconds)|
|milisecond (msec)|60000 (60 seconds)|
|second (sec)|86400 (1 day)|
|minute (min)|1440 (1 day)|
|hour|24 (1 day)|
|day|1|
|week|1|
|month|1|
|year|1|

For example, if you type in DATE_TRUNC('second', time, 120), the value returned will be displayed **every two minutes** and is the same as DATE_TRUNC('minute', time, 2).

## DATE_BIN
This function bins the given datetime value into a `time unit` and `time range`
based on the specified `origin`.

```sql
DATE_BIN(field, count, source [, origin])
```

- If `origin` is specified, the bin boundary is calculated from that timestamp.
- If `origin` is omitted, the bin boundary is calculated from `1970-01-01 00:00:00`
  in the server's local timezone.
- `count` must be an integer greater than or equal to 1.

Use the 3-argument form when you want local-time bucket boundaries consistent with
`DATE_TRUNC()` or `ROLLUP()`. Use the 4-argument form when you need a fixed origin
that does not depend on the server timezone.

For example, on a `UTC+09:00` server, users previously had to provide a timezone-adjusted
`origin` value instead of `DATE_BIN(..., 0)` to align with local-time boundaries. The
3-argument form now provides the same local-time alignment directly.

```sql
Mach> CREATE TABLE log (time DATETIME);
Created successfully.

Mach> INSERT INTO log VALUES (TO_DATE('2000-01-01 00:00:00'));
1 row(s) inserted.

Mach> INSERT INTO log VALUES (TO_DATE('2000-01-01 01:00:00'));
1 row(s) inserted.

Mach> INSERT INTO log VALUES (TO_DATE('2000-01-01 02:00:00'));
1 row(s) inserted.

Mach> INSERT INTO log VALUES (TO_DATE('2000-01-01 03:00:00'));
1 row(s) inserted.

Mach> INSERT INTO log VALUES (TO_DATE('2000-01-01 04:00:00'));
1 row(s) inserted.

Mach> SELECT TIME, DATE_BIN('hour', 2, time, TO_DATE('2020-01-01 00:00:00')) FROM log ORDER BY time;
TIME                            DATE_BIN('hour', 2, time, TO_DATE('2020-01-01 00:00:00'))
---------------------------------------------------------------------------------------------
2000-01-01 00:00:00 000:000:000 2000-01-01 00:00:00 000:000:000
2000-01-01 01:00:00 000:000:000 2000-01-01 00:00:00 000:000:000
2000-01-01 02:00:00 000:000:000 2000-01-01 02:00:00 000:000:000
2000-01-01 03:00:00 000:000:000 2000-01-01 02:00:00 000:000:000
2000-01-01 04:00:00 000:000:000 2000-01-01 04:00:00 000:000:000
[5] row(s) selected.
```

The following example shows local-time bucket alignment with the 3-argument form.

```sql
Mach> CREATE TABLE t3521 (ts DATETIME);
Created successfully.

Mach> INSERT INTO t3521 VALUES (TO_DATE('2000-01-01 00:30:00'));
1 row(s) inserted.

Mach> INSERT INTO t3521 VALUES (TO_DATE('2000-01-01 02:59:59'));
1 row(s) inserted.

Mach> INSERT INTO t3521 VALUES (TO_DATE('2000-01-01 03:00:00'));
1 row(s) inserted.

Mach> INSERT INTO t3521 VALUES (TO_DATE('2000-01-01 08:00:00'));
1 row(s) inserted.

Mach> SELECT ts,
             DATE_BIN('hour', 3, ts) AS date_bin_3arg,
             DATE_TRUNC('hour', ts, 3) AS date_trunc_3arg
        FROM t3521
    ORDER BY ts;
ts                              date_bin_3arg                   date_trunc_3arg
----------------------------------------------------------------------------------------------------
2000-01-01 00:30:00 000:000:000 2000-01-01 00:00:00 000:000:000 2000-01-01 00:00:00 000:000:000
2000-01-01 02:59:59 000:000:000 2000-01-01 00:00:00 000:000:000 2000-01-01 00:00:00 000:000:000
2000-01-01 03:00:00 000:000:000 2000-01-01 03:00:00 000:000:000 2000-01-01 03:00:00 000:000:000
2000-01-01 08:00:00 000:000:000 2000-01-01 06:00:00 000:000:000 2000-01-01 06:00:00 000:000:000
[4] row(s) selected.
```

The allowable time ranges for time units and time units are as follows.

* nanosecond, microsecond, and milisecond units and abbreviations can be used starting from 5.5.6.
* week is equal to 7 days.

|Time Unit|
|----:|
|nanosecond (nsec)|
|microsecond (usec)|
|milisecond (msec)|
|second (sec)|
|minute (min)|
|hour|
|day|
|week|
|month|
|year|


## DAYOFWEEK

This function returns a natural number representing the day of the week for a given datetime value.

Returns a semantically equivalent value for [TO_CHAR (time, 'DAY')](#to_char), but returns an integer here.

```sql
DAYOFWEEK(date_val)
```

The returned natural number represents the next day of the week.

|Return Value|Day of Week|
|--|--|
|0|Sunday|
|1|Monday|
|2|Tuesday|
|3|Wednesday|
|4|Thursday|
|5|Friday|
|6|Saturday|


## DECODE

This function compares the given Column value with Search, and returns the next return value if it is the same. If there is no satisfactory Search value, it returns the default value. If Default is omitted, NULL is returned.

```sql
DECODE(column, [search, return],.. default)
```

```sql
Mach> CREATE TABLE decode_table (id1 VARCHAR(11));
Created successfully.

Mach> INSERT INTO decode_table VALUES('decodetest1');
1 row(s) inserted.

Mach> INSERT INTO decode_table VALUES('decodetest2');
1 row(s) inserted.

Mach> SELECT id1, DECODE(id1, 'decodetest1', 'result1', 'decodetest2', 'result2', 'DEFAULT') FROM decode_table;
id1          DECODE(id1, 'decodetest1', 'result1', 'decodetest2', 'result2', 'DEFAULT')
---------------------------------------------------------
decodetest2  result2
decodetest1  result1
[2] row(s) selected.

Mach> SELECT id1, DECODE(id1, 'codetest', 2, 99) FROM decode_table;
id1          DECODE(id1, 'codetest', 2, 99)
-----------------------------------------------
decodetest2  99
decodetest1  99
[2] row(s) selected.

Mach> SELECT DECODE(id1, 'decodetest1', 2) FROM decode_table;
DECODE(id1, 'decodetest1', 2)
--------------------------------
NULL
2
[2] row(s) selected.

Mach> SELECT DECODE(id1, 'codetest', 2) FROM decode_table;
DECODE(id1, 'codetest', 2)
-----------------------------
NULL
NULL
[2] row(s) selected.
```


## EXTRACT_*

Bit-extraction helpers for binary frames.
`EXTRACT_*` uses a big-endian model and `EXTRACT_LE_*` uses a little-endian model.
All functions accept `BINARY/VARBINARY` frames; NULL frames return NULL.

**Endian Model**

- `EXTRACT_*`: MSB-first (`bit 0` is the MSB of `byte[0]`)
- `EXTRACT_LE_*`: LSB-first (`bit 0` is the LSB of `byte[0]`)
- Bit indexes are zero-based across the full frame.

**Common Rules**

- Single bit: `0 <= bit_pos < frame_bits`
- Bit range: `start_bit >= 0`, `1 <= bit_count <= 64`,
  `start_bit + bit_count <= frame_bits`
- `EXTRACT_FLOAT*` reads 32 bits and `EXTRACT_DOUBLE*` reads 64 bits.
- Signed extraction uses two's-complement interpretation with sign-extension to
  64-bit.
- Range errors: `ERR_QP_INVALID_ARG_VALUE` (`ERR-02229` family)
- Argument type errors: `ERR_QP_FUNCTION_ARG_TYPE`

### EXTRACT_BIT

```
EXTRACT_BIT(frame, bit_pos) / EXTRACT_LE_BIT(frame, bit_pos) → TINYINT
```

Returns a single bit as 0 or 1.

```sql
-- frame = 0x80 (1000 0000)
SELECT EXTRACT_BIT(frame, 0)    AS be_bit0,
       EXTRACT_LE_BIT(frame, 0) AS le_bit0
FROM t;
```

### EXTRACT_LONG, EXTRACT_ULONG

```
EXTRACT_ULONG(frame, start_bit, bit_count) → BIGINT UNSIGNED
EXTRACT_LE_ULONG(frame, start_bit, bit_count) → BIGINT UNSIGNED
EXTRACT_LONG(frame, start_bit, bit_count) → BIGINT
EXTRACT_LE_LONG(frame, start_bit, bit_count) → BIGINT
```

Reads 1~64 bits as unsigned or two's-complement signed integers.

```sql
-- frame = 0x12 34
SELECT EXTRACT_ULONG(frame, 0, 16)    AS be_u16,  -- 0x1234
       EXTRACT_LE_ULONG(frame, 0, 16) AS le_u16   -- 0x3412
FROM t;
```

### EXTRACT_FLOAT,EXTRACT_DOUBLE

```
EXTRACT_FLOAT(frame, start_bit) → FLOAT
EXTRACT_LE_FLOAT(frame, start_bit) → FLOAT
EXTRACT_DOUBLE(frame, start_bit) → DOUBLE
EXTRACT_LE_DOUBLE(frame, start_bit) → DOUBLE
```

Reinterprets 32/64 bits as IEEE754 float/double; the selected bit window must
fit within the frame.

```sql
SELECT EXTRACT_FLOAT(frame, 0)      AS be_f32,
       EXTRACT_LE_FLOAT(frame, 0)   AS le_f32,
       EXTRACT_DOUBLE(frame, 64)    AS be_f64,
       EXTRACT_LE_DOUBLE(frame, 64) AS le_f64
FROM sensor_bin;
```

### EXTRACT_SCALED_DOUBLE

```
EXTRACT_SCALED_DOUBLE(frame, start_bit, bit_count, signed, scale, offset) → DOUBLE
EXTRACT_LE_SCALED_DOUBLE(frame, start_bit, bit_count, signed, scale, offset) → DOUBLE
```

Reads 1~64 bits as unsigned (`signed=0`) or two's-complement signed (`signed=1`)
integer, then returns `raw * scale + offset`.

```sql
-- 20-bit sensor value, scale 0.01, offset -40.0
SELECT EXTRACT_SCALED_DOUBLE(frame, 0, 20, 0, 0.01, -40.0)    AS be_value,
       EXTRACT_LE_SCALED_DOUBLE(frame, 0, 20, 0, 0.01, -40.0) AS le_value
FROM t_bin;
```


## FIRST / LAST

This function is an aggregate function that returns the specific value of the highest (or last) record in the sequence in which the 'reference value' in each group is in order.

* FIRST: Returns a specific value from the most advanced record in the sequence
* LAST: Returns a specific value from the last record in the sequence

```sql
FIRST(sort_expr, return_expr)
LAST(sort_expr, return_expr)
```

```sql
Mach> create table firstlast_table (id integer, name varchar(20), group_no integer);
Created successfully.
Mach> insert into firstlast_table values (1, 'John', 0);
1 row(s) inserted.
Mach> insert into firstlast_table values (2, 'Grey', 1);
1 row(s) inserted.
Mach> insert into firstlast_table values (5, 'Ryan', 0);
1 row(s) inserted.
Mach> insert into firstlast_table values (4, 'Andrew', 0);
1 row(s) inserted.
Mach> insert into firstlast_table values (7, 'Kyle', 1);
1 row(s) inserted.
Mach> insert into firstlast_table values (6, 'Ross', 1);
1 row(s) inserted.

Mach> select group_no, first(id, name) from firstlast_table group by group_no;
group_no    first(id, name)
-------------------------------------
1           Grey
0           John
[2] row(s) selected.


Mach> select group_no, last(id, name) from firstlast_table group by group_no;
group_no    last(id, name)
-------------------------------------
1           Kyle
0           Ryan
```


## FROM_UNIXTIME

This function converts a 32-bit UNIXTIME value entered as an integer to a datetime datatype value. (UNIX_TIMESTAMP converts datetime data to 32-bit UNIXTIME integer data.)

```sql
FROM_UNIXTIME(unix_timestamp_value)
```

```sql
Mach> SELECT FROM_UNIXTIME(315540671) FROM TEST;
FROM_UNIXTIME(315540671)
----------------------------------
1980-01-01 11:11:11 000:000:000

Mach> SELECT FROM_UNIXTIME(UNIX_TIMESTAMP('2001-01-01')) FROM unix_table;
FROM_UNIXTIME(UNIX_TIMESTAMP('2001-01-01'))
------------------------------------------
2001-01-01 00:00:00 000:000:000
```


## FROM_TIMESTAMP

This function takes a nanosecond value that has passed since 1970-01-01 09:00 and converts it to a datetime data type.

(TO_TIMESTAMP () converts a datetime data type to nanosecond data that has passed since 1970-01-01 09:00.)

```sql
FROM_TIMESTAMP(nanosecond_time_value)
```

```sql
Mach> SELECT FROM_TIMESTAMP(1562302560007248869) FROM TEST;
FROM_TIMESTAMP(1562302560007248869)
--------------------------------------
2019-07-05 13:56:00 007:248:869
```

Both sysdate and now represent nanosecond values elapsed since 1970-01-01 09:00 at the current time, so you can use FROM_TIMESTAMP () immediately.

Of course, the results are the same without using them. This can be useful if you have sysdate and now operations in nanoseconds.

```sql
Mach> select sysdate, from_timestamp(sysdate) from test_tbl;
sysdate                         from_timestamp(sysdate)
-------------------------------------------------------------------
2019-07-05 14:00:59 722:822:443 2019-07-05 14:00:59 722:822:443
[1] row(s) selected.

Mach> select sysdate, from_timestamp(sysdate-1000000) from test_tbl;
sysdate                         from_timestamp(sysdate-1000000)
-------------------------------------------------------------------
2019-07-05 14:01:05 130:939:525 2019-07-05 14:01:05 129:939:525      -- 1 ms (1,000,000 ns) 차이가 발생함
[1] row(s) selected.
```


## GROUP_CONCAT

This function is an aggregate function that outputs the value of the corresponding column in the group in a string.

{{<callout type="warning">}}
This function cannot be used in Cluster Edition.
{{</callout>}}

```sql
GROUP_CONCAT(
     [DISTINCT] column
     [ORDER BY { unsigned_integer | column }
     [ASC | DESC] [, column ...]]
     [SEPARATOR str_val]
)
```

* DISTINCT: Duplicate values ​​are not appended if duplicate values ​​are attached.
* ORDER BY: Arranges the sequence of column values ​​to be attached according to the specified column values.
* SEPARATOR: A delimiter string used to append column values. The default value is a comma (,).

The syntax notes are as follows.

* You can specify only one column, and if you want to specify more than one column, you must use the TO_CHAR () function and the CONCAT operator (||) to make one expression.
* ORDER BY can specify other columns besides the columns to be joined, and can specify multiple columns.
* You must enter a string constant in SEPARATOR, and you can not enter a string column.

```sql
Mach> CREATE TABLE concat_table(id1 INTEGER, id2 DOUBLE, name VARCHAR(10));
Created successfully.

Mach> INSERT INTO concat_table VALUES (1, 2, 'John');
1 row(s) inserted.

Mach> INSERT INTO concat_table VALUES (2, 1, 'Ram');
1 row(s) inserted.

Mach> INSERT INTO concat_table VALUES (3, 2, 'Zara');
1 row(s) inserted.

Mach> INSERT INTO concat_table VALUES (4, 2, 'Jill');
1 row(s) inserted.

Mach> INSERT INTO concat_table VALUES (5, 1, 'Jack');
1 row(s) inserted.

Mach> INSERT INTO concat_table VALUES (6, 1, 'Jack');
1 row(s) inserted.


Mach> SELECT GROUP_CONCAT(name) AS G_NAMES FROM concat_table GROUP BY id2;
G_NAMES
------------------------------------------------------------------------------------
Jack,Jack,Ram
Jill,Zara,John
[2] row(s) selected.

Mach> SELECT GROUP_CONCAT(DISTINCT name) AS G_NAMES FROM concat_table GROUP BY Id2;
G_NAMES
------------------------------------------------------------------------------------
Jack,Ram
Jill,Zara,John
[2] row(s) selected.

Mach> SELECT GROUP_CONCAT(name SEPARATOR '.') G_NAMES FROM concat_table GROUP BY Id2;
G_NAMES
------------------------------------------------------------------------------------
Jack.Jack.Ram
Jill.Zara.John
[2] row(s) selected.

Mach> SELECT GROUP_CONCAT(name ORDER BY id1) G_NAMES, GROUP_CONCAT(id1 ORDER BY id1) G_SORTID FROM concat_table GROUP BY id2;
G_NAMES
------------------------------------------------------------------------------------
G_SORTID
------------------------------------------------------------------------------------
Ram,Jack,Jack
2,5,6
John,Zara,Jill
1,3,4
[2] row(s) selected.
```


## INSTR

This function returns the index of the number of characters in the string entered together. The index starts at 1.

* If no string pattern is found, 0 is returned.
* If the length of the string pattern to find is 0 or NULL, NULL is returned.

```sql
INSTR(target_string, pattern_string)
```

```sql
Mach> CREATE TABLE string_table(c1 VARCHAR(20));
Created successfully.

Mach> INSERT INTO string_table VALUES ('abstract');
1 row(s) inserted.

Mach> INSERT INTO string_table VALUES ('override');
1 row(s) inserted.

Mach> SELECT c1, INSTR(c1, 'act') FROM string_table;
c1                    INSTR(c1, 'act')
------------------------------------------
override              0
abstract              6
[2] row(s) selected.
```


## LEAST / GREATEST

Both functions return the smallest value (LEAST) or the largest value (GREATEST) if you specify multiple columns or values ​​as input parameters.

If the input value is 1 or absent, it is treated as an error. If the input value is NULL, NULL is returned. Therefore, if the input value is a column, it must be converted in advance using a function.
If a column (BLOB, TEXT) that can not be compared with the input value is included or type conversion is not possible for comparison, comparison is processed as an error.

```sql
LEAST(value_list, value_list,...)
GREATEST(value_list, value_list,...)
```

```sql
Mach> CREATE TABLE lgtest_table(c1 INTEGER, c2 LONG, c3 VARCHAR(10), c4 VARCHAR(5));
Created successfully.

Mach> INSERT INTO lgtest_table VALUES (1, 2, 'abstract', 'ace');
1 row(s) inserted.

Mach> INSERT INTO lgtest_table VALUES (null, 100, null, 'bag');
1 row(s) inserted.

Mach> SELECT LEAST (c1, c2) FROM lgtest_table;
LEAST (c1, c2)
-----------------------
NULL
1
[2] row(s) selected.

Mach> SELECT LEAST (c1, c2, -1) FROM lgtest_table;
LEAST (c1, c2, -1)
-----------------------
NULL
-1
[2] row(s) selected.

Mach> SELECT GREATEST(c3, c4) FROM lgtest_table;
GREATEST(c3, c4)
--------------------
NULL
ace
[2] row(s) selected.

Mach> SELECT LEAST(c3, c4) FROM lgtest_table;
LEAST(c3, c4)
-----------------
NULL
abstract
[2] row(s) selected.

Mach> SELECT LEAST(NVL(c3, 'aa'), c4) FROM lgtest_table;
LEAST(NVL(c3, 'aa'), c4)
----------------------------
aa
abstract
[2] row(s) selected.
```


## LENGTH

This function gets the length of a string column. The obtained value outputs the number of bytes in English.

```sql
LENGTH(column_name)
```

```sql
Mach> CREATE TABLE length_table (id1 INTEGER, id2 DOUBLE, name VARCHAR(15));
Created successfully.

Mach> INSERT INTO length_table VALUES(1, 10, 'Around the Horn');
1 row(s) inserted.

Mach> INSERT INTO length_table VALUES(NULL, 20, 'Alfreds Futterkiste');
1 row(s) inserted.

Mach> INSERT INTO length_table VALUES(3, NULL, 'Antonio Moreno');
1 row(s) inserted.

Mach> INSERT INTO length_table VALUES(4, 40, NULL);
1 row(s) inserted.

Mach> select * FROM length_table;
ID1         ID2                         NAME
-------------------------------------------------------------
4           40                          NULL
3           NULL                        Antonio Moreno
NULL        20                          Alfreds Futterk
1           10                          Around the Horn
[4] row(s) selected.

Mach> select id1 * 10 FROM length_table;
id1 * 10
-----------------------
40
30
NULL
10
[4] row(s) selected.

Mach> select * FROM length_table Where id1 > 1 and id2 < 50;
ID1         ID2                         NAME
-------------------------------------------------------------
4           40                          NULL
[1] row(s) selected.

Mach> select name || ' with null concat' FROM length_table;
name || ' with null concat'
------------------------------------
NULL
Antonio Moreno with null concat
Alfreds Futterk with null concat
Around the Horn with null concat
[4] row(s) selected.

Mach> select LENGTH(name) FROM length_table;
LENGTH(name)
---------------
NULL
14
15
15
[4] row(s) selected.
```


## LOWER

This function converts an English string to lowercase.

```sql
LOWER(column_name)
```

```sql
Mach> CREATE TABLE lower_table (name VARCHAR(20));
Created successfully.

Mach> INSERT INTO lower_table VALUES('');
1 row(s) inserted.

Mach> INSERT INTO lower_table VALUES('James Backley');
1 row(s) inserted.

Mach> INSERT INTO lower_table VALUES('Alfreds Futterkiste');
1 row(s) inserted.

Mach> INSERT INTO lower_table VALUES('Antonio MORENO');
1 row(s) inserted.

Mach> INSERT INTO lower_table VALUES (NULL);
1 row(s) inserted.

Mach> SELECT LOWER(name) FROM lower_table;
LOWER(name)
------------------------
NULL
antonio moreno
alfreds futterkiste
james backley
NULL
[5] row(s) selected.
```


## LPAD / RPAD

This function adds a character to the left (LPAD) or to the right (RPAD) until the input is of a given length.

The last parameter, char, can be omitted, or a space ' ' character if omitted.
If the input column value is longer than the given length, the characters are not appended but only the length is taken from the beginning.

```sql
LPAD(str, len, padstr)
RPAD(str, len, padstr)
```

```sql
Mach> CREATE TABLE pad_table (c1 integer, c2 varchar(15));
Created successfully.

Mach> INSERT INTO pad_table VALUES (1, 'Antonio');
1 row(s) inserted.

Mach> INSERT INTO pad_table VALUES (25, 'Johnathan');
1 row(s) inserted.

Mach> INSERT INTO pad_table VALUES (30, 'M');
1 row(s) inserted.

Mach> SELECT LPAD(to_char(c1), 5, '0') FROM pad_table;
LPAD(to_char(c1), 5, '0')
-----------------------------
00030
00025
00001
[3] row(s) selected.

Mach> SELECT RPAD(to_char(c1), 5, '0') FROM pad_table;
RPAD(to_char(c1), 5, '0')
-----------------------------
30000
25000
10000
[3] row(s) selected.

Mach> SELECT LPAD(c2, 5) FROM pad_table;
LPAD(c2, 5)
---------------
    M
Johna
Anton
[3] row(s) selected.

Mach> SELECT RPAD(c2, 5) FROM pad_table;
RPAD(c2, 5)
---------------
M
Johna
Anton
[3] row(s) selected.

Mach> SELECT RPAD(c2, 10, '***') FROM pad_table;
RPAD(c2, 10, '***')
-----------------------
M*********
Johnathan*
Antonio***
[3] row(s) selected.
```


## LTRIM / RTRIM

This function removes the value corresponding to the pattern string from the first parameter. The LTRIM function checks to see if the characters are in pattern from left to right, the RTRIM function from right to left, and truncates until a character not in pattern is encountered. If all the strings are present in the pattern, NULL is returned.

If you do not specify a pattern expression, use the space character '' as a basis to remove the space character.

```sql
LTRIM(column_name, pattern)
RTRIM(column_name, pattern)
```

```sql
Mach> CREATE TABLE trim_table1(name VARCHAR(10));
Created successfully.

Mach> INSERT INTO trim_table1 VALUES ('   smith   ');
1 row(s) inserted.

Mach> SELECT ltrim(name) FROM trim_table1;
ltrim(name)
---------------
smith
[1] row(s) selected.

Mach> SELECT rtrim(name) FROM trim_table1;
rtrim(name)
---------------
   smith
[1] row(s) selected.

Mach> SELECT ltrim(name, ' s') FROM trim_table1;
ltrim(name, ' s')
---------------------
mith
[1] row(s) selected.

Mach> SELECT rtrim(name, 'h ') FROM trim_table1;
rtrim(name, 'h ')
---------------------
   smit
[1] row(s) selected.

Mach> CREATE TABLE trim_table2 (name VARCHAR(10));
Created successfully.

Mach> INSERT INTO trim_table2 VALUES ('ddckaaadkk');
1 row(s) inserted.

Mach> SELECT ltrim(name, 'dc') FROM trim_table2;
ltrim(name, 'dc')
---------------------
kaaadkk
[1] row(s) selected.

Mach> SELECT rtrim(name, 'dk') FROM trim_table2;
rtrim(name, 'dk')
---------------------
ddckaaa
[1] row(s) selected.

Mach> SELECT ltrim(name, 'dckak') FROM trim_table2;
ltrim(name, 'dckak')
------------------------
NULL
[1] row(s) selected.

Mach> SELECT rtrim(name, 'dckak') FROM trim_table2;
rtrim(name, 'dckak')
------------------------
NULL
[1] row(s) selected.
```


## MAX

This function is an aggregate function that obtains the maximum value of a given numeric column.

```sql
MAX(column_name)
```

```sql
Mach> CREATE TABLE max_table (c INTEGER);
Created successfully.

Mach> INSERT INTO max_table VALUES(10);
1 row(s) inserted.

Mach> INSERT INTO max_table VALUES(20);
1 row(s) inserted.

Mach> INSERT INTO max_table VALUES(30);
1 row(s) inserted.

Mach> SELECT MAX(c) FROM max_table;
MAX(c)
--------------
30
[1] row(s) selected.
```


## MEDIAN {#median}

`MEDIAN(value)` returns the exact median of a numeric expression. In the current implementation, it behaves like `PERCENTILE_CONT(value, 0.5)`.

```sql
MEDIAN(value)
```

- `value` must be numeric.
- `NULL` values are ignored.
- The result type is `DOUBLE`.

```sql
SELECT MEDIAN(temp_c)
FROM sensor_log;
```


## MIN

This function is an aggregate function that obtains the minimum value of a corresponding numeric column.

```sql
MIN(column_name)
```

```sql
Mach> CREATE TABLE min_table(c1 INTEGER);
Created successfully.

Mach> INSERT INTO min_table VALUES(1);
1 row(s) inserted.

Mach> INSERT INTO min_table VALUES(22);
1 row(s) inserted.

Mach> INSERT INTO min_table VALUES(33);
1 row(s) inserted.

Mach> SELECT MIN(c1) FROM min_table;
MIN(c1)
--------------
1
[1] row(s) selected.
```


## NVL

This function returns value if the value of the column is NULL, or the value of the original column if it is not NULL.

```sql
NVL(string1, replace_with)
```

```sql
Mach> CREATE TABLE nvl_table (c1 varchar(10));
Created successfully.

Mach> INSERT INTO nvl_table VALUES ('Johnathan');
1 row(s) inserted.

Mach> INSERT INTO nvl_table VALUES (NULL);
1 row(s) inserted.

Mach> SELECT NVL(c1, 'Thomas') FROM nvl_table;
NVL(c1, 'Thomas')
---------------------
Thomas
Johnathan
```

## NEXTVAL

`NEXTVAL(sequence_column)` returns the next value for a Lookup table sequence column.

```sql
NEXTVAL(sequence_column)
```

- `NEXTVAL` can be used only in an `INSERT` statement.
- The argument must be a column configured with `PROPERTY(SEQUENCE=...)`.
- For sequence column creation and examples, see [Sequence Column](#sequence-column).

```sql
INSERT INTO seq_lookup (id, name) VALUES (NEXTVAL(id), 'sensor-a');
```


## ROUND

This function returns the result of rounding off the digits of the input value (input digit +1). If no digits are entered, the rounding is done at position 0. It is possible to enter a negative number in decimals place to round the decimal place.

```sql
ROUND(column_name, [decimals])
```

```sql
Mach> CREATE TABLE round_table (c1 DOUBLE);
Created successfully.

Mach> INSERT INTO round_table VALUES (1.994);
1 row(s) inserted.

Mach> INSERT INTO round_table VALUES (1.995);
1 row(s) inserted.

Mach> SELECT c1, ROUND(c1, 2) FROM round_table;
c1                          ROUND(c1, 2)
-----------------------------------------------------------
1.995                       2
1.994                       1.99
```


## ROWNUM

This function assigns a number to the SELECT query result row.

It can be used inside Subquery or Inline View that is used inside SELECT query. If you use ROWNUM () function in Inline View in Target List, you need to give Alias ​​to refer to from outside.

```sql
ROWNUM()
```

**Available Clauses**

This function can be used in the target list, GROUP BY, or ORDER BY clause of a SELECT query. However, it can not be used in the WHERE and HAVING clauses of a SELECT query. ROWNUM () If you want to control WHERE or HAVING clause with result number, you can use SELECT query with ROWNUM () in Inline View and refer to it in WHERE or HAVING clause.

|Available Clauses|Unavailable Clauses|
|--|--|
|Target List / GROUP BY / ORDER BY|WHERE / HAVING|

```sql
Mach> CREATE TABLE rownum_table(c1 INTEGER, c2 DOUBLE, c3 VARCHAR(10));
Created successfully.

Mach> INSERT INTO rownum_table VALUES(1, 1.0, '');
1 row(s) inserted.

Mach> INSERT INTO rownum_table VALUES(2, 2.0, 'Second Row');
1 row(s) inserted.

Mach> INSERT INTO rownum_table VALUES(3, 3.3, 'Third Row');
1 row(s) inserted.

Mach> INSERT INTO rownum_table VALUES(4, 4.3, 'Fourth Row');
1 row(s) inserted.

Mach> SELECT INNER_RANK, c3 AS NAME
    2 FROM   (SELECT ROWNUM() AS INNER_RANK, * FROM rownum_table)
    3 WHERE  INNER_RANK < 3;
INNER_RANK           NAME
------------------------------------
1                    Fourth Row
2                    Third Row
[2] row(s) selected.
```

**Altering Results Due to Sorting**

If there is an ORDER BY clause in the SELECT query, the result number of ROWNUM () in the target list may not be sequentially assigned. This is because the ROWNUM () operation is performed before the operation of the ORDER BY clause. If you want to give it sequentially, you can use the query containing the ORDER BY clause in Inline View and then call ROWNUM () in the outer SELECT statement.

```sql
Mach> CREATE TABLE rownum_table(c1 INTEGER, c2 DOUBLE, c3 VARCHAR(10));
Created successfully.

Mach> INSERT INTO rownum_table VALUES(1, 1.0, '');
1 row(s) inserted.

Mach> INSERT INTO rownum_table VALUES(2, 2.0, 'John');
1 row(s) inserted.

Mach> INSERT INTO rownum_table VALUES(3, 3.3, 'Sarah');
1 row(s) inserted.

Mach> INSERT INTO rownum_table VALUES(4, 4.3, 'Micheal');
1 row(s) inserted.

Mach> SELECT ROWNUM(), c2 AS SORT, c3 AS NAME
    2 FROM   ( SELECT * FROM rownum_table ORDER BY c3 );
ROWNUM()             SORT                        NAME
-----------------------------------------------------------------
1                    1                           NULL
2                    2                           John
3                    4.3                         Micheal
4                    3.3                         Sarah
[4] row(s) selected.
```


## SERIESNUM

Returns a number indicating how many of the records belong to the series grouped by SERIES BY. The return type is BIGINT type, and always returns 1 if the SERIES BY clause is not used.

```sql
SERIESNUM()
```

```sql
Mach> CREATE TABLE T1 (C1 INTEGER, C2 INTEGER);
Created successfully.

Mach> INSERT INTO T1 VALUES (0, 1);
1 row(s) inserted.

Mach> INSERT INTO T1 VALUES (1, 2);
1 row(s) inserted.

Mach> INSERT INTO T1 VALUES (2, 3);
1 row(s) inserted.

Mach> INSERT INTO T1 VALUES (3, 2);
1 row(s) inserted.

Mach> INSERT INTO T1 VALUES (4, 1);
1 row(s) inserted.

Mach> INSERT INTO T1 VALUES (5, 2);
1 row(s) inserted.

Mach> INSERT INTO T1 VALUES (6, 3);
1 row(s) inserted.

Mach> INSERT INTO T1 VALUES (7, 1);
1 row(s) inserted.


Mach> SELECT SERIESNUM(), C1, C2 FROM T1 ORDER BY C1 SERIES BY C2 > 1;
SERIESNUM() C1 C2
-------------------------------------------------
1 1 2
1 2 3
1 3 2
2 5 2
2 6 3
[5] row(s) selected.
```


## STDDEV / STDDEV_POP

This function is an aggregate function that returns the (standard) deviation and the population standard deviation of the (input) column. Equivalent to the square root of the VARIANCE and VAR_POP values, respectively.

```sql
STDDEV(column)
STDDEV_POP(column)
```

```sql
Mach> CREATE TABLE stddev_table(c1 INTEGER, C2 DOUBLE);

Mach> INSERT INTO stddev_table VALUES (1, 1);
1 row(s) inserted.

Mach> INSERT INTO stddev_table VALUES (2, 1);
1 row(s) inserted.

Mach> INSERT INTO stddev_table VALUES (3, 2);
1 row(s) inserted.

Mach> INSERT INTO stddev_table VALUES (4, 2);
1 row(s) inserted.

Mach> SELECT c2, STDDEV(c1) FROM stddev_table GROUP BY c2;
c2                          STDDEV(c1)
-----------------------------------------------------------
1                           0.707107
2                           0.707107
[2] row(s) selected.

Mach> SELECT c2, STDDEV_POP(c1) FROM stddev_table GROUP BY c2;
c2                          STDDEV_POP(c1)
-----------------------------------------------------------
1                           0.5
2                           0.5
[2] row(s) selected.
```


## SUBSTR

This function truncates the variable string column data from START to SIZE.

* START starts at 1 and returns NULL if it is zero.
* If SIZE is larger than the size of the corresponding string, only the maximum value of the string is returned.
SIZE is optional, and if omitted, it is internally specified by the size of the string.

```sql
SUBSTRING(column_name, start, [length])
```

```sql
Mach> CREATE TABLE substr_table (c1 VARCHAR(10));
Created successfully.

Mach> INSERT INTO substr_table values('ABCDEFG');
1 row(s) inserted.

Mach> INSERT INTO substr_table values('abstract');
1 row(s) inserted.

Mach> SELECT SUBSTR(c1, 1, 1) FROM substr_table;
SUBSTR(c1, 1, 1)
--------------------
a
A
[2] row(s) selected.

Mach> SELECT SUBSTR(c1, 3, 3) FROM substr_table;
SUBSTR(c1, 3, 3)
--------------------
str
CDE
[2] row(s) selected.

Mach> SELECT SUBSTR(c1, 2) FROM substr_table;
SUBSTR(c1, 2)
-----------------
bstract
BCDEFG
[2] row(s) selected.

Mach> drop table substr_table;
Dropped successfully.

Mach> CREATE TABLE substr_table (c1 VARCHAR(10));
Created successfully.

Mach> INSERT INTO substr_table values('ABCDEFG');
1 row(s) inserted.

Mach> SELECT SUBSTR(c1, 1, 1) FROM substr_table;
SUBSTR(c1, 1, 1)
--------------------
A
[1] row(s) selected.

Mach> SELECT SUBSTR(c1, 3, 3) FROM substr_table;
SUBSTR(c1, 3, 3)
--------------------
CDE
[1] row(s) selected.

Mach> SELECT SUBSTR(c1, 2) FROM substr_table;
SUBSTR(c1, 2)
-----------------
BCDEFG
[1] row(s) selected.
```


## SUBSTRING_INDEX

Returns the duplicate string until the given delim is found by the count entered. If count is a negative value, it checks the delimiter from the end of the input string and returns it from the position where the delimiter was found to the end of the string.

If you enter count as 0 or there is no delimiter in the string, the function will return NULL.

```sql
SUBSTRING_INDEX(expression, delim, count)
```

```sql
Mach> CREATE TABLE substring_table (url VARCHAR(30));
Created successfully.

Mach> INSERT INTO substring_table VALUES('www.machbase.com');
1 row(s) inserted.

Mach> SELECT SUBSTRING_INDEX(url, '.', 1) FROM substring_table;
SUBSTRING_INDEX(url, '.', 1)
----------------------------------
www
[1] row(s) selected.

Mach> SELECT SUBSTRING_INDEX(url, '.', 2) FROM substring_table;
SUBSTRING_INDEX(url, '.', 2)
----------------------------------
www.machbase
[1] row(s) selected.

Mach> SELECT SUBSTRING_INDEX(url, '.', -1) FROM substring_table;
SUBSTRING_INDEX(url, '.', -1)
----------------------------------
com
[1] row(s) selected.

Mach> SELECT SUBSTRING_INDEX(SUBSTRING_INDEX(url, '.', 2), '.', -1) FROM substring_table;
SUBSTRING_INDEX(SUBSTRING_INDEX(url, '.', 2), '.', -1)
-------------------------------------------
machbase
[1] row(s) selected.

Mach> SELECT SUBSTRING_INDEX(url, '.', 0) FROM substring_table;
SUBSTRING_INDEX(url, '.', 0)
----------------------------------
NULL
[1] row(s) selected.
```


## SUM

This function is an aggregate function that represents the sum of the numeric columns.

```sql
SUM(column_name)
```

```sql
Mach> CREATE TABLE sum_table (c1 INTEGER, c2 INTEGER);
Created successfully.

Mach> INSERT INTO sum_table VALUES(1, 1);
1 row(s) inserted.

Mach> INSERT INTO sum_table VALUES(1, 2);
1 row(s) inserted.

Mach> INSERT INTO sum_table VALUES(1, 3);
1 row(s) inserted.

Mach> INSERT INTO sum_table VALUES(2, 1);
1 row(s) inserted.

Mach> INSERT INTO sum_table VALUES(2, 2);
1 row(s) inserted.

Mach> INSERT INTO sum_table VALUES(2, 3);
1 row(s) inserted.

Mach> INSERT INTO sum_table VALUES(3, 4);
1 row(s) inserted.

Mach> SELECT c1, SUM(c1) from sum_table group by c1;
c1          SUM(c1)
------------------------------------
2           6
3           3
1           3
[3] row(s) selected.

Mach> SELECT c1, SUM(c2) from sum_table group by c1;
c1          SUM(c2)
------------------------------------
2           6
3           4
1           6
[3] row(s) selected.
```


## SUMSQ

SUMSQ returns the sum of squares of the numeric values.

```sql
SUMSQ(value)
```

```sql
Mach> CREATE TABLE sumsq_table (c1 INTEGER, c2 INTEGER);
Created successfully.

Mach> INSERT INTO sumsq_table VALUES (1, 1);
1 row(s) inserted.

Mach> INSERT INTO sumsq_table VALUES (1, 2);
1 row(s) inserted.

Mach> INSERT INTO sumsq_table VALUES (1, 3);
1 row(s) inserted.

Mach> INSERT INTO sumsq_table VALUES (2, 4);
1 row(s) inserted.

Mach> INSERT INTO sumsq_table VALUES (2, 5);
1 row(s) inserted.

Mach> SELECT c1, SUMSQ(c2) FROM sumsq_table GROUP BY c1;
c1          SUMSQ(c2)
------------------------------------
2           41
1           14
[2] row(s) selected.
```


## SYSDATE / NOW

SYSDATE is a pseudocolumn, not a function, that returns the system's current time.

NOW is the same function as SYSDATE and is provided for user convenience.

```sql
SYSDATE
NOW
```

```sql
Mach> SELECT SYSDATE, NOW FROM t1;

SYSDATE                         NOW
-------------------------------------------------------------------
2017-01-16 14:14:53 310:973:000 2017-01-16 14:14:53 310:973:000
```


## TO_CHAR

This function converts a given data type to a string type. Depending on the type, format_string may be specified, but not for binary types.

```sql
TO_CHAR(column)
```

**TO_CHAR: Default Datatype**

The default data types are converted to data in the form of strings as shown below.

```sql
Mach> CREATE TABLE fixed_table (id1 SHORT, id2 INTEGER, id3 LONG, id4 FLOAT, id5 DOUBLE, id6 IPV4, id7 IPV6, id8 VARCHAR (128));
Created successfully.

Mach> INSERT INTO fixed_table values(200, 19234, 1234123412, 3.14, 7.8338, '192.168.0.1', '::127.0.0.1', 'log varchar');
1 row(s) inserted.

Mach> SELECT '[ ' || TO_CHAR(id1) || ' ]' FROM fixed_table;
'[ ' || TO_CHAR(id1) || ' ]'
------------------------------------------------------------------------------------
[ 200 ]
[1] row(s) selected.

Mach> SELECT '[ ' || TO_CHAR(id2) || ' ]' FROM fixed_table;
'[ ' || TO_CHAR(id2) || ' ]'
------------------------------------------------------------------------------------
[ 19234 ]
[1] row(s) selected.

Mach> SELECT '[ ' || TO_CHAR(id3) || ' ]' FROM fixed_table;
'[ ' || TO_CHAR(id3) || ' ]'
------------------------------------------------------------------------------------
[ 1234123412 ]
[1] row(s) selected.

Mach> SELECT '[ ' || TO_CHAR(id4) || ' ]' FROM fixed_table;
'[ ' || TO_CHAR(id4) || ' ]'
------------------------------------------------------------------------------------
[ 3.140000 ]
[1] row(s) selected.

Mach> SELECT '[ ' || TO_CHAR(id5) || ' ]' FROM fixed_table;
'[ ' || TO_CHAR(id5) || ' ]'
------------------------------------------------------------------------------------
[ 7.833800 ]
[1] row(s) selected.

Mach> SELECT '[ ' || TO_CHAR(id6) || ' ]' FROM fixed_table;
'[ ' || TO_CHAR(id6) || ' ]'
------------------------------------------------------------------------------------
[ 192.168.0.1 ]
[1] row(s) selected.

Mach> SELECT '[ ' || TO_CHAR(id7) || ' ]' FROM fixed_table;
'[ ' || TO_CHAR(id7) || ' ]'
------------------------------------------------------------------------------------
[ 0000:0000:0000:0000:0000:0000:7F00:0001 ]
[1] row(s) selected.

Mach> SELECT '[ ' || TO_CHAR(id8) || ' ]' FROM fixed_table;
'[ ' || TO_CHAR(id8) || ' ]'
------------------------------------------------------------------------------------
[ log varchar ]
[1] row(s) selected.
```

**TO_CHAR: Floating Point Number**

* Supported from 5.5.6 version

This function converts the values ​​of float and double into strings.
Format expression cannot be used repeatedly, and must be entered in the form of '[letter][number]'.

|Format Expression|Descibe|
|--|--|
|F / f|Specifies the number of decimal places for the column value. The maximum numeric value to input is 30.|
|N / n|Specify the number of decimal places for the column value, and enter a comma (,) for every three digits of the integer part. The maximum numeric value to input is 30.|

```sql
Mach> create table float_table (i1 float, i2 double);
Created successfully.

Mach> insert into float_table values (1.23456789, 1234.5678901234567890);
1 row(s) inserted.

Mach> select TO_CHAR(i1, 'f8'), TO_CHAR(i2, 'N9') from float_table;
TO_CHAR(i1, 'f8')       TO_CHAR(i2, 'N9')
--------------------------------------------------------------
1.23456788              1,234.567890123
[1] row(s) selected.
```

**TO_CHAR: DATETIME Type**

A function that converts the value of a datetime column to an arbitrary string. You can use this function to create and combine various types of strings.

If format_string is omitted, the default is "YYYY-MM-DD HH24: MI: SS mmm: uuu: nnn".

|Format Expression|Descibe|
|--|--|
|YYYY|Converts year to a four-digit number.|
|YY|Converts year to a two-digit number.|
|MM|Converts the month to a two-digit number.|
|MON|Converts the month to a three-digit abbreviated alphabet. (eg JAN, FEB, MAY, ...)|
|DD|Converts the day to a two-digit number.|
|DAY|Converts the day of the week to a three-digit abbreviation . (eg SUN, MON, ...)|
|IW|Converts the week number of a specific year from 1 to 53 (taking into account the day of the week) by the ISO 8601 rule.<br> - The start of one week is Monday.<br> - The first week can be considered as the last week of the previous year. Likewise, the last week can be considered the first week of the next year.<br>    See ISO 8601 more information.|
|WW|Converts week number of the particular year from 1 to 53 (Week Number) not taking into account the day of the week.<br>That is, from January 1 to January 7, it is converted to 1.|
|W|Converts week number of a given month from 1 to 5 (Number The Week) not taking in to account the day of the week.<br>That is, from March 1 to March 7 is converted to 1.|
|HH|Converts the time to a two-digit number.|
|HH12|Converts the time to a 2-digit number, from 1 to 12.|
|HH24|Converts the time to a 2-digit number, from 1 to 23.|
|HH2, HH3, HH6|Cuts the time to the number following HH.<br><br>That is, when HH6 is used, 0 is expressed from 0 to 5, and 6 is expressed from 6 to 11.<br>This expression is useful for calculating certain time-series statistics on time series.<br>This value is expressed on a 24-hour basis.|
|MI|The minute is represented by a two-digit number.|
|MI2, MI5, MI10, MI20, MI30|The corresponding minute is cut to the number following MI.<br><br>That is, when MI30 is used, 0 is expressed from 0 to 29 minutes, and 30 is represented from 30 to 59 minutes.<br>This expression is useful for calculating certain time-series statistics on time series.|
|SS|The second is represented by a two-digit number.|
|SS2, SS5, SS10, SS20, SS30|The corresponding seconds are truncated to successive digits.<br><br>That is, when SS30 is used, 0 is expressed from 0 to 29 seconds, and 30 is represented from 30 to 59 seconds.<br>This expression is useful for calculating certain time-series statistics on time series.|
|AM|The current time is expressed in AM or PM according to AM and PM, respectively.|
|mmm|The millisecond of the time is represented by a three-digit number.<br><br>The range of values ​​is 0 to 999.|
|uuu|The micro second of the time is represented as a three-digit number.<br><br>The range of values ​​is 0 to 999.|
|nnn|The nano second of the time is expressed as a three-digit number.<br><br>The range of values ​​is 0 to 999.|

```sql
Mach> CREATE TABLE datetime_table (id integer, dt datetime);
Created successfully.

Mach> INSERT INTO  datetime_table values(1, TO_DATE('1999-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  datetime_table values(2, TO_DATE('2012-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  datetime_table values(3, TO_DATE('2013-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  datetime_table values(4, TO_DATE('2014-12-30 11:22:33 444:555:666'));
1 row(s) inserted.

Mach> SELECT id, dt FROM datetime_table WHERE dt > TO_DATE('2000-11-11 1:2:3 4:5:0');
id          dt
-----------------------------------------------
4           2014-12-30 11:22:33 444:555:666
3           2013-11-11 01:02:03 004:005:006
2           2012-11-11 01:02:03 004:005:006
[3] row(s) selected.

Mach> SELECT id, dt FROM datetime_table WHERE dt > TO_DATE('2013-11-11 1:2:3') and dt < TO_DATE('2014-11-11 1:2:3');
id          dt
-----------------------------------------------
3           2013-11-11 01:02:03 004:005:006
[1] row(s) selected.

Mach> SELECT id, TO_CHAR(dt) FROM datetime_table;
id          TO_CHAR(dt)
-------------------------------------------------------------------------------------------------
4           2014-12-30 11:22:33 444:555:666
3           2013-11-11 01:02:03 004:005:006
2           2012-11-11 01:02:03 004:005:006
1           1999-11-11 01:02:03 004:005:006
[4] row(s) selected.

Mach> SELECT id, TO_CHAR(dt, 'YYYY') FROM datetime_table;
id          TO_CHAR(dt, 'YYYY')
-------------------------------------------------------------------------------------------------
4           2014
3           2013
2           2012
1           1999
[4] row(s) selected.

Mach> SELECT id, TO_CHAR(dt, 'YYYY-MM') FROM datetime_table;
id          TO_CHAR(dt, 'YYYY-MM')
-------------------------------------------------------------------------------------------------
4           2014-12
3           2013-11
2           2012-11
1           1999-11
[4] row(s) selected.

Mach> SELECT id, TO_CHAR(dt, 'YYYY-MM-DD') FROM datetime_table;
id          TO_CHAR(dt, 'YYYY-MM-DD')
-------------------------------------------------------------------------------------------------
4           2014-12-30
3           2013-11-11
2           2012-11-11
1           1999-11-11
[4] row(s) selected.

Mach> SELECT id, TO_CHAR(dt, 'YYYY-MM-DD TO_CHAR') FROM datetime_table;
id          TO_CHAR(dt, 'YYYY-MM-DD TO_CHAR')
-------------------------------------------------------------------------------------------------
4           2014-12-30 TO_CHAR
3           2013-11-11 TO_CHAR
2           2012-11-11 TO_CHAR
1           1999-11-11 TO_CHAR
[4] row(s) selected.

Mach> SELECT id, TO_CHAR(dt, 'YYYY-MM-DD HH24:MI:SS') FROM datetime_table;
id          TO_CHAR(dt, 'YYYY-MM-DD HH24:MI:SS')
-------------------------------------------------------------------------------------------------
4           2014-12-30 11:22:33
3           2013-11-11 01:02:03
2           2012-11-11 01:02:03
1           1999-11-11 01:02:03
[4] row(s) selected.

Mach> SELECT id, TO_CHAR(dt, 'YYYY-MM-DD HH24:MI:SS mmm.uuu.nnn') FROM datetime_table;
id          TO_CHAR(dt, 'YYYY-MM-DD HH24:MI:SS mmm.
-------------------------------------------------------------------------------------------------
4           2014-12-30 11:22:33 444.555.666
3           2013-11-11 01:02:03 004.005.006
2           2012-11-11 01:02:03 004.005.006
1           1999-11-11 01:02:03 004.005.006
[4] row(s) selected.
```

**TO_CHAR: Unsupported Type**

Currently, TO_CHAR is not supported for binary types.

This is because it is impossible to convert to plain text. If you want to output it to the screen, you can check it by outputting hexadecimal value through TO_HEX () function.


## TO_DATE

This function converts a string represented by a given format string to a datetime type.

If format_string is omitted, the default is "YYYY-MM-DD HH24: MI: SS mmm: uuu: nnn".

```sql
-- default format is "YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn" if no format exists.
TO_DATE(date_string [, format_string])
```

```sql
Mach> CREATE TABLE to_date_table (id INTEGER, dt datetime);
Created successfully.

Mach> INSERT INTO  to_date_table VALUES(1, TO_DATE('1999-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  to_date_table VALUES(2, TO_DATE('2012-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  to_date_table VALUES(3, TO_DATE('2014-12-30 11:22:33 444:555:666'));
1 row(s) inserted.

Mach> INSERT INTO  to_date_table VALUES(4, TO_DATE('2014-12-30 23:22:34 777:888:999', 'YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn'));
1 row(s) inserted.

Mach> SELECT id, dt FROM to_date_table WHERE dt > TO_DATE('1999-11-11 1:2:3 4:5:0');
id          dt
-----------------------------------------------
4           2014-12-30 23:22:34 777:888:999
3           2014-12-30 11:22:33 444:555:666
2           2012-11-11 01:02:03 004:005:006
1           1999-11-11 01:02:03 004:005:006
[4] row(s) selected.

Mach> SELECT id, dt FROM to_date_table WHERE dt > TO_DATE('2000-11-11 1:2:3 4:5:0');
id          dt
-----------------------------------------------
4           2014-12-30 23:22:34 777:888:999
3           2014-12-30 11:22:33 444:555:666
2           2012-11-11 01:02:03 004:005:006
[3] row(s) selected.

Mach> SELECT id, dt FROM to_date_table WHERE dt > TO_DATE('2012-11-11 1:2:3','YYYY-MM-DD HH24:MI:SS') and dt < TO_DATE('2014-11-11 1:2:3','YYYY-MM-DD HH24:MI:SS');
id          dt
-----------------------------------------------
2           2012-11-11 01:02:03 004:005:006
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999', 'YYYY') FROM to_date_table LIMIT 1;
id          TO_DATE('1999', 'YYYY')
-----------------------------------------------
4           1999-01-01 00:00:00 000:000:000
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999-12', 'YYYY-MM') FROM to_date_table LIMIT 1;
id          TO_DATE('1999-12', 'YYYY-MM')
-----------------------------------------------
4           1999.12.01 00:00:00 000:000:000
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999', 'YYYY') FROM to_date_table LIMIT 1;
id          TO_DATE('1999', 'YYYY')
-----------------------------------------------
4           1999-01-01 00:00:00 000:000:000
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999-12', 'YYYY-MM') FROM to_date_table LIMIT 1;
id          TO_DATE('1999-12', 'YYYY-MM')
-----------------------------------------------
4           1999-12-01 00:00:00 000:000:000
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999-12-31 13:12', 'YYYY-MM-DD HH24:MI') FROM to_date_table LIMIT 1;
id          TO_DATE('1999-12-31 13:12', 'YYYY-MM-DD HH24:MI')
-------------------------------------------------------
4           1999-12-31 13:12:00 000:000:000
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999-12-31 13:12:32', 'YYYY-MM-DD HH24:MI:SS') FROM to_date_table LIMIT 1;
id          TO_DATE('1999-12-31 13:12:32', 'YYYY-MM-DD HH24:MI:SS')
-------------------------------------------------------
4           1999-12-31 13:12:32 000:000:000
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999-12-31 13:12:32 123', 'YYYY-MM-DD HH24:MI:SS mmm') FROM to_date_table LIMIT 1;
id          TO_DATE('1999-12-31 13:12:32 123', 'YYYY-MM-DD HH24:MI:SS mmm')
-------------------------------------------------------
4           1999-12-31 13:12:32 123:000:000
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999-12-31 13:12:32 123:456', 'YYYY-MM-DD HH24:MI:SS mmm:uuu') FROM to_date_table LIMIT 1;
id          TO_DATE('1999-12-31 13:12:32 123:456', 'YYYY-MM-DD HH24:MI:SS mmm:uuu')
-------------------------------------------------------
4           1999-12-31 13:12:32 123:456:000
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999-12-31 13:12:32 123:456:789', 'YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn') FROM to_date_table LIMIT 1;
id           TO_DATE('1999-12-31 13:12:32 123:456:789', 'YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn')
-------------------------------------------------------
4           1999-12-31 13:12:32 123:456:789
[1] row(s) selected.
```


## TO_DATE_SAFE

Similar to TO_DATE (), but returns NULL without error if conversion fails.

```sql
TO_DATE_SAFE(date_string [, format_string])
```

```sql
Mach> CREATE TABLE date_table (ts DATETIME);
Created successfully.

Mach> INSERT INTO date_table VALUES (TO_DATE_SAFE('2016-01-01', 'YYYY-MM-DD'));
1 row(s) inserted.
Mach> INSERT INTO date_table VALUES (TO_DATE_SAFE('2016-01-02', 'YYYY'));
1 row(s) inserted.
Mach> INSERT INTO date_table VALUES (TO_DATE_SAFE('2016-12-32', 'YYYY-MM-DD'));
1 row(s) inserted.

Mach> SELECT ts FROM date_table;
ts
----------------------------------
NULL
NULL
2016-01-01 00:00:00 000:000:000
[3] row(s) selected.
```


## TO_HEX

This function returns value if the value of the column is NULL, or the value of the original column if it is not NULL. To ensure consistency of output, convert to BIG ENDIAN type for short, int, and long types.

```sql
TO_HEX(column)
```

```sql
Mach> CREATE TABLE hex_table (id1 SHORT, id2 INTEGER, id3 VARCHAR(10), id4 FLOAT, id5 DOUBLE, id6 LONG, id7 IPV4, id8 IPV6, id9 TEXT, id10 BINARY,
id11 DATETIME);
Created successfully.

Mach> INSERT INTO hex_table VALUES(256, 65535, '0123456789', 3.141592, 1024 * 1024 * 1024 * 3.14, 13513135446, '192.168.0.1', '::192.168.0.1', 'textext',
'binary', TO_DATE('1999', 'YYYY'));
1 row(s) inserted.

Mach> SELECT TO_HEX(id1), TO_HEX(id2), TO_HEX(id3), TO_HEX(id4), TO_HEX(id5), TO_HEX(id6), TO_HEX(id7), TO_HEX(id8), TO_HEX(id9), TO_HEX(id10), TO_HEX(id11)
FROM hex_table;
TO_HEX(id1)  TO_HEX(id2)  TO_HEX(id3)            TO_HEX(id4)  TO_HEX(id5)        TO_HEX(id6)        TO_HEX(id7)
-------------------------------------------------------------------------------------------------------------------------
TO_HEX(id8)                          TO_HEX(id9)
--------------------------------------------------------------------------------------------------------------------------
TO_HEX(id10)                                                                      TO_HEX(id11)
--------------------------------------------------------------------------------------------------------
0100   0000FFFF   30313233343536373839   D80F4940   1F85EB51B81EE941   0000000325721556   04C0A80001
06000000000000000000000000C0A80001   74657874657874
62696E617279                                                                      0CB325846E226000
[1] row(s) selected.
```


## TO_INET_STR

`TO_INET_STR(ipv4_value)` converts an `IPV4` value to dotted-decimal text.

```sql
TO_INET_STR(ipv4_value)
```

```sql
SELECT TO_INET_STR(TO_IPV4('192.168.0.1'));
```


## TO_IPV4 / TO_IPV4_SAFE

This function converts a given string to an IP version 4 type. If the string can not be converted to a numeric value, the TO_IPV4 () function returns an error and terminates the operation.

However, in the case of the TO_IPV4_SAFE () function, NULL is returned in case of error, and the operation can continue.

```sql
TO_IPV4(string_value)
TO_IPV4_SAFE(string_value)
```

```sql
Mach> CREATE TABLE ipv4_table (c1 varchar(100));
Created successfully.

Mach> INSERT INTO ipv4_table VALUES('192.168.0.1');
1 row(s) inserted.

Mach> INSERT INTO ipv4_table VALUES('     192.168.0.2    ');
1 row(s) inserted.

Mach> INSERT INTO ipv4_table VALUES(NULL);
1 row(s) inserted.

Mach> SELECT c1 FROM ipv4_table;
c1
------------------------------------------------------------------------------------
NULL
     192.168.0.2
192.168.0.1
[3] row(s) selected.

Mach> SELECT TO_IPV4(c1) FROM ipv4_table;
TO_IPV4(c1)
------------------
NULL
192.168.0.2
192.168.0.1
[3] row(s) selected.

Mach> INSERT INTO ipv4_table VALUES('192.168.0.1.1');
1 row(s) inserted.

Mach> SELECT TO_IPV4(c1) FROM ipv4_table limit 1;
TO_IPV4(c1)
------------------
[ERR-02068 : Invalid IPv4 address format (192.168.0.1.1).]
[0] row(s) selected.

Mach> SELECT TO_IPV4_SAFE(c1) FROM ipv4_table;
TO_IPV4_SAFE(c1)
-------------------
NULL
NULL
192.168.0.2
192.168.0.1
[4] row(s) selected.
```


## TO_IPV6 / TO_IPV6_SAFE

This function converts a given string to an IP version 6 type. If the string can not be converted to a numeric type, the TO_IPV6 () function returns an error and terminates the operation.

However, in the case of the TO_IPV6_SAFE () function, NULL is returned in case of error, and the operation can continue.

```sql
TO_IPV6(string_value)
TO_IPV6_SAFE(string_value)
```

```sql
Mach> CREATE TABLE ipv6_table (id varchar(100));
Created successfully.

Mach> INSERT INTO ipv6_table VALUES('::0.0.0.0');
1 row(s) inserted.

Mach> INSERT INTO ipv6_table VALUES('::127.0.0.1');
1 row(s) inserted.

Mach> INSERT INTO ipv6_table VALUES('::127.0' || '.0.2');
1 row(s) inserted.

Mach> INSERT INTO ipv6_table VALUES('   ::127.0.0.3');
1 row(s) inserted.

Mach> INSERT INTO ipv6_table VALUES('::127.0.0.4  ');
1 row(s) inserted.

Mach> INSERT INTO ipv6_table VALUES('   ::FFFF:255.255.255.255   ');
1 row(s) inserted.

Mach> INSERT INTO ipv6_table VALUES('21DA:D3:0:2F3B:2AA:FF:FE28:9C5A');
1 row(s) inserted.

Mach> SELECT TO_IPV6(id) FROM ipv6_table;
TO_IPV6(id)
---------------------------------------------------------------
21da:d3::2f3b:2aa:ff:fe28:9c5a
::ffff:255.255.255.255
::127.0.0.4
::127.0.0.3
::127.0.0.2
::127.0.0.1
::
[7] row(s) selected.

Mach> INSERT INTO ipv6_table VALUES('127.0.0.10.10');
1 row(s) inserted.

Mach> SELECT TO_IPV6(id) FROM ipv6_table limit 1;
TO_IPV6(id)
---------------------------------------------------------------
[ERR-02148 : Invalid IPv6 address format.(127.0.0.10.10)]
[0] row(s) selected.

Mach> SELECT TO_IPV6_SAFE(id) FROM ipv6_table;
TO_IPV6_SAFE(id)
---------------------------------------------------------------
NULL
21da:d3::2f3b:2aa:ff:fe28:9c5a
::ffff:255.255.255.255
::127.0.0.4
::127.0.0.3
::127.0.0.2
::127.0.0.1
::
[8] row(s) selected.
```


## TO_NUMBER / TO_NUMBER_SAFE

This function converts a given string to a numeric double. If the string can not be converted to a numeric value, the TO_NUMBER () function returns an error and terminates the operation.

However, in case of TO_NUMBER_SAFE () function, NULL is returned in case of error, and the operation can continue.

```sql
TO_NUMBER(string_value)
TO_NUMBER_SAFE(string_value)
```

```sql
Mach> CREATE TABLE number_table (id varchar(100));
Created successfully.

Mach> INSERT INTO number_table VALUES('10');
1 row(s) inserted.

Mach> INSERT INTO number_table VALUES('20');
1 row(s) inserted.

Mach> INSERT INTO number_table VALUES('30');
1 row(s) inserted.

Mach> SELECT TO_NUMBER(id) from number_table;
TO_NUMBER(id)
------------------------------
30
20
10
[3] row(s) selected.

Mach> CREATE TABLE safe_table (id varchar(100));
Created successfully.

Mach> INSERT INTO safe_table VALUES('invalidnumber');
1 row(s) inserted.

Mach> SELECT TO_NUMBER(id) from safe_table;
TO_NUMBER(id)
------------------------------
[ERR-02145 : The string cannot be converted to number value.(invalidnumber)]
[0] row(s) selected.

Mach> SELECT TO_NUMBER_SAFE(id) from safe_table;
TO_NUMBER_SAFE(id)
------------------------------
NULL
[1] row(s) selected.
```


## TOP_K {#top_k}

`TOP_K(value, k)` returns the most frequent `k` numeric values as a comma-separated `value:count` string.

```sql
TOP_K(value, k)
```

- `value` must be numeric.
- `k` must be a positive constant integer.
- `NULL` values are ignored.
- The result type is `VARCHAR`.
- Rows are ordered by frequency descending and, for ties, value ascending.

```sql
SELECT TOP_K(alarm_code, 3)
FROM event_log;
```

Example result:

```text
101:532,205:317,301:90
```


## TO_TIMESTAMP

This function converts a datetime data type to nanosecond data that has passed since 1970-01-01 09:00.

```sql
TO_TIMESTAMP(datetime_value)
```

```sql
Mach> create table datetime_tbl (c1 datetime);
Created successfully.

Mach> insert into datetime_tbl values ('2010-01-01 10:10:10');
1 row(s) inserted.

Mach> select to_timestamp(c1) from datetime_tbl;
to_timestamp(c1)
-----------------------
1262308210000000000
[1] row(s) selected.
```


## TRUNC

The TRUNC function returns the number truncated at the nth place after the decimal point.

If n is omitted, treat it as 0 and delete all decimal places. If n is negative, it returns the value truncated from n before the decimal point.

```sql
TRUNC(number [, n])
```

```sql
Mach> CREATE TABLE trunc_table (i1 DOUBLE);
Created successfully.

Mach> INSERT INTO trunc_table VALUES (158.799);
1 row(s) inserted.

Mach> SELECT TRUNC(i1, 1), TRUNC(i1, -1) FROM trunc_table;
TRUNC(i1, 1)                TRUNC(i1, -1)
-----------------------------------------------------------
158.7                       150
[1] row(s) selected.

Mach> SELECT TRUNC(i1, 2), TRUNC(i1, -2) FROM trunc_table;
TRUNC(i1, 2)                TRUNC(i1, -2)
-----------------------------------------------------------
158.79                      100
[1] row(s) selected.
```


## TS_CHANGE_COUNT

This function is an aggregate function that obtains the number of changes to a particular column value.

This function can not be used with 1) Join or 2) Inline view because it can be guaranteed that input data is input in chronological order.
The current version only supports types except varchar.

* **This function cannot be used in Cluster Edition.**

```sql
TS_CHANGE_COUNT(column)
```

```sql
Mach> CREATE TABLE ipcount_table (id INTEGER, ip IPV4);
Created successfully.

Mach> INSERT INTO ipcount_table VALUES (1, '192.168.0.1');
1 row(s) inserted.

Mach> INSERT INTO ipcount_table VALUES (1, '192.168.0.2');
1 row(s) inserted.

Mach> INSERT INTO ipcount_table VALUES (1, '192.168.0.1');
1 row(s) inserted.

Mach> INSERT INTO ipcount_table VALUES (1, '192.168.0.2');
1 row(s) inserted.

Mach> INSERT INTO ipcount_table VALUES (2, '192.168.0.3');
1 row(s) inserted.

Mach> INSERT INTO ipcount_table VALUES (2, '192.168.0.3');
1 row(s) inserted.

Mach> INSERT INTO ipcount_table VALUES (2, '192.168.0.4');
1 row(s) inserted.

Mach> INSERT INTO ipcount_table VALUES (2, '192.168.0.4');
1 row(s) inserted.

Mach> SELECT id, TS_CHANGE_COUNT(ip) from ipcount_table GROUP BY id;
id          TS_CHANGE_COUNT(ip)
------------------------------------
2           2
1           4
[2] row(s) selected.
```


## UNIX_TIMESTAMP

UNIX_TIMESTAMP is a function that converts a date type value to a 32-bit integer value that is converted by unix's time () system call. (FROM_UNIXTIME is a function that converts integer data to a date type value on the contrary.)

```sql
UNIX_TIMESTAMP(datetime_value)
```

```sql
Mach> CREATE table unix_table (c1 int);
Created successfully.

Mach> INSERT INTO unix_table VALUES (UNIX_TIMESTAMP('2001-01-01'));
1 row(s) inserted.

Mach> SELECT * FROM unix_table;
C1
--------------
978274800
[1] row(s) selected.
```


## UPPER

This function converts the contents of a given English column to uppercase.

```sql
UPPER(string_value)
```

```sql
Mach> CREATE TABLE upper_table(id INTEGER,name VARCHAR(10));
Created successfully.

Mach> INSERT INTO upper_table VALUES(1, '');
1 row(s) inserted.

Mach> INSERT INTO upper_table VALUES(2, 'James');
1 row(s) inserted.

Mach> INSERT INTO upper_table VALUES(3, 'sarah');
1 row(s) inserted.

Mach> INSERT INTO upper_table VALUES(4, 'THOMAS');
1 row(s) inserted.

Mach> SELECT id, UPPER(name) FROM upper_table;
id          UPPER(name)
----------------------------
4           THOMAS
3           SARAH
2           JAMES
1           NULL
[4] row(s) selected.
```


## VARIANCE / VAR_POP

This function is an aggregate function that returns the variance of a given numeric column value. The Variance function returns the variance for the sample, and the VAR_POP function returns the variance for the population.

```sql
VARIANCE(column_name)
VAR_POP(column_name)
```

```sql
Mach> CREATE TABLE var_table(c1 INTEGER, c2 DOUBLE);
Created successfully.

Mach> INSERT INTO var_table VALUES (1, 1);
1 row(s) inserted.

Mach> INSERT INTO var_table VALUES (2, 1);
1 row(s) inserted.

Mach> INSERT INTO var_table VALUES (1, 2);
1 row(s) inserted.

Mach> INSERT INTO var_table VALUES (2, 2);
1 row(s) inserted.

Mach> SELECT VARIANCE(c1) FROM var_table;
VARIANCE(c1)
------------------------------
0.333333
[1] row(s) selected.

Mach> SELECT VAR_POP(c1) FROM var_table;
VAR_POP(c1)
------------------------------
0.25
[1] row(s) selected.
```


## YEAR / MONTH / DAY

These functions extract the corresponding year, month, and day from the input datetime column value and return it as an integer type value.

```sql
YEAR(datetime_col)
MONTH(datetime_col)
DAY(datetime_col)
```

```sql
Mach> CREATE TABLE extract_table(c1 DATETIME, c2 INTEGER);
Created successfully.

Mach> INSERT INTO extract_table VALUES (to_date('2001-01-01 12:30:00 000:000:000'), 1);
1 row(s) inserted.

Mach> SELECT YEAR(c1), MONTH(c1), DAY(c1) FROM extract_table;
year(c1)    month(c1)   day(c1)
----------------------------------------
2001        1           1
```


## ISNAN / ISINF

This function determines whether the numeric value received as an argument is a NaN or Inf value. Returns 1 for NaN or Inf values, and 0 otherwise.

```sql
ISNAN(number)
ISINF(number)
```

The following example assumes that the table already contains `NaN` and `Inf` values.
Bare `nan` or `inf` tokens are not valid values for a SQL `INSERT` statement.

```sql
Mach> SELECT * FROM test;
I1                          I2                          I3
------------------------------------------------------------------------
1                           1                           1
nan                         inf                         0
NULL                        NULL                        NULL
[3] row(s) selected.


Mach> SELECT ISNAN(i1), ISNAN(i2), ISNAN(i3), i3 FROM test ;
ISNAN(i1)   ISNAN(i2)   ISNAN(i3)   i3
-----------------------------------------------------
0           0           0           1
1           0           0           0
NULL        NULL        NULL        NULL
[3] row(s) selected.

Mach> SELECT * FROM test WHERE ISNAN(i1) = 1;
I1                          I2                          I3
------------------------------------------------------------------------
nan                         inf                         0
[1] row(s) selected.
```

## JSON_SET

Stores a SQL scalar value at the given path as a JSON scalar.

```sql
JSON_SET(json_doc, path, scalar)
```

```sql
Mach> SELECT JSON_SET('{"ship":{"status":"READY"}}', '$.ship.status', 'DONE') FROM dual;
JSON_SET('{"ship":{"status":"READY"}}', '$.ship.status', 'DONE')
--------------------------------------------------------------------------------
{"ship":{"status":"DONE"}}
[1] row(s) selected.
```

Notes:

- `path` must use full JSONPath syntax.
- `JSON_SET(..., path, NULL)` stores JSON `null`.
- If the JSON document argument is `NULL`, the result is SQL `NULL`.
- If `path` is `NULL` or an empty string, the function raises an error.
- Object paths are supported.
- Array element mutation such as `$.items[0]` is not supported.

## JSON_SET_JSON

Parses the third argument as JSON text and stores it as an object or array subtree.

```sql
JSON_SET_JSON(json_doc, path, json_text)
```

```sql
Mach> SELECT JSON_SET_JSON('{"ship":{}}', '$.ship.owner', '{"name":"machbase"}') FROM dual;
JSON_SET_JSON('{"ship":{}}', '$.ship.owner', '{"name":"machbase"}')
----------------------------------------------------------------------------
{"ship":{"owner":{"name":"machbase"}}}
[1] row(s) selected.
```

Notes:

- `path` must use full JSONPath syntax.
- If the third argument is SQL `NULL`, the result is SQL `NULL`.
- Invalid JSON text raises an error.
- Object paths are supported.
- Array element mutation is not supported.

## JSON_REMOVE

Removes a member or subtree from a JSON document.

```sql
JSON_REMOVE(json_doc, path)
```

```sql
Mach> SELECT JSON_REMOVE('{"owner":{"name":"machbase","team":"db"}}', '$.owner.team') FROM dual;
JSON_REMOVE('{"owner":{"name":"machbase","team":"db"}}', '$.owner.team')
--------------------------------------------------------------------------
{"owner":{"name":"machbase"}}
[1] row(s) selected.
```

Notes:

- `path` must use full JSONPath syntax.
- A missing path is treated as a no-op.
- `JSON_REMOVE(..., '$')` is not allowed.
- If the JSON document argument is `NULL`, the result is SQL `NULL`.

## PI() {#pi}

Returns a `DOUBLE` constant π.

```sql
SELECT PI();
```

```sql
Mach> SELECT PI();
PI()
------------------------------
3.141592653589793
[1] row(s) selected.
```

## SQRT() {#sqrt}

Returns the square root of one numeric argument.

```sql
SELECT SQRT(9), SQRT(2.25), SQRT(16.0);
```

```sql
Mach> SELECT SQRT(9), SQRT(2.25), SQRT(16.0);
SQRT(9)   SQRT(2.25)         SQRT(16.0)
-----------------------------------------------
3         1.5000000000000000  4
[1] row(s) selected.
```

## POWER() {#power}

Returns `base` raised to `exponent`.

```sql
SELECT POWER(2, 3), POWER(9, 0.5), POWER(4, -1);
```

```sql
Mach> SELECT POWER(2, 3), POWER(9, 0.5), POWER(4, -1);
POWER(2, 3)   POWER(9, 0.5)   POWER(4, -1)
------------------------------------------------
8             3.0000000000000000 0.2500000000000000
[1] row(s) selected.
```

## POW() {#pow}

Alias of `POWER()`.

```sql
SELECT POW(2, 3), POW(2, -1), POW(10, 0);
```

```sql
Mach> SELECT POW(2, 3), POW(2, -1), POW(10, 0);
POW(2, 3)   POW(2, -1)   POW(10, 0)
-----------------------------------------
8           0.5           1
[1] row(s) selected.
```

## LOG() {#log}

`LOG(n)` is the same as natural log; `LOG(base, n)` calculates logarithm with a base.

```sql
SELECT LOG(2, 8), LOG(100), LOG(10, 1000);
```

```sql
Mach> SELECT LOG(2, 8), LOG(100), LOG(10, 1000);
LOG(2, 8)   LOG(100)             LOG(10, 1000)
------------------------------------------------
3           4.605170185988092     3
[1] row(s) selected.
```

## LN() {#ln}

Returns natural logarithm `ln(n)`.

```sql
SELECT LN(1), LN(10), LN(1000);
```

```sql
Mach> SELECT LN(1), LN(10), LN(1000);
LN(1)      LN(10)         LN(1000)
-----------------------------------
0          2.302585092994046 6.907755278982137
[1] row(s) selected.
```

## EXP() {#exp}

Returns `e^n` of the argument.

```sql
SELECT EXP(0), EXP(1), EXP(-1);
```

```sql
Mach> SELECT EXP(0), EXP(1), EXP(-1);
EXP(0)      EXP(1)         EXP(-1)
-----------------------------------
1           2.718281828459045 0.36787944117144233
[1] row(s) selected.
```

## FLOOR() {#floor}

Rounds down toward negative infinity.

```sql
SELECT FLOOR(-1.2), FLOOR(3.9), FLOOR(-3.0);
```

```sql
Mach> SELECT FLOOR(-1.2), FLOOR(3.9), FLOOR(-3.0);
FLOOR(-1.2)  FLOOR(3.9)  FLOOR(-3.0)
-----------------------------------------
-2            3           -3
[1] row(s) selected.
```

## CEIL() {#ceil}

Rounds up toward positive infinity.

```sql
SELECT CEIL(-1.2), CEIL(3.2), CEIL(-3.0);
```

```sql
Mach> SELECT CEIL(-1.2), CEIL(3.2), CEIL(-3.0);
CEIL(-1.2)  CEIL(3.2)  CEIL(-3.0)
-------------------------------------
-1           4          -3
[1] row(s) selected.
```

## SIN() {#sin}

Returns sine value of a radian input.

```sql
SELECT SIN(0), SIN(PI()/2), SIN(PI());
```

```sql
Mach> SELECT SIN(0), SIN(PI()/2), SIN(PI());
SIN(0)      SIN(PI()/2)   SIN(PI())
------------------------------------
0           1             0
[1] row(s) selected.
```

## SLOPE {#slope}

`SLOPE(y, x)` calculates the slope of the linear regression line for numeric `(x, y)` pairs.

```sql
SLOPE(y, x)
```

- Both arguments must be numeric.
- `NULL` values are ignored.
- If there are not enough valid rows or the `x` variance is zero, the result is `NULL`.
- The result type is `DOUBLE`.

```sql
SELECT SLOPE(temp_c, sample_sec)
FROM sensor_log;
```

## COS() {#cos}

Returns cosine value of a radian input.

```sql
SELECT COS(0), COS(PI()), COS(PI()/2);
```

```sql
Mach> SELECT COS(0), COS(PI()), COS(PI()/2);
COS(0)      COS(PI())   COS(PI()/2)
-------------------------------------
1           -1          0
[1] row(s) selected.
```

## TAN() {#tan}

Returns tangent value of a radian input.

```sql
SELECT TAN(0), TAN(PI()/4), TAN(PI());
```

```sql
Mach> SELECT TAN(0), TAN(PI()/4), TAN(PI());
TAN(0)      TAN(PI()/4)  TAN(PI())
-----------------------------------
0           1            0
[1] row(s) selected.
```

## MOD() {#mod}

Returns remainder using truncation toward zero of the quotient.

```sql
SELECT MOD(10, 3), MOD(11, 4), MOD(-10, 3), MOD(3.5, 0.5);
```

```sql
Mach> SELECT MOD(10, 3), MOD(11, 4), MOD(-10, 3), MOD(3.5, 0.5);
MOD(10, 3)  MOD(11, 4)  MOD(-10, 3)  MOD(3.5, 0.5)
-------------------------------------------------------
1           3           -1           0
[1] row(s) selected.
```

## MODE {#mode}

`MODE(value)` returns the most frequent numeric value in the input set.

```sql
MODE(value)
```

- `value` must be numeric.
- `NULL` values are ignored.
- If multiple values have the same highest frequency, the smallest value is returned.
- The result type is `DOUBLE` in the current implementation.

```sql
SELECT MODE(alarm_code)
FROM event_log;
```

## P05 / P10 / P90 / P95 {#p05-p10-p90-p95}

These are shorthand forms of exact percentile calculations for frequently used percentile points.

```sql
P05(value)
P10(value)
P90(value)
P95(value)
```

- `value` must be numeric.
- `NULL` values are ignored.
- The result type is `DOUBLE`.

`P05`, `P10`, `P90`, and `P95` are equivalent to `PERCENTILE_CONT(value, 0.05)`, `0.10`, `0.90`, and `0.95`.

```sql
SELECT P05(response_ms),
       P10(response_ms),
       P90(response_ms),
       P95(response_ms)
FROM web_log;
```

## PERCENTILE_CONT / PERCENTILE_DISC {#percentile_cont-percentile_disc}

These aggregate functions calculate exact percentiles on numeric input.

```sql
PERCENTILE_CONT(value, ratio)
PERCENTILE_DISC(value, ratio)
```

- `value` must be numeric.
- `ratio` must be a constant in the range `0.0` to `1.0`.
- `PERCENTILE_CONT` interpolates between adjacent sorted values when needed.
- `PERCENTILE_DISC` selects one of the observed values at the target rank.
- Both functions currently return `DOUBLE`.

```sql
SELECT PERCENTILE_CONT(latency_ms, 0.95) AS pcont95,
       PERCENTILE_DISC(latency_ms, 0.95) AS pdisc95
FROM api_log;
```

## QUANTILE {#quantile}

`QUANTILE(value, ratio)` calculates an exact continuous quantile on numeric input.

```sql
QUANTILE(value, ratio)
```

- `value` must be numeric.
- `ratio` must be a constant in the range `0.0` to `1.0`.
- The result type is `DOUBLE`.
- In the current implementation, it belongs to the same continuous percentile family as `PERCENTILE_CONT`.

```sql
SELECT QUANTILE(cpu_usage, 0.75)
FROM host_metric;
```

## RAND() {#rand}

Generates pseudo-random values.

```sql
SELECT RAND(5) = RAND(5) AS same_seed, RAND(7) = RAND(8) AS diff_seed, RAND() = RAND() AS diff_default;
```

```sql
Mach> SELECT RAND(5) = RAND(5) AS same_seed, RAND(7) = RAND(8) AS diff_seed, RAND() = RAND() AS diff_default FROM m$sys_users WHERE name = 'SYS';
same_seed   diff_seed   diff_default
------------------------------------
1           0           0
[1] row(s) selected.
```

`RAND(seed)` is deterministic for the same `seed`. `RAND()` without a seed uses session internal state and generates values in `[0,1)`.

## REGEXP_LIKE

`REGEXP_LIKE` tests whether a string matches a regular expression pattern. It returns a
boolean value and is commonly used in a `WHERE` clause.

```sql
REGEXP_LIKE(source, pattern)
REGEXP_LIKE(source, pattern, match_param)
```

- `source` must be `VARCHAR`.
- `pattern` must be a constant `VARCHAR` regular expression.
- `match_param` is optional and must be a constant `VARCHAR`: `c` for case-sensitive
  matching or `i` for case-insensitive matching. The default is `c`.

```sql
SELECT *
FROM sensor_text
WHERE REGEXP_LIKE(message, 'error|warn', 'i');
```

## REGEXP_INSTR

`REGEXP_INSTR` returns the 1-based position of a regular expression match. If no match is
found, it returns `0`.

```sql
REGEXP_INSTR(source, pattern[, position[, occurrence[, return_pos[, match_param]]]])
```

- `source` must be `VARCHAR`.
- `pattern` must be a constant `VARCHAR` regular expression.
- `position` and `occurrence` are constant integers starting from `1`.
- `return_pos` is a constant integer: `0` returns the start position and `1` returns the
  position after the match.
- `match_param` accepts `c` or `i`. The default is `c`.

```sql
SELECT REGEXP_INSTR('TechOnTheNet', 'The', 1, 1, 1, 'i');
```

## REGEXP_SUBSTR

`REGEXP_SUBSTR` returns the substring that matches a regular expression.

```sql
REGEXP_SUBSTR(source, pattern[, position[, occurrence[, match_param]]])
```

- `source` must be `VARCHAR`.
- `pattern` must be a constant `VARCHAR` regular expression.
- `position` and `occurrence` are constant integers starting from `1`.
- `match_param` accepts `c` or `i`. The default is `c`.

```sql
SELECT REGEXP_SUBSTR('TechOnTheNet', 'a|e|i|o|u', 1, 2, 'i');
```

## REGEXP_REPLACE

`REGEXP_REPLACE` replaces text that matches a regular expression.

```sql
REGEXP_REPLACE(source, pattern[, replacement[, position[, occurrence[, match_param]]]])
```

- `source` must be `VARCHAR`.
- `pattern` and `replacement` must be constant `VARCHAR` values.
- If `replacement` is omitted, matching text is removed.
- `position` is a constant integer starting from `1`.
- `occurrence` is a constant integer. `0` replaces all matches; values greater than `0`
  replace only that occurrence.
- `match_param` accepts `c` or `i`. The default is `c`.

```sql
SELECT REGEXP_REPLACE('TechOnTheNet', 'a|e|i|o|u', 'Z', 1, 2, 'i');
```

## Support Type of Built-In Function

| |Short|Integer|Long|Float|Double|Varchar|Text|Ipv4|Ipv6|Datetime|Binary|
|--|--|--|--|--|--|--|--|--|--|--|--|
|ABS|o|o|o|o|o|x|x|x|x|x|x|
|ADD_TIME|x|x|x|x|x|x|x|x|x|o|x|
|APPROX_PERCENTILE / APPROX_MEDIAN / APPROX_P05 / APPROX_P10 / APPROX_P90 / APPROX_P95|o|o|o|o|o|x|x|x|x|x|x|
|AREA|o|o|o|o|o|x|x|x|x|x|x|
|AVG|o|o|o|o|o|x|x|x|x|x|x|
|BITAND / BITOR|o|o|o|x|x|x|x|x|x|x|x|
|COUNT|o|o|o|o|o|o|x|o|o|o|x|
|CUME_DIST|o|o|o|o|o|x|x|x|x|x|x|
|DATE_TRUNC|x|x|x|x|x|x|x|x|x|o|x|
|DECODE|o|o|o|o|o|o|x|o|x|o|x|
|FIRST / LAST|o|o|o|o|o|o|x|o|o|o|x|
|FROM_UNIXTIME|o|o|o|o|o|x|x|x|x|x|x|
|FROM_TIMESTAMP|o|o|o|o|o|x|x|x|x|x|x|
|GROUP_CONCAT|o|o|o|o|o|o|x|o|o|o|x|
|INSTR|x|x|x|x|x|o|o|x|x|x|x|
|LEAST / GREATEST|o|o|o|o|o|o|x|x|x|x|x|
|LENGTH|x|x|x|x|x|o|o|x|x|x|o|
|LOWER|x|x|x|x|x|o|x|x|x|x|x|
|LPAD / RPAD|x|x|x|x|x|o|x|x|x|x|x|
|LTRIM / RTRIM|x|x|x|x|x|o|x|x|x|x|x|
|MAX|o|o|o|o|o|o|x|o|o|o|x|
|MEDIAN|o|o|o|o|o|x|x|x|x|x|x|
|MIX|o|o|o|o|o|o|x|o|o|o|x|
|MODE|o|o|o|o|o|x|x|x|x|x|x|
|NVL|x|x|x|x|x|o|x|o|x|x|x|
|P05 / P10 / P90 / P95|o|o|o|o|o|x|x|x|x|x|x|
|PERCENTILE_CONT / PERCENTILE_DISC|o|o|o|o|o|x|x|x|x|x|x|
|QUANTILE|o|o|o|o|o|x|x|x|x|x|x|
|REGEXP_LIKE|x|x|x|x|x|o|x|x|x|x|x|
|REGEXP_INSTR|x|x|x|x|x|o|x|x|x|x|x|
|REGEXP_SUBSTR|x|x|x|x|x|o|x|x|x|x|x|
|REGEXP_REPLACE|x|x|x|x|x|o|x|x|x|x|x|
|SLOPE|o|o|o|o|o|x|x|x|x|x|x|
|TOP_K|o|o|o|o|o|x|x|x|x|x|x|
|ROUND|o|o|o|o|o|x|x|x|x|x|x|
|ROWNUM|o|o|o|o|o|o|o|o|o|o|o|
|SERIESNUM|o|o|o|o|o|o|o|o|o|o|o|
|STDDEV / STDDEV_POP|o|o|o|o|o|x|x|x|x|x|x|
|SUBSTR|x|x|x|x|x|o|x|x|x|x|x|
|SUBSTRING_INDEX|x|x|x|x|x|o|o|x|x|x|x|
|SUM|o|o|o|o|o|x|x|x|x|x|x|
|SYSDATE / NOW|x|x|x|x|x|x|x|x|x|x|x|
|TO_CHAR|o|o|o|o|o|o|x|o|o|o|x|
|TO_DATE / TO_DATE_SAFE|x|x|x|x|x|o|x|x|x|x|x|
|TO_HEX|o|o|o|o|o|o|o|o|o|o|o|
|TO_INET_STR|x|x|x|x|x|x|x|o|x|x|x|
|TO_IPV4 / TO_IPV4_SAFE|x|x|x|x|x|o|x|x|x|x|x|
|TO_IPV6 / TO_IPV6_SAFE|x|x|x|x|x|o|x|x|x|x|x|
|TO_NUMBER / TO_NUMBER_SAFE|x|x|x|x|x|o|x|x|x|x|x|
|TO_TIMESTAMP|x|x|x|x|x|x|x|x|x|o|x|
|TRUNC|o|o|o|o|o|x|x|x|x|x|x|
|TS_CHANGE_COUNT|o|o|o|o|o|x|x|o|o|o|x|
|UNIX_TIMESTAMP|o|o|o|o|o|x|x|x|x|x|x|
|UPPER|x|x|x|x|x|o|x|x|x|x|x|
|VARIANCE / VAR_POP|o|o|o|o|o|x|x|x|x|x|x|
|YEAR / MONTH / DAY|x|x|x|x|x|x|x|x|x|o|x|
|ISNAN / ISINF|o|o|o|o|o|x|x|x|x|x|x|


## JSON-related function

These functions use json data type as an argument.

|Function name|Explanation|Note|
|--|--|--|
|JSON_EXTRACT(JSON column name, 'json path')|Return the value as string type.<br>(If the value does not exist, return ERROR.)| - JSON object or array : Convert every objects into string type and return it.<br> - String type : Return as is<br> - Numeric type : Convert into string type and return it<br> - boolean type : Return "True" or "False"|
|JSON_EXTRACT_DOUBLE(JSON column name, 'json path')	|Return the value as 64 bits double type.<br>(If the value does not exist, return NULL.)| - JSON object or array : Return NULL<br> - String type : Convert and return if possible. Else return NULL.<br> - Numeric type : Return 64bit real number.<br> - boolean type : Return "True" as 1.0 or "False" as 0.0|
|JSON_EXTRACT_INTEGER(JSON column name, 'json path')|Return the value as 64 bits integer type.<br>(If the value does not exist, return NULL.)| - JSON object or array : Return NULL<br> - String type : Convert and return if possible. Else return NULL.<br> - Numeric type : Return 64bit integer.<br> - boolean type : Return "True" as 1 or "False" as 0|
|JSON_EXTRACT_STRING(JSON column name, 'json path')|Return the value as string type.<br>(If the value does not exist, return NULL.)<br>Returns same results as operator(→)| - JSON object or array : Convert every objects into string type and return it.<br> - String type : Return as is <br> - Numeric type : Convert into string type and return it <br> - boolean type : Return "True" or "False"|
|JSON_SET(json_doc, path, scalar)|Returns a new JSON document with the SQL scalar value stored at the given path as a JSON scalar.| - `path` must use full JSONPath syntax.<br> - `NULL` is stored as JSON `null`.<br> - Only object paths are supported.|
|JSON_SET_JSON(json_doc, path, json_text)|Returns a new JSON document with the JSON text stored at the given path as an object or array subtree.| - `path` must use full JSONPath syntax.<br> - If the third argument is SQL `NULL`, the result is SQL `NULL`.<br> - Invalid JSON text raises an error.|
|JSON_REMOVE(json_doc, path)|Returns a new JSON document with the member or subtree at the given path removed.| - `path` must use full JSONPath syntax.<br> - Missing paths are treated as no-op.<br> - `JSON_REMOVE(..., '$')` is not allowed.|
|JSON_IS_VALID('json string')|Check if the json string is valid for the json format| - 0 : False<br> - 1 : True|
|JSON_TYPEOF(JSON column name, 'json path')|Returns the type of the value.| - None : Key does not exists.<br> - Object : Object type<br> - Integer : Integer Type<br> - Real : Real number type<br> - String : String type<br> - True/False : Boolean<br> - Array : Array Type<br> - Null : NULL|

```sql
Mach> CREATE TABLE jsontbl (name VARCHAR(20), jval JSON);
Created successfully.

Mach> INSERT INTO jsontbl VALUES("name1", '{"name":"test1"}');
1 row(s) inserted.
Mach> INSERT INTO jsontbl VALUES("name2", '{"name":"test2", "value":123}');
1 row(s) inserted.
Mach> INSERT INTO jsontbl VALUES("name3", '{"name":{"class1": "test3"}}');
1 row(s) inserted.
Mach> INSERT INTO jsontbl VALUES("name4", '{"myarray": [1, 2, 3, 4]}');
1 row(s) inserted.
Mach> INSERT INTO jsontbl VALUES("name5", '{"name":"error"');
[ERR-02233: Error occurred at column (2): (Error in json load.)]

Mach> SELECT name, JSON_EXTRACT_STRING(jval, '$.name') FROM jsontbl;
name                  JSON_EXTRACT_STRING(jval, '$.name')
-----------------------------------------------------------------------------------------------------------
name4                 NULL
name3                 {"class1": "test3"}
name2                 test2
name1                 test1
[4] row(s) selected.

Mach> SELECT name, JSON_EXTRACT_INTEGER(jval, '$.myarray[1]') FROM jsontbl;
name                  JSON_EXTRACT_INTEGER(jval, '$.myarray[1]')
--------------------------------------------------------------------
name4                 2
name3                 NULL
name2                 NULL
name1                 NULL
[4] row(s) selected.

Mach> SELECT name, JSON_TYPEOF(jval, '$.name') FROM jsontbl;
name                  JSON_TYPEOF(jval, '$.name')
-----------------------------------------------------------------------------------------------------------
name4                 None
name3                 Object
name2                 String
name1                 String
[4] row(s) selected.
```


## JSON Operator

The `->` operator is used for accessing an object of JSON data.

Returns the same results as JSON_EXTRACT_STRING function.

```sql
json_col -> 'json path'
```

JSON member values can be accessed with the JSONPath-based `->` operator or with JSON dot shorthand.

```sql
-- JSONPath arrow syntax
jval->'$.sensor.temperature'

-- JSON dot shorthand
jval.sensor.temperature
```

Both expressions access the same JSON value. The existing `->` operator remains supported, and dot shorthand is an additional syntax for writing the same access path more concisely.

```sql
Mach> SELECT name, jval->'$.name' FROM jsontbl;
name                  JSON_EXTRACT_STRING(jval, '$.name')
-----------------------------------------------------------------------------------------------------------
name4                 NULL
name3                 {"class1": "test3"}
name2                 test2
name1                 test1
[4] row(s) selected.

Mach> SELECT name, jval->'$.myarray[1]' FROM jsontbl;
name                  JSON_EXTRACT_INTEGER(jval, '$.myarray[1]')
--------------------------------------------------------------------
name4                 2
name3                 NULL
name2                 NULL
name1                 NULL
[4] row(s) selected.

Mach> SELECT name, jval->'$.name.class1' FROM jsontbl;
name                  jval->'$.name.class1'
-----------------------------------------------------------------------------------------------------------
name4                 NULL
name3                 test3
name2                 NULL
name1                 NULL
[4] row(s) selected
```

### JSONPath arrow syntax

The arrow syntax uses a JSONPath string.

```sql
jval->'$.name'
jval->'$.sensor.temperature'
jval->'$.items[0].name'
```

You can also use bracket syntax to specify a JSON key directly. Use bracket syntax when a key name contains a dot (`.`).

```sql
-- Key name is a.b
jval->'$["a.b"]'
jval->'$[a.b]'

-- Multiple key levels with brackets
jval->'$[Plant1][Line1][Temperature]'

-- One key name containing dots
jval->'$[Plant1.Line1.Temperature]'
```

`$[Plant1.Line1.Temperature]` looks for a single key named `Plant1.Line1.Temperature`. To access `Plant1`, `Line1`, and `Temperature` as separate nested keys, use `$[Plant1][Line1][Temperature]` or `$.Plant1.Line1.Temperature`.

When a key name contains special characters or dots, quoted bracket syntax is recommended.

```sql
jval->'$["a.b"]["c.d"]["e.f"]'
```

The following syntax is not supported.

```sql
jval->'$."a.b"'
```

### JSON dot shorthand

You can access a JSON value by appending member names after a JSON column.

```sql
-- Single member
jval.name

-- Nested member
jval.sensor.temperature

-- Array index
jval.items[0].name

-- Key containing special characters
jval.items[0]."product-id"
```

A key enclosed in double quotes keeps its case and special characters.

```sql
SELECT name, jval."Camel-Key", jval.items[0]."product-id"
  FROM jsontbl
 ORDER BY name;
```

### Type comparison in WHERE

JSON member access results are displayed like strings in query output. However, when they are compared with numeric SQL values in a `WHERE` clause, the JSON value is parsed and compared numerically.

```sql
SELECT name
  FROM jsontbl
 WHERE jval->'$.value' > 100
 ORDER BY name;

SELECT name
  FROM jsontbl
 WHERE jval.value BETWEEN 10 AND 30
 ORDER BY name;

SELECT name
  FROM jsontbl
 WHERE jval.value IN (10, 20, 30)
 ORDER BY name;
```

Supported comparisons are:

- JSON integer values compared with SQL integer values
- JSON real/double values compared with SQL numeric values
- JSON numeric strings compared with SQL numeric values
- JSON boolean values compared with string literals `'true'` and `'false'`
- `=`, `<>`, `<`, `<=`, `>`, `>=`, `BETWEEN`, and literal `IN (...)`

When compared with a SQL integer value, a JSON integer is compared as an integer. Values beyond double precision, such as `9007199254740992` and `9007199254740993`, can therefore be compared as distinct values.

When compared with a character value, the existing string comparison behavior is used.

```sql
SELECT name
  FROM jsontbl
 WHERE jval->'$.name' = 'test1'
 ORDER BY name;
```

If a JSON value cannot be parsed as a number during a numeric comparison, the predicate does not match and no error is raised. The comparison policy for ordinary `VARCHAR` columns is unchanged; automatic numeric comparison applies only to JSON member access expressions.

### Name resolution

Normal SQL column-name resolution takes precedence over JSON dot resolution.

```sql
SELECT t.jval.name
  FROM jsontbl t;
```

Machbase first tries to resolve the expression as ordinary column names. If it cannot be resolved as a normal column reference and `jval` is a JSON column, `jval.name` is treated as JSON member access.

JSON dot access can be used only from a JSON column.

```sql
-- Not supported
(jval->'$.sensor').temperature
name.member
```

### Limitations

The following syntax is not supported.

- Wildcard: `jval.items[*].name`
- Recursive descent: `jval..name`
- Filter expression: `jval.items[?(@.price > 10)]`
- Negative array index: `jval.items[-1]`
- Single quoted key: `jval.'product-id'`
- Mixed dot and arrow syntax: `jval.items->'$.name'`
- Dot access on a non-JSON column: `name.member`
- Dot access after an arbitrary expression: `(jval->'$.sensor').temperature`
- Quoted member arrow path: `jval->'$."a.b"'`

Numeric automatic comparison for JSON member values is not supported for subquery `IN` predicates in the form `IN (SELECT ...)`. Use literal `IN (...)` instead.

## WINDOW FUNCTION

The WINDOW function is a function for comparison, operation, and definition between rows. It is also called an analysis function or ranking function.

It can only be used in the SELECT statement.

### WINDOW FUNCTION SYNTAX

Window functions necessarily include the OVER clause.

```
WINDOW_FUNCTION (ARGUMENTS) OVER ([PARTITION BY column_name] [ORDER BY column_name])
```

* WINDOW_FUNCTION: Window function name
* ARGUMENTS: Depending on the function, 0 to N arguments can be specified.
* PARTITION BY clause: The entire set can be divided into small groups based on criteria. (can be omitted)
* ORDER BY clause: Describes the order by clause on which items to sort. (Can be omitted)

### WINDOW FUNCTION LIST

#### LAG

Retrieve the value of the previous Nth row in a partition-specific window.

If there are no rows to retrieve, NULL is returned.

```
LAG(column_name, N) OVER ([PARTITION BY column_name] [ORDER BY column_name])
```

```
Mach> CREATE TABLE lag_table (name varchar(10), dt datetime, value INTEGER);
Created successfully.

Mach> INSERT INTO lag_table VALUES('name1', TO_DATE('2024-01-01'), 1);
1 row(s) inserted.

Mach> INSERT INTO lag_table VALUES('name1', TO_DATE('2024-01-02'), 2);
1 row(s) inserted.

Mach> INSERT INTO lag_table VALUES('name1', TO_DATE('2024-01-03'), 3);
1 row(s) inserted.

-- Divide the set by name, sort by dt, and retrieve the first previous value.
Mach> SELECT name, dt, value, LAG(value, 1) OVER(PARTITION BY name ORDER BY dt) FROM lag_table;
name        dt                              value       LAG(value, 1)
---------------------------------------------------------------------------
name1       2024-01-01 00:00:00 000:000:000 1           NULL
name1       2024-01-02 00:00:00 000:000:000 2           1
name1       2024-01-03 00:00:00 000:000:000 3           2
[3] row(s) selected.
```


#### LEAD

Retrieve the value of the Nth row from the partition-specific window.

If there are no rows to retrieve, NULL is returned.

```
LEAD(column_name, N) OVER ([PARTITION BY column_name] [ORDER BY column_name])
```

```
Mach> CREATE TABLE lead_table (name varchar(10), dt datetime, value INTEGER);
Created successfully.

Mach> INSERT INTO lead_table VALUES('name1', TO_DATE('2024-01-01'), 1);
1 row(s) inserted.

Mach> INSERT INTO lead_table VALUES('name1', TO_DATE('2024-01-02'), 2);
1 row(s) inserted.

Mach> INSERT INTO lead_table VALUES('name1', TO_DATE('2024-01-03'), 3);
1 row(s) inserted.

-- Divide the set by name, sort by dt, and retrieve the first and subsequent values.
Mach> SELECT name, dt, value, LEAD(value, 1) OVER(PARTITION BY name ORDER BY dt) FROM lead_table;
name        dt                              value       LEAD(value, 1)
----------------------------------------------------------------------------
name1       2024-01-01 00:00:00 000:000:000 1           2
name1       2024-01-02 00:00:00 000:000:000 2           3
name1       2024-01-03 00:00:00 000:000:000 3           NULL
[3] row(s) selected.
```


#### NTILE

`NTILE(n)` divides ordered rows into `n` buckets as evenly as possible and returns the bucket number of each row.

```
NTILE(n) OVER ([PARTITION BY column_name] ORDER BY column_name)
```

- `n` must be a positive constant.
- `ORDER BY` inside `OVER (...)` is required.
- If rows cannot be divided evenly, earlier buckets receive one more row.

```
Mach> SELECT user_id,
             score,
             NTILE(4) OVER (ORDER BY score) AS score_band
      FROM exam_result;
```
