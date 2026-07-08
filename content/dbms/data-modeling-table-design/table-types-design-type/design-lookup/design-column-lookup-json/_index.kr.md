---
type: docs
title: 'JSON 컬럼 설계'
weight: 40
---

LOOKUP 테이블은 참조 데이터에 붙는 유연한 속성을 `JSON` 컬럼에 저장할 수 있습니다.
자주 조회하는 값은 별도 컬럼으로 분리하고, 유동적인 속성은 JSON 컬럼에 둡니다.

## 설계 예

```sql
CREATE LOOKUP TABLE sensor_config (
    sensor_id VARCHAR(64) PRIMARY KEY,
    site      VARCHAR(32),
    status    VARCHAR(16),
    config    JSON
);
```

```sql
INSERT INTO sensor_config VALUES (
    'TEMP-01',
    'SEOUL',
    'READY',
    '{"unit":"Celsius","range":{"min":-40,"max":150},"level":3}'
);
```

## 조회와 갱신

```sql
SELECT sensor_id
FROM sensor_config
WHERE site = 'SEOUL'
  AND config->'$.unit' = 'Celsius'
  AND JSON_EXTRACT_INTEGER(config, '$.level') >= 3;

UPDATE sensor_config
SET config = JSON_SET(config, '$.status', 'active')
WHERE sensor_id = 'TEMP-01';
```

## 설계 기준

| 상황 | 권장 접근 |
|------|----------|
| 조인/검색에 자주 쓰는 값 | 별도 컬럼 |
| 장비별로 다른 유동 속성 | JSON 컬럼 |
| 숫자 조건 검색 | `JSON_EXTRACT_INTEGER`, `JSON_EXTRACT_DOUBLE` 사용 |
| primary key | JSON이 아닌 안정적인 식별자 컬럼 사용 |
| 고빈도 path 검색 | 별도 컬럼으로 추출 |

## 주의사항

- JSON 컬럼은 일반 컬럼으로 사용할 수 있지만 primary key로 선언할 수 없습니다.
- JSON path별 전용 인덱스는 지원하지 않습니다.
- JSON path 문자열은 작은따옴표(`'$.key'`)로 작성합니다.
