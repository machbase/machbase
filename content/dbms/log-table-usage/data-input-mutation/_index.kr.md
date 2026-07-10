---
title: '7.4 데이터 입력과 변경'
weight: 40
toc: true
---

LOG 테이블에 데이터를 입력하는 방법은 SQL INSERT, Append API, machloader Import, LOAD DATA 네 가지가 있다.


<a id="original-85-insert-data"></a>

## Insert


다른 상용 RDBMS와 마찬가지로, 테이블을 먼저 생성한 뒤 INSERT INTO 문으로 데이터를 입력한다.

Machbase는 대화형 쿼리 프로세서로 'machsql' 도구를 제공한다.


### 테이블 생성

```sql
CREATE TABLE table_name ( column1 datatype, column2 datatype, column3 datatype, .... );
```

```sql
CREATE TABLE sensor_data ( id VARCHAR(32), val DOUBLE );
```


### 데이터 삽입

```sql
INSERT INTO table_name VALUES (value1, value2, value3, ...);
```

```sql
INSERT INTO sensor_data VALUES('sensor1', 10.1);
INSERT INTO sensor_data VALUES('sensor2', 20.2);
INSERT INTO sensor_data VALUES('sensor3', 30.3);
```


### 데이터 삽입 확인

```sql
SELECT column1, column2, ... FROM table_name;
```

```sql
SELECT * FROM sensor_data;
```


### 전체 프로세스

machsql을 사용한 예제는 다음과 같다.

```sql
Mach> CREATE TABLE sensor_data (id VARCHAR(32), val DOUBLE);
 Created successfully.
Mach> INSERT INTO sensor_data VALUES('sensor1', 10.1);
 1 row(s) inserted.
Mach> INSERT INTO sensor_data VALUES('sensor2', 20.2);
 1 row(s) inserted.
Mach> INSERT INTO sensor_data VALUES('sensor3', 30.3);
 1 row(s) inserted.
Mach> SELECT * FROM sensor_data;
ID VAL
-----------------------------------------------------------------
sensor3 30.3
sensor2 20.2
sensor1 10.1
[3] row(s) selected.
```

<a id="original-85-append-data"></a>

## Append


Machbase가 제공하는 고속 실시간 데이터 입력 API다.

C, C++, C#, Java, Python, PHP, Javascript로 호출할 수 있다.

자세한 내용은 [SDK 및 통합](../../../../sdk-integration/) 가이드를 참조한다.

<a id="original-85-import-data"></a>

## Import


machloader 도구를 사용하면 CSV 등 구분자 기반 텍스트 파일을 일괄 입력할 수 있다.

machloader에 대한 자세한 설명은 [machloader](/dbms/application-integration/data-input-load-export/#file-import-machloader) 문서를 참조한다.

### 목차

* [데이터 가져오기](#importing-data)
* [데이터 입력 확인](#confirm-data-insert)
* [샘플 예제](#sample-example)


### 테이블 생성

```sql
CREATE TABLE import_sample
(
    srcip     IPV4,
    srcport   INTEGER,
    dstip     IPV4,
    dstport   INTEGER,
    protocol  SHORT,
    eventlog  VARCHAR(1024),
    eventcode SHORT,
    eventsize LONG
);
```


### 데이터 가져오기

machloader로 csv 파일을 입력한다.

```bash
machloader  -i  -t  import_sample   -d  sample_data.csv
```


### 데이터 입력 확인

입력된 데이터를 확인한다.


``` sql
SELECT  COUNT(*)    FROM    import_sample;
```


### 샘플 예제

machloader와 machsql을 사용한 전체 프로세스다.

```sql
Mach> CREATE TABLE import_sample
     (
         srcip     IPV4,
         srcport   INTEGER,
         dstip     IPV4,
         dstport   INTEGER,
         protocol  SHORT,
         eventlog  VARCHAR(1024),
         eventcode SHORT,
         eventsize LONG
     );
Created successfully.
Mach> quit
```

```bash
[mach@localhost ~]$ cd $MACHBASE_HOME/sample/quickstart
[mach@localhost ~]$ tar -xzf sample_data.tar.gz
[mach@localhost ~]$ ls -l sample_data.csv
-rw-r--r-- 1 mach mach 110477124 Nov  9  2022 sample_data.csv

[mach@localhost ~]$ machloader -i -t import_sample -d sample_data.csv
-----------------------------------------------------------------
     Machbase Data Import/Export Utility.
     Release Version x.x.x.official
     Copyright 2014, Machbase Inc. or its subsidiaries.
     All Rights Reserved.
-----------------------------------------------------------------
NLS            : US7ASCII            EXECUTE MODE   : IMPORT
TARGET TABLE   : import_sample
DATA FILE      : sample_data.csv
IMPORT MODE    : APPEND              FIELD TERM     : ,
ROW TERM       : \n                  ENCLOSURE      : "
ESCAPE         : \                   ARRIVAL_TIME   : FALSE
ENCODING       : NONE                HEADER         : FALSE
CREATE TABLE   : FALSE
 Progress bar                       Imported records        Error records
                                             1000000                    0
Import time         :  0 hour  0 min  2.39 sec
Load success count  : 1000000
Load fail count     : 0
[mach@localhost ~]$
```

```sql
Mach> SELECT COUNT(*) FROM import_sample;
COUNT(*)
-----------------------
1000000
[1] row(s) selected.
Mach>
```

<a id="original-85-load-data"></a>

## SQL로 로드


'Load Data' 문은 csv 파일의 데이터를 Machbase에 입력한다.

csv 파일의 첫 번째 줄로 컬럼을 자동 생성하며, 생성되는 컬럼의 데이터 타입은 VARCHAR(32768)이다. 데이터 파일 경로는 $MACHBASE_HOME 기준의 상대 경로이며, 절대 경로도 사용 가능하다.

테이블 데이터를 csv 파일로 저장하려면 SAVE DATA 문을 사용한다.

미리 테이블을 생성하는 경우, CSV 파일의 각 필드에 대한 데이터 타입은 VARCHAR 또는 TEXT로 설정해야 한다.

'load_sample.csv' 파일을 LOAD DATA 문에 입력하면 'load_sample' 테이블이 자동으로 생성된다.


### 데이터 로드

```sql
LOAD DATA INFILE 'sample/quickstart/load_sample.csv' INTO TABLE load_sample AUTO HEADUSE;
```

### 데이터 로드 확인

```sql
SELECT * FROM load_sample;
```


### 샘플 예제

샘플 파일을 사용한 전체 수행 과정이다.

```bash
[mach@localhost ~]$ cd $MACHBASE_HOME/sample/quickstart
[mach@localhost ~]$ ls -l load_sample.csv
-rw-r--r-- 1 mach mach 2373 Jun 13 15:07 load_sample.csv

[mach@localhost ~]$ machsql
=================================================================
     Machbase Client Query Utility
     Release Version x.x.x.official
     Copyright 2014, Machbase Inc. or its subsidiaries.
     All Rights Reserved
=================================================================
Machbase server address (Default:127.0.0.1) :
Machbase user ID  (Default:SYS)
Machbase User Password :
MACHBASE_CONNECT_MODE=INET, PORT=5656 EDITION=STANDARD

Mach> LOAD DATA INFILE 'sample/quickstart/load_sample.csv' INTO TABLE load_sample AUTO HEADUSE;
50 row(s) loaded.
Mach> DESC load_sample;
----------------------------------------------------------------
NAME                          TYPE                LENGTH
----------------------------------------------------------------
SENSOR_ID                     varchar             32767
EPOCH_TIME                    varchar             32767
E_YEAR                        varchar             32767
E_MONTH                       varchar             32767
E_DAY                         varchar             32767
E_HOUR                        varchar             32767
E_MINUTE                      varchar             32767
E_SECOND                      varchar             32767
VALUE                         varchar             32767
Mach> SELECT COUNT(*) FROM load_sample;
COUNT(*)
-----------------------
50
[1] row(s) selected.
Mach>
```
