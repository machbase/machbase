---
title: '7.7 운영과 데이터 생명주기'
weight: 70
toc: true
---

LOG 테이블의 데이터 삭제와 보존 정책을 다룬다.


<a id="original-85-deleting-data"></a>

## Log 데이터 삭제


Log 테이블에서 DELETE 문을 실행할 수 있다.

임의 위치의 데이터를 삭제하는 것은 불가능하며, 임의 위치에서 마지막(가장 오래된 로그) 레코드까지 연속적으로 삭제하는 방식만 지원한다. 로그 데이터의 특성을 활용한 정책으로, 공간 확보를 위해 파일을 순서대로 삭제하는 행위를 DB 형식으로 표현한 것이다.

사용할 수 있는 표현식은 다음과 같다.

###  구문

```sql
DELETE FROM table_name;
DELETE FROM table_name OLDEST number ROWS;
DELETE FROM table_name EXCEPT number ROWS;
DELETE FROM table_name EXCEPT number [YEAR | MONTH | WEEK | DAY | HOUR | MINUTE | SECOND];
DELETE FROM table_name BEFORE datetime_expr;
```


###  예제

```sql
-- 모든 데이터 삭제
mach>DELETE FROM devices;
10 row(s) deleted.

-- 가장 오래된 5개 삭제
mach>DELETE FROM devices OLDEST 5 ROWS;
5 row(s) deleted.

-- 마지막 5개를 제외한 모든 데이터 삭제
mach>DELETE FROM devices EXCEPT 5 ROWS;
15 row(s) deleted.

-- 2018년 6월 1일 이전 또는 같은 시각의 모든 데이터 삭제
mach>DELETE FROM devices BEFORE TO_DATE('2018-06-01', 'YYYY-MM-DD');
50 row(s) deleted.
```
