---
type: docs
title: 'REGEXP_LIKE 함수'
weight: 30
---

`REGEXP_LIKE`는 정규 표현식 매칭 결과를 **숫자값(1/0)**으로 반환하는 함수입니다. `REGEXP` 연산자가 WHERE 조건 전용인 것과 달리, `REGEXP_LIKE`는 SELECT 목록, CASE 표현식, WHERE 조건에서 사용할 수 있습니다.

## 구문

```sql
REGEXP_LIKE(string_expr, 'pattern')
```

| 인수 | 설명 |
|------|------|
| `string_expr` | 검사할 문자열 컬럼 또는 표현식 |
| `pattern` | POSIX 확장 정규 표현식(ERE) 패턴 |

- 패턴이 일치하면 `1`, 일치하지 않으면 `0`을 반환합니다.
- `string_expr`이 NULL이면 `NULL`을 반환합니다.

## REGEXP 연산자와의 비교

| 구분 | `REGEXP` 연산자 | `REGEXP_LIKE` 함수 |
|------|----------------|-------------------|
| 사용 위치 | WHERE 절 전용 | SELECT 목록, CASE, WHERE 등 어디서나 |
| 반환 타입 | 조건 (행 필터) | 정수 (1 또는 0) |
| 사용 목적 | 행 필터링 | 값 계산, 태깅, 분기 |

## 예시

### SELECT 목록에서 행 태깅

```sql
-- 각 행에 패턴 일치 여부를 숫자로 부여
SELECT
    sensor_id,
    value,
    REGEXP_LIKE(sensor_id, 'TEMP[0-9]+') AS is_temp_sensor
FROM sensor_log;
```

### CASE 표현식과 조합

```sql
-- 패턴에 따라 센서 종류를 분류
SELECT
    sensor_id,
    value,
    CASE
        WHEN REGEXP_LIKE(sensor_id, '^TEMP') THEN '온도 센서'
        WHEN REGEXP_LIKE(sensor_id, '^PRESS') THEN '압력 센서'
        WHEN REGEXP_LIKE(sensor_id, '^FLOW') THEN '유량 센서'
        ELSE '기타'
    END AS sensor_type
FROM sensor_log;
```

### WHERE 절과 함께 사용

```sql
-- WHERE에서도 사용 가능 (REGEXP 연산자와 동일한 효과)
SELECT * FROM sensor_log
WHERE REGEXP_LIKE(sensor_id, 'TEMP[0-9]+');

-- 위 쿼리는 아래와 결과가 같음
SELECT * FROM sensor_log
WHERE sensor_id REGEXP 'TEMP[0-9]+';
```

### 집계와 조합

```sql
-- 패턴별 행 수 집계
SELECT
    SUM(CASE WHEN REGEXP_LIKE(sensor_id, '^TEMP') THEN 1 ELSE 0 END) AS temp_count,
    SUM(CASE WHEN REGEXP_LIKE(sensor_id, '^PRESS') THEN 1 ELSE 0 END) AS press_count,
    SUM(CASE WHEN REGEXP_LIKE(sensor_id, '^FLOW') THEN 1 ELSE 0 END) AS flow_count
FROM sensor_log
WHERE ts >= NOW - 3600000000000;
```

## 지원 정규식 문법

Machbase는 POSIX 확장 정규 표현식(ERE)을 지원합니다. `REGEXP` 연산자와 동일한 패턴 문법을 사용합니다.

| 패턴 | 의미 |
|------|------|
| `.` | 임의의 한 문자 |
| `*` | 0회 이상 반복 |
| `+` | 1회 이상 반복 |
| `?` | 0 또는 1회 |
| `[abc]` | a, b, c 중 하나 |
| `[^abc]` | a, b, c가 아닌 문자 |
| `^` | 문자열 시작 |
| `$` | 문자열 끝 |
| `{m,n}` | m~n회 반복 |
| `(abc)` | 그룹 |
| `a\|b` | a 또는 b |

## 성능 주의사항

> `REGEXP_LIKE`는 인덱스를 사용하지 않습니다. 시간 범위나 다른 인덱스 조건을 먼저 적용하여 대상 행 수를 줄인 뒤 사용하세요.

```sql
-- 권장: 시간 조건으로 범위를 먼저 축소
SELECT
    sensor_id,
    REGEXP_LIKE(sensor_id, '^TEMP') AS is_temp
FROM sensor_log
WHERE ts >= NOW - 3600000000000;   -- 인덱스 활용
```
