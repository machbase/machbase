---
title : '롤업 테이블의 생성 및 조회'
type: docs
weight: 40
---

## ROLLUP 테이블 생성

Tag Table 생성시 Rollup이 기본으로 생성되지 않고, 사용자가 직접 생성하는 방식으로 변경되었으며 문법은 아래와 같다.

![create-rollup](../create-rollup.png)

* rollup name : 생성될 rollup table의 이름 (40자 이내의 문자열로 자유롭게 생성 가능)
* source table name : 생성될 rollup이 데이터를 집계할 source table 이름
* src_table_column : rollup 대상 데이터 칼럼 이름
    * 숫자형 타입의 칼럼만 가능
    * source table이 rollup table인 경우 생략하며, source table의 rollup 대상 칼럼으로 자동 지정
* number sec/min/hour : 집계할 시간 숫자와 시간 단위 <br>
    ex) 1초 단위 집계 : 1 sec <br>
    ex) 30초 단위 집계 : 30 sec <br>
    ex) 1분 단위 집계 : 1 min <br>
    ex) 1시간 단위 집계 : 1 hour <br>

* 제약조건
    * 집계할 source table은 tag table 또는 rollup table만 지정 가능하다.
    * 집계할 source table이 rollup table일 경우 생성될 rollup table의 시간은 source table의 시간보다 크며, 배수어야 한다.

롤업 테이블 생성 예시

```sql
Mach> CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE, strvalue VARCHAR(20));
Executed successfully.
 
-- tag table의 value 칼럼 대상 1초 rollup 생성
Mach> CREATE ROLLUP _tag_rollup_sec ON tag(value) INTERVAL 1 SEC;
  
-- tag table의 value 칼럼 대상 1분 rollup 생성
Mach> CREATE ROLLUP _tag_rollup_min ON tag(value) INTERVAL 1 MIN;
  
-- tag table 대상 1시간 rollup 생성
Mach> CREATE ROLLUP _tag_rollup_hour ON tag(value) INTERVAL 1 HOUR;
  
-- tag table 대상 30초 rollup 생성
Mach> CREATE ROLLUP _tag_rollup_30sec ON tag(value) INTERVAL 30 SEC;
  
-- rollup table(위 30초 rollup) 대상 10분 rollup 생성
Mach> CREATE ROLLUP _tag_rollup_10min ON _tag_rollup_30sec INTERVAL 10 MIN;
 
-- 숫자형 타입이 아닌 칼럼에 대해 rollup 생성 시 에러
Mach> CREATE ROLLUP _tag_rollup_sec ON tag(strvalue) INTERVAL 1 SEC;
[ERR-02671: Invalid type for ROLLUP column (STRVALUE).]
```

### ROLLUP 테이블 자동 생성

`WITH ROLLUP (time_unit)` 키워드를 사용해서 롤업 테이블을 자동으로 생성할 수 있다.
```sql
CREATE TAG TABLE tagtbl (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED) WITH ROLLUP (time_unit)
 
time_unit := {SEC|MIN|HOUR}
```
아래와 같이 time_unit 을 명시 안 해주면 SEC 기준으로 진행된다.
```sql
CREATE TAG TABLE tagtbl (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED) WITH ROLLUP
```

자동으로 생성되는 rollup 의 이름은 다음과 같은 형식으로 생성된다. (`tagtbl` 에 tag tabe name 이 들어간다.)
* _`tagtbl`_ROLLUP_SEC
* _`tagtbl`_ROLLUP_MIN
* _`tagtbl`_ROLLUP_HOUR

```sql
Mach> CREATE TAG TABLE tagtbl (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED) WITH ROLLUP (SEC)
 
Mach> SHOW TABLES;
USER_NAME             DB_NAME                                             TABLE_NAME                                          TABLE_TYPE 
-----------------------------------------------------------------------------------------------------------------------------------------------
SYS                   MACHBASEDB                                          TAGTBL                                              TAGDATA    
SYS                   MACHBASEDB                                          _TAGTBL_DATA_0                                      KEYVALUE   
SYS                   MACHBASEDB                                          _TAGTBL_DATA_1                                      KEYVALUE   
SYS                   MACHBASEDB                                          _TAGTBL_DATA_2                                      KEYVALUE   
SYS                   MACHBASEDB                                          _TAGTBL_DATA_3                                      KEYVALUE   
SYS                   MACHBASEDB                                          _TAGTBL_META                                        LOOKUP     
SYS                   MACHBASEDB                                          _TAGTBL_ROLLUP_HOUR                                 KEYVALUE   
SYS                   MACHBASEDB                                          _TAGTBL_ROLLUP_MIN                                  KEYVALUE   
SYS                   MACHBASEDB                                          _TAGTBL_ROLLUP_SEC                                  KEYVALUE   
[9] row(s) selected.
Elapsed time: 0.001
Mach>
```

time_unit 에 들어간 기준을 가장 작은 기준으로 보고 상위 time unit 까지 자동으로 생성해준다.

> 롤업 테이블 이름 충돌이 발생할시 롤업 테이블 생성은 모두 실패하고 태그 테이블만 생성된다.

### 확장 롤업

Rollup 테이블 생성 구문 마지막에 `EXTENSION` 키워드를 추가하면 확장 롤업을 생성할 수 있다.
확장 Rollup은 해당 구간의 시작 값, 종료 값을 가지고 있다.

```sql
-- 확장 Rollup 테이블 수동 생성
CREATE ROLLUP _tag_rollup_sec ON tag(value) INTERVAL 1 SEC EXTENSION;

-- 확장 Rollup 테이블 자동 생성
CREATE TAG TABLE tagtbl (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED) WITH ROLLUP EXTENSION;
```


## ROLLUP 테이블 시작/중지

rollup 생성시 rollup thread가 자동으로 시작되며, 사용자가 rollup thread를 임의로 시작/중지 가능하다.

```sql

-- 특정 rollup 시작
EXEC ROLLUP_START(rollup_name)
 
-- 특정 rollup 중지
EXEC ROLLUP_STOP(rollup_name)
```

## ROLLUP 테이블 즉시 수집

rollup은 기본적으로 설정된 시간 단위마다 데이터 집계를 시작한다.

* ex) 1시간 단위 rollup이라면 1시간 마다 한번씩 데이터 집계를 하고, 나머지 시간은 대기한다.

사용자가 수동으로 대기 시간을 무시하고 강제로 데이터 집계를 실행할 수 있다.

```sql
-- 특정 rollup 즉시 수집
EXEC ROLLUP_FORCE(rollup_name)
```

## ROLLUP 테이블 삭제

Rollup을 삭제한다.

```sql
DROP ROLLUP rollup_name
```

* rollup_name : 삭제할 rollup 이름
* 제약조건: 삭제할 rollup table을 source table로 참조하고 있는 rollup이 존재할 경우 삭제 할 수 없으며 rollup 간의 의존성이 있는 경우 rollup 을 생성한 역순으로 삭제해야 한다.

```sql
mach> create tag table tag (name varchar(20) primary key, time datetime basetime, value double summarized);
mach> create rollup _tag_rollup_1 on tag(value) interval 1 sec;
mach> create rollup _tag_rollup_2 on _tag_rollup_1 interval 1 min;
mach> create rollup _tag_rollup_3 on _tag_rollup_2 interval 1 hour;
  
위와 같이 생성했을 경우 참조 순서는 아래와 같다.
  
tag -> _tag_rollup_1 -> _tag_rollup_2 -> _tag_rollup_3
  
이 때 tag table이나, 중간에 있는 rollup을 삭제하려고 하면 에러가 발생한다.
  
mach> drop rollup tag
> [ERR-02651: Dependent ROLLUP table exists.]
mach> drop rollup _tag_rollup_1
> [ERR-02651: Dependent ROLLUP table exists.]
  
아래 순서대로 삭제해야 정상적으로 삭제할 수 있다.
  
mach> drop rollup _tag_rollup_3;
mach> drop rollup _tag_rollup_2;
mach> drop rollup _tag_rollup_1;
mach> drop table tag;
```
### TAG 테이블 삭제시 ROLLUP 테이블 같이 삭제
`CASCADE` 키워드를 사용해서 태그 테이블 삭제할 때 태그 테이블에 종속적인 롤업 테이블도 같이 삭제할 수 있다.
```sql
DROP TABLE TAG CASCADE;
```
```sql
Mach> SHOW TABLES;
USER_NAME             DB_NAME                                             TABLE_NAME                                          TABLE_TYPE 
-----------------------------------------------------------------------------------------------------------------------------------------------
SYS                   MACHBASEDB                                          TAGTBL                                              TAGDATA    
SYS                   MACHBASEDB                                          _TAGTBL_DATA_0                                      KEYVALUE   
SYS                   MACHBASEDB                                          _TAGTBL_DATA_1                                      KEYVALUE   
SYS                   MACHBASEDB                                          _TAGTBL_DATA_2                                      KEYVALUE   
SYS                   MACHBASEDB                                          _TAGTBL_DATA_3                                      KEYVALUE   
SYS                   MACHBASEDB                                          _TAGTBL_META                                        LOOKUP     
SYS                   MACHBASEDB                                          _TAGTBL_ROLLUP_HOUR                                 KEYVALUE   
SYS                   MACHBASEDB                                          _TAGTBL_ROLLUP_MIN                                  KEYVALUE   
SYS                   MACHBASEDB                                          _TAGTBL_ROLLUP_SEC                                  KEYVALUE   
[9] row(s) selected.
Elapsed time: 0.001
Mach>

Mach> DROP TABLE tagtbl CASCADE;
Dropped successfully.
 
Mach> show tables;
USER_NAME             DB_NAME                                             TABLE_NAME                                          TABLE_TYPE 
-----------------------------------------------------------------------------------------------------------------------------------------------
[0] row(s) selected.
```

## 조회 문법

```sql
SELECT TIME ROLLUP 3 SECOND, AVG(VALUE) FROM TAG WHERE ...;
```

위와 같이 BASETIME 속성으로 지정된 Datetime 형 컬럼 뒤에 ROLLUP 절을 붙여 지정하면 롤업 테이블 조회가 된다.

```
[BASETIME_COLUMN] ROLLUP [PERIOD] [TIME_UNIT]
```

* BASETIME_COLUMN : BASETIME 속성으로 지정된 TAG 테이블의 Datetime 형 컬럼
* PERIOD : DATE_TRUNC() 함수에서 사용 가능한 시간 단위별 범위를 지정할 수 있다. (아래 참고)
* TIME_UNIT : DATE_TRUNC() 함수에서 사용 가능한 모든 시간 단위를 사용할 수 있다. (아래 참고)

TIME_UNIT 의 선택에 따라, 조회되는 롤업 테이블이 달라진다.

|시간 단위(축약어)|시간 범위| 조회 대상 롤업 테이블|
|--|--|--|
|nanosecond (nsec)|1000000000 (1초)|SECOND|
|microsecond (usec)|60000000 (60초)|SECOND|
|milisecond (msec)|60000 (60초)|SECOND|
|second (sec)|86400 (1일)|SECOND|
|minute (min)|1440 (1일)|MINUTE|
|hour|24 (1일)|HOUR|
|day|1|HOUR|
|month|1|HOUR|
|year|1|HOUR|

ROLLUP 절을 사용하는 것은 롤업 테이블 조회를 직접 하는 것이기 때문에, 집계 함수를 사용하려면 다음의 특징이 있다.

* 숫자형 타입의 컬럼에 집계 함수를 호출해야 한다. 단, 롤업 테이블에서 지원하는 여섯 가지 집계 함수 (SUM, COUNT, MIN, MAX, AVG, SUMSQ) 만 지원한다.
    * 확장 롤업의 경우 (FIRST, LAST)도 추가로 지원한다.
* ROLLUP 하는 BASETIME 컬럼으로 GROUP BY 를 직접 해야 한다.
    * 같은 의미의 ROLLUP 절을 그대로 사용해도 된다.
    * 또는, ROLLUP 절에 별명 (alias) 를 붙이고, 별명으로 GROUP BY 에 작성해도 된다.

```sql
SELECT   time rollup 3 sec mtime, avg(value)
FROM     TAG
GROUP BY time rollup 3 sec mtime;
 
-- 또는
SELECT   time rollup 3 sec mtime, avg(value)
FROM     TAG
GROUP BY mtime;
```

## 데이터 샘플

아래는 롤업 테스트를 위한 샘플 데이터이다.

```sql
create tag table TAG (name varchar(20) primary key, time datetime basetime, value double summarized) with rollup extension;
 
insert into tag metadata values ('TAG_0001');
 
insert into tag values('TAG_0001', '2018-01-01 01:00:01 000:000:000', 1);
insert into tag values('TAG_0001', '2018-01-01 01:00:02 000:000:000', 2);
insert into tag values('TAG_0001', '2018-01-01 01:01:01 000:000:000', 3);
insert into tag values('TAG_0001', '2018-01-01 01:01:02 000:000:000', 4);
insert into tag values('TAG_0001', '2018-01-01 01:02:01 000:000:000', 5);
insert into tag values('TAG_0001', '2018-01-01 01:02:02 000:000:000', 6);
 
insert into tag values('TAG_0001', '2018-01-01 02:00:01 000:000:000', 1);
insert into tag values('TAG_0001', '2018-01-01 02:00:02 000:000:000', 2);
insert into tag values('TAG_0001', '2018-01-01 02:01:01 000:000:000', 3);
insert into tag values('TAG_0001', '2018-01-01 02:01:02 000:000:000', 4);
insert into tag values('TAG_0001', '2018-01-01 02:02:01 000:000:000', 5);
insert into tag values('TAG_0001', '2018-01-01 02:02:02 000:000:000', 6);
 
insert into tag values('TAG_0001', '2018-01-01 03:00:01 000:000:000', 1);
insert into tag values('TAG_0001', '2018-01-01 03:00:02 000:000:000', 2);
insert into tag values('TAG_0001', '2018-01-01 03:01:01 000:000:000', 3);
insert into tag values('TAG_0001', '2018-01-01 03:01:02 000:000:000', 4);
insert into tag values('TAG_0001', '2018-01-01 03:02:01 000:000:000', 5);
insert into tag values('TAG_0001', '2018-01-01 03:02:02 000:000:000', 6);
```

태그 하나에 대해서 3시간 동안 초단위의 각기 다른 값을 입력해 놓았다.


## ROLLUP 평균값 얻기

아래는 해당 태그에 대해 초, 분, 시 단위의 평균값을 얻는 예제이다.

```sql
Mach> SELECT time rollup 1 sec mtime, avg(value) FROM TAG WHERE name = 'TAG_0001' group by mtime order by mtime;
mtime                           avg(value)
---------------------------------------------------------------
2018-01-01 01:00:01 000:000:000 1
2018-01-01 01:00:02 000:000:000 2
2018-01-01 01:01:01 000:000:000 3
2018-01-01 01:01:02 000:000:000 4
2018-01-01 01:02:01 000:000:000 5
2018-01-01 01:02:02 000:000:000 6
2018-01-01 02:00:01 000:000:000 1
2018-01-01 02:00:02 000:000:000 2
2018-01-01 02:01:01 000:000:000 3
2018-01-01 02:01:02 000:000:000 4
2018-01-01 02:02:01 000:000:000 5
2018-01-01 02:02:02 000:000:000 6
2018-01-01 03:00:01 000:000:000 1
2018-01-01 03:00:02 000:000:000 2
2018-01-01 03:01:01 000:000:000 3
2018-01-01 03:01:02 000:000:000 4
2018-01-01 03:02:01 000:000:000 5
2018-01-01 03:02:02 000:000:000 6
[18] row(s) selected.
 
Mach> SELECT time rollup 1 min mtime, avg(value) FROM TAG WHERE name = 'TAG_0001' group by mtime order by mtime;
mtime                           avg(value)
---------------------------------------------------------------
2018-01-01 01:00:00 000:000:000 1.5
2018-01-01 01:01:00 000:000:000 3.5
2018-01-01 01:02:00 000:000:000 5.5
2018-01-01 02:00:00 000:000:000 1.5
2018-01-01 02:01:00 000:000:000 3.5
2018-01-01 02:02:00 000:000:000 5.5
2018-01-01 03:00:00 000:000:000 1.5
2018-01-01 03:01:00 000:000:000 3.5
2018-01-01 03:02:00 000:000:000 5.5
[9] row(s) selected.
 
Mach> SELECT time rollup 1 hour mtime, avg(value) FROM TAG WHERE name = 'TAG_0001' group by mtime order by mtime;
mtime                           avg(value)
---------------------------------------------------------------
2018-01-01 01:00:00 000:000:000 3.5
2018-01-01 02:00:00 000:000:000 3.5
2018-01-01 03:00:00 000:000:000 3.5
[3] row(s) selected.
```

## ROLLUP 최소/최대값 얻기

아래는 해당 태그의 시간 범위에 따른 최소/최대값을 얻는 예제를 나타낸다. 이전 예제와 다른 점은, 쿼리 한 번에 최대값과 최소값을 동시에 얻을 수 있다는 것이다.

```sql
Mach> SELECT time rollup 1 hour mtime, min(value), max(value) FROM TAG WHERE name = 'TAG_0001' group by mtime order by mtime;
mtime                           min(value)                  max(value)
--------------------------------------------------------------------------------------------
2018-01-01 01:00:00 000:000:000 1                           6
2018-01-01 02:00:00 000:000:000 1                           6
2018-01-01 03:00:00 000:000:000 1                           6
[3] row(s) selected.
 
Mach> SELECT time rollup 1 min mtime, min(value), max(value) FROM TAG WHERE name = 'TAG_0001' group by mtime order by mtime;
mtime                           min(value)                  max(value)
--------------------------------------------------------------------------------------------
2018-01-01 01:00:00 000:000:000 1                           2
2018-01-01 01:01:00 000:000:000 3                           4
2018-01-01 01:02:00 000:000:000 5                           6
2018-01-01 02:00:00 000:000:000 1                           2
2018-01-01 02:01:00 000:000:000 3                           4
2018-01-01 02:02:00 000:000:000 5                           6
2018-01-01 03:00:00 000:000:000 1                           2
2018-01-01 03:01:00 000:000:000 3                           4
2018-01-01 03:02:00 000:000:000 5                           6
[9] row(s) selected.
```

## ROLLUP 합계/개수 얻기

아래는 합계 및 데이터 개수 값을 얻는 예제이다. 역시 하나의 쿼리에 합계와 개수를 얻을 수 있다.

```sql
Mach> SELECT time rollup 1 min  mtime, sum(value), count(value) FROM TAG WHERE name = 'TAG_0001' group by mtime order by mtime;
mtime                           sum(value)                  count(value)
-------------------------------------------------------------------------------------
2018-01-01 01:00:00 000:000:000 3                           2
2018-01-01 01:01:00 000:000:000 7                           2
2018-01-01 01:02:00 000:000:000 11                          2
2018-01-01 02:00:00 000:000:000 3                           2
2018-01-01 02:01:00 000:000:000 7                           2
2018-01-01 02:02:00 000:000:000 11                          2
2018-01-01 03:00:00 000:000:000 3                           2
2018-01-01 03:01:00 000:000:000 7                           2
2018-01-01 03:02:00 000:000:000 11                          2
[9] row(s) selected.
```

## ROLLUP 제곱합 얻기

아래는 제곱합 값을 얻는 예제이다.

```sql
Mach> SELECT time ROLLUP 1 SEC mtime, SUMSQ(value) FROM tag GROUP BY mtime ORDER BY mtime;
mtime                           SUMSQ(value)               
---------------------------------------------------------------
2018-01-01 01:00:01 000:000:000 1                          
2018-01-01 01:00:02 000:000:000 4                          
2018-01-01 01:01:01 000:000:000 9                          
2018-01-01 01:01:02 000:000:000 16                         
2018-01-01 01:02:01 000:000:000 25                         
2018-01-01 01:02:02 000:000:000 36                         
2018-01-01 02:00:01 000:000:000 1                          
2018-01-01 02:00:02 000:000:000 4                          
2018-01-01 02:01:01 000:000:000 9                          
2018-01-01 02:01:02 000:000:000 16                         
2018-01-01 02:02:01 000:000:000 25                         
2018-01-01 02:02:02 000:000:000 36                         
2018-01-01 03:00:01 000:000:000 1                          
2018-01-01 03:00:02 000:000:000 4                          
2018-01-01 03:01:01 000:000:000 9                          
2018-01-01 03:01:02 000:000:000 16                         
2018-01-01 03:02:01 000:000:000 25                         
2018-01-01 03:02:02 000:000:000 36                         
[18] row(s) selected.
 
Mach> SELECT time ROLLUP 1 MIN mtime, SUMSQ(value) FROM tag GROUP BY mtime ORDER BY mtime;
mtime                           SUMSQ(value)               
---------------------------------------------------------------
2018-01-01 01:00:00 000:000:000 5                          
2018-01-01 01:01:00 000:000:000 25                         
2018-01-01 01:02:00 000:000:000 61                         
2018-01-01 02:00:00 000:000:000 5                          
2018-01-01 02:01:00 000:000:000 25                         
2018-01-01 02:02:00 000:000:000 61                         
2018-01-01 03:00:00 000:000:000 5                          
2018-01-01 03:01:00 000:000:000 25                         
2018-01-01 03:02:00 000:000:000 61                         
[9] row(s) selected.
```

## ROLLUP 시작/종료 값 얻기

아래는 확장 롤업에서 제공하는 시작 및 종료 값을 얻는 예제이다.

```sql
Mach> SELECT time ROLLUP 1 MIN mtime, FIRST(time, value), LAST(time, value) FROM tag GROUP BY mtime ORDER BY mtime;
mtime                           FIRST(time, value)          LAST(time, value)           
--------------------------------------------------------------------------------------------
2018-01-01 01:00:00 000:000:000 1                           2                           
2018-01-01 01:01:00 000:000:000 3                           4                           
2018-01-01 01:02:00 000:000:000 5                           6                           
2018-01-01 02:00:00 000:000:000 1                           2                           
2018-01-01 02:01:00 000:000:000 3                           4                           
2018-01-01 02:02:00 000:000:000 5                           6                           
2018-01-01 03:00:00 000:000:000 1                           2                           
2018-01-01 03:01:00 000:000:000 3                           4                           
2018-01-01 03:02:00 000:000:000 5                           6                           
[9] row(s) selected.

Mach> SELECT time ROLLUP 1 HOUR mtime, FIRST(time, value), LAST(time, value) FROM tag GROUP BY mtime ORDER BY mtime;
mtime                           FIRST(time, value)          LAST(time, value)           
--------------------------------------------------------------------------------------------
2018-01-01 01:00:00 000:000:000 1                           6                           
2018-01-01 02:00:00 000:000:000 1                           6                           
2018-01-01 03:00:00 000:000:000 1                           6                           
[3] row(s) selected.
```

## 다양한 시간 간격으로 그룹화

ROLLUP 절의 장점은, DATE_TRUNC() 를 의도적으로 사용해서 시간 간격을 다변화할 필요가 없다는 것이다.

3초 간격의 합계와 데이터 개수를 얻으려면 아래와 같이 하면 된다.
예제 시간 범위가 0초, 1초, 2초 뿐이라 전부 0초로 수렴된 것을 확인할 수 있다. 결과적으로는 '분 단위 롤업' 조회 결과와 일치한다.

```sql
Mach> SELECT time rollup 3 sec  mtime, sum(value), count(value) FROM TAG WHERE name = 'TAG_0001' GROUP BY mtime ORDER BY mtime;
mtime                           sum(value)                  count(value)
-------------------------------------------------------------------------------------
2018-01-01 01:00:00 000:000:000 3                           2
2018-01-01 01:01:00 000:000:000 7                           2
2018-01-01 01:02:00 000:000:000 11                          2
2018-01-01 02:00:00 000:000:000 3                           2
2018-01-01 02:01:00 000:000:000 7                           2
2018-01-01 02:02:00 000:000:000 11                          2
2018-01-01 03:00:00 000:000:000 3                           2
2018-01-01 03:01:00 000:000:000 7                           2
2018-01-01 03:02:00 000:000:000 11                          2
```

## JSON 타입 대상의 ROLLUP 활용

7.5 버전부터 JSON 타입을 대상으로 ROLLUP을 사용할 수 있다.

생성 구문에 JSON PATH를 OPERATOR와 연결하면 된다.

JSON 타입 특성상, 하나의 JSON 칼럼에 PATH 별로 ROLLUP을 생성할 수 있다.

```sql
-- create tag table
CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, jval JSON);
 
-- insert data
insert into tag values ('tag-01', '2022-09-01 01:01:01', "{ \"x\": 1, \"y\": 1.1}");
insert into tag values ('tag-01', '2022-09-01 01:01:02', "{ \"x\": 2, \"y\": 1.2}");
insert into tag values ('tag-01', '2022-09-01 01:01:03', "{ \"x\": 3, \"y\": 1.3}");
insert into tag values ('tag-01', '2022-09-01 01:01:04', "{ \"x\": 4, \"y\": 1.4}");
insert into tag values ('tag-01', '2022-09-01 01:01:05', "{ \"x\": 5, \"y\": 1.5}");
insert into tag values ('tag-01', '2022-09-01 01:02:00', "{ \"x\": 6, \"y\": 1.6}");
insert into tag values ('tag-01', '2022-09-01 01:03:00', "{ \"x\": 7, \"y\": 1.7}");
insert into tag values ('tag-01', '2022-09-01 01:04:00', "{ \"x\": 8, \"y\": 1.8}");
insert into tag values ('tag-01', '2022-09-01 01:05:00', "{ \"x\": 9, \"y\": 1.9}");
insert into tag values ('tag-01', '2022-09-01 01:06:00', "{ \"x\": 10, \"y\": 2.0}");
 
-- create rollup
CREATE ROLLUP _tag_rollup_jval_x_sec ON tag(jval->'$.x') INTERVAL 1 SEC;
CREATE ROLLUP _tag_rollup_jval_y_sec ON tag(jval->'$.y') INTERVAL 1 SEC;
```

ROLLUP 조회도 동일하게 사용하면 된다.

```sql
Mach> SELECT time ROLLUP 2 SEC mtime, MIN(jval->'$.x'), MAX(jval->'$.x'), SUM(jval->'$.x'), COUNT(jval->'$.x'), SUMSQ(jval->'$.x') FROM tag GROUP BY mtime ORDER BY mtime;
mtime                           min(jval->'$.x')            max(jval->'$.x')            sum(jval->'$.x')            count(jval->'$.x')   sumsq(jval->'$.x')         
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
2022-09-01 01:01:00 000:000:000 1                           1                           1                           1                    1                          
2022-09-01 01:01:02 000:000:000 2                           3                           5                           2                    13                         
2022-09-01 01:01:04 000:000:000 4                           5                           9                           2                    41                         
2022-09-01 01:02:00 000:000:000 6                           6                           6                           1                    36                         
2022-09-01 01:03:00 000:000:000 7                           7                           7                           1                    49                         
2022-09-01 01:04:00 000:000:000 8                           8                           8                           1                    64                         
2022-09-01 01:05:00 000:000:000 9                           9                           9                           1                    81                         
2022-09-01 01:06:00 000:000:000 10                          10                          10                          1                    100                        
[8] row(s) selected.
 
Mach> SELECT time ROLLUP 2 SEC mtime, MIN(jval->'$.y'), MAX(jval->'$.y'), SUM(jval->'$.y'), COUNT(jval->'$.y'), SUMSQ(jval->'$.y') FROM tag GROUP BY mtime ORDER BY mtime
mtime                           min(jval->'$.y')            max(jval->'$.y')            sum(jval->'$.y')            count(jval->'$.y')   sumsq(jval->'$.y')         
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
2022-09-01 01:01:00 000:000:000 1.1                         1.1                         1.1                         1                    1.21                       
2022-09-01 01:01:02 000:000:000 1.2                         1.3                         2.5                         2                    3.13                       
2022-09-01 01:01:04 000:000:000 1.4                         1.5                         2.9                         2                    4.21                       
2022-09-01 01:02:00 000:000:000 1.6                         1.6                         1.6                         1                    2.56                       
2022-09-01 01:03:00 000:000:000 1.7                         1.7                         1.7                         1                    2.89                       
2022-09-01 01:04:00 000:000:000 1.8                         1.8                         1.8                         1                    3.24                       
2022-09-01 01:05:00 000:000:000 1.9                         1.9                         1.9                         1                    3.61                       
2022-09-01 01:06:00 000:000:000 2                           2                           2                           1                    4                          
[8] row(s) selected.
```
