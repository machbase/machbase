---
type: docs
title: 'LOOKUP JSON 컬럼 제약'
weight: 60
---

LOOKUP 테이블은 `JSON` 컬럼을 지원하지 않습니다. 유연한 속성이 필요한 참조 데이터는
자주 조회하는 값을 일반 컬럼으로 분리하고, 유동적인 속성은 문자열로 직렬화하거나 RDB/TAG
테이블의 JSON 컬럼 사용을 검토합니다.

## 컬럼 정의

```sql
-- 실패: LOOKUP 테이블에는 JSON 컬럼을 만들 수 없음
CREATE LOOKUP TABLE device_config (
    device_id VARCHAR(40) PRIMARY KEY,
    site      VARCHAR(32),
    status    VARCHAR(16),
    config    JSON
);
```

## 대안 스키마와 조회

```sql
CREATE LOOKUP TABLE device_config (
    device_id VARCHAR(40) PRIMARY KEY,
    site      VARCHAR(32),
    status    VARCHAR(16),
    region    VARCHAR(16),
    level     INTEGER,
    limits    VARCHAR(512)
);

SELECT device_id, limits
FROM device_config
WHERE region = 'kr'
  AND level >= 3;
```

## 값 갱신

```sql
UPDATE device_config
SET status = 'ACTIVE'
WHERE site = 'SEOUL';

UPDATE device_config
SET limits = '{"high":85.0,"low":5.0,"verified":1}'
WHERE device_id = 'DEV-01';
```

## 제약 사항

- LOOKUP/VOLATILE 테이블에는 JSON 컬럼을 생성할 수 없습니다.
- JSON path 조건이나 JSON path 인덱스가 필요하면 RDB/TAG 테이블 사용을 검토합니다.
- 자주 검색하는 값은 LOOKUP 일반 컬럼으로 분리합니다.
