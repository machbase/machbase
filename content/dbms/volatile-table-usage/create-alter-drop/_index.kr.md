---
title: '10.3 생성, 변경, 삭제'
weight: 30
toc: true
---
생성, 변경, 삭제에 해당하는 세부 문서를 모았습니다.


<a id="original-85-creating-volatile-tables"></a>

## Volatile 테이블 생성 및 관리

> **8.5 원문 보강 자료**: 이 문서는 기존 8.5 매뉴얼의 내용을 새 장 구조에 맞춰 보존한 것입니다. Machbase 8.6 기준과 표현이 다른 부분은 같은 절의 최신 리뉴얼 문서를 우선합니다.

volatile 테이블의 생성 및 삭제 방법은 다음과 같습니다.

### 생성

```sql
create volatile table vtable (id1 integer, name varchar(20));
```


### 삭제

```sql
drop table vtable;
```

<a id="differences-persistence-ddl"></a>

## 영속성 차이·DDL

VOLATILE 테이블은 다른 테이블 타입과 달리 메모리에만 존재합니다.

### 영속성 비교

| 항목 | VOLATILE | LOOKUP | RDB | TAG | LOG |
|------|----------|--------|-----|-----|-----|
| 저장 위치 | 메모리 | 디스크 | 디스크 | 디스크 | 디스크 |
| 서버 재시작 후 데이터 유지 | X | O | O | O | O |
| 테이블 구조(DDL) 유지 | X | O | O | O | O |

### DDL 특성

VOLATILE 테이블은 서버 재시작 시 테이블 자체가 사라집니다. 따라서 서버 시작 시 테이블을 재생성해야 합니다.

```sql
-- 서버 시작 시 VOLATILE 테이블 생성 (초기화 스크립트 필요)
CREATE VOLATILE TABLE sensor_latest (
    sensor_id  VARCHAR(64) PRIMARY KEY,
    value      DOUBLE,
    updated_at DATETIME
);
```

### 생성 문법

```sql
CREATE VOLATILE TABLE table_name (
    pk_col  type  PRIMARY KEY,  -- PK 기반 동작이 필요할 때 지정
    col2    type,
    ...
);
```

- `PRIMARY KEY` 선택
- PRIMARY KEY 컬럼은 하나만 지정

### 삭제

```sql
DROP TABLE sensor_latest;
```

### 주의사항

- VOLATILE 테이블의 DDL(구조 정의)은 데이터베이스에 영구 저장되지 않습니다.
- 서버 재시작 후 자동으로 재생성되지 않으므로, 초기화 스크립트(예: 시작 시 machsql 실행)를 구성합니다.
