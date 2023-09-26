---
title : '태그 데이터의 추출'
type: docs
weight: 20
---

마크베이스는 고속의 태그 데이터 추출 성능을 제공하며, 특히 특정 태그의 시간 범위에 대한 탁월한 성능을 제공한다.

## 샘플 스키마

이후의 샘플은 아래와 같이  TAG 테이블이 생성되고, 두개의 태그를 생성하였다.

각 태그에 대해 각각 2018년 1월 1일부터 2월 10일까지의 데이터를 입력하였다.

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

## 전체 TAG 데이터 추출

```sql
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

위와 같이 특별한 조건이 없으면, 각 시간 순으로 정렬된 태그별로 데이터를 추출할 수 있다.

## 임의 TAG명에 대한 데이터 추출

아래는 TAG 이름이 TAG_0002 인 데이터를 출력하는 예제이다. WHERE 절에 주어진 name에 대한 조건을 설정한다.

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

## 시간 범위에 대한 쿼리

아래는 TAG_0002에 대한 시간 범위를 주고, 데이터를 받아오는 쿼리이다.

> between 절을 활용해서 시간 범위를 주는 것이 일반적인 방법이다. 물론, time을 < 혹은 > 기호로 시간 범위를 입력해도 같은 결과를 얻을 수 있다.

```sql
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

## 다중 태그에 대한 시간 범위 검색

아래는 2개 이상의 태그에 대해서 동일한 시간 범위 데이터를 검색하는 예제이다.

만일 한번의 질의 수행으로 다수의 태그에 대해 한꺼번에 빠른 결과를 받고 싶을 경우에는 아래와 같은 형태의 수행이 바람직하다.

```sql
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

## 특정 값 이상의 태그만 출력하기

간단한 예제이긴 하지만, 태그 값에 대한 조건도 함께 아래와 같이 줄 수 있다.

TAG_0002의 값 중에 12보다 크고, 15보다 작을 것들에 대해 필터링을 수행했다.

```sql
Mach> select * from tag where name = 'TAG_0002' and value > 12 and value < 15 and time between to_date('2018-02-01') and to_date('2018-02-05');
NAME                  TIME                            VALUE                      
--------------------------------------------------------------------------------------
TAG_0002              2018-02-03 03:00:00 000:000:000 13                         
TAG_0002              2018-02-04 04:00:00 000:000:000 14                         
[2] row(s) selected.
```

## 특정 태그 아이디별 통계 정보 출력하기

태그 테이블을 생성하면 기본적으로 태그 테이블의 태그 아이디별 간단한 통계 정보를 수집하는 별도의 가상 테이블이 생성된다.

가상 테이블의 이름은 v${태그테이블 이름}\_stat 의 규칙을 따르게 된다.

해당 테이블을 사용하면 태그 테이블의 통계 정보를 빠르게 얻어올 수 있다.

통계 정보 대상 칼럼은 자동으로 3번째 칼럼이 지정된다.

```sql
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

수집하는 통계 정보는 아래와 같다.

| 컬럼이름|정보|
|--|--|
NAME|태그 아이디의 이름|
ROW_COUNT|Row 개수|
MIN_TIME|해당 태그 아이디 Row 중 가장 작은 Basetime 컬럼 값|
MAX_TIME|해당 태그 아이디 Row 중 가장 큰 Basetime 컬럼 값|
MIN_VALUE|해당 태그 아이디 Row 중 가장 작은 Summarized 컬럼 값|
MIN_VALUE_TIME|MIN_VALUE 값과 같이 입력된 Basetime 컬럼 값|
MAX_VALUE|해당 태그 아이디 Row 중 가장 큰 Summarized 컬럼 값|
MAX_VALUE_TIME|MAX_VALUE 값과 같이 입력된 Basetime 컬럼 값|
RECENT_ROW_TIME|해당 태그 아이디 Row 중 가장 최근에 입력된 Basetime 컬럼 값|

3번째 칼럼에 SUMMARIZED 키워드가 없으면, VALUE 관련 정보(MIN_VALUE, MAX_VALUE, MIN_VALUE_TIME, MAX_VALUE_TIME)는 저장하지 않는다.

조회 예시는 아래와 같다.

```sql
1. SUMMARIZED 칼럼이 존재하는 경우
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
 
2. SUMMARIZED 칼럼이 존재하지 않는 경우
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

## RESTful API를 통한 추출

### RESTful API를 위한 준비 사항

아래 프로퍼티의 값을 지정하고 서버를 시작한다.

machbase.conf

```
HTTP_ENABLE = 1
HTTP_PORT_NO = 5678
```


### RESTful API 호출 규약 

```bash
{MWA URL}/machiot-rest-api/datapoints/raw/{TagName}/{Start}/{End}/{Direction}/{Count}/{Offset}/ 
 
TagName    : Tag Name. 복수의 Tag 지원(,로 구분하여 사용)
Start, End : 기간, YYYY-MM-DD HH24:MI:SS 또는 YYYY-MM-DD 또는 YYYY-MM-DD HH24:MI:SS,mmm (mmm: millisecond, 생략시 start는 000, End는 999이며, 마이크로와 나노도 모두 999임)
실제 스트링으로 지정할 때는 날짜와 시간 사이에 T를 넣어서 빈공간을 없애준다.
Direction  : 0(ascending), 추후 지원 (시간이 증가하는 방향)
Count      : LIMIT, 0이면 전체
Offset     : offset (기본값 = 0)
```

### CURL을 통한 단일 태그 데이터 가져오기 샘플 

아래와 같이 192.168.0.148에 설치된 마크베이스에 대한 호출을 수행하면, 해당 데이터를 웹으로 부터 가져올 수 있다.

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

### CURL을 통한 다중 태그 데이터 가져오기

아래는 두개의 태그에 대한 값을 가져오는 샘플 예제이다.

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

## 힌트(hint)를 이용한 검색 방향 지정하기

태그 테이블은 일반적으로 입력한 순서가 오래된 레코드부터 조회가 가능하다. 가장 최근에 입력한 레코드부터 조회하고 싶을 때에는 힌트를 이용해 조회 방향을 제어할 수 있다.

### 정방향 검색

기본값이며, `/*+ SCAN_FORWARD(table_name) */` 힌트를 추가하여 조회가 가능하다.

```sql
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

`/*+ SCAN_BACKWARD(table_name) */` 힌트를 추가하여 조회가 가능하다.

```sql
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

### 기본 스캔 방향 프로퍼티로 설정

[TABLE_SCAN_DIRECTION](/kr/dbms/config-monitor/property#table_scan_direction)  프로퍼티로 SELECT 문에 힌트가 없을 때 태그 테이블의 스캔 방향을 설정할 수 있다.
