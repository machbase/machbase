---
title: 'Tag 테이블 인덱스'
type: docs
weight: 70
---

## 개요

tag 테이블의 인덱스는 추가 컬럼이나 JSON 경로로 검색할 때 쿼리 성능을 크게 향상시킵니다. 이 가이드는 TAG 인덱스를 효과적으로 생성하고 관리하는 방법을 다룹니다.

## TAG 인덱스란?

Machbase TAG 테이블에 TAG 인덱스 유형을 생성할 수 있습니다.

자세한 내용은 SQL 참조의 DDL 섹션을 참조하세요.

* TAG Index: TAG 인덱스는 TAG 테이블의 추가 컬럼에 생성할 수 있습니다.


## 인덱스 생성

CREATE INDEX 문을 사용하여 특정 컬럼에 인덱스를 생성합니다.

```sql
CREATE INDEX index_name ON table_name (column_name) [index_type]
    index_type ::= INDEX_TYPE { TAG }
```

```bash
Mach> CREATE INDEX id_index ON tag (id) INDEX_TYPE TAG;
Created successfully.
```

버전 7.5부터는 tag 테이블에서만 json 타입 컬럼에 대해 각 json 경로마다 인덱스를 생성할 수 있습니다.

기존 인덱스 생성 구문에 연산자로 json 경로를 연결하기만 하면 됩니다.

json 연산자의 반환 타입은 VARCHAR이므로 VARCHAR를 비교할 때만 인덱스가 사용됩니다.

```bash
Mach> CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, jval JSON);
Executed successfully.

Mach> CREATE INDEX idx_jval_value1 ON tag (jval->'$.value1');
Created successfully.

Mach> CREATE INDEX idx_jval_value2 ON tag (jval->'$.value2');
Created successfully.

Mach> EXPLAIN SELECT * FROM tag WHERE jval->'$.value1' = '10';
PLAN
------------------------------------------------------------------------------------
 PROJECT
  TAG READ (RAW)
   KEYVALUE INDEX SCAN (_TAG_DATA_0)
    [KEY RANGE]
     * jval->'$.value1' = '10'
   VOLATILE FULL SCAN (_TAG_META)
[6] row(s) selected.
```

## Tag 메타데이터 JSON path 인덱스

`TAG METADATA` 의 JSON 컬럼에도 path 인덱스를 생성할 수 있습니다.

```sql
CREATE TAGDATA TABLE ships (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE
)
METADATA (
    status VARCHAR(20),
    info JSON
);

CREATE INDEX idx_ship_owner
ON ships METADATA (info->'$.owner');
```

생성 시 함께 선언할 수도 있습니다.

```sql
CREATE TAGDATA TABLE ships (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE
)
METADATA (
    info JSON INDEX('name', 'ship.status')
);
```

주의사항:

- metadata JSON path 인덱스는 `CREATE INDEX ... ON TAG METADATA (...)` 문법을 사용합니다.
- `INFO JSON INDEX(...)` 는 생성 시 자주 사용하는 path를 함께 선언하는 방식입니다.
- 현재 JSON path 인덱스는 문자열 literal 비교 중심으로 동작합니다.
- 숫자 literal 비교는 full scan 으로 처리될 수 있습니다.

## 인덱스 삭제

DROP INDEX 문을 사용하여 지정된 인덱스를 삭제합니다. 그러나 테이블을 검색하고 있는 다른 세션이 있으면 오류와 함께 실패합니다.

```sql
DROP INDEX index_name;
```

```bash
Mach> DROP INDEX id_index;
Dropped successfully.
```

metadata JSON path 인덱스도 인덱스 이름만으로 삭제합니다.

```sql
DROP INDEX idx_ship_owner;
```
