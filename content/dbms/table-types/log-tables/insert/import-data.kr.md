---
title : Import
type: docs
weight: 30
---

machloader 도구를 사용하면 CSV 또는 다른 구분자로 구분된 텍스트 파일을 입력할 수 있습니다.

machloader 도구에 대한 자세한 설명은 [machloader](/dbms/tools-reference/machloader) 문서를 참조하세요.

## 목차

* [데이터 가져오기](#importing-data)
* [데이터 입력 확인](#confirm-data-insert)
* [샘플 예제](#sample-example)


## 테이블 생성

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


## 데이터 가져오기

machloader 도구를 사용하여 csv 파일을 입력합니다.

```bash
machloader  -i  -t  import_sample   -d  sample_data.csv
```


## 데이터 입력 확인

입력된 데이터를 확인합니다.


``` sql
SELECT  COUNT(*)    FROM    import_sample;
```


## 샘플 예제

다음은 실제 machloader와 machsql을 사용한 샘플 프로세스입니다.

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
[mach@localhost ~]$ ls -l sample_data.csv
-rw-r--r--- 1 mach mach 110477124 2017-02-23 15:18 sample_data.csv
 
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
IMPORT_MODE    : APPEND
FILED TERM     : ,                   ROW TERM       : \n
ENCLOSURE      : "                   ARRIVAL_TIME   : FALSE
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
