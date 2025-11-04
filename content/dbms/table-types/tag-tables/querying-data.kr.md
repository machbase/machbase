---
title: 'Tag 데이터 조회'
type: docs
weight: 40
---

## 개요

Machbase는 특정 tag에 대한 시간 범위 조회에 특히 뛰어난 고속 tag 데이터 추출 기능을 제공합니다. 이 가이드는 tag 테이블 작업에 필요한 모든 조회 패턴을 다룹니다.

## 빠른 시작

Machbase는 특정 tag의 시간 범위에 대한 고속 tag 데이터 추출을 제공합니다.

##  샘플 스키마

다음 예제에서는 아래와 같이 TAG 테이블을 생성하고 두 개의 tag를 생성했습니다.

각 tag에 대해 2018년 1월 1일부터 2018년 2월 10일까지의 데이터가 입력되었습니다.

```sql
create tag table TAG (name varchar(20) primary key, time datetime basetime, value double summarized);

insert into tag metadata values ('TAG_0001');
insert into tag metadata values ('TAG_0002');

insert into tag values('TAG_0001', '2018-01-01 01:00:00 000:000:000', 1);
insert into tag values('TAG_0001', '2018-01-02 02:00:00 000:000:000', 2);
insert into tag values('TAG_0001', '2018-01-03 03:00:00 000:000:000', 3);
insert into tag values('TAG_0001', '2018-01-04 04:00:00 000:000:000', 4);
insert into tag values('TAG_0001', '2018-01-05 05:00:00 000:000:000', 5);
insert into tag values('TAG_0001', '2018-01-06 06:00:00 000:000:000', 6);
insert into tag values('TAG_0001', '2018-01-07 07:00:00 000:000:000', 7);
insert into tag values('TAG_0001', '2018-01-08 08:00:00 000:000:000', 8);
insert into tag values('TAG_0001', '2018-01-09 09:00:00 000:000:000', 9);
insert into tag values('TAG_0001', '2018-01-10 10:00:00 000:000:000', 10);

insert into tag values('TAG_0002', '2018-02-01 01:00:00 000:000:000', 11);
insert into tag values('TAG_0002', '2018-02-02 02:00:00 000:000:000', 12);
insert into tag values('TAG_0002', '2018-02-03 03:00:00 000:000:000', 13);
insert into tag values('TAG_0002', '2018-02-04 04:00:00 000:000:000', 14);
insert into tag values('TAG_0002', '2018-02-05 05:00:00 000:000:000', 15);
insert into tag values('TAG_0002', '2018-02-06 06:00:00 000:000:000', 16);
insert into tag values('TAG_0002', '2018-02-07 07:00:00 000:000:000', 17);
insert into tag values('TAG_0002', '2018-02-08 08:00:00 000:000:000', 18);
insert into tag values('TAG_0002', '2018-02-09 09:00:00 000:000:000', 19);
insert into tag values('TAG_0002', '2018-02-10 10:00:00 000:000:000', 20);
```


## 모든 TAG 데이터 추출

```bash
Mach> select * from tag;
NAME TIME VALUE
--------------------------------------------------------------------------------------
TAG_0001 2018-01-01 01:00:00 000:000:000 1
TAG_0001 2018-01-02 02:00:00 000:000:000 2
TAG_0001 2018-01-03 03:00:00 000:000:000 3
TAG_0001 2018-01-04 04:00:00 000:000:000 4
TAG_0001 2018-01-05 05:00:00 000:000:000 5
TAG_0001 2018-01-06 06:00:00 000:000:000 6
TAG_0001 2018-01-07 07:00:00 000:000:000 7
TAG_0001 2018-01-08 08:00:00 000:000:000 8
TAG_0001 2018-01-09 09:00:00 000:000:000 9
TAG_0001 2018-01-10 10:00:00 000:000:000 10
TAG_0002 2018-02-01 01:00:00 000:000:000 11
TAG_0002 2018-02-02 02:00:00 000:000:000 12
TAG_0002 2018-02-03 03:00:00 000:000:000 13
TAG_0002 2018-02-04 04:00:00 000:000:000 14
TAG_0002 2018-02-05 05:00:00 000:000:000 15
TAG_0002 2018-02-06 06:00:00 000:000:000 16
TAG_0002 2018-02-07 07:00:00 000:000:000 17
TAG_0002 2018-02-08 08:00:00 000:000:000 18
TAG_0002 2018-02-09 09:00:00 000:000:000 19
TAG_0002 2018-02-10 10:00:00 000:000:000 20
[20] row(s) selected.
```

위와 같이 특별한 조건이 없으면 각 tag별로 시간 순서로 정렬된 데이터를 추출할 수 있습니다.


## 특정 tag 이름으로 데이터 추출

다음은 TAG 이름이 TAG_0002인 데이터의 예제입니다.

```sql
Mach> select * from tag where name='TAG_0002';
NAME                  TIME                            VALUE
--------------------------------------------------------------------------------------
TAG_0002              2018-02-01 01:00:00 000:000:000 11
TAG_0002              2018-02-02 02:00:00 000:000:000 12
TAG_0002              2018-02-03 03:00:00 000:000:000 13
TAG_0002              2018-02-04 04:00:00 000:000:000 14
TAG_0002              2018-02-05 05:00:00 000:000:000 15
TAG_0002              2018-02-06 06:00:00 000:000:000 16
TAG_0002              2018-02-07 07:00:00 000:000:000 17
TAG_0002              2018-02-08 08:00:00 000:000:000 18
TAG_0002              2018-02-09 09:00:00 000:000:000 19
TAG_0002              2018-02-10 10:00:00 000:000:000 20
[10] row(s) selected.
```


## 시간 범위 조회

다음은 TAG_0002에 대한 시간 범위를 조회하여 데이터를 받는 경우입니다.

> between 절을 사용하여 시간 범위를 지정하는 것이 일반적입니다. 물론 '<' 또는 '>'를 사용하여 시간 범위를 지정해도 동일한 결과를 얻을 수 있습니다.

```bash
Mach> select * from tag where name = 'TAG_0002' and time between to_date('2018-02-01') and to_date('2018-02-05');
NAME                  TIME                            VALUE
--------------------------------------------------------------------------------------
TAG_0002              2018-02-01 01:00:00 000:000:000 11
TAG_0002              2018-02-02 02:00:00 000:000:000 12
TAG_0002              2018-02-03 03:00:00 000:000:000 13
TAG_0002              2018-02-04 04:00:00 000:000:000 14
[4] row(s) selected.

Mach> select * from tag where name = 'TAG_0002' and time > to_date('2018-02-01') and time < to_date('2018-02-05');
NAME                  TIME                            VALUE
--------------------------------------------------------------------------------------
TAG_0002              2018-02-01 01:00:00 000:000:000 11
TAG_0002              2018-02-02 02:00:00 000:000:000 12
TAG_0002              2018-02-03 03:00:00 000:000:000 13
TAG_0002              2018-02-04 04:00:00 000:000:000 14
[4] row(s) selected.
```

## 다중 tag에 대한 시간 범위 검색

다음은 두 개 이상의 tag에 대해 동일한 시간 범위의 데이터를 조회하는 예제입니다.

많은 수의 tag에 대해 동시에 빠른 결과를 얻고 싶다면 다음 유형의 쿼리를 수행하는 것이 바람직합니다.

```bash
Mach> select * from tag where name in ('TAG_0002', 'TAG_0001') and time between to_date('2018-01-05') and to_date('2018-02-05');
NAME                  TIME                            VALUE
--------------------------------------------------------------------------------------
TAG_0001              2018-01-05 05:00:00 000:000:000 5
TAG_0001              2018-01-06 06:00:00 000:000:000 6
TAG_0001              2018-01-07 07:00:00 000:000:000 7
TAG_0001              2018-01-08 08:00:00 000:000:000 8
TAG_0001              2018-01-09 09:00:00 000:000:000 9
TAG_0001              2018-01-10 10:00:00 000:000:000 10
TAG_0002              2018-02-01 01:00:00 000:000:000 11
TAG_0002              2018-02-02 02:00:00 000:000:000 12
TAG_0002              2018-02-03 03:00:00 000:000:000 13
TAG_0002              2018-02-04 04:00:00 000:000:000 14
[10] row(s) selected.
```

## 특정 값 이상의 데이터 검색

tag 값에 대한 조건도 다음과 같이 지정할 수 있습니다.

TAG_0002의 값 중 12보다 크고 15보다 작은 값에 대해 필터링이 수행되었습니다.

```bash
Mach> select * from tag where name = 'TAG_0002' and value > 12 and value < 15 and time between to_date('2018-02-01') and to_date('2018-02-05');
NAME                  TIME                            VALUE
--------------------------------------------------------------------------------------
TAG_0002              2018-02-03 03:00:00 000:000:000 13
TAG_0002              2018-02-04 04:00:00 000:000:000 14
[2] row(s) selected.
```

## 특정 Tag ID별 통계 정보 표시

tag 테이블을 생성하면, tag 테이블의 tag ID별로 간단한 통계 정보를 집계하는 가상 테이블이 생성됩니다.

가상 테이블 이름은 v${tag 테이블 이름}_stat입니다.

사용자가 이 테이블을 사용하면 tag 테이블의 통계 정보를 빠르게 얻을 수 있습니다.

통계 정보 대상 컬럼은 자동으로 세 번째 컬럼으로 지정됩니다.


```bash
Mach> CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED);
Executed successfully.

Mach> DESC v$tag_stat;
[ COLUMN ]
----------------------------------------------------------------------------------------------------
NAME                                                        NULL?    TYPE                LENGTH
----------------------------------------------------------------------------------------------------
NAME                                                                 varchar             100
ROW_COUNT                                                            ulong               20
MIN_TIME                                                             datetime            31
MAX_TIME                                                             datetime            31
MIN_VALUE                                                            double              17
MIN_VALUE_TIME                                                       datetime            31
MAX_VALUE                                                            double              17
MAX_VALUE_TIME                                                       datetime            31
RECENT_ROW_TIME                                                      datetime            31
```

세 번째 컬럼에 SUMMARIZED 키워드가 없으면 VALUE 관련 정보(MIN_VALUE, MAX_VALUE, MIN_VALUE_TIME, MAX_VALUE_TIME)는 저장되지 않습니다.

수집되는 통계 정보는 다음과 같습니다.

|컬럼 이름|정보|
|--|--|
|NAME|Tag ID의 이름|
|ROW_COUNT|행 수|
|MIN_TIME|해당 tag ID 행 중 가장 작은 basetime 컬럼 값|
|MAX_TIME|해당 tag ID 행 중 가장 큰 basetime 컬럼 값|
|MIN_VALUE|해당 tag ID 행 중 가장 작은 summarized 컬럼 값|
|MIN_VALUE_TIME|MIN_VALUE와 함께 삽입된 basetime 컬럼 값|
|MAX_VALUE|해당 tag ID 행 중 가장 큰 summarized 컬럼 값|
|MAX_VALUE_TIME|MAX_VALUE와 함께 삽입된 basetime 컬럼 값|
|RECENT_ROW_TIME|가장 최근에 삽입된 basetime 컬럼 값|

select 예제는 다음과 같습니다.

1. SUMMARIZED 컬럼이 존재하는 경우

```bash
Mach> CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED);
Executed successfully.

Mach> INSERT INTO tag VALUES('tag-0', TO_DATE('2021-08-12'), 10);
Mach> INSERT INTO tag VALUES('tag-0', TO_DATE('2021-08-13'), 10);
Mach> INSERT INTO tag VALUES('tag-0', TO_DATE('2021-08-14'), 20);
Mach> INSERT INTO tag VALUES('tag-0', TO_DATE('2021-08-11'), 5);
Mach> INSERT INTO tag VALUES('tag-1', TO_DATE('2022-08-12'), 100);
Mach> INSERT INTO tag VALUES('tag-1', TO_DATE('2022-08-11'), 200);
Mach> INSERT INTO tag VALUES('tag-1', TO_DATE('2022-08-10'), 50);

Mach> SELECT * FROM v$tag_stat;
NAME                                                                              ROW_COUNT            MIN_TIME                        MAX_TIME                        MIN_VALUE
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
MIN_VALUE_TIME                  MAX_VALUE                   MAX_VALUE_TIME                  RECENT_ROW_TIME
---------------------------------------------------------------------------------------------------------------------------------
tag-0                                                                             4                    2021-08-11 00:00:00 000:000:000 2021-08-14 00:00:00 000:000:000 5
2021-08-11 00:00:00 000:000:000 20                          2021-08-14 00:00:00 000:000:000 2021-08-11 00:00:00 000:000:000
tag-1                                                                             3                    2022-08-10 00:00:00 000:000:000 2022-08-12 00:00:00 000:000:000 50
2022-08-10 00:00:00 000:000:000 200                         2022-08-11 00:00:00 000:000:000 2022-08-10 00:00:00 000:000:000
[2] row(s) selected.

2. SUMMARIZED 컬럼이 존재하지 않는 경우
Mach> CREATE TAG TABLE other_tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE);
Executed successfully.

Mach> INSERT INTO other_tag VALUES('tag-0', TO_DATE('2021-08-12'), 10);
Mach> INSERT INTO other_tag VALUES('tag-0', TO_DATE('2021-08-13'), 10);
Mach> INSERT INTO other_tag VALUES('tag-0', TO_DATE('2021-08-14'), 20);
Mach> INSERT INTO other_tag VALUES('tag-0', TO_DATE('2021-08-11'), 5);
Mach> INSERT INTO other_tag VALUES('tag-1', TO_DATE('2022-08-12'), 100);
Mach> INSERT INTO other_tag VALUES('tag-1', TO_DATE('2022-08-11'), 200);
Mach> INSERT INTO other_tag VALUES('tag-1', TO_DATE('2022-08-10'), 50);

Mach> SELECT * FROM v$other_tag_stat;
NAME                                                                              ROW_COUNT            MIN_TIME                        MAX_TIME                        MIN_VALUE
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
MIN_VALUE_TIME                  MAX_VALUE                   MAX_VALUE_TIME                  RECENT_ROW_TIME
---------------------------------------------------------------------------------------------------------------------------------
tag-0                                                                             4                    2021-08-11 00:00:00 000:000:000 2021-08-14 00:00:00 000:000:000 NULL
NULL                            NULL                        NULL                            2021-08-11 00:00:00 000:000:000
tag-1                                                                             3                    2022-08-10 00:00:00 000:000:000 2022-08-12 00:00:00 000:000:000 NULL
NULL                            NULL                        NULL                            2022-08-10 00:00:00 000:000:000
[2] row(s) selected.
```


## RESTful API를 사용한 추출

### RESTful API 준비

다음 속성 값을 지정하고 서버를 시작합니다.

machbase.conf

```
HTTP_ENABLE = 1
HTTP_PORT_NO = 5678
```

RESTful API 호출 규칙

**SELECT 형식**

```bash
{MWA URL}/machiot-rest-api/datapoints/raw/{TagName}/{Start}/{End}/{Direction}/{Count}/{Offset}/

TagName    : Tag 이름. 여러 tag 사용 가능 (','로 구분)
Start, End : 범위, YYYY-MM-DD HH24:MI:SS 또는 YYYY-MM-DD 또는 YYYY-MM-DD HH24:MI:SS,mmm (mmm: 밀리초, 생략시 start는 000, End는 999, micro와 nano는 999)
실제 문자열을 사용할 때는 공백을 제거하기 위해 날짜와 시간 사이에 'T'를 넣습니다.
Direction  : 0(오름차순), 향후 지원 예정 (시간 증가)
Count      : LIMIT, 0이면 전체
Offset     : 오프셋 (기본값 = 0)
```

### CURL을 사용한 단일 tag 데이터 조회 샘플

192.168.0.148에 설치된 machbase에 대해 다음과 같이 호출하면 웹에서 데이터를 조회할 수 있습니다.

**단일 Tag**

```bash
$ curl -G "http://192.168.0.148:5001/machiot-rest-api/v1/datapoints/raw/TAG_0001/2018-01-01T00:00:00/2018-01-06T00:00:00"

{"ErrorCode": 0,
 "ErrorMessage": "",
 "Data": [{"DataType": "DOUBLE",
 "ErrorCode": 0,
 "TagName": "TAG_0001",
 "CalculationMode": "raw",
 "Samples": [{"TimeStamp": "2018-01-01 01:00:00 000:000:000", "Value": 1.0, "Quality": 1},
             {"TimeStamp": "2018-01-02 02:00:00 000:000:000", "Value": 2.0, "Quality": 1},
             {"TimeStamp": "2018-01-03 03:00:00 000:000:000", "Value": 3.0, "Quality": 1},
             {"TimeStamp": "2018-01-04 04:00:00 000:000:000", "Value": 4.0, "Quality": 1},
             {"TimeStamp": "2018-01-05 05:00:00 000:000:000", "Value": 5.0, "Quality": 1}]}]
}
```

### CURL을 사용한 다중 tag 데이터 조회

다음은 두 개의 tag 값을 조회하는 샘플입니다.

```bash
$ curl -G "http://192.168.0.148:5001/machiot-rest-api/datapoints/raw/TAG_0001,TAG_0002/2018-01-05T00:00:00/2018-02-05T00:00:00"
{"ErrorCode": 0,
 "ErrorMessage": "",
 "Data": [{"DataType": "DOUBLE",
           "ErrorCode": 0,
           "TagName": "TAG_0001,TAG_0002",
           "CalculationMode": "raw",
           "Samples": [{"TimeStamp": "2018-01-05 05:00:00 000:000:000", "Value": 5.0, "Quality": 1},
                       {"TimeStamp": "2018-01-06 06:00:00 000:000:000", "Value": 6.0, "Quality": 1},
                       {"TimeStamp": "2018-01-07 07:00:00 000:000:000", "Value": 7.0, "Quality": 1},
                       {"TimeStamp": "2018-01-08 08:00:00 000:000:000", "Value": 8.0, "Quality": 1},
                       {"TimeStamp": "2018-01-09 09:00:00 000:000:000", "Value": 9.0, "Quality": 1},
                       {"TimeStamp": "2018-01-10 10:00:00 000:000:000", "Value": 10.0, "Quality": 1},
                       {"TimeStamp": "2018-02-01 01:00:00 000:000:000", "Value": 11.0, "Quality": 1},
                       {"TimeStamp": "2018-02-02 02:00:00 000:000:000", "Value": 12.0, "Quality": 1},
                       {"TimeStamp": "2018-02-03 03:00:00 000:000:000", "Value": 13.0, "Quality": 1},
                       {"TimeStamp": "2018-02-04 04:00:00 000:000:000", "Value": 14.0, "Quality": 1}
]}]}
```


## 힌트를 사용하여 검색 방향 지정

일반적으로 tag 테이블은 가장 오래된 레코드부터 검색할 수 있습니다. 가장 최근에 삽입된 레코드부터 검색하려면 힌트를 사용하여 검색 방향을 제어할 수 있습니다.

### 정방향 검색

기본값으로, '/*+ SCAN_FORWARD(table_name) */' 힌트를 사용하여 검색합니다.

```bash
Mach> SELECT * FROM tag WHERE t_name='TAG_99' LIMIT 10;
T_NAME                T_TIME                          T_VALUE
--------------------------------------------------------------------------------------
TAG_99                2017-01-01 00:00:49 500:000:000 0
TAG_99                2017-01-01 00:01:39 500:000:000 1
TAG_99                2017-01-01 00:02:29 500:000:000 2
TAG_99                2017-01-01 00:03:19 500:000:000 3
TAG_99                2017-01-01 00:04:09 500:000:000 4
TAG_99                2017-01-01 00:04:59 500:000:000 5
TAG_99                2017-01-01 00:05:49 500:000:000 6
TAG_99                2017-01-01 00:06:39 500:000:000 7
TAG_99                2017-01-01 00:07:29 500:000:000 8
TAG_99                2017-01-01 00:08:19 500:000:000 9
[10] row(s) selected.
Elapsed time: 0.001

Mach> SELECT /*+ SCAN_FORWARD(tag) */  * FROM tag WHERE t_name='TAG_99' LIMIT 10;
T_NAME                T_TIME                          T_VALUE
--------------------------------------------------------------------------------------
TAG_99                2017-01-01 00:00:49 500:000:000 0
TAG_99                2017-01-01 00:01:39 500:000:000 1
TAG_99                2017-01-01 00:02:29 500:000:000 2
TAG_99                2017-01-01 00:03:19 500:000:000 3
TAG_99                2017-01-01 00:04:09 500:000:000 4
TAG_99                2017-01-01 00:04:59 500:000:000 5
TAG_99                2017-01-01 00:05:49 500:000:000 6
TAG_99                2017-01-01 00:06:39 500:000:000 7
TAG_99                2017-01-01 00:07:29 500:000:000 8
TAG_99                2017-01-01 00:08:19 500:000:000 9
[10] row(s) selected.
Elapsed time: 0.001
Mach>
```

### 역방향 검색

'/*+ SCAN_BACKWARD(table_name) */' 힌트를 사용하여 검색합니다.

```bash
Mach> SELECT /*+ SCAN_BACKWARD(tag) */ * FROM tag WHERE t_name='TAG_99' LIMIT 10;
T_NAME                T_TIME                          T_VALUE
--------------------------------------------------------------------------------------
TAG_99                2017-02-27 20:53:19 500:000:000 9
TAG_99                2017-02-27 20:52:29 500:000:000 8
TAG_99                2017-02-27 20:51:39 500:000:000 7
TAG_99                2017-02-27 20:50:49 500:000:000 6
TAG_99                2017-02-27 20:49:59 500:000:000 5
TAG_99                2017-02-27 20:49:09 500:000:000 4
TAG_99                2017-02-27 20:48:19 500:000:000 3
TAG_99                2017-02-27 20:47:29 500:000:000 2
TAG_99                2017-02-27 20:46:39 500:000:000 1
TAG_99                2017-02-27 20:45:49 500:000:000 0
[10] row(s) selected.
Elapsed time: 0.001
Mach>
```

### 기본 스캔 방향 속성 설정

[TABLE_SCAN_DIRECTION](/dbms/config-monitor/property#table_scan_direction) 속성을 사용하여, select 쿼리에 힌트가 없을 때 tag 테이블 스캔 방향을 설정할 수 있습니다.
