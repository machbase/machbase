---
title : '스트림 활용을 위한 샘플 예제'
type: docs
weight: 30
---

## 샘플 데이터 다운로드

아래 가이드를 따라 샘플 데이터를 다운로드한다.

```bash
### 1. MACHBASE git repository에서 샘플 데이터를 clone한다.
$ git clone https://www.github.com/MACHBASE/TagTutorial.git MyTutorial
 
### 2. 필요한 데이터를 압축 해제한다.
$ cd MyTutorial/
$ gunzip edu_3_plc_stream/*.gz
 
### 3. 샘플 데이터가 있는 이렉토리로 이동한다.
$ cd edu_3_plc_stream/
```

## TAG, LOG 테이블의 생성

STREAM 기능을 사용하기 위해 아래 명령어들을 환경에 맞게 수정 후 실행해 TAG, LOG 테이블을 생성한다.

```bash
$ pwd
~/MyTutorial/edu_3_plc_stream
 
### 1-1. TAG 테이블 생성
$ machsql --server=127.0.0.1 --port=${MACHBASE_PORT_NO} --user=SYS --password=MANAGER --script=1_create_tag.sql
### 1-2. TAG Meta 로드
$ sh 2_load_meta.sh
 
### 2. LOG 테이블 생성
$ machsql --server=127.0.0.1 --port=${MACHBASE_PORT_NO} --user=SYS --password=MANAGER --script=3_create_plc_tag_table.sql
```

## STREAM 생성, 구동

생성된 TAG, LOG 테이블에 맞게 작성된 샘플 파일을 수행해 STREAM을 시작한다.

```bash
$ machsql --server=127.0.0.1 --port=${MACHBASE_PORT_NO} --user=SYS --password=MANAGER --script=4_plc_stream_tag.sql
```

해당 샘플 파일에 포함된 쿼리에는 두 종류가 있는데 각각 STREAM을 생성하고 생성된 STREAM을 구동하는 역할을 한다.

```sql
### STREAM 생성 Query 예
### event_v0라는 이름의 MTAG_V00를 name으로 가지고 plc_tag_table에 입력되는 데이터 중 tm과 v0 column 데이터를 time, value로 가지는 row를 tag 테이블에 입력하는 STREAM을 생성
EXEC STREAM_CREATE(event_v0, 'insert into tag select ''MTAG_V00'', tm, v0 from plc_tag_table;');
### STREAM 구동 Query 예
EXEC STREAM_START(event_v0);
```

STREAM을 정상적으로 구동시켰다면 이제부터 plc_tag_table에 데이터가 입력되는 순간 각 STREAM이 동작해 해당되는 데이터를 TAG 테이블에 입력한다.

## STREAM 상태 확인

Machbase에서 지원하는 가상 테이블인 v$streams를 통해 수행중인 STREAM의 갯수, 사용 쿼리, 상태, 에러 메시지 등을 확인할 수 있다.

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

다음과 같이 모든 STREAM의 상태를 확인할 수 있다.

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

## 데이터 로드

STREAM이 모두 구동중임을 확인했으니 Machloader를 사용해 데이터를 입력, 작동을 확인한다.

STREAM은 입력 방식에 관계 없이 작동하므로 CLI, JDBC, Collector 등 어떤 방식의 입력이 발생하더라도 TAG 테이블로 자동 입력된다.

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

데이터 로드 중 TAG 테이블 데이터를 확인해보면 실시간으로 데이터가 입력됨을 확인할 수 있다.

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

## STREAM 동작의 결과 확인

아래와 같이 STREAM이 소스 테이블(plc_tag_table)의 데이터를 어디까지 읽었는지를 확인할 수 있다.

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

end_rid column의 값이 소스 테이블의 레코드 갯수와 동일하면 소스 테이블에서 더 이상 읽을 것이 없다는 뜻이다.

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

TAG 테이블의 데이터 갯수가 소스 테이블의 갯수 * STREAM의 갯수와 같으므로 STREAM이 정상적으로 모든 데이터를 읽었음을 확인할 수 있다.

```sql
Mach> select count(*) from TAG;
count(*)
-----------------------
36000000
[1] row(s) selected.
```

입력된 데이터의 시간 범위도 다음과 같이 확인할 수 있다.

```sql
Mach> select min(time), max(time) from TAG;
min(time)                       max(time)
-------------------------------------------------------------------
2009-01-28 07:03:34 000:000:000 2009-01-28 12:36:58 020:000:000
[1] row(s) selected.
```

## 데이터 추가

STREAM이 실제로 각 데이터 입력마다 반응하는지 확인하기 위해 insert 구문을 통해 확인해볼 수 있다.

```sql
Mach> insert into plc_tag_table values(TO_DATE('2009-01-28 12:37:00 000:000:000'), 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000);
1 row(s) inserted.
```

PLC_TAG_TABLE에 레코드 하나를 더 추가한 순간 아래와 같이 각 스트림의 end_rid가 1건 늘어 2000001 건이 된 것을 확인할 수 있다.

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
