---
type: docs
title: 'JSON 컬럼 설계'
weight: 40
---

LOOKUP 테이블에서 유연한 속성 구조가 필요한 경우 `JSON` 타입 컬럼을 사용합니다.

## JSON 컬럼 스키마

```sql
CREATE LOOKUP TABLE sensor_config (
    sensor_id  VARCHAR(64) PRIMARY KEY,
    config     JSON
);
```

## JSON 삽입 및 조회

```sql
-- 삽입
INSERT INTO sensor_config VALUES (
    'TEMP-01',
    '{"unit":"Celsius","range":{"min":-40,"max":150},"alert":{"low":0,"high":80}}'
);

-- 전체 JSON 조회
SELECT sensor_id, config FROM sensor_config WHERE sensor_id = 'TEMP-01';

-- JSON 필드 조회 (json_value 함수)
SELECT sensor_id,
       json_value(config, '$.unit') AS unit,
       json_value(config, '$.alert.high') AS alert_high
FROM sensor_config;
```

## JSON UPDATE

```sql
-- JSON 전체 교체 (부분 업데이트 미지원)
UPDATE sensor_config
SET config = '{"unit":"Fahrenheit","range":{"min":-40,"max":300},"alert":{"low":32,"high":176}}'
WHERE sensor_id = 'TEMP-01';
```

## 언제 JSON 컬럼을 사용하는가

| 상황 | 권장 접근 |
|------|---------|
| 속성이 고정적 | 별도 컬럼 |
| 속성이 센서마다 다름 | JSON 컬럼 |
| 해당 필드로 자주 조회 | 별도 컬럼 + 인덱스 |
| 단순 저장·조회 | JSON 컬럼 |

## 주의사항

- JSON 컬럼 전체를 UPDATE할 때는 전체 JSON 문자열을 교체해야 합니다.
- JSON 특정 경로로 조건 검색 시 인덱스가 없으면 풀스캔이 발생합니다.
- 자주 사용하는 JSON 필드는 별도 컬럼으로 분리하는 것을 권장합니다.
