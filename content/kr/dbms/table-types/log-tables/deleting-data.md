---
title : Log 데이터 삭제
type: docs
weight: 40
---

Machbase의 DELETE 문은 Log 테이블에서 수행할 수 있습니다.

또한, 중간의 임의 위치에 있는 데이터를 삭제하는 것은 불가능하며, 임의 위치에서 마지막(가장 오래된 로그) 레코드까지 연속적으로 삭제하는 것이 가능합니다. 이는 로그 데이터의 특성을 활용한 정책입니다. 한번 입력된 데이터에 대해 공간을 확보하기 위해 파일을 순서대로 삭제하는 행위의 DB 형식 표현입니다.

다음은 사용할 수 있는 표현식 유형입니다.

##  구문

```sql
DELETE FROM table_name;
DELETE FROM table_name OLDEST number ROWS;
DELETE FROM table_name EXCEPT number ROWS;
DELETE FROM table_name EXCEPT number [YEAR | MONTH | WEEK | DAY | HOUR | MINUTE | SECOND];
DELETE FROM table_name BEFORE datetime_expr;
```


##  예제

```sql
-- 모든 데이터 삭제
mach>DELETE FROM devices;
10 row(s) deleted.
 
-- 가장 오래된 5개 삭제
mach>DELETE FROM devices OLDEST 5 ROWS;
10 row(s) deleted.
 
-- 마지막 5개를 제외한 모든 데이터 삭제
mach>DELETE FROM devices EXCEPT 5 ROWS;
15 row(s) deleted.
 
-- 2018년 6월 1일 이전의 모든 데이터 삭제
mach>DELETE FROM devices BEFORE TO_DATE('2018-06-01', 'YYYY-MM-DD');
50 row(s) deleted.
```
