---
title : '로그 데이터의 삭제'
type: docs
weight: 40
---

마크베이스에서의 DELETE 구문은 로그 테이블에 대해서 수행 가능하다.

또한, 중간의 임의 위치에 있는 데이터를 삭제할 수 없으며, 임의의 위치부터 연속적으로 마지막(가장 오래된 로그) 레코드까지 지울 수 있도록 구현되었다. 

이는 로그 데이터의 특성을 살린 정책으로서 한번 입력되면 수정이 없고, 공간 확보를 위해 파일을 삭제하는 행위를 DB 형식으로 표현한 것이다.

아래는 사용할 수 있는 표현의 종류이다.

## 문법

```sql
DELETE FROM table_name;
DELETE FROM table_name OLDEST number ROWS;
DELETE FROM table_name EXCEPT number ROWS;
DELETE FROM table_name EXCEPT number [YEAR | MONTH | WEEK | DAY | HOUR | MINUTE | SECOND];
DELETE FROM table_name BEFORE datetime_expr;
```

## 예제

```sql
-- 모든 데이터를 삭제한다.
mach>DELETE FROM devices;
10 row(s) deleted.
 
-- 가장 오래된 5건을 삭제한다.
mach>DELETE FROM devices OLDEST 5 ROWS;
10 row(s) deleted.
 
-- 최근 5건을 제외하고 모두 삭제한다.
mach>DELETE FROM devices EXCEPT 5 ROWS;
15 row(s) deleted.
 
-- 2018년 6월 1일 이전의 데이터를 모두 삭제한다.
mach>DELETE FROM devices BEFORE TO_DATE('2018-06-01', 'YYYY-MM-DD');
50 row(s) deleted.
```