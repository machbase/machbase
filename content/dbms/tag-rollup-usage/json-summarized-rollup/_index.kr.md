---
title: '6.8 JSON SUMMARIZED ROLLUP'
weight: 80
toc: true
---

<a id="json-summarized-rollup"></a>

## JSON SUMMARIZED ROLLUP

JSON 타입 컬럼에 `SUMMARIZED` 속성을 추가하면 JSON 내 숫자 필드를 ROLLUP 집계 대상으로 사용할 수 있습니다.

### JSON SUMMARIZED 컬럼 생성

```sql
CREATE TAG TABLE tag_json (
    name  VARCHAR(40) PRIMARY KEY,
    time  DATETIME BASETIME,
    value JSON SUMMARIZED
);
```

### JSON ROLLUP 생성

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

### 조회

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

### JSON Whole-Document 집계

JSON SUMMARIZED 컬럼 전체를 대상으로 집계하면 객체의 숫자 경로별 통계를 JSON으로
반환합니다. 배열 내부 요소를 자동으로 펼쳐 집계하는 방식은 아닙니다.

```sql
CREATE ROLLUP tag_json_whole_ru
  ON tag_json(value)  -- 컬럼 전체 지정
  INTERVAL 1 MIN;
```

### 주의사항

- 개별 경로의 숫자 집계와 문서 전체 집계를 구분합니다. 문서 전체 집계는 숫자 값만
  계산에 사용하며 문자열·불리언·JSON null·배열은 숫자 집계에서 제외합니다.
- 문서 전체 집계에서 비숫자 경로는 결과에 null로 표시되거나 생략될 수 있습니다.
  문자열 속성이 포함되어 있다는 이유만으로 ROLLUP 생성이 거부되는 것은 아닙니다.
- 유효하지 않은 JSON은 입력 단계에서 오류가 발생합니다.
- `COUNT(value)`는 SQL NULL이 아닌 문서 수, `COUNT(*)`는 행 수입니다. 각 숫자 경로의
  유효 표본 수와 혼동하지 않습니다.
- JSONPath 문법: `value->'$.path'`, dot 문법: `value.path` 둘 다 사용 가능합니다.
