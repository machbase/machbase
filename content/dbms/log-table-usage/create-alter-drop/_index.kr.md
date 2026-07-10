---
title: '7.3 생성, 변경, 삭제'
weight: 30
toc: true
---

LOG 테이블의 생성과 삭제 방법을 다룬다.


<a id="original-85-creating-log-tables"></a>

## Log 테이블 생성 및 관리

> **8.5 원문 보강 자료**: 이 문서는 기존 8.5 매뉴얼의 내용을 새 장 구조에 맞춰 보존한 것입니다. Machbase 8.6 기준과 표현이 다른 부분은 같은 절의 최신 리뉴얼 문서를 우선합니다.

Log 테이블은 간단하게 생성할 수 있다.

다음은 sensor_data 테이블을 생성하고 삭제하는 예제다. Machbase 호환 데이터 타입은 SQL Reference Types에서 확인할 수 있다.


### Log 테이블 생성

'CREATE TABLE' 구문으로 Log 테이블을 생성한다.

```sql
Mach> CREATE TABLE sensor_data (id VARCHAR(32), val DOUBLE);
Created successfully.

Mach> DROP TABLE sensor_data;
Dropped successfully.
```


### Log 테이블 삭제

'DROP TABLE' 문으로 Log 테이블을 삭제한다.

```sql
-- DROP은 데이터와 테이블을 모두 삭제합니다.
Mach> DROP TABLE sensor_data;
Dropped successfully.

-- TRUNCATE는 데이터만 삭제하고 테이블은 유지합니다.
Mach> TRUNCATE TABLE sensor_data;
Truncated successfully.
```
