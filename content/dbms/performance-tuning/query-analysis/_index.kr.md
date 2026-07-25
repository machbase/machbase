---
type: docs
title: '12.10 쿼리와 분석'
weight: 100
toc: true
---
일반 SQL에 더해 DURATION, PIVOT, ROLLUP, SERIES BY, 보간, 윈도우 함수 등 시계열 분석에 특화된 확장 문법을 제공합니다.


<a id="selection-query-method"></a>

## 조회 방식 선택

데이터 조회 방법은 목적과 테이블 타입에 따라 다릅니다.

### 조회 방식 요약

| 조회 목적 | 권장 방식 |
|----------|---------|
| 특정 시간 범위 시계열 조회 | WHERE + 시간 조건 또는 DURATION |
| 최근 N분/시간/일 데이터 | DURATION |
| 태그별 집계 (평균, 최대, 최소) | GROUP BY + 집계 함수 |
| 분 단위 자동 집계 결과 조회 | ROLLUP |
| 여러 TAG를 컬럼으로 배열 | PIVOT |
| 복잡한 SELECT를 단계별로 구성 | WITH / CTE (Standard Edition) |
| 누락 구간 보간 | INTERPOLATION 힌트 |
| 텍스트 패턴 검색 | SEARCH / ESEARCH / LIKE |
| 설정값·상태 JOIN | LOG/TAG ↔ LOOKUP/VOLATILE JOIN |
| 실시간 변환·적재 | STREAM |

하위 페이지에서 테이블 타입별 조회 제약과 선택 가이드를 확인하십시오.

<a id="selection-query-method-selection-guide-query-method"></a>

### 조회 방식 선택 가이드

분석 목적별로 최적의 조회 방식을 선택하는 기준을 정리합니다.

#### 목적별 선택

##### 최근 데이터 조회

```sql
-- 최근 1시간 데이터 (DURATION 권장)
SELECT name, time, value FROM tag DURATION 1 HOUR;

-- 특정 시간 범위 (WHERE 시간 조건)
SELECT name, time, value FROM tag
WHERE time BETWEEN '2024-01-15 00:00:00' AND '2024-01-15 23:59:59';
```

##### 집계 분석

```sql
-- 태그별 1시간 평균 (GROUP BY)
SELECT name, DATE_TRUNC('hour', time) AS h, AVG(value)
FROM tag
GROUP BY name, h
ORDER BY name, h;

-- 사전 계산된 분 단위 집계 (ROLLUP, 더 빠름)
SELECT * FROM rollup(tag, '1 min', '2024-01-15', '2024-01-16');
```

##### 여러 태그를 컬럼으로 배열

```sql
-- PIVOT으로 태그를 컬럼화
SELECT * FROM (SELECT time, name, value FROM tag DURATION 1 HOUR)
PIVOT (AVG(value) FOR name IN ('TEMP-01', 'TEMP-02', 'PRESS-01'));
```

##### 결측 구간 채우기

```sql
-- INTERPOLATION 힌트로 누락 구간 선형 보간
SELECT /*+ INTERPOLATION(time) */ name, time, value
FROM tag DURATION 1 HOUR;
```

##### 설정 정보 JOIN

```sql
-- TAG 데이터와 LOOKUP 설정을 JOIN
SELECT t.name, t.time, t.value, l.location, l.dept
FROM tag t
LEFT JOIN device_meta l ON t.name = l.sensor_id
WHERE t.time BETWEEN '2024-01-15 00:00:00' AND '2024-01-15 12:00:00';
```

##### 실시간 변환·적재 자동화

STREAM을 사용하면 데이터가 삽입될 때마다 자동으로 쿼리가 실행되어 다른 테이블로 적재합니다. 상세는 [STREAM](/dbms/operations-configuration-recovery/automation-stream/#stream)을 참고하십시오.

<a id="selection-query-method-table-types-type-query"></a>

### 테이블 타입별 조회 제약

테이블 타입에 따라 사용 가능한 조회 구문과 제약이 다릅니다.

#### 테이블 타입별 조회 지원 범위

| 기능 | TAG | LOG | TRANSACTION | VOLATILE | LOOKUP |
|------|-----|-----|-----|---------|--------|
| SELECT * | O | O | O | O | O |
| WHERE 시간 조건 | O | O | O | O | O |
| DURATION | O | O | X | X | X |
| GROUP BY | O | O | O | O | O |
| ORDER BY | O | O | O | O | O |
| LIMIT | O | O | O | O | O |
| SERIES BY | O (시간) | O | O | O | O |
| JOIN | O | O | O | O | O |
| PIVOT | O | O | O | O | O |
| ROLLUP 조회 | O (WITH ROLLUP 테이블) | X | X | X | X |
| INTERPOLATION 힌트 | O | X | X | X | X |
| SAMPLING 힌트 | O | X | X | X | X |
| UNION ALL | O | O | O | O | O |
| WITH / CTE (Standard Edition) | O | O | O | O | O |

#### 주요 제약

##### TAG 테이블
- `DURATION` 키워드를 사용하면 BASETIME 컬럼 기준으로 검색 범위를 좁혀 성능을 크게 향상시킵니다.
- ROLLUP, INTERPOLATION, SAMPLING 힌트는 TAG 테이블 전용 기능입니다.
- `FROM TAG METADATA`로 메타데이터만 조회할 수 있습니다.

##### LOG 테이블
- `DURATION`은 `_ARRIVAL_TIME` 기준으로 동작합니다.
- KEYWORD 인덱스가 있으면 `SEARCH`, `ESEARCH` 조건을 사용할 수 있습니다.

##### VOLATILE 테이블
- DURATION은 지원하지 않습니다.
- `_ARRIVAL_TIME` 컬럼이 있으나 DURATION의 의미상 시계열 조회에는 적합하지 않습니다.

##### LOOKUP 테이블
- 주로 JOIN 참조 테이블로 활용됩니다.
- DURATION 미지원.

<a id="query-select"></a>

## SELECT 조회

Machbase의 SELECT 문법과 시계열 특화 조회 기능을 정리합니다.

### 이 절에서 다루는 내용

- **[SELECT 기본 조회](/dbms/performance-tuning/query-analysis/#query-select)**: SELECT 구문, CASE, 서브쿼리, 집합 연산자
- **[WHERE / ORDER BY / LIMIT](/dbms/performance-tuning/query-analysis/#where-order-limit)**: 조건·정렬·결과 수 제한
- **[시간 조건과 DURATION](/dbms/performance-tuning/query-analysis/#condition-time-duration)**: 시계열 조회를 위한 시간 조건
- **[상대 시간 표현](/dbms/performance-tuning/query-analysis/#relative-time)**: DATEADD, NOW 등 상대 시간 함수
- **[거리축 범위 조회](/dbms/tag-table-usage/time-distance-axis/#distance-axis-query-range)**: 거리 기반 TAG 테이블 조회
- **[VIEW 조회](/dbms/performance-tuning/query-analysis/#query-view)**: 저장 VIEW 활용
- **[WITH / CTE](/dbms/performance-tuning/query-analysis/#query-cte)**: 문장 안에서 SELECT 결과를 단계별로 재사용
- **[집합 연산: UNION](/dbms/performance-tuning/query-analysis/#set-operators-union-intersect-except)**: UNION ALL
- **[SELECT 힌트](/dbms/performance-tuning/query-analysis/#hint-select)**: SAMPLING, INTERPOLATION 등 힌트
- **[EXPLAIN으로 실행 계획 확인](/dbms/performance-tuning/query-analysis/#execution-plan-explain)**: 쿼리 성능 분석

<a id="query-select-query-select"></a>

### SELECT 기본 조회

#### SELECT 기본 구문

```sql
SELECT target_list [FROM table_list]
[WHERE condition_expr]
[GROUP BY expr] [HAVING expr]
[ORDER BY expr [DESC]] [SERIES BY expr]
[LIMIT n[,n]]
[DURATION duration_expr];
```

#### 기본 예시

```sql
-- 전체 조회
SELECT * FROM sensor_log;

-- 특정 컬럼 조회
SELECT sensor_id, ts, value FROM sensor_log;

-- 컬럼 별칭
SELECT sensor_id AS id, value AS temp FROM sensor_log;

-- 수식 활용
SELECT sensor_id, value * 1.8 + 32 AS fahrenheit FROM sensor_log;
```

#### FROM 절 없는 SELECT

테이블 조회 없이 상수, 계산식, 함수 결과를 1행으로 반환합니다.

```sql
SELECT 1;
SELECT 'alive';
SELECT 1 + 2;
SELECT ABS(-7);
SELECT NOW;
```

#### CASE 문

```sql
-- 조건별 분기
SELECT sensor_id, value,
    CASE
        WHEN value > 80.0 THEN 'HIGH'
        WHEN value > 50.0 THEN 'NORMAL'
        ELSE 'LOW'
    END AS level
FROM sensor_log;

-- 컬럼 값 매핑
SELECT sensor_id,
    CASE status
        WHEN 'A' THEN 'ALARM'
        WHEN 'N' THEN 'NORMAL'
        ELSE 'UNKNOWN'
    END AS status_label
FROM device_status;
```

#### 서브쿼리

```sql
-- WHERE에서 서브쿼리
SELECT * FROM sensor_log
WHERE value > (SELECT AVG(value) FROM sensor_log);

-- SELECT 절에서 단일 값 서브쿼리
SELECT sensor_id, value,
    (SELECT MAX(value) FROM sensor_log) AS max_val
FROM sensor_log;

-- IN + 서브쿼리
SELECT * FROM sensor_log
WHERE sensor_id IN (
    SELECT sensor_id FROM alarm_threshold WHERE high_limit < 80.0
);
```

> Machbase는 상관 서브쿼리(외부 쿼리 컬럼 참조)를 지원하지 않습니다.

#### 집합 연산자 (UNION ALL)

Machbase는 `UNION ALL`만 지원합니다. 두 SELECT의 컬럼 수와 타입이 호환되어야 합니다.

```sql
SELECT sensor_id, value FROM sensor_log WHERE value > 90.0
UNION ALL
SELECT sensor_id, value FROM backup_log WHERE value > 90.0;
```

결과의 컬럼명은 좌측 SELECT의 컬럼명을 사용합니다.

#### 집계 함수

```sql
SELECT
    sensor_id,
    COUNT(*) AS cnt,
    AVG(value) AS avg_val,
    MAX(value) AS max_val,
    MIN(value) AS min_val,
    SUM(value) AS sum_val
FROM sensor_log
GROUP BY sensor_id;
```

<a id="where-order-limit"></a>
<a id="query-select-where-order-limit"></a>

### WHERE / ORDER BY / LIMIT

#### WHERE 절

일반적인 비교 연산자를 모두 사용할 수 있습니다.

```sql
SELECT * FROM sensor_log
WHERE value > 25.0 AND sensor_id = 'TEMP-01';

-- BETWEEN
SELECT * FROM sensor_log
WHERE value BETWEEN 20.0 AND 30.0;

-- IN
SELECT * FROM sensor_log
WHERE sensor_id IN ('TEMP-01', 'TEMP-02', 'PRESS-01');

-- IS NULL / IS NOT NULL
SELECT * FROM sensor_log WHERE status IS NULL;
SELECT * FROM sensor_log WHERE status IS NOT NULL;
```

#### ORDER BY

```sql
-- 오름차순 (기본)
SELECT * FROM sensor_log ORDER BY ts;

-- 내림차순
SELECT * FROM sensor_log ORDER BY ts DESC;

-- 다중 컬럼 정렬
SELECT * FROM sensor_log ORDER BY sensor_id, ts DESC;
```

TAG/LOG 테이블은 최신 데이터가 먼저 반환되는 경향이 있습니다. 명시적 정렬이 필요하면 ORDER BY를 지정하십시오.

#### LIMIT

결과 행 수를 제한합니다.

```sql
-- 최근 100건
SELECT * FROM sensor_log ORDER BY ts DESC LIMIT 100;

-- offset, count (100번째부터 50건)
SELECT * FROM sensor_log ORDER BY ts LIMIT 100, 50;
```

#### HAVING

GROUP BY와 함께 사용하여 집계 결과에 조건을 적용합니다.

```sql
SELECT sensor_id, AVG(value) AS avg_val
FROM sensor_log
GROUP BY sensor_id
HAVING AVG(value) > 30.0;
```

#### RANGE 연산자

현재 시각 기준으로 일정 기간 내의 데이터를 조회합니다.

```sql
-- 현재 기준 최근 1시간 데이터
SELECT * FROM sensor_log WHERE ts RANGE 1 HOUR;

-- 최근 30분
SELECT * FROM sensor_log WHERE ts RANGE 30 MINUTE;
```

`RANGE`는 `_ARRIVAL_TIME` 외의 DATETIME 컬럼에도 사용할 수 있습니다.

<a id="condition-time-duration"></a>
<a id="query-select-condition-time-duration"></a>

### 시간 조건과 DURATION

시계열 데이터 조회에서 시간 범위를 효율적으로 지정하는 방법입니다.

#### WHERE 시간 조건

DATETIME 컬럼에 직접 조건을 지정합니다.

```sql
-- 특정 시간 범위
SELECT * FROM sensor_log
WHERE ts BETWEEN '2024-01-15 00:00:00' AND '2024-01-15 23:59:59';

-- TO_DATE 함수 사용
SELECT * FROM sensor_log
WHERE ts >= TO_DATE('2024-01-15', 'YYYY-MM-DD')
  AND ts < TO_DATE('2024-01-16', 'YYYY-MM-DD');

-- TAG 테이블 시간 조건
SELECT name, time, value FROM tag
WHERE time BETWEEN '2024-01-15 00:00:00' AND '2024-01-15 12:00:00';
```

#### DURATION 키워드

`DURATION`은 `_ARRIVAL_TIME` 컬럼을 기준으로 조회 범위를 쉽고 빠르게 지정합니다. TAG 테이블에서는 BASETIME 컬럼 기준으로 동작합니다.

```sql
DURATION number {YEAR|MONTH|WEEK|DAY|HOUR|MINUTE|SECOND}
         [BEFORE number {YEAR|MONTH|WEEK|DAY|HOUR|MINUTE|SECOND}]

DURATION FROM expr TO expr
```

##### 기본 사용법

```sql
-- 최근 1시간 데이터
SELECT * FROM sensor_log DURATION 1 HOUR;

-- 최근 7일 데이터
SELECT * FROM sensor_log DURATION 7 DAY;

-- 최근 1개월
SELECT * FROM sensor_log DURATION 1 MONTH;
```

##### BEFORE 절

기준 시점 이전의 특정 구간을 조회합니다.

```sql
-- 1일 전 시점부터 1시간 구간
SELECT * FROM sensor_log DURATION 1 HOUR BEFORE 1 DAY;

-- 1주일 전 시점부터 1일 구간
SELECT * FROM sensor_log DURATION 1 DAY BEFORE 1 WEEK;
```

##### 명시적 범위

```sql
-- 특정 날짜 범위를 명시적으로 지정
SELECT * FROM sensor_log
DURATION FROM TO_DATE('2024-01-01', 'YYYY-MM-DD')
         TO   TO_DATE('2024-01-31', 'YYYY-MM-DD');
```

#### DURATION vs WHERE 시간 조건 비교

| 항목 | DURATION | WHERE 시간 조건 |
|------|---------|--------------|
| 조건 대상 | `_ARRIVAL_TIME` 또는 BASETIME | 사용자 지정 컬럼 |
| 상대 시간 | O (1 HOUR, 7 DAY 등) | 별도 계산 필요 |
| 성능 최적화 | 내부적으로 파티션 스캔 최적화 | 인덱스 활용 필요 |
| 명시적 범위 | DURATION FROM ... TO ... | BETWEEN / >=, <= |

**성능 팁**: 대용량 테이블에서는 `DURATION`을 사용하거나 인덱스가 있는 컬럼으로 WHERE 시간 조건을 지정하면 전체 스캔을 방지합니다.

<a id="relative-time"></a>
<a id="query-select-relative-time"></a>

### 상대 시간 표현

상대 시간 표현은 알려진 기준 시점으로부터의 차이를 SQL 문 안에서 직접 기술할 수 있도록 해 줍니다. 최근 계측 데이터를 필터링하거나 향후 작업을 예약하고, 보조 함수 호출 없이 시계열 윈도를 정렬해야 하는 운영자에게 유용합니다.

> **참고**: 이 기능은 Machbase 8.0.50 이상에서 지원됩니다.

#### 빠르게 살펴보기

```sql
-- 최근 1시간 데이터 조회
SELECT * FROM sensor_log WHERE event_time > now - 1h;

-- 2일 6시간 이후까지의 일정 확인
SELECT * FROM maintenance_plan WHERE planned_at < now + 2d6h;

-- 하위 초 단위까지 세그먼트 결합
SELECT to_char(now + 3s125ms10us4ns, 'YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn');
```

#### 구문 요약

- 리터럴은 공백 없이 이어지는 `<숫자><단위>` 세그먼트 하나 이상으로 작성합니다.
- 단위는 소문자를 사용하며, 서로 다른 크기는 이어 붙여 표현합니다(`2h30m`).
- `+` 또는 `-` 접두어를 붙이거나 산술식을 사용할 수 있습니다(`now - 90m`, `sample_time + 15s` 등).
- 숫자 뒤에 단위를 붙이지 않으면 나노초 단위로 해석됩니다.
- 상대 리터럴은 `INTERVAL`로 평가되며, `DATETIME`에 더하거나 빼면 결과 역시 `DATETIME`이 됩니다.

#### 지원 단위

| 접미사 | 의미 | 예시 | 동일한 기간 |
|--------|------|------|------------|
| `ns` | 나노초 | `500ns` | 500 나노초 |
| `us` | 마이크로초 | `20us` | 0.00002초 |
| `ms` | 밀리초 | `15ms` | 0.015초 |
| `s` | 초 | `45s` | 45초 |
| `m` | 분 | `30m` | 30분 |
| `h` | 시간 | `12h` | 12시간 |
| `d` | 일 | `7d` | 7일 |
| `w` | 주 | `2w` | 14일 |

> **참고**: 월과 연은 길이가 일정하지 않아 지원하지 않습니다. 지원하지 않는 접미사(`1y`, `1mo` 등)를 사용하면 `ERR-02034` (invalid time expression) 오류가 발생합니다.

#### 복합 리터럴 작성

- 가독성을 위해 가장 큰 단위부터 작성합니다(`5d4h30m`).
- 값이 0인 세그먼트는 생략합니다. `4h15m0s`보다는 `4h15m`이 좋습니다.
- 세그먼트 순서는 바뀌어도 되지만 일관성을 유지하면 실수를 줄일 수 있습니다. `1h30m`과 `30m1h`는 동일하게 평가됩니다.

#### 활용 패턴

##### 시간 구간 필터링

```sql
-- 최근 24시간 기록
SELECT *
  FROM rtrollup
 WHERE time BETWEEN now - 1d AND now;

-- 최근 10분 이내 발생한 알람
SELECT alert_id, level, occurred_at
  FROM alert_log
 WHERE occurred_at >= sysdate - 10m;

-- 최근 15분, 특정 센서
SELECT device_id, ts, value
  FROM metrics_stream
 WHERE ts BETWEEN now - 15m AND now
   AND device_id = 'sensor-01';
```

##### 향후 작업 예약

```sql
-- 다음 영업일 + 2시간 이내 실행할 작업
SELECT job_id, scheduled_at
  FROM job_queue
 WHERE scheduled_at <= now + 1d2h;

-- 30분 후 정비 일정 등록
INSERT INTO device_schedule (device_id, maintenance_due)
VALUES ('device-001', now + 30m);
```

##### 시간 기반 조인

```sql
-- 상대 오프셋을 이용해 두 소스를 조인 (±500ms 범위)
SELECT a.ts, a.value AS raw_value, b.value AS calibrated
  FROM raw_metrics a
  JOIN calibration b
    ON b.ts BETWEEN a.ts - 500ms AND a.ts + 500ms;
```

##### DATETIME 값과 캐스팅

```sql
SELECT to_char(to_date('2024-05-01', 'YYYY-MM-DD') + 3d,
               'YYYY-MM-DD');                              -- 2024-05-04

SELECT to_char(to_date('2024-05-01 08:00:00',
                       'YYYY-MM-DD HH24:MI:SS') - 4h15m,
               'YYYY-MM-DD HH24:MI:SS');                   -- 2024-05-01 03:45:00

SELECT to_char(to_date('2024-05-01', 'YYYY-MM-DD') + 2h30m45s250ms,
               'YYYY-MM-DD HH24:MI:SS mmm');               -- 2024-05-01 02:30:45 250
```

> 문자열 리터럴은 interval 산술에서 `DATETIME`으로 암시적 변환되지 않습니다. 먼저 `TO_DATE`로 변환해야 합니다.

##### 순수 숫자 (나노초)

```sql
-- 숫자 리터럴은 기본적으로 나노초이므로 정확히 1초가 더해집니다.
SELECT event_time + 1000000000 AS event_time_plus_1s
  FROM events;

-- 250나노초를 뺍니다.
SELECT event_time - 250 AS event_time_minus_250ns
  FROM events;
```

#### 동작 및 제한 사항

- 정밀도는 나노초까지 지원합니다. 64비트 범위를 넘으면 오버플로가 발생합니다.
- 인터벌 비교는 최종 `DATETIME` 값을 기준으로 이루어집니다. 인터벌 자체는 `ORDER BY` 절에서 사용할 수 없습니다.

#### 오류 처리

| 시나리오 | 오류 코드 | 해결 방법 |
|----------|-----------|-----------|
| 지원하지 않는 접미사(`1y`, `5mo`) | `ERR-02034` | 지원 단위(`30d` 등)로 교체합니다. |
| 단위 누락(`now + 10`) | 나노초로 해석됨 | 의도가 분/초라면 명시적으로 접미사를 붙입니다. |
| 값이 너무 큰 리터럴(`1000000d`) | `ERR_OVERFLOW_INTERVAL` | 크기를 줄이거나 반복 처리로 나눕니다. |
| 숫자가 아닌 문자 포함(`1h3xm`) | Invalid time expression | 오탈자를 수정합니다(`1h3m`). |

#### 참고 치트시트

```
패턴                                           의미
---------------------------------------------  ----------------------------------------
now - 5m                                       정확히 5분 전 시각
sysdate + 1d                                   시스템 시간 기준 24시간 후
col_ts + 90s                                   컬럼 값을 90초 뒤로 이동
TO_DATE('2024-01-01','YYYY-MM-DD') + 2w        날짜 값에 14일을 더함
value + 250                                    value에 250나노초를 더함
```

<a id="query-view"></a>
<a id="query-select-query-view"></a>

### VIEW 조회

저장 VIEW는 `CREATE VIEW`로 정의한 논리 객체로, SELECT 문에서 테이블처럼 사용합니다. 자주 쓰는 복잡한 조인이나 조건을 VIEW로 정의하면 쿼리를 단순화하고 재사용성을 높일 수 있습니다.

#### VIEW 조회

```sql
-- 저장 VIEW 조회
SELECT * FROM active_alarms;

SELECT sensor_id, location, value
FROM enriched_sensor_data
WHERE value > 80.0;
```

#### 저장 VIEW 목록 확인

```sql
SELECT VIEW_NAME, VIEW_TEXT FROM M$SYS_VIEWS;
```

#### DESC로 VIEW 구조 확인

```sql
DESC active_alarms;
```

#### VIEW 활용 예시

```sql
-- VIEW 정의: TAG + LOOKUP JOIN
CREATE VIEW sensor_with_meta AS
    SELECT t.name, t.time, t.value, l.location, l.dept
    FROM tag t
    LEFT JOIN device_meta l ON t.name = l.sensor_id;

-- VIEW 조회
SELECT name, time, value, location
FROM sensor_with_meta
WHERE time >= NOW - 3600000000000
  AND location = 'zone-1';

-- VIEW에 집계 적용
SELECT location, AVG(value) AS avg_temp
FROM sensor_with_meta
WHERE time >= NOW - 86400000000000
GROUP BY location
ORDER BY avg_temp DESC;
```

#### VIEW의 특성과 제한

- VIEW는 데이터를 물리적으로 저장하지 않습니다. 조회 시마다 정의된 쿼리를 실행합니다.
- INSERT/UPDATE/DELETE를 지원하지 않습니다. 읽기 전용입니다.
- VIEW는 다른 VIEW를 참조할 수 있습니다.
- TAG, LOG, TRANSACTION, VOLATILE, LOOKUP 모든 테이블 타입을 VIEW 정의에 포함할 수 있습니다.

> VIEW 생성·삭제 방법은 [4장 테이블 타입 개념과 선택](/dbms/data-modeling-table-design/schema-objects-definition/#create-view)를 참고하십시오.

<a id="query-cte"></a>
<a id="query-select-query-cte"></a>

### WITH / CTE

Machbase 8.6.0 Standard Edition은 비재귀 CTE(Common Table Expression)를 지원합니다. CTE는
한 SQL 문 안에서 `SELECT` 결과에 이름을 붙여 복잡한 조회를 단계별로 구성할 때 사용합니다.

```sql
WITH recent_data AS (
    SELECT device_id, value
    FROM sensor_data
    WHERE time >= NOW - 30m
),
device_avg AS (
    SELECT device_id, AVG(value) AS avg_value
    FROM recent_data
    GROUP BY device_id
)
SELECT device_id, avg_value
FROM device_avg
WHERE avg_value >= 80;
```

뒤 CTE는 앞 CTE를 참조할 수 있지만 전방 참조와 재귀 참조는 지원하지 않습니다. CTE는
인라인 뷰로 전개되므로 같은 CTE를 여러 번 참조하면 각 참조가 별도로 실행될 수 있습니다.
문법, 지원 문맥과 확장 한도는 [WITH / CTE syntax](/dbms/reference/sql/syntax-dictionary-sql/cte-syntax/)를
참고하십시오.

<a id="set-operators-union-intersect-except"></a>
<a id="query-select-set-operators-union-intersect-except"></a>

### 집합 연산: UNION ALL

Machbase는 복수 SELECT 결과를 결합하는 집합 연산으로 `UNION ALL`만 지원합니다.

#### UNION ALL

두 SELECT 결과를 중복 포함하여 합칩니다.

```sql
SELECT i1, i2 FROM table_1
UNION ALL
SELECT c1, c2 FROM table_2;
```

##### 사용 조건

- 좌측과 우측 SELECT의 **컬럼 수가 동일**해야 합니다.
- 대응하는 컬럼의 **타입이 호환 가능**해야 합니다.
  - 부호 있는 정수 ↔ 부호 없는 정수: 호환 불가
  - 정수 ↔ 실수: 호환 (결과는 실수 타입)
  - 문자열: 길이가 달라도 호환
  - IPv4 ↔ IPv6: 호환 불가
- 결과의 **컬럼명은 좌측 SELECT**의 컬럼명을 사용합니다.

##### 예시

```sql
-- 두 날짜 범위의 데이터 합치기
SELECT name, time, value FROM tag
WHERE time BETWEEN '2024-01-01' AND '2024-01-15'
UNION ALL
SELECT name, time, value FROM tag
WHERE time BETWEEN '2024-02-01' AND '2024-02-15';

-- 두 테이블의 데이터 통합
SELECT sensor_id AS id, ts AS time, value FROM sensor_log_2023
UNION ALL
SELECT sensor_id AS id, ts AS time, value FROM sensor_log_2024;

-- 두 집계 결과 합치기
SELECT 'zone-1' AS zone, AVG(value) FROM tag WHERE name LIKE 'ZONE1%' DURATION 1 DAY
UNION ALL
SELECT 'zone-2' AS zone, AVG(value) FROM tag WHERE name LIKE 'ZONE2%' DURATION 1 DAY;
```

#### UNION (DISTINCT) 미지원

Machbase는 `UNION ALL`만 지원하며, 중복 제거가 필요한 `UNION` (DISTINCT)은 지원하지 않습니다. 중복 제거가 필요하면 서브쿼리나 애플리케이션 레이어에서 처리하십시오.

```sql
-- 미지원
SELECT i1 FROM t1 UNION SELECT i1 FROM t2;
-- → 오류 발생

-- 대안: UNION ALL 후 애플리케이션에서 중복 제거
SELECT DISTINCT * FROM (
    SELECT i1 FROM t1
    UNION ALL
    SELECT i1 FROM t2
);
```

> INTERSECT, EXCEPT(MINUS)도 지원하지 않습니다.

<a id="hint-select"></a>
<a id="query-select-hint-select"></a>

### SELECT 힌트 사용

SELECT 힌트는 쿼리 최적화 방향을 명시적으로 지정하는 주석 형태의 지시어입니다.

#### 힌트 문법

```sql
SELECT /*+ hint_name(option) */ ...
```

#### 이 절에서 다루는 힌트

- **[SAMPLING 힌트](/dbms/performance-tuning/query-analysis/#hint-sampling)**: TAG 데이터 시간 구간별 샘플링
- **[INTERPOLATION 힌트](/dbms/performance-tuning/query-analysis/#hint-interpolation)**: TAG 데이터 누락 구간 보간

#### 기타 힌트

##### PARALLEL

병렬 처리 계수를 지정합니다.

```sql
SELECT /*+ PARALLEL(sensor_log, 8) */ sensor_id, AVG(value)
FROM sensor_log
GROUP BY sensor_id;
```

##### NOPARALLEL

병렬 처리를 사용하지 않도록 강제합니다.

```sql
SELECT /*+ NOPARALLEL(sensor_log) */ * FROM sensor_log WHERE value > 50.0;
```

##### FULL

인덱스를 사용하지 않고 전체 스캔을 수행합니다. 인덱스보다 풀 스캔이 유리한 경우에 사용합니다.

```sql
SELECT /*+ FULL(sensor_log) */ * FROM sensor_log WHERE value > 50.0;
```

##### NO_INDEX

특정 인덱스 사용을 방지합니다.

```sql
SELECT /*+ NO_INDEX(sensor_log, idx_value) */ * FROM sensor_log WHERE value > 50.0;
```

##### ROLLUP_TABLE

ROLLUP 조회 시 특정 ROLLUP 테이블을 강제 지정합니다.

```sql
SELECT /*+ ROLLUP_TABLE(tag, _rollup_tag_value_min) */ *
FROM tag WHERE name = 'TEMP-01' DURATION 1 DAY;
```

##### SCAN_FORWARD / SCAN_BACKWARD

스캔 방향을 지정합니다. 기본값은 역방향(최신 데이터 먼저)입니다.

```sql
-- 오래된 데이터부터 순방향 스캔
SELECT /*+ SCAN_FORWARD(sensor_log) */ * FROM sensor_log LIMIT 100;

-- 최신 데이터부터 역방향 스캔 (기본값과 동일)
SELECT /*+ SCAN_BACKWARD(sensor_log) */ * FROM sensor_log LIMIT 100;
```

##### RID_RANGE

특정 RID(Row ID) 범위의 데이터를 직접 조회합니다. 내부 디버깅이나 특정 구간 데이터 추출에 사용됩니다.

```sql
SELECT /*+ RID_RANGE(table_name, start_rid, end_rid) */ _RID, *
FROM table_name;
```

```sql
-- RID 45부터 50까지 데이터 조회
SELECT /*+ RID_RANGE(TEST, 45, 50) */ _RID, * FROM TEST;
```

> `_RID`는 Machbase 내부 행 식별자입니다. 일반적인 운영 쿼리에서는 사용하지 않으며, RID_RANGE 힌트도 디버깅 목적으로만 사용합니다.

<a id="hint-sampling"></a>
<a id="query-select-hint-select-hint-sampling"></a>

#### SAMPLING 힌트

`SAMPLING` 힌트는 TAG 테이블의 대용량 시계열 데이터를 시간 구간별로 균일하게 샘플링하여 반환합니다. 대시보드에서 전체 추세를 빠르게 파악할 때 유용합니다.

##### 구문

```sql
SELECT /*+ SAMPLING(time_column, interval, count) */ ...
FROM tag_table
WHERE ...;
```

- `time_column`: BASETIME 컬럼 이름
- `interval`: 샘플링 시간 단위 (`'1 sec'`, `'1 min'`, `'1 hour'` 등)
- `count`: 각 구간에서 반환할 최대 행 수

##### 예시

```sql
-- 1시간 범위를 1분 단위로 샘플링 (구간당 1건)
SELECT /*+ SAMPLING(time, '1 min', 1) */ name, time, value
FROM tag
WHERE name = 'TEMP-01' DURATION 1 HOUR;

-- 24시간 데이터를 1시간 단위로 샘플링
SELECT /*+ SAMPLING(time, '1 hour', 1) */ name, time, value
FROM tag
WHERE name = 'TEMP-01' DURATION 1 DAY;
```

##### SAMPLING vs ROLLUP

| 항목 | SAMPLING 힌트 | ROLLUP |
|------|-------------|--------|
| 동작 방식 | 구간별 N건 샘플 반환 | 구간별 AVG/MIN/MAX 집계 |
| 사전 계산 | X (조회 시 계산) | O (백그라운드 사전 계산) |
| 정확도 | 샘플 (근사치) | 정확한 집계 |
| 대시보드 활용 | 전체 추세 파악 | 정확한 통계 |

**팁**: 실시간 대시보드에서 빠른 렌더링이 필요하면 SAMPLING, 정확한 집계 값이 필요하면 ROLLUP을 사용하십시오.

<a id="hint-interpolation"></a>
<a id="query-select-hint-select-hint-interpolation"></a>

#### INTERPOLATION 힌트

`INTERPOLATION` 힌트는 TAG 테이블의 시계열 데이터에서 누락된 시간 구간을 자동으로 채워 반환합니다.

##### 구문

```sql
SELECT /*+ INTERPOLATION(time_column) */ ...
FROM tag_table
WHERE ...;
```

##### 기본 예시

```sql
-- 1분 간격 데이터에서 누락 구간을 선형 보간
SELECT /*+ INTERPOLATION(time) */ name, time, value
FROM tag
WHERE name = 'TEMP-01' DURATION 1 HOUR;
```

누락된 타임스탬프 구간에 대해 인접 값 사이를 선형 보간(linear interpolation)한 행이 자동으로 채워져 반환됩니다.

##### INTERPOLATION과 함께 사용

```sql
-- 보간 + 특정 태그
SELECT /*+ INTERPOLATION(time) */ name, time, value
FROM tag
WHERE name IN ('TEMP-01', 'TEMP-02') DURATION 1 DAY;
```

##### 보간 방식

- **선형 보간**: 앞뒤 실제 값 사이를 직선으로 보간
- 누락 구간의 시작/끝에 실제 데이터가 없으면 보간을 수행하지 않습니다.

##### 활용 패턴

```sql
-- 보간 후 PIVOT으로 컬럼화
SELECT * FROM (
    SELECT /*+ INTERPOLATION(time) */ name, time, value
    FROM tag WHERE DURATION 1 HOUR
) PIVOT (AVG(value) FOR name IN ('TEMP-01', 'TEMP-02', 'PRESS-01'));
```

##### INTERPOLATION vs SERIES BY

| 항목 | INTERPOLATION 힌트 | SERIES BY |
|------|-----------------|---------|
| 용도 | 누락 시간 구간 채우기 | 연속 조건 만족 구간 추출 |
| 대상 | TAG 테이블 | 모든 테이블 |
| 결과 | 보간된 행 자동 추가 | 조건 만족 행만 반환 |

<a id="execution-plan-explain"></a>
<a id="query-select-execution-plan-explain"></a>

### EXPLAIN으로 실행 계획 확인

`EXPLAIN`은 SELECT 쿼리의 실행 계획을 출력합니다. 데이터를 실제로 조회하지 않고 옵티마이저가 선택한 스캔 방식·인덱스 사용 여부를 확인할 수 있습니다.

#### 구문

```sql
EXPLAIN SELECT ...;
EXPLAIN FULL WITH cte_name AS (SELECT ...) SELECT ... FROM cte_name;
```

#### 예시

```sql
-- 인덱스 사용 확인
EXPLAIN SELECT sensor_id, value
FROM sensor_log
WHERE sensor_id = 'TEMP-01';
```

```
PLAN
-----------------------------------------------------------
 PROJECT
  INDEX SCAN
   *BITMAP RANGE (table id:3, column id:2, index id:4)
   [KEY RANGE]
    * sensor_id = 'TEMP-01'
```

```sql
-- 병렬 처리 힌트 적용 확인
EXPLAIN SELECT /*+ PARALLEL(sensor_log, 8) */ sensor_id, AVG(value)
FROM sensor_log
GROUP BY sensor_id;
```

```
PLAN
-----------------------------------------------------------
 PROJECT
  GROUP AGGREGATE
   PARALLEL INDEX SCAN
    *BITMAP RANGE (table id:3, column id:2, index id:4)
```

#### 실행 계획 항목 설명

| 항목 | 설명 |
|------|------|
| `FULL SCAN` | 인덱스 없이 전체 테이블 스캔 |
| `INDEX SCAN` | 인덱스를 사용한 범위 스캔 |
| `PARALLEL INDEX SCAN` | 병렬 인덱스 스캔 |
| `BITMAP RANGE` | BITMAP 인덱스 범위 스캔 |
| `KEY RANGE` | 실제 적용된 인덱스 조건 |
| `FILTER` | 인덱스 적용 후 추가 필터 조건 |
| `GROUP AGGREGATE` | GROUP BY 집계 처리 |
| `PROJECT` | SELECT 대상 목록 처리 |

#### 활용 팁

- `FULL SCAN`이 나타나면 WHERE 조건에 인덱스가 없는 것입니다. 인덱스를 추가하거나 힌트로 스캔 방향을 조정하십시오.
- `DURATION`을 사용하면 `_ARRIVAL_TIME` 기준 파티션 가지치기가 적용되어 스캔 범위가 줄어듭니다.
- CTE는 각 참조가 인라인 뷰로 전개되므로 반복 참조의 스캔과 JOIN 계획을 각각 확인하십시오.
- 대용량 테이블에서 느린 쿼리는 `EXPLAIN` 결과를 먼저 확인하십시오.

<a id="item"></a>

## 고급 조회 항목

Machbase는 시계열 데이터 분석에 필요한 다양한 고급 SQL 기능을 제공합니다. 기본 SELECT 조회에서 한 단계 나아가, 데이터를 집계·변환·보간·연산하는 분석 쿼리를 작성할 수 있습니다.

### 이 절에서 다루는 내용

- **[집계 함수와 GROUP BY](/dbms/performance-tuning/query-analysis/#aggregation-group)**: COUNT, SUM, AVG 등 집계 함수와 GROUP BY, HAVING 절 사용법
- **[GROUP_CONCAT](/dbms/performance-tuning/query-analysis/#aggregation-group-concat)**: 그룹 내 값을 하나의 문자열로 이어 붙이는 함수
- **[JOIN](/dbms/performance-tuning/query-analysis/#join)**: 시계열 테이블과 참조 테이블의 결합, 메타데이터 조인 패턴
- **[PIVOT](/dbms/performance-tuning/query-analysis/#pivot)**: 행을 열로 변환하여 여러 센서 값을 나란히 비교
- **[윈도우 함수와 OVER](/dbms/performance-tuning/query-analysis/#window-functions-over)**: 이동 평균, 순위 등 윈도우 기반 분석 연산
- **[보간 조회와 SERIES BY](/dbms/performance-tuning/query-analysis/#query-interpolation-series)**: 누락 구간을 채우는 보간 및 SERIES BY 절
- **[ROLLUP](/dbms/tag-rollup-usage/overview-use-criteria/#rollup)**: 시간 축 기반 자동 집계와 다단계 시간 해상도 조회

<a id="aggregation-group"></a>
<a id="item-aggregation-group"></a>

### 집계 함수와 GROUP BY

집계 함수(Aggregate Function)는 여러 행의 값을 하나의 결과로 요약합니다. Machbase는 표준 SQL 집계 함수를 지원하며, GROUP BY와 HAVING 절을 함께 사용하여 그룹별 집계를 수행할 수 있습니다.

#### 지원 집계 함수

| 함수 | 설명 |
|------|------|
| `COUNT(*)` | 전체 행 수 |
| `COUNT(col)` | NULL이 아닌 값의 수 |
| `SUM(col)` | 합계 |
| `AVG(col)` | 평균 |
| `MIN(col)` | 최솟값 |
| `MAX(col)` | 최댓값 |
| `SUMSQ(col)` | 제곱합 |
| `STDDEV(col)` | 표준편차 |
| `VARIANCE(col)` | 분산 |

#### GROUP BY 기본 사용법

GROUP BY 절은 지정한 컬럼의 값이 같은 행들을 하나의 그룹으로 묶고, 각 그룹에 집계 함수를 적용합니다.

```sql
-- LOG 테이블: 장비 유형별 측정값 평균
SELECT device_type, AVG(value) AS avg_value, COUNT(*) AS cnt
FROM sensor_log
WHERE time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-02')
GROUP BY device_type;
```

```sql
-- TAG 테이블: 센서 이름별 최대·최솟값
SELECT name, MIN(value) AS min_val, MAX(value) AS max_val
FROM tag
WHERE time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-02')
GROUP BY name;
```

##### HAVING 절

HAVING은 집계 결과에 조건을 적용합니다. WHERE가 행 수준 필터라면, HAVING은 그룹 수준 필터입니다.

```sql
-- 하루 평균이 50 이상인 센서만 조회
SELECT name, AVG(value) AS avg_val
FROM tag
WHERE time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-02')
GROUP BY name
HAVING AVG(value) >= 50;
```

#### NULL 처리

집계 함수는 기본적으로 NULL 값을 무시합니다. `COUNT(*)`는 NULL 포함 전체 행을 세지만, `COUNT(col)`은 해당 컬럼이 NULL인 행을 제외합니다.

```sql
-- col에 NULL이 있는 경우 두 결과가 다를 수 있음
SELECT COUNT(*), COUNT(value) FROM sensor_log;
```

#### 시계열 데이터에서의 주의 사항

> **주의**: TAG 테이블에서 단순 GROUP BY를 사용하면 전체 기간의 값을 하나의 그룹으로 처리합니다. 시간 축을 기준으로 일정 간격마다 집계하려면 [ROLLUP](/dbms/tag-rollup-usage/overview-use-criteria/#rollup)을 사용하십시오. ROLLUP은 시간 해상도(초, 분, 시간 등)를 지정하여 자동으로 시간 버킷을 만들어 줍니다.

```sql
-- 잘못된 예: 전체 기간을 하나의 그룹으로 집계
SELECT name, AVG(value) FROM tag GROUP BY name;

-- 올바른 예: 1시간 단위로 집계하려면 ROLLUP 사용
SELECT name, AVG(value)
FROM tag
GROUP BY name
ROLLUP (time, 1 HOUR);
```

#### LOG 테이블과 TAG 테이블 비교

LOG 테이블은 임의 컬럼을 GROUP BY 기준으로 사용할 수 있습니다. TAG 테이블은 `name` 컬럼을 그룹 기준으로 자주 사용하며, 시간 축 집계는 ROLLUP을 병행하는 것이 권장됩니다.

```sql
-- LOG 테이블: 여러 컬럼을 GROUP BY 기준으로 사용
SELECT factory, line, AVG(temperature) AS avg_temp
FROM production_log
WHERE time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-02-01')
GROUP BY factory, line
ORDER BY factory, line;
```

<a id="aggregation-group-concat"></a>
<a id="item-aggregation-group-concat"></a>

### GROUP_CONCAT

`GROUP_CONCAT`은 그룹 내 여러 행의 값을 하나의 문자열로 이어 붙이는 집계 함수입니다. 쿼리 결과를 쉼표로 구분된 목록으로 가공하거나, 센서 이름·상태 값 등을 한 셀에 요약할 때 유용합니다.

#### 기본 문법

```sql
GROUP_CONCAT(column [SEPARATOR 'sep'])
```

- `column`: 이어 붙일 값이 있는 컬럼
- `SEPARATOR 'sep'`: 구분자를 지정합니다. 생략하면 기본값 `,`(쉼표)가 사용됩니다.

#### 기본 사용 예시

##### 위치별 센서 이름 목록 만들기

```sql
-- 각 위치에 설치된 센서 이름을 쉼표로 나열
SELECT location, GROUP_CONCAT(sensor_name) AS sensors
FROM sensor_meta
GROUP BY location;
```

결과 예시:

| location | sensors |
|----------|---------|
| 1공장 | temp_01,temp_02,pressure_01 |
| 2공장 | temp_03,flow_01 |

##### 구분자 변경

```sql
-- 세미콜론으로 구분
SELECT location, GROUP_CONCAT(sensor_name SEPARATOR '; ') AS sensors
FROM sensor_meta
GROUP BY location;
```

#### TAG 테이블 활용 예시

TAG 테이블의 메타데이터나 LOOKUP 테이블과 조합하면 특정 조건에 해당하는 태그명 목록을 한 번에 조회할 수 있습니다.

```sql
-- 상태가 'ACTIVE'인 센서 이름을 그룹별로 나열
SELECT factory, GROUP_CONCAT(tag_name SEPARATOR ', ') AS active_sensors
FROM tag_metadata
WHERE status = 'ACTIVE'
GROUP BY factory;
```

```sql
-- 특정 시간대에 이상값이 발생한 센서 목록
SELECT GROUP_CONCAT(DISTINCT name SEPARATOR ', ') AS alert_sensors
FROM tag
WHERE time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-02')
  AND value > 100;
```

#### 결과 길이 제한

> **주의**: `GROUP_CONCAT`의 결과 문자열 길이에는 내부 제한이 있습니다. 그룹 내 행 수가 매우 많을 경우 문자열이 잘릴 수 있으므로, 대량 데이터보다는 메타 정보나 코드 목록처럼 항목 수가 적은 경우에 사용하는 것이 적합합니다.

#### 활용 패턴

| 패턴 | 설명 |
|------|------|
| 코드 목록 조회 | 그룹별 코드·이름 값을 단일 행으로 반환 |
| 태그 이름 집합 | 공장/라인별 센서 이름을 하나의 컬럼으로 요약 |
| 상태 값 나열 | 시간대별 발생한 이벤트 코드를 순서대로 연결 |
| 동적 IN 목록 | 애플리케이션에서 후속 쿼리의 IN 조건에 사용할 목록 생성 |

#### 관련 항목

- [집계 함수와 GROUP BY](/dbms/performance-tuning/query-analysis/#item-aggregation-group): COUNT, AVG 등 일반 집계 함수
- [JOIN](#item-join): 메타데이터 테이블과의 조인으로 풍부한 정보 조회

<a id="item-join"></a>

### JOIN

JOIN은 두 개 이상의 테이블을 연결하여 하나의 결과 집합으로 조회하는 SQL 연산입니다. Machbase에서는 대용량 시계열 테이블(TAG/LOG)과 소규모 참조 테이블(LOOKUP/VOLATILE)을 결합하는 패턴이 가장 일반적입니다.

#### 지원 JOIN 유형

| 유형 | 설명 |
|------|------|
| INNER JOIN | 두 테이블에서 조인 조건을 만족하는 행만 반환 |
| LEFT OUTER JOIN | 왼쪽 테이블의 모든 행과 오른쪽 테이블의 일치 행 반환, 일치하지 않으면 NULL |
| 암묵적 JOIN | FROM 절에 쉼표로 테이블을 나열하고 WHERE에서 조인 조건 지정 |

#### 기본 문법

##### INNER JOIN (명시적)

```sql
SELECT a.컬럼, b.컬럼
FROM 테이블A a
INNER JOIN 테이블B b ON a.키 = b.키
WHERE 조건;
```

##### 암묵적 JOIN (쉼표 구문)

```sql
SELECT a.컬럼, b.컬럼
FROM 테이블A a, 테이블B b
WHERE a.키 = b.키
  AND 추가조건;
```

#### TAG 테이블과 메타데이터 조인

TAG 테이블은 센서 값을 저장하고, 별도 메타데이터 테이블은 센서의 위치·단위·설명 등 부가 정보를 보관합니다. JOIN을 통해 두 정보를 결합합니다.

```sql
-- 센서 값과 위치 정보를 함께 조회
SELECT
    t.time,
    t.name,
    t.value,
    m.location,
    m.unit
FROM tag t
INNER JOIN tag_meta m ON t.name = m.name
WHERE t.time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-02')
  AND m.location = '1공장'
ORDER BY t.time;
```

#### LOOKUP 테이블을 활용한 참조 값 조인

LOOKUP 테이블은 자주 조인하는 소규모 참조 데이터를 메모리에 유지하므로 조인 성능이 우수합니다.

```sql
-- 센서 측정값에 허용 임계값 정보를 함께 조회
SELECT
    t.time,
    t.name,
    t.value,
    r.threshold_high,
    r.threshold_low,
    CASE
        WHEN t.value > r.threshold_high THEN 'HIGH'
        WHEN t.value < r.threshold_low  THEN 'LOW'
        ELSE 'NORMAL'
    END AS status
FROM tag t
INNER JOIN ref_threshold r ON t.name = r.sensor_name
WHERE t.time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-02');
```

#### LEFT OUTER JOIN

오른쪽 테이블에 일치하는 행이 없어도 왼쪽 테이블의 행을 모두 유지합니다. 메타 정보가 없는 센서도 누락 없이 조회해야 할 때 사용합니다.

```sql
-- 메타 정보가 없는 센서도 포함하여 조회 (미등록 센서는 NULL로 표시)
SELECT
    t.time,
    t.name,
    t.value,
    m.location,
    m.description
FROM tag t
LEFT OUTER JOIN tag_meta m ON t.name = m.name
WHERE t.time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-02');
```

#### 서브쿼리를 FROM 절에서 사용

집계 결과나 필터링된 데이터를 인라인 뷰로 활용하여 JOIN할 수 있습니다.

```sql
-- 센서별 일 평균과 메타 정보를 함께 조회
SELECT avg_t.name, avg_t.avg_value, m.location
FROM (
    SELECT name, AVG(value) AS avg_value
    FROM tag
    WHERE time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-02')
    GROUP BY name
) avg_t
INNER JOIN tag_meta m ON avg_t.name = m.name
ORDER BY avg_t.avg_value DESC;
```

#### 성능 권장 사항

> **팁**: JOIN에서 큰 테이블(TAG/LOG)을 왼쪽에, 작은 참조 테이블(LOOKUP/VOLATILE/메타)을 오른쪽에 배치하십시오. Machbase는 오른쪽 테이블을 기준으로 해시 또는 인덱스 조인을 수행하므로, 참조 테이블이 작을수록 성능이 향상됩니다.

> **주의**: TAG 테이블끼리의 대용량 JOIN은 성능에 큰 부담을 줄 수 있습니다. TAG-TAG JOIN이 필요한 경우 반드시 시간 범위 조건을 지정하고, 결과 크기를 LIMIT로 제한하는 것을 권장합니다.

#### 제한 사항

- CROSS JOIN은 대용량 테이블에서 지원되지 않습니다.
- TAG 테이블 간 JOIN 시 양쪽 모두 시간 조건을 명시하는 것이 필수입니다.
- OUTER JOIN에서 집계 함수를 사용할 경우 NULL 값 처리에 주의가 필요합니다.

#### 관련 항목

- [PIVOT](#item-pivot): JOIN 결과를 열 방향으로 변환
- [집계 함수와 GROUP BY](/dbms/performance-tuning/query-analysis/#item-aggregation-group): JOIN 후 그룹별 집계
- [조건 검색 - TAG 메타데이터 조회](/dbms/tag-table-usage/tag-metadata/#metadata-query-tag): FROM TAG METADATA 구문

<a id="item-pivot"></a>

### PIVOT

PIVOT은 행(row) 방향의 데이터를 열(column) 방향으로 변환하는 연산입니다. 여러 센서의 측정값을 시간대별로 나란히 비교하거나, 코드 값을 컬럼 헤더로 표현할 때 활용합니다.

#### 기본 문법

```sql
SELECT *
FROM (서브쿼리)
PIVOT (
    집계함수(값_컬럼)
    FOR 피벗_컬럼 IN ('값1' "alias1", '값2' "alias2", ...)
);
```

- **서브쿼리**: PIVOT 대상이 될 원본 데이터를 반환합니다. 일반적으로 피벗 기준 컬럼, 피벗 대상 컬럼, 값 컬럼을 포함합니다.
- **집계함수**: `AVG`, `SUM`, `MIN`, `MAX`, `COUNT` 등을 사용합니다.
- **FOR 피벗_컬럼 IN (...)**: 행 값을 열 이름으로 변환할 컬럼과 대상 값 목록을 지정합니다.

> **주의**: PIVOT의 열 목록(`IN` 절)은 쿼리 실행 시점에 정적으로 지정해야 합니다. 동적으로 열을 생성하는 기능은 지원되지 않으며, 열 이름은 미리 알고 있어야 합니다.

#### 센서별 평균값 비교 예시

여러 센서의 평균값을 한 행으로 나란히 조회합니다.

```sql
-- 원본 데이터: (time, name, value) 형태의 TAG 테이블
SELECT *
FROM (
    SELECT
        DATE_TRUNC('hour', time) AS hour,
        name,
        value
    FROM tag
    WHERE time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-02')
      AND name IN ('temp_01', 'temp_02', 'pressure_01')
)
PIVOT (
    AVG(value)
    FOR name IN (
        'temp_01'     "temp_01",
        'temp_02'     "temp_02",
        'pressure_01' "pressure_01"
    )
)
ORDER BY hour;
```

결과 예시:

| hour | temp_01 | temp_02 | pressure_01 |
|------|-----------|-----------|-----------|
| 2024-01-01 00:00 | 22.5 | 23.1 | 101.3 |
| 2024-01-01 01:00 | 22.8 | 23.4 | 101.5 |
| 2024-01-01 02:00 | 21.9 | 22.7 | 100.8 |

#### 최대·최솟값 PIVOT

집계 함수를 바꾸면 동일한 구조로 최대·최솟값 비교도 가능합니다.

```sql
SELECT *
FROM (
    SELECT name, value
    FROM tag
    WHERE time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-02-01')
      AND name IN ('sensor_A', 'sensor_B', 'sensor_C', 'sensor_D', 'sensor_E')
)
PIVOT (
    MAX(value)
    FOR name IN (
        'sensor_A' "A_MAX",
        'sensor_B' "B_MAX",
        'sensor_C' "C_MAX",
        'sensor_D' "D_MAX",
        'sensor_E' "E_MAX"
    )
);
```

#### 상태 코드를 열로 변환하는 예시

숫자나 코드 값을 열로 펼쳐 각 상태별 발생 횟수를 비교할 수 있습니다.

```sql
SELECT *
FROM (
    SELECT factory, status_code
    FROM event_log
    WHERE time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-02-01')
)
PIVOT (
    COUNT(*)
    FOR status_code IN (
        '0' "NORMAL",
        '1' "WARNING",
        '2' "ERROR",
        '3' "CRITICAL"
    )
)
ORDER BY factory;
```

#### ROLLUP 결과를 PIVOT으로 변환

ROLLUP으로 시간 집계한 결과를 PIVOT으로 열 변환하면 시간대별 센서 비교 대시보드 데이터를 얻을 수 있습니다.

```sql
SELECT *
FROM (
    SELECT
        DATE_TRUNC('hour', time) AS hour,
        name,
        AVG(value) AS avg_val
    FROM tag
    WHERE time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-02')
      AND name IN ('inlet_temp', 'outlet_temp', 'flow_rate')
    GROUP BY hour, name
)
PIVOT (
    AVG(avg_val)
    FOR name IN (
        'inlet_temp'  "inlet_temp",
        'outlet_temp' "outlet_temp",
        'flow_rate'   "flow_rate"
    )
)
ORDER BY hour;
```

#### 활용 시 고려사항

| 항목 | 내용 |
|------|------|
| 열 목록 | 쿼리 작성 시 고정된 값 목록만 지원 |
| 집계 함수 | AVG, SUM, MIN, MAX, COUNT 사용 가능 |
| 결과 테이블 | 피벗 기준 컬럼 1개 + 지정한 값 수만큼의 열로 구성 |
| NULL 처리 | 해당 시간대에 데이터가 없으면 NULL로 채워짐 |

#### 관련 항목

- [ROLLUP](/dbms/tag-rollup-usage/overview-use-criteria/#rollup): 시간 축 기반 자동 집계
- [JOIN](#item-join): 메타데이터와 결합하여 풍부한 컬럼 구성
- [집계 함수와 GROUP BY](/dbms/performance-tuning/query-analysis/#item-aggregation-group): PIVOT 내부에 사용하는 집계 함수

<a id="window-functions-over"></a>
<a id="item-window-functions-over"></a>

### 윈도우 함수 (OVER)

윈도우 함수(Window Function)는 현재 행과 관련된 행 집합(윈도우)에 대해 계산을 수행하는 함수입니다. `GROUP BY`와 달리 결과 행을 그룹으로 축소하지 않고 모든 행을 유지한 채로 집계 또는 순위 연산을 수행할 수 있습니다.

#### 지원 함수

SQL `OVER` 절과 함께 사용할 수 있는 함수는 다음과 같습니다.

| 함수 | 설명 |
|------|------|
| `LAG(col, n)` | 현재 행 기준 n행 이전의 값을 반환 |
| `LEAD(col, n)` | 현재 행 기준 n행 이후의 값을 반환 |
| `NTILE(n)` | 결과 집합을 n개의 동등한 버킷으로 나누고 버킷 번호를 반환 |

#### 기본 문법

```sql
함수() OVER (
    [PARTITION BY 파티션_컬럼, ...]
    [ORDER BY 정렬_컬럼 [ASC | DESC]]
)
```

- **PARTITION BY**: 윈도우 계산을 수행할 데이터 그룹을 정의합니다. 생략하면 전체 결과 집합이 하나의 윈도우가 됩니다.
- **ORDER BY**: 윈도우 내에서 행의 순서를 결정합니다. `LAG`, `LEAD`, `NTILE`처럼 순서가 중요한 함수에서 사용합니다.

#### 사용 예시

##### 이전 행과의 비교 (LAG)

```sql
SELECT
    time,
    value,
    LAG(value, 1) OVER (PARTITION BY sensor_id ORDER BY time) AS prev_value,
    value - LAG(value, 1) OVER (PARTITION BY sensor_id ORDER BY time) AS delta
FROM sensor_data;
```

##### 버킷 번호 부여 (NTILE)

```sql
SELECT
    NTILE(4) OVER (PARTITION BY tag_name ORDER BY value) AS bucket_no,
    tag_name,
    time,
    value
FROM tag_data
WHERE time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-02');
```

##### 다음 행 참조 (LEAD)

```sql
SELECT
    sensor_id,
    time,
    value,
    LEAD(value, 1) OVER (PARTITION BY sensor_id ORDER BY time) AS next_value
FROM sensor_data;
```

#### 지원 테이블 유형

윈도우 함수는 Machbase의 주요 테이블 유형 모두에서 사용할 수 있습니다.

| 테이블 유형 | 지원 여부 |
|------------|----------|
| LOG 테이블 | 지원 |
| TRANSACTION 테이블 | 지원 |
| VOLATILE 테이블 | 지원 |
| TAG 테이블 | 지원 (시간 범위 조건과 함께 사용 권장) |

#### 주의사항

> **윈도우 함수는 WHERE 절에서 직접 사용할 수 없습니다.**
> 윈도우 함수의 결과를 필터링하려면 서브쿼리를 사용해야 합니다.

```sql
-- 잘못된 예시 (오류 발생)
SELECT * FROM sensor_data
WHERE LAG(value, 1) OVER (ORDER BY time) IS NOT NULL;

-- 올바른 예시 (서브쿼리 사용)
SELECT * FROM (
    SELECT
        time, value,
        LAG(value, 1) OVER (ORDER BY time) AS prev_value
    FROM sensor_data
)
WHERE prev_value IS NOT NULL;
```

> **성능 고려사항**: 윈도우 함수는 내부적으로 정렬을 수행하므로 대용량 데이터에서는 적절한 시간 범위 조건을 함께 사용하는 것을 권장합니다.

#### 하위 문서

- [LAG / LEAD](/dbms/performance-tuning/query-analysis/#lag-lead): 이전/다음 행 값 참조
- [NTILE](/dbms/performance-tuning/query-analysis/#ntile): 결과를 n개 버킷으로 분할
- [PARTITION BY / ORDER BY](/dbms/performance-tuning/query-analysis/#partition-order): 윈도우 정의 방법

<a id="lag-lead"></a>
<a id="item-window-functions-over-lag-lead"></a>

#### LAG / LEAD

`LAG`와 `LEAD`는 현재 행을 기준으로 이전 또는 이후 행의 값을 참조하는 윈도우 함수입니다. 시계열 데이터에서 변화량(delta)을 계산하거나, 이전 측정값과 현재 측정값을 비교하는 데 유용합니다.

##### 문법

```sql
LAG(컬럼, 오프셋) OVER (
    [PARTITION BY 파티션_컬럼]
    ORDER BY 정렬_컬럼
)

LEAD(컬럼, 오프셋) OVER (
    [PARTITION BY 파티션_컬럼]
    ORDER BY 정렬_컬럼
)
```

| 인자 | 설명 |
|------|------|
| `컬럼` | 참조할 컬럼 이름 |
| `오프셋` | 현재 행으로부터 몇 행 앞/뒤를 참조할지 지정 (기본값: 1) |

- **LAG**: 현재 행 기준 `오프셋`만큼 **이전** 행의 값을 반환합니다.
- **LEAD**: 현재 행 기준 `오프셋`만큼 **이후** 행의 값을 반환합니다.

> **ORDER BY는 필수입니다.** `LAG`/`LEAD`는 행의 순서에 의존하므로 `OVER` 절에 반드시 `ORDER BY`를 명시해야 합니다.

##### 예시

###### 이전 측정값과의 차이(변화량) 계산

센서 데이터에서 각 측정값이 직전 측정값과 얼마나 차이나는지 계산합니다.

```sql
SELECT
    time,
    sensor_id,
    value,
    LAG(value, 1) OVER (
        PARTITION BY sensor_id
        ORDER BY time
    ) AS prev_value,
    value - LAG(value, 1) OVER (
        PARTITION BY sensor_id
        ORDER BY time
    ) AS delta
FROM sensor_data
WHERE time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-02');
```

###### 1분 전 값과 현재 값 비교

```sql
SELECT
    time,
    tag_name,
    value AS current_value,
    LAG(value, 1) OVER (
        PARTITION BY tag_name
        ORDER BY time
    ) AS prev_1min_value
FROM tag_data
WHERE time BETWEEN TO_DATE('2024-06-01 00:00:00') AND TO_DATE('2024-06-01 01:00:00');
```

###### 다음 행 값 참조 (LEAD)

```sql
SELECT
    time,
    sensor_id,
    value,
    LEAD(value, 1) OVER (
        PARTITION BY sensor_id
        ORDER BY time
    ) AS next_value
FROM sensor_data;
```

###### 이상 감지: 이전 값 대비 급격한 변화 탐지

서브쿼리를 활용하여 직전 값 대비 일정 비율 이상 변화한 행만 필터링합니다.

```sql
SELECT *
FROM (
    SELECT
        time,
        sensor_id,
        value,
        LAG(value, 1) OVER (
            PARTITION BY sensor_id
            ORDER BY time
        ) AS prev_value
    FROM sensor_data
    WHERE time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-02')
)
WHERE prev_value IS NOT NULL
  AND ABS(value - prev_value) / prev_value > 0.2;  -- 20% 이상 변화
```

##### NULL 처리

오프셋이 범위를 벗어나는 경우(예: 첫 번째 행에서 LAG를 사용할 때) `NULL`이 반환됩니다.

```text
-- 첫 번째 행의 prev_value는 NULL로 반환됨
LAG(value, 1) OVER (ORDER BY time)
```

> **성능 고려사항**: `LAG`/`LEAD`는 내부적으로 데이터를 정렬한 후 처리합니다. 대용량 테이블에서는 쿼리 시간 범위를 제한하거나 `PARTITION BY` 조건을 적절히 지정하여 처리 대상 데이터를 줄이는 것을 권장합니다.

<a id="item-window-functions-over-ntile"></a>

#### NTILE

`NTILE(n)`은 결과 집합을 `n`개의 동등한 크기의 버킷으로 나누고, 각 행에 해당 버킷 번호를 부여하는 윈도우 함수입니다. 백분위수 계산, 사분위수 분석, 데이터 구간 분류 등에 활용합니다.

##### 문법

```sql
NTILE(버킷_수) OVER (
    [PARTITION BY 파티션_컬럼]
    ORDER BY 정렬_컬럼
)
```

| 인자 | 설명 |
|------|------|
| `버킷_수` | 결과를 나눌 버킷의 수 (양의 정수) |

- 행 수가 `버킷_수`로 나누어 떨어지지 않으면, 앞쪽 버킷이 한 행씩 더 가집니다.
- 버킷 번호는 1부터 시작합니다.

> **ORDER BY는 필수입니다.** 버킷 할당은 지정된 순서에 따라 이루어지므로 반드시 `ORDER BY`를 명시해야 합니다.

##### 예시

###### 사분위수(Quartile) 분류

센서 측정값을 4개 구간으로 나누어 각 행에 사분위수 번호를 부여합니다.

```sql
SELECT
    time,
    sensor_id,
    value,
    NTILE(4) OVER (
        PARTITION BY sensor_id
        ORDER BY value
    ) AS quartile
FROM sensor_data
WHERE time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-02-01');
```

결과에서 `quartile = 1`은 하위 25%, `quartile = 4`는 상위 25%에 해당하는 행입니다.

###### 백분위수 버킷 할당

100개의 버킷으로 나누어 백분위수를 근사 계산합니다.

```sql
SELECT
    sensor_id,
    value,
    NTILE(100) OVER (
        PARTITION BY sensor_id
        ORDER BY value
    ) AS percentile_bucket
FROM sensor_data
WHERE time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-02-01');
```

###### 버킷별 통계 계산

외부 쿼리와 결합하여 각 사분위수 버킷의 평균과 최대/최소값을 구합니다.

```sql
SELECT
    sensor_id,
    quartile,
    COUNT(*)    AS row_count,
    MIN(value)  AS min_value,
    MAX(value)  AS max_value,
    AVG(value)  AS avg_value
FROM (
    SELECT
        sensor_id,
        value,
        NTILE(4) OVER (
            PARTITION BY sensor_id
            ORDER BY value
        ) AS quartile
    FROM sensor_data
    WHERE time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-02-01')
)
GROUP BY sensor_id, quartile
ORDER BY sensor_id, quartile;
```

##### NTILE 활용 기준

`NTILE`은 정확한 순위가 아니라 정렬된 결과를 균등한 구간으로 나누는 데 사용합니다.

| 구분 | 설명 |
|------|------|
| 목적 | 전체를 n개 버킷으로 균등 분할 |
| 동일 값 처리 | 동일 값이라도 다른 버킷에 배치될 수 있음 |
| 반환값 범위 | 1 ~ n (버킷 번호) |
| 주요 용도 | 백분위수, 구간 분류 |

```text
-- NTILE: 4개 버킷으로 균등 분할
NTILE(4) OVER (ORDER BY value)

-- NTILE: 100개 버킷으로 백분위수 근사
NTILE(100) OVER (ORDER BY value)
```

> **주의**: 버킷 내에서 동일한 값을 가진 행들이 서로 다른 버킷에 나뉘어 배치될 수 있습니다.

<a id="partition-order"></a>
<a id="item-window-functions-over-partition-order"></a>

#### PARTITION BY / ORDER BY

`OVER` 절의 `PARTITION BY`와 `ORDER BY`는 윈도우 함수가 연산을 수행할 범위와 순서를 정의합니다. 두 절의 조합에 따라 윈도우 함수의 동작이 달라지므로 각각의 역할을 정확히 이해하는 것이 중요합니다.

##### PARTITION BY

`PARTITION BY`는 결과 집합을 논리적 그룹(파티션)으로 분할합니다. 윈도우 함수는 각 파티션 내에서 독립적으로 계산됩니다.

- `GROUP BY`와 유사하지만, **행을 축소하지 않고 모든 행을 유지**한 채로 그룹별 계산을 수행합니다.
- 여러 컬럼을 지정하면 해당 컬럼 조합으로 파티션이 나뉩니다.

```sql
-- sensor_id별로 파티션을 나누어 각 센서 내에서 버킷 번호 부여
SELECT
    sensor_id,
    time,
    value,
    NTILE(4) OVER (PARTITION BY sensor_id ORDER BY time) AS bucket_no
FROM sensor_data;
```

###### PARTITION BY 생략

`PARTITION BY`를 생략하면 전체 결과 집합이 하나의 윈도우가 됩니다.

```sql
-- 전체 결과를 하나의 파티션으로 처리
SELECT
    time,
    value,
    NTILE(10) OVER (ORDER BY value) AS decile
FROM sensor_data;
```

##### ORDER BY (OVER 절 내)

`OVER` 절 내의 `ORDER BY`는 윈도우 내에서 행의 처리 순서를 결정합니다. 일반 쿼리의 `ORDER BY`와는 별개이며, 최종 출력 순서에는 영향을 주지 않습니다.

- `LAG`, `LEAD`, `NTILE`처럼 순서에 의존하는 함수에서 사용합니다.
- `NTILE`도 버킷 할당 순서를 결정하기 위해 `ORDER BY`가 필요합니다.

```sql
-- OVER 내 ORDER BY: 윈도우 내 순서 결정
-- 쿼리 끝의 ORDER BY: 최종 출력 순서 결정
SELECT
    sensor_id,
    time,
    value,
    NTILE(4) OVER (PARTITION BY sensor_id ORDER BY time) AS bucket_no
FROM sensor_data
ORDER BY sensor_id, time;  -- 출력 순서
```

###### ORDER BY 생략

`LAG`/`LEAD`는 `ORDER BY` 없이 사용할 수 있지만, 행 순서가 명확하지 않으면 결과가
불확정적입니다. 시간 순서나 측정 순서를 기준으로 비교할 때는 `ORDER BY`를 명시합니다.

```sql
-- ORDER BY를 명시하지 않은 예: 입력/조회 순서에 의존하므로 권장하지 않음
SELECT
    sensor_id,
    time,
    value,
    LAG(value, 1) OVER (PARTITION BY sensor_id) AS prev_value
FROM sensor_data;
```

> `NTILE`은 버킷 할당 순서가 필요하므로 `ORDER BY`를 명시해야 합니다.

##### PARTITION BY와 ORDER BY의 조합

###### 둘 다 사용 (가장 일반적)

파티션별로 나누어 정렬된 순서로 계산합니다.

```sql
SELECT
    tag_name,
    time,
    value,
    LAG(value, 1) OVER (
        PARTITION BY tag_name
        ORDER BY time
    ) AS prev_value,
    NTILE(4) OVER (
        PARTITION BY tag_name
        ORDER BY value
    ) AS quartile
FROM tag_data
WHERE time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-02');
```

###### PARTITION BY만 사용

`LAG`/`LEAD`에서 `PARTITION BY`만 지정할 수 있지만, 순서가 명확하지 않아 권장하지 않습니다.

```sql
-- 권장하지 않음: 파티션 내 행 순서가 명확하지 않음
SELECT
    sensor_id,
    time,
    value,
    LAG(value, 1) OVER (PARTITION BY sensor_id) AS prev_value
FROM sensor_data
WHERE time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-02-01');
```

###### ORDER BY만 사용

전체 결과 집합에서 순서 기반 계산을 수행합니다.

```sql
-- 전체 데이터에서 값 기준 버킷 부여
SELECT
    time,
    sensor_id,
    value,
    NTILE(4) OVER (ORDER BY value) AS quartile
FROM sensor_data;
```

##### 실전 예시: 복합 파티션

여러 컬럼의 조합으로 파티션을 구성하는 예시입니다.

```sql
-- 장비(device_id)별로 이전 값 계산
SELECT
    plant_id,
    device_id,
    time,
    value,
    LAG(value, 1) OVER (
        PARTITION BY device_id
        ORDER BY time
    ) AS prev_value
FROM equipment_sensor
WHERE time BETWEEN TO_DATE('2024-06-01') AND TO_DATE('2024-07-01');
```

> **팁**: 하나의 `SELECT` 문에서 `OVER` 절이 동일한 윈도우 함수를 여러 번 사용할 경우,
> 동일한 `OVER` 정의를 반복해서 작성해야 합니다. 쿼리가 복잡해지면 서브쿼리나 Standard
> Edition의 CTE(Common Table Expression)로 분리하면 가독성이 높아집니다.

<a id="query-interpolation-series"></a>
<a id="item-query-interpolation-series"></a>

### SERIES BY와 보간

Machbase Neo는 시계열 데이터 분석에 특화된 두 가지 기능을 제공합니다. `SERIES BY`는 특정 조건을 만족하는 연속적인 행의 시퀀스를 식별하고, `INTERPOLATION` 힌트는 시간 간격 사이의 빠진 데이터를 채워 연속적인 시계열을 구성합니다.

#### SERIES BY

##### 개요

`SERIES BY`는 지정한 조건을 **연속적으로** 만족하는 행들의 묶음(시리즈)을 추출합니다. 조건이 중단되면 시리즈가 끊기고, 이후 다시 조건이 만족되면 새로운 시리즈가 시작됩니다.

##### 문법

```sql
SELECT [SERIESNUM(),] 컬럼, ...
FROM 테이블
WHERE 조건
SERIES BY 시리즈_조건;
```

- `SERIESNUM()`: 현재 행이 속한 시리즈 번호를 반환하는 함수입니다 (1부터 시작).
- `시리즈_조건`: 시리즈를 구성하는 컬럼 또는 표현식을 지정합니다.

##### 예시: 연속 고온 이벤트 탐지

온도가 80도 이상인 측정값이 **연속으로** 이어지는 구간을 시리즈로 식별합니다.

```sql
SELECT
    SERIESNUM() AS series_num,
    time,
    sensor_id,
    temperature
FROM temperature_log
WHERE temperature >= 80
SERIES BY sensor_id;
```

이 쿼리는 `sensor_id`가 동일하고 `temperature >= 80` 조건을 연속으로 만족하는 행들을 하나의 시리즈로 묶어 반환합니다.

##### 예시: 연속 알람 상태 구간 찾기

```sql
SELECT
    SERIESNUM() AS series_no,
    MIN(time)   AS series_start,
    MAX(time)   AS series_end,
    COUNT(*)    AS event_count
FROM (
    SELECT
        SERIESNUM() AS sn,
        time,
        alarm_flag
    FROM equipment_log
    WHERE alarm_flag = 1
    SERIES BY equipment_id
)
GROUP BY sn
ORDER BY series_no;
```

> **활용 팁**: `SERIES BY`는 알람 발생 구간, 특정 임계값 초과 구간, 장비 가동 상태 등 연속성이 중요한 분석에 적합합니다.

---

#### INTERPOLATION (보간)

##### 개요

실제 측정 데이터에는 네트워크 장애, 센서 오류 등으로 인해 특정 시간대의 데이터가 누락될 수 있습니다. `INTERPOLATION` 쿼리 힌트는 지정한 시간 간격 내에 데이터가 없는 구간을 수학적 방법으로 채워 연속적인 시계열 데이터를 반환합니다.

##### 힌트 문법

```sql
SELECT /*+ INTERPOLATION(컬럼 보간방법 간격) */
    time, 컬럼, ...
FROM 테이블
WHERE time BETWEEN 시작시간 AND 종료시간;
```

##### 보간 방법

| 방법 | 설명 |
|------|------|
| `LINEAR` | 앞뒤 값을 이용한 선형 보간. 값이 균일하게 변화한다고 가정할 때 사용 |
| `PREV` | 이전 유효 값으로 채움(전방 채움, Forward Fill). 상태값이나 마지막 측정값을 유지할 때 사용 |
| `NULL` | 누락된 구간을 `NULL`로 채움 |

##### 예시: 1분 간격 선형 보간

센서 데이터에서 1분(60,000,000,000 나노초) 간격으로 빠진 값을 선형 보간으로 채웁니다.

```sql
SELECT /*+ INTERPOLATION(value LINEAR 60000000000) */
    time,
    sensor_id,
    value
FROM sensor_data
WHERE time BETWEEN TO_DATE('2024-01-01 00:00:00') AND TO_DATE('2024-01-01 01:00:00')
  AND sensor_id = 'TEMP_001';
```

> **시간 단위**: Machbase의 시간 간격은 나노초(ns) 단위입니다. 자주 사용하는 단위 변환은 다음을 참고하십시오.
> - 1초 = 1,000,000,000 ns
> - 1분 = 60,000,000,000 ns
> - 1시간 = 3,600,000,000,000 ns

##### 예시: 이전 값으로 채우기 (PREV)

상태 코드처럼 마지막 상태를 유지해야 하는 경우에 사용합니다.

```sql
SELECT /*+ INTERPOLATION(status_code PREV 60000000000) */
    time,
    device_id,
    status_code
FROM device_status
WHERE time BETWEEN TO_DATE('2024-06-01 00:00:00') AND TO_DATE('2024-06-01 06:00:00')
  AND device_id = 'DEVICE_A';
```

##### 예시: TAG 테이블에서 보간

TAG 테이블과 함께 `INTERPOLATION`을 사용할 때는 시간 범위 조건(`BETWEEN`)과 태그 이름 조건을 함께 지정합니다.

```sql
SELECT /*+ INTERPOLATION(value LINEAR 300000000000) */
    time,
    name,
    value
FROM tag
WHERE name = 'plant1.sensor.temp'
  AND time BETWEEN TO_DATE('2024-01-01 00:00:00') AND TO_DATE('2024-01-02 00:00:00');
```

> **주의**: `INTERPOLATION` 힌트는 시간 범위 조건이 명시된 쿼리에서 동작합니다. 시간 범위 없이 사용하면 전체 데이터를 대상으로 하여 성능에 영향을 줄 수 있습니다.

---

#### SERIES BY와 INTERPOLATION 비교

| 구분 | SERIES BY | INTERPOLATION |
|------|-----------|---------------|
| 목적 | 연속 조건을 만족하는 행 그룹 식별 | 누락된 시간대 데이터 채우기 |
| 동작 방식 | 조건 불만족 시 시리즈 분리 | 지정 간격마다 가상의 행 생성 |
| 출력 행 수 | 원본 행 수와 동일 또는 이하 | 원본보다 많을 수 있음 (보간 행 추가) |
| 주요 용도 | 이벤트 구간 분석, 연속 상태 감지 | 시계열 시각화, 균일 간격 데이터 필요 시 |

<a id="condition-conditional-search"></a>

## 조건 검색

Machbase는 일반 비교 연산자 외에 텍스트 검색, 정규식, JSON 경로, 네트워크 타입 연산자 등 다양한 조건 검색 기능을 제공합니다.

### 이 절에서 다루는 내용

- **[텍스트 검색](/dbms/log-table-usage/text-search-keyword-index/#text-search)**: SEARCH, ESEARCH, NOT SEARCH
- **[정규식 검색](/dbms/log-table-usage/regex-network-query/#regex)**: REGEXP, NOT REGEXP, REGEXP_LIKE
- **[네트워크 데이터 타입](/dbms/log-table-usage/regex-network-query/#type-network-data-types-operators)**: IPV4/IPV6 조건 검색
- **[JSON 조회와 JSON path](/dbms/performance-tuning/query-analysis/#query-json-path)**: JSON 컬럼 필드 접근
- **[TAG 메타데이터 조회](/dbms/tag-table-usage/tag-metadata/#metadata-query-tag)**: FROM TAG METADATA 활용

<a id="query-json-path"></a>
<a id="condition-conditional-search-query-json-path"></a>

### JSON 컬럼 조회

Machbase의 JSON 컬럼은 구조가 유동적인 데이터를 저장할 때 사용합니다. TAG 테이블의 `value` 컬럼이나 별도로 정의한 JSON 타입 컬럼에 임의의 JSON 객체를 저장하고 JSONPath 문법으로 개별 필드에 접근할 수 있습니다.

#### 이 절에서 다루는 내용

- **[LOOKUP JSON 조건 조회](/dbms/lookup-table-usage/json-column-query/#condition-query-lookup-json)**: LOOKUP 테이블 JSON 컬럼의 path 조건 조회와 주의사항

#### JSON 컬럼 접근 방법

Machbase는 두 가지 JSONPath 접근 문법을 지원합니다.

##### 화살표 연산자 (`->`)

```text
column->'$.path'
```

##### 점 표기법 (dot shorthand)

```text
column.path
```

두 문법은 동일한 결과를 반환합니다.

#### 기본 조회 예시

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

#### 중첩 필드 접근

```sql
-- 중첩 객체 접근
SELECT name, value->'$.location.building' AS building
FROM tag
WHERE ts >= NOW - 3600000000000;

-- 중첩 예: {"device": {"id": "A1", "type": "temp"}}
SELECT name, value->'$.device.id' AS device_id
FROM tag_json;
```

#### 배열 인덱스 접근

```sql
-- 배열의 첫 번째 요소 접근 (0-based)
SELECT name, value->'$.readings[0]' AS first_reading
FROM tag_json;

-- 배열의 두 번째 요소
SELECT name, value->'$.readings[1]' AS second_reading
FROM tag_json;
```

#### 조건 필터링

##### 동등 비교

```sql
SELECT * FROM tag
WHERE value->'$.status' = 'active';
```

##### 숫자 범위 비교

```sql
SELECT name, value->'$.temperature' AS temp
FROM tag
WHERE value->'$.temperature' > 80.0
  AND ts >= NOW - 3600000000000;
```

##### ISNULL / IS NOT NULL

```sql
-- JSON 필드가 없거나 null인 행 조회
SELECT * FROM tag
WHERE value->'$.error_code' IS NOT NULL;

-- JSON 필드가 존재하는 행만 조회
SELECT name, value->'$.unit'
FROM tag
WHERE value->'$.unit' IS NOT NULL;
```

##### LIKE 패턴 매칭

```sql
-- JSON 문자열 필드에 LIKE 적용
SELECT name, value->'$.location'
FROM tag
WHERE value->'$.location' LIKE 'factory%';
```

#### JSON SUMMARIZED 컬럼

TAG 테이블에서 JSON 컬럼에 대한 롤업(rollup) 집계를 지원하려면 `SUMMARIZED` 옵션을 사용합니다.

```sql
CREATE TAG TABLE tag_json (
    name    VARCHAR(80) PRIMARY KEY,
    time    DATETIME BASETIME,
    value   JSON SUMMARIZED
);
```

`SUMMARIZED`로 선언된 JSON 컬럼은 숫자 필드에 대해 `ROLLUP` 함수와 함께 집계 최적화가 적용됩니다.

#### 성능 주의사항

> JSON 필드 조건은 인덱스를 사용하지 않습니다. `name`(기본키)과 `time`(BASETIME) 조건을 함께 지정하여 스캔 범위를 최소화하십시오.

```sql
-- 권장 패턴: name과 시간 조건으로 범위 축소 후 JSON 필드 필터링
SELECT name, value->'$.temperature' AS temp
FROM tag
WHERE name = 'sensor1'                          -- 기본키 인덱스 활용
  AND ts BETWEEN '2024-01-01' AND '2024-01-02'  -- 시간 인덱스 활용
  AND value->'$.temperature' > 50.0;            -- JSON 필드 필터
```
