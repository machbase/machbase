---
type: docs
title: 'JSON 컬럼 설계'
weight: 40
---

현재 빌드에서는 LOOKUP 테이블에 `JSON` 타입 컬럼을 생성할 수 없습니다. 유연한 속성 구조가 필요하면 `VARCHAR` 컬럼에 JSON 문자열을 저장하고, 자주 조회하는 필드는 별도 컬럼으로 분리합니다.

## JSON 컬럼 스키마

```sql
CREATE LOOKUP TABLE sensor_config (
    sensor_id  VARCHAR(64) PRIMARY KEY,
    config     VARCHAR(4096)
);
```

## JSON 삽입 및 조회

```sql
-- 삽입
INSERT INTO sensor_config VALUES (
    'TEMP-01',
    '{"unit":"Celsius","range":{"min":-40,"max":150},"alert":{"low":0,"high":80}}'
);

-- JSON 문자열 조회
SELECT sensor_id, config FROM sensor_config WHERE sensor_id = 'TEMP-01';
```

## 값 UPDATE

```sql
-- 전체 JSON 문자열 교체
UPDATE sensor_config
SET config = '{"unit":"Fahrenheit","range":{"min":-40,"max":300},"alert":{"low":32,"high":176}}'
WHERE sensor_id = 'TEMP-01';
```

## 언제 JSON 컬럼을 사용하는가

| 상황 | 권장 접근 |
|------|---------|
| 속성이 고정적 | 별도 컬럼 |
| 속성이 센서마다 다름 | `VARCHAR`에 JSON 문자열 저장 |
| 해당 필드로 자주 조회 | 별도 컬럼 + 인덱스 |
| 단순 저장·조회 | JSON 문자열 컬럼 |

## 주의사항

- LOOKUP 테이블의 `JSON` 타입 컬럼은 현재 지원되지 않습니다.
- JSON 문자열 내부 필드는 SQL의 JSON path 조건으로 조회할 수 없습니다.
- 자주 사용하는 JSON 필드는 별도 컬럼으로 분리하는 것을 권장합니다.
