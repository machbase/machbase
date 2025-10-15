---
title : An example of tag table
type: docs
weight: 50
---

## Introduction

Introduction
The TAG table can load the structure type of the file in which general sensor data is stored.

The most common types of text storage files are <value, value, value> <value, value, value> <repeat> which is a random file content that just lists a number of numeric values .

In the case of a file containing time, there are <time, value, value, value> <time, value, value, value> <repeat ..>.

The data in these files is created when a device called PLC (programmable logic controller) collects data from one or more sensors continuously over a long period of time.

The following is the picture of PLC example file.

![ex1](../ex1.png)

Now we will load this file into Machbase's TAG table.


## Data conversion flowchart

![ex2](../ex2.png)

As you can see in the figure above, we will load the raw CSV file into Machbase's log table and convert it into a tag table.


## Tag table creation and tag meta loading

Create TAG table as shown below and load the tag names (tag meta) stored in the CSV file at once using a tool called tagmetaimport.

Not only options that are described below, but also every options available in machloader are able to use.

```bash
Mach> create tag table tag (name varchar(32) primary key, time datetime basetime, value double
summarized);
Executed successfully.
Elapsed time: 3.032
 
$ cat tag_meta.csv
MTAG_V00
MTAG_V01
MTAG_C00
MTAG_C01
MTAG_C02
MTAG_C03
MTAG_C04
MTAG_C05
MTAG_C06
MTAG_C07
MTAG_C08
MTAG_C09
MTAG_C10
MTAG_C11
MTAG_C12
MTAG_C13
MTAG_C14
MTAG_C15
 
$ tagmetaimport -d tag_meta.csv
Import time : 0 hour 0 min 0.340 sec
Load success count : 18
```

(If you changed Machbase Port number from basic port number, you should use changed port number by using -P option on tagmeraimport.)
As shown above, 18 tag meta information were loaded successfully.


## Create table for PLC data loading

Execute the following query to create the log table.

```sql
create table plc_tag_table(
    tm datetime,
    V0 DOUBLE ,
    V1 DOUBLE ,
    C0 DOUBLE ,
    C1 DOUBLE ,
    C2 DOUBLE ,
    C3 DOUBLE ,
    C4 DOUBLE ,
    C5 DOUBLE,
    C6 DOUBLE ,
    C7 DOUBLE ,
    C8 DOUBLE ,
    C9 DOUBLE ,
    C10 DOUBLE ,
    C11 DOUBLE ,
    C12 DOUBLE ,
    C13 DOUBLE ,
    C14 DOUBLE ,
    C15 DOUBLE
);
```

{{< callout type="warning" >}}
Note that this table is a log type of table (do not get confused by file names). In Machbase, if you do not specify a separate table type, the default type of table is log.
{{< /callout >}}

## Loading PLC data

Input the plc_tag.csv file, which contains 2 million original PLC data, using the machloader as PLC input in the log table plc_tag_table created above.

In the plc_tag.csv file, the first column is time, then V0, V1, ... Columns are divided up to C15.

As for the data pattern in 1 second, about 100 pieces of data are input from 0 to 99 milliseconds, there is no input from 100 milliseconds to 999 milliseconds, and the same pattern is input for the next 1 second.

```bash
$ machloader -t plc_tag_table -i -d plc_tag.csv -F "tm YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn"
-----------------------------------------------------------------
Machbase Data Import/Export Utility.
Release Version 5.5.0.official
Copyright 2014, MACHBASE Corporation or its subsidiaries.
All Rights Reserved.
-----------------------------------------------------------------
NLS : US7ASCII EXECUTE MODE : IMPORT
TARGET TABLE : plc_tag_table DATA FILE : 4_plc_tag.csv
IMPORT MODE : APPEND FIELD TERM : ,
ROW TERM : \n ENCLOSURE : "
ESCAPE : \ ARRIVAL_TIME : FALSE
ENCODING : NONE HEADER : FALSE
CREATE TABLE : FALSE
Progress bar Imported records Error records
============================== 2000000 0
Import time : 0 hour 0 min 26.544 sec
Load success count : 2000000
Load fail count : 0
```

## Tag meta name generation rules

Now you insert data into the tag table in order to  see the data through the Tag Analyzer.

For this, the insert-select statement will insert every data in plc_tag_table in tag table.

The name of each tag should be matched so it is determined as follows.

|Column name of log table|Tag name values of tag table|
|--|--|
|V0|MTAG_V00|
|V1|MTAG_V01|
|C0|MTAG_C00|
|C1|MTAG_C01|
|...| |
|C15|MTAG_C15|


## Loading Tag table data

It's time to load the actual data into the tag table.

Query at the below insert data in to tag table sequentially.

```bash
Mach> insert into tag select 'MTAG_V00', tm, v0 from plc_tag_table;
2000000 row(s) inserted.
Elapsed time: 4.898
Mach> insert into tag select 'MTAG_V01', tm, v1 from plc_tag_table;
2000000 row(s) inserted.
Elapsed time: 5.577
Mach> insert into tag select 'MTAG_C00', tm, c0 from plc_tag_table;
2000000 row(s) inserted.
Elapsed time: 6.327
Mach> insert into tag select 'MTAG_C01', tm, c1 from plc_tag_table;
2000000 row(s) inserted.
Elapsed time: 7.445
Mach> insert into tag select 'MTAG_C02', tm, c2 from plc_tag_table;
2000000 row(s) inserted.
Elapsed time: 6.898
Mach> insert into tag select 'MTAG_C03', tm, c3 from plc_tag_table;
2000000 row(s) inserted.
Elapsed time: 7.078
Mach> insert into tag select 'MTAG_C04', tm, c4 from plc_tag_table;
2000000 row(s) inserted.
Elapsed time: 6.799
Mach> insert into tag select 'MTAG_C05', tm, c5 from plc_tag_table;
2000000 row(s) inserted.
Elapsed time: 7.210
Mach> insert into tag select 'MTAG_C06', tm, c6 from plc_tag_table;
2000000 row(s) inserted.
Elapsed time: 9.232
Mach> insert into tag select 'MTAG_C07', tm, c7 from plc_tag_table;
2000000 row(s) inserted.
Elapsed time: 6.398
Mach> insert into tag select 'MTAG_C08', tm, c8 from plc_tag_table;
2000000 row(s) inserted.
Elapsed time: 6.432
Mach> insert into tag select 'MTAG_C09', tm, c9 from plc_tag_table;
2000000 row(s) inserted.
Elapsed time: 6.734
Mach> insert into tag select 'MTAG_C10', tm, c10 from plc_tag_table;
2000000 row(s) inserted.
Elapsed time: 7.692
Mach> insert into tag select 'MTAG_C11', tm, c11 from plc_tag_table;
2000000 row(s) inserted.
Elapsed time: 8.628
Mach> insert into tag select 'MTAG_C12', tm, c12 from plc_tag_table;
2000000 row(s) inserted.
Elapsed time: 8.229
Mach> insert into tag select 'MTAG_C13', tm, c13 from plc_tag_table;
2000000 row(s) inserted.
Elapsed time: 9.517
Mach> insert into tag select 'MTAG_C14', tm, c14 from plc_tag_table;
2000000 row(s) inserted.
Elapsed time: 7.231
Mach> insert into tag select 'MTAG_C15', tm, c15 from plc_tag_table;
2000000 row(s) inserted.
Elapsed time: 7.830
```

A total of 36 millions of records are created.