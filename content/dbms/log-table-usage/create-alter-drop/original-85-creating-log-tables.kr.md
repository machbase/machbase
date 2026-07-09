---
type: docs
title: '7.3.1 Log 테이블 생성 및 관리'
weight: 10
---

> **8.5 원문 보강 자료**: 이 문서는 기존 8.5 매뉴얼의 내용을 새 장 구조에 맞춰 보존한 것입니다. Machbase 8.6 기준과 표현이 다른 부분은 같은 절의 최신 리뉴얼 문서를 우선합니다.

Log 테이블은 다음과 같이 간단하게 생성할 수 있습니다.

sensor_data라는 테이블을 생성하고 삭제해 보겠습니다.

Machbase와 호환되는 데이터 타입은 SQL Reference Types에서 찾을 수 있습니다.


## Log 테이블 생성

'CREATE TABLE' 구문으로 Log 테이블을 생성합니다.

```sql
Mach> CREATE TABLE sensor_data (id VARCHAR(32), val DOUBLE);
Created successfully.

Mach> DROP TABLE sensor_data;
Dropped successfully.
```


## Log 테이블 삭제

'DROP TABLE' 문으로 Log 테이블을 삭제합니다.

```sql
-- DROP은 데이터와 테이블을 모두 삭제합니다.
Mach> DROP TABLE sensor_data;
Dropped successfully.

-- TRUNCATE는 데이터만 삭제하고 테이블은 유지합니다.
Mach> TRUNCATE TABLE sensor_data;
Truncated successfully.
```
