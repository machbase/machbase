---
title: '6.11 ROLLUP 성능 튜닝'
weight: 110
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

### 조회 문법 정본

`rollup()` signature, 지원 단위, origin과 후보 선택은
[ROLLUP 조회 문법](../query-syntax-rollup/)을 정본으로 사용합니다. 이 페이지에서는 같은 query의
원시 GROUP BY와 ROLLUP 실행 시간만 비교합니다.

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

### ROLLUP_TABLE hint

특정 후보를 강제해야 할 때만 `ROLLUP_TABLE` hint를 사용합니다. 정확한 형식과 자동 선택은
[ROLLUP 조회 문법](../query-syntax-rollup/)을 참고합니다.

### 운영 상태와 즉시 집계

WAKEUP interval, START/STOP/FORCE, `V`과 `SHOW ROLLUPGAP`은
[ROLLUP 제어와 상태 확인](../ingestion-control-rollup/)에서 다룹니다. 성능 변경 전후에는 gap이
0인 같은 상태에서 query를 비교합니다.

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
