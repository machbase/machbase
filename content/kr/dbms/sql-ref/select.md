---
title : 'SELECT'
type: docs
weight: 40
---

SELECT는 마크베이스에서 각종 테이블로부터 데이터를 찾거나 필터링 및 조작하는 데 사용되는 구문이다.

## SELECT Syntax

```sql
select_stmt UNION ALL select_stmt
```
```sql
SELECT target_list FROM TableList WHERE Condition GROUP BY Expr ORDER BY Expr [Desc] HAVING Expr SERIES BY Expr LIMIT N[,N] DURATION TimeExpr;
```

## SET OPERATOR

여러 개의 Select문의 결과를 하나의 질의 결과로 전달받을 경우에 사용한다. 마크베이스는 UNION ALL 집합 연산자만을 지원한다. 집합 연산자는 좌우에 기술된 Select문이 (1) 같거나 호환가능한 타입이며 (2) 질의 결과값의 개수가 동일한 경우에만 실행이 가능하며 두 조건 중 하나라도 일치하지 않은 경우에는 오류로 처리된다.

다음의 기준으로 데이터 타입 변환이나 호환성 검증을 수행한다.
* 부호 있는 정수형 타입과 부호 없는 정수형 타입은 호환이 되지 않는다.
* 정수형 타입은 실수형 타입과 호환이 되며 질의 결과는 실수형 타입으로 변환되어 반환된다.
* 문자형 타입은 길이가 달라도 호환이 된다.
* IPv6 타입과 IPv4 타입은 호환이 되지 않는다.
* 두 개의 SELECT 문 중 항상 왼쪽 질의의 컬럼명이 사용된다.

실행 예제
```sql
SELECT i1, i2 FROM table_1
UNION ALL
SELECT c1, c2 FROM table_2
```

## TARGET LIST

Select 문이 대상으로 하는 컬럼 또는 Subquery 의 리스트이다.

Target list에 사용된 Subquery는 WHERE 조건절에서 사용되는 Subquery와 같이 두 개 이상의 값을 갖거나 두 개 이상의 결과 컬럼을 갖는 경우에는 오류로 처리된다.

```sql
SELECT i1, i2 ...
SELECT i1 (Select avg(c1) FROM t1), i2 ...
```

## CASE 구문

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

일반적인 프로그램 언어의 IF... THEN... ELSE블록을 지원하는 표현식이다. simple_case_expression은 하나의 컬럼이나 표현식이 when 뒤에 오는 comparison_expr 값과 같은 경우 return_expr을 반환하는 형태로 수행되며 이 when ... then 절은 원하는 만큼 반복하여 기술할 수 있다.

searched_case_expression은 CASE 이후에 표현식을 지정하지 않고 when절에 비교연산자를 포함한 조건절을 기술한다. 각 비교연산의 결과가 참이면 then 절의 값을 반환한다. else 절은 when 절들의 값이 만족하지 않을 경우(expression 결과가 NULL인 경우에도) else_value를 반환한다.

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

simple_case_expression의 예제에서 i1 컬럼의 값이 2인 경우에 해당하는 값이 없으면 NULL을 반환한다.

```sql
select case when i1 > 0 then 100 when i1 > 1 then 200 end from t1;
case when i1 > 0 then 100 when i1 > 1 then 200 end
------------------------------------------
100        
100        
[2] row(s) selected.
```

searched_case_expression에서 만족하는 첫 번째 조건절을 반환하므로 첫 번째 조건절의 반환값인 100이 반환되며 두 번째 조건절은 실행이 되지 않는다.

## FROM

FROM 절에는 테이블 이름이나 Inline view를 지정할 수 있다. 테이블 간의 Join을 수행하려면 테이블 혹은 Inline view를 쉼표(,)로 구분해서 나열한다.

```sql
FROM table_name
```

table_name로 지정한 테이블 내의 데이터를 검색한다.

### SUBQUERY(INLINE VIEW) 사용

```sql
FROM (Select statement)
```

괄호로 둘려쳐진 subquery의 내용에 대하여 데이터를 검색한다.

* 마크베이스 서버는 correlated subquery를 지원하지 않으므로 outer query에서 subquery 내의 column을 참조할 수 없다.

### JOIN(INNER JOIN)

```sql
FROM TABLE_1, TABLE_2
```

두 개의 테이블 table_1 과 table_2를 JOIN한다. INNER JOIN은 테이블이 3개 이상 나열될 때에도 사용이 가능하며 WHERE 절에 검색 조건절과 JOIN 조건절을 모두 기술하여 사용한다.

```sql
SELECT t1.i1, t2.i1 FROM t1, t2 WHERE t1.i1 = t2.i1 AND t1.i1 > 1 AND t2.i2 = 3;
```

### INNER JOIN 및 OUTER JOIN

ANSI 스타일의 INNER JOIN, LEFT OUTER JOIN, RIGHT OUTER JOIN을 지원한다. FULL OUTER JOIN은 지원하지 않는다.

```sql
FROM TABLE_1 [INNER|LEFT OUTER|RIGHT OUTER] JOIN TABLE_2 ON expression
```

ANSI 스타일 JOIN절의 ON절에는 JOIN에서 수행하는 조건절을 사용한다. OUTER JOIN 질의에서 where절에 Inner table(ON 절의 조건을 만족하지 않으면 NULL이 채워지는 테이블)에 대한 조건절이 있는 경우, 해당 질의는 INNER JOIN으로 변환된다.

```sql
SELECT t1.i1 t2.i1 FROM t1 LEFT OUTER JOIN t2 ON (t1.i1 = t2.i1) WHERE t2.i2 = 1;
```

위 질의는 WHERE 절의 조건 t2.i2 = 1에 의하여 INNER JOIN으로 변환된다.

### PIVOT

* PIVOT 구문은 마크베이스 5.5.6 버전부터 지원한다.

**pivot_clause:**

![pivot](../select_image/pivot_clause.png)


PIVOT 구문은 ROW로 출력되는 GROUP BY에 대한 집계 결과를 컬럼으로 재배열하여 보여준다.

Inline view와 함께 사용되며 다음과 같이 수행된다.

* Inline view의 결과 컬럼 중 PIVOT 절에 사용되지 않은 컬럼으로 GROUP BY를 수행한 후 PIVOT IN 절에 나열된 값 별로 집계함수를 수행한다.
* 결과로 나온 grouping 컬럼과 집계 결과를 회전하여 컬럼으로 보여준다.

예) 여러 센서로부터 수집된 데이터에서 각 device 별로 value 값을 집계해서 출력하라.

CASE 구문을 통해 수행해야하는 질의를 PIVOT 구문을 통해 간단히 표현할 수 있다.

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

## WHERE

### SUBQUERY의 사용

조건절에 대해서 subquery의 사용이 가능하다. IN 구문을 제외한 조건절에서 subquery가 두 개 이상의 레코드를 리턴하거나, subquery의 결과 컬럼이 두 개 이상인 경우는 지원하지 않는다.

```sql
WHERE i1 = (SELECT MAX(c2) FROM T1)
```

subquery를 조건연산자 오른쪽에 괄호를 둘러쳐서 사용한다.

* 마크베이스 서버는 correlated subquery를 지원하지 않으므로 outer query에서 subquery 내의 column을 
참조할 수 없다.

### SEARCH 구문

일반 데이터베이스와의 문법이 동일하다. 단, 반드시 keyword index를 등록해야 하며, 텍스트 검색을 위한 연산자 키워드인 "SEARCH"를 추가하여, 부가적인 검색 연산이 가능하다.

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

수행 결과는 다음과 같다.

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

### ESEARCH 구문

ESEARCH 구문은 ASCII 문자 텍스트에 대한 확장 검색을 가능하게 해주는 검색 키워드이다. 이러한 확장을 위해 % 문자를 이용하여 원하는 패턴의 검색을 수행한다. 이 Like 연산에서 앞에 %가 오는 경우 모든 레코드를 검사해야 하지만, ESEARCH의 장점은 이 경우에도 빠르게 해당 단어를 찾을 수 있다는 데 있다. 이 기능은 영문 문자열(에러 문자열 혹은 코드)의 일부를 찾을 때 매우 유용하게 사용할 수 있다.

```sql

예제
 
select id2 from realdual where id2 esearch 'bbb%';
id2
--------------------------------------------
bbb ccc1
aaa bbb1
 
[2] row(s) selected.
 
검색 pattern 'bbb%'에 의하여 bbb1도 검색 결과에 포함된다.
 
 
select id3 from realdual where id3 esearch '%cd%';
id3
--------------------------------------------
cdf def1
bcd/cdf1ad
abc, bcd1
[3] row(s) selected.
 
% 문자는 검색 pattern의 처음, 끝 뿐만 아니라 가운데에 있어도 동작한다.
 
select id3 from realdual where id3 esearch '%cd%';
id3
--------------------------------------------
cdf def1
bcd/cdf1ad
abc, bcd1
[3] row(s) selected.
```

### NOT SEARCH 구문

NOT SEARCH는 SEARCH구문에서 검색되는 조건 이외의 레코드들에 대해서 참을 리턴하는 구문이다.

NOT ESEARCH는 사용할 수 없다.

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

### REGEXP 구문

REGEXP 구문은 정규표현식을 사용하여 데이터에 대한 검색을 수행하는데 사용된다. 일반적으로 특정 컬럼의 패턴을 정규표현식을 사용하여 데이터를 필터링하게 된다.

한가지 주의할 점은 REGEXP 구문을 사용할 경우 인덱스를 활용할 수 없기 때문에 전체 검색 범위를 줄이기 위해 반드시 다른 컬럼에 대한 인덱스 조건을 넣어서 전체적인 검색 비용을 낮춰야 한다.

특정 패턴을 검사하고자 할 때에는 SEARCH 혹은 ESEARCH를 통해 인덱스를 활용하도록 하고, 이를 통해 전체적인 데이터 건수가 작아진 상태에서 다시 REGEXP를 이용하는 것이 시스템 전체 효율 향상에 도움이 된다

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

### IN 구문

```sql
column_name IN (value1, value2,...)
```

IN 구문은 뒤의 value 리스트에서 만족할 경우 TRUE를 리턴한다. OR로 연결된 구문과 동일하다.

### IN 구문과 SUBQUERY의 사용

조건절의 IN 구문의 오른쪽에 subquery를 사용할 수 있다. 단, IN 조건절의 왼쪽에는 컬럼 두 개 이상의 컬럼을 지정하면 오류로 처리하고 오른쪽의 subquery에서 리턴되는 결과 집합이 왼쪽 컬럼값에 존재하는지를 검사한다.

```sql
WHERE i1 IN (Select c1 from ...)
```

* 마크베이스 서버는 correlated subquery를 지원하지 않으므로 outer query에서 subquery 내의 column을 참조할 수 없다.

### BETWEEN 구문

```sql
column_name BETWEEN value1 AND value2
```

BETWEEN 구문은 column의 값이 value1과 value2 범위에 있을 경우, TRUE를 리턴한다.

### RANGE 구문

```sql
column_name RANGE duration_spec;

-- duration_spec : integer (YEAR | WEEK | HOUR | MINUTE | SECOND);
```

지정된 컬럼에 대해 시간 조건절을 쉽게 지정하는 Range 연산자를 제공한다. Range 연산자는 (BEFORE 키워드로 지정하는 것처럼) 특정 시점을 지정하는 게 아니라 현재 시점부터의 시간 범위를 연산의 대상 조건으로 지정한다. 이 연산자를 사용하면 손쉽게 원하는 시간 범위 내의 결과 레코드들을 검색할 수 있다.

```sql
select * from test where id < 2 and c1 range 1 hour;
ID          C1                             
-----------------------------------------------
1           2014-07-25 09:28:53 706:707:001
[1] row(s) selected.
```

## GROUP BY / HAVING

GROUP BY 절은 SELECT 문으로 검색한 결과를 특정 컬럼을 기준으로 그룹화하기 위해 사용하며, 그룹별로 정렬을 수행하거나 집계 함수를 사용하여 그룹별 집계를 구할 때 사용한다. 그룹이란 GROUP BY 절에 명시된 컬럼에 대해 동일한 컬럼 값을 가지는 레코드들을 의미한다.

GROUP BY 절 뒤에 HAVING 절을 결합하여 그룹 선택을 위한 조건식을 설정할 수 있다. 즉, GROUP BY 절로 구성되는 모든 그룹 중 HAVING 절에 명시된 조건식을 만족하는 그룹만 조회한다.

```sql
SELECT ...
GROUP BY { col_name | expr } ,...[ HAVING <search_condition> ]
 
select id1, avg(id2) from exptab where id2 group by id1 order by id1;
id1 컬럼을 기준으로 id2의 평균값을 구한다.
```

## ORDER BY
ORDER BY 절은 질의 결과를 오름차순 또는 내림차순으로 정렬하며, ASC 또는 DESC와 같은 정렬 옵션을 명시하지 않으면 디폴트로 오름차순으로 정렬한다. ORDER BY 절을 지정하지 않으면, 조회되는 레코드의 순서는 질의에 따라 다르다.

```sql
SELECT ...
ORDER BY {col_name | expr} [ASC | DESC]
 
select id1, avg(id2) from exptab where id2 group by id1 order by id1;
id1 컬럼을 기준으로 id2의 평균값을 구한다.
```

## SERIES BY

SERIES BY 절은 정렬된 결과집합을 SERIES BY 조건절을 만족하는 연속된 결과값들로 추출한다. 만약 ORDER BY 절이 지정되지 않은 경우에는 _ARRIVAL_TIME 컬럼값을 이용하여 정렬된 결과를 생성하므로, _ARRIVAL_TIME 컬럼이 없는 휘발성 테이블이나 참조 테이블에 대한 질의나, GROUP BY 절을 이용하는 경우에는 반드시 ORDER BY 절을 이용해야 한다.

조건절을 만족하는 결과값들은 같은 SERIESNUM() 함수의 반환값을 갖게 된다.

```sql
예를 들어 다음의 데이터에 대해서
CREATE TABLE T1 (C1 INTEGER, C2 INTEGER);
INSERT INTO T1 VALUES (0, 1);
 
INSERT INTO T1 VALUES (1, 2);
 
INSERT INTO T1 VALUES (2, 3);
 
INSERT INTO T1 VALUES (3, 2);
 
INSERT INTO T1 VALUES (4, 1);
 
INSERT INTO T1 VALUES (5, 2);
 
INSERT INTO T1 VALUES (6, 3);
 
INSERT INTO T1 VALUES (7, 1);
 
 
아래의 질의는 다음의 결과를 출력한다.
SELECT C1,C2 FROM T1 ORDER BY C1 SERIES BY C2>1;
C1          C2         
---------------------------
1           2          
2           3          
3           2          
5           2          
6           3   
 
C2 컬럼의 값이 1 보다 큰 C1의 RANGE값을 알고 싶은 경우, SERIESNUM 함수로 각 레코드가 어느 그룹에 포함되는지를 출력하여 RANGE를 결정할 수 있다.
```

## LIMIT

LIMIT 절은 출력되는 레코드의 개수를 제한할 때 사용한다. 결과 집합의 특정 행부터 마지막 행까지 출력하기 위해 정수를 지정할 수 있다

```sql
LIMIT [offset,] row_count
 
select id1, avg(id2) from exptab where id2 group by id1 order by id1 LIMIT 10;
```

## DURATION

DURATION은 _arrival_time을 기준으로 데이터 검색 범위를 손쉽게 결정하도록 해 주는 키워드이다. BEFORE 구문과 함께 사용되어 특정 시점의 특정 데이터 범위를 설정하게 해 준다. 이 DURATION을 잘 활용하면 검색 성능을 현격하게 올림과 동시에 시스템 부하를 획기적으로 낮출 수 있다. 더 자세한 활용 용도는 다음을 참조한다.

```sql
DURATION Number TimeSpec [BEFORE/AFTER Number TimeSpec]
TimeSpec : YEAR | MONTH | WEEK |  DAY | HOUR | MINUTE | SECOND
```

```sql
create table t8(i1 integer);
insert into t8 values(1);
insert into t8 values(2);
 
select i1 from t8;
 
## BEFORE 절 없이
select i1 from t8 duration 2 second;
select i1 from t8 duration 1 minute;
select i1 from t8 duration 1 hour;
select i1 from t8 duration 1 day;
select i1 from t8 duration 1 week;
select i1 from t8 duration 1 month;
select i1 from t8 duration 1 year;
 
## DURATION 구문 전체를 써서
select i1 from t8 duration 1 second before 1 day;
select i1 from t8 duration 1 minute before 1 day;
select i1 from t8 duration 1 hour before 1 day;
select i1 from t8 duration 1 day before 1 day;
select i1 from t8 duration 1 week before 1 day;
select i1 from t8 duration 1 month before 1 day;
select i1 from t8 duration 1 year before 1 day;
```

수행 결과는 다음과 같다.

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
 
## DURATION 구문 전체를 써서
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

## SAVE DATA

질의의 결과를 CSV 데이터 파일로 바로 저장한다.

```sql
SAVE DATA INTO 'file_name.csv' [HEADER ON|OFF] [(FIELDS | COLUMNS) [TERMINATED BY 'char'] [ENCLOSED BY 'char']] [ENCODED BY coding_name] AS select query;
```

옵션의 설명은 다음과 같다.

|옵션|설명|
|--|--|
|HEADER (ON\|OFF)|생성할 csv 파일의 첫번째 라인에 컬럼명을 입력할지를 결정한다. 기본값은 OFF이다.|
|(FIELDS\|COLUMNS) TERMINATED BY 'term_char'<br>ENCLOSED BY 'escape_char'|생성할 csv 파일의 컬럼 구분자와 이스케이프 구분자를 지정한다.|
|ENCODED BY coding_name<br>coding_name = ( UTF8, MS949, KSC5601, EUCJP, SHIFTJIS, BIG5, GB231280 )|출력 데이터 파일의 인코딩 포맷을 지정한다. 기본값은 UTF8이다.|

```sql
SAVE DATA INTO '/tmp/aaa.csv' AS select * from t1;
-- select 문을 실행하여 그 결과를 '/tmp/aaa.csv' 파일에 csv 포멧으로 기록한다.
  
SAVE DATA INTO '/tmp/ccc.csv' HEADER ON FIELDS TERMINATED BY ';' ENCLOSED BY '\'' ENCODED BY MS949 AS select * from t1 where i1 > 100;
-- select 문을 실행하여 그 결과를 /tmp/ccc.csv파일에 기록한다. 필드 구분자와 이스케이프 구분자를 각각 지정하고 저장되는 데이터의 인코딩은 MS949로 설정한다.
```
