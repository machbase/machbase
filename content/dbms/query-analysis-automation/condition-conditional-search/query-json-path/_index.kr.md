---
type: docs
title: 'JSON 컬럼 조회'
weight: 50
---

Machbase의 JSON 컬럼은 구조가 유동적인 데이터를 저장할 때 사용합니다. TAG 테이블의 `value` 컬럼이나 별도로 정의한 JSON 타입 컬럼에 임의의 JSON 객체를 저장하고 JSONPath 문법으로 개별 필드에 접근할 수 있습니다.

## 이 절에서 다루는 내용

- **[LOOKUP JSON 조건 조회](./condition-query-lookup-json/)**: LOOKUP 테이블 JSON 컬럼의 path 조건 조회와 주의사항

## JSON 컬럼 접근 방법

Machbase는 두 가지 JSONPath 접근 문법을 지원합니다.

### 화살표 연산자 (`->`)

```text
column->'$.path'
```

### 점 표기법 (dot shorthand)

```text
column.path
```

두 문법은 동일한 결과를 반환합니다.

## 기본 조회 예시

```sql
-- 화살표 연산자로 JSON 필드 조회
SELECT name, value->'$.temperature' AS temp
FROM tag
WHERE name = 'sensor1';

-- 점 표기법으로 동일하게 조회
SELECT name, value.temperature AS temp
FROM tag
WHERE name = 'sensor1';
```

## 중첩 필드 접근

```sql
-- 중첩 객체 접근
SELECT name, value->'$.location.building' AS building
FROM tag
WHERE ts >= NOW - 3600000000000;

-- 중첩 예: {"device": {"id": "A1", "type": "temp"}}
SELECT name, value->'$.device.id' AS device_id
FROM tag_json;
```

## 배열 인덱스 접근

```sql
-- 배열의 첫 번째 요소 접근 (0-based)
SELECT name, value->'$.readings[0]' AS first_reading
FROM tag_json;

-- 배열의 두 번째 요소
SELECT name, value->'$.readings[1]' AS second_reading
FROM tag_json;
```

## 조건 필터링

### 동등 비교

```sql
SELECT * FROM tag
WHERE value->'$.status' = 'active';
```

### 숫자 범위 비교

```sql
SELECT name, value->'$.temperature' AS temp
FROM tag
WHERE value->'$.temperature' > 80.0
  AND ts >= NOW - 3600000000000;
```

### ISNULL / IS NOT NULL

```sql
-- JSON 필드가 없거나 null인 행 조회
SELECT * FROM tag
WHERE value->'$.error_code' IS NOT NULL;

-- JSON 필드가 존재하는 행만 조회
SELECT name, value->'$.unit'
FROM tag
WHERE value->'$.unit' IS NOT NULL;
```

### LIKE 패턴 매칭

```sql
-- JSON 문자열 필드에 LIKE 적용
SELECT name, value->'$.location'
FROM tag
WHERE value->'$.location' LIKE 'factory%';
```

## JSON SUMMARIZED 컬럼

TAG 테이블에서 JSON 컬럼에 대한 롤업(rollup) 집계를 지원하려면 `SUMMARIZED` 옵션을 사용합니다.

```sql
CREATE TAG TABLE tag_json (
    name    VARCHAR(80) PRIMARY KEY,
    time    DATETIME BASETIME,
    value   JSON SUMMARIZED
);
```

`SUMMARIZED`로 선언된 JSON 컬럼은 숫자 필드에 대해 `ROLLUP` 함수와 함께 집계 최적화가 적용됩니다.

## 성능 주의사항

> JSON 필드 조건은 인덱스를 사용하지 않습니다. `name`(기본키)과 `time`(BASETIME) 조건을 함께 지정하여 스캔 범위를 최소화하세요.

```sql
-- 권장 패턴: name과 시간 조건으로 범위 축소 후 JSON 필드 필터링
SELECT name, value->'$.temperature' AS temp
FROM tag
WHERE name = 'sensor1'                          -- 기본키 인덱스 활용
  AND ts BETWEEN '2024-01-01' AND '2024-01-02'  -- 시간 인덱스 활용
  AND value->'$.temperature' > 50.0;            -- JSON 필드 필터
```
