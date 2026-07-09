---
type: docs
title: '6.9.1 JSON SUMMARIZED ROLLUP'
weight: 120
---

JSON 타입 컬럼에 `SUMMARIZED` 속성을 추가하면 JSON 컬럼 내 숫자 필드를 ROLLUP 집계 대상으로 지정할 수 있습니다.

## JSON SUMMARIZED 컬럼 생성

```sql
CREATE TAG TABLE tag_json (
    name  VARCHAR(40) PRIMARY KEY,
    time  DATETIME BASETIME,
    value JSON SUMMARIZED
);
```

## JSON ROLLUP 생성

JSONPath 또는 dot 축약 문법으로 집계할 필드를 지정합니다.

```sql
-- dot 축약 문법
CREATE ROLLUP tag_json_metric_ru
  ON tag_json(value.metric)
  INTERVAL 1 SEC;

-- 기존 JSONPath arrow 문법
CREATE ROLLUP tag_json_metric_arrow_ru
  ON tag_json(value->'$.metric')
  INTERVAL 1 SEC;

-- 배열 인덱스와 특수 key
CREATE ROLLUP tag_json_item_ru
  ON tag_json(value.items[0]."metric-id")
  INTERVAL 1 SEC;
```

## 조회

```sql
-- JSON ROLLUP 조회 (dot 문법)
SELECT rollup('min', 1, time) AS rt,
       AVG(value.metric)
FROM   tag_json
WHERE  name = 'SENSOR-01'
  AND  time BETWEEN '2024-01-01' AND '2024-01-02'
GROUP BY rt
ORDER BY rt;

-- JSONPath arrow 문법
SELECT rollup('min', 1, time) AS rt,
       AVG(value->'$.metric')
FROM   tag_json
WHERE  name = 'SENSOR-01'
GROUP BY rt
ORDER BY rt;
```

## JSON Whole-Document 집계

JSON SUMMARIZED 컬럼 전체를 대상으로 하는 특수 집계도 지원됩니다. 이 경우 JSON 내 모든 숫자 필드를 한 번에 집계합니다.

```sql
CREATE ROLLUP tag_json_whole_ru
  ON tag_json(value)  -- 컬럼 전체 지정
  INTERVAL 1 MIN;
```

## 주의사항

- JSON ROLLUP 대상은 숫자형(number)으로 파싱 가능한 필드여야 합니다.
- 문자열 JSON 값에 대해 ROLLUP을 생성하면 오류가 발생합니다.
- JSONPath 문법: `value->'$.path'`, dot 문법: `value.path` 둘 다 사용 가능합니다.
