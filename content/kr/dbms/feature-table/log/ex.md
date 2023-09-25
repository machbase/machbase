---
title : '로그 테이블 활용 샘플 예제'
type: docs
weight: 60
---

마크베이스 패키지를 설치하면 로그 테이블을 생성하고 로그 데이터를 생성된 테이블에 입력하고 조회하는 튜토리얼을 제공한다.

아래 경로에서 확인할 수 있다.

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

## 로그 테이블 생성

입력할 로그 데이터는 다음은 csv 포맷의 파일이다.

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

로그 데이터의 각각의 필드 값을 확인하고 테이블을 생성한다. machsql 상에서 'CREATE TABLE' 구문을 이용하여 생성하면 된다.

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

또는 테이블 생성 스크립트 파일을 만들어서 OS 커맨드 라인상에서 machsql 을 실행해도 된다.

```sql
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

## 로그 데이터 입력

로그 데이터는 csv 포맷 파일이므로 csvimport 를 이용하여 로딩하면 된다.

로그 파일의 첫번째 필드가 날짜인데, 이 값을 _arrival_time 컬럼에 입력하도록  옵션을 지정한다.

```sql
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

## 로그 데이터 조회

데이터 조회는 machsql 상에서 확인한다.

```sql
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

## 인덱스 생성 및 조회

생성된 sample_table 컬럼 중에서 varchar 형인 eventlog 컬럼에 대해서 keyword 인덱스를 생성하고 텍스트 검색을 해본다.

```sql
-- eventlog_index 인덱스를 생성한다.
Mach> CREATE INDEX eventlog_index ON SAMPLE_TABLE( eventlog) INDEX_TYPE KEYWORD;
Created successfully.
Elapsed time: 0.442
 
-- 생성된 인덱스를 확인한다.
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
 
 
-- SEARCH 구문을 이용하여 'view' 가 들어간 데이터를 검색한다.
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
 
-- 'robots.txt'가 포함된 데이터 건수를 구한다.
Mach> SELECT COUNT(*) FROM SAMPLE_TABLE WHERE EVENTLOG SEARCH 'robots.txt';
COUNT(*)
-----------------------
40283
[1] row(s) selected.
 
-- 'robots.txt'가 포함된 데이터를 SRCIP 별로 집계해서 상위 10개만 출력한다.
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

## 시계열 데이터 조회

마크베이스는 시계열 데이터를 조회하는데 편리한 구문을 제공하고 있다. DURATION을 이용하여 빠른 데이터를 조회하는 방법을 알아본다.

```sql
-- _arrival_time 컬럼에 입력된 최대,최소값을 확인한다.
Mach> SELECT MIN(_ARRIVAL_TIME), MAX(_ARRIVAL_TIME) FROM SAMPLE_TABLE;
MIN(_ARRIVAL_TIME)              MAX(_ARRIVAL_TIME)
-------------------------------------------------------------------
2015-05-20 06:00:00 000:000:000 2015-05-20 06:40:10 000:000:000
[1] row(s) selected.
 
-- DATE_TRUNC() 함수를 이용하여 분당 건수를 구한다.
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
 
-- DURATION 구문을 이용하여 특정시각 기준 1분 이전 시간 범위를 지정하여 조회한다.
Mach> SELECT MIN(_ARRIVAL_TIME), MAX(_ARRIVAL_TIME), COUNT(*) as COUNT FROM SAMPLE_TABLE DURATION 1 MINUTE BEFORE TO_DATE('2015-05-20 06:30:00');
MIN(_ARRIVAL_TIME)              MAX(_ARRIVAL_TIME)              COUNT
-----------------------------------------------------------------------------------------
2015-05-20 06:29:05 000:000:000 2015-05-20 06:29:45 000:000:000 20000
[1] row(s) selected.
 
-- DURATION 구문을 이용하여 특정시각 기준 1분 이후 시간 범위를 지정하여 조회한다.
Mach> SELECT MIN(_ARRIVAL_TIME), MAX(_ARRIVAL_TIME), COUNT(*) as COUNT FROM SAMPLE_TABLE DURATION 1 MINUTE AFTER TO_DATE('2015-05-20 06:30:00');
MIN(_ARRIVAL_TIME)              MAX(_ARRIVAL_TIME)              COUNT
-----------------------------------------------------------------------------------------
2015-05-20 06:30:04 000:000:000 2015-05-20 06:30:57 000:000:000 28000
[1] row(s) selected.
 
 
-- DURATION 구문을 이용하여 FROM ~ TO 시간 범위를 지정하여 조회한다.
Mach> SELECT MIN(_ARRIVAL_TIME), MAX(_ARRIVAL_TIME), COUNT(*) as COUNT FROM SAMPLE_TABLE DURATION FROM TO_DATE('2015-05-20 06:20:00') TO TO_DATE('2015-05-20 06:30:00');
MIN(_ARRIVAL_TIME)              MAX(_ARRIVAL_TIME)              COUNT
-----------------------------------------------------------------------------------------
2015-05-20 06:20:03 000:000:000 2015-05-20 06:29:45 000:000:000 252000
[1] row(s) selected.
```

## 인터넷 주소형 데이터 조회

마크베이스는 인터넷 주소에 대해서 데이터 타입으로 제공하고 편리하게 검색할 수 있다.

```sql
-- Netmask 형식으로 IP 대역을 설정하여 조회한다.
Mach> SELECT COUNT(*) FROM SAMPLE_TABLE WHERE SRCIP CONTAINED '100.195.159.0/24';
COUNT(*)
-----------------------
13097
[1] row(s) selected.
 
 
-- '*' 를 이용하여 Equal(=) 검색도 가능하다.
Mach> SELECT COUNT(*) FROM SAMPLE_TABLE WHERE SRCIP = '100.195.159.*';
COUNT(*)
-----------------------
13097
[1] row(s) selected.
```
