---
type: docs
title: 'LOOKUP JSON 조건 조회'
weight: 10
---

LOOKUP 테이블의 `JSON` 컬럼은 JSON path 조건 조회에 사용할 수 있습니다.

## 기본 조회

```sql
CREATE LOOKUP TABLE sensor_config (
    sensor_id VARCHAR(80) PRIMARY KEY,
    location  VARCHAR(200),
    config    JSON
);

INSERT INTO sensor_config VALUES (
    'TEMP-01',
    'factory1',
    '{"unit":"celsius","level":3,"threshold":{"high":90.0}}'
);

SELECT sensor_id, config
FROM sensor_config
WHERE config->'$.unit' = 'celsius';
```

## 타입별 추출 함수

숫자 값을 숫자로 비교할 때는 타입별 JSON 추출 함수를 사용합니다.

```sql
SELECT sensor_id
FROM sensor_config
WHERE JSON_EXTRACT_INTEGER(config, '$.level') >= 3
  AND JSON_EXTRACT_DOUBLE(config, '$.threshold.high') > 80.0;
```

## JSON 상태 확인

```sql
SELECT sensor_id
FROM sensor_config
WHERE JSON_IS_VALID(config) = 1
  AND JSON_TYPEOF(config, '$.threshold') = 'Object';
```

## 주의사항

- JSON path 문자열은 작은따옴표(`'$.unit'`)로 작성합니다. 큰따옴표는 SQL 식별자로 해석됩니다.
- `->` 연산자는 path 값을 문자열처럼 비교할 때 사용합니다.
- JSON path별 전용 인덱스는 지원하지 않습니다. 대량 LOOKUP 테이블에서 자주 검색하는 JSON 값은 별도 컬럼으로 분리합니다.
