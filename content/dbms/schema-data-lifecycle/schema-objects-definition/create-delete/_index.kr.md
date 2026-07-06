---
type: docs
title: '테이블 생성과 삭제'
weight: 10
---

## CREATE TABLE

### LOG 테이블

```sql
CREATE TABLE log_name (
    col1  TYPE1,
    col2  TYPE2,
    ...
);
```

LOG 테이블은 아무 키워드 없이 `CREATE TABLE`을 사용합니다. `_arrival_time` 컬럼이 자동으로 추가됩니다.

```sql
-- 예시: 웹 액세스 로그
CREATE TABLE web_access (
    method   VARCHAR(8),
    uri      VARCHAR(1024),
    status   SHORT,
    src_ip   IPV4,
    bytes    INTEGER
);
```

### TAG 테이블

```sql
CREATE TAG TABLE tag_name (
    name  VARCHAR(n)  PRIMARY KEY,
    time  DATETIME    BASETIME,
    value DOUBLE
) [METADATA (meta_col TYPE, ...)]
  [TAG_PARTITION_COUNT = n]
  [TAG_DATA_PART_SIZE  = n];
```

거리축 TAG 테이블은 `BASETIME` 대신 `BASE DISTANCE`를 사용합니다.

```sql
-- 시간축
CREATE TAG TABLE sensor_data (
    name  VARCHAR(64) PRIMARY KEY,
    time  DATETIME    BASETIME,
    value DOUBLE      SUMMARIZED
);

-- 거리축
CREATE TAG TABLE pipeline_data (
    name      VARCHAR(32) PRIMARY KEY,
    distance  DOUBLE      BASE DISTANCE,
    thickness DOUBLE
);
```

### RDB 테이블

```sql
CREATE RDB TABLE table_name (
    col1  TYPE1,
    col2  TYPE2,
    ...
);
```

```sql
CREATE RDB TABLE orders (
    order_id LONG,
    customer VARCHAR(64),
    amount   DOUBLE,
    status   VARCHAR(16)
);
```

### VOLATILE 테이블

```sql
CREATE VOLATILE TABLE table_name (
    pk_col  TYPE  PRIMARY KEY,
    col2    TYPE,
    ...
);
```

### LOOKUP 테이블

```sql
CREATE LOOKUP TABLE table_name (
    pk_col  TYPE  PRIMARY KEY,
    col2    TYPE,
    ...
);
```

### IF NOT EXISTS

동일한 이름의 테이블이 이미 존재해도 오류가 발생하지 않습니다.

```sql
CREATE TABLE IF NOT EXISTS web_access (...);
```

## DROP TABLE

```sql
DROP TABLE table_name;
```

테이블을 조회 중인 세션이 있으면 오류가 발생합니다. 조회를 종료한 후 삭제합니다.

```sql
DROP TABLE orders;
```

## 테이블 이름 규칙

- 영문자·숫자·언더스코어(`_`) 조합
- 대소문자 구분 없음 (내부 저장 시 대문자 변환)
- 특수문자 사용 시 큰따옴표(`"`) 로 감쌉니다

```sql
CREATE TABLE "my-table" (id INTEGER);
```
