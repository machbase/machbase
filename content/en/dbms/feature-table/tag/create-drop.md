---
title : 'Creating and Dropping Tag table'
type: docs
weight: 10
---

The user must write 'TAG' as the table type. By manipulating this table, sensor data can be utilized in various ways.

Unlike the previous version, tag table name does not need to be "TAG", and can be freely specified.

Note that there is no TAG table when the database is first installed.

Since the TAG table is, in basic, intended to store sensor data, the following three essential items must be included.
* Tag name
* Input time
* Sensor value

However, the Machbase TAG table is accompanied by keywords for the above required columns, as it allows input of the above three and additional columns.

Starting from version 7.5, the SUMMARIZED keyword in the tag value is optional.
* Tag name : PRIMARY KEY
* Input time : BASETIME

This tag name is used as tag meta information described in the next section.


## Creation of Tag table

The simplest tag table is generated as follows.

```sql
Mach> CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME, value DOUBLE);
[ERR-02253: Mandatory column definition (PRIMARY KEY / BASETIME) is missing.]
==> If you omit some keywords on creating tag table, error occurs.
 
Mach> CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED);
Executed successfully.
==> To use statistical information, the SUMMARIZED keyword must be added to the tag value.
 
Mach> desc tag;
[ COLUMN ]              
----------------------------------------------------------------
NAME      TYPE        LENGTH
----------------------------------------------------------------
NAME      varchar         20
TIME      datetime       31
VALUE    double          17
 
Mach> CREATE TAG TABLE other_tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE);
Executed successfully.
 
Mach> desc OTHER_TAG;
[ COLUMN ]              
----------------------------------------------------------------
NAME      TYPE        LENGTH
----------------------------------------------------------------
NAME      varchar         20
TIME      datetime       31
VALUE    double          17
```

==> If you omit some keywords on creating tag table, error occurs. To improve performance, an internal table is created which divided into four partitions.

## Additional Sensor Column

In reality, it is sometimes difficult to solve a given problem with just three columns when using the TAG table..

In particular, since the information of the sensor data to be input may be a specific group or an Internet address as well as a name, a time, and a value, the following can be added.

```sql
Mach> create tag table TAG (name varchar(20) primary key, time datetime basetime, value double, grpid short, myip ipv4) ;
Executed successfully.
 
Mach> desc tag;
[ COLUMN ]              
----------------------------------------------------------------
NAME             TYPE        LENGTH
----------------------------------------------------------------
NAME             varchar         20
TIME             datetime        31
VALUE            double          17
GRPID            short            6       <=== added column
MYIP             ipv4            15       <=== added column
```

Note, however, that in older versions, including 5.5, values of type VARCHAR can not fit into the supplementary column.

```sql
Mach> create tag table TAG (name varchar(20) primary key, time datetime basetime, value double summarized, myname varchar(100)) ;
[ERR-01851: Variable length columns are not allowed in tag table.]
```

In the case of string type, the above error occurs. In versions 5.6 and later, VARCHAR is also supported for additional columns in the TAG table.

## Additional metadata columns

It is not only possible to add sensor columns to the TAG table, but also to input information dependent on each tag name.

Since this information does not need to be redundantly stored in the sensor data, it is necessary to add a separate column definition syntax METADATA (...) for efficient management.

```sql
Mach> create tag table TAG (name varchar(20) primary key, time datetime basetime, value double)
   2  metadata (room_no integer, tag_description varchar(100));
```

Here, room_no and tag_description are information dependent on name. For example, you can input this information.

|name|room_no|tag_description|
|--|--|--|
|temp_001|1|It reads current temperature as Celsius|
|humid_001|1|It reads current humidity as percentage|

After input, you can query with TAG table through SELECT.

```sql
Mach> SELECT name, time, value, tag_description FROM tag LIMIT 1;
name                  time                            value
--------------------------------------------------------------------------------------
tag_description
------------------------------------------------------------------------------------
temp_001              2019-03-01 09:52:17 000:000:000 25.3
```

It reads current temperature as Celsius

## Setting Table Property

When creating tag table, user can set 3 types of property.

|NAME|EXPLANATION|VALUE|
|--|--|--|
|TAG_PARTITION_COUNT|User can specify the number of partition to control memory and CPU usage.| - Default: 4<br> - Min: 1<br> - Max: 1024|
|TAG_DATA_PART_SIZE	|User can specify data size to control memory and CPU usage for each partition.<br>User can specify in BYTE, can ALIGN in to MB.| - Default: 16MB (16 * 1024 * 1024)<br> - Min: 1MB (1024 * 1024)<br> - Max: 1GB (1024 * 1024 * 1024)|
|TAG_STAT_ENABLE|User can specify it to activate the function that save statistical information for each TAG ID.| - Default : 1<br> - Min: 0  (disable)<br> - Max: 1 (enable)|

```sql
Mach> CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE) TAG_PARTITION_COUNT=1;
Executed successfully.
 
Mach> CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE) TAG_DATA_PART_SIZE=1048576;
Executed successfully.
 
Mach> CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE) TAG_STAT_ENABLE=0;
Executed successfully.
 
Mach> CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED) TAG_PARTITION_COUNT=2, TAG_STAT_ENABLE=1;
Executed successfully.
```

## Dropping tag table

If you need to recreate the generated tag table, or if you need to free up disk space, you can use the following DROP command to drop it.

Note that all data related to the TAG table, ie tag data, metadata tables are also dropped.

```sql
Mach> DROP TABLE tag;
Dropped successfully.
 
Mach> DESC tag;
tag does not exist.
```
