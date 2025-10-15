---
title : 'SELECT'
type: docs
weight: 40
---

## 목차

* [SELECT 구문](#select-구문)
* [집합 연산자](#집합-연산자)
* [대상 목록](#대상-목록)
    * [CASE 문](#case-문)
* [FROM 절](#from-절)
    * [서브쿼리(인라인 뷰)](#서브쿼리인라인-뷰)
    * [조인(INNER JOIN)](#조인inner-join)
    * [INNER JOIN과 OUTER JOIN](#inner-join과-outer-join)
    * [PIVOT](#pivot)
* [WHERE 절](#where-절)
    * [서브쿼리 사용](#서브쿼리-사용)
    * [SEARCH 문](#search-문)
    * [ESEARCH 문](#esearch-문)
    * [NOT SEARCH 문](#not-search-문)
    * [REGEXP 문](#regexp-문)
    * [IN 문](#in-문)
    * [IN 문과 서브쿼리 사용](#in-문과-서브쿼리-사용)
    * [BETWEEN 문](#between-문)
    * [RANGE 문](#range-문)
* [GROUP BY / HAVING](#group-by--having)
* [ORDER BY](#order-by)
* [SERIES BY](#series-by)
* [LIMIT](#limit)
* [DURATION](#duration)
* [데이터 저장](#데이터-저장)


SELECT는 Machbase의 다양한 테이블에서 데이터를 조회, 필터링, 조작하는 데 사용되는 구문입니다.

## SELECT 구문

```sql
select_stmt UNION ALL select_stmt
```

```sql
SELECT target_list FROM table_list
WHERE condition_expr DURATION time_expr
GROUP BY expr ORDER BY expr [DESC] HAVING expr SERIES BY expr
LIMIT n[,n];
```

> 버전 <= 8.0.25에서는 다음 구문을 사용합니다.
> ```sql
> SELECT target_list FROM table_list
> WHERE condition_expr
> GROUP BY expr ORDER BY expr [DESC] HAVING expr SERIES BY expr
> LIMIT n[,n];
> DURATION time_expr
> ```

## 집합 연산자

여러 SELECT 쿼리의 결과를 단일 쿼리 결과로 받고자 할 때 사용합니다. Machbase는 UNION ALL 집합 연산자만 지원합니다. 집합 연산자는 좌측과 우측의 SELECT 문이 (1) 같거나 호환 가능한 타입이고, (2) 쿼리 결과의 개수가 동일한 경우에만 실행할 수 있으며, 두 조건 중 하나라도 일치하지 않으면 에러로 처리됩니다.

데이터 타입 변환 및 호환성 확인은 다음 기준에 따라 수행됩니다.
* 부호 있는 정수 타입과 부호 없는 정수 타입은 호환되지 않습니다.
* 정수 타입은 실수 타입과 호환되며, 쿼리 결과는 실수 타입으로 변환되어 반환됩니다.
* 문자 타입은 다른 길이와 호환됩니다.
* IPv6 타입과 IPv4 타입은 호환되지 않습니다.
* 두 SELECT 문 중 좌측 쿼리의 컬럼명이 항상 사용됩니다.

사용 예

```sql
SELECT i1, i2 FROM table_1
UNION ALL
SELECT c1, c2 FROM table_2
```


## 대상 목록

SELECT 문의 대상이 되는 **컬럼 또는 서브쿼리의 목록**입니다.

대상 목록에 사용되는 서브쿼리는 WHERE 절에 사용되는 서브쿼리와 마찬가지로 두 개 이상의 값이나 두 개 이상의 결과 컬럼을 가지면 에러로 처리됩니다.

```sql
SELECT i1, i2 ...
SELECT i1 (Select avg(c1) FROM t1), i2 ...
```

## CASE 문

```sql
CASE <simple_case_expression|searched_case_expression> [else_clause] END

simple_case_expression ::=
    expr WHEN comparison_expr THEN return_expr
        [WHEN comparison_expr THEN return_expr ...]

searched_case_expression ::=
    WHEN condtion_expr THEN return EXPR [WHEN condtion_expr THEN return EXPR ...]

else_clause ::=
    ELSE else_value_expr
```

일반적인 프로그래밍 언어의 IF ... THEN ... ELSE 블록을 지원하는 표현식입니다. simple_case_expression은 하나의 컬럼 또는 표현식이 when 뒤에 나오는 comparison_expr의 값과 같을 때 return_expr의 형태로 실행되며, 이 when ... then 절은 원하는 만큼 반복할 수 있습니다.

searched_case_expression은 CASE 뒤에 표현식을 지정하지 않고 when 절에 비교 연산자를 포함하는 조건절을 기술합니다. 각 비교 연산의 결과가 true이면 then 절의 값이 반환됩니다. else 절은 when 절의 값이 만족되지 않을 때 (표현식이 NULL인 경우에도) else_value를 반환합니다.

```sql
select * from t1;
I1          I2
---------------------------
2           2
1           1
[2] row(s) selected.

select case i1 when 1 then 100 end from t1;
case i1 when 1 then 100 end
------------------------------
NULL
100
[2] row(s) selected.
```

simple_case_expression 예제에서 i1 컬럼의 값이 2이면 NULL이 반환됩니다.

```
select case when i1 > 0 then 100 when i1 > 1 then 200 end from t1;
case when i1 > 0 then 100 when i1 > 1 then 200 end
------------------------------------------
100
100
[2] row(s) selected.
```

searched_case_expression은 조건을 만족하는 첫 번째 조건을 반환하므로 100이 반환되며, 두 번째 조건은 실행되지 않습니다.


## FROM 절

FROM 절에는 테이블명 또는 인라인 뷰를 지정할 수 있습니다. 테이블 간의 조인을 수행하려면 테이블 또는 인라인 뷰를 쉼표(,)로 구분하여 나열합니다.

```sql
FROM table_name
```

table_name으로 지정된 테이블의 데이터를 조회합니다.

### 서브쿼리(인라인 뷰)

```sql
FROM (Select statement)
```

괄호로 묶인 서브쿼리의 내용에 대한 데이터를 조회합니다.

* Machbase 서버는 상관 서브쿼리를 지원하지 않으므로, 서브쿼리에서 외부 쿼리의 컬럼을 참조할 수 없습니다.

### 조인(INNER JOIN)

```sql
JOIN(INNER JOIN)
```

두 테이블 table_1과 table_2를 조인합니다. 세 개 이상의 테이블이 나열된 경우 INNER JOIN을 사용할 수 있으며, 검색 조건과 조건절은 모두 WHERE 절에 기술합니다.

```sql
SELECT t1.i1, t2.i1 FROM t1, t2 WHERE t1.i1 = t2.i1 AND t1.i1 > 1 AND t2.i2 = 3;
```

### INNER JOIN과 OUTER JOIN

ANSI 스타일 INNER JOIN, LEFT OUTER JOIN, RIGHT OUTER JOIN을 지원합니다. FULL OUTER JOIN은 지원하지 않습니다.

```sql
FROM TABLE_1 [INNER|LEFT OUTER|RIGHT OUTER] JOIN TABLE_2 ON expression
```

ANSI 스타일 JOIN 절의 ON 절은 JOIN에 의해 수행되는 조건절을 사용합니다. OUTER JOIN 쿼리의 WHERE 절에 내부 테이블(ON 절의 조건이 만족되지 않으면 NULL로 채워지는 테이블)에 대한 절이 있으면 쿼리가 INNER JOIN으로 변환됩니다.

```sql
SELECT t1.i1 t2.i1 FROM t1 LEFT OUTER JOIN t2 ON (t1.i1 = t2.i1) WHERE t2.i2 = 1;
```

위 쿼리는 WHERE 절의 t2.i2 = 1 조건에 의해 INNER JOIN으로 변환됩니다.

### PIVOT

* PIVOT 구문은 Machbase 버전 5.6부터 지원됩니다.

**pivot_clause:**

![pivot_clause](/images/sql/select/pivot_clause.png)


PIVOT 문은 GROUP BY 출력의 집계 결과를 ROW로 표시하고 컬럼으로 재배열합니다.

인라인 뷰와 함께 사용되며 다음과 같이 수행됩니다.
* 인라인 뷰의 PIVOT 절에 사용되지 않은 컬럼에 대해 GROUP BY를 수행한 다음, PIVOT IN 절에 나열된 값에 대해 집계 함수를 수행합니다.
* 결과 그룹 컬럼과 집계 결과가 회전되어 컬럼으로 표시됩니다.

예를 들어, 다양한 센서에서 수집된 데이터에서 각 장치의 값을 집계합니다.
CASE 문을 통해 수행해야 하는 쿼리를 PIVOT 문을 통해 간단하게 표현할 수 있습니다.

```sql
-- w/o PIVOT
SELECT * FROM (
    SELECT
             regtime,
             SUM(CASE WHEN tagid = 'FRONT_AXIS_TORQUE' THEN dvalue ELSE 0 END)  AS front_axis_torque,
             SUM(CASE WHEN tagid = 'REAR_AXIS_TORQUE' THEN dvalue ELSE 0 END)  AS rear_axis_torque,
             SUM(CASE WHEN tagid = 'HOIST_AXIS_TORQUE' THEN dvalue ELSE 0 END)  AS hoist_axis_torque,
             SUM(CASE WHEN tagid = 'SLIDE_AXIS_TORQUE' THEN dvalue ELSE 0 END)  AS slide_axis_torque
    FROM     result_d
    WHERE    regtime BETWEEN TO_DATE('2018-12-07 00:00:00') AND TO_DATE('2018-12-08 05:00:00')
    GROUP BY regtime
) WHERE front_axis_torque >= 40 AND rear_axis_torque >= 20;

-- w/ PIVOT
SELECT * FROM (
    SELECT regtime, tagid, dvalue FROM result_d
    WHERE  regtime BETWEEN TO_DATE('2018-12-07 00:00:00') AND TO_DATE('2018-12-08 05:00:00')
) PIVOT (SUM(dvalue) FOR tagid IN ('FRONT_AXIS_TORQUE', 'REAR_AXIS_TORQUE', 'HOIST_AXIS_TORQUE', 'SLIDE_AXIS_TORQUE'))
WHERE front_axis_torque >= 40 AND rear_axis_torque >= 20;

-- Result
regtime                         'FRONT_AXIS_TORQUE'         'REAR_AXIS_TORQUE'          'HOIST_AXIS_TORQUE'         'SLIDE_AXIS_TORQUE'
------------------------------------------------------------------------------------------------------------------------------------------------------
2018-12-07 16:42:29 840:000:000 12158                       7244                        NULL                        NULL
2018-12-07 14:56:26 220:000:000 3308                        663                         NULL                        NULL
2018-12-07 12:20:13 844:000:000 3804                        113                         NULL                        NULL
2018-12-07 11:10:01 957:000:000 8729                        5384                        NULL                        NULL
2018-12-07 17:46:57 812:000:000 7500                        4559                        NULL                        NULL
2018-12-07 14:30:06 138:000:000 5080                        6817                        NULL                        -429
2018-12-07 13:09:20 464:000:000 5233                        1869                        -7253                       NULL
2018-12-07 15:43:03 539:000:000 7491                        4453                        NULL                        NULL
...
```


## WHERE 절

### 서브쿼리 사용

조건문에 서브쿼리를 사용할 수 있습니다. IN 절을 제외한 절에서 서브쿼리가 둘 이상의 레코드를 반환하거나, 서브쿼리에 둘 이상의 결과 컬럼이 있으면 지원되지 않습니다.

```sql
WHERE i1 = (SELECT MAX(c2) FROM T1)
```

조건 연산자의 우측에 괄호로 둘러싸서 서브쿼리를 사용합니다.

* Machbase 서버는 상관 서브쿼리를 지원하지 않으므로, 서브쿼리에서 외부 쿼리의 컬럼을 참조할 수 없습니다.

### SEARCH 문

일반 데이터베이스와 동일한 구문입니다. 단, 키워드 인덱스가 등록되어 있어야 하며, 텍스트 검색을 위한 연산자 키워드로 "SEARCH"를 추가하여 추가 검색 작업이 가능합니다.

```sql
-- drop table realdual;
create table realdual (id1 integer, id2 varchar(20), id3 varchar(20));

create keyword index idx1 on realdual (id2);
create keyword index idx2 on realdual (id3);

insert into realdual values(1, 'time time2', 'series series2');

select * from realdual;

select * from realdual where id2 search 'time';
select * from realdual where id3 search 'series' ;
select * from realdual where id2 search 'time' and id3 search 'series';
```

결과는 다음과 같습니다.

```sql
Mach> create table realdual (id1 integer, id2 varchar(20), id3 varchar(20));
Created successfully.

Mach> create keyword index idx1 on realdual (id2);
Created successfully.

Mach> create keyword index idx2 on realdual (id3);
Created successfully.

Mach> insert into realdual values(1, 'time time2', 'series series2');
1 row(s) inserted.

Mach> select * from realdual;
ID1         ID2                   ID3
------------------------------------------------------------
1           time time2            series series2
[1] row(s) selected.

Mach> select * from realdual where id2 search 'time';
ID1         ID2                   ID3
------------------------------------------------------------
1           time time2            series series2
[1] row(s) selected.

Mach> select * from realdual where id3 search 'series';
ID1         ID2                   ID3
------------------------------------------------------------
1           time time2            series series2
[1] row(s) selected.

Mach> select * from realdual where id2 search 'time' and id3 search 'series';
ID1         ID2                   ID3
------------------------------------------------------------
1           time time2            series series2
[1] row(s) selected.
```

### ESEARCH 문

ESEARCH 문은 ASCII 텍스트에 대한 확장 검색을 가능하게 하는 검색 키워드입니다. 이 확장을 위해 % 문자를 사용하여 원하는 패턴을 검색합니다. Like 연산에서 % 앞에 모든 레코드를 확인하면 ESEARCH의 장점은 이러한 경우에도 단어를 빠르게 찾을 수 있다는 것입니다. 이 기능은 영어 문자열(에러 문자열이나 코드)의 일부를 찾을 때 매우 유용할 수 있습니다.

```sql
-- Example

select id2 from realdual where id2 esearch 'bbb%';
id2
--------------------------------------------
bbb ccc1
aaa bbb1

[2] row(s) selected.

-- 검색 패턴 'bbb%'는 검색 결과에 bbb1도 포함합니다.


select id3 from realdual where id3 esearch '%cd%';
id3
--------------------------------------------
cdf def1
bcd/cdf1ad
abc, bcd1
[3] row(s) selected.

-- % 문자는 검색 패턴의 시작과 끝뿐만 아니라 중간에서도 작동합니다.

select id3 from realdual where id3 esearch '%cd%';
id3
--------------------------------------------
cdf def1
bcd/cdf1ad
abc, bcd1
[3] row(s) selected.
```

### NOT SEARCH 문

NOT SEARCH는 SEARCH 문에서 찾은 레코드 이외의 레코드에 대해 true를 반환하는 문입니다.

NOT ESEARCH는 사용할 수 없습니다.

```sql
create table t1 (id integer, i2 varchar(10));
create keyword index t1_i2 on t1(i2);
insert into t1 values (1, 'aaaa');
insert into t1 values (2, 'bbbb');

select id from t1 where i2 not search 'aaaa';

id
--------------------------------------------
2
[1] row(s) selected.
```

### REGEXP 문

REGEXP 문은 정규 표현식을 사용하여 데이터를 검색하는 데 사용됩니다. 일반적으로 특정 컬럼의 패턴을 정규 표현식을 사용하여 필터링합니다.

유의할 점은 REGEXP 절을 사용할 때 인덱스를 사용할 수 없으므로, 전체 검색 범위를 줄이기 위해 다른 컬럼에 인덱스 조건을 넣어 전체 검색 비용을 낮춰야 합니다.
특정 패턴을 확인하려면 SEARCH 또는 ESEARCH로 인덱스를 사용한 다음, 전체 데이터 수가 적은 상태에서 다시 REGEXP를 사용하면 전체 시스템의 효율성 향상에 도움이 됩니다.

```sql
Mach>
create table realdual (id1 integer, id2 varchar(20), id3 varchar(20));
create table dual (id integer);
insert into dual values(1);
insert into realdual values(1, 'time1', 'series1 series21');
insert into realdual values(1, 'time2', 'series2 series22');
insert into realdual values(1, 'time3', 'series3 series32');


Mach> select * from realdual where id2 REGEXP 'time' ;
ID1         ID2                   ID3
------------------------------------------------------------
1           time3                 series3 series32
1           time2                 series2 series22
1           time1                 series1 series21
[3] row(s) selected.

Mach> select * from realdual where id2 REGEXP 'time[12]' ;
ID1         ID2                   ID3
------------------------------------------------------------
1           time2                 series2 series22
1           time1                 series1 series21
[2] row(s) selected.

Mach> select * from realdual where id2 REGEXP 'time[13]' ;
ID1         ID2                   ID3
------------------------------------------------------------
1           time3                 series3 series32
1           time1                 series1 series21
[2] row(s) selected.

Mach> select * from realdual where id2 regexp 'time[13]' and id3 regexp 'series[12]';
ID1         ID2                   ID3
------------------------------------------------------------
1           time1                 series1 series21
[1] row(s) selected.

Mach> select * from realdual where id2 NOT REGEXP 'time[12]';
ID1         ID2                   ID3
------------------------------------------------------------
1           time3                 series3 series32
[1] row(s) selected.

Mach> SELECT 'abcde' REGEXP 'a[bcd]{1,10}e' from dual;
'abcde' REGEXP 'a[bcd]{1,10}e'
---------------------------------
1
[1] row(s) selected.
```

### IN 문

```sql
column_name IN (value1, value2,...)
```

IN 문은 값 목록에서 만족하면 TRUE를 반환합니다. OR로 연결된 구문과 동일합니다.

### IN 문과 서브쿼리 사용

조건문에서 IN 문의 우측에 서브쿼리를 사용할 수 있습니다. 단, IN 조건의 좌측에 둘 이상의 컬럼을 지정하면 에러로 처리되며, 우측 서브쿼리에서 반환된 결과 집합이 좌측 컬럼 값에 존재하는지 확인합니다.

```sql
WHERE i1 IN (Select c1 from ...)
```

* Machbase 서버는 상관 서브쿼리를 지원하지 않으므로, 서브쿼리에서 외부 쿼리의 컬럼을 참조할 수 없습니다.

### BETWEEN 문

```sql
column_name BETWEEN value1 AND value2
```

BETWEEN 문은 컬럼의 값이 value1과 value2의 범위에 있으면 TRUE를 반환합니다.

### RANGE 문

```sql
column_name RANGE duration_spec;

-- duration_spec : integer (YEAR | WEEK | HOUR | MINUTE | SECOND);
```

주어진 컬럼에 대한 시간 조건을 쉽게 지정할 수 있는 Range 연산자를 제공합니다. Range 연산자는 (BEFORE 키워드로 지정된) 특정 시간을 지정하는 대신, 현재 시간으로부터 시간 범위를 연산 대상으로 지정합니다. 이 연산자를 사용하면 원하는 시간 범위 내의 결과 레코드를 쉽게 조회할 수 있습니다.

```sql
select * from test where id < 2 and c1 range 1 hour;
ID          C1
-----------------------------------------------
1           2014-07-25 09:28:53 706:707:001
[1] row(s) selected.
```


## GROUP BY / HAVING

GROUP BY 절은 SELECT 문의 결과를 특정 컬럼을 기준으로 그룹화하는 데 사용됩니다. 집계 함수를 사용하여 그룹별로 정렬하거나 집계할 때 사용됩니다. 그룹은 GROUP BY 절에 지정된 컬럼에 대해 동일한 컬럼 값을 가진 레코드를 의미합니다. GROUP BY 절 뒤에 HAVING 절을 결합하여 그룹 선택에 대한 조건식을 설정할 수 있습니다. 즉, GROUP BY 절로 구성된 모든 그룹 중 HAVING 절에 지정된 조건식을 만족하는 그룹만 조회됩니다.

```sql
SELECT ...
GROUP BY { col_name | expr } ,...[ HAVING <search_condition> ]

select id1, avg(id2) from exptab where id2 group by id1 order by id1;
id1 컬럼을 기준으로 id2의 평균값을 구합니다.
```


## ORDER BY

ORDER BY 절은 쿼리 결과를 오름차순 또는 내림차순으로 정렬합니다. ASC 또는 DESC와 같은 정렬 옵션을 지정하지 않으면 ORDER BY 절은 기본적으로 오름차순으로 정렬합니다. ORDER BY 절이 지정되지 않으면 조회될 레코드의 순서는 쿼리에 따라 달라집니다.

```sql
SELECT ...
ORDER BY {col_name | expr} [ASC | DESC]

select id1, avg(id2) from exptab where id2 group by id1 order by id1;
id1 컬럼을 기준으로 id2의 평균값을 구합니다.
```


## SERIES BY

SERIES BY 절은 정렬된 결과 집합을 SERIES BY 조건을 만족하는 연속적인 결과 값으로 추출합니다. ORDER BY 절이 지정되지 않으면 _ARRIVAL_TIME 컬럼 값을 사용하여 정렬된 결과를 생성합니다. 따라서 GROUP BY 절을 사용하거나 _ARRIVAL_TIME 컬럼이 없는 volatile 테이블 또는 lookup 테이블에 대한 쿼리인 경우 ORDER BY 절을 사용해야 합니다.

조건절을 만족하는 결과 값은 동일한 SERIESNUM() 함수의 반환 값을 가집니다.

```sql
예를 들어, 다음 데이터에 대해

CREATE TABLE T1 (C1 INTEGER, C2 INTEGER);
INSERT INTO T1 VALUES (0, 1);

INSERT INTO T1 VALUES (1, 2);

INSERT INTO T1 VALUES (2, 3);

INSERT INTO T1 VALUES (3, 2);

INSERT INTO T1 VALUES (4, 1);

INSERT INTO T1 VALUES (5, 2);

INSERT INTO T1 VALUES (6, 3);

INSERT INTO T1 VALUES (7, 1);


다음 쿼리는 다음 출력을 생성합니다:

SELECT C1,C2 FROM T1 ORDER BY C1 SERIES BY C2>1;
C1          C2
---------------------------
1           2
2           3
3           2
5           2
6           3

C2 컬럼의 값이 1보다 큰 경우 C1의 RANGE 값을 알고 싶다면 SERIESNUM 함수로 각 레코드가 어느 그룹에 포함되는지 출력하여 범위를 결정할 수 있습니다.
```


## LIMIT

LIMIT 절은 출력할 레코드 수를 제한하는 데 사용됩니다. 결과 집합의 첫 번째 행부터 마지막 행까지 출력할 정수를 지정할 수 있습니다.

```sql
LIMIT [offset,] row_count

select id1, avg(id2) from exptab where id2 group by id1 order by id1 LIMIT 10;
```


## DURATION

DURATION은 _arrival_time을 기준으로 데이터 조회 범위를 쉽게 결정할 수 있는 키워드입니다. BEFORE 문과 함께 사용하여 특정 시점의 특정 범위의 데이터를 설정합니다. 이 DURATION을 사용하면 검색 성능을 극적으로 높이고 시스템 부하를 극적으로 줄일 수 있습니다. 보다 자세한 사용법은 다음을 참조하십시오.

```sql
DURATION Number TimeSpec [BEFORE/AFTER Number TimeSpec]
TimeSpec : YEAR | MONTH | WEEK |  DAY | HOUR | MINUTE | SECOND
```

```sql
create table t8(i1 integer);
insert into t8 values(1);
insert into t8 values(2);

select i1 from t8;

## Without BEFORE clause
select i1 from t8 duration 2 second;
select i1 from t8 duration 1 minute;
select i1 from t8 duration 1 hour;
select i1 from t8 duration 1 day;
select i1 from t8 duration 1 week;
select i1 from t8 duration 1 month;
select i1 from t8 duration 1 year;

## Using full DURATION statement
select i1 from t8 duration 1 second before 1 day;
select i1 from t8 duration 1 minute before 1 day;
select i1 from t8 duration 1 hour before 1 day;
select i1 from t8 duration 1 day before 1 day;
select i1 from t8 duration 1 week before 1 day;
select i1 from t8 duration 1 month before 1 day;
select i1 from t8 duration 1 year before 1 day;
```

결과는 다음과 같습니다.

```sql
Mach> create table t8(i1 integer);
Created successfully.

Mach> insert into t8 values(1);
1 row(s) inserted.

Mach> insert into t8 values(2);
1 row(s) inserted.

Mach> select i1 from t8;
i1
--------------
2
1
[2] row(s) selected.

## BEFORE 절 없이
Mach> select i1 from t8 duration 2 second;
i1
--------------
2
1
[2] row(s) selected.

Mach> select i1 from t8 duration 1 minute;
i1
--------------
2
1
[2] row(s) selected.

Mach> select i1 from t8 duration 1 hour;
i1
--------------
2
1
[2] row(s) selected.

Mach> select i1 from t8 duration 1 day;
i1
--------------
2
1
[2] row(s) selected.

Mach> select i1 from t8 duration 1 week;
i1
--------------
2
1
[2] row(s) selected.

Mach> select i1 from t8 duration 1 month;
i1
--------------
2
1
[2] row(s) selected.

Mach> select i1 from t8 duration 1 year;
i1
--------------
2
1
[2] row(s) selected.

## Using full DURATION statement
Mach> select i1 from t8 duration 1 second before 1 day;
i1
--------------
[0] row(s) selected.

Mach> select i1 from t8 duration 1 minute before 1 day;
i1
--------------
[0] row(s) selected.

Mach> select i1 from t8 duration 1 hour before 1 day;
i1
--------------
[0] row(s) selected.

Mach> select i1 from t8 duration 1 day before 1 day;
i1
--------------
[0] row(s) selected.

Mach> select i1 from t8 duration 1 week before 1 day;
i1
--------------
[0] row(s) selected.

Mach> select i1 from t8 duration 1 month before 1 day;
i1
--------------
[0] row(s) selected.

Mach> select i1 from t8 duration 1 year before 1 day;
i1
--------------
[0] row(s) selected.
```


## 데이터 저장

쿼리 결과를 CSV 데이터 파일로 직접 저장합니다.

```sql
SAVE DATA INTO 'file_name.csv' [HEADER ON|OFF] [(FIELDS | COLUMNS) [TERMINATED BY 'char'] [ENCLOSED BY 'char']] [ENCODED BY coding_name] AS select query;
```

옵션은 다음과 같습니다.

|옵션|설명|
|--|--|
|HEADER (ON\|OFF)|생성될 csv 파일의 컬럼 구분자와 이스케이프 구분자를 지정합니다.|
|(FIELDS\|COLUMNS) TERMINATED BY 'term_char'<br><br>ENCLOSED BY 'escape_char'|생성될 csv 파일의 첫 줄에 컬럼명을 입력할지 여부를 결정합니다. 기본값은 OFF입니다.|
|ENCODED BY coding_name<br><br>coding_name = ( UTF8, MS949, KSC5601, EUCJP, SHIFTJIS, BIG5, GB231280 )|출력 데이터 파일의 인코딩 형식을 지정합니다. 기본값은 UTF8입니다.|

```sql
SAVE DATA INTO '/tmp/aaa.csv' AS select * from t1;
-- select 문을 실행하고 결과를 '/tmp/aaa.csv' 파일에 csv 형식으로 작성합니다.

SAVE DATA INTO '/tmp/ccc.csv' HEADER ON FIELDS TERMINATED BY ';' ENCLOSED BY '\'' ENCODED BY MS949 AS select * from t1 where i1 > 100;
-- select 문을 실행하고 결과를 /tmp/ccc.csv 파일에 작성합니다. 필드 구분자와 이스케이프 구분자를 각각 지정하고, 저장된 데이터의 인코딩을 MS949로 설정합니다.
```
