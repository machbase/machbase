---
type: docs
title: 'ROLLUP 활용 튜닝'
weight: 60
---

ROLLUP은 시계열 집계 쿼리의 성능을 획기적으로 향상시키는 Machbase 고유의 기능입니다. 수백만~수억 건의 원시 데이터를 매번 스캔하는 대신, 백그라운드에서 미리 계산된 집계값을 사용해 응답 시간을 수십~수백 배 단축할 수 있습니다.

## ROLLUP 없을 때의 집계 성능

ROLLUP 없이 1개월치 원시 데이터를 시간 단위로 집계하는 경우를 생각해 보겠습니다.

```sql
-- ROLLUP 미사용: 수천만 건을 직접 스캔하여 GROUP BY 집계
SELECT DATE_TRUNC('hour', time) AS hour_bucket,
       AVG(value)               AS avg_val,
       MAX(value)               AS max_val,
       MIN(value)               AS min_val
FROM   sensor_tag
WHERE  name = 'TEMP-01'
  AND  time BETWEEN '2025-06-01' AND '2025-07-01'
GROUP BY hour_bucket
ORDER BY hour_bucket;
-- 수천만 건 스캔 → 수 초~수십 초 소요
```

동일한 결과를 ROLLUP을 활용하면 미리 집계된 값만 읽으므로 훨씬 빠릅니다.

```sql
-- ROLLUP 활용: 사전 집계된 1시간 단위 결과를 직접 조회
SELECT rollup('hour', 1, time) AS hour_bucket,
       AVG(value)              AS avg_val,
       MAX(value)              AS max_val,
       MIN(value)              AS min_val
FROM   sensor_tag
WHERE  name = 'TEMP-01'
  AND  time BETWEEN '2025-06-01' AND '2025-07-01'
GROUP BY hour_bucket
ORDER BY hour_bucket;
-- 수십~수백 배 빠름
```

## rollup() 함수로 사전 집계 결과 조회

`rollup()` 함수는 지정한 시간 단위에 해당하는 ROLLUP 테이블을 자동으로 선택해 집계 결과를 반환합니다.

```sql
rollup('단위', 배수, 시간컬럼)
```

| 단위 | 약어 | 설명 |
|------|------|------|
| `sec` | `s` | 초 단위 |
| `min` | `m` | 분 단위 |
| `hour` | `h` | 시간 단위 |
| `day` | `d` | 일 단위 |
| `week` | `w` | 주 단위 |
| `month` | `M` | 월 단위 |
| `year` | `y` | 연 단위 |

```sql
-- 1분 단위 집계 (1분 ROLLUP 활용)
SELECT rollup('min', 1, time)  AS bucket, AVG(value) AS avg_val
FROM   sensor_tag
WHERE  name = 'SENSOR-01'
  AND  time BETWEEN '2025-06-01 00:00:00' AND '2025-06-01 06:00:00'
GROUP BY bucket ORDER BY bucket;

-- 5분 단위 집계 (1분 ROLLUP을 5개 합산)
SELECT rollup('min', 5, time)  AS bucket, AVG(value) AS avg_val
FROM   sensor_tag
WHERE  name = 'SENSOR-01'
  AND  time BETWEEN '2025-06-01 00:00:00' AND '2025-06-01 06:00:00'
GROUP BY bucket ORDER BY bucket;

-- 1시간 단위 집계 (1시간 ROLLUP 활용)
SELECT rollup('hour', 1, time) AS bucket, AVG(value) AS avg_val
FROM   sensor_tag
WHERE  name = 'SENSOR-01'
  AND  time BETWEEN '2025-06-01' AND '2025-07-01'
GROUP BY bucket ORDER BY bucket;
```

## 적절한 ROLLUP 계층 설계

ROLLUP은 계층 구조로 설계합니다. 하위 ROLLUP이 상위 ROLLUP의 소스가 되어 처리 부하를 분산합니다.

```
원시 데이터 (초 단위)
  └── 1초 ROLLUP  (_tag_ru_1s)
        └── 1분 ROLLUP  (_tag_ru_1m)
              └── 1시간 ROLLUP (_tag_ru_1h)
```

```sql
-- 계층 ROLLUP 생성 예시
-- 1. 1초 단위 집계 (원시 데이터 → 1초 버킷)
CREATE ROLLUP _tag_ru_1s ON sensor_tag(value) INTERVAL 1 SEC;

-- 2. 1분 단위 집계 (1초 ROLLUP → 1분 버킷)
CREATE ROLLUP _tag_ru_1m ON _tag_ru_1s(value) INTERVAL 1 MIN;

-- 3. 1시간 단위 집계 (1분 ROLLUP → 1시간 버킷)
CREATE ROLLUP _tag_ru_1h ON _tag_ru_1m(value) INTERVAL 1 HOUR;
```

**계층 설계 기준:**

| 조회 주기 | 권장 ROLLUP | 예상 결과 건수 (1개월) |
|-----------|------------|----------------------|
| 초 단위 | 1초 ROLLUP | ~2,592,000 건 |
| 분 단위 | 1분 ROLLUP | ~43,200 건 |
| 시간 단위 | 1시간 ROLLUP | ~720 건 |
| 일 단위 | 1시간 또는 1일 ROLLUP | ~30 건 |

자주 조회하는 시간 단위에 대응하는 ROLLUP을 미리 준비해 두면 대시보드와 리포트 응답 시간을 안정적으로 유지할 수 있습니다.

## ROLLUP_TABLE 힌트로 특정 테이블 강제 지정

동일한 컬럼에 대해 여러 ROLLUP이 있을 때, 옵티마이저가 선택한 ROLLUP이 최적이 아닌 경우 `ROLLUP_TABLE` 힌트로 직접 지정합니다.

```sql
-- 조건 ROLLUP(_tag_ru_cond_1m)을 강제 선택
SELECT /*+ ROLLUP_TABLE(_tag_ru_cond_1m) */
       rollup('min', 1, time) AS bucket,
       AVG(value)
FROM   sensor_tag
WHERE  name = 'SENSOR-01'
  AND  time BETWEEN '2025-06-01 00:00:00' AND '2025-06-01 01:00:00'
GROUP BY bucket
ORDER BY bucket;
```

`FIRST()` 또는 `LAST()` 함수를 사용하는 경우, EXTENSION ROLLUP 테이블을 힌트로 지정해야 합니다.

```sql
-- EXTENSION ROLLUP 강제 지정 (FIRST/LAST 사용 시)
SELECT /*+ ROLLUP_TABLE(_tag_ru_1m_ext) */
       rollup('min', 1, time) AS bucket,
       FIRST(time, value)     AS first_val,
       LAST(time, value)      AS last_val
FROM   sensor_tag
WHERE  name = 'SENSOR-01'
  AND  time BETWEEN '2025-06-01 00:00:00' AND '2025-06-01 01:00:00'
GROUP BY bucket
ORDER BY bucket;
```

## WAKEUP INTERVAL 조정

ROLLUP 스레드가 새 데이터를 확인하는 주기(WAKEUP INTERVAL)를 조정해 실시간성과 시스템 부하 사이의 균형을 맞춥니다.

**기본 동작:** WAKEUP INTERVAL = ROLLUP INTERVAL (집계 주기와 동일)

```sql
-- 현재 ROLLUP 상태 확인
SELECT ROLLUP_TABLE, INTERVAL_TIME, WAKEUP_INTERVAL, LAST_ELAPSED_MSEC, RUN_STATE
FROM   V$ROLLUP
ORDER BY ROLLUP_TABLE;
```

### 실시간성이 중요한 경우

WAKEUP INTERVAL을 짧게 설정하면 새 데이터가 빨리 집계됩니다. CPU 사용량이 소폭 증가합니다.

```sql
-- 1분 ROLLUP을 10초마다 깨우기 (실시간성 향상)
ALTER ROLLUP _tag_ru_1m SET WAKEUP INTERVAL 10 SEC;

-- 1시간 ROLLUP을 5분마다 깨우기
ALTER ROLLUP _tag_ru_1h SET WAKEUP INTERVAL 5 MIN;
```

규칙: WAKEUP INTERVAL은 ROLLUP INTERVAL의 약수(정수 배)여야 합니다.

### 입력 부하가 클 때

WAKEUP INTERVAL을 길게 설정하면 집계 작업이 덜 자주 실행되어 입력 처리 성능을 보호합니다.

```sql
-- 부하가 큰 상황: wakeup 주기를 ROLLUP 주기와 동일하게 유지 (기본값)
ALTER ROLLUP _tag_ru_1s SET WAKEUP INTERVAL 1 SEC;  -- 1초 ROLLUP = 1초마다 wakeup
```

### 처리 지연(Gap) 모니터링

```sql
-- 집계 지연 상태 확인
Mach> SHOW ROLLUPGAP;

-- 집계 소요 시간이 wakeup 주기에 근접하거나 초과하면 주기 재검토 필요
SELECT ROLLUP_TABLE, LAST_ELAPSED_MSEC, WAKEUP_INTERVAL
FROM   V$ROLLUP
WHERE  LAST_ELAPSED_MSEC > WAKEUP_INTERVAL * 0.8;  -- 80% 이상 사용 시 경고
```

## 대량 데이터 로드 후 즉시 집계

machloader나 Append API로 대량 데이터를 적재한 직후에는 ROLLUP이 아직 처리하지 못한 데이터가 많습니다. FORCE 명령으로 즉시 집계를 완료합니다.

```sql
-- 하위 ROLLUP부터 순서대로 강제 집계 (블로킹: 완료까지 대기)
ALTER ROLLUP _tag_ru_1s FORCE;
ALTER ROLLUP _tag_ru_1m FORCE;
ALTER ROLLUP _tag_ru_1h FORCE;

-- 비블로킹 방식 (집계 트리거 후 즉시 반환)
ALTER ROLLUP _tag_ru_1s WAKEUP;
```

## ROLLUP 조회 vs GROUP BY 성능 비교

| 방식 | 스캔 대상 | 1개월 기준 예상 응답 시간 |
|------|-----------|--------------------------|
| 원시 데이터 GROUP BY | 수천만 건 원시 레코드 | 수 초 ~ 수십 초 |
| 1분 ROLLUP 조회 | ~43,200 건 집계 레코드 | 밀리초 수준 |
| 1시간 ROLLUP 조회 | ~720 건 집계 레코드 | 밀리초 이하 |

ROLLUP이 준비된 시간 단위로 쿼리를 작성하면 대시보드와 리포트의 응답 시간을 밀리초 수준으로 유지할 수 있습니다.

## 관련 페이지

- [ROLLUP 개념과 생성](../../../query-analysis-automation/item/rollup/) — ROLLUP 생성, 계층 설계 전반
- [SELECT 힌트 사용](../../../query-analysis-automation/query-select/hint-select/) — ROLLUP_TABLE 힌트 상세
