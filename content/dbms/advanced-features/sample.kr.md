---
title : 스트림 사용 예제
type: docs
weight: 30
---

## 샘플 데이터 다운로드

아래 절차에 따라 샘플 데이터를 다운로드합니다.

```bash
## ##  1. MACHBASE Git 저장소에서 샘플 데이터를 클론합니다.
$ git clone https://www.github.com/MACHBASE/TagTutorial.git MyTutorial

## ##  2. 필요 데이터의 압축을 해제합니다.
$ cd MyTutorial/
$ gunzip edu_3_plc_stream/*.gz

## ##  3. 샘플 데이터가 위치한 디렉터리로 이동합니다.
$ cd edu_3_plc_stream/
```

## TAG, LOG 테이블 생성

STREAM 기능을 사용하기 위해 아래 명령을 환경에 맞게 수정해 실행하면 TAG/LOG 테이블이 생성됩니다.

```bash
$ pwd
~/MyTutorial/edu_3_plc_stream

## ##  1-1. TAG 테이블 생성
$ machsql --server=127.0.0.1 --port=${MACHBASE_PORT_NO} --user=SYS --password=MANAGER --script=1_create_tag.sql
## ##  1-2. TAG 메타 로딩
$ sh 2_load_meta.sh

## ##  2. LOG 테이블 생성
$ machsql --server=127.0.0.1 --port=${MACHBASE_PORT_NO} --user=SYS --password=MANAGER --script=3_create_plc_tag_table.sql
```

## STREAM 생성 및 실행

생성된 TAG/LOG 테이블을 대상으로 작성된 샘플 스크립트를 실행해 STREAM을 생성하고 시작합니다.

```bash
$ machsql --server=127.0.0.1 --port=${MACHBASE_PORT_NO} --user=SYS --password=MANAGER --script=4_plc_stream_tag.sql
```

샘플 파일에는 STREAM을 생성하는 쿼리와 실행하는 쿼리가 포함되어 있습니다.

```sql
## ##  STREAM 생성 예시
EXEC STREAM_CREATE(event_v0, 'insert into tag select ''MTAG_V00'', tm, v0 from plc_tag_table;');

## ##  STREAM 실행 예시
EXEC STREAM_START(event_v0);
```

STREAM이 정상적으로 실행되면 `plc_tag_table`에 데이터가 삽입될 때마다 모든 STREAM이 동작하여 해당 데이터를 TAG 테이블로 적재합니다.

## STREAM 상태 확인

Machbase가 제공하는 가상 테이블 `v$streams`를 통해 실행 중인 스트림 수, 사용 중인 쿼리, 상태, 오류 메시지를 확인할 수 있습니다.

```sql
Mach> desc v$streams;
[ COLUMN ]
----------------------------------------------------------------------------------------------------
NAME                                                        NULL?    TYPE                LENGTH
----------------------------------------------------------------------------------------------------
NAME                                                                 varchar             100
LAST_EX_TIME                                                         datetime            31
TABLE_NAME                                                           varchar             100
END_RID                                                              long                20
STATE                                                                varchar             10
QUERY_TXT                                                            varchar             2048
ERROR_MSG                                                            varchar             2048
FREQUENCY                                                            ulong               20
```

실행 중인 모든 STREAM은 다음과 같이 조회할 수 있습니다.

```sql
Mach> select state, name, table_name, query_txt from v$streams;
STATE   NAME     TABLE_NAME    QUERY_TXT
------------------------------------------------------------------------------------------------
RUNNING EVENT_V0 PLC_TAG_TABLE insert into tag select 'MTAG_V00', tm, v0 from plc_tag_table;
RUNNING EVENT_V1 PLC_TAG_TABLE insert into tag select 'MTAG_V00', tm, v1 from plc_tag_table;
RUNNING EVENT_C0 PLC_TAG_TABLE insert into tag select 'MTAG_C00', tm, c0 from plc_tag_table;
RUNNING EVENT_C1 PLC_TAG_TABLE insert into tag select 'MTAG_C01', tm, c1 from plc_tag_table;
RUNNING EVENT_C2 PLC_TAG_TABLE insert into tag select 'MTAG_C02', tm, c2 from plc_tag_table;
RUNNING EVENT_C3 PLC_TAG_TABLE insert into tag select 'MTAG_C03', tm, c3 from plc_tag_table;
RUNNING EVENT_C4 PLC_TAG_TABLE insert into tag select 'MTAG_C04', tm, c4 from plc_tag_table;
RUNNING EVENT_C5 PLC_TAG_TABLE insert into tag select 'MTAG_C05', tm, c5 from plc_tag_table;
RUNNING EVENT_C6 PLC_TAG_TABLE insert into tag select 'MTAG_C06', tm, c6 from plc_tag_table;
RUNNING EVENT_C7 PLC_TAG_TABLE insert into tag select 'MTAG_C07', tm, c7 from plc_tag_table;
RUNNING EVENT_C8 PLC_TAG_TABLE insert into tag select 'MTAG_C08', tm, c8 from plc_tag_table;
RUNNING EVENT_C9 PLC_TAG_TABLE insert into tag select 'MTAG_C09', tm, c9 from plc_tag_table;
RUNNING EVENT_C10 PLC_TAG_TABLE insert into tag select 'MTAG_C10', tm, c10 from plc_tag_table;
RUNNING EVENT_C11 PLC_TAG_TABLE insert into tag select 'MTAG_C11', tm, c11 from plc_tag_table;
RUNNING EVENT_C12 PLC_TAG_TABLE insert into tag select 'MTAG_C12', tm, c12 from plc_tag_table;
RUNNING EVENT_C13 PLC_TAG_TABLE insert into tag select 'MTAG_C13', tm, c13 from plc_tag_table;
RUNNING EVENT_C14 PLC_TAG_TABLE insert into tag select 'MTAG_C14', tm, c14 from plc_tag_table;
RUNNING EVENT_C15 PLC_TAG_TABLE insert into tag select 'MTAG_C15', tm, c15 from plc_tag_table;
```

## 데이터 적재

모든 STREAM이 동작하는 것을 확인했으면, Machloader를 사용해 데이터를 입력하고 동작을 검증합니다. STREAM은 입력 방식과 무관하게 동작하므로 CLI, JDBC, Collector 등 어떤 입력 도구를 사용해도 TAG 테이블에 자동으로 적재됩니다.

```bash
$ cat 5_plc_tag_load.sh
machloader  -t plc_tag_table -i -d 5_plc_tag.csv -F "tm YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn"

$ sh 5_plc_tag_load.sh
-----------------------------------------------------------------
     Machbase Data Import/Export Utility.
     Release Version 6.5.1.official
     Copyright 2014, MACHBASE Corporation or its subsidiaries.
     All Rights Reserved.
-----------------------------------------------------------------
NLS            : US7ASCII            EXECUTE MODE   : IMPORT
TARGET TABLE   : plc_tag_table       DATA FILE      : 5_plc_tag.csv
IMPORT MODE    : APPEND              FIELD TERM     : ,
ROW TERM       : \n                  ENCLOSURE      : "
ESCAPE         : \                   ARRIVAL_TIME   : FALSE
ENCODING       : NONE                HEADER         : FALSE
CREATE TABLE   : FALSE

 Progress bar                       Imported records        Error records
                                              80000                    0
```

데이터 로딩 중에 TAG 테이블을 조회하면 데이터가 실시간으로 적재되는 것을 확인할 수 있습니다.

```sql
Mach> select count(*) from TAG;
count(*)
-----------------------
16775979
[1] row(s) selected.
Mach> select count(*) from TAG;
count(*)
-----------------------
17609187
[1] row(s) selected.
Mach> select count(*) from TAG;
count(*)
-----------------------
18238357
[1] row(s) selected.
Elapsed time: 0.000
```

## STREAM 처리 결과

STREAM이 소스 테이블(`plc_tag_table`) 데이터를 어느 지점까지 읽었는지 다음과 같이 확인할 수 있습니다.

```sql
Mach> select name, state, end_rid from v$streams;
name      state   end_rid
---------------------------------------------------------
EVENT_V0  RUNNING 909912
EVENT_V1  RUNNING 1584671
EVENT_C0  RUNNING 1312416
EVENT_C1  RUNNING 1268520
EVENT_C2  RUNNING 1636800
EVENT_C3  RUNNING 1197840
EVENT_C4  RUNNING 622728
EVENT_C5  RUNNING 972780
EVENT_C6  RUNNING 1021512
EVENT_C7  RUNNING 1287474
EVENT_C8  RUNNING 826956
EVENT_C9  RUNNING 1639032
EVENT_C10 RUNNING 725954
EVENT_C11 RUNNING 1511436
EVENT_C12 RUNNING 531079
EVENT_C13 RUNNING 1004400
EVENT_C14 RUNNING 741768
EVENT_C15 RUNNING 746604
[18] row(s) selected.
```

`end_rid` 값이 소스 테이블의 총 레코드 수와 동일하면 더 이상 읽을 데이터가 없다는 의미입니다.

```sql
Mach> select name, state, end_rid from v$streams;
name      state   end_rid
---------------------------------------------------------
EVENT_V0  RUNNING 2000000
EVENT_V1  RUNNING 2000000
EVENT_C0  RUNNING 2000000
EVENT_C1  RUNNING 2000000
EVENT_C2  RUNNING 2000000
EVENT_C3  RUNNING 2000000
EVENT_C4  RUNNING 2000000
EVENT_C5  RUNNING 2000000
EVENT_C6  RUNNING 2000000
EVENT_C7  RUNNING 2000000
EVENT_C8  RUNNING 2000000
EVENT_C9  RUNNING 2000000
EVENT_C10 RUNNING 2000000
EVENT_C11 RUNNING 2000000
EVENT_C12 RUNNING 2000000
EVENT_C13 RUNNING 2000000
EVENT_C14 RUNNING 2000000
EVENT_C15 RUNNING 2000000
[18] row(s) selected.
```

TAG 테이블의 데이터 수는 `소스 테이블 레코드 수 × STREAM 개수`와 동일하므로, STREAM이 정상적으로 모든 데이터를 처리했음을 확인할 수 있습니다.

```sql
Mach> select count(*) from TAG;
count(*)
-----------------------
36000000
[1] row(s) selected.
```

입력 데이터의 시간 범위도 다음과 같이 확인 가능합니다.

```sql
Mach> select min(time), max(time) from TAG;
min(time)                       max(time)
-------------------------------------------------------------------
2009-01-28 07:03:34 000:000:000 2009-01-28 12:36:58 020:000:000
[1] row(s) selected.
```

## 데이터 추가

STREAM이 데이터 입력마다 반응하는지 INSERT 구문으로 확인합니다.

```sql
Mach> insert into plc_tag_table values(TO_DATE('2009-01-28 12:37:00 000:000:000'), 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000);
1 row(s) inserted.
```

`PLC_TAG_TABLE`에 한 건이 추가되면 아래와 같이 각 스트림의 `end_rid` 값이 2,000,001로 증가합니다.

```sql
Mach> select name, state, end_rid from v$streams;
name      state   end_rid
---------------------------------------------------------------
EVENT_V0  RUNNING 2000001
EVENT_V1  RUNNING 2000001
EVENT_C0  RUNNING 2000001
EVENT_C1  RUNNING 2000001
EVENT_C2  RUNNING 2000001
EVENT_C3  RUNNING 2000001
EVENT_C4  RUNNING 2000001
EVENT_C5  RUNNING 2000001
EVENT_C6  RUNNING 2000001
EVENT_C7  RUNNING 2000001
EVENT_C8  RUNNING 2000001
EVENT_C9  RUNNING 2000001
EVENT_C10 RUNNING 2000001
EVENT_C11 RUNNING 2000001
EVENT_C12 RUNNING 2000001
EVENT_C13 RUNNING 2000001
EVENT_C14 RUNNING 2000001
EVENT_C15 RUNNING 2000001
[18] row(s) selected.
```
