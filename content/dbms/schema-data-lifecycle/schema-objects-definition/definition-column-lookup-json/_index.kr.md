---
type: docs
title: 'LOOKUP JSON 컬럼 정의'
weight: 60
---

LOOKUP 테이블은 일반 컬럼으로 `JSON` 타입을 사용할 수 있습니다. JSON 컬럼은 생성,
저장, 조회, 조건 검색, 갱신에 사용할 수 있습니다.

## 컬럼 정의

```sql
CREATE LOOKUP TABLE device_config (
    device_id VARCHAR(40) PRIMARY KEY,
    site      VARCHAR(32),
    status    VARCHAR(16),
    config    JSON
);
```

## 삽입과 조회

```sql
INSERT INTO device_config VALUES (
    'DEV-01',
    'SEOUL',
    'READY',
    '{"region":"kr","level":3,"limits":{"high":85.0,"low":5.0}}'
);

SELECT device_id, config
FROM device_config
WHERE config->'$.region' = 'kr'
  AND JSON_EXTRACT_INTEGER(config, '$.level') >= 3;
```

## JSON 값 갱신

```sql
UPDATE device_config
SET config = JSON_SET(config, '$.status', 'active')
WHERE site = 'SEOUL';

UPDATE device_config
SET config = JSON_SET_JSON(config, '$.extra', '{"verified":1}')
WHERE device_id = 'DEV-01';

UPDATE device_config
SET config = JSON_REMOVE(config, '$.extra')
WHERE device_id = 'DEV-01';
```

## 제약 사항

- `JSON` 컬럼은 LOOKUP 테이블의 일반 컬럼으로 사용할 수 있습니다.
- `JSON` 컬럼 자체를 primary key로 선언할 수는 없습니다.
- JSON path 문자열은 작은따옴표(`'$.key'`)로 작성합니다.
- JSON path별 전용 인덱스는 지원하지 않습니다. 자주 검색하는 값은 별도 컬럼으로 분리하는 설계를 고려합니다.
