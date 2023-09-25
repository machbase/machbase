---
title : '데이터 불러오기 : Load'
type: docs
weight: 40
---

'Load Data' 문은 csv 파일을 마크베이스에 입력한다.

먼저 데이터를 저장할 테이블을 생성하는데, csv 파일의 첫 번째 라인을 이용하여 칼럼들을 생성한다.

* 생성된 칼럼들의 데이터 타입은 VARCHAR(32768)이다.
* 데이터 파일 경로는 $MACHBASE_HOME을 기준으로 한 상대 경로이다. 절대경로로 설정할 수도 있다.
테이블의 데이터들을 csv 파일로 저장하기 위해서는 SAVE DATA 문을 이용한다.

만약 csv파일의 각 필드에 대한 데이터 타입을 미리 알고 있다면, 테이블을 미리 생성하여 데이터를 입력할 수 있다.

'load_sample.csv' 파일을 LOAD DATA 문으로 입력하면, 테이블 'load_sample' 이 자동으로 생성된다.

## 데이터 불러오기
```sql
LOAD DATA INFILE 'sample/quickstart/load_sample.csv' INTO TABLE load_sample AUTO HEADUSE;
```

## 입력 데이터 확인
```sql
SELECT * FROM load_sample;
```

## 샘플 예제

샘플 파일을 이용하여, 다음과 같이 실행할 수 있다.

```sql
[mach@localhost ~]$ cd $MACHBASE_HOME/sample/quickstart
[mach@localhost ~]$ ls -l load_sample.csv
-rw-r
--r--- 1 root root 2827 2017-02-23 15:01 load_sample.csv
 
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
MACH_CONNECT_MODE=INET, PORT=5656
 
Mach> LOAD DATA INFILE 'sample/quickstart/load_sample.csv' INTO TABLE load_sample AUTO HEADUSE;
50 row(s) loaded. Failed to load 0 row(s).
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
