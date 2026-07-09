---
type: docs
title: '5.10.3 JSON METADATA 설계'
weight: 50
---

METADATA 컬럼이 복잡하거나 유연한 속성 구조가 필요한 경우, JSON 형태로 메타데이터를 저장할 수 있습니다.

## JSON 컬럼 사용

```sql
CREATE TAG TABLE sensor_json_meta (
    name   VARCHAR(64) PRIMARY KEY,
    time   DATETIME    BASETIME,
    value  DOUBLE
) METADATA (
    attributes JSON     -- 유연한 속성 저장
);
```

## JSON 삽입

```sql
INSERT INTO sensor_json_meta METADATA (name, attributes)
VALUES ('sensor-01', '{"location":"Building-A","floor":3,"unit":"Celsius","dept":"Mfg"}');
```

## JSON 조회

```sql
-- JSON 필드 추출
SELECT name, attributes->'$.location' AS location
FROM sensor_json_meta METADATA
WHERE name = 'sensor-01';

-- JSON 조건 필터
SELECT name
FROM sensor_json_meta METADATA
WHERE JSON_EXTRACT_INTEGER(attributes, '$.floor') = 3;
```

## 일반 METADATA vs JSON METADATA

| 항목 | 일반 METADATA | JSON METADATA |
|------|--------------|---------------|
| 스키마 유연성 | 고정 컬럼 | 동적 속성 |
| 쿼리 편의성 | 컬럼 직접 참조 | `->` 연산자 또는 JSON_EXTRACT 계열 함수 사용 |
| 성능 | 빠름 | 약간 느림 |
| 적합한 경우 | 속성이 고정적 | 속성이 가변적 |

## 주의사항

- 자주 조회하는 JSON path에는 METADATA JSON path 인덱스를 생성할 수 있습니다.
- JSON 필드를 매우 자주 필터링 조건으로 사용한다면, 해당 필드를 별도 METADATA 컬럼으로 분리하는 것도 고려합니다.
