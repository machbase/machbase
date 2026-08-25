---
title: '6.17 ROLLUP 성능 튜닝'
weight: 160
toc: true
---

<a id="tuning-rollup"></a>

## ROLLUP 활용 튜닝

ROLLUP은 백그라운드에서 미리 계산한 집계값을 사용하여 반복 집계 시 원시 데이터 스캔 범위를
줄입니다. 개선 폭은 원시 데이터 양, 조회 기간, 집계 간격과 스토리지 성능에 따라 달라집니다.

### ROLLUP 없을 때의 집계 성능

ROLLUP 없이 1개월치 원시 데이터를 시간 단위로 집계하는 경우입니다.

```sql
-- ROLLUP 미사용: 조회 기간의 원시 데이터를 직접 GROUP BY 집계
SELECT DATE_TRUNC('hour', time) AS hour_bucket,
       AVG(value)               AS avg_val,
       MAX(value)               AS max_val,
       MIN(value)               AS min_val
FROM   sensor_tag
WHERE  name = 'TEMP-01'
  AND  time BETWEEN '2025-06-01' AND '2025-07-01'
GROUP BY hour_bucket
ORDER BY hour_bucket;
-- 실행 계획과 응답 시간을 기준값으로 기록
```

ROLLUP을 활용하면 미리 집계된 값만 읽으므로 훨씬 빠릅니다.

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
-- 같은 조건으로 실행 계획, 스캔 행 수와 응답 시간을 비교
```

### rollup() 함수로 사전 집계 결과 조회

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

### 적절한 ROLLUP 계층 설계

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
CREATE ROLLUP _tag_ru_1m FROM _tag_ru_1s INTERVAL 1 MIN;

-- 3. 1시간 단위 집계 (1분 ROLLUP → 1시간 버킷)
CREATE ROLLUP _tag_ru_1h FROM _tag_ru_1m INTERVAL 1 HOUR;
```

**계층 설계 기준:**

| 조회 주기 | 권장 ROLLUP | 예상 결과 건수 (1개월) |
|-----------|------------|----------------------|
| 초 단위 | 1초 ROLLUP | ~2,592,000 건 |
| 분 단위 | 1분 ROLLUP | ~43,200 건 |
| 시간 단위 | 1시간 ROLLUP | ~720 건 |
| 일 단위 | 1시간 ROLLUP을 조회 시 `rollup('day', 1, ...)`로 재집계하거나 24시간 간격 ROLLUP 사용 | ~30 건 |

자주 조회하는 시간 단위에 맞는 ROLLUP을 준비해 두면 대시보드와 리포트 응답 시간을 안정적으로 유지할 수 있습니다.

### ROLLUP_TABLE 힌트로 특정 테이블 강제 지정

동일한 컬럼에 여러 ROLLUP이 있을 때 옵티마이저 선택이 최적이 아니면 `ROLLUP_TABLE` 힌트로 직접 지정합니다.

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

### WAKEUP INTERVAL 조정

ROLLUP 스레드가 새 데이터를 확인하는 주기(WAKEUP INTERVAL)를 조정해 실시간성과 시스템 부하 사이의 균형을 맞춥니다.

**기본 동작:** WAKEUP INTERVAL = ROLLUP INTERVAL (집계 주기와 동일)

```sql
-- 현재 ROLLUP 상태 확인
SELECT ROLLUP_TABLE, INTERVAL_TIME, WAKEUP_INTERVAL, LAST_ELAPSED_MSEC, RUN_STATE
FROM   V$ROLLUP
ORDER BY ROLLUP_TABLE;
```

#### 실시간성이 중요한 경우

WAKEUP INTERVAL을 짧게 설정하면 새 데이터가 빨리 집계됩니다. CPU 사용량이 소폭 증가합니다.

```sql
-- 1분 ROLLUP을 10초마다 깨우기 (실시간성 향상)
ALTER ROLLUP _tag_ru_1m SET WAKEUP INTERVAL 10 SEC;

-- 1시간 ROLLUP을 5분마다 깨우기
ALTER ROLLUP _tag_ru_1h SET WAKEUP INTERVAL 5 MIN;
```

규칙: WAKEUP INTERVAL은 ROLLUP INTERVAL의 약수(정수 배)여야 합니다.

#### 입력 부하가 클 때

WAKEUP INTERVAL을 길게 설정하면 집계 작업이 덜 자주 실행되어 입력 처리 성능을 보호합니다.

```sql
-- 부하가 큰 상황: wakeup 주기를 ROLLUP 주기와 동일하게 유지 (기본값)
ALTER ROLLUP _tag_ru_1s SET WAKEUP INTERVAL 1 SEC;  -- 1초 ROLLUP = 1초마다 wakeup
```

#### 처리 지연(Gap) 모니터링

```sql
-- 집계 지연 상태 확인
Mach> SHOW ROLLUPGAP;

-- 집계 소요 시간이 wakeup 주기에 근접하거나 초과하면 주기 재검토 필요
SELECT ROLLUP_TABLE, LAST_ELAPSED_MSEC, WAKEUP_INTERVAL
FROM   V$ROLLUP
WHERE  LAST_ELAPSED_MSEC > WAKEUP_INTERVAL * 0.8;  -- 80% 이상 사용 시 경고
```

### 대량 데이터 로드 후 즉시 집계

machloader나 Append API로 대량 데이터를 적재한 직후에는 아직 집계되지 않은 데이터가 많습니다. FORCE 명령으로 즉시 집계합니다.

```sql
-- 하위 ROLLUP부터 순서대로 강제 집계 (블로킹: 완료까지 대기)
ALTER ROLLUP _tag_ru_1s FORCE;
ALTER ROLLUP _tag_ru_1m FORCE;
ALTER ROLLUP _tag_ru_1h FORCE;

-- 비블로킹 방식 (집계 트리거 후 즉시 반환)
ALTER ROLLUP _tag_ru_1s WAKEUP;
```

### ROLLUP 조회와 원시 GROUP BY 비교

| 방식 | 주요 처리 대상 | 확인 항목 |
|------|---------------|-----------|
| 원시 데이터 GROUP BY | 조회 기간의 원시 레코드 | 원시 스캔 행 수, 집계 시간 |
| 1분 ROLLUP 조회 | 분 단위 사전 집계 레코드 | 선택한 ROLLUP, 후속 재집계 행 수 |
| 1시간 ROLLUP 조회 | 시간 단위 사전 집계 레코드 | 조회 간격 적합성, 응답 시간 |

동일한 태그, 기간과 집계 함수를 사용해 원시 쿼리와 ROLLUP 쿼리의 실행 계획과 응답 시간을
비교합니다. 운영 목표를 충족하는 가장 거친 ROLLUP 간격을 선택하면 읽는 집계 레코드를 줄일 수
있습니다.

### 관련 페이지

- [ROLLUP 개념과 생성](/dbms/tag-rollup-usage/overview-use-criteria/#rollup) — ROLLUP 생성, 계층 설계 전반
- [SELECT hint syntax](/dbms/reference/sql/syntax-dictionary-sql/select-hint-syntax/) — ROLLUP_TABLE 힌트 상세
