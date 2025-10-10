---
title : SQL로 로드
type: docs
weight: 40
---

'Load Data' 문은 csv 파일의 데이터를 Machbase에 입력합니다.

먼저 데이터를 저장할 테이블을 생성하는데, csv 파일의 첫 번째 줄을 사용하여 컬럼을 생성합니다.

* 생성된 컬럼의 데이터 타입은 VARCHAR(32768)입니다.
* 데이터 파일 경로는 $MACHBASE_HOME 기준의 상대 경로입니다. 절대 경로로 설정할 수도 있습니다.

테이블 데이터를 csv 파일로 저장하려면 SAVE DATA 문을 사용합니다.

미리 테이블을 생성하는 경우, CSV 파일의 각 필드에 대한 데이터 타입은 VARCHAR 또는 TEXT로 설정해야 합니다.

'load_sample.csv' 파일을 LOAD DATA 문에 입력하면 'load_sample' 테이블이 자동으로 생성됩니다.


## 데이터 로드

```sql
LOAD DATA INFILE 'sample/quickstart/load_sample.csv' INTO TABLE load_sample AUTO HEADUSE;
```

## 데이터 로드 확인

```sql
SELECT * FROM load_sample;
```


## 샘플 예제

샘플 파일을 사용하여 다음과 같이 수행할 수 있습니다.

```bash
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
