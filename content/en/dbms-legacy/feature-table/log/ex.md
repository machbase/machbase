---
title : Example of Log Table
type: docs
weight: 60
---

Installing the Machbase package provides a tutorial that creates a log table, populates the generated table with the log data, and displays the log data.

You can find it in the path below.

```bash
[machbase@localhost tutorials]$ cd $MACHBASE_HOME/tutorials
[machbase@localhost tutorials]$ ls -l
total 0
drwxrwxr-x 2 machbase machbase 103 Oct 30 16:10 backup_mount
drwxrwxr-x 2 machbase machbase  44 Oct 30 16:10 connect_r
drwxrwxr-x 2 machbase machbase 177 Oct 30 16:10 csvload
drwxrwxr-x 2 machbase machbase  49 Oct 30 16:10 export_data
drwxrwxr-x 2 machbase machbase  32 Oct 30 16:10 install_docker_image
drwxrwxr-x 2 machbase machbase  49 Oct 30 16:10 ip_address
drwxrwxr-x 2 machbase machbase  75 Oct 30 16:10 searchtext
drwxrwxr-x 2 machbase machbase  93 Oct 30 16:10 time_series
[machbase@localhost tutorials]$
```

##  Create Log Table

The log data to be input is a file in the following csv format.

```bash
[machbase@localhost csvload]$ cd $MACHBASE_HOME/tutorials/csvload
[machbase@localhost csvload]$ more sample_data.csv
2015-05-20 06:00:00,63.214.191.124,2296,122.195.164.32,5416,12,GET /twiki/bin/view/Main/TWikiGroups?rev=1.2 HTTP/1.1,200,5162
2015-05-20 06:00:07,212.237.153.79,6203,71.129.68.118,8859,67,GET /twiki/bin/view/Main/WebChanges HTTP/1.1,200,40520
2015-05-20 06:00:07,243.9.49.80,344,122.195.164.32,6203,46,GET /twiki/bin/view/Main/TWikiGroups?rev=1.2 HTTP/1.1,200,5162
2015-05-20 06:00:07,232.191.241.129,5377,174.47.129.59,1247,17,GET /mailman/listinfo/hsdivision HTTP/1.1,200,6291
2015-05-20 06:00:07,121.67.24.216,2296,212.237.153.79,6889,68,GET /twiki/bin/view/TWiki/WebTopicEditTemplate HTTP/1.1,200,3732
2015-05-20 06:00:07,31.224.72.52,450,100.46.183.122,10541,20,GET /twiki/bin/view/Main/WebChanges HTTP/1.1,200,40520
2015-05-20 06:00:07,210.174.159.227,6180,173.149.119.202,6927,2,GET /twiki/bin/rdiff/TWiki/AlWilliams?rev1=1.2&rev2=1.1 HTTP/1.1,200,5234
2015-05-20 06:00:07,210.174.159.227,10124,16.194.51.72,10512,69,GET /twiki/bin/rdiff/TWiki/AlWilliams?rev1=1.2&rev2=1.1 HTTP/1.1,200,5234
2015-05-20 06:00:07,60.48.99.15,12333,85.183.139.166,12020,64,GET /robots.txt HTTP/1.1,200,68
```

Check each field value of log data and create a table. You can create it in machsql using 'CREATE TABLE' syntax.

```sql
CREATE TABLE SAMPLE_TABLE
(
    srcip        IPV4,
    srcport      INTEGER,
    dstip        IPV4,
    dstport      INTEGER,
    protocol     SHORT,
    eventlog     VARCHAR(1204),
    eventcode    SHORT,
    eventsize    LONG
);
```

Alternatively, you can create a table creation script file and run machsql on the OS command line.

```bash
[machbase@localhost csvload]$ machsql -s localhost -u sys -p manager -f create_sample_table.sql
=================================================================
     Machbase Client Query Utility
     Release Version x.x.x.official
     Copyright 2014 MACHBASE Corporation or its subsidiaries.
     All Rights Reserved.
=================================================================
MACHBASE_CONNECT_MODE=INET, PORT=5656
Type 'help' to display a list of available commands.
Mach> CREATE TABLE SAMPLE_TABLE
(
    srcip        IPV4,
    srcport      INTEGER,
    dstip        IPV4,
    dstport      INTEGER,
    protocol     SHORT,
    eventlog     VARCHAR(1204),
    eventcode    SHORT,
    eventsize    LONG
);
Created successfully. 
```


##  Log Data Insert

Since the log data is a csv format file, you can load it using csvimport.

The first field in the log file is the date, which specifies the option to enter this value into the _arrival_time column.

```bash
[machbase@localhost csvload]$ csvimport -t sample_table -d sample_data.csv -a -F "_arrival_time YYYY-MM-DD HH24:MI:SS"
-----------------------------------------------------------------
     Machbase Data Import/Export Utility.
     Release Version x.x.x.official
     Copyright 2014, MACHBASE Corporation or its subsidiaries.
     All Rights Reserved.
-----------------------------------------------------------------
NLS            : US7ASCII            EXECUTE MODE   : IMPORT
TARGET TABLE   : sample_table        DATA FILE      : sample_data.csv
IMPORT_MODE    : APPEND              FILED TERM     : ,
ROW TERM       :
                   ENCLOSURE      : "
ESCAPE         : "                   ARRIVAL_TIME   : TRUE
ENCODING       : NONE                HEADER         : FALSE
CREATE TABLE   : FALSE
 
 Progress bar                       Imported records        Error records
                                             1000000                    0
 
Import time         :  0 hour  0 min  5.728 sec
Load success count  : 1000000
Load fail count     : 0
 
[machbase@localhost csvload]$
```

##  Log Data Retrieval

Check the data in machsql.

```bash
[machbase@localhost csvload]$ machsql
=================================================================
     Machbase Client Query Utility
     Release Version x.x.x.official
     Copyright 2014 MACHBASE Corporation or its subsidiaries.
     All Rights Reserved.
=================================================================
Machbase server address (Default:127.0.0.1) :
Machbase user ID  (Default:SYS)
Machbase User Password :
MACHBASE_CONNECT_MODE=INET, PORT=5656
Type 'help' to display a list of available commands.
Mach> show tables;
NAME                                                                              TYPE
-----------------------------------------------------------------------------------------------
SAMPLE_TABLE                                                                      LOG
[1] row(s) selected.
 
Mach> desc sample_table;
[ COLUMN ]
----------------------------------------------------------------
NAME                          TYPE                LENGTH
----------------------------------------------------------------
SRCIP                         ipv4                15
SRCPORT                       integer             11
DSTIP                         ipv4                15
DSTPORT                       integer             11
PROTOCOL                      short               6
EVENTLOG                      varchar             1204
EVENTCODE                     short               6
EVENTSIZE                     long                20
 
Mach> SELECT COUNT(*) FROM SAMPLE_TABLE;
COUNT(*)
-----------------------
1000000
[1] row(s) selected.
 
Mach> SELECT SRCIP, COUNT(*) FROM SAMPLE_TABLE GROUP BY SRCIP ORDER BY 2 DESC LIMIT 10;
SRCIP           COUNT(*)
----------------------------------------
96.128.212.177  13594
173.149.119.202 13546
219.229.142.218 13537
69.99.246.62    13511
239.81.105.222  13501
86.45.186.17    13487
231.146.69.51   13483
248.168.229.34  13472
105.9.103.49    13472
115.18.128.171  13468
[10] row(s) selected.
Mach>
```


##  Create and View Index

Create a keyword index for the eventlog column of varchar type in the generated sample_table column and search for text.

```sql
-- Create eventlog_index index.
Mach> CREATE INDEX eventlog_index ON SAMPLE_TABLE( eventlog) INDEX_TYPE KEYWORD;
Created successfully.
Elapsed time: 0.442
 
-- Check created index.
Mach> desc sample_table;
[ COLUMN ]
----------------------------------------------------------------
NAME                          TYPE                LENGTH
----------------------------------------------------------------
SRCIP                         ipv4                15
SRCPORT                       integer             11
DSTIP                         ipv4                15
DSTPORT                       integer             11
PROTOCOL                      short               6
EVENTLOG                      varchar             1204
EVENTCODE                     short               6
EVENTSIZE                     long                20
 
[ INDEX ]
----------------------------------------------------------------
NAME                          TYPE                COLUMN
----------------------------------------------------------------
EVENTLOG_INDEX                KEYWORD_LSM         EVENTLOG
 
 
-- Retrieve data containing 'view' using SEARCH syntax.
Mach> SELECT EVENTLOG FROM SAMPLE_TABLE WHERE EVENTLOG SEARCH 'view' LIMIT 10;
EVENTLOG
------------------------------------------------------------------------------------
GET /twiki/bin/view/TWiki/ManagingWebs?skin=print HTTP/1.1
GET /twiki/bin/view/Main/TokyoOffice HTTP/1.1
GET /twiki/bin/view/TWiki/ManagingWebs?rev=1.22 HTTP/1.1
GET /twiki/bin/view/Main/DCCAndPostFix HTTP/1.1
GET /twiki/bin/view/TWiki/WebTopicEditTemplate HTTP/1.1
GET /twiki/bin/view/Main/TokyoOffice HTTP/1.1
GET /twiki/bin/view/TWiki/WikiCulture HTTP/1.1
GET /twiki/bin/view/Main/MikeMannix HTTP/1.1
GET /twiki/bin/view/TWiki/WikiCulture HTTP/1.1
GET /twiki/bin/view/TWiki/WikiCulture HTTP/1.1
[10] row(s) selected.
 
-- Obtain number of data containing 'robots.txt'.
Mach> SELECT COUNT(*) FROM SAMPLE_TABLE WHERE EVENTLOG SEARCH 'robots.txt';
COUNT(*)
-----------------------
40283
[1] row(s) selected.
 
-- Aggregate data containing 'robots.txt' by SRCIP and output only top 10.
Mach> SELECT SRCIP, COUNT(*) FROM SAMPLE_TABLE WHERE EVENTLOG SEARCH 'robots.txt' GROUP BY SRCIP ORDER BY 2 DESC LIMIT 10;
SRCIP           COUNT(*)
----------------------------------------
81.227.25.139   616
162.80.44.96    596
7.234.88.67     595
227.106.13.91   578
220.192.100.45  570
46.201.48.18    570
231.146.69.51   564
185.22.195.164  564
64.58.31.79     561
50.5.206.126    561
[10] row(s) selected.
```


##  Time Series Data Retrieval

Machbase provides a convenient syntax for querying time series data. Learn how to query fast data using DURATION.

```sql
-- Check maximum and minimum values entered in _arrival_time column.
Mach> SELECT MIN(_ARRIVAL_TIME), MAX(_ARRIVAL_TIME) FROM SAMPLE_TABLE;
MIN(_ARRIVAL_TIME)              MAX(_ARRIVAL_TIME)
-------------------------------------------------------------------
2015-05-20 06:00:00 000:000:000 2015-05-20 06:40:10 000:000:000
[1] row(s) selected.
 
-- Use DATE_TRUNC() to obtain count per minute.
Mach> SELECT DATE_TRUNC('minute', _ARRIVAL_TIME) as TIME, COUNT(*) as COUNT FROM SAMPLE_TABLE GROUP BY TIME ORDER BY TIME;
TIME                            COUNT
--------------------------------------------------------
2015-05-20 06:00:00 000:000:000 32001
2015-05-20 06:01:00 000:000:000 28000
2015-05-20 06:02:00 000:000:000 24000
2015-05-20 06:03:00 000:000:000 32000
2015-05-20 06:04:00 000:000:000 16000
2015-05-20 06:05:00 000:000:000 16000
2015-05-20 06:06:00 000:000:000 32000
2015-05-20 06:07:00 000:000:000 32000
2015-05-20 06:08:00 000:000:000 20000
2015-05-20 06:09:00 000:000:000 24000
2015-05-20 06:10:00 000:000:000 20000
2015-05-20 06:11:00 000:000:000 20000
2015-05-20 06:12:00 000:000:000 24000
2015-05-20 06:13:00 000:000:000 20000
2015-05-20 06:14:00 000:000:000 32000
2015-05-20 06:15:00 000:000:000 24000
2015-05-20 06:16:00 000:000:000 32000
2015-05-20 06:17:00 000:000:000 28000
2015-05-20 06:18:00 000:000:000 32000
2015-05-20 06:19:00 000:000:000 12000
2015-05-20 06:20:00 000:000:000 24000
2015-05-20 06:21:00 000:000:000 28000
2015-05-20 06:22:00 000:000:000 28000
2015-05-20 06:23:00 000:000:000 24000
2015-05-20 06:24:00 000:000:000 28000
2015-05-20 06:25:00 000:000:000 28000
2015-05-20 06:26:00 000:000:000 32000
2015-05-20 06:27:00 000:000:000 20000
2015-05-20 06:28:00 000:000:000 20000
2015-05-20 06:29:00 000:000:000 20000
2015-05-20 06:30:00 000:000:000 28000
2015-05-20 06:31:00 000:000:000 32000
2015-05-20 06:32:00 000:000:000 32000
2015-05-20 06:33:00 000:000:000 28000
2015-05-20 06:34:00 000:000:000 20000
2015-05-20 06:35:00 000:000:000 24000
2015-05-20 06:36:00 000:000:000 24000
2015-05-20 06:37:00 000:000:000 16000
2015-05-20 06:38:00 000:000:000 24000
2015-05-20 06:39:00 000:000:000 16000
2015-05-20 06:40:00 000:000:000 3999
[41] row(s) selected.
 
-- Use DURATION statement to specify time range one minute before specified time reference.
Mach> SELECT MIN(_ARRIVAL_TIME), MAX(_ARRIVAL_TIME), COUNT(*) as COUNT FROM SAMPLE_TABLE DURATION 1 MINUTE BEFORE TO_DATE('2015-05-20 06:30:00');
MIN(_ARRIVAL_TIME)              MAX(_ARRIVAL_TIME)              COUNT
-----------------------------------------------------------------------------------------
2015-05-20 06:29:05 000:000:000 2015-05-20 06:29:45 000:000:000 20000
[1] row(s) selected.
 
-- Use DURATION syntax to specify time range after one minute from specific time reference.
Mach> SELECT MIN(_ARRIVAL_TIME), MAX(_ARRIVAL_TIME), COUNT(*) as COUNT FROM SAMPLE_TABLE DURATION 1 MINUTE AFTER TO_DATE('2015-05-20 06:30:00');
MIN(_ARRIVAL_TIME)              MAX(_ARRIVAL_TIME)              COUNT
-----------------------------------------------------------------------------------------
2015-05-20 06:30:04 000:000:000 2015-05-20 06:30:57 000:000:000 28000
[1] row(s) selected.
 
 
-- Use DURATION statement to specify FROM to TO time range.
Mach> SELECT MIN(_ARRIVAL_TIME), MAX(_ARRIVAL_TIME), COUNT(*) as COUNT FROM SAMPLE_TABLE DURATION FROM TO_DATE('2015-05-20 06:20:00') TO TO_DATE('2015-05-20 06:30:00');
MIN(_ARRIVAL_TIME)              MAX(_ARRIVAL_TIME)              COUNT
-----------------------------------------------------------------------------------------
2015-05-20 06:20:03 000:000:000 2015-05-20 06:29:45 000:000:000 252000
[1] row(s) selected.
```


##  Internet Address Type Data Retrieval

Machbase provides data types for Internet addresses and can be conveniently searched.

```sql
-- Set IP band in Netmask format and inquire.
Mach> SELECT COUNT(*) FROM SAMPLE_TABLE WHERE SRCIP CONTAINED '100.195.159.0/24';
COUNT(*)
-----------------------
13097
[1] row(s) selected.
 
 
-- Equal (=) search is also possible using '*'.
Mach> SELECT COUNT(*) FROM SAMPLE_TABLE WHERE SRCIP = '100.195.159.*';
COUNT(*)
-----------------------
13097
[1] row(s) selected.
```