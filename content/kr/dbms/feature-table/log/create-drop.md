---
type: docs
title : '로그 테이블 생성 및 삭제'
weight: 10
---

로그 테이블은 다음과 같이 간단하게 생성할 수 있다.

sensor_data 라는 테이블을 생성하고 삭제해 보도록 하자.

마크베이스에서 사용가능한 데이터 타입은 SQL 레퍼런스의 자료형 에서 확인하면 된다.

## 로그 테이블 생성

'CREATE TABLE' 구문으로 로그 테이블을 생성한다.
```sql
Mach> CREATE TABLE sensor_data 
(
    id VARCHAR(32),
    val DOUBLE
);
Created successfully.
 
Mach> DROP TABLE sensor_data;
Dropped successfully.
```

## 로그 테이블 삭제

'DROP TABLE' 구문으로 로그 테이블을 삭제한다

```sql
-- DROP은 데이터와 테이블 모두 삭제한다.
Mach> DROP TABLE sensor_data;
Dropped successfully.

-- TRUNCATE는 데이터만 삭제하고 테이블은 유지한다.
Mach> TRUNCATE TABLE sensor_data;
Truncated successfully.
```
